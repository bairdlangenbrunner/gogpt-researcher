"""
Keep one local copy of the newest EIA-860M monthly generator inventory.

    python eia860m.py              # print the path of the newest local file (fetching if none)
    python eia860m.py --check      # look at eia.gov now for a newer release and download it
    python eia860m.py --path       # path only, no network, for other scripts and the sweep prompt

Where: <repo>/work/eia/<month>_generator<year>.xlsx plus work/eia/latest.json
({file, url, release_date, next_release, checked}). EIA releases the file about
once a month (the page states the next release date), so the page is checked
at most once every 7 days unless --check is given; a batch start therefore
costs one small page read, and the 14 MB download happens only when the month
has changed. Earlier months are kept (the sweep cites a dated file).

Library use:
    from eia860m import ensure_latest, load_generators
    path, meta = ensure_latest()            # obeys the 7-day check cadence
    gens = load_generators(path)            # pandas DataFrame, all four sheets, with a "sheet" column
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.request
from pathlib import Path

from paths import work_dir

PAGE = "https://www.eia.gov/electricity/data/eia860m/"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august",
          "september", "october", "november", "december"]
SHEETS = ["Operating", "Planned", "Retired", "Canceled or Postponed"]
CHECK_EVERY_DAYS = 7


def eia_dir():
    d = work_dir() / "eia"
    d.mkdir(parents=True, exist_ok=True)
    return d


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    # EIA answers a not-yet-released month with a 301 to an HTML landing page;
    # following it would "download" that page as the spreadsheet.
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_opener = urllib.request.build_opener(_NoRedirect)


def _get(url, head=False, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept-Language": "en-US,en;q=0.9"},
                                 method="HEAD" if head else "GET")
    return _opener.open(req, timeout=timeout)


def _is_xlsx(resp):
    ctype = resp.headers.get("Content-Type", "")
    return resp.status == 200 and ("spreadsheet" in ctype or "officedocument" in ctype
                                   or "octet-stream" in ctype)


def _month_key(fname):
    m = re.match(r"([a-z]+)_generator(\d{4})\.xlsx$", fname)
    if not m or m.group(1) not in MONTHS:
        return None
    return (int(m.group(2)), MONTHS.index(m.group(1)) + 1)


def page_candidates():
    """The current (non-archive) file links on the EIA page, newest first, with the
    release dates the page states. EIA lists upcoming months before the files exist,
    so callers must HEAD each candidate until one answers 200."""
    html = _get(PAGE).read().decode("utf-8", "replace")
    links = sorted({m.group(1) for m in
                    re.finditer(r'href="(/electricity/data/eia860m/xls/[a-z]+_generator\d{4}\.xlsx)"',
                                html)}, key=lambda u: _month_key(u.rsplit("/", 1)[1]) or (0, 0),
                   reverse=True)
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text)
    rel = re.search(r"Release Date:\s*([A-Z][a-z]+ \d{1,2}, \d{4})", text)
    nxt = re.search(r"Next Release Date:\s*([A-Z][a-z]+ \d{1,2}, \d{4})", text)
    return (["https://www.eia.gov" + u for u in links],
            rel.group(1) if rel else "", nxt.group(1) if nxt else "")


def local_files():
    return sorted((p for p in eia_dir().glob("*_generator*.xlsx") if _month_key(p.name)),
                  key=lambda p: _month_key(p.name), reverse=True)


def read_meta():
    p = eia_dir() / "latest.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def write_meta(meta):
    (eia_dir() / "latest.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")


def check_now(verbose=True):
    """Look at eia.gov; download the newest real file if it is not local. Returns (path, meta)."""
    urls, release, nxt = page_candidates()
    chosen = None
    for u in urls:
        try:
            with _get(u, head=True) as r:
                if _is_xlsx(r):
                    chosen = u
                    break
        except Exception:
            continue
    if not chosen:
        sys.exit("ERROR: no EIA-860M file on the page answered with a spreadsheet; "
                 "try again later")
    fname = chosen.rsplit("/", 1)[1]
    dest = eia_dir() / fname
    if not dest.exists():
        if verbose:
            print(f"downloading {chosen} ...")
        tmp = dest.with_suffix(".part")
        with _get(chosen) as r, open(tmp, "wb") as f:
            if not _is_xlsx(r):
                sys.exit(f"ERROR: {chosen} did not return a spreadsheet")
            while True:
                chunk = r.read(1 << 20)
                if not chunk:
                    break
                f.write(chunk)
        tmp.rename(dest)
    meta = {"file": fname, "url": chosen, "release_date": release, "next_release": nxt,
            "checked": dt.date.today().isoformat()}
    write_meta(meta)
    return dest, meta


def ensure_latest(force=False, verbose=True):
    """The newest local file, checking eia.gov when the last check is older than
    CHECK_EVERY_DAYS (or there is no local file, or force)."""
    meta = read_meta()
    files = local_files()
    stale = True
    if meta.get("checked") and files:
        try:
            age = (dt.date.today() - dt.date.fromisoformat(meta["checked"])).days
            stale = age >= CHECK_EVERY_DAYS
        except ValueError:
            stale = True
    if force or stale or not files:
        try:
            return check_now(verbose=verbose)
        except SystemExit:
            raise
        except Exception as e:
            if not files:
                sys.exit(f"ERROR: could not reach {PAGE} and no local EIA-860M file: {e}")
            if verbose:
                print(f"WARNING: eia.gov check failed ({e}); using local {files[0].name}")
    return files[0], meta


def load_generators(path, sheets=SHEETS):
    """All four generator sheets as one DataFrame (header row 3), plus a `sheet`
    column. Plant ID and Generator ID are strings."""
    import pandas as pd
    frames = []
    for s in sheets:
        df = pd.read_excel(path, sheet_name=s, header=2, dtype={"Plant ID": str,
                                                                "Generator ID": str,
                                                                "Unit Code": str})
        df["sheet"] = s
        frames.append(df)
    out = pd.concat(frames, ignore_index=True)
    out["Plant ID"] = out["Plant ID"].astype(str).str.replace(r"\.0$", "", regex=True).str.strip()
    out["Generator ID"] = out["Generator ID"].astype(str).str.strip()
    out = out[out["Plant ID"].str.match(r"^\d+$")]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true", help="check eia.gov now")
    ap.add_argument("--path", action="store_true", help="newest local path only, no network")
    a = ap.parse_args()
    if a.path:
        files = local_files()
        if not files:
            sys.exit("ERROR: no local EIA-860M file; run eia860m.py without --path")
        print(files[0])
        return
    path, meta = ensure_latest(force=a.check)
    print(path)
    if meta:
        print(f"release: {meta.get('release_date') or '?'}  next release: "
              f"{meta.get('next_release') or '?'}  checked: {meta.get('checked')}")


if __name__ == "__main__":
    main()

"""
Keep one local copy of the newest annual EIA-860 zip and read its Plant table.

    python eia860.py              # print the path of the newest local zip (fetching if none)
    python eia860.py --check      # look at eia.gov now for a newer release and download it
    python eia860.py --path       # path only, no network, for other scripts

Where: <repo>/work/eia/eia860<year>.zip plus work/eia/latest_860.json
({file, url, year, checked}). The annual page lists xls/eia860<YYYY>.zip and
sometimes xls/eia860<YYYY>ER.zip (early release). The newest year wins and the
final release beats the early release of the same year. The page is checked at
most once every 7 days unless --check is given. The zip is always saved as
eia860<year>.zip.

The Plant table (member 2___Plant_Y<YYYY>.xlsx, header on the second row) carries
a street address, county and coordinates for each EIA plant code, which the
location step (location_candidates.py) uses as a dataset point.

Library use:
    from eia860 import ensure_latest, load_plants, plant_index
    path, meta = ensure_latest()
    idx = plant_index(load_plants(path))      # {plant_code: {name, address, city, state, zip, county, lat, lon, utility}}
"""
from __future__ import annotations

import argparse
import datetime as dt
import io
import json
import re
import sys
import zipfile

from eia860m import UA, _get, eia_dir  # same user agent, no-redirect opener and work/eia dir

PAGE = "https://www.eia.gov/electricity/data/eia860/"
CHECK_EVERY_DAYS = 7
META_NAME = "latest_860.json"
LINK_RE = re.compile(r'href="([^"]*?/xls/eia860(\d{4})(ER)?\.zip)"', re.I)


def candidate_links(html):
    """Zip links on the page as [(year, early_release, absolute_url)], best first:
    newest year, and the final release before the early release of the same year."""
    seen, out = set(), []
    for m in LINK_RE.finditer(html):
        href, year, er = m.group(1), int(m.group(2)), bool(m.group(3))
        if href.startswith("http"):
            url = href
        elif href.startswith("/"):
            url = "https://www.eia.gov" + href
        else:
            url = PAGE.rstrip("/") + "/" + href.lstrip("./")
        if (url, er) in seen:
            continue
        seen.add((url, er))
        out.append((year, er, url))
    out.sort(key=lambda t: (t[0], not t[1]), reverse=True)
    return out


def _is_zip(resp):
    ctype = resp.headers.get("Content-Type", "").lower()
    return resp.status == 200 and ("zip" in ctype or "octet-stream" in ctype)


def local_files():
    def year(p):
        m = re.match(r"eia860(\d{4})\.zip$", p.name)
        return int(m.group(1)) if m else None
    return sorted((p for p in eia_dir().glob("eia860*.zip") if year(p)), key=year, reverse=True)


def read_meta():
    p = eia_dir() / META_NAME
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def write_meta(meta):
    (eia_dir() / META_NAME).write_text(json.dumps(meta, indent=2), encoding="utf-8")


def check_now(verbose=True):
    """Look at eia.gov; download the newest real zip if it is not local. Returns (path, meta)."""
    html = _get(PAGE).read().decode("utf-8", "replace")
    chosen = None
    for year, er, url in candidate_links(html):
        try:
            with _get(url, head=True) as r:
                if _is_zip(r):
                    chosen = (year, er, url)
                    break
        except Exception:
            continue
    if not chosen:
        sys.exit("ERROR: no EIA-860 zip on the page answered with a zip file; try again later")
    year, er, url = chosen
    dest = eia_dir() / f"eia860{year}.zip"
    if not dest.exists():
        if verbose:
            print(f"downloading {url} ...")
        tmp = dest.with_suffix(".part")
        with _get(url) as r, open(tmp, "wb") as f:
            if not _is_zip(r):
                sys.exit(f"ERROR: {url} did not return a zip file")
            while True:
                chunk = r.read(1 << 20)
                if not chunk:
                    break
                f.write(chunk)
        tmp.rename(dest)
    meta = {"file": dest.name, "url": url, "year": year, "early_release": er,
            "checked": dt.date.today().isoformat()}
    write_meta(meta)
    return dest, meta


def ensure_latest(force=False, verbose=True):
    """The newest local zip, checking eia.gov when the last check is older than
    CHECK_EVERY_DAYS (or there is no local file, or force). Returns (zip_path, meta)."""
    meta = read_meta()
    files = local_files()
    stale = True
    if meta.get("checked") and files:
        try:
            stale = (dt.date.today() - dt.date.fromisoformat(meta["checked"])).days >= CHECK_EVERY_DAYS
        except ValueError:
            stale = True
    if force or stale or not files:
        try:
            return check_now(verbose=verbose)
        except SystemExit:
            raise
        except Exception as e:
            if not files:
                sys.exit(f"ERROR: could not reach {PAGE} and no local EIA-860 zip: {e}")
            if verbose:
                print(f"WARNING: eia.gov check failed ({e}); using local {files[0].name}")
    if not meta or meta.get("file") != files[0].name:
        m = re.match(r"eia860(\d{4})\.zip$", files[0].name)
        meta = dict(meta, file=files[0].name, year=int(m.group(1)))
    return files[0], meta


PLANT_MEMBER_RE = re.compile(r"(?:^|/)2___Plant_Y(\d{4})\.xlsx$", re.I)
KEEP = ["Utility ID", "Utility Name", "Plant Code", "Plant Name", "Street Address", "City",
        "State", "Zip", "County", "Latitude", "Longitude"]


def load_plants(zip_path):
    """The Plant sheet of the annual zip as a DataFrame (header row index 1). Plant Code is a
    string without a trailing .0; Zip is a string."""
    import pandas as pd
    with zipfile.ZipFile(zip_path) as z:
        names = [n for n in z.namelist() if PLANT_MEMBER_RE.search(n)]
        if not names:
            raise ValueError(f"{zip_path} has no 2___Plant_Y<year>.xlsx member")
        raw = z.read(names[0])
    df = pd.read_excel(io.BytesIO(raw), sheet_name="Plant", header=1, engine="openpyxl",
                       dtype={"Plant Code": str, "Zip": str, "Utility ID": str})
    df.columns = [str(c).strip() for c in df.columns]
    df["Plant Code"] = df["Plant Code"].astype(str).str.replace(r"\.0$", "", regex=True).str.strip()
    df = df[df["Plant Code"].str.match(r"^\d+$")]
    cols = [c for c in KEEP if c in df.columns]
    return df[cols].reset_index(drop=True)


def _s(v):
    if v is None:
        return ""
    try:
        if v != v:       # NaN
            return ""
    except Exception:
        pass
    s = str(v).strip()
    return re.sub(r"\.0$", "", s) if re.fullmatch(r"\d+\.0", s) else s


def _f(v):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return None if x != x else x


def plant_index(df):
    """{plant_code: {name, address, city, state, zip, county, lat, lon, utility}}.
    lat and lon are floats or None."""
    out = {}
    for r in df.to_dict("records"):
        code = _s(r.get("Plant Code"))
        if not code:
            continue
        out[code] = {"name": _s(r.get("Plant Name")), "address": _s(r.get("Street Address")),
                     "city": _s(r.get("City")), "state": _s(r.get("State")),
                     "zip": _s(r.get("Zip")), "county": _s(r.get("County")),
                     "lat": _f(r.get("Latitude")), "lon": _f(r.get("Longitude")),
                     "utility": _s(r.get("Utility Name"))}
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true", help="check eia.gov now")
    ap.add_argument("--path", action="store_true", help="newest local path only, no network")
    a = ap.parse_args()
    if a.path:
        files = local_files()
        if not files:
            sys.exit("ERROR: no local EIA-860 zip; run eia860.py without --path")
        print(files[0])
        return
    path, meta = ensure_latest(force=a.check)
    print(path)
    print(f"year: {meta.get('year') or '?'}  checked: {meta.get('checked') or '?'}")


if __name__ == "__main__":
    main()

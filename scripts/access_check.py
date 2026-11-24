"""
Access check: prove, before a batch runs, that every statewide source the scope
lists can be read, and keep the proof.

Baird 2026-11-03 (Oklahoma planning): "I want to be ASSURED that you're able
to access any documents and websites that are helpful or relevant to the
research." Until now a source was listed in scopes/<tag>/coverage.json and
only the sweep found out whether it opened. This script opens each one first,
through fetch.py's whole ladder (curl, TLS impersonation, real-Chrome
clearance, a real-Chrome page load, a Wayback copy), reads one real document
from it when the list names one, checks that what came back is the kind of
thing the entry promises (a PDF with PDF bytes, a CSV with a header, a table
with rows, JSON that parses, a page with a sentence that must be on it), and
writes `batches/<tag>/access_proof.json` plus `access_proof.md` with the
route, the time, the size and where the sample was saved. state_gate.py's
`access-proof` gate reads the file: every listed source is proven, or the
list says in words what a person has to do to open it (`human_wall`), or the
batch does not run.

    python access_check.py --scope us-ok               # every source
    python access_check.py --scope us-ok --only odeq-onbase,occ-weblink
    python access_check.py --scope us-ok --batch ../batches/us-ok-dc

Fields an entry in scopes/<tag>/coverage.json may carry, all optional:

    "proof": {
        "sample":  "https://.../one-real-document.pdf",   # read this instead of `url`
        "method":  "POST", "json": {...}, "headers": {...}, # for an API entry
        "warm":    "https://.../Welcome.aspx",              # GET first, for the session cookie
        "kind":    "pdf" | "csv" | "json" | "table" | "html",
        "expect":  "a phrase that must appear in the text",
        "min_rows": 50,                                     # table or csv rows
        "insecure": true                                    # the host's certificate fails
    },
    "human_wall": "what a person must do (a sign-in, a records request) and why"

A Google Sheets or Docs address is proven through the work gws profile (the
file's metadata is read with `gws drive files get`), never through a public
export link. An entry with `human_wall` is still tried; the gate accepts it
unproven only because the words say what the person does.

Failures are also written to fetch.py's give-up log tagged with the scope, so
`access_audit.py --retry` and gate `access` see them like any other read.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import fetch  # noqa: E402
from paths import REPO_ROOT, scope_base, scope_coverage, scope_work  # noqa: E402

PROOF_FILE = "access_proof.json"
MAX_AGE_DAYS = 7
KINDS = ("pdf", "csv", "json", "table", "html")
SAMPLE_CHARS = 4000
GOOGLE_RX = re.compile(r"https?://docs\.google\.com/(?:spreadsheets|document)/d/([A-Za-z0-9_-]+)")
TABLE_ROW_RX = re.compile(r"<tr[\s>]", re.I)
_SOFT_ERROR = re.compile(r"<title>[^<]*(?:not found|error|access denied|forbidden|sign in|log in)[^<]*</title>", re.I)


# ----------------------------------------------------------------- checks ---

_FRAME_RX = re.compile(r"<\s*(frameset|frame|iframe)\b", re.I)
FRAME_TEXT_MIN = 300   # visible characters a framed page needs to count as content


def _frame_only(html: str) -> bool:
    """True for a page that is a frame or iframe around another page and has almost no
    visible text of its own, so a phrase such as 'OASIS' in its title proves nothing."""
    if not _FRAME_RX.search(html or ""):
        return False
    body = re.sub(r"(?is)<(script|style|noscript|title|head)\b.*?</\1>", " ", html)
    visible = re.sub(r"\s+", " ", re.sub(r"(?s)<[^>]+>", " ", body)).strip()
    return len(visible) < FRAME_TEXT_MIN

def check_kind(kind: str, raw: bytes, text: str, content_type: str, min_rows: int | None = None,
               ladder_pdf: bool = False) -> str:
    """'' when the body is the promised kind, else the reason it is not. `ladder_pdf` says
    fetch.py's ladder already saw %PDF bytes and extracted the text (its own check), which
    stands in when plain curl, the only route that keeps the bytes here, is turned away."""
    kind = (kind or "").lower()
    if kind == "pdf":
        if not raw.startswith(b"%PDF") and not ladder_pdf:
            return "not a PDF: the body does not start with %PDF (an HTML page came back)"
        if not text.strip():
            return "a PDF with no text layer (scan); OCR it or find the text copy"
        return ""
    if kind == "csv":
        body = raw.decode("utf-8", "replace")
        lines = [ln for ln in body.splitlines() if ln.strip()]
        if not lines or "<html" in body[:2000].lower():
            return "not a CSV: an HTML page came back"
        try:
            rows = list(csv.reader(io.StringIO(body)))
        except csv.Error as e:
            return f"not a CSV: {e}"
        if len(rows) < 2 or len(rows[0]) < 2:
            return "not a CSV table: fewer than two rows or two columns"
        if min_rows and len(rows) - 1 < min_rows:
            return f"only {len(rows) - 1} rows, expected at least {min_rows}"
        return ""
    if kind == "json":
        try:
            json.loads(raw.decode("utf-8", "replace"))
        except ValueError:
            return "not JSON: the body does not parse"
        return ""
    if kind == "table":
        n = len(TABLE_ROW_RX.findall(text))
        if n < 2:
            return "no table rows in the page (a script draws the table, or a form must be posted)"
        if min_rows and n - 1 < min_rows:
            return f"only {n - 1} table rows, expected at least {min_rows}"
        return ""
    if kind in ("html", ""):
        if not text.strip():
            return "an empty body"
        if _SOFT_ERROR.search(text[:4000]):
            return f"a soft error page (title {re.search(r'<title>([^<]*)', text, re.I).group(1).strip()!r})"
        if _frame_only(text):
            return ("a frame around another page with almost no text of its own (the OATI OASIS "
                    "shell is one); point the entry at the documents the frame loads")
        return ""
    return f"unknown kind {kind!r}: use one of {', '.join(KINDS)}"


def expect_missing(expect: str, text: str) -> str:
    if not expect:
        return ""
    norm = re.sub(r"\s+", " ", text).lower()
    return "" if re.sub(r"\s+", " ", expect).lower() in norm else f"the phrase {expect!r} is not on the page"


# ------------------------------------------------------------------ fetch ---

def _session():
    import requests
    return requests.Session()


def _api_call(url: str, method: str, body, headers: dict | None, timeout: int, insecure: bool,
              warm: str = ""):
    """One request with a method or a JSON body (the fetch ladder does GET only). `warm` is
    an address opened first in the same session, for a site whose services answer only with
    the cookie its welcome page sets (the OCC Laserfiche WebLink store).
    Returns (status, content_type, raw, notes)."""
    import requests
    h = {"User-Agent": fetch.CHROME_UA, "Accept": "application/json, application/pdf, */*"}
    h.update(headers or {})
    notes = ["direct_" + method.lower()]
    if insecure:
        notes.append("insecure_tls")
        import urllib3
        urllib3.disable_warnings()
    s = _session()
    try:
        if warm:
            notes.append("warm_cookie")
            s.get(warm, headers={"User-Agent": fetch.CHROME_UA}, timeout=timeout, verify=not insecure)
        r = s.request(method, url, json=body if method != "GET" else None, headers=h,
                      timeout=timeout, verify=not insecure)
    except requests.RequestException as e:
        return "000", "", b"", notes + [f"error: {e.__class__.__name__}"]
    return str(r.status_code), r.headers.get("content-type", ""), r.content, notes


def fetch_proof(url: str, proof: dict, timeout: int = 60):
    """(status, content_type, raw, text, is_pdf, notes, final_url) for the address the
    proof names, through the whole fetch ladder; a POST or a JSON body goes direct."""
    method = (proof.get("method") or "GET").upper()
    if method != "GET" or proof.get("json") is not None or proof.get("warm"):
        status, ctype, raw, notes = _api_call(url, method, proof.get("json"), proof.get("headers"),
                                              timeout, bool(proof.get("insecure")),
                                              warm=proof.get("warm") or "")
        text = raw.decode("utf-8", "replace") if not raw.startswith(b"%PDF") else ""
        is_pdf = raw.startswith(b"%PDF")
        if is_pdf:
            text = pdf_text(raw)
        return status, ctype, raw, text, is_pdf, notes, url
    page = fetch.fetch_page(url, timeout=timeout, headers=proof.get("headers"))
    raw = page.text.encode("utf-8", "replace") if not page.is_pdf else b""
    notes = list(page.notes)
    if page.is_pdf or (proof.get("kind") == "pdf"):
        # fetch_page hands back extracted text; the bytes themselves prove the kind
        raw = raw_bytes(url, timeout, proof)
        if page.is_pdf and not raw.startswith(b"%PDF"):
            # plain curl was turned away (a Cloudflare host); the ladder's route saw the
            # %PDF bytes itself (fetch._extract) and extracted this text, so that stands
            raw = b""
            notes.append("pdf_via_ladder")
    return page.status, page.content_type, raw, page.text, page.is_pdf, notes, page.final_url


def raw_bytes(url: str, timeout: int, proof: dict) -> bytes:
    """The body as bytes, for the magic-byte check, through curl with the learned
    route's user agent (the ladder keeps only text)."""
    try:
        fd, name = tempfile.mkstemp(prefix="access_check_", suffix=".bin")
        os.close(fd)
        out = Path(name)
    except OSError:
        return b""
    try:
        args = ["curl", "-sL", "--compressed", "-A", fetch.CHROME_UA, "--max-time", str(timeout)]
        if proof.get("insecure"):
            args.append("-k")
        subprocess.run(args + [url, "-o", str(out)], capture_output=True, timeout=timeout + 10)
        return out.read_bytes() if out.exists() else b""
    except (OSError, subprocess.SubprocessError):
        return b""
    finally:
        try:
            out.unlink()
        except OSError:
            pass


def pdf_text(raw: bytes) -> str:
    try:
        from pypdf import PdfReader
        return "\n".join((p.extract_text() or "") for p in PdfReader(io.BytesIO(raw)).pages[:5])
    except Exception:
        return ""


def google_proof(file_id: str, timeout: int = 60):
    """A work Drive file is proven through the work gws profile: the file's name and
    type come back when the login can see it. Returns (ok, note, name)."""
    try:
        from gsheets import _env
        env = _env()
    except (Exception, SystemExit) as e:        # the helper exits when the profile or gws is missing
        return False, f"gws profile not available: {e}", ""
    params = {"fileId": file_id, "supportsAllDrives": True, "fields": "id,name,mimeType,modifiedTime"}
    try:
        p = subprocess.run(["gws", "drive", "files", "get", "--params", json.dumps(params)],
                           env=env, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError) as e:
        return False, f"gws did not run: {e}", ""
    if p.returncode != 0:
        tail = " | ".join(((p.stderr or p.stdout).strip().splitlines() or ["no output"])[-2:])
        return False, f"gws drive files get failed: {tail}", ""
    try:
        meta = json.loads(p.stdout)
    except ValueError:
        meta = {}
    name = meta.get("name") or ""
    return bool(name), ("read through the work gws profile" if name else "gws returned no file name"), name


# ---------------------------------------------------------------- entries ---

def check_entry(entry: dict, sample_dir: Path, timeout: int = 60, fetch_fn=None, google_fn=None) -> dict:
    """Open one listed source and say what came back. fetch_fn and google_fn are the
    test seams (fetch_proof and google_proof by default)."""
    fetch_fn = fetch_fn or fetch_proof
    google_fn = google_fn or google_proof
    proof = entry.get("proof") or {}
    url = proof.get("sample") or entry.get("url") or ""
    rec = {"id": entry.get("id"), "url": url, "checked": time.strftime("%Y-%m-%dT%H:%M:%S"),
           "kind": proof.get("kind") or "", "ok": False, "route": "", "status": "", "reason": "",
           "bytes": 0, "sample": ""}
    if entry.get("human_wall"):
        rec["human_wall"] = entry["human_wall"]
    m = GOOGLE_RX.match(url)
    if m:
        ok, note, name = google_fn(m.group(1), timeout)
        rec.update(ok=ok, route="gws-gem", status="200" if ok else "", reason="" if ok else note,
                   file_name=name)
        return rec
    status, ctype, raw, text, is_pdf, notes, final = fetch_fn(url, proof, timeout)
    rec.update(status=status, content_type=ctype, bytes=len(raw) if raw else len(text.encode("utf-8", "replace")),
               route=", ".join(notes) or "curl", final_url=final or "")
    if status != "200":
        rec["reason"] = f"HTTP {status}" + (f" ({', '.join(notes)})" if notes else "")
        return rec
    kind = proof.get("kind") or ("pdf" if is_pdf else "html")
    body = raw if raw else text.encode("utf-8", "replace")
    why = (check_kind(kind, body, text, ctype, proof.get("min_rows"), ladder_pdf=bool(is_pdf and not raw))
           or expect_missing(proof.get("expect") or "", text))
    if "empty_answer" in notes and not why:
        why = "an empty record page (the site answered with its empty-result page)"
    rec["reason"] = why
    rec["ok"] = not why
    try:
        sample_dir.mkdir(parents=True, exist_ok=True)
        ext = "pdf" if kind == "pdf" and body.startswith(b"%PDF") else "txt"
        sp = sample_dir / f"{entry.get('id')}.{ext}"
        sp.write_bytes(body if ext == "pdf" else text[:SAMPLE_CHARS].encode("utf-8", "replace"))
        rec["sample"] = str(sp.relative_to(REPO_ROOT)) if sp.is_relative_to(REPO_ROOT) else str(sp)
    except OSError:
        pass
    if not rec["ok"]:
        log_give_up(url, status, notes, entry.get("id"))
    return rec


def log_give_up(url: str, status: str, notes: list, sid) -> None:
    """A source the check could not prove goes into fetch.py's give-up log, tagged
    with the scope (GEM_BATCH), so access_audit.py --retry and gate `access` see it."""
    try:
        fetch._log_failure(url, status, list(notes) + [f"access_check:{sid}"])
    except Exception:
        pass


def load_proof(batch: Path) -> dict | None:
    try:
        return json.loads((Path(batch) / PROOF_FILE).read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return None


def age_days(stamp: str, now: float | None = None) -> float | None:
    try:
        t = time.mktime(time.strptime(stamp[:19], "%Y-%m-%dT%H:%M:%S"))
    except (TypeError, ValueError):
        return None
    return ((now if now is not None else time.time()) - t) / 86400


def markdown(scope: str, proof: dict) -> str:
    lines = [f"# Access proof: {scope}", "",
             f"Checked {proof.get('checked')}. {proof.get('ok_count')} of {proof.get('total')} sources proven; "
             f"{proof.get('human_walls')} behind a person's action.", "",
             "| id | ok | route | status | kind | bytes | reason or person |", "|---|---|---|---|---|---|---|"]
    for sid, r in sorted((proof.get("sources") or {}).items()):
        what = r.get("reason") or ""
        if r.get("human_wall") and not r.get("ok"):
            what = f"PERSON: {r['human_wall']}"
        lines.append(f"| {sid} | {'yes' if r.get('ok') else 'NO'} | {r.get('route', '')} | {r.get('status', '')} | "
                     f"{r.get('kind') or ''} | {r.get('bytes', 0)} | {what} |")
    lines += ["", "Samples are under the scope's work folder (`access/`), never committed. "
                  "A NO with no PERSON line blocks the batch: fix the route (fetch.py --render, a harvester, "
                  "the real document's address) and run the check again."]
    return "\n".join(lines) + "\n"


def run(scope: str, batch: Path, only: set[str] | None = None, timeout: int = 60,
        fetch_fn=None, google_fn=None, list_path: Path | None = None, sample_dir: Path | None = None) -> dict:
    lp = list_path or scope_coverage(scope)
    wanted = json.loads(lp.read_text(encoding="utf-8"))
    sample_dir = sample_dir or (scope_work(scope) / "access")
    os.environ.setdefault("GEM_BATCH", Path(batch).name)
    earlier = load_proof(batch) or {}
    sources = dict(earlier.get("sources") or {}) if only else {}
    for w in wanted:
        if only and w.get("id") not in only:
            continue
        print(f"  {w.get('id')}: {(w.get('proof') or {}).get('sample') or w.get('url')}", file=sys.stderr)
        sources[w.get("id")] = check_entry(w, sample_dir, timeout, fetch_fn, google_fn)
    out = {"scope": scope, "list": str(lp.relative_to(REPO_ROOT)) if lp.is_relative_to(REPO_ROOT) else str(lp),
           "checked": time.strftime("%Y-%m-%dT%H:%M:%S"), "total": len(sources),
           "ok_count": sum(1 for r in sources.values() if r.get("ok")),
           "human_walls": sum(1 for r in sources.values() if r.get("human_wall") and not r.get("ok")),
           "sources": sources}
    Path(batch).mkdir(parents=True, exist_ok=True)
    (Path(batch) / PROOF_FILE).write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    (Path(batch) / "access_proof.md").write_text(markdown(scope, out), encoding="utf-8")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scope", required=True, help="scope tag, e.g. us-ok")
    ap.add_argument("--batch", default=None, help="batch folder (default batches/<scope>)")
    ap.add_argument("--only", default="", help="comma-separated source ids to re-check; the rest keep their proof")
    ap.add_argument("--timeout", type=int, default=60)
    a = ap.parse_args(argv)
    batch = Path(a.batch) if a.batch else REPO_ROOT / "batches" / a.scope
    only = {s.strip() for s in a.only.split(",") if s.strip()} or None
    out = run(scope_base(a.scope), batch, only, a.timeout)
    print((batch / "access_proof.md").read_text(encoding="utf-8"))
    bad = [sid for sid, r in out["sources"].items() if not r.get("ok") and not r.get("human_wall")]
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

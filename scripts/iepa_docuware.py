"""
Read the Illinois EPA's permit record: Document Explorer and the DocuWare cabinet behind it.

The Illinois EPA keeps every permit document it has issued or received in a DocuWare cabinet.
Two public doors open onto it (worked out 2026-10-30, after the CyrusOne Bilter Road engine
fleet was missed because only the public notice feed had been read):

  1. Document Explorer, https://webapps.illinois.gov/EPA/DocumentExplorer/. A site directory.
     Its search is an ajax GET (Attributes/Search) by name fragment, address, city, county or
     the Bureau site ID (the InterestId box; an air site ID looks like 043407AEH). Ten rows a
     page, 35,306 sites statewide. A site's record page, Documents/Index/<IEPAID>, names the
     site and address and lists its document categories, each as a DocuWare link. The record
     page is the address a person can open, so it is the one the harvest cites.
  2. The DocuWare cabinet, https://docuware7.illinois.gov/DocuWare/PlatformRO, cabinet
     87263d25-3843-4ee0-907b-464feabd20f0. The Document Explorer links land in its web client,
     which calls a JSON API. That API answers plain requests once two things are in hand: the
     x-docuware-pl-auth token the web client gets from its sign-in (read once from a real
     browser with Playwright, then cached in work/iepa_dw_session.json and reused for every
     call) and the x-docuware-pl-cs header, a Java-style string hash of the request path. With
     those, one POST queries the whole cabinet by any field (site name, site ID, category,
     date, permit number, subject line) in pages of up to 1,000 rows, and one GET downloads any
     document as a PDF. Nearly every document is a scan, so the text comes from OCR.

Cabinet fields: BUREAUID (the site ID), SITENAME, IEPAID (the Document Explorer record), CATEGORY
(a code; 03K is a final air permit, 03M an air permit application), ITEMDATE, PERMITID, PERMITLOG,
COMMENTTEXT (the subject line, for example "57 New Generators-CHI9/CHI10"), DWDOCID (the
document) and DWPAGECOUNT.

    from iepa_docuware import Client, de_search, de_record, AIR_CATEGORIES
    c = Client()                                   # bootstraps or reuses the saved session
    rows = c.query('[SITENAME] LIKE "*CYRUSONE*"')  # list of {field: value}
    for r in c.query_all('[CATEGORY]="03K" AND [ITEMDATE] >= "2024-01-01"'): ...
    c.download_pdf(doc_id, path)                   # the document as a PDF
    text = c.document_text(doc_id, cache_dir)      # its text (OCR), cached next to the PDF

Command line:

    python scripts/iepa_docuware.py search --name "cyrusone"          # Document Explorer rows
    python scripts/iepa_docuware.py query '[SITENAME] LIKE "*ALIGNED*"' # cabinet rows
    python scripts/iepa_docuware.py record 170002668842                # one record page
    python scripts/iepa_docuware.py text 1465329                       # one document's text

Nothing here writes anywhere but the gitignored work folders.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import unquote, urlencode, urlparse, parse_qs

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import REPO_ROOT, work_dir  # noqa: E402

BASE = "https://docuware7.illinois.gov/DocuWare/PlatformRO"
PREFIX = "/DocuWare/PlatformRO"
CABINET = "87263d25-3843-4ee0-907b-464feabd20f0"
DE = "https://webapps.illinois.gov/EPA/DocumentExplorer"
NULL_DIALOG = "00000000-0000-0000-0000-000000000000"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")
# A record page known to carry a DocuWare link, used to bootstrap a session when no other
# link is at hand (CyrusOne, 2725 Bilter Road, Aurora).
BOOT_RECORD = "170002668842"
SESSION_PATH = work_dir() / "iepa_dw_session.json"
FIELDS = "DWDOCID,DWPAGECOUNT,BUREAUID,SITENAME,ITEMDATE,PERMITID,PERMITLOG,COMMENTTEXT,CATEGORY,IEPAID"

# Category codes of the Bureau of Air family and what each holds (read from samples of the
# cabinet, 2026-10-30; Document Explorer labels 03K "Air Permit - Final" and 08 "Compliance").
AIR_CATEGORIES = {
    "03K": "final air permit",
    "03M": "air permit application",
    "03N": "air permit correspondence (name and ownership changes, fugitive dust plans)",
    "03L": "air permit file (Bureau of Air)",
    "03P": "open burning permit",
    "08": "compliance (Bureau of Air)",
}
PERMIT_CATEGORIES = ("03K", "03M")       # the documents a harvest downloads and reads
DATE_RX = re.compile(r"/Date\((-?\d+)\)/")

# The site ID starts with the county's three-digit FIPS code (043 = DuPage, 031 = Cook).
IL_COUNTIES = [
    "Adams", "Alexander", "Bond", "Boone", "Brown", "Bureau", "Calhoun", "Carroll", "Cass", "Champaign",
    "Christian", "Clark", "Clay", "Clinton", "Coles", "Cook", "Crawford", "Cumberland", "DeKalb", "DeWitt",
    "Douglas", "DuPage", "Edgar", "Edwards", "Effingham", "Fayette", "Ford", "Franklin", "Fulton", "Gallatin",
    "Greene", "Grundy", "Hamilton", "Hancock", "Hardin", "Henderson", "Henry", "Iroquois", "Jackson", "Jasper",
    "Jefferson", "Jersey", "Jo Daviess", "Johnson", "Kane", "Kankakee", "Kendall", "Knox", "Lake", "LaSalle",
    "Lawrence", "Lee", "Livingston", "Logan", "McDonough", "McHenry", "McLean", "Macon", "Macoupin", "Madison",
    "Marion", "Marshall", "Mason", "Massac", "Menard", "Mercer", "Monroe", "Montgomery", "Morgan", "Moultrie",
    "Ogle", "Peoria", "Perry", "Piatt", "Pike", "Pope", "Pulaski", "Putnam", "Randolph", "Richland",
    "Rock Island", "St Clair", "Saline", "Sangamon", "Schuyler", "Scott", "Shelby", "Stark", "Stephenson",
    "Tazewell", "Union", "Vermilion", "Wabash", "Warren", "Washington", "Wayne", "White", "Whiteside", "Will",
    "Williamson", "Winnebago", "Woodford",
]


def _fips_key(name):
    s = name.lower()
    s = re.sub(r"^mc", "mac", s)
    s = re.sub(r"^st\.? ", "saint ", s)
    return re.sub(r"[^a-z]", "", s)


COUNTY_BY_CODE = {f"{2 * i + 1:03d}": n for i, n in enumerate(sorted(IL_COUNTIES, key=_fips_key))}


def county_of_site_id(site_id):
    """'043407AEH' -> 'DuPage'; '' when the ID does not start with a county code."""
    return COUNTY_BY_CODE.get(str(site_id or "")[:3], "")


def jhash(s):
    """Java String.hashCode of s as DocuWare's x-docuware-pl-cs header wants it."""
    h = 0
    for c in s:
        h = (31 * h + ord(c)) & 0xFFFFFFFF
    return str(h - 2 ** 32 if h >= 2 ** 31 else h)


def dw_date(v):
    """'/Date(1733288400000)/' -> '2024-12-04'; other values unchanged."""
    m = DATE_RX.match(str(v or ""))
    if not m:
        return v
    return time.strftime("%Y-%m-%d", time.gmtime(int(m.group(1)) / 1000))


def log(msg):
    print(f"  [iepa] {msg}", file=sys.stderr, flush=True)


def looks_like_words(text):
    """True when most tokens are word-like (OCR of a sideways page is a soup of short tokens)."""
    toks = re.findall(r"\S+", text)
    if len(toks) < 20:
        return False
    good = sum(1 for t in toks if re.fullmatch(r"[A-Za-z][A-Za-z'’.,;:()-]{2,}", t))
    return good / len(toks) >= 0.45


def ocr_png(png):
    """Tesseract on one page image; a page that reads as soup is retried with orientation
    detection (sideways tables in applications and emission reports)."""
    t = subprocess.run(["tesseract", str(png), "stdout", "-l", "eng", "--psm", "6"],
                       capture_output=True, text=True, timeout=180)
    out = t.stdout if t.returncode == 0 else ""
    if not looks_like_words(out):
        t2 = subprocess.run(["tesseract", str(png), "stdout", "-l", "eng", "--psm", "1"],
                            capture_output=True, text=True, timeout=240)
        if t2.returncode == 0 and len(re.findall(r"[A-Za-z]{3,}", t2.stdout)) > len(re.findall(r"[A-Za-z]{3,}", out)):
            out = t2.stdout
    return out


# --------------------------------------------------------- Document Explorer ---

def de_search(name="", county="", interest_id="", city="", address="", page=1, timeout=60):
    """One page of Document Explorer's site directory: ([{name, address, city, state, zip, iepaid}], total)."""
    params = {"Length": 10, "Name": name, "Address": address, "City": city, "Zip": "", "County": county,
              "InterestId": interest_id, "ActiveTab": "#attributesTab", "SearchButton": "Search"}
    url = f"{DE}/Attributes/Search?{urlencode(params)}"
    if page > 1:
        url += f"&Page={page}"
    r = requests.get(url, headers={"User-Agent": UA, "X-Requested-With": "XMLHttpRequest"}, timeout=timeout)
    r.raise_for_status()
    return parse_de_rows(r.text)


def parse_de_rows(text):
    m = re.search(r"returned\s+([\d,]+)\s+records?", text)
    total = int(m.group(1).replace(",", "")) if m else 0
    rows = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", text, flags=re.S):
        cells = [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", c))).strip()
                 for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, flags=re.S)]
        link = re.search(r"Documents/Index/(\d+)", tr)
        if link and len(cells) >= 5:
            rows.append({"name": cells[0], "address": cells[1], "city": cells[2], "state": cells[3],
                         "zip": cells[4], "iepaid": link.group(1)})
    return rows, total


def de_record_url(iepaid, doc_id=None):
    """The citable address of a site's record, optionally pointing at one document."""
    u = f"{DE}/Documents/Index/{iepaid}"
    return f"{u}?dwdocid={doc_id}" if doc_id else u


def de_record(iepaid, timeout=60):
    """A record page: {iepaid, name, address, categories: [{category, label, count, pages, bureau, link}]}."""
    r = requests.get(de_record_url(iepaid), headers={"User-Agent": UA}, timeout=timeout)
    if r.status_code != 200:
        return None
    return parse_de_record(r.text, iepaid)


def parse_de_record(text, iepaid=""):
    out = {"iepaid": iepaid, "name": "", "address": "", "city": "", "categories": []}
    m = re.search(r'id="facilityAddress".*?<p>(.*?)</p>', text, flags=re.S)
    if m:
        lines = [re.sub(r"\s+", " ", html.unescape(re.sub(r"<(?!br)[^>]+>", " ", x))).strip()
                 for x in re.split(r"<br\s*/?>", m.group(1))]
        lines = [x for x in lines if x]
        if lines:
            out["name"] = re.sub(r"\s*[–-]\s*\d{9,}\s*$", "", lines[0])
            out["address"] = ", ".join(lines[1:])
            if len(lines) > 2:
                out["city"] = re.sub(r",\s*IL\b.*$", "", lines[-1]).strip()
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", text, flags=re.S):
        cells = [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", c))).strip()
                 for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, flags=re.S)]
        link = re.search(r"(https://docuware7\.illinois\.gov/[^\"'\s]+Integration\?ep=[A-Za-z0-9_=-]+)", tr)
        if link and cells:
            out["categories"].append({"label": cells[0], "count": cells[1] if len(cells) > 1 else "",
                                      "pages": cells[2] if len(cells) > 2 else "",
                                      "bureau": cells[3] if len(cells) > 3 else "",
                                      "link": html.unescape(link.group(1))})
    return out


def integration_link(iepaid=BOOT_RECORD):
    """Any DocuWare link from a record page (used to open a session)."""
    rec = de_record(iepaid)
    for c in (rec or {}).get("categories", []):
        if c.get("link"):
            return c["link"]
    return None


# ------------------------------------------------------------- the session ---

def bootstrap(link=None, path=SESSION_PATH, timeout=90000):
    """Open one DocuWare link in a real browser, keep the token and cookies its web client
    uses, and save them. Needs Playwright with Chrome or Chromium."""
    link = link or integration_link()
    if not link:
        raise RuntimeError("no DocuWare link found on the Document Explorer record page")
    from playwright.sync_api import sync_playwright
    got = {}
    with sync_playwright() as p:
        try:
            b = p.chromium.launch(channel="chrome", headless=True)
        except Exception:
            b = p.chromium.launch(headless=True)
        ctx = b.new_context()
        pg = ctx.new_page()

        def on_req(r):
            if "DialogExpression" in r.url and "token" not in got:
                h = r.all_headers()
                if h.get("x-docuware-pl-auth"):
                    got["token"] = h["x-docuware-pl-auth"]
                    got["ua"] = h.get("user-agent", UA)
        ctx.on("request", on_req)
        pg.goto(link, wait_until="networkidle", timeout=timeout)
        for _ in range(40):
            if "token" in got:
                break
            pg.wait_for_timeout(500)
        got["cookies"] = {c["name"]: c["value"] for c in ctx.cookies()}
        got["referer"] = pg.url
        got["saved"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        b.close()
    if "token" not in got:
        raise RuntimeError("the DocuWare web client sent no token; is the site up?")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(got), encoding="utf-8")
    log(f"new DocuWare session saved to {path}")
    return got


class Client:
    """Plain requests against the cabinet API with the web client's token."""

    def __init__(self, session_path=SESSION_PATH, cabinet=CABINET, refresh=False):
        self.path = Path(session_path)
        self.fc = cabinet
        self.sess = None
        self.http = requests.Session()
        self._load(refresh)

    def _load(self, refresh=False):
        if not refresh and self.path.exists():
            self.sess = json.loads(self.path.read_text(encoding="utf-8"))
        else:
            self.sess = bootstrap(path=self.path)
        self.http.headers["User-Agent"] = self.sess.get("ua") or UA
        self.http.cookies.clear()
        for k, v in self.sess.get("cookies", {}).items():
            self.http.cookies.set(k, v, domain="docuware7.illinois.gov")

    def call(self, path, method="GET", body=None, accept="application/json", timeout=120, stream=False):
        """One API call; a rejected token is renewed once in a fresh browser."""
        for attempt in (0, 1):
            h = {"Accept": accept, "x-docuware-pl-auth": self.sess["token"], "x-docuware-pl-cs": jhash(PREFIX + path),
                 "x-requested-with": "XMLHttpRequest", "Referer": self.sess.get("referer", BASE),
                 "Origin": "https://docuware7.illinois.gov"}
            r = self.http.request(method, BASE + path, headers=h, json=body, timeout=timeout, stream=stream)
            if attempt == 0 and self._stale(r):
                log(f"HTTP {r.status_code} from DocuWare (stale session); opening a new session")
                self._load(refresh=True)
                continue
            return r
        return r

    @staticmethod
    def _stale(r):
        """True when the response says the saved token is no longer good: 401/403, or the 500
        'Error occurred during a cryptographic operation' the server sends once its key rolls."""
        if r.status_code in (401, 403):
            return "signature" not in r.text[:300].lower()
        return r.status_code == 500 and "cryptographic" in r.text[:400].lower()

    # ----- queries
    def query_page(self, condition, start=0, count=1000, fields=FIELDS, sort=("ITEMDATE", "Asc")):
        path = (f"/FileCabinets/{self.fc}/Query/DialogExpression?dialogId={NULL_DIALOG}"
                f"&fields={fields.replace(',', '%2C')}")
        body = {"CompleteCondition": condition, "CompleteConditionInInvariantCulture": False, "Condition": [],
                "SortOrder": [{"Field": sort[0], "Direction": sort[1]}], "ForceRefresh": True, "Operation": "And",
                "AdditionalResultFields": [], "Start": start, "Count": count, "IncludeSuggestions": False}
        r = self.call(path, "POST", body, "application/vnd.docuware.platform.documentstable+json, application/json")
        if r.status_code != 200:
            raise RuntimeError(f"DocuWare query failed, HTTP {r.status_code}: {r.text[:200]}")
        d = r.json()
        heads = [h["FieldName"] for h in d.get("Headers", [])]
        keep = set(fields.split(",")) if fields else None    # the API returns every field regardless
        rows = [{k: dw_date(v) for k, v in zip(heads, row) if not keep or k in keep} for row in d.get("Rows", [])]
        total = (d.get("Count") or {}).get("Value", len(rows))
        return rows, total

    def query(self, condition, count=1000, fields=FIELDS):
        return self.query_page(condition, 0, count, fields)[0]

    def query_all(self, condition, fields=FIELDS, page=1000, limit=None):
        """Every row of a condition, 1,000 a request."""
        start, out = 0, []
        while True:
            rows, total = self.query_page(condition, start, page, fields)
            out += rows
            start += len(rows)
            if not rows or start >= total or (limit and start >= limit):
                return out

    def select_list(self, field, count=400):
        r = self.call(f"/FileCabinets/{self.fc}/Query/SelectListExpression?dialogId={NULL_DIALOG}"
                      f"&fieldName={field}&count={count}")
        return r.json() if r.status_code == 200 else None

    # ----- documents
    def document(self, doc_id):
        r = self.call(f"/FileCabinets/{self.fc}/Documents/{doc_id}")
        return r.json() if r.status_code == 200 else None

    def download_pdf(self, doc_id, path, timeout=300):
        """The document as a PDF (a scanned image PDF for nearly every record). True when saved."""
        path = Path(path)
        if path.exists() and path.stat().st_size > 1000:
            return True
        r = self.call(f"/FileCabinets/{self.fc}/Documents/{doc_id}/FileDownload?targetFileType=PDF&keepAnnotations=false",
                      accept="*/*", timeout=timeout)
        if r.status_code != 200 or not r.content.startswith(b"%PDF"):
            return False
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(r.content)
        return True

    def page_image(self, doc_id, page=0, path=None, section=None):
        """One page as a PNG (section ids are '<docid>-<n>'; the document JSON lists them)."""
        sec = section or f"{doc_id}-{page + 1}"
        r = self.call(f"/FileCabinets/{self.fc}/Rendering/{sec}/Image?page=0&v=0", accept="image/png,*/*")
        if r.status_code != 200:
            return None
        if path:
            Path(path).write_bytes(r.content)
        return r.content

    def document_text(self, doc_id, cache_dir, max_pages=25):
        """The document's text, cached as <cache_dir>/<doc_id>.txt next to <doc_id>.pdf. The PDF
        goes through fetch.py's reader (text layer, else OCR of the first pages); a scan that
        still yields nothing is OCR'd from the cabinet's own page images (one per scanned page)."""
        cache_dir = Path(cache_dir)
        cache_dir.mkdir(parents=True, exist_ok=True)
        txt = cache_dir / f"{doc_id}.txt"
        if txt.exists():
            return txt.read_text(encoding="utf-8", errors="replace")
        other = cached_text_elsewhere(doc_id)
        if other is not None:
            txt.write_text(other, encoding="utf-8")
            return other
        pdf = cache_dir / f"{doc_id}.pdf"
        got_pdf = self.download_pdf(doc_id, pdf)
        meta = self.document(doc_id) or {}
        sections = meta.get("Sections") or []
        if not got_pdf and not sections:
            raise RuntimeError(f"DocuWare returned neither the PDF nor the page list for document {doc_id}")
        scanned = any(str(s.get("ContentType", "")).startswith("image/") for s in sections)
        text = ""
        if not scanned and pdf.exists():
            try:
                from fetch import _pdftotext
                text = _pdftotext(str(pdf))
            except Exception:
                text = ""
        if len(text.strip()) < 200:
            # Scanned pages: the cabinet's own page renders (one section per scanned page, or
            # page=N of a native PDF's single section) OCR cleanly; fetch.py's OCR of the image
            # PDF does not, so it is not used here.
            pages = []
            for s in sections:
                for i in range(int(s.get("PageCount") or 1)):
                    pages.append((s["Id"], i if not scanned else 0))
            chunks = []
            for n, (sec, pg) in enumerate(pages[:max_pages]):
                png = cache_dir / f"{doc_id}_p{n + 1}.png"
                r = self.call(f"/FileCabinets/{self.fc}/Rendering/{sec}/Image?page={pg}&v=0", accept="image/png,*/*")
                if r.status_code != 200:
                    continue
                png.write_bytes(r.content)
                try:
                    chunks.append(ocr_png(png))
                except (FileNotFoundError, subprocess.SubprocessError):
                    break
                finally:
                    png.unlink(missing_ok=True)
            if len("".join(chunks).strip()) > len(text.strip()):
                text = "\n\f\n".join(chunks)
        if text.strip() or got_pdf:
            txt.write_text(text, encoding="utf-8")    # an empty result is cached only when the PDF itself is here
        return text


def cached_text_elsewhere(doc_id, roots=None):
    """The document's text when a harvest already read it into another cache: the scope
    folders' work/permits/docs/<site>/<doc_id>.txt, fetch.py's work/iepa_docs/<record>/, and the
    older work/permits/<tag>/docs/. Saves a second download and a second OCR of the same scan
    when url_verifier.py or data_center_fleets.py comes to a document the harvester has read.
    None when no copy with text exists."""
    roots = roots or [REPO_ROOT / "scopes", work_dir()]
    patterns = ["*/work/permits/docs/*/{id}.txt", "permits/*/docs/*/{id}.txt", "iepa_docs/*/{id}.txt"]
    for root in roots:
        for pat in patterns:
            for p in sorted(Path(root).glob(pat.format(id=doc_id))):
                try:
                    text = p.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
                if text.strip():
                    return text
    return None


# ------------------------------------------------- reading a record address ---

def record_text(url, cache_dir=None, client=None, max_docs=6):
    """The text behind a Document Explorer record address, for fetch.py and url_verifier.py:
    the record page's own words, then the text of the document named by ?dwdocid=, or of the
    newest permit documents (final permits and applications) when none is named. None when
    the address is not a record page."""
    m = re.search(r"DocumentExplorer/Documents/Index/(\d+)", url)
    if not m:
        return None
    iepaid = m.group(1)
    want = (parse_qs(urlparse(url).query).get("dwdocid") or [None])[0]
    rec = de_record(iepaid)
    if rec is None:
        return None
    cache_dir = Path(cache_dir or work_dir() / "iepa_docs" / iepaid)
    parts = [f"Illinois EPA Document Explorer record {iepaid}: {rec['name']}", rec.get("address", ""),
             "Document categories: " + "; ".join(f"{c['label']} ({c['count']} documents, {c['bureau']})"
                                                  for c in rec["categories"])]
    try:
        c = client or Client()
        if want:
            # ask for the one document: a big record (Nelson has over 200 rows) would
            # otherwise be cut off before its newest documents
            rows = [r for r in c.query(f'[IEPAID]="{iepaid}" AND [DWDOCID]={int(want)}', count=5)
                    if str(r.get("DWDOCID")) == str(want)]
        else:
            rows, _ = c.query_page(f'[IEPAID]="{iepaid}"', 0, 200, sort=("ITEMDATE", "Desc"))
    except Exception as e:  # the record page alone is still something
        parts.append(f"(the DocuWare cabinet could not be read: {e})")
        return "\n".join(parts)
    if not want:
        rows = sorted([r for r in rows if r.get("CATEGORY") in PERMIT_CATEGORIES],
                      key=lambda r: str(r.get("ITEMDATE") or ""), reverse=True)[:max_docs]
    for r in rows:
        parts.append(f"\n==== Document {r.get('DWDOCID')} ({AIR_CATEGORIES.get(r.get('CATEGORY'), r.get('CATEGORY'))}, "
                     f"{r.get('ITEMDATE')}, permit {r.get('PERMITID') or ''} {r.get('PERMITLOG') or ''}, "
                     f"subject {r.get('COMMENTTEXT') or ''}) ====")
        parts.append(c.document_text(r["DWDOCID"], cache_dir))
    return "\n".join(p for p in parts if p)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="Document Explorer site directory")
    s.add_argument("--name", default="")
    s.add_argument("--county", default="")
    s.add_argument("--site-id", default="", help="Bureau site ID, e.g. 043407AEH")
    s.add_argument("--city", default="")
    s.add_argument("--page", type=int, default=1)
    q = sub.add_parser("query", help="a cabinet condition, e.g. '[SITENAME] LIKE \"*ALIGNED*\"'")
    q.add_argument("condition")
    q.add_argument("--count", type=int, default=100)
    r = sub.add_parser("record", help="one Document Explorer record page")
    r.add_argument("iepaid")
    t = sub.add_parser("text", help="one document's text (OCR)")
    t.add_argument("doc_id")
    t.add_argument("--out", default=None, help="cache folder (default work/iepa_docs/_cli)")
    u = sub.add_parser("read", help="what fetch.py sees behind a record address")
    u.add_argument("url")
    sub.add_parser("bootstrap", help="open a fresh browser session and save it")
    args = ap.parse_args()

    if args.cmd == "search":
        rows, total = de_search(args.name, args.county, args.site_id, args.city, page=args.page)
        print(f"{total} records; page {args.page}")
        for x in rows:
            print(f"{x['iepaid']}\t{x['name']}\t{x['address']}, {x['city']} {x['zip']}")
    elif args.cmd == "query":
        for x in Client().query(args.condition, count=args.count):
            print(json.dumps(x, ensure_ascii=False))
    elif args.cmd == "record":
        print(json.dumps(de_record(args.iepaid), indent=1))
    elif args.cmd == "text":
        print(Client().document_text(args.doc_id, args.out or work_dir() / "iepa_docs" / "_cli"))
    elif args.cmd == "read":
        print(record_text(args.url))
    elif args.cmd == "bootstrap":
        bootstrap()


if __name__ == "__main__":
    main()

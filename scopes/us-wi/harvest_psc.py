"""
Harvest Public Service Commission of Wisconsin (PSC) dockets on generation before a research sweep.

The PSC's Electronic Records Filing system (ERF, apps.psc.wi.gov/ERF) holds every filing of every
docket, and none of it needs a sign-in. What was found (2026-11-17):

  1. A docket's page is a plain GET:
       /ERF/ERFsearch/content/searchResult.aspx?UTIL=<utility>&CASE=<type>&SEQ=<number>&START=none&END=none
       &TYPE=none&SERVICE=none&KEY=none&NON=N&EXM=N
     "6630-CE-318" is UTIL 6630, CASE CE, SEQ 318. The "Search Criteria" box at the top of the page
     carries the docket title in its first row, and the table lists every filing: PSC reference
     number, description, document type, received date, file format and size, and a class code
     (P public, C confidential). Confidential and in-camera filings have no link.
  2. The same address with UTIL=0, SEQ=0, a START and END date and SERVICE=ELE lists every filing
     of every electric docket of one case type received in that window. The page is 25 to 110 MB and
     carries no titles, so this harvester keeps only the docket numbers and fetches each docket's
     title from its own page.
  3. A document downloads from /ERF/ERFview/viewdoc.aspx?docid=<n> (PDF with a text layer, Word,
     Excel). The public address to cite is https://apps.psc.wi.gov/pages/viewdoc.htm?docid=<n>.
  4. Access: a request with no browser User-Agent gets a short 404 error page, which is why a plain
     curl on CE-315, CE-318 and CE-319 looked like a failure. A browser User-Agent plus an
     Accept-Language header answers every time (fetch.py's CHROME_UA does this). No cookie, no
     session. This harvester sends those headers itself and falls back to fetch.py's ladder.
  5. The case pages under psc.wi.gov/Pages/CommissionActions/CasePages/ are linked from
     HighlightedCases.aspx. They carry the docket title, an application summary and the filing links.

Steps:
  1. Collect docket numbers: the statewide filing lists of each case type (CE, CA, AE, BS, TE, ES) for
     each year from --from-year, each utility's own list (--utilities), and the hand list KNOWN_DOCKETS.
  2. Fetch each docket's page (cached under scopes/us-wi/work/psc/<docket>/search.json) for its title and
     filing table. Keep dockets about a gas or oil plant, a conversion, a retirement, a data center
     service agreement or large load tariff, an acquisition, the Strategic Energy Assessment, a resource
     plan or LNG storage. Transmission-only, wind, solar and storage dockets are listed, not read.
  3. For each key docket, download the application, engineering plan, decision and the data request
     answers that name a unit (capped, larger first) into scopes/us-wi/work/psc/<docket>/ (not
     committed) and keep the lines that give technology, megawatts, maker and model, in-service and
     retirement years and location.
  4. Read the case pages linked from the Highlighted Cases page.
  5. Match dockets to the Wisconsin plants in the scoped GEM export by name in the docket title
     (strong) or by name in the documents read three or more times.

Output, in batches/us-wi/harvest/: psc_dockets.json (read by build_state_brief.py --harvest; one entry
per docket) and psc_dockets.md. Nothing here stages a record and nothing here signs in.

Usage (from the repo root):
    python scopes/us-wi/harvest_psc.py                         # from 2021, read key documents
    python scopes/us-wi/harvest_psc.py --no-docs               # list dockets, download nothing
    python scopes/us-wi/harvest_psc.py --dockets 6630-CE-318   # only the named dockets
    python scopes/us-wi/harvest_psc.py --match-only batches/us-wi/harvest/psc_dockets.json
"""
import argparse
import datetime as dt
import html
import json
import re
import subprocess
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from fetch import CHROME_UA  # noqa: E402
from harvest_lib import (CSV, DOCKET_MAKER, DOCKET_SIZE, REPO, clean, clean_ws, docket_cache,  # noqa: E402
                         get, merge_facts, report_failure, sentences)

SITE = "https://apps.psc.wi.gov"
SEARCH = (SITE + "/ERF/ERFsearch/content/searchResult.aspx?UTIL={util}&CASE={case}&SEQ={seq}&START={start}"
          "&END={end}&TYPE=none&SERVICE={service}&KEY=none&NON=N&EXM=N")
DOWNLOAD = SITE + "/ERF/ERFview/viewdoc.aspx?docid={id}"
CITE = SITE + "/pages/viewdoc.htm?docid={id}"
CASE_INDEX = "https://psc.wi.gov/Pages/CommissionActions/HighlightedCases.aspx"
OUT = REPO / "batches" / "us-wi" / "harvest"
WORK = docket_cache("us-wi")
HEADERS = {"User-Agent": CHROME_UA, "Accept-Language": "en-US,en;q=0.9"}

# Case types read from the statewide lists: certificate of public convenience and necessity,
# certificate of authority, acquisition, business, tariff or service agreement, energy assessment.
CASE_TYPES = {"CE": "ELE", "CA": "ELE", "AE": "ELE", "BS": "none", "TE": "ELE", "ES": "none"}
CASE_LABEL = {"CE": "Certificate of public convenience and necessity", "CA": "Certificate of authority",
              "AE": "Acquisition", "BS": "Business or sale", "TE": "Tariff or service agreement",
              "ES": "Strategic Energy Assessment or electric system"}
# Utility numbers the plan names (5 is the joint docket series). Dairyland and WPPI file under their own
# numbers; add them with --utilities once confirmed.
UTILITIES = {"6630": "Wisconsin Electric Power Company", "6690": "Wisconsin Public Service", "6680": "Wisconsin Power and Light",
             "3270": "Madison Gas and Electric", "4220": "Northern States Power-Wisconsin", "5": "Joint dockets"}
# Dockets read whatever the lists show. Add one here when a lead names it.
KNOWN_DOCKETS = [
    "6630-CE-315", "6630-CE-316", "6630-CE-317", "6630-CE-318", "6630-CE-319", "5-CE-161", "5-CE-162",
    "9837-CE-100", "6630-BS-104", "9835-CE-100", "9698-CE-100", "9698-CE-101", "6680-TE-115",
]

# GEM plant -> regexes over a docket title (lower case) and, for a weaker match, the documents read.
PSC_KNOWN = {
    "L100000104267": [r"blount street"],
    "L100000104269": [r"edgewater"],
    "L100000104274": [r"elm road", r"oak creek (generating|power).*elm"],
    "L100000104276": [r"pulliam"],
    "L100000104279": [r"valley (power|generating|station)"],
    "L100000104280": [r"weston (generating|power|unit|plant|station)", r"\bweston\b.*(unit 4|conversion)"],
    "L100000104693": [r"port washington"],
    "L100000401577": [r"west campus"],
    "L100000401635": [r"sheboygan falls"],
    "L100000401640": [r"riverside (energy|generating|power|station)"],
    "L100000401676": [r"whitewater"],
    "L100000402073": [r"west marinette"],
    "L100000402381": [r"west marinette"],
    "L100000402253": [r"rockgen", r"rock gen"],
    "L100000402372": [r"concord (generating|power|station)"],
    "L100000402373": [r"germantown"],
    "L100000402374": [r"paris (generating|power|station)", r"paris combustion"],
    "L100000402376": [r"neenah"],
    "L100000402378": [r"de pere"],
    "L100000402379": [r"fox (energy|generating)"],
    "L100000409233": [r"wheaton"],
    "L100000409253": [r"weston (rice|reciprocating)"],
    "L100000409271": [r"french island"],
    "L100000407359": [r"nemadji"],
    "L100001025603": [r"south oak creek", r"oak creek.*(combustion turbine|lng)"],
    "L100001047775": [r"paris rice", r"paris.*reciprocating", r"paris.*internal combustion"],
    "L100001047813": [r"foundry ridge"],
    "L100001062057": [r"red oak ridge"],
    "L100001083378": [r"forest junction"],
    "L100001089647": [r"union depot"],
    "L100001089648": [r"fox north"],
    "L100001089674": [r"mount pleasant.*(data|microsoft)", r"microsoft"],
    "L100001089699": [r"vantage", r"lighthouse"],
}

NAME_NOISE = re.compile(
    r"\b(power station|power plant|generating station|generating|generation|facility|station|energy center|"
    r"energy|plant|power|wi|wisconsin|the|of|and|city|llc|inc|company|co|corp|corporation|combined|cycle|"
    r"county|industrial|park|campus|data|center|peaking|cogeneration|combustion|turbine|project)\b", re.I)
GEN = re.compile(r"generat|power plant|power station|energy center|certificate of (public convenience|authority)|"
                 r"capacity|turbine|combined[- ]cycle|simple[- ]cycle|peak|acqui|purchase of|resource plan|"
                 r"strategic energy|data cent|large load|retire|cogenerat|megawatt|\bMW\b|gas[- ]fired|"
                 r"natural gas|\bLNG\b|reciprocating|overhaul|conversion|fuel flexib|service agreement", re.I)
WIRES = re.compile(r"transmission|\bkv\b|substation|\bline\b|right[- ]of[- ]way|pipeline", re.I)
WIND_SOLAR = re.compile(r"\bwind\b|solar|photovoltaic|battery|storage|hydro", re.I)
GAS = re.compile(r"\bgas\b|turbine|combined[- ]cycle|simple[- ]cycle|peak|reciprocating|generating|"
                 r"power plant|energy center|power station|data cent|large load|strategic energy|resource plan|"
                 r"acqui|retire|capacity|\bLNG\b|overhaul|conversion|fuel flexib|service agreement", re.I)
TECH = re.compile(r"combined[- ]cycle|combustion turbine|simple[- ]cycle|peaking|reciprocating|internal combustion|"
                  r"aeroderivative|frame turbine|natural gas[- ]fired|gas[- ]fired|duct[- ]fir", re.I)
INSERVICE = re.compile(r"in[- ]service|commercial operation|\bCOD\b|placed in service|on[- ]line|begin operat|"
                       r"construction (will|to) (begin|start|commence)", re.I)
RETIRE = re.compile(r"retire|retirement|deactivat|mothball|cease operat|shut ?down|decommission", re.I)
LOCATION = re.compile(r"located (at|in|on|near|approximately)|site (is|in|at)|county,? wisconsin|"
                      r"\bsection \d+|township \d+|range \d+|\bT\d{1,2}N\b|latitude|longitude", re.I)
LATLON = re.compile(r"\b(4[2-7]\.\d{3,})\s*[,;/ ]\s*-?\s*(8[7-9]\.\d{3,}|9[0-2]\.\d{3,})\b")
DOC_PRIORITY = re.compile(r"application|engineering plan|final decision|decision|order|testimony|environmental|"
                          r"data request|response|summary|exhibit|resource plan|assessment|agreement", re.I)
DOC_SKIP = re.compile(r"notice of (appearance|proceeding|hearing|investigation)|certificate of service|affidavit|"
                      r"proof of publication|transcript|public comment|comment from|letter from (a )?(member|citizen)|"
                      r"cover letter|intervene|withdraw|waiver|protective|errata only|sign[- ]?up|"
                      r"customer (comment|letter)|notice of (filing|assignment)", re.I)
READABLE = {"PDF", "DOCX", "DOC"}


def log(msg):
    print(f"[psc-wi] {msg}", file=sys.stderr, flush=True)


def split_docket(d):
    """'6630-CE-318' -> ('6630', 'CE', '318'), or None."""
    m = re.fullmatch(r"(\d{1,5})-([A-Z]{2})-(\d{1,4})", str(d).strip())
    return m.groups() if m else None


def us_date(s):
    """'11/16/2026 11:11:00 AM' to 2026-11-16, or ''."""
    m = re.search(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b", s or "")
    return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}" if m else ""


def words(text):
    t = NAME_NOISE.sub(" ", re.sub(r"\(.*?\)", " ", str(text or "")))
    return {w.lower() for w in re.split(r"[^A-Za-z]+", t) if len(w) >= 4}


def size_bytes(s):
    m = re.search(r"([\d.,]+)\s*(KB|MB|GB|bytes)", s or "", re.I)
    if not m:
        return 0
    return int(float(m.group(1).replace(",", "")) * {"bytes": 1, "kb": 1e3, "mb": 1e6, "gb": 1e9}[m.group(2).lower()])


# ------------------------------------------------------------------ parsers ---

def parse_title(page):
    """(docket, title) from the Search Criteria box of a one-docket page, or ('', '')."""
    m = re.search(r"Docket ID:</b></td><td[^>]*>(.*?)</td>", page or "", re.S)
    if not m:
        return "", ""
    parts = [clean(p) for p in re.split(r"<br\s*/?>", m.group(1)) if clean(p)]
    docket = parts[0] if parts else ""
    title = " ".join(parts[1:]).strip()
    title = re.sub(r"^\((.*)\)$", r"\1", title).strip()
    return docket, title


def parse_total(page):
    m = re.search(r"Total Return:\s*([\d,]+)\s*rows", page or "")
    return int(m.group(1).replace(",", "")) if m else 0


def _field(block, ident):
    m = re.search(rf'id="lv_data_{ident}_\d+"[^>]*>(.*?)</span>', block, re.S)
    return m.group(1) if m else ""


def _hidden(block, ident):
    m = re.search(rf'id="lv_data_{ident}_\d+"\s+value="([^"]*)"', block)
    return html.unescape(m.group(1)).strip() if m else ""


def parse_filings(page):
    """Rows of the filing table: PSC reference, description, type, received date, format, size,
    class (P public, C confidential) and whether a download link exists. Filer names and e-mail
    addresses are not kept."""
    out = []
    for block in re.split(r'<tr class="(?:row|altrow|alt)"', page or "")[1:]:
        block = block.split("</tr>")[0]
        doc_id = clean(_field(block, "lbl_doc_id"))
        if not doc_id.isdigit():
            continue
        desc_html = _field(block, "lbl_doc_desc_txt")
        out.append({
            "doc_id": doc_id,
            "description": re.sub(r"\s*\([\d.,]+ (?:KB|MB|GB|bytes)\)\s*$", "", clean_ws(clean(desc_html))),
            "has_link": "viewdoc" in desc_html,
            "doc_type": clean(_field(block, "lbl_doc_type_desc_txt")),
            "docket": clean(_field(block, "lbl_docket_or_util")),
            "received": us_date(clean(_field(block, "lbl_doc_recv_dt"))),
            "format": _hidden(block, "hdf_doc_format").upper(),
            "class": _hidden(block, "hdf_doc_class_cd").upper(),
            "in_camera": _hidden(block, "hdf_in_camera_ind") == "Y",
            "paper": _hidden(block, "hdf_papr_doc_ind") == "Y",
            "bytes": size_bytes(_hidden(block, "hdf_doc_file_size_amt")),
        })
    return out


def parse_docket_list(page):
    """Sorted docket numbers named in a statewide filing list."""
    return sorted(set(re.findall(r"dockt_id=(\d{1,5}-[A-Z]{2}-\d{1,4})", page or "")))


def parse_case_links(page):
    """Absolute addresses of the case pages linked from the Highlighted Cases page."""
    t = html.unescape(page or "")
    found = re.findall(r'href="([^"]*?/CasePages/[A-Za-z0-9_\-]+\.aspx)"', t)
    out = []
    for u in found:
        u = re.sub(r":443", "", u)
        u = u if u.startswith("http") else "https://psc.wi.gov" + u
        if u not in out:
            out.append(u)
    return out


def parse_case_page(page):
    """Docket id(s), title and the application summary text of one case page."""
    text = clean_ws(clean(page).replace("\u200b", ""))
    m = re.search(r"Docket ID:\s*(\d{1,5}-[A-Z]{2}-\d{1,4})\s*(.*?)\s*(?:View and Download|Related Dockets|Jump to Section)", text)
    related = re.findall(r"\b\d{1,5}-[A-Z]{2}-\d{1,4}\b", (re.search(r"Related Dockets:(.*?)Jump to", text) or [None, ""])[1])
    summ = re.search(r"Application Summary\s*Overview\s*(.*?)(?:Application Documents|Case Contacts|Public Participation)", text)
    return {"docket": m.group(1) if m else "", "title": clean_ws(m.group(2)) if m else "",
            "related": related, "summary": clean_ws(summ.group(1))[:2500] if summ else ""}


def utility_of(title):
    m = re.search(r"(?:Pre-)?Application of (?:the )?(.+?)(?:,? (?:for|to|requesting|seeking|pursuant)\b|$)", title or "", re.I)
    return clean_ws(m.group(1)).strip(" ,") if m else ""


# -------------------------------------------------------------------- fetch ---

class Erf:
    """The ERF site. A browser User-Agent and Accept-Language are what it needs."""

    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update(HEADERS)
        self.failed = []

    def page(self, url, timeout=600, retries=2):
        """Text of a page, or None. A short body (the 404 error page) falls back to fetch.py's ladder."""
        for i in range(retries + 1):
            try:
                r = self.s.get(url, timeout=timeout)
                if r.status_code == 200 and len(r.content) > 3000:
                    return r.text
            except requests.RequestException as e:
                log(f"retry {i + 1}: {str(e)[:80]}")
            time.sleep(3 * (i + 1))
        res = get(url, timeout=300)
        if res.status == "200" and len(res.text) > 3000:
            return res.text
        self.failed.append(url)
        report_failure(url, res.status, "ERF page")
        return None

    def docket(self, docket):
        p = split_docket(docket)
        if not p:
            return None
        return self.page(SEARCH.format(util=p[0], case=p[1], seq=p[2], start="none", end="none", service="none"))

    def list_window(self, util, case, start, end, service):
        return self.page(SEARCH.format(util=util, case=case, seq=0, start=start, end=end, service=service), timeout=900)

    def download(self, doc_id, dest, max_bytes):
        """Save a document; True when real bytes came back (not the HTML error page)."""
        url = DOWNLOAD.format(id=doc_id)
        try:
            r = self.s.get(url, timeout=300, stream=True)
            ctype = r.headers.get("content-type", "")
            if r.status_code != 200 or "html" in ctype.lower():
                report_failure(url, r.status_code, f"not a document ({ctype[:40]})")
                return False
            data = b""
            for chunk in r.iter_content(1 << 20):
                data += chunk
                if len(data) > max_bytes:
                    return False
            dest.write_bytes(data)
            return True
        except requests.RequestException as e:
            report_failure(url, "000", str(e)[:120])
            return False


def collect_dockets(erf, from_year, today, cases, utilities, extra):
    """Docket numbers from the statewide lists (one window per year and case type), each utility's own
    list and the hand list."""
    found, failed = set(extra), []
    for case in cases:
        for year in range(from_year, today.year + 1):
            end = f"{year}-12-31" if year < today.year else today.isoformat()
            cache = WORK / "lists" / f"{case}-{year}.json"
            if cache.exists() and year < today.year:
                found.update(json.loads(cache.read_text()))
                continue
            page = erf.list_window(0, case, f"{year}-01-01", end, CASE_TYPES.get(case, "none"))
            if page is None:
                failed.append(f"{case} {year}")
                continue
            nums = parse_docket_list(page)
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_text(json.dumps(nums))
            found.update(nums)
            log(f"list {case} {year}: {len(nums)} dockets")
    for util in utilities:
        for case in cases:
            page = erf.list_window(util, case, f"{from_year}-01-01", "none", "none")
            if page is None:
                failed.append(f"utility {util} {case}")
                continue
            found.update(parse_docket_list(page))
    return sorted(found), failed


def docket_record(erf, docket):
    """Title and filing table of one docket, cached as search.json."""
    folder = WORK / docket
    cache = folder / "search.json"
    if cache.exists() and docket not in KNOWN_DOCKETS:
        return json.loads(cache.read_text())
    page = erf.docket(docket)
    if page is None:
        return None
    _, title = parse_title(page)
    rec = {"docket": docket, "title": title, "total": parse_total(page), "filings": parse_filings(page),
           "fetched": dt.date.today().isoformat()}
    folder.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(rec))
    time.sleep(0.3)
    return rec


# ----------------------------------------------------------------- classify ---

def classify(d):
    """(relevant, key, reasons): relevant = about generation, a data center load, a resource assessment;
    key = one whose documents are read (not only wires, wind or solar)."""
    title = d.get("title", "")
    reasons = []
    if d["docket"] in KNOWN_DOCKETS:
        reasons.append("on the hand-checked list")
    if GEN.search(title):
        reasons.append("its title is about generation, a plant, an acquisition or a large load")
    wires_only = bool(WIRES.search(title)) and not re.search(
        r"generat|power plant|station|energy center|turbine|resource plan|strategic energy", title, re.I)
    ws_only = bool(WIND_SOLAR.search(title)) and not re.search(r"\bgas\b|turbine|combined|peak|generating station|reciprocating", title, re.I)
    relevant = bool(reasons)
    key = d["docket"] in KNOWN_DOCKETS or (bool(GEN.search(title)) and bool(GAS.search(title)) and not wires_only and not ws_only)
    return relevant, key, reasons


# ------------------------------------------------------------------- facts ---

# Boilerplate that is never a plant fact: filing headers, service lists, notices, noise and flood studies.
FACT_JUNK = re.compile(r"PSC REF#|RECEIVED:|Post Office Box|Secretary to the Commission|certificate of service|service list|"
                       r"notice of (investigation|proceeding|hearing|comment|appearance|filing|assignment)|"
                       r"sound (level|survey)|noise (survey|study)|measurement points?|flood ?plain|\bTables? \d-\d|"
                       r"Docket \d{1,4}-[A-Z]{2}-\d+\s*$|please (contact|direct)|sincerely|\bpage \d+ of \d+", re.I)
PLACE = re.compile(r"\b(City|Town|Village|Township|County) of [A-Z]|\b[A-Z][a-z]+ County\b|"
                   r"\b\d{2,5} [A-Z][\w.]*( [A-Z][\w.]*)? (Road|Rd|Street|St|Avenue|Ave|Drive|Dr|Highway|Hwy|Lane|Way|Boulevard)\b|"
                   r"\bsection \d+|township \d+|range \d+|\bT\d{1,2}N\b|latitude|longitude", re.I)
SITE_CUE = re.compile(r"\b(site|located|plant|station|facility|project|campus|generating|unit)\b", re.I)
EQUIP = re.compile(r"\b(units?|turbines?|engines?|CTs?|generators?|plant|station|facility|project|coal|boilers?)\b", re.I)
COST = re.compile(r"\$\s?\d[\d,.]*(\s?(million|billion))?", re.I)
COST_CUE = re.compile(r"cost|capital|estimated|budget|price|investment", re.I)
OWNER = re.compile(r"\b(owned|operated|developed|applicant|applies|seeks authority|requests authority|joint(ly)? own|acquire[sd]?|"
                   r"purchase[sd]? (of|a|the)|will own|ownership)\b", re.I)


def pick(text, rx, limit, lo=20, hi=420, need=None, drop=FACT_JUNK):
    """The first `limit` sentences that match `rx` and `need`, never boilerplate, never a repeat across a list."""
    out = []
    for s in sentences(text):
        if rx.search(s) and lo < len(s) < hi and s not in out and not (drop and drop.search(s)) and (need is None or need.search(s)):
            out.append(s)
            if len(out) >= limit:
                break
    return out


def doc_facts(text):
    """Sentences that state plant facts: size, equipment, fuel, dates, cost, owner and place. Boilerplate is dropped."""
    yr = r"(?:.*\b20[2-5]\d\b|\b20[2-5]\d\b.*)"   # grouped: a bare alternation let a year alone match
    cue = EQUIP
    facts = {
        "technology": sorted({m.group(0).lower() for m in TECH.finditer(text)})[:8],
        "equipment_maker_model": pick(text, DOCKET_MAKER, 8, need=re.compile(r"\b[A-Z]{2,}\b|\d")),
        "megawatts": pick(text, DOCKET_SIZE, 10),
        "in_service": pick(text, re.compile(f"({INSERVICE.pattern}){yr}({INSERVICE.pattern})?", re.I), 6, need=re.compile(EQUIP.pattern + r"|commercial operation|construction", re.I)),
        "retirement": pick(text, re.compile(f"({RETIRE.pattern}){yr}({RETIRE.pattern})?", re.I), 8, need=cue),
        "location": pick(text, LOCATION, 6, need=re.compile(PLACE.pattern, re.I)),
        "cost": pick(text, COST, 6, need=COST_CUE),
        "owner": pick(text, OWNER, 4, need=re.compile(r"\b(LLC|Inc\.?|Company|Corporation|Cooperative|Energy|Power|Electric|Utilit\w+)\b")),
        "coords": [f"{a}, -{b.lstrip('-')}" for a, b in LATLON.findall(text)][:3],
    }
    return facts


def pdf_text(path):
    """Plain text of a PDF; a scanned one goes through OCR."""
    t = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True).stdout
    if len(t.strip()) < 300:
        import fetch
        try:
            ocr = fetch._pdf_ocr(str(path))
        except Exception:  # noqa: BLE001
            ocr = ""
        if len(ocr.strip()) > len(t.strip()):
            t = ocr
    return t


def docx_text(path):
    try:
        import docx
        d = docx.Document(str(path))
        parts = [p.text for p in d.paragraphs]
        for tb in d.tables:
            for row in tb.rows:
                parts.append(" | ".join(c.text for c in row.cells))
        return "\n".join(parts)
    except Exception:  # noqa: BLE001
        return ""


def file_text(path, fmt):
    head = Path(path).read_bytes()[:5]
    if head == b"%PDF-":
        return pdf_text(path)
    if head[:2] == b"PK" and fmt in ("DOCX", "DOC"):
        return docx_text(path)
    return ""


def pick_docs(filings, cap, max_bytes):
    """The filings most likely to hold facts: the application, engineering plan, decision, testimony and
    data request answers, the earliest filing and larger files first. Never confidential or in-camera
    filings, never a format that is not text, never above the size cap, never appearances or notices."""
    scored = []
    for f in filings:
        name = f"{f['description']} {f['doc_type']}"
        if (not f["has_link"] or f["class"] == "C" or f["in_camera"] or f["paper"] or f["format"] not in READABLE
                or f["bytes"] > max_bytes or DOC_SKIP.search(name)):
            continue
        s = 4 if DOC_PRIORITY.search(name) else 0
        s += 3 if re.search(r"application|engineering plan", name, re.I) else 0
        s += 3 if re.search(r"final decision|\border\b", name, re.I) else 0
        scored.append((-s, -f["bytes"], f["received"], f["doc_id"], f))
    return [x[-1] for x in sorted(scored, key=lambda x: x[:4])[:cap]]


def read_docket(erf, d, rec, cap, max_bytes):
    folder = WORK / d["docket"]
    folder.mkdir(parents=True, exist_ok=True)
    docs, parts = [], []
    for f in pick_docs(rec["filings"], cap, max_bytes):
        txt = folder / f"{f['doc_id']}.txt"
        text = txt.read_text(errors="replace") if txt.exists() else ""
        if not text:
            raw = folder / f"{f['doc_id']}.{f['format'].lower()}"
            if raw.exists() or erf.download(f["doc_id"], raw, max_bytes):
                text = file_text(raw, f["format"])
            if text.strip():
                txt.write_text(text)
        out = {"doc_id": f["doc_id"], "title": f["description"][:200], "kind": f["doc_type"], "date": f["received"],
               "url": CITE.format(id=f["doc_id"]), "format": f["format"],
               "saved": str(txt.relative_to(REPO)) if text.strip() else "", "read": len(text.strip()) >= 300}
        if out["read"]:
            out["facts"] = doc_facts(text)
            parts.append(out["facts"])
        docs.append(out)
        time.sleep(0.3)
    return docs, merge_facts(parts)


# -------------------------------------------------------------------- match ---

def match_docket(plant, d, others_by_title=False):
    """How a docket matches a plant, or None: the plant's name in the title (strong), or in the
    documents read three or more times (six when the title already names another plant)."""
    head = f"{d.get('title', '')} {d.get('utility', '')}".lower()
    pats = PSC_KNOWN.get(plant["id"])
    if not pats:
        ws = plant["name_words"]
        return "name words in the docket title, check it is this plant" if ws and ws <= words(head) else None
    if any(re.search(p, head, re.I) for p in pats):
        return "name in the docket title"
    body = d.get("text_blob", "")
    n = sum(len(re.findall(p, body, re.I)) for p in pats)
    if n >= (6 if others_by_title else 3):
        return f"named {n} times in the documents read"
    return None


def match_all(plants, dockets):
    by_plant = {p["id"]: [] for p in plants}
    matched = set()
    for d in dockets:
        d["matched"] = []
        titled = any(match_docket(p, {**d, "text_blob": ""}) for p in plants)
        for p in plants:
            how = match_docket(p, d, others_by_title=titled)
            if how:
                d["matched"].append({"plant_id": p["id"], "plant": p["name"], "how": how})
                by_plant[p["id"]].append(d["docket"])
                matched.add(d["docket"])
    return by_plant, matched


def load_plants(csv_path=None):
    import pandas as pd
    df = pd.read_csv(csv_path or CSV, low_memory=False, encoding="utf-8-sig")
    df = df[df["State/Province"] == "Wisconsin"]
    plants = []
    for pid, rows in df.groupby("GEM location ID", sort=False):
        r = rows.iloc[0]
        city = r.get("City") if isinstance(r.get("City"), str) else ""
        county = r.get("Local area (taluk, county)")
        plants.append({"id": pid, "name": r["Plant name"], "city": city,
                       "county": re.sub(r"\s+county$", "", county.strip(), flags=re.I) if isinstance(county, str) else "",
                       "statuses": sorted(set(rows["Status"].astype(str))), "name_words": words(r["Plant name"])})
    return plants


# ------------------------------------------------------------------- output ---

def docket_block(d, full=True):
    L = [f"- **{d['docket']}**, {d.get('utility') or 'applicant not shown'}: {(d.get('title') or 'title not read')[:300]}",
         f"  - {d.get('relief_type') or 'type not shown'}; first filing {d.get('filed') or 'unknown'}"
         + (f"; {d['filings_listed']} filings listed" if d.get("filings_listed") else "") + f"; link {d['url']}"]
    if full and d.get("facts"):
        f = d["facts"]
        for k, label in [("technology", "Technology"), ("megawatts", "Megawatts"), ("equipment_maker_model", "Equipment"),
                         ("in_service", "In service"), ("retirement", "Retirements"), ("location", "Location"),
                         ("coords", "Coordinates")]:
            if f.get(k):
                L.append(f"  - {label}: " + " | ".join(f[k][:4]))
    for doc in d.get("documents", []):
        L.append(f"  - {'read' if doc.get('read') else 'not read'}: {doc['title'][:100]} ({doc['kind']}, {doc['date']}): {doc['url']}")
    return L


def write_outputs(out_dir, plants, dockets, by_plant, matched, sources, today, from_year, case_pages):
    out_dir.mkdir(parents=True, exist_ok=True)
    slim = [{k: v for k, v in d.items() if k != "text_blob"} for d in dockets]
    unmatched = [d for d in dockets if d.get("key") and d["docket"] not in matched]
    data = {"generated": today, "from_year": from_year, "sources": sources, "dockets": slim, "case_pages": case_pages,
            "by_plant": by_plant, "unmatched_generation": [d["docket"] for d in unmatched]}
    (out_dir / "psc_dockets.json").write_text(json.dumps(data, indent=1, default=str))
    by_id = {d["docket"]: d for d in dockets}
    L = [f"# Public Service Commission of Wisconsin dockets on generation ({today})", "",
         f"Dockets with a filing from {from_year} on, plus the hand-checked list. A document's "
         "apps.psc.wi.gov/pages/viewdoc.htm address is a stable public link and can be cited. "
         "Copies of documents read are in scopes/us-wi/work/psc/ and are not committed.", "", "## Sources", ""]
    L += [f"- {s['name']}: {s['how']} ({s['url']})" for s in sources]
    L += ["", "## Matched to GEM plants", ""]
    for p in plants:
        L += [f"### {p['name']} ({p['id']}), {p['city'] or 'city blank'}, {p['county'] or 'county blank'} County", ""]
        ids = by_plant.get(p["id"], [])
        if not ids:
            L += ["No docket matched.", ""]
            continue
        for k in ids:
            d = by_id[k]
            L += docket_block(d)
            L.append(f"  - Match: {next(m['how'] for m in d['matched'] if m['plant_id'] == p['id'])}")
        L.append("")
    L += ["## Generation dockets that match no GEM plant (possible new plants, uprates or retirements)", ""]
    for d in sorted(unmatched, key=lambda x: x["docket"]):
        L += docket_block(d)
    L += ["", "## Other generation-related dockets (lines, wind, solar; not read)", ""]
    for d in sorted((d for d in dockets if d.get("relevant") and not d.get("key")), key=lambda x: x["docket"]):
        L += docket_block(d, full=False)
    L += ["", "## Case pages", ""]
    for c in case_pages:
        L.append(f"- {c['url']}: {c.get('docket') or 'docket not shown'}, {c.get('title', '')[:240]}")
        if c.get("summary"):
            L.append(f"  - Summary: {c['summary'][:700]}")
    (out_dir / "psc_dockets.md").write_text("\n".join(L) + "\n")
    return unmatched


# --------------------------------------------------------------------- main ---

def read_case_pages(erf):
    idx = erf.page(CASE_INDEX, timeout=120, retries=1)
    out = []
    for u in (parse_case_links(idx) if idx else []):
        page = erf.page(u, timeout=120, retries=1)
        if page:
            out.append({"url": u, **parse_case_page(page)})
            time.sleep(0.3)
    return out, bool(idx)


def main():
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    ap.add_argument("--from-year", type=int, default=2021)
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--cases", default=",".join(CASE_TYPES), help="comma-separated case types for the statewide lists")
    ap.add_argument("--utilities", default=",".join(UTILITIES), help="comma-separated utility numbers for their own lists")
    ap.add_argument("--dockets", help="comma-separated dockets only (skips the statewide lists)")
    ap.add_argument("--docs-per-docket", type=int, default=10)
    ap.add_argument("--max-mb", type=float, default=60, help="skip filings larger than this")
    ap.add_argument("--no-docs", action="store_true", help="list dockets, download nothing")
    ap.add_argument("--no-case-pages", action="store_true")
    ap.add_argument("--match-only", metavar="JSON", help="re-match a saved psc_dockets.json, no network")
    a = ap.parse_args()
    plants = load_plants()
    today = dt.date.today()
    if a.match_only:
        saved = json.loads(Path(a.match_only).read_text())
        dockets = saved["dockets"]
        for d in dockets:
            d["text_blob"] = " ".join(x for doc in d.get("documents", []) for v in (doc.get("facts") or {}).values() for x in v)
        by_plant, matched = match_all(plants, dockets)
        write_outputs(Path(a.out), plants, dockets, by_plant, matched, saved["sources"], today.isoformat(),
                      saved.get("from_year", a.from_year), saved.get("case_pages", []))
        return

    erf = Erf()
    if a.dockets:
        numbers, list_failed = sorted(set(a.dockets.split(","))), []
    else:
        numbers, list_failed = collect_dockets(erf, a.from_year, today, [c for c in a.cases.split(",") if c],
                                               [u for u in a.utilities.split(",") if u], KNOWN_DOCKETS)
    log(f"{len(numbers)} dockets to title")
    dockets, title_failed = [], []
    for n in numbers:
        rec = docket_record(erf, n)
        if rec is None:
            title_failed.append(n)
            continue
        dates = sorted(f["received"] for f in rec["filings"] if f["received"])
        d = {"docket": n, "utility": utility_of(rec["title"]), "title": rec["title"],
             "relief_type": CASE_LABEL.get(n.split("-")[1], ""), "filed": dates[0] if dates else "",
             "last_filing": dates[-1] if dates else "", "filings_listed": rec["total"],
             "url": SEARCH.format(util=split_docket(n)[0], case=split_docket(n)[1], seq=split_docket(n)[2],
                                  start="none", end="none", service="none")}
        d["relevant"], d["key"], d["reasons"] = classify(d)
        if not d["key"] and any(match_docket(p, {**d, "text_blob": ""}) for p in plants) and not WIRES.search(d["title"]):
            d["relevant"] = d["key"] = True
            d["reasons"].append("its title names a GEM plant")
        d["_rec"] = rec
        if d["relevant"]:
            dockets.append(d)
    log(f"{len(dockets)} generation related; {sum(1 for d in dockets if d['key'])} key")

    for d in dockets:
        rec = d.pop("_rec")
        d["documents"], d["facts"], d["text_blob"] = [], {}, ""
        if not d["key"] or a.no_docs:
            continue
        log(f"reading {d['docket']}: {d['title'][:90]}")
        d["documents"], d["facts"] = read_docket(erf, d, rec, a.docs_per_docket, int(a.max_mb * 1e6))
        folder = WORK / d["docket"]
        d["text_blob"] = " ".join(p.read_text(errors="replace") for p in sorted(folder.glob("*.txt"))) if folder.exists() else ""

    case_pages, idx_ok = ([], True) if a.no_case_pages else read_case_pages(erf)
    sources = [
        {"name": "PSC ERF statewide filing lists", "url": SITE + "/ERF/ERFsearch/",
         "how": f"case types {a.cases} from {a.from_year}" + (f"; windows that did not answer: {', '.join(list_failed)}" if list_failed else "")},
        {"name": "PSC ERF docket pages", "url": SITE + "/ERF/ERFsearch/",
         "how": f"{len(numbers) - len(title_failed)} of {len(numbers)} docket titles and filing tables read"
                + (f"; did not answer: {', '.join(title_failed[:20])}" if title_failed else "")},
        {"name": "PSC ERF documents", "url": SITE + "/ERF/ERFview/",
         "how": f"up to {a.docs_per_docket} filings read per key docket" if not a.no_docs else "skipped"},
        {"name": "PSC case pages", "url": CASE_INDEX,
         "how": f"{len(case_pages)} pages read" if idx_ok else "the Highlighted Cases page did not answer"}]
    by_plant, matched = match_all(plants, dockets)
    unmatched = write_outputs(Path(a.out), plants, dockets, by_plant, matched, sources, today.isoformat(), a.from_year, case_pages)
    log(f"{len(matched)} dockets matched to plants; {len(unmatched)} key dockets unmatched")


if __name__ == "__main__":
    main()

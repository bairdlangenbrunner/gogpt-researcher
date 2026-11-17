"""
Harvest Kentucky Public Service Commission cases on generation before a research sweep.

The commission rules on every certificate of public convenience and necessity
for a new unit, every retirement, every integrated resource plan and every
large load or data center contract of Kentucky Power, East Kentucky Power
Cooperative, Big Rivers, LG&E and KU and Duke Energy Kentucky. Merchant plants
and municipal utilities go to the State Board on Electric Generation and
Transmission Siting, whose cases are kept on the same site. Nothing needs a
sign-in. What was found (2026-11-04):

  1. A whole-year case list per year, https://psc.ky.gov/Case/searchCases/<year>:
     one row per case with the case number, service type, filing date,
     category, utilities and the case title ("ELECTRONIC APPLICATION OF ... FOR
     CERTIFICATES OF PUBLIC CONVENIENCE AND NECESSITY ..."). No RSS.
  2. A filings page per case, https://psc.ky.gov/Case/ViewCaseFilings/<case>:
     the case information, then one table row per filing with its date, its
     description and open PDF links (psc.ky.gov/pscecf/... for electronic
     filings, psc.ky.gov/pscscf/... for commission orders and letters). A PDF
     address is what a note cites.
  3. Three sibling tabs on the same address plus /Post (construction notices
     and other filings after the final order), /Public (public comments) and
     /Hearings (hearing video links with dates). Public comments name members
     of the public, so only their count and the newest date are kept.
  ViewCaseDetails redirects and the search form's POST answers 500; the year
  list is the way in.

Steps:
  1. Read the year lists from --from-year (cached in scopes/us-ky/work/psc/; the
     current year is fetched again) and keep electric and siting board cases
     whose titles are about generation, a resource plan, a retirement or a
     large load, plus the hand-checked list KNOWN_CASES.
  2. For each kept case read the filings page and the Post, Hearings and
     Public tabs.
  3. For a key case (about gas or generation, not only wires, wind or solar),
     download the application, testimony, orders, resource plans and every
     Post filing (capped, newest first after the application) into
     scopes/us-ky/work/psc/<case>/ (not committed) and keep the lines that give
     technology, megawatts, maker and model, in-service and retirement years
     and location.
  4. Match cases to the Kentucky plants in the scoped GEM export: the
     hand-checked list, a plant's name in the case title (strong), or in the
     documents read three or more times.

Output, in batches/us-ky/harvest/: psc_dockets.json (read by
build_state_brief.py --harvest; one entry per case, "docket" is the case
number) and psc_dockets.md. Filer names are not kept. Nothing here stages a
record.

Usage (from the repo root):
    python scopes/us-ky/harvest_psc.py                     # from 2021, read key documents
    python scopes/us-ky/harvest_psc.py --no-docs           # list cases, download nothing
    python scopes/us-ky/harvest_psc.py --cases 2024-00370  # only these cases
    python scopes/us-ky/harvest_psc.py --match-only batches/us-ky/harvest/psc_dockets.json
"""
import argparse
import datetime as dt
import html
import json
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from fetch import CHROME_UA  # noqa: E402
from harvest_lib import (DOCKET_MAKER, DOCKET_SIZE, REPO, clean_ws, docket_cache,  # noqa: E402
                         merge_facts, report_failure, sentences)

from paths import load_scope_module  # noqa: E402

_permits = load_scope_module("us-ky", "harvest_permits")
load_plants, words = _permits.load_plants, _permits.words

SITE = "https://psc.ky.gov"
YEAR_LIST = SITE + "/Case/searchCases/{year}"
CASE = SITE + "/Case/ViewCaseFilings/{case}"
OUT = REPO / "batches" / "us-ky" / "harvest"
WORK = docket_cache("us-ky")

# Cases read whatever the year lists say, with the GEM plants each is about (hand-checked
# 2026-11-04). An empty list means the case is read and matched by name.
KNOWN_CASES = {
    "2024-00370": ["L100000103935"],                    # EKPC new generation, Cooper combined cycle
    "2024-00310": ["L100001025720"],                    # EKPC Liberty Station
    "2025-00045": ["L100000103945", "L100000103937"],   # LG&E and KU, Mill Creek 6 and Brown 12
    "2026-00324": ["L100001062558"],                    # Kentucky Power, Lawrence County combined cycle
    "2026-00103": ["L100001062558"],                    # Kentucky Power, withdrawn
    "2023-00092": ["L100001062558", "L100000103930"],   # Kentucky Power 2023 resource plan
    "2026-00291": ["L100000103947", "L100000103943"],   # Big Rivers, Reid turbine retirement, Green backup fuel
    "2026-00268": ["L100001062552"],                    # Big Rivers 2026 resource plan
    "2023-00310": ["L100001062552"],                    # Big Rivers 2023 resource plan
    "2021-00079": ["L100000103943"],                    # Big Rivers, Green conversion to gas
    "2024-00197": ["L100000103938"],                    # Duke Energy Kentucky resource plan
    "2024-00326": [],                                   # LG&E and KU resource plan
    "2025-00087": [],                                   # EKPC resource plan
    "2026-00167": [],
    "2025-00140": [],                                   # EKPC data center tariff
    "2026-00115": [],                                   # TeraWulf, Justified Datapower
    "2026-00323": [],                                   # TeraWulf, DB Long Hunts Data
    "2025-00415": [],                                   # EKPC certificate case
    "2023-00312": [],
}

# GEM plant -> regexes over a case's title and documents (lower case).
PSC_KNOWN = {pid: list(v.get("names", [])) for pid, v in _permits.KNOWN.items()}
for pid, pats in {
    "L100000103935": [r"\bcooper\b"], "L100000103937": [r"\bbrown\b"], "L100000103938": [r"east bend"],
    "L100000103943": [r"\bgreen station\b", r"\bgreen (unit|plant|generating)"], "L100000103947": [r"\breid\b"],
    "L100000103930": [r"big sandy"], "L100000401893": [r"\bsmith station\b", r"j\.? ?k\.? smith"],
    "L100000103939": [r"elmer smith", r"green river east"], "L100001025720": [r"liberty station"],
    "L100000401892": [r"\bbluegrass (generating|station|plant)"], "L100001026095": [r"kymea"],
    "L100000103950": [r"spurlock"], "L100000103951": [r"trimble county (station|generating|unit|plant)"],
}.items():
    PSC_KNOWN.setdefault(pid, [])
    PSC_KNOWN[pid] = list(dict.fromkeys(PSC_KNOWN[pid] + pats))

SERVICE_KEEP = re.compile(r"electric|siting|generation", re.I)
GEN = re.compile(r"generat|power plant|certificate(s)? of public convenience|\bCPCN\b|site compatibility|"
                 r"construction certificate|merchant|capacity|turbine|combined[- ]cycle|simple[- ]cycle|peak|"
                 r"acqui|purchase of .{0,60}(facilit|plant|station)|integrated resource|\bIRP\b|resource plan|"
                 r"request for proposal|\bRFP\b|data cent|large load|high load factor|\bEHLF\b|retire|"
                 r"cogenerat|megawatt|\bMW\b|energy center|power station|\bgas[- ]fired|special contract", re.I)
WIRES = re.compile(r"transmission|\bkv\b|substation|\bline\b|right[- ]of[- ]way", re.I)
WIND_SOLAR = re.compile(r"\bwind\b|solar|photovoltaic|battery|storage", re.I)
GAS = re.compile(r"\bgas\b|turbine|combined[- ]cycle|simple[- ]cycle|peak|reciprocating|generat|"
                 r"power plant|energy center|power station|data cent|large load|high load factor|resource plan|"
                 r"integrated resource|\bIRP\b|request for proposal|\bRFP\b|convenience|site compatibility|"
                 r"construction certificate|acqui|retire|capacity|special contract", re.I)
TECH = re.compile(r"combined[- ]cycle|combustion turbine|simple[- ]cycle|peaking|reciprocating|internal combustion|"
                  r"aeroderivative|frame turbine|natural gas[- ]fired|gas[- ]fired|duct[- ]fir|co-?fir|"
                  r"gas conversion|convert(ed|ing)? to (natural )?gas", re.I)
INSERVICE = re.compile(r"in[- ]service|commercial operation|\bCOD\b|placed in service|on[- ]line|begin operat|"
                       r"commence(ment of)? construction|construction (will|to) (begin|start|commence)", re.I)
RETIRE = re.compile(r"retire|retirement|deactivat|mothball|cease operat|shut ?down|decommission", re.I)
LOCATION = re.compile(r"located (at|in|on|near|approximately)|site (is|in|at)|county,? kentucky|"
                      r"latitude|longitude|acres? (site|parcel|tract)", re.I)
LATLON = re.compile(r"\b(3[6-9]\.\d{3,})[\s,;/°N-]{1,12}(8[2-9]\.\d{3,})\b")
DOC_PRIORITY = re.compile(r"application|testimony|order|report|settlement|stipulation|exhibit|"
                          r"resource plan|\bIRP\b|request for proposal|\bRFP\b|supplement|read.?first|"
                          r"notice of intent|construction|commencement|siting|site assessment", re.I)
DOC_SKIP = re.compile(r"appearance|certificate_of_service|affidavit|proof_of_publication|transcript|"
                      r"motion_(for|to)_(confidential|intervene|withdraw|deviat|extend|leave)|confidential|\bCONF\b|"
                      r"petition_for_confidential|exhibit_list|witness_list|hearing_video|"
                      r"cover_letter|letter_of_counsel", re.I)


def log(msg):
    print(f"[harvest-ky-psc] {msg}", file=sys.stderr, flush=True)


def iso(s):
    m = re.search(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b", str(s or ""))
    if m:
        return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}"
    try:
        return dt.datetime.strptime(clean_ws(s), "%b %d, %Y").date().isoformat()
    except (TypeError, ValueError):
        return ""


def text_of(fragment):
    return clean_ws(html.unescape(re.sub(r"<[^>]+>", " ", fragment or "")))


def abs_url(href):
    href = html.unescape(href.strip())
    if href.startswith("/"):
        href = SITE + href
    # the site writes spaces raw and doubles slashes; keep the path as the site serves it, but encoded
    parts = urllib.parse.urlsplit(href)
    return urllib.parse.urlunsplit(parts._replace(path=urllib.parse.quote(urllib.parse.unquote(parts.path), safe="/@")))


# ---------------------------------------------------------------- parsers ---

def parse_year(text):
    """A year list: [{docket, service, filed, category, utility, title}]."""
    out = []
    for blk in (text or "").split("<div class='row' style=\"\">")[1:]:
        m = re.search(r"href='/Case/ViewCaseFilings/(\d{4}-\d{5})'", blk)
        if not m:
            continue
        fields = {k: text_of(v) for k, v in re.findall(
            r"id='lblLbl(\w+)'>[^<]*</span>\s*<span>(.*?)</span>", blk, re.S)}
        title = re.search(r'<p class="form-control-static">\s*<span>(.*?)</span>', blk, re.S)
        out.append({"docket": m.group(1), "service": fields.get("ServType", ""), "filed": iso(fields.get("FilingDt")),
                    "category": fields.get("Category", ""), "utility": fields.get("Utils", ""),
                    "title": text_of(title.group(1)) if title else ""})
    return out


def parse_case_info(text):
    f = {k: text_of(v) for k, v in re.findall(r"ID='lbl(\w+)'[^>]*>(.*?)</span>", text or "", re.S)}
    return {"docket": f.get("CaseNumber", ""), "service": f.get("ServiceType", ""), "filed": iso(f.get("FilingDt")),
            "category": f.get("Category", ""), "utility": f.get("Utilities", ""),
            "title": text_of(re.search(r"id='lblNature'>(.*?)</span>", text or "", re.S).group(1))
            if re.search(r"id='lblNature'>(.*?)</span>", text or "", re.S) else ""}


def parse_filings(text):
    """The filings table of a case page or tab: [{date, description, documents: [{name, url, description}]}].
    Filer names (pFiler) are not kept."""
    m = re.search(r'<tbody id="tblCaseFiles">(.*?)</tbody>', text or "", re.S)
    out = []
    for tr in re.findall(r"<tr>(.*?)</tr>", m.group(1) if m else "", re.S):
        date = re.search(r"id='spnRcvdDt'>\s*<span>(.*?)</span>", tr, re.S)
        desc = re.search(r"id='pFileDesc'>(.*?)</p>", tr, re.S)
        docs = []
        for href, name, rest in re.findall(r"<a href='([^']+)'[^>]*>(.*?)</a>(.*?)(?=<a href=|</td>)", tr, re.S):
            dd = re.search(r"id='pDocDesc'>(.*?)</p>", rest, re.S)
            docs.append({"name": text_of(name), "url": abs_url(href), "description": text_of(dd.group(1)) if dd else ""})
        out.append({"date": iso(date.group(1)) if date else "", "description": text_of(desc.group(1)) if desc else "",
                    "documents": docs})
    return out


def parse_hearings(text):
    """Hearing videos: [{date, title, url}]."""
    out = []
    for href, label in re.findall(r"id='lnkVid' href='([^']+)'[^>]*>(.*?)</a>", text or "", re.S):
        label = text_of(label)
        d = re.search(r"\(([A-Z][a-z]{2}) (\d{1,2}), (\d{4})\)", label)
        out.append({"date": iso(f"{d.group(1)} {d.group(2)}, {d.group(3)}") if d else "", "title": label, "url": href})
    return out


# ---------------------------------------------------------------- network ---

class PSC:
    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": CHROME_UA})
        self.failed = []

    def page(self, url):
        for attempt in range(3):
            try:
                r = self.s.get(url, timeout=120)
                if r.status_code == 200:
                    return r.text
                err = str(r.status_code)
            except requests.RequestException as e:
                err = "000"
                log(f"  {url}: {str(e)[:100]}")
            time.sleep(2 * (attempt + 1))
        self.failed.append(url)
        report_failure(url, err, "commission page failed three times")
        return None

    def download(self, url, path, max_bytes):
        try:
            with self.s.get(url, timeout=300, stream=True) as r:
                if r.status_code != 200:
                    report_failure(url, r.status_code, "commission document")
                    return False
                buf = b""
                for chunk in r.iter_content(1 << 16):
                    buf += chunk
                    if len(buf) > max_bytes:
                        log(f"  skipped, larger than {max_bytes // 1_000_000} MB: {url}")
                        return False
        except requests.RequestException as e:
            report_failure(url, "000", f"commission document: {str(e)[:80]}")
            return False
        if buf[:5] != b"%PDF-":
            report_failure(url, "200", "commission document is not a PDF")
            return False
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(buf)
        return True


def year_cases(psc, year, refresh):
    cache = WORK / "years" / f"{year}.html"
    if cache.exists() and not refresh:
        text = cache.read_text(errors="replace")
    else:
        text = psc.page(YEAR_LIST.format(year=year))
        if text is None:
            return None
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(text)
    return parse_year(text)


# ------------------------------------------------------------ classifying ---

def classify(d):
    """(relevant, key, reasons): relevant = an electric or siting board case about generation;
    key = one whose documents are read (not only wires, wind or solar)."""
    title = d.get("title", "")
    reasons = []
    if d["docket"] in KNOWN_CASES:
        reasons.append("on the hand-checked list")
    gen = bool(GEN.search(title)) and bool(SERVICE_KEEP.search(d.get("service", "") or "electric"))
    if gen:
        reasons.append("its title is about generation, a resource plan, a retirement or a large load")
    wires_only = bool(WIRES.search(title)) and not re.search(
        r"generat|plant|station|energy center|turbine|resource plan|convenience and necessity to construct (a )?(new )?gen",
        title, re.I)
    ws_only = bool(WIND_SOLAR.search(title)) and not re.search(r"\bgas\b|turbine|combined|peak|generating station", title, re.I)
    relevant = bool(reasons)
    key = d["docket"] in KNOWN_CASES or (gen and bool(GAS.search(title)) and not wires_only and not ws_only)
    return relevant, key, reasons


# ---------------------------------------------------------- document facts ---

def pick(text, rx, limit, lo=20, hi=420):
    out = []
    for s in sentences(text):
        if rx.search(s) and lo < len(s) < hi and s not in out:
            out.append(s)
            if len(out) >= limit:
                break
    return out


def doc_facts(text):
    yr = r".*\b20[2-5]\d\b|\b20[2-5]\d\b.*"
    return {
        "technology": sorted({m.group(0).lower() for m in TECH.finditer(text)})[:8],
        "equipment_maker_model": pick(text, DOCKET_MAKER, 8),
        "megawatts": pick(text, DOCKET_SIZE, 10),
        "in_service": pick(text, re.compile(f"({INSERVICE.pattern}){yr}({INSERVICE.pattern})?", re.I), 6),
        "retirement": pick(text, re.compile(f"({RETIRE.pattern}){yr}({RETIRE.pattern})?", re.I), 8),
        "location": pick(text, LOCATION, 6),
        "coords": [f"{a}, -{b.lstrip('-')}" for a, b in LATLON.findall(text)][:3],
    }


def pdf_text(path):
    """Plain text of a PDF; a scanned one goes through OCR."""
    try:
        t = subprocess.run(["pdftotext", str(path), "-"], capture_output=True, text=True, timeout=600).stdout
    except (subprocess.SubprocessError, OSError):
        t = ""
    if len(t.strip()) < 300:
        import fetch
        try:
            ocr = fetch._pdf_ocr(str(path))
        except Exception:  # noqa: BLE001
            ocr = ""
        if len(ocr.strip()) > len(t.strip()):
            t = ocr
    return t


def all_docs(filings, tab):
    out = []
    for n, f in enumerate(filings):
        for d in f["documents"]:
            out.append({**d, "date": f["date"], "filing": f["description"][:300], "tab": tab, "row": n})
    return out


def pick_docs(docs, cap, post_cap=3):
    """PDFs only, ranked: the application filing and the final order first, then construction
    notices after the final order, testimony, plans and reports, newest first within a rank.
    At most post_cap documents from after the final order (most are quarterly reports). Never
    appearances, confidential versions, service certificates or cover letters, judged on the
    document's own name and description (an application row is often titled "Application and
    Motion for Confidential Treatment")."""
    scored = []
    for d in docs:
        if not re.search(r"\.pdf$", urllib.parse.urlsplit(d["url"]).path, re.I):
            continue
        own = f"{d['name']} {d['description']}".replace(" ", "_")
        if re.search(r"motion|petition|notice_of_(filing|intent)|read.?(1st|first)", own, re.I) and d["tab"] != "post" \
                or DOC_SKIP.search(own) and not re.match(r"(REDACTED_)?application", d["name"], re.I):
            continue
        s = 2 if DOC_PRIORITY.search(own) else 0
        if d["tab"] == "post":
            s += 7 if re.search(r"construct|commence|in[- ]service|commercial operation", own + d["filing"], re.I) else 1
        elif re.match(r"(amended |supplemental )?application", d["filing"], re.I):
            s += 8 + (3 if re.search(r"application", own, re.I) else 0)
        elif re.match(r"final order", d["filing"], re.I):
            s += 9
        elif re.search(r"testimony", own + d["filing"], re.I):
            s += 3
        scored.append((-s, "".join(chr(255 - ord(c)) for c in d["date"]), d))
    out, posts = [], 0
    for *_, d in sorted(scored, key=lambda x: x[:2]):
        if d["tab"] == "post":
            if posts >= post_cap:
                continue
            posts += 1
        out.append(d)
        if len(out) >= cap:
            break
    return out


def doc_file(folder, doc):
    base = urllib.parse.unquote(doc["url"].rsplit("/", 1)[-1])
    base = re.sub(r"[^A-Za-z0-9._-]+", "_", base)[-120:] or "document.pdf"
    return folder / f"{doc['date'] or 'nodate'}_{base}"


def read_doc(psc, doc, folder, max_bytes):
    pdf = doc_file(folder, doc)
    txt = pdf.with_suffix(".txt")
    if txt.exists():
        return txt.read_text(errors="replace"), txt
    text = ""
    if (pdf.exists() and pdf.read_bytes()[:5] == b"%PDF-") or psc.download(doc["url"], pdf, max_bytes):
        text = pdf_text(pdf)
    if text.strip():
        txt.write_text(text)
    return text, txt


def read_case(psc, d, cap, max_bytes, read_docs=True):
    """The case page and its tabs; then the key documents."""
    base = CASE.format(case=d["docket"])
    main_page = psc.page(base)
    if main_page is None:
        d["store_state"] = "the filings page did not load"
        return
    info = parse_case_info(main_page)
    for k in ("service", "filed", "category", "utility", "title"):
        if info.get(k) and not d.get(k):
            d[k] = info[k]
    filings = parse_filings(main_page)
    post = parse_filings(psc.page(base + "/Post") or "")
    public = parse_filings(psc.page(base + "/Public") or "")
    hear = parse_hearings(psc.page(base + "/Hearings") or "")
    d["url"] = base
    d["filings_listed"] = len(filings)
    d["latest_filing"] = max((f["date"] for f in filings + post if f["date"]), default="")
    d["post"] = [{"date": f["date"], "description": f["description"][:300],
                  "documents": [{"name": x["name"], "url": x["url"]} for x in f["documents"]]} for f in post]
    d["public_comments"] = {"count": len(public), "newest": max((f["date"] for f in public if f["date"]), default="")}
    d["hearings"] = [h["date"] for h in hear if h["date"]]
    d["hearing_videos"] = hear
    d["orders"] = [{"date": f["date"], "title": f["description"][:200], "url": f["documents"][0]["url"]}
                   for f in filings if f["documents"] and re.match(r"(final )?order", f["description"], re.I)][:12]
    if not read_docs:
        return
    folder = WORK / d["docket"]
    folder.mkdir(parents=True, exist_ok=True)
    docs, parts = [], []
    for doc in pick_docs(all_docs(filings, "filings") + all_docs(post, "post"), cap):
        text, txt = read_doc(psc, doc, folder, max_bytes)
        rec = {"title": (doc["description"] or doc["filing"] or doc["name"])[:200], "file": doc["name"][:120],
               "kind": "post-case filing" if doc["tab"] == "post" else "filing", "date": doc["date"],
               "url": doc["url"], "saved": str(txt.relative_to(REPO)) if txt.exists() else "",
               "read": len(text.strip()) >= 300}
        if rec["read"]:
            rec["facts"] = doc_facts(text)
            parts.append(rec["facts"])
        docs.append(rec)
        time.sleep(0.3)
    d["documents"], d["facts"] = docs, merge_facts(parts)
    d["store_state"] = f"{len(filings)} filings listed, {len(post)} after the final order"
    d["text_blob"] = " ".join(p.read_text(errors="replace") for p in sorted(folder.glob("*.txt")))


# ------------------------------------------------------------------ match ---

def match_docket(plant, d, others_by_title=False):
    """How a case matches a plant, or None: the hand-checked list, the plant's name in the case
    title or an order (strong), or, for a case with no hand-checked plants and no plant in its
    title, in the documents read five or more times. An application or resource plan names
    every plant the utility owns, so document mentions alone never add a plant to a case
    that already has its plants."""
    known = KNOWN_CASES.get(d["docket"])
    if plant["id"] in (known or []):
        return "on the hand-checked case list"
    head = f"{d.get('title', '')} {' '.join(o.get('title', '') for o in d.get('orders', []))}".lower()
    pats = PSC_KNOWN.get(plant["id"])
    if not pats:
        ws = plant["name_words"]
        return "name words in the case title, check it is this plant" if ws and ws <= words(head) else None
    if any(re.search(p, head, re.I) for p in pats):
        return "name in the case title or an order"
    if known or others_by_title:
        return None
    blob = d.get("text_blob", "")
    n = len({m.start() for p in pats for m in re.finditer(p, blob, re.I)})   # one count per place named
    return f"named {n} times in the documents read, check the case is about this plant" if n >= 5 else None


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


# ----------------------------------------------------------------- output ---

def docket_block(d, full=True):
    pc = d.get("public_comments") or {}
    L = [f"- **{d['docket']}**, {d.get('utility') or 'utility not shown'}: {d['title'][:300]}",
         f"  - {d.get('service') or 'service not shown'}, {d.get('category') or 'category not shown'}; filed "
         f"{d.get('filed') or 'unknown'}"
         + (f"; newest filing {d['latest_filing']}" if d.get("latest_filing") else "")
         + (f"; hearings {', '.join(d['hearings'][-4:])}" if d.get("hearings") else "")
         + (f"; {pc['count']} public comments, newest {pc['newest']}" if pc.get("count") else "")
         + f"; link {d.get('url') or CASE.format(case=d['docket'])}"]
    for o in d.get("orders", [])[:6]:
        L.append(f"  - order ({o['date']}): {o['title'][:140]}, {o['url']}")
    for p in d.get("post", [])[:6]:
        L.append(f"  - after the final order ({p['date']}): {p['description'][:140]}"
                 + (f", {p['documents'][0]['url']}" if p["documents"] else ""))
    if full and d.get("facts"):
        f = d["facts"]
        for k, label in [("technology", "Technology"), ("megawatts", "Megawatts"),
                         ("equipment_maker_model", "Equipment"), ("in_service", "In service"),
                         ("retirement", "Retirements"), ("location", "Location"), ("coords", "Coordinates")]:
            if f.get(k):
                L.append(f"  - {label}: " + " | ".join(f[k][:4]))
    for doc in d.get("documents", []):
        L.append(f"  - {'read' if doc.get('read') else 'not read'}: {doc['title'][:100]} ({doc['kind']}, {doc['date']}): {doc['url']}")
    return L


def write_outputs(out_dir, plants, dockets, by_plant, matched, sources, today, from_year):
    out_dir.mkdir(parents=True, exist_ok=True)
    slim = [{k: v for k, v in d.items() if k not in ("text_blob",)} for d in dockets]
    unmatched = [d for d in dockets if d.get("key") and d["docket"] not in matched]
    data = {"generated": today, "from_year": from_year, "sources": sources, "dockets": slim,
            "by_plant": by_plant, "unmatched_generation": [d["docket"] for d in unmatched]}
    (out_dir / "psc_dockets.json").write_text(json.dumps(data, indent=1, default=str))
    by_id = {d["docket"]: d for d in dockets}
    L = [f"# Kentucky Public Service Commission cases on generation ({today})", "",
         f"Electric and siting board cases filed {from_year} or later whose titles are about generation, a resource "
         "plan, a retirement or a large load, plus the hand-checked list. A document's psc.ky.gov/pscecf or pscscf "
         "address is a stable public link and can be cited. Copies of documents read are in scopes/us-ky/work/psc/ "
         "and are not committed. Public comments are counted, not listed.", "", "## Sources", ""]
    L += [f"- {s['name']}: {s['how']} ({s['url']})" for s in sources]
    L += ["", "## Matched to GEM plants", ""]
    for p in plants:
        L += [f"### {p['name']} ({p['id']}), {p['city'] or 'city blank'}, {p['county'] or 'county blank'} County", ""]
        ids = by_plant.get(p["id"], [])
        if not ids:
            L += ["No case matched.", ""]
            continue
        for k in ids:
            d = by_id[k]
            L += docket_block(d)
            L.append(f"  - Match: {next(m['how'] for m in d['matched'] if m['plant_id'] == p['id'])}")
        L.append("")
    L += ["## Generation cases that match no GEM plant (possible new plants, data center loads, uprates or retirements)", ""]
    for d in sorted(unmatched, key=lambda x: x["docket"]):
        L += docket_block(d)
    L += ["", "## Other generation-related cases (lines, wind, solar; not read)", ""]
    for d in sorted((d for d in dockets if d.get("relevant") and not d.get("key")), key=lambda x: x["docket"]):
        L += docket_block(d, full=False)
    (out_dir / "psc_dockets.md").write_text("\n".join(L) + "\n")
    return unmatched


# ------------------------------------------------------------------- main ---

def main():
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    ap.add_argument("--from-year", type=int, default=2021)
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--plants", help="comma-separated GEM location IDs")
    ap.add_argument("--cases", help="comma-separated case numbers: read only these (no year lists)")
    ap.add_argument("--docs-per-docket", type=int, default=10)
    ap.add_argument("--max-mb", type=float, default=80, help="skip documents larger than this")
    ap.add_argument("--no-docs", action="store_true", help="list cases and read their pages, download nothing")
    ap.add_argument("--match-only", metavar="JSON", help="re-match a saved psc_dockets.json, no network")
    a = ap.parse_args()
    plants = load_plants(argparse.Namespace(plants=a.plants))
    today = dt.date.today()
    if a.match_only:
        saved = json.loads(Path(a.match_only).read_text())
        dockets = saved["dockets"]
        for d in dockets:
            folder = WORK / d["docket"]
            d["text_blob"] = " ".join(p.read_text(errors="replace") for p in sorted(folder.glob("*.txt"))) \
                if folder.exists() else ""
        by_plant, matched = match_all(plants, dockets)
        write_outputs(Path(a.out), plants, dockets, by_plant, matched, saved["sources"], today.isoformat(),
                      saved.get("from_year", a.from_year))
        return

    psc = PSC()
    cases, years_read, years_failed = {}, [], []
    if a.cases:
        for k in a.cases.split(","):
            cases[k.strip()] = {"docket": k.strip()}
    else:
        for year in range(a.from_year, today.year + 1):
            rows = year_cases(psc, year, refresh=year >= today.year - (1 if today.month == 1 else 0))
            if rows is None:
                years_failed.append(str(year))
                continue
            years_read.append(f"{year} ({len(rows)} cases)")
            for r in rows:
                cases[r["docket"]] = r
        for k in KNOWN_CASES:
            cases.setdefault(k, {"docket": k})
    log(f"year lists: {', '.join(years_read) or 'none'}; {len(cases)} cases")

    dockets = []
    for d in cases.values():
        for k in ("service", "filed", "category", "utility", "title"):
            d.setdefault(k, "")
        d["relevant"], d["key"], d["reasons"] = classify(d)
        if a.cases:
            d["relevant"] = d["key"] = True
            d["reasons"].append("named on the command line")
        elif not d["key"] and SERVICE_KEEP.search(d["service"] or "") and not WIRES.search(d["title"]) \
                and any(match_docket(p, {**d, "text_blob": ""}) for p in plants):
            d["relevant"] = d["key"] = True
            d["reasons"].append("its title names a GEM plant")
        if d["relevant"]:
            dockets.append(d)
    log(f"{len(dockets)} generation related; {sum(1 for d in dockets if d['key'])} key")

    for n, d in enumerate(dockets, 1):
        d.setdefault("documents", [])
        d.setdefault("facts", {})
        d["text_blob"] = ""
        if not d["key"]:
            d["url"] = CASE.format(case=d["docket"])
            continue
        read_case(psc, d, a.docs_per_docket, int(a.max_mb * 1e6), read_docs=not a.no_docs)
        log(f"({n}/{len(dockets)}) {d['docket']}: {d['title'][:90]}; {len(d['documents'])} documents")
        if not d["relevant"] or not d["title"]:
            d["relevant"], d["key"], _ = classify(d)
            d["relevant"] = d["key"] = d["key"] or bool(a.cases) or d["docket"] in KNOWN_CASES

    sources = [
        {"name": "Kentucky PSC whole-year case lists", "url": YEAR_LIST.format(year=today.year),
         "how": ("skipped, cases named on the command line" if a.cases else
                 f"every year from {a.from_year}: {', '.join(years_read)}")
                + (f"; years that did not load: {', '.join(years_failed)}" if years_failed else "")},
        {"name": "Kentucky PSC case filings pages and their Post, Public and Hearings tabs", "url": SITE + "/Case/ViewCaseFilings/",
         "how": f"every key case, up to {a.docs_per_docket} documents read per case"
                + ("; documents not downloaded (--no-docs)" if a.no_docs else "")
                + (f"; pages that did not load: {len(psc.failed)}" if psc.failed else "")}]
    by_plant, matched = match_all(plants, dockets)
    unmatched = write_outputs(Path(a.out), plants, dockets, by_plant, matched, sources, today.isoformat(), a.from_year)
    log(f"{len(matched)} cases matched to plants; {len(unmatched)} key cases unmatched")
    for p in plants:
        if by_plant[p["id"]]:
            log(f"  {p['name']}: {', '.join(by_plant[p['id']])}")


if __name__ == "__main__":
    main()

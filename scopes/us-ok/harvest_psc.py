"""
Harvest Oklahoma Corporation Commission (OCC) utility causes on generation before a research sweep.

The OCC's Public Utility Division hears every request by OG&E, PSO, Empire and
the cooperatives to build, buy or retire a plant (preapproval causes, under
17 O.S. 286), every integrated resource plan filing and every request for
proposals report. Its case filing site needs a sign-in to search, but the
documents do not. What was found (2026-11-03 and 2026-11-04):

  1. Daily dockets, oklahoma.gov/occ/court-dockets/docket-results.html: a page
     of links to one PDF per hearing day and courtroom, about three years back.
     Only the `-pud` files hold utility causes (the `-okc` and `-tulsa` files
     are oil and gas causes). An unlinked date answers with a 404 page, so the
     links on the index page are the list. Each entry gives the cause number
     (PUD2026-000073), the hearing date, the applicant, the relief type and the
     relief sought. Judges, attorneys and court reporters are not kept.
  2. The Laserfiche WebLink store, public.occ.ok.gov/WebLink: every filing and
     order, no sign-in. Open Welcome.aspx once for the session cookie, then
     post JSON to SearchService.aspx/GetSearchListing. A month of Public
     Utility Division orders is one field search on ECF Division and ECF
     Docket Date (September 2026 had 484); each order carries its Case
     Number, Order Title, Relief Types and Relief Requested. A name search
     `{LF:Name="PUD2026-000073*"}` lists every filing of one cause.
  3. Documents: an electronic filing (isEdoc) downloads as a text PDF from
     ElectronicFile.aspx?docid=<entryId>&dbid=0&repo=OCC with no cookie, and
     that address is its citation. An imaged order is cited by its
     DocView.aspx?id=<entryId>&dbid=0&repo=OCC address and read through the
     fetch.py rule `occ_weblink`, which asks the viewer for each page's text.

Steps:
  1. Read the daily docket index, download every `-pud` file from --from-year
     (cached; the last two weeks are fetched again) and parse the entries.
  2. Sweep the WebLink store month by month for Public Utility Division
     orders (cached per month; the last two months are fetched again) and add
     their causes.
  3. Keep causes on generation: preapproval, a plant, a certificate, capacity,
     turbines, an acquisition, a resource plan, a request for proposals, a
     data center or large load tariff, a retirement. Transmission-only causes
     are listed, not read.
  4. For each kept cause, list its filings by name, then download the
     application, testimony, reports and orders (capped, larger first) into
     scopes/us-ok/work/psc/<cause>/ (not committed) and keep the lines that
     give technology, megawatts, maker and model, in-service and retirement
     years, and location.
  5. Match causes to the Oklahoma plants in the scoped GEM export by name in
     the relief sought or applicant (strong) or by name in the documents read
     three or more times.

Output, in batches/us-ok/harvest/: psc_dockets.json (read by
build_state_brief.py --harvest; one entry per cause, "docket" is the cause
number) and psc_dockets.md. Nothing here stages a record, and nothing here
signs in: a cause whose documents are not in the public store is listed for
Baird to fetch by hand.

Usage (from the repo root):
    python scopes/us-ok/harvest_psc.py                        # from 2024, read key documents
    python scopes/us-ok/harvest_psc.py --no-docs              # list causes, download nothing
    python scopes/us-ok/harvest_psc.py --match-only batches/us-ok/harvest/psc_dockets.json
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
from harvest_lib import (DOCKET_MAKER, DOCKET_SIZE, REPO, clean_ws, docket_cache, get,  # noqa: E402
                         merge_facts, report_failure, sentences)

from paths import load_scope_module  # noqa: E402

_permits = load_scope_module("us-ok", "harvest_permits")
load_plants, words = _permits.load_plants, _permits.words

INDEX = "https://oklahoma.gov/occ/court-dockets/docket-results.html"
SITE = "https://oklahoma.gov"
WEBLINK = "https://public.occ.ok.gov/WebLink/"
EFILE = WEBLINK + "ElectronicFile.aspx?docid={id}&dbid=0&repo=OCC"
DOCVIEW = WEBLINK + "DocView.aspx?id={id}&dbid=0&repo=OCC"
OUT = REPO / "batches" / "us-ok" / "harvest"
WORK = docket_cache("us-ok")
JSON_HDR = {"Content-Type": "application/json", "X-Lf-Suppress-Login-Redirect": "1"}

# Causes read whatever the search finds. Add a cause here when a lead names it.
KNOWN_CASES: list[str] = []

# GEM plant -> regexes over a cause's relief sought, applicant and documents (lower case).
PSC_KNOWN = dict(_permits.KNOWN)

DOCKET_LINK = re.compile(r"(/content/dam/ok/en/occ/documents/ajls/jls-courts/court-clerk/docket-results/"
                         r"(\d{4})/(\d{4}-\d\d-\d\d)-([a-z]+)\.pdf)", re.I)
CAUSE = re.compile(r"^\s*([A-Z]{2,5}\d{4}-\d{6})\b")
HEARING = re.compile(r"(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s+([A-Z][a-z]+ \d{1,2}, \d{4})")
GEN = re.compile(r"generat|power plant|preapprov|pre-approv|certificate of (convenience|authority)|capacity|"
                 r"turbine|combined[- ]cycle|simple[- ]cycle|peak|acqui|purchase of .{0,60}(facilit|plant|station)|"
                 r"integrated resource|\bIRP\b|resource plan|request for proposal|\bRFP\b|data cent|large load|"
                 r"retire|cogenerat|megawatt|\bMW\b|energy center|power station|\bgas[- ]fired", re.I)
WIRES = re.compile(r"transmission|\bkv\b|substation|\bline\b|right[- ]of[- ]way", re.I)
WIND_SOLAR = re.compile(r"\bwind\b|solar|photovoltaic|battery|storage", re.I)
GAS = re.compile(r"\bgas\b|turbine|combined[- ]cycle|simple[- ]cycle|peak|reciprocating|generating|"
                 r"power plant|energy center|power station|data cent|large load|resource plan|\bIRP\b|"
                 r"request for proposal|\bRFP\b|preapprov|pre-approv|acqui|retire|capacity", re.I)
TECH = re.compile(r"combined[- ]cycle|combustion turbine|simple[- ]cycle|peaking|reciprocating|internal combustion|"
                  r"aeroderivative|frame turbine|natural gas[- ]fired|gas[- ]fired|duct[- ]fir", re.I)
INSERVICE = re.compile(r"in[- ]service|commercial operation|\bCOD\b|placed in service|on[- ]line|begin operat|"
                       r"construction (will|to) (begin|start|commence)", re.I)
RETIRE = re.compile(r"retire|retirement|deactivat|mothball|cease operat|shut ?down|decommission", re.I)
LOCATION = re.compile(r"located (at|in|on|near|approximately)|site (is|in|at)|county,? oklahoma|"
                      r"\bsection \d+|township \d+|range \d+|\bT\d{1,2}[NS]\b|latitude|longitude", re.I)
LATLON = re.compile(r"\b(3[3-7]\.\d{3,})\s*[,;/ ]\s*-?\s*(9[4-9]\.\d{3,}|10[0-3]\.\d{3,})\b")
DOC_PRIORITY = re.compile(r"application|testimony|order|report|settlement|stipulation|exhibit|"
                          r"resource plan|\bIRP\b|request for proposal|\bRFP\b|supplement", re.I)
DOC_SKIP = re.compile(r"entry_of_appearance|appearance|notice_of_hearing|certificate_of_service|affidavit|"
                      r"motion_to_(determine_notice|establish|intervene|continue)|proof_of_publication|"
                      r"transcript|summons|withdraw", re.I)


def log(msg):
    print(f"[psc-ok] {msg}", file=sys.stderr, flush=True)


def us_date(s):
    """'9/1/2026' or 'October 29, 2026' to 2026-09-01, or ''."""
    s = (s or "").strip()
    for fmt in ("%m/%d/%Y", "%B %d, %Y"):
        try:
            return dt.datetime.strptime(s.split(" ")[0] if fmt == "%m/%d/%Y" else s, fmt).date().isoformat()
        except ValueError:
            pass
    return ""


def kb(props):
    """Bytes from an entryProperties string like '0 pages - 579 KB '."""
    m = re.search(r"([\d.,]+)\s*(KB|MB|GB|bytes)", props or "", re.I)
    if not m:
        return 0
    n = float(m.group(1).replace(",", ""))
    return int(n * {"bytes": 1, "kb": 1e3, "mb": 1e6, "gb": 1e9}[m.group(2).lower()])


# ----------------------------------------------------------- daily dockets ---

def docket_links(index_html, from_year, kind="pud"):
    """[(date, absolute url)] of the index page's daily docket files of one kind, oldest first."""
    t = html.unescape(index_html or "")
    out = {}
    for path, year, day, k in DOCKET_LINK.findall(t):
        if k.lower() == kind and int(year) >= from_year:
            out[day] = SITE + path
    return sorted(out.items())


def hearing_kind(text):
    """What the hearing was, without names: 'Hearing on the Merits', 'Continued (1) | Motion to
    Intervene'. A motion's text can name the people who moved, so anything after a dash goes."""
    parts = re.sub(r"Court Reporter:.*", "", text).split("|")
    return " | ".join(clean_ws(re.split(r"\s*-\s*", x, maxsplit=1)[0]) for x in parts if x.strip())


def parse_daily(text, day="", url=""):
    """Entries of one daily docket's text (pdftotext -layout): cause, hearing date, applicant,
    relief type, relief sought and the hearing text. Judges, attorneys and reporters are dropped."""
    blocks, cur = [], None
    for ln in (text or "").splitlines():
        m = CAUSE.match(ln)
        if m:
            cur = [ln]
            blocks.append(cur)
        elif cur is not None:
            cur.append(ln)
    out = []
    for b in blocks:
        cause = CAUSE.match(b[0]).group(1)
        if not cause.startswith("PUD"):      # universal service fund and other causes; applicants can be people
            continue
        hm = HEARING.search(b[0])
        parties, hearing_text, relief, in_relief = [], "", [], False
        for ln in b[1:]:
            s = ln.strip()
            if s.startswith("Result:"):
                break
            if in_relief:
                relief.append(s)
            elif s.startswith("Relief Type:"):
                in_relief = True
                relief.append(s[len("Relief Type:"):])
            elif s.startswith("Text:"):
                hearing_text = hearing_kind(s[len("Text:"):])
            elif not hearing_text:
                parties.append(re.sub(r"\s(Legal|Attorney):.*", "", s.replace("Parties:", "")).strip())
        joined = clean_ws(" ".join(parties))
        applicants = [clean_ws(x) for x in re.findall(r"([^()]+?)\s*\(Applicant\)", joined)]
        rel = clean_ws(" ".join(relief))
        rtype, _, sought = rel.partition("Relief Sought:")
        out.append({"docket": cause, "hearing": us_date(hm.group(1)) if hm else day,
                    "applicant": "; ".join(a.strip(" ,;") for a in applicants if a.strip(" ,;")),
                    "relief_type": rtype.strip(), "relief_sought": sought.strip(),
                    "hearing_text": hearing_text, "docket_pdf": url})
    return out


# ---------------------------------------------------------------- WebLink ---

class WebLink:
    def __init__(self):
        self.s = requests.Session()
        self.s.headers["User-Agent"] = CHROME_UA
        self.failed = []
        self.warm = False

    def _warm(self):
        if not self.warm:
            self.s.get(WEBLINK + "Welcome.aspx?dbid=0&repo=OCC", timeout=60)
            self.warm = True

    def search(self, syn, start=0, end=100):
        """(hit count, results) for one page of a Laserfiche search, or (None, []) after three tries."""
        body = {"repoName": "OCC", "searchSyn": syn, "searchUuid": "", "sortColumn": "", "startIdx": start,
                "endIdx": end, "getNewListing": True, "sortOrder": 0, "displayInGridView": True}
        for i in range(3):
            try:
                self._warm()
                r = self.s.post(WEBLINK + "SearchService.aspx/GetSearchListing", headers=JSON_HDR,
                                data=json.dumps(body), timeout=180)
                if r.status_code == 200:
                    d = (r.json() or {}).get("data") or {}
                    return int(d.get("hitCount") or 0), d.get("results") or []
                err = f"HTTP {r.status_code}"
            except Exception as e:  # noqa: BLE001
                err = str(e)[:120]
            self.warm = False
            time.sleep(3 * (i + 1))
        self.failed.append(f"{syn} [{start}-{end}]: {err}")
        report_failure(WEBLINK + "SearchService.aspx/GetSearchListing", "000", f"{syn}: {err}")
        return None, []

    def search_all(self, syn, page=100, cap=3000):
        hits, results = self.search(syn, 0, page)
        if hits is None:
            return None
        out = list(results)
        while len(out) < min(hits, cap) and results:
            _, results = self.search(syn, len(out), len(out) + page)
            out += results
            time.sleep(0.3)
        return out

    def download(self, url, path, max_bytes):
        """Save a PDF; False when the answer is not a PDF or is too large."""
        try:
            r = self.s.get(url, timeout=300)
        except Exception as e:  # noqa: BLE001
            report_failure(url, "000", str(e)[:120])
            return False
        if r.status_code != 200 or r.content[:5] != b"%PDF-" or len(r.content) > max_bytes:
            report_failure(url, str(r.status_code), "not a PDF" if r.status_code == 200 else "")
            return False
        path.write_bytes(r.content)
        return True


def meta(r):
    return {m["name"]: "; ".join(m.get("values") or []) for m in r.get("metadata") or []}


def parse_result(r):
    """One WebLink search result as a document record."""
    m = meta(r)
    edoc = bool(r.get("isEdoc"))
    eid = r.get("entryId")
    case = m.get("Case Number") or ""
    if not case and m.get("ECF Case Number"):
        case = f"{m.get('ECF Division') or 'PUD'}{m['ECF Case Number']}"
    if not case:
        cm = re.match(r"([A-Z]{2,5}\d{4}-\d{6})", r.get("name") or "")
        case = cm.group(1) if cm else ""
    title = m.get("Order Title") or re.sub(r"^[A-Z]{2,5}\d{4}-\d{6}_\d+_", "", r.get("name") or "").replace("_", " ")
    entry = re.match(r"[A-Z]{2,5}\d{4}-\d{6}_(\d+)_", r.get("name") or "")
    return {"entry_id": eid, "name": r.get("name") or "", "case": case, "title": clean_ws(title),
            "kind": "electronic filing" if edoc else "imaged order",
            "date": us_date(m.get("ECF Docket Date") or m.get("Signing Agenda Date") or ""),
            "docket_entry": int(entry.group(1)) if entry else 0,
            "order_number": m.get("ECF Order Number") or ("" if edoc else r.get("name") or ""),
            "doc_type": m.get("ECF Document Type") or "", "relief_types": m.get("ECF Relief Types") or "",
            "relief": m.get("Relief Requested") or "", "applicant": m.get("ECF Applicant") or "",
            "confidential": m.get("ECF Confidential") or "", "pages": r.get("entryProperties", "").strip(),
            "bytes": kb(r.get("entryProperties")),
            "url": (EFILE if edoc else DOCVIEW).format(id=eid)}


def month_windows(from_year, today):
    d = dt.date(from_year, 1, 1)
    while d <= today:
        nxt = dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1)
        yield d, nxt - dt.timedelta(days=1)
        d = nxt


def order_syn(first, last):
    f = lambda d: f"{d.month}/{d.day}/{d.year}"  # noqa: E731
    return ('{[ECF Document]:[ECF Division]="PUD", '
            f'[ECF Docket Date]>="{f(first)}", [ECF Docket Date]<="{f(last)}"}}')


def applicant_of(relief):
    m = re.search(r"APPLICATION OF (?:THE )?(.+?)(?:,? (?:FOR|TO|REQUESTING|SEEKING|PURSUANT)\b|$)", relief or "", re.I)
    return clean_ws(m.group(1)).strip(" ,") if m else ""


# --------------------------------------------------------------- classify ---

def head_of(d):
    return " ".join([d.get("title", ""), d.get("relief_type", ""), " ".join(d.get("relief_types", [])),
                     " ".join(o.get("title", "") for o in d.get("orders", []))])


def classify(d):
    """(relevant, key, reasons): relevant = a utility cause about generation; key = one whose
    documents are read (not only wires, wind or solar)."""
    head = head_of(d)
    reasons = []
    if d["docket"] in KNOWN_CASES:
        reasons.append("on the hand-checked list")
    gen = bool(GEN.search(head))
    if gen:
        reasons.append("its relief sought is about generation, a resource plan or a large load")
    wires_only = bool(WIRES.search(d.get("title", ""))) and not re.search(
        r"generat|plant|station|energy center|turbine|preapprov|pre-approv|resource plan", d.get("title", ""), re.I)
    ws_only = bool(WIND_SOLAR.search(d.get("title", ""))) and not re.search(r"\bgas\b|turbine|combined|peak|generating station", d.get("title", ""), re.I)
    relevant = bool(reasons)
    key = d["docket"] in KNOWN_CASES or (gen and bool(GAS.search(head)) and not wires_only and not ws_only)
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
    t = subprocess.run(["pdftotext", str(path), "-"], capture_output=True, text=True).stdout
    if len(t.strip()) < 300:
        import fetch
        try:
            ocr = fetch._pdf_ocr(str(path))
        except Exception:  # noqa: BLE001
            ocr = ""
        if len(ocr.strip()) > len(t.strip()):
            t = ocr
    return t


def pick_docs(docs, cap, max_bytes):
    """The documents most likely to hold facts: applications, testimony, reports and orders, the
    first filing and larger files first, never appearances, notices or service certificates,
    never confidential, never above the size cap. Imaged orders count against the cap too."""
    scored = []
    for d in docs:
        name = f"{d['name']} {d['title']} {d['doc_type']}"
        if DOC_SKIP.search(name.replace(" ", "_")) or "confidential" == d.get("confidential", "").lower():
            continue
        if d["kind"] == "electronic filing" and d["bytes"] > max_bytes:
            continue
        s = (4 if DOC_PRIORITY.search(name) else 0) + (3 if d["docket_entry"] == 1 else 0)
        s += 3 if d["kind"] == "imaged order" and re.search(r"final|order (approving|granting)", name, re.I) else 0
        scored.append((-s, -d["bytes"], d["docket_entry"], str(d["entry_id"]), d))
    return [x[-1] for x in sorted(scored, key=lambda x: x[:4])[:cap]]


def read_doc(wl, doc, folder, max_bytes):
    """Text of one document, cached as <entry id>.txt beside its PDF."""
    txt = folder / f"{doc['entry_id']}.txt"
    if txt.exists():
        return txt.read_text(errors="replace")
    text = ""
    if doc["kind"] == "electronic filing":
        pdf = folder / f"{doc['entry_id']}.pdf"
        if (pdf.exists() and pdf.read_bytes()[:5] == b"%PDF-") or wl.download(doc["url"], pdf, max_bytes):
            text = pdf_text(pdf)
    else:
        page = get(doc["url"], timeout=300)          # fetch.py rule occ_weblink reads the viewer's page text
        if page.status == "200":
            text = page.text
        else:
            report_failure(doc["url"], page.status, "imaged order text")
    if text.strip():
        txt.write_text(text)
    return text


def read_cause(wl, d, cap, max_bytes):
    folder = WORK / d["docket"]
    folder.mkdir(parents=True, exist_ok=True)
    found = wl.search_all(f'{{LF:Name="{d["docket"]}*"}}', cap=400)
    if found is None:
        return [], {}, "the store's name search did not answer"
    filings = [parse_result(r) for r in found if r.get("type") != 0]
    by_id = {f["entry_id"]: f for f in filings}
    for o in d.get("orders", []):
        by_id.setdefault(o["entry_id"], o)
    alldocs = list(by_id.values())
    d["filings_listed"] = len(alldocs)
    if not d.get("filed"):
        dates = sorted(x["date"] for x in alldocs if x["date"])
        d["filed"] = dates[0] if dates else ""
    if not d.get("utility"):
        d["utility"] = next((x["applicant"] for x in alldocs if x["applicant"]), "")
    docs, parts = [], []
    for doc in pick_docs(alldocs, cap, max_bytes):
        text = read_doc(wl, doc, folder, max_bytes)
        rec = {k: doc[k] for k in ("entry_id", "title", "kind", "date", "docket_entry", "order_number", "pages", "url")}
        rec["file"] = doc["name"][:120]
        rec["saved"] = str((folder / f"{doc['entry_id']}.txt").relative_to(REPO)) if text.strip() else ""
        rec["read"] = len(text.strip()) >= 300
        if rec["read"]:
            rec["facts"] = doc_facts(text)
            parts.append(rec["facts"])
        docs.append(rec)
        time.sleep(0.3)
    state = f"{len(alldocs)} documents in the public store" if alldocs else \
        "no documents in the public store (confidential or not yet imaged); Baird can fetch them through the case filing site"
    return docs, merge_facts(parts), state


# ------------------------------------------------------------------ match ---

def match_docket(plant, d, others_by_title=False):
    """How a cause matches a plant, or None: the plant's name in the relief sought, order titles or
    applicant (strong), or in the documents read three or more times (six when the relief sought
    already names another plant)."""
    head = f"{head_of(d)} {d.get('utility', '')}".lower()
    pats = PSC_KNOWN.get(plant["id"])
    if not pats:
        ws = plant["name_words"]
        return "name words in the relief sought, check it is this plant" if ws and ws <= words(head) else None
    if any(re.search(p, head, re.I) for p in pats):
        return "name in the relief sought or an order title"
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


# ----------------------------------------------------------------- output ---

def docket_block(d, full=True):
    hearings = d.get("hearings", [])
    L = [f"- **{d['docket']}**, {d.get('utility') or 'applicant not shown'}: {d['title'][:300]}",
         f"  - {d.get('relief_type') or '; '.join(d.get('relief_types', [])) or 'relief type not shown'}; first filing "
         f"{d.get('filed') or 'unknown'}"
         + (f"; hearings {', '.join(hearings[-4:])}" if hearings else "")
         + (f"; {d['filings_listed']} documents in the public store" if d.get("filings_listed") else "")
         + f"; link {d['url']}"]
    for o in d.get("orders", [])[:6]:
        L.append(f"  - order {o['order_number']} ({o['date']}): {o['title'][:120]}, {o['url']}")
    if full and d.get("facts"):
        f = d["facts"]
        for k, label in [("technology", "Technology"), ("megawatts", "Megawatts"),
                         ("equipment_maker_model", "Equipment"), ("in_service", "In service"),
                         ("retirement", "Retirements"), ("location", "Location"), ("coords", "Coordinates")]:
            if f.get(k):
                L.append(f"  - {label}: " + " | ".join(f[k][:4]))
    for doc in d.get("documents", []):
        state = "read" if doc.get("read") else "not read"
        L.append(f"  - {state}: {doc['title'][:100]} ({doc['kind']}, {doc['date']}): {doc['url']}")
    if d.get("store_state") and not d.get("filings_listed"):
        L.append(f"  - {d['store_state']}")
    return L


def write_outputs(out_dir, plants, dockets, by_plant, matched, sources, today, from_year):
    out_dir.mkdir(parents=True, exist_ok=True)
    slim = [{k: v for k, v in d.items() if k not in ("text_blob",)} for d in dockets]
    unmatched = [d for d in dockets if d.get("key") and d["docket"] not in matched]
    data = {"generated": today, "from_year": from_year, "sources": sources, "dockets": slim,
            "by_plant": by_plant, "unmatched_generation": [d["docket"] for d in unmatched]}
    (out_dir / "psc_dockets.json").write_text(json.dumps(data, indent=1, default=str))
    by_id = {d["docket"]: d for d in dockets}
    L = [f"# Oklahoma Corporation Commission utility causes on generation ({today})", "",
         f"Causes heard or ordered {from_year} or later, plus the hand-checked list. An electronic filing's "
         "ElectronicFile address and an imaged order's DocView address are stable public links and can be cited. "
         "Copies of documents read are in scopes/us-ok/work/psc/ and are not committed.", "", "## Sources", ""]
    L += [f"- {s['name']}: {s['how']} ({s['url']})" for s in sources]
    L += ["", "## Matched to GEM plants", ""]
    for p in plants:
        L += [f"### {p['name']} ({p['id']}), {p['city'] or 'city blank'}, {p['county'] or 'county blank'} County", ""]
        ids = by_plant.get(p["id"], [])
        if not ids:
            L += ["No cause matched.", ""]
            continue
        for k in ids:
            d = by_id[k]
            L += docket_block(d)
            L.append(f"  - Match: {next(m['how'] for m in d['matched'] if m['plant_id'] == p['id'])}")
        L.append("")
    L += ["## Generation causes that match no GEM plant (possible new plants, uprates or retirements)", ""]
    for d in sorted(unmatched, key=lambda x: x["docket"]):
        L += docket_block(d)
    L += ["", "## Other generation-related causes (lines, wind, solar; not read)", ""]
    for d in sorted((d for d in dockets if d.get("relevant") and not d.get("key")), key=lambda x: x["docket"]):
        L += docket_block(d, full=False)
    (out_dir / "psc_dockets.md").write_text("\n".join(L) + "\n")
    return unmatched


# ------------------------------------------------------------------- main ---

def fetch_daily(links, refresh_after):
    """Text of each daily docket file, cached under work/psc/daily/."""
    folder = WORK / "daily"
    folder.mkdir(parents=True, exist_ok=True)
    out, failed = [], []
    s = requests.Session()
    s.headers["User-Agent"] = CHROME_UA
    for day, url in links:
        pdf = folder / f"{day}-pud.pdf"
        txt = pdf.with_suffix(".txt")
        if txt.exists() and day < refresh_after:
            out.append((day, url, txt.read_text(errors="replace")))
            continue
        try:
            r = s.get(url, timeout=120)
            ok = r.status_code == 200 and r.content[:5] == b"%PDF-"
        except Exception as e:  # noqa: BLE001
            r, ok = None, False
            report_failure(url, "000", str(e)[:120])
        if not ok:
            if r is not None:
                report_failure(url, str(r.status_code), "daily docket not a PDF")
            failed.append(day)
            continue
        pdf.write_bytes(r.content)
        text = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True).stdout
        txt.write_text(text)
        out.append((day, url, text))
        time.sleep(0.3)
    return out, failed


def sweep_orders(wl, from_year, today, refresh_after):
    """Every Public Utility Division order in the store, month by month, cached per month."""
    folder = WORK / "orders"
    folder.mkdir(parents=True, exist_ok=True)
    out, failed = [], []
    for first, last in month_windows(from_year, today):
        cache = folder / f"{first:%Y-%m}.json"
        if cache.exists() and last.isoformat() < refresh_after:
            out += json.loads(cache.read_text())
            continue
        found = wl.search_all(order_syn(first, last), cap=5000)
        if found is None:
            failed.append(f"{first:%Y-%m}")
            continue
        recs = [parse_result(r) for r in found]
        cache.write_text(json.dumps(recs))
        out += recs
        log(f"orders {first:%Y-%m}: {len(recs)}")
    return out, failed


def build_causes(entries, orders):
    causes = {}

    def cause(k):
        return causes.setdefault(k, {"docket": k, "utility": "", "title": "", "relief_type": "", "relief_types": [],
                                     "filed": "", "hearings": [], "orders": [], "docket_pdfs": [], "url": ""})
    for e in entries:
        c = cause(e["docket"])
        c["utility"] = c["utility"] or e["applicant"]
        if len(e["relief_sought"]) > len(c["title"]):
            c["title"] = e["relief_sought"]
        c["relief_type"] = c["relief_type"] or e["relief_type"]
        if e["hearing"] and e["hearing"] not in c["hearings"]:
            c["hearings"].append(e["hearing"])
        if e["docket_pdf"] not in c["docket_pdfs"]:
            c["docket_pdfs"].append(e["docket_pdf"])
    for o in orders:
        if not o["case"].startswith("PUD"):
            continue
        c = cause(o["case"])
        if o["entry_id"] not in {x["entry_id"] for x in c["orders"]}:
            c["orders"].append(o)
        if not c["title"] and o["relief"]:
            c["title"] = o["relief"]
        c["utility"] = c["utility"] or applicant_of(o["relief"])
        for t in (o["relief_types"] or "").split("; "):
            if t and t not in c["relief_types"]:
                c["relief_types"].append(t)
    for c in causes.values():
        c["hearings"].sort()
        c["orders"].sort(key=lambda o: o["date"])
        c["url"] = c["orders"][-1]["url"] if c["orders"] else (c["docket_pdfs"][-1] if c["docket_pdfs"] else "")
    return causes


def main():
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    ap.add_argument("--from-year", type=int, default=2024)
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--plants", help="comma-separated GEM location IDs")
    ap.add_argument("--docs-per-docket", type=int, default=8)
    ap.add_argument("--max-mb", type=float, default=80, help="skip electronic filings larger than this")
    ap.add_argument("--no-docs", action="store_true", help="list causes, download nothing")
    ap.add_argument("--no-orders", action="store_true", help="skip the month-by-month order sweep")
    ap.add_argument("--match-only", metavar="JSON", help="re-match a saved psc_dockets.json, no network")
    a = ap.parse_args()
    plants = load_plants(argparse.Namespace(plants=a.plants))
    today = dt.date.today()
    if a.match_only:
        saved = json.loads(Path(a.match_only).read_text())
        dockets = saved["dockets"]
        for d in dockets:
            d["text_blob"] = " ".join(x for doc in d.get("documents", []) for v in (doc.get("facts") or {}).values() for x in v)
        by_plant, matched = match_all(plants, dockets)
        write_outputs(Path(a.out), plants, dockets, by_plant, matched, saved["sources"], today.isoformat(),
                      saved.get("from_year", a.from_year))
        return

    refresh_daily = (today - dt.timedelta(days=14)).isoformat()
    refresh_orders = (today - dt.timedelta(days=62)).isoformat()
    idx = get(INDEX)
    links = docket_links(idx.text, a.from_year) if idx.status == "200" else []
    if idx.status != "200":
        report_failure(INDEX, idx.status, "daily docket index")
    daily, daily_failed = fetch_daily(links, refresh_daily)
    entries = [e for day, url, text in daily for e in parse_daily(text, day, url)]
    log(f"daily dockets: {len(links)} files, {len(daily)} read, {len(entries)} entries")
    wl = WebLink()
    orders, months_failed = ([], []) if a.no_orders else sweep_orders(wl, a.from_year, today, refresh_orders)
    log(f"orders: {len(orders)}")
    causes = build_causes(entries, orders)
    for k in KNOWN_CASES:
        causes.setdefault(k, {"docket": k, "utility": "", "title": "", "relief_type": "", "relief_types": [],
                              "filed": "", "hearings": [], "orders": [], "docket_pdfs": [], "url": ""})

    dockets = []
    for d in causes.values():
        d["relevant"], d["key"], d["reasons"] = classify(d)
        if not d["key"] and any(match_docket(p, {**d, "text_blob": ""}) for p in plants) and not WIRES.search(d["title"]):
            d["relevant"] = d["key"] = True
            d["reasons"].append("its relief sought names a GEM plant")
        if d["relevant"]:
            dockets.append(d)
    log(f"{len(causes)} causes; {len(dockets)} generation related; {sum(1 for d in dockets if d['key'])} key")

    for d in dockets:
        d["documents"], d["facts"], d["text_blob"] = [], {}, ""
        if not d["key"] or a.no_docs:
            continue
        log(f"reading {d['docket']}: {d['title'][:90]}")
        d["documents"], d["facts"], d["store_state"] = read_cause(wl, d, a.docs_per_docket, int(a.max_mb * 1e6))
        app = next((x for x in d["documents"] if x["docket_entry"] == 1 and x["kind"] == "electronic filing"), None)
        d["url"] = app["url"] if app else (d["url"] or (d["documents"][0]["url"] if d["documents"] else ""))
        folder = WORK / d["docket"]
        d["text_blob"] = " ".join(p.read_text(errors="replace") for p in sorted(folder.glob("*.txt"))) if folder.exists() else ""

    sources = [
        {"name": "OCC daily Public Utility Division dockets", "url": INDEX,
         "how": f"every -pud file linked from the index page from {a.from_year}, {len(daily)} read, {len(entries)} entries"
                + (f"; files that did not load: {', '.join(daily_failed)}" if daily_failed else "")},
        {"name": "OCC Laserfiche WebLink store, Public Utility Division orders", "url": WEBLINK,
         "how": ("skipped" if a.no_orders else f"month-by-month field search from {a.from_year}, {len(orders)} orders")
                + (f"; months that did not answer: {', '.join(months_failed)}" if months_failed else "")},
        {"name": "OCC Laserfiche WebLink store, cause filings", "url": WEBLINK,
         "how": f"name search for every key cause, up to {a.docs_per_docket} documents read per cause"
                + (f"; searches that did not answer: {len(wl.failed)}" if wl.failed else "")}]
    by_plant, matched = match_all(plants, dockets)
    unmatched = write_outputs(Path(a.out), plants, dockets, by_plant, matched, sources, today.isoformat(), a.from_year)
    log(f"{len(matched)} causes matched to plants; {len(unmatched)} key causes unmatched")
    for p in plants:
        if by_plant[p["id"]]:
            log(f"  {p['name']}: {len(by_plant[p['id']])}")


if __name__ == "__main__":
    main()

"""
Harvest New Mexico Public Regulation Commission (PRC) cases on generation before a research sweep.

The PRC rules on every integrated resource plan, every certificate of public
convenience and necessity for a plant, every abandonment (a retirement), every
purchased power agreement for capacity and every data center or large load
tariff of PNM, Southwestern Public Service (SPS, Xcel), El Paso Electric (EPE),
Tri-State and the cooperatives. Its docket system is PRCe360,
https://e360.prc.nm.gov. It needs no sign-in: the public portal's "Continue as
Guest" button just calls anonymous JSON endpoints. What was found (2026-11-17):

  1. Case search, POST /core/api/_q/v1/prc/nm/intake/dashboard/getAllCases. The
     searchTerm matches the case number, caption and company as a substring. An
     empty term lists every case in the guest index (151 on 2026-11-17, 100 a
     page). Each row has caseid, casenumber, casetype, casecategory,
     casecaption, company and filedon.
  2. Case documents, POST /core/api/apiflow/v1/prc/nm/intake/casepublicdocument/getAll
     with the caseId: one row per filing (id, documentnumber, documentname,
     documenttype, fileddate, contenttype). Page size 100.
  3. A document download is two calls: POST /core/api/apiflow/v1/casex/cms/downloadToken
     with {context: File, documentId, fileName, annotationType: WITH_ANNOTATION,
     isPreview: true} answers a token, then GET
     /core/api/document/v1/previewDocument?token=<token> streams the PDF.
     downloadDocument answers 401. The server sometimes answers 500 on a listing;
     the calls here retry.
  4. The guest index holds only cases from about 2023 on, with the older docket
     numbers kept (23-00073-UT) and new ones numbered 26-0000114. Rio Grande 6
     (20-00194-UT) and Rio Grande 7 (23-00403-UT) are not in it. Those two are
     listed as "not in the guest index" and answered from the commission's
     other records by the sweep. The case page link is
     https://e360.prc.nm.gov/portal/public/#/public/nm-prc/en/CaseXscreen?screen=external-Case360&caseId=<caseid>.
     A document has no stable address of its own: a note cites the case page
     link and the document number and title.

Steps:
  1. List every case in the guest index (cached for the day in scopes/us-nm/work/psc/),
     add the term searches (utilities, leads) and the hand-checked KNOWN_CASES,
     and keep cases filed from --from-year whose caption or category is about
     generation, a resource plan, an abandonment, a data center or large load, or a
     purchased power agreement, plus every case of the named utilities that
     matches those keywords.
  2. For each kept case list all its documents.
  3. For a key case (gas or generation, not only wires, wind, solar or a rule),
     download the orders, applications, plans, testimony summaries and notices
     (capped, orders and applications first) into scopes/us-nm/work/psc/<case>/ (not
     committed), extract each with pdftotext -layout, and keep the sentences that
     name a plant or lead, a megawatt figure for gas, a retirement date, an
     in-service date or a place. A file over --max-mb is skipped unless its document
     id is in ALWAYS_DOWNLOAD (the SPS 2026 plan, 140 MB, 2,425 pages); downloads
     stream to disk.
  4. Match cases to the New Mexico plants in the scoped GEM export.

Output, in batches/us-nm/harvest/: psc_dockets.json and psc_dockets.md.
build_state_brief.py --harvest reads only the name psc_dockets.json (the plan
calls the file prc_dockets.json; the brief builder wins). One entry per case,
"docket" is the case number. Filer names are not kept. Nothing here stages a record.

Usage (from the repo root):
    python scopes/us-nm/harvest_prc.py                          # from 2021, read key documents
    python scopes/us-nm/harvest_prc.py --no-docs                # list cases and documents, download nothing
    python scopes/us-nm/harvest_prc.py --cases 23-00403-UT      # only these cases
    python scopes/us-nm/harvest_prc.py --match-only batches/us-nm/harvest/psc_dockets.json
"""
import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from fetch import CHROME_UA  # noqa: E402
from harvest_lib import (DOCKET_MAKER, DOCKET_SIZE, REPO, clean_ws, docket_cache,  # noqa: E402
                         merge_facts, norm_county, report_failure, sentences)

SITE = "https://e360.prc.nm.gov"
CORE = SITE + "/core/api/"
CASES_API = CORE + "_q/v1/prc/nm/intake/dashboard/getAllCases"
DOCS_API = CORE + "apiflow/v1/prc/nm/intake/casepublicdocument/getAll"
TOKEN_API = CORE + "apiflow/v1/casex/cms/downloadToken"
PREVIEW = CORE + "document/v1/previewDocument"
CASE_PAGE = SITE + "/portal/public/#/public/nm-prc/en/CaseXscreen?screen=external-Case360&caseId={cid}"
OUT = REPO / "batches" / "us-nm" / "harvest"
WORK = docket_cache("us-nm")
STATE = "New Mexico"

# Documents downloaded whatever their size.
ALWAYS_DOWNLOAD = {"f1f5a543-d072-43bf-a67d-b4ec01397c98"}      # SPS 2026 IRP, case 25-00076-UT

# Cases read whatever the case list says: case number -> (title when the portal lacks the case,
# regexes over GEM plant names the case is about). An empty list means the case is matched by
# name. Hand-checked 2026-11-17 from the plan's known leads.
KNOWN_CASES = {
    "25-00022-UT": ("PNM 2026 integrated resource plan", []),
    "25-00076-UT": ("SPS 2026 integrated resource plan", []),
    "24-00260-UT": ("EPE 2025 integrated resource plan", []),
    "23-00073-UT": ("SPS 2023 integrated resource plan", []),
    "25-00066-UT": ("SPS certificates for 3,850 MW incl. 2,088 MW of gas, approved 2026-05-07", []),
    "23-00409-UT": ("PNM 2023 integrated resource plan", []),
    "20-00194-UT": ("EPE abandonment of Rio Grande Unit 6", [r"rio grande"]),
    "23-00403-UT": ("EPE abandonment of Rio Grande Unit 7", [r"rio grande"]),
}

# Searches run in addition to the full list: utilities, then the plan's known leads and plants.
UTILITY_TERMS = ["Public Service Company of New Mexico", "PNM", "Southwestern Public Service", "El Paso Electric",
                 "Tri-State", "Cooperative", "Kit Carson", "Farmington", "Los Alamos", "Navajo", "Western Farmers"]
LEAD_TERMS = ["Pyramid", "NTEC", "Navajo Transitional", "Westside", "Saddle Butte", "Lea County", "New Era", "Roswell",
              "Zenith", "Site Layer", "Jupiter", "Hobbs", "Cunningham", "Maddox", "Reeves", "Afton", "Lordsburg",
              "La Luz", "Rio Bravo", "Luna", "Newman", "Rio Grande", "Four Corners", "San Juan", "Bluffview",
              "Chino", "data center", "large load", "abandon", "retire", "resource plan", "certificate",
              "power purchase", "purchased power", "gas"]
UTILITY = re.compile(r"public service company of new mexico|\bpnm\b|southwestern public service|\bsps\b|el paso electric|"
                     r"\bepe\b|tri-state|cooperative|kit carson|farmington electric|los alamos|navajo|"
                     r"western farmers|continental divide|otero|socorro|central valley|mora-san miguel|"
                     r"springer|jemez|northern rio arriba|sierra electric|columbus electric|lea county electric|"
                     r"southwestern electric", re.I)
GEN = re.compile(r"integrated resource|\bIRP\b|resource plan|certificate of (public )?convenience|\bCCN\b|"
                 r"abandon|retire|retirement|decommission|data cent|large load|large[- ]customer|special contract|"
                 r"purchased power|power purchase|\bPPA\b|capacity|generat|power plant|station|turbine|"
                 r"combined[- ]cycle|energy storage agreement|system resources|resource (acquisition|procurement)|"
                 r"request for proposals?|\bRFP\b|cogenerat|\bgas\b|peaker|energy center|power purchase", re.I)
GAS = re.compile(r"\bgas\b|turbine|combined[- ]cycle|peak|reciprocating|generat|power plant|station|data cent|"
                 r"large load|large[- ]customer|resource plan|integrated resource|\bIRP\b|abandon|retire|"
                 r"certificate of (public )?convenience|\bCCN\b|purchased power|power purchase|\bPPA\b|capacity|"
                 r"system resources|resource (acquisition|procurement)|request for proposals?|\bRFP\b|special contract",
                 re.I)
WIRES = re.compile(r"transmission|\bkv\b|substation|\bline\b|right[- ]of[- ]way|rio puerco|hvdc|high[- ]voltage", re.I)
WIND_SOLAR = re.compile(r"\bwind\b|solar|photovoltaic|battery|storage|renewable energy (portfolio|procurement)", re.I)
NOT_GEN = re.compile(r"competitive local exchange|telecommunic|advice notice|first mortgage bonds|retail rates|rate case|"
                     r"formal complaint|water|fuel (and|&) purchased power cost|amendments? to .{0,60}(rule|nmac)|"
                     r"rulemaking|\bnmac\b", re.I)
TECH = re.compile(r"combined[- ]cycle|combustion turbine|simple[- ]cycle|peaking|reciprocating|internal combustion|"
                  r"aeroderivative|frame turbine|natural gas[- ]fired|gas[- ]fired|duct[- ]fir|co-?fir|"
                  r"gas conversion|convert(ed|ing)? to (natural )?gas|fuel cell", re.I)
INSERVICE = re.compile(r"in[- ]service|commercial operation|\bCOD\b|placed in service|on[- ]line|begin operat|"
                       r"commence(ment of)? construction|construction (will|to) (begin|start|commence)", re.I)
RETIRE = re.compile(r"retire|retirement|deactivat|mothball|cease operat|shut ?down|decommission|abandon", re.I)
LOCATION = re.compile(r"located (at|in|on|near|approximately)|site (is|in|at)|county,? new mexico|"
                      r"latitude|longitude|acres? (site|parcel|tract)", re.I)
GAS_WORD = re.compile(r"\bgas\b|turbine|combined[- ]cycle|simple[- ]cycle|peaker|peaking|reciprocating|"
                      r"natural gas|generating|\bCT\b|\bCC\b|\bRICE\b", re.I)
LATLON = re.compile(r"\b(3[1-7]\.\d{3,})[\s,;/°N-]{1,12}(10[3-9]\.\d{3,})\b")

# Plant and lead names whose sentences are kept from a document (lower-case regexes).
LEAD_NAMES = {
    "Pyramid": r"\bpyramid\b", "Cunningham": r"\bcunningham\b", "Maddox": r"\bmaddox\b", "Reeves": r"\breeves\b",
    "Afton": r"\bafton\b", "Lordsburg": r"\blordsburg\b", "La Luz": r"\bla luz\b", "Rio Bravo": r"\brio bravo\b",
    "Luna": r"\bluna (energy|generating|station|facility)\b", "Rio Grande": r"\brio grande (unit|generating|station|\d)",
    "Newman": r"\bnewman\b", "Hobbs": r"\bhobbs (generating|station|plant|power|swpp|eras)\b",
    "Westside": r"\bwestside\b", "NTEC": r"\bntec\b|navajo transitional", "Four Corners": r"\bfour corners\b",
    "Lea County data center": r"lea county data|new era energy", "Project Jupiter": r"project jupiter",
    "Roswell Information Park": r"roswell information park|\bE2B4\b|sustany", "Site Layer": r"site layer",
    "Zenith Volts": r"zenith volts", "Chino": r"\bchino\b", "Bluffview": r"\bbluffview\b", "San Juan": r"\bsan juan (generating|station|plant)\b",
    "Escalante": r"\bescalante\b", "Valencia": r"valencia energy", "Rio Puerco": r"rio puerco",
}
DOC_PRIORITY = re.compile(r"application|testimony|order|report|settlement|stipulation|exhibit|resource plan|\bIRP\b|"
                          r"integrated resource|request for proposal|\bRFP\b|notice|summary|portfolio|abandon|"
                          r"certificate|plan\b|agreement|disposition|recommended decision", re.I)
DOC_SKIP = re.compile(r"pro hac vice|entry of appearance|notice of appearance|certificate of service|affidavit|"
                      r"proof of publication|transcript|confidentiality ?agreement|protective order|motion for admission|"
                      r"notice of screening|errata|exhibit list|witness list|cover letter|letter of counsel|"
                      r"motion (to|for) (intervene|extend|withdraw|deviat|leave|continue)|certificate of registration|"
                      r"return receipt|scheduling|prehearing|rescheduling|extending (the )?deadline|setting (a )?deadline|procedural (order|variance)|"
                      r"facilitator|order on designation|status update|"
                      r"granting (motion|request) .{0,40}(extension|variance)|data request|discovery", re.I)


def log(msg):
    print(f"[harvest-nm-prc] {msg}", file=sys.stderr, flush=True)


NAME_NOISE = re.compile(
    r"\b(power station|power plant|generating station|generating|generation|facility|station|energy center|"
    r"energy|plant|power|nm|new|mexico|the|of|and|city|llc|inc|company|co|corp|corporation|combined|cycle|county|"
    r"industrial|park|campus|data|center|unit|units|phase|east|west|north|south|gen|stn|solar|storage)\b", re.I)


def words(text):
    t = NAME_NOISE.sub(" ", re.sub(r"\(.*?\)", " ", str(text or "")))
    return {w.lower() for w in re.split(r"[^A-Za-z]+", t) if len(w) >= 4}


def iso(s):
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", str(s or ""))
    return m.group(0) if m else ""


def load_plants(args=None, csv_path=None):
    """The scoped export's New Mexico plants: [{id, name, city, county, statuses, name_words}]."""
    import pandas as pd
    from harvest_lib import CSV
    csv = pd.read_csv(csv_path or CSV, low_memory=False, encoding="utf-8-sig")
    csv = csv[csv["State/Province"] == STATE]
    wanted = set(args.plants.split(",")) if args is not None and getattr(args, "plants", None) else None
    plants = []
    for pid, rows in csv.groupby("GEM location ID", sort=False):
        if wanted is not None and pid not in wanted:
            continue
        r = rows.iloc[0]
        city = r.get("City") if isinstance(r.get("City"), str) else ""
        county = r.get("Local area (taluk, county)")
        plants.append({"id": pid, "name": r["Plant name"], "city": city,
                       "county": norm_county(county).title() if isinstance(county, str) else "",
                       "statuses": sorted(set(rows["Status"].astype(str))),
                       "name_words": words(r["Plant name"])})
    return plants


# ---------------------------------------------------------------- network ---

def search_body(term, page, size):
    p = {"screen": "external-Dashboard", "searchTerm": term}
    return {"data": {}, "origin": "", "origin_key": "CaseX", "queryParams": ["screen"],
            "gridInput": {"params": {"parameters": p}, "persistPrevParams": False},
            "parameters": p, "pageNo": page, "pageSize": size, "sortBy": {}}


def docs_body(case_id, page, size, term=""):
    p = {"caseId": case_id, "searchTerm": term}
    return {"data": {}, "origin": "", "origin_key": "CaseX", "queryParams": ["caseId"],
            "gridInput": {"params": {"parameters": p}, "persistPrevParams": False},
            "parameters": p, "pageNo": page, "pageSize": size, "sortBy": {}}


def token_body(doc):
    return {"context": "File", "documentId": doc["id"], "fileName": doc.get("docname") or doc["id"],
            "annotationType": "WITH_ANNOTATION", "isPreview": True}


class PRC:
    def __init__(self, pause=0.4):
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": CHROME_UA, "Content-Type": "application/json", "Accept": "application/json"})
        self.pause = pause
        self.failed = []

    def post(self, url, body):
        err = "000"
        for attempt in range(4):
            try:
                time.sleep(self.pause)
                r = self.s.post(url, json=body, timeout=90)
                if r.status_code == 200:
                    return r.json()
                err = str(r.status_code)
            except (requests.RequestException, ValueError) as e:
                err = "000"
                log(f"  {url}: {str(e)[:100]}")
            time.sleep(3 * (attempt + 1))
        self.failed.append(url)
        report_failure(url, err, "PRCe360 call failed four times")
        return None

    def search(self, term, page_size=100):
        """Every case matching a term (all pages)."""
        out, page = [], 1
        while True:
            r = self.post(CASES_API, search_body(term, page, page_size))
            if r is None:
                return out if out else None
            out += r.get("items") or []
            if len(out) >= int(r.get("totalItemCount") or 0) or not r.get("items"):
                return out
            page += 1

    def documents(self, case_id):
        out, page = [], 1
        while True:
            r = self.post(DOCS_API, docs_body(case_id, page, 100))
            if r is None:
                return out if out else None
            out += r.get("items") or []
            if len(out) >= int(r.get("totalItemCount") or 0) or not r.get("items"):
                return out
            page += 1

    def download(self, doc, path, max_bytes):
        """Token, then stream the PDF to disk. False (with the reason logged) on any failure."""
        t = self.post(TOKEN_API, token_body(doc))
        token = (t or {}).get("token")
        if not token:
            return False
        url = f"{PREVIEW}?token={token}"
        tmp = path.with_suffix(".part")
        try:
            time.sleep(self.pause)
            with self.s.get(url, timeout=600, stream=True, headers={"Content-Type": "application/pdf"}) as r:
                if r.status_code != 200:
                    report_failure(f"{PREVIEW}?document={doc['id']}", r.status_code, "PRCe360 document download")
                    return False
                size = int(r.headers.get("content-length") or 0)
                if size > max_bytes and doc["id"] not in ALWAYS_DOWNLOAD:
                    log(f"  skipped, {size // 1_000_000} MB is larger than {max_bytes // 1_000_000} MB: {doc.get('documentname', '')[:60]}")
                    return False
                path.parent.mkdir(parents=True, exist_ok=True)
                n, head = 0, b""
                with open(tmp, "wb") as f:
                    for chunk in r.iter_content(1 << 20):
                        if not head:
                            head = chunk[:5]
                        n += len(chunk)
                        if n > max_bytes and doc["id"] not in ALWAYS_DOWNLOAD:
                            log(f"  skipped, larger than {max_bytes // 1_000_000} MB: {doc.get('documentname', '')[:60]}")
                            f.close()
                            tmp.unlink(missing_ok=True)
                            return False
                        f.write(chunk)
        except requests.RequestException as e:
            report_failure(f"{PREVIEW}?document={doc['id']}", "000", f"PRCe360 document download: {str(e)[:80]}")
            tmp.unlink(missing_ok=True)
            return False
        if head != b"%PDF-":
            report_failure(f"{PREVIEW}?document={doc['id']}", "200", "PRCe360 download is not a PDF")
            tmp.unlink(missing_ok=True)
            return False
        tmp.replace(path)
        return True


# -------------------------------------------------------------- case list ---

def case_row(x):
    """One getAllCases item as the harvester's case record (filer names are dropped)."""
    cap = clean_ws(x.get("casecaption"))
    return {"docket": x["casenumber"], "case_id": x.get("caseid", ""), "service": x.get("casetype") or "",
            "category": clean_ws(x.get("casecategory")), "utility": clean_ws(x.get("company")).title(),
            "filed": iso(x.get("filedon")), "title": cap, "status": x.get("statusdescription") or "",
            "url": CASE_PAGE.format(cid=x["caseid"]) if x.get("caseid") else ""}


def classify(d):
    """(relevant, key, reasons): relevant = a case about generation, a resource plan, an
    abandonment, a data center or large load, or a purchased power agreement; key = one whose
    documents are read (not only wires, wind, solar, rules, rates or telecommunications)."""
    head = f"{d.get('title', '')} {d.get('category', '')}"
    reasons = []
    known = d["docket"] in KNOWN_CASES
    if known:
        reasons.append("on the hand-checked list")
    dc = bool(re.search(r"data cent|large load|large[- ]customer", head, re.I))
    gen = bool(GEN.search(head)) and (dc or not NOT_GEN.search(d.get("title", "")))
    if gen:
        reasons.append("its caption or category is about generation, a resource plan, an abandonment, a data "
                       "center or large load, or a power purchase agreement")
    if gen and UTILITY.search(d.get("utility", "")):
        reasons.append("one of the named utilities")
    wires_only = bool(WIRES.search(d.get("title", ""))) and not re.search(
        r"generat|\bplant\b|generating station|power station|energy center|turbine|resource plan|abandon|"
        r"system resources|power purchase|purchased power",
        d.get("title", ""), re.I)
    ws_only = bool(WIND_SOLAR.search(head)) and not re.search(
        r"\bgas\b|turbine|combined|peak|generating station|resource plan|abandon|data cent|large load", head, re.I)
    relevant = bool(reasons)
    key = known or (gen and bool(GAS.search(head)) and not wires_only and not ws_only)
    return relevant, key, reasons


# ---------------------------------------------------------- document facts ---

def pick_s(sents, rx, limit, lo=20, hi=420):
    out = []
    for s in sents:
        if rx.search(s) and lo < len(s) < hi and s not in out:
            out.append(s)
            if len(out) >= limit:
                break
    return out


def doc_facts(text):
    """Sentences a researcher wants from one document: plants and leads named, gas megawatts,
    retirement and in-service dates, location and equipment."""
    sents = sentences(text)
    yr = r".*\b20[2-5]\d\b|\b20[2-5]\d\b.*"
    gas_mw = [s for s in sents if DOCKET_SIZE.search(s) and GAS_WORD.search(s) and 20 < len(s) < 420]
    leads = {}
    for name, rx in LEAD_NAMES.items():
        hits = pick_s(sents, re.compile(rx, re.I), 3)
        if hits:
            leads[name] = hits
    return {
        "technology": sorted({m.group(0).lower() for m in TECH.finditer(text)})[:8],
        "equipment_maker_model": pick_s(sents, DOCKET_MAKER, 8),
        "megawatts": list(dict.fromkeys(gas_mw))[:10],
        "in_service": pick_s(sents, re.compile(f"({INSERVICE.pattern}){yr}({INSERVICE.pattern})?", re.I), 6),
        "retirement": pick_s(sents, re.compile(f"({RETIRE.pattern}){yr}({RETIRE.pattern})?", re.I), 8),
        "location": pick_s(sents, LOCATION, 6),
        "coords": [f"{a}, -{b.lstrip('-')}" for a, b in LATLON.findall(text)][:3],
        "leads": leads,
    }


def merge_all(parts):
    """merge_facts for the list keys, plus the per-lead sentence dict (three per lead)."""
    leads = {}
    for p in parts:
        for k, v in (p.get("leads") or {}).items():
            cur = leads.setdefault(k, [])
            cur += [x for x in v if x not in cur]
    out = merge_facts([{k: v for k, v in p.items() if k != "leads"} for p in parts])
    out["leads"] = {k: v[:6] for k, v in leads.items()}
    return out


def pdf_text(path):
    """Plain text of a PDF with the layout kept; a scanned small one goes through OCR."""
    try:
        t = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True,
                           timeout=900).stdout
    except (subprocess.SubprocessError, OSError):
        t = ""
    if len(t.strip()) < 300 and Path(path).stat().st_size < 15_000_000:
        import fetch
        try:
            ocr = fetch._pdf_ocr(str(path))
        except Exception:  # noqa: BLE001
            ocr = ""
        if len(ocr.strip()) > len(t.strip()):
            t = ocr
    return t


# ------------------------------------------------------------ choosing docs ---

def doc_record(x):
    """A getAll documents item without filer names."""
    return {"id": x["id"], "number": x.get("documentnumber", ""), "name": clean_ws(x.get("documentname"))[:300],
            "type": x.get("documenttype") or "", "date": iso(x.get("fileddate") or x.get("filedon")),
            "docname": x.get("docname") or x["id"], "contenttype": x.get("contenttype") or x.get("docType") or "",
            "can_download": x.get("candownload") is not False}


def is_order(d):
    return bool(re.match(r"orders?\b", d["type"], re.I) or re.match(r"(final |recommended )?order\b", d["name"], re.I)
                or re.search(r"commission order", d["type"], re.I))


def pick_docs(docs, cap):
    """PDFs only, ranked: orders on the merits, applications, plans and reports, testimony
    summaries, notices; newest first within a rank. Never appearances, service certificates,
    confidentiality agreements, procedural scheduling orders or motions to extend. Documents
    in ALWAYS_DOWNLOAD come first whatever the cap."""
    scored = []
    for d in docs:
        if "pdf" not in d["contenttype"].lower() or not d["can_download"]:
            continue
        own = f"{d['name']} {d['type']}"
        if d["id"] in ALWAYS_DOWNLOAD:
            scored.append((-99, "", d))
            continue
        if DOC_SKIP.search(own) and not re.search(r"abandon|certificate of public convenience|integrated resource", own, re.I):
            continue
        s = 0
        if is_order(d):
            s += 6 + (3 if re.search(r"approv|grant|accept|certificate|abandon|final|recommended|resource plan|"
                                     r"integrated resource", d["name"], re.I) else 0)
        if re.search(r"application|petition|request for approval", own, re.I):
            s += 8
        if re.search(r"integrated resource plan|\bIRP\b|resource plan|report|portfolio|request for proposal|\bRFP\b", own, re.I):
            s += 7
        if re.search(r"summary of (direct |rebuttal )?testimony|testimony summary|executive summary", own, re.I):
            s += 6
        elif re.search(r"testimony", own, re.I):
            s += 2
        if re.search(r"notice", own, re.I):
            s += 2
        if DOC_PRIORITY.search(own):
            s += 1
        scored.append((-s, "".join(chr(255 - ord(c)) for c in d["date"]), d))
    out = []
    for *_, d in sorted(scored, key=lambda x: x[:2]):
        out.append(d)
        if len([x for x in out if x["id"] not in ALWAYS_DOWNLOAD]) >= cap:
            break
    return out


def doc_file(folder, doc):
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", f"{doc['number']}_{doc['name']}")[:100].strip("_")
    return folder / (safe + ".pdf")


def read_doc(prc, doc, folder, max_bytes):
    pdf = doc_file(folder, doc)
    txt = pdf.with_suffix(".txt")
    if txt.exists():
        return txt.read_text(errors="replace"), txt
    text = ""
    if (pdf.exists() and pdf.read_bytes()[:5] == b"%PDF-") or prc.download(doc, pdf, max_bytes):
        text = pdf_text(pdf)
    if text.strip():
        txt.write_text(text)
    return text, txt


def read_case(prc, d, cap, max_bytes, read_docs=True):
    """List the case's documents; then read the key ones."""
    if not d.get("case_id"):
        d["store_state"] = "not in the PRCe360 guest index"
        return
    rows = prc.documents(d["case_id"])
    if rows is None:
        d["store_state"] = "the document list did not load"
        return
    docs = sorted((doc_record(x) for x in rows), key=lambda x: x["date"], reverse=True)
    d["documents_listed"] = len(docs)
    d["latest_filing"] = max((x["date"] for x in docs if x["date"]), default="")
    d["filings"] = [{"number": x["number"], "date": x["date"], "type": x["type"], "title": x["name"][:200]} for x in docs]
    d["orders"] = [{"date": x["date"], "title": x["name"][:200], "number": x["number"], "url": d["url"]}
                   for x in docs if is_order(x)][:12]
    if not read_docs:
        d["store_state"] = f"{len(docs)} documents listed, none downloaded"
        return
    folder = WORK / d["docket"]
    folder.mkdir(parents=True, exist_ok=True)
    out, parts = [], []
    for doc in pick_docs(docs, cap):
        text, txt = read_doc(prc, doc, folder, max_bytes)
        rec = {"title": doc["name"][:200], "number": doc["number"], "kind": doc["type"] or "filing", "date": doc["date"],
               "url": d["url"], "document_id": doc["id"], "saved": str(txt.relative_to(REPO)) if txt.exists() else "",
               "read": len(text.strip()) >= 300}
        if rec["read"]:
            rec["facts"] = doc_facts(text)
            parts.append(rec["facts"])
        out.append(rec)
        log(f"    {doc['number']} {doc['name'][:70]}: {'read' if rec['read'] else 'not read'}")
    d["documents"], d["facts"] = out, merge_all(parts)
    d["store_state"] = f"{len(docs)} documents listed, {sum(1 for r in out if r['read'])} read"
    d["text_blob"] = " ".join(p.read_text(errors="replace") for p in sorted(folder.glob("*.txt")))


# ------------------------------------------------------------------ match ---

def plant_patterns(plant):
    """Regexes over a case title for one plant: its name with the generic words dropped."""
    ws = sorted(plant["name_words"])
    return [r"\b" + re.escape(" ".join(ws)) + r"\b"] if len(ws) > 1 else ([r"\b" + re.escape(ws[0]) + r"\b"] if ws else [])


def match_docket(plant, d, others_by_title=False):
    """How a case matches a plant, or None: the hand-checked list, the plant's name in the case
    title or an order (strong), or, for a case with no hand-checked plants and no plant in its
    title, in the documents read five or more times. A resource plan names every plant the
    utility owns, so document mentions alone never add a plant to a case that is hand-checked."""
    known = KNOWN_CASES.get(d["docket"])
    if known and any(re.search(p, plant["name"], re.I) for p in known[1]):
        return "on the hand-checked case list"
    head = f"{d.get('title', '')} {' '.join(o.get('title', '') for o in d.get('orders', []))}".lower()
    pats = plant_patterns(plant)
    if not pats:
        return None
    if any(re.search(p, head, re.I) for p in pats):
        return "name in the case title or an order"
    if known or others_by_title:
        return None
    blob = d.get("text_blob", "")
    n = len({m.start() for p in pats for m in re.finditer(p, blob, re.I)})
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
    L = [f"- **{d['docket']}**, {d.get('utility') or 'utility not shown'}: {d['title'][:300]}",
         f"  - {d.get('category') or 'category not shown'}; filed {d.get('filed') or 'unknown'}"
         + (f"; newest filing {d['latest_filing']}" if d.get("latest_filing") else "")
         + (f"; {d['documents_listed']} documents listed" if d.get("documents_listed") else "")
         + f"; case page {d.get('url') or 'not in the PRCe360 guest index'}"]
    if d.get("store_state") and "not in" in d["store_state"]:
        L.append(f"  - {d['store_state']}: look for it in the commission's other records or ask the PRC records office")
    for o in d.get("orders", [])[:6]:
        L.append(f"  - order ({o['date']}): {o['title'][:140]}, {o['number']}")
    if full and d.get("facts"):
        f = d["facts"]
        for k, label in [("technology", "Technology"), ("megawatts", "Gas megawatts"),
                         ("equipment_maker_model", "Equipment"), ("in_service", "In service"),
                         ("retirement", "Retirements"), ("location", "Location"), ("coords", "Coordinates")]:
            if f.get(k):
                L.append(f"  - {label}: " + " | ".join(f[k][:4]))
        for name, hits in (f.get("leads") or {}).items():
            L.append(f"  - {name}: " + " | ".join(h[:260] for h in hits[:2]))
    for doc in d.get("documents", []):
        L.append(f"  - {'read' if doc.get('read') else 'not read'}: {doc['number']} {doc['title'][:100]} "
                 f"({doc['kind']}, {doc['date']}); saved copy {doc.get('saved') or 'none'}")
    return L


def write_outputs(out_dir, plants, dockets, by_plant, matched, sources, today, from_year):
    out_dir.mkdir(parents=True, exist_ok=True)
    slim = [{k: v for k, v in d.items() if k != "text_blob"} for d in dockets]
    unmatched = [d for d in dockets if d.get("key") and d["docket"] not in matched]
    data = {"generated": today, "from_year": from_year, "sources": sources, "dockets": slim,
            "by_plant": by_plant, "unmatched_generation": [d["docket"] for d in unmatched],
            "not_in_guest_index": [d["docket"] for d in dockets if not d.get("case_id")]}
    (out_dir / "psc_dockets.json").write_text(json.dumps(data, indent=1, default=str))
    by_id = {d["docket"]: d for d in dockets}
    L = [f"# New Mexico Public Regulation Commission cases on generation ({today})", "",
         f"Cases filed {from_year} or later whose captions are about generation, a resource plan, an abandonment, a "
         "data center or large load, or a power purchase agreement, plus the hand-checked list. A document has no "
         "address of its own in PRCe360: cite the case page link with the document number and title. Copies of "
         "documents read are in scopes/us-nm/work/psc/ and are not committed.", "", "## Sources", ""]
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
    L += ["", "## Other generation-related cases (wires, wind, solar; not read)", ""]
    for d in sorted((d for d in dockets if d.get("relevant") and not d.get("key")), key=lambda x: x["docket"]):
        L += docket_block(d, full=False)
    (out_dir / "psc_dockets.md").write_text("\n".join(L) + "\n")
    return unmatched


# ------------------------------------------------------------------- main ---

def collect_cases(prc, a, today):
    """{docket: case record} from the full list, the term searches and the hand-checked cases;
    plus the searches that found nothing for a named case."""
    cases, notes = {}, []
    if a.cases:
        for k in [c.strip() for c in a.cases.split(",") if c.strip()]:
            hit = None
            for term in (k, re.sub(r"-UT$", "", k)):
                rows = prc.search(term) or []
                hit = next((x for x in rows if x["casenumber"].upper() == k.upper()), None)
                if hit:
                    break
            if hit:
                cases[k] = case_row(hit)
            else:
                cases[k] = {"docket": k, "case_id": "", "title": KNOWN_CASES.get(k, ("",))[0], "filed": "", "service": "",
                            "category": "", "utility": "", "url": ""}
                notes.append(f"{k}: searched by number, no match in the PRCe360 guest index")
        return cases, notes
    full = prc.search("")
    if full is None:
        notes.append("the full case list did not load")
    for x in full or []:
        cases[x["casenumber"]] = case_row(x)
    log(f"full list: {len(full or [])} cases")
    for term in UTILITY_TERMS + LEAD_TERMS:
        for x in prc.search(term) or []:
            cases.setdefault(x["casenumber"], case_row(x))
    log(f"after {len(UTILITY_TERMS) + len(LEAD_TERMS)} term searches: {len(cases)} cases")
    for k, (title, _) in KNOWN_CASES.items():
        if k not in cases:
            hit = next((x for x in (prc.search(k) or []) if x["casenumber"].upper() == k.upper()), None)
            if hit:
                cases[k] = case_row(hit)
            else:
                cases[k] = {"docket": k, "case_id": "", "title": title, "filed": "", "service": "", "category": "",
                            "utility": "", "url": ""}
                notes.append(f"{k}: searched by number, no match in the PRCe360 guest index")
    return cases, notes


def main():
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    ap.add_argument("--from-year", type=int, default=2021)
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--plants", help="comma-separated GEM location IDs")
    ap.add_argument("--cases", help="comma-separated case numbers: read only these")
    ap.add_argument("--docs-per-docket", type=int, default=12)
    ap.add_argument("--max-mb", type=float, default=80, help="skip documents larger than this")
    ap.add_argument("--pause", type=float, default=0.4, help="seconds between calls")
    ap.add_argument("--no-docs", action="store_true", help="list cases and documents, download nothing")
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

    prc = PRC(a.pause)
    cases, notes = collect_cases(prc, a, today)
    dockets = []
    for d in cases.values():
        d["relevant"], d["key"], d["reasons"] = classify(d)
        if a.cases:
            d["relevant"] = d["key"] = True
            d["reasons"].append("named on the command line")
        elif d["filed"] and int(d["filed"][:4]) < a.from_year and d["docket"] not in KNOWN_CASES:
            d["relevant"] = d["key"] = False
        elif not d["key"] and not NOT_GEN.search(d["title"]) and not WIRES.search(d["title"]) \
                and any(match_docket(p, {**d, "text_blob": ""}) for p in plants):
            d["relevant"] = d["key"] = True
            d["reasons"].append("its caption names a GEM plant")
        if d["relevant"]:
            dockets.append(d)
    log(f"{len(dockets)} generation related; {sum(1 for d in dockets if d['key'])} key")

    for n, d in enumerate(sorted(dockets, key=lambda x: x["docket"]), 1):
        d.setdefault("documents", [])
        d.setdefault("facts", {})
        d["text_blob"] = ""
        if not d["key"] and not a.no_docs:
            d["store_state"] = "listed, not read"
            continue
        log(f"({n}/{len(dockets)}) {d['docket']}: {d['title'][:90]}")
        read_case(prc, d, a.docs_per_docket, int(a.max_mb * 1e6), read_docs=not a.no_docs and d["key"])
        log(f"    {d.get('store_state', '')}")

    sources = [
        {"name": "PRCe360 case search (getAllCases)", "url": CASES_API,
         "how": ("cases named on the command line, searched by number" if a.cases else
                 "the full guest case list plus term searches for the utilities and leads")
                + (f"; {'; '.join(notes)}" if notes else "")},
        {"name": "PRCe360 case documents (casepublicdocument/getAll) and token downloads", "url": DOCS_API,
         "how": f"every key case, up to {a.docs_per_docket} documents read per case"
                + ("; documents not downloaded (--no-docs)" if a.no_docs else "")
                + (f"; calls that failed: {len(prc.failed)}" if prc.failed else "")}]
    by_plant, matched = match_all(plants, dockets)
    unmatched = write_outputs(Path(a.out), plants, dockets, by_plant, matched, sources, today.isoformat(), a.from_year)
    log(f"{len(matched)} cases matched to plants; {len(unmatched)} key cases unmatched")
    for p in plants:
        if by_plant[p["id"]]:
            log(f"  {p['name']}: {', '.join(by_plant[p['id']])}")


if __name__ == "__main__":
    main()

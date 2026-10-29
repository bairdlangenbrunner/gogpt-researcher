"""
Harvest North Dakota Public Service Commission cases on generation before a research sweep.

The North Dakota Public Service Commission (PSC) sites every energy conversion
facility of 50 MW or more (a certificate of site compatibility, North Dakota
Century Code chapter 49-22) and every transmission line of 115 kV or more, so a
gas plant, a peaker or a large data center plant with its own generation shows
up as a siting case before it is built. What was found (2026-10-29):

  1. Case search, apps.psc.nd.gov/cases/pscasesearch: a plain form POST (no
     login; a session cookie is set on the first answer). Search by filing
     date, entity name or description. The answer lists cases as rows: case
     number (PU-25-086), description, case type and category (Siting
     Application, Electric), entities, docket count, filing and closing dates.
     It shows at most 100 rows ("100 of 1,006 Cases") and its paging link does
     not work, so a date search is split into shorter windows until each
     answer is complete.
  2. Case detail, pscasedetail?getId=<yy>&getId2=<sequence>: the filing date,
     description, type, category, entities and every docket entry (number,
     title, kind, page count, on behalf of, filing date). The "Filed By" column
     names a person and is not kept.
  3. The documents, www.psc.nd.gov/webdocs/case/<yy>-<nnnn>/: a plain folder
     listing of PDFs named <docket>-<attachment>.pdf (001-020.pdf is docket 1,
     second attachment) with date and size. The listing is a stable,
     anonymous link per document, so a fact read here can be cited.
  4. The siting page, www.psc.nd.gov/jurisdictions/siting: the Commission's
     siting spreadsheet PDF (every sited facility) and its map of wind
     projects. The lines of the spreadsheet that name gas or a GEM plant are
     kept.

Steps:
  1. Search by filing date from --from-date (split until complete), by each
     owner in ENTITIES and by each word in DESCRIPTIONS; add the KNOWN_CASES.
  2. Keep electric cases on generation (gas, generating station, energy
     center, peaking, data center) and every utility's ten year plan (it lists
     planned plants and retirements); transmission-only and wind or
     solar-only cases are listed, not read.
  3. For each kept case read the detail page and the documents folder, then
     download the key documents (applications, orders, findings, testimony;
     larger first) into scopes/us-nd/work/psc/<case>/ (not committed: filings
     carry staff and landowner contact details) and keep the lines that give
     technology, megawatts, maker and model, in-service and retirement years,
     and location.
  4. Match cases to the North Dakota plants in the scoped GEM export by name
     in the case description or entities (strong) or by name in the text of
     the documents read (three or more times).

Output, in batches/us-nd/harvest/: psc_dockets.json (read by
build_state_brief.py --harvest; one entry per case, "docket" is the case
number) and psc_dockets.md. Nothing here stages a record.

Usage (from the repo root):
    python scopes/us-nd/harvest_psc.py                         # search from 2022, read key documents
    python scopes/us-nd/harvest_psc.py --no-docs               # list cases, download nothing
    python scopes/us-nd/harvest_psc.py --match-only batches/us-nd/harvest/psc_dockets.json
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
from harvest_lib import (DOCKET_MAKER, DOCKET_SIZE, REPO, YEAR, clean, clean_ws, docket_cache, get,  # noqa: E402
                         merge_facts, sentences)

from paths import load_scope_module  # noqa: E402

_permits = load_scope_module("us-nd", "harvest_permits")
load_plants, words = _permits.load_plants, _permits.words

CASES = "https://apps.psc.nd.gov/cases"
SEARCH = f"{CASES}/pscasesearch"
WEBDOCS = "https://www.psc.nd.gov/webdocs/case/{folder}/"
SITING_PAGE = "https://www.psc.nd.gov/jurisdictions/siting"
SITING_PDFS = ["https://www.psc.nd.gov/sites/www/files/documents/jurisdiction/siting/Siting-Spreadsheet.pdf"]
OUT = REPO / "batches" / "us-nd" / "harvest"
WORK = docket_cache("us-nd")

ENTITIES = ["Basin Electric", "Minnkota", "Otter Tail", "Montana-Dakota", "Northern States Power",
            "Great River Energy", "Applied Digital", "Nakota", "Base Electron", "Rainbow Energy", "NextEra",
            "Cerilon", "Geronimo"]
DESCRIPTIONS = ["Generation", "Generating", "Station", "Energy Center", "Peaking", "Turbine", "Data Center", "Gas"]
# Cases read whatever the search finds (2026-10-29): gas plants, their lines and data center plants.
KNOWN_CASES = ["PU-25-086", "PU-24-342", "PU-22-380", "PU-14-829", "PU-12-509", "PU-23-325", "PU-26-155",
               "PU-24-359", "PU-24-330", "PU-26-173", "PU-26-236", "PU-26-219", "PU-26-022", "PU-26-284",
               "PU-25-263", "PU-21-325", "PU-26-254", "PU-26-277", "PU-26-256", "PU-25-280", "PU-24-365",
               "PU-11-631", "PU-13-194"]

# GEM plant -> regexes that name the plant in a case description, its entities or its documents.
PSC_KNOWN = {
    "L100000104092": [r"heskett"],
    "L100000104096": [r"spiritwood"],
    "L100000401740": [r"lonesome creek"],
    "L100000401741": [r"pioneer (gener|station|plant)", r"pioneer generating"],
    "L100000407864": [r"xcel.*fargo", r"fargo (peak|gener|station|combustion)"],
    "L100001047848": [r"\bbison\b"],
    "L100001080387": [r"river run"],
    "L100001083334": [r"polaris forge (1|one)\b", r"applied digital.*ellendale", r"ellendale.*data cent"],
    "L100001083335": [r"polaris forge (2|two)\b", r"applied digital.*harwood", r"harwood.*data cent"],
    "L100001084854": [r"nakota"],
    "L100001089055": [r"base electron"],
    "L100001089073": [r"applied digital.*harwood", r"harwood.*data cent", r"polaris forge (2|two)\b"],
    "L100001089074": [r"applied digital.*ellendale", r"ellendale.*data cent", r"polaris forge (1|one)\b"],
}

GEN = re.compile(r"generat|station|energy center|power plant|peak|turbine|combined[- ]cycle|simple[- ]cycle|"
                 r"reciprocating|\bRICE\b|conversion facilit|data cent|\bMW\b|megawatt|cogenerat|\bgas\b", re.I)
GAS = re.compile(r"\bgas\b|natural gas|turbine|combined[- ]cycle|simple[- ]cycle|peak|reciprocating|engine|"
                 r"generating station|generation station|energy center|data cent|cogenerat", re.I)
WIND_SOLAR = re.compile(r"\bwind\b|solar|photovoltaic|battery|storage|repower", re.I)
WIRES = re.compile(r"transmission|\btrans\b|\bkv\b|substation|\bline\b|\bln\b|pipeline|corridor|route", re.I)
TECH = re.compile(r"combined[- ]cycle|combustion turbine|simple[- ]cycle|peaking|reciprocating|internal combustion|"
                  r"aeroderivative|frame turbine|natural gas[- ]fired|gas[- ]fired|duct[- ]fir", re.I)
INSERVICE = re.compile(r"in[- ]service|commercial operation|\bCOD\b|placed in service|on[- ]line|begin operat|"
                       r"construction (will|to) (begin|start|commence)", re.I)
RETIRE = re.compile(r"retire|retirement|deactivat|mothball|cease operat|shut ?down|decommission", re.I)
LOCATION = re.compile(r"located (at|in|on|near|approximately)|site (is|in|at)|county,? north dakota|"
                      r"\bsection \d+|township \d+|range \d+|\bT\d{2,3}N\b|latitude|longitude", re.I)
LATLON = re.compile(r"\b(4[5-8]\.\d{3,}|49\.0\d*)\s*[,;/ ]\s*-?\s*(9[6-9]\.\d{3,}|10[0-4]\.\d{3,})\b")
DOC_PRIORITY = re.compile(r"application|order|findings|testimony|amend|notice of (filing|hearing)|"
                          r"supplement|response|exhibit|certificate|permit", re.I)
DOC_SKIP = re.compile(r"receipt|fee|affidavit of (mailing|publication)|certificate of service|transcript", re.I)


def log(msg):
    print(f"[psc-nd] {msg}", file=sys.stderr, flush=True)


def ymd(s):
    """'2025.03.05' or '03/05/2025' to 2025-03-05, or ''."""
    s = (s or "").strip()
    m = re.match(r"(\d{4})\.(\d\d)\.(\d\d)", s)
    if m:
        return "-".join(m.groups())
    m = re.match(r"(\d\d)/(\d\d)/(\d{4})", s)
    return f"{m.group(3)}-{m.group(1)}-{m.group(2)}" if m else ""


def case_parts(case):
    """'PU-25-086' -> ('PU', 25, 86)."""
    m = re.match(r"([A-Z]{2})-(\d\d)-(\d+)", case)
    return m.group(1), int(m.group(2)), int(m.group(3))


def case_url(case):
    _, yy, seq = case_parts(case)
    return f"{CASES}/pscasedetail?getId={yy}&getId2={seq}"


def webdocs_url(case):
    _, yy, seq = case_parts(case)
    return WEBDOCS.format(folder=f"{yy:02d}-{seq:04d}")


# ------------------------------------------------------------------ parsing ---

def result_count(text):
    """(shown, total) from the results header: '15 Cases:' -> (15, 15); '100 of 1,006 Cases:' -> (100, 1006)."""
    m = re.search(r"<h2>\s*([\d,]+)(?:\s+of\s+([\d,]+))?\s+Cases?:", text or "")
    if not m:
        return 0, 0
    shown = int(m.group(1).replace(",", ""))
    return shown, int((m.group(2) or m.group(1)).replace(",", ""))


def parse_results(text):
    """Case rows of a search answer."""
    out = []
    for row in re.findall(r"<tr>(.*?)</tr>", text or "", re.S):
        m = re.search(r'href="pscasedetail\?getId=(\d+)&(?:amp;)?getId2=(\d+)"[^>]*>([A-Z]{2}-\d\d-\d+)</a>', row)
        if not m:
            continue
        tds = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)
        if len(tds) < 6:
            continue
        desc = clean((re.search(r"<small>(.*?)</small>", tds[1], re.S) or [0, ""])[1])
        kind = re.split(r"<br\s*/?>", tds[2], maxsplit=1)
        out.append({"docket": m.group(3), "url": f"{CASES}/pscasedetail?getId={m.group(1)}&getId2={m.group(2)}",
                    "title": desc, "type": clean(kind[0]), "category": clean(kind[1]) if len(kind) > 1 else "",
                    "entities": [clean(x) for x in re.findall(r"<li>(.*?)</li>", tds[3], re.S) if clean(x)],
                    "doc_count": int(clean(tds[4]) or 0) if clean(tds[4]).isdigit() else 0,
                    "filed": ymd(clean(tds[5])), "closed": ymd(clean(tds[6])) if len(tds) > 6 else ""})
    return out


def parse_case(text):
    """Detail page: dates, description, type, category, entities and the docket entries
    (the person in "Filed By" is dropped)."""
    def label(name):
        m = re.search(rf"<label>{name}:</label>(.*?)<br", text or "", re.S)
        return clean(m.group(1)) if m else ""
    ent = re.search(r"<h2>Entities:</h2>(.*?)<input", text or "", re.S)
    entities = [clean_ws(x) for x in re.split(r"<br\s*/?>", ent.group(1)) if clean(x)] if ent else []
    entities = [clean(x) for x in entities]
    dockets = []
    part = (text or "").split("Dockets:</h2>", 1)
    for row in re.findall(r"<tr>(.*?)</tr>", part[1] if len(part) > 1 else "", re.S):
        row = re.sub(r"<!--.*?-->", "", row, flags=re.S)
        tds = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)
        if len(tds) < 7:
            continue
        a = re.search(r'getId3=(\d+)"[^>]*>(.*?)</a>', tds[2], re.S)
        if not a:
            continue
        dockets.append({"n": int(a.group(1)), "title": clean(a.group(2)),
                        "kind": clean((re.search(r"<small>(.*?)</small>", tds[2], re.S) or [0, ""])[1]),
                        "pages": int(clean(tds[3])) if clean(tds[3]).isdigit() else 0,
                        "on_behalf": clean(tds[4]), "filed": ymd(clean(tds[6]))})
    return {"filed": ymd(label("Date Filed")), "closed": ymd(label("Date Closed")), "title": label("Description"),
            "type": label("Type"), "category": label("Category"), "entities": entities, "entries": dockets}


def size_bytes(s):
    m = re.match(r"\s*([\d.]+)\s*([KMG]?)", s or "")
    if not m:
        return 0
    return int(float(m.group(1)) * {"": 1, "K": 1e3, "M": 1e6, "G": 1e9}[m.group(2)])


def parse_webdocs(text):
    """Files of a case's documents folder: name, docket number, attachment, date, size."""
    out = []
    for name, date, size in re.findall(r'<a href="(\d+-\d+\.pdf)">[^<]*</a>\s*</td><td[^>]*>([^<]*)</td><td[^>]*>([^<]*)', text or "", re.I):
        n, att = name[:-4].split("-")
        out.append({"file": name, "n": int(n), "attachment": int(att), "date": date.strip()[:10],
                    "size": size.strip(), "bytes": size_bytes(size)})
    return out


def siting_pdfs(text):
    """The siting page's PDF links, full addresses."""
    links = re.findall(r'href="(/sites/www/files/documents/jurisdiction/siting/[^"]+\.pdf)"', text or "")
    return sorted({"https://www.psc.nd.gov" + html.unescape(x) for x in links})


# ------------------------------------------------------------------- search ---

class Psc:
    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": CHROME_UA, "Referer": SEARCH})
        self.failed = []

    def _get(self, url, **kw):
        for i in range(3):
            try:
                r = self.s.get(url, timeout=120, **kw)
                if r.status_code == 200:
                    time.sleep(0.7)
                    return r
            except requests.RequestException:
                pass
            time.sleep(5 * (i + 1))
        return None

    def search(self, **fields):
        form = {k: "" for k in ("jurisdictionId", "casePrefix", "caseYear", "caseSequence", "sosId", "entityName",
                                "description", "filedFromDate", "filedToDate", "closedFromDate", "closedToDate",
                                "caseStatusCode", "caseTypeCode")}
        form.update(fields)
        form["search"] = "Search"
        if not self.s.cookies:
            self._get(SEARCH)
        for i in range(3):
            try:
                r = self.s.post(SEARCH, data=form, timeout=120)
                if r.status_code == 200:
                    time.sleep(0.7)
                    return r.text
            except requests.RequestException:
                pass
            time.sleep(5 * (i + 1))
        self.failed.append(", ".join(f"{k} {v}" for k, v in fields.items() if v))
        return None

    def by_dates(self, start, end, depth=0):
        """Every case filed from start to end, splitting the window while the answer is cut off."""
        text = self.search(filedFromDate=start.isoformat(), filedToDate=end.isoformat())
        if text is None:
            return []
        shown, total = result_count(text)
        if total > shown and end > start:
            mid = start + (end - start) // 2
            log(f"  {start} to {end}: {shown} of {total}, splitting")
            return self.by_dates(start, mid, depth + 1) + self.by_dates(mid + dt.timedelta(days=1), end, depth + 1)
        if total > shown:
            self.failed.append(f"filed {start}: {shown} of {total} shown")
        return parse_results(text)

    def case(self, case):
        r = self._get(case_url(case))
        return parse_case(r.text) if r is not None else None

    def webdocs(self, case):
        r = self._get(webdocs_url(case))
        return parse_webdocs(r.text) if r is not None else None

    def download(self, url, path, max_bytes):
        try:
            with self.s.get(url, timeout=600, stream=True) as r:
                if r.status_code != 200:
                    return False
                n = 0
                with path.open("wb") as fh:
                    for chunk in r.iter_content(1 << 16):
                        n += len(chunk)
                        if n > max_bytes:
                            break
                        fh.write(chunk)
            if n > max_bytes:
                path.unlink(missing_ok=True)
                return False
            return path.read_bytes()[:5] == b"%PDF-"
        except requests.RequestException:
            path.unlink(missing_ok=True)
            return False


def classify(d):
    """(relevant, key, reasons): relevant = an electric case about generation; key = one whose
    documents are read (gas or generation, not only wind, solar or wires)."""
    head = f"{d['title']} {d.get('type', '')}"
    reasons = []
    if d["docket"] in KNOWN_CASES:
        reasons.append("on the hand-checked list")
    electric = not d.get("category") or re.search(r"electric", d.get("category", ""), re.I)
    gen = bool(GEN.search(head))
    gas = bool(GAS.search(head))
    wires_only = bool(WIRES.search(d["title"])) and not re.search(r"generat|station|energy center|plant|data cent", d["title"], re.I)
    ws_only = bool(WIND_SOLAR.search(d["title"])) and not gas
    if electric and gen:
        reasons.append("an electric case about generation")
    plan = bool(re.search(r"ten year plan", head, re.I))
    if plan:
        reasons.append("a ten year plan, which lists planned plants and retirements")
    relevant = bool(reasons)
    key = d["docket"] in KNOWN_CASES or plan or (relevant and gas and not wires_only and not ws_only)
    if key and gas:
        reasons.append("gas or generating station words in the title")
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


def pick_docs(entries, files, cap, max_bytes):
    """The files most likely to hold facts: those of applications, orders, findings and testimony,
    larger files first, never receipts or mailing affidavits, never above the size cap."""
    by_n = {e["n"]: e for e in entries}
    scored = []
    for f in files:
        e = by_n.get(f["n"], {"title": "", "kind": "", "pages": 0})
        name = f"{e['title']} {e['kind']}"
        if DOC_SKIP.search(name) or f["bytes"] > max_bytes:
            continue
        s = (4 if DOC_PRIORITY.search(name) else 0) + (2 if e["pages"] >= 20 else 1 if e["pages"] >= 5 else 0)
        s += 2 if f["n"] == 1 else 0
        scored.append((-s, -f["bytes"], f["n"], f["attachment"], {**f, "title": e["title"], "kind": e["kind"]}))
    return [x[-1] for x in sorted(scored, key=lambda x: x[:4])[:cap]]


def read_case(psc, d, cap, max_bytes):
    folder = WORK / d["docket"]
    folder.mkdir(parents=True, exist_ok=True)
    files = psc.webdocs(d["docket"])
    if files is None:
        return [], {}, "documents folder did not load"
    docs, parts = [], []
    for f in pick_docs(d.get("entries", []), files, cap, max_bytes):
        url = webdocs_url(d["docket"]) + f["file"]
        rec = {"file": f["file"], "url": url, "docket_entry": f["n"], "title": f["title"], "kind": f["kind"],
               "date": f["date"], "size": f["size"], "saved": "", "read": False}
        path = folder / f["file"]
        ok = path.exists() and path.read_bytes()[:5] == b"%PDF-"
        if not ok:
            ok = psc.download(url, path, max_bytes)
        if ok:
            txt = path.with_suffix(".txt")
            text = txt.read_text(errors="replace") if txt.exists() else pdf_text(path)
            if not txt.exists():
                txt.write_text(text)
            rec["saved"] = str(path.relative_to(REPO))
            rec["read"] = len(text.strip()) >= 300
            if rec["read"]:
                rec["facts"] = doc_facts(text)
                parts.append(rec["facts"])
        docs.append(rec)
    return docs, merge_facts(parts), f"{len(files)} files in the documents folder"


# ------------------------------------------------------------------ match ---

def match_docket(plant, d, others_by_title=False):
    """How a case matches a plant, or None: the plant's name in the case description or entities
    (strong), or in the text of the documents read three or more times (six when the description
    already names another plant)."""
    head = f"{d['title']} {' '.join(d.get('entities', []))}"
    pats = PSC_KNOWN.get(plant["id"])
    if not pats:
        ws = plant["name_words"]
        return "name words in the case description, check it is this plant" if ws and ws <= words(head) else None
    if any(re.search(p, head, re.I) for p in pats):
        return "name in the case description or entities"
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
    L = [f"- **{d['docket']}**, {d['utility'] or 'applicant not shown'}: {d['title'][:300]}",
         f"  - {d.get('type') or 'type not shown'}, {d.get('category') or 'category not shown'}; filed "
         f"{d.get('filed') or 'unknown'}" + (f", closed {d['closed']}" if d.get("closed") else "")
         + f"; {d.get('doc_count', 0)} docket entries; case page {d['url']}; documents {webdocs_url(d['docket'])}"]
    if full and d.get("facts"):
        f = d["facts"]
        for k, label in [("technology", "Technology"), ("megawatts", "Megawatts"),
                         ("equipment_maker_model", "Equipment"), ("in_service", "In service"),
                         ("retirement", "Retirements"), ("location", "Location"), ("coords", "Coordinates")]:
            if f.get(k):
                L.append(f"  - {label}: " + " | ".join(f[k][:4]))
    for doc in d.get("documents", []):
        if doc.get("saved"):
            L.append(f"  - read {doc['file']} (entry {doc['docket_entry']}, {doc['title'][:100]}, {doc['size']}, "
                     f"{doc['date']}): {doc['url']}")
        else:
            L.append(f"  - not read: {doc['file']} ({doc['title'][:100]}, {doc['size']}): {doc['url']}")
    return L


def write_outputs(out_dir, plants, dockets, by_plant, matched, sources, today, from_year, siting_lines=()):
    out_dir.mkdir(parents=True, exist_ok=True)
    slim = [{k: v for k, v in d.items() if k not in ("text_blob", "entries")} for d in dockets]
    unmatched = [d for d in dockets if d.get("key") and d["docket"] not in matched]
    data = {"generated": today, "from_year": from_year, "sources": sources, "dockets": slim,
            "by_plant": by_plant, "unmatched_generation": [d["docket"] for d in unmatched],
            "siting_spreadsheet_lines": list(siting_lines)}
    (out_dir / "psc_dockets.json").write_text(json.dumps(data, indent=1, default=str))
    by_id = {d["docket"]: d for d in dockets}
    L = [f"# North Dakota Public Service Commission cases on generation ({today})", "",
         f"Cases filed {from_year} or later, plus the hand-checked list. The case page and each document in the "
         "case's documents folder are stable public links and can be cited. Copies of documents read are in "
         "scopes/us-nd/work/psc/ and are not committed.", "", "## Sources", ""]
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
    L += ["## Generation cases that match no GEM plant (possible new plants, uprates or retirements)", ""]
    for d in sorted(unmatched, key=lambda x: x["docket"]):
        L += docket_block(d)
    L += ["", "## Other generation-related cases (wind, solar, lines; not read)", ""]
    for d in sorted((d for d in dockets if d.get("relevant") and not d.get("key")), key=lambda x: x["docket"]):
        L += docket_block(d, full=False)
    if siting_lines:
        L += ["", "## Lines of the Commission's siting spreadsheet that name gas or a GEM plant", ""]
        L += [f"- {s}" for s in siting_lines]
    (out_dir / "psc_dockets.md").write_text("\n".join(L) + "\n")
    return unmatched


def siting_lines(text, plants):
    pats = [p for pl in plants for p in PSC_KNOWN.get(pl["id"], [])]
    out = []
    for ln in (text or "").splitlines():
        s = clean_ws(ln)
        if 6 < len(s) < 300 and (re.search(r"\bgas\b|turbine|peak|generating station|data cent", s, re.I)
                                 or any(re.search(p, s, re.I) for p in pats)) and s not in out:
            out.append(s)
    return out[:80]


def main():
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    ap.add_argument("--from-date", default="2022-01-01", help="filing date search starts here (yyyy-mm-dd)")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--plants", help="comma-separated GEM location IDs")
    ap.add_argument("--docs-per-docket", type=int, default=8)
    ap.add_argument("--max-mb", type=float, default=120, help="skip documents larger than this")
    ap.add_argument("--no-docs", action="store_true", help="list cases, download nothing")
    ap.add_argument("--match-only", metavar="JSON", help="re-match a saved psc_dockets.json, no network")
    a = ap.parse_args()
    plants = load_plants(argparse.Namespace(plants=a.plants))
    today = dt.date.today().isoformat()
    from_year = int(a.from_date[:4])
    if a.match_only:
        saved = json.loads(Path(a.match_only).read_text())
        dockets = saved["dockets"]
        for d in dockets:
            d["text_blob"] = " ".join(x for doc in d.get("documents", []) for v in (doc.get("facts") or {}).values() for x in v)
        by_plant, matched = match_all(plants, dockets)
        write_outputs(Path(a.out), plants, dockets, by_plant, matched, saved["sources"], today,
                      saved.get("from_year", from_year), saved.get("siting_spreadsheet_lines", []))
        return

    psc = Psc()
    found = {}
    start = dt.date.fromisoformat(a.from_date)
    for r in psc.by_dates(start, dt.date.today()):
        found.setdefault(r["docket"], r)
    log(f"filing date search from {start}: {len(found)} cases")
    for name in ENTITIES:
        text = psc.search(entityName=name)
        rows = parse_results(text) if text else []
        shown, total = result_count(text or "")
        if total > shown:
            text = psc.search(entityName=name, filedFromDate="2010-01-01")
            rows = parse_results(text) if text else rows
        log(f"entity {name!r}: {len(rows)} cases" + (f" ({shown} of {total} shown)" if total > shown else ""))
        for r in rows:
            found.setdefault(r["docket"], r)
    for word in DESCRIPTIONS:
        text = psc.search(description=word, jurisdictionId="PU")
        rows = parse_results(text) if text else []
        log(f"description {word!r}: {len(rows)} cases")
        for r in rows:
            found.setdefault(r["docket"], r)
    for case in KNOWN_CASES:
        found.setdefault(case, {"docket": case, "url": case_url(case), "title": "", "type": "", "category": "",
                                "entities": [], "doc_count": 0, "filed": "", "closed": ""})

    dockets = []
    for d in found.values():
        d["relevant"], d["key"], d["reasons"] = classify(d)
        if not d["key"] and any(match_docket(p, {**d, "text_blob": ""}) for p in plants) and not WIRES.search(d["title"]):
            d["relevant"] = d["key"] = True
            d["reasons"].append("its description names a GEM plant")
        if d["relevant"]:
            dockets.append(d)
    log(f"{len(found)} cases; {len(dockets)} generation related; {sum(1 for d in dockets if d['key'])} key")

    for d in dockets:
        d["documents"], d["facts"], d["text_blob"] = [], {}, ""
        if not d["key"]:
            continue
        det = psc.case(d["docket"])
        if det is None:
            d["reasons"].append("case page did not load")
            continue
        d.update({k: det[k] or d.get(k, "") for k in ("filed", "closed", "title", "type", "category")})
        d["entities"] = det["entities"] or d.get("entities", [])
        d["entries"] = det["entries"]
        d["doc_count"] = len(det["entries"]) or d.get("doc_count", 0)
        d["relevant"], d["key"], reasons = classify(d)
        d["key"] = True
        d["reasons"] = sorted(set(d["reasons"] + reasons))
        if a.no_docs:
            continue
        log(f"reading {d['docket']}: {d['title'][:90]}")
        d["documents"], d["facts"], d["folder_state"] = read_case(psc, d, a.docs_per_docket, int(a.max_mb * 1e6))
        folder = WORK / d["docket"]
        d["text_blob"] = " ".join(p.read_text(errors="replace") for p in sorted(folder.glob("*.txt"))) if folder.exists() else ""
    for d in dockets:
        d["utility"] = "; ".join(d.get("entities", []))

    lines, pdfs = [], []
    page = get(SITING_PAGE)
    pdfs = siting_pdfs(page.text) if page.status == "200" else []
    for url in [u for u in pdfs if re.search(r"spreadsheet", u, re.I)] or SITING_PDFS:
        p = get(url, timeout=300)
        if p.status == "200":
            lines += siting_lines(p.text, plants)
    sources = [
        {"name": "North Dakota PSC case search", "url": SEARCH,
         "how": f"form search by filing date from {a.from_date} (split into windows until complete), by "
                f"{len(ENTITIES)} entity names and {len(DESCRIPTIONS)} description words, plus {len(KNOWN_CASES)} "
                f"hand-checked cases; {len(found)} cases, {len(dockets)} generation related"
                + (f"; searches that got no full answer: {'; '.join(psc.failed)}" if psc.failed else "")},
        {"name": "North Dakota PSC case documents folders", "url": "https://www.psc.nd.gov/webdocs/case/",
         "how": "key documents of each gas or generation case downloaded and read"},
        {"name": "North Dakota PSC siting page", "url": SITING_PAGE,
         "how": f"siting spreadsheet read, {len(lines)} lines kept" + ("" if page.status == "200" else f" (page HTTP {page.status})")}]
    by_plant, matched = match_all(plants, dockets)
    unmatched = write_outputs(Path(a.out), plants, dockets, by_plant, matched, sources, today, from_year, lines)
    log(f"{len(matched)} cases matched to plants; {len(unmatched)} key cases unmatched")
    for p in plants:
        log(f"  {p['name']}: {len(by_plant[p['id']])}")


if __name__ == "__main__":
    main()

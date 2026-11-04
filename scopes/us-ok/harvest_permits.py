"""
Harvest Oklahoma air permits before a research sweep.

The Oklahoma Department of Environmental Quality (ODEQ) publishes permits in two
places. Both answer without a login. What was found (2026-11-03 and 2026-11-04):

  1. The Permits for Public Review table,
     https://applications.deq.ok.gov/PermitsPublicReview/. One anonymous GET
     returns the whole server-rendered table (about 290 rows, about 175 of them
     air quality), no paging. Its certificate fails verification, so it is read
     with verification off. Columns: Division, County, Company, Facility (a link
     to permitinformation.aspx?id=<object id>), Permit #, Tier, Type, Step (the
     comment dates sit in a span, "(04/25/2026 - 07/24/2026)"), Staff Name,
     Status. Staff names are not kept. Rows leave the table once a permit is
     final, so a dated copy is kept under ppr/ on every run.
  2. The OnBase Public Access store,
     https://okdeqonbaseexternal.databankcloud.com/pav/api. It holds the permit
     documents from April 2016 on (applications, draft permits, memoranda,
     notices). Every call needs a browser User-Agent, else 403.
       POST /CustomQuery/KeywordSearch with
         {"QueryID":262,"Keywords":[{"ID":"828","Value":"*HORSESHOE*"}],"QueryLimit":0}
       Keyword ids: 844 the table's object id, 830 permit number, 828 facility,
       827 company, 312 county, 829 division. Leading and trailing wildcards work.
       A date-only search sends "Keywords":[] with "FromDate" and "ToDate"
       (yyyy-mm-dd); 2016 to 2026 returned 1,502 documents, none cut off.
       Each result has an opaque ID (new on every search, but an old one still
       downloads a day later), a Name such as "6293248 - DEQ Permits Public
       Application - 5/1/2026" (the leading number is ODEQ's document number,
       the stable key here) and the document type and date received. Results
       never name the facility, so a document is tied to a facility by the
       search that found it.
       GET /Document/<quoted ID>/?ViewerMode=PDF&ForceDownload=true returns the
       PDF. That address is what a note cites; fetch.py and url_verifier.py read it.
     Full-text search is not licensed (403). Documents before April 2016 are not
     online: a plant with no document at all is recorded as needing an open
     records request (ODEQ Central Records form), never retried as a give-up.

Steps:
  1. Read the table, keep every row (water and land rows name data centers),
     save the dated copy.
  2. Match rows to GEM Oklahoma plants (KNOWN holds hand-checked patterns; a
     plant missing there is matched by its name words, marked for checking).
  3. For every row: OnBase search by object id (844) and by permit number base
     (830), so each document is tied to its table row.
  4. For every GEM plant: OnBase facility searches (828) with its PLANT_TERMS.
     For every owner and power word: company (827) and facility (828) searches.
     A document found only by a broad power word is read (first pages) to learn
     its facility.
  5. A date-only sweep in yearly slices from 2016 lists every document; the ones
     no search tied to a facility are listed, and the newest applications and
     draft permits among them are read (first pages) up to --sweep-read, kept
     when the text looks like a power plant or data center.
  6. Download the documents of every matched or power-like facility into
     work/permits/docs/<permit>/, extract text with pdftotext (fetch.py's OCR
     when a scan has no text layer) and keep the lines that give the permit
     number, project, equipment, maker, sizes and location.

Output, in scopes/us-ok/work/permits/ (what the sweep agents read): one plain-text
index per plant (<GEM location id>.md), _unmatched.md, _sweep.md, index.json,
harvest_log.jsonl and ppr/<date>.json. A summary and facilities.json (the file
data_center_fleets.py reads) go to batches/<scope>/harvest/. Permit PDFs name
agency and company staff: the PDFs and their text stay under work/ (never
committed). Nothing here stages a record.

Usage (from the repo root):
    python scopes/us-ok/harvest_permits.py --scope us-ok                  # everything
    python scopes/us-ok/harvest_permits.py --scope us-ok --plants L100000402162
    python scopes/us-ok/harvest_permits.py --scope us-ok --match-only     # table matches only, no OnBase
    python scopes/us-ok/harvest_permits.py --scope us-ok --no-sweep       # skip the date sweep
"""
import argparse
import html
import json
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

import pandas as pd
import requests
import urllib3

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from fetch import CHROME_UA  # noqa: E402
from harvest_lib import CSV, REPO, SIZE, clean, get, harvest_out, norm_county, pick, report_failure  # noqa: E402

PPR = "https://applications.deq.ok.gov/PermitsPublicReview/"
PPR_ROW = PPR + "permitinformation.aspx?id={oid}"
API = "https://okdeqonbaseexternal.databankcloud.com/pav/api"
SEARCH = f"{API}/CustomQuery/KeywordSearch"
DOC = API + "/Document/{qid}/?ViewerMode=PDF&ForceDownload=true"
QUERY_ID = 262
RECORDS_FORM = "https://oklahoma.gov/deq/about/asd/records/central-records-request-form.html"
K_OBJECT, K_PERMIT, K_FACILITY, K_COMPANY, K_COUNTY, K_DIVISION = "844", "830", "828", "827", "312", "829"
FIRST_YEAR = 2016

# Hand-checked patterns (2026-11-04, against the table of 2026-11-03): GEM plant -> regexes that
# must hit fac_text() (company | facility | county, lower case). A plant missing here is matched
# by its name words, marked for checking. "mustang" alone is a gas gatherer (Mustang Gas
# Products), "tinker" alone a pipeline booster station, "spring creek" a compressor station.
KNOWN = {
    "L100000104122": [r"grand river energy center", r"grand river dam.*(energy|power|generat|chouteau)"],
    "L100000104123": [r"western farmers.*hugo", r"hugo (power|generat|station|plant)"],
    "L100000104124": [r"muskogee generating"],
    "L100000104126": [r"northeastern (power )?station", r"pso northeastern"],
    "L100000401594": [r"mcclain (generat|energy|power|station)"],
    "L100000401595": [r"redbud"],
    "L100000401619": [r"kiamichi", r"kiowa power"],
    "L100000401723": [r"associated electric.*chouteau", r"chouteau (power|generat|energy)"],
    "L100000401932": [r"spring creek (energy|power|generat)"],
    "L100000401991": [r"green country (power|energy|generat)"],
    "L100000402162": [r"horseshoe lake"],
    "L100000402164": [r"mustang (power|generat|energy)", r"(og&e|og and e|oklahoma gas).*mustang"],
    "L100000402165": [r"(og&e|og and e|oklahoma gas).*seminole", r"seminole (power|generat)"],
    "L100000402166": [r"lamb energy", r"charles d\.? lamb"],
    "L100000402167": [r"ponca city (power|generat|municipal|energy)", r"municipal power.*ponca"],
    "L100000402175": [r"oneta"],
    "L100000402231": [r"comanche (power|generat)"],
    "L100000402233": [r"riverside (power|generat)"],
    "L100000402234": [r"southwestern (power|generat)"],
    "L100000402235": [r"tulsa power station", r"public service.*\| tulsa (power|plant)"],
    "L100000402236": [r"weleetka"],
    "L100000402369": [r"western farmers.*anadarko", r"anadarko (power|plant|generat)"],
    "L100000402370": [r"western farmers.*moore?land", r"moore?land (power|generat|station)"],
    "L100000402493": [r"frontier (power|generat|cogen)"],
    "L100000409256": [r"stillwater (energy|utilit|power|electric)", r"ferguson (power|generat|station)"],
    "L100001023579": [r"ripley energy"],
    "L100001063385": [r"tinker turbines", r"(og&e|og and e|oklahoma gas).*tinker"],
    "L100001063386": [r"chickasha (industrial|power|generat)"],
    "L100001080983": [r"cross timbers (power|energy|generat)"],
    "L100001081005": [r"core scientific", r"muskogee data"],
    "L100001089274": [r"bristow (energy|power|generat)"],
    "L100001089312": [r"citadel"],
    "L100001089319": [r"port of inola (power|station)", r"inola power"],
    "L100001089336": [r"thunderbird", r"plainsmen"],
}

# OnBase facility (828) searches per GEM plant. Each finds documents whose facility field carries
# the word; documents found this way are tied to the plant and marked for checking. Words shared
# with unrelated sites (Mustang, Tinker, Comanche, Tulsa, Seminole) get a narrower form.
PLANT_TERMS = {
    "L100000104122": ["*GRAND RIVER ENERGY*", "*GREC*"],
    "L100000104123": ["*HUGO*"],
    "L100000104124": ["*MUSKOGEE GENERATING*", "*MUSKOGEE POWER*"],
    "L100000104126": ["*NORTHEASTERN*"],
    "L100000401594": ["*MCCLAIN*"],
    "L100000401595": ["*REDBUD*"],
    "L100000401619": ["*KIAMICHI*", "*KIOWA POWER*"],
    "L100000401723": ["*CHOUTEAU*"],
    "L100000401932": ["*SPRING CREEK ENERGY*", "*SPRING CREEK POWER*"],
    "L100000401991": ["*GREEN COUNTRY*"],
    "L100000402162": ["*HORSESHOE*"],
    "L100000402164": ["*MUSTANG POWER*", "*MUSTANG GENERAT*", "*MUSTANG ENERGY*"],
    "L100000402165": ["*SEMINOLE POWER*", "*SEMINOLE GENERAT*", "*SEMINOLE STATION*"],
    "L100000402166": ["*LAMB*"],
    "L100000402167": ["*PONCA CITY*"],
    "L100000402175": ["*ONETA*"],
    "L100000402231": ["*COMANCHE POWER*", "*COMANCHE GENERAT*", "*PSO COMANCHE*"],
    "L100000402233": ["*RIVERSIDE POWER*", "*RIVERSIDE GENERAT*", "*PSO-RIVERSIDE*", "*PSO RIVERSIDE*"],
    "L100000402234": ["*SOUTHWESTERN POWER*", "*SOUTHWESTERN GENERAT*", "*PSO SOUTHWESTERN*"],
    "L100000402235": ["*TULSA POWER*", "*PSO TULSA*"],
    "L100000402236": ["*WELEETKA*"],
    "L100000402369": ["*ANADARKO PLANT*", "*ANADARKO POWER*", "*FARMERS ANADARKO*"],
    "L100000402370": ["*MOORELAND*", "*MOORLAND*"],
    "L100000402493": ["*FRONTIER POWER*", "*FRONTIER GENERAT*", "*FRONTIER COGEN*"],
    "L100000409256": ["*STILLWATER ENERGY*", "*STILLWATER UTIL*", "*STILLWATER POWER*"],
    "L100001023579": ["*RIPLEY*"],
    "L100001063385": ["*TINKER TURBINE*", "*TINKER POWER*", "*TINKER GENERAT*"],
    "L100001063386": ["*CHICKASHA INDUSTRIAL*", "*CHICKASHA POWER*"],
    "L100001080983": ["*CROSS TIMBERS*"],
    "L100001081005": ["*CORE SCIENTIFIC*", "*MUSKOGEE DATA*"],
    "L100001082617": [],
    "L100001089274": ["*BRISTOW*"],
    "L100001089312": ["*CITADEL*"],
    "L100001089319": ["*INOLA POWER*", "*PORT OF INOLA*"],
    "L100001089336": ["*THUNDERBIRD*"],
}
# Company (827) searches: the owners and the companies that build power and data centers here.
COMPANY_TERMS = ["OG&E*", "OG AND E*", "OKLAHOMA GAS*", "PUBLIC SERVICE CO*", "PSO*", "*WESTERN FARMERS*",
                 "*GRAND RIVER DAM*", "*ASSOCIATED ELECTRIC*", "*MUNICIPAL POWER*", "*PEOPLES ELECTRIC*",
                 "*KIOWA POWER*", "*TENASKA*", "*ONETA*", "*EVERGY*", "*WESTAR*", "*STILLWATER UTIL*",
                 "*CORE SCIENTIFIC*", "*CITADEL*", "*PLAINSMEN*", "*CROSS TIMBERS*", "*ELECTRIC*", "*POWER*",
                 "*GENERATION*", "*DATA*", "*DIGITAL*", "*COMPUT*", "*MYALL*", "*GOOGLE*"]
# Facility (828) power words. Documents found only this way are read to learn their facility.
POWER_TERMS = ["*POWER*", "*ENERGY CENTER*", "*GENERATING*", "*GENERATION*", "*TURBINE*", "*DATA CENTER*",
               "*DATA STORAGE*", "*DATACENTER*", "*COGEN*", "*ELECTRIC*", "*PEAKING*", "*CAMPUS*"]

POWER_NAME = re.compile(
    r"power|electric|generat|energy center|turbine|cogen|data ?cent|datacent|data storage|compute|"
    r"bitcoin|crypto|hyperscal|peaking|combined cycle|og&e|og and e|oklahoma gas|public service co|"
    r"western farmers|grand river dam|associated electric|municipal power|peoples electric|kiowa power|"
    r"tenaska|oneta|redbud|horseshoe|mustang power|tinker turbine|core scientific|citadel|thunderbird", re.I)
POWER_DROP = re.compile(
    r"compressor|booster|gas plant|gas processing|processing plant|dehy|treating|\bwells?\b|\bpad\b|tank|"
    r"saltwater|disposal|pipeline|breakout|gathering|elevator|grain|feed|ethanol|refinery|landfill|"
    r"asphalt|concrete|ready mix|gravel|sand|quarry|lumber|brick|cement|foundry|steel|fertilizer|"
    r"nitrogen|ammonia|wastewater|water treatment|\bww?tf?\b|\bwtp\b|golf|manufactur|lagoon|terminal|\brng\b|"
    r"halliburton|frac", re.I)
NAME_NOISE = re.compile(
    r"\b(power station|power plant|generating station|generating|generation|facility|station|energy center|"
    r"energy|plant|power|ok|oklahoma|the|municipal|of|and|city|llc|inc|company|co|corp|"
    r"corporation|combined|cycle|county|industrial|park|campus|data|center|pso|og|e)\b", re.I)
EQUIPMENT = re.compile(r"turbine|\bct\b|engine|rice\b|generat|\bgen\b|boiler|duct burner|hrsg|"
                       r"combined cycle|simple cycle|peaking|diesel|reciprocating|genset", re.I)
MAKER = re.compile(r"model\b|caterpillar|cat g|wartsila|w[äa]rtsil[äa]|jenbacher|"
                   r"general electric|\bGE\b|siemens|solar turbines|mitsubishi|cummins|rolls[- ]royce|"
                   r"mtu\b|kohler|generac|waukesha|pratt|ansaldo|baker hughes|"
                   r"hitachi|titan \d|taurus|mars \d|lm ?\d{4}|7ea|7fa|7ha|6b\b|f-?class|h-?class", re.I)
LOCATION = re.compile(
    r"latitude|longitude|\blat\b|\blong\b|\bUTM\b|\bsection \d+|township|\bT\d{1,2}[NS]\b|\bR\d{1,2}[EW]\b|"
    r"located (at|in|on|near|approximately)|physical address|site address|facility address|"
    r"street address|\b\d{2,5} [A-Z0-9][\w. ]+ (road|rd|street|st|avenue|ave|"
    r"highway|hwy|drive|dr|lane|ln|blvd|boulevard)\b|county,? oklahoma|ok 7[34]\d{3}|oklahoma 7[34]\d{3}",
    re.I)
PROJECT = re.compile(r"proposes|propose to|will consist|project (is|will|consists)|construction of|"
                     r"to construct|new (electric|power|generat)|install(ation)? of", re.I)
FACILITY_LINE = re.compile(r"facility( name)?:|company( name)?:|applicant:|\bre:|permit (no|number)|"
                           r"facility id|site name|county,? oklahoma", re.I)
LATLON = re.compile(r"\b(3[3-6]\.\d{3,}|37\.0\d*)\s*[,;/ ]\s*-?\s*(9[4-9]\.\d{3,}|10[0-3]\.\d{3,})\b")
PERMIT_NO = re.compile(r"\b(?:\d{4}-\d{3,4}-[A-Z]{1,5}\d?|(?:TV|MAC|PSD|AR|MIC|O|OK)\d{6,7})\b")
PERMIT_BASE = re.compile(r"\d{4}-\d{3,4}|(?:TV|MAC|PSD|AR|MIC|O|OK)\d{6,7}")
DOC_NAME = re.compile(r"^\s*(\d{5,9})\s*-\s*(.*?)\s*-\s*(\d{1,2}/\d{1,2}/\d{4})\s*$")
READ_TYPES = re.compile(r"application|draft permit|^permit\b|memorand|evaluation|notice", re.I)
SWEEP_TYPES = re.compile(r"application(?! additional)|draft permit|permit application", re.I)


def log(msg):
    print(f"[harvest-ok] {msg}", file=sys.stderr, flush=True)


def words(text):
    t = NAME_NOISE.sub(" ", re.sub(r"\(.*?\)", " ", str(text or "")))
    return {w.lower() for w in re.split(r"[^A-Za-z]+", t) if len(w) >= 4}


def us_date(s):
    """'5/1/2026' or '05/01/2026' to 2026-05-01, or ''."""
    m = re.search(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b", s or "")
    return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}" if m else ""


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s or "").lower()).strip("-")[:60] or "x"


def permit_base(p):
    """'2019-0607-C M-2' -> '2019-0607', 'TV0000530 v6.0' -> 'TV0000530', else ''."""
    m = PERMIT_BASE.search(str(p or ""))
    return m.group(0) if m else ""


# ---------------------------------------------------------------- the table ---

def parse_ppr(text):
    """Rows of the Permits for Public Review table, staff names left out."""
    rows = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", text or "", re.S | re.I):
        cells = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S | re.I)
        if len(cells) < 10:
            continue
        oid = re.search(r"permitinformation\.aspx\?id=(\d+)", cells[3], re.I)
        step = cells[7]
        dates = re.search(r"\((\d{1,2}/\d{1,2}/\d{4})\s*-\s*(\d{1,2}/\d{1,2}/\d{4})\)", clean(step))
        rows.append({
            "division": clean(cells[0]).upper(), "county": norm_county(clean(cells[1])).title(),
            "company": clean(cells[2]), "facility": clean(cells[3]), "object_id": oid.group(1) if oid else "",
            "permit": clean(cells[4]), "tier": clean(cells[5]), "type": clean(cells[6]),
            "step": clean(re.sub(r"<span.*?</span>", " ", step, flags=re.S | re.I)),
            "comment_begins": us_date(dates.group(1)) if dates else "",
            "comment_ends": us_date(dates.group(2)) if dates else "",
            "status": clean(cells[9]),
        })
    return rows


def read_ppr():
    """The live table (certificate check off: the host's chain fails verification)."""
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    for i in range(3):
        try:
            r = requests.get(PPR, headers={"User-Agent": CHROME_UA}, timeout=120, verify=False)
            if r.status_code == 200 and "permitinformation.aspx" in r.text:
                return r.text
            err = f"HTTP {r.status_code}"
        except requests.RequestException as e:
            err = type(e).__name__
        time.sleep(5 * (i + 1))
    report_failure(PPR, err, "permits for public review table")
    return ""


def build_facilities(rows):
    """One facility per company + facility + county; every table row kept on it."""
    facs = {}
    for r in rows:
        key = "ppr-" + slug(f"{r['facility']} {r['county']}")
        f = facs.get(key)
        if f is None:
            f = facs[key] = new_fac(key, r["facility"] or r["company"], "table")
            f["company"], f["county"] = r["company"], r["county"]
        f["rows"].append(r)
        if r["object_id"] and r["object_id"] not in f["object_ids"]:
            f["object_ids"].append(r["object_id"])
        b = permit_base(r["permit"])
        if b and b not in f["permit_bases"]:
            f["permit_bases"].append(b)
        if r["division"] not in f["divisions"]:
            f["divisions"].append(r["division"])
    return facs


def new_fac(key, name, source):
    return {"key": key, "name": name, "source": source, "company": "", "county": "", "rows": [],
            "object_ids": [], "permit_bases": [], "divisions": [], "found_by": [], "docs": [], "hint": ""}


def fac_text(f):
    return " | ".join(x for x in (f["company"], f["name"], f["county"], f.get("hint", "")) if x).lower()


def is_power(f):
    """A facility looks like a power or data center site: a power-like name or company that is
    not on the drop list (a compressor station of an electric company is dropped)."""
    if POWER_DROP.search(f["name"]):
        return False
    return bool(POWER_NAME.search(f"{f['company']} {f['name']} {f.get('hint', '')}"))


def match(plant, facs):
    """[(facility, how)]: hand-checked patterns, else every distinctive word of the plant's name,
    else its county plus a power-like name of the plant's owner."""
    out = []
    pats = KNOWN.get(plant["id"])
    for f in facs:
        t = fac_text(f)
        if pats and any(re.search(p, t) for p in pats):
            how = "checked by hand" if f["source"] == "table" else f"found by an ODEQ document search ({', '.join(f['found_by'])}), check it is this plant"
            out.append((f, how))
    if pats:
        return out
    ws = plant["name_words"]
    for f in facs:
        t = fac_text(f)
        if ws and ws <= words(t):
            out.append((f, "name match, check it is this plant"))
    return out


# ---------------------------------------------------------------- OnBase ---

class OnBase:
    """The ODEQ OnBase public access API: keyword and date searches, PDF downloads. Paced at
    about two calls a second; three tries per call; failures go to fetch.py's give-up log."""

    def __init__(self, pause=0.5):
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": CHROME_UA, "Accept": "application/json, application/pdf, */*"})
        self.pause = pause
        self.errors = []
        self.calls = 0

    def _post(self, body, what):
        for i in range(3):
            time.sleep(self.pause)
            self.calls += 1
            try:
                r = self.s.post(SEARCH, json=body, timeout=120)
                if r.status_code == 200:
                    return r.json().get("Data") or []
                err = f"HTTP {r.status_code}"
            except (requests.RequestException, ValueError) as e:
                err = type(e).__name__
            time.sleep(4 * (i + 1))
        self.errors.append(f"{what}: {err}")
        report_failure(SEARCH + "#" + urllib.parse.quote(what), err, "odeq onbase search")
        return None

    def search(self, kws):
        """kws: [(keyword id, value)]. Documents, or None when the call failed."""
        body = {"QueryID": QUERY_ID, "Keywords": [{"ID": k, "Value": v} for k, v in kws], "QueryLimit": 0}
        got = self._post(body, " ".join(f"{k}={v}" for k, v in kws))
        return None if got is None else [parse_doc(d) for d in got]

    def dates(self, start, end):
        body = {"QueryID": QUERY_ID, "Keywords": [], "QueryLimit": 0, "FromDate": start, "ToDate": end}
        got = self._post(body, f"dates {start} to {end}")
        return None if got is None else [parse_doc(d) for d in got]

    def download(self, doc, path):
        """Save the PDF at path. Returns a state string."""
        for i in range(3):
            time.sleep(self.pause)
            self.calls += 1
            try:
                r = self.s.get(doc["url"], timeout=300)
                if r.status_code == 200 and r.content[:5] == b"%PDF-":
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(r.content)
                    return "saved"
                err = f"HTTP {r.status_code}" + ("" if r.status_code != 200 else ", not a PDF")
            except requests.RequestException as e:
                err = type(e).__name__
            time.sleep(4 * (i + 1))
        report_failure(doc["url"], err, "odeq onbase document")
        return f"not saved, {err}"


def parse_doc(d):
    """One search result as {number, title, type, date, url, key}. The number is ODEQ's document
    number (leading part of the Name); the opaque ID changes on every search."""
    name = d.get("Name", "")
    m = DOC_NAME.match(name)
    vals = [c.get("Value") or "" for c in d.get("DisplayColumnValues") or []]
    number = m.group(1) if m else ""
    title = m.group(2) if m else name
    date = us_date(vals[1]) if len(vals) > 1 and vals[1] else (us_date(m.group(3)) if m else "")
    dtype = vals[0] if vals and vals[0] else re.sub(r"^DEQ Permits Public\s*", "", title)
    permits = sorted(set(PERMIT_NO.findall(title)))
    return {"number": number, "title": title, "type": dtype, "date": date, "name_permits": permits,
            "url": DOC.format(qid=urllib.parse.quote(d.get("ID", ""), safe="")),
            "key": f"{number}|{dtype}|{date}" if number else name}


def add_docs(f, docs, how):
    seen = {d["key"] for d in f["docs"]}
    for d in docs or []:
        if d["key"] not in seen:
            seen.add(d["key"])
            f["docs"].append({**d, "how": how})
    if how not in f["found_by"]:
        f["found_by"].append(how)


def doc_path(out_dir, f, d):
    base = permit_base(d["name_permits"][0]) if d.get("name_permits") else ""
    folder = slug(base or (f["permit_bases"][0] if f["permit_bases"] else "no-permit-number"))
    return out_dir / "docs" / folder / f"{d['date'] or 'nodate'}_{slug(d['type'])}_{d['number'] or 'x'}.pdf"


def pdf_text(path, pages=None):
    cmd = ["pdftotext", "-layout"] + (["-l", str(pages)] if pages else []) + [str(path), "-"]
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=300).stdout
    except (subprocess.SubprocessError, OSError):
        return ""


def read_doc(ob, out_dir, f, d, pages=None, ocr=True):
    """Download one document (kept on disk, reused next run), extract its text and keep facts."""
    path = doc_path(out_dir, f, d)
    state = "saved (from an earlier run)" if path.exists() else ob.download(d, path)
    d["file"] = str(path.relative_to(REPO)) if path.exists() else ""
    text = pdf_text(path, pages) if path.exists() else ""
    if path.exists() and len(text.strip()) < 200 and ocr:
        page = get(d["url"], timeout=600)
        if page.status == "200" and page.text.strip():
            text, state = page.text, state + ", text read by OCR"
    if path.exists():
        path.with_suffix(".txt").write_text(text, encoding="utf-8")
    d["state"] = state if text.strip() or not path.exists() else state + ", no text layer"
    d["facts"] = doc_facts(text) if text.strip() else {}
    return text


def doc_facts(text):
    latlon = [f"{a}, -{b.lstrip('-')}" for a, b in LATLON.findall(text)][:3]
    return {
        "ids": sorted({re.sub(r"\s+", "", x).upper() for x in PERMIT_NO.findall(text)})[:6],
        "facility": pick(text, FACILITY_LINE, 6),
        "project": pick(text, PROJECT, 6),
        "equipment": pick(text, EQUIPMENT, 10),
        "makers": pick(text, MAKER, 8),
        "sizes": pick(text, SIZE, 10),
        "location": pick(text, LOCATION, 8),
        "coords": latlon,
    }


def rank_docs(docs):
    """Newest first, applications, draft permits and memoranda before letters and proofs."""
    return sorted(docs, key=lambda d: (not READ_TYPES.search(d["type"]), "".join(chr(255 - ord(c)) for c in d["date"])))


def hint_of(text):
    """The lines of a document's first pages that name its facility and company."""
    return " ".join(pick(text, FACILITY_LINE, 4))[:400]


# ---------------------------------------------------------------- reporting ---

def fac_block(f, how=None):
    L = [f"- {f['name']} ({f['company'] or 'company not shown'}"
         + (f", {f['county']} County" if f["county"] else "") + f"; {f['source']})"]
    if f.get("hint"):
        L.append(f"    - the document text names: {f['hint']}")
    for oid in f["object_ids"]:
        L.append(f"    - table entry: {PPR_ROW.format(oid=oid)}")
    for r in f["rows"]:
        L.append(f"    - permit in review: {r['permit']}, {r['type']} ({r['division']}, {r['tier']}), step {r['step']}"
                 + (f", comments {r['comment_begins']} to {r['comment_ends']}" if r["comment_ends"] else "")
                 + f", {r['status']}")
    if f["found_by"]:
        L.append(f"    - ODEQ document searches that found it: {'; '.join(f['found_by'])}")
    for d in f["docs"]:
        L.append(f"    - document ({d.get('state', 'not read')}, {d['date'] or 'date not shown'}): {d['number']} {d['type']}"
                 + (f" ({', '.join(d['name_permits'])})" if d["name_permits"] else "") + f": {d['url']}")
        fa = d.get("facts") or {}
        for key, label in (("ids", "permit numbers"), ("facility", "facility"), ("project", "project"),
                           ("equipment", "equipment"), ("makers", "maker or model"), ("sizes", "size"),
                           ("location", "site address or location"), ("coords", "coordinates")):
            for line in fa.get(key, []):
                L.append(f"        - {label}: {line}")
    if how:
        L.insert(0, f"Matched: {how}.")
    return L


def write_index(path, plant, matched, no_docs=False):
    L = [f"# Oklahoma air permit files for {plant['name']} ({plant['id']})", "",
         "Source: the ODEQ Permits for Public Review table (" + PPR + ") and the ODEQ OnBase public document "
         "store. A document address (pav/api/Document/...) is citable as it stands; fetch.py and url_verifier.py "
         "read it. The PDFs and their text are saved under work/permits/docs/.", "",
         f"Harvested: {time.strftime('%Y-%m-%d %H:%M %Z')}", "",
         f"GEM statuses: {', '.join(plant['statuses'])}. City in GEM: {plant['city'] or 'blank'}. "
         f"County in GEM: {plant['county'] or 'blank'}.", ""]
    if no_docs:
        L += ["No ODEQ permit document for this plant is online. The OnBase store starts in April 2016 and no "
              "search found this plant's documents. An open records request to ODEQ Central Records is needed "
              f"for its permits ({RECORDS_FORM}). Do not retry the store.", ""]
    elif not matched:
        L += ["No permit facility matched this plant by name. That does not mean it has no permits: it may be "
              "filed under the owner, a contractor or another site name. Check _unmatched.md and _sweep.md in "
              "this folder.", ""]
    for f, how in matched:
        L += fac_block(f, how) + [""]
    path.write_text("\n".join(L), encoding="utf-8")


def slim(f):
    """A facility as facilities.json and index.json keep it: no full document text."""
    return {"key": f["key"], "name": f["name"], "source": f["source"], "company": f["company"],
            "county": f["county"], "city": "", "address": "", "codes": [], "hint": f.get("hint", ""),
            "object_ids": f["object_ids"], "found_by": f["found_by"],
            "permits": [{"number": r["permit"], "type": r["type"], "status": r["status"], "step": r["step"],
                         "comment_ends": r["comment_ends"]} for r in f["rows"]],
            "docs": [{k: d[k] for k in ("number", "name", "type", "date", "url", "state", "file", "facts", "how")
                      if k in d} | {"name": f"{d['number']} {d['type']}"} for d in f["docs"]]}


# ----------------------------------------------------------------- plants ---

def load_plants(args=None, csv_path=None):
    csv = pd.read_csv(csv_path or CSV, low_memory=False, encoding="utf-8-sig")
    csv = csv[csv["State/Province"] == "Oklahoma"]
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


def main():
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n\n")[0])
    ap.add_argument("--scope", required=True, help="batch folder name, e.g. us-ok")
    ap.add_argument("--plants", help="comma-separated GEM location IDs (default: every plant)")
    ap.add_argument("--match-only", action="store_true", help="table matches only, no OnBase calls")
    ap.add_argument("--no-sweep", action="store_true", help="skip the date sweep")
    ap.add_argument("--docs-per-facility", type=int, default=15)
    ap.add_argument("--sweep-read", type=int, default=150,
                    help="read the first pages of this many untied applications and draft permits")
    ap.add_argument("--pages", type=int, default=3, help="pages read from a document read only for its facility")
    args = ap.parse_args()

    out_dir = harvest_out(args.scope)
    hv_dir = REPO / "batches" / args.scope / "harvest"
    hv_dir.mkdir(parents=True, exist_ok=True)
    plants = load_plants(args)
    stamp = time.strftime("%Y-%m-%d")

    text = read_ppr()
    rows = parse_ppr(text)
    (out_dir / "ppr").mkdir(exist_ok=True)
    (out_dir / "ppr" / f"{stamp}.json").write_text(json.dumps({"read": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                                                               "url": PPR, "rows": rows}, indent=1), encoding="utf-8")
    log(f"table: {len(rows)} rows, {sum(r['division'] == 'AQD' for r in rows)} air quality")
    facs = build_facilities(rows)

    if args.match_only:
        for p in plants:
            for f, how in match(p, list(facs.values())) or [(new_fac("", "no match", ""), "")]:
                print(f"{p['id']}\t{p['name']}\t{f['name']}\t{f['key']}\t{how}")
        for f in facs.values():
            if is_power(f) and not any(f in [x for x, _ in match(p, [f])] for p in plants):
                print(f"UNMATCHED\t\t{f['name']}\t{f['key']}\t{f['company']}\t{f['county']}")
        return

    ob = OnBase()
    # 3. every table row's documents, by object id and permit number base
    for k, f in enumerate(facs.values(), 1):
        for oid in f["object_ids"]:
            add_docs(f, ob.search([(K_OBJECT, oid)]), f"object id {oid}")
        for b in f["permit_bases"]:
            add_docs(f, ob.search([(K_PERMIT, b + "*")]), f"permit {b}")
        if k % 25 == 0:
            log(f"  table facilities {k}/{len(facs)}, {ob.calls} calls")
    tied = {d["key"] for f in facs.values() for d in f["docs"]}

    # 4. per-plant facility searches, then owner and power words
    plant_ids = {p["id"] for p in plants}
    for pid, terms in PLANT_TERMS.items():
        if pid not in plant_ids:
            continue
        for term in terms:
            got = [d for d in ob.search([(K_FACILITY, term)]) or [] if d["key"] not in tied]
            if got:
                f = facs.setdefault(f"term-{pid}", new_fac(f"term-{pid}", next(p["name"] for p in plants if p["id"] == pid), "document search"))
                add_docs(f, got, f"facility {term}")
                tied |= {d["key"] for d in got}
    loose = {}
    for k_id, terms in ((K_COMPANY, COMPANY_TERMS), (K_FACILITY, POWER_TERMS)):
        for term in terms:
            got = ob.search([(k_id, term)])
            log(f"OnBase {'company' if k_id == K_COMPANY else 'facility'} {term!r}: {'no answer' if got is None else len(got)} documents")
            for d in got or []:
                if d["key"] not in tied:
                    loose.setdefault(d["key"], {**d, "how": f"{'company' if k_id == K_COMPANY else 'facility'} {term}"})
    log(f"{len(loose)} documents found by an owner or power word with no facility yet")

    # 5. the date sweep
    sweep, sweep_state = {}, []
    if not args.no_sweep:
        for year in range(FIRST_YEAR, int(stamp[:4]) + 1):
            got = ob.dates(f"{year}-01-01", f"{year}-12-31")
            sweep_state.append(f"{year}: {'no answer' if got is None else len(got)}")
            for d in got or []:
                sweep.setdefault(d["key"], d)
        log("sweep: " + ", ".join(sweep_state))
    untied = {k: d for k, d in sweep.items() if k not in tied and k not in loose}

    # read the loose documents (first pages) to learn their facility; then the newest untied
    # applications and draft permits from the sweep, up to --sweep-read
    to_read = list(loose.values())
    to_read += sorted((d for d in untied.values() if SWEEP_TYPES.search(d["type"])),
                      key=lambda d: d["date"], reverse=True)[:args.sweep_read]
    for n, d in enumerate(to_read, 1):
        shell = new_fac("doc-" + d["number"], f"document {d['number']}", "document search" if d["key"] in loose else "date sweep")
        txt = read_doc(ob, out_dir, shell, d, pages=args.pages, ocr=False)
        d["hint"] = hint_of(txt)
        d["power"] = bool(POWER_NAME.search(txt[:6000])) and not POWER_DROP.search(d["hint"])
        if n % 25 == 0:
            log(f"  read {n}/{len(to_read)} documents for their facility")
    for d in to_read:
        if not d.get("power"):
            continue
        shell = new_fac("doc-" + d["number"], d["hint"][:80] or f"document {d['number']}", "document search" if d["key"] in loose else "date sweep")
        shell["hint"] = d["hint"]
        shell["permit_bases"] = d["name_permits"][:1]
        add_docs(shell, [d], d.get("how", "date sweep"))
        facs[shell["key"]] = shell
        tied.add(d["key"])

    # 2 and 6. match, then read every matched or power-like facility's documents
    matches = {p["id"]: match(p, list(facs.values())) for p in plants}
    for pid, terms_fac in ((pid, facs.get(f"term-{pid}")) for pid in plant_ids):
        if terms_fac and terms_fac not in [f for f, _ in matches[pid]]:
            matches[pid].append((terms_fac, f"found by an ODEQ document search ({', '.join(terms_fac['found_by'])}), check it is this plant"))
    matched_keys = {f["key"] for ms in matches.values() for f, _ in ms}
    power = [f for f in facs.values() if f["key"] in matched_keys or is_power(f)]
    unmatched = [f for f in power if f["key"] not in matched_keys]
    log(f"{len(facs)} facilities: {len(power)} power-like, {len(matched_keys)} matched, {len(unmatched)} unmatched")
    for k, f in enumerate(power, 1):
        f["docs"] = rank_docs(f["docs"])
        for n, d in enumerate(f["docs"]):
            if n >= args.docs_per_facility:
                d["state"] = "not read (cap)"
            elif "facts" not in d or d.get("state", "").endswith("no text layer") or f["source"] != "table":
                read_doc(ob, out_dir, f, d)
        log(f"({k}/{len(power)}) {f['name']}: {min(len(f['docs']), args.docs_per_facility)} of {len(f['docs'])} documents read")

    no_docs = {p["id"] for p in plants if not any(f["docs"] for f, _ in matches[p["id"]])}
    with (out_dir / "harvest_log.jsonl").open("a", encoding="utf-8") as logf:
        for p in plants:
            write_index(out_dir / f"{p['id']}.md", p, matches[p["id"]], p["id"] in no_docs)
            logf.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "plant": p["id"], "name": p["name"],
                                   "facilities": [{"name": f["name"], "key": f["key"], "how": how,
                                                   "docs": {f"{d['number']} {d['type']}": d.get("state", "not read") for d in f["docs"]}}
                                                  for f, how in matches[p["id"]]]}) + "\n")

    L = ["# Oklahoma facilities that look like power or data center sites but match no GEM plant in this batch", "",
         "Each may be a plant outside this batch, a plant GEM lacks, a backup generator fleet at a data center "
         "or another site, or not a power plant at all. Check engines or turbines of 50 MW or more in total "
         "(generating capacity only). Entries named \"document <number>\" came from a document search or the "
         "date sweep; the facility lines are what the document's first pages say.", ""]
    for f in sorted(unmatched, key=lambda f: f["name"].lower()):
        L += fac_block(f) + [""]
    if not unmatched:
        L.append("None this run.")
    (out_dir / "_unmatched.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    rest = [d for k, d in untied.items() if k not in tied]
    by_type = {}
    for d in rest:
        by_type[d["type"]] = by_type.get(d["type"], 0) + 1
    L = [f"# ODEQ documents with no facility tie ({len(rest)} of {len(sweep)} in the date sweep)", "",
         "The OnBase store does not say which facility a document belongs to. These documents were found only "
         "by the date sweep. The newest applications and draft permits were read (first pages) and moved to "
         "_unmatched.md when they looked like a power plant or data center. The rest are listed so nothing is "
         "missed: open any whose date or type fits a lead.", "",
         "Sweep by year: " + ", ".join(sweep_state) + ".", "",
         "By type: " + ", ".join(f"{t} {n}" for t, n in sorted(by_type.items(), key=lambda x: -x[1])) + ".", ""]
    for d in sorted(rest, key=lambda d: d["date"], reverse=True):
        L.append(f"- {d['date'] or 'date not shown'}, {d['number']} {d['type']}"
                 + (f" ({', '.join(d['name_permits'])})" if d["name_permits"] else "")
                 + (f", read: {d['hint'][:160]}" if d.get("hint") else "") + f": {d['url']}")
    (out_dir / "_sweep.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    index = {"harvested": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "table_rows": len(rows),
             "plants": {p["id"]: {"name": p["name"], "facilities": [{"key": f["key"], "name": f["name"], "how": how}
                                                                    for f, how in matches[p["id"]]]} for p in plants},
             "no_documents_online": {pid: {"name": next(p["name"] for p in plants if p["id"] == pid),
                                           "records_request": RECORDS_FORM} for pid in sorted(no_docs)},
             "unmatched": [f["key"] for f in unmatched],
             "facilities": {f["key"]: slim(f) for f in power},
             "onbase_errors": ob.errors}
    (out_dir / "index.json").write_text(json.dumps(index, indent=1), encoding="utf-8")
    (hv_dir / "facilities.json").write_text(json.dumps({
        "harvested": index["harvested"], "matches": index["plants"],
        "unmatched": [slim(f) for f in unmatched],
        "matched": [slim(f) for f in power if f["key"] in matched_keys]}, indent=1), encoding="utf-8")

    S = [f"# Oklahoma air permit harvest, {stamp}", "",
         f"Table rows: {len(rows)} ({sum(r['division'] == 'AQD' for r in rows)} air quality). Facilities: {len(facs)}. "
         f"Power-like: {len(power)}. Matched to GEM plants: {len(matched_keys)}. Unmatched: {len(unmatched)}.", "",
         f"OnBase calls: {ob.calls}. Date sweep: {len(sweep)} documents ({', '.join(sweep_state) or 'skipped'}). "
         f"Documents with no facility tie: {len(rest)}.", ""]
    if ob.errors:
        S += ["OnBase calls that failed after three tries (retry before concluding anything):", ""]
        S += [f"- {e}" for e in ob.errors[:40]] + [""]
    if no_docs:
        S += ["Plants with no ODEQ document online (open records request needed): "
              + ", ".join(next(p["name"] for p in plants if p["id"] == pid) for pid in sorted(no_docs)) + ".", ""]
    S += ["## Matches per GEM plant", ""]
    for p in plants:
        ms = matches[p["id"]]
        S.append(f"- {p['name']} ({p['id']}): " + ("; ".join(f"{f['name']} ({f['key']}, {how})" for f, how in ms)
                                                   if ms else "no facility matched"))
    S += ["", "## Unmatched power-like facilities", ""]
    S += [f"- {f['name']} ({f['company'] or 'company not shown'}, {f['county'] or '?'} County)"
          for f in sorted(unmatched, key=lambda f: f["name"].lower())]
    (hv_dir / "harvest_summary.md").write_text("\n".join(S) + "\n", encoding="utf-8")
    log("done")


if __name__ == "__main__":
    main()

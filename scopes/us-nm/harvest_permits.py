"""
Harvest New Mexico air permits before a research sweep.

New Mexico has three air permit authorities and several lists that show work in progress. Every
source below answers without a sign-in. What was found (2026-11-17):

  1. The New Mexico Environment Department (NMED) Air Quality Bureau, everywhere outside
     Bernalillo County and tribal land. Its complete record is APMAP, the facility map at
     https://rsmt.air.net.env.nm.gov/. The map reads an open service,
     https://rsmt-api-c4cwg2h3a2ewdjf4.westus2-01.azurewebsites.net/ :
       get-facility-locations            every facility: AI number (tempoMasterAiId), name, address,
                                         county, latitude, longitude
       get-facility-name-wildcards?facility=<name>   facility names that contain the text
       get-facility-popup?ai=<n>         an HTML card: organization, program, NSR and Title V
                                         permit numbers, AIRS number, facility type
     Each facility's documents are a public collection. The map's utils.js holds a public key, and
       https://cloud.env.nm.gov/air/plugins/api_search/index.php?key=<key>&search_type=public_collections&search=AI%20<n>
     (needs a browser User-Agent and the header Referer: https://rsmt.air.net.env.nm.gov/, else
     403) answers with the collection address, https://cloud.env.nm.gov/resources/collection/<id>.
     That page lists every PDF as a /resources/_translator.php/<code>.pdf link. The key is read from
     utils.js at run time; the constant below is the fallback when that page cannot be read.
  2. NMED public notices, https://www.env.nm.gov/public-notices/. One accordion block per notice
     (a heading, then links). Air Quality Bureau blocks carry the draft permit, statement of basis
     and application links.
  3. NMED Coda tables (Current Permitting Actions Under Review, AQB NSR Issued Report, AQB
     Facilities Lat Long Report). They are published Coda docs. Coda's page shows only the first
     rows, and its API answers 401 without a token, so the harvester reads them through the Coda
     API only when CODA_API_TOKEN is set (a free token from a Coda account) and otherwise records
     what a person must do.
  4. The City of Albuquerque Air Quality Program (Bernalillo County: Reeves, Rio Bravo, Albuquerque
     data centers): the pending applications page, the monthly air quality notification report
     (aqn-report.pdf) and the application pages under cabq.gov/airquality/news/.
  5. EPA Region 9 for the Navajo Transitional Energy Company (NTEC) gas plant, docket
     EPA-R09-OAR-2024-0028, through api.regulations.gov (the DEMO_KEY allows 10 calls an hour, so
     calls are cached and paced; set REGULATIONS_GOV_KEY for a free key). EPA ECHO lists the state's
     electric facilities (SIC 4911) as a cross-check.

Steps:
  1. Read APMAP's facility list and match each GEM plant and each lead (name patterns checked by
     hand, then the distance to the GEM point, then name words) to facilities. Popups give the
     organization and permit numbers.
  2. List each matched facility's document collection, download the PDFs into
     scopes/us-nm/work/permits/docs/<AI>/ (a page that is not a PDF falls back to a saved copy at
     the Wayback Machine), extract text with pdftotext -layout and keep the lines that give permit
     numbers, equipment counts, makers, sizes, dates and the site.
  3. Read the notices, the Coda tables, the Albuquerque pages, the EPA docket and the ECHO list.
  4. The sweep: facilities with power-like names that match no plant or lead go to _unmatched.md,
     with their collection address (the first --sweep-read are listed).

Output, in scopes/us-nm/work/permits/ (what the sweep agents read): <GEM location id>.md and .json
per plant, _leads.md, _unmatched.md, _notices.md, _coda.md, _albuquerque.md, _epa.md, index.json
and harvest_log.jsonl. A summary and facilities.json (the file data_center_fleets.py reads) go to
batches/<scope>/harvest/. Permit PDFs name agency and company staff: the PDFs and their text stay
under work/ (never committed). Nothing here stages a record.

Usage (from the repo root):
    python scopes/us-nm/harvest_permits.py --scope us-nm                         # everything
    python scopes/us-nm/harvest_permits.py --scope us-nm --plants L100000402297  # one plant
    python scopes/us-nm/harvest_permits.py --scope us-nm --match-only            # list matches only
    python scopes/us-nm/harvest_permits.py --scope us-nm --offline               # saved sample pages
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

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from fetch import CHROME_UA  # noqa: E402
from geo import distance_m  # noqa: E402
from harvest_lib import (CSV, REPO, SIZE, clean_ws, get, harvest_out, norm_county, pick, report_failure,  # noqa: E402
                         wayback_url)

APMAP_UI = "https://rsmt.air.net.env.nm.gov/"
APMAP = "https://rsmt-api-c4cwg2h3a2ewdjf4.westus2-01.azurewebsites.net/"
APMAP_UTILS = APMAP_UI + "js/utils.js"
CLOUD_SEARCH = "https://cloud.env.nm.gov/air/plugins/api_search/index.php"
# The public key in APMAP's utils.js (a constant every visitor's browser sends). Read live first.
CLOUD_KEY_FALLBACK = "I4M8PZ4avSwxh4mC-Btujz3BrY4THHRtT0BvSyoWz9QCqL5t_1DGuJS5QWhuujjX2iujgvATfR-ouCBzLVmWAA"
NOTICES = "https://www.env.nm.gov/public-notices/"
AQB_PAGE = "https://www.env.nm.gov/air-quality/permitting-section/"
CODA_DOCS = [
    {"name": "Current Permitting Actions Under Review", "doc": "w_kXh6I1El",
     "url": "https://coda.io/d/Current-Permitting-Actions-Under-Review_dw_kXh6I1El/Current-Permitting-Actions-Under-Review_suKp1"},
    {"name": "AQB NSR Issued Report", "doc": "or5zr_0oRP",
     "url": "https://coda.io/d/AQB-NSR-Issued-Report_dor5zr_0oRP/AQB-NSR-Issued-Data_suKp1"},
    {"name": "AQB Facilities Lat Long Report", "doc": "JP8fpOjfLG",
     "url": "https://coda.io/d/AQB-Facilities-Lat-Long-Report_dJP8fpOjfLG/AQB-Facilities-Latitude-Longitude_suKp1"},
]
CODA_API = "https://coda.io/apis/v1"
ABQ_PENDING = "https://www.cabq.gov/airquality/pending-air-permit-applications"
ABQ_AQN = "https://www.cabq.gov/airquality/documents/aqn-report.pdf"
REGS_API = "https://api.regulations.gov/v4"
REGS_DOCKET = "EPA-R09-OAR-2024-0028"
ECHO = "https://echodata.epa.gov/echo/air_rest_services"
ECHO_COLS = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21"
FIXTURES = REPO / "tests" / "fixtures" / "harvest_nm"

# Hand-checked per GEM plant. "ai" are APMAP AI numbers (Cunningham 604 and Maddox 588 were proven
# on 2026-11-17; the rest are matched by name and distance and marked for checking). "names" are
# lower-case regular expressions tried on a facility's name, organization and notice text.
KNOWN = {
    "L100000401601": {"ai": [], "names": [r"\bluna (energy|generat|power)"]},
    "L100000401903": {"ai": [], "names": [r"rio grande (generating|power|station|plant)", r"\bepe\b.*rio grande"]},
    "L100000402045": {"ai": [25726], "names": [r"hobbs generat", r"hobbs power"]},
    "L100000402228": {"ai": [], "names": [r"afton generat"]},
    "L100000402229": {"ai": [], "names": [r"reeves"]},
    "L100000402230": {"ai": [], "names": [r"rio bravo (gen|power|station)", r"rio bravo"]},
    "L100000402297": {"ai": [604], "names": [r"cunningham (station|power|plant)"]},
    "L100000402299": {"ai": [588], "names": [r"maddox"]},
    "L100000402347": {"ai": [], "names": [r"valencia (energy|power|gen)"]},
    "L100000402507": {"ai": [], "names": [r"chino mine"]},
    "L100000402529": {"ai": [3535], "names": [r"bluffview"]},
    "L100000408054": {"ai": [], "names": [r"clean path"]},
    "L100001043002": {"ai": [], "names": [r"\bntec\b", r"navajo transitional"]},
    "L100001080449": {"ai": [], "names": [r"lea county data", r"lea county.*data cent"]},
    "L100001080450": {"ai": [], "names": [r"project jupiter", r"borderplex", r"\bacoma\b"]},
    "L100001083303": {"ai": [560], "names": [r"lordsburg generat", r"lordsburg (?:energy|repowering)"]},
    "L100001089557": {"ai": [], "names": [r"site layer"]},
    "L100001089610": {"ai": [], "names": [r"westside", r"saddle butte"]},
    "L100001089629": {"ai": [], "names": [r"roswell information", r"e2b4", r"sustany"]},
    # IRP placeholders have no site yet; SWPP ERAS Hobbs is a planning entry. Nothing to match by name.
    "L100001082463": {"ai": [], "names": []}, "L100001082465": {"ai": [], "names": []},
    "L100001082467": {"ai": [], "names": []}, "L100001082470": {"ai": [], "names": []},
    "L100001083387": {"ai": [], "names": [r"lea power"]},
}
DIST_KM = 2.0

# Leads: projects GEM lacks or knows under another name. "queries" go to the APMAP name search.
LEADS = [
    {"key": "pyramid", "name": "Pyramid Generating Station (Tri-State)", "queries": ["Pyramid", "Tri-State"],
     "names": [r"pyramid (gen|station|power)", r"tri-?state.*pyramid"]},
    {"key": "zenith-volts", "name": "Zenith Volts (Chaves County)", "queries": ["Zenith"], "names": [r"zenith"]},
    {"key": "greater-kudu", "name": "Greater Kudu (Meta Los Lunas)", "queries": ["Kudu", "Meta Platforms", "Los Lunas"],
     "names": [r"kudu", r"meta platforms", r"los lunas.*data"]},
    {"key": "project-jupiter", "name": "Project Jupiter, Acoma, BorderPlex, Stack",
     "queries": ["Jupiter", "BorderPlex", "Acoma", "Stack"], "names": [r"project jupiter", r"borderplex", r"\bacoma\b", r"stack infra"]},
    {"key": "google-lea", "name": "Google Lea County", "queries": ["Google"], "names": [r"google"]},
    {"key": "new-era", "name": "New Era Energy & Digital", "queries": ["New Era", "NEE"],
     "names": [r"new era (energy|helium|digital)", r"nee digital"]},
    {"key": "e2b4-sustany", "name": "E2B4 / Sustany (Roswell)", "queries": ["E2B4", "Sustany", "Roswell Information"],
     "names": [r"e2b4", r"sustany", r"roswell information"]},
    {"key": "site-layer-1", "name": "Site Layer 1", "queries": ["Site Layer"], "names": [r"site layer"]},
    {"key": "santa-teresa", "name": "Santa Teresa data centers", "queries": ["Santa Teresa"],
     "names": [r"santa teresa.*(data|power|energy)"]},
    {"key": "saddle-butte", "name": "Saddle Butte Westside", "queries": ["Saddle Butte", "Westside"],
     "names": [r"saddle butte", r"westside"]},
    {"key": "ntec", "name": "NTEC (Navajo Transitional Energy Company)", "queries": ["NTEC", "Navajo Transitional"],
     "names": [r"\bntec\b", r"navajo transitional"]},
    {"key": "lea-power-partners", "name": "Lea Power Partners (Hobbs)", "queries": ["Lea Power"], "names": [r"lea power"]},
]

POWER_NAME = re.compile(
    r"power|generat|station|energy|data ?cent|datacent|micro ?grid|turbine|engine|electric|cogen|peaking|"
    r"combined cycle|hyperscal|bitcoin|crypto|computing|compute|\bpnm\b|public service co|southwestern public|"
    r"el paso electric|tri-?state|xcel|\bntec\b|meta platforms|google|microsoft|amazon|\bqts\b", re.I)
POWER_DROP = re.compile(
    r"compressor|gas plant|gas processing|processing plant|booster|\bcdp\b|\bctb\b|\bpad\b|wellsite|well site|"
    r"battery|tank farm|pipeline|\bmine\b|quarry|crusher|asphalt|concrete|landfill|dairy|school|hospital|"
    r"cell tower|substation|lift station|pump station|metering|meter station|gathering|dehydrat|saltwater|"
    r"disposal|\bswd\b|truck|refinery|terminal|alternative compliance|ozone precursor|rulemaking|hearing notice|"
    r"\beib\b|water|college|university|airport|fuel(ing)? station|filling station|gasoline|\bcrude\b", re.I)
NAME_NOISE = re.compile(
    r"\b(power station|power plant|generating station|generating|generation|facility|station|energy center|"
    r"energy|plant|power|nm|new|mexico|the|of|and|llc|inc|company|co|corp|corporation|combined|cycle|county|"
    r"center|data|east|west|gen|stn)\b", re.I)
EQUIPMENT = re.compile(r"turbine|\bct\b|engine|rice\b|generat|\bgen\b|boiler|duct burner|hrsg|combined cycle|"
                       r"simple cycle|peaking|diesel|reciprocating|genset|microgrid|fuel cell", re.I)
MAKER = re.compile(r"model\b|caterpillar|cat g|wartsila|w[äa]rtsil[äa]|jenbacher|general electric|\bGE\b|siemens|"
                   r"solar turbines|mitsubishi|cummins|rolls[- ]royce|mtu\b|kohler|generac|waukesha|pratt|ansaldo|"
                   r"baker hughes|hitachi|bloom|titan \d|taurus|mars \d|lm ?\d{4}|7ea|7fa|7ha|6b\b|f-?class|h-?class",
                   re.I)
LOCATION = re.compile(
    r"latitude|longitude|\blat\b|\blong\b|\bUTM\b|located (at|in|on|near|approximately)|physical address|"
    r"site address|facility address|street address|\b\d+(\.\d+)? mi(les)? [NSEW]{1,3} of\b|county,? new mexico|"
    r"\bNM 8[0-9]{4}\b|new mexico 8[0-9]{4}", re.I)
PROJECT = re.compile(r"proposes|propose to|will consist|project (is|will|consists)|construction of|to construct|"
                     r"new (electric|power|generat)|install(ation)? of|modification", re.I)
FACILITY_LINE = re.compile(r"facility( name)?:|company( name)?:|applicant:|source name|permittee|\bre:|"
                           r"permit (no|number)|\bAI\b ?(#|no|number)|\bAI ?\d{3,6}|county,? new mexico|operator", re.I)
DATES = re.compile(r"(issued|effective|expir|received|startup|start-up|commence|completion|deadline|due)\b.{0,60}"
                   r"(\d{1,2}/\d{1,2}/\d{2,4}|(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.? \d{1,2},? \d{4})",
                   re.I)
COUNT = re.compile(r"\b(\d{1,3}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|sixteen|eighteen|"
                   r"twenty)\s+(?:[A-Za-z\-]+\s+){0,3}(engines?|turbines?|generators?|gensets?|units?)\b", re.I)
LATLON = re.compile(r"\b(3[1-7]\.\d{3,})[\s,;/°N-]{1,12}(10[3-9]\.\d{3,})\b")
PERMIT_NO = re.compile(r"\b(?:P\d{3}(?:R\d+)?(?:M\d+)?|PSD ?\d{2,4}(?:M\d+)?|\d{3,5}-M\d+(?:R\d+)?|NSR ?\d{3,5}(?:M\d+)?|"
                       r"GCP-\d-\d{4}|\d{4}-AQN\d+)\b")
READ_FIRST = re.compile(r"permit|statement of basis|application|technical|evaluation|review|NSR|PSD|database summary", re.I)
SWEEP_DC = re.compile(r"data ?cent|datacent|hyperscal|cryptocurrenc|bitcoin|blockchain|\bcolocation\b|microgrid", re.I)
MONTHS = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}


def log(msg):
    print(f"[harvest-nm] {msg}", file=sys.stderr, flush=True)


def words(text):
    t = NAME_NOISE.sub(" ", re.sub(r"\(.*?\)", " ", str(text or "")))
    return {w.lower() for w in re.split(r"[^A-Za-z]+", t) if len(w) >= 4}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s or "").lower()).strip("-")[:60] or "x"


def iso_date(s):
    """'2026-10-07T..', '10/07/2026' or 'August 19, 2002' to 2026-10-07, or ''."""
    s = str(s or "")
    m = re.match(r"(\d{4}-\d{2}-\d{2})", s)
    if m:
        return m.group(1)
    m = re.search(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b", s)
    if m:
        return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}"
    m = re.search(r"\b([A-Za-z]{3})[a-z]*\.? (\d{1,2}),? (\d{4})\b", s)
    if m and m.group(1).lower() in MONTHS:
        return f"{m.group(3)}-{MONTHS[m.group(1).lower()]:02d}-{int(m.group(2)):02d}"
    return ""


def tags_to_text(s):
    return clean_ws(html.unescape(re.sub(r"<[^>]+>", " ", s or "")))


# ------------------------------------------------------------------- access ---

class Net:
    """Plain requests with retries, or saved sample pages when offline. Every give-up goes to
    fetch.py's give-up log through report_failure so access_audit.py retries it."""

    def __init__(self, offline=False, fixtures=None):
        self.offline = offline
        self.fix = Path(fixtures) if fixtures else FIXTURES
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": CHROME_UA, "Accept": "*/*", "Accept-Language": "en-US,en;q=0.9"})
        self.calls, self.errors = 0, []

    def fixture(self, name):
        p = self.fix / name
        return p.read_text(encoding="utf-8") if p.exists() else None

    def req(self, url, fixture=None, headers=None, params=None, timeout=120, tries=3, quiet=False, binary=False):
        """The response (or a fixture stand-in with .status_code, .text, .content), or None."""
        if self.offline:
            txt = self.fixture(fixture) if fixture else None
            if txt is None:
                return None
            return type("Fixture", (), {"status_code": 200, "text": txt, "content": txt.encode("utf-8"),
                                        "json": lambda self_: json.loads(txt)})()
        err = ""
        for attempt in range(tries):
            self.calls += 1
            try:
                r = self.s.get(url, headers=headers, params=params, timeout=timeout)
                if r.status_code == 200:
                    return r
                err = str(r.status_code)
                if r.status_code in (401, 403, 404, 429) and attempt >= 1:
                    break
            except requests.RequestException as e:
                err = "000 " + str(e)[:100]
            time.sleep(2 * (attempt + 1))
        self.errors.append(f"GET {url}: {err}")
        if not quiet:
            report_failure(url, err.split()[0] if err else "000", "harvester call failed")
        return None

    def json(self, url, fixture=None, **kw):
        r = self.req(url, fixture, **kw)
        try:
            return r.json() if r is not None else None
        except ValueError:
            self.errors.append(f"GET {url}: not JSON")
            return None


def cloud_key(net):
    """The public key in APMAP's utils.js, read live; the fallback constant if the page is unreadable."""
    r = net.req(APMAP_UTILS, "apmap_utils.js", quiet=True, tries=2)
    m = re.search(r"api_search/index\.php\"?\s*\+?\s*\"\?key=([A-Za-z0-9_\-]+)", r.text) if r is not None else None
    return m.group(1) if m else CLOUD_KEY_FALLBACK


# ---------------------------------------------------------------- facilities ---

def new_fac(key, name, source):
    return {"key": key, "name": name, "source": source, "company": "", "county": "", "city": "", "address": "",
            "ai": None, "lat": None, "lon": None, "codes": [], "activities": [], "permits": [], "found_by": [],
            "docs": [], "hint": "", "links": [], "collection": ""}


def fac_text(f):
    return " | ".join(x for x in (f["company"], f["name"], f["county"], f.get("hint", "")) if x).lower()


def is_power(f):
    """A power or data center look: a power-like name not on the drop list."""
    if POWER_DROP.search(f["name"]):
        return False
    return bool(POWER_NAME.search(f"{f['company']} {f['name']} {f.get('hint', '')[:200]}"))


def parse_locations(rows):
    """APMAP get-facility-locations JSON to facilities keyed ai-<n>."""
    facs = {}
    for r in rows or []:
        try:
            ai = int(r["tempoMasterAiId"])
        except (KeyError, TypeError, ValueError):
            continue
        f = facs.setdefault(f"ai-{ai}", new_fac(f"ai-{ai}", clean_ws(r.get("facilityName")), "NMED APMAP"))
        f["ai"] = ai
        f["county"] = clean_ws(r.get("county"))
        f["city"] = clean_ws(r.get("city"))
        f["address"] = ", ".join(x for x in (clean_ws(r.get("address1")), clean_ws(r.get("address2")),
                                             clean_ws(r.get("city")), clean_ws(r.get("zip"))) if x)
        f["lat"], f["lon"] = r.get("latitude"), r.get("longitude")
        f["links"] = [{"kind": "APMAP facility report", "number": "", "url": f"{APMAP_UI}facility-report.html?ai={ai}"}]
    return facs


def parse_popup(text):
    """APMAP popup HTML to {name, location, county, program, nsr, tv, airs, type, organization}."""
    cells = [tags_to_text(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", text or "", re.S)]
    cells = [c for c in cells if c]
    out = {"cells": cells}

    def after(label):
        for c in cells:
            m = re.match(re.escape(label) + r"\s*:?\s*(.*)$", c, re.I)
            if m:
                return m.group(1).strip()
        return ""
    out.update(name=cells[0] if cells else "", organization=after("Organization"), program=after("Facility Program"),
               nsr=after("NSR Permit Number"), tv=after("TV Permit Number"), airs=after("AIRS Number"),
               type=after("Facility Type"), county=next((c for c in cells if c.endswith(" County")), ""))
    return out


def apply_popup(f, pop):
    f["company"] = pop.get("organization", "") or f["company"]
    nums = []
    for label, key in (("NSR permit", "nsr"), ("Title V permit", "tv")):
        v = pop.get(key, "")
        if v:
            nums.append(v)
            f["permits"].append({"number": v, "type": label, "status": "listed on the APMAP card",
                                 "step": pop.get("program", ""), "comment_ends": ""})
    if pop.get("airs"):
        f["codes"].append(f"AIRS {pop['airs']}")
    if pop.get("type"):
        f["hint"] = (f["hint"] + " " + f"Facility type: {pop['type']}.").strip()


def parse_collection(text):
    """A cloud.env.nm.gov collection page: [{url, title, filename, number, date, type}]."""
    docs = []
    for url, title, fname in re.findall(
            r"<a href='([^']*_translator\.php/[^']+)'[^>]*>\s*<h3>\s*(.*?)\s*</h3>\s*</a>\s*"
            r"<p class='originalfilename'>Original Filename: (.*?)</p>", text or "", re.S):
        title, fname = clean_ws(html.unescape(title)), clean_ws(html.unescape(fname))
        m = re.match(r"(\w[\w ]*?)\s*\((.+?)\)\.\w+$", fname)
        docs.append({"url": url, "title": title, "filename": fname, "type": m.group(1) if m else fname,
                     "number": m.group(2) if m else "", "date": iso_date(title) or iso_date(fname),
                     "name": f"{title} ({fname})", "key": url})
    h1 = re.search(r"<h1>Collection:\s*(.*?)</h1>", text or "", re.S)
    return (clean_ws(html.unescape(h1.group(1))) if h1 else ""), docs


def parse_notices(text):
    """The NMED public notices page: one entry per accordion block, with the Air Quality Bureau
    ones flagged. [{title, air, text, posted, comment, numbers, links: [{label, url}]}]"""
    out = []
    for blk in re.split(r"<div class='nmenv_accordion_item level_1'>", text or "")[1:]:
        t = re.search(r"<h2>(.*?)</h2>", blk, re.S)
        if not t:
            continue
        body = blk[t.end():]
        plain = tags_to_text(body)
        links = [{"label": tags_to_text(lbl), "url": html.unescape(href)}
                 for href, lbl in re.findall(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>', body, re.S)
                 if href.startswith("http") and not href.startswith("mailto")]
        posted = re.search(r"posted\s+(\d{1,2}/\d{1,2}/\d{4})", plain, re.I)
        comment = re.search(r"Comment period\s+(\d{1,2}/\d{1,2}/\d{4})\s*(?:to|-|–)\s*(\d{1,2}/\d{1,2}/\d{4})", plain, re.I)
        title = tags_to_text(t.group(1))
        air = bool(re.search(r"Air Quality Bureau|\bAQB\b|air quality (operating|permit)", plain + " " + title, re.I))
        out.append({"title": title, "air": air, "text": plain[:1500], "links": links,
                    "posted": iso_date(posted.group(1)) if posted else "",
                    "comment": [iso_date(comment.group(1)), iso_date(comment.group(2))] if comment else [],
                    "numbers": sorted(set(PERMIT_NO.findall(plain + " " + " ".join(x["label"] for x in links))))})
    return out


def notice_facilities(notices):
    facs = {}
    for n in notices:
        if not n["air"]:
            continue
        key = "notice-" + slug(n["title"])
        f = facs.setdefault(key, new_fac(key, n["title"], "NMED public notices"))
        f["hint"] = n["text"][:400]
        f["permits"].append({"number": ", ".join(n["numbers"]), "type": "notice at comment", "status": "public notice",
                             "step": f"posted {n['posted']}" if n["posted"] else "",
                             "comment_ends": n["comment"][1] if len(n["comment"]) > 1 else ""})
        for x in n["links"]:
            f["docs"].append({"number": ", ".join(PERMIT_NO.findall(x["label"])), "name": x["label"], "type": x["label"],
                              "date": n["posted"], "url": x["url"], "how": "NMED public notices page", "key": x["url"]})
    return facs


def parse_abq_pending(text):
    """Albuquerque pending applications page: [{application, name, description, url}]."""
    out = []
    for art in re.findall(r"<article class=\"row mb-3\">(.*?)</article>", text or "", re.S):
        m = re.search(r'<h2>\s*<a class="summary url" href="([^"]+)"[^>]*>(.*?)</a>', art, re.S)
        if not m:
            continue
        title = tags_to_text(m.group(2))
        a = re.match(r"Application #?\s*([\w\-]+),?\s*(.*)$", title)
        d = re.search(r'<span class="description">(.*?)</span>', art, re.S)
        out.append({"application": a.group(1) if a else "", "name": a.group(2) if a else title, "title": title,
                    "description": tags_to_text(d.group(1)) if d else "", "url": html.unescape(m.group(1))})
    return out


def parse_aqn_report(text):
    """Albuquerque monthly notification report text: one dict per record line."""
    rows, cur = [], None
    for ln in (text or "").splitlines():
        m = re.match(r"^(\d{4}-AQN\d+)\s+(.*)$", ln)
        if m:
            cur = {"record": m.group(1), "lines": [m.group(2)]}
            rows.append(cur)
        elif cur is not None and ln.strip() and not ln.startswith("Record #"):
            cur["lines"].append(ln.strip())
    out = []
    for r in rows:
        head = re.split(r"\s{2,}", r["lines"][0].strip())
        tail = " ".join(re.sub(r"\s{2,}", " ", x) for x in r["lines"][1:])
        issued = re.search(r"(\d{1,2}/\d{1,2}/\d{4})", " ".join(r["lines"]))
        out.append({"record": r["record"], "facility": head[0] if head else "", "company": head[1] if len(head) > 1 else "",
                    "text": clean_ws(" ".join(head[2:]) + " " + tail), "issued": iso_date(issued.group(1)) if issued else ""})
    return out


def abq_facilities(pending, aqn):
    facs = {}
    for p in pending:
        key = "abq-pending-" + slug(p["application"] + "-" + p["name"])
        f = facs.setdefault(key, new_fac(key, p["name"], "Albuquerque Air Quality pending applications"))
        f["county"], f["city"], f["company"] = "Bernalillo", "Albuquerque", p["description"][:120]
        f["hint"] = p["description"]
        f["permits"].append({"number": p["application"], "type": "pending application", "status": "pending",
                             "step": "", "comment_ends": ""})
        f["links"].append({"kind": p["title"], "number": p["application"], "url": p["url"]})
    for r in aqn:
        key = "abq-aqn-" + slug(r["record"])
        f = facs.setdefault(key, new_fac(key, r["facility"], "Albuquerque notification report"))
        f["county"], f["city"], f["company"] = "Bernalillo", "Albuquerque", r["company"]
        f["hint"] = r["text"]
        f["permits"].append({"number": r["record"], "type": "air quality notification", "status": "issued",
                             "step": f"issued {r['issued']}" if r["issued"] else "", "comment_ends": ""})
        f["links"].append({"kind": "Albuquerque air quality notification report", "number": r["record"], "url": ABQ_AQN})
    return facs


def echo_facilities(rows):
    facs = {}
    for r in rows or []:
        if "PORTABLE" in str(r.get("AIRStreet") or "").upper():
            continue
        sid = r.get("SourceID") or slug(r.get("AIRName"))
        f = facs.setdefault(f"echo-{sid}", new_fac(f"echo-{sid}", clean_ws(r.get("AIRName")), "EPA ECHO (SIC 4911)"))
        f["county"] = clean_ws(r.get("AIRCounty")).title()
        f["city"] = clean_ws(r.get("AIRCity")).title()
        f["address"] = clean_ws(r.get("AIRStreet"))
        f["codes"] = [c for c in (r.get("FacSICCodes"), r.get("AIRNAICS")) if c]
        f["hint"] = f"ECHO source {sid}; SIC {r.get('FacSICDescs') or ''}"
        f["links"].append({"kind": "ECHO facility", "number": "",
                           "url": f"https://echo.epa.gov/detailed-facility-report?fid={r.get('RegistryID')}"})
    return facs


def regs_facility(docs):
    f = new_fac("epa-ntec-docket", f"NTEC gas plant, EPA Region 9 docket {REGS_DOCKET}", "EPA Region 9 docket")
    f["county"], f["city"] = "San Juan", "Farmington"
    f["hint"] = "NTEC gas plant (Navajo Transitional Energy Company), a synthetic minor permit on Navajo land."
    for d in docs:
        f["docs"].append({"number": d["id"], "name": d["title"], "type": d["type"], "date": d["posted"],
                          "url": d["url"], "page": d["page"], "how": "regulations.gov docket list", "key": d["id"]})
    return f


def coda_facilities(table, rows):
    facs = {}
    for i, r in enumerate(rows):
        vals = [str(v) for v in r.values() if v not in (None, "")]
        label = next((str(r[k]) for k in r if re.search(r"facility|company|name|applicant", k, re.I) and r[k]), vals[0] if vals else "")
        key = f"coda-{slug(table)}-{i}"
        f = facs.setdefault(key, new_fac(key, clean_ws(label), f"NMED Coda: {table}"))
        f["hint"] = " | ".join(f"{k}: {v}" for k, v in r.items() if v not in (None, ""))[:400]
        for n in dict.fromkeys(PERMIT_NO.findall(f["hint"])):
            f["permits"].append({"number": n, "type": table, "status": "listed in a Coda table", "step": "", "comment_ends": ""})
        for k, v in r.items():
            if re.search(r"lat", k, re.I) and re.match(r"-?\d+\.\d+$", str(v)):
                f["lat"] = float(v)
            if re.search(r"lon", k, re.I) and re.match(r"-?\d+\.\d+$", str(v)):
                f["lon"] = float(v)
    return facs


def match(plant, facs):
    """[(facility, how)]: hand-checked AI numbers and names, then distance to the GEM point (APMAP
    facilities only), else the plant's name words plus county for a plant with no hand-checked entry."""
    k = KNOWN.get(plant["id"])
    out = []
    for f in facs:
        t = fac_text(f)
        if k and f["ai"] in k.get("ai", []) and f["ai"] is not None:
            out.append((f, "checked by hand"))
        elif k and any(re.search(p, t) for p in k.get("names", [])):
            out.append((f, "matched by a hand-checked name, check it is this plant"))
        elif f["source"] == "NMED APMAP" and plant.get("lat") is not None and f["lat"] is not None \
                and (d := distance_m(plant["lat"], plant["lon"], f["lat"], f["lon"])) is not None and d <= DIST_KM * 1000 \
                and is_power(f):
            out.append((f, f"{d / 1000:.1f} km from the GEM point, check it is this plant"))
        elif not k and plant["name_words"] and plant["name_words"] <= words(f["name"]) and is_power(f) \
                and (not plant["county"] or not f["county"] or plant["county"].lower() == f["county"].lower()):
            out.append((f, "matched by name and county, check it is this plant"))
    return out


def match_lead(lead, facs):
    return [f for f in facs if any(re.search(p, fac_text(f)) for p in lead["names"])]


# ---------------------------------------------------------------- documents ---

def pdf_text(path, pages=None):
    cmd = ["pdftotext", "-layout"] + (["-l", str(pages)] if pages else []) + [str(path), "-"]
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=300).stdout
    except (subprocess.SubprocessError, OSError):
        return ""


def doc_path(out_dir, f, d):
    folder = str(f["ai"]) if f["ai"] else slug(f["key"])
    return out_dir / "docs" / folder / f"{d['date'] or 'nodate'}_{slug(d['type'])[:30]}_{slug(d['number'] or d['title'] if 'title' in d else d['name'])[:24]}.pdf"


def download(net, url, path, headers=None):
    """Download a PDF. A server that answers with an HTML page falls back to the newest saved copy at
    the Wayback Machine. Returns a state sentence."""
    if net.offline:
        return "offline, not downloaded"
    r = net.req(url, headers=headers, timeout=300)
    state = "downloaded"
    if r is None or r.content[:5] != b"%PDF-":
        if r is not None:
            report_failure(url, "200", "not a PDF")
        wb = wayback_url(url)
        r2 = net.req(wb, timeout=300, quiet=True) if wb else None
        if r2 is None or r2.content[:5] != b"%PDF-":
            return "not downloaded" if r is None else "not a PDF"
        r, state = r2, "downloaded from a saved copy at the Wayback Machine (" + wb + ")"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(r.content)
    return state


def doc_facts(text):
    return {
        "ids": sorted({re.sub(r"\s+", " ", x).upper() for x in PERMIT_NO.findall(text)})[:8],
        "facility": pick(text, FACILITY_LINE, 6),
        "project": pick(text, PROJECT, 6),
        "equipment": pick(text, EQUIPMENT, 10),
        "counts": [f"{m.group(0)}" for m in COUNT.finditer(text)][:8],
        "makers": pick(text, MAKER, 8),
        "sizes": pick(text, SIZE, 10),
        "dates": pick(text, DATES, 8),
        "location": pick(text, LOCATION, 8),
        "coords": [f"{a}, -{b.lstrip('-')}" for a, b in LATLON.findall(text)][:3],
    }


def read_doc(net, out_dir, f, d, pages=None):
    """Download one document (kept on disk, reused next run), extract its text and keep facts."""
    path = doc_path(out_dir, f, d)
    txt = path.with_suffix(".txt")
    if not d["url"].lower().split("?")[0].endswith(".pdf") and "_translator.php" not in d["url"] \
            and "downloads.regulations.gov" not in d["url"]:
        d["state"], d["file"], d["facts"] = "a web page, not downloaded; open the link", "", {}
        return ""
    headers = {"Referer": APMAP_UI} if "cloud.env.nm.gov" in d["url"] else None
    state = "saved (from an earlier run)" if path.exists() else download(net, d["url"], path, headers)
    d["file"] = str(path.relative_to(REPO)) if path.exists() else ""
    text = pdf_text(path, pages) if path.exists() else ""
    if path.exists():
        txt.write_text(text, encoding="utf-8")
    d["state"] = state if text.strip() or not d["file"] else state + ", no text layer (a scan; use fetch.py --render for OCR)"
    d["facts"] = doc_facts(text) if text.strip() else {}
    return text


def rank_docs(docs):
    """Permits, statements of basis and applications first, newest first, undated last."""
    return sorted(docs, key=lambda d: (not READ_FIRST.search(d["type"] + " " + d.get("name", "")), not d["date"],
                                       "".join(chr(255 - ord(c)) for c in d["date"])))


def cloud_collection(net, key, ai):
    """The public collection address of an AI number, or ''."""
    j = net.json(CLOUD_SEARCH, f"cloud_search_{ai}.json", headers={"Referer": APMAP_UI},
                 params={"key": key, "search_type": "public_collections", "search": f"AI {ai}"})
    for it in (j or {}).get("items", []):
        if f"(AI {ai})" in it.get("title", ""):
            return it.get("public_collection_url", "").replace("\\/", "/")
    return ""


def list_documents(net, key, f):
    """Fill f['collection'] and return the facility's documents."""
    if not f["ai"]:
        return []
    f["collection"] = f["collection"] or cloud_collection(net, key, f["ai"])
    if not f["collection"]:
        return []
    r = net.req(f["collection"], f"collection_{f['ai']}.html", headers={"User-Agent": CHROME_UA})
    if r is None:
        return []
    _, docs = parse_collection(r.text)
    f["links"].append({"kind": "document collection", "number": "", "url": f["collection"]})
    return docs


# ------------------------------------------------------- the other sources ---

def read_notices(net):
    r = net.req(NOTICES, "notices.html")
    return parse_notices(r.text) if r is not None else None


def read_coda(net):
    """Rows of the three Coda tables. Coda's API needs a token; without one each table is reported
    as a give-up that says what a person must do. Returns ({table: rows}, [problem sentences])."""
    import os
    token = os.environ.get("CODA_API_TOKEN")
    out, problems = {}, []
    for d in CODA_DOCS:
        if net.offline:
            txt = net.fixture(f"coda_{d['doc']}.json")
            if txt:
                out[d["name"]] = json.loads(txt)
                continue
            problems.append(f"{d['name']}: offline, no saved rows")
            continue
        if token:
            hdr = {"Authorization": f"Bearer {token}"}
            tj = net.json(f"{CODA_API}/docs/{d['doc']}/tables", headers=hdr, quiet=True)
            tables = (tj or {}).get("items", [])
            if tables:
                rows, url = [], f"{CODA_API}/docs/{d['doc']}/tables/{tables[0]['id']}/rows?useColumnNames=true&limit=500"
                while url:
                    j = net.json(url, headers=hdr)
                    if not j:
                        break
                    rows += [r.get("values", {}) for r in j.get("items", [])]
                    url = j.get("nextPageLink")
                out[d["name"]] = rows
                continue
        msg = (f"{d['name']}: Coda's page shows only the first rows and its API answers 401 without a token. "
               f"A person must set CODA_API_TOKEN (a free Coda account token) and rerun, or open {d['url']} and "
               "export the table to CSV into scopes/us-nm/work/permits/coda/")
        report_failure(d["url"], "401", msg)
        problems.append(msg)
        csv = Path(REPO / "scopes" / "us-nm" / "work" / "permits" / "coda" / f"{slug(d['name'])}.csv")
        if csv.exists():
            out[d["name"]] = pd.read_csv(csv, dtype=str).fillna("").to_dict("records")
            problems[-1] += f" (a hand export {csv.name} was read instead)"
    return out, problems


def read_abq(net, pages_for=None):
    r = net.req(ABQ_PENDING, "abq_pending.html")
    pending = parse_abq_pending(r.text) if r is not None else []
    aqn = []
    if net.offline:
        t = net.fixture("aqn_report.txt")
    else:
        pdf = net.req(ABQ_AQN, timeout=300)
        t = None
        if pdf is not None and pdf.content[:5] == b"%PDF-":
            tmp = REPO / "scopes" / "us-nm" / "work" / "permits" / "albuquerque" / "aqn-report.pdf"
            tmp.parent.mkdir(parents=True, exist_ok=True)
            tmp.write_bytes(pdf.content)
            t = pdf_text(tmp)
    if t:
        aqn = parse_aqn_report(t)
    return pending, aqn


def read_echo(net):
    if net.offline:
        j = net.json("", "echo_qid.json")
        return (j or {}).get("Results", {}).get("Facilities", [])
    q = net.json(f"{ECHO}.get_facilities", params={"output": "JSON", "p_st": "NM", "p_sic": "4911", "responseset": "100"})
    qid = ((q or {}).get("Results") or {}).get("QueryID")
    rows = []
    for page in range(1, 30):
        if not qid:
            break
        j = net.json(f"{ECHO}.get_qid", params={"output": "JSON", "qid": qid, "pageno": page, "qcolumns": ECHO_COLS})
        fac = ((j or {}).get("Results") or {}).get("Facilities") or []
        rows += fac
        if len(fac) < 100:
            break
    return rows


def read_regs(net, cache_dir):
    """Documents of the NTEC docket [{id, title, type, posted, url, page}]. Cached a day, paced for
    the DEMO_KEY (10 calls an hour); REGULATIONS_GOV_KEY is used when set."""
    import os
    cache = cache_dir / "regs_ntec.json"
    if not net.offline and cache.exists() and time.time() - cache.stat().st_mtime < 86400:
        return json.loads(cache.read_text(encoding="utf-8"))
    key = os.environ.get("REGULATIONS_GOV_KEY") or "DEMO_KEY"
    docs, page = [], 1
    while page <= 6:
        j = net.json(f"{REGS_API}/documents", "regs_documents.json",
                     params={"filter[docketId]": REGS_DOCKET, "api_key": key, "page[size]": 250, "page[number]": page,
                             "sort": "postedDate"}, tries=1)
        if not j:
            net.errors.append("regulations.gov documents call failed (DEMO_KEY allows 10 calls an hour; set REGULATIONS_GOV_KEY)")
            break
        for d in j.get("data", []):
            a = d.get("attributes", {})
            docs.append({"id": d["id"], "title": clean_ws(a.get("title")), "type": a.get("documentType") or "",
                         "posted": iso_date(a.get("postedDate")),
                         "url": f"https://downloads.regulations.gov/{d['id']}/content.pdf",
                         "page": f"https://www.regulations.gov/document/{d['id']}"})
        if not j.get("meta", {}).get("hasNextPage") or net.offline:
            break
        page += 1
        time.sleep(medium_pause(key))
    if docs and not net.offline:
        cache_dir.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(docs), encoding="utf-8")
    return docs


def medium_pause(key):
    return 400 if key == "DEMO_KEY" else 1


# ---------------------------------------------------------------- reporting ---

def fac_block(f, how=None):
    where = ", ".join(x for x in (f["city"], f"{f['county']} County" if f["county"] else "") if x)
    L = [f"- {f['name']} ({where or 'place not shown'}; {f['source']}" + (f", AI {f['ai']}" if f["ai"] else "") + ")"]
    if f["company"]:
        L.append(f"    - organization or applicant: {f['company']}")
    if f["address"]:
        L.append(f"    - address: {f['address']}")
    if f["lat"] is not None and f["lon"] is not None:
        L.append(f"    - point: https://www.google.com/maps?q={f['lat']},{f['lon']}")
    if f.get("hint"):
        L.append(f"    - the record says: {f['hint'][:300]}")
    for p in f["permits"]:
        L.append(f"    - permit: {p['number'] or 'number not shown'}, {p['type']}, {p['status']}"
                 + (f", {p['step']}" if p["step"] else "") + (f", comments end {p['comment_ends']}" if p["comment_ends"] else ""))
    for x in f["links"]:
        L.append(f"    - page: {x['kind']}: {x['url']}")
    if f["found_by"]:
        L.append(f"    - found by: {'; '.join(f['found_by'])}")
    for d in f["docs"]:
        L.append(f"    - document ({d.get('state', 'not read')}, {d['date'] or 'date not shown'}): {d['name']}: {d['url']}")
        fa = d.get("facts") or {}
        for key, label in (("ids", "permit numbers"), ("facility", "facility"), ("project", "project"),
                           ("equipment", "equipment"), ("counts", "count"), ("makers", "maker or model"),
                           ("sizes", "size"), ("dates", "date"), ("location", "site address or location"),
                           ("coords", "coordinates")):
            for line in fa.get(key, []):
                L.append(f"        - {label}: {line}")
    if how:
        L.insert(0, f"Matched: {how}.")
    return L


def write_index(path, plant, matched, notices, extra):
    L = [f"# New Mexico air permit files for {plant['name']} ({plant['id']})", "",
         "Sources: the NMED APMAP facility record (" + APMAP_UI + ") and its public document collections on "
         "cloud.env.nm.gov, the NMED public notices page (" + NOTICES + "), the City of Albuquerque Air Quality "
         "Program pages (" + ABQ_PENDING + "), EPA Region 9 and EPA ECHO. A collection document address "
         "(cloud.env.nm.gov/resources/_translator.php/...pdf) is citable as it stands; fetch.py and url_verifier.py "
         "read it. The PDFs and their text are saved under work/permits/docs/.", "",
         f"Harvested: {time.strftime('%Y-%m-%d %H:%M %Z')}", "",
         f"GEM statuses: {', '.join(plant['statuses'])}. City in GEM: {plant['city'] or 'blank'}. "
         f"County in GEM: {plant['county'] or 'blank'}.", ""]
    if not matched:
        L += ["No permit facility matched this plant. That does not mean it has no permits: it may be filed under the "
              "owner, a contractor or another site name, or it may be only a planning entry with no site. Check "
              "_unmatched.md and _leads.md in this folder, and search APMAP by the owner's name.", ""]
    elif not any(f["docs"] for f, _ in matched):
        L += ["The matched facilities have no documents online. Older permits need a public records request to the "
              "Air Quality Bureau.", ""]
    for f, how in matched:
        L += fac_block(f, how) + [""]
    for n in notices:
        L += [f"Public notice: {n['title']} (posted {n['posted'] or 'date not shown'})"] + \
             [f"    - {x['label']}: {x['url']}" for x in n["links"][:12]] + [""]
    for e in extra:
        L += [e, ""]
    path.write_text("\n".join(L), encoding="utf-8")


def slim(f):
    """A facility as facilities.json and index.json keep it: no full document text."""
    return {"key": f["key"], "name": f["name"], "source": f["source"], "company": f["company"],
            "county": f["county"], "city": f["city"], "address": f["address"], "codes": f["codes"],
            "hint": f.get("hint", ""), "ai": f["ai"], "lat": f["lat"], "lon": f["lon"], "found_by": f["found_by"],
            "collection": f["collection"], "activities": f["activities"][:40], "links": f["links"],
            "permits": f["permits"],
            "docs": [{k: d[k] for k in ("number", "name", "type", "date", "url", "state", "file", "facts", "how", "page")
                      if k in d} for d in f["docs"]]}


# ----------------------------------------------------------------- plants ---

def load_plants(args=None, csv_path=None):
    csv = pd.read_csv(csv_path or CSV, low_memory=False, encoding="utf-8-sig")
    csv = csv[csv["State/Province"] == "New Mexico"]
    wanted = set(args.plants.split(",")) if args is not None and getattr(args, "plants", None) else None
    plants = []
    for pid, rows in csv.groupby("GEM location ID", sort=False):
        if wanted is not None and pid not in wanted:
            continue
        r = rows.iloc[0]
        city = r.get("City") if isinstance(r.get("City"), str) else ""
        county = r.get("Local area (taluk, county)")
        lat, lon = r.get("Latitude"), r.get("Longitude")
        plants.append({"id": pid, "name": r["Plant name"], "city": city,
                       "county": norm_county(county).title() if isinstance(county, str) else "",
                       "lat": float(lat) if pd.notna(lat) else None, "lon": float(lon) if pd.notna(lon) else None,
                       "statuses": sorted(set(rows["Status"].astype(str))),
                       "name_words": words(r["Plant name"])})
    return plants


def wildcard_names(net, query):
    j = net.json(APMAP + "get-facility-name-wildcards", f"name_wildcards_{slug(query)}.json", params={"facility": query}, quiet=True)
    return [str(x).strip().upper() for x in (j or []) if isinstance(x, str)]


# ------------------------------------------------------------------- main ---

def main():
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n\n")[0])
    ap.add_argument("--scope", required=True, help="batch folder name, e.g. us-nm")
    ap.add_argument("--plants", help="comma-separated GEM location IDs (default: every plant); reads only their "
                    "facilities' documents and skips the sweep")
    ap.add_argument("--leads", default="all", help="comma-separated lead keys, 'all' or 'none'")
    ap.add_argument("--match-only", action="store_true", help="list matches only, no document reads")
    ap.add_argument("--no-sweep", action="store_true", help="skip the unmatched power-like sweep")
    ap.add_argument("--no-notices", action="store_true")
    ap.add_argument("--no-coda", action="store_true")
    ap.add_argument("--no-abq", action="store_true")
    ap.add_argument("--no-epa", action="store_true", help="skip the NTEC docket and the ECHO list")
    ap.add_argument("--offline", action="store_true", help="read the saved sample pages in tests/fixtures/harvest_nm/, no network")
    ap.add_argument("--fixtures", help="another folder of saved sample pages")
    ap.add_argument("--docs-per-facility", type=int, default=15)
    ap.add_argument("--sweep-read", type=int, default=60, help="list the document collection of this many unmatched facilities")
    ap.add_argument("--popups", type=int, default=80, help="most APMAP popups read for unmatched power-like facilities")
    ap.add_argument("--pages", type=int, default=None, help="read only the first pages of each document")
    args = ap.parse_args()

    out_dir = harvest_out(args.scope)
    hv_dir = REPO / "batches" / args.scope / "harvest"
    hv_dir.mkdir(parents=True, exist_ok=True)
    plants = load_plants(args)
    stamp = time.strftime("%Y-%m-%d")
    net = Net(args.offline, args.fixtures)
    key = cloud_key(net)
    leads = [] if args.leads == "none" else [x for x in LEADS if args.leads == "all" or x["key"] in args.leads.split(",")]

    # 1. APMAP facilities
    rows = net.json(APMAP + "get-facility-locations", "apmap_locations.json", timeout=300)
    if rows is None:
        log("APMAP facility list failed; see the errors in harvest_summary.md")
    facs = parse_locations(rows)
    log(f"APMAP: {len(facs)} facilities")
    by_name = {}
    for f in facs.values():
        by_name.setdefault(f["name"].strip().upper(), []).append(f)

    # name searches add facilities whose names the plant and lead patterns do not already reach
    queries = {}
    for p in plants:
        w = sorted(p["name_words"], key=len, reverse=True)[:1]
        for q in w:
            queries.setdefault(q, []).append(p["id"])
    for ld in leads:
        for q in ld["queries"]:
            queries.setdefault(q, []).append(ld["key"])
    wild = {}
    for q in queries:
        for nm in wildcard_names(net, q):
            for f in by_name.get(nm, []):
                wild.setdefault(f["key"], set()).add(q)
    for k, qs in wild.items():
        facs[k]["found_by"].append("APMAP name search for " + ", ".join(sorted(qs)))

    # popups for facilities a pattern or name search reaches (organization and permit numbers)
    def reached(f):
        t = fac_text(f)
        return f["key"] in wild or any(re.search(p, t) for k in KNOWN.values() for p in k["names"]) \
            or any(re.search(p, t) for ld in leads for p in ld["names"]) \
            or any(f["ai"] in k.get("ai", []) for k in KNOWN.values())
    popped = set()

    def popup(f):
        if f["key"] in popped or not f["ai"]:
            return
        popped.add(f["key"])
        r = net.req(APMAP + "get-facility-popup", f"popup_{f['ai']}.html", params={"ai": f["ai"]}, quiet=True)
        if r is not None:
            apply_popup(f, parse_popup(r.text))

    near = [f for f in facs.values() if any(
        p.get("lat") is not None and f["lat"] is not None and (distance_m(p["lat"], p["lon"], f["lat"], f["lon"]) or 1e9) <= DIST_KM * 1000
        for p in plants)]
    for f in list(facs.values()):
        if reached(f) or f in near:
            popup(f)

    # other lists
    notices = []
    if not args.no_notices:
        got = read_notices(net)
        if got is None:
            report_failure(NOTICES, "000", "NMED notices page")
        notices = got or []
        facs.update(notice_facilities(notices))
        log(f"NMED notices: {len(notices)} blocks, {sum(1 for n in notices if n['air'])} Air Quality Bureau")
    coda, coda_problems = ({}, [])
    if not args.no_coda and not args.plants:
        coda, coda_problems = read_coda(net)
        for tname, trows in coda.items():
            facs.update(coda_facilities(tname, trows))
    pending, aqn = ([], [])
    if not args.no_abq and not args.plants:
        pending, aqn = read_abq(net)
        facs.update(abq_facilities(pending, aqn))
        log(f"Albuquerque: {len(pending)} pending applications, {len(aqn)} notification records")
    regs, echo = [], []
    if not args.no_epa and not args.plants:
        regs = read_regs(net, out_dir / "regs")
        if regs:
            facs["epa-ntec-docket"] = regs_facility(regs)
        echo = read_echo(net)
        facs.update(echo_facilities(echo))
        log(f"EPA: {len(regs)} NTEC docket documents, {len(echo)} ECHO electric facilities")

    allf = list(facs.values())
    matches = {p["id"]: match(p, allf) for p in plants}
    lead_hits = {ld["key"]: match_lead(ld, allf) for ld in leads}
    matched_keys = {f["key"] for ms in matches.values() for f, _ in ms} | {f["key"] for v in lead_hits.values() for f in v}
    power = [f for f in allf if f["key"] in matched_keys or (is_power(f) and f["source"] != "NMED APMAP")]
    apmap_unmatched = [f for f in allf if f["source"] == "NMED APMAP" and f["key"] not in matched_keys and is_power(f)]
    for f in sorted(apmap_unmatched, key=lambda x: -(x["ai"] or 0))[:args.popups] if not args.plants and not args.no_sweep else []:
        popup(f)
    power += apmap_unmatched

    if args.match_only:
        for p in plants:
            for f, how in matches[p["id"]] or [(new_fac("", "no match", ""), "")]:
                print(f"{p['id']}\t{p['name']}\t{f['name']}\t{f['key']}\t{how}")
        for ld in leads:
            for f in lead_hits[ld["key"]] or [new_fac("", "no match", "")]:
                print(f"LEAD {ld['key']}\t{ld['name']}\t{f['name']}\t{f['key']}")
        for f in power:
            if f["key"] not in matched_keys:
                print(f"UNMATCHED\t\t{f['name']}\t{f['key']}\t{f['city']}\t{f['county']}")
        return

    # 2. documents for every matched facility
    for k, f in enumerate([x for x in power if x["key"] in matched_keys], 1):
        if f["ai"] and not f["docs"]:
            for d in list_documents(net, key, f):
                f["docs"].append({**d, "how": "APMAP document collection"})
        f["docs"] = rank_docs(f["docs"])
        for n, d in enumerate(f["docs"]):
            if n >= args.docs_per_facility:
                d["state"] = "not read (cap)"
            elif "facts" not in d:
                read_doc(net, out_dir, f, d, pages=args.pages)
        log(f"({k}) {f['name']}: {min(len(f['docs']), args.docs_per_facility)} of {len(f['docs'])} documents read")

    # 4. the sweep: unmatched APMAP facilities get their collection address, the newest first
    sweep = [f for f in sorted(apmap_unmatched, key=lambda x: -(x["ai"] or 0))][:args.sweep_read] \
        if not args.plants and not args.no_sweep else []
    for f in sweep:
        if f["ai"] and not f["collection"]:
            f["collection"] = cloud_collection(net, key, f["ai"])
            if f["collection"]:
                f["links"].append({"kind": "document collection", "number": "", "url": f["collection"]})
            if SWEEP_DC.search(fac_text(f)):
                f["found_by"].append("the name or card names a data center or microgrid")
    unmatched = [f for f in power if f["key"] not in matched_keys]
    log(f"{len(facs)} facilities: {len(power)} power-like or matched, {len(matched_keys)} matched, {len(unmatched)} unmatched")

    # notices tied to plants and leads
    def notice_hits(patterns):
        return [n for n in notices if n["air"] and any(re.search(p, (n["title"] + " " + n["text"]).lower()) for p in patterns)]

    with (out_dir / "harvest_log.jsonl").open("a", encoding="utf-8") as logf:
        for p in plants:
            k = KNOWN.get(p["id"]) or {"names": []}
            nh = notice_hits(k["names"]) if k["names"] else []
            extra = []
            if p["id"] == "L100001043002":
                extra.append(f"EPA Region 9 docket {REGS_DOCKET}: {len(regs)} documents listed in _epa.md (the draft is a synthetic minor "
                             "permit for 742 MW from 18 LM6000 turbines; GEM has 18 units at 60.5 MW).")
            write_index(out_dir / f"{p['id']}.md", p, matches[p["id"]], nh, extra)
            (out_dir / f"{p['id']}.json").write_text(json.dumps(
                {"plant": {k2: p[k2] for k2 in ("id", "name", "city", "county", "statuses", "lat", "lon")},
                 "facilities": [{**slim(f), "how": how} for f, how in matches[p["id"]]],
                 "notices": nh}, indent=1), encoding="utf-8")
            logf.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "plant": p["id"], "name": p["name"],
                                   "facilities": [{"name": f["name"], "key": f["key"], "how": how,
                                                   "docs": {d["name"]: d.get("state", "not read") for d in f["docs"]}}
                                                  for f, how in matches[p["id"]]]}) + "\n")

    L = ["# New Mexico leads: projects GEM lacks or knows under another name", "",
         "Each lead is searched in APMAP by name and in the notices and lists. No hit does not mean no permit: the "
         "permit may be filed under a developer, a contractor or an LLC; search the owner's name in APMAP and "
         "check the PRC and county records.", ""]
    for ld in leads:
        hits = lead_hits[ld["key"]]
        L += [f"## {ld['name']}", ""]
        L += [x for f in hits for x in fac_block(f)] if hits else ["No facility, notice or list entry matched."]
        for n in notice_hits(ld["names"]):
            L.append(f"- Public notice: {n['title']} (posted {n['posted'] or 'date not shown'})")
        L.append("")
    (out_dir / "_leads.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    L = ["# New Mexico facilities that look like power or data center sites but match no GEM plant or lead", "",
         "Each may be a plant outside this batch, a plant GEM lacks, a backup generator fleet at a data center or another "
         "site, or not a power plant at all. Check engines or turbines of 50 MW or more in total (generating capacity "
         "only). APMAP entries list the newest first and only the first " + str(args.sweep_read) + " have their document "
         "collection address; open the facility report to see the rest.", ""]
    for f in sorted(unmatched, key=lambda f: f["name"].lower()):
        L += fac_block(f) + [""]
    if not unmatched:
        L.append("None this run.")
    (out_dir / "_unmatched.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    L = [f"# NMED public notices read {stamp}", "", f"{len(notices)} blocks, {sum(1 for n in notices if n['air'])} from the Air Quality Bureau. Source: {NOTICES}", ""]
    for n in notices:
        if n["air"]:
            L += [f"- {n['title']} (posted {n['posted'] or 'date not shown'}"
                  + (f", comments {n['comment'][0]} to {n['comment'][1]}" if n["comment"] else "") + ")"]
            L += [f"    - {x['label']}: {x['url']}" for x in n["links"][:10]]
    (out_dir / "_notices.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    L = [f"# NMED Coda tables {stamp}", "", f"Found from {AQB_PAGE}", ""]
    for d in CODA_DOCS:
        L.append(f"- {d['name']}: {d['url']} ({len(coda.get(d['name'], []))} rows read)")
    L += [""] + [f"- Not read: {p}" for p in coda_problems]
    for tname, trows in coda.items():
        L += ["", f"## {tname}", ""] + [f"- {' | '.join(str(v) for v in r.values() if v not in (None, ''))[:300]}" for r in trows
                                       if is_power({"name": next(iter(r.values()), ""), "company": "", "hint": " ".join(map(str, r.values()))})]
    (out_dir / "_coda.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    L = [f"# Albuquerque air quality {stamp}", "", f"Pending applications ({ABQ_PENDING}): {len(pending)}. Monthly notification report ({ABQ_AQN}): {len(aqn)} records.", ""]
    L += [f"- Application {p['application']}, {p['name']}: {p['description']} {p['url']}" for p in pending]
    L += [""] + [f"- {r['record']} {r['facility']} ({r['company']}), issued {r['issued']}: {r['text']}" for r in aqn
                 if is_power({"name": r["facility"], "company": r["company"], "hint": r["text"]})
                 or re.search(r"engine|generator|turbine|data ?cent", r["text"], re.I)]
    (out_dir / "_albuquerque.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    L = [f"# EPA records {stamp}", "", f"## NTEC docket {REGS_DOCKET}", ""]
    L += [f"- {d['posted']} {d['type']}: {d['title']} ({d['page']}; file {d['url']})" for d in regs] or ["No documents listed."]
    L += ["", "## EPA ECHO electric facilities in New Mexico (SIC 4911), a cross-check list", ""]
    L += [f"- {r.get('AIRName')} ({r.get('AIRCity')}, {r.get('AIRCounty')}; source {r.get('SourceID')})" for r in echo
          if "PORTABLE" not in str(r.get("AIRStreet") or "").upper()]
    (out_dir / "_epa.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    index = {"harvested": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "apmap_facilities": sum(1 for f in allf if f["source"] == "NMED APMAP"),
             "notices": len(notices), "coda_tables": {k: len(v) for k, v in coda.items()}, "coda_problems": coda_problems,
             "abq_pending": len(pending), "abq_aqn": len(aqn), "epa_docket_documents": len(regs), "echo_facilities": len(echo),
             "plants": {p["id"]: {"name": p["name"], "facilities": [{"key": f["key"], "name": f["name"], "how": how}
                                                                    for f, how in matches[p["id"]]]} for p in plants},
             "leads": {ld["key"]: [f["key"] for f in lead_hits[ld["key"]]] for ld in leads},
             "unmatched": [f["key"] for f in unmatched],
             "facilities": {f["key"]: slim(f) for f in power},
             "errors": net.errors}
    (out_dir / "index.json").write_text(json.dumps(index, indent=1), encoding="utf-8")
    (hv_dir / "facilities.json").write_text(json.dumps({
        "harvested": index["harvested"], "matches": index["plants"], "leads": index["leads"],
        "unmatched": [slim(f) for f in unmatched],
        "matched": [slim(f) for f in power if f["key"] in matched_keys]}, indent=1), encoding="utf-8")

    S = [f"# New Mexico air permit harvest, {stamp}", "",
         f"APMAP facilities: {index['apmap_facilities']}. NMED notices: {len(notices)} blocks. Coda tables read: "
         f"{len(coda)} of {len(CODA_DOCS)}. Albuquerque: {len(pending)} pending, {len(aqn)} notification records. EPA: "
         f"{len(regs)} NTEC docket documents, {len(echo)} ECHO facilities. Power-like: {len(power)}. Matched: "
         f"{len(matched_keys)}. Unmatched: {len(unmatched)}.", "", f"Calls: {net.calls}.", ""]
    if net.errors:
        S += ["Calls that failed (retry before concluding anything):", ""] + [f"- {e}" for e in net.errors[:40]] + [""]
    if coda_problems:
        S += ["Coda tables not read:", ""] + [f"- {p}" for p in coda_problems] + [""]
    S += ["## Matches per GEM plant", ""]
    for p in plants:
        ms = matches[p["id"]]
        S.append(f"- {p['name']} ({p['id']}): " + ("; ".join(f"{f['name']} ({f['key']}, {how})" for f, how in ms)
                                                   if ms else "no facility matched"))
    S += ["", "## Leads", ""]
    for ld in leads:
        S.append(f"- {ld['name']}: " + ("; ".join(f"{f['name']} ({f['key']})" for f in lead_hits[ld['key']]) or "nothing matched"))
    S += ["", "## Unmatched power-like facilities", ""]
    S += [f"- {f['name']} ({f['city'] or '?'}, {f['county'] or '?'} County; {f['source']})"
          for f in sorted(unmatched, key=lambda f: f["name"].lower())]
    (hv_dir / "harvest_summary.md").write_text("\n".join(S) + "\n", encoding="utf-8")
    log("done")


if __name__ == "__main__":
    main()

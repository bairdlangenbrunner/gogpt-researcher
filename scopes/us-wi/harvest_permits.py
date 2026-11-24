"""
Harvest Wisconsin air permits before a research sweep.

Wisconsin's Department of Natural Resources (DNR) keeps one public record of every air permit, the
Air Management permit tracking ("WARP") system at https://apps.dnr.wi.gov/warp_ext/. Every page below
answers without a sign-in to plain requests with a browser User-Agent. What was found (2026-11-17):

  1. WARP search, AM_PermitTrackingSearch.aspx. An ASP.NET form. GET it, then POST every input by
     name with the button ctl00$ContentPlaceHolder1$btnSearch. Fields: txtFid, txtFacName, txtSic,
     txtNaics, txtAddress, txtPermit, ddlCounty, and chkInactive=on (include inactive facilities).
     The grp* radios choose starts with, contains or exact (rdbFid1/2/3 and so on). SIC 4911 with
     inactive on returns 141 facilities. The result table (gvResult) lists FID, name, address, city
     and county. One hit redirects to the facility page.
  2. The facility page, AM_PermitTracking2.aspx?id=<n>. THE id IS NOT THE FID. It is the DNR's own
     sequence number, and id=<FID> answers HTTP 500. Reach a facility by searching its FID (exact).
     The page shows address, SIC and NAICS codes, a site description and the permit grid (gvPermits).
     The grid hides inactive permits (withdrawn or expired) until a postback with
     __EVENTTARGET=ctl00$ContentPlaceHolder1$chkInactive and chkInactive=on. Keep chkInactive=on on
     every later POST. A withdrawn construction permit is still a record of a project.
  3. Documents. POST __EVENTTARGET=...$gvPermits, __EVENTARGUMENT=Select$N lists that permit's
     documents (gvDocuments); POST ...$gvDocuments, Select$N reveals one link,
     AM_DownloadObject.aspx?id=<doc id>. That link needs no session: a plain GET downloads the PDF
     (HEAD answers 500), and the address is stable, so it is the citation. Some files are .docx;
     old scans need OCR.
  4. DNR notice feeds, each with the whole list as JSON in a script variable (pubstring):
     public_notice.aspx (live public notices with the notice PDF's document id),
     apps_received.aspx (applications received, last 180 days) and final_permit_decisions.aspx.
     Each row has AM_FACILITY_SEQ_NO, so a notice facility opens directly with ?id=<seq>.
  5. EPA ECHO lists the state's electric facilities (SIC 4911) as a cross-check. EPA's RACT/BACT/
     LAER Clearinghouse (RBLC) moved: cfpub.epa.gov/rblc/ answers 404. The current app is
     https://cdxoarapps.epa.gov/oar-rblc/ and its open JSON service answers
     POST /oar-rblc/api/rblc/keyword-search with {"keywords": "turbine", "state": "WI"}. Other
     filter names are ignored (they return all 1,542 records). No sign-in, no human wall.

Steps:
  1. Run the WARP lists (SIC 4911, NAICS 2211, SIC 7374, NAICS 518210, data center and developer
     names, and one search per GEM plant that has no known FID) and read the three notice feeds.
  2. Match each GEM plant and each lead (hand-checked FIDs and name patterns, then name words and
     county) to facilities.
  3. For each matched facility: open it by FID (or by sequence number for a notice facility), turn on
     inactive permits, list every permit, list each permit's documents, download the newest
     --docs-per-facility documents (permits, analyses and applications first) into
     scopes/us-wi/work/permits/docs/<FID>/, extract the text (pdftotext -layout, python-docx for
     .docx, tesseract for scans) and keep permit numbers, equipment counts, makers, sizes, dates and
     the site.
  4. The sweep: power-like facilities that match no plant or lead go to _unmatched.md.

Output, in scopes/us-wi/work/permits/ (what the sweep agents read): <GEM location id>.md and .json
per plant, _leads.md, _unmatched.md, _notices.md, _epa.md, _rblc.md, index.json and harvest_log.jsonl.
A summary and facilities.json (the file data_center_fleets.py reads) go to batches/<scope>/harvest/.
Permit documents and their text stay under work/ (never committed). Contact names and emails on the
facility pages and notice rows are not copied. Nothing here stages a record.

Usage (from the repo root):
    python scopes/us-wi/harvest_permits.py --scope us-wi                         # everything
    python scopes/us-wi/harvest_permits.py --scope us-wi --plants L100001047775  # one plant
    python scopes/us-wi/harvest_permits.py --scope us-wi --match-only            # list matches only
    python scopes/us-wi/harvest_permits.py --scope us-wi --offline               # saved sample pages
"""
import argparse
import html
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from fetch import CHROME_UA  # noqa: E402
from harvest_lib import (CSV, REPO, SIZE, clean_ws, harvest_out, norm_county, pick, report_failure,  # noqa: E402
                         wayback_url)

WARP = "https://apps.dnr.wi.gov/warp_ext/"
SEARCH_PAGE = WARP + "AM_PermitTrackingSearch.aspx"
FACILITY_PAGE = WARP + "AM_PermitTracking2.aspx"
DOWNLOAD = WARP + "AM_DownloadObject.aspx?id="
FEEDS = {"public notice": WARP + "public_notice.aspx",
         "application received": WARP + "apps_received.aspx",
         "final decision": WARP + "final_permit_decisions.aspx"}
CP = "ctl00$ContentPlaceHolder1$"
ECHO = "https://echodata.epa.gov/echo/air_rest_services"
ECHO_COLS = "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21"
RBLC = "https://cdxoarapps.epa.gov/oar-rblc/"
RBLC_API = RBLC + "api/rblc/keyword-search"
RBLC_KEYWORDS = ["turbine", "engine", "generator", "combustion", "boiler"]
FIXTURES = REPO / "tests" / "fixtures" / "harvest_wi"

# Hand-checked per GEM plant. "fid" are WARP facility IDs (proven from the plan's probe, 2026-11-17).
# "names" are lower-case regular expressions tried on a facility's name and description. "q" is a
# WARP name search ("contains") for a plant with no known FID.
KNOWN = {
    "L100000402376": {"fid": [], "names": [r"\bneenah\b"], "q": "Neenah"},
    "L100000104267": {"fid": [], "names": [r"blount"], "q": "Blount"},
    "L100000402527": {"fid": [], "names": [r"combined locks"], "q": "Combined Locks"},
    "L100000402372": {"fid": [], "names": [r"\bconcord\b"], "q": "Concord"},
    "L100000402378": {"fid": [], "names": [r"de pere"], "q": "De Pere"},
    "L100000409212": {"fid": [], "names": [r"madison gas.*(diesel|generat)", r"mge.*diesel"], "q": "Madison Gas"},
    "L100000104269": {"fid": [], "names": [r"edgewater"], "q": "Edgewater"},
    "L100000104274": {"fid": [], "names": [r"elm road"], "q": "Elm Road"},
    "L100001083378": {"fid": [], "names": [r"forest junction"], "q": "Forest Junction"},
    "L100001047813": {"fid": [265200320, 265200430], "names": [r"foundry ridge"], "q": "Foundry Ridge"},
    "L100001089648": {"fid": [], "names": [r"fox north"], "q": "Fox North"},
    "L100000402379": {"fid": [], "names": [r"fox energy"], "q": "Fox Energy"},
    "L100000409271": {"fid": [], "names": [r"french island"], "q": "French Island"},
    "L100000402373": {"fid": [], "names": [r"germantown"], "q": "Germantown"},
    "L100000402388": {"fid": [], "names": [r"island street"], "q": "Island Street"},
    "L100000401676": {"fid": [], "names": [r"whitewater"], "q": "Whitewater"},
    "L100000401798": {"fid": [], "names": [r"marshfield"], "q": "Marshfield"},
    "L100001089674": {"fid": [252302490], "names": [r"microsoft", r"mount pleasant.*data", r"\bdmm\b"], "q": "Microsoft"},
    "L100000407359": {"fid": [], "names": [r"nemadji"], "q": "Nemadji"},
    "L100000402374": {"fid": [230094810], "names": [r"paris (gen|power|station)"], "q": "Paris"},
    "L100001047775": {"fid": [252304470], "names": [r"paris rice"], "q": "Paris"},
    "L100000104693": {"fid": [246004000], "names": [r"port washington"], "q": "Port Washington"},
    "L100000104276": {"fid": [], "names": [r"pulliam"], "q": "Pulliam"},
    "L100001062057": {"fid": [], "names": [r"red oak ridge"], "q": "Red Oak"},
    "L100000401640": {"fid": [13490124], "names": [r"riverside (energy|gen|power)"], "q": "Riverside"},
    "L100000402377": {"fid": [], "names": [r"rock river"], "q": "Rock River"},
    "L100000402253": {"fid": [], "names": [r"rockgen"], "q": "RockGen"},
    "L100000401635": {"fid": [], "names": [r"sheboygan falls"], "q": "Sheboygan Falls"},
    "L100000401636": {"fid": [], "names": [r"south fond du lac"], "q": "Fond du Lac"},
    "L100001025603": {"fid": [241007690, 241219440], "names": [r"oak creek"], "q": "Oak Creek"},
    "L100001089647": {"fid": [], "names": [r"union depot"], "q": "Union Depot"},
    "L100000104279": {"fid": [], "names": [r"valley (power|plant|gen)"], "q": "Valley Power"},
    "L100001089699": {"fid": [246185280], "names": [r"vantage"], "q": "Vantage"},
    "L100000401577": {"fid": [], "names": [r"west campus"], "q": "West Campus"},
    "L100000402073": {"fid": [], "names": [r"west marinette"], "q": "West Marinette"},
    "L100000402381": {"fid": [], "names": [r"west marinette"], "q": "West Marinette"},
    "L100000104280": {"fid": [737009020], "names": [r"\bweston\b"], "q": "Weston"},
    "L100000409253": {"fid": [737009020], "names": [r"\bweston\b"], "q": "Weston"},
    "L100000409233": {"fid": [], "names": [r"wheaton"], "q": "Wheaton"},
}

# Leads: projects GEM lacks or knows under another name. "q" go to the WARP name search.
LEADS = [
    {"key": "fitchburg", "name": "Fitchburg (Madison Gas and Electric)", "q": ["Fitchburg"],
     "names": [r"fitchburg.*(power|energy|gener|mge)", r"madison gas.*fitchburg"], "fid": []},
    {"key": "elk-mound", "name": "Elk Mound (Dairyland Power)", "q": ["Elk Mound"],
     "names": [r"elk mound", r"dairyland"], "fid": [13798522]},
    {"key": "meta-beaver-dam", "name": "Meta Beaver Dam data center", "q": ["Meta", "Beaver Dam"],
     "names": [r"\bmeta\b", r"beaver dam.*data", r"facebook"], "fid": []},
    {"key": "microsoft-kenosha", "name": "Microsoft Kenosha and Caledonia", "q": ["Microsoft", "Caledonia"],
     "names": [r"microsoft", r"caledonia.*data"], "fid": []},
    {"key": "qts", "name": "QTS data center", "q": ["QTS"], "names": [r"\bqts\b"], "fid": []},
    {"key": "cloverleaf", "name": "Cloverleaf data center", "q": ["Cloverleaf"], "names": [r"cloverleaf"], "fid": []},
    {"key": "greater-kudu", "name": "Greater Kudu", "q": ["Kudu"], "names": [r"kudu"], "fid": []},
    {"key": "oracle", "name": "Oracle data center", "q": ["Oracle"], "names": [r"oracle"], "fid": []},
    {"key": "vantage", "name": "Vantage data centers", "q": ["Vantage"], "names": [r"vantage"], "fid": [246185280]},
    {"key": "port-washington-ce", "name": "Port Washington 6630-CE-318", "q": ["Port Washington"],
     "names": [r"port washington"], "fid": [246004000]},
    {"key": "concord-ce", "name": "Concord 6630-CE-315", "q": ["Concord"], "names": [r"\bconcord\b"], "fid": []},
    {"key": "forest-union", "name": "Forest Junction and Union Depot", "q": ["Forest Junction", "Union Depot"],
     "names": [r"forest junction", r"union depot"], "fid": []},
    {"key": "fox-north", "name": "Fox North", "q": ["Fox North"], "names": [r"fox north"], "fid": []},
    {"key": "red-oak-ridge", "name": "Red Oak Ridge", "q": ["Red Oak"], "names": [r"red oak ridge"], "fid": []},
    {"key": "foundry-ridge", "name": "Foundry Ridge", "q": ["Foundry Ridge"], "names": [r"foundry ridge"], "fid": [265200320, 265200430]},
    {"key": "nemadji", "name": "Nemadji Trail", "q": ["Nemadji"], "names": [r"nemadji"], "fid": []},
]

# Lists that are searched whole: (label, field, value, mode). Mode is starts, contains or exact.
LISTS = [("sic4911", "sic", "4911", "starts"), ("naics2211", "naics", "2211", "starts"),
         ("sic7374", "sic", "7374", "starts"), ("naics518210", "naics", "518210", "starts")]
CODES = {"sic4911": "SIC 4911", "naics2211": "NAICS 2211", "sic7374": "SIC 7374", "naics518210": "NAICS 518210"}
DC_QUERIES = ["Microsoft", "Vantage", "Meta", "Kudu", "QTS", "Cloverleaf", "Oracle", "Data", "Google", "Amazon", "Compute"]

POWER_NAME = re.compile(
    r"power|generat|energy|data ?cent|datacent|micro ?grid|turbine|engine|electric|cogen|peaking|\brice\b|"
    r"combined cycle|hyperscal|bitcoin|crypto|computing|compute|\bqts\b|microsoft|vantage|\bmeta\b|google|"
    r"amazon|oracle|cloverleaf|kudu|utilit|light|\bwe energies\b|alliant|\bwpl\b|\bwps\b|dairyland|invenergy|"
    r"\bmge\b|wppi", re.I)
POWER_DROP = re.compile(
    r"paper|ethanol|dairy|cheese|quarry|sand|gravel|asphalt|landfill|school|hospital|compressor station|"
    r"plating|foundry corp|brewery|hotel|church|clinic|nursing|bakery|packaging|plastics|cranberr|meat|"
    r"lumber|sawmill|truck|trucking|crushing|concrete|printing|milling|mill\b|veneer|furniture", re.I)
NAME_NOISE = re.compile(
    r"\b(power station|power plant|generating station|generating|generation|facility|station|energy center|"
    r"energy|plant|power|wi|wisconsin|the|of|and|llc|inc|company|co|corp|corporation|combined|cycle|county|"
    r"center|data|east|west|gen|we|alliant|wpl|wps|rice)\b", re.I)
EQUIPMENT = re.compile(r"turbine|\bct\b|engine|rice\b|generat|\bgen\b|boiler|duct burner|hrsg|combined cycle|"
                       r"simple cycle|peaking|diesel|reciprocating|genset|microgrid|fuel cell", re.I)
MAKER = re.compile(r"model\b|caterpillar|cat g|wartsila|w[äa]rtsil[äa]|jenbacher|general electric|\bGE\b|siemens|"
                   r"solar turbines|mitsubishi|cummins|rolls[- ]royce|mtu\b|kohler|generac|waukesha|pratt|ansaldo|"
                   r"baker hughes|hitachi|bloom|titan \d|taurus|mars \d|lm ?\d{4}|7ea|7fa|7ha|6b\b|f-?class|h-?class",
                   re.I)
LOCATION = re.compile(
    r"latitude|longitude|\blat\b|\blong\b|\bUTM\b|located (at|in|on|near|approximately)|physical address|"
    r"site address|facility address|street address|county,? wisconsin|\bWI 5[34][0-9]{3}\b", re.I)
PROJECT = re.compile(r"proposes|propose to|will consist|project (is|will|consists)|construction of|to construct|"
                     r"new (electric|power|generat)|install(ation)? of|modification", re.I)
FACILITY_LINE = re.compile(r"facility( name)?:|company( name)?:|applicant:|source name|permittee|\bre:|"
                           r"permit (no|number)|\bFID\b|county,? wisconsin|operator", re.I)
DATES = re.compile(r"(issued|effective|expir|received|startup|start-up|commence|completion|deadline|due)\b.{0,60}"
                   r"(\d{1,2}/\d{1,2}/\d{2,4}|(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.? \d{1,2},? \d{4})",
                   re.I)
COUNT = re.compile(r"\b(\d{1,3}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|sixteen|eighteen|"
                   r"twenty)\s+(?:[A-Za-z\-]+\s+){0,3}(engines?|turbines?|generators?|gensets?|units?)\b", re.I)
LATLON = re.compile(r"\b(4[2-7]\.\d{3,})[\s,;/°N-]{1,12}(8[6-9]\.\d{3,}|9[0-3]\.\d{3,})\b")
PERMIT_NO = re.compile(r"\b(?:\d{2}-[A-Z]{3}-\d{2,4}(?:-R\d)?|\d{8}[A-Z]-[A-Z]\d{2}|\d{2}-DMM-\d{2,4}|PSD-[A-Z]{2}-\d+)\b")
READ_FIRST = re.compile(r"permit|analysis|preliminary|determination|application|technical|review|draft|final|"
                        r"statement|evaluation|summary", re.I)
LOW_VALUE = re.compile(r"request_to_withdraw|public_comments|public_notice|hearing|transmittal|letter|cover", re.I)
SWEEP_DC = re.compile(r"data ?cent|datacent|hyperscal|cryptocurrenc|bitcoin|blockchain|colocation|microgrid", re.I)
FILE_DATE = re.compile(r"(20\d{2})-(\d{2})-(\d{2})")


def log(msg):
    print(f"[harvest-wi] {msg}", file=sys.stderr, flush=True)


def words(text):
    t = NAME_NOISE.sub(" ", re.sub(r"\(.*?\)", " ", str(text or "")))
    return {w.lower() for w in re.split(r"[^A-Za-z]+", t) if len(w) >= 4}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s or "").lower()).strip("-")[:60] or "x"


def iso_date(s):
    """'10/07/2026' or '2026-10-07T..' to 2026-10-07, or ''."""
    s = str(s or "")
    m = re.match(r"(\d{4}-\d{2}-\d{2})", s)
    if m:
        return m.group(1)
    m = re.search(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b", s)
    return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}" if m else ""


def text_of(s):
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
        return p.read_text(encoding="utf-8") if name and p.exists() else None

    def _fake(self, txt):
        return type("Fixture", (), {"status_code": 200, "text": txt, "content": txt.encode("utf-8"), "url": "",
                                    "headers": {}, "json": lambda self_: json.loads(txt)})()

    def req(self, url, fixture=None, method="GET", data=None, json_body=None, params=None, timeout=120, tries=3,
            quiet=False, ok404=False):
        """The response (or a fixture stand-in), or None."""
        if self.offline:
            txt = self.fixture(fixture)
            return self._fake(txt) if txt is not None else None
        err = ""
        for attempt in range(tries):
            self.calls += 1
            try:
                r = self.s.request(method, url, data=data, json=json_body, params=params, timeout=timeout)
                if r.status_code == 200:
                    return r
                err = str(r.status_code)
                if r.status_code in (401, 403, 404, 429) and attempt >= 1:
                    break
            except requests.RequestException as e:
                err = "000 " + str(e)[:100]
            time.sleep(2 * (attempt + 1))
        self.errors.append(f"{method} {url}: {err}")
        if not quiet:
            report_failure(url, err.split()[0] if err else "000", "harvester call failed")
        return None

    def json(self, url, fixture=None, **kw):
        r = self.req(url, fixture, **kw)
        try:
            return r.json() if r is not None else None
        except ValueError:
            self.errors.append(f"{url}: not JSON")
            return None


# --------------------------------------------------------------- WARP pages ---

def hidden_fields(h):
    """The ASP.NET state fields (__VIEWSTATE and the rest) of a page."""
    d = {}
    for m in re.finditer(r"<input[^>]*>", h):
        t = m.group(0)
        n = re.search(r'name="(__[^"]+)"', t)
        if n:
            v = re.search(r'value="([^"]*)"', t)
            d[n.group(1)] = html.unescape(v.group(1)) if v else ""
    return d


def form_fields(h):
    """Every input a browser would send: text and hidden values, the checked radio of each group, the
    selected option of each select. Checkboxes, buttons and submit inputs are left out."""
    d = {}
    for m in re.finditer(r"<input[^>]*>", h):
        t = m.group(0)
        n = re.search(r'name="([^"]+)"', t)
        if not n:
            continue
        ty = (re.search(r'type="([^"]+)"', t) or [0, "text"])[1].lower()
        v = html.unescape((re.search(r'value="([^"]*)"', t) or [0, ""])[1])
        if ty in ("checkbox", "submit", "button", "image"):
            continue
        if ty == "radio":
            if "checked" in t:
                d[n.group(1)] = v
            continue
        d[n.group(1)] = v
    for m in re.finditer(r'<select[^>]*name="([^"]+)"[^>]*>(.*?)</select>', h, re.S):
        o = re.search(r'<option selected="selected" value="([^"]*)"', m.group(2)) \
            or re.search(r"<option[^>]*value=\"([^\"]*)\"", m.group(2))
        d[m.group(1)] = html.unescape(o.group(1)) if o else ""
    return d


def form_action(h, base=SEARCH_PAGE):
    """The address the page's form posts to, as an absolute address."""
    m = re.search(r'<form[^>]*action="([^"]*)"', h)
    a = html.unescape(m.group(1)) if m else ""
    if not a:
        return base
    return WARP + a.lstrip("./") if not a.startswith("http") else a


def grid_rows(h, grid):
    """The <tr> blocks of one grid (gvPermits, gvDocuments, gvResult), header row first."""
    m = re.search(r'<table[^>]*id="ctl00_ContentPlaceHolder1_%s"[^>]*>(.*?)</table>' % grid, h, re.S)
    return re.findall(r"<tr[^>]*>(.*?)</tr>", m.group(1), re.S) if m else []


def cells(row):
    return [text_of(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)]


def parse_results(h):
    """Search result rows: [{fid, name, address, city, county}]."""
    out = []
    for row in grid_rows(h, "gvResult")[1:]:
        g = lambda k: (re.search(r'_%s"[^>]*>([^<]*)<' % k, row) or [0, ""])[1]
        fid = clean_ws(g("lblFid"))
        if fid:
            out.append({"fid": fid, "name": clean_ws(html.unescape(g("lblName"))),
                        "address": clean_ws(html.unescape(g("lblAddress"))),
                        "city": clean_ws(html.unescape(g("lblCity"))),
                        "county": clean_ws(html.unescape(g("lblCounty"))).title()})
    return out


def parse_facility_page(h):
    """A facility page to {fid, name, seq, address, city, activity, description, sic, naics, permits}."""
    title = text_of((re.search(r'lblTitle2">(.*?)</span>', h, re.S) or [0, ""])[1])
    m = re.match(r"(\d{6,9})\s+(.*)", title)
    sel = lambda key: [text_of(o) for o in re.findall(r"<option[^>]*>(.*?)</option>",
                                                       (re.search(r'id="ctl00_ContentPlaceHolder1_%s">(.*?)</select>' % key, h, re.S) or [0, ""])[1], re.S)]
    inp = lambda key: html.unescape((re.search(r'id="ctl00_ContentPlaceHolder1_%s"[^>]*value="([^"]*)"' % key, h) or
                                     re.search(r'value="([^"]*)"[^>]*id="ctl00_ContentPlaceHolder1_%s"' % key, h) or [0, ""])[1])
    desc = text_of((re.search(r'id="ctl00_ContentPlaceHolder1_txtDescription"[^>]*>(.*?)</textarea>', h, re.S) or [0, ""])[1])
    loc = lambda n: text_of((re.search(r'lblLocation%d">(.*?)</span>' % n, h, re.S) or [0, ""])[1])
    seq = re.search(r"AM_PermitTracking2\.aspx\?id=(\d+)", h, re.I)
    return {"fid": m.group(1) if m else "", "name": clean_ws(m.group(2)) if m else title, "seq": seq.group(1) if seq else "",
            "address": loc(1), "city": loc(2), "state": loc(3),
            "activity": clean_ws(inp("txtPrimaryActivity")), "description": desc,
            "sic": sel("lstSic"), "naics": sel("lstNaics"), "permits": parse_permits(h)}


def parse_permits(h):
    """The permit grid: [{idx, number, type, received, complete, notice, decision, status}]."""
    out = []
    for row in grid_rows(h, "gvPermits")[1:]:
        i = re.search(r"Select\$(\d+)", row)
        c = cells(row)
        if i and len(c) >= 8:
            out.append({"idx": int(i.group(1)), "number": c[1], "type": c[2], "received": iso_date(c[3]),
                        "complete": iso_date(c[4]), "notice": iso_date(c[5]), "decision": iso_date(c[6]) or c[6].strip("\xa0 "),
                        "status": c[7]})
    return out


def parse_documents(h):
    """The document grid of the selected permit: [{idx, permit, name, doc_id}], doc_id only on the opened row."""
    out = []
    for row in grid_rows(h, "gvDocuments")[1:]:
        i = re.search(r"Select\$(\d+)", row)
        c = [x for x in cells(row) if x not in ("", "Select", "Dwnld")]
        d = re.search(r"AM_DownloadObject\.aspx\?id=(\d+)", row)
        if i and len(c) >= 2:
            out.append({"idx": int(i.group(1)), "permit": c[-2], "name": c[-1], "doc_id": d.group(1) if d else ""})
    return out


def parse_feed(h, kind):
    """A notice feed's pubstring JSON to [{seq, name, county, permit, date, ...}]. No contact names or emails."""
    m = re.search(r"pubstring\s*=\s*'(.*?)';", h, re.S)
    try:
        rows = json.loads(m.group(1)) if m else []
    except ValueError:
        return []
    out = []
    for r in rows:
        r = r or {}
        doc_ids = [x for x in str(r.get("DOCS_SEQNO") or "").split("***") if x.strip()]
        titles = [x for x in str(r.get("DOCS_TITLE") or "").split("***") if x.strip()]
        out.append({"kind": kind, "seq": str(r.get("AM_FACILITY_SEQ_NO") or ""), "name": clean_ws(r.get("FACILITY_NAME")),
                    "county": clean_ws(r.get("COUNTY_NAME") or r.get("COUNTY")).title(), "permit": clean_ws(r.get("PERMIT_NO")),
                    "date": iso_date(r.get("POSTING_DATE") or r.get("APP_RECEIVED") or r.get("PERMIT_ISSUED")),
                    "comment_ends": iso_date(r.get("COMMENT_DEADLINE")), "hearing": clean_ws(r.get("EVENT_DATE")),
                    "docs": [{"doc_id": i.strip(), "name": titles[n] if n < len(titles) else titles[-1] if titles else ""}
                             for n, i in enumerate(doc_ids)]})
    return out


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


def rblc_facilities(results):
    """RBLC keyword search rows to [{facility, authority, issued, processes, permit_guid}] with the process names."""
    out = {}
    for r in results or []:
        k = r.get("rblcPermitGuid") or slug(r.get("rblcFacilityName"))
        out[k] = {"facility": clean_ws(r.get("rblcFacilityName")), "authority": clean_ws(r.get("rblcPermittingAuthority")),
                  "issued": r.get("rblcPermitIssuanceDateFormatted") or "", "processes": [clean_ws(x) for x in r.get("rblcProcesses") or []][:8],
                  "permit_guid": r.get("rblcPermitGuid") or ""}
    return list(out.values())


# ---------------------------------------------------------------- facilities ---

def new_fac(key, name, source):
    return {"key": key, "name": name, "source": source, "company": "", "county": "", "city": "", "address": "",
            "fid": "", "seq": "", "codes": [], "found_by": [], "permits": [], "docs": [], "hint": "", "links": [],
            "collection": "", "ai": None, "lat": None, "lon": None, "activities": []}


def fac_text(f):
    return " | ".join(x for x in (f["name"], f["county"], f.get("hint", "")) if x).lower()


def is_power(f):
    """A power or data center look: a power-like name not on the drop list."""
    if POWER_DROP.search(f["name"]) and not SWEEP_DC.search(f["name"]):
        return False
    return bool(POWER_NAME.search(f"{f['name']} {f.get('hint', '')[:200]}")) or any(
        re.search(r"7374|518210|4911|2211", str(c)) for c in f.get("codes", [])
        if not str(c).startswith(("SIC 4911", "NAICS 2211"))) or bool(
        f.get("fid") and any(str(c) in ("SIC 4911", "NAICS 2211") for c in f.get("codes", [])))


def warp_link(f):
    return WARP + f"AM_PermitTracking2.aspx?id={f['seq']}" if f["seq"] else SEARCH_PAGE


def facility_from_row(row, label):
    f = new_fac(f"fid-{row['fid']}", row["name"], "DNR WARP")
    f.update({"fid": row["fid"], "county": row["county"], "city": row["city"], "address": row["address"]})
    f["codes"] = [CODES.get(label, label)]
    f["found_by"] = [f"WARP list {label}"]
    return f


def merge_into(facs, f):
    """Add a facility, or fold it into one with the same FID, sequence number or upper-case name."""
    for g in facs.values():
        same = (f["fid"] and f["fid"] == g["fid"]) or (f["seq"] and f["seq"] == g["seq"]) or \
               (f["name"].strip().upper() == g["name"].strip().upper() and f["name"])
        if same:
            for k in ("fid", "seq", "county", "city", "address"):
                g[k] = g[k] or f[k]
            g["codes"] = sorted(set(g["codes"]) | set(f["codes"]))
            g["found_by"] += [x for x in f["found_by"] if x not in g["found_by"]]
            g["permits"] += [p for p in f["permits"] if p not in g["permits"]]
            g["docs"] += [d for d in f["docs"] if d["url"] not in {x["url"] for x in g["docs"]}]
            g["links"] += [x for x in f["links"] if x not in g["links"]]
            return g
    facs[f["key"]] = f
    return f


def notice_facilities(items):
    facs = {}
    for it in items:
        f = new_fac(f"seq-{it['seq']}", it["name"], "DNR notice feeds")
        f["seq"], f["county"] = it["seq"], it["county"]
        f["found_by"] = [f"DNR {it['kind']} feed"]
        f["permits"].append({"number": it["permit"], "type": "", "status": it["kind"], "step": f"{it['kind']} {it['date']}".strip(),
                             "comment_ends": it["comment_ends"]})
        f["links"].append({"kind": "WARP facility page", "number": "", "url": warp_link(f)})
        for d in it["docs"]:
            f["docs"].append({"number": it["permit"], "name": d["name"] or f"notice document {d['doc_id']}", "type": "Public notice",
                              "date": it["date"], "url": DOWNLOAD + d["doc_id"], "how": f"DNR {it['kind']} feed"})
        k = f["key"]
        if k in facs:
            facs[k]["permits"] += f["permits"]
            facs[k]["docs"] += [d for d in f["docs"] if d["url"] not in {x["url"] for x in facs[k]["docs"]}]
        else:
            facs[k] = f
    return facs


def match(plant, facs):
    """[(facility, how)]: hand-checked FIDs and names, then name words plus county for a plant with no
    hand-checked entry."""
    k = KNOWN.get(plant["id"])
    out = []
    for f in facs:
        t = fac_text(f)
        if k and f["fid"] and int(f["fid"]) in k.get("fid", []):
            out.append((f, "checked by hand"))
        elif k and any(re.search(p, t) for p in k.get("names", [])):
            out.append((f, "matched by a hand-checked name, check it is this plant"))
        elif not k and plant["name_words"] and plant["name_words"] <= words(f["name"]) and is_power(f) \
                and (not plant["county"] or not f["county"] or plant["county"].lower() == f["county"].lower()):
            out.append((f, "matched by name and county, check it is this plant"))
    return out


def match_lead(lead, facs):
    return [f for f in facs if (f["fid"] and f["fid"].isdigit() and int(f["fid"]) in lead.get("fid", []))
            or any(re.search(p, fac_text(f)) for p in lead["names"])]


# ------------------------------------------------------------- WARP session ---

class Warp:
    """One browser-like session on WARP: searches, a facility page with inactive permits on, permit and
    document selections. Every call is a form POST that carries the latest hidden state."""

    def __init__(self, net, pause=0.3):
        self.net, self.pause = net, pause
        self.form_html = None

    def _post(self, url, data, fixture):
        time.sleep(0 if self.net.offline else self.pause)
        return self.net.req(url, fixture, method="POST", data=data)

    def search(self, label, mode="contains", **fields):
        """Search WARP. fields: fid, name, sic, naics, address. Returns ('facility', page, url) for a single
        hit, ('list', rows) for a result table, or ('none', None)."""
        if self.form_html is None:
            r = self.net.req(SEARCH_PAGE, "search_form.html")
            if r is None:
                return "none", None, ""
            self.form_html = r.text
        d = form_fields(self.form_html)
        grp = {"starts": "1", "contains": "2", "exact": "3"}[mode]
        for fld, rdb, radio in (("fid", "grpFid", "rdbFid"), ("name", "grpName", "rdbFacName"), ("sic", "grpSic", "rdbSic"),
                                ("naics", "grpNaics", "rdbNaics"), ("address", "grpAddress", "rdbAddress")):
            if fields.get(fld):
                d[CP + {"fid": "txtFid", "name": "txtFacName", "sic": "txtSic", "naics": "txtNaics",
                        "address": "txtAddress"}[fld]] = str(fields[fld])
                d[CP + rdb] = radio + grp
        d[CP + "chkInactive"] = "on"
        d[CP + "btnSearch"] = "Search"
        r = self._post(SEARCH_PAGE, d, f"search_{label}.html")
        if r is None:
            return "none", None, ""
        if "gvPermits" in r.text and "lblTitle2" in r.text:
            return "facility", r.text, getattr(r, "url", "") or ""
        rows = parse_results(r.text)
        return ("list", rows, "") if rows else ("none", None, "")

    def open_seq(self, seq, fixture):
        r = self.net.req(f"{FACILITY_PAGE}?id={seq}", fixture)
        return r.text if r is not None else None

    def facility_state(self, text, url):
        return {"html": text, "url": form_action(text, url or FACILITY_PAGE)}

    def _postback(self, st, target, arg, fixture):
        d = hidden_fields(st["html"])
        d["__EVENTTARGET"], d["__EVENTARGUMENT"] = target, arg
        d[CP + "chkInactive"] = "on"
        r = self._post(st["url"], d, fixture)
        if r is not None:
            st["html"] = r.text
        return r

    def inactive_on(self, st, fixture):
        d = hidden_fields(st["html"])
        d["__EVENTTARGET"], d["__EVENTARGUMENT"] = CP + "chkInactive", ""
        d[CP + "chkInactive"] = "on"
        r = self._post(st["url"], d, fixture)
        if r is not None:
            st["html"] = r.text
        return r is not None

    def select_permit(self, st, idx, fixture):
        return self._postback(st, CP + "gvPermits", f"Select${idx}", fixture) is not None

    def select_document(self, st, idx, fixture):
        """Open one document row; returns its download id or ''."""
        if self._postback(st, CP + "gvDocuments", f"Select${idx}", fixture) is None:
            return ""
        for d in parse_documents(st["html"]):
            if d["idx"] == idx and d["doc_id"]:
                return d["doc_id"]
        m = re.search(r"AM_DownloadObject\.aspx\?id=(\d+)", st["html"])
        return m.group(1) if m else ""


# ---------------------------------------------------------------- documents ---

def pdf_text(path, pages=None):
    cmd = ["pdftotext", "-layout"] + (["-l", str(pages)] if pages else []) + [str(path), "-"]
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=300).stdout
    except (subprocess.SubprocessError, OSError):
        return ""


def docx_text(path):
    try:
        import docx
        d = docx.Document(str(path))
        parts = [p.text for p in d.paragraphs]
        for t in d.tables:
            for row in t.rows:
                parts.append(" | ".join(c.text for c in row.cells))
        return "\n".join(parts)
    except Exception:  # noqa: BLE001 a damaged or odd file
        return ""


def ocr_text(path, pages=6):
    """OCR a scanned PDF (first pages): pdftoppm, then tesseract. '' when the tools are missing."""
    if not (shutil.which("pdftoppm") and shutil.which("tesseract")):
        return ""
    base = path.with_suffix("")
    try:
        subprocess.run(["pdftoppm", "-r", "200", "-l", str(pages), "-png", str(path), str(base) + "_p"],
                       capture_output=True, timeout=300)
        out = []
        for img in sorted(path.parent.glob(base.name + "_p*.png")):
            out.append(subprocess.run(["tesseract", str(img), "-", "--psm", "6"], capture_output=True, text=True,
                                      timeout=300).stdout)
            img.unlink()
        return "\n".join(out)
    except (subprocess.SubprocessError, OSError):
        return ""


def download(net, url, path):
    """Download a document. A server that answers with an HTML page falls back to the newest saved copy at
    the Wayback Machine. Returns a state sentence."""
    if net.offline:
        return "offline, not downloaded"
    r = net.req(url, timeout=300)
    state = "downloaded"
    ok = lambda x: x is not None and (x.content[:5] == b"%PDF-" or x.content[:2] == b"PK" or x.content[:4] == b"\xd0\xcf\x11\xe0")
    if not ok(r):
        if r is not None:
            report_failure(url, "200", "not a PDF or Word file")
        wb = wayback_url(url)
        r2 = net.req(wb, timeout=300, quiet=True) if wb else None
        if not ok(r2):
            return "not downloaded" if r is None else "not a document"
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


def doc_date(d):
    m = FILE_DATE.search(d.get("name", ""))
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else d.get("date", "")


def doc_path(out_dir, f, d):
    folder = f["fid"] or slug(f["key"])
    stem = slug(Path(d["name"]).stem)[:70] or f"doc-{d['doc_id']}"
    return out_dir / "docs" / folder / f"{d['doc_id']}_{stem}{Path(d['name']).suffix.lower() or '.pdf'}"


def read_doc(net, out_dir, f, d, pages=None, ocr_pages=6):
    """Download one document (kept on disk, reused next run), extract its text and keep the facts."""
    path = doc_path(out_dir, f, d)
    txt = path.with_suffix(".txt")
    state = "saved (from an earlier run)" if path.exists() else download(net, d["url"], path)
    d["file"] = str(path.relative_to(REPO)) if path.exists() else ""
    text = ""
    if path.exists():
        text = docx_text(path) if path.suffix == ".docx" else pdf_text(path, pages)
        if path.suffix != ".docx" and len(text.strip()) < 200:
            ocr = ocr_text(path, ocr_pages)
            if len(ocr.strip()) > len(text.strip()):
                text, state = ocr, state + ", read by OCR (a scan; check figures against the page)"
        txt.write_text(text, encoding="utf-8")
    d["state"] = state if text.strip() or not d["file"] else state + ", no text found (a scan or an unreadable file; open the link)"
    d["facts"] = doc_facts(text) if text.strip() else {}
    return text


def rank_docs(docs):
    """Permits, analyses and applications first, comments and letters last, newest first within each."""
    def key(d):
        n = d.get("type", "") + " " + d.get("name", "")
        return (bool(LOW_VALUE.search(n)), not READ_FIRST.search(n), "".join(chr(255 - ord(c)) for c in doc_date(d) or "0"))
    return sorted(docs, key=key)


# ---------------------------------------------------------------- one facility ---

def open_facility(w, f, tag=None):
    """Open a facility's page with inactive permits on. Returns (state, parsed) or (None, None)."""
    tag = tag or f["fid"] or f["seq"]
    if f["fid"]:
        kind, page, url = w.search(f"fid_{f['fid']}", "exact", fid=f["fid"])
        if kind != "facility":
            return None, None
        st = w.facility_state(page, url)
    elif f["seq"]:
        page = w.open_seq(f["seq"], f"facility_seq_{f['seq']}.html")
        if page is None:
            return None, None
        st = w.facility_state(page, FACILITY_PAGE + f"?id={f['seq']}")
    else:
        return None, None
    if "gvPermits" not in st["html"] or not w.inactive_on(st, f"facility_inactive_{tag}.html"):
        return None, None
    p = parse_facility_page(st["html"])
    if not p["seq"]:
        m = re.search(r"id=(\d+)", st["url"])
        p["seq"] = m.group(1) if m else f["seq"]
    return st, p


def fill_facility(f, p):
    f["fid"], f["seq"] = f["fid"] or p["fid"], f["seq"] or p["seq"]
    f["address"] = f["address"] or ", ".join(x for x in (p["address"], p["city"]) if x)
    f["city"] = f["city"] or p["city"]
    f["codes"] = sorted(set(f["codes"]) | {f"SIC {c.split()[0]}" for c in p["sic"] if c} | {f"NAICS {c.split()[0]}" for c in p["naics"] if c})
    f["hint"] = clean_ws(" ".join(x for x in (p["activity"], p["description"]) if x))[:400] or f["hint"]
    f["permits"] = [{"number": x["number"], "type": x["type"], "status": x["status"],
                     "step": ", ".join(y for y in (f"application received {x['received']}" if x["received"] else "",
                                                   f"public notice {x['notice']}" if x["notice"] else "",
                                                   f"decision {x['decision']}" if x["decision"] else "") if y),
                     "comment_ends": ""} for x in p["permits"]]
    f["links"] = [x for x in f["links"] if x["kind"] != "WARP facility page"] + [
        {"kind": "WARP facility page", "number": "", "url": warp_link(f)}]


def list_documents(w, st, p, tag):
    """Every document of every permit: [{number, name, type, date, url, permit_idx, doc_idx, doc_id}] without links yet."""
    docs = []
    for x in p["permits"]:
        if not w.select_permit(st, x["idx"], f"permit_{tag}_{x['idx']}.html"):
            continue
        for d in parse_documents(st["html"]):
            docs.append({"number": x["number"], "name": d["name"], "type": x["type"] + " " + x["status"], "date": doc_date(d) or x["decision"] or x["received"],
                         "permit_idx": x["idx"], "doc_idx": d["idx"], "doc_id": d["doc_id"], "url": DOWNLOAD + d["doc_id"] if d["doc_id"] else "",
                         "how": "WARP permit documents"})
    return docs


def reveal_links(w, st, docs, cap, tag):
    """Reveal the download address of the first `cap` ranked documents (one postback each, a permit at a time)."""
    shown = 0
    for d in rank_docs(docs):
        if d["url"] or shown >= cap:
            continue
        if not w.select_permit(st, d["permit_idx"], f"permit_{tag}_{d['permit_idx']}.html"):
            continue
        d["doc_id"] = w.select_document(st, d["doc_idx"], f"doc_{tag}_{d['permit_idx']}_{d['doc_idx']}.html")
        if d["doc_id"]:
            d["url"] = DOWNLOAD + d["doc_id"]
        shown += 1


# ---------------------------------------------------------------- reporting ---

def fac_block(f, how=None):
    where = ", ".join(x for x in (f["city"], f"{f['county']} County" if f["county"] else "") if x)
    L = [f"- {f['name']} ({where or 'place not shown'}; {f['source']}" + (f", FID {f['fid']}" if f["fid"] else "") + ")"]
    if f["address"]:
        L.append(f"    - address: {f['address']}")
    if f["codes"]:
        L.append(f"    - industry codes: {', '.join(f['codes'])}")
    if f.get("hint"):
        L.append(f"    - the record says: {f['hint'][:300]}")
    for p in f["permits"]:
        L.append(f"    - permit: {p['number'] or 'number not shown'}, {p['type'] or 'type not shown'}, {p['status']}"
                 + (f", {p['step']}" if p["step"] else "") + (f", comments end {p['comment_ends']}" if p["comment_ends"] else ""))
    for x in f["links"]:
        L.append(f"    - page: {x['kind']}: {x['url']}")
    if f["found_by"]:
        L.append(f"    - found by: {'; '.join(f['found_by'])}")
    for d in f["docs"]:
        L.append(f"    - document ({d.get('state', 'not read')}, {d['date'] or 'date not shown'}): {d['name']}: {d['url'] or 'link not opened'}")
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
    L = [f"# Wisconsin air permit files for {plant['name']} ({plant['id']})", "",
         "Sources: the Wisconsin DNR permit tracking record (WARP, " + WARP + "), its public notice, applications received and "
         "final decision feeds, EPA ECHO and the EPA RBLC. A document address (AM_DownloadObject.aspx?id=...) needs no sign-in, "
         "is stable and is citable as it stands; fetch.py and url_verifier.py read it. The documents and their text are saved "
         "under work/permits/docs/.", "", f"Harvested: {time.strftime('%Y-%m-%d %H:%M %Z')}", "",
         f"GEM statuses: {', '.join(plant['statuses'])}. City in GEM: {plant['city'] or 'blank'}. County in GEM: {plant['county'] or 'blank'}.", ""]
    if not matched:
        L += ["No permit facility matched this plant. That does not mean it has no permits: it may be filed under the owner, a "
              "contractor or another site name, or it may be only a planning entry with no site. Check _unmatched.md and _leads.md "
              "in this folder, and search WARP by the owner's name.", ""]
    elif not any(f["docs"] for f, _ in matched):
        L += ["The matched facilities have no documents online. Older permits need a public records request to the DNR Air Management Program.", ""]
    for f, how in matched:
        L += fac_block(f, how) + [""]
    for n in notices:
        L += [f"DNR {n['kind']}: {n['permit']} (posted {n['date'] or 'date not shown'})"
              + (f", comments end {n['comment_ends']}" if n["comment_ends"] else "")] + [""]
    for e in extra:
        L += [e, ""]
    path.write_text("\n".join(L), encoding="utf-8")


def slim(f):
    """A facility as facilities.json and index.json keep it: no full document text."""
    return {"key": f["key"], "name": f["name"], "source": f["source"], "company": f["company"],
            "county": f["county"], "city": f["city"], "address": f["address"], "codes": f["codes"],
            "hint": f.get("hint", ""), "fid": f["fid"], "seq": f["seq"], "ai": f.get("ai"), "lat": f["lat"], "lon": f["lon"],
            "found_by": f["found_by"], "collection": f["collection"], "activities": f["activities"][:40], "links": f["links"],
            "permits": f["permits"],
            "docs": [{k: d[k] for k in ("number", "name", "type", "date", "url", "state", "file", "facts", "how", "page")
                      if k in d} for d in f["docs"]]}


# ----------------------------------------------------------------- plants ---

def load_plants(args=None, csv_path=None):
    csv = pd.read_csv(csv_path or CSV, low_memory=False, encoding="utf-8-sig")
    csv = csv[csv["State/Province"] == "Wisconsin"]
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
                       "statuses": sorted(set(rows["Status"].astype(str))), "name_words": words(r["Plant name"])})
    return plants


def read_echo(net):
    if net.offline:
        j = net.json("", "echo_wi.json")
        return (j or {}).get("Results", {}).get("Facilities", [])
    q = net.json(f"{ECHO}.get_facilities", params={"output": "JSON", "p_st": "WI", "p_sic": "4911", "p_act": "Y", "responseset": "100"})
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


def read_rblc(net):
    out = []
    for kw in RBLC_KEYWORDS:
        j = net.json(RBLC_API, f"rblc_{kw}.json" if kw == "turbine" else "", method="POST", json_body={"keywords": kw, "state": "WI"}, quiet=True)
        out += rblc_facilities((j or {}).get("results"))
    seen, uniq = set(), []
    for x in out:
        if x["permit_guid"] not in seen:
            seen.add(x["permit_guid"])
            uniq.append(x)
    return uniq


# ------------------------------------------------------------------- main ---

def main():
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n\n")[0])
    ap.add_argument("--scope", required=True, help="batch folder name, e.g. us-wi")
    ap.add_argument("--plants", help="comma-separated GEM location IDs (default: every plant); reads only their facilities' documents and skips the sweep")
    ap.add_argument("--fid", help="comma-separated WARP FIDs to read as extra matched facilities (a smoke test)")
    ap.add_argument("--leads", default="all", help="comma-separated lead keys, 'all' or 'none'")
    ap.add_argument("--match-only", action="store_true", help="list matches only, no document reads")
    ap.add_argument("--no-sweep", action="store_true")
    ap.add_argument("--no-notices", action="store_true")
    ap.add_argument("--no-epa", action="store_true", help="skip the ECHO list and the RBLC")
    ap.add_argument("--no-lists", action="store_true", help="skip the whole-list WARP searches and the data center name searches")
    ap.add_argument("--offline", action="store_true", help="read the saved sample pages in tests/fixtures/harvest_wi/, no network")
    ap.add_argument("--fixtures", help="another folder of saved sample pages")
    ap.add_argument("--docs-per-facility", type=int, default=15)
    ap.add_argument("--pages", type=int, default=None, help="read only the first pages of each document")
    ap.add_argument("--ocr-pages", type=int, default=6)
    args = ap.parse_args()

    out_dir = harvest_out(args.scope)
    hv_dir = REPO / "batches" / args.scope / "harvest"
    hv_dir.mkdir(parents=True, exist_ok=True)
    plants = load_plants(args)
    stamp = time.strftime("%Y-%m-%d")
    net = Net(args.offline, args.fixtures)
    w = Warp(net)
    leads = [] if args.leads == "none" else [x for x in LEADS if args.leads == "all" or x["key"] in args.leads.split(",")]
    facs = {}

    # 1. WARP lists and name searches
    searches = []
    if not args.no_lists and not args.plants:
        searches += [(label, {fld: val}, mode) for label, fld, val, mode in LISTS]
        searches += [(f"name_{slug(q)}", {"name": q}, "contains") for q in DC_QUERIES]
    wanted_q = {}
    for p in plants:
        k = KNOWN.get(p["id"])
        if k and k["q"] and not k["fid"]:
            wanted_q.setdefault(k["q"], []).append(p["id"])
    for ld in leads:
        for q in ld["q"]:
            wanted_q.setdefault(q, []).append(ld["key"])
    searches += [(f"name_{slug(q)}", {"name": q}, "contains") for q in wanted_q if f"name_{slug(q)}" not in [s[0] for s in searches]]
    for label, fields, mode in searches:
        kind, got, url = w.search(label, mode, **fields)
        if kind == "list":
            for row in got:
                merge_into(facs, facility_from_row(row, label if label in CODES else "name"))
        elif kind == "facility":
            p = parse_facility_page(got)
            f = new_fac(f"fid-{p['fid']}", p["name"], "DNR WARP")
            f["fid"], f["found_by"] = p["fid"], [f"WARP search {label}"]
            merge_into(facs, f)
        log(f"WARP {label}: {len(got) if kind == 'list' else 1 if kind == 'facility' else 0} facilities")
    for p in plants:  # a plant with a known FID is added directly so it is always opened
        for fid in KNOWN.get(p["id"], {}).get("fid", []):
            f = new_fac(f"fid-{fid}", f"FID {fid}", "DNR WARP")
            f["fid"], f["found_by"] = str(fid), ["hand-checked FID"]
            merge_into(facs, f)
    for ld in leads:
        for fid in ld.get("fid", []):
            f = new_fac(f"fid-{fid}", f"FID {fid}", "DNR WARP")
            f["fid"], f["found_by"] = str(fid), ["lead FID"]
            merge_into(facs, f)
    for fid in (args.fid or "").split(","):
        if fid.strip():
            f = new_fac(f"fid-{fid.strip()}", f"FID {fid.strip()}", "DNR WARP")
            f["fid"], f["found_by"] = fid.strip(), ["--fid"]
            merge_into(facs, f)

    # 2. notice feeds
    items = []
    if not args.no_notices:
        for kind, url in FEEDS.items():
            r = net.req(url, url.rsplit("/", 1)[-1].replace(".aspx", ".html"))
            got = parse_feed(r.text, kind) if r is not None else []
            if r is None:
                report_failure(url, "000", "DNR notice feed")
            items += got
            log(f"DNR {kind}: {len(got)} rows")
        for f in notice_facilities(items).values():
            merge_into(facs, f)

    # 3. EPA lists
    echo, rblc = [], []
    if not args.no_epa and not args.plants:
        echo = read_echo(net)
        for f in echo_facilities(echo).values():
            merge_into(facs, f)
        rblc = read_rblc(net)
        log(f"EPA: {len(echo)} ECHO electric facilities, {len(rblc)} RBLC permits")

    allf = list(facs.values())
    matches = {p["id"]: match(p, allf) for p in plants}
    lead_hits = {ld["key"]: match_lead(ld, allf) for ld in leads}
    extra_keys = {f["key"] for f in allf if "--fid" in f["found_by"]}
    matched_keys = {f["key"] for ms in matches.values() for f, _ in ms} | {f["key"] for v in lead_hits.values() for f in v} | extra_keys
    power = [f for f in allf if f["key"] in matched_keys or is_power(f)]
    unmatched = [f for f in power if f["key"] not in matched_keys]

    if args.match_only:
        for p in plants:
            for f, how in matches[p["id"]] or [(new_fac("", "no match", ""), "")]:
                print(f"{p['id']}\t{p['name']}\t{f['name']}\t{f['key']}\t{how}")
        for ld in leads:
            for f in lead_hits[ld["key"]] or [new_fac("", "no match", "")]:
                print(f"LEAD {ld['key']}\t{ld['name']}\t{f['name']}\t{f['key']}")
        for f in unmatched:
            print(f"UNMATCHED\t\t{f['name']}\t{f['key']}\t{f['city']}\t{f['county']}")
        return

    # 4. open every matched facility, list permits and documents, read the newest documents
    for k, f in enumerate([x for x in power if x["key"] in matched_keys], 1):
        if f["source"] == "EPA ECHO (SIC 4911)":
            continue
        st, p = open_facility(w, f)
        if st is None:
            net.errors.append(f"could not open {f['name']} (FID {f['fid'] or '?'}, seq {f['seq'] or '?'})")
            continue
        f["name"] = p["name"] or f["name"]
        fill_facility(f, p)
        tag = f["fid"] or f["seq"]
        docs = list_documents(w, st, p, tag)
        known_ids = {d["url"] for d in f["docs"]}
        f["docs"] += [d for d in docs if d["url"] not in known_ids or not d["url"]]
        reveal_links(w, st, [d for d in f["docs"] if "permit_idx" in d], args.docs_per_facility, tag)
        f["docs"] = rank_docs(f["docs"])
        for n, d in enumerate(f["docs"]):
            if not d["url"]:
                d["state"] = "not opened (cap); open the facility page and select the permit"
            elif n >= args.docs_per_facility:
                d["state"] = "not read (cap)"
            elif "facts" not in d:
                read_doc(net, out_dir, f, d, pages=args.pages, ocr_pages=args.ocr_pages)
        log(f"({k}) {f['name']}: {len(p['permits'])} permits, {min(len(f['docs']), args.docs_per_facility)} of {len(f['docs'])} documents read")

    def notice_hits(patterns):
        return [n for n in items if patterns and any(re.search(p, n["name"].lower()) for p in patterns)]

    with (out_dir / "harvest_log.jsonl").open("a", encoding="utf-8") as logf:
        for p in plants:
            k = KNOWN.get(p["id"]) or {"names": []}
            nh = notice_hits(k["names"])
            write_index(out_dir / f"{p['id']}.md", p, matches[p["id"]], nh, [])
            (out_dir / f"{p['id']}.json").write_text(json.dumps(
                {"plant": {k2: p[k2] for k2 in ("id", "name", "city", "county", "statuses", "lat", "lon")},
                 "facilities": [{**slim(f), "how": how} for f, how in matches[p["id"]]], "notices": nh}, indent=1), encoding="utf-8")
            logf.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "plant": p["id"], "name": p["name"],
                                   "facilities": [{"name": f["name"], "key": f["key"], "how": how,
                                                   "docs": {d["name"]: d.get("state", "not read") for d in f["docs"]}}
                                                  for f, how in matches[p["id"]]]}) + "\n")

    L = ["# Wisconsin leads: projects GEM lacks or knows under another name", "",
         "Each lead is searched in WARP by name and in the notice feeds. No hit does not mean no permit: the permit may be filed "
         "under a developer, a contractor or an LLC; search the owner's name in WARP and check the PSC and county records.", ""]
    for ld in leads:
        hits = lead_hits[ld["key"]]
        L += [f"## {ld['name']}", ""]
        L += [x for f in hits for x in fac_block(f)] if hits else ["No facility or notice matched."]
        for n in notice_hits(ld["names"]):
            L.append(f"- DNR {n['kind']}: {n['name']}, {n['permit']} (posted {n['date'] or 'date not shown'})")
        L.append("")
    (out_dir / "_leads.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    L = ["# Wisconsin facilities that look like power or data center sites but match no GEM plant or lead", "",
         "Each may be a plant outside this batch, a plant GEM lacks, a backup generator fleet at a data center or another site, or not a "
         "power plant at all. Check engines or turbines of 50 MW or more in total (generating capacity only). Open the facility page to see its permits.", ""]
    for f in sorted(unmatched, key=lambda f: f["name"].lower()):
        L += fac_block(f) + [""]
    if not unmatched:
        L.append("None this run.")
    (out_dir / "_unmatched.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    L = [f"# DNR notice feeds read {stamp}", "", f"{len(items)} rows. Sources: " + "; ".join(FEEDS.values()), ""]
    for n in items:
        if is_power({"name": n["name"], "hint": n["permit"], "codes": []}) or any(re.search(p, n["name"].lower()) for k in KNOWN.values() for p in k["names"]):
            L += [f"- {n['name']} ({n['county']} County), {n['kind']}, permit {n['permit']}, {n['date'] or 'date not shown'}"
                  + (f", comments end {n['comment_ends']}" if n["comment_ends"] else "")]
            L += [f"    - {d['name']}: {DOWNLOAD + d['doc_id']}" for d in n["docs"]]
    (out_dir / "_notices.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    L = [f"# EPA records {stamp}", "", "## EPA ECHO electric facilities in Wisconsin (SIC 4911), a cross-check list", ""]
    L += [f"- {r.get('AIRName')} ({r.get('AIRCity')}, {r.get('AIRCounty')}; source {r.get('SourceID')})" for r in echo
          if "PORTABLE" not in str(r.get("AIRStreet") or "").upper()]
    (out_dir / "_epa.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    L = [f"# EPA RBLC permits in Wisconsin {stamp}", "", f"From the RBLC keyword search ({RBLC}), keywords {', '.join(RBLC_KEYWORDS)}, state WI. "
         "The RBLC lists permits that set a best available control limit; it is a lead list, not the permit record.", ""]
    for x in rblc:
        L.append(f"- {x['facility']} ({x['authority']}), issued {x['issued'] or 'date not shown'}: {'; '.join(x['processes'][:4])}")
    (out_dir / "_rblc.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    index = {"harvested": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "warp_facilities": sum(1 for f in allf if f["source"] == "DNR WARP"),
             "notice_rows": len(items), "echo_facilities": len(echo), "rblc_permits": len(rblc),
             "plants": {p["id"]: {"name": p["name"], "facilities": [{"key": f["key"], "name": f["name"], "how": how}
                                                                    for f, how in matches[p["id"]]]} for p in plants},
             "leads": {ld["key"]: [f["key"] for f in lead_hits[ld["key"]]] for ld in leads},
             "unmatched": [f["key"] for f in unmatched], "facilities": {f["key"]: slim(f) for f in power}, "errors": net.errors}
    (out_dir / "index.json").write_text(json.dumps(index, indent=1), encoding="utf-8")
    (hv_dir / "facilities.json").write_text(json.dumps({
        "harvested": index["harvested"], "matches": index["plants"], "leads": index["leads"],
        "unmatched": [slim(f) for f in unmatched], "matched": [slim(f) for f in power if f["key"] in matched_keys]}, indent=1), encoding="utf-8")

    S = [f"# Wisconsin air permit harvest, {stamp}", "",
         f"WARP facilities: {index['warp_facilities']}. Notice feed rows: {len(items)}. EPA: {len(echo)} ECHO facilities, {len(rblc)} RBLC permits. "
         f"Power-like: {len(power)}. Matched: {len(matched_keys)}. Unmatched: {len(unmatched)}.", "", f"Calls: {net.calls}.", ""]
    if net.errors:
        S += ["Calls that failed (retry before concluding anything):", ""] + [f"- {e}" for e in net.errors[:40]] + [""]
    S += ["## Matches per GEM plant", ""]
    for p in plants:
        ms = matches[p["id"]]
        S.append(f"- {p['name']} ({p['id']}): " + ("; ".join(f"{f['name']} ({f['key']}, {how})" for f, how in ms) if ms else "no facility matched"))
    S += ["", "## Leads", ""]
    for ld in leads:
        S.append(f"- {ld['name']}: " + ("; ".join(f"{f['name']} ({f['key']})" for f in lead_hits[ld['key']]) or "nothing matched"))
    S += ["", "## Unmatched power-like facilities", ""]
    S += [f"- {f['name']} ({f['city'] or '?'}, {f['county'] or '?'} County; {f['source']})" for f in sorted(unmatched, key=lambda f: f["name"].lower())]
    (hv_dir / "harvest_summary.md").write_text("\n".join(S) + "\n", encoding="utf-8")
    log("done")


if __name__ == "__main__":
    main()

"""
Harvest Michigan air permits before a research sweep.

The Michigan Department of Environment, Great Lakes, and Energy (EGLE) keeps
its Air Quality Division (AQD) permit records in three places. None needs a
login for what this script reads. What was found (2026-10-23):

  1. The MiEnviro Portal (mienviro.michigan.gov), a Windsor nCore system like
     the Kansas KEIMS portal.
       - The portal side (/ncore/) answers 401 "IAM session is invalid" for its
         site search, permit list and document list. Only the public notice
         list works without a login:
         GET /ncore/ss/publicnoticeslist?queryParams={"filter":[{"programAreaId":"AQD_AIR"}]}
         gives the air notices out for comment now (site, SRN, permit number,
         notice type, dates, latitude and longitude), and
         GET /ncore/ss/publicnoticedocuments?PublicNoticeId=<id> lists each
         notice's documents (the id is a top-level parameter, not a filter).
       - The Map Explorer side (/nsite/) is the public "Data Explorer". It
         works without a login once each request carries the header
         Referer: https://mienviro.michigan.gov/nsite/default/map/results.
         Without that header every service answers 400 "Value cannot be null.
         (Parameter 'uriString')", which looks like a block and is not.
         (Kansas KEIMS gives the same 400; its note may have the same cause.)
         POST /nsite/ss/explorersites searches sites by name, inside a map
         box, with filters that can be combined: site type ("Air - Air
         Facility", 15,579 sites), NAICS code, SIC code, permit category ("Air
         Renewable Operating Permit", 647 sites). It answers with map points
         and clusters. A cluster lists its sites unless it is large, so this
         script splits the box into quarters until every cluster lists them.
         Each air site name ends with its State Registration Number (SRN) in
         brackets, for example "Midland Cogeneration Venture (B6527)". The
         site profile services (GET, queryParams={"filter":[{"id":<site id>}]})
         give the address and county, the SRN alias, the NAICS and SIC codes,
         every permit with its status and dates (in effect, extended,
         terminated), every submission (applications, with their status and
         dates), active public notices, and the full document list. Each
         document downloads as a plain GET of /ncore/downloadpdf/<id>, served
         as a PDF even when the original was a Word file.
  2. The older AQD file server (www.egle.state.mi.us/aps/downloads/, the same
     files at www.deq.state.mi.us), plain directory listings:
       - SRN/<SRN>/: inspection reports (FCE, SAR), test reports and
         violation notices per facility, 2014 onward.
       - rop/Pub_ntce/<SRN>/: the final Renewable Operating Permit (ROP), its
         staff report and the renewal application.
       - permits/finpticon/<year>/<number>.pdf: every final Permit to Install
         (PTI) from 1967 to 2024 (the 2025 folder is empty: newer permits are
         in MiEnviro only). permits/finpticon/Active PTIs by SRN.pdf lists every
         active PTI since 1997 by SRN with its approval date, and Pending PTI
         Applications.pdf lists the applications open at the end of 2024 with
         a one-line reason ("modifications to two existing turbines").
       - permits/PubNotice/: the three AQD notice lists, rebuilt each week:
         NSR_PTIs_Open_for_Comment.pdf, NSR_PTIs_Pending_Decision.pdf and
         NSR_PTIs_Final_Decisions.pdf. Before MiEnviro (to mid 2024) each
         notice's documents sat in PubNotice/<application>/ (project summary,
         notice of hearing, technical fact sheet, proposed permit, company
         letter). Those folders are removed after the decision, but the
         Wayback Machine holds 15 or more distinct copies of each list from
         2022 on and about 1,000 saved notice files, so this script reads every
         distinct copy of the three lists and takes the document links out of
         each PDF.
  3. The AQD public notice page on michigan.gov
     (/egle/about/organization/air-quality/public-notice) only links the three
     lists above. The EGLE public notice calendar is a Coveo search page; its
     air entries repeat the MiEnviro notices, so this script does not script
     it.

Steps:
  1. List the air sites (site type "Air - Air Facility") with a power or data
     center NAICS or SIC code, every ROP site, and the air sites whose name
     holds a power word or the name of a GEM plant or watch-list project.
  2. Keep the ones that look like power plants or data centers, match each GEM
     Michigan plant to them (KNOWN holds hand-checked name patterns; a name
     word match adds more, marked for checking) and list the rest as possible
     new plants.
  3. For each kept site read the MiEnviro profile (address, permits,
     submissions, notices, documents, map point) and the older file server
     folders, and parse the active PTI and pending application lists.
  4. Read the notices: MiEnviro now, and the three AQD lists now and in every
     distinct Wayback copy.
  5. Download the key documents of each site (final PTIs, technical fact
     sheets, project summaries, proposed permits, ROPs and staff reports, PTI
     applications, the newest full compliance evaluation, and the notice
     documents) through fetch.py, newest first, and keep the lines that give
     the permit number, project, equipment, maker, model, sizes (MW, MMBtu/hr,
     horsepower) and the location. Michigan hosts are added to fetch.py's paced
     hosts at run time, so every document lands in the disk cache
     (work/fetch_cache/) and url_verifier.py reads it at once.

Output, in work/permits/<scope>/ (what the sweep agents read): one plain-text
index per plant (<GEM location id>.md), plus _unmatched.md, _notices.md,
_activity.md and harvest_log.jsonl (one line per plant per run, with the
MiEnviro map point of each matched site for location_candidates.py). A summary
and the data behind it go to batches/<scope>/harvest/ (harvest_summary.md,
facilities.json, notices.json, activity_air.json, pti_lists.json). Permit PDFs
name agency and company staff with their contact details: the PDFs and the
full document text stay under work/ (never committed). Nothing here stages a
record.

Usage (from scripts/):
    python harvest_permits_michigan.py --scope us-mi                  # every plant
    python harvest_permits_michigan.py --scope us-mi --plants L100000402478
    python harvest_permits_michigan.py --scope us-mi --match-only     # list matches, download no documents
    python harvest_permits_michigan.py --scope us-mi --no-wayback     # current notice lists only
"""
import argparse
import html
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import quote, unquote, urljoin

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fetch  # noqa: E402
from fetch import CHROME_UA, fetch_page  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
MIE = "https://mienviro.michigan.gov"
NSITE = f"{MIE}/nsite"
NCORE = f"{MIE}/ncore"
PROFILES = f"{NSITE}/ss/api/nsite-explorer/default-mode/profiles"
APS = "https://www.egle.state.mi.us/aps/downloads"
CDX = "http://web.archive.org/cdx/search/cdx"
CSV = REPO / "scripts" / "gem_export_gogpt_scoped.csv"
REFERER = f"{NSITE}/default/map/results"
MI_BOX = (41.0, 48.9, -92.5, -80.3)          # lat min, lat max, lon min, lon max

AIR_SITE = {"attributeName": "1H_Site Type", "attributeValue": "Air - Air Facility"}
ROP_SITES = {"attributeName": "2D_Permit Category", "attributeValue": "Air Renewable Operating Permit"}
# NAICS and SIC codes whose sites can hold generating capacity: electric power
# generation (fossil, nuclear, other), transmission and distribution, steam and
# air conditioning supply, data processing and hosting.
POWER_NAICS = ["221111", "221112", "221113", "221117", "221118", "221121", "221122", "221330", "518210"]
POWER_SICS = ["4911", "4931", "4932", "4939", "4961", "7374"]
NOTICE_LISTS = ["NSR_PTIs_Open_for_Comment.pdf", "NSR_PTIs_Pending_Decision.pdf", "NSR_PTIs_Final_Decisions.pdf"]

# Name searches (each limited to air sites): power words, the owners, every GEM
# Michigan plant's distinctive name or town, the watch list (2026-10-23) and
# the EIA plants GEM lacks.
TERMS = [
    "Power", "Generat", "Energy", "Peaking", "Cogen", "Electric", "Data Center", "Turbine", "Board of Water",
    "BPW", "Wolverine", "Indeck", "CMS", "Consumers", "DTE", "Utility", "Light", "Municipal", "Cooperative",
    "Covert", "Zeeland", "Karn", "Renaissance", "Kuester", "Mihm", "Alpine", "Sumpter", "Greenwood", "Dean",
    "Delray", "Blue Water", "Kalamazoo", "Kalkaska", "Marquette", "Ludington", "Niles", "Holland", "Midland",
    "Dearborn", "Belle River", "Handy", "Milan", "Marshall", "Thetford", "Hampton", "Weadock", "Campbell",
    "Monroe", "Fermi", "Hancock", "Northeast", "Superior", "Johnson", "University of Michigan", "Livingston",
    "Gaylord", "Simon", "Saline", "Jackson", "Lansing", "Delta", "REO", "Eckert", "Erickson", "Trenton",
    "River Rouge", "St. Clair", "Harbor Beach", "Cobb", "Whiting", "Presque", "Mitten", "Stargate", "Related",
    "Oracle", "OpenAI", "Microsoft", "Google", "Meta", "Amazon", "Switch", "Project", "Development Partners",
]

# Hand-checked name patterns (2026-10-23): GEM plant -> regexes that must hit
# "<site name> | <city>" of a MiEnviro air site. A plant missing here is matched
# by its name words, and those matches are marked for checking.
KNOWN = {
    "L100000401789": [r"\(n2586\)"],                      # Holland BPW 48th Street Peaking Station
    "L100000409227": [r"\(n2586\)", r"?\(n6000\)"],      # same address; the older Holland BPW site
    "L100000409204": [r"\(p0796\)"],                      # Upper Michigan Energy Resources, A.J. Mihm
    "L100000402385": [r"\(p0582\)"],                      # Wolverine Alpine Power Plant
    "L100001083332": [r"?\(b2840\)"],                     # Karn gas project, proposed at the D.E. Karn site
    "L100000103973": [r"\(b2796\)"],                      # DTE St. Clair / Belle River
    "L100000402393": [r"?\(b2796\)", r"?\(n6945\)"],     # Blue Water Energy Center, next to Belle River
    "L100000401829": [r"\(b2840\)"],                      # Consumers Energy D.E. Karn
    "L100000401855": [r"?\(b2796\)"],                     # Dean peakers, East China, no site of their own seen
    "L100000402454": [r"\(n6631\)"],                      # Dearborn Industrial Generation
    "L100000401856": [r"\(b2798\)"],                      # DTE Delray Power Plant
    "L100000402461": [r"\(b4001\)"],                      # Lansing BWL Erickson site, where Delta Energy Park sits
    "L100000409210": [r"\(p0797\)"],                      # Upper Michigan Energy Resources, F.D. Kuester
    "L100001083333": [r"?\(b2918\)"],                     # Genesee County project; Thetford CT plant site
    "L100000401857": [r"\(b6145\)"],                      # DTE Greenwood Energy Center
    "L100001082478": [r"?\(b2795\)"],                     # Handy Township project; Colfax peakers in Handy Twp
    "L100000401790": [r"\(p0465\)"],                      # Holland Energy Park
    "L100000402411": [r"\(n6921\)"],                      # Indeck Niles
    "L100000401830": [r"\(n6626\)"],                      # Consumers Jackson Generating Station
    "L100000401824": [r"\(n6731\)"],                      # CMS Generation Kalamazoo River
    "L100000402079": [r"\(n7113\)", r"?\(n6522\)"],      # Michigan Public Power Agency, Kalkaska
    "L100000103983": [r"\(b2647\)", r"?\(b4001\)"],      # Lansing BWL REO Town
    "L100000407415": [r"\(p0884\)", r"?\(p1499\)"],      # Marshall Energy Center LLC; DTE Marshall
    "L100000407414": [r"\(p0884\)", r"?\(p1499\)"],
    "L100000409279": [r"\(p0668\)", r"?\(n5887\)", r"?\(b1833\)"],  # Marquette Board of Light and Power
    "L100000401674": [r"\(n4975\)"],                      # DTE Michigan Power, Ludington
    "L100000402478": [r"\(b6527\)"],                      # Midland Cogeneration Venture
    "L100001088928": [r"milan.*(dte|power|energy|generat)|(dte|power|energy|generat).*milan"],
    "L100000402123": [r"\(n6767\)"],                      # Covert Generating Station
    "L100000401858": [r"\(n6873\)"],                      # DTE Renaissance
    "L100000402386": [r"\(m4854\)", r"?\(m4095\)", r"?\(n7066\)"],  # Sumpter
    "L100000401831": [r"\(n6521\)"],                      # Consumers Zeeland Generating Station
}
# Sites kept whatever their name says (2026-10-23 watch list): coal plants with gas
# plans, EIA plants GEM lacks, data center projects.
WATCH = {
    "B2835": "J.H. Campbell coal plant, watch for gas replacement",
    "B2816": "Monroe coal plant, watch for gas replacement",
    "B4321": "Fermi, EIA plant 1729 that GEM lacks (combustion turbines)",
    "B2805": "Hancock peakers, EIA plant 1730 that GEM lacks",
    "B2808": "Northeast peakers, EIA plant 1734 that GEM lacks",
    "B2806": "Superior peakers, EIA plant 1744 that GEM lacks",
    "K3249": "Michigan State University, T B Simon plant, EIA plant 10328 that GEM lacks",
    "M0675": "University of Michigan central plant, EIA plant 50431 that GEM lacks",
    "N6526": "Livingston Generating Station, EIA plant 55102 that GEM lacks",
    "N6833": "Wolverine Gaylord Generating Station, EIA plant 7932 that GEM lacks",
    "B2942": "Consumers Gaylord combustion turbines",
    "P1598": "Project Mitten data center, Saline Township",
}

POWER_NAME = re.compile(
    r"power|electric|generat|energy|edison|\bdte\b|consumers|cms |wolverine|indeck|board of (water|public)|"
    r"\bbpw\b|\bbwl\b|light|utilit|cooperative|turbine|cogen|steam|peaking|data ?cent|datacent|compute|"
    r"cloud|hyperscal|stargate|mitten|combined cycle|\bcep\b|\breo\b|energy park", re.I)
POWER_DROP = re.compile(
    r"sawmill|lumber|forest products|timber|plywood|veneer|asphalt|ready mix|concrete|landfill|"
    r"compressor|pipeline|pipe line|gas transmission|gas storage|refinery|chemical|steel|wire|foundry|"
    r"casting|motors|bakeries|ethanol|biodiesel|pellet|shipyard|marine|hospital|school|college|casino|"
    r"walmart|dollar|apparel|furniture|paper|pulp|packaging|brick|cement|lime\b|aluminum|silicon|"
    r"oil and gas|gas processing|terminal|propane|truck|rail|crematory|cemetery|funeral|printing|bottling|"
    r"sand|gravel|quarry|wood|mill\b|manufactur|light ?(metal|ing|house)|lighthouse|dairy|farm|"
    r"tool|plating|coating|paint|plastic|auto body|collision|dry clean|cleaners|church|well site|"
    r"\bwells?\b|tank battery|production facility|cpf|\bgas plant\b|oil field|battery plant", re.I)
NAME_NOISE = re.compile(
    r"\b(power station|power plant|generating station|generating|generation|facility|station|energy center|"
    r"energy|plant|power|gt|mi|michigan|the|municipal|of|and|city|llc|inc|company|co|corp|"
    r"corporation|advanced|combined|cycle|county|township|twp|electric|dte|consumers|board|"
    r"water|light|natural|gas|project|cogeneration|venture)\b", re.I)
EQUIPMENT = re.compile(r"turbine|\bct\b|\bctg\b|engine|\brice\b|generat|\bgen\b|boiler|duct burner|hrsg|"
                       r"combined cycle|simple cycle|peaking|diesel|reciprocating|genset|\bEUCT|\bEUGT|\bFGCT", re.I)
SIZE = re.compile(r"\d[\d,.]*\s*(MW|MWe|megawatt|kW|kilowatt|MMBtu|mmbtu|hp|horsepower|bhp)\b")
MAKER = re.compile(r"model\b|caterpillar|cat g|wartsila|w[äa]rtsil[äa]|jenbacher|"
                   r"general electric|\bGE\b|siemens|solar turbines|mitsubishi|cummins|rolls[- ]royce|"
                   r"mtu\b|kohler|generac|waukesha|baldor|detroit diesel|pratt|ansaldo|"
                   r"hitachi|titan \d|taurus|mars \d|lm ?\d{4}|7ea|7fa|7ha|6b\b|f-?class|h-?class", re.I)
LOCATION = re.compile(
    r"latitude|longitude|\blat\b|\blong\b|\bUTM\b|\bsection \d+|township|"
    r"located (at|in|on|near|approximately)|physical address|site address|facility address|"
    r"street address|\b\d{2,5} [A-Z0-9][\w. ]+ (road|rd|street|st|avenue|ave|"
    r"highway|hwy|drive|dr|lane|ln|blvd|boulevard)\b|county,? michigan|mi 4[89]\d{3}|michigan 4[89]\d{3}",
    re.I)
PROJECT = re.compile(r"proposes|propose to|proposed project|will consist|project (is|will|consists)|"
                     r"construction of|to construct|new (electric|power|generat|natural gas)|install(ation)? of|"
                     r"request to install|replace|retire|convert|conversion|shut ?down|decommission", re.I)
LATLON = re.compile(r"\b(4[1-8]\.\d{3,})\s*[,;/ ]\s*(-\s*)?(8[2-9]\.\d{3,}|90\.\d{3,})\b")
PERMIT_NO = re.compile(r"\bPTI\s?\d{7}(?: v\d+\.\d+)?|\bROP\s?\d{7}|\bMI-ROP-[A-Z]\d{4}-\d{4}|\bAPP-\d{4}-\d{4}|"
                       r"\bPKG-\d{7}|\bPTI (?:No\.? ?)?\d{1,4}-\d{2}[A-Z]?\b|\bPermit (?:to Install )?No\.? ?\d{1,4}-\d{2}[A-Z]?\b",
                       re.I)
SRN_SUFFIX = re.compile(r"\s*\(([A-Z]\d{4})\)\s*$")
SKIP_DOC = re.compile(r"\.(msg|xlsx?|csv|zip|jpe?g|png|gif|tiff?)$|spanish|arabic|espa[ñn]ol|"
                      r"\(spanish\)|\(arabic\)|test (report|plan|details)|stack test|rata|cems|excess emission|"
                      r"monitor downtime|quarterly|semi-annual|deviation report|mapr|emissions report", re.I)


EMAIL = re.compile(r"[\w.+-]+@[\w-]+(\.[\w-]+)+")
PHONE = re.compile(r"\(?\b\d{3}\)?[-. ]\d{3}[-. ]\d{4}\b")


def scrub(s):
    """Drop email addresses and phone numbers from text kept in the batch folder."""
    return PHONE.sub("[phone]", EMAIL.sub("[email]", s or ""))


def log(msg):
    print(f"[harvest-mi] {msg}", file=sys.stderr, flush=True)


def clean(s):
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s or "", flags=re.S | re.I)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def pace_michigan_hosts():
    """Make fetch.py pace and cache the Michigan hosts, so every document this run reads
    lands in work/fetch_cache/ (url_verifier.py then reads it without a second download)."""
    extra = (
        (re.compile(r"(^|\.)mienviro\.michigan\.gov$"), "mienviro", 0.5),
        (re.compile(r"^(www\.)?(egle|deq)\.state\.mi\.us$"), "egle-aps", 0.5),
    )
    have = {k for _, k, _ in fetch._PACED_HOSTS}
    fetch._PACED_HOSTS = tuple(fetch._PACED_HOSTS) + tuple(x for x in extra if x[1] not in have)


def get(url, timeout=120):
    return fetch_page(url, timeout=timeout)


def words(text):
    t = NAME_NOISE.sub(" ", re.sub(r"\(.*?\)", " ", str(text or "")))
    return {w.lower() for w in re.split(r"[^A-Za-z]+", t) if len(w) >= 4}


def iso(s):
    """'2026-10-12T08:30:53.6470000-04:00' or '10/12/2026' to '2026-10-12', or ''."""
    s = str(s or "")
    m = re.match(r"(\d{4}-\d{2}-\d{2})", s)
    if m:
        return m.group(1)
    m = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
    return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}" if m else ""


def split_srn(site_name):
    """'Midland Cogeneration Venture (B6527)' -> ('Midland Cogeneration Venture', 'B6527')."""
    m = SRN_SUFFIX.search(site_name or "")
    if not m:
        return (site_name or "").strip(), ""
    return site_name[:m.start()].strip(), m.group(1)


def parse_wkt(wkt):
    """'POINT(-88.6166085 46.7936854)' -> (46.7936854, -88.6166085), or (None, None)."""
    m = re.match(r"\s*POINT\s*\(\s*(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s*\)", wkt or "", re.I)
    return (float(m.group(2)), float(m.group(1))) if m else (None, None)


# ------------------------------------------------------------- MiEnviro ---

class Mie:
    """The MiEnviro Map Explorer services. Every call carries the map page Referer."""

    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": CHROME_UA, "Referer": REFERER,
                               "Accept": "application/json, text/plain, */*"})
        self.calls = 0

    def _req(self, method, url, retries=4, **kw):
        last = ""
        for i in range(retries):
            try:
                self.calls += 1
                r = self.s.request(method, url, timeout=180, **kw)
                if r.status_code == 200:
                    return r.json()
                last = f"HTTP {r.status_code} {r.text[:120]}"
            except (requests.RequestException, ValueError) as e:
                last = str(e)[:160]
            time.sleep(4 * (i + 1))
        log(f"{url.split('?')[0]}: {last}")
        return None

    def search(self, term="", filters=None, box=MI_BOX):
        body = {"insertUpdateList": [{
            "displayHeight": 900, "displayWidth": 1400, "filterValuesJson": filters or None,
            "isIncludeUnmappable": True, "latitudeMin": str(box[0]), "latitudeMax": str(box[1]),
            "longitudeMin": str(box[2]), "longitudeMax": str(box[3]), "modeId": "default",
            "searchTerm": term, "responseContentType": "application/json", "filterString": ""}]}
        return self._req("POST", f"{NSITE}/ss/explorersites", json=body) or {}

    def sites(self, term="", filters=None, box=MI_BOX, depth=0):
        """{site id: row}. A cluster too large to list its sites is searched again in
        four smaller boxes."""
        d = self.search(term, filters, box)
        out, split = {}, False
        for x in d.get("insertUpdateList") or []:
            out.update(cluster_rows(x))
            if x.get("clusterCount") and not x.get("clusterSites"):
                split = True
        if split and depth < 8:
            a, b, c, e = box
            m, n = (a + b) / 2, (c + e) / 2
            for bx in ((a, m, c, n), (a, m, n, e), (m, b, c, n), (m, b, n, e)):
                out.update(self.sites(term, filters, bx, depth + 1))
        return out

    def profile(self, path, site_id, extra=None):
        q = json.dumps({"filter": [{"id": str(site_id), **(extra or {})}]})
        d = self._req("GET", f"{PROFILES}/{path}", params={
            "queryParams": q, "responseContentType": "application/json",
            "includeMetadataInResponse": "false", "loadChildren": "true"})
        return (d or {}).get("queryResults") or []

    def header(self, site_id):
        q = json.dumps({"filter": [{"id": str(site_id)}]})
        d = self._req("GET", f"{NSITE}/ss/explorersiteheader", params={
            "queryParams": q, "responseContentType": "application/json",
            "includeMetadataInResponse": "false", "loadChildren": "true"})
        rows = (d or {}).get("queryResults") or []
        return rows[0] if rows else {}

    def notices(self):
        """MiEnviro air public notices open now, each with its documents."""
        d = self._req("GET", f"{NCORE}/ss/publicnoticeslist", params={
            "queryParams": json.dumps({"filter": [{"programAreaId": "AQD_AIR"}]}),
            "includeMetadataInResponse": "false"})
        rows = (d or {}).get("queryResults") if isinstance(d, dict) else d
        out = []
        for x in rows or []:
            dd = self._req("GET", f"{NCORE}/ss/publicnoticedocuments", params={
                "PublicNoticeId": x.get("id"), "includeMetadataInResponse": "false"}) or {}
            out.append(mie_notice(x, dd.get("queryResults") or []))
        return out


def cluster_rows(x):
    """Sites of one explorersites row: a single site, or every site a cluster lists."""
    if x.get("clusterCount"):
        try:
            return {c["siteId"]: {"site_id": c["siteId"], "site_name": c["siteName"]}
                    for c in json.loads(x.get("clusterSites") or "[]")}
        except ValueError:
            return {}
    if x.get("siteId"):
        lat, lon = parse_wkt(x.get("geographyWKT"))
        return {x["siteId"]: {"site_id": x["siteId"], "site_name": x.get("siteName") or "",
                              "address": x.get("siteAddress") or "", "city": x.get("city") or "",
                              "zip": x.get("zip") or "", "lat": lat, "lon": lon}}
    return {}


def mie_notice(x, docs):
    name, srn = split_srn(x.get("siteName") or "")
    return {
        "source": "MiEnviro public notice list",
        "facility": name, "srn": srn, "permit": x.get("permitNumber") or "",
        "type": x.get("publicNotificationTypeDescription") or "",
        "start": iso(x.get("startDate")), "end": iso(x.get("endDate")),
        "lat": x.get("latitude"), "lon": x.get("longitude"),
        "text": "", "seen": [time.strftime("%Y-%m-%d")],
        "docs": [{"name": d.get("documentName") or "", "url": f"{NCORE}/downloadpdf/{d['id']}",
                  "date": iso(d.get("updatedDate")), "about": d.get("description") or ""}
                 for d in docs if d.get("id")],
    }


def list_sites(mie, extra_terms=()):
    """Every candidate air site: {site id: {site_id, site_name, name, srn, sources}}."""
    found = {}

    def add(src, rows):
        for sid, r in rows.items():
            f = found.setdefault(sid, {**r, "sources": set()})
            for k, v in r.items():
                if v not in (None, "") and not f.get(k):
                    f[k] = v
            f["sources"].add(src)

    for code in POWER_NAICS:
        rows = mie.sites("", [AIR_SITE, {"attributeName": "1K_Industry NAICS Codes", "attributeValue": code}])
        log(f"air sites with NAICS {code}: {len(rows)}")
        add(f"NAICS {code}", rows)
    for code in POWER_SICS:
        rows = mie.sites("", [AIR_SITE, {"attributeName": "1J_Industry SIC Codes", "attributeValue": code}])
        log(f"air sites with SIC {code}: {len(rows)}")
        add(f"SIC {code}", rows)
    rows = mie.sites("", [ROP_SITES])
    log(f"sites with a Renewable Operating Permit: {len(rows)}")
    add("ROP", rows)
    for term in list(TERMS) + sorted({t for t in extra_terms if t not in TERMS}):
        add(f"name search '{term}'", mie.sites(term, [AIR_SITE]))
    # A plant with water and waste programs too (Campbell, Greenwood, Fermi) is not
    # listed as an air facility, so the watch list and hand-checked SRNs are searched
    # by SRN across every site type. A broad name search without the filter returns
    # thousands of sites and is too slow.
    for srn in sorted(set(WATCH) | known_srns()):
        add(f"SRN search {srn}", mie.sites(srn))
    log(f"{len(found)} sites found by the searches")
    out = {}
    for sid, f in found.items():
        name, srn = split_srn(f["site_name"])
        if not srn:
            continue
        f["name"], f["srn"] = name, srn
        f["sources"] = sorted(f["sources"])
        out[sid] = f
    log(f"{len(out)} of them carry an SRN (air sites)")
    return out


def known_srns():
    """Every SRN named in a hand-checked pattern, upper case."""
    return {m.upper() for pats in KNOWN.values() for p in pats
            for m in re.findall(r"\(([a-z]\d{4})\\\)", p)}


def power_code(f):
    return any(s.startswith(("NAICS", "SIC")) for s in f.get("sources", []))


def read_site(mie, f, full=True):
    """Fill one site from its MiEnviro profile (and, with full, its permits, submissions,
    notices and documents)."""
    h = mie.header(f["site_id"])
    f["address"] = f.get("address") or h.get("siteAddress1") or ""
    f["city"] = f.get("city") or h.get("siteCity") or ""
    f["zip"] = f.get("zip") or h.get("siteZip") or ""
    if not full:
        return f
    det = mie.profile("1-profile/0-site-details", f["site_id"])
    if det:
        f["county"] = det[0].get("siteCnty") or ""
        f["full_address"] = det[0].get("siteAddr") or ""
    codes = mie.profile("1-profile/1-sic-and-naics", f["site_id"])
    f["codes"] = sorted({" ".join(str(v) for k, v in c.items() if v and not k.endswith("Id"))[:120] for c in codes})
    alts = mie.profile("1-profile/4-alternative-names", f["site_id"])
    f["alt_names"] = sorted({f"{a.get('siteAltNameAliasname')} ({a.get('description') or 'alias'})"
                             for a in alts if a.get("siteAltNameAliasname")})
    f["permits"] = [{"number": p.get("prmtPrmtNum") or "", "category": p.get("prmtRefPrmtCatgDescr") or "",
                     "status": p.get("prmtRefPrmtStatDescr") or "", "effective": iso(p.get("prmtEfctvDate")),
                     "expires": iso(p.get("prmtExprDate")), "terminated": iso(p.get("prmtTermDate"))}
                    for p in mie.profile("2-environmental-interests/1-permits", f["site_id"])]
    f["submissions"] = [{"form": s.get("submFormName") or "", "ref": s.get("submSubmRefNum") or "",
                         "status": s.get("submStatus") or "", "received": iso(s.get("submRcvdDate")),
                         "about": scrub(s.get("submDescr") or "")[:300]}
                        for s in mie.profile("2-environmental-interests/2-submissions", f["site_id"])]
    f["site_notices"] = mie.profile("1-profile/2-active-public-notices", f["site_id"])
    f["documents"] = [{"name": d.get("docMgmtDocName") or "", "url": d.get("docMgmtDocurl") or "",
                       "category": d.get("docMgmtCategory") or "", "date": iso(d.get("docMgmtDocRvcdCreatedDate")),
                       "number": d.get("docMgmtSourcenumber") or "", "kind": d.get("docMgmtSourcetype") or ""}
                      for d in mie.profile("4-documents/1-documents", f["site_id"]) if d.get("docMgmtDocurl")]
    if f.get("lat") is None:
        for r in mie.sites(f["srn"], [AIR_SITE]).values():
            if r["site_id"] == f["site_id"] and r.get("lat") is not None:
                f["lat"], f["lon"] = r["lat"], r["lon"]
                f["address"] = f["address"] or r.get("address", "")
                break
    return f


# ------------------------------------------------- the older AQD file server ---

def parse_listing(text, base=APS):
    """Rows of an IIS directory listing: [{date, size or 'dir', url, name}]."""
    out = []
    for m in re.finditer(r"(\d{1,2}/\d{1,2}/\d{4})\s+\d{1,2}:\d{2}\s+[AP]M\s+(&lt;dir&gt;|<dir>|\d+)\s+"
                         r"<A HREF=\"([^\"]+)\">([^<]+)</A>", text or "", re.I):
        url = urljoin(base, m.group(3))
        out.append({"date": iso(m.group(1)), "size": "dir" if "dir" in m.group(2) else int(m.group(2)),
                    "url": url, "name": html.unescape(m.group(4))})
    return out


def legacy_folder(path):
    page = get(f"{APS}/{path}", timeout=90)
    return parse_listing(page.text) if page.status == "200" else []


PTI_ROW = re.compile(r"^(?P<co>\S.{2,}?)\s{2,}(?P<srn>[A-Z]\d{4})?\s{2,}(?P<rest>.*?)\s(?P<pti>\d{1,4}-\d{2}[A-Z]{0,2})\s+"
                     r"(?P<date>\d{1,2}/\d{1,2}/\d{4})(?P<note>.*)$")


def parse_active_ptis(text):
    """Rows of 'Active PTIs by SRN': [{company, srn, place, pti, approved, note, url}]."""
    out = []
    for ln in (text or "").splitlines():
        m = PTI_ROW.match(ln.rstrip())
        if not m or not m.group("srn"):
            continue
        pti = m.group("pti")
        yy = int(pti.split("-")[1][:2])
        year = 1900 + yy if yy >= 60 else 2000 + yy
        out.append({"company": m.group("co").strip(), "srn": m.group("srn"),
                    "place": re.sub(r"\s{2,}", ", ", m.group("rest").strip()), "pti": pti,
                    "approved": iso(m.group("date")), "note": m.group("note").strip(),
                    "url": f"{APS}/permits/finpticon/{year}/{pti}.pdf"})
    return out


def parse_pending_apps(text):
    """Rows of 'Pending PTI Applications': [{company, srn, city, county, app, received, reason}]."""
    out, cur = [], None
    row = re.compile(r"^(?P<co>\S.{2,}?)\s{2,}(?P<srn>[A-Z]\d{4})\s{2,}(?P<mid>.*?)\s{2,}(?P<county>[A-Z][A-Z .]+?)\s{2,}"
                     r"(?P<app>APP-\d{4}-\d{4}|\d{1,4}-\d{2}[A-Z]?)\s+(?P<date>\d{1,2}/\d{1,2}/\d{4})")
    for ln in (text or "").splitlines():
        m = row.match(ln.strip())
        if m:
            mid = re.split(r"\s{2,}", m.group("mid").strip())
            cur = {"company": m.group("co").strip(), "srn": m.group("srn"),
                   "city": mid[1] if len(mid) > 2 else (mid[-1] if mid else ""),
                   "county": m.group("county").strip(), "app": m.group("app"),
                   "received": iso(m.group("date")), "reason": ""}
            out.append(cur)
            continue
        r = re.match(r"\s*Application Reason:\s*(.*)", ln)
        if r and cur is not None:
            cur["reason"] = r.group(1).strip()
    return out


# ------------------------------------------------------- notice lists ---

def snapshots(url, wayback=True, limit=0):
    """[(label, fetch url)]: the live file, then each distinct Wayback copy, newest first."""
    out = [("live", url)]
    if not wayback:
        return out
    seen = set()
    for host in ("www.egle.state.mi.us", "www.deq.state.mi.us"):
        for case in (url, url.replace("_for_", "_For_")):
            try:
                r = requests.get(CDX, params={"url": case.split("://", 1)[-1].replace("www.egle.state.mi.us", host),
                                              "output": "json", "fl": "timestamp,original,digest",
                                              "filter": "statuscode:200", "collapse": "digest", "limit": 500},
                                 timeout=120)
                rows = r.json()[1:]
            except (requests.RequestException, ValueError):
                rows = []
            for ts, orig, dg in rows:
                if dg not in seen:
                    seen.add(dg)
                    out.append((ts[:8], f"https://web.archive.org/web/{ts}id_/{orig}"))
    head, rest = out[:1], sorted(out[1:], reverse=True)
    return head + (rest[:limit] if limit else rest)


def pdf_links(url):
    """Hyperlinks inside a cached PDF, by page: {page index: [uri]}."""
    got = fetch._cache_get(url)
    raw = got[2] if got else b""
    if not raw:
        try:
            r = requests.get(url, headers={"User-Agent": CHROME_UA}, timeout=180)
            raw = r.content if r.status_code == 200 else b""
        except requests.RequestException:
            raw = b""
    if not raw.startswith(b"%PDF"):
        return {}
    try:
        import io

        import pypdf
        rd = pypdf.PdfReader(io.BytesIO(raw))
        out = {}
        for i, p in enumerate(rd.pages):
            for a in p.get("/Annots") or []:
                a = a.get_object()
                uri = (a.get("/A") or {}).get("/URI")
                if uri and not str(uri).startswith("mailto:"):
                    out.setdefault(i, []).append(str(uri))
        return out
    except Exception as e:  # a bad PDF must not stop the harvest
        log(f"could not read the links of {url}: {e}")
        return {}


TOC = re.compile(r"^\s*(?P<h>\S.*?)\s*\.{6,}\s*\d+\s*$")


def parse_notice_list(text, kind, label, links=None):
    """Entries of one AQD notice list PDF: [{facility, ids, text, docs}]. The table of
    contents gives the headings; each heading's body runs to the next heading."""
    lines = (text or "").splitlines()
    heads, prev = [], ""
    for ln in lines[:80]:
        m = TOC.match(ln)
        if m:
            h = m.group("h").strip()
            # a heading that wraps puts its first part on the line above, with no dots
            if prev and not re.search(r"\.{3,}|following|New Source Review|Permits (Open|Pending)|Final Decision", prev):
                h = f"{prev} {h}"
            prev = ""
            if not re.match(r"(submitting comments|types of documents)", h, re.I):
                heads.append(h)
        else:
            prev = ln.strip() if ln.strip() and len(ln.strip()) < 100 else ""
    nth = 2                      # the heading's second appearance starts its body
    if not heads:                # lists before 2021 have no table of contents
        nth = 1
        heads = [m.group(1).strip() for m in re.finditer(
            r"^\s*(\S.{2,90}?\s[–-]\s(?:Permit to Install(?: Application)?(?: No\.?)? ?\S+|APP-\d{4}-\d{4}|"
            r"PKG-\d{7}|PTI\S+)(?: and \S+)?)\s*$", text or "", re.M)]
    # headings that wrap onto a second line in the table of contents
    joined = "\n".join(lines)
    flat = re.sub(r"\s+", " ", joined)
    out = []
    for k, h in enumerate(heads):
        core = re.sub(r"\s+", " ", h)
        key = core[:40]
        starts = [m.start() for m in re.finditer(re.escape(key), flat)]
        body = ""
        if len(starts) >= nth:
            s = starts[nth - 1]
            nxt = len(flat)
            for h2 in heads[k + 1:]:
                pos = [m.start() for m in re.finditer(re.escape(re.sub(r"\s+", " ", h2)[:40]), flat)]
                pos = [p for p in pos if p > s]
                if pos:
                    nxt = min(nxt, pos[0])
                    break
            for stop in ("Submitting Comments", "Types of Documents"):
                p = flat.find(stop, s + len(key))
                if 0 < p < nxt:
                    nxt = p
            body = flat[s:nxt].strip()
        ids = sorted(set(re.findall(r"APP-\d{4}-\d{4}|PKG-\d{7}|PTI\d{7}(?: v\d+\.\d+)?|\b\d{1,4}-\d{2}[A-Z]?\b(?=\D)",
                                    core + " " + body[:600], re.I)))
        fac = re.split(r"\s+[–-]\s+(?=(?:Permit|PKG|APP|PTI|\d))", core)[0].strip()
        out.append({"source": f"AQD {kind} list", "facility": fac, "heading": core, "ids": ids,
                    "text": scrub(body[:1500]), "seen": [label], "docs": []})
    # document links: a link belongs to the entry whose id is in its folder name, else to
    # every entry when the list has just one
    for uris in (links or {}).values():
        for u in uris:
            if "/PubNotice/" not in u and "/finpticon/" not in u and "mienviro" not in u:
                continue
            tgt = [e for e in out if any(i.lower() in u.lower() for i in e["ids"] if len(i) > 5)]
            if not tgt and len(out) == 1:
                tgt = out
            for e in tgt:
                if u not in [d["url"] for d in e["docs"]]:
                    e["docs"].append({"name": unquote(u.rsplit("/", 1)[-1]), "url": u})
    return out


def read_notice_lists(wayback=True, limit=0):
    recs = []
    for fname in NOTICE_LISTS:
        kind = {"NSR_PTIs_Open_for_Comment.pdf": "open for comment", "NSR_PTIs_Pending_Decision.pdf":
                "pending decision", "NSR_PTIs_Final_Decisions.pdf": "final decisions"}[fname]
        snaps = snapshots(f"{APS}/permits/PubNotice/{fname}", wayback, limit)
        n = 0
        for label, url in snaps:
            page = get(url, timeout=180)
            if page.status != "200" or not page.text.strip():
                continue
            if label == "live":
                label = time.strftime("%Y%m%d")
                m = re.search(r"Rev\. (\d{1,2}/\d{1,2}/\d{4})", page.text)
                if m:
                    label = iso(m.group(1)).replace("-", "")
            n += 1
            for e in parse_notice_list(page.text, kind, label, pdf_links(url)):
                e["list_url"] = url
                recs.append(e)
        log(f"AQD notice list '{kind}': {n} copies read")
    return merge_notices(recs)


def merge_notices(recs):
    """One record per facility and heading, with every list copy it was seen in."""
    out = {}
    for r in recs:
        k = (r["source"], r["heading"].lower()[:80])
        if k not in out:
            out[k] = {**r, "seen": set(r["seen"]), "docs": list(r["docs"])}
        else:
            o = out[k]
            o["seen"] |= set(r["seen"])
            o["text"] = o["text"] or r["text"]
            for d in r["docs"]:
                if d["url"] not in [x["url"] for x in o["docs"]]:
                    o["docs"].append(d)
    return list(out.values())


def legacy_notice_folders(wayback=True):
    """Names of the old per-application notice folders the Wayback Machine saw:
    {folder: [saved file urls]}."""
    if not wayback:
        return {}
    out = {}
    for host in ("www.egle.state.mi.us", "www.deq.state.mi.us"):
        try:
            r = requests.get(CDX, params={"url": f"{host}/aps/downloads/permits/PubNotice/", "matchType": "prefix",
                                          "output": "json", "fl": "timestamp,original", "filter": "statuscode:200",
                                          "collapse": "urlkey", "limit": 20000}, timeout=180)
            rows = r.json()[1:]
        except (requests.RequestException, ValueError):
            rows = []
        for ts, orig in rows:
            m = re.search(r"/PubNotice/([^/]+)/([^/?]+\.(?:pdf|docx?))$", orig, re.I)
            if m:
                out.setdefault(m.group(1), []).append(f"https://web.archive.org/web/{ts}id_/{orig}")
    log(f"older notice folders seen by the Wayback Machine: {len(out)}")
    return out


# ------------------------------------------------------------- match, facts ---

def is_power(f):
    """A site looks like a power or data center site: on the watch list, a power NAICS or
    SIC code, or a power-like name that is not on the drop list."""
    if f.get("srn") in WATCH:
        return True
    if POWER_DROP.search(f["name"]) and not power_code(f):
        return False
    return power_code(f) or bool(POWER_NAME.search(f["name"]))


def fac_text(f):
    return f"{f['name']} ({f.get('srn', '')}) | {f.get('city', '')}".lower()


def match(plant, facs):
    """[(facility, how)]: hand-checked patterns alone, else every distinctive word of the
    plant's name, or its city plus a power-like name."""
    out = []
    pats = KNOWN.get(plant["id"])
    if pats is not None:
        for f in facs:
            t = fac_text(f)
            if any(re.search(p, t) for p in pats if not p.startswith("?")):
                out.append((f, "checked by hand"))
            elif any(re.search(p[1:], t) for p in pats if p.startswith("?")):
                out.append((f, "checked by hand as a possible site, check it is this plant"))
        return out
    ws = plant["name_words"]
    city = plant["city"].lower()
    for f in facs:
        t = fac_text(f)
        if ws and ws <= words(t):
            out.append((f, "name match, check it is this plant"))
        elif city and (f.get("city") or "").lower() == city and is_power(f):
            out.append((f, "same city, power-like name, check it is this plant"))
    return out


def lines_of(text):
    return [re.sub(r"\s+", " ", ln).strip() for ln in text.splitlines()]


def pick(text, rx, limit, lo=12, hi=260):
    out = []
    for s in lines_of(text):
        if rx.search(s) and lo < len(s) < hi and s not in out:
            out.append(s)
            if len(out) >= limit:
                break
    return out


def doc_facts(text):
    latlon = [f"{a}, -{c}" for a, _, c in LATLON.findall(text)][:3]
    return {
        "ids": sorted({re.sub(r"\s+", " ", x) for x in PERMIT_NO.findall(text)})[:8],
        "project": pick(text, PROJECT, 6),
        "equipment": pick(text, EQUIPMENT, 10),
        "makers": pick(text, MAKER, 8),
        "sizes": pick(text, SIZE, 10),
        "location": pick(text, LOCATION, 8),
        "coords": latlon,
    }


def doc_rank(d):
    """Lower is read first. Key permit documents, then applications, then the rest."""
    n, c, k = d["name"].lower(), d.get("category", "").lower(), d.get("kind", "").lower()
    if re.search(r"enforcement|testing|schedule", c) or re.search(r"test|cems|violation|schedule", k):
        return 9
    if re.search(r"fact sheet|project summary|staff report|proposed permit|draft|public notice|notice of", n):
        return 0
    if "permit to install documents" in c:
        return 1
    if "rop documents" in c:
        return 2
    if "application" in c or "application" in k:
        return 3
    if "full compliance evaluation" in k:
        return 4
    return 9


def fac_docs(f, notices, legacy_ptis, cap):
    """The documents to read for one site, newest first within each rank, at most `cap`.
    Each is {name, url, date, why}."""
    docs, seen = [], set()

    def add(name, url, date, why):
        if url and url not in seen and not SKIP_DOC.search(name):
            seen.add(url)
            docs.append({"name": name, "url": url, "date": date or "", "why": why})

    for r in notices:
        for d in r["docs"]:
            add(d["name"], d["url"], d.get("date") or (sorted(r["seen"])[-1] if r.get("seen") else ""),
                f"{r['source']}, {r.get('type') or r.get('heading', '')}")
    mdocs = sorted((d for d in f.get("documents", []) if doc_rank(d) < 9),
                   key=lambda d: (doc_rank(d), "" if d["date"] else "0", d["date"]), reverse=False)
    mdocs = sorted(mdocs, key=lambda d: d["date"], reverse=True)
    mdocs = sorted(mdocs, key=doc_rank)
    fce = 0
    for d in mdocs:
        if doc_rank(d) == 4:
            fce += 1
            if fce > 1:
                continue
        add(d["name"], d["url"], d["date"], f"MiEnviro {d['category']} ({d['number']})")
    have_numbers = " ".join(d["name"] + " " + d.get("number", "") for d in f.get("documents", []))
    for p in sorted(legacy_ptis, key=lambda p: p["approved"], reverse=True)[:4]:
        if p["pti"] not in have_numbers:
            add(f"PTI {p['pti']} approved {p['approved']}", p["url"], p["approved"], "AQD final PTI file")
    for x in sorted(f.get("legacy_rop", []), key=lambda x: x["date"], reverse=True):
        if re.search(r"staff report|final", x["name"], re.I) and x["name"].lower().endswith(".pdf"):
            add(x["name"], x["url"], x["date"], "AQD ROP notice folder")
    return docs[:cap], docs[cap:]


def wayback_url(url):
    """Newest saved copy of an address (id_ form, so the original bytes), or ''."""
    for i in range(3):
        try:
            r = requests.get(CDX, params={"url": url.split("://", 1)[-1], "output": "json",
                                          "fl": "timestamp,original", "filter": "statuscode:200",
                                          "limit": 5}, timeout=120)
            rows = r.json()[1:]
            if not rows:
                return ""
            ts, orig = max(rows)
            return f"https://web.archive.org/web/{ts}id_/{orig}"
        except (requests.RequestException, ValueError):
            time.sleep(8 * (i + 1))
    return ""


def read_docs(docs):
    """Download documents and keep facts. Each doc is {name, url}."""
    for d in docs:
        if "web.archive.org" in d["url"]:
            page = get(d["url"], timeout=300)
        else:
            page = get(d["url"], timeout=300)
        ok = page.status == "200" and bool(page.text.strip())
        via = ""
        if not ok and "web.archive.org" not in d["url"]:
            snap = wayback_url(d["url"])
            if snap:
                page = get(snap, timeout=300)
                if page.status == "200" and page.text.strip():
                    ok, via = True, f" (from the Wayback copy {snap})"
                    d["archive"] = snap
        d["state"] = f"saved{via}" if ok else f"not saved, HTTP {page.status}"
        d["facts"] = doc_facts(page.text) if ok else {}


# ---------------------------------------------------------------- reporting ---

def notice_line(r):
    seen = sorted(r.get("seen") or [])
    when = f", comments {r['start']} to {r['end']}" if r.get("end") else ""
    span = f", on the list {seen[0]} to {seen[-1]}" if seen and r["source"].startswith("AQD") else ""
    return f"{r['source']}: {r.get('type') or r.get('heading', '')}{when}{span}"


def fac_block(f, how=None):
    L = [f"- {f['name']} (SRN {f['srn']}, MiEnviro site {f['site_id']}): "
         f"{f.get('full_address') or ', '.join(x for x in (f.get('address'), f.get('city')) if x)}"
         + (f", {f['county']} County" if f.get("county") else "")]
    if f.get("lat") is not None:
        L.append(f"    - MiEnviro map point: {f['lat']}, {f['lon']} "
                 f"(https://www.google.com/maps?q={f['lat']},{f['lon']})")
    if f.get("codes"):
        L.append(f"    - industry codes: {'; '.join(f['codes'][:6])}")
    if f.get("alt_names"):
        L.append(f"    - other names: {'; '.join(f['alt_names'][:8])}")
    L.append(f"    - found by: {', '.join(f.get('sources', [])[:6])}")
    if f.get("srn") in WATCH:
        L.append(f"    - on the watch list: {WATCH[f['srn']]}")
    for p in sorted(f.get("permits", []), key=lambda p: p["effective"], reverse=True):
        if "air" not in p["category"].lower():
            continue
        dates = ", ".join(x for x in (f"effective {p['effective']}" if p["effective"] else "",
                                      f"expires {p['expires']}" if p["expires"] else "",
                                      f"ended {p['terminated']}" if p["terminated"] else "") if x)
        L.append(f"    - permit: {p['category']} {p['number']}, {p['status']}" + (f", {dates}" if dates else ""))
    for s in sorted(f.get("submissions", []), key=lambda s: s["received"], reverse=True)[:15]:
        if re.search(r"application|permit change|notification of change|rescission|void", s["form"], re.I):
            L.append(f"    - submission {s['received'] or 'no date'}: {s['form']} {s['ref']}, {s['status']}"
                     + (f": {s['about']}" if s["about"] else ""))
    for p in sorted(f.get("legacy_ptis", []), key=lambda p: p["approved"], reverse=True)[:12]:
        L.append(f"    - active PTI on the AQD list: {p['pti']} approved {p['approved']}"
                 + (f" ({p['note']})" if p["note"] else "") + f": {p['url']}")
    for a in f.get("pending_apps", []):
        L.append(f"    - pending PTI application at the end of 2024: {a['app']} received {a['received']}: {a['reason']}")
    for r in f.get("notices", []):
        L.append(f"    - public notice: {notice_line(r)}")
        if r.get("text"):
            L.append(f"        - says: {r['text'][:500]}")
    lf = f.get("legacy_files", [])
    if lf:
        kinds = {}
        for x in lf:
            k = re.sub(r"^[A-Z]\d{4}_|_?\d{8}.*$|\.pdf$", "", x["name"]) or "file"
            kinds.setdefault(k, []).append(x)
        L.append(f"    - AQD file server folder {APS}/SRN/{f['srn']}/: "
                 + "; ".join(f"{k} x{len(v)} (newest {max(x['date'] for x in v)})" for k, v in sorted(kinds.items())))
    for x in f.get("legacy_rop", []):
        L.append(f"    - AQD ROP notice folder file {x['date']}: {x['name']}: {x['url']}")
    for d in f.get("docs", []):
        L.append(f"    - document ({d.get('state', 'not read')}), {d.get('date') or 'no date'}, {d['why']}: {d['name']}: {d['url']}")
        fa = d.get("facts") or {}
        for key, label in (("ids", "permit numbers"), ("project", "project"), ("equipment", "equipment"),
                           ("makers", "maker or model"), ("sizes", "size"),
                           ("location", "site address or location"), ("coords", "coordinates")):
            for line in fa.get(key, []):
                L.append(f"        - {label}: {line if isinstance(line, str) else ', '.join(line)}")
    rest = f.get("docs_not_read", [])
    if rest:
        L.append(f"    - {len(rest)} more key documents not read this run (cap): "
                 + "; ".join(f"{d['name']} {d['url']}" for d in rest[:10]))
    n_all = len(f.get("documents", []))
    if n_all:
        L.append(f"    - MiEnviro holds {n_all} documents for this site in all (tests, reports, inspections "
                 f"included); open the site in the Map Explorer to see them.")
    if how:
        L.insert(0, f"Matched: {how}.")
    return L


def write_index(path, plant, matched):
    L = [f"# Michigan air permit files for {plant['name']} ({plant['id']})", "",
         "Source: EGLE Air Quality Division records in the MiEnviro Portal (Map Explorer site profile: permits, "
         "submissions, notices, documents), the AQD file server (final PTI files, the active PTI and pending "
         "application lists, ROP notice folders, inspection folders) and the AQD notice lists, now and in Wayback "
         "copies. Documents marked saved are in the local fetch cache, so `python scripts/fetch.py <url> --text` "
         "and `url_verifier.py` read them at once.", "",
         f"Harvested: {time.strftime('%Y-%m-%d %H:%M %Z')}", "",
         f"GEM statuses: {', '.join(plant['statuses'])}. City in GEM: {plant['city'] or 'blank'}."
         + (f" Other names in GEM: {'; '.join(plant['other_names'])}." if plant["other_names"] else ""), ""]
    if not matched:
        L += ["No MiEnviro air site matched this plant by name. That does not mean it has no permits: a "
              "proposed plant often has no air site until its first application, and an existing one may be "
              "listed under the owner or an older site name. Check _unmatched.md and _notices.md in this folder.", ""]
    for f, how in matched:
        L += fac_block(f, how) + [""]
    path.write_text("\n".join(L), encoding="utf-8")


# ----------------------------------------------------------------- plants ---

def load_plants(args):
    csv = pd.read_csv(CSV, low_memory=False)
    csv = csv[csv["State/Province"] == "Michigan"]
    wanted = set(args.plants.split(",")) if args.plants else None
    plants = []
    for pid, rows in csv.groupby("GEM location ID", sort=False):
        if wanted is not None and pid not in wanted:
            continue
        r = rows.iloc[0]
        others = [x.strip() for x in str(r.get("Other Name(s)") or "").split(";")
                  if x.strip() and x.strip() != "nan"]
        city = r.get("City") if isinstance(r.get("City"), str) else ""
        plants.append({"id": pid, "name": r["Plant name"], "city": city, "other_names": others,
                       "statuses": sorted(set(rows["Status"].astype(str))),
                       "name_words": words(r["Plant name"])})
    return plants


def notice_matches(f, r):
    """True when a notice record is about this site: same SRN, the SRN in its text, or
    every distinctive word of one name found in the other."""
    if r.get("srn"):
        return r["srn"] == f["srn"]
    if re.search(rf"\b{f['srn']}\b", r.get("text") or ""):
        return True
    sw, hw = words(f["name"]), words(r.get("facility") or "")
    return bool(sw and hw) and (sw <= hw or hw <= sw)


def slim(f):
    keys = ("site_id", "srn", "name", "address", "full_address", "city", "zip", "county", "lat", "lon",
            "sources", "codes", "alt_names", "permits", "submissions", "legacy_ptis", "pending_apps", "legacy_rop")
    out = {k: f.get(k) for k in keys}
    out["notices"] = [{k: (sorted(v) if isinstance(v, set) else v) for k, v in r.items() if k != "text"}
                      for r in f.get("notices", [])]
    out["docs"] = f.get("docs", [])
    out["documents_total"] = len(f.get("documents", []))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--scope", required=True, help="batch folder name, e.g. us-mi")
    ap.add_argument("--plants", help="comma-separated GEM location IDs (default: every plant)")
    ap.add_argument("--match-only", action="store_true", help="list matches, download no documents")
    ap.add_argument("--no-wayback", action="store_true", help="skip the archive copies of the notice lists")
    ap.add_argument("--snapshots", type=int, default=0, help="read only the newest N copies of each list (0 = all)")
    ap.add_argument("--docs-per-facility", type=int, default=15, help="documents read per matched site")
    ap.add_argument("--docs-per-unmatched", type=int, default=6, help="documents read per unmatched site")
    args = ap.parse_args()

    pace_michigan_hosts()
    out_dir = REPO / "work" / "permits" / args.scope
    out_dir.mkdir(parents=True, exist_ok=True)
    hv_dir = REPO / "batches" / args.scope / "harvest"
    hv_dir.mkdir(parents=True, exist_ok=True)
    plants = load_plants(args)

    mie = Mie()
    extra = [w for p in plants for w in list(p["name_words"]) + p["other_names"]]
    facs = list_sites(mie, extra)
    cands = {sid: f for sid, f in facs.items()
             if is_power(f) or any(any(re.search(p.lstrip("?"), fac_text(f)) for p in pats) for pats in KNOWN.values())}
    log(f"{len(cands)} air sites look like power or data center sites, or match a hand-checked pattern")
    for k, f in enumerate(cands.values(), 1):
        read_site(mie, f, full=False)
    matches = {p["id"]: match(p, list(cands.values())) for p in plants}
    matched_ids = {f["site_id"] for ms in matches.values() for f, _ in ms}
    power = [f for f in cands.values() if is_power(f) or f["site_id"] in matched_ids]
    unmatched = [f for f in power if f["site_id"] not in matched_ids]
    log(f"{len(power)} power-like sites: {len(matched_ids)} matched to GEM plants, {len(unmatched)} unmatched")

    if args.match_only:
        for p in plants:
            for f, how in matches[p["id"]] or [({"name": "no match", "srn": "", "city": ""}, "")]:
                print(f"{p['id']}\t{p['name']}\t{f['name']}\t{f['srn']}\t{f.get('city', '')}\t{how}")
        for f in sorted(unmatched, key=lambda f: f["name"]):
            print(f"UNMATCHED\t\t{f['name']}\t{f['srn']}\t{f.get('city', '')}\t{', '.join(f['sources'][:3])}")
        return

    # the older file server lists and the notices
    page = get(f"{APS}/permits/finpticon/Active%20PTIs%20by%20SRN.pdf", timeout=300)
    active_ptis = parse_active_ptis(page.text) if page.status == "200" else []
    page = get(f"{APS}/permits/finpticon/Pending%20PTI%20Applications.pdf", timeout=300)
    pending = parse_pending_apps(page.text) if page.status == "200" else []
    log(f"AQD lists: {len(active_ptis)} active PTIs, {len(pending)} pending applications")
    mnotices = mie.notices()
    log(f"MiEnviro air notices open now: {len(mnotices)}")
    lnotices = read_notice_lists(wayback=not args.no_wayback, limit=args.snapshots)
    log(f"AQD notice list entries: {len(lnotices)}")
    folders = legacy_notice_folders(wayback=not args.no_wayback)
    notices = mnotices + lnotices

    for k, f in enumerate(power, 1):
        read_site(mie, f, full=True)
        f["legacy_files"] = legacy_folder(f"SRN/{f['srn']}/")
        f["legacy_rop"] = [x for x in legacy_folder(f"rop/Pub_ntce/{f['srn']}/") if x["size"] != "dir"]
        f["legacy_ptis"] = [p for p in active_ptis if p["srn"] == f["srn"]]
        f["pending_apps"] = [a for a in pending if a["srn"] == f["srn"]]
        f["notices"] = [r for r in notices if notice_matches(f, r)]
        for r in f["notices"]:
            for fid in r.get("ids", []):
                for folder, urls in folders.items():
                    if fid.lower() in folder.lower():
                        for u in urls:
                            if u not in [d["url"] for d in r["docs"]]:
                                r["docs"].append({"name": unquote(u.rsplit("/", 1)[-1]), "url": u})
        cap = args.docs_per_facility if f["site_id"] in matched_ids else args.docs_per_unmatched
        f["docs"], f["docs_not_read"] = fac_docs(f, f["notices"], f["legacy_ptis"], cap)
        log(f"({k}/{len(power)}) {f['name']} ({f['srn']}): {len(f.get('permits', []))} permits, "
            f"{len(f.get('documents', []))} MiEnviro documents, reading {len(f['docs'])}")
        read_docs(f["docs"])

    logf = (out_dir / "harvest_log.jsonl").open("a", encoding="utf-8")
    for p in plants:
        write_index(out_dir / f"{p['id']}.md", p, matches[p["id"]])
        logf.write(json.dumps({
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "plant": p["id"], "name": p["name"],
            "facilities": [{"name": f["name"], "srn": f["srn"], "site_id": f["site_id"], "how": how,
                            "permits": len(f.get("permits", [])),
                            "docs": {d["name"]: d.get("state", "not read") for d in f.get("docs", [])}}
                           for f, how in matches[p["id"]]],
            "procedures": [{"procedure": f"MiEnviro site point, SRN {f['srn']}", "lat": f.get("lat"),
                            "lon": f.get("lon")} for f, how in matches[p["id"]] if f.get("lat") is not None],
        }) + "\n")
    logf.close()

    L = ["# Michigan air sites that look like power or data center sites but match no GEM plant in this batch", "",
         "Each may be a plant outside this batch, a plant GEM lacks, a backup generator at a site that is not "
         "a power plant, or not a power plant at all. Check engines or turbines of 50 MW or more in total "
         "(generating capacity only).", ""]
    for f in sorted(unmatched, key=lambda f: (not power_code(f), f["name"])):
        L += fac_block(f) + [""]
    if not unmatched:
        L.append("None this run.")
    (out_dir / "_unmatched.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    L = [f"# Michigan air permit notices: MiEnviro now, and the AQD notice lists now and in archive copies "
         f"({len(notices)} records)", "",
         "Power-like entries first. Every entry is listed, since a new plant may appear under its developer's name.", ""]
    for r in sorted(notices, key=lambda r: (not POWER_NAME.search(r.get("facility", "") + " " + r.get("text", "")[:300]),
                                            -int((sorted(r.get("seen") or ["0"])[-1]).replace("-", "")[:8] or 0))):
        L.append(f"- {r['facility']}" + (f" ({r['srn']})" if r.get("srn") else "") + f": {notice_line(r)}")
        if r.get("text"):
            L.append(f"    - says: {r['text'][:400]}")
        for d in r["docs"][:12]:
            L.append(f"    - {d['name']}: {d['url']}")
    (out_dir / "_notices.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    acts = []
    for f in power:
        for s in f.get("submissions", []):
            if re.search(r"application|permit change|rescission|void", s["form"], re.I):
                acts.append({"date": s["received"], "srn": f["srn"], "facility": f["name"],
                             "text": f"{s['form']} {s['ref']}, {s['status']}" + (f": {s['about']}" if s["about"] else ""),
                             "source": "MiEnviro submissions"})
        for p in f.get("permits", []):
            if "air" in p["category"].lower() and p["effective"] >= "2020":
                acts.append({"date": p["effective"], "srn": f["srn"], "facility": f["name"],
                             "text": f"{p['category']} {p['number']} effective, now {p['status']}",
                             "source": "MiEnviro permits"})
    power_srns = {f["srn"] for f in power}
    for a in pending:
        if a["srn"] in power_srns or re.search(r"turbine|generat|power|electric|combined heat|chp|cogen|data cent",
                                               a["reason"] + " " + a["company"], re.I):
            acts.append({"date": a["received"], "srn": a["srn"], "facility": a["company"],
                         "text": f"pending PTI application {a['app']} ({a['city']}, {a['county']} County): {a['reason']}",
                         "source": "AQD pending PTI list, end of 2024"})
    acts.sort(key=lambda a: a["date"] or "", reverse=True)
    L = ["# Michigan air applications and permit actions of power-like sites since 2020, newest first", "",
         "Includes pending applications at the end of 2024 from the AQD list whose reason names turbines, "
         "generators, power or data centers, even at sites not listed as power-like.", ""]
    for a in acts:
        if (a["date"] or "") >= "2020":
            L.append(f"- {a['date'] or 'no date'}: {a['facility']} ({a['srn']}): {a['text']} [{a['source']}]")
    (out_dir / "_activity.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    (hv_dir / "facilities.json").write_text(json.dumps({
        "harvested": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "matches": {p["id"]: {"name": p["name"], "facilities": [{"srn": f["srn"], "site_id": f["site_id"],
                                                                  "name": f["name"], "how": how}
                                                                 for f, how in matches[p["id"]]]} for p in plants},
        "unmatched": [slim(f) for f in unmatched],
        "matched": [slim(f) for f in power if f["site_id"] in matched_ids]}, indent=1), encoding="utf-8")
    (hv_dir / "notices.json").write_text(json.dumps(
        [{**r, "seen": sorted(r.get("seen") or [])} for r in notices], indent=1), encoding="utf-8")
    (hv_dir / "activity_air.json").write_text(json.dumps(acts, indent=0), encoding="utf-8")
    (hv_dir / "pti_lists.json").write_text(json.dumps({
        "active_ptis_power_sites": [p for p in active_ptis if p["srn"] in power_srns],
        "pending_applications": pending}, indent=1), encoding="utf-8")

    S = [f"# Michigan air permit harvest, {time.strftime('%Y-%m-%d')}", "",
         f"Air sites found by the searches: {len(facs)}. Power-like: {len(power)}. "
         f"Matched to GEM plants: {len(matched_ids)}. Unmatched: {len(unmatched)}.", "",
         f"MiEnviro air notices open now: {len(mnotices)}. AQD notice list entries (now and archive copies): "
         f"{len(lnotices)}. Older notice folders seen by the Wayback Machine: {len(folders)}. "
         f"AQD active PTIs: {len(active_ptis)}. Pending applications at the end of 2024: {len(pending)}. "
         f"MiEnviro service calls: {mie.calls}.", "",
         "## Matches per GEM plant", ""]
    for p in plants:
        ms = matches[p["id"]]
        S.append(f"- {p['name']} ({p['id']}): " + (
            "; ".join(f"{f['name']} ({f['srn']}, {how}, {len(f.get('permits', []))} permits, "
                      f"{len([d for d in f.get('docs', []) if d.get('state', '').startswith('saved')])} documents read)"
                      for f, how in ms) if ms else "no site matched"))
    S += ["", "## Unmatched power-like facilities", ""]
    for f in sorted(unmatched, key=lambda f: (not power_code(f), f["name"])):
        S.append(f"- {f['name']} ({f['srn']}), {f.get('city', '')}" + (f", {f['county']} County" if f.get("county") else "")
                 + (", power or data center industry code" if power_code(f) else "")
                 + (f", watch list: {WATCH[f['srn']]}" if f.get("srn") in WATCH else ""))
    (hv_dir / "harvest_summary.md").write_text("\n".join(S) + "\n", encoding="utf-8")
    log("done")


if __name__ == "__main__":
    main()

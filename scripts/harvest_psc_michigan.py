"""Michigan Public Service Commission cases on gas and oil generation, resource plans and retirements (pre-sweep step for scope us-mi).

    python harvest_psc_michigan.py [--from-year 2022] [--no-docs] [--match-only FILE]

Lists every case on the Commission's E-Dockets site from a start year on, keeps
the electric cases about generation (integrated resource plans, certificates of
necessity, plant purchases, retirements, data center special contracts and any
case whose title names a gas plant), reads the key documents of each and writes
the facts a plant brief needs: plant name, megawatts, technology, turbine maker
and model, in-service year, retirement years, county and township, the lines of
resource-plan tables that name a plant, and the filing and page where each GEM
plant appears.

What was found per source (2026-10-23):

E-Dockets, `https://mi-psc.my.site.com/s/` (the "E-Dockets Community"). It is a
Salesforce Experience site open to guests. No sign-in, no Cloudflare gate, no
Chrome needed: plain curl with a browser User-Agent gets every answer below. The
page itself is a script shell, so the data comes from the site's own Aura calls,
which this script replays:
  1. GET `/s/` once. Its URL-encoded boot links carry the framework id (`fwuid`)
     and the app version for `siteforce:communityApp`. A stale pair still
     answers SUCCESS with a warning, so the values found on 2026-10-23 are kept
     as a fallback.
  2. POST `/s/sfsites/aura?r=1` with form fields `message` (one action:
     descriptor plus params, JSON), `aura.context` (mode PROD, fwuid, app,
     loaded), `aura.pageURI=/s/` and `aura.token=null`. The answer is JSON,
     sometimes led by `*/`.
  3. Case list: the list view controller
     `ListViewDataManagerController/ACTION$getItems` with list filter
     `00Bt0000000S9OxEAK` (all cases), pageSize 500, offset 0, 500, ... It holds
     6,719 cases sorted newest open date first. Each page lists record ids; the
     case fields (CaseNumber, Open_Date__c, Subject, the company and
     Industry__c) come in the `$Record` value provider of the same answer. The
     list stops at offset 2,500, which reaches back to 2016, so every case
     opened 2019 or later is listed. A page sometimes comes back without
     records; a retry fixes it.
  4. Case detail: `apex://CaseRecordDetailCompCtrl/ACTION$getCaseRecordDetails`
     with the case record id gives Status (Open or Closed) and Type (for example
     "Integrated Resource Plan"). It also carries a staff contact's phone and
     email, which this script drops.
  5. Filings: `apex://CaseFilingsRelatedListCompCtrl/ACTION$getCaseFilings`
     returns every filing of a case in one answer (U-21090, the 2021 Consumers
     plan, has 942): filing number (U-21090-0901), filing type (Application,
     Application - Ex Parte, Exhibits, Testimony and Exhibits, Order, Other and
     so on), date, description, page count, who filed it and the download link.
     A page count of 0 means the document is sealed or not public; it is skipped.
     The Commission's orders are filings of type Order in the same list (the
     separate orders list answered empty for the cases tried).
  6. Each document downloads with a plain GET of
     `https://mi-psc.my.site.com/sfc/servlet.shepherd/version/download/068...`,
     no cookie, PDF answer. That link and the case page
     `https://mi-psc.my.site.com/s/case/<record id>` are stable and citable.
     Large filings are big: the 2026 Consumers application part 1
     (U-22127-0009) is 685 pages and 20 MB, and downloads in about a second.
  7. Search box: `ScopedResultsDataProviderController/ACTION$getItems` with
     scope Filing__c (or Case) and a term, pageSize 50, paged by currentPage
     while moreResultsAvailable is true. It matches words in the filing
     description, not the document text. This script searches plant names and
     words such as "combustion turbine" and "special contract", and reads the
     filings it finds alongside each case's own key filings.
  Limits: sealed exhibits are not public (`Public__c` false or
  `Confidential__c` other than "No"; "No" is the normal value). The list is
  by open date, so a case opened before 2019 is read only when it is in
  `PRIORITY_CASES` or a 2022 or later filing in it turns up in the search.
  Case numbers that are skipped in the list are not found by the site's own
  search either, so they are unused or not public.

Cases read in full on the first run (2026-10-23), with what they hold:
  U-21090 (Consumers Energy plan, 2021): the purchase of the New Covert
  Generating Facility on or about May 31, 2023 for $815 million, and of the
  Dearborn Industrial Generation, Kalamazoo and Livingston plants in 2025.
  U-22127 (Consumers Energy plan and certificates of necessity, 2026): a
  456 MW simple-cycle gas plant at the Karn site in Essexville, Bay County, and
  a 919 MW simple-cycle gas plant at the Thetford site in Genesee County;
  Karn Units 3 and 4 run through May 2031; an early 2040 retirement of Zeeland
  and of Covert is a modeled sensitivity, not the plan. U-22168 (DTE Electric
  plan, 2026): the Livingston County Project, a nominal 1,400 MW combined cycle
  plant in Handy Township, in service by the end of 2031; the Monroe County
  Project, a nominal 700 MW combined cycle plant in Milan Township, by the end
  of 2032; buying the 138 MW Michigan Power Cogeneration plant in Ludington from
  DTE Sustainable Generation in 2030; Belle River Unit 1 converted to gas in
  2025, the whole plant a gas peaker by the end of 2026 and retired in 2039;
  Monroe Units 3 and 4 retire in 2028 and Units 1 and 2 in 2032; the Superior
  Peaking Station retires in 2032. U-21193 (DTE Electric plan, 2022). U-21081
  and U-21542 (Upper Michigan Energy Resources): Mihm, three Wartsila 18V50SG
  engines, 54.9 MW, and Kuester, 125.6 MW. U-21990 and U-22058 (DTE data center
  special contracts): an Oracle data center near Saline of about 1.4 GW and a
  Google data center in Van Buren Township of about 1.0 GW; neither names a
  power plant of its own. U-22175 (Upper Michigan Energy Resources plan, 2026)
  and U-22069 (Indiana Michigan Power plan, 2026) held only notices and orders
  on schedule so far. The matched plants, facts and pages are in the output
  files.

Output (batches/us-mi/harvest/): `psc_dockets.json` and `psc_dockets.md`, the
same shape as the Mississippi harvest, so `build_state_brief.py --harvest` reads
them. Each matched plant carries the filings and pages where it is named.
Documents and their text go to `work/psc_mi/<case>/` (never committed). A PDF
over `--drop-pdfs-over` megabytes is deleted once its text is saved, since its
download link is stable. `--match-only FILE` re-matches a saved
psc_dockets.json against the saved text, no network; `--no-docs` lists cases
without downloading documents.
"""

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch import CHROME_UA  # noqa: E402
from harvest_psc_mississippi import MAKER, SIZE, YEAR, merge_facts, sentences  # noqa: E402
from ms_match import REPO, clean_ws  # noqa: E402
from pull_queues import load_plants as load_state_plants  # noqa: E402

SITE = "https://mi-psc.my.site.com"
HOME = f"{SITE}/s/"
AURA = f"{SITE}/s/sfsites/aura?r=1"
LIST_FILTER = "00Bt0000000S9OxEAK"
OUT = REPO / "batches" / "us-mi" / "harvest"
WORK = REPO / "work" / "psc_mi"
LIST_START = 2019            # cases opened this year or later are always listed and classified

FALLBACK_FWUID = "ZVYtV2g3NHN0UGNVNzBMbldfZ0ZwZ2tVMjdnTGFERUU2S3FfSVdrcU92bkExNS4zLjE2MDEw"
FALLBACK_APP = "1897_Qx6CsUG7r803A_23Hon_1g"

D_LIST = "serviceComponent://ui.force.components.controllers.lists.listViewDataManager.ListViewDataManagerController/ACTION$getItems"
D_DETAIL = "apex://CaseRecordDetailCompCtrl/ACTION$getCaseRecordDetails"
D_FILINGS = "apex://CaseFilingsRelatedListCompCtrl/ACTION$getCaseFilings"
D_SEARCH = "serviceComponent://ui.search.components.forcesearch.scopedresultsdataprovider.ScopedResultsDataProviderController/ACTION$getItems"

# Words searched in filing descriptions with the site's own search box: the tracked plants, the
# planned ones, and the kinds of filing that announce a gas plant. A hit dated from the start year
# on brings its case in and puts that filing on the reading list.
SEARCH_TERMS = ["Belle River", "Covert", "Zeeland", "Karn", "Thetford", "Jackson generating", "Handy Township",
                "Milan Township", "Mihm", "Kuester", "Midland Cogeneration", "MCV", "Blue Water", "Indeck", "Delray",
                "Greenwood", "Renaissance Power", "Sumpter", "Alpine power", "Kalkaska", "Dearborn Industrial",
                "Delta Energy Park", "REO Town", "Holland Energy Park", "Marquette Energy Center",
                "combustion turbine", "combined cycle", "simple cycle", "peaker", "peaking",
                "natural gas generation", "gas plant", "power plant", "generating facility", "data center",
                "special contract", "certificate of necessity", "plant retirement", "unit retirement"]

# Cases read in full whatever their title says: the resource plans and the cases the user named.
PRIORITY_CASES = {
    "U-21090": "Consumers Energy integrated resource plan, 2021",
    "U-22127": "Consumers Energy integrated resource plan and certificates of necessity, 2026",
    "U-21193": "DTE Electric integrated resource plan, 2022",
    "U-22168": "DTE Electric integrated resource plan, 2026",
    "U-22057": "DTE Electric data center special contracts",
    "U-22058": "DTE Electric special contracts, 2026",
    "U-21990": "DTE Electric data center special contracts, 2025",
    "U-22175": "Upper Michigan Energy Resources integrated resource plan, 2026",
    "U-21081": "Upper Michigan Energy Resources integrated resource plan, 2021",
    "U-21542": "Upper Michigan Energy Resources, Mihm and Kuester engines",
    "U-21371": "Upper Michigan Energy Resources special contract",
    "U-21809": "Upper Peninsula Power integrated resource plan, 2024",
    "U-22069": "Indiana Michigan Power integrated resource plan, 2026",
    "U-21189": "Indiana Michigan Power integrated resource plan, 2022",
    "U-21377": "Indiana Michigan Power certificate of necessity, 2023",
    "U-21814": "Northern States Power integrated resource plan, 2024",
}

ELECTRIC_CO = re.compile(r"consumers energy|dte electric|detroit edison|upper michigan energy|\bumerc\b|"
                         r"upper peninsula power|\buppco\b|indiana michigan power|northern states power|"
                         r"wisconsin electric|wisconsin public service|alpena power|lansing board|wolverine|"
                         r"cloverland|presque isle electric|great lakes energy|midwest energy|thumb electric|"
                         r"tri-county electric|homeworks|ontonagon|michigan electric cooperative|"
                         r"michigan public power|\bmppa\b|board of water|indeck|midland cogeneration|"
                         r"new covert|zeeland board", re.I)
KEY = re.compile(r"integrated resource plan|\bIRP\b|certificates? of necessity|460\.6s|combined[- ]cycle|"
                 r"combustion turbine|simple[- ]cycle|peak(ing|er) (plant|unit|generat)|gas[- ]fired|"
                 r"natural gas (generat|plant|unit|fuel)|generating (plant|facility|station|unit)|power plant|"
                 r"retire|special contracts?|data center|hyperscale|reciprocating|repower|"
                 r"(purchase|acqui\w*|transfer) .{0,80}(plant|generat\w*|station|facility|facilities)|"
                 r"capacity (purchase|resource)|electric generation facilit", re.I)
RELEVANT = re.compile(KEY.pattern + r"|generation|generating|capacity|securitization|PURPA|qualifying facilit|"
                      r"cogeneration|power purchase agreement|interconnection|electric rates|"
                      r"rates for the (generation|sale) of electricity", re.I)
NOT_GEN = re.compile(r"power supply cost recovery|\bPSCR\b|renewable energy plan|energy waste reduction|"
                     r"energy optimization|demand response|low[- ]income|gas cost recovery|\bGCR\b|"
                     r"telecommunications?|\bpipeline\b|distribution of natural gas|natural gas distribution|"
                     r"service quality|reliability (performance|standards)|\bvoluntary green pricing\b|"
                     r"license to|\bcable\b|meter|customer choice|code of conduct|tree trimming|"
                     r"electric vehicle|\bEV\b|transportation electrification", re.I)
NOT_GAS_ONLY = re.compile(r"solar|wind|photovoltaic|battery|storage|hydro|renewable", re.I)
GASTECH = re.compile(r"natural gas|gas[- ]fired|combined[- ]cycle|combustion turbines?|simple[- ]cycle|"
                     r"peak(ing|er)s?\b|\bNGCC\b|\bCCGT\b|\bCTGs?\b|\bCTs?\b|reciprocating|\bRICE\b|"
                     r"oil[- ]fired|diesel|duct fir|coal[- ]to[- ]gas|gas conversion|convert\w* .{0,30}natural gas")
GASTECH = re.compile(GASTECH.pattern, re.I)

# Hand-checked patterns (2026-10-23): GEM plant id -> regexes that, found in a case title or a
# document, mean the text names this plant. Built for long filings, which name the company's
# home town (Jackson), neighboring boards (Zeeland Board of Public Works) and the Ludington
# pumped storage plant, so bare town names are avoided. (?-i:...) keeps an acronym case sensitive.
KNOWN = {
    "L100000103973": [r"belle river"],
    "L100000103983": [r"reo town", r"lansing board of water and light.{0,40}(cc|combined|plant|turbine)"],
    "L100000401674": [r"michigan power l(imited|\.?\s?p\b)", r"michigan power station", r"michigan power cogeneration"],
    "L100000401789": [r"48th street"],
    "L100000409227": [r"48th street"],
    "L100000401790": [r"holland energy park"],
    "L100000401824": [r"kalamazoo river generat"],
    "L100000401829": [r"\bkarn\b(?![- ]?weadock)", r"\bD\.\s?E\.\s?Karn"],
    "L100000401830": [r"jackson (generating|plant|facility|station|power plant|ngcc|combined|units?)\b",
                      r"zeeland, jackson", r"jackson,? and (covert|zeeland)"],
    "L100000401831": [r"zeeland(?!\s+(board|bpw|public|city|township|charter))\s*(generating|plant|facility|station|"
                      r"ngcc|combined[- ]cycle|units?|retirement|site|power)", r"(jackson|covert)( plants?)?,? (and )?zeeland\b",
                      r"zeeland,? (and )?(jackson|covert)\b"],
    "L100000401855": [r"\bdean (peak\w*|ctgs?|cts?|plant|station|units?|power)\b"],
    "L100000401856": [r"\bdelray\b"],
    "L100000401857": [r"\bgreenwood\b(?!\s+(township|twp|road|rd|charter|public|city|ave\w*|street|st\b|energy|sand\w*|village|transmitter))"],
    "L100000401858": [r"renaissance (power|peak\w*|plant|station|ctgs?|cts?|units?|energy)\b"],
    "L100000402079": [r"kalkaska (ct|cts|combustion|peak\w*|generat\w*|plant|station|units?)\b"],
    "L100000402123": [r"(?<!-)\bcovert\b(?!-)(?!\s+(township|twp|road|rd|charter|public|city|ave\w*|street|st\b|energy|sand\w*|village|transmitter))"],
    "L100000402385": [r"\balpine (power|plant|station|generat\w*|ct|peak\w*)"],
    "L100000402386": [r"\bsumpter\b(?!\s+(township|twp|road|rd|charter|public|city|ave\w*|street|st\b|energy|sand\w*|village|transmitter))"],
    "L100000402393": [r"blue water energy", r"(?-i:\bBWEC\b)"],
    "L100000402411": [r"\bindeck\b"],
    "L100000402454": [r"dearborn industrial", r"(?-i:\bDIG\b)"],
    "L100000402461": [r"delta energy park"],
    "L100000402478": [r"midland cogeneration", r"(?-i:\bMCV\b)"],
    "L100000407414": [r"(?-i:\bMEC South\b)", r"development partners group"],
    "L100000407415": [r"(?-i:\bMEC North\b)", r"development partners group"],
    "L100000409204": [r"\bmihm\b"],
    "L100000409210": [r"\bkuester\b"],
    "L100000409279": [r"marquette energy center"],
    "L100001082478": [r"handy township", r"livingston county (project|ccgt|combined|ngcc)", r"\bfowlerville\b"],
    "L100001083332": [r"bay county (power|gas|plant|project|ct|simple)", r"karn (ct|cts|project|combustion|simple)",
                      r"(?-i:\bDEK CT\b)"],
    "L100001083333": [r"thetford (site|project|generating|plant|simple|ct|cts|units?|station|facility|gas)\b", r"genesee county (power|gas|plant|project|ct|simple)"],
    "L100001088928": [r"milan township", r"monroe county (project|ccgt|combined|ngcc)", r"\bmilan (ngcc|cc|site|plant|project|energy|combined|gas)"],
}

# Names that put a line of a resource-plan table on the list (tracked gas plants, the coal plants
# whose retirement drives the plans, and the DTE peaker sites).
IRP_NAMES = re.compile(r"\bkarn\b|campbell|zeeland|jackson|covert|belle river|monroe|greenwood|\bdean\b|delray|"
                       r"renaissance|blue water|trenton|st\.? clair|river rouge|ludington|midland|\bmcv\b|"
                       r"\bDIG\b|dearborn industrial|handy|\bmilan\b|bay county|genesee|thetford|mihm|kuester|"
                       r"\balpine\b|sumpter|indeck|kalkaska|reo town|delta energy|erickson|holland|48th street|"
                       r"marquette|weadock|hancock|northeast|superior|placid|putnam|colfax|slocum|fermi|"
                       r"rockport|cook\b|presque isle|portage|gaylord|straits", re.I)
INSERVICE = re.compile(r"in[- ]service|commercial operation|\bCOD\b|placed in service|on[- ]?line|begin operat|"
                       r"construction (will|is expected)|completion|available (in|by)", re.I)
RETIRE = re.compile(r"retire|retirement|deactivat|mothball|cease operat|shut ?down|decommission", re.I)
LOCATION = re.compile(r"located (at|in|on|near|approximately)|site (is|in|at)|county,? michigan|township|"
                      r"latitude|longitude|\bacres?\b|parcel|city of", re.I)
LATLON = re.compile(r"\b(4[1-8]\.\d{3,})\s*[,;/ ]\s*(?:-\s*)?(8[2-9]\.\d{3,}|90\.\d{3,})\b")
EXHIBIT = re.compile(r"\bExhibit(?:\s+No\.)?\s*:?\s*([A-Z]{1,3}-\d+(?:\.\d+)?(?:\s*\([A-Z]{2,5}-\d+\))?)")
LINE_NO = re.compile(r"(?m)^[ \t]{0,10}\d{1,2}[ \t]{2,}")

# Filing types never read: service, appearances, scheduling, briefs and other argument.
SKIP_TYPES = re.compile(r"proof of service|appearance|intervention|^comments?$|press release|letter|withdrawal|"
                        r"scheduling|notice of hearing|transcript|motion|ruling|brief|exceptions|affidavit|"
                        r"protective order|appeal|^response|^request|official hearing|errata", re.I)
MUST_TYPES = re.compile(r"^order$|^application", re.I)
SETTLEMENT = re.compile(r"settlement agreement|stipulation|settlement", re.I)
UTILITY_DOC = re.compile(r"^exhibits?$|testimony and exhibits|^testimony$|^other$|^report$|^petition$|^plan", re.I)
UTILITY_DESC = re.compile(r"application|exhibit|testimony|plan|filing announcement|summary|report", re.I)


def log(msg):
    print(f"[psc-mi] {msg}", file=sys.stderr, flush=True)


# ------------------------------------------------------------------ portal ---

def boot_context(html_text):
    """(fwuid, app version) from the URL-encoded boot links of the /s/ page, or the fallback pair."""
    t = urllib.parse.unquote(html_text or "")
    fw = re.search(r'"fwuid":"([^"]+)"', t)
    app = re.search(r'"APPLICATION@markup://siteforce:communityApp":"([^"]+)"', t)
    return (fw.group(1) if fw else FALLBACK_FWUID), (app.group(1) if app else FALLBACK_APP)


def parse_aura(text):
    """The JSON of an Aura answer (some start with `*/`); None when it is not JSON."""
    t = (text or "").strip()
    if t.startswith("*/"):
        t = t[2:]
    try:
        return json.loads(t)
    except ValueError:
        return None


def action_value(answer):
    """(state, returnValue) of the first action of an Aura answer."""
    acts = (answer or {}).get("actions") or []
    if not acts:
        return None, None
    return acts[0].get("state"), acts[0].get("returnValue")


def list_page(answer):
    """Cases on one page of the list view: [{id, case, open, company, subject, industry}], plus
    (has_more, next_offset, total). Records come from the `$Record` value provider."""
    state, rv = action_value(answer)
    if state != "SUCCESS" or not rv:
        return None
    provs = [g for g in (answer.get("context") or {}).get("globalValueProviders") or [] if g.get("type") == "$Record"]
    if not provs:
        return None
    recs = provs[0].get("values", {}).get("records", {})
    out = []
    for x in rv.get("recordIdActionsList") or []:
        rec = recs.get(x["recordId"])
        if not rec:
            return None
        f = rec["Case"]["record"]["fields"]
        val = lambda k: (f.get(k) or {}).get("value")  # noqa: E731
        out.append({"id": x["recordId"], "case": val("CaseNumber"), "open": val("Open_Date__c") or "",
                    "company": (f.get("On_Behalf_of_Company__r") or {}).get("displayValue") or "",
                    "subject": clean_ws(val("Subject")), "industry": val("Industry__c") or ""})
    return out, bool(rv.get("hasMoreData")), rv.get("offset"), rv.get("totalCount")


def filing_row(x):
    """One filing from getCaseFilings, flattened (the answer nests it under `filing`)."""
    f = x.get("filing", x)
    return {"name": f.get("Name") or "", "type": f.get("Filing_Type__c") or "", "date": f.get("File_Date__c") or "",
            "desc": clean_ws(f.get("Filing_Description__c")), "pages": f.get("Num_Pages__c") or 0,
            "public": f.get("Public__c", True) is not False
            and str(f.get("Confidential__c") or "No").strip().lower() in ("no", "false", ""),
            "url": f.get("File_Link_URL__c") or "",
            "by": (f.get("Filed_By__r") or {}).get("Name") or "",
            "for": (f.get("On_Behalf_of_Company__r") or {}).get("Name") or ""}


def seq_of(name):
    m = re.search(r"-(\d{4})$", name or "")
    return int(m.group(1)) if m else 0


def search_hit(rec, term):
    """A filing found by the search box, flattened: (case number, filing name, type, date, description)."""
    name = rec.get("Name") or ""
    m = re.match(r"(U-\d+)-\d{4}$", name)
    return {"case": m.group(1) if m else "", "name": name, "type": rec.get("Filing_Type__c") or "",
            "date": (rec.get("File_Date__c") or "")[:10], "desc": clean_ws(rec.get("Filing_Description__c")),
            "term": term}


class Portal:
    def __init__(self):
        html = subprocess.run(["curl", "-sL", "--max-time", "60", "-A", CHROME_UA, HOME],
                              capture_output=True, text=True).stdout
        self.fwuid, self.app = boot_context(html)
        self.calls = 0

    def call(self, descriptor, params, tries=4):
        msg = {"actions": [{"id": "1;a", "descriptor": descriptor, "callingDescriptor": "UNKNOWN", "params": params}]}
        ctx = {"mode": "PROD", "fwuid": self.fwuid, "app": "siteforce:communityApp",
               "loaded": {"APPLICATION@markup://siteforce:communityApp": self.app},
               "dn": [], "globals": {}, "uad": True}
        data = urllib.parse.urlencode({"message": json.dumps(msg), "aura.context": json.dumps(ctx),
                                       "aura.pageURI": "/s/", "aura.token": "null"})
        for i in range(tries):
            self.calls += 1
            r = subprocess.run(["curl", "-s", "--max-time", "180", "-A", CHROME_UA,
                                "-H", "Content-Type: application/x-www-form-urlencoded; charset=UTF-8",
                                "--data-binary", "@-", AURA], input=data, capture_output=True, text=True)
            ans = parse_aura(r.stdout)
            if ans and action_value(ans)[0] == "SUCCESS":
                return ans
            time.sleep(2 + 3 * i)
        return None

    def cases(self, stop_year):
        """Every listed case opened in `stop_year` or later (the list is newest first)."""
        out, off = [], 0
        while True:
            page = None
            for _ in range(4):
                ans = self.call(D_LIST, {"filterName": LIST_FILTER, "entityName": "Case", "pageSize": 500,
                                         "layoutType": "LIST", "sortBy": None, "getCount": True,
                                         "enableRowActions": False, "offset": off})
                page = list_page(ans) if ans else None
                if page:
                    break
                time.sleep(3)
            if not page:
                log(f"case list: no records at offset {off}; stopping there")
                break
            rows, more, nxt, total = page
            out += rows
            log(f"case list offset {off}: {len(rows)} cases (total {total})")
            if not rows or not more or nxt is None or rows[-1]["open"][:4] < str(stop_year):
                break
            off = nxt
        return out

    def search(self, scope, term, max_pages=10):
        """Records the site's search box finds for `term` in one scope ("Filing__c" or "Case")."""
        prefix = {"Case": "500", "Filing__c": "a00"}[scope]
        out = []
        for page in range(1, max_pages + 1):
            ans = self.call(D_SEARCH, {"scopeMap": {"label": scope, "keyPrefix": prefix, "name": scope,
                                                    "namespace": "forceCommunity", "cacheable": "Y",
                                                    "id": f"forceCommunity:{scope}", "labelPlural": scope},
                                       "term": term, "pageSize": 50, "currentPage": page, "sortBy": None,
                                       "enableRowActions": False, "context": {"persistedContextParams": {"feeds": {}}},
                                       "withSpellCorrection": False})
            rv = action_value(ans)[1] if ans else None
            if not rv:
                break
            out += [x.get("record") or {} for x in rv.get("result") or []]
            if not rv.get("moreResultsAvailable"):
                break
        return out

    def detail(self, case_id):
        ans = self.call(D_DETAIL, {"caseId": case_id})
        rv = action_value(ans)[1] if ans else None
        return {"status": (rv or {}).get("Status") or "", "type": (rv or {}).get("Type") or "",
                "subject": clean_ws((rv or {}).get("Subject"))}

    def filings(self, case_id):
        ans = self.call(D_FILINGS, {"caseId": case_id, "sortField": "Name", "isAsc": True})
        rv = action_value(ans)[1] if ans else None
        return [filing_row(x) for x in rv or []] if rv is not None else None


def download(url, path):
    """Plain GET of a public filing; True when a PDF arrived."""
    tmp = path.with_suffix(".part")
    subprocess.run(["curl", "-sL", "--max-time", "600", "-A", CHROME_UA, "-o", str(tmp), url], capture_output=True)
    if tmp.exists() and tmp.read_bytes()[:5] == b"%PDF-":
        tmp.rename(path)
        return True
    tmp.unlink(missing_ok=True)
    return False


# ---------------------------------------------------------- classification ---

def classify(case, detail=None):
    """(relevant, key, reasons) for one case from its title, company, industry and type."""
    detail = detail or {}
    title = f"{case['subject']} {detail.get('type', '')}"
    reasons = []
    if case["case"] in PRIORITY_CASES:
        return True, True, [f"named case: {PRIORITY_CASES[case['case']]}"]
    if case.get("industry") and case["industry"] not in ("Electric", ""):
        # A gas case matters only when it serves a power plant or a data center.
        if not re.search(r"generat|power plant|data center|electric", case["subject"], re.I):
            return False, False, []
        return True, False, ["gas case that names generation, a power plant or a data center"]
    if re.search(r"integrated resource plan", detail.get("type", ""), re.I):
        return True, True, ["case type is an integrated resource plan"]
    if NOT_GEN.search(case["subject"]) and not re.search(r"integrated resource plan|certificate of necessity|"
                                                        r"combined[- ]cycle|combustion turbine", case["subject"], re.I):
        return False, False, []
    key_hits = sorted({m.group(0).lower() for m in KEY.finditer(title)})
    if key_hits:
        reasons.append("title says " + ", ".join(key_hits[:4]))
        renewables_only = NOT_GAS_ONLY.search(title) and not GASTECH.search(title) and not re.search(
            r"integrated resource plan|certificate of necessity|retire|data center|special contract", title, re.I)
        if renewables_only:
            return True, False, reasons + ["renewables or storage only"]
        return True, bool(ELECTRIC_CO.search(case["company"]) or GASTECH.search(title)), reasons
    if RELEVANT.search(title) and ELECTRIC_CO.search(case["company"]):
        return True, False, ["generation-related title"]
    return False, False, []


def pick_docs(filings, cap, company="", wanted=()):
    """The filings most likely to hold plant facts, in filing order: every order, application and
    settlement and every filing the search box found (`wanted`), then the applicant's own exhibits
    and testimony (earliest first) up to `cap`. Sealed or non-public filings (0 pages) are skipped."""
    open_ = [f for f in filings if f["pages"] and f["public"] and f["url"]]
    must = [f for f in open_ if MUST_TYPES.search(f["type"]) or SETTLEMENT.search(f"{f['type']} {f['desc']}")
            or (f["name"] in wanted and not SKIP_TYPES.search(f["type"]))]
    co = re.escape(company.split(" Company")[0].strip()) if company else r"$^"
    extra = [f for f in open_ if f not in must and not SKIP_TYPES.search(f["type"])
             and UTILITY_DOC.search(f["type"]) and UTILITY_DESC.search(f["desc"] or f["type"])
             and (re.search(co, f"{f['for']} {f['desc']}", re.I) or re.search(r"^other$|^report$", f["type"], re.I))]
    chosen = must[:cap]
    for f in sorted(extra, key=lambda x: (x["date"], seq_of(x["name"]))):
        if len(chosen) >= cap:
            break
        chosen.append(f)
    return sorted(chosen, key=lambda x: seq_of(x["name"]))


# ---------------------------------------------------------- document facts ---

def clean_text(t):
    """Text with testimony line numbers removed."""
    return LINE_NO.sub("", t or "")


def pick_s(sents, rx, limit, need=None, lo=20, hi=420):
    out = []
    for s in sents:
        if lo < len(s) < hi and rx.search(s) and (need is None or need.search(s)) and s not in out:
            out.append(s)
            if len(out) >= limit:
                break
    return out


def table_lines(layout_text, limit=20):
    """Lines of layout text that name a plant and carry a year or megawatts: the rows of
    resource-plan addition and retirement tables."""
    out = []
    for ln in clean_text(layout_text).splitlines():
        s = clean_ws(ln)
        if 6 < len(s) < 260 and IRP_NAMES.search(s) and (YEAR.search(s) or SIZE.search(s)) and s not in out:
            out.append(s)
            if len(out) >= limit:
                break
    return out


GAS_OR_PLANT = re.compile(GASTECH.pattern + "|" + IRP_NAMES.pattern, re.I)


def doc_facts(text, layout_text=""):
    plain = clean_text(text or layout_text)
    sents = sentences(plain)
    return {
        "technology": sorted({m.group(0).lower() for m in GASTECH.finditer(plain)})[:8],
        "equipment_maker_model": pick_s(sents, MAKER, 8, need=GASTECH),
        "megawatts": pick_s(sents, SIZE, 10, need=GAS_OR_PLANT),
        "in_service": [s for s in pick_s(sents, INSERVICE, 40, need=GAS_OR_PLANT) if YEAR.search(s)][:6],
        "retirement": [s for s in pick_s(sents, RETIRE, 60, need=GAS_OR_PLANT) if YEAR.search(s)][:8],
        "location": pick_s(sents, LOCATION, 6, need=GAS_OR_PLANT),
        "coords": [f"{a}, -{b}" for a, b in LATLON.findall(plain)][:3],
        "resource_plan_table_lines": table_lines(layout_text or text),
    }


def pdf_texts(path):
    """(plain text, layout text) of a PDF; pages stay split by form feeds. Scans go through OCR."""
    def run(args):
        return subprocess.run(["pdftotext"] + args + [str(path), "-"], capture_output=True, text=True).stdout
    plain, layout = run([]), run(["-layout"])
    if len(plain.strip()) < 300:
        import fetch
        try:
            ocr = fetch._pdf_ocr(str(path))
        except Exception:  # noqa: BLE001
            ocr = ""
        if len(ocr.strip()) > len(plain.strip()):
            plain = layout = ocr
    return plain, layout


def plant_pages(layout_text, patterns, limit=8):
    """[{page, exhibit}] where any pattern hits, page numbers counted by form feeds (1-based),
    with the exhibit label printed on that page when there is one."""
    out = []
    for n, page in enumerate((layout_text or "").split("\f"), 1):
        if any(re.search(p, page, re.I) for p in patterns):
            ex = EXHIBIT.search(page)
            out.append({"page": n, "exhibit": clean_ws(ex.group(1)) if ex else ""})
            if len(out) >= limit:
                break
    return out


def read_case(d, filings, cap, drop_mb, wanted=()):
    """Download and read the key filings of one case; returns (docs, facts)."""
    folder = WORK / d["docket"]
    folder.mkdir(parents=True, exist_ok=True)
    docs, parts = [], []
    for f in pick_docs(filings, cap, d.get("utility", ""), wanted):
        rec = {"seq": seq_of(f["name"]), "file": f["name"], "type": f["type"], "comment": f["desc"],
               "pages": f["pages"], "received": f["date"], "url": f["url"], "filed_by": f["for"] or f["by"],
               "saved": "", "read": False}
        pdf, txt = folder / f"{f['name']}.pdf", folder / f"{f['name']}.txt"
        if txt.exists() and len(txt.read_text(errors="replace").strip()) >= 300:
            layout = txt.read_text(errors="replace")
            plain = layout
        else:
            ok = (pdf.exists() and pdf.read_bytes()[:5] == b"%PDF-") or download(f["url"], pdf)
            if not ok:
                log(f"  {f['name']}: download failed")
                docs.append(rec)
                continue
            plain, layout = pdf_texts(pdf)
            txt.write_text(layout)
            if drop_mb and pdf.stat().st_size > drop_mb * 1e6:
                pdf.unlink()
        rec["saved"] = str((pdf if pdf.exists() else txt).relative_to(REPO))
        rec["text"] = str(txt.relative_to(REPO))
        rec["read"] = len(plain.strip()) >= 300
        if rec["read"]:
            rec["facts"] = doc_facts(plain, layout)
            parts.append(rec["facts"])
        docs.append(rec)
        log(f"  {f['name']} {f['type']} ({f['pages']} pages): {'read' if rec['read'] else 'no text'}")
    return docs, merge_facts(parts)


# ------------------------------------------------------------------ match ---

def case_texts(d):
    """{filing name: layout text} of the documents read for a case."""
    out = {}
    for doc in d.get("docs") or []:
        p = REPO / doc["text"] if doc.get("text") else None
        if p and p.exists():
            out[doc["file"]] = p.read_text(errors="replace")
    return out


def match_case(plant, d, texts, others_by_title=False):
    """(how, where, plant facts) when a case names a plant, else None. A name in the case title is
    a strong match; otherwise the documents read must name it three or more times (six when the
    title already names another plant, since big filings mention neighbors)."""
    pats = KNOWN.get(plant["id"])
    if not pats:
        return None
    if any(re.search(p, d["title"], re.I) for p in pats):
        how = "name in the case title"
    else:
        n = sum(len(re.findall(p, t, re.I)) for t in texts.values() for p in pats)
        if n < (6 if others_by_title else 3):
            return None
        how = f"named {n} times in the documents read"
    where, facts = [], []
    for name, t in texts.items():
        pages = plant_pages(t, pats)
        if pages:
            where.append({"filing": name, "pages": pages})
            hit = re.compile("|".join(f"(?:{p})" for p in pats), re.I)
            for s in pick_s(sentences(clean_text(t)), hit, 30):
                if (SIZE.search(s) or YEAR.search(s)) and s not in facts:
                    facts.append(s)
                if len(facts) >= 6:
                    break
    if where:
        first = "; ".join(f"{w['filing']} page {w['pages'][0]['page']}"
                          + (f" (Exhibit {w['pages'][0]['exhibit']})" if w["pages"][0]["exhibit"] else "")
                          for w in where[:3])
        how += f"; first named in {first}"
    return how, where, facts[:6]


def match_all(plants, dockets, texts_by_case=None):
    by_plant = {p["id"]: [] for p in plants}
    matched = set()
    for d in dockets:
        texts = (texts_by_case or {}).get(d["docket"])
        if texts is None:
            texts = case_texts(d)
        d["matched"] = []
        titled = any(match_case(p, d, {}) for p in plants)
        for p in plants:
            hit = match_case(p, d, texts, others_by_title=titled)
            if hit:
                how, where, facts = hit
                d["matched"].append({"plant_id": p["id"], "plant": p["name"], "how": how,
                                     "where": where, "plant_facts": facts})
                by_plant[p["id"]].append(d["docket"])
                matched.add(d["docket"])
    return by_plant, matched


# ----------------------------------------------------------------- output ---

def docket_block(d, full=True):
    L = [f"- **{d['docket']}**, {d['utility'] or 'applicant not shown'}: {d['title'][:300]}",
         f"  - Opened {d.get('filed') or 'date not shown'}; status {d.get('status') or 'not shown'}; "
         f"type {d.get('case_type') or 'not shown'}; filings on file: {d['doc_count']}; case page: {d.get('case_url')}"]
    if full and d.get("facts"):
        f = d["facts"]
        for k, label in [("technology", "Technology"), ("megawatts", "Megawatts"),
                         ("equipment_maker_model", "Equipment"), ("in_service", "In service"),
                         ("retirement", "Retirements"), ("location", "Location"), ("coords", "Coordinates"),
                         ("resource_plan_table_lines", "Plan table lines")]:
            v = f.get(k)
            if v:
                L.append(f"  - {label}: " + " | ".join(x[:300] for x in v[:4 if k != "resource_plan_table_lines" else 10]))
    for doc in d.get("docs", []):
        if doc.get("read"):
            L.append(f"  - Read {doc['file']}, {doc['type']} ({doc['pages']} pages, filed {doc['received']}): "
                     f"{doc['comment'][:140]}. Link: {doc['url']}")
    return L


def write_outputs(out_dir, plants, dockets, by_plant, matched, sources, today, from_year):
    out_dir.mkdir(parents=True, exist_ok=True)
    unmatched = [d for d in dockets if d["key"] and d["docket"] not in matched]
    data = {"generated": today, "from_year": from_year, "sources": sources, "dockets": dockets,
            "by_plant": by_plant, "unmatched_generation": [d["docket"] for d in unmatched]}
    (out_dir / "psc_dockets.json").write_text(json.dumps(data, indent=1, default=str))
    by_id = {d["docket"]: d for d in dockets}
    L = [f"# Michigan Public Service Commission cases on generation, resource plans and retirements ({today})", "",
         f"Cases opened {from_year} or later, plus the named resource-plan and special contract cases. Each filing has a "
         "stable download link and each case a stable case page, so both can be cited. Copies of the documents read are "
         "in work/psc_mi/ and are not committed. Page numbers count PDF pages from the first page of the filing.", "",
         "## Sources", ""]
    L += [f"- {s['name']}: {s['how']} ({s['url']})" for s in sources]
    L += ["", "## Matched to GEM plants", ""]
    for p in plants:
        ids = by_plant.get(p["id"], [])
        L.append(f"### {p['name']} ({p['id']}), {p['city'] or 'city not shown'}, "
                 f"{(p['county'] or 'county not shown').title()} County")
        L.append("")
        if not ids:
            L += ["No case matched.", ""]
            continue
        for k in ids:
            d = by_id[k]
            m = next(x for x in d["matched"] if x["plant_id"] == p["id"])
            L.append(f"- **{d['docket']}**, {d['utility']}, opened {d['filed']} ({d.get('status') or 'status not shown'}): "
                     f"{d['title'][:200]}")
            L.append(f"  - Match: {m['how']}")
            for w in m["where"][:6]:
                pages = ", ".join(str(x["page"]) + (f" (Exhibit {x['exhibit']})" if x["exhibit"] else "")
                                  for x in w["pages"][:6])
                L.append(f"  - {w['filing']}: pages {pages}")
            for s in m["plant_facts"][:4]:
                L.append(f"  - Says: {s[:300]}")
        L.append("")
    L += ["## Generation cases that match no GEM plant (possible new plants, uprates or retirements)", ""]
    for d in sorted(unmatched, key=lambda x: x["docket"]):
        L += docket_block(d)
    L += ["", "## Cases read in full", ""]
    for d in sorted((d for d in dockets if d["key"] and d["docket"] in matched), key=lambda x: x["docket"]):
        L += docket_block(d)
    L += ["", "## Other generation-related cases (not read in full)", ""]
    for d in sorted((d for d in dockets if d["relevant"] and not d["key"]), key=lambda x: x["docket"]):
        L += docket_block(d, full=False)
    (out_dir / "psc_dockets.md").write_text("\n".join(L) + "\n")
    return unmatched


def make_docket(c, detail, filings):
    return {"docket": c["case"], "year": int(c["open"][:4]) if c["open"] else None, "type": "U",
            "number": c["case"].split("-", 1)[-1], "utility": c["company"], "title": detail.get("subject") or c["subject"],
            "filed": c["open"], "status": detail.get("status", ""), "case_type": detail.get("type", ""),
            "industry": c.get("industry", ""), "case_id": c["id"], "case_url": f"{SITE}/s/case/{c['id']}",
            "agenda_pdfs": [], "comments_text": c["subject"], "routine": False,
            "doc_count": len(filings) if filings is not None else 0,
            "latest_filing": max((f["date"] for f in filings or []), default=""), "docs": [], "facts": {}}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--from-year", type=int, default=2022)
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--plants", help="comma-separated GEM location IDs")
    ap.add_argument("--docs-per-case", type=int, default=12, help="filings read per ordinary case")
    ap.add_argument("--docs-per-plan", type=int, default=40, help="filings read per resource-plan case")
    ap.add_argument("--drop-pdfs-over", type=float, default=25, help="MB; larger PDFs are deleted once their text is saved")
    ap.add_argument("--no-docs", action="store_true", help="list cases, download nothing")
    ap.add_argument("--match-only", metavar="JSON", help="re-match a saved psc_dockets.json, no network")
    a = ap.parse_args()
    plants = load_state_plants("Michigan", KNOWN)
    if a.plants:
        plants = [p for p in plants if p["id"] in set(a.plants.split(","))]
    today = dt.date.today().isoformat()
    if a.match_only:
        saved = json.loads(Path(a.match_only).read_text())
        dockets, sources = saved["dockets"], saved["sources"]
        by_plant, matched = match_all(plants, dockets)
        write_outputs(Path(a.out), plants, dockets, by_plant, matched, sources, today, saved.get("from_year", a.from_year))
        return
    portal = Portal()
    cases = portal.cases(min(LIST_START, a.from_year))
    listed = {c["case"] for c in cases}
    missing = sorted(set(PRIORITY_CASES) - listed)
    if missing:
        log(f"named cases not in the list: {', '.join(missing)}")
    hits = {}
    for term in SEARCH_TERMS:
        n = 0
        for rec in portal.search("Filing__c", term):
            h = search_hit(rec, term)
            if h["case"] and h["date"][:4] >= str(a.from_year) and not SKIP_TYPES.search(h["type"]):
                hits.setdefault(h["case"], []).append(h)
                n += 1
        log(f"filing search {term!r}: {n} filings from {a.from_year} on")
    by_case = {c["case"]: c for c in cases}
    for num in sorted(set(hits) - set(by_case)):
        recs = [r for r in portal.search("Case", num, max_pages=1) if r.get("CaseNumber") == num]
        if recs:
            r = recs[0]
            c = {"id": r.get("Id"), "case": num, "open": (r.get("Open_Date__c") or "")[:10],
                 "company": (r.get("On_Behalf_of_Company__r") or {}).get("Name") or "",
                 "subject": clean_ws(r.get("Subject")), "industry": r.get("Industry__c") or ""}
            cases.append(c)
            by_case[num] = c
        else:
            log(f"filing search found {num}, but the case search does not return it")
    dockets = []
    for c in cases:
        relevant, key, reasons = classify(c)
        recent = c["open"][:4] >= str(a.from_year)
        found = hits.get(c["case"], [])
        if not found and (not relevant or not (recent or key)):
            continue
        detail = portal.detail(c["id"])
        relevant, key, reasons = classify(c, detail)
        if found:
            terms = sorted({h["term"] for h in found})
            reasons.append(f"{len(found)} filings from {a.from_year} on found by the search for " + ", ".join(terms))
            electric = c.get("industry") in ("Electric", "") or GASTECH.search(" ".join(terms))
            relevant = True
            key = key or bool(electric and any(MUST_TYPES.search(h["type"]) or UTILITY_DOC.search(h["type"])
                                               or SETTLEMENT.search(h["type"]) for h in found))
        if not relevant:
            continue
        filings = portal.filings(c["id"]) if key else None
        if not recent and c["case"] not in PRIORITY_CASES and not found:
            # An older case is read only when it still gets filings from the start year on.
            if not filings or max(f["date"] for f in filings)[:4] < str(a.from_year):
                continue
            reasons.append(f"opened {c['open'][:4]}, filings since {a.from_year}")
        d = make_docket(c, detail, filings)
        d["relevant"], d["key"], d["reasons"] = relevant, key, reasons
        d["_filings"] = filings or []
        d["search_hits"] = [{k: h[k] for k in ("name", "type", "date", "desc", "term")} for h in found]
        dockets.append(d)
    log(f"{len(cases)} cases listed; {len(dockets)} generation related; {sum(1 for d in dockets if d['key'])} key")
    if not a.no_docs:
        for d in dockets:
            if not d["key"]:
                continue
            plan = bool(re.search(r"integrated resource plan|certificate of necessity", f"{d['case_type']} {d['title']}", re.I))
            log(f"reading {d['docket']} ({len(d['_filings'])} filings): {d['title'][:90]}")
            try:
                d["docs"], d["facts"] = read_case(d, d["_filings"], a.docs_per_plan if plan else a.docs_per_case,
                                                  a.drop_pdfs_over, {h["name"] for h in d["search_hits"]})
            except Exception as e:  # noqa: BLE001
                log(f"  {d['docket']} failed: {e}")
    for d in dockets:
        d.pop("_filings", None)
    read = sum(1 for d in dockets for doc in d["docs"] if doc.get("read"))
    sources = [{"name": "Michigan PSC E-Dockets (guest Aura calls)", "url": HOME,
                "how": f"plain curl replays the site's own list, search, case and filings calls, no sign-in; {len(cases)} cases "
                       f"opened {min(LIST_START, a.from_year)} or later listed, {len(dockets)} generation related, "
                       f"{sum(1 for d in dockets if d['key'])} read, {read} filings read; the filing search for {len(SEARCH_TERMS)} "
                       f"words found filings in {len(hits)} cases; {portal.calls} calls"
                       + (f"; named cases not found in the list: {', '.join(missing)}" if missing else "")}]
    by_plant, matched = match_all(plants, dockets)
    unmatched = write_outputs(Path(a.out), plants, dockets, by_plant, matched, sources, today, a.from_year)
    log(f"{len(matched)} cases matched to plants; {len(unmatched)} key cases unmatched")
    for p in plants:
        log(f"  {p['name']}: {', '.join(by_plant[p['id']]) or 'none'}")


if __name__ == "__main__":
    main()

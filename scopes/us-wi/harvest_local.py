"""
Harvest Wisconsin city, village, town and county planning, zoning, board and council records before a sweep.

Wisconsin data center and power sites are approved by the village board, town board, plan commission
or county board where they sit (rezonings, conditional use permits, development agreements, tax
incremental financing, utility service agreements), and those records name generator fleets and
turbines long before an air permit exists. This reads every posted record since --since (default
2024-01-01) for the bodies around the GEM plants and the leads, and keeps the sentences that name a
plant, a lead or a power or data center project. Nothing needs a sign-in. Routes (probed 2026-11-17):

  legistar     Milwaukee, Madison, Dane County and Waukesha: the open API at
               webapi.legistar.com/v1/<client>/Events, agenda and minutes PDFs, and item
               attachments whose item names a power or data center project.
  legistar_html  The City of Racine (client cityofracine; its API answers 400): the Calendar.aspx form
               posted once per year and body, agenda and minutes View.ashx links from the grid.
  wpmedia      Somers and Town of Paris: the WordPress media library at /wp-json/wp/v2/media, every PDF
               since the date whose title looks like a meeting record.
  swagit       Menomonee Falls: the swagit.com video tables; each Agenda link hands off to the village's
               public agenda site (agenda text and packet PDF).
  civicclerk   Rock County, Beaver Dam, Green Bay and Kronenwetter: the open OData API at
               <host>.api.civicclerk.com/v1/Events; GetMeetingFileStream downloads the PDFs.
  agendacenter CivicPlus AgendaCenter sites (Mount Pleasant, Ozaukee County, Calumet County, Superior,
               Douglas County, Menomonie, Walworth County, Kenosha County, Oak Creek):
               /AgendaCenter/Search/?CIDs=all with a date range; files at
               /AgendaCenter/ViewFile/Agenda|Minutes/_MMDDYYYY-ID. Kenosha County sits behind
               Cloudflare and is read through fetch.py.
  municode     Sheboygan: sheboygan-wi.municodemeetings.com/meetings3?page=N, a meetings table with
               PDF agenda, packet and minutes links (newest first, read until the dates pass --since).
  granicus     DeForest: deforestwi.granicus.com/ViewPublisher.php?view_id=1.
  brown        Brown County: each committee's agendas and minutes page lists ?i= links; each ?i= page
               holds the /i/agendas|minutes/<id>/<name>.pdf file.
  pages        Every other body (Port Washington, Racine County, Brillion, Rothschild, Wrightstown,
               Dodge County): its agendas or minutes page(s), followed level by level (`follow` is a list of patterns),
               read through fetch.py's access ladder (with a real-Chrome render where the page is built
               by script), plus the committee pages it links when `follow` is set, and every dated
               document link on them (PDF, showpublisheddocument, /a/uploads/, aptg.co short links).

Scanned minutes are read by OCR (pdftoppm then tesseract, through fetch.py). Documents are saved under
scopes/us-wi/work/local/<body>/ (not committed). Bodies that post no records are listed for a person
(the coverage list's human wall). Nothing here stages a record.

Output, in batches/us-wi/harvest/: local_records.json and local_records.md.

Usage (from the repo root):
    python scopes/us-wi/harvest_local.py                          # every body since 2024
    python scopes/us-wi/harvest_local.py --bodies port-washington,brown-county --since 2025-01-01
    python scopes/us-wi/harvest_local.py --list-only              # list documents, read nothing
    python scopes/us-wi/harvest_local.py --no-ocr
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
from fetch import CHROME_UA, fetch_page  # noqa: E402
from harvest_lib import REPO, clean_ws, get, report_failure, sentences, tag_batch  # noqa: E402

from paths import scope_work  # noqa: E402

OUT = REPO / "batches" / "us-wi" / "harvest"
CSV = REPO / "scripts" / "gem_export_gogpt_scoped.csv"
LEGISTAR = "https://webapi.legistar.com/v1/{client}"


def norm_wi_county(s):
    """'Racine County' and 'RACINE' both become 'Racine'; 'Fond Du Lac' stays as the export spells it."""
    return re.sub(r"\s+county$", "", str(s or "").strip(), flags=re.I).strip().title()


def load_plants(csv_path=None):
    import pandas as pd
    csv = pd.read_csv(csv_path or CSV, low_memory=False, encoding="utf-8-sig")
    csv = csv[csv["State/Province"] == "Wisconsin"]
    plants = []
    for pid, rows in csv.groupby("GEM location ID", sort=False):
        r = rows.iloc[0]
        county = r.get("Local area (taluk, county)")
        name = str(r["Plant name"])
        words = {w for w in re.findall(r"[a-z]+", name.lower())
                 if w not in {"power", "station", "plant", "plants", "generating", "facility", "energy", "center",
                              "data", "centers", "new", "wi", "irp", "the", "of", "gas", "street", "river",
                              "project", "combustion", "turbine", "cogeneration", "campus", "diesel", "generators"}}
        plants.append({"id": pid, "name": name, "city": r.get("City") if isinstance(r.get("City"), str) else "",
                       "county": norm_wi_county(county) if isinstance(county, str) else "",
                       "statuses": sorted(set(rows["Status"].astype(str))), "name_words": words})
    return plants


def _civic(host, slug, name, county):
    return {"id": slug, "name": name, "county": county, "reader": "civicclerk",
            "api": f"https://{host}.api.civicclerk.com/v1", "index": f"https://{host}.portal.civicclerk.com/"}


def _ac(slug, name, county, site):
    return {"id": slug, "name": name, "county": county, "reader": "agendacenter", "site": site}


def _leg(client, county, label, ids):
    host = client
    return [{"id": f"{client}-{slug}", "name": f"{label} {name}", "county": county, "reader": "legistar",
             "client": host, "body_id": bid, "index": f"https://{host}.legistar.com/Calendar.aspx"}
            for bid, slug, name in ids]


BROWN_COMMITTEES = ["county-board-of-supervisors", "executive-committee", "planning-development--transportation-committee",
                    "brown-county-planning-commission-board-of-directors", "land-conservation-sub-committee",
                    "administration-committee", "board-of-adjustment", "solid-waste-board", "public-safety-committee"]

# Boards worth reading at the high-volume civicclerk bodies (Rock County, Green Bay and Beaver Dam list
# well over 1,000 documents each). A document is kept when its title (the meeting name plus the file
# name) matches one of these. --all-boards turns the filter off.
LAND_USE_BOARDS = [r"plan(ning)? (commission|board|committee)|plan commission|zoning|land (use|conservation|resources|management)|"
                   r"economic development|redevelopment|community development|board of (appeals|adjustment)|"
                   r"finance|public works|utilit(y|ies)|infrastructure|committee of the whole|"
                   r"(city|common|village|town) (council|board)|county board|board of supervisors|executive|"
                   r"special (council|meeting)|data ?cent|power|energy"]

BODIES = [
    *_leg("milwaukee", "Milwaukee", "City of Milwaukee", [
        (1, "council", "Common Council"), (11, "znd", "Zoning, Neighborhoods and Development Committee"),
        (199, "ced", "Community and Economic Development Committee"), (272, "plan", "City Plan Commission"),
        (75, "racm", "Redevelopment Authority"), (5, "finance", "Finance and Personnel Committee")]),
    *_leg("madison", "Dane", "City of Madison", [(1, "council", "Common Council"), (3, "plan", "Plan Commission"),
                                                  (235, "carpc", "Capital Area Regional Planning Commission")]),
    *[{"id": f"racine-{slug}", "name": f"City of Racine {name}", "county": "Racine", "reader": "legistar_html",
       "client": "cityofracine", "body_name": name, "index": "https://cityofracine.legistar.com/Calendar.aspx"}
      for slug, name in [("council", "Common Council"), ("cow", "Committee of the Whole"),
                         ("phdc", "Planning Heritage and Design Commission"), ("exec", "Executive Committee"),
                         ("finance", "Finance and Personnel Committee"), ("pws", "Public Works and Services Committee"),
                         ("cda", "Community Development Authority")]],
    *_leg("dane", "Dane", "Dane County", [(138, "board", "County Board"), (190, "zlr", "Zoning and Land Regulation Committee"),
                                           (189, "pwt", "Public Works and Transportation Committee"),
                                           (139, "eanr", "Environment, Agriculture and Natural Resources Committee"),
                                           (191, "exec", "Executive Committee"), (369, "datacenters", "Advisory Committee on Data Centers")]),
    *_leg("waukesha", "Waukesha", "City of Waukesha", [(138, "council", "City Council"), (185, "plan", "Plan Commission"),
                                                        (250, "cow", "Committee of the Whole")]),
    {**_civic("rockcowi", "rock-county", "Rock County Board and committees", "Rock"), "boards": LAND_USE_BOARDS},
    {**_civic("beaverdamwi", "beaver-dam", "City of Beaver Dam", "Dodge"), "boards": LAND_USE_BOARDS},
    {**_civic("greenbaywi", "green-bay", "City of Green Bay", "Brown"), "boards": LAND_USE_BOARDS},
    _civic("kronenwetterwi", "kronenwetter", "Village of Kronenwetter", "Marathon"),
    _ac("mount-pleasant", "Village of Mount Pleasant", "Racine", "https://www.mtpleasantwi.gov"),
    _ac("ozaukee-county", "Ozaukee County", "Ozaukee", "https://www.ozaukeecounty.gov"),
    _ac("calumet-county", "Calumet County", "Calumet", "https://www.calumetcounty.org"),
    _ac("superior", "City of Superior", "Douglas", "https://www.superiorwi.gov"),
    _ac("douglas-county", "Douglas County", "Douglas", "https://www.douglascountywi.gov"),
    _ac("menomonie", "City of Menomonie", "Dunn", "https://www.menomonie-wi.gov"),
    _ac("walworth-county", "Walworth County", "Walworth", "https://www.co.walworth.wi.us"),
    _ac("kenosha-county", "Kenosha County", "Kenosha", "https://www.kenoshacountywi.gov"),
    _ac("oak-creek", "City of Oak Creek", "Milwaukee", "https://www.oakcreekwi.gov"),
    {"id": "sheboygan", "name": "City of Sheboygan", "county": "Sheboygan", "reader": "municode",
     "site": "https://sheboygan-wi.municodemeetings.com", "index": "https://sheboygan-wi.municodemeetings.com/meetings3"},
    {"id": "deforest", "name": "Village of DeForest", "county": "Dane", "reader": "granicus",
     "site": "https://deforestwi.granicus.com", "view_id": 1},
    {"id": "brown-county", "name": "Brown County Board and committees", "county": "Brown", "reader": "brown",
     "site": "https://www.browncountywi.gov", "committees": BROWN_COMMITTEES,
     "index": "https://www.browncountywi.gov/government/minutes_and_agendas/"},
    {"id": "port-washington", "name": "City of Port Washington Common Council and Plan Commission", "county": "Ozaukee",
     "reader": "pages", "render": True,
     "pages": ["https://www.portwashingtonwi.gov/our-city/boards-commissions-committees/common-council",
               "https://www.portwashingtonwi.gov/our-city/boards-commissions-committees/plan-commission"]},
    {"id": "racine-county", "name": "Racine County Board and committees", "county": "Racine", "reader": "pages",
     "render": True, "pages": ["https://www.racinecounty.gov/departments/county-board/all-boards-and-committees"],
     "follow": [r"/departments/county-board/all-boards-and-committees/[^/]+/?$",
                r"/all-boards-and-committees/[^/]+/(agendas|minutes|meeting-packet-s)/?$", r"/-folder-\d+$"]},
    {"id": "brillion", "name": "City of Brillion", "county": "Calumet", "reader": "pages", "render": True,
     "pages": ["https://www.brillionwi.gov/agendas", "https://www.brillionwi.gov/minutes"],
     "follow": [r"(/minutes-[a-z-]+|\?page=\d+)$", r"\?page=\d+$"]},
    {"id": "somers", "name": "Village of Somers", "county": "Kenosha", "reader": "wpmedia", "site": "https://www.somerswi.gov",
     "index": "https://www.somerswi.gov/government/agendas-minutes/"},
    {"id": "town-of-paris", "name": "Town of Paris", "county": "Kenosha", "reader": "wpmedia", "site": "https://townofparis.org",
     "index": "https://townofparis.org/government/agenda-minutes/"},
    {"id": "rothschild", "name": "Village of Rothschild", "county": "Marathon", "reader": "pages",
     "pages": ["https://www.rothschildwi.com/government/village_agendas_recordings___minute_meetings/index.php"]},
    {"id": "wrightstown", "name": "Village of Wrightstown", "county": "Outagamie", "reader": "pages", "render": True,
     "unescape": True, "pages": ["https://www.wrightstown.us/page/agendas"]},
    {"id": "dodge-county", "name": "Dodge County Board and committees", "county": "Dodge", "reader": "pages",
     "render": True, "pages": ["https://co.dodge.wi.gov/government/county-board/meetings",
               "https://co.dodge.wi.gov/government/land-water-conservation/document-center"]},
    {"id": "menomonee-falls", "name": "Village of Menomonee Falls", "county": "Waukesha", "reader": "swagit",
     "site": "https://menomoneefallswi.new.swagit.com",
     "pages": ["http://menomoneefallswi.swagit.com/village-board/", "http://menomoneefallswi.swagit.com/plan-commission/"],
     "index": "https://menomoneefallswi.new.swagit.com/"},
]

# Bodies that post no current records, or whose records sit behind a portal a person opens.
# Each is a human wall for that body alone (scopes/us-wi/coverage.json, local_records).
NOT_POSTED = [
    {"name": "City of Janesville Council and Plan Commission", "county": "Rock",
     "why": "agendas and minutes sit in a Laserfiche WebLink portal (cms.ci.janesville.wi.us/WebLink) that has no listing a script can read; a person opens the meeting folders for 2024 onward"},
    {"name": "City of Beloit Council and Plan Commission", "county": "Rock",
     "why": "agendas sit in a Laserfiche portal and a PowerDMS site behind Cloudflare that list no meetings a script can read; a person opens them"},
    {"name": "Village of Caledonia Board and Plan Commission", "county": "Racine",
     "why": "the village posts agendas through an eboard site built by script that exposes no document list; ask the village clerk"},
    {"name": "Village of Darien", "county": "Walworth",
     "why": "no village site posting agendas or minutes was found; ask the village clerk"},
]

# Projects that are not GEM plants yet (developers and sites from scopes/us-wi/plan.md).
LEADS = {
    "Port Washington gas generation (docket 6630-CE-318)": r"6630-CE-318|port washington.{0,80}(generat|gas|turbine|combustion|power plant)",
    "Vantage and Oracle Port Washington campus": r"vantage.{0,60}(port washington|data cent|lighthouse)|lighthouse.{0,40}data|oracle.{0,60}(port washington|openai)|stargate",
    "Concord power station (docket 6630-CE-315)": r"6630-CE-315|concord.{0,40}(generat|power|station|unit|turbine)",
    "Microsoft Mount Pleasant": r"microsoft.{0,80}(mount pleasant|data cent|generat)|mount pleasant.{0,80}(data cent|microsoft|generat)",
    "Microsoft Kenosha and Caledonia": r"microsoft.{0,80}(kenosha|caledonia)|caledonia.{0,80}(data cent|microsoft)",
    "Meta Beaver Dam": r"meta.{0,60}(beaver dam|data cent)|beaver dam.{0,60}(data cent|meta)|6680-TE-115",
    "Forest Junction and Union Depot": r"forest junction|union depot|5-CE-162|invenergy.{0,80}(brillion|calumet|woodville)",
    "Foundry Ridge and Red Oak Ridge": r"foundry ridge|red oak ridge|9837-CE-100|invenergy.{0,80}(darien|somers|kenosha|walworth)",
    "North Madison gas plant (MISO J4164)": r"north madison.{0,60}(gas|power|plant|generat)|J4164",
    "We Energies generation": r"we energies.{0,80}(generat|gas|turbine|combustion|power plant|battery)|wisconsin electric power.{0,60}(generat|gas|turbine)",
    "Alliant gas generation": r"alliant.{0,80}(gas|generat|turbine|combustion|peaker)|wisconsin power (and|&) light.{0,60}(generat|gas|turbine)",
    "Madison Gas and Electric": r"madison gas (and|&) electric.{0,80}(gas|generat|turbine|combustion|peaker)|\bMGE\b.{0,60}(generat|gas|turbine|combustion)",
    "Dairyland and WPPI": r"dairyland power.{0,60}(gas|generat|turbine|plant)|\bWPPI\b.{0,60}(gas|generat|turbine|plant)",
    "ATC MISO gas interconnection": r"J4179|J4184|american transmission.{0,60}(gas|generat|interconnect)",
    "QTS, Cloverleaf, Greater Kudu data centers": r"\bQTS\b.{0,60}(wisconsin|data cent|generat)|cloverleaf.{0,60}(data|wisconsin)|greater kudu",
    "Yorkville data center": r"yorkville.{0,80}(data cent|generat|power|microgrid)",
    "Nemadji Trail": r"nemadji trail",
}

STRONG = re.compile(r"data ?cent(er|re)s?|power plant|generating (station|facility|plant|unit)|power station|"
                    r"combustion turbines?|gas turbines?|combined[- ]cycle|simple[- ]cycle|peaking (plant|units?)|"
                    r"natural gas[- ](fired|plant|power|generat)|\bmegawatts?\b|\b\d[\d,.]*\s?MW\b|energy center|"
                    r"reciprocating engines?|\bengines?\b.{0,40}(data cent|MW|megawatt|generat)|micro-?grids?|"
                    r"backup generat|standby generat|\bgenerat(ors?|ion)\b.{0,60}(data|MW|megawatt|fleet|plant|facility)|"
                    r"electric generation|substation.{0,40}(data|generat)|large load|"
                    r"\b(We Energies|Alliant|WPS|Wisconsin Public Service|MGE|Dairyland|WPPI|Xcel|Invenergy|ATC)\b.{0,60}(generat|gas|plant|turbine|load|data)", re.I)
CONTEXT = re.compile(r"rezon|zone change|map amendment|special use|conditional use|variance|tax incremental|\bTIF\b|\bTID\b|"
                     r"development agreement|developer'?s agreement|site plan|plat|annex|moratorium|"
                     r"payment in lieu|tax (abatement|incentive)|utility service agreement|PSC|certificate of public convenience", re.I)
DOC_KEEP = re.compile(r"agenda|minute|packet|order|staff report|commission|planning|zoning|council|"
                      r"board|hearing|ordinance|resolution|action", re.I)
MONTHS = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}

def log(msg):
    print(f"[harvest-wi-local] {msg}", file=sys.stderr, flush=True)


def text_of(fragment):
    return clean_ws(html.unescape(re.sub(r"<[^>]+>", " ", fragment or "")))


def date_of(s):
    """The first meeting date in a file name, link text or path, as YYYY-MM-DD, or ''."""
    s = urllib.parse.unquote(str(s or ""))

    def ok(y, m, d):
        try:
            return dt.date(y, m, d).isoformat()
        except ValueError:
            return ""

    for rx, order in [(r"(?<!\d)(20[12]\d)[-_.](\d{1,2})[-_.](\d{1,2})(?!\d)", "ymd"),
                      (r"(?<!\d)(\d{1,2})[-_./](\d{1,2})[-_./](20[12]\d)(?!\d)", "mdy"),
                      (r"(?<!\d)(\d{2})(\d{2})(20[12]\d)(?!\d)", "mdy"),
                      (r"(?<!\d)(20[12]\d)(\d{2})(\d{2})(?!\d)", "ymd"),
                      (r"(?<!\d)(\d{1,2})[-_.](\d{1,2})[-_.](\d{2})(?!\d)", "mdy2"),
                      (r"(?:^|/)(\d{2})(\d{2})(\d{2})(?=[ _-]?[A-Za-z])", "mdy2"),
                      (r"(?<!\d)(20[12]\d)(\d)(\d{2})(?=[A-Za-z])", "ymd")]:
        for m in re.finditer(rx, s):
            a, b, c = (int(x) for x in m.groups())
            got = ok(a, b, c) if order == "ymd" else ok(c, a, b) if order == "mdy" else ok(2000 + c, a, b)
            if got:
                return got
    m = re.search(r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+(\d{1,2}),?\s+(20[12]\d)", s, re.I)
    if m:
        return ok(int(m.group(3)), MONTHS[m.group(1).lower()], int(m.group(2)))
    m = re.search(r"\b(20[12]\d)\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+(\d{1,2})\b", s, re.I)
    if m:   # "2025 October 6 Plan Commission" (Brillion)
        return ok(int(m.group(1)), MONTHS[m.group(2).lower()], int(m.group(3)))
    m = re.search(r"/uploads/(20[12]\d)/(\d{2})/", s)
    return ok(int(m.group(1)), int(m.group(2)), 1) if m else ""


def kind_of(s):
    s = s.lower()
    for k, rx in [("minutes", r"minute|action report|verbatim"), ("packet", r"packet|staff[ _-]?report|attachment"),
                  ("agenda", r"agenda|action form")]:
        if re.search(rx, s):
            return k
    return "document"


def doc(body, url, title, date, kind=None, item=""):
    return {"body": body["id"], "url": url, "title": clean_ws(title)[:200], "date": date,
            "kind": kind or (kind_of(title) if kind_of(title) != "document" else kind_of(url.rsplit("/", 1)[-1])),
            "item": clean_ws(item)[:300]}


# ---------------------------------------------------------------- listers ---

class Net:
    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": CHROME_UA, "Accept-Language": "en-US,en;q=0.9"})

    def json(self, url, params=None):
        for attempt in range(3):
            try:
                r = self.s.get(url, params=params, timeout=120)
                if r.status_code == 200:
                    return r.json()
                err = r.status_code
            except (requests.RequestException, ValueError) as e:
                err = "000"
                log(f"  {url}: {str(e)[:100]}")
            time.sleep(2 * (attempt + 1))
        report_failure(url, err, "local records listing failed three times")
        return None

    def page(self, url, render=False):
        for attempt in range(3):
            p = fetch_page(url, timeout=120, force_render=True) if render else get(url, timeout=120)
            if p.status == "200":
                return p.text
            log(f"  {url}: {p.status}")
            time.sleep(5 * (attempt + 1))
        report_failure(url, p.status, "local records index page failed three times")
        return None


def list_legistar(net, body, since, until):
    base = LEGISTAR.format(client=body["client"])
    flt = (f"EventBodyId eq {body['body_id']} and EventDate ge datetime'{since}' "
           f"and EventDate le datetime'{until}'")
    events = net.json(f"{base}/Events", {"$filter": flt, "$orderby": "EventDate desc"})
    if events is None:
        return None
    docs = []
    for e in events:
        date = (e.get("EventDate") or "")[:10]
        for key, kind in [("EventAgendaFile", "agenda"), ("EventMinutesFile", "minutes")]:
            if e.get(key):
                docs.append(doc(body, e[key], f"{body['name']} {kind} {date}", date, kind))
        items = net.json(f"{base}/Events/{e['EventId']}/EventItems", {"Attachments": 1})
        for it in items or []:
            label = " ".join(str(it.get(k) or "") for k in ("EventItemTitle", "EventItemMatterName", "EventItemMatterFile"))
            names = " ".join(a.get("MatterAttachmentName") or "" for a in it.get("EventItemMatterAttachments") or [])
            if not (STRONG.search(label + " " + names) or any(re.search(p, label, re.I) for p in LEADS.values())):
                continue
            for a in it.get("EventItemMatterAttachments") or []:
                # The attachment's own hyperlink (louisville.legistar1.com/model/attachments/...) answers
                # 404 since 2026; the API's file endpoint serves the same PDF (checked 2026-11-05).
                if it.get("EventItemMatterId") and a.get("MatterAttachmentId"):
                    url = f"{base}/Matters/{it['EventItemMatterId']}/Attachments/{a['MatterAttachmentId']}/File"
                elif a.get("MatterAttachmentHyperlink"):
                    url = a["MatterAttachmentHyperlink"]
                else:
                    continue
                docs.append(doc(body, url, a.get("MatterAttachmentName") or "attachment", date, "packet", item=label))
        time.sleep(0.2)
    return docs


def parse_legistar_calendar(text, body, since="0000", until="9999"):
    """Meeting rows of a Legistar Calendar.aspx grid: the date cell plus the Agenda (M=A) and Minutes (M=M)
    View.ashx links."""
    docs = []
    base = f"https://{body['client']}.legistar.com/"
    for row in re.findall(r'<tr class="rg(?:Alt)?Row"[^>]*>(.*?)</tr>', text or "", re.S):
        m = re.search(r"(?<!\d)(\d{1,2})/(\d{1,2})/(20\d\d)(?!\d)", text_of(row))
        if not m:
            continue
        date = f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}"
        if not since <= date <= until:
            continue
        for kind, code in [("agenda", "A"), ("minutes", "M")]:
            l = re.search(r'href="(View\.ashx\?M=%s&amp;ID=\d+&amp;GUID=[0-9A-Fa-f-]+)"' % code, row)
            if l:
                docs.append(doc(body, base + html.unescape(l.group(1)), f"{body['name']} {kind} {date}", date, kind))
    return docs


def list_legistar_html(net, body, since, until):
    """A Legistar client whose open API is switched off (City of Racine answers 400): post the calendar
    form once per year for the body and read the grid, which is one page for a year of one body."""
    url = f"https://{body['client']}.legistar.com/Calendar.aspx"
    docs = []

    def cs(text):
        return json.dumps({"logEntries": [], "value": "", "text": text, "enabled": True,
                           "checkedIndices": [], "checkedItemsTextOverflows": False})
    for year in range(int(since[:4]), int(until[:4]) + 1):
        page = net.page(url)
        if page is None:
            return docs or None
        f = {m.group(1): html.unescape(m.group(2)) for m in re.finditer(r'<input[^>]*name="(__[A-Z]+)"[^>]*value="([^"]*)"', page)}
        f.update({"ctl00$ContentPlaceHolder1$lstYears": str(year), "ctl00_ContentPlaceHolder1_lstYears_ClientState": cs(str(year)),
                  "ctl00$ContentPlaceHolder1$lstBodies": body["body_name"],
                  "ctl00_ContentPlaceHolder1_lstBodies_ClientState": cs(body["body_name"]),
                  "ctl00$ContentPlaceHolder1$btnSearch": "Search Calendar"})
        try:
            r = net.s.post(url, data=f, timeout=120)
        except requests.RequestException as e:
            log(f"  {url}: {str(e)[:100]}")
            return docs or None
        if r.status_code != 200:
            report_failure(url, r.status_code, "local records listing failed")
            return docs or None
        docs += parse_legistar_calendar(r.text, body, since, until)
        time.sleep(0.5)
    return docs


def list_civicclerk(net, body, since, until):
    url = f"{body['api']}/Events"
    params = {"$filter": f"startDateTime ge {since}T00:00:00Z and startDateTime le {until}T23:59:59Z",
              "$orderby": "startDateTime desc"}
    docs = []
    while url:
        data = net.json(url, params)
        if data is None:
            return None if not docs else docs
        for e in data.get("value", []):
            date = (e.get("startDateTime") or "")[:10]
            for f in e.get("publishedFiles") or []:
                if f.get("fileId"):
                    docs.append(doc(body, f"{body['api']}/Meetings/GetMeetingFileStream(fileId={f['fileId']},plainText=false)",
                                    f"{e.get('eventName', '')} {f.get('name') or f.get('type') or ''}", date,
                                    kind_of(f.get("type") or f.get("name") or "")))
        url, params = data.get("@odata.nextLink"), None
    return docs


def parse_agendacenter(text, body):
    docs = []
    for row in re.split(r'<tr id="row', text or "")[1:]:
        m = re.search(r'id="_(\d{8})-(\d+)"', row)
        if not m:
            continue
        md = m.group(1)
        date = f"{md[4:]}-{md[:2]}-{md[2:4]}"
        title = re.search(r'aria-describedby="h4[^"]*"[^>]*>(.*?)</a>', row, re.S)
        title = text_of(title.group(1)) if title else ""
        seen = set()
        for href in re.findall(r'href="(/AgendaCenter/ViewFile/(?:Agenda|Minutes)/_[^"]+)"', row):
            href = html.unescape(href)
            if href in seen:
                continue
            seen.add(href)
            kind = "minutes" if "/Minutes/" in href else "packet" if "packet" in href.lower() else "agenda"
            docs.append(doc(body, body["site"] + href, f"{title} {kind}", date, kind))
    return docs


def list_agendacenter(net, body, since, until):
    s, u = dt.date.fromisoformat(since), dt.date.fromisoformat(until)
    url = (f"{body['site']}/AgendaCenter/Search/?term=&CIDs=all&startDate={s:%m/%d/%Y}&endDate={u:%m/%d/%Y}"
           "&dateRange=&dateSelector=")
    text = net.page(url)
    return None if text is None else parse_agendacenter(text, body)


LINK_RX = re.compile(r"\.pdf($|\?)|/DocumentCenter/View/|/AgendaCenter/ViewFile/|/files/\d+/|/home/showpublisheddocument|"
                     r"showpublisheddocument|/a/uploads/|aptg\.co/|/i/(agendas|minutes)/|document[_ %20]center|/ArchiveCenter/View/", re.I)


def unescape_json_html(text):
    """A page built by script carries its HTML as escaped JSON (\\" and \\/ and \\u003c); undo that."""
    text = text.replace('\\\\"', '"').replace('\\"', '"').replace("\\/", "/")
    return re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), text)


def parse_links(text, base, body, since):
    """Every dated document link on an index page."""
    docs, seen = [], set()
    text = text or ""
    if body.get("unescape"):
        text = unescape_json_html(text)
    tag = re.search(r'<base\b[^>]*href=["\']([^"\']+)["\']', text, re.I)
    if tag:   # a page's <base> tag sets where its relative links point, as in a browser
        base = urllib.parse.urljoin(base, html.unescape(tag.group(1)).strip())
    for m in re.finditer(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', text, re.S | re.I):
        href, label = m.groups()
        href = html.unescape(href).strip()
        if not LINK_RX.search(href):
            continue
        url = urllib.parse.urljoin(base, href).replace(" ", "%20")
        if url in seen:
            continue
        label = text_of(label)
        path = urllib.parse.urlsplit(href).path
        row = text.rfind("<tr", 0, m.start())
        row = text_of(text[row:m.start()]) if row != -1 and text.rfind("</tr>", row, m.start()) == -1 else ""
        date = date_of(label) or date_of(path.rsplit("/", 1)[-1]) or date_of(path) or date_of(row)
        if not date:
            y = re.search(r"(?<!\d)(20[12]\d)\s*-\s*(20[12]\d)(?!\d)", f"{label} {urllib.parse.unquote(href)}")   # a term book: dated to its end year
            y = y or re.search(r"\b(20[12]\d)\b", f"{label} {href}")
            date = f"{y.group(y.lastindex)}-01-01" if y else ""
        if not date or date < since[:4] + "-01-01" or (date < since and not date.endswith("-01-01")):
            continue
        seen.add(url)   # a file linked twice (an icon, then its "Download ..." title) is kept once, from the dated link
        docs.append(doc(body, url, label or href.rsplit("/", 1)[-1], date))
    return docs


def page_links(text, base, pattern, limit=60, since_year=0):
    """Same-site pages a body's index links to (its committee pages, year folders, next pages), for the
    `follow` setting. The pattern is tried on the path plus the query; a link whose text is only a year
    older than since_year is dropped (Racine County keeps one folder per year)."""
    out = []
    for h, label in re.findall(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', text or "", re.S | re.I):
        url = urllib.parse.urljoin(base, html.unescape(h).strip()).split("#")[0]
        parts = urllib.parse.urlsplit(url)
        y = re.fullmatch(r"\s*(20[12]\d)\s*", text_of(label))
        if y and since_year and int(y.group(1)) < since_year:
            continue
        if re.search(pattern, parts.path + ("?" + parts.query if parts.query else "")) and url not in out:
            out.append(url)
    return out[:limit]


def list_pages(net, body, since, until):
    """Read each index page, then follow its links level by level. `follow` is one pattern (links on the
    index pages) or a list of patterns, one per level (Racine County: committee, then Agendas / Minutes /
    Meeting Packets, then one folder per year)."""
    docs, read, seen = [], 0, set()
    follow = body.get("follow") or []
    follow = [follow] if isinstance(follow, str) else follow
    todo = [(u, 0) for u in body["pages"]]
    done = set()
    while todo:
        url, level = todo.pop(0)
        if url in done:
            continue
        done.add(url)
        text = net.page(url, render=body.get("render", False))
        if text is None:
            continue
        read += 1
        for d in parse_links(text, url, body, since):
            if d["url"] not in seen:
                seen.add(d["url"])
                docs.append(d)
        if level < len(follow):
            todo += [(u, level + 1) for u in page_links(text, url, follow[level], since_year=int(since[:4]))]
    return docs if read else None


def list_wpmedia(net, body, since, until):
    """A WordPress site's media library through /wp-json/wp/v2/media (Somers, Town of Paris): every PDF
    uploaded since the date, kept when its title looks like a meeting record. The page route is walled or
    thin on both sites, the library lists every upload with its title and address."""
    docs, page, total = [], 1, 1
    while page <= total and page <= 60:
        url = (f"{body['site']}/wp-json/wp/v2/media?per_page=100&page={page}&mime_type=application/pdf"
               f"&after={since}T00:00:00&orderby=date&order=desc&_fields=id,date,title,source_url")
        text = net.page(url)
        try:
            rows = json.loads(text) if text else None
        except ValueError:
            rows = None
        if not isinstance(rows, list):
            return docs or None
        if not rows:
            break
        for r in rows:
            title = text_of((r.get("title") or {}).get("rendered") or "")
            src = r.get("source_url") or ""
            label = f"{title} {src.rsplit('/', 1)[-1]}"
            if not DOC_KEEP.search(label):
                continue
            date = date_of(label) or (r.get("date") or "")[:10]
            if date >= since:
                docs.append(doc(body, src, title or src.rsplit("/", 1)[-1], date))
        if len(rows) < 100:
            break
        page += 1
    return docs


def parse_swagit(text, body, since="0000", until="9999"):
    """Swagit video index (Menomonee Falls): one table row per meeting, with the committee, the date and
    an Agenda link. The agenda address hands off to the village's public agenda site (a page with the
    agenda text and a packet PDF)."""
    docs, seen = [], set()
    host = body["site"]
    for row in re.findall(r"<tr>(.*?)</tr>", text or "", re.S | re.I):
        m = re.search(r'href="(/videos/\d+)/agenda"', row)
        cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S | re.I)
        if not m or len(cells) < 2:
            continue
        date = date_of(text_of(cells[1]))
        url = host + m.group(1) + "/agenda"
        if not date or date < since or date > until or url in seen:
            continue
        seen.add(url)
        docs.append(doc(body, url, f"{text_of(cells[0])} agenda and packet {date}", date, "agenda"))
    return docs


def list_swagit(net, body, since, until):
    docs, read, seen = [], 0, set()
    for u in body["pages"]:
        text = net.page(u)
        if text is None:
            continue
        read += 1
        for d in parse_swagit(text, body, since, until):
            if d["url"] not in seen:
                seen.add(d["url"])
                docs.append(d)
    return docs if read else None


def parse_municode(text, body, since="0000", until="9999"):
    """Municode Meetings table: one row per meeting with a content="YYYY-MM-DD..." date and PDF links."""
    docs = []
    for row in re.split(r'<tr class="(?:odd|even)', text or "")[1:]:
        d = re.search(r'content="(20\d\d-\d\d-\d\d)', row)
        if not d or not since <= d.group(1) <= until:
            continue
        date = d.group(1)
        title = re.search(r'data-th="Meeting">(.*?)</td>', row, re.S)
        title = text_of(title.group(1)) if title else ""
        for cell, kind in (("agendas", "agenda"), ("packets", "packet"), ("minutes", "minutes")):
            seg = re.search(rf'field-field-{cell}"[^>]*>(.*?)</td>', row, re.S)
            for href in re.findall(r'href="([^"]+\.pdf[^"]*)"', seg.group(1) if seg else ""):
                docs.append(doc(body, html.unescape(href), f"{title} {kind} {date}", date, kind))
    return docs


def list_municode(net, body, since, until):
    docs, seen, read = [], set(), 0
    for page in range(0, 40):
        url = body["index"] + (f"?page={page}" if page else "")
        text = net.page(url)
        if text is None:
            break
        read += 1
        dates = re.findall(r'content="(20\d\d-\d\d-\d\d)', text)
        for d in parse_municode(text, body, since, until):
            if d["url"] not in seen:
                seen.add(d["url"])
                docs.append(d)
        if not dates or min(dates) < since:
            break
        time.sleep(0.2)
    return docs if read else None


def parse_brown_list(text, base, since):
    """A Brown County committee page: dated ?i= links, one per meeting. Returns (url, label, date)."""
    out, seen = [], set()
    for href, label in re.findall(r'<a[^>]*href="([^"]*\?i=[0-9a-f]+)"[^>]*>(.*?)</a>', text or "", re.S):
        url = urllib.parse.urljoin(base, html.unescape(href))
        label = text_of(label)
        date = date_of(label)
        if not date or date < since or url in seen:
            continue
        seen.add(url)
        out.append((url, label, date))
    return out


def parse_brown_detail(text, base):
    return [urllib.parse.urljoin(base, html.unescape(h)).replace(" ", "%20")
            for h in re.findall(r'<a[^>]*href="(/i/(?:agendas|minutes)/[^"]+\.pdf)"', text or "")]


def list_brown(net, body, since, until):
    docs, seen, read = [], set(), 0
    for slug in body["committees"]:
        for kind in ("agendas", "minutes"):
            base = f"{body['site']}/government/minutes_and_agendas/{kind}/{slug}/"
            text = net.page(base)
            if text is None:
                continue
            read += 1
            for url, label, date in parse_brown_list(text, base, since):
                if date > until:
                    continue
                detail = net.page(url)
                for pdf in parse_brown_detail(detail, url):
                    if pdf not in seen:
                        seen.add(pdf)
                        docs.append(doc(body, pdf, f"{slug.replace('-', ' ')} {kind[:-1]} {label}", date, kind[:-1]))
                time.sleep(0.2)
    return docs if read else None


def parse_granicus(text, body, since="0000", until="9999"):
    docs = []
    for row in re.split(r'<tr class="listingRow"', text or "")[1:]:
        name = re.search(r'headers="Name"[^>]*>(.*?)</td>', row, re.S)
        name = text_of(name.group(1)) if name else ""
        if body.get("boards") and not re.search(body["boards"], name, re.I):
            continue
        d = re.search(r'headers="Date"[^>]*>(.*?)</td>', row, re.S)
        dtext = text_of(d.group(1)).replace("\xa0", " ") if d else ""
        date = date_of(dtext)
        if not date or not since <= date <= until:
            continue
        if re.search(r"cancel", row, re.I) and not re.search(r"href=", row):
            continue
        for href, label in re.findall(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', row, re.S):
            label = text_of(label)
            if not re.search(r"agenda|minutes|packet", label, re.I):
                continue
            url = urllib.parse.urljoin(body["site"] + "/", html.unescape(href))
            docs.append(doc(body, url, f"{name} {label} {date}", date, kind_of(label)))
    return docs


def list_granicus(net, body, since, until):
    text = net.page(f"{body['site']}/ViewPublisher.php?view_id={body['view_id']}")
    return None if text is None else parse_granicus(text, body, since, until)


LISTERS = {"legistar": list_legistar, "legistar_html": list_legistar_html, "civicclerk": list_civicclerk, "agendacenter": list_agendacenter,
           "pages": list_pages, "wpmedia": list_wpmedia, "swagit": list_swagit, "granicus": list_granicus, "municode": list_municode, "brown": list_brown}


# ---------------------------------------------------------------- reading ---

def pdf_text(path, ocr=True):
    try:
        t = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True, timeout=600).stdout
    except (subprocess.SubprocessError, OSError):
        t = ""
    if ocr and len(re.sub(r"\s", "", t)) < 400:
        import fetch
        try:
            o = fetch._pdf_ocr(str(path))
        except Exception:  # noqa: BLE001
            o = ""
        if len(o.strip()) > len(t.strip()):
            return o, True
    return t, False


def doc_file(folder, d):
    tail = urllib.parse.unquote(urllib.parse.urlsplit(d["url"]).path.rsplit("/", 1)[-1]) or "document"
    tail = re.sub(r"[^A-Za-z0-9._-]+", "_", re.sub(r"\.pdf$", "", tail, flags=re.I))[-80:]
    m = re.search(r"fileId=(\d+)", d["url"])
    if m:
        tail = f"file{m.group(1)}"
    m = re.search(r"FileOpen\.aspx\?Type=(\d+)&ID=(\d+)", d["url"])
    if m:
        tail = f"iqm2_type{m.group(1)}_id{m.group(2)}"
    m = re.search(r"showpublisheddocument/(\d+)", d["url"])
    if m:
        tail = f"doc{m.group(1)}"
    m = re.search(r"/document/(\d+)/", d["url"])
    if m:
        tail = f"cw{m.group(1)}_{tail}"
    m = re.search(r"AgendaViewer\.php\?.*?(?:clip|event)_id=(\d+)", d["url"])
    if m:
        tail = f"agenda{m.group(1)}"
    m = re.search(r"/Matters/(\d+)/Attachments/(\d+)/File", d["url"])
    if m:
        tail = f"matter{m.group(1)}_attachment{m.group(2)}"
    return folder / f"{d['date'] or 'nodate'}_{d['kind']}_{tail}.pdf"


def read(net, d, folder, ocr, max_bytes):
    """(text, state). A PDF is saved and kept; a host that refuses a plain request is read
    through fetch.py's ladder and only its text is kept."""
    pdf = doc_file(folder, d)
    txt = pdf.with_suffix(".txt")
    if txt.exists():
        d["saved"] = str(txt.relative_to(REPO))
        return txt.read_text(errors="replace"), "saved (from an earlier run)"
    body, state = b"", ""
    try:
        r = net.s.get(d["url"], timeout=300)
        body = r.content if r.status_code == 200 and len(r.content) <= max_bytes else b""
        state = f"plain request {r.status_code}"
    except requests.RequestException as e:
        state = f"plain request failed: {str(e)[:60]}"
    text, used_ocr = "", False
    if body[:5] == b"%PDF-":
        folder.mkdir(parents=True, exist_ok=True)
        pdf.write_bytes(body)
        text, used_ocr = pdf_text(pdf, ocr)
    else:
        p = get(d["url"], timeout=600)
        if p.status == "200" and p.text.strip():
            text, state = (p.text if p.is_pdf else text_of(p.text)), f"read through fetch.py ({p.status})"
            used_ocr = "pdf_ocr" in (p.notes or [])
        else:
            report_failure(d["url"], p.status, "local record")
            return "", f"not read ({state}; fetch.py {p.status})"
    if text.strip():
        folder.mkdir(parents=True, exist_ok=True)
        txt.write_text(text)
        d["saved"] = str(txt.relative_to(REPO))
    return text, state + (", OCR" if used_ocr else "") + ("" if text.strip() else ", no text")


# ---------------------------------------------------------------- finding ---

# Plant names that are also surnames, towns or rivers. In board minutes a bare "Paris", "Concord"
# or "Weston" is a place, so these need a plant word next to them. They replace any broader
# patterns for the local records only.
PLANT_WORD = r"(station|generating|generation|power|plant|unit|units|cc|ct|combined|combustion|peaker|peaking|rice|energy facility|energy center)"
LOCAL_KNOWN = {
    "L100000104267": [r"blount street " + PLANT_WORD],
    "L100000104269": [r"edgewater " + PLANT_WORD],
    "L100000104274": [r"elm road " + PLANT_WORD],
    "L100000104276": [r"pulliam " + PLANT_WORD],
    "L100000104279": [r"valley " + PLANT_WORD + r".{0,20}(milwaukee|we energies)", r"valley power plant"],
    "L100000104280": [r"weston " + PLANT_WORD],
    "L100000104693": [r"port washington " + PLANT_WORD],
    "L100000401577": [r"west campus cogeneration"],
    "L100000401635": [r"sheboygan falls " + PLANT_WORD],
    "L100000401636": [r"south fond du lac " + PLANT_WORD],
    "L100000401640": [r"riverside energy center"],
    "L100000401676": [r"whitewater " + PLANT_WORD, r"LSP.whitewater"],
    "L100000401798": [r"marshfield utilities.{0,30}(gas|plant|generat)"],
    "L100000402073": [r"west marinette " + PLANT_WORD],
    "L100000402253": [r"rockgen"],
    "L100000402372": [r"concord " + PLANT_WORD],
    "L100000402373": [r"germantown " + PLANT_WORD],
    "L100000402374": [r"paris " + PLANT_WORD],
    "L100000402376": [r"neenah " + PLANT_WORD],
    "L100000402377": [r"rock river " + PLANT_WORD],
    "L100000402378": [r"de pere energy"],
    "L100000402379": [r"fox energy center"],
    "L100000402381": [r"west marinette " + PLANT_WORD],
    "L100000402388": [r"island street " + PLANT_WORD],
    "L100000402527": [r"combined locks energy"],
    "L100000407359": [r"nemadji trail"],
    "L100000409212": [r"diesel generators power station"],
    "L100000409233": [r"wheaton " + PLANT_WORD],
    "L100000409253": [r"weston rice", r"kronenwetter.{0,60}(engine|generat|power)"],
    "L100000409271": [r"french island " + PLANT_WORD],
    "L100001025603": [r"south oak creek " + PLANT_WORD, r"oak creek.{0,60}combustion turbine"],
    "L100001047775": [r"paris rice"],
    "L100001047813": [r"foundry ridge"],
    "L100001062057": [r"red oak ridge"],
    "L100001083378": [r"forest junction"],
    "L100001089647": [r"union depot"],
    "L100001089648": [r"fox north"],
    "L100001089674": [r"microsoft.{0,60}mount pleasant", r"mount pleasant.{0,60}microsoft"],
    "L100001089699": [r"vantage.{0,60}(lighthouse|port washington|data cent)", r"lighthouse.{0,30}data cent"],
}


def plant_patterns(plants):
    pats = {}
    for p in plants:
        rx = list(LOCAL_KNOWN.get(p["id"], []))
        if rx:
            pats[p["id"]] = rx
    return pats


def findings(text, pats, county_plants):
    """What a document says: plants and leads named, and the sentences about power or data
    center projects (a plant or lead name, or a strong power word)."""
    named, leads, keep = set(), set(), []
    for s in sentences(re.sub(r"[ \t]+", " ", text)):
        if len(s) < 15 or len(s) > 600:
            continue
        hit = False
        for pid, rx in pats.items():
            if any(re.search(r, s, re.I) for r in rx):
                named.add(pid)
                hit = True
        for lead, rx in LEADS.items():
            if re.search(rx, s, re.I):
                leads.add(lead)
                hit = True
        if hit or STRONG.search(s):
            if s not in keep:
                keep.append(s)
    nearby = sorted(set(county_plants) - named) if keep else []
    return {"named": sorted(named), "leads": sorted(leads), "nearby": nearby,
            "context": sorted({m.group(0).lower() for s in keep for m in CONTEXT.finditer(s)})[:8],
            "sentences": keep[:12]}


# ----------------------------------------------------------------- output ---

def write_outputs(out_dir, plants, bodies, records, since, today):
    out_dir.mkdir(parents=True, exist_ok=True)
    by_plant = {p["id"]: [] for p in plants}
    for i, r in enumerate(records):
        for pid in r["named"]:
            by_plant[pid].append(i)
    by_county = {}
    for p in plants:
        by_county.setdefault(p["county"], []).append(p["id"])
    no_minutes = [{**n, "plants": by_county.get(n["county"], [])} for n in NOT_POSTED]
    data = {"generated": today, "since": since, "bodies": bodies, "records": records,
            "by_plant": by_plant, "not_posted": no_minutes}
    (out_dir / "local_records.json").write_text(json.dumps(data, indent=1))
    names = {p["id"]: p["name"] for p in plants}
    bname = {b["id"]: b["name"] for b in bodies}

    def line(r):
        L = [f"- {bname.get(r['body'], r['body'])}, {r['date'] or 'date not shown'}, {r['kind']}: {r['title'][:120]}, {r['url']}"]
        if r.get("item"):
            L.append(f"  - Agenda item: {r['item'][:200]}")
        if r["leads"]:
            L.append(f"  - Leads named: {', '.join(r['leads'])}")
        if r["context"]:
            L.append(f"  - Also mentions: {', '.join(r['context'])}")
        L += [f"  - \"{s[:300]}\"" for s in r["sentences"][:5]]
        return L

    L = [f"# Wisconsin local planning and commission records ({today})", "",
         f"Agendas, packets, staff reports and minutes posted since {since} by the bodies around the GEM plants "
         "and the leads, searched for plant and developer names and for power and data center words. A record "
         "is a lead: open the document at its address and cite it there. Copies are in scopes/us-wi/work/local/ "
         "and are not committed.", "", "## Bodies read", ""]
    for b in bodies:
        L.append(f"- {b['name']} ({b['county']} County, {b['reader']}): {b['state']}")
    L += ["", "## Records that name a GEM plant", ""]
    for p in plants:
        idx = by_plant[p["id"]]
        if idx:
            L += [f"### {p['name']} ({p['id']}), {p['county'] or 'county blank'} County", ""]
            for i in idx:
                L += line(records[i])
            L.append("")
    L += ["## Records that name a lead", ""]
    for r in records:
        if r["leads"] and not r["named"]:
            L += line(r)
    L += ["", "## Other power or data center mentions (check whether they are a new project)", ""]
    for r in records:
        if not r["leads"] and not r["named"] and r["sentences"]:
            L += line(r)
            if r["nearby"]:
                L.append(f"  - GEM plants in the same county: {', '.join(names[x] for x in r['nearby'])}")
    L += ["", "## Bodies whose records are not posted or sit behind a portal a person opens", ""]
    for n in no_minutes:
        L.append(f"- {n['name']} ({n['county']} County): {n['why']}."
                 + (f" GEM plants in the county: {', '.join(names[x] for x in n['plants'])}." if n["plants"] else ""))
    (out_dir / "local_records.md").write_text("\n".join(L) + "\n")


# ------------------------------------------------------------------- main ---

def main():
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    ap.add_argument("--since", default="2024-01-01")
    ap.add_argument("--bodies", help="comma-separated body ids (default: every body)")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--max-docs", type=int, default=0, help="read at most this many documents per body, newest first (0: all)")
    ap.add_argument("--max-mb", type=float, default=60)
    ap.add_argument("--all-boards", action="store_true", help="ignore each body's `boards` filter (Rock County, Green Bay, Beaver Dam)")
    ap.add_argument("--list-only", action="store_true", help="list documents, read nothing")
    ap.add_argument("--no-ocr", action="store_true", help="skip OCR of scanned documents")
    a = ap.parse_args()
    tag_batch("us-wi")
    until = dt.date.today().isoformat()
    plants = load_plants()
    pats = plant_patterns(plants)
    county_plants = {}
    for p in plants:
        county_plants.setdefault(p["county"], []).append(p["id"])
    wanted = set(a.bodies.split(",")) if a.bodies else None
    work = scope_work("us-wi") / "local"
    net = Net()
    bodies, records = [], []
    for b in BODIES:
        if wanted and b["id"] not in wanted:
            continue
        docs = LISTERS[b["reader"]](net, b, a.since, until)
        info = {k: b[k] for k in ("id", "name", "county", "reader")}
        info["index"] = b.get("index") or b.get("site") or b.get("api") or b["pages"][0]
        if docs is None:
            info.update(listed=0, read=0, state="the listing did not load (logged for access_audit.py --retry)")
            bodies.append(info)
            log(f"{b['id']}: listing failed")
            continue
        if b.get("boards") and b["reader"] != "granicus" and not a.all_boards:   # the granicus lister applies its own `boards` pattern
            keep = re.compile("|".join([b["boards"]] if isinstance(b["boards"], str) else b["boards"]), re.I)
            total = len(docs)
            docs = [d for d in docs if keep.search(f"{d['title']} {d.get('item', '')}")]
            log(f"{b['id']}: boards filter kept {len(docs)} of {total} documents")
        docs.sort(key=lambda d: d["date"], reverse=True)
        todo = docs if not a.max_docs else docs[:a.max_docs]
        n_read = n_ocr = 0
        for d in ([] if a.list_only else todo):
            text, state = read(net, d, work / b["id"], not a.no_ocr, int(a.max_mb * 1e6))
            d["state"] = state
            n_read += bool(text.strip())
            n_ocr += "OCR" in state
            if text.strip():
                d.update(findings(text, pats, county_plants.get(b["county"], [])))
                if d["sentences"]:
                    records.append(d)
            time.sleep(0.2)
        info.update(listed=len(docs), read=n_read, ocr=n_ocr,
                    state=(f"{len(docs)} documents listed since {a.since}"
                           + ("" if a.list_only else f", {n_read} read" + (f" ({n_ocr} by OCR)" if n_ocr else ""))
                           + (f", newest {len(todo)} only" if a.max_docs and len(docs) > len(todo) else "")
                           + ("; no dated documents found on the index, check the address" if not docs else "")))
        bodies.append(info)
        log(f"{b['id']}: {info['state']}; {sum(1 for r in records if r['body'] == b['id'])} with findings")
    write_outputs(Path(a.out), plants, bodies, records, a.since, until)
    log(f"{len(records)} records with findings; outputs in {a.out}")


if __name__ == "__main__":
    main()


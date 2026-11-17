"""
Harvest New Mexico city and county planning, zoning, commission and council records before a sweep.

New Mexico data center and power sites are approved by the county commission or the city where
they sit (industrial revenue bonds, rezonings, special use permits, development agreements), and
those records name generator fleets, microgrids and turbines long before an air permit exists.
This reads every posted record since --since (default 2024-01-01) for the bodies around the GEM
plants and the leads, and keeps the sentences that name a plant, a lead or a power or data
center project. Nothing needs a sign-in. Routes (probed 2026-11-17):

  legistar     Albuquerque City Council and its committees (Council 1, Land Use Planning and
               Zoning 6, Committee of the Whole 7, Finance and Government Operations 9,
               Council Study Session 46, Albuquerque Development Commission 50) and Los Alamos
               County (Council 2, Planning and Zoning 35, Board of Public Utilities 204): the open
               API at webapi.legistar.com/v1/<client>/Events, agenda and minutes PDFs, and item
               attachments whose item names a power or data center project.
  civicclerk   Hobbs (City Commission), Carlsbad and Dona Ana County (Board of County
               Commissioners and Planning): the open OData API at <host>.api.civicclerk.com/v1/
               Events; GetMeetingFileStream downloads the PDFs.
  iqm2         Bernalillo County: the portal's Calendar.aspx for a year lists every meeting; each
               row links FileOpen.aspx PDFs (Agenda, Agenda Packet, Action Report, Minutes).
  civicweb     Las Cruces City Council: lascruces.civicweb.net MeetingTypeList, one
               MeetingInformation page per meeting, document links /document/<id>/<name>.pdf.
  granicus     Rio Rancho: riorancho.granicus.com/ViewPublisher.php?view_id=14, one page with
               every archived meeting, AgendaViewer, MinutesViewer and packet links.
  sjcounty     San Juan County: the county's calendar page (-toggle-allpast and -toggle-all lists),
               showpublisheddocument links; the page answers 403 to plain requests, so it is read
               through fetch.py.
  agendacenter CivicPlus AgendaCenter sites (Eddy County, Roswell, Farmington, Los Lunas, Grant
               County): /AgendaCenter/Search/?CIDs=all with a date range; files at
               /AgendaCenter/ViewFile/Agenda|Minutes/_MMDDYYYY-ID.
  pages        Every other body (Las Cruces boards, Valencia, Sandoval and Chaves counties): its
               agendas or minutes index page, read through fetch.py's access ladder, and every
               dated document link on it.

Scanned minutes are read by OCR (pdftoppm then tesseract, through fetch.py). Documents are
saved under scopes/us-nm/work/local/<body>/ (not committed). Bodies that post no records are
listed for a person (the coverage list's human wall). Nothing here stages a record.

Output, in batches/us-nm/harvest/: local_records.json and local_records.md.

Usage (from the repo root):
    python scopes/us-nm/harvest_local.py                          # every body since 2024
    python scopes/us-nm/harvest_local.py --bodies hobbs,grant-county --since 2025-01-01
    python scopes/us-nm/harvest_local.py --list-only              # list documents, read nothing
    python scopes/us-nm/harvest_local.py --no-ocr
"""
import argparse
import datetime as dt
import html
import json
import re
import subprocess
import sys
import time
import unicodedata
import urllib.parse
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from fetch import CHROME_UA  # noqa: E402
from harvest_lib import REPO, clean_ws, get, report_failure, sentences, tag_batch  # noqa: E402

from paths import scope_work  # noqa: E402

OUT = REPO / "batches" / "us-nm" / "harvest"
CSV = REPO / "scripts" / "gem_export_gogpt_scoped.csv"
LEGISTAR = "https://webapi.legistar.com/v1/{client}"


def norm_nm_county(s):
    """'Doña Ana', 'Dona Ana County' and 'LEA' all become 'Dona Ana' / 'Lea'."""
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"\s+county$", "", s.strip(), flags=re.I).strip().title()


def load_plants(csv_path=None):
    import pandas as pd
    csv = pd.read_csv(csv_path or CSV, low_memory=False, encoding="utf-8-sig")
    csv = csv[csv["State/Province"] == "New Mexico"]
    plants = []
    for pid, rows in csv.groupby("GEM location ID", sort=False):
        r = rows.iloc[0]
        county = r.get("Local area (taluk, county)")
        name = str(r["Plant name"])
        words = {w for w in re.findall(r"[a-z]+", name.lower())
                 if w not in {"power", "station", "plant", "plants", "generating", "facility", "energy", "center",
                              "data", "new", "mexico", "nm", "irp", "the", "of", "gas", "microgrid", "layer",
                              "information", "park", "county", "clean", "path"}}
        plants.append({"id": pid, "name": name, "city": r.get("City") if isinstance(r.get("City"), str) else "",
                       "county": norm_nm_county(county) if isinstance(county, str) else "",
                       "statuses": sorted(set(rows["Status"].astype(str))), "name_words": words})
    return plants


def _civic(host, slug, name, county, extra=""):
    return {"id": slug, "name": name, "county": county, "reader": "civicclerk",
            "api": f"https://{host}.api.civicclerk.com/v1", "index": f"https://{host}.portal.civicclerk.com/",
            "category": extra}


def _ac(slug, name, county, site):
    return {"id": slug, "name": name, "county": county, "reader": "agendacenter", "site": site}


BODIES = [
    *[{"id": f"albuquerque-{slug}", "name": f"City of Albuquerque {name}", "county": "Bernalillo", "reader": "legistar",
       "client": "cabq", "body_id": bid, "index": "https://cabq.legistar.com/Calendar.aspx"}
      for bid, slug, name in [(1, "council", "City Council"), (6, "lupz", "Land Use, Planning, and Zoning Committee"),
                              (7, "cow", "Committee of the Whole"), (9, "finance", "Finance and Government Operations Committee"),
                              (46, "study", "Council Study Session"), (50, "adc", "Albuquerque Development Commission")]],
    *[{"id": f"los-alamos-{slug}", "name": f"Los Alamos County {name}", "county": "Los Alamos", "reader": "legistar",
       "client": "losalamos", "body_id": bid, "index": "https://losalamos.legistar.com/Calendar.aspx"}
      for bid, slug, name in [(2, "council", "County Council"), (35, "pz", "Planning and Zoning Commission"),
                              (204, "bpu", "Board of Public Utilities")]],
    {"id": "hobbs", "name": "City of Hobbs City Commission", "county": "Lea", "reader": "civicclerk",
     "api": "https://hobbsnm.api.civicclerk.com/v1", "index": "https://hobbsnm.portal.civicclerk.com/"},
    {"id": "carlsbad", "name": "City of Carlsbad", "county": "Eddy", "reader": "civicclerk",
     "api": "https://carlsbadnm.api.civicclerk.com/v1", "index": "https://carlsbadnm.portal.civicclerk.com/"},
    {"id": "dona-ana-county", "name": "Dona Ana County Commission and Planning", "county": "Dona Ana", "reader": "civicclerk",
     "api": "https://donaanaconm.api.civicclerk.com/v1", "index": "https://donaanaconm.portal.civicclerk.com/"},
    {"id": "bernalillo-county", "name": "Bernalillo County Commission and planning boards", "county": "Bernalillo",
     "reader": "iqm2", "site": "https://bernalillocountynm.iqm2.com/Citizens",
     "boards": r"Board of County Commissioners|Development Review|Planning Commission|Zoning Administrator|"
               r"Economic Development|Air Quality|Local Government Coordinating"},
    {"id": "las-cruces-council", "name": "City of Las Cruces City Council", "county": "Dona Ana", "reader": "civicweb",
     "site": "https://lascruces.civicweb.net"},
    {"id": "las-cruces-boards", "name": "City of Las Cruces boards (planning and zoning, development review)",
     "county": "Dona Ana", "reader": "pages", "pages": ["https://lascruces.gov/multimedia-center/agenda-center/"]},
    {"id": "rio-rancho", "name": "City of Rio Rancho Governing Body and Planning and Zoning Board", "county": "Sandoval",
     "reader": "granicus", "site": "https://riorancho.granicus.com", "view_id": 14,
     "boards": r"Governing Body|Planning and Zoning"},
    {"id": "san-juan-county", "name": "San Juan County Commission", "county": "San Juan", "reader": "sjcounty",
     "site": "https://www.sjcounty.net",
     "pages": ["https://www.sjcounty.net/elected-officials/commissioners/commission-agendas-minutes/-toggle-allpast",
               "https://www.sjcounty.net/elected-officials/commissioners/commission-agendas-minutes/-toggle-all"]},
    _ac("eddy-county", "Eddy County Commission", "Eddy", "https://www.eddycountynm.gov"),
    _ac("roswell", "City of Roswell", "Chaves", "https://www.roswell-nm.gov"),
    _ac("farmington", "City of Farmington", "San Juan", "https://www.farmingtonnm.gov"),
    _ac("los-lunas", "Village of Los Lunas", "Valencia", "https://www.loslunasnm.gov"),
    _ac("grant-county", "Grant County Board of County Commissioners", "Grant", "https://www.grantcountynm.gov"),
    {"id": "valencia-county", "name": "Valencia County Commission", "county": "Valencia", "reader": "pages",
     "pages": ["https://www.valencianm.gov/agenda-center/"]},
    {"id": "sandoval-county", "name": "Sandoval County Commission and planning", "county": "Sandoval", "reader": "pages",
     "pages": ["https://www.sandovalcountynm.gov/meetings/"]},
    {"id": "chaves-county", "name": "Chaves County Commission", "county": "Chaves", "reader": "pages",
     "pages": ["https://www.chavescounty.gov/government/agendas_and_minutes.php"]},
]

# Bodies that post no current records, or whose records sit behind a portal a person opens.
# Each is a human wall for that body alone (scopes/us-nm/coverage.json, local_records).
NOT_POSTED = [
    {"name": "Lea County Commission and Planning and Zoning Board", "county": "Lea",
     "why": "leacounty.gov has no working agenda module (the AgendaCenter address answers 404) and posts only public comment forms; meetings are livestreamed on YouTube; ask the county clerk in Lovington; the Hobbs News-Sun reports meetings"},
    {"name": "Valencia County Commission, current agendas", "county": "Valencia",
     "why": "valencianm.gov posts agenda PDFs only through May 2025; newer agendas are in a Google Drive folder a person opens"},
    {"name": "Luna County Commission", "county": "Luna", "why": "no county site posts agendas or minutes that a script can list; ask the county manager in Deming"},
    {"name": "Hidalgo County Commission", "county": "Hidalgo", "why": "no county site posts agendas or minutes that a script can list; ask the clerk in Lordsburg; the Lordsburg Liberal reports meetings"},
    {"name": "City of Albuquerque Environmental Planning Commission", "county": "Bernalillo",
     "why": "not on Legistar; staff reports sit on cabq.gov planning pages a person browses"},
]

# Projects that are not GEM plants yet (developers and sites from scopes/us-nm/plan.md).
LEADS = {
    "Pyramid Generating Station": r"pyramid (generating|power|station|plant)|tri-state.{0,60}hidalgo",
    "SPS gas buildout": r"\bSPS\b.{0,80}(gas|generat|2,?088)|southwestern public service.{0,80}(gas|generat)",
    "SWPP ERAS Hobbs": r"\bERAS\b|hobbs.{0,60}(southwest power pool|SWPP)",
    "PNM IRP placeholders": r"\bPNM\b.{0,80}(IRP|integrated resource|gas (plant|turbine|generat))",
    "Rio Grande units and El Paso Electric": r"el paso electric.{0,80}(rio grande|generat|gas|turbine)|rio grande (generating|power|station|unit)",
    "NTEC": r"\bNTEC\b|navajo transitional energy",
    "Westside power station": r"saddle butte|westside (power|generating|station)|kirtland.{0,60}(power|generat|gas)",
    "Lea County Data Center": r"new era energy|lea county data cent|\bNEE\b.{0,40}data",
    "Roswell Information Park": r"roswell information park|\bE2B4\b|sustany",
    "Site Layer 1": r"site layer|w[a\u00e4]rtsil[a\u00e4].{0,60}grant|grant county.{0,60}(data cent|moratorium)",
    "Zenith Volts": r"zenith volts",
    "Google data center in Lea County": r"google.{0,60}(lea county|hobbs|data cent)",
    "Meta Los Lunas": r"greater kudu|meta.{0,60}los lunas|los lunas.{0,60}(meta|data cent)",
    "Santa Teresa data centers": r"santa teresa.{0,80}(data cent|generat|power|microgrid)|(data cent|microgrid).{0,80}santa teresa",
    "Project Jupiter": r"project jupiter|stratton ranch|\bBorderplex digital\b|oracle.{0,40}openai.{0,60}(santa teresa|dona ana)",
    "Clean Path": r"clean path",
    "Cunningham and Maddox": r"cunningham (station|power|generating)|maddox (station|power|generating)|lea power partners",
    "Chino Mines": r"chino mines?.{0,40}(power|generat|plant)|freeport.{0,40}(power|generat)",
}

STRONG = re.compile(r"data ?cent(er|re)s?|power plant|generating (station|facility|plant|unit)|power station|"
                    r"combustion turbines?|gas turbines?|combined[- ]cycle|simple[- ]cycle|peaking (plant|units?)|"
                    r"natural gas[- ](fired|plant|power|generat)|\bmegawatts?\b|\b\d[\d,.]*\s?MW\b|energy center|"
                    r"reciprocating engines?|\bengines?\b.{0,40}(data cent|MW|megawatt|generat)|micro-?grids?|"
                    r"backup generat|standby generat|\bgenerat(ors?|ion)\b.{0,60}(data|MW|megawatt|fleet|plant|facility)|"
                    r"electric generation|substation.{0,40}(data|generat)|large load|"
                    r"\b(Xcel|SPS|PNM|El Paso Electric|Tri-State)\b.{0,60}(generat|gas|plant|turbine|load|data)", re.I)
CONTEXT = re.compile(r"rezon|zone change|map amendment|special use|conditional use|variance|industrial revenue bond|\bIRB\b|"
                     r"payment in lieu|\bPILOT\b|tax (abatement|incentive)|development agreement|site plan|plat|"
                     r"annex|local economic development act|\bLEDA\b|moratorium", re.I)
DOC_KEEP = re.compile(r"agenda|minute|packet|order|staff report|commission|planning|zoning|council|"
                      r"board|hearing|ordinance|resolution|action", re.I)
MONTHS = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}


def log(msg):
    print(f"[harvest-nm-local] {msg}", file=sys.stderr, flush=True)


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

    def page(self, url):
        for attempt in range(3):
            p = get(url, timeout=120)
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


def parse_links(text, base, body, since):
    """Every dated document link on an index page."""
    docs, seen = [], set()
    text = text or ""
    tag = re.search(r'<base\b[^>]*href=["\']([^"\']+)["\']', text, re.I)
    if tag:   # a page's <base> tag sets where its relative links point, as in a browser
        base = urllib.parse.urljoin(base, html.unescape(tag.group(1)).strip())
    for m in re.finditer(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', text, re.S | re.I):
        href, label = m.groups()
        href = html.unescape(href).strip()
        if not re.search(r"\.pdf($|\?)|/DocumentCenter/View/|/AgendaCenter/ViewFile/|/files/\d+/", href, re.I):
            continue
        url = urllib.parse.urljoin(base, href).replace(" ", "%20")
        if url in seen:
            continue
        seen.add(url)
        label = text_of(label)
        path = urllib.parse.urlsplit(href).path
        row = text.rfind("<tr", 0, m.start())
        row = text_of(text[row:m.start()]) if row != -1 and text.rfind("</tr>", row, m.start()) == -1 else ""
        date = date_of(label) or date_of(path.rsplit("/", 1)[-1]) or date_of(path) or date_of(row)
        if not date:
            y = re.search(r"\b(20[12]\d)\b", f"{label} {href}")
            date = f"{y.group(1)}-01-01" if y else ""
        if not date or date < since[:4] + "-01-01" or (date < since and not date.endswith("-01-01")):
            continue
        docs.append(doc(body, url, label or href.rsplit("/", 1)[-1], date))
    return docs


def list_pages(net, body, since, until):
    docs, read = [], 0
    for url in body["pages"]:
        text = net.page(url)
        if text is None:
            continue
        read += 1
        docs += [d for d in parse_links(text, url, body, since) if d["url"] not in {x["url"] for x in docs}]
    return docs if read else None


def parse_iqm2(text, body, site):
    """Bernalillo County style IQM2 calendar: one MeetingRow per meeting, FileOpen.aspx PDF links."""
    docs = []
    for row in re.split(r'<div class="Row MeetingRow"', text or "")[1:]:
        title = html.unescape(re.search(r'title="([^"]*)"', row).group(1)) if re.search(r'title="([^"]*)"', row) else ""
        board = re.search(r"Board:\s*(.*?)\s*(?:Type:|$)", re.sub(r"[\r\n\t]+", " ", title))
        board = clean_ws(board.group(1)) if board else ""
        if body.get("boards") and board and not re.search(body["boards"], board, re.I):
            continue
        date_m = re.search(r"(?:MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY),\s+([A-Z]+ \d{1,2}, 20\d\d)", title)
        date = date_of(date_m.group(1)) if date_m else ""
        for href, label in re.findall(r"href=['\"](FileOpen\.aspx\?[^'\"]+)['\"][^>]*>(.*?)</a>", row, re.S):
            url = f"{site}/{html.unescape(href)}"
            docs.append(doc(body, url, f"{board} {text_of(label)} {date}", date, kind_of(text_of(label))))
    return docs


def list_iqm2(net, body, since, until):
    s, u = dt.date.fromisoformat(since), dt.date.fromisoformat(until)
    docs, seen, read = [], set(), 0
    for year in range(s.year, u.year + 1):
        text = net.page(f"{body['site']}/Calendar.aspx?From=1/1/{year}&To=12/31/{year}")
        if text is None:
            continue
        read += 1
        for d in parse_iqm2(text, body, body["site"]):
            if d["url"] not in seen and since <= d["date"] <= until:
                seen.add(d["url"])
                docs.append(d)
    return docs if read else None


def parse_civicweb_types(text, site):
    return sorted({urllib.parse.urljoin(site + "/", html.unescape(h)) for h in
                   re.findall(r'href="([^"]*MeetingInformation\.aspx\?[^"]*type=\d+[^"]*)"', text or "", re.I)})


def parse_civicweb_meetings(text, site, body):
    """MeetingInformation page rows: 'Title - Mon DD YYYY' with the meeting page, and its /document/ links."""
    docs = []
    for href, label in re.findall(r'<a[^>]*href="(/document/\d+/[^"]+)"[^>]*>(.*?)</a>', text or "", re.S):
        label = text_of(label)
        docs.append((urllib.parse.urljoin(site, html.unescape(href)), label))
    return docs


def list_civicweb(net, body, since, until):
    site = body["site"]
    types = net.page(f"{site}/Portal/MeetingTypeList.aspx")
    if types is None:
        return None
    docs, seen = [], set()
    for t_url in parse_civicweb_types(types, site):
        page = net.page(t_url)
        for href, label in re.findall(r'<a[^>]*href="(/Portal/MeetingInformation\.aspx\?Id=\d+)"[^>]*>(.*?)</a>', page or "", re.S):
            label = text_of(label)
            date = date_of(label)
            if not date or not since <= date <= until:
                continue
            m_url = urllib.parse.urljoin(site, html.unescape(href))
            if m_url in seen:
                continue
            seen.add(m_url)
            meeting = net.page(m_url)
            for url, doc_label in parse_civicweb_meetings(meeting, site, body):
                docs.append(doc(body, url, f"{label} {doc_label}", date, kind_of(doc_label)))
            time.sleep(0.2)
    return docs


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


def parse_sjcounty(text, body, since="0000", until="9999"):
    docs = []
    for row in re.split(r"<tr><td class='title_column", text or "")[1:]:
        title = re.search(r"itemprop='summary'>(.*?)</span>", row, re.S)
        title = text_of(title.group(1)) if title else ""
        when = re.search(r"class='event_datetime'>\s*(\d{1,2})/(\d{1,2})/(20\d\d)", row)
        date = f"{when.group(3)}-{int(when.group(1)):02d}-{int(when.group(2)):02d}" if when else ""
        if not date or not since <= date <= until:
            continue
        for cell, kind in (("event_agenda", "agenda"), ("event_minutes", "minutes"), ("event_other", "packet")):
            seg = re.search(rf"class='{cell}'>(.*?)</td>", row, re.S)
            for href, label in re.findall(r"href='([^']*showpublisheddocument[^']*)'[^>]*>(.*?)</a>", seg.group(1) if seg else "", re.S):
                docs.append(doc(body, urllib.parse.urljoin(body["site"], html.unescape(href)),
                                f"{title} {text_of(label)}", date, kind))
    return docs


def list_sjcounty(net, body, since, until):
    docs, seen, read = [], set(), 0
    for url in body["pages"]:
        text = None
        for _ in range(2):
            p = get(url, timeout=120)
            if p.status == "200" and p.text:
                text = p.text
                break
        if text is None:
            report_failure(url, p.status, "local records listing failed")
            continue
        read += 1
        for d in parse_sjcounty(text, body, since, until):
            if d["url"] not in seen:
                seen.add(d["url"])
                docs.append(d)
    return docs if read else None


LISTERS = {"legistar": list_legistar, "civicclerk": list_civicclerk, "agendacenter": list_agendacenter,
           "pages": list_pages, "iqm2": list_iqm2, "civicweb": list_civicweb, "granicus": list_granicus,
           "sjcounty": list_sjcounty}


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

# Plant names that are also surnames, counties, towns or rivers. In commission minutes a bare
# "Hobbs", "Luna" or "Rio Grande" is a place, so these need a plant word next to them. They
# replace the commission's patterns for the local records only.
PLANT_WORD = r"(station|generating|generation|power|plant|unit|units|cc|ct|combined|combustion|peaker|energy facility|energy center)"
LOCAL_KNOWN = {
    "L100000401601": [r"luna " + PLANT_WORD, r"luna energy"],
    "L100000401903": [r"rio grande " + PLANT_WORD, r"el paso electric.{0,40}rio grande"],
    "L100000402045": [r"hobbs " + PLANT_WORD, r"hobbs generating"],
    "L100000402228": [r"afton " + PLANT_WORD],
    "L100000402229": [r"reeves " + PLANT_WORD],
    "L100000402230": [r"rio bravo " + PLANT_WORD],
    "L100000402297": [r"cunningham " + PLANT_WORD],
    "L100000402299": [r"maddox " + PLANT_WORD],
    "L100000402347": [r"valencia " + PLANT_WORD],
    "L100000402507": [r"chino mines? " + PLANT_WORD],
    "L100000402529": [r"bluffview " + PLANT_WORD],
    "L100000408054": [r"clean path"],
    "L100001043002": [r"\bNTEC\b.{0,40}(gas|power|plant)", r"navajo transitional energy.{0,60}(gas|power plant)"],
    "L100001080449": [r"lea county data cent", r"new era energy"],
    "L100001080450": [r"project jupiter"],
    "L100001083303": [r"lordsburg " + PLANT_WORD, r"pyramid " + PLANT_WORD],
    "L100001083387": [r"\bERAS\b"],
    "L100001089557": [r"site layer"],
    "L100001089610": [r"westside " + PLANT_WORD],
    "L100001089629": [r"roswell information park"],
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

    L = [f"# New Mexico local planning and commission records ({today})", "",
         f"Agendas, packets, staff reports and minutes posted since {since} by the bodies around the GEM plants "
         "and the leads, searched for plant and developer names and for power and data center words. A record "
         "is a lead: open the document at its address and cite it there. Copies are in scopes/us-nm/work/local/ "
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
    ap.add_argument("--list-only", action="store_true", help="list documents, read nothing")
    ap.add_argument("--no-ocr", action="store_true", help="skip OCR of scanned documents")
    a = ap.parse_args()
    tag_batch("us-nm")
    until = dt.date.today().isoformat()
    plants = load_plants()
    pats = plant_patterns(plants)
    county_plants = {}
    for p in plants:
        county_plants.setdefault(p["county"], []).append(p["id"])
    wanted = set(a.bodies.split(",")) if a.bodies else None
    work = scope_work("us-nm") / "local"
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

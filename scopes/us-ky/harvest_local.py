"""
Harvest Kentucky city and county planning, zoning, fiscal court and council records before a sweep.

Kentucky data center and power sites are approved by the county fiscal court or the city where
they sit, and those records (agendas, packets, staff reports, minutes, rezonings, industrial
revenue bonds) name backup generator fleets and turbines long before an air permit exists.
This reads every posted record since --since (default 2024-01-01) for the bodies around the
GEM plants and the leads, and keeps the sentences that name a plant, a lead or a power or
data center project. Nothing needs a sign-in. Routes (probed 2026-11-04):

  legistar     Louisville Metro (Council 138, Planning Commission 195, Board of Zoning
               Adjustment 196, Planning Committee 139, Land Development and Transportation 154,
               Development Review Committee 165, Planning and Zoning Committee 333, Labor and Economic
               Development Committee 180): the open API at webapi.legistar.com/v1/
               louisville/Events, the agenda and minutes PDFs, and every item attachment whose
               item names a power or data center project.
  civicclerk   City of Madisonville: the open OData API at madisonvilleky.api.civicclerk.com/v1/
               Events (Agenda, Agenda Packet and Minutes files; GetMeetingFileStream downloads).
  agendacenter CivicPlus AgendaCenter sites (Henderson County, City of Henderson, Clark,
               Marshall, Hardin): /AgendaCenter/Search/?CIDs=all with a date range; files at
               /AgendaCenter/ViewFile/Agenda|Minutes/_MMDDYYYY-ID.
  wpmedia      WordPress sites (Pulaski County, Daviess County, City of Somerset, Simpson County): the open
               media API /wp-json/wp/v2/media, PDFs uploaded since --since whose titles are
               agendas, minutes, orders or packets.
  pages        Every other body: its agendas or minutes index page, read through fetch.py's
               access ladder, and every dated document link on it.

Scanned minutes are read by OCR (pdftoppm then tesseract, through fetch.py). Documents are
saved under scopes/us-ky/work/local/<body>/ (not committed). Bodies that post no minutes are
listed for a person (the coverage list's human wall). Nothing here stages a record.

Output, in batches/us-ky/harvest/: local_records.json and local_records.md.

Usage (from the repo root):
    python scopes/us-ky/harvest_local.py                          # every body since 2024
    python scopes/us-ky/harvest_local.py --bodies henderson-county,madisonville --since 2026-01-01
    python scopes/us-ky/harvest_local.py --list-only              # list documents, read nothing
    python scopes/us-ky/harvest_local.py --no-ocr
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
from fetch import CHROME_UA  # noqa: E402
from harvest_lib import REPO, clean_ws, get, report_failure, sentences, tag_batch  # noqa: E402

from paths import load_scope_module, scope_work  # noqa: E402

_permits = load_scope_module("us-ky", "harvest_permits")
_psc = load_scope_module("us-ky", "harvest_psc")
load_plants = _permits.load_plants

OUT = REPO / "batches" / "us-ky" / "harvest"
LEGISTAR = "https://webapi.legistar.com/v1/{client}"

BODIES = [
    *[{"id": f"louisville-{slug}", "name": f"Louisville Metro {name}", "county": "Jefferson", "reader": "legistar",
       "client": "louisville", "body_id": bid, "index": "https://louisville.legistar.com/Calendar.aspx"}
      for bid, slug, name in [(138, "council", "Council"), (195, "planning-commission", "Planning Commission"),
                              (196, "boza", "Board of Zoning Adjustment"), (139, "planning-committee", "Planning Committee"),
                              (154, "ldt", "Land Development and Transportation Committee"),
                              (165, "drc", "Development Review Committee"),
                              (333, "pz-committee", "Planning and Zoning Committee"),
                              (180, "econ-dev", "Labor and Economic Development Committee")]],
    {"id": "madisonville", "name": "City of Madisonville", "county": "Hopkins", "reader": "civicclerk",
     "api": "https://madisonvilleky.api.civicclerk.com/v1", "index": "https://madisonvilleky.civicclerk.com/"},
    {"id": "henderson-county", "name": "Henderson County Fiscal Court, Planning and Zoning", "county": "Henderson",
     "reader": "agendacenter", "site": "https://www.hendersoncountyky.gov"},
    {"id": "henderson-city", "name": "City of Henderson", "county": "Henderson", "reader": "agendacenter",
     "site": "https://www.hendersonky.gov"},
    {"id": "clark-county", "name": "Clark County Fiscal Court", "county": "Clark", "reader": "agendacenter",
     "site": "https://www.clarkcoky.com"},
    {"id": "marshall-county", "name": "Marshall County Fiscal Court", "county": "Marshall", "reader": "agendacenter",
     "site": "https://www.marshallcountyky.gov"},
    {"id": "hardin-county", "name": "Hardin County Fiscal Court and Planning", "county": "Hardin",
     "reader": "agendacenter", "site": "https://www.hardincountyky.gov"},
    {"id": "pulaski-county", "name": "Pulaski County Fiscal Court", "county": "Pulaski", "reader": "wpmedia",
     "site": "https://pulaskigov.com"},
    {"id": "daviess-county", "name": "Daviess County Fiscal Court", "county": "Daviess", "reader": "wpmedia",
     "site": "https://daviessky.org"},
    {"id": "somerset", "name": "City of Somerset", "county": "Pulaski", "reader": "wpmedia",
     "site": "https://cityofsomerset.com"},
    {"id": "mason-county", "name": "Mason County Fiscal Court", "county": "Mason", "reader": "pages",
     "pages": ["https://masoncountykentucky.us/Minutes.php", "https://masoncountykentucky.us/Agendas.php"]},
    {"id": "harrodsburg", "name": "City of Harrodsburg", "county": "Mercer", "reader": "pages",
     "pages": ["https://harrodsburgky.gov/AgendaMinutes"]},
    {"id": "oldham-county", "name": "Oldham County Fiscal Court", "county": "Oldham", "reader": "pages",
     "pages": ["https://www.oldhamcountyky.gov/fiscalcourtagendas"]},
    {"id": "boone-county", "name": "Boone County Fiscal Court", "county": "Boone", "reader": "pages",
     "pages": ["https://www.boonecountyky.org/government/boone_county_fiscal_court/fiscal_court_meeting_minutes.php",
               "https://www.boonecountyky.org/government/boone_county_fiscal_court/meetings/index.php"]},
    {"id": "ompc", "name": "Owensboro Metropolitan Planning Commission and Board of Adjustment", "county": "Daviess",
     "reader": "pages",
     "pages": ["https://iompc.org/about/owensboro_metropolitan_planning_commission/agendas_minutes.php",
               "https://iompc.org/about/owensboro_metropolitan_board_of_adjustment/agendas_minutes.php",
               "https://iompc.org/about/public_hearings.php"]},
    {"id": "boyd-county", "name": "Boyd County Fiscal Court", "county": "Boyd", "reader": "agendacenter",
     "site": "https://www.boydcountyky.gov"},
    {"id": "elizabethtown", "name": "City of Elizabethtown", "county": "Hardin", "reader": "pages",
     "pages": ["https://www.elizabethtownky.org/government/city_clerk/meeting_minutes_/index.php"]},
    {"id": "mccracken-county", "name": "McCracken County Fiscal Court and Planning and Zoning", "county": "McCracken",
     "reader": "pages", "pages": ["https://www.mccrackencountyky.gov/agenda/", "https://www.mccrackencountyky.gov/planning-zoning/"]},
    {"id": "maysville", "name": "City of Maysville", "county": "Mason", "reader": "pages",
     "pages": [f"https://www.cityofmaysvilleky.gov/government/maysville_city_commission/{y}_agendas___minutes.php"
               for y in (2026, 2025, 2024)]},
    {"id": "franklin", "name": "City of Franklin, city commission and Franklin-Simpson Planning and Zoning",
     "county": "Simpson", "reader": "pages",
     "pages": ["https://www.franklinky.gov/government/meetings_agendas_minutes.php",
               "https://www.franklinky.gov/departments/planning_zoning/agendas_and_minutes.php"]},
    {"id": "simpson-county", "name": "Simpson County Fiscal Court", "county": "Simpson", "reader": "wpmedia",
     "site": "https://simpsoncountyky.gov"},
]

# Bodies that post no current minutes, or whose records sit behind a portal a person opens.
# Each is a human wall for that body alone (scopes/us-ky/coverage.json, local_records).
NOT_POSTED = [
    {"name": "Lawrence County Fiscal Court", "county": "Lawrence",
     "why": "lawrencecountyky.gov posts events only; ask the fiscal court clerk; the Big Sandy News and The Levisa Lazer report meetings"},
    {"name": "Casey County Fiscal Court", "county": "Casey",
     "why": "no working county site (caseycountyky.gov does not resolve); ask the clerk; chasinthebuck.com reports meetings"},
    {"name": "Mercer County Fiscal Court", "county": "Mercer", "why": "mercercounty.ky.gov lists officers and no minutes; ask the clerk"},
    {"name": "Trimble County Fiscal Court", "county": "Trimble", "why": "trimblecountyky.gov posts events and an open records page, no minutes"},
    {"name": "Muhlenberg County Fiscal Court", "county": "Muhlenberg", "why": "muhlenbergcounty.org has a fiscal court page and no minutes"},
    {"name": "Hancock County Fiscal Court", "county": "Hancock", "why": "hancockky.us posts no minutes"},
    {"name": "Hopkins County Fiscal Court", "county": "Hopkins", "why": "hopkinscounty.ky.gov minutes stop around 2014"},
    {"name": "Bullitt County Fiscal Court", "county": "Bullitt", "why": "site under construction"},
    {"name": "Christian County Fiscal Court", "county": "Christian", "why": "christiancountyky.gov posts no minutes"},
    {"name": "Warren County Fiscal Court", "county": "Warren", "why": "agendas and minutes are in Google Drive folders linked from warrencountyky.gov; a person opens them"},
    {"name": "City of Owensboro", "county": "Daviess", "why": "agendas on the KSBA portal (portal.ksba.org, agency 4396) and minutes in Laserfiche WebLink (laserfiche.owensboro.org); a person browses them"},
    {"name": "City of Paducah", "county": "McCracken", "why": "minutes and packets in Laserfiche WebLink (citydocs.paducahky.gov); action forms at paducahky.gov/files/<n>/; a person browses them"},
    {"name": "City of Hopkinsville", "county": "Christian", "why": "Laserfiche portal; a person browses it"},
    {"name": "Webster County Fiscal Court", "county": "Webster", "why": "webstercountyky.com answers a bot challenge; the sweep opens it with fetch.py --render"},
    {"name": "Todd County Fiscal Court", "county": "Todd",
     "why": "toddcountyky.com, the old county address, now serves an unrelated foreign site; no county site posts minutes; ask the fiscal court clerk in Elkton; the Todd County Standard reports meetings"},
    {"name": "Union County Fiscal Court", "county": "Union", "why": "unioncountyky.org needs the browser-fingerprint route; the sweep opens it through fetch.py"},
]

# Projects that are not GEM plants yet (developers and sites from the plan and the permit harvest).
LEADS = {
    "TeraWulf": r"terawulf", "Justified Datapower": r"justified data ?power", "DB Long Hunts Data": r"long hunts",
    "Green River East GenCo": r"green river east", "Meta": r"\bmeta platforms\b|\bmeta\b.{0,40}data cent",
    "Amazon Data Services": r"amazon data services|\baws\b.{0,40}data cent", "CyrusOne": r"cyrusone",
    "Flexential": r"flexential", "Middle Mile Infrastructure": r"middle mile", "PPL and Blackstone": r"blackstone",
    "Bluegrass Cellular data center": r"bluegrass cellular", "Lynn Bark Energy Center": r"lynn bark",
    "Kentucky Power Lawrence County combined cycle": r"lawrence county.{0,60}(combined cycle|generat|power plant)",
    "TenKey LandCo": r"ten ?key", "TVA queue 628 in Todd County": r"todd county.{0,80}(gas|generat|power plant|TVA)",
}

STRONG = re.compile(r"data ?cent(er|re)s?|power plant|generating (station|facility|plant|unit)|power station|"
                    r"combustion turbines?|gas turbines?|combined[- ]cycle|simple[- ]cycle|peaking (plant|units?)|"
                    r"natural gas[- ](fired|plant|power|generat)|\bmegawatts?\b|\b\d[\d,.]*\s?MW\b|energy center|"
                    r"reciprocating engines?|backup generat|standby generat|\bgenerators?\b.{0,60}(data|MW|megawatt|fleet)|"
                    r"electric generation|substation.{0,40}(data|generat)|large load", re.I)
CONTEXT = re.compile(r"rezon|zone change|map amendment|conditional use|variance|industrial revenue bond|\bIRB\b|"
                     r"payment in lieu|\bPILOT\b|tax (abatement|incentive)|development agreement|site plan|plat|"
                     r"annex|KEDFA|economic development finance", re.I)
DOC_KEEP = re.compile(r"agenda|minute|packet|order|staff report|fiscal court|planning|zoning|council|"
                      r"commission|FCM|board|hearing|ordinance|resolution", re.I)
MONTHS = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}


def log(msg):
    print(f"[harvest-ky-local] {msg}", file=sys.stderr, flush=True)


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
                      (r"(?:^|/)(\d{2})(\d{2})(\d{2})(?=[ _-]?[A-Za-z])", "mdy2")]:
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
    for k, rx in [("minutes", r"minute|fcm|order book"), ("packet", r"packet|staff[ _-]?report|attachment"),
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


def list_wpmedia(net, body, since, until):
    docs, page = [], 1
    while True:
        data = net.json(f"{body['site']}/wp-json/wp/v2/media",
                        {"per_page": 100, "page": page, "after": f"{since}T00:00:00", "mime_type": "application/pdf"})
        if not data:
            break
        for m in data:
            title = text_of((m.get("title") or {}).get("rendered", ""))
            src = m.get("source_url") or ""
            if not DOC_KEEP.search(f"{title} {src.rsplit('/', 1)[-1]}"):
                continue
            date = date_of(title) or date_of(src.rsplit("/", 1)[-1]) or (m.get("date") or "")[:10]
            docs.append(doc(body, src, title, date))
        if len(data) < 100:
            break
        page += 1
    return docs if docs or page > 1 else ([] if data == [] else docs)


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


LISTERS = {"legistar": list_legistar, "civicclerk": list_civicclerk, "agendacenter": list_agendacenter,
           "wpmedia": list_wpmedia, "pages": list_pages}


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

# Plant names that are also surnames, rivers, roads or county names. In council minutes a bare
# "Brown", "Reid" or "Trimble County" is a person or a place, so these need a plant word next
# to them. They replace the commission's patterns for the local records only.
PLANT_WORD = r"(station|generating|generation|power|plant|unit|units|cc|ct|combined|combustion|peaker|fossil|energy)"
LOCAL_KNOWN = {
    "L100000402085": [r"big sandy peak"],
    "L100000103930": [r"big sandy " + PLANT_WORD, r"kentucky power.{0,40}big sandy"],
    "L100000103932": [r"cane run " + PLANT_WORD],
    "L100000103935": [r"\bcooper " + PLANT_WORD, r"ekpc.{0,40}cooper", r"john sherman cooper"],
    "L100000103937": [r"\bbrown " + PLANT_WORD, r"\be\.? ?w\.? brown", r"\bku brown"],
    "L100000103945": [r"mill creek " + PLANT_WORD, r"mill creek [1-6]\b"],
    "L100000103946": [r"paradise " + PLANT_WORD, r"tva.{0,40}paradise"],
    "L100000103947": [r"\breid " + PLANT_WORD, r"robert (a\.? )?reid"],
    "L100000103950": [r"spurlock " + PLANT_WORD, r"\bh\.? ?l\.? spurlock", r"ekpc.{0,40}spurlock"],
    "L100000103951": [r"trimble county " + PLANT_WORD],
}


def plant_patterns(plants):
    pats = {}
    for p in plants:
        rx = list(LOCAL_KNOWN.get(p["id"]) or _psc.PSC_KNOWN.get(p["id"], []))
        if not rx and p["name_words"]:
            rx = [r"\b" + r"\W+".join(map(re.escape, sorted(p["name_words"]))) + r"\b"] if len(p["name_words"]) == 1 else []
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

    L = [f"# Kentucky local planning and fiscal court records ({today})", "",
         f"Agendas, packets, staff reports and minutes posted since {since} by the bodies around the GEM plants "
         "and the leads, searched for plant and developer names and for power and data center words. A record "
         "is a lead: open the document at its address and cite it there. Copies are in scopes/us-ky/work/local/ "
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
    tag_batch("us-ky")
    until = dt.date.today().isoformat()
    plants = load_plants()
    pats = plant_patterns(plants)
    county_plants = {}
    for p in plants:
        county_plants.setdefault(p["county"], []).append(p["id"])
    wanted = set(a.bodies.split(",")) if a.bodies else None
    work = scope_work("us-ky") / "local"
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

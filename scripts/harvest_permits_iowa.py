"""
Harvest Iowa air construction permits before a research sweep.

The Iowa Department of Natural Resources (DNR) Air Quality Bureau posts every
construction permit it has issued, by facility, on plain server pages
(idnraqrr.iowadnr.gov/ConPermitSearch). The search page looks like a form that
needs a script, and the October 2026 Iowa sweep wrongly logged it as blocked
and missed the March 2026 Burlington engine permits. Every list on the site
loads with a plain request; this script reads them all once, ahead of the
sweep, so no plant's permits are missed again:

  1. The facility directory: every DNR facility id, name, city and plant
     number (one page, about 3,300 rows).
  2. Match each GEM plant to its DNR facilities. A plant can have several
     (Burlington has the generating station and the Agency Street turbines).
     KNOWN holds hand-checked matches; name and city matching adds more,
     marked for checking.
  3. Each facility's permit table (ConstructionPermit?id=N): permit number,
     project number, equipment, issue date and a link to the permit PDF.
     Recent permits for engines, turbines, generators and boilers are
     downloaded and their size lines (MW, kW, MMBtu/hr, horsepower) kept.
  4. The large-project (PSD) document list for the facility, when it has one.
  5. Open public comment periods (PublicComment), with their documents.
  6. Applications still under review in the EasyAir system (all pages of the
     Active Applications tab, which needs form posts to page through), and
     the forms each power or data center application submitted: equipment,
     manufacturer, model, nameplate MW and installation date. The view
     button opens a detail page whose report links download each form as a
     PDF by a plain request; a pre-application that points at a draft
     application is followed to that draft too.
  7. Power-like facilities that match no GEM plant, for discovery.
  8. The Linn and Polk County permit programs (see the end of this note).

Output: one plain-text index per plant under work/permits/<scope>/<pid>.md,
plus _unmatched.md, _public_comment.md, _applications.md, _county.md and
harvest_log.jsonl. Every page and PDF fetched through fetch.py lands in its
disk cache (work/fetch_cache/), so url_verifier.py reads it at once. Permit
PDFs name agency and company staff with their contact details: they stay in
work/ (never committed). Nothing here stages a record.

Usage (from scripts/):
    python harvest_permits_iowa.py --scope us-ia                 # every plant
    python harvest_permits_iowa.py --scope us-ia --plants L100000103905
    python harvest_permits_iowa.py --scope us-ia --map L100001047779=11491
    python harvest_permits_iowa.py --scope us-ia --match-only    # list matches, fetch nothing else

Linn County (Cedar Rapids) and Polk County (Des Moines) run their own air
permit programs on their own sites, and the DNR pages can lack their newest
permits. For a plant in either county the index adds the county's issued
permits (Linn: the company's emission points with authorization-to-install
dates and permit PDFs, read from the table's data address) and the permits
under review or out for public comment; _county.md lists both counties' open
items. KNOWN_LINN and KNOWN_POLK hold the hand-checked county names.
"""
import argparse
import html
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch import CHROME_UA, fetch_page  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
BASE = "https://idnraqrr.iowadnr.gov/ConPermitSearch"
EASYAIR = ("https://programs.iowadnr.gov/easyair/Public/Client/IA_EASY/Public/Pages/"
           "PublicApplicationList.aspx")
GRID = "ctl00$ctl00$SimpleMainContent$MainContent$ucApplicationTabList$GridView1"
TAB = "ctl00$ctl00$SimpleMainContent$MainContent$ucApplicationTabList$"
REPORT = ("https://programs.iowadnr.gov/easyair/Public/EnSuite/Shared/Pages/Util/"
          "ServerRptViewer.aspx?sr=%2fIDNR%2fReports%2fEASY%2f")
FORM_LINE = re.compile(r"Project includes|Emission Unit Name|Manufacturer|Model:|Model Number|"
                       r"Nameplate|Material Processed|Date of On-Site|heat input|Submittal:", re.I)
FORM_NOISE = re.compile(r"Engineering Specifications|Certificate of Conformity|"
                        r"certified|Date of Modification \(", re.I)
DATA_CENTER = re.compile(r"data cent|datacent", re.I)

# Hand-checked GEM plant -> DNR facility ids (2026-10-19). A plant missing
# here is matched by name and city words, and those matches are marked for
# checking in its index.
KNOWN = {
    "L100000103905": [1499, 3223],      # Burlington GS, Agency Street turbines
    "L100000402016": [954],             # Emery
    "L100001047779": [11491, 1862],     # Orient Energy Center; Hawkeye Generating, Orient
    "L100000409203": [1296, 3395],      # Ames combustion turbine; Ames Municipal Electric
    "L100000103902": [1645, 3395],      # Ames steam electric plant; Ames Municipal Electric
    "L100000103908": [3052],            # Wisdom
    "L100000402080": [1875],            # Electrifarm turbines
    "L100000402371": [1617],            # Western Minnesota Municipal Power Agency, Brayton
    "L100000402081": [571],             # Pleasant Hill/GDMEC
    "L100001047759": [230],             # Lime Creek turbines
    "L100000402018": [1462],            # Marshalltown generating station
    "L100000402017": [1462],            # Marshalltown (Sutherland) turbines, same DNR facility
    "L100001062090": [1462],            # Bobcat, permitted under Marshalltown GS (project 26-003)
    "L100000402082": [571],             # Pleasant Hill/GDMEC
    "L100000103917": [76],              # Prairie Creek
    "L100000409255": [1366],            # Summit Lake
    "L100000402084": [11340],           # Sycamore turbines
    "L100000103918": [183],             # Riverside station, Bettendorf
}

# Linn and Polk counties run their own air permit programs, on their own sites.
LINN = "https://aqbi.linncounty.org"
POLK = "https://airquality.polkcountyiowa.gov/Pages"
LINN_CITIES = {"cedar rapids", "marion", "hiawatha", "palo", "mount vernon", "fairfax", "center point"}
POLK_CITIES = {"des moines", "pleasant hill", "ankeny", "urbandale", "west des moines", "johnston",
               "altoona", "grimes", "clive", "bondurant"}
# Hand-checked GEM plant -> company names in the Linn County issued-permit list,
# and GEM plant -> facility name in the Polk County lists (2026-10-19).
KNOWN_LINN = {
    "L100000103917": ["IPL - Prairie Creek Generating Station"],
    "L100001062089": ["IPL - Prairie Creek Generating Station"],   # the engines are at Prairie Creek
    "L100001083294": ["IPL - Morgan Valley Energy Center"],
}
KNOWN_POLK = {
    "L100000402081": "MidAmerican Energy Co.- Pleasant Hill",
    "L100000402082": "MidAmerican Energy Co.- Pleasant Hill",
}

POWER_NAME = re.compile(
    r"\b(IPL|INTERSTATE POWER|MIDAMERICAN|ALLIANT|CENTRAL IOWA POWER|CIPCO|CORN BELT|"
    r"MUNICIPAL (ELECTRIC|UTILIT|POWER)|POWER PLANT|POWER STATION|GENERATING|"
    r"GENERATION|COMBUSTION TURBINE|TURBINES?|ENERGY CENTER|POWER MODULE|"
    r"POWER COOP|POWER AGENCY|ELECTRIC COOP)", re.I)
POWER_NAME_DROP = re.compile(r"OPERATIONS CENTER|SERVICE CTR|TRAINING|AREA OFFICE|CAMPUS|"
                             r"REPAIR|READY MIX|WTP|WWTP|WATER|PORTABLE", re.I)
NAME_NOISE = re.compile(
    r"\b(power station|power plant|generating station|generating|station|energy center|"
    r"plant|power|gt|ia|iowa|the|municipal|of|and|\d{4}|irp|interstate|light|midamerican)\b",
    re.I)
EQUIPMENT = re.compile(r"turbine|\bct\b|engine|rice|generat|\bgen\b|boiler|duct|"
                       r"hrsg|combined|peak|diesel|reciprocat", re.I)
SIZE = re.compile(r"\d[\d,.]*\s*(MW|MWe|megawatt|kW|kilowatt|MMBtu|mmbtu|hp|horsepower|"
                  r"bhp)\b")


def log(msg):
    print(f"[harvest-ia] {msg}", file=sys.stderr, flush=True)


def clean(s):
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S | re.I)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def get(url, timeout=120):
    return fetch_page(url, timeout=timeout)


# ------------------------------------------------------------- directory ---

def directory():
    """[{id, name, city, number}] for every DNR facility."""
    page = get(f"{BASE}/ByConstructionPermitPlantNameView?searchString=a")
    if page.status != "200":
        sys.exit(f"facility directory: HTTP {page.status}; run fetch.py on it and read site_access.md")
    rows = re.findall(r'data-selectclick="(\d+)".*?</a>\s*</td>\s*<td[^>]*>(.*?)</td>\s*'
                      r'<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>', page.text, re.S)
    out = [{"id": int(i), "name": clean(n), "city": clean(c), "number": clean(no)}
           for i, n, c, no in rows]
    if len(out) < 1000:
        sys.exit(f"facility directory parsed only {len(out)} rows; the page layout changed")
    return out


def words(text):
    t = NAME_NOISE.sub(" ", re.sub(r"\(.*?\)", " ", str(text or "")))
    return {w.lower() for w in re.split(r"[^A-Za-z]+", t) if len(w) >= 4}


def match(plant, facilities):
    """Facility matches for one plant: [(facility, how)]. A hand-checked
    match is used alone; otherwise a facility must carry every distinctive
    word of the plant's name, or share its city and owner."""
    out, seen = [], set()
    by_id = {f["id"]: f for f in facilities}
    for fid in plant["map"] or KNOWN.get(plant["id"], []):
        if fid in by_id:
            out.append((by_id[fid], "checked by hand"))
            seen.add(fid)
    if out:
        return out
    name_words = set()
    for n in [plant["name"]] + plant["other_names"]:
        name_words |= words(n)
    city = str(plant.get("city") or "").strip().lower()
    for f in facilities:
        if f["id"] in seen or POWER_NAME_DROP.search(f["name"]):
            continue
        fw = {w.lower() for w in re.split(r"[^A-Za-z]+", f["name"]) if len(w) >= 4}
        if name_words and name_words <= fw and POWER_NAME.search(f["name"]):
            out.append((f, "name match, check it is this plant"))
            seen.add(f["id"])
        elif (city and f["city"].strip().lower() == city and POWER_NAME.search(f["name"])
              and plant["owner_word"] and plant["owner_word"] in f["name"].lower()):
            out.append((f, "same city and owner, check it is this plant"))
            seen.add(f["id"])
    return out


# ---------------------------------------------------------- permit pages ---

def permit_table(fid):
    """(status, rows) for one facility's permit page."""
    url = f"{BASE}/ConstructionPermit?id={fid}"
    page = get(url)
    if page.status != "200":
        return page.status, []
    body = page.text[page.text.find("<tbody"):]
    rows = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", body, re.S):
        tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
        if len(tds) < 6:
            continue
        m = re.search(r'href="([^"]+)"', tds[0])
        link = html.unescape(m.group(1)) if m else ""
        if link.startswith("/"):
            link = "https://idnraqrr.iowadnr.gov" + link
        date = clean(tds[5])
        rows.append({"permit": clean(tds[1]), "project": clean(tds[2]), "point": clean(tds[3]),
                     "equipment": clean(tds[4]), "date": date, "link": link,
                     "iso": _iso(date)})
    rows.sort(key=lambda r: r["iso"], reverse=True)
    return "200", rows


def _iso(us_date):
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})", us_date or "")
    return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}" if m else ""


def size_lines(text, limit=10):
    out = []
    for line in text.splitlines():
        s = re.sub(r"\s+", " ", line).strip()
        if SIZE.search(s) and 15 < len(s) < 300 and s not in out:
            out.append(s)
            if len(out) >= limit:
                break
    return out


def pdf_facts(text):
    """Project description and date lines from a DNR permit PDF."""
    facts = []
    for label in ("Project Description", "Equipment Description", "Equipment Location",
                  "Project Number", "Date"):
        m = re.search(rf"{label}:\s*(.+)", text)
        if m:
            value = re.sub(r"\s+", " ", m.group(1)).strip()[:200]
            facts.append(f"{label}: {value}")
    return facts


def psd_index():
    page = get(f"{BASE}/PSDSearch")
    if page.status != "200":
        log(f"PSD list: HTTP {page.status}")
        return None
    return {int(i) for i in re.findall(r'data-selectclick="(\d+)"', page.text)} | \
        {int(i) for i in re.findall(r"PSDSearch\?id=(\d+)", page.text)}


def psd_documents(fid):
    url = f"{BASE}/PSDSearch?id={fid}"
    page = get(url)
    if page.status != "200":
        return url, page.status, []
    docs = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", page.text, re.S):
        tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
        m = re.search(r'href="([^"]*DownloadFromOpenText[^"]*)"', tr)
        if not m or len(tds) < 4:
            continue
        link = "https://idnraqrr.iowadnr.gov" + html.unescape(m.group(1))
        docs.append({"file": clean(tds[1]), "type": clean(tds[2]), "project": clean(tds[3]),
                     "link": link})
    docs.sort(key=lambda d: d["project"], reverse=True)
    return url, "200", docs


# ------------------------------------------------- comments, applications ---

def public_comments():
    url = f"{BASE}/PublicComment"
    page = get(url)
    if page.status != "200":
        log(f"public comment list: HTTP {page.status}")
        return url, None
    out = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", page.text, re.S):
        m = re.search(r'data-id="(\d+)"', tr)
        tds = [clean(x) for x in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
        tds = [x for x in tds if x]
        if m and tds:
            out.append({"id": m.group(1), "cells": tds,
                        "url": f"{BASE}/PublicComment?id={m.group(1)}"})
    for c in out:
        p = get(c["url"])
        c["status"] = p.status
        c["text"] = clean(p.text)[:1500] if p.status == "200" else ""
        c["documents"] = [{"name": clean(n), "url": "https://idnraqrr.iowadnr.gov" + html.unescape(h)
                           if h.startswith("/") else html.unescape(h)}
                          for h, n in re.findall(r'href="([^"]*Download[^"]*)"[^>]*>.*?</a>\s*</td>\s*'
                                                 r'<td[^>]*>(.*?)</td>', p.text, re.S)]
    return url, out


def _form(text):
    d = {}
    for m in re.finditer(r"<input[^>]*>", text):
        tag = m.group(0)
        n = re.search(r'name="([^"]+)"', tag)
        v = re.search(r'value="([^"]*)"', tag)
        ty = re.search(r'type="([^"]+)"', tag)
        if n and (not ty or ty.group(1) in ("hidden", "text")):
            d[html.unescape(n.group(1))] = html.unescape(v.group(1)) if v else ""
    for m in re.finditer(r'<select[^>]*name="([^"]+)"[^>]*>(.*?)</select>', text, re.S):
        sel = (re.search(r'<option[^>]*selected="selected"[^>]*value="([^"]*)"', m.group(2))
               or re.search(r'<option[^>]*value="([^"]*)"', m.group(2)))
        d[html.unescape(m.group(1))] = html.unescape(sel.group(1)) if sel else ""
    return d


def _app_rows(text):
    out = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", text, re.S):
        c = [clean(x) for x in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
        if len(c) == 7 and "Facility Number" in c[1]:
            m = re.search(r"Facility Number:\s*(\S+)", c[1])
            out.append({"facility": c[1].split(" Facility Number")[0].strip(),
                        "number": m.group(1) if m else "", "detail": c[1],
                        "type": c[2], "submitted": c[3], "status": c[5]})
    return out


def applications(max_pages=40):
    """Every row of EasyAir's Active Applications tab. The table pages by
    ASP.NET form posts, so this keeps one session and posts the page events."""
    s = requests.Session()
    s.headers["User-Agent"] = CHROME_UA
    try:
        r = s.get(EASYAIR, timeout=90)
    except requests.RequestException as e:
        log(f"application list: {e}")
        return None
    if r.status_code != 200:
        log(f"application list: HTTP {r.status_code}")
        return None
    rows, text = _app_rows(r.text), r.text
    pages = sorted({int(n) for n in re.findall(r"Page\$(\d+)", text)})
    last = max(pages) if pages else 1
    n = 2
    while n <= min(last, max_pages):
        d = _form(text)
        d["__EVENTTARGET"], d["__EVENTARGUMENT"] = GRID, f"Page${n}"
        try:
            r = s.post(EASYAIR, data=d, timeout=90)
        except requests.RequestException as e:
            log(f"application list page {n}: {e}")
            break
        if r.status_code != 200:
            log(f"application list page {n}: HTTP {r.status_code}")
            break
        text = r.text
        rows += _app_rows(text)
        more = {int(x) for x in re.findall(r"Page\$(\d+)", text)}
        last = max(more | {last})
        n += 1
        time.sleep(1)
    return rows


def _search_apps(s, name):
    r = s.get(EASYAIR, timeout=90)
    d = _form(r.text)
    d[TAB + "txtFacilityName"], d[TAB + "btnSearch"] = name, "Search"
    return s.post(EASYAIR, data=d, timeout=90).text


def _form_lines(text, limit=40):
    out = []
    for line in text.splitlines():
        t = re.sub(r"\s+", " ", line).strip()
        if (FORM_LINE.search(t) and not FORM_NOISE.search(t) and t not in out
                and len(t) < 300):
            out.append(t)
    return out[:limit]


def _read_report(link):
    page = get(REPORT + link, timeout=300)
    ok = page.status == "200" and bool(page.text.strip())
    return {"url": REPORT + link, "state": "saved" if ok else page.status,
            "lines": _form_lines(page.text) if ok else []}


def application_forms(apps):
    """Read the submitted forms of each application in `apps`; adds a "forms"
    list to each. One search per facility name, then the view button of each
    wanted row (an image button, so it posts click coordinates)."""
    by_name = {}
    for a in apps:
        by_name.setdefault(a["facility"], []).append(a)
    for name, group in by_name.items():
        wanted = {a["type"].split(" - ")[0].strip(): a for a in group}
        s = requests.Session()
        s.headers["User-Agent"] = CHROME_UA
        try:
            text = _search_apps(s, name[:40])
        except requests.RequestException as e:
            log(f"application search {name}: {e}")
            continue
        buttons = {}
        for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", text, re.S):
            b = re.search(r'name="([^"]*GridView1\$ctl\d+\$btnEditRecord)"', tr)
            sid = re.search(r"(\d+) - [A-Z]", clean(tr))
            if b and sid:
                buttons[sid.group(1)] = html.unescape(b.group(1))
        for sid, a in wanted.items():
            a["forms"] = []
            if sid not in buttons:
                continue
            try:
                d = _form(_search_apps(s, name[:40]))
                d[buttons[sid] + ".x"], d[buttons[sid] + ".y"] = "5", "5"
                detail = s.post(EASYAIR, data=d, timeout=90).text
            except requests.RequestException as e:
                log(f"application {sid}: {e}")
                continue
            links = sorted({html.unescape(x) for x in re.findall(
                r"(RPT_[A-Za-z0-9_+\-]+&amp;SUBMISSION_RID=\d+(?:&amp;SUB_FORM_RID=\d+)?)", detail)})
            whole = [x for x in links if "SUB_FORM_RID" not in x] or links
            for link in whole:
                a["forms"].append(_read_report(link))
                # a pre-application can point at a draft application
                for f in a["forms"][-1]["lines"]:
                    m = re.search(r"Submittal:\s*(\d+) - Construction", f)
                    if m and m.group(1) != sid:
                        a["forms"].append(_read_report(
                            f"RPT_Construction_Application&SUBMISSION_RID={m.group(1)}"))
            time.sleep(1)
        log(f"    application forms for {name}: "
            f"{sum(len(a.get('forms', [])) for a in group)} read")
    return apps


def _app_block(a):
    L = [f"- {a['submitted']}: {a['type']}, {a['status']} ({a['detail']})"]
    if "forms" in a and not a["forms"]:
        L.append("    - the detail page lists no form reports for this application.")
    for f in a.get("forms", []):
        tag = "saved" if f["state"] == "saved" else f"not saved, HTTP {f['state']}"
        L.append(f"    - submitted form ({tag}): {f['url']}")
        L += [f"    - {x}" for x in f["lines"]]
    return L


# ---------------------------------------------------------- county programs ---

def _post_json(url, data):
    try:
        r = requests.post(url, data=data, timeout=90, headers={
            "User-Agent": CHROME_UA, "X-Requested-With": "XMLHttpRequest"})
        return r.json().get("data") or [] if r.status_code == 200 else None
    except (requests.RequestException, ValueError) as e:
        log(f"{url}: {e}")
        return None


def linn_companies():
    """{name: picker id} for every company in the Linn County issued-permit list."""
    page = get(f"{LINN}/IssuedPermits/PV_Company_Picker")
    if page.status != "200":
        log(f"Linn County company list: HTTP {page.status}")
        return None
    return {clean(n): v for v, n in re.findall(r'value="(\d+)"[^>]*>([^<]+)<', page.text)}


def linn_issued(cid):
    """A Linn County company's emission points, newest approval first. The
    table is filled by a script from GetTableData, which this posts to."""
    rows = _post_json(f"{LINN}/IssuedPermits/GetTableData",
                      {"draw": 1, "start": 0, "length": -1, "sSearchKeyword": "", "sPickerValue": cid})
    out = []
    for r in rows or []:
        ati = r.get("dtATIApprovalStr") or ""
        out.append({"point": r.get("siNumber"), "equipment": r.get("strDescription") or "",
                    "ati": r.get("siATINumber"), "ati_date": ati, "iso": _iso(ati) if ati else "9999",
                    "pto": r.get("siPTONumber"), "pto_date": r.get("dtPTOApprovalStr") or "",
                    "link": (f"{LINN}/IssuedPermits/Preview/{r['iEmissionPointDocsKey']}"
                             if r.get("iEmissionPointDocsKey") else "")})
    out.sort(key=lambda r: r["iso"], reverse=True)   # no approval date yet sorts first
    return None if rows is None else out


def linn_review():
    rows = _post_json(f"{LINN}/ApplicationsUnderReview/GetTableData", {"draw": 1, "start": 0, "length": -1})
    return None if rows is None else [
        {"facility": r.get("sFacilityName", ""), "project": r.get("sProject", ""),
         "type": r.get("sPermitType", ""), "received": r.get("sReceived", "")} for r in rows]


def polk_drafts(max_pages=10):
    """Polk County construction permits out for public comment, with each
    one's detail page (project, date received, description). The list pages
    by ASP.NET form posts."""
    s = requests.Session()
    s.headers["User-Agent"] = CHROME_UA
    url, out, n = f"{POLK}/ConstructionDrafts.aspx", [], 1
    try:
        text = s.get(url, timeout=90).text
        while True:
            for pid, fac, proj in re.findall(
                    r'ConstructionDetails\.aspx\?Permitid=(\d+)".*?</td>\s*<td[^>]*>(.*?)</td>\s*'
                    r'<td[^>]*>(.*?)</td>', text, re.S):
                out.append({"id": pid, "facility": clean(fac), "project": clean(proj),
                            "url": f"{POLK}/ConstructionDetails.aspx?Permitid={pid}"})
            n += 1
            if n > max_pages or f"Page${n}" not in text:
                break
            d = _form(text)
            d["__EVENTTARGET"], d["__EVENTARGUMENT"] = "ctl00$ContentPlaceHolder1$gvConstPermit", f"Page${n}"
            text = s.post(url, data=d, timeout=90).text
    except requests.RequestException as e:
        log(f"Polk County drafts: {e}")
        return None
    for o in out:
        p = get(o["url"])
        t = clean(p.text) if p.status == "200" else ""
        i = t.find("Facility:")
        o["text"] = t[i:i + 700].split("©")[0].strip() if i >= 0 else f"(detail page HTTP {p.status})"
    return out


def county_section(plant, linn, linn_co, polk_rows, since, docs_cap):
    """Index lines for the plant's county permit program, if it has one."""
    L = []
    if plant["county_prog"] == "linn":
        names = KNOWN_LINN.get(plant["id"], [])
        L += ["## Linn County air permits", "",
              f"Linn County Public Health issues this plant's air permits. Issued permits: "
              f"{LINN}/IssuedPermits (pick the company). Applications under review: "
              f"{LINN}/ApplicationsUnderReview.", ""]
        if linn_co is None:
            L += ["The county company list did not load this run. Retry before concluding anything.", ""]
        for name in names:
            rows = linn["issued"].get(name)
            L += [f"### {name}", ""]
            if rows is None:
                L += ["Not in the county company list, or the table did not load.", ""]
                continue
            n = 0
            for r in rows[:args_rows_limit]:
                when = r["ati_date"] or "not approved yet"
                L.append(f"- emission point {r['point']}, {r['equipment']}: authorization to install "
                         f"{r['ati']} ({when}), permit to operate {r['pto'] or 'none'} "
                         f"{r['pto_date']}".rstrip())
                if r["link"] and EQUIPMENT.search(r["equipment"]) and n < docs_cap and r["iso"] >= since:
                    page = get(r["link"], timeout=300)
                    ok = page.status == "200" and bool(page.text.strip())
                    L.append(f"    - permit file ({'saved' if ok else 'not saved, HTTP ' + page.status}): "
                             f"{r['link']}")
                    L += [f"    - {c}" for c in (pdf_facts(page.text) + [f"states: {x}" for x in
                                                                    size_lines(page.text)] if ok else [])]
                    n += 1
            L.append("")
        mine = [a for a in linn["review"] or [] if any(
            w in a["facility"].lower() for w in [x.lower() for x in names] + plant["name_words"])]
        if mine:
            L += ["Linn County applications under review:", ""]
            L += [f"- received {a['received']}: {a['facility']}, {a['project']}, {a['type']}" for a in mine]
            L.append("")
    if plant["county_prog"] == "polk":
        L += ["## Polk County air permits", "",
              "Polk County Air Quality issues this plant's air permits. Issued permits: "
              f"{POLK}/construction.aspx (search by the facility's AIRS number). Out for public comment: "
              f"{POLK}/ConstructionDrafts.aspx.", ""]
        key = KNOWN_POLK.get(plant["id"], "").lower()
        mine = [d for d in polk_rows or [] if (key and key in d["facility"].lower())
                or any(w in d["facility"].lower() for w in plant["name_words"])]
        if polk_rows is None:
            L += ["The public comment list did not load this run. Retry before concluding anything.", ""]
        for d in mine:
            L += [f"- out for comment, project {d['project']}: {d['url']}", f"    - {d['text']}"]
        if mine:
            L.append("")
    return L


# ---------------------------------------------------------------- plants ---

def load_plants(args):
    scope_dir = REPO / "batches" / args.scope
    sweep = json.loads((scope_dir / "staging" / "sweep_args.json").read_text())
    csv = pd.read_csv(sweep["csv"], low_memory=False)
    wanted = set(args.plants.split(",")) if args.plants else None
    maps = {}
    for m in args.map or []:
        pid, ids = m.split("=", 1)
        maps[pid] = [int(x) for x in ids.split(",") if x]
    plants = []
    for p in sweep["plants"]:
        pid = p["plant_id"]
        if wanted is not None and pid not in wanted:
            continue
        rows = csv[csv["GEM location ID"] == pid]
        if rows.empty:
            continue
        r = rows.iloc[0]
        others = [x for x in str(r.get("Other Name(s)") or "").split(";") if x.strip() and x != "nan"]
        owner = str(r.get("Owner(s)") or "")
        ow = ""
        for key, word in (("interstate power", "ipl"), ("alliant", "ipl"),
                          ("midamerican", "midamerican"), ("central iowa power", "central iowa power"),
                          ("city of ames", "ames")):
            if key in owner.lower():
                ow = word
                break
        city = r.get("City") if isinstance(r.get("City"), str) else ""
        county = str(r.get("Local area (taluk, county)") or "").lower()
        prog = ("linn" if "linn" in county or city.lower() in LINN_CITIES or pid in KNOWN_LINN else
                "polk" if "polk" in county or city.lower() in POLK_CITIES or pid in KNOWN_POLK else "")
        plants.append({"id": pid, "name": p.get("plant_name") or r["Plant name"],
                       "other_names": others, "city": r.get("City") if isinstance(r.get("City"), str) else "",
                       "county": str(r.get("Local area (taluk, county)") or ""),
                       "statuses": sorted(set(rows["Status"].astype(str))),
                       "owner_word": ow, "map": maps.get(pid, []), "county_prog": prog,
                       "name_words": sorted(words(p.get("plant_name") or r["Plant name"]))})
    return plants


# ----------------------------------------------------------------- write ---

def write_index(path, plant, matched, facilities_done, comments, apps, county):
    L = [f"# Iowa air permit files for {plant['name']} ({plant['id']})", "",
         "Source: the Iowa Department of Natural Resources air construction permit pages, "
         "idnraqrr.iowadnr.gov/ConPermitSearch. Pages and permit files marked as saved are in "
         "the local fetch cache, so `python scripts/fetch.py <url> --text` and "
         "`url_verifier.py` read them at once.", "",
         f"Harvested: {time.strftime('%Y-%m-%d %H:%M %Z')}", ""]
    if county:
        L += [f"This plant is in a county with its own air permit program. The county's permits "
              f"are listed at the end of this file.", ""]
    if not matched:
        L += ["No Iowa DNR facility was matched to this plant. A new plant gets a facility page "
              "once its first permit is issued. Read _applications.md (applications under review) "
              "and _public_comment.md (open comment periods) and _unmatched.md (power facilities "
              "that match no GEM plant) in this folder for it.", ""]
    for f, how in matched:
        fd = facilities_done.get(f["id"], {})
        L += [f"## {f['name']} (DNR facility {f['id']}, plant number {f['number']}, {f['city']})", "",
              f"Matched: {how}.", f"Permit page: {BASE}/ConstructionPermit?id={f['id']}"]
        if fd.get("status") != "200":
            L += [f"The permit page did not load (HTTP {fd.get('status')}). Run "
                  "`python scripts/fetch.py <url>` on it; never record it as blocked without "
                  "the whole fetch ladder.", ""]
            continue
        rows = fd["rows"]
        L += [f"Permits listed: {len(rows)}, newest issued {rows[0]['date'] if rows else 'none'}.", ""]
        for r in rows[:args_rows_limit]:
            L.append(f"- {r['date']}: permit {r['permit']}, project {r['project']}, "
                     f"emission point {r['point']}, {r['equipment']}")
            d = r.get("doc")
            if d:
                tag = "saved" if d["state"] == "saved" else f"not saved, HTTP {d['state']}"
                L.append(f"    - permit file ({tag}): {r['link']}")
                for c in d.get("facts", []) + [f"states: {x}" for x in d.get("sizes", [])]:
                    L.append(f"    - {c}")
        if len(rows) > args_rows_limit:
            L.append(f"- and {len(rows) - args_rows_limit} older permits on the permit page.")
        L.append("")
        psd = fd.get("psd")
        if psd:
            L += [f"Large-project (PSD) documents: {psd['url']}", ""]
            for d in psd["docs"][:20]:
                L.append(f"- project {d['project']}, {d['type']}, {d['file']}: {d['link']}")
            L.append("")
        mine = [a for a in apps or [] if a["number"].startswith(f["number"])]
        if mine:
            L += ["Applications under review in the EasyAir system:", ""]
            L += [x for a in mine for x in _app_block(a)]
            L.append("")
        cm = [c for c in comments or [] if f["number"] in c.get("text", "")
              or f["name"].lower() in " ".join(c["cells"]).lower()]
        for c in cm:
            L += [f"Open public comment: {c['url']}", "", "> " + c["text"][:600], ""]
            L += [f"- {d['name']}: {d['url']}" for d in c["documents"]] + [""]
    # a new plant has no facility page yet, but its application names it
    numbers = [f["number"] for f, _ in matched]
    named = [a for a in apps or [] if plant["name_words"]
             and set(plant["name_words"]) <= words(a["facility"]) | {"ipl"}
             and not any(a["number"].startswith(n) for n in numbers)]
    if named:
        L += ["Applications under review in the EasyAir system that name this plant:", ""]
        L += [x for a in named for x in _app_block(a)]
        L.append("")
    L += county
    path.write_text("\n".join(L), encoding="utf-8")


args_rows_limit = 40


def main():
    global args_rows_limit
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--scope", required=True, help="batch folder name, e.g. us-ia")
    ap.add_argument("--plants", help="comma-separated GEM location IDs (default: every plant)")
    ap.add_argument("--map", action="append", metavar="PLANT=ID[,ID]",
                    help="DNR facility ids for a plant, replacing the built-in match (repeatable)")
    ap.add_argument("--since", default="2018-01-01", help="download permit files issued on or after this date")
    ap.add_argument("--docs-per-facility", type=int, default=12)
    ap.add_argument("--rows", type=int, default=40, help="permit rows listed per facility")
    ap.add_argument("--match-only", action="store_true", help="list facility matches and stop")
    args = ap.parse_args()
    args_rows_limit = args.rows

    out_dir = REPO / "work" / "permits" / args.scope
    out_dir.mkdir(parents=True, exist_ok=True)
    facilities = directory()
    log(f"directory: {len(facilities)} facilities")
    plants = load_plants(args)
    matches = {p["id"]: match(p, facilities) for p in plants}
    if args.match_only:
        for p in plants:
            for f, how in matches[p["id"]] or [({"id": "-", "name": "no match", "city": ""}, "")]:
                print(f"{p['id']}\t{p['name']}\t{f['id']}\t{f['name']}\t{f['city']}\t{how}")
        return

    psd_ids = psd_index() or set()
    comment_url, comments = public_comments()
    apps = applications()
    log(f"public comment: {len(comments or [])} open; applications under review: {len(apps or [])}")
    application_forms([a for a in apps or [] if (POWER_NAME.search(a["facility"])
                       and not POWER_NAME_DROP.search(a["facility"]))
                       or DATA_CENTER.search(a["facility"])])
    linn_co = linn_companies() if any(p["county_prog"] == "linn" for p in plants) else {}
    linn = {"issued": {}, "review": linn_review() if linn_co else []}
    for name in sorted({n for p in plants if p["county_prog"] == "linn" for n in KNOWN_LINN.get(p["id"], [])}):
        if linn_co and name in linn_co:
            linn["issued"][name] = linn_issued(linn_co[name])
    polk_rows = polk_drafts() if any(p["county_prog"] == "polk" for p in plants) else []
    log(f"Linn County: {len(linn['issued'])} companies read, {len(linn['review'] or [])} under review; "
        f"Polk County: {len(polk_rows or [])} out for comment")

    done = {}

    def harvest_facility(f):
        if f["id"] in done:
            return done[f["id"]]
        status, rows = permit_table(f["id"])
        fd = {"status": status, "rows": rows}
        n = 0
        for r in rows:
            if n >= args.docs_per_facility or r["iso"] < args.since:
                break
            if not r["link"] or not EQUIPMENT.search(r["equipment"]):
                continue
            page = get(r["link"], timeout=300)
            ok = page.status == "200" and bool(page.text.strip())
            r["doc"] = {"state": "saved" if ok else page.status,
                        "facts": pdf_facts(page.text) if ok else [],
                        "sizes": size_lines(page.text) if ok else []}
            n += 1
        if f["id"] in psd_ids:
            url, st, docs = psd_documents(f["id"])
            fd["psd"] = {"url": url, "status": st, "docs": docs}
        log(f"    facility {f['id']} {f['name']}: HTTP {status}, {len(rows)} permits, {n} files read")
        done[f["id"]] = fd
        return fd

    logf = (out_dir / "harvest_log.jsonl").open("a", encoding="utf-8")
    matched_ids = set()
    for k, p in enumerate(plants, 1):
        log(f"({k}/{len(plants)}) {p['name']}")
        for f, _ in matches[p["id"]]:
            harvest_facility(f)
            matched_ids.add(f["id"])
        county = county_section(p, linn, linn_co, polk_rows, args.since, args.docs_per_facility)
        write_index(out_dir / f"{p['id']}.md", p, matches[p["id"]], done, comments, apps, county)
        logf.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "plant": p["id"],
                               "name": p["name"],
                               "facilities": [{"id": f["id"], "how": how,
                                               "status": done[f["id"]]["status"],
                                               "permits": len(done[f["id"]]["rows"])}
                                              for f, how in matches[p["id"]]]}) + "\n")
        logf.flush()

    # power-like facilities that no GEM plant matched, newest permit first
    L = ["# Iowa DNR power facilities that match no GEM plant in this batch", "",
         "Each may be a plant outside this batch, a plant GEM lacks, or not a power plant at all. "
         "Check the newest permits for engines or turbines of 50 MW or more in total.", ""]
    others = [f for f in facilities if f["id"] not in matched_ids
              and POWER_NAME.search(f["name"]) and not POWER_NAME_DROP.search(f["name"])]
    for f in others:
        st, rows = permit_table(f["id"])
        f["newest"] = rows[0] if rows else None
        f["status"] = st
    others.sort(key=lambda f: (f["newest"] or {}).get("iso", ""), reverse=True)
    for f in others:
        nw = f["newest"]
        tail = (f"newest permit {nw['date']}, {nw['permit']}, {nw['equipment']}" if nw
                else f"no permits listed (HTTP {f['status']})")
        L.append(f"- {f['name']} ({f['city']}, plant number {f['number']}): {tail}. "
                 f"{BASE}/ConstructionPermit?id={f['id']}")
    (out_dir / "_unmatched.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    L = [f"# Iowa DNR open public comment periods ({comment_url})", ""]
    for c in comments or []:
        L += [f"## {' | '.join(c['cells'])}", "", c["url"], "", "> " + c["text"][:800], ""]
        L += [f"- {d['name']}: {d['url']}" for d in c["documents"]] + [""]
    if comments is None:
        L.append("The list did not load this run. Run fetch.py on it before concluding anything.")
    (out_dir / "_public_comment.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    L = ["# County air permit programs (Linn and Polk)", "",
         f"Linn County applications under review ({LINN}/ApplicationsUnderReview):", ""]
    L += [f"- received {a['received']}: {a['facility']}, {a['project']}, {a['type']}"
          for a in linn["review"] or []] or ["- none listed, or the list did not load."]
    L += ["", f"Polk County permits out for public comment ({POLK}/ConstructionDrafts.aspx):", ""]
    L += [f"- {d['facility']}, project {d['project']}: {d['text']} {d['url']}" for d in polk_rows or []] \
        or ["- none listed, or the list did not load."]
    L += ["", "Linn County companies whose names look like power plants (pick them at "
          f"{LINN}/IssuedPermits):", ""]
    L += [f"- {n}" for n in sorted(linn_co or {}) if POWER_NAME.search(n) and not POWER_NAME_DROP.search(n)]
    (out_dir / "_county.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    L = [f"# Iowa DNR applications under review ({EASYAIR})", "",
         f"{len(apps or [])} applications. Power plant and data center ones first, with the "
         "lines read from their submitted forms.", ""]
    if apps is None:
        L.append("The list did not load this run. Retry before concluding anything.")
    for a in sorted(apps or [], key=lambda a: "forms" not in a):
        L += _app_block(a)
    (out_dir / "_applications.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    log("done")


if __name__ == "__main__":
    main()

"""
Harvest Mississippi air permits before a research sweep.

The Mississippi Department of Environmental Quality (MDEQ) keeps its air permit
records in three places. All three load without a login, and none is a dead
end. What was found (2026-10-23):

  1. enSearch Online (opcgis.deq.state.ms.us/ensearchonline/), an ASP.NET
     WebForms site. Its search pages look like forms that need a script, so
     this script posts them the way a browser does (hidden form state first):
       - epd-active-permits-and-coverages.aspx: every active permit by permit
         type (the five Air types) and by SIC code (electric utilities,
         cogeneration, data processing). One page of results, no paging.
       - epd-activity-search.aspx: every permit application received and every
         permit issued in a date range, one sentence each, grouped by county.
         This is the history: applications since 2021 show projects before a
         permit exists.
       - epd-permits-at-public-notice.aspx: permits out for comment now, with
         the notice, the draft permit and the statement of basis as PDFs. The
         archive holds 20 or more saved copies of this page, which recover
         notices that have since come down.
       - ai_info.aspx?ai=N: one facility (an "agency interest"): address,
         active permits with their PDFs (get_doc.aspx?dt=finalp&id=N), and the
         status of every application. The permit PDFs hold the equipment list.
  2. The Permit Board agenda and minutes archive on www.mdeq.ms.gov
     (/permits/permit-board/agendas/ and /minutes/), one page per year, each
     listing the meeting PDFs. The board hears only the larger or contested
     items, so a power plant shows up there rarely, but a hearing item is a
     strong lead.
  3. The Air Division public notice page (www.mdeq.ms.gov/air/air-division/)
     carries only rule and fee notices. Facility permit notices are in
     enSearch (item 1), not on that page.

Steps:
  1. Read the activity search for every air action since --since (default 2021).
  2. Read the active permit lists: five Air permit types, and the power and
     data center SIC codes.
  3. Read the public notice page, now and in every archive snapshot.
  4. Read the Permit Board agendas and minutes (default from 2021 on).
  5. Keep the facilities that look like power plants or data centers (an air
     permit and a power SIC code or a power-like name), match each GEM
     Mississippi plant to them (KNOWN holds hand-checked name patterns; a name
     word match adds more, marked for checking) and list the rest as possible
     new plants.
  6. Download every document of a matched or power-like facility (the active
     permit PDFs and the public notice, draft permit and statement of basis
     PDFs) through fetch.py (disk cache in work/fetch_cache/, so
     url_verifier.py reads them at once) and keep the lines that give the
     permit number, project, equipment, maker, model, sizes (MW, MMBtu/hr,
     horsepower) and the location.

Output, in scopes/<scope>/work/permits/ (what the sweep agents read): one plain-text
index per plant (<GEM location id>.md), plus _unmatched.md, _notices.md,
_board.md, _activity.md and harvest_log.jsonl. A summary and the data behind it
go to batches/<scope>/harvest/ (harvest_summary.md, facilities.json,
notices.json, board_items.json, activity_air.json). Permit PDFs name agency
and company staff with their contact details: the PDFs and the full document
text stay under work/ (never committed). Nothing here stages a record.

Usage (from the repo root):
    python scopes/us-ms/harvest_permits.py --scope us-ms                  # every plant
    python scopes/us-ms/harvest_permits.py --scope us-ms --plants L100001025781
    python scopes/us-ms/harvest_permits.py --scope us-ms --match-only     # list matches, download no documents
    python scopes/us-ms/harvest_permits.py --scope us-ms --no-wayback     # current notices only
"""
import argparse
import html
import json
import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from fetch import CHROME_UA, fetch_page  # noqa: E402
from harvest_lib import CDX, CSV, REPO, SIZE, clean, get, harvest_out, lines_of, pick, wayback_url  # noqa: E402

ENS = "https://opcgis.deq.state.ms.us/ensearchonline"
MDEQ = "https://www.mdeq.ms.gov"

AIR_TYPES = ["Air - Construction PSD", "Air - Construction Permit", "Air - Title V", "Air - SMOP",
             "Air - State Operating Permit"]
# SIC codes whose facilities can hold generating capacity: electric services,
# electric and other services combined, gas and other services combined,
# combination utilities, steam supply, cogeneration, data processing.
POWER_SICS = ["4911", "4931", "4932", "4939", "4961", "4991", "7374"]

# Hand-checked name patterns (2026-10-23): GEM plant -> regexes that must hit
# "<facility name> | <city>" of an enSearch facility. A plant missing here is
# matched by its name words, and those matches are marked for checking.
KNOWN = {
    "L100000401921": [r"attala"],                                         # Attala power station, Sallis
    "L100000401833": [r"batesville (gener|power|energy)"],                # Batesville generation facility
    "L100000401922": [r"baxter wilson"],
    "L100000401627": [r"tva caledonia", r"tennessee valley.*caledonia combined"],   # Caledonia power station, Steens
    "L100000402094": [r"chevron.*pascagoula refinery", r"chevron cogenerat"],
    "L100000401923": [r"choctaw county (gener|power|energy)", r"french camp"],
    "L100001047324": [r"\bxai\b", r"mzx", r"colossus"],                   # Colossus 2, xAI Southaven
    "L100000401819": [r"crossroads (energy|power|gener)"],
    "L100001025781": [r"delta blues advanced"],
    "L100000401924": [r"andrus"],
    "L100000401925": [r"hinds (energy|power|gener)", r"hinds county plant"],
    "L100000104009": [r"watson"],
    "L100000402320": [r"kemper (county|project|energy|power)", r"\bkemper\b"],
    "L100000402322": [r"magnolia (combined|power|gener|energy)"],
    "L100000104011": [r"morrow"],
    "L100000401834": [r"moselle (power|gener|energy|station)"],
    "L100001023568": [r"new caledonia"],
    "L100000402325": [r"quantum choctaw", r"ackerman (combined|power|gener|energy)"],
    "L100000402096": [r"ratcliffe"],
    "L100000401835": [r"silver creek (power|energy|gener)"],
    "L100000401628": [r"southaven (combined|power|gener|energy)", r"tva.*southaven"],
    "L100001064651": [r"traceview", r"madison county advanced", r"ridgeland power"],
    "L100001080981": [r"vicksburg advanced", r"\bvaps\b"],
    "L100000402097": [r"victor j|plant daniel|daniel (electric|gener|power)"],
}

POWER_NAME = re.compile(
    r"power|electric|generat|energy|entergy|\btva\b|tennessee valley|cooperative|southern company|"
    r"turbine|cogen|steam|utilit|data ?cent|datacent|\bxai\b|\bmzx\b|amazon|\baws\b|compute|colossus|"
    r"hyperscal|cloud|combined cycle|peaking|kemper|ratcliffe|daniel|watson|morrow|traceview|"
    r"baxter|andrus|attala|caledonia|moselle|choctaw", re.I)
POWER_DROP = re.compile(
    r"sawmill|lumber|forest products|timber|plywood|veneer|asphalt|ready mix|concrete|landfill|"
    r"poultry|catfish|feed|gin\b|cotton|compressor|pipeline|pipe line|gas transmission|gas pipe|"
    r"refinery|chemical|steel|wire|motors|bakeries|ethanol|biodiesel|pellet|shipyard|marine|"
    r"hospital|school|university|college|casino|resort|walmart|wal mart|dollar|apparel|furniture|"
    r"paper|pulp|packaging|brick|cement|lime|aluminum|silicon|oil and gas|gas processing|"
    r"terminal|storage|propane|truck|rail|crematory|cemetery|funeral|printing|bottling|sand|gravel|"
    r"quarry|wood|mill\b|manufactur", re.I)
NAME_NOISE = re.compile(
    r"\b(power station|power plant|generating station|generating|generation|facility|station|energy center|"
    r"energy|plant|power|gt|ms|mississippi|the|municipal|of|and|city|llc|inc|company|co|corp|"
    r"corporation|advanced|combined|cycle|county)\b", re.I)
EQUIPMENT = re.compile(r"turbine|\bct\b|engine|rice\b|generat|\bgen\b|boiler|duct burner|hrsg|"
                       r"combined cycle|peaking|diesel|reciprocating|genset", re.I)
MAKER = re.compile(r"model\b|caterpillar|cat g|wartsila|w[äa]rtsil[äa]|jenbacher|"
                   r"general electric|\bGE\b|siemens|solar turbines|mitsubishi|cummins|rolls[- ]royce|"
                   r"mtu\b|kohler|generac|waukesha|baldor|clarke (fire|diesel|engine)|detroit diesel|pratt|ansaldo|"
                   r"hitachi|titan \d|taurus|mars \d|lm ?\d{4}|7ea|7fa|7ha|6b\b|f-?class|h-?class", re.I)
LOCATION = re.compile(
    r"latitude|longitude|\blat\b|\blong\b|\bUTM\b|\bsection \d+|township|"
    r"located (at|in|on|near|approximately)|physical address|site address|facility address|"
    r"street address|\b\d{2,5} [A-Z0-9][\w. ]+ (road|rd|street|st|avenue|ave|"
    r"highway|hwy|drive|dr|lane|ln|blvd|boulevard)\b|county,? mississippi|ms 3[89]\d{3}|mississippi 3[89]\d{3}",
    re.I)
PROJECT = re.compile(r"proposes|propose to|will consist|project (is|will|consists)|construction of|"
                     r"to construct|new (electric|power|generat)|install(ation)? of", re.I)
LATLON = re.compile(r"\b(3[0-5]\.\d{3,})\s*[,;/ ]\s*-?\s*(8[7-9]\.\d{3,}|9[0-2]\.\d{3,})\b")
PERMIT_NO = re.compile(r"\b\d{4}-\d{5}\b")


def log(msg):
    print(f"[harvest-ms] {msg}", file=sys.stderr, flush=True)


def words(text):
    t = NAME_NOISE.sub(" ", re.sub(r"\(.*?\)", " ", str(text or "")))
    return {w.lower() for w in re.split(r"[^A-Za-z]+", t) if len(w) >= 4}


def us_date(s):
    """MM/DD/YYYY to YYYY-MM-DD, or '' when it is not a date."""
    m = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", s or "")
    return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}" if m else ""


# ------------------------------------------------------------ enSearch forms ---

class Ens:
    """A WebForms session: GET the page for its hidden state, POST the filled form."""

    def __init__(self):
        self.s = requests.Session()
        self.s.headers["User-Agent"] = CHROME_UA

    @staticmethod
    def hidden(text):
        return {m.group(1): html.unescape(m.group(2)) for m in
                re.finditer(r'<input[^>]*type="hidden"[^>]*name="([^"]+)"[^>]*value="([^"]*)"', text)}

    def post(self, page, fields, retries=3, timeout=300):
        url = f"{ENS}/{page}"
        last = ""
        for i in range(retries):
            try:
                r = self.s.get(url, timeout=90)
                if r.status_code != 200:
                    last = f"GET HTTP {r.status_code}"
                    time.sleep(5 * (i + 1))
                    continue
                data = self.hidden(r.text)
                data.update(fields)
                r = self.s.post(url, data=data, timeout=timeout)
                if r.status_code == 200:
                    return r.text
                last = f"POST HTTP {r.status_code}"
            except requests.RequestException as e:
                last = str(e)
            time.sleep(5 * (i + 1))
        log(f"{page}: {last}")
        return None


def parse_active(text):
    """Rows of the active permits grid: ai id, name, permit number and type, city, county."""
    out = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", text or "", re.S):
        m = re.search(r"ai_info\.aspx\?ai=(\d+)", tr)
        if not m:
            continue
        tds = [clean(x) for x in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
        tds = [x for x in tds if x != ""]
        if len(tds) < 6:
            continue
        out.append({"ai": int(m.group(1)), "name": tds[1], "permit": tds[2], "type": tds[3],
                    "city": tds[4], "county": tds[5]})
    return out


def active_search(ens, permit_type="$$$", sic=""):
    text = ens.post("epd-active-permits-and-coverages.aspx", {
        "uxName": "", "uxSIC": sic, "uxCity$uxCity": "$$$", "uxCounty$uxCounty": "$$$",
        "uxBasin$uxBasin": "$$", "uxPermitNumber": "", "uxPermitType": permit_type,
        "uxSort": "AINAME", "uxSubmit": "SEARCH"})
    return None if text is None else parse_active(text)


ACTION = re.compile(r"\s*(?:,\s*)?([A-Z][A-Za-z.' -]+, MS\s+)?(?P<what>(applied|was issued|was granted|was).*)$", re.S)


def parse_activity(text):
    """Every sentence of the activity search: county, facility, ai id, sentence, date."""
    out = []
    county = ""
    for m in re.finditer(r"countytitle'?\"?>(.*?)</h2>|<a href=\"ai_info\.aspx\?ai=(\d+)\">(.*?)</a>(.*?)</p>",
                         text or "", re.S):
        if m.group(1) is not None:
            county = clean(m.group(1))
            continue
        sentence = clean(m.group(4))
        out.append({"ai": int(m.group(2)), "name": clean(m.group(3)), "county": county,
                    "text": sentence.lstrip(", ").strip(), "date": us_date(sentence[-14:])})
    return out


def activity_search(ens, since):
    end = time.strftime("%m/%d/%Y")
    text = ens.post("epd-activity-search.aspx", {"uxActionType": "$$$$", "uxStartDate": since,
                                                "uxEndDate": end, "uxSubmit": "SEARCH"}, timeout=600)
    return None if text is None else parse_activity(text)


def air_sentence(a):
    return bool(re.search(r"\bair\b", a["text"], re.I))


# --------------------------------------------------------------- facility page ---

def parse_ai_info(text):
    """The parts of a facility page the harvest keeps (no staff names or phone numbers)."""
    def table(tid):
        m = re.search(rf'<table[^>]*id="{tid}"[^>]*>(.*?)</table>', text, re.S)
        if not m:
            return []
        rows = []
        for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", m.group(1), re.S)[1:]:
            cells = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
            docs = [d for d in re.findall(r"href='([^']*get_doc[^']*)'", tr)]
            rows.append([clean(c) for c in cells] + [f"{ENS}/{d}" for d in docs])
        return rows
    gen = table("uxGeneral")
    addr = table("uxAddress")
    out = {
        "name": clean((re.search(r'id="uxAIName">(.*?)</span>', text, re.S) or [0, ""])[1]),
        "general": gen[0] if gen else [],
        "address": addr[0][0] if addr and addr[0] else "",
        "alt_ids": table("uxAlt"),
        "active_permits": [],
        "applications": table("uxPER"),
        "general_applications": table("uxGNP"),
    }
    for r in table("uxACTIVEPER"):
        out["active_permits"].append({"type": r[0], "number": r[1], "issued": us_date(r[2]),
                                      "docs": [x for x in r[3:] if x.startswith("http")]})
    return out


def ai_page(ai):
    page = get(f"{ENS}/ai_info.aspx?ai={ai}")
    if page.status != "200":
        log(f"ai_info {ai}: HTTP {page.status}")
        return None
    return parse_ai_info(page.text)


# ---------------------------------------------------------------- public notices ---

def parse_notice_page(text, base=ENS):
    """Rows of the permits-at-public-notice table: name, ai id, type, city, county,
    end date and the notice, draft permit and statement of basis PDFs."""
    out = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", text or "", re.S):
        m = re.search(r"ai_info\.aspx\?ai=(\d+)", tr)
        if not m:
            continue
        tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
        if len(tds) < 5:
            continue
        cells = [clean(x) for x in tds]
        docs = []
        for h in re.findall(r"""href=['"]([^'"]*get_doc[^'"]*)['"]""", tr):
            h = html.unescape(h)
            kind = re.search(r"dt=(\w+)", h)
            docs.append({"name": {"pnotice": "public notice", "dpermit": "draft permit",
                                  "eparat": "statement of basis"}.get(kind.group(1) if kind else "", "document"),
                         "url": h if h.startswith("http") else f"{base}/{h.lstrip('/')}"})
        out.append({"source": "enSearch public notice", "ai": int(m.group(1)), "facility": cells[0],
                    "type": cells[1], "city": cells[2], "county": cells[3], "end": us_date(cells[4]),
                    "docs": docs})
    return out


def notice_snapshots(wayback=True, limit=0):
    """Records from the live public notice page and every distinct archive snapshot of it."""
    recs = []
    live = get(f"{ENS}/epd-permits-at-public-notice.aspx")
    if live.status == "200":
        for r in parse_notice_page(live.text):
            r["seen"] = "now"
            recs.append(r)
    else:
        log(f"public notice page: HTTP {live.status}")
    snaps = []
    if wayback:
        try:
            r = requests.get(CDX, params={"url": "opcgis.deq.state.ms.us/ensearchonline/epd-permits-at-public-notice.aspx",
                                          "output": "json", "fl": "timestamp", "filter": "statuscode:200",
                                          "collapse": "digest", "limit": 2000}, timeout=120)
            snaps = [x[0] for x in r.json()[1:]]
        except (requests.RequestException, ValueError) as e:
            log(f"Wayback index: {e}")
        if limit:
            snaps = snaps[-limit:]
        for ts in snaps:
            p = get(f"https://web.archive.org/web/{ts}id_/{ENS}/epd-permits-at-public-notice.aspx", timeout=180)
            if p.status != "200":
                log(f"  snapshot {ts}: HTTP {p.status}")
                continue
            for r in parse_notice_page(p.text):
                r["seen"] = ts[:8]
                recs.append(r)
        log(f"Wayback: {len(snaps)} snapshots read")
    return recs, len(snaps)


def merge_notices(recs):
    """One record per (facility id, notice document); the dates seen are unioned."""
    out = {}
    for r in recs:
        key = (r["ai"], r["type"], tuple(sorted(d["url"] for d in r["docs"])) or r["end"])
        m = out.setdefault(key, {**r, "seen": set()})
        if r.get("seen"):
            m["seen"].add(r["seen"])
    return list(out.values())


# ---------------------------------------------------------------- permit board ---

def board_year_pages(kind):
    """{year label: page url} from the archive index (kind is agendas or minutes)."""
    idx = get(f"{MDEQ}/permits/permit-board/{kind}/")
    if idx.status != "200":
        log(f"permit board {kind} index: HTTP {idx.status}")
        return {}
    pages = {}
    for h in re.findall(r'href="((?:https://www\.mdeq\.ms\.gov)?/permits/permit-board/' + kind + r'/[^"]+/)"', idx.text):
        h = h if h.startswith("http") else MDEQ + h
        if h.rstrip("/").endswith("/" + kind):
            continue
        pages[h] = None
    return list(pages)


def board_docs(kind, since_year):
    """[(year, label, pdf url)] for every agenda or minutes file from since_year on."""
    docs = []
    for url in board_year_pages(kind):
        p = get(url)
        if p.status != "200":
            log(f"  {url}: HTTP {p.status}")
            continue
        main = p.text[p.text.find("<main"):p.text.find("</main>")]
        year = (re.search(r"(20\d\d)", url) or re.search(r"Permit Board \w+ (20\d\d)", clean(main)) or [0, ""])[1]
        if not year:
            m = re.search(r"/uploads/(20\d\d)/", main)
            year = m.group(1) if m else ""
        for h, t in re.findall(r'<a [^>]*href="([^"]+\.(?:pdf|docx?))"[^>]*>(.*?)</a>', main, re.S):
            y = (re.search(r"/uploads/(20\d\d)/", h) or [0, year])[1]
            if y and int(y) >= since_year:
                docs.append({"kind": kind, "year": y, "label": clean(t), "url": html.unescape(h), "page": url})
    seen, out = set(), []
    for d in docs:
        if d["url"] not in seen:
            seen.add(d["url"])
            out.append(d)
    return out


MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"


def meeting_date(text, url):
    m = re.search(rf"\b({MONTHS})\s+(\d{{1,2}}),?\s+(20\d\d)", text[:1500])
    if m:
        return f"{m.group(3)}-{MONTHS.split('|').index(m.group(1)) + 1:02d}-{int(m.group(2)):02d}"
    return ""


def board_items(text):
    """Air items of an agenda or minutes: chunks that name an air permit number or an Air
    Division action, with the facility line above it."""
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]
    items, i = [], 0
    starts = [k for k, ln in enumerate(lines) if re.match(r"(Facility:|Permit Board Agenda|Mississippi Environmental Quality Permit Board)", ln, re.I)]
    starts = starts or [0]
    starts.append(len(lines))
    for a, b in zip(starts, starts[1:]):
        chunk = lines[a:b]
        blob = " ".join(chunk)
        if not (PERMIT_NO.search(blob) and re.search(r"\bair\b", blob, re.I)) and not re.search(r"air (title v|construction|operating|division)", blob, re.I):
            continue
        fac = next((re.sub(r"^Facility:\s*", "", ln) for ln in chunk if ln.lower().startswith("facility:")), "")
        items.append({"facility": fac, "permits": sorted(set(PERMIT_NO.findall(blob))),
                      "text": blob[:900]})
    return items


def read_board(since_year):
    docs = board_docs("agendas", since_year) + board_docs("minutes", since_year)
    log(f"Permit Board: {len(docs)} agenda and minutes files from {since_year}")
    out = []
    for k, d in enumerate(docs, 1):
        p = get(d["url"], timeout=200)
        ok = p.status == "200" and bool(p.text.strip())
        d["state"] = "saved" if ok else f"not saved, HTTP {p.status}"
        if not ok:
            snap = wayback_url(d["url"])
            if snap:
                p = get(snap, timeout=200)
                ok = p.status == "200" and bool(p.text.strip())
                d["state"] = "saved (from the Wayback copy)" if ok else f"not saved, HTTP {p.status}"
        d["date"] = meeting_date(p.text, d["url"]) if ok else ""
        d["items"] = board_items(p.text) if ok else []
        d["power_lines"] = [ln.strip() for ln in p.text.splitlines()
                            if ok and POWER_NAME.search(ln) and not POWER_DROP.search(ln)
                            and re.search(r"power|generat|electric|energy|turbine|data ?cent|entergy|tva", ln, re.I)][:12]
        out.append(d)
        if k % 20 == 0:
            log(f"  board file {k}/{len(docs)}")
    return out


# ------------------------------------------------------------- match, facts ---

def is_power(fac):
    """A facility looks like a power or data center site: power SIC code, or a power-like
    name that is not on the drop list. Needs an air permit or air action (checked by the caller)."""
    if fac["name"] and POWER_DROP.search(fac["name"]) and not fac.get("sic_power"):
        return False
    return bool(fac.get("sic_power")) or bool(POWER_NAME.search(fac["name"]))


def fac_text(f):
    return f"{f['name']} | {f.get('city', '')}".lower()


def match(plant, facs):
    """[(facility, how)]: hand-checked patterns alone, else every distinctive word of the
    plant's name, or its city plus a power-like name."""
    out = []
    pats = KNOWN.get(plant["id"])
    if pats:
        for f in facs:
            if any(re.search(p, fac_text(f)) for p in pats):
                out.append((f, "checked by hand"))
        return out
    ws = plant["name_words"]
    city = plant["city"].lower()
    for f in facs:
        t = fac_text(f)
        if ws and ws <= words(t):
            out.append((f, "name match, check it is this plant"))
        elif city and f.get("city", "").lower() == city and is_power(f):
            out.append((f, "same city, power-like name, check it is this plant"))
    return out


def doc_facts(text):
    latlon = [f"{a}, -{b.lstrip('-')}" for a, b in LATLON.findall(text)][:3]
    return {
        "ids": sorted(set(PERMIT_NO.findall(text)))[:6],
        "project": pick(text, PROJECT, 6),
        "equipment": pick(text, EQUIPMENT, 10),
        "makers": pick(text, MAKER, 8),
        "sizes": pick(text, SIZE, 10),
        "location": pick(text, LOCATION, 8),
        "coords": latlon,
    }


def read_docs(docs, cap=10):
    """Download a facility's documents and keep facts. Each doc is {name, url}."""
    for n, d in enumerate(docs):
        if n >= cap:
            d["state"] = "not read (cap)"
            continue
        page = get(d["url"], timeout=300)
        ok = page.status == "200" and bool(page.text.strip())
        via = ""
        if not ok:
            snap = wayback_url(d["url"])
            if snap:
                page = get(snap, timeout=300)
                if page.status == "200" and page.text.strip():
                    ok, via = True, f" (from the Wayback copy {snap})"
                    d["archive"] = snap
        d["state"] = f"saved{via}" if ok else f"not saved, HTTP {page.status}"
        d["facts"] = doc_facts(page.text) if ok else {}


# ---------------------------------------------------------------- reporting ---

def fac_docs(f, notices):
    """Every document of a facility: active permit PDFs and its public notice PDFs."""
    docs, seen = [], set()
    for p in f.get("page", {}).get("active_permits", []):
        if not p["type"].lower().startswith("air"):
            continue
        for u in p["docs"]:
            if u not in seen:
                seen.add(u)
                docs.append({"name": f"{p['type']} {p['number']} issued {p['issued']}", "url": u})
    for r in notices:
        if r["ai"] == f["ai"] and re.match(r"air", r["type"], re.I):
            for d in r["docs"]:
                if d["url"] not in seen:
                    seen.add(d["url"])
                    docs.append({"name": f"{d['name']} ({r['type']}, comments end {r['end']})", "url": d["url"]})
    return docs


def fac_block(f, how=None):
    pg = f.get("page") or {}
    gen = pg.get("general") or []
    L = [f"- {f['name']} (enSearch facility {f['ai']}): {f.get('city', '')}, {f.get('county', '')} County"
         + (f", SIC {gen[2]}" if len(gen) > 2 else "")]
    if pg.get("address"):
        L.append(f"    - where: {pg['address']}")
    for p in f.get("permits", [])[:12]:
        L.append(f"    - permit: {p['type']} {p['permit']}")
    for p in pg.get("active_permits", []):
        if p["type"].lower().startswith("air"):
            L.append(f"    - active permit available online: {p['type']} {p['number']} issued {p['issued']}")
    for r in pg.get("applications", []):
        if r and r[0] == "Air":
            L.append(f"    - application: {r[1]} {r[2]}, {us_date(r[3])}, {r[4] if len(r) > 4 else ''}")
    for a in f.get("activity", [])[-12:]:
        L.append(f"    - {a['date'] or 'no date'}: {a['text']}")
    for r in f.get("notices", []):
        L.append(f"    - public notice: {r['type']}, comments end {r['end']}"
                 + (f", seen on the notice page {sorted(r['seen'])[0]} to {sorted(r['seen'])[-1]}" if r.get("seen") else ""))
    for d in f.get("docs", []):
        L.append(f"    - document ({d.get('state', 'not read')}): {d['name']}: {d['url']}")
        fa = d.get("facts") or {}
        for key, label in (("ids", "permit numbers"), ("project", "project"), ("equipment", "equipment"),
                           ("makers", "maker or model"), ("sizes", "size"),
                           ("location", "site address or location"), ("coords", "coordinates")):
            for line in fa.get(key, []):
                L.append(f"        - {label}: {line if isinstance(line, str) else ', '.join(line)}")
    for b in f.get("board", [])[:8]:
        L.append(f"    - Permit Board {b['kind']} {b['date'] or b['year']}: {b['text'][:300]}  ({b['url']})")
    if how:
        L.insert(0, f"Matched: {how}.")
    return L


def write_index(path, plant, matched):
    L = [f"# Mississippi air permit files for {plant['name']} ({plant['id']})", "",
         "Source: MDEQ enSearch Online (active permits, application and issue history, permits at public "
         "notice and its archive copies, facility pages) and the Permit Board agendas and minutes. "
         "Documents marked saved are in the local fetch cache, so `python scripts/fetch.py <url> --text` "
         "and `url_verifier.py` read them at once.", "",
         f"Harvested: {time.strftime('%Y-%m-%d %H:%M %Z')}", "",
         f"GEM statuses: {', '.join(plant['statuses'])}. City in GEM: {plant['city'] or 'blank'}.", ""]
    if not matched:
        L += ["No enSearch facility matched this plant by name. That does not mean it has no permits: it "
              "may be listed under the owner, a contractor or a different site name. Check _unmatched.md "
              "and _board.md in this folder, and search enSearch by city and county.", ""]
    for f, how in matched:
        L += fac_block(f, how) + [""]
    path.write_text("\n".join(L), encoding="utf-8")


# ----------------------------------------------------------------- plants ---

def load_plants(args):
    csv = pd.read_csv(CSV, low_memory=False)
    csv = csv[csv["State/Province"] == "Mississippi"]
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


def build_facilities(active_air, active_sic, activity):
    """{ai: facility}: every facility with an air permit or an air action, with power flags."""
    facs = {}

    def fac(ai, name, city="", county=""):
        f = facs.setdefault(ai, {"ai": ai, "name": name, "city": city, "county": county,
                                 "permits": [], "activity": [], "notices": [], "board": [],
                                 "sic_power": False})
        f["city"] = f["city"] or city
        f["county"] = f["county"] or county
        return f

    for r in active_air:
        f = fac(r["ai"], r["name"], r["city"], r["county"])
        if r not in f["permits"]:
            f["permits"].append(r)
    for r in active_sic:
        if r["ai"] in facs:
            facs[r["ai"]]["sic_power"] = True
    sic_ids = {r["ai"] for r in active_sic}
    for a in activity:
        if air_sentence(a):
            f = fac(a["ai"], a["name"], "", a["county"])
            f["activity"].append(a)
            f["sic_power"] = f["sic_power"] or a["ai"] in sic_ids
    return facs, sic_ids


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--scope", required=True, help="batch folder name, e.g. us-ms")
    ap.add_argument("--plants", help="comma-separated GEM location IDs (default: every plant)")
    ap.add_argument("--match-only", action="store_true", help="list matches, download no documents")
    ap.add_argument("--no-wayback", action="store_true", help="skip the archive copies of the notice page")
    ap.add_argument("--snapshots", type=int, default=0, help="read only the newest N snapshots (0 = all)")
    ap.add_argument("--since", default="1/1/2021", help="start of the activity search, M/D/YYYY")
    ap.add_argument("--board-since", type=int, default=2021, help="first Permit Board year to read")
    ap.add_argument("--docs-per-facility", type=int, default=10)
    args = ap.parse_args()

    out_dir = harvest_out(args.scope)
    out_dir.mkdir(parents=True, exist_ok=True)
    hv_dir = REPO / "batches" / args.scope / "harvest"
    hv_dir.mkdir(parents=True, exist_ok=True)
    plants = load_plants(args)

    ens = Ens()
    active_air = []
    for ty in AIR_TYPES:
        rows = active_search(ens, ty)
        log(f"active permits, {ty}: {len(rows) if rows is not None else 'did not load'}")
        active_air += rows or []
    active_sic = []
    for sic in POWER_SICS:
        rows = active_search(ens, "$$$", sic)
        log(f"active permits, SIC {sic}: {len(rows) if rows is not None else 'did not load'}")
        active_sic += rows or []
    activity = activity_search(ens, args.since)
    log(f"activity search since {args.since}: {len(activity) if activity is not None else 'did not load'} actions")
    activity = activity or []
    facs, sic_ids = build_facilities(active_air, active_sic, activity)
    log(f"{len(facs)} facilities with an air permit or air action; {len([f for f in facs.values() if f['sic_power']])} with a power SIC code")

    notices = merge_notices(notice_snapshots(wayback=not args.no_wayback, limit=args.snapshots)[0])
    log(f"{len(notices)} distinct public notice records ({len([r for r in notices if re.match('air', r['type'], re.I)])} air)")
    for r in notices:
        if r["ai"] in facs:
            facs[r["ai"]]["notices"].append(r)
        elif re.match(r"air", r["type"], re.I):
            f = {"ai": r["ai"], "name": r["facility"], "city": r["city"], "county": r["county"],
                 "permits": [], "activity": [], "notices": [r], "board": [], "sic_power": r["ai"] in sic_ids}
            facs[r["ai"]] = f

    board = [] if args.match_only else read_board(args.board_since)
    for d in board:
        for it in d["items"]:
            for f in facs.values():
                nm = it["facility"] or it["text"]
                core = re.sub(r"[^a-z0-9 ]", "", f["name"].lower())
                if (it["permits"] and any(p.replace("-", "") in "".join(x["permit"].replace("-", "") for x in f["permits"]) for p in it["permits"])) \
                        or (len(core) > 8 and core in re.sub(r"[^a-z0-9 ]", "", nm.lower())):
                    f["board"].append({"kind": d["kind"], "date": d["date"], "year": d["year"],
                                       "url": d["url"], "text": it["text"]})

    power = [f for f in facs.values() if is_power(f)]
    matches = {p["id"]: match(p, list(facs.values())) for p in plants}
    for p in plants:
        for f, _ in matches[p["id"]]:
            if f not in power:
                power.append(f)
    matched_ids = {f["ai"] for ms in matches.values() for f, _ in ms}
    unmatched = [f for f in power if f["ai"] not in matched_ids]
    log(f"{len(power)} power-like facilities: {len(matched_ids)} matched to GEM plants, {len(unmatched)} unmatched")

    if args.match_only:
        for p in plants:
            for f, how in matches[p["id"]] or [({"name": "no match", "ai": "", "city": ""}, "")]:
                print(f"{p['id']}\t{p['name']}\t{f['name']}\t{f['ai']}\t{f.get('city', '')}\t{how}")
        for f in unmatched:
            print(f"UNMATCHED\t\t{f['name']}\t{f['ai']}\t{f.get('city', '')}\t{f['county']}")
        return

    for k, f in enumerate(power, 1):
        f["page"] = ai_page(f["ai"]) or {}
        f["docs"] = fac_docs(f, notices)
        log(f"({k}/{len(power)}) reading {len(f['docs'])} documents of {f['name']} ({f['ai']})")
        read_docs(f["docs"], args.docs_per_facility)

    logf = (out_dir / "harvest_log.jsonl").open("a", encoding="utf-8")
    for p in plants:
        write_index(out_dir / f"{p['id']}.md", p, matches[p["id"]])
        logf.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "plant": p["id"], "name": p["name"],
                               "facilities": [{"name": f["name"], "ai": f["ai"], "how": how,
                                               "docs": {d["name"]: d.get("state", "not read") for d in f["docs"]}}
                                              for f, how in matches[p["id"]]]}) + "\n")
    logf.close()

    L = ["# Mississippi facilities that look like power or data center sites but match no GEM plant in this batch", "",
         "Each may be a plant outside this batch, a plant GEM lacks, a backup generator at a site that is not "
         "a power plant, or not a power plant at all. Check engines or turbines of 50 MW or more in total "
         "(generating capacity only).", ""]
    for f in sorted(unmatched, key=lambda f: (not f["sic_power"], f["name"])):
        L += fac_block(f) + [""]
    if not unmatched:
        L.append("None this run.")
    (out_dir / "_unmatched.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    L = [f"# Mississippi air permits at public notice, now and in archive copies of the page ({len(notices)} records)", ""]
    for r in sorted(notices, key=lambda r: r["end"] or "", reverse=True):
        if not re.match(r"air", r["type"], re.I):
            continue
        L.append(f"- {r['facility']} ({r['ai']}), {r['city']}, {r['county']} County: {r['type']}, comments end {r['end']}"
                 + (f", on the page {sorted(r['seen'])[0]} to {sorted(r['seen'])[-1]}" if r.get("seen") else ""))
        for d in r["docs"]:
            L.append(f"    - {d['name']}: {d['url']}")
    (out_dir / "_notices.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    L = [f"# Mississippi Permit Board agendas and minutes read ({len(board)} files)", "",
         "Air items and power-like lines. The board hears only larger or contested items.", ""]
    for d in sorted(board, key=lambda d: d["date"] or d["year"], reverse=True):
        if not d["items"] and not d["power_lines"]:
            continue
        L.append(f"- {d['kind']} {d['date'] or d['year']} ({d['state']}): {d['url']}")
        for it in d["items"]:
            L.append(f"    - air item: {it['facility'] or '(no facility line)'} {', '.join(it['permits'])}: {it['text'][:240]}")
        for ln in d["power_lines"]:
            L.append(f"    - line: {ln[:200]}")
    (out_dir / "_board.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    L = [f"# Mississippi air actions of power-like facilities since {args.since}", ""]
    for f in sorted(power, key=lambda f: f["name"]):
        for a in sorted(f["activity"], key=lambda a: a["date"]):
            L.append(f"- {a['date']}: {f['name']} ({f['ai']}), {f['county']} County: {a['text']}")
    (out_dir / "_activity.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    # data behind the summary: no full document text, no staff names
    def slim(f):
        return {"ai": f["ai"], "name": f["name"], "city": f["city"], "county": f["county"],
                "sic_power": f["sic_power"], "permits": f["permits"],
                "address": (f.get("page") or {}).get("address", ""),
                "active_permits": (f.get("page") or {}).get("active_permits", []),
                "applications": (f.get("page") or {}).get("applications", []),
                "activity": f["activity"],
                "notices": [{**r, "seen": sorted(r.get("seen", []))} for r in f["notices"]],
                "docs": f["docs"], "board": f["board"]}
    (hv_dir / "facilities.json").write_text(json.dumps({
        "harvested": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "matches": {p["id"]: {"name": p["name"], "facilities": [{"ai": f["ai"], "name": f["name"], "how": how}
                                                                  for f, how in matches[p["id"]]]} for p in plants},
        "unmatched": [slim(f) for f in unmatched],
        "matched": [slim(f) for f in power if f["ai"] in matched_ids]}, indent=1), encoding="utf-8")
    (hv_dir / "notices.json").write_text(json.dumps(
        [{**r, "seen": sorted(r.get("seen", []))} for r in notices], indent=1), encoding="utf-8")
    (hv_dir / "board_items.json").write_text(json.dumps(
        [{k: v for k, v in d.items()} for d in board], indent=1), encoding="utf-8")
    (hv_dir / "activity_air.json").write_text(json.dumps(
        [a for a in activity if air_sentence(a)], indent=0), encoding="utf-8")

    S = [f"# Mississippi air permit harvest, {time.strftime('%Y-%m-%d')}", "",
         f"Facilities with an air permit or air action: {len(facs)}. Power-like: {len(power)}. "
         f"Matched to GEM plants: {len(matched_ids)}. Unmatched: {len(unmatched)}.", "",
         f"Activity search since {args.since}: {len(activity)} actions ({len([a for a in activity if air_sentence(a)])} air). "
         f"Public notice records: {len(notices)}. Permit Board files read: {len(board)}.", "",
         "## Matches per GEM plant", ""]
    for p in plants:
        ms = matches[p["id"]]
        S.append(f"- {p['name']} ({p['id']}): " + ("; ".join(f"{f['name']} ({f['ai']}, {how})" for f, how in ms)
                                                   if ms else "no facility matched"))
    S += ["", "## Unmatched power-like facilities", ""]
    for f in sorted(unmatched, key=lambda f: (not f["sic_power"], f["name"])):
        S.append(f"- {f['name']} ({f['ai']}), {f['city']}, {f['county']} County" + (", power SIC code" if f["sic_power"] else ""))
    (hv_dir / "harvest_summary.md").write_text("\n".join(S) + "\n", encoding="utf-8")
    log("done")


if __name__ == "__main__":
    main()

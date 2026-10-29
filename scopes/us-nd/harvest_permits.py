"""
Harvest North Dakota air permits before a research sweep.

The North Dakota Department of Environmental Quality (DEQ) Division of Air
Quality posts its permits in four places. All four load without a login. What
was found (2026-10-29):

  1. The public comment page, deq.nd.gov/AQ/PublicCom.aspx. One block per
     facility (an anchor such as #BasinElectricBison) with the company and
     facility name, what it makes, the county, the permit type, the comment
     dates and the documents: the cover letter and notice, the draft permit and
     the air quality effects memo, all PDFs under AQ/Notices/<Folder>/, plus a
     link to the application documents in CERIS (item 4). A notice comes down
     when its comment period ends, so the archive's saved copies of the page
     are read too.
  2. The notice PDFs themselves. The AQ/Notices/ folder listing answers 403, so
     the Wayback Machine index (CDX, prefix match) lists every PDF it saved
     under deq.nd.gov/AQ/Notices/ and the older ndhealth.gov/AQ/Notices/: about
     290 files in about 100 facility folders, from 2016 on. Each is read from
     its live address, else from its raw saved copy. The index answers 429 or a
     "Temporarily Offline" page when pressed, so calls are paced and retried.
  3. The DEQ public notice list (deq.nd.gov/publicnotice.aspx) and its feed
     (PublicNoticesRSSFeed.aspx). Every division posts there; the air items
     link back to an anchor on the public comment page, and the list keeps
     items (such as the Bison permit issuance, ID 3962) after the comment
     page drops them.
  4. CERIS-ND (ceris.deq.nd.gov), the DEQ's site and permit system. Its
     services answer anonymously when the request carries the map page as
     Referer (without it: 400 "Value cannot be null"). The site search
     (POST ss/explorersites with a search term and the state's bounding box)
     returns sites with their coordinates; air sites end in "AQ". For each
     power-like or matched air site the profile tabs give the address and
     county, the SIC and NAICS codes, every permit (number, kind, status,
     effective and expiry dates) and every document with an anonymous PDF link
     (ext/ncore/downloadpdf/<id>). The public notice list
     (ext/ncore/ss/publicnoticeslist) is read too; on 2026-10-29 it held only
     solid waste notices. CERIS rows carry staff names and phone numbers;
     none of those fields are kept.

Steps:
  1. Read the public comment page, now and in every saved copy.
  2. List the saved notice PDFs (both prefixes) and group them by folder.
  3. Read the DEQ notice list and feed; keep the air items.
  4. Search CERIS for each owner, plant name and power word; keep air sites.
  5. Keep facilities that look like power plants or data centers, match each
     GEM North Dakota plant to them (KNOWN holds hand-checked patterns; OWNER
     marks a site of the right company whose plant must still be checked; a
     name word match adds more, marked for checking) and list the rest as
     possible new plants.
  6. Read the documents of every matched or power-like facility through
     fetch.py (disk cache in work/fetch_cache/, so url_verifier.py reads them
     at once) and keep the lines that give the permit number, project,
     equipment, maker, model, sizes and location.

Output, in scopes/us-nd/work/permits/ (what the sweep agents read): one
plain-text index per plant (<GEM location id>.md), _unmatched.md, _notices.md,
index.json and harvest_log.jsonl. A summary and the data behind it go to
batches/<scope>/harvest/ (harvest_summary.md, facilities.json, the file
data_center_fleets.py reads). Permit PDFs name agency and company staff with
their contact details: the PDFs and their full text stay under work/ (never
committed). Nothing here stages a record.

Usage (from the repo root):
    python scopes/us-nd/harvest_permits.py --scope us-nd                  # every plant
    python scopes/us-nd/harvest_permits.py --scope us-nd --plants L100001047848
    python scopes/us-nd/harvest_permits.py --scope us-nd --match-only     # list matches, download no documents
    python scopes/us-nd/harvest_permits.py --scope us-nd --no-wayback     # current notices only
"""
import argparse
import html
import json
import re
import sys
import time
import urllib.parse
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from fetch import CHROME_UA  # noqa: E402
from harvest_lib import CDX, CSV, REPO, SIZE, clean, get, harvest_out, norm_county, pick, wayback_url  # noqa: E402

AQ = "https://deq.nd.gov/AQ"
PUBLICCOM = f"{AQ}/PublicCom.aspx"
NOTICE_LIST = "https://deq.nd.gov/publicnotice.aspx"
RSS = "https://deq.nd.gov/PublicNoticesRSSFeed.aspx"
CDX_PREFIXES = ["deq.nd.gov/AQ/Notices/", "ndhealth.gov/AQ/Notices/"]
CERIS = "https://ceris.deq.nd.gov/ext"
CERIS_REFERER = f"{CERIS}/nsite/DEFAULT/map/results"
CERIS_SEARCH = f"{CERIS}/nsite/ss/explorersites"
CERIS_TABS = f"{CERIS}/nsite/ss/api/nsite-explorer/default-mode/profiles"
CERIS_NOTICES = f"{CERIS}/ncore/ss/publicnoticeslist"
CERIS_DETAIL = f"{CERIS}/nsite/DEFAULT/map/results/detail/{{sid}}/detail"

# CERIS site searches: owners, plant names and words a power or data center site carries.
CERIS_TERMS = ["Basin Electric", "Montana-Dakota", "Minnkota", "Otter Tail", "Northern States Power", "Xcel",
               "Great River Energy", "Rainbow Energy", "NextEra", "Applied Digital", "APLD", "Polaris Forge",
               "Nakota", "Base Electron", "Pioneer Generation", "Lonesome Creek", "Heskett", "Spiritwood",
               "Bison", "River Run", "Generation Station", "Generating Station", "Power", "Energy Center",
               "Data Center", "Cogeneration"]

# Hand-checked patterns (2026-10-29): GEM plant -> regexes that must hit fac_text(), which
# joins a facility's name, its notice folder (as "folder:<name>"), city, county and what it
# makes. A plant missing here is matched by its name words, and those matches are marked
# for checking.
KNOWN = {
    "L100000104092": [r"heskett"],
    "L100000104096": [r"spiritwood (station|energy|gener|power)", r"great river.*spiritwood"],
    "L100000401740": [r"lonesome creek", r"folder:lonesome\b"],
    "L100000401741": [r"pioneer (gener|station|plant|power)", r"basin electric.*pioneer", r"folder:basin\b"],
    "L100000407864": [r"xcel.*fargo", r"northern states power.*(fargo|cass)"],
    "L100001047848": [r"basin ?electric ?bison", r"bison generat", r"folder:basinelectricbison\b"],
    "L100001080387": [r"river run"],
    "L100001083334": [r"polaris forge (1|one)\b", r"applied ?digital.*(ellendale|dickey)", r"folder:eln\b"],
    "L100001089074": [r"applied ?digital.*(ellendale|dickey)", r"folder:eln\b", r"polaris forge (1|one)\b"],
    "L100001083335": [r"polaris forge (2|two)\b", r"applied ?digital.*(harwood|cass)"],
    "L100001089073": [r"applied ?digital.*(harwood|cass)", r"polaris forge (2|two)\b"],
    "L100001084854": [r"nakota"],
    "L100001089055": [r"base electron", r"\bbis-?0?1\b", r"apld.*(center|oliver)"],
}
# A site of the plant's company whose own plant the text does not settle: kept, marked for checking.
OWNER = {
    "L100001083334": [r"applied ?digital|\bapld\b"],
    "L100001089074": [r"applied ?digital|\bapld\b"],
    "L100001083335": [r"applied ?digital|\bapld\b"],
    "L100001089073": [r"applied ?digital|\bapld\b"],
    "L100001089055": [r"applied ?digital|\bapld\b"],
}

POWER_NAME = re.compile(
    r"power|electric|generat|energy|turbine|cogen|steam|utilit|data ?cent|datacent|compute|bitcoin|crypto|"
    r"hyperscal|basin|minnkota|otter ?tail|montana-dakota|\bmdu\b|xcel|northern states|great river|rainbow|"
    r"nakota|polaris|applied ?digital|\bapld\b|base electron|heskett|spiritwood|lonesome|pioneer|bison|"
    r"river run|coal creek|antelope valley|leland olds|coyote|milton r|young station|combined cycle|peaking", re.I)
POWER_DROP = re.compile(
    r"compressor|gas plant|gas processing|processing plant|well\b|wells\b|\bpad\b|battery|tank|saltwater|disposal|"
    r"pipeline|pipe line|gathering|elevator|grain|feed|ethanol|biodiesel|soybean|oilseed|crush|refinery|"
    r"landfill|asphalt|concrete|ready mix|gravel|sand|quarry|lumber|wood|window|door|fiberglass|composite|"
    r"manufactur|foundry|iron|steel|fertilizer|nitrogen|ammonia|urea|sugar|potato|malt|bakery|hospital|"
    r"school|university|college|crematory|terminal|rail|truck|lignite mine|coal mine\b|mine\b", re.I)
POWER_CODES = re.compile(r"\((4911|4931|4932|4939|4961|7374|2211\d\d|518210)\)")
NAME_NOISE = re.compile(
    r"\b(power station|power plant|generating station|generating|generation|facility|station|energy center|"
    r"energy|plant|power|nd|north dakota|the|municipal|of|and|city|llc|inc|company|co|corp|"
    r"corporation|combined|cycle|county|industrial|park|campus|data|center|aq)\b", re.I)
EQUIPMENT = re.compile(r"turbine|\bct\b|engine|rice\b|generat|\bgen\b|boiler|duct burner|hrsg|"
                       r"combined cycle|simple cycle|peaking|diesel|reciprocating|genset", re.I)
MAKER = re.compile(r"model\b|caterpillar|cat g|wartsila|w[äa]rtsil[äa]|jenbacher|"
                   r"general electric|\bGE\b|siemens|solar turbines|mitsubishi|cummins|rolls[- ]royce|"
                   r"mtu\b|kohler|generac|waukesha|pratt|ansaldo|baker hughes|"
                   r"hitachi|titan \d|taurus|mars \d|lm ?\d{4}|7ea|7fa|7ha|6b\b|f-?class|h-?class", re.I)
LOCATION = re.compile(
    r"latitude|longitude|\blat\b|\blong\b|\bUTM\b|\bsection \d+|township|\bT\d{2,3}N\b|\bR\d{2,3}W\b|"
    r"located (at|in|on|near|approximately)|physical address|site address|facility address|"
    r"street address|\b\d{2,5} [A-Z0-9][\w. ]+ (road|rd|street|st|avenue|ave|"
    r"highway|hwy|drive|dr|lane|ln|blvd|boulevard)\b|county,? north dakota|nd 58\d{3}|north dakota 58\d{3}",
    re.I)
PROJECT = re.compile(r"proposes|propose to|will consist|project (is|will|consists)|construction of|"
                     r"to construct|new (electric|power|generat)|install(ation)? of", re.I)
LATLON = re.compile(r"\b(4[5-8]\.\d{3,}|49\.0\d*)\s*[,;/ ]\s*-?\s*(9[6-9]\.\d{3,}|10[0-4]\.\d{3,})\b")
PERMIT_NO = re.compile(r"\b(?:ACP|AOP|PTC|PTO|T5|AOT)-?\s?\d{4,6}(?:\s?v\d+(?:\.\d+)?)?\b", re.I)
MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"


def log(msg):
    print(f"[harvest-nd] {msg}", file=sys.stderr, flush=True)


def words(text):
    t = NAME_NOISE.sub(" ", re.sub(r"\(.*?\)", " ", str(text or "")))
    return {w.lower() for w in re.split(r"[^A-Za-z]+", t) if len(w) >= 4}


def long_date(s):
    """'October 27, 2026' or 'Monday, December 29, 2025' to 2026-10-27, or ''."""
    m = re.search(rf"\b({MONTHS})\s+(\d{{1,2}}),?\s+(20\d\d)", s or "")
    return f"{m.group(3)}-{MONTHS.split('|').index(m.group(1)) + 1:02d}-{int(m.group(2)):02d}" if m else ""


def file_date(name):
    """The yyyymmdd a notice file name often starts with, as yyyy-mm-dd, or ''."""
    m = re.search(r"(20\d\d)([01]\d)([0-3]\d)", name or "")
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else ""


def folder_of(url):
    m = re.search(r"/notices/([^/]+)/", url or "", re.I)
    return urllib.parse.unquote(m.group(1)) if m else ""


def notice_url(href):
    """A public comment page link as a full, quoted address under AQ/."""
    href = html.unescape(href.strip())
    if href.lower().startswith("http"):
        return href
    return f"{AQ}/" + urllib.parse.quote(href.lstrip("/"), safe="/#?=&")


# ------------------------------------------------------- public comment page ---

def parse_publiccom(text):
    """One record per facility block: anchor, folder, company and facility, what it makes,
    county, permit type, comment dates and documents."""
    out = []
    for m in re.finditer(r'<div class="sectionGray" id="([^"]+)"(.*?)(?=<div class="sectionGray"|<!--end|\Z)', text or "", re.S):
        anchor, body = m.group(1), m.group(2)
        h3 = clean((re.search(r"<h3>(.*?)</h3>", body, re.S) or [0, ""])[1])
        h4 = [clean(x) for x in re.findall(r"<h4>(.*?)</h4>", body, re.S)]
        county = next((x for x in h4 if re.search(r"\bcounty\b", x, re.I)), "")
        what = next((x for x in h4 if x != county), "")
        fields = {clean(k).rstrip(":"): clean(v) for k, v in re.findall(r"<li><b>(.*?)</b>(.*?)</li>", body, re.S)}
        docs = []
        for h, t in re.findall(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>', body, re.S):
            url = notice_url(h)
            docs.append({"name": clean(t), "url": url, "date": file_date(h),
                         "kind": "ceris" if "ceris.deq.nd.gov" in url else "notice"})
        folder = next((folder_of(d["url"]) for d in docs if folder_of(d["url"])), "")
        out.append({"anchor": anchor, "folder": folder, "name": h3, "what": what,
                    "county": re.sub(r"\s*county\s*$", "", county, flags=re.I).strip(),
                    "permit_type": fields.get("Permit Type", ""),
                    "begins": long_date(fields.get("Public Comment Period Begins", "")),
                    "ends": long_date(fields.get("Public Comment Period Ends", "")),
                    "docs": docs,
                    "ceris_sites": sorted({s for d in docs for s in re.findall(r"/detail/(-?\d+)/", d["url"])})})
    return out


# ------------------------------------------------------------ Wayback index ---

def cdx_query(params, tries=5, pause=2.0):
    """Rows of a Wayback index query (header row dropped), retried with backoff on 429, 503,
    504 and the archive's "Temporarily Offline" page. None when every try failed."""
    for i in range(tries):
        try:
            r = requests.get(CDX, params={"output": "json", **params}, timeout=180)
            if r.status_code in (429, 503, 504) or "Temporarily Offline" in r.text[:2000]:
                raise ValueError(f"HTTP {r.status_code}")
            rows = r.json()
            time.sleep(pause)
            return rows[1:] if rows else []
        except (requests.RequestException, ValueError) as e:
            log(f"  Wayback index busy ({e}); waiting")
            time.sleep(15 * (i + 1))
    return None


def cdx_notice_files(rows):
    """{folder (lower case): [file]} from index rows [timestamp, original, status, mime]. One
    entry per file (newest saved copy), live address rewritten under deq.nd.gov/AQ/Notices/.
    The RuleRevisions folder is rules, not facilities, and is skipped."""
    files = {}
    for ts, orig, *_ in rows:
        folder = folder_of(orig)
        if not folder or folder.lower() == "rulerevisions":
            continue
        name = orig.rsplit("/", 1)[-1]
        if not name.lower().endswith(".pdf"):
            continue
        key = (folder.lower(), urllib.parse.unquote(name).lower())
        live = f"{AQ}/Notices/{folder}/{name}"
        cur = files.get(key)
        if cur is None or ts > cur["ts"]:
            files[key] = {"folder": folder, "name": urllib.parse.unquote(name), "url": live, "ts": ts,
                          "archive": f"https://web.archive.org/web/{ts}id_/{orig}",
                          "date": file_date(name) or f"{ts[:4]}-{ts[4:6]}-{ts[6:8]}"}
    out = {}
    for (folder, _), f in sorted(files.items()):
        out.setdefault(folder, []).append(f)
    return out


def saved_notice_files():
    rows = []
    for prefix in CDX_PREFIXES:
        got = cdx_query({"url": prefix, "matchType": "prefix", "filter": "statuscode:200",
                         "fl": "timestamp,original,statuscode,mimetype", "limit": 20000})
        log(f"Wayback index {prefix}: {'no answer' if got is None else len(got)} rows")
        rows += got or []
    return cdx_notice_files(rows)


def publiccom_snapshots(wayback=True, limit=0):
    """Records from the live public comment page and every distinct saved copy of it."""
    recs = []
    live = get(PUBLICCOM)
    if live.status == "200":
        recs += [{**r, "seen": "now"} for r in parse_publiccom(live.text)]
    else:
        log(f"public comment page: HTTP {live.status}")
    n = 0
    if wayback:
        snaps = []
        for u in ("deq.nd.gov/AQ/PublicCom.aspx", "deq.nd.gov/aq/PublicCom.aspx", "www.ndhealth.gov/AQ/PublicCom.aspx"):
            got = cdx_query({"url": u, "fl": "timestamp,original", "filter": "statuscode:200", "collapse": "digest"})
            snaps += got or []
        snaps = sorted({ts: orig for ts, orig in snaps}.items())
        if limit:
            snaps = snaps[-limit:]
        for ts, orig in snaps:
            p = get(f"https://web.archive.org/web/{ts}id_/{orig}", timeout=180)
            time.sleep(1)
            if p.status != "200":
                log(f"  snapshot {ts}: HTTP {p.status}")
                continue
            n += 1
            recs += [{**r, "seen": ts[:8]} for r in parse_publiccom(p.text)]
        log(f"Wayback: {n} saved copies of the public comment page read")
    return recs, n


def merge_publiccom(recs):
    """One record per (folder or anchor, permit type, comment end); dates seen are unioned."""
    out = {}
    for r in recs:
        key = ((r["folder"] or r["anchor"]).lower(), r["permit_type"], r["ends"])
        m = out.setdefault(key, {**r, "seen": set(), "docs": []})
        if r.get("seen"):
            m["seen"].add(r["seen"])
        for d in r["docs"]:
            if d["url"] not in {x["url"] for x in m["docs"]}:
                m["docs"].append(d)
    return list(out.values())


# ------------------------------------------------------- DEQ notice list ---

NOTICE_ROW = re.compile(r"<li><a class=menulist[^>]*href=\"([^\"]+)\"[^>]*>(.*?)<span[^>]*> \(ID=(\d+)\)</span></a><br>\s*Posted: ([^<]+)", re.S)


def parse_notice_list(text):
    out = []
    for h, title, nid, posted in NOTICE_ROW.findall(text or ""):
        url = h if h.startswith("http") else "https://deq.nd.gov" + h
        out.append({"id": int(nid), "title": clean(title), "url": html.unescape(url),
                    "posted": long_date(posted), "anchor": url.split("#", 1)[1] if "#" in url else ""})
    return out


def parse_rss(text):
    out = []
    for item in re.findall(r"<item>(.*?)</item>", (text or "").lstrip("﻿"), re.S):
        def tag(t):
            m = re.search(rf"<{t}[^>]*>(.*?)</{t}>", item, re.S)
            return html.unescape(m.group(1)).strip() if m else ""
        guid = tag("guid")
        out.append({"id": int(guid.rsplit("#", 1)[1]) if "#" in guid else None, "title": clean(tag("title")),
                    "url": tag("link"), "posted": tag("pubDate"),
                    "anchor": tag("link").split("#", 1)[1] if "#" in tag("link") else ""})
    return out


def is_air_notice(n):
    return bool(re.search(r"/aq/", n["url"], re.I) or re.search(r"air pollution|air quality|\bPSD\b|title v", n["title"], re.I))


# ------------------------------------------------------------------- CERIS ---

# Fields of the CERIS notice list worth keeping. The rest name staff (assigned user, phone,
# contact names) and are dropped.
CERIS_NOTICE_KEEP = ["siteId", "siteName", "siteProfileUrl", "city", "countyDescription", "programAreaDescription",
                     "permitNumber", "publicNotificationTypeDescription", "comments", "startDate", "endDate",
                     "latitude", "longitude"]
TAB_ROUTES = {"details": "1-profile/0-site-details", "codes": "1-profile/1-sic-and-naics",
              "permits": "2-environmental-interests/1-permits", "documents": "4-documents/1-documents"}


class Ceris:
    """Anonymous CERIS-ND calls: the services answer when the map page is the Referer."""

    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": CHROME_UA, "Referer": CERIS_REFERER, "Accept": "application/json"})
        self.errors = []

    def _call(self, method, url, **kw):
        last = ""
        for i in range(3):
            try:
                r = self.s.request(method, url, timeout=90, **kw)
                if r.status_code == 200:
                    time.sleep(0.5)
                    return r.json()
                last = f"HTTP {r.status_code}"
            except (requests.RequestException, ValueError) as e:
                last = str(e)[:120]
            time.sleep(4 * (i + 1))
        self.errors.append(f"{url.split('?')[0]}: {last}")
        return None

    def notices(self):
        d = self._call("GET", CERIS_NOTICES)
        return None if d is None else slim_ceris_notices(d.get("queryResults") or [])

    def search(self, term):
        body = {"insertUpdateList": [{"displayHeight": 900, "displayWidth": 1400, "filterValuesJson": None,
                                      "isIncludeUnmappable": True, "latitudeMax": "49.1", "latitudeMin": "45.8",
                                      "longitudeMax": "-96.4", "longitudeMin": "-104.2", "modeId": "DEFAULT",
                                      "searchTerm": term, "responseContentType": "application/json",
                                      "filterString": ""}]}
        d = self._call("POST", CERIS_SEARCH, json=body)
        return None if d is None else ceris_sites(d)

    def tab(self, sid, name):
        q = urllib.parse.quote(json.dumps({"filter": [{"id": str(sid)}]}))
        url = (f"{CERIS_TABS}/{TAB_ROUTES[name]}?responseContentType=application/json"
               f"&includeMetadataInResponse=true&loadChildren=true&queryParams={q}&filterString=")
        d = self._call("GET", url)
        return None if d is None else (d.get("queryResults") or [])

    def profile(self, sid):
        tabs = {k: self.tab(sid, k) for k in TAB_ROUTES}
        return ceris_profile(tabs)


def slim_ceris_notices(rows):
    return [{k: r.get(k) for k in CERIS_NOTICE_KEEP} for r in rows]


def ceris_sites(resp):
    """Sites (not map clusters) of a search answer: id, name, city, address, zip, coordinates."""
    out = []
    for r in resp.get("insertUpdateList") or []:
        if not r.get("siteId") or not r.get("siteName"):
            continue
        m = re.match(r"POINT\((-?[\d.]+) (-?[\d.]+)\)", r.get("geographyWKT") or "")
        out.append({"site_id": str(r["siteId"]), "name": r["siteName"].strip(), "city": r.get("city") or "",
                    "address": r.get("siteAddress") or "", "zip": r.get("zip") or "",
                    "lat": float(m.group(2)) if m else None, "lon": float(m.group(1)) if m else None})
    return out


def is_air_site(name):
    return bool(re.search(r"-\s*AQ\s*$", name or ""))


def ceris_profile(tabs):
    """What the harvest keeps of a site's profile tabs: no contacts, document file names only."""
    det = (tabs.get("details") or [{}])[0] or {}
    codes = (tabs.get("codes") or [{}])[0] or {}
    permits = [{"number": p.get("prmtPrmtNum"), "type": p.get("prmtRefPrmtCatgDescr") or "",
                "kind": p.get("prmtPrmtTypeDescr") or "", "status": p.get("prmtRefPrmtStatDescr") or "",
                "effective": (p.get("prmtEfctvDate") or "")[:10], "expires": (p.get("prmtExprDate") or "")[:10]}
               for p in tabs.get("permits") or []]
    docs = []
    for d in tabs.get("documents") or []:
        if not d.get("docMgmtDocurl"):
            continue
        name = re.split(r"[\\/]", d.get("docMgmtDocName") or "")[-1]
        docs.append({"name": " ".join(x for x in (d.get("docMgmtDocDescr") or "", f"({name})" if name else "") if x),
                     "url": d["docMgmtDocurl"], "date": (d.get("docMgmtDocRvcdCreatedDate") or "")[:10],
                     "category": d.get("docMgmtCategory") or "", "program": d.get("docMgmtSourceprogramarea") or "",
                     "kind": "ceris"})
    return {"address": det.get("siteAddr") or "", "county": det.get("siteCnty") or "",
            "site_types": det.get("siteSiteTypes") or "",
            "codes": [c for c in (codes.get("siteSicCodes"), codes.get("siteNaicsCodes")) if c],
            "permits": permits, "docs": docs, "loaded": {k: v is not None for k, v in tabs.items()}}


def rank_ceris_docs(docs):
    """Air permit documents first (permits, applications, notices, memos), newest first."""
    def score(d):
        t = f"{d['name']} {d['category']}"
        s = 0 if re.search(r"air", d.get("program", ""), re.I) or d.get("program") in ("", "n/a") else 2
        s += 0 if re.search(r"permit|application|notice|memo|analysis|technical|review", t, re.I) else 1
        return (s, "".join(chr(255 - ord(c)) for c in d.get("date", "")))
    return sorted(docs, key=score)


# ------------------------------------------------------------- facilities ---

def new_fac(key, name, source):
    return {"key": key, "name": name, "source": source, "folder": "", "anchor": "", "city": "", "county": "",
            "what": "", "address": "", "lat": None, "lon": None, "codes": [], "permits": [],
            "notices": [], "list_items": [], "saved_files": [], "ceris_ids": [], "docs": []}


def build_facilities(publiccom, saved, sites):
    """{key: facility}: one per notice folder (or anchor) and one per CERIS air site. A CERIS
    site that a notice links to is folded into that notice's facility."""
    facs = {}
    for r in publiccom:
        key = "aq:" + (r["folder"] or r["anchor"]).lower()
        f = facs.setdefault(key, new_fac(key, r["name"], "DEQ air quality notice"))
        f["name"] = f["name"] or r["name"]
        f["folder"] = f["folder"] or r["folder"]
        f["anchor"] = f["anchor"] or r["anchor"]
        f["county"] = f["county"] or r["county"]
        f["what"] = f["what"] or r["what"]
        f["notices"].append(r)
        for sid in r["ceris_sites"]:
            if sid not in f["ceris_ids"]:
                f["ceris_ids"].append(sid)
    for folder, files in saved.items():
        key = "aq:" + folder
        f = facs.setdefault(key, new_fac(key, "", "DEQ air quality notice"))
        f["folder"] = f["folder"] or files[0]["folder"]
        f["saved_files"] = files
    by_site = {sid: f for f in facs.values() for sid in f["ceris_ids"]}
    for s in sites:
        f = by_site.get(s["site_id"])
        if f is None:
            key = "ceris:" + s["site_id"]
            f = facs.setdefault(key, new_fac(key, s["name"], "CERIS site"))
            f["ceris_ids"] = [s["site_id"]]
        f["name"] = f["name"] or s["name"]
        f["city"] = f["city"] or s["city"]
        f["address"] = f["address"] or s["address"]
        if f["lat"] is None and s["lat"] is not None:
            f["lat"], f["lon"] = s["lat"], s["lon"]
    for f in facs.values():
        if not f["name"]:
            f["name"] = f"Air Quality notice folder {f['folder']}"
    return facs


def attach_list_items(facs, items):
    """Hang each air item of the DEQ notice list on the facility whose page anchor it links to."""
    by_anchor = {f["anchor"].lower(): f for f in facs.values() if f["anchor"]}
    by_folder = {f["folder"].lower(): f for f in facs.values() if f["folder"]}
    loose = []
    for n in items:
        a = n["anchor"].lower()
        f = by_anchor.get(a) or by_folder.get(a)
        if f is not None:
            if n["id"] not in {x["id"] for x in f["list_items"]}:
                f["list_items"].append(n)
        else:
            loose.append(n)
    return loose


def fac_text(f):
    return " | ".join(x for x in (f["name"], f"folder:{f['folder'].lower()}" if f["folder"] else "",
                                  f["city"], f["county"], f["what"], f["address"]) if x).lower()


def is_power(f):
    """A facility looks like a power or data center site: a power or data processing code, or
    a power-like name, company or folder that is not on the drop list."""
    if any(POWER_CODES.search(c) for c in f.get("codes", [])):
        return True
    text = f"{f['name']} {f['folder']} {f['what']}"
    if POWER_DROP.search(f"{f['name']} {f['what']}"):
        return False
    return bool(POWER_NAME.search(text))


def match(plant, facs):
    """[(facility, how)]: hand-checked patterns, else the plant's company for an owner pattern,
    else every distinctive word of the plant's name, or its city plus a power-like name."""
    out = []
    pats = KNOWN.get(plant["id"])
    owner = OWNER.get(plant["id"], [])
    for f in facs:
        t = fac_text(f)
        if pats and any(re.search(p, t) for p in pats):
            out.append((f, "checked by hand"))
        elif owner and any(re.search(p, t) for p in owner):
            out.append((f, "the plant's company, check which site this is"))
    if pats:
        return out
    ws = plant["name_words"]
    city = plant["city"].lower()
    for f in facs:
        if f in [x for x, _ in out]:
            continue
        t = fac_text(f)
        if ws and ws <= words(t):
            out.append((f, "name match, check it is this plant"))
        elif city and city == f["city"].lower() and is_power(f):
            out.append((f, "same city, power-like name, check it is this plant"))
    return out


def doc_facts(text):
    latlon = [f"{a}, -{b.lstrip('-')}" for a, b in LATLON.findall(text)][:3]
    return {
        "ids": sorted({re.sub(r"\s+", "", x).upper() for x in PERMIT_NO.findall(text)})[:6],
        "project": pick(text, PROJECT, 6),
        "equipment": pick(text, EQUIPMENT, 10),
        "makers": pick(text, MAKER, 8),
        "sizes": pick(text, SIZE, 10),
        "location": pick(text, LOCATION, 8),
        "coords": latlon,
    }


def fac_docs(f):
    """Every document of a facility, newest notice first: the notice PDFs (live address,
    saved copy as a fallback) and the CERIS documents."""
    docs, seen = [], set()

    def add(d):
        if d["url"] not in seen:
            seen.add(d["url"])
            docs.append(d)
    for r in sorted(f["notices"], key=lambda r: r["ends"] or "", reverse=True):
        for d in r["docs"]:
            if d["kind"] == "notice":
                add({**d, "name": f"{d['name']} ({r['permit_type'] or 'notice'}, comments end {r['ends'] or 'not shown'})"})
    for s in sorted(f["saved_files"], key=lambda s: s["date"], reverse=True):
        add({"name": s["name"], "url": s["url"], "date": s["date"], "archive": s["archive"], "kind": "notice"})
    for d in rank_ceris_docs(f.get("ceris_docs", [])):
        add(d)
    return docs


def read_docs(docs, cap=10, wayback=True):
    """Download a facility's documents and keep facts. Each doc is {name, url[, archive]}."""
    for n, d in enumerate(docs):
        if n >= cap:
            d["state"] = "not read (cap)"
            continue
        page = get(d["url"], timeout=300)
        ok = page.status == "200" and bool(page.text.strip())
        via = ""
        if not ok and wayback:
            snap = d.get("archive") or wayback_url(d["url"])
            if snap:
                page = get(snap, timeout=300)
                if page.status == "200" and page.text.strip():
                    ok, via = True, f" (from the Wayback copy {snap})"
                    d["archive"] = snap
        d["state"] = f"saved{via}" if ok else f"not saved, HTTP {page.status}"
        d["facts"] = doc_facts(page.text) if ok else {}


# ---------------------------------------------------------------- reporting ---

def fac_block(f, how=None):
    where = ", ".join(x for x in (f["city"], f"{f['county']} County" if f["county"] else "") if x)
    ids = [f"notice folder {f['folder']}" if f["folder"] else "",
           "CERIS site " + ", ".join(f["ceris_ids"]) if f["ceris_ids"] else ""]
    L = [f"- {f['name']} ({'; '.join(x for x in ids if x) or f['source']})" + (f": {where}" if where else "")]
    if f["what"]:
        L.append(f"    - what it makes: {f['what']}")
    if f["address"]:
        L.append(f"    - where: {f['address']}")
    if f["lat"] is not None:
        L.append(f"    - CERIS map point: {f['lat']}, {f['lon']} (https://www.google.com/maps?q={f['lat']},{f['lon']})")
    for c in f["codes"]:
        L.append(f"    - codes: {c}")
    for sid in f["ceris_ids"]:
        L.append(f"    - CERIS site page: {CERIS_DETAIL.format(sid=sid)}")
    for p in f["permits"][:14]:
        L.append(f"    - permit: {p['number']}, {p['type']} ({p['kind']}), {p['status']}, effective {p['effective'] or 'not shown'}"
                 + (f", expires {p['expires']}" if p["expires"] else ""))
    for r in sorted(f["notices"], key=lambda r: r["ends"] or "", reverse=True):
        seen = sorted(r.get("seen") or [])
        L.append(f"    - public comment notice: {r['permit_type'] or 'type not shown'}, comments {r['begins'] or '?'} to {r['ends'] or '?'}"
                 + (f", on the page {seen[0]} to {seen[-1]}" if seen else "") + f" ({PUBLICCOM}#{r['anchor']})")
    for n in f["list_items"]:
        L.append(f"    - DEQ notice list item {n['id']}, posted {n['posted'] or 'date not shown'}: {n['title']}")
    for d in f["docs"]:
        L.append(f"    - document ({d.get('state', 'not read')}{', ' + d['date'] if d.get('date') else ''}): {d['name']}: {d['url']}")
        fa = d.get("facts") or {}
        for key, label in (("ids", "permit numbers"), ("project", "project"), ("equipment", "equipment"),
                           ("makers", "maker or model"), ("sizes", "size"),
                           ("location", "site address or location"), ("coords", "coordinates")):
            for line in fa.get(key, []):
                L.append(f"        - {label}: {line}")
    if how:
        L.insert(0, f"Matched: {how}.")
    return L


def write_index(path, plant, matched):
    L = [f"# North Dakota air permit files for {plant['name']} ({plant['id']})", "",
         "Source: North Dakota DEQ Division of Air Quality public comment page and its saved copies, the "
         "notice PDFs saved by the Wayback Machine, the DEQ public notice list, and CERIS-ND site profiles "
         "(permits and documents). Documents marked saved are in the local fetch cache, so "
         "`python scripts/fetch.py <url> --text` and `url_verifier.py` read them at once.", "",
         f"Harvested: {time.strftime('%Y-%m-%d %H:%M %Z')}", "",
         f"GEM statuses: {', '.join(plant['statuses'])}. City in GEM: {plant['city'] or 'blank'}. "
         f"County in GEM: {plant['county'] or 'blank'}.", ""]
    if not matched:
        L += ["No air permit facility matched this plant by name. That does not mean it has no permits: it "
              "may be listed under the owner, a contractor or a different site name. Check _unmatched.md "
              "and _notices.md in this folder, and search CERIS-ND by owner and county.", ""]
    for f, how in matched:
        L += fac_block(f, how) + [""]
    path.write_text("\n".join(L), encoding="utf-8")


def slim(f):
    """A facility as facilities.json and index.json keep it: no full document text."""
    return {"key": f["key"], "name": f["name"], "source": f["source"], "folder": f["folder"],
            "anchor": f["anchor"], "city": f["city"], "county": f["county"], "what": f["what"],
            "address": f["address"], "lat": f["lat"], "lon": f["lon"], "codes": f["codes"],
            "ceris_ids": f["ceris_ids"], "permits": f["permits"],
            "notices": [{k: (sorted(v) if k == "seen" else v) for k, v in r.items()} for r in f["notices"]],
            "list_items": f["list_items"],
            "docs": [{k: d[k] for k in ("name", "url", "date", "state", "archive", "facts") if k in d} for d in f["docs"]]}


# ----------------------------------------------------------------- plants ---

def load_plants(args=None, csv_path=None):
    csv = pd.read_csv(csv_path or CSV, low_memory=False, encoding="utf-8-sig")
    csv = csv[csv["State/Province"] == "North Dakota"]
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
    ap.add_argument("--scope", required=True, help="batch folder name, e.g. us-nd")
    ap.add_argument("--plants", help="comma-separated GEM location IDs (default: every plant)")
    ap.add_argument("--match-only", action="store_true", help="list matches, download no documents")
    ap.add_argument("--no-wayback", action="store_true", help="skip saved copies (page, notice PDF index, PDF fallback)")
    ap.add_argument("--snapshots", type=int, default=0, help="read only the newest N saved copies of the page (0 = all)")
    ap.add_argument("--docs-per-facility", type=int, default=10)
    args = ap.parse_args()

    out_dir = harvest_out(args.scope)
    hv_dir = REPO / "batches" / args.scope / "harvest"
    hv_dir.mkdir(parents=True, exist_ok=True)
    plants = load_plants(args)
    wayback = not args.no_wayback

    publiccom, n_snaps = publiccom_snapshots(wayback=wayback, limit=args.snapshots)
    publiccom = merge_publiccom(publiccom)
    log(f"{len(publiccom)} distinct public comment notices")
    saved = saved_notice_files() if wayback else {}
    log(f"{sum(len(v) for v in saved.values())} saved notice PDFs in {len(saved)} folders")

    notice_items, list_state = [], []
    for name, url, parse in (("DEQ public notice list", NOTICE_LIST, parse_notice_list), ("DEQ notice feed", RSS, parse_rss)):
        p = get(url)
        got = parse(p.text) if p.status == "200" else []
        list_state.append(f"{name}: HTTP {p.status}, {len(got)} items")
        for n in got:
            if n["id"] not in {x["id"] for x in notice_items}:
                notice_items.append(n)
    air_items = [n for n in notice_items if is_air_notice(n)]
    log("; ".join(list_state) + f"; {len(air_items)} air items")

    ceris = Ceris()
    ceris_notices = ceris.notices()
    sites = {}
    for term in CERIS_TERMS:
        got = ceris.search(term)
        log(f"CERIS search {term!r}: {'no answer' if got is None else len(got)} sites")
        for s in got or []:
            if is_air_site(s["name"]):
                sites.setdefault(s["site_id"], s)
    log(f"CERIS: {len(sites)} air sites")

    facs = build_facilities(publiccom, saved, list(sites.values()))
    loose = attach_list_items(facs, air_items)
    matches = {p["id"]: match(p, list(facs.values())) for p in plants}
    power = [f for f in facs.values() if is_power(f)]
    for ms in matches.values():
        for f, _ in ms:
            if f not in power:
                power.append(f)
    matched_keys = {f["key"] for ms in matches.values() for f, _ in ms}

    for k, f in enumerate(power, 1):
        for sid in f["ceris_ids"]:
            prof = ceris.profile(sid)
            f["address"] = f["address"] or prof["address"]
            f["county"] = f["county"] or prof["county"]
            f["codes"] = sorted(set(f["codes"]) | set(prof["codes"]))
            f["permits"] += [p for p in prof["permits"] if p not in f["permits"]]
            f.setdefault("ceris_docs", []).extend(prof["docs"])
        if k % 10 == 0:
            log(f"  CERIS profiles {k}/{len(power)}")
    # a profile can show a power code on a site whose name did not look like one
    unmatched = [f for f in power if f["key"] not in matched_keys and is_power(f)]
    log(f"{len(power)} power-like facilities: {len(matched_keys)} matched to GEM plants, {len(unmatched)} unmatched")

    if args.match_only:
        for p in plants:
            for f, how in matches[p["id"]] or [({"name": "no match", "key": "", "city": ""}, "")]:
                print(f"{p['id']}\t{p['name']}\t{f['name']}\t{f['key']}\t{f.get('city', '')}\t{how}")
        for f in unmatched:
            print(f"UNMATCHED\t\t{f['name']}\t{f['key']}\t{f['city']}\t{f['county']}")
        return

    for k, f in enumerate(power, 1):
        f["docs"] = fac_docs(f)
        log(f"({k}/{len(power)}) reading {min(len(f['docs']), args.docs_per_facility)} of {len(f['docs'])} documents of {f['name']}")
        read_docs(f["docs"], args.docs_per_facility, wayback=wayback)

    with (out_dir / "harvest_log.jsonl").open("a", encoding="utf-8") as logf:
        for p in plants:
            write_index(out_dir / f"{p['id']}.md", p, matches[p["id"]])
            logf.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "plant": p["id"], "name": p["name"],
                                   "facilities": [{"name": f["name"], "key": f["key"], "how": how,
                                                   "docs": {d["name"]: d.get("state", "not read") for d in f["docs"]}}
                                                  for f, how in matches[p["id"]]]}) + "\n")

    L = ["# North Dakota facilities that look like power or data center sites but match no GEM plant in this batch", "",
         "Each may be a plant outside this batch, a plant GEM lacks, a backup generator at a site that is not "
         "a power plant, or not a power plant at all. Check engines or turbines of 50 MW or more in total "
         "(generating capacity only).", ""]
    for f in sorted(unmatched, key=lambda f: f["name"].lower()):
        L += fac_block(f) + [""]
    if not unmatched:
        L.append("None this run.")
    (out_dir / "_unmatched.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    L = [f"# North Dakota air notices: the public comment page now and in saved copies ({len(publiccom)} notices)", ""]
    for r in sorted(publiccom, key=lambda r: r["ends"] or "", reverse=True):
        seen = sorted(r.get("seen") or [])
        L.append(f"- {r['name'] or r['anchor']} ({r['county']} County): {r['permit_type'] or 'type not shown'}, "
                 f"comments end {r['ends'] or 'not shown'}" + (f", on the page {seen[0]} to {seen[-1]}" if seen else ""))
        for d in r["docs"]:
            L.append(f"    - {d['name']}: {d['url']}")
    L += ["", f"## Air items of the DEQ public notice list and feed ({len(air_items)})", ""]
    L += [f"- {n['posted'] or 'date not shown'}, item {n['id']}: {n['title']} ({n['url']})" for n in air_items]
    if loose:
        L += ["", "Items above that link to no notice block on the page (read them by hand): "
              + ", ".join(str(n["id"]) for n in loose)]
    L += ["", "## CERIS-ND public notice list", ""]
    if ceris_notices is None:
        L.append("Did not load this run. Retry before concluding anything.")
    for n in ceris_notices or []:
        L.append(f"- {n['siteName']}, {n['city']}, {n['countyDescription']}: {n['programAreaDescription']}, "
                 f"{n['publicNotificationTypeDescription']} {n['permitNumber'] or ''}, {str(n['startDate'])[:10]} to "
                 f"{str(n['endDate'])[:10]} ({n['siteProfileUrl']})")
    (out_dir / "_notices.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    index = {"harvested": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
             "plants": {p["id"]: {"name": p["name"], "facilities": [{"key": f["key"], "name": f["name"], "how": how}
                                                                    for f, how in matches[p["id"]]]} for p in plants},
             "unmatched": [f["key"] for f in unmatched],
             "facilities": {f["key"]: slim(f) for f in power}}
    (out_dir / "index.json").write_text(json.dumps(index, indent=1), encoding="utf-8")
    (hv_dir / "facilities.json").write_text(json.dumps({
        "harvested": index["harvested"],
        "matches": index["plants"],
        "unmatched": [slim(f) for f in unmatched],
        "matched": [slim(f) for f in power if f["key"] in matched_keys]}, indent=1), encoding="utf-8")

    S = [f"# North Dakota air permit harvest, {time.strftime('%Y-%m-%d')}", "",
         f"Facilities seen: {len(facs)}. Power-like: {len(power)}. Matched to GEM plants: {len(matched_keys)}. "
         f"Unmatched: {len(unmatched)}.", "",
         f"Public comment notices: {len(publiccom)} (saved copies of the page read: {n_snaps}). "
         f"Saved notice PDFs: {sum(len(v) for v in saved.values())} in {len(saved)} folders. "
         f"{'; '.join(list_state)}. CERIS air sites: {len(sites)}; CERIS notices: "
         f"{'did not load' if ceris_notices is None else len(ceris_notices)}.", ""]
    if ceris.errors:
        S += ["CERIS calls that failed after three tries (retry before concluding anything):", ""]
        S += [f"- {e}" for e in ceris.errors[:40]] + [""]
    S += ["## Matches per GEM plant", ""]
    for p in plants:
        ms = matches[p["id"]]
        S.append(f"- {p['name']} ({p['id']}): " + ("; ".join(f"{f['name']} ({f['key']}, {how})" for f, how in ms)
                                                   if ms else "no facility matched"))
    S += ["", "## Unmatched power-like facilities", ""]
    S += [f"- {f['name']} ({f['key']}), {f['city'] or 'city not shown'}, {f['county'] or '?'} County" for f in
          sorted(unmatched, key=lambda f: f["name"].lower())]
    (hv_dir / "harvest_summary.md").write_text("\n".join(S) + "\n", encoding="utf-8")
    log("done")


if __name__ == "__main__":
    main()

"""Mississippi Public Service Commission dockets for new generation, IRPs and plant retirements (pre-sweep step for scope us-ms).

Finds the dockets of Entergy Mississippi, Mississippi Power, Cooperative Energy
and TVA (and any docket whose title says gas plant, turbine, combined cycle,
certificate, resource plan or retirement) from a start year on, reads the key
documents and writes the facts a plant brief needs: plant name, megawatts,
technology, turbine maker and model, in-service year, retirement years, county
and city, plus the lines of any resource-plan table that name a plant.

What was found per source (2026-10-23):

Commission document search (CTS portal), `https://ctsportal.psc.ms.gov/portal/document-search`.
This is the real search, and it holds every filing. It is an ASP.NET page with a
Cloudflare Turnstile gate, and Python `requests` fails on its certificate chain
(curl works). The ladder that works:
  1. Real Chrome (the fetch ladder's `cf_clearance` helpers) opens the search
     page. The page script passes the gate by itself and sets
     `sessionStorage.recaptcha_valid` to true after 10 to 15 seconds. Chrome's
     cookies and the rendered page are read, then Chrome is closed.
  2. The page holds a CSRF token (`X-Valence-CSRF-Token` in `$.ajaxSetup`) and a
     per-page encrypted search address (`/WidgetManagement/GenericGrid/ExecuteSearchProc2?...`).
     Both are session-bound and change on every page load.
  3. curl replays the search as a POST with those cookies, the token,
     `X-Requested-With: XMLHttpRequest` and the form fields `data.CaseYear`,
     `data.CaseType`, `data.CaseNumber`, `data.Company`, `data.Keywords` and the
     other filters (blank when unused), `page=1`, `pageSize` up to 1000. CaseYear is
     required. The answer is JSON `{"Data": [...], "Total": n}`. A bare `[]` means
     the session is not verified, so the script earns a new one.
  4. Each row is one filed document: company, docket year, type and number,
     sequence, file name, page count, date received, comments. 2022 to 2024 documents
     carry their own comments; 2025 and later name the first document "Public Case
     File" with the docket title in its comment.
  5. A document downloads with GET `/portal/Workflow/Run?workflowId=...&ewd=<Id_encrypted>`
     with the cookies and `Referer: .../portal/document-search`; without the Referer
     it redirects to the login page. The encrypted id is session-bound, so the script
     searches the docket again right before it downloads.
  Limits: the search finds a docket by the year it was opened, so a docket opened
  before the start year with new filings since is not listed (a person can search
  the portal for it). Documents that are not on the public side are not returned.

Monthly docket PDFs, `https://www.psc.ms.gov/exec-sec/dockets`. Open, stable links
to the agenda for each Commission meeting (the Utility Docket lists each docket
with number, utility, title and filing date). These are the citation for a
docket's existence, title and filing date, since portal document links need a
session. They do not hold every docket, only those on an agenda.

The old domain `www.psc.state.ms.us` is dead (status 000). The portal's own docket
pages (`/portal/PSC/DocketDetails?docketId=<guid>`) need the guid, which the document
search does not return, so they are not used.

Output (batches/us-ms/harvest/): `psc_dockets.json` and `psc_dockets.md`. Documents
and their text go to `work/psc_ms/<docket>/` (never committed; they can hold staff
contact details). `--match-only FILE` re-matches a saved psc_dockets.json with no
network; `--no-docs` lists dockets without downloading documents.
"""

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch import CHROME_UA, download, fetch_page  # noqa: E402
from ms_match import OUT, REPO, KNOWN, clean_ws, load_plants, norm_county  # noqa: E402

PORTAL = "https://ctsportal.psc.ms.gov"
SEARCH_PAGE = f"{PORTAL}/portal/document-search"
WORKFLOW = "g2de856dc-0e14-4250-9e46-9d7f635c5b1a"
DOCKET_LIST_PAGE = "https://www.psc.ms.gov/exec-sec/dockets"
WORK = REPO / "work" / "psc_ms"

COMPANIES = ["Entergy", "Mississippi Power", "Cooperative Energy", "Tennessee Valley", "TVA",
             "South Mississippi Electric"]
KEYWORDS = ["CPCN", "certificate", "turbine", "generation", "generating", "gas", "combined cycle",
            "peaking", "IRP", "resource plan", "integrated resource", "acquisition", "capacity",
            "retire", "retirement", "power plant", "natural gas", "data center", "RFP"]

TARGET_UTILITY = re.compile(r"entergy mississippi|mississippi power|cooperative energy|south mississippi electric|"
                            r"tennessee valley|\btva\b|\bsmepa\b|\bemi\b", re.I)
GEN = re.compile(r"\bCPCN\b|certificate of public convenience|convenience and necessity|generat(ion|ing|or)|"
                 r"combined[- ]cycle|turbine|peaking|gas[- ]fired|natural gas|power (plant|station)|"
                 r"integrated resource|\bIRP\b|resource plan|acquisition of|retire|reserve margin|"
                 r"mothball|deactivat|data ?center|large load|\bRFP\b|request for proposals?|battery|"
                 r"generating (station|facility)|energy center|\bunit \d", re.I)
GAS = re.compile(r"turbine|combined[- ]cycle|gas[- ]fired|natural gas|peaking|combustion|\blng\b|"
                 r"reciprocating|\bcc\b|\bct\b", re.I)
SOLAR_ONLY = re.compile(r"solar|photovoltaic|\bpv\b", re.I)
# wires, substations, rates and other utility work that share the word "certificate" but add no generation
WIRES = re.compile(r"transmission|\btrans\b|substation|\bsub\b|distribution line|power ?line|\bkv\b|feeder|"
                   r"utility facilities|electric cooperative|cert\.? of amendment|certificate of amendment|"
                   r"water|sewer|rate (case|change)|formula rate|fuel adjustment|storm|\baudit of|intrastate|pipeline|"
                   r"fiber|telecommunication|energy efficiency|net metering|pole|\binfrastructure\b", re.I)
ROUTINE = re.compile(r"rule 7\.103", re.I)
STRONG = re.compile(r"\bCPCN\b|certificate of public convenience|convenience and necessity|"
                    r"integrated resource|\bIRP\b|resource plan|acquisition|retire|mothball|deactivat|"
                    r"\bRFP\b|request for proposals?", re.I)

# Name patterns for document text, stricter than ms_match.KNOWN because a word like
# "daniel" or "watson" is common in text. A plant missing here falls back to KNOWN.
DOC_KNOWN = {
    "L100000401922": [r"baxter wilson"],
    "L100000402097": [r"plant daniel|daniel (unit|plant|generat|electric|coal)|victor j"],
    "L100000104009": [r"plant watson|jack watson|watson (unit|plant|electric|generat)"],
    "L100000104011": [r"plant morrow|morrow (plant|generat|unit)|r\.? ?d\.? morrow"],
    "L100000401923": [r"choctaw county (plant|power|generat|unit)|choctaw (plant|generat)"],
    "L100000402322": [r"magnolia (power|plant|generat|facility)"],
    "L100000401925": [r"hinds (energy|plant|generat|facility)"],
    "L100000402094": [r"chevron (cogeneration|oil|refinery|unit|plant)|plant chevron"],
    "L100000402325": [r"quantum"],
    "L100000401628": [r"southaven"],
    "L100001080981": [r"vicksburg advanced|vicksburg (power|generat|project|combined)"],
    "L100000402320": [r"kemper (county )?(energy|igcc|plant|facility|generat)"],
}
# Plants that are not GEM rows but that resource plans and dockets name; matched lines
# are listed so a person sees them. Plant Sweatt and Rex Brown are Mississippi Power or
# Cooperative Energy units the user named, plus the ones GEM tracks that are retired.
IRP_NAMES = re.compile(r"moselle|andrus|(plant )?daniel|watson|sweatt|chevron|pascagoula|baxter wilson|"
                       r"morrow|silver creek|attala|choctaw|hinds|rex brown|delta blues|traceview|"
                       r"vicksburg|magnolia|ratcliffe|kemper|batesville|crossroads|southaven|caledonia", re.I)

TECH = re.compile(r"combined[- ]cycle|combustion turbine|simple[- ]cycle|peaking|reciprocating|internal combustion|"
                  r"battery|solar|steam turbine|\bhrsg\b|duct fir", re.I)
MAKER = re.compile(r"general electric|\bGE\b|siemens|mitsubishi|solar turbines|wartsila|w[äa]rtsil[äa]|"
                   r"rolls[- ]royce|caterpillar|pratt|hitachi|ansaldo|\b7H[AF]\b|7HA|7FA|SGT[- ]?\d|"
                   r"\bM501|\bLM ?\d{4}|\b501[GJ]|\b6B\b|titan \d|model\b|manufactur", re.I)
SIZE = re.compile(r"\d[\d,.]*\s*(MW|MWe|megawatt|MWac|kW)\b", re.I)
INSERVICE = re.compile(r"in[- ]service|commercial operation|\bCOD\b|placed in service|on[- ]line|begin operat|"
                       r"construction (will|is expected)|completion", re.I)
RETIRE = re.compile(r"retire|retirement|deactivat|mothball|cease operat|shut ?down|decommission", re.I)
LOCATION = re.compile(r"located (at|in|on|near|approximately)|site (is|in|at)|county,? mississippi|"
                      r"latitude|longitude|\bacres?\b|parcel|city of|town of", re.I)
YEAR = re.compile(r"\b20[2-5]\d\b")
LATLON = re.compile(r"\b(3[0-5]\.\d{3,})\s*[,;/ ]\s*-?\s*(8[7-9]\.\d{3,}|9[0-2]\.\d{3,})\b")

DOC_PRIORITY = re.compile(r"petition|application|order|testimony|irp|resource plan|plan|notice|report|"
                          r"exhibit|attachment|public case file|supplement|motion|response", re.I)


def log(msg):
    print(f"[harvest-psc] {msg}", file=sys.stderr, flush=True)


# ------------------------------------------------------------- the search ---

def parse_search_page(html_text):
    """(csrf token, search address) from the rendered document-search page."""
    tok = re.search(r"X-Valence-CSRF-Token[^']*'([^']+)", html_text)
    url = re.search(r'"url":"(/WidgetManagement/GenericGrid/ExecuteSearchProc2[^"]+)"', html_text)
    if not tok or not url:
        raise RuntimeError("search page has no CSRF token or search address")
    return tok.group(1), url.group(1).replace("\\u0026", "&").replace("&amp;", "&")


def earn_session():
    """Real Chrome passes the page's own gate; returns a session dict, or raises."""
    import cf_clearance as cf
    with cf._browser_lock():
        proc, ver = cf._launch_chrome(cf.CDP_PORT)
        cdp = cf._CDP(ver["webSocketDebuggerUrl"])
        try:
            tid = cf._new_tab(cdp, "about:blank", cf.browser_mode())
            s = cdp.send("Target.attachToTarget", {"targetId": tid, "flatten": True})["sessionId"]
            cdp.send("Page.navigate", {"url": SEARCH_PAGE}, session=s)
            ok = False
            for _ in range(30):
                time.sleep(2)
                try:
                    v = cdp.send("Runtime.evaluate", {"expression": "sessionStorage['recaptcha_valid']",
                                                      "returnByValue": True}, session=s)["result"].get("value")
                except Exception:  # noqa: BLE001
                    v = None
                if v in ("true", True):
                    ok = True
                    break
            html_text = cf._page_html(cdp, s)
            cookies = cdp.send("Storage.getCookies").get("cookies", [])
        finally:
            cf._stop_chrome(cdp, proc)
    if not ok:
        raise RuntimeError("the search page did not pass its own gate in 60 seconds")
    token, url = parse_search_page(html_text)
    cookie = "; ".join(f"{c['name']}={c['value']}" for c in cookies if "psc.ms.gov" in c["domain"])
    return {"cookie": cookie, "token": token, "url": url, "ua": ver.get("User-Agent") or CHROME_UA}


FILTERS = "CaseYear CaseType CaseNumber Company FormType FormSubType ExactDate StartDate EndDate UtilityCode " \
          "Central South North Master Operation Comments Keywords".split()


class Portal:
    def __init__(self):
        self.session = None
        self.earned = 0

    def ensure(self, force=False):
        if self.session is None or force:
            for attempt in range(3):
                if self.earned >= 40:
                    raise RuntimeError("the portal session was lost 40 times; stopping")
                log("earning a portal session in real Chrome ...")
                self.earned += 1
                try:
                    self.session = earn_session()
                    return
                except Exception as e:  # noqa: BLE001
                    log(f"  session attempt {attempt + 1} failed: {e}")
                    time.sleep(10)
            raise RuntimeError("could not earn a portal session in three tries")

    def cached_search(self, label, **kw):
        """search() with an on-disk cache of the day's answers, so a rerun resumes."""
        path = WORK / "search_cache" / f"{dt.date.today().isoformat()}_{re.sub(r'[^A-Za-z0-9]+', '_', label)}.json"
        if path.exists():
            return json.loads(path.read_text())
        got = self.search(**kw)
        if got is not None:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(got))
        return got

    def search(self, page_size=1000, **kw):
        for attempt in range(2):
            self.ensure(force=attempt > 0)
            form = {"sort": "", "page": 1, "pageSize": page_size, "group": "", "filter": ""}
            form.update({f"data.{k}": kw.get(k, "") for k in FILTERS})
            args = []
            for k, v in form.items():
                args += ["--data-urlencode", f"{k}={v}"]
            r = subprocess.run(
                ["curl", "-s", "--max-time", "120", "-A", self.session["ua"], "-H", "Cookie: " + self.session["cookie"],
                 "-H", "X-Valence-CSRF-Token: " + self.session["token"], "-H", "X-Requested-With: XMLHttpRequest",
                 "-X", "POST", PORTAL + self.session["url"]] + args, capture_output=True, text=True)
            try:
                data = json.loads(r.stdout)
            except ValueError:
                data = []
            if isinstance(data, dict) and "Data" in data:
                return data["Data"]
        return None

    def download(self, id_encrypted, path):
        """True when a PDF was saved."""
        url = f"{PORTAL}/portal/Workflow/Run?workflowId={WORKFLOW}&ewd={id_encrypted}"
        subprocess.run(["curl", "-sL", "--max-time", "180", "-A", self.session["ua"], "-H",
                        "Cookie: " + self.session["cookie"], "-H", f"Referer: {SEARCH_PAGE}", url, "-o", str(path)],
                       capture_output=True)
        p = Path(path)
        return p.exists() and p.read_bytes()[:5] == b"%PDF-"


# ------------------------------------------------------------ the dockets ---

def seq_int(row, default=0):
    """Document sequence as a number; the portal also has labels such as 'ORDER '."""
    try:
        return int(row.get("DocSequence"))
    except (TypeError, ValueError):
        return default


def docket_key(row):
    try:
        n = int(row.get("DocNum"))
    except (TypeError, ValueError):
        n = row.get("DocNum")
    return f"{row.get('DocYear')}-{row.get('DocType')}-{n}"


TITLE_LIKE = re.compile(r"\s*(IN RE|PETITION|JOINT PETITION|APPLICATION|NOTICE|RULE 7\.103|INFORMATIONAL|CPCN|"
                        r"COMPLAINT|AUDIT|REQUEST|MOTION|AWS|.{0,40}\b(CERTIFICATE|PETITION)\b)", re.I)


def group_dockets(rows):
    """{docket key: {rows..}} from document rows (deduplicated by row id)."""
    by = {}
    for r in rows:
        d = by.setdefault(docket_key(r), {"docket": docket_key(r), "year": r.get("DocYear"), "type": r.get("DocType"),
                                           "number": r.get("DocNum"), "rows": {}})
        d["rows"][r.get("Id")] = r
    out = []
    for d in by.values():
        rs = sorted(d["rows"].values(), key=lambda x: seq_int(x))
        names = [x["DisplayName"] for x in rs if x.get("DisplayName")]
        utility = max(set(names), key=names.count) if names else ""
        comments = [clean_ws(x.get("Comments")) for x in rs if x.get("Comments")]
        titles = [c for c in comments if TITLE_LIKE.match(c)]
        title = titles[0] if titles else (comments[0] if comments else "")
        out.append({"docket": d["docket"], "year": d["year"], "type": d["type"], "number": d["number"],
                    "utility": utility, "title": title,
                    "filed": min((ms_date(x.get("DateReceived")) for x in rs if x.get("DateReceived")), default=""),
                    "rows": rs})
    return out


def ms_date(v):
    """'/Date(1700000000000)/' or '2024-05-01T..' or epoch ms -> yyyy-mm-dd."""
    if isinstance(v, (int, float)):
        return dt.datetime.fromtimestamp(v / 1000, dt.timezone.utc).strftime("%Y-%m-%d")
    m = re.search(r"/Date\((-?\d+)", str(v or ""))
    if m:
        return ms_date(int(m.group(1)))
    return str(v or "")[:10]


def classify(d, listing=None):
    """(relevant, key, reasons) from a docket's title, comments and utility."""
    text = " ".join([d["title"]] + [clean_ws(r.get("Comments")) for r in d["rows"]]
                    + [(listing or {}).get("title", "")])
    reasons = []
    target = bool(TARGET_UTILITY.search(d["utility"] or "") or TARGET_UTILITY.search(text))
    if GEN.search(text):
        reasons.append("title or comments mention " + ", ".join(sorted({m.group(0).lower() for m in GEN.finditer(text)})[:5]))
    gas = bool(GAS.search(text))
    solar_only = bool(SOLAR_ONLY.search(text)) and not gas
    relevant = bool(reasons) and (target or gas) and not (solar_only and not STRONG.search(text))
    wires = bool(WIRES.search(text)) and not (gas and re.search(r"generat|plant|turbine|combined|peaking", text, re.I))
    routine = bool(ROUTINE.search(text))
    key = relevant and not wires and not routine and (gas or (target and bool(STRONG.search(text))))
    return relevant, bool(key), reasons, text


# --------------------------------------------------------- monthly agendas ---

def parse_docket_list(text):
    """{docket: {utility, title, filed}} from one monthly docket PDF (pdftotext -layout)."""
    lines = text.splitlines()
    starts = [i for i, ln in enumerate(lines) if re.match(r"\s*\d{4}-[A-Z]{2}-\d+\b", ln)]
    out = {}
    for n, i in enumerate(starts):
        j = starts[n + 1] if n + 1 < len(starts) else len(lines)
        block = lines[i:j]
        num = re.match(r"\s*(\d{4}-[A-Z]{2}-\d+)", block[0]).group(1)
        col = block[0].find("IN RE")
        if col < 0:
            col = next((ln.find("IN RE") for ln in block if "IN RE" in ln), -1)
        if col < 0:
            continue
        left = [ln[:col].strip() for ln in block]
        right = [ln[col:].strip() for ln in block]
        left_text = [x for x in left if x and not re.match(r"^\d{4}-[A-Z]{2}-\d+$", x)]
        filed = re.search(r"Filing Date:\s*(\d{1,2}/\d{1,2}/\d{2,4})", " ".join(block))
        title = clean_ws(re.sub(r"Filing Date:.*$", "", " ".join(x for x in right if x)))
        title = re.sub(r"^IN RE:\s*", "", title, flags=re.I)
        util = left_text[0] if left_text else ""
        out[num] = {"utility": util, "title": title, "filed": filed.group(1) if filed else ""}
    return out


def agenda_urls(page_html, from_year):
    urls = []
    for h in re.findall(r"href=\"?(/sites/default/files/[^\" >]+\.pdf)", page_html):
        m = re.search(r"/files/(\d{4})-\d{2}/", h)
        if m and int(m.group(1)) >= from_year and re.search(r"UTILITY|CONSENT", h, re.I):
            urls.append("https://www.psc.ms.gov" + h)
    return sorted(set(urls))


def read_agendas(from_year):
    page = fetch_page(DOCKET_LIST_PAGE, timeout=60)
    if page.status != "200":
        log(f"docket list page: HTTP {page.status}")
        return {}, []
    urls = agenda_urls(page.text, from_year)
    listing, used = {}, []
    for u in urls:
        path = WORK / "agendas" / Path(u).name
        try:
            if not path.exists():
                download(u, path, timeout=90)
            text = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True).stdout
        except Exception as e:  # noqa: BLE001
            log(f"agenda {u}: {e}")
            continue
        for num, v in parse_docket_list(text).items():
            e = listing.setdefault(num, {**v, "pdfs": []})
            e["pdfs"].append(u)
        used.append(u)
    log(f"agendas read: {len(used)} PDFs, {len(listing)} dockets")
    return listing, used


# ---------------------------------------------------------- document facts ---

def sentences(text):
    t = re.sub(r"-\n(?=[a-z])", "", text)
    t = re.sub(r"\s+", " ", t)
    return [s.strip() for s in re.split(r"(?<=[.;:!?])\s+(?=[A-Z(\"])", t) if s.strip()]


def pick(text, rx, limit, lo=20, hi=420):
    out = []
    for s in sentences(text):
        if rx.search(s) and lo < len(s) < hi and s not in out:
            out.append(s)
            if len(out) >= limit:
                break
    return out


def table_lines(layout_text, limit=14):
    """Lines of layout text that name a tracked plant and carry a year or megawatts:
    the rows of resource-plan addition and retirement tables."""
    out = []
    for ln in layout_text.splitlines():
        s = clean_ws(ln)
        if 6 < len(s) < 260 and IRP_NAMES.search(s) and (YEAR.search(s) or SIZE.search(s) or re.search(r"\d{2,4}", s)):
            if s not in out:
                out.append(s)
                if len(out) >= limit:
                    break
    return out


def doc_facts(text, layout_text=""):
    plain = text or layout_text
    coords = [f"{a}, -{b.lstrip('-')}" for a, b in LATLON.findall(plain)][:3]
    sizes = pick(plain, SIZE, 10)
    return {
        "technology": sorted({m.group(0).lower() for m in TECH.finditer(plain)})[:8],
        "equipment_maker_model": pick(plain, MAKER, 8),
        "megawatts": sizes,
        "in_service": pick(plain, re.compile(INSERVICE.pattern + r".*\b20[2-5]\d\b|\b20[2-5]\d\b.*(" + INSERVICE.pattern + ")", re.I), 6),
        "retirement": pick(plain, re.compile(r"(" + RETIRE.pattern + r").*\b20[2-5]\d\b|\b20[2-5]\d\b.*(" + RETIRE.pattern + ")", re.I), 8),
        "location": pick(plain, LOCATION, 6),
        "coords": coords,
        "resource_plan_table_lines": table_lines(layout_text or plain),
    }


def merge_facts(parts):
    out = {}
    for f in parts:
        for k, v in f.items():
            cur = out.setdefault(k, [])
            for x in v:
                if x not in cur:
                    cur.append(x)
    return {k: v[:14] for k, v in out.items()}


STAMP = re.compile(r"\*\*MPSC Electronic Copy[^\n]*")


def real_text(t):
    """Text without the Commission's page stamp (a scanned page carries only the stamp)."""
    return STAMP.sub("", t or "").strip()


def pdf_texts(path):
    """(plain text, layout text) of a PDF; scanned pages go through OCR (first 25 pages)."""
    def run(args):
        return STAMP.sub("", subprocess.run(["pdftotext"] + args + [str(path), "-"], capture_output=True, text=True).stdout)
    plain, layout = run([]), run(["-layout"])
    if len(real_text(plain)) < 300:
        import fetch
        try:
            ocr = fetch._pdf_ocr(str(path))
        except Exception:  # noqa: BLE001
            ocr = ""
        if len(real_text(ocr)) > len(real_text(plain)):
            plain = layout = STAMP.sub("", ocr)
    return plain, layout


def pick_docs(rows, cap):
    """The documents most likely to hold facts: named petitions, applications, orders,
    testimony and plans first, larger files before small ones, the first documents always."""
    scored = []
    for r in rows:
        name = f"{r.get('FileName') or ''} {r.get('Comments') or ''} {r.get('DocumentTypeName') or ''}"
        pages = r.get("FilePageCount") or 0
        s = (3 if DOC_PRIORITY.search(name) else 0) + (2 if pages >= 8 else 1 if pages >= 3 else 0)
        s += 2 if seq_int(r, 99) <= 2 else 0
        s += 2 if re.search(r"order|petition|application|irp|resource plan|testimony", name, re.I) else 0
        scored.append((-s, seq_int(r), r))
    return [r for _, _, r in sorted(scored, key=lambda x: (x[0], x[1]))[:cap]]


def read_docket(portal, d, cap):
    """Download and read the key documents of one docket; returns (docs, facts)."""
    folder = WORK / d["docket"]
    folder.mkdir(parents=True, exist_ok=True)
    fresh = portal.search(CaseYear=str(d["year"]), CaseType=str(d["type"]), CaseNumber=str(int(d["number"]))) or []
    fresh_by_seq = {seq_int(x): x for x in fresh if docket_key(x) == d["docket"]}
    docs, parts = [], []
    for r in pick_docs(d["rows"], cap):
        seq = seq_int(r)
        fr = fresh_by_seq.get(seq, r)
        rec = {"seq": seq, "file": r.get("FileName"), "type": r.get("DocumentTypeName"),
               "comment": clean_ws(r.get("Comments")), "pages": r.get("FilePageCount"),
               "received": ms_date(r.get("DateReceived")), "saved": "", "read": False}
        path = folder / f"{seq:03d}.pdf"
        ok = path.exists() and path.read_bytes()[:5] == b"%PDF-"
        if not ok and fr.get("Id_encrypted"):
            ok = portal.download(fr["Id_encrypted"], path)
        if ok:
            txt = folder / f"{seq:03d}.txt"
            if txt.exists() and len(real_text(txt.read_text())) >= 300:
                plain = layout = txt.read_text()
            else:
                plain, layout = pdf_texts(path)
                txt.write_text(layout)
            rec["saved"] = str(path.relative_to(REPO))
            rec["read"] = len(real_text(plain)) >= 300
            if rec["read"]:
                f = doc_facts(plain, layout)
                rec["facts"] = f
                parts.append(f)
        docs.append(rec)
    return docs, merge_facts(parts)


# ------------------------------------------------------------------ match ---

def match_docket(plant, d, others_by_title=False):
    """How a docket matches a plant, or None: the plant's name in the docket title or comments
    (strong), or in the text of the documents read three or more times (six when the title
    already names another plant, since big filings mention neighbors)."""
    pats = DOC_KNOWN.get(plant["id"]) or KNOWN.get(plant["id"])
    if not pats:
        return None
    head = f"{d['title']} {d.get('comments_text', '')}"
    if any(re.search(p, head, re.I) for p in pats):
        return "name in the docket title or comments"
    body = d.get("text_blob", "")
    n = sum(len(re.findall(p, body, re.I)) for p in pats)
    if n >= (6 if others_by_title else 3):
        return f"named {n} times in the documents read"
    return None


def match_all(plants, dockets):
    by_plant = {p["id"]: [] for p in plants}
    matched = set()
    for d in dockets:
        d["matched"] = []
        titled = any(match_docket(p, {**d, "text_blob": ""}) for p in plants)
        for p in plants:
            how = match_docket(p, d, others_by_title=titled)
            if how:
                d["matched"].append({"plant_id": p["id"], "plant": p["name"], "how": how})
                by_plant[p["id"]].append(d["docket"])
                matched.add(d["docket"])
    return by_plant, matched


# ----------------------------------------------------------------- output ---

def docket_block(d, full=True):
    pdfs = d.get("agenda_pdfs") or []
    L = [f"- **{d['docket']}**, {d['utility'] or 'applicant not shown'}: {d['title'][:300]}",
         f"  - Filed: {d.get('filed') or 'unknown'}; documents on file: {d['doc_count']}; "
         f"citation: docket number {d['docket']} in the Commission's document search"
         + (f"; agenda PDF (stable link): {pdfs[0]}" if pdfs else "")]
    if full and d.get("facts"):
        f = d["facts"]
        for k, label in [("technology", "Technology"), ("megawatts", "Megawatts"),
                         ("equipment_maker_model", "Equipment"), ("in_service", "In service"),
                         ("retirement", "Retirements"), ("location", "Location"), ("coords", "Coordinates"),
                         ("resource_plan_table_lines", "Plan table lines")]:
            v = f.get(k)
            if v:
                L.append(f"  - {label}: " + " | ".join(v[:4 if k != "resource_plan_table_lines" else 8]))
    for doc in d.get("docs", []):
        if doc.get("saved"):
            L.append(f"  - read {doc['file']} ({doc['pages']} pages, {doc['received']}): {doc['comment'][:120]}; copy in {doc['saved']}")
    return L


def write_outputs(out_dir, plants, dockets, by_plant, matched, sources, today, from_year):
    out_dir.mkdir(parents=True, exist_ok=True)
    slim = []
    for d in dockets:
        x = {k: v for k, v in d.items() if k not in ("rows", "text_blob")}
        slim.append(x)
    unmatched = [d for d in dockets if d["key"] and d["docket"] not in matched]
    data = {"generated": today, "from_year": from_year, "sources": sources, "dockets": slim,
            "by_plant": by_plant, "unmatched_generation": [d["docket"] for d in unmatched]}
    (out_dir / "psc_dockets.json").write_text(json.dumps(data, indent=1, default=str))
    by_id = {d["docket"]: d for d in dockets}
    L = [f"# Mississippi Public Service Commission dockets on generation, resource plans and retirements ({today})", "",
         f"Dockets opened {from_year} or later. Portal document links need a session, so cite the docket number and document name; "
         "the monthly agenda PDF is a stable link for a docket's title and filing date. Copies of documents read are in work/psc_ms/ and are not committed.", "",
         "## Sources", ""]
    L += [f"- {s['name']}: {s['how']} ({s['url']})" for s in sources]
    L += ["", "## Matched to GEM plants", ""]
    for p in plants:
        ids = by_plant.get(p["id"], [])
        L.append(f"### {p['name']} ({p['id']}), {p['city']}, {p['county'].title()} County")
        L.append("")
        if not ids:
            L += ["No docket matched.", ""]
            continue
        for k in ids:
            d = by_id[k]
            if d.get("routine"):
                continue
            how = next(m["how"] for m in d["matched"] if m["plant_id"] == p["id"])
            L += docket_block(d)
            L.append(f"  - Match: {how}")
        routine = [by_id[k] for k in ids if by_id[k].get("routine")]
        if routine:
            L.append("- Routine equipment notices (Rule 7.103, a utility tells the Commission it will replace or repair parts; "
                     "they show a unit was still running, nothing more):")
            for d in routine:
                L.append(f"  - {d['docket']}, filed {d.get('filed') or 'date not shown'}: {d['title'][:140]}")
        L.append("")
    L += ["## Generation dockets that match no GEM plant (possible new plants, uprates or retirements)", ""]
    for d in sorted(unmatched, key=lambda x: x["docket"]):
        L += docket_block(d)
    L += ["", "## Other generation-related dockets (not read in full)", ""]
    for d in sorted((d for d in dockets if d["relevant"] and not d["key"]), key=lambda x: x["docket"]):
        L += docket_block(d, full=False)
    (out_dir / "psc_dockets.md").write_text("\n".join(L) + "\n")
    return unmatched


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--from-year", type=int, default=2022)
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--plants", help="comma-separated GEM location IDs")
    ap.add_argument("--docs-per-docket", type=int, default=8)
    ap.add_argument("--no-docs", action="store_true", help="list dockets, download nothing")
    ap.add_argument("--match-only", metavar="JSON", help="re-match a saved psc_dockets.json, no network")
    a = ap.parse_args()
    plants = load_plants(wanted=set(a.plants.split(",")) if a.plants else None)
    today = dt.date.today().isoformat()
    if a.match_only:
        saved = json.loads(Path(a.match_only).read_text())
        dockets, sources = saved["dockets"], saved["sources"]
        for d in dockets:
            d["text_blob"] = " ".join(" ".join(sum(((doc.get("facts") or {}).values() for doc in d.get("docs", [])), []))
                                      for _ in [0])
        by_plant, matched = match_all(plants, dockets)
        write_outputs(Path(a.out), plants, dockets, by_plant, matched, sources, today, saved.get("from_year", a.from_year))
        return
    listing, agendas = read_agendas(a.from_year)
    portal = Portal()
    rows = {}
    this_year = dt.date.today().year
    failed = []
    queries = [(f"{year}_company_{co}", {"CaseYear": str(year), "Company": co}, f"{year} company {co!r}")
               for year in range(a.from_year, this_year + 1) for co in COMPANIES]
    queries += [(f"{year}_keyword_{kw}", {"CaseYear": str(year), "Keywords": kw}, f"{year} keyword {kw!r}")
                for year in range(a.from_year, this_year + 1) for kw in KEYWORDS]
    for label, kw, nice in queries:
        try:
            got = portal.cached_search(label, **kw)
        except Exception as e:  # noqa: BLE001
            log(f"{nice}: {e}")
            got = None
        if got is None:
            failed.append(nice)
            log(f"{nice}: no answer")
            continue
        log(f"{nice}: {len(got)} documents")
        rows.update({x["Id"]: x for x in got})
    dockets = group_dockets(list(rows.values()))
    for d in dockets:
        lst = listing.get(d["docket"], {})
        if lst.get("title") and not re.match(r"\s*IN RE", d["title"], re.I) and len(lst["title"]) > len(d["title"]):
            d["title"] = lst["title"]
        d["utility"] = d["utility"] or lst.get("utility", "")
        d["filed"] = d["filed"] or lst.get("filed", "")
        d["agenda_pdfs"] = lst.get("pdfs", [])[:3]
        d["relevant"], d["key"], d["reasons"], d["comments_text"] = classify(d, lst)
        d["routine"] = bool(ROUTINE.search(d["comments_text"]))
        if not d["key"] and not d["routine"] and not WIRES.search(d["comments_text"]) and any(
                match_docket(p, {**d, "text_blob": ""}) for p in plants):
            d["relevant"] = d["key"] = True
            d["reasons"] = d["reasons"] + ["its title names a GEM plant"]
        d["doc_count"] = len(d["rows"])
    log(f"{len(dockets)} dockets; {sum(1 for d in dockets if d['relevant'])} generation related; "
        f"{sum(1 for d in dockets if d['key'])} key")
    for d in dockets:
        d["docs"], d["facts"], d["text_blob"] = [], {}, ""
        if d["key"] and not a.no_docs:
            log(f"reading {d['docket']}: {d['title'][:90]}")
            try:
                d["docs"], d["facts"] = read_docket(portal, d, a.docs_per_docket)
            except Exception as e:  # noqa: BLE001
                log(f"  {d['docket']} failed: {e}")
            folder = WORK / d["docket"]
            d["text_blob"] = " ".join(p.read_text(errors="replace") for p in sorted(folder.glob("*.txt"))) if folder.exists() else ""
    sources = [
        {"name": "Mississippi PSC document search (CTS portal)", "url": SEARCH_PAGE,
         "how": f"real Chrome earns the page's own gate, then curl replays the search; {len(rows)} documents from {a.from_year} on, "
                f"{len(dockets)} dockets, {sum(1 for d in dockets if d['relevant'])} generation related"
                + (f"; {len(failed)} searches got no answer and are not in this list: {'; '.join(failed)}" if failed else "")},
        {"name": "Monthly Commission docket PDFs", "url": DOCKET_LIST_PAGE,
         "how": f"{len(agendas)} utility and consent docket PDFs read for titles and filing dates (stable links)"}]
    by_plant, matched = match_all(plants, dockets)
    for d in dockets:
        d.pop("rows", None)
    unmatched = write_outputs(Path(a.out), plants, dockets, by_plant, matched, sources, today, a.from_year)
    log(f"{len(matched)} dockets matched to plants; {len(unmatched)} key dockets unmatched")
    for p in plants:
        log(f"  {p['name']}: {len(by_plant[p['id']])}")


if __name__ == "__main__":
    main()

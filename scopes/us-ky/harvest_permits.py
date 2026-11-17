"""
Harvest Kentucky air permits before a research sweep.

Kentucky has two air permit authorities. Every source below answers without a
login. What was found (2026-11-04):

  1. The Division for Air Quality (DAQ), everywhere outside Jefferson County. Its
     complete record is the Department for Environmental Protection eSearch API,
     https://dep.gateway.ky.gov/eSearch.WebApi/api (the search page a person
     uses is https://dep.gateway.ky.gov/eSearch/). Plain requests work.
       POST /IssuedApprovals/Search and POST /PendingApproval/Search with
         {"AgencyId":"","AgencyName":"","County":"","Municipality":"",
          "Program":"Air","ActivityType":"","LastIssuedDays":""}
       return the whole statewide air record in one answer (18,404 issued
       approvals and 809 pending ones on 2026-11-04). Each row names the agency
       interest (AgencyId, AgencyName, County, Municipality), the activity
       (ActivityCode, ActivityYear, ActivityNum, ActivityType such as
       "Title V-Renewal"), its milestone and dates, and DetailRows, the number
       of documents online (0 for most approvals before about 2023).
       GET /issuedapprovals/Document/<key> or /pendingapproval/document/<key>
       lists an activity's documents. <key> is the percent-encoded JSON
       {"AgencyId":..,"ActivityCode":..,"ActivityYear":..,"ActivityNumber":..};
       unencoded JSON answers 400. Each document has DocTitle, DocDate and
       SourceDocId.
       GET /documentGenerate/getDocument/<SourceDocId> returns the PDF. That
       address is what a note cites; fetch.py and url_verifier.py read it.
  2. The DAQ public notices page,
     https://eec.ky.gov/Environmental-Protection/Air/Pages/Public-Notices.aspx,
     links the drafts at comment ("<Facility> - Permit V-21-048 R1 Draft.pdf",
     "- Statement of Basis and Summary.pdf", "- Application.pdf",
     "- Public Notice.pdf"). It is a notice feed only; eSearch is the record.
  3. The Louisville Metro Air Pollution Control District (APCD), Jefferson
     County (Mill Creek, Cane Run, Paddy's Run, every Louisville data center).
     Its pages need fetch.py's browser-fingerprint route, so they are read with
     get(). The active operating permits page lists operating permits only
     (Mill Creek 5 and 6 construction permits are not on it); each permit link
     is a media page that resolves to a /sites/default/files/...pdf. The
     proposed actions page lists permits at comment, one table row each.

Steps:
  1. Read the statewide issued and pending air lists, group them by agency
     interest, and keep a dated copy under esearch/.
  2. Match agency interests to GEM Kentucky plants (KNOWN holds hand-checked
     agency ids; a plant missing there is matched by its name words, marked for
     checking). Facilities that look like power plants or data centers and
     match no plant are kept as unmatched leads.
  3. List the documents of every matched or power-like facility's activities
     that have any (DetailRows above 0), download them into
     work/permits/docs/<agency id>/, extract text with pdftotext (OCR through
     fetch.py when a scan has no text layer) and keep the lines that give the
     permit number, project, equipment, maker, sizes and location.
  4. The sweep: the newest initial and revision approvals with documents at
     facilities whose names do not look like power sites are read (first
     pages, up to --sweep-read). A generator fleet or data center found that
     way becomes an unmatched lead.
  5. Read the DAQ notices and the two Louisville pages and do the same.

Output, in scopes/us-ky/work/permits/ (what the sweep agents read): one plain-text
index per plant (<GEM location id>.md), _unmatched.md, _sweep.md, index.json,
harvest_log.jsonl and esearch/<date>.json. A summary and facilities.json (the
file data_center_fleets.py reads) go to batches/<scope>/harvest/. Permit PDFs
name agency and company staff: the PDFs and their text stay under work/ (never
committed). Nothing here stages a record.

Usage (from the repo root):
    python scopes/us-ky/harvest_permits.py --scope us-ky                  # everything
    python scopes/us-ky/harvest_permits.py --scope us-ky --plants L100001025720
    python scopes/us-ky/harvest_permits.py --scope us-ky --match-only     # list matches, no documents
    python scopes/us-ky/harvest_permits.py --scope us-ky --no-sweep       # skip the sweep
"""
import argparse
import html
import json
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from fetch import CHROME_UA  # noqa: E402
from harvest_lib import CSV, REPO, SIZE, clean_ws, get, harvest_out, norm_county, pick, report_failure  # noqa: E402

API = "https://dep.gateway.ky.gov/eSearch.WebApi/api"
UI = "https://dep.gateway.ky.gov/eSearch/"
DOCGEN = API + "/documentGenerate/getDocument/{sid}"
SEARCH_BODY = {"AgencyId": "", "AgencyName": "", "County": "", "Municipality": "", "Program": "Air",
               "ActivityType": "", "LastIssuedDays": ""}
DAQ_NOTICES = "https://eec.ky.gov/Environmental-Protection/Air/Pages/Public-Notices.aspx"
EEC = "https://eec.ky.gov"
LOU = "https://louisvilleky.gov"
APCD_ACTIVE = LOU + "/government/air-pollution-control-district/active-air-pollution-operating-permits-louisville"
APCD_PROPOSED = LOU + "/government/air-pollution-control-district/services/proposed-actions-apcd"
RECORDS = "https://eec.ky.gov/Pages/Open-Records.aspx"

# Hand-checked agency interest ids per GEM plant (eSearch AgencyInterest search, 2026-11-04).
# "check" ids are related names that may or may not be this plant. "names" match the
# DAQ notice and Louisville APCD facility names (lower case regular expressions).
KNOWN = {
    "L100000103930": {"ai": [2610], "names": [r"big sandy plant", r"kentucky power.*big sandy"]},
    "L100000103932": {"ai": [], "names": [r"cane run"]},
    "L100000103935": {"ai": [3808], "names": [r"\bcooper (station|power|plant|gen)", r"ekpc.*cooper"]},
    "L100000103937": {"ai": [3148], "check": [83749], "names": [r"\bbrown (station|gen)", r"ku brown"]},
    "L100000103938": {"ai": [176], "check": [77286], "names": [r"east bend"]},
    "L100000103939": {"ai": [942], "names": [r"elmer smith", r"green river east"]},
    "L100000103943": {"ai": [44411], "names": [r"\bgreen (station|gen)", r"rd green"]},
    "L100000103945": {"ai": [], "names": [r"mill creek"]},
    "L100000103946": {"ai": [127687], "names": [r"paradise"]},
    "L100000103947": {"ai": [4196], "check": [44411], "names": [r"\breid\b"]},
    "L100000103950": {"ai": [3004], "names": [r"spurlock"]},
    "L100000103951": {"ai": [4054], "names": [r"trimble county"]},
    "L100000401571": {"ai": [], "names": [r"padd(y|ie)'?s run"]},
    "L100000401892": {"ai": [39541], "names": [r"bluegrass gen"]},
    "L100000401893": {"ai": [808], "names": [r"j\.? ?k\.? smith", r"smith (station|gen)"]},
    "L100000402189": {"ai": [84744], "names": [r"paducah power", r"\bpps\b"]},
    "L100000402250": {"ai": [4392], "names": [r"riverside gen"]},
    "L100000402323": {"ai": [39146], "names": [r"marshall energy", r"kgen marshall"]},
    "L100001025720": {"ai": [183908], "names": [r"liberty station"]},
    "L100001026095": {"ai": [184265], "names": [r"kymea"]},
}
# Jefferson County plants are permitted by the Louisville APCD, never by DAQ eSearch.
APCD_PLANTS = {"L100000103932", "L100000103945", "L100000401571"}

POWER_NAME = re.compile(
    r"power|electric|generat|energy center|energy facility|turbine|cogen|data ?cent|datacent|data storage|"
    r"computing|compute (campus|center)|bitcoin|crypto|hyperscal|peaking|combined cycle|kentucky utilities|\bku\b|lg ?& ?e|louisville gas|"
    r"east k(y|entucky) power|\bekpc\b|big rivers|duke energy|kentucky power|\btva\b|tennessee valley|kymea|"
    r"municipal (utilit|power|light)|hmp ?& ?l|kgen|\bnrg\b|terawulf|justified data|cyrusone|digital realty|"
    r"meta platforms|microsoft|amazon data|\baws\b|google|\bqts\b|vantage data|flexential|stack infra|"
    r"aligned data|core scientific|middle mile", re.I)
POWER_DROP = re.compile(
    r"cell tower|tower engine|pump station|lift station|powerscreen|power ?screen|portable|pipeline|pipe line|"
    r"midstream|gas storage|gate station|compressor|transmission station|service center|operations center|"
    r"\boffice\b|landfill(?! gas to electric)|cooperage|electric products|speaker|wintec|lamp|glass|coil|"
    r"motor & electric|substation|electric motor|electric co-?op(erative)?(?! .*(station|plant))|"
    r"distillery|hospital|school|university|church|crusher|quarry|asphalt|concrete|water|senior center|"
    r"tower site|computer supplies|powertrain|aircraft|vernova|emerson|schneider|warden electric|hydro|"
    r"storeroom|dehydration|meter station", re.I)
NAME_NOISE = re.compile(
    r"\b(power station|power plant|generating station|generating|generation|facility|station|energy center|"
    r"energy|plant|power|ky|kentucky|the|municipal|of|and|city|llc|inc|company|co|corp|corporation|combined|"
    r"cycle|county|industrial|park|campus|data|center|fossil|peaker|no|east|west|gen|stn)\b", re.I)
EQUIPMENT = re.compile(r"turbine|\bct\b|engine|rice\b|generat|\bgen\b|boiler|duct burner|hrsg|"
                       r"combined cycle|simple cycle|peaking|diesel|reciprocating|genset", re.I)
MAKER = re.compile(r"model\b|caterpillar|cat g|wartsila|w[äa]rtsil[äa]|jenbacher|"
                   r"general electric|\bGE\b|siemens|solar turbines|mitsubishi|cummins|rolls[- ]royce|"
                   r"mtu\b|kohler|generac|waukesha|pratt|ansaldo|baker hughes|"
                   r"hitachi|titan \d|taurus|mars \d|lm ?\d{4}|7ea|7fa|7ha|6b\b|f-?class|h-?class", re.I)
LOCATION = re.compile(
    r"latitude|longitude|\blat\b|\blong\b|\bUTM\b|located (at|in|on|near|approximately)|physical address|"
    r"site address|facility address|street address|\b\d{2,5} [A-Z0-9][\w. ]+ (road|rd|street|st|avenue|ave|"
    r"highway|hwy|drive|dr|lane|ln|blvd|boulevard|pike)\b|county,? kentucky|ky 4[0-2]\d{3}|kentucky 4[0-2]\d{3}",
    re.I)
PROJECT = re.compile(r"proposes|propose to|will consist|project (is|will|consists)|construction of|"
                     r"to construct|new (electric|power|generat)|install(ation)? of", re.I)
FACILITY_LINE = re.compile(r"facility( name)?:|company( name)?:|applicant:|source name|permittee|\bre:|"
                           r"permit (no|number)|agency interest|\bAI\b ?(#|no|number)|county,? kentucky", re.I)
LATLON = re.compile(r"\b(3[6-9]\.\d{3,})\s*[,;/ °]*\s*N?\s*[,;/ ]?\s*-?\s*(8[2-9]\.\d{3,})\b")
PERMIT_NO = re.compile(r"\b(?:[VFSCO]-\d{2}-\d{3}(?: ?R\d)?|O-\d{4}-\d{2}-[A-Z]|C-\d{4}-\d{2}-\d{4}-[A-Z])\b")
READ_FIRST = re.compile(r"statement of basis|application|executive summary|draft|permit", re.I)
SWEEP_TYPES = re.compile(r"initial|sig rev|revision|construct", re.I)
SWEEP_DC = re.compile(r"data ?cent|datacent|hyperscal|cryptocurrenc|bitcoin|blockchain|digital mining|"
                      r"\bcolocation\b|server (farm|hall)", re.I)
SWEEP_GEN = re.compile(r"(emergency|standby|backup|prime)\s+(diesel\s+|natural gas\s+)?(engine|generator)s?|"
                       r"generator sets?|gensets?|combustion turbines?|electric generat", re.I)
SWEEP_MW = re.compile(r"\b\d[\d,.]*\s*(MW|megawatts?)\b", re.I)


def log(msg):
    print(f"[harvest-ky] {msg}", file=sys.stderr, flush=True)


def words(text):
    t = NAME_NOISE.sub(" ", re.sub(r"\(.*?\)", " ", str(text or "")))
    return {w.lower() for w in re.split(r"[^A-Za-z]+", t) if len(w) >= 4}


def iso(s):
    """'2026-10-07T00:00:00' or '10/07/2026' to 2026-10-07, or ''."""
    s = str(s or "")
    m = re.match(r"(\d{4}-\d{2}-\d{2})", s)
    if m:
        return m.group(1)
    m = re.search(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b", s)
    return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}" if m else ""


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s or "").lower()).strip("-")[:60] or "x"


def doc_key(row):
    """The percent-encoded JSON key the eSearch document calls take."""
    k = {"AgencyId": int(row["AgencyId"]), "ActivityCode": row["ActivityCode"],
         "ActivityYear": int(row["ActivityYear"]), "ActivityNumber": int(row["ActivityNum"])}
    return urllib.parse.quote(json.dumps(k, separators=(",", ":")), safe="")


def activity_name(row):
    return f"{row['ActivityCode']} {int(row['ActivityYear'])}-{int(row['ActivityNum'])}"


# ---------------------------------------------------------------- facilities ---

def new_fac(key, name, source):
    return {"key": key, "name": name, "source": source, "company": "", "county": "", "city": "", "ai": None,
            "activities": [], "permits": [], "found_by": [], "docs": [], "hint": "", "links": []}


def fac_text(f):
    return " | ".join(x for x in (f["company"], f["name"], f["county"], f.get("hint", "")) if x).lower()


def is_power(f):
    """A power or data center look: a power-like name not on the drop list."""
    if POWER_DROP.search(f["name"]):
        return False
    return bool(POWER_NAME.search(f"{f['company']} {f['name']} {f.get('hint', '')}"))


def esearch_facilities(issued, pending):
    """Group the statewide issued and pending rows by agency interest."""
    facs = {}
    for status, rows in (("issued", issued), ("pending", pending)):
        for r in rows or []:
            try:
                aid = int(r["AgencyId"])
            except (KeyError, TypeError, ValueError):
                continue
            f = facs.setdefault(f"ai-{aid}", new_fac(f"ai-{aid}", clean_ws(r.get("AgencyName") or ""), "eSearch"))
            f["ai"] = aid
            f["county"] = f["county"] or clean_ws(r.get("County") or "")
            f["city"] = f["city"] or re.sub(r"\s*\(.*?\)\s*$", "", clean_ws(r.get("Municipality") or ""))
            f["activities"].append({
                "status": status, "activity": activity_name(r), "type": r.get("ActivityType") or "",
                "milestone": r.get("CurrentMilestone") or "", "milestone_date": iso(r.get("MilestoneDate")),
                "issued": iso(r.get("IssuedDate")), "documents": int(r.get("DetailRows") or 0),
                "key": doc_key(r)})
    for f in facs.values():
        f["activities"].sort(key=lambda a: a["issued"] or a["milestone_date"], reverse=True)
    return facs


def parse_notices(text):
    """DAQ public notices: {facility name: [{kind, title, url}]}, repeats dropped."""
    out = {}
    for href in dict.fromkeys(re.findall(r'href="(/Environmental-Protection/Air/Draft%20Permit%20Documents/[^"]+?\.pdf)"',
                                         text or "", re.I)):
        base = urllib.parse.unquote(href.rsplit("/", 1)[-1])[:-4]
        name, _, kind = base.rpartition(" - ")
        if not name:
            name, kind = base, "document"
        out.setdefault(clean_ws(html.unescape(name)), []).append(
            {"kind": clean_ws(kind), "title": base, "url": EEC + href})
    return out


def parse_apcd_active(text):
    """Louisville active operating permits: [{name, permits: [{number, kind, url}], effective}].
    The page repeats each permit under several headings; the caller merges by permit number."""
    out = []
    for strong, rest in re.findall(r"<p><strong>(.*?)</strong>(.*?)</p>", text or "", re.S):
        name = clean_ws(html.unescape(re.sub(r"<[^>]+>", " ", strong)))
        if not name:
            continue
        links = []
        for href, label in re.findall(r'<a href="([^"]+)"[^>]*>(.*?)</a>', rest, re.S):
            label = clean_ws(html.unescape(re.sub(r"<[^>]+>", " ", label)))
            url = href if href.startswith("http") else LOU + href
            m = PERMIT_NO.search(label)
            links.append({"number": m.group(0) if m else "", "kind": label, "url": url})
        eff = re.search(r"Effective(?:&nbsp;|\s)*([\d/]+)", rest)
        out.append({"name": name, "permits": links, "effective": iso(eff.group(1)) if eff else ""})
    return out


def parse_apcd_proposed(text):
    """Louisville proposed actions: [{name, action, links, comment_begins, comment_ends, hearing}]."""
    m = re.search(r"<main.*?</main>", text or "", re.S)
    out = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", m.group(0) if m else "", re.S):
        cells = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
        if len(cells) < 2:
            continue
        desc = cells[0]
        plain = clean_ws(html.unescape(re.sub(r"<[^>]+>", " ", desc)))
        fm = re.match(r"(Proposed .*?) for (.*?),\s*(?:<a|$)", clean_ws(html.unescape(desc)))
        action, name = (fm.group(1), clean_ws(re.sub(r"<[^>]+>", "", fm.group(2)))) if fm else ("", plain[:80])
        links = []
        for href, label in re.findall(r'<a href="([^"]+)"[^>]*>(.*?)</a>', desc, re.S):
            label = clean_ws(html.unescape(re.sub(r"<[^>]+>", " ", label)))
            links.append({"number": (PERMIT_NO.search(label) or [""])[0] if PERMIT_NO.search(label) else "",
                          "kind": label, "url": href if href.startswith("http") else LOU + href})
        dates = re.findall(r"\d{1,2}/\d{1,2}/\d{4}", cells[1])
        out.append({"name": name, "action": action, "text": plain, "links": links,
                    "comment_begins": iso(dates[0]) if dates else "", "comment_ends": iso(dates[1]) if len(dates) > 1 else "",
                    "hearing": clean_ws(html.unescape(re.sub(r"<[^>]+>", " ", cells[2]))) if len(cells) > 2 else ""})
    return out


def apcd_facilities(active, proposed):
    facs = {}
    for blk in active:
        nums = [p["number"] for p in blk["permits"] if p["number"]]
        key = "apcd-" + slug(nums[0] if nums else blk["name"])
        f = facs.setdefault(key, new_fac(key, blk["name"], "Louisville APCD active permits"))
        if blk["name"] not in f["name"] and blk["name"] not in f["company"]:
            f["company"] = (f["company"] + "; " if f["company"] else "") + blk["name"]
        f["county"] = "Jefferson"
        for p in blk["permits"]:
            if p["url"] not in [x["url"] for x in f["links"]]:
                f["links"].append({**p, "effective": blk["effective"]})
        if nums and not any(x["number"] == nums[0] for x in f["permits"]):
            f["permits"].append({"number": nums[0], "type": "operating permit", "status": "active",
                                 "step": f"effective {blk['effective']}" if blk["effective"] else "", "comment_ends": ""})
    for row in proposed:
        key = "apcd-proposed-" + slug(row["name"])
        f = facs.setdefault(key, new_fac(key, row["name"], "Louisville APCD proposed actions"))
        f["county"] = "Jefferson"
        f["links"] += [{**x, "effective": ""} for x in row["links"]]
        num = next((x["number"] for x in row["links"] if x["number"]), "")
        f["permits"].append({"number": num, "type": row["action"], "status": "proposed, at comment",
                             "step": f"hearing: {row['hearing']}" if row["hearing"] else "",
                             "comment_ends": row["comment_ends"]})
    return facs


def notice_facilities(notices):
    facs = {}
    for name, docs in notices.items():
        key = "daq-notice-" + slug(name)
        f = facs.setdefault(key, new_fac(key, name, "DAQ public notices"))
        num = next((m.group(0) for d in docs for m in [PERMIT_NO.search(d["kind"])] if m), "")
        f["permits"].append({"number": num, "type": "draft at comment", "status": "public notice", "step": "",
                             "comment_ends": ""})
        for d in docs:
            f["docs"].append({"number": num, "name": d["title"], "type": d["kind"], "date": "", "url": d["url"],
                              "how": "DAQ public notices page", "key": d["url"]})
    return facs


def match(plant, facs):
    """[(facility, how)]: hand-checked agency ids and names, else the plant's distinctive name words
    plus its county."""
    out = []
    k = KNOWN.get(plant["id"])
    for f in facs:
        if f["source"] == "eSearch":
            if k and f["ai"] in k.get("ai", []):
                out.append((f, "checked by hand"))
            elif k and f["ai"] in k.get("check", []):
                out.append((f, "a related agency interest, check it is this plant"))
            elif not k and plant["name_words"] and plant["name_words"] <= words(f["name"]) and is_power(f) \
                    and (not plant["county"] or not f["county"] or plant["county"].lower() == f["county"].lower()):
                out.append((f, "matched by name and county, check it is this plant"))
        else:
            t = fac_text(f)
            if k and any(re.search(p, t) for p in k.get("names", [])):
                out.append((f, "checked by hand" if plant["id"] in APCD_PLANTS else "matched by a hand-checked name, check it is this plant"))
            elif not k and plant["name_words"] and plant["name_words"] <= words(f["name"]) and is_power(f):
                out.append((f, "matched by name, check it is this plant"))
    return out


# ---------------------------------------------------------------- documents ---

class ESearch:
    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": CHROME_UA, "Accept": "application/json"})
        self.calls, self.errors = 0, []

    def _do(self, method, url, **kw):
        for attempt in range(3):
            self.calls += 1
            try:
                r = self.s.request(method, url, timeout=kw.pop("timeout", 180) if attempt == 0 else 180, **kw)
                if r.status_code == 200:
                    return r
                err = str(r.status_code)
            except requests.RequestException as e:
                err = "000 " + str(e)[:100]
            time.sleep(2 * (attempt + 1))
        self.errors.append(f"{method} {url}: {err}")
        report_failure(url, err.split()[0], "eSearch call failed three times")
        return None

    def search(self, kind):
        r = self._do("POST", f"{API}/{kind}/Search", json=SEARCH_BODY, timeout=300)
        try:
            return r.json() if r is not None else None
        except ValueError:
            self.errors.append(f"{kind}: not JSON")
            return None

    def documents(self, act):
        path = "issuedapprovals/Document" if act["status"] == "issued" else "pendingapproval/document"
        r = self._do("GET", f"{API}/{path}/{act['key']}")
        try:
            rows = r.json() if r is not None else []
        except ValueError:
            rows = []
        out = []
        for d in rows or []:
            sid = d.get("SourceDocId") or d.get("DocId")
            if sid is None:
                continue
            sid = int(sid)
            title = clean_ws(d.get("DocTitle") or "")
            out.append({"number": str(sid), "name": title, "type": re.sub(r"\.pdf$", "", title, flags=re.I),
                        "date": iso(d.get("DocDate")), "url": DOCGEN.format(sid=sid),
                        "activity": f"{act['activity']} {act['type']}", "key": str(sid)})
        return out

    def download(self, url, path):
        r = self._do("GET", url, timeout=300)
        if r is None:
            return "not downloaded"
        if r.content[:5] != b"%PDF-":
            report_failure(url, "200", "not a PDF")
            return "not a PDF"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(r.content)
        return "downloaded"


def pdf_text(path, pages=None):
    cmd = ["pdftotext", "-layout"] + (["-l", str(pages)] if pages else []) + [str(path), "-"]
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=300).stdout
    except (subprocess.SubprocessError, OSError):
        return ""


def doc_path(out_dir, f, d):
    folder = str(f["ai"]) if f["ai"] else slug(f["key"])
    return out_dir / "docs" / folder / f"{d['date'] or 'nodate'}_{slug(d['type'])[:40]}_{slug(d['number'])[:12]}.pdf"


def read_doc(es, out_dir, f, d, pages=None, ocr=True):
    """Download one document (kept on disk, reused next run), extract its text and keep facts.
    Louisville pages are read through get() (they need the browser-fingerprint route), and the
    text alone is kept."""
    path = doc_path(out_dir, f, d)
    txt_path = path.with_suffix(".txt")
    if d["url"].startswith(LOU):
        if txt_path.exists():
            text, state = txt_path.read_text(encoding="utf-8"), "saved (from an earlier run)"
        else:
            page = get(d["url"], timeout=300)
            text = page.text if page.status == "200" else ""
            state = f"read through fetch.py ({page.status})"
            if text.strip():
                txt_path.parent.mkdir(parents=True, exist_ok=True)
                txt_path.write_text(text, encoding="utf-8")
        d["file"] = str(txt_path.relative_to(REPO)) if txt_path.exists() else ""
    else:
        state = "saved (from an earlier run)" if path.exists() else es.download(d["url"], path)
        d["file"] = str(path.relative_to(REPO)) if path.exists() else ""
        text = pdf_text(path, pages) if path.exists() else ""
        if path.exists() and len(text.strip()) < 200 and ocr:
            page = get(d["url"], timeout=600)
            if page.status == "200" and page.text.strip():
                text, state = page.text, state + ", text read by OCR"
        if path.exists():
            txt_path.write_text(text, encoding="utf-8")
    d["state"] = state if text.strip() or not d["file"] else state + ", no text layer"
    d["facts"] = doc_facts(text) if text.strip() else {}
    return text


def doc_facts(text):
    latlon = [f"{a}, -{b.lstrip('-')}" for a, b in LATLON.findall(text)][:3]
    return {
        "ids": sorted({re.sub(r"\s+", " ", x).upper() for x in PERMIT_NO.findall(text)})[:6],
        "facility": pick(text, FACILITY_LINE, 6),
        "project": pick(text, PROJECT, 6),
        "equipment": pick(text, EQUIPMENT, 10),
        "makers": pick(text, MAKER, 8),
        "sizes": pick(text, SIZE, 10),
        "location": pick(text, LOCATION, 8),
        "coords": latlon,
    }


def rank_docs(docs):
    """Newest first; statements of basis, applications and permits before notices and letters."""
    return sorted(docs, key=lambda d: (not READ_FIRST.search(d["type"]), "".join(chr(255 - ord(c)) for c in d["date"])))


def apcd_pdf(media_url):
    """A Louisville media page's PDF address, or ''."""
    page = get(media_url, timeout=120)
    if page.status != "200":
        return ""
    if page.is_pdf:
        return page.final_url or media_url
    m = re.search(r"(?:https://louisvilleky\.gov)?(/sites/default/files/[^\"'<> ]+?\.pdf)", page.text or "")
    return LOU + m.group(1) if m else ""


def sweep_keep(text):
    """A generator fleet or data center in a document read only by the sweep."""
    if SWEEP_DC.search(text):
        return "names a data center"
    if SWEEP_GEN.search(text) and (SWEEP_MW.search(text) or len(SWEEP_GEN.findall(text)) >= 8):
        return "lists generators or turbines"
    return ""


def hint_of(text):
    return " ".join(pick(text, FACILITY_LINE, 4))[:400]


# ---------------------------------------------------------------- reporting ---

def fac_block(f, how=None):
    where = ", ".join(x for x in (f["city"], f"{f['county']} County" if f["county"] else "") if x)
    L = [f"- {f['name']} ({where or 'place not shown'}; {f['source']}"
         + (f", agency interest {f['ai']}" if f["ai"] else "") + ")"]
    if f["company"]:
        L.append(f"    - also listed as: {f['company']}")
    if f.get("hint"):
        L.append(f"    - the document text names: {f['hint']}")
    for a in f["activities"][:25]:
        L.append(f"    - {a['status']} {a['activity']}, {a['type']}: {a['milestone']}"
                 + (f" {a['milestone_date']}" if a["milestone_date"] else "")
                 + (f", issued {a['issued']}" if a["issued"] else "")
                 + (f", {a['documents']} documents online" if a["documents"] else ", no documents online"))
    if len(f["activities"]) > 25:
        L.append(f"    - {len(f['activities']) - 25} older activities not listed (index.json has none either; search eSearch)")
    for p in f["permits"]:
        L.append(f"    - permit: {p['number'] or 'number not shown'}, {p['type']}, {p['status']}"
                 + (f", {p['step']}" if p["step"] else "") + (f", comments end {p['comment_ends']}" if p["comment_ends"] else ""))
    for x in f["links"]:
        L.append(f"    - page: {x['kind']}: {x['url']}")
    if f["found_by"]:
        L.append(f"    - found by: {'; '.join(f['found_by'])}")
    for d in f["docs"]:
        L.append(f"    - document ({d.get('state', 'not read')}, {d['date'] or 'date not shown'}): {d['name']}"
                 + (f" ({d['activity']})" if d.get("activity") else "") + f": {d['url']}")
        fa = d.get("facts") or {}
        for key, label in (("ids", "permit numbers"), ("facility", "facility"), ("project", "project"),
                           ("equipment", "equipment"), ("makers", "maker or model"), ("sizes", "size"),
                           ("location", "site address or location"), ("coords", "coordinates")):
            for line in fa.get(key, []):
                L.append(f"        - {label}: {line}")
    if how:
        L.insert(0, f"Matched: {how}.")
    return L


def write_index(path, plant, matched):
    L = [f"# Kentucky air permit files for {plant['name']} ({plant['id']})", "",
         "Sources: the Kentucky Department for Environmental Protection eSearch record (" + UI + "), the Division "
         "for Air Quality public notices page (" + DAQ_NOTICES + ") and the Louisville Metro Air Pollution Control "
         "District permit pages (" + APCD_ACTIVE + ", " + APCD_PROPOSED + "). A document address "
         "(eSearch.WebApi/api/documentGenerate/getDocument/...) is citable as it stands; fetch.py and "
         "url_verifier.py read it. The PDFs and their text are saved under work/permits/docs/.", "",
         f"Harvested: {time.strftime('%Y-%m-%d %H:%M %Z')}", "",
         f"GEM statuses: {', '.join(plant['statuses'])}. City in GEM: {plant['city'] or 'blank'}. "
         f"County in GEM: {plant['county'] or 'blank'}.", ""]
    if plant["id"] in APCD_PLANTS:
        L += ["This plant is in Jefferson County, so its air permits come from the Louisville APCD, not the state "
              "record. The APCD's active permits page lists operating permits only; construction permits (for "
              "example new units) are found in the proposed actions page while at comment, in LG&E's commission "
              "filings, or by an open records request to the APCD.", ""]
    if not matched:
        L += ["No permit facility matched this plant. That does not mean it has no permits: it may be filed under "
              "the owner, a contractor or another site name. Check _unmatched.md and _sweep.md in this folder, and "
              "search eSearch by the owner's name.", ""]
    elif not any(f["docs"] for f, _ in matched):
        L += ["The matched facilities have no documents online. eSearch lists documents for approvals from about "
              f"2023 on; older permits need an open records request to the Division for Air Quality ({RECORDS}).", ""]
    for f, how in matched:
        L += fac_block(f, how) + [""]
    path.write_text("\n".join(L), encoding="utf-8")


def slim(f):
    """A facility as facilities.json and index.json keep it: no full document text."""
    return {"key": f["key"], "name": f["name"], "source": f["source"], "company": f["company"],
            "county": f["county"], "city": f["city"], "address": "", "codes": [], "hint": f.get("hint", ""),
            "ai": f["ai"], "found_by": f["found_by"],
            "activities": f["activities"][:40], "links": f["links"],
            "permits": f["permits"] + [{"number": a["activity"], "type": a["type"], "status": a["status"],
                                        "step": a["milestone"], "comment_ends": ""} for a in f["activities"][:10]],
            "docs": [{k: d[k] for k in ("number", "name", "type", "date", "url", "state", "file", "facts", "how", "activity")
                      if k in d} for d in f["docs"]]}


# ----------------------------------------------------------------- plants ---

def load_plants(args=None, csv_path=None):
    csv = pd.read_csv(csv_path or CSV, low_memory=False, encoding="utf-8-sig")
    csv = csv[csv["State/Province"] == "Kentucky"]
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


# ------------------------------------------------------------------- main ---

def main():
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n\n")[0])
    ap.add_argument("--scope", required=True, help="batch folder name, e.g. us-ky")
    ap.add_argument("--plants", help="comma-separated GEM location IDs (default: every plant); "
                    "reads only their facilities' documents and skips the sweep")
    ap.add_argument("--match-only", action="store_true", help="list matches only, no document reads")
    ap.add_argument("--no-sweep", action="store_true", help="skip the sweep of non-power names")
    ap.add_argument("--docs-per-facility", type=int, default=15)
    ap.add_argument("--activities-per-facility", type=int, default=12,
                    help="list documents for this many of a facility's newest activities that have any")
    ap.add_argument("--sweep-read", type=int, default=150,
                    help="read the first pages of this many approvals at non-power names")
    ap.add_argument("--sweep-from", default="2023-01-01", help="oldest approval date the sweep reads")
    ap.add_argument("--pages", type=int, default=4, help="pages read from a document read only by the sweep")
    args = ap.parse_args()

    out_dir = harvest_out(args.scope)
    hv_dir = REPO / "batches" / args.scope / "harvest"
    hv_dir.mkdir(parents=True, exist_ok=True)
    plants = load_plants(args)
    stamp = time.strftime("%Y-%m-%d")

    es = ESearch()
    issued, pending = es.search("IssuedApprovals"), es.search("PendingApproval")
    if issued is None or pending is None:
        log("eSearch statewide search failed; see the errors in harvest_summary.md")
    (out_dir / "esearch").mkdir(exist_ok=True)
    (out_dir / "esearch" / f"{stamp}.json").write_text(json.dumps(
        {"read": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "issued": issued or [], "pending": pending or []}),
        encoding="utf-8")
    facs = esearch_facilities(issued, pending)
    log(f"eSearch: {len(issued or [])} issued and {len(pending or [])} pending air approvals at {len(facs)} agency interests")

    page = get(DAQ_NOTICES)
    notices = parse_notices(page.text) if page.status == "200" else {}
    if page.status != "200":
        report_failure(DAQ_NOTICES, page.status, "DAQ notices page")
    facs.update(notice_facilities(notices))
    act, prop = get(APCD_ACTIVE), get(APCD_PROPOSED)
    active = parse_apcd_active(act.text) if act.status == "200" else []
    proposed = parse_apcd_proposed(prop.text) if prop.status == "200" else []
    for p, url in ((act, APCD_ACTIVE), (prop, APCD_PROPOSED)):
        if p.status != "200":
            report_failure(url, p.status, "Louisville APCD page")
    facs.update(apcd_facilities(active, proposed))
    log(f"DAQ notices: {len(notices)} facilities. Louisville: {len(active)} active permit entries, {len(proposed)} proposed actions")

    matches = {p["id"]: match(p, list(facs.values())) for p in plants}
    matched_keys = {f["key"] for ms in matches.values() for f, _ in ms}
    power = [f for f in facs.values() if f["key"] in matched_keys or is_power(f)]

    if args.match_only:
        for p in plants:
            for f, how in matches[p["id"]] or [(new_fac("", "no match", ""), "")]:
                print(f"{p['id']}\t{p['name']}\t{f['name']}\t{f['key']}\t{how}")
        for f in power:
            if f["key"] not in matched_keys:
                print(f"UNMATCHED\t\t{f['name']}\t{f['key']}\t{f['city']}\t{f['county']}")
        return

    # 4. the sweep: newest initial and revision approvals with documents at non-power names
    sweep_log = []
    if not args.no_sweep and not args.plants:
        cands = [(a, f) for f in facs.values() if f["source"] == "eSearch" and f["key"] not in matched_keys
                 and not is_power(f) for a in f["activities"]
                 if a["documents"] and SWEEP_TYPES.search(a["type"]) and (a["issued"] or a["milestone_date"]) >= args.sweep_from]
        cands.sort(key=lambda x: x[0]["issued"] or x[0]["milestone_date"], reverse=True)
        seen = set()
        for n, (a, f) in enumerate(cands, 1):
            if len(seen) >= args.sweep_read:
                break
            if f["key"] in seen:
                continue
            seen.add(f["key"])
            docs = rank_docs(es.documents(a))
            if not docs:
                continue
            d = docs[0]
            text = read_doc(es, out_dir, f, d, pages=args.pages, ocr=False)
            why = sweep_keep(text)
            sweep_log.append({"facility": f["name"], "ai": f["ai"], "activity": f"{a['activity']} {a['type']}",
                              "document": d["name"], "url": d["url"], "kept": why})
            if why:
                f["hint"] = hint_of(text)
                f["found_by"].append(f"the sweep read {d['name']} and it {why}")
                f["docs"].append({**d, "how": "sweep"})
                power.append(f)
            if len(seen) % 25 == 0:
                log(f"  sweep read {len(seen)} facilities")
        log(f"sweep: {len(cands)} approvals with documents since {args.sweep_from}, {len(seen)} facilities read, "
            f"{sum(1 for s in sweep_log if s['kept'])} kept")

    unmatched = [f for f in power if f["key"] not in matched_keys]
    log(f"{len(facs)} facilities: {len(power)} power-like, {len(matched_keys)} matched, {len(unmatched)} unmatched")

    # 3 and 5. list and read every matched or power-like facility's documents
    todo = [f for f in power if f["key"] in matched_keys] if args.plants else power
    for k, f in enumerate(todo, 1):
        acts = [a for a in f["activities"] if a["documents"]][:args.activities_per_facility]
        have = {d["key"] for d in f["docs"]}
        for a in acts:
            for d in es.documents(a):
                if d["key"] not in have:
                    have.add(d["key"])
                    f["docs"].append({**d, "how": "eSearch"})
        if f["source"].startswith("Louisville"):
            for x in f["links"]:
                if "/document/" not in x["url"]:
                    continue
                pdf = apcd_pdf(x["url"])
                if pdf and pdf not in have:
                    have.add(pdf)
                    f["docs"].append({"number": x["number"], "name": x["kind"], "type": x["kind"],
                                      "date": x.get("effective", ""), "url": pdf, "page": x["url"],
                                      "how": "Louisville APCD media page", "key": pdf})
                elif not pdf:
                    report_failure(x["url"], "200", "Louisville media page gave no PDF address")
        f["docs"] = rank_docs(f["docs"])
        for n, d in enumerate(f["docs"]):
            if n >= args.docs_per_facility:
                d["state"] = "not read (cap)"
            elif "facts" not in d or d.get("how") == "sweep":
                read_doc(es, out_dir, f, d)
        log(f"({k}/{len(todo)}) {f['name']}: {min(len(f['docs']), args.docs_per_facility)} of {len(f['docs'])} documents read")

    with (out_dir / "harvest_log.jsonl").open("a", encoding="utf-8") as logf:
        for p in plants:
            write_index(out_dir / f"{p['id']}.md", p, matches[p["id"]])
            logf.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "plant": p["id"], "name": p["name"],
                                   "facilities": [{"name": f["name"], "key": f["key"], "how": how,
                                                   "docs": {d["name"]: d.get("state", "not read") for d in f["docs"]}}
                                                  for f, how in matches[p["id"]]]}) + "\n")

    L = ["# Kentucky facilities that look like power or data center sites but match no GEM plant in this batch", "",
         "Each may be a plant outside this batch, a plant GEM lacks, a backup generator fleet at a data center or "
         "another site, or not a power plant at all. Check engines or turbines of 50 MW or more in total "
         "(generating capacity only). Entries found by the sweep were read because their documents name a data "
         "center or list generators.", ""]
    for f in sorted(unmatched, key=lambda f: f["name"].lower()):
        L += fac_block(f) + [""]
    if not unmatched:
        L.append("None this run.")
    (out_dir / "_unmatched.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    L = [f"# Sweep of approvals at names that do not look like power sites ({len(sweep_log)} read)", "",
         f"The newest initial and revision approvals with documents since {args.sweep_from}, one document each "
         f"(first {args.pages} pages). Kept ones moved to _unmatched.md.", ""]
    L += [f"- {'KEPT, ' + s['kept'] + ': ' if s['kept'] else ''}{s['facility']} (agency interest {s['ai']}), "
          f"{s['activity']}, {s['document']}: {s['url']}" for s in sweep_log]
    (out_dir / "_sweep.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    index = {"harvested": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
             "esearch": {"issued": len(issued or []), "pending": len(pending or [])},
             "daq_notices": len(notices), "apcd_active": len(active), "apcd_proposed": len(proposed),
             "plants": {p["id"]: {"name": p["name"], "facilities": [{"key": f["key"], "name": f["name"], "how": how}
                                                                    for f, how in matches[p["id"]]]} for p in plants},
             "unmatched": [f["key"] for f in unmatched],
             "facilities": {f["key"]: slim(f) for f in power},
             "esearch_errors": es.errors}
    (out_dir / "index.json").write_text(json.dumps(index, indent=1), encoding="utf-8")
    (hv_dir / "facilities.json").write_text(json.dumps({
        "harvested": index["harvested"], "matches": index["plants"],
        "unmatched": [slim(f) for f in unmatched],
        "matched": [slim(f) for f in power if f["key"] in matched_keys]}, indent=1), encoding="utf-8")

    S = [f"# Kentucky air permit harvest, {stamp}", "",
         f"eSearch: {len(issued or [])} issued and {len(pending or [])} pending air approvals. DAQ notices: "
         f"{len(notices)} facilities. Louisville APCD: {len(active)} active permit entries, {len(proposed)} proposed "
         f"actions. Facilities: {len(facs)}. Power-like: {len(power)}. Matched to GEM plants: {len(matched_keys)}. "
         f"Unmatched: {len(unmatched)}. Sweep: {len(sweep_log)} read, {sum(1 for s in sweep_log if s['kept'])} kept.", "",
         f"eSearch calls: {es.calls}.", ""]
    if es.errors:
        S += ["eSearch calls that failed after three tries (retry before concluding anything):", ""]
        S += [f"- {e}" for e in es.errors[:40]] + [""]
    S += ["## Matches per GEM plant", ""]
    for p in plants:
        ms = matches[p["id"]]
        S.append(f"- {p['name']} ({p['id']}): " + ("; ".join(f"{f['name']} ({f['key']}, {how})" for f, how in ms)
                                                   if ms else "no facility matched"))
    S += ["", "## Unmatched power-like facilities", ""]
    S += [f"- {f['name']} ({f['city'] or '?'}, {f['county'] or '?'} County; {f['source']})"
          for f in sorted(unmatched, key=lambda f: f["name"].lower())]
    (hv_dir / "harvest_summary.md").write_text("\n".join(S) + "\n", encoding="utf-8")
    log("done")


if __name__ == "__main__":
    main()

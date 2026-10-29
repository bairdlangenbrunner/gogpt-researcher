"""
Harvest Kansas air construction permits before a research sweep.

Kansas Department of Health and Environment (KDHE) Bureau of Air permits live
in KEIMS (Kansas Environmental Information Management System,
keims.kdhe.ks.gov/nsuite/ncore/), a Windsor Solutions nSuite AngularJS single
page app. The pages need a script, and the site search needs a login, but
several of its JSON services answer anonymously. What was found (2026-10-21):

  Anonymous, used here
  - KEIMS public notice list: GET /nsuite/ncore/ss/publicnoticeslist. Every
    program (air, water, waste) currently out for public comment: site, permit
    number and version, notice type, comment dates, county, address, latitude
    and longitude of the site.
  - KEIMS public notice documents: GET /nsuite/ncore/ss/publicnoticedocuments
    with queryParams={"filter":[{"publicNoticeId":ID}]}, then each file by
    GET /nsuite/ncore/DownloadFile/<document id> (a plain PDF, no login).
  - The KDHE Bureau of Air public notice page (kdhe.ks.gov/413/Public-Notices):
    the air permits on public notice with site id, tracking number, address,
    permit type, comment end date and PDF links (/DocumentCenter/View/N). The
    live page lists only the current notices (and a few recent ones), so this
    script also reads every distinct Wayback Machine snapshot of the page
    (2022 onward) to recover notices that have since come down. The PDFs
    themselves stay on the KDHE document center and download by plain request.

  Needs a login, not usable
  - KEIMS site search, permit search and the permit and document lists
    (/ss/sitesearch, /ss/permitslist, ...) answer 401 "IAM session is invalid".
  - The "Data Explorer" (keims.kdhe.ks.gov/nsuite/nsite/) loads, and its public
    mode says it continues as a public user, but its service proxy
    (/nsuite/nsite/ss/explorersites, explorersitefilter ...) fails for every
    request with HTTP 400 "Value cannot be null (uriString)": the server's
    services host setting is empty. The site profile pages it links to are
    the same single page app. Retry it from time to time.
  - The Kansas Register (now rules.ks.gov, an Esper single page app whose API
    returns 403) was not usable; the old kssos.org Register URLs redirect to
    that site.

So the harvest covers permits and applications that were on public notice,
not every permit ever issued. A permit issued without a public notice (a minor
construction approval) is not here; ask KDHE for it through KORA (open
records) or check it in KEIMS with a login.

The document center deletes a notice's PDFs soon after the comment period
closes (live links answer 404), but the Wayback Machine holds most of them at
web.archive.org/web/2id_/<document center address>, which read_docs() tries
when the live link fails. The archive stores most of them under the LONG
address (/View/52540/Evergy-Viola-Energy-Center-Permit-Summary-PDF?bidId=),
not the bare /View/52540 the notice table links, so wayback_copy() asks the
archive's index for every saved address that starts with the document number
and reads the newest good one (found 2026-10-23, after about 60 documents were
wrongly written off as having no archive copy).

Steps:
  1. Read the KEIMS notice list (air only) and its documents.
  2. Read the KDHE notice page, now and in every Wayback snapshot.
  3. Merge the two by tracking number.
  4. Match each GEM Kansas plant to records. KNOWN holds hand-checked name
     patterns; a name-word match adds more, marked for checking.
  5. Download the documents of every matched record (and of power-like
     records that match no plant) through fetch.py (disk cache in
     work/fetch_cache/, so url_verifier.py reads them at once) and keep the
     lines that give the permit number, equipment, manufacturer, model, sizes
     (MW, kW, MMBtu/hr, horsepower) and the site address or coordinates.

Output: one plain-text index per plant under work/permits/<scope>/<GEM
location id>.md, plus _unmatched.md, _notices.md (every air notice read) and
harvest_log.jsonl. Permit PDFs name agency and company staff with their
contact details: they stay in work/ (never committed). Nothing here stages a
record.

Usage (from scripts/):
    python harvest_permits_kansas.py --scope us-ks                    # every plant
    python harvest_permits_kansas.py --scope us-ks --plants L100001043000,L100001023601
    python harvest_permits_kansas.py --scope us-ks --match-only       # list matches, download no documents
    python harvest_permits_kansas.py --scope us-ks --no-wayback       # current notices only
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch import CHROME_UA, fetch_page  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
KEIMS = "https://keims.kdhe.ks.gov/nsuite/ncore"
KDHE = "https://www.kdhe.ks.gov"
NOTICE_PAGE = f"{KDHE}/413/Public-Notices"
CDX = "http://web.archive.org/cdx/search/cdx"
CSV = REPO / "scripts" / "gem_export_gogpt_scoped.csv"

# Hand-checked name patterns (2026-10-21): GEM plant -> regexes that must hit
# the facility name or address of a KEIMS/KDHE record. A plant missing here is
# matched by its name words, and those matches are marked for checking.
KNOWN = {
    "L100001043000": [r"viola"],                                   # Viola Generating Station
    "L100001023601": [r"mc ?new"],            # McNew Generating Station
    "L100001023564": [r"walnut energy", r"kansas power pool"],     # Walnut Energy Center, Winfield
    "L100000103924": [r"lawrence energy", r"lawrence generating"],
    "L100000103922": [r"jeffrey energy"],
    "L100000401931": [r"hutchinson energy", r"hutchinson (generating|power)"],
    "L100000401930": [r"emporia energy"],
    "L100000401933": [r"gordon evans"],
    "L100000401792": [r"kaw (power|valley)"],
    "L100000103925": [r"nearman"],
    "L100000103926": [r"quindaro"],
    "L100000401614": [r"cimarron river"],
    "L100000401615": [r"clifton (power|station|generating)", r"sunflower.*clifton"],
    "L100000401616": [r"fort dodge (power|station)", r"sunflower.*dodge city"],
    "L100000402306": [r"sunflower.*garden city", r"garden city (power|station)"],
    "L100000401617": [r"great bend (sunflower|power|station)", r"sunflower.*great bend"],
    "L100000409259": [r"rubart"],
    "L100000401799": [r"mcpherson.*(power|board|energy|station)"],
    "L100000401800": [r"mcpherson.*(power|board|energy|station)"],
    "L100000401782": [r"chanute.*(power|energy|utilit|station)"],
    "L100000409214": [r"coffeyville.*(power|electric|municipal|energy)", r"cml ?&? ?p"],
    "L100000103927": [r"riverton (power|plant|station)", r"empire district.*riverton"],
    "L100000401935": [r"osawatomie"],
    "L100000401936": [r"west gardner", r"gardner (energy|power|station)"],
    "L100000409209": [r"goodman energy"],
}

POWER_NAME = re.compile(
    r"power|electric|generat|energy center|turbine|municipal (util|power)|utilit|evergy|westar|"
    r"sunflower|midwest energy|kansas gas|empire district|\bkpp\b|\bkepco\b|ameren|nextera|"
    r"data cent|datacent|peaking|\bcogen", re.I)
POWER_DROP = re.compile(r"ethanol|packing|biodiesel|fiberglass|aviation|gas processing|asphalt|"
                        r"feedlot|quarry|elevator|manufactur|refiner", re.I)
NAME_NOISE = re.compile(
    r"\b(power station|power plant|generating station|generating|station|energy center|energy|"
    r"plant|power|gt|ks|kansas|the|municipal|of|and|city|llc|inc|company|co|irp|evergy|facility)\b", re.I)
EQUIPMENT = re.compile(r"turbine|\bct\b|engine|rice\b|generat|\bgen\b|boiler|duct burner|hrsg|"
                       r"combined cycle|peaking|diesel|reciprocating|genset", re.I)
SIZE = re.compile(r"\d[\d,.]*\s*(MW|MWe|megawatt|kW|kilowatt|MMBtu|mmbtu|hp|horsepower|bhp)\b")
MAKER = re.compile(r"manufactur|model\b|caterpillar|cat g|wartsila|w[äa]rtsil[äa]|jenbacher|"
                   r"general electric|\bGE\b|siemens|solar turbines|mitsubishi|cummins|rolls[- ]royce|"
                   r"mtu\b|kohler|generac|waukesha|baldor|clarke|detroit diesel|pratt|ansaldo|"
                   r"hitachi|titan \d|taurus|mars \d|lm ?\d{4}|7ea|7fa|6b\b", re.I)
LOCATION = re.compile(
    r"latitude|longitude|\blat\b|\blong\b|\bUTM\b|\bsection \d+|township|\bT ?\d+ ?S\b.*\bR ?\d+ ?[EW]|"
    r"located (at|in|on|near|approximately)|physical address|site address|facility address|"
    r"street address|mailing address|\b\d{2,5} [A-Z0-9][\w. ]+ (road|rd|street|st|avenue|ave|"
    r"highway|hwy|drive|dr|lane|ln|blvd|boulevard)\b|county,? kansas|ks 6\d{4}|kansas 6\d{4}", re.I)
LATLON = re.compile(r"\b(3[6-9]\.\d{3,})\s*[,;/ ]\s*-?\s*(9[4-9]\.\d{3,}|10[0-2]\.\d{3,})\b")


def log(msg):
    print(f"[harvest-ks] {msg}", file=sys.stderr, flush=True)


def clean(s):
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s or "", flags=re.S | re.I)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def get(url, timeout=120):
    return fetch_page(url, timeout=timeout)


def wayback_copy(url, tries=4):
    """Find the newest saved copy of a document center address, bare or long.

    Returns (snapshot address or "", note). The note says why nothing was found:
    "no copy" only when the index answered and held no match; "index offline"
    when it never answered, so the caller must not treat that as a verdict."""
    m = re.search(r"/DocumentCenter/View/(\d+)", url)
    if not m:
        return "", "not a document center address"
    num = m.group(1)
    prefix = f"www.kdhe.ks.gov/DocumentCenter/View/{num}"
    for i in range(tries):
        try:
            r = requests.get(CDX, params={"url": prefix, "matchType": "prefix", "output": "json",
                                          "fl": "timestamp,original,statuscode",
                                          "filter": "statuscode:200", "limit": 50}, timeout=120)
            rows = r.json()[1:]
        except (requests.RequestException, ValueError):
            time.sleep(10 * (i + 1))
            continue
        rows = [x for x in rows if re.search(rf"/View/{num}(?:/|\?|$)", x[1])]
        if not rows:
            return "", "no copy"
        ts, orig = max(rows)[:2]
        return f"https://web.archive.org/web/{ts}/{orig}", "found"
    return "", "index offline"


def words(text):
    t = NAME_NOISE.sub(" ", re.sub(r"\(.*?\)", " ", str(text or "")))
    return {w.lower() for w in re.split(r"[^A-Za-z]+", t) if len(w) >= 4}


def tracking_key(s):
    return re.sub(r"\s+", "", str(s or "")).upper()


# ------------------------------------------------------------------ KEIMS ---

def keims_get(service, filt=None, retries=2):
    params = {"queryParams": json.dumps({"filter": filt or []}), "includeMetadataInResponse": "false"}
    last = None
    for _ in range(retries + 1):
        try:
            r = requests.get(f"{KEIMS}/ss/{service}", params=params,
                             headers={"User-Agent": CHROME_UA, "Accept": "application/json"}, timeout=90)
            if r.status_code == 200:
                return r.json().get("queryResults", [])
            last = f"HTTP {r.status_code} {r.text[:120]}"
        except (requests.RequestException, ValueError) as e:
            last = str(e)
        time.sleep(2)
    log(f"KEIMS {service}: {last}")
    return None


def keims_notices():
    """Air public notices currently open in KEIMS, each with its documents."""
    rows = keims_get("publicnoticeslist", [{"programAreaId": "AIR"}])
    if rows is None:
        return None
    out = []
    for x in rows:
        docs = keims_get("publicnoticedocuments", [{"publicNoticeId": x["id"]}]) or []
        out.append({
            "source": "KEIMS",
            "facility": re.sub(r"\s*\(Air\)\s*$", "", x.get("siteName") or ""),
            "tracking": x.get("permitNumber") or "",
            "site_id": "",
            "address": ", ".join(p for p in [x.get("address1"), x.get("city"), x.get("stateId"),
                                             x.get("zipCode")] if p and p != "UNKNOWN"),
            "county": x.get("countyDescription") or "",
            "type": x.get("publicNotificationTypeDescription") or "",
            "start": (x.get("startDate") or "")[:10], "end": (x.get("endDate") or "")[:10],
            "lat": x.get("latitude"), "lon": x.get("longitude"),
            "profile": x.get("siteProfileUrl") or "",
            "docs": [{"name": d["documentName"], "url": f"{KEIMS}/DownloadFile/{d['id']}",
                      "updated": (d.get("updatedDate") or "")[:10]} for d in docs],
        })
    return out


# ------------------------------------------------------- KDHE notice page ---

def parse_notice_page(text):
    """Rows of the 'Proposed Air Quality Permits' table: site id, tracking
    number, facility, address, permit type, comment end date, document links."""
    out = []
    i = text.find("Proposed Air Quality")
    body = text[i:] if i >= 0 else text
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", body, re.S):
        tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
        if len(tds) < 3:
            continue
        a = [clean(x) for x in re.split(r"<br\s*/?>", tds[0]) if clean(x)]
        b = [clean(x) for x in re.split(r"<br\s*/?>", tds[1]) if clean(x)]
        if not a or not b:
            continue
        if len(b) == 1:     # older snapshots run the whole cell together
            m = re.match(r"(.*?)\s(\d{2,5}\s.*?)\s(Class .*|Construction .*|PSD .*|Comment End.*)$", b[0])
            if m:
                b = [m.group(1), m.group(2), m.group(3)]
                b = b[:2] + [x.strip() for x in re.split(r"(?=Comment End Date:)", b[2]) if x.strip()]
        end = next((re.sub(r"^Comment End Date:\s*", "", x) for x in b if x.startswith("Comment End")), "")
        rest = [x for x in b[1:] if not x.startswith("Comment End")]
        docs = []
        for h, t in re.findall(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>', tds[2], re.S):
            h = html.unescape(h)
            if h.startswith("/"):
                h = KDHE + h
            if "DocumentCenter" in h:
                docs.append({"name": clean(t), "url": h})
        out.append({"source": "KDHE page",
                    "facility": b[0], "tracking": a[1] if len(a) > 1 else "", "site_id": a[0],
                    "address": rest[0] if rest else "", "county": "",
                    "type": rest[1] if len(rest) > 1 else "", "start": "", "end": end,
                    "lat": None, "lon": None, "profile": "", "docs": docs})
    return out


def kdhe_notices(wayback=True, limit=0):
    """Records from the live KDHE page and every distinct Wayback snapshot of it."""
    recs = []
    live = get(NOTICE_PAGE)
    if live.status == "200":
        for r in parse_notice_page(live.text):
            r["seen"] = "now"
            recs.append(r)
    else:
        log(f"KDHE notice page: HTTP {live.status}")
    snaps = []
    if wayback:
        try:
            r = requests.get(CDX, params={"url": "kdhe.ks.gov/413/Public-Notices", "output": "json",
                                          "fl": "timestamp", "filter": "statuscode:200",
                                          "collapse": "digest", "limit": 1000}, timeout=120)
            snaps = [x[0] for x in r.json()[1:]]
        except (requests.RequestException, ValueError) as e:
            log(f"Wayback index: {e}")
        if limit:
            snaps = snaps[-limit:]
        for ts in snaps:
            url = f"https://web.archive.org/web/{ts}id_/https://www.kdhe.ks.gov/413/Public-Notices"
            p = get(url, timeout=180)
            if p.status != "200":
                log(f"  snapshot {ts}: HTTP {p.status}")
                continue
            for r in parse_notice_page(p.text):
                r["seen"] = ts[:8]
                recs.append(r)
        log(f"Wayback: {len(snaps)} snapshots read")
    return recs, len(snaps)


# ------------------------------------------------------------ merge, match ---

def merge(keims, kdhe):
    """One record per tracking number; documents and sources are unioned."""
    out = {}
    for r in (keims or []) + kdhe:
        key = tracking_key(r["tracking"]) or tracking_key(r["facility"] + r["type"])
        m = out.setdefault(key, {**r, "docs": [], "sources": set(), "seen": set()})
        m["sources"].add(r["source"])
        if r.get("seen"):
            m["seen"].add(r["seen"])
        for f in ("site_id", "address", "county", "type", "start", "end", "profile", "lat", "lon"):
            if not m.get(f) and r.get(f):
                m[f] = r[f]
        urls = {d["url"] for d in m["docs"]}
        for d in r["docs"]:
            if d["url"] not in urls:
                m["docs"].append(d)
                urls.add(d["url"])
    return list(out.values())


def record_text(r):
    return f"{r['facility']} {r['address']}".lower()


def match(plant, records):
    """[(record, how)] for one plant: hand-checked patterns first, else every
    distinctive word of the plant's name plus its city."""
    out = []
    pats = KNOWN.get(plant["id"])
    if pats:
        for r in records:
            if any(re.search(p, record_text(r)) for p in pats):
                out.append((r, "checked by hand"))
        return out
    ws = plant["name_words"]
    city = plant["city"].lower()
    for r in records:
        t = record_text(r)
        if ws and ws <= words(t):
            out.append((r, "name match, check it is this plant"))
        elif city and city in t and POWER_NAME.search(r["facility"]) and not POWER_DROP.search(r["facility"]):
            out.append((r, "same city, power-like name, check it is this plant"))
    return out


# --------------------------------------------------------- document facts ---

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
    latlon = [f"{a}, -{b.lstrip('-')}" for a, b in LATLON.findall(text)][:3]
    return {
        "ids": pick(text, re.compile(r"permit (no|number|#)|tracking|source id|CSP\d|OP\d{6}|"
                                     r"application (no|number)", re.I), 4),
        "equipment": pick(text, EQUIPMENT, 10),
        "makers": pick(text, MAKER, 8),
        "sizes": pick(text, SIZE, 10),
        "location": pick(text, LOCATION, 8),
        "coords": latlon,
    }


def read_docs(rec, cap=8):
    """Download a record's documents (not the Spanish copies) and keep facts."""
    n = 0
    for d in rec["docs"]:
        if re.search(r"espanol|spanish|espa", d["name"], re.I):
            d["state"] = "skipped (Spanish copy)"
            continue
        if n >= cap:
            d["state"] = "not read (cap)"
            continue
        page = get(d["url"], timeout=300)
        ok = page.status == "200" and bool(page.text.strip())
        via = ""
        if not ok and "kdhe.ks.gov/DocumentCenter" in d["url"]:
            # the document center drops a notice's files once it closes; the archive keeps them
            for _ in range(3):
                page = get("https://web.archive.org/web/2id_/" + d["url"], timeout=300)
                if page.status == "200" and page.text.strip():
                    ok, via = True, " (from the Wayback copy)"
                    break
                if page.status == "404":
                    break           # the bare address has no copy; try the long one below
                time.sleep(15)
            if not ok:
                snap, why = wayback_copy(d["url"])
                if snap:
                    ts, _, orig = snap.removeprefix("https://web.archive.org/web/").partition("/")
                    page = get(f"https://web.archive.org/web/{ts}id_/{orig}", timeout=300)
                    if page.status == "200" and page.text.strip():
                        ok, via = True, f" (from the Wayback copy {snap})"
                        d["archive"] = snap
                elif why == "index offline":
                    d["state"] = "not saved, archive index offline (retry)"
        if d.get("state", "").startswith("not saved, archive index"):
            d["facts"] = {}
            n += 1
            continue
        d["state"] = f"saved{via}" if ok else f"not saved, HTTP {page.status}"
        d["facts"] = doc_facts(page.text) if ok else {}
        n += 1


def rec_block(r, full=True):
    seen = sorted(r["seen"]) if r.get("seen") else []
    L = [f"- {r['facility']}: {r['type'] or 'permit notice'}, tracking number {r['tracking'] or 'none shown'}"
         + (f", site id {r['site_id']}" if r["site_id"] else "")]
    L.append(f"    - where: {r['address'] or 'no address on the notice'}"
             + (f", {r['county']} County" if r["county"] else ""))
    if r.get("lat") is not None and r.get("lon") is not None:
        L.append(f"    - the KEIMS notice gives the site point {r['lat']:.6f}, {r['lon']:.6f} "
                 f"(https://www.google.com/maps?q={r['lat']:.6f},{r['lon']:.6f})")
    dates = []
    if r["start"]:
        dates.append(f"comment period {r['start']} to {r['end']}")
    elif r["end"]:
        dates.append(f"comment ends {r['end']}")
    if seen:
        dates.append(f"on the KDHE page snapshots from {seen[0]} to {seen[-1]}")
    if dates:
        L.append("    - " + "; ".join(dates))
    L.append(f"    - read from: {', '.join(sorted(r['sources']))}" + (f"; {r['profile']}" if r["profile"] else ""))
    if full:
        for d in r["docs"]:
            L.append(f"    - document ({d.get('state', 'not read')}): {d['name']}: {d['url']}")
            f = d.get("facts") or {}
            for key, label in (("ids", "numbers"), ("equipment", "equipment"), ("makers", "maker or model"),
                               ("sizes", "size"), ("location", "site address or location"),
                               ("coords", "coordinates")):
                for line in f.get(key, []):
                    L.append(f"        - {label}: {line}")
    return L


# ---------------------------------------------------------------- plants ---

def load_plants(args):
    csv = pd.read_csv(CSV, low_memory=False)
    csv = csv[csv["State/Province"] == "Kansas"]
    wanted = set(args.plants.split(",")) if args.plants else None
    plants = []
    for pid, rows in csv.groupby("GEM location ID", sort=False):
        if wanted is not None and pid not in wanted:
            continue
        r = rows.iloc[0]
        if re.search(r"IRP power station", str(r["Plant name"])):
            continue            # unsited placeholder rows
        others = [x.strip() for x in str(r.get("Other Name(s)") or "").split(";")
                  if x.strip() and x.strip() != "nan"]
        city = r.get("City") if isinstance(r.get("City"), str) else ""
        plants.append({"id": pid, "name": r["Plant name"], "city": city, "other_names": others,
                       "statuses": sorted(set(rows["Status"].astype(str))),
                       "name_words": words(r["Plant name"])})
    return plants


def write_index(path, plant, matched):
    L = [f"# Kansas air permit files for {plant['name']} ({plant['id']})", "",
         "Source: KDHE Bureau of Air public notices (KEIMS public notice list and documents, "
         "keims.kdhe.ks.gov/nsuite/ncore/, and the KDHE public notice page with its Wayback snapshots). "
         "Only permits and applications that went on public notice are listed; KEIMS site and permit "
         "search needs a login. Documents marked saved are in the local fetch cache, so "
         "`python scripts/fetch.py <url> --text` and `url_verifier.py` read them at once.", "",
         f"Harvested: {time.strftime('%Y-%m-%d %H:%M %Z')}", "",
         f"GEM statuses: {', '.join(plant['statuses'])}. City in GEM: {plant['city'] or 'blank'}.", ""]
    if not matched:
        L += ["No public notice record matched this plant. That does not mean it has no permits: only "
              "notices are visible without a login. Check _notices.md and _unmatched.md in this folder "
              "for power facilities under another name, and ask KDHE (KORA request) or check KEIMS "
              "with a login for permits issued without a notice.", ""]
    for r, how in sorted(matched, key=lambda m: m[0]["end"] or "", reverse=True):
        L += [f"Matched: {how}."] + rec_block(r) + [""]
    path.write_text("\n".join(L), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--scope", required=True, help="batch folder name, e.g. us-ks")
    ap.add_argument("--plants", help="comma-separated GEM location IDs (default: every plant)")
    ap.add_argument("--match-only", action="store_true", help="list matches, download no documents")
    ap.add_argument("--no-wayback", action="store_true", help="skip the Wayback snapshots of the KDHE page")
    ap.add_argument("--snapshots", type=int, default=0, help="read only the newest N snapshots (0 = all)")
    ap.add_argument("--docs-per-record", type=int, default=8)
    args = ap.parse_args()

    out_dir = REPO / "work" / "permits" / args.scope
    out_dir.mkdir(parents=True, exist_ok=True)
    plants = load_plants(args)
    keims = keims_notices()
    log(f"KEIMS air notices open now: {len(keims) if keims is not None else 'list did not load'}")
    kdhe, nsnap = kdhe_notices(wayback=not args.no_wayback, limit=args.snapshots)
    records = merge(keims, kdhe)
    log(f"{len(records)} distinct air notices ({len(kdhe)} KDHE page rows over {nsnap} snapshots)")
    matches = {p["id"]: match(p, records) for p in plants}

    if args.match_only:
        for p in plants:
            for r, how in matches[p["id"]] or [({"facility": "no match", "tracking": "", "end": ""}, "")]:
                print(f"{p['id']}\t{p['name']}\t{r['facility']}\t{r['tracking']}\t{r['end']}\t{how}")
        return

    matched_keys = {tracking_key(r["tracking"]) for ms in matches.values() for r, _ in ms}
    unmatched = [r for r in records if tracking_key(r["tracking"]) not in matched_keys
                 and POWER_NAME.search(r["facility"]) and not POWER_DROP.search(r["facility"])]
    to_read = {tracking_key(r["tracking"]): r for ms in matches.values() for r, _ in ms}
    for r in unmatched:
        to_read[tracking_key(r["tracking"])] = r
    for k, r in enumerate(to_read.values(), 1):
        log(f"({k}/{len(to_read)}) reading {len(r['docs'])} documents of {r['facility']} {r['tracking']}")
        read_docs(r, args.docs_per_record)

    logf = (out_dir / "harvest_log.jsonl").open("a", encoding="utf-8")
    for p in plants:
        write_index(out_dir / f"{p['id']}.md", p, matches[p["id"]])
        logf.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "plant": p["id"],
                               "name": p["name"],
                               "records": [{"facility": r["facility"], "tracking": r["tracking"],
                                            "how": how,
                                            "docs": {d["name"]: d.get("state", "not read") for d in r["docs"]}}
                                           for r, how in matches[p["id"]]]}) + "\n")
    logf.close()

    L = ["# Kansas air notices that look like power facilities but match no GEM plant in this batch", "",
         "Each may be a plant outside this batch, a plant GEM lacks, or not a power plant at all. "
         "Check engines or turbines of 50 MW or more in total (generating capacity only).", ""]
    for r in sorted(unmatched, key=lambda r: r["end"] or "", reverse=True):
        L += rec_block(r) + [""]
    if not unmatched:
        L.append("None this run.")
    (out_dir / "_unmatched.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    L = [f"# Every Kansas air public notice read ({len(records)})", "",
         "Open now in KEIMS, or recovered from snapshots of the KDHE notice page.", ""]
    for r in sorted(records, key=lambda r: r["end"] or "", reverse=True):
        L += rec_block(r, full=False) + [f"    - documents: {len(r['docs'])}"]
    (out_dir / "_notices.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    log("done")


if __name__ == "__main__":
    main()

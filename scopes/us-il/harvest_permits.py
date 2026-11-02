"""
Harvest Illinois air permits before a research sweep.

The Illinois EPA's complete permit record is the DocuWare cabinet behind its Document Explorer
(scripts/iepa_docuware.py explains both and holds the client). The public notice page lists only
the permits that went to public notice; construction permits for engine fleets, peakers and most
data center sites never do, which is how the CyrusOne Bilter Road fleet (57 diesel engines, permit
24080019) was missed in October 2026. This script reads the cabinet itself:

  1. Every final air permit (category 03K) and air permit application (03M) filed statewide
     since --since (default 2021-01-01), plus the correspondence (03N) and permit file (03L)
     entries for the same window, in pages of 1,000 rows. That is the complete list of air
     permits issued in the window, with the site ID, site name, permit number and date of each.
  2. Every cabinet entry, any date, for every GEM plant in the batch: by the plant's site ID when
     KNOWN names one, and by each distinctive word of the plant name and owner (the cabinet's
     site names are owner or project names, in capitals, often abbreviated).
  3. The sites are grouped by site ID. Those that match a GEM plant, and those whose names look
     like power or data center sites, get their address and city from Document Explorer and their
     newest final permits and applications downloaded and read (OCR; nearly every document is a
     scan). The equipment lines (engines, turbines, kW, hp, MW), the permit numbers, the subject
     line, the project sentences and the address lines are kept as facts.

Outputs (scopes/us-il/work/permits/, gitignored; the sweep agents read these):
  <plant id>.md      the cabinet entries and document facts matched to one GEM plant
  _unmatched.md      power-like sites that match no plant in the batch (possible adds)
  _applications.md   every application since --since at a power-like site, newest first
  _dw_air_docs.json  the raw cabinet rows (the statewide permit list for the window)
  docs/<site id>/    the PDFs and their text
  harvest_log.jsonl  one line per plant per run
and batches/<scope>/harvest/facilities.json + harvest_summary.md, which data_center_fleets.py
and the scope brief read.

The address a researcher cites for any document is the Document Explorer record page,
https://webapps.illinois.gov/EPA/DocumentExplorer/Documents/Index/<IEPAID>?dwdocid=<document>,
which fetch.py and url_verifier.py read through the same client.

Usage (from the repo root; needs the saved DocuWare session or Playwright with Chrome):
    python scopes/us-il/harvest_permits.py --scope us-il
    python scopes/us-il/harvest_permits.py --scope us-il-dc --match-only
    python scopes/us-il/harvest_permits.py --scope us-il --plants L100000115044 --docs-per-facility 6
"""
from __future__ import annotations

import argparse
import json
from concurrent.futures import ThreadPoolExecutor
import re
import sys
import time
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from harvest_lib import REPO, CSV, SIZE, clean_ws, pick, merge_facts, harvest_out  # noqa: E402
from iepa_docuware import (Client, de_search, de_record, de_record_url, county_of_site_id,  # noqa: E402
                           AIR_CATEGORIES, PERMIT_CATEGORIES)

STATE = "Illinois"
TAG = "us-il"

# GEM plant id -> cabinet site IDs (Bureau IDs) checked by hand against the site names of the
# 2026-10-30 run. These are always included; the name match adds to them. Add one whenever a sweep
# finds the right site under a name the word match does not reach.
KNOWN = {
    "L100000115044": ["043407AEH", "043407ACW"],   # CyrusOne Bilter Road / Diehl Road, Aurora
    "L100000401731": ["043407AAF"],                # Aurora power station: AURORA GENERATION LLC
    "L100000402251": ["201030BCG", "201030BCO"],   # NRG Rockford I: NRG ROCKFORD ENERGY CENTER (both IDs)
    "L100000402252": ["201030BCG", "201030BCO"],   # NRG Rockford II: same site record
    "L100000103864": ["197809AAO", "197445ACD"],   # Joliet 29: MIDWEST GENERATION LLC, Joliet (AAO is 29, ACD is named Joliet 9)
    "L100000103865": ["197445ACD", "197809AAO"],   # Joliet 9: MIDWEST GENERATION,LLC-JOLIET 9
    "L100000402024": ["103814AAC", "103814AAD"],   # Nelson: INVENERGY NELSON LLC, Rock Falls
    "L100000103868": ["199055ACS"],                # Marion: SOUTHERN ILL POWER-MARION
    "L100000402416": ["167085ABB"],                # Lincoln Land energy center, Pawnee
    "L100000401554": ["197035AAG", "197035AAH", "197808AAG"],  # Elwood Energy facility
    "L100000401569": ["103817AAH"],                # Lee: DYNEGY LEE II LLC, Dixon
    "L100000407358": ["063060AEV"],                # CPV Three Rivers, Morris
    "L100000402389": ["097200ABB"],                # Zion energy center
    "L100000402061": ["197899AAB", "197899AAC"],   # University Park North: UNIVERSITY PARK ENERGY / LSP UNIVERSITY PARK
    "L100000402343": ["197899AAC", "197899AAB"],   # University Park South: same pair, which is which is in the permits
    "L100000402075": ["077806AAA"],                # Grand Tower energy center
    "L100000407695": ["115015BWL"],                # Broadwing Energy Center, Decatur
    "L100000407386": ["115015ABX"],                # Tate & Lyle Decatur: TATE & LYLE INGREDIENTS AMERICAS LLC
}

POWER_NAME = re.compile(
    r"power|electric|generat|energy|cogen|turbine|peak|combined cycle|utilit|municipal|"
    r"data ?cent|datacent|digital|cloud|colocation|hyperscale|compute|server|"
    r"equinix|cyrusone|aligned|stream data|compass|vantage|\bqts\b|microsoft|amazon|\baws\b|google|"
    r"meta platforms|oracle|stack infra|prime data|edged|\bt5\b|novva|edgecore|iron mountain|flexential|"
    r"cologix|element critical|databank|sabey|\b1547\b|ensono|\bntt\b|northern trust data|dipper ventures|"
    r"exelon|constellation|vistra|dynegy|\bnrg\b|midwest gen|calpine|invenergy|ameren|comed|"
    r"commonwealth edison|\bcpv\b|\blsp\b|\bmph\b|kincaid|prairie state|grand tower|"
    r"rockford energy|university park|broadwing|tilton|gibson city energy|crete energy|rocky road|"
    r"shelby county energy|cordova energy|kendall energy|elgin energy|lee ii|southeast chicago|will county|"
    r"duck creek|dallman|pinckneyville|mcleansboro|coffeen|hennepin power|edwards power|newton power|"
    r"peru generating|sullivan power|geneva generating|moline combustion|highland electric|"
    r"princeton municipal|marshall municipal|rochelle municipal|winnetka electric|breese municipal|"
    r"bushnell municipal|carlyle municipal|rantoul electric|city water light", re.I)
# Names that carry a power word but are not power or data center sites.
POWER_DROP = re.compile(
    r"grain|coop\b|cooperative|elevator|farm|feed|ethanol|biodiesel|renewable fuels|agri-energy|asphalt|"
    r"ready mix|concrete|quarry|sand|gravel|landfill|hospital|school|university|college|academy|foundry|"
    r"galvaniz|fastener|silk screen|printing|packaging|wind (farm|tower)|solar|battery builders|lion electric|"
    r"gotion|inventus|\bg & w\b|s&c electric|powertrain|rust-oleum|vantage (chemical|special)|"
    r"advantage foundry|all paws|storage warehouse|terminal|pipeline|pipe line|enbridge|nicor|"
    r"compressor|transmission|substation|\bmgp\b|gas group|energy systems group|power packaging|"
    r"power solutions|chemical|steel|wire|manufactur|\bmfg\b|propane|truck|rail|railway|\brr\b|wood|lumber|"
    r"mill\b|fire dep|police|library|park dist|cabinet|pattern works|shop+ing|cleaners|bridge|highway|"
    r"hwy|water works|frozen foods|motor service|electric equipment|electric motor|industrial electric|"
    r"refinery|oiltanking|flint hills|exxon|tetra process|tac inc|ozinga|residence|training|trng|usarc|"
    r"ammunition|correctional|job corp|union station|auto parts|merinque|\bstp\b|pump house|pond|dukes of|"
    r"clublands|macklin|rust craft|basler|watlow|alstom|gd energy products|ally energy|chip energy|"
    r"compressed energy|energy servers|tri-gen power systems|hoosier energy rec|corn belt energy|"
    r"marquis|sugar camp|williamson energy|hillsboro energy|sivam|tienergy|one winnetka|kendall county|"
    r"kendall new century|prairie state group|pine ash|lincoln park power ho|iit central|edwardsville|"
    r"decatur water works|crawford llc exchange|michigan cogeneration|o'brien cogeneration|"
    r"washington mills|military|naval|army|cat land|ingenco|kms joliet|lincoln generation llc", re.I)
NAME_NOISE = re.compile(
    r"\b(power station|power plant|generating station|generating|generation|cogeneration|cogen|facility|station|energy center|"
    r"energy|center|plant|power|electric|gt|il|illinois|the|municipal|of|and|city|llc|inc|company|co|corp|"
    r"corporation|combined|cycle|county|lp|holdings|group|services|svcs|north|south|east|west|i|ii|iii|iv)\b", re.I)
# Words of an owner string worth a cabinet search (the first distinctive word of each owner).
OWNER_NOISE = re.compile(r"\b(llc|inc|corp|corporation|company|co|lp|holdings|energy|power|generation|"
                         r"generating|partners|capital|group|the|of|and|services|operating|midwest|"
                         r"north|america|american|us|usa|electric|utilities|utility)\b", re.I)

ADDRESS_NAME = re.compile(r"^\d+[\s-]")   # '1520 AURORA AVE' and the like are street addresses, not sites
EQUIPMENT = re.compile(r"turbine|\bengine|generator|genset|\brice\b|boiler|duct burner|hrsg|"
                       r"combined cycle|simple cycle|peaking|diesel|natural gas[- ]fired|reciprocating|"
                       r"emergency|standby|backup", re.I)
MAKER = re.compile(r"model\b|caterpillar|\bcat\b|wartsila|w[äa]rtsil[äa]|jenbacher|general electric|\bGE\b|"
                   r"siemens|solar turbines|mitsubishi|cummins|rolls[- ]royce|\bmtu\b|kohler|generac|"
                   r"waukesha|detroit diesel|pratt|ansaldo|hitachi|titan \d|taurus|mars \d|lm ?\d{4}|"
                   r"7ea|7fa|7ha|6b\b|f-?class|h-?class|3516|3512|c175|qsk|kta", re.I)
LOCATION = re.compile(
    r"latitude|longitude|\blat\b|\blong\b|\bUTM\b|\bsection \d+|township|located (at|in|on|near|approximately)|"
    r"site (address|location)|facility (address|location)|source location|"
    r"\b\d{2,5} [A-Z0-9][\w. ]+ (road|rd|street|st|avenue|ave|highway|hwy|drive|dr|lane|ln|blvd|boulevard|"
    r"parkway|pkwy|court|ct|way)\b|county,? illinois|illinois 6\d{4}|,? il 6\d{4}", re.I)
PROJECT = re.compile(r"proposes|propose to|will consist|project (is|will|consists)|construction of|"
                     r"to construct|new (electric|power|generat|emergency|standby|diesel|natural gas)|"
                     r"install(ation)? of|subject:|applicant's designation|this permit (is|covers|authorizes)", re.I)
IDS = re.compile(r"(?:application|permit|i\.?d\.?)\s*no\.?:?\s*([0-9]{6,9}[A-Z]{0,3})", re.I)
LATLON = re.compile(r"\b(3[6-9]|4[0-2])\.(\d{3,})\D{1,6}-?\s?(8[7-9]|9[01])\.(\d{3,})\b")
FUEL = re.compile(r"\b(diesel|natural gas|distillate|fuel oil|no\. ?2|ULSD|propane|landfill gas|hydrogen|dual[- ]fuel)\b", re.I)
KW = re.compile(r"(\d[\d,.]*)\s*(kW|kilowatt|MW|megawatt|hp|horsepower|bhp|ekW|kWe|MWe)\b", re.I)
SINCE_DEFAULT = "2021-01-01"
HARVEST_CATEGORIES = ("03K", "03M", "03N", "03L")


def log(msg):
    print(f"[harvest-il] {msg}", file=sys.stderr, flush=True)


def words(text):
    t = NAME_NOISE.sub(" ", re.sub(r"\(.*?\)", " ", str(text or "")))
    return {w.lower() for w in re.split(r"[^A-Za-z]+", t) if len(w) >= 4}


def owner_words(owner):
    """Distinctive words of an owner string ('Invenergy Nelson LLC [100%]; ...' -> {'invenergy', 'nelson'})."""
    out = set()
    for part in re.split(r"[;,]", str(owner or "")):
        part = re.sub(r"\[.*?\]|\(.*?\)|\d+%", " ", part)
        part = OWNER_NOISE.sub(" ", part)
        for w in re.split(r"[^A-Za-z]+", part):
            if len(w) >= 5:
                out.add(w.lower())
    return out


def is_power(fac):
    names = " ".join(fac["names"])
    if ADDRESS_NAME.match(fac["names"][0]) or POWER_DROP.search(names):
        return False
    return bool(POWER_NAME.search(names))


# ----------------------------------------------------------------- plants ---

def load_plants(args):
    """Plants of the batch: the ids in --plants, else the sweep's plant list when the batch has
    one, else every Illinois plant in the scoped export."""
    sweep_path = REPO / "batches" / args.scope / "staging" / "sweep_args.json"
    csv_path = CSV
    ids = None
    if sweep_path.exists():
        sweep = json.loads(sweep_path.read_text(encoding="utf-8"))
        csv_path = sweep.get("csv") or CSV
        ids = [p["plant_id"] for p in sweep.get("plants", [])]
    csv = pd.read_csv(csv_path, low_memory=False)
    csv = csv[csv["State/Province"] == STATE]
    wanted = set(args.plants.split(",")) if args.plants else (set(ids) if ids else None)
    plants = []
    for pid, rows in csv.groupby("GEM location ID", sort=False):
        if wanted is not None and pid not in wanted:
            continue
        r = rows.iloc[0]
        others = [x.strip() for x in str(r.get("Other Name(s)") or "").split(";") if x.strip() and x.strip() != "nan"]
        city = r.get("City") if isinstance(r.get("City"), str) else ""
        county = str(r.get("Local area (taluk, county)") or "")
        county = "" if county == "nan" else re.sub(r"\s+County$", "", county, flags=re.I)
        name_words = words(r["Plant name"])
        for o in others:
            name_words |= words(o)
        plants.append({"id": pid, "name": r["Plant name"], "city": city, "county": county, "other_names": others,
                       "owner": str(r.get("Owner(s)") or ""), "statuses": sorted(set(rows["Status"].astype(str))),
                       "name_words": words(r["Plant name"]), "all_words": name_words,
                       "owner_words": owner_words(r.get("Owner(s)"))})
    return plants


# ---------------------------------------------------------------- cabinet ---

def pull_window(client, since, categories=HARVEST_CATEGORIES):
    rows = []
    for cat in categories:
        got = client.query_all(f'[CATEGORY]="{cat}" AND [ITEMDATE] >= "{since}"')
        log(f"category {cat} ({AIR_CATEGORIES.get(cat, '')}) since {since}: {len(got)} documents")
        rows += got
    return rows


def pull_by_name(client, plants):
    """Every cabinet entry for each plant's known site IDs and distinctive words."""
    rows, asked = [], set()
    for p in plants:
        conds = [f'[BUREAUID]="{sid}"' for sid in KNOWN.get(p["id"], [])]
        terms = sorted(w for w in (p["name_words"] | p["owner_words"]) if len(w) >= 5)[:6]
        conds += [f'[SITENAME] LIKE "*{w.upper()}*"' for w in terms]
        for cond in conds:
            if cond in asked:
                continue
            asked.add(cond)
            got = client.query_all(cond, limit=3000)
            if len(got) >= 3000:
                log(f"{cond}: 3,000 or more rows, too common a word, dropped")
                continue
            for r in got:
                r["_by"] = cond
            rows += got
    log(f"{len(asked)} by-name and by-id queries, {len(rows)} rows")
    return rows


def build_facilities(rows):
    """{site id: facility} with the distinct site names and the documents (one per DWDOCID)."""
    facs = {}
    for r in rows:
        sid = str(r.get("BUREAUID") or "").strip()
        if not sid:
            continue
        f = facs.setdefault(sid, {"ai": sid, "names": [], "county": county_of_site_id(sid), "iepaids": [],
                                  "docs": {}, "by": set()})
        nm = clean_ws(r.get("SITENAME"))
        if nm and nm not in f["names"]:
            f["names"].append(nm)
        ie = str(r.get("IEPAID") or "").strip()
        if ie and ie not in f["iepaids"]:
            f["iepaids"].append(ie)
        if r.get("_by"):
            f["by"].add(r["_by"])
        d = f["docs"].setdefault(str(r.get("DWDOCID")), {
            "id": str(r.get("DWDOCID")), "category": r.get("CATEGORY"), "date": str(r.get("ITEMDATE") or ""),
            "permit": str(r.get("PERMITID") or ""), "log": str(r.get("PERMITLOG") or ""),
            "subject": clean_ws(r.get("COMMENTTEXT")), "pages": r.get("DWPAGECOUNT"), "iepaid": ie})
        d["pages"] = d["pages"] or r.get("DWPAGECOUNT")
    for f in facs.values():
        f["name"] = f["names"][0]
        f["docs"] = sorted(f["docs"].values(), key=lambda d: (d["date"], d["id"]), reverse=True)
        f["permits"] = sorted({d["permit"] for d in f["docs"] if d["permit"]}, reverse=True)
    return facs


def fac_text(f):
    return (" | ".join(f["names"]) + " | " + f.get("city", "")).lower()


def match(plant, facs):
    """[(facility, how)]: the hand-checked site IDs, plus every site whose name carries the
    plant's distinctive words. A plant whose name is one word (Aurora, Rockford, Nelson) shares
    it with every school and fire station in town, so a one-word match also needs a power-like
    site name or a word of the owner's name; a site named by a street address never matches
    by words. Last, a power-like site in the plant's city."""
    out, seen = [], set()
    for s in KNOWN.get(plant["id"], []):
        if s in facs:
            out.append((facs[s], "checked by hand"))
            seen.add(s)
    ws = plant["name_words"] - words(plant["city"])
    ows = plant["owner_words"] - words(plant["city"])
    city = plant["city"].lower()
    for f in facs.values():
        if f["ai"] in seen or ADDRESS_NAME.match(f["name"]):
            continue
        fw = words(fac_text(f))
        how = None
        if ws and ws <= fw:
            if len(ws) >= 3 or is_power(f):
                how = "name match, check it is this plant"
        elif len(ws) >= 3 and len(ws & fw) >= len(ws) - 1 and is_power(f):
            how = "most name words match a power-like site, check it is this plant"
        elif ows and (ows & fw) and is_power(f) and (not city or f.get("city", "").lower() == city):
            how = "owner's name on a power-like site in the same city, check it is this plant"
        elif city and f.get("city", "").lower() == city and is_power(f):
            how = "same city, power-like name, check it is this plant"
        if how:
            out.append((f, how))
            seen.add(f["ai"])
    return out


def lookup_site(f, cache=None):
    """Address, city and record id from Document Explorer (by site ID, else the record page).
    Answers are kept in cache (site id -> fields) so a rerun asks the site directory once."""
    if cache is not None and f["ai"] in cache:
        c = cache[f["ai"]]
        f["address"], f["city"], f["zip"], f["de_name"] = c["address"], c["city"], c.get("zip", ""), c.get("de_name", "")
        for ie in c.get("iepaids", []):
            if ie not in f["iepaids"]:
                f["iepaids"].insert(0, ie)
        return
    _lookup_site_live(f)
    if cache is not None and f.get("address") is not None:
        cache[f["ai"]] = {"address": f.get("address", ""), "city": f.get("city", ""), "zip": f.get("zip", ""),
                          "de_name": f.get("de_name", ""), "iepaids": f["iepaids"][:1]}


def _lookup_site_live(f):
    try:
        rows, _ = de_search(interest_id=f["ai"])
    except Exception as e:
        rows = []
        log(f"Document Explorer search failed for {f['ai']}: {e}")
    if rows:
        r = rows[0]
        f["address"] = r["address"]
        f["city"] = r["city"]
        f["zip"] = r["zip"]
        if r["iepaid"] not in f["iepaids"]:
            f["iepaids"].insert(0, r["iepaid"])
        f["de_name"] = r["name"]
        return
    for ie in f["iepaids"]:
        rec = de_record(ie)
        if rec and rec.get("address"):
            f["address"], f["city"], f["de_name"] = rec["address"], rec.get("city", ""), rec["name"]
            return
    f.setdefault("address", "")


def doc_facts(text):
    latlon = [f"{a}.{b}, -{c}.{d}" for a, b, c, d in LATLON.findall(text)][:3]
    sizes = pick(text, KW, 12)
    return {
        "ids": sorted({m.upper() for m in IDS.findall(text)})[:6],
        "project": pick(text, PROJECT, 6),
        "equipment": pick(text, EQUIPMENT, 10),
        "makers": pick(text, MAKER, 6),
        "sizes": sizes or pick(text, SIZE, 10),
        "fuel": sorted({m.lower() for m in FUEL.findall(text)})[:6],
        "location": pick(text, LOCATION, 6),
        "coords": latlon,
    }


def read_docs(client, f, cache_root, cap, max_pages=25):
    """Download and read the newest final permits, then applications, up to cap documents."""
    order = sorted([d for d in f["docs"] if d["category"] in PERMIT_CATEGORIES],
                   key=lambda d: (d["category"] != "03K", d["date"]), reverse=False)
    order = sorted(order, key=lambda d: d["date"], reverse=True)
    order = sorted(order, key=lambda d: d["category"] != "03K")
    for n, d in enumerate(order):
        d["url"] = de_record_url(d["iepaid"] or (f["iepaids"][0] if f["iepaids"] else ""), d["id"])
        if n >= cap:
            d["state"] = "not read (cap)"
            continue
        try:
            text = client.document_text(d["id"], cache_root / f["ai"], max_pages=max_pages)
        except Exception as e:
            d["state"] = f"not read ({e})"
            continue
        d["state"] = "saved" if text.strip() else "saved, no text came out"
        d["facts"] = doc_facts(text) if text.strip() else {}
        d["chars"] = len(text)
    for d in f["docs"]:
        if "url" not in d:
            d["url"] = de_record_url(d["iepaid"] or (f["iepaids"][0] if f["iepaids"] else ""), d["id"])


def fac_block(f, how=None):
    L = [f"- {f['name']} (Illinois EPA site {f['ai']}): {f.get('city', '') or 'city not looked up'}, "
         f"{f['county'] or 'county unknown'} County" + (f"; also listed as {', '.join(f['names'][1:3])}" if len(f["names"]) > 1 else "")]
    if f.get("address"):
        L.append(f"    - where: {f['address']}")
    for ie in f["iepaids"][:2]:
        L.append(f"    - record: {de_record_url(ie)}")
    if f.get("permits"):
        L.append(f"    - permit numbers: {', '.join(f['permits'][:10])}")
    for d in f["docs"][:20]:
        kind = AIR_CATEGORIES.get(d["category"], d["category"])
        line = f"    - {d['date'] or 'no date'}: {kind}, permit {d['permit'] or 'none'}"
        if d.get("subject"):
            line += f", {d['subject']}"
        line += f", {d.get('pages') or '?'} pages"
        if d.get("state"):
            line += f" ({d['state']})"
        line += f": {d.get('url', '')}"
        L.append(line)
        fa = d.get("facts") or {}
        for key, label in (("ids", "permit numbers in the text"), ("project", "project"), ("equipment", "equipment"),
                           ("makers", "maker or model"), ("sizes", "size"), ("fuel", "fuel words"),
                           ("location", "site address or location"), ("coords", "coordinates")):
            v = fa.get(key) or []
            if v:
                if key in ("ids", "fuel", "coords"):
                    L.append(f"        - {label}: {', '.join(v)}")
                else:
                    for line in v:
                        L.append(f"        - {label}: {line}")
    if len(f["docs"]) > 20:
        L.append(f"    - and {len(f['docs']) - 20} more cabinet entries (see _dw_air_docs.json)")
    if how:
        L.insert(0, f"Matched: {how}.")
    return L


def write_index(path, plant, matched, since):
    L = [f"# Illinois air permit files for {plant['name']} ({plant['id']})", "",
         "Source: the Illinois EPA DocuWare cabinet behind Document Explorer, which holds every air permit "
         f"and application the agency has filed (every final permit and application statewide since {since}, "
         "and every entry for this plant's site IDs and name words at any date). A document marked saved has "
         "its text in the local cache, so `python scripts/fetch.py <record address> --text` and "
         "`url_verifier.py` read it at once. The record address is the one to cite.", "",
         f"Harvested: {time.strftime('%Y-%m-%d %H:%M %Z')}", "",
         f"GEM statuses: {', '.join(plant['statuses'])}. City in GEM: {plant['city'] or 'blank'}. "
         f"County in GEM: {plant['county'] or 'blank'}. Owner in GEM: {plant['owner'] or 'blank'}.", ""]
    if not matched:
        L += ["No cabinet site matched this plant by site ID or name. That does not mean it has no permits: "
              "the site may be filed under an older owner, a project company or a street name. Search the "
              "cabinet with `python scripts/iepa_docuware.py query '[SITENAME] LIKE \"*WORD*\"'` and Document "
              "Explorer by city, and check _unmatched.md in this folder.", ""]
    for f, how in matched:
        L += fac_block(f, how) + [""]
    path.write_text("\n".join(L), encoding="utf-8")


def slim(f, how=None):
    return {"ai": f["ai"], "name": f["name"], "names": f["names"], "city": f.get("city", ""),
            "county": f["county"], "address": f.get("address", ""), "iepaids": f["iepaids"],
            "codes": [], "power_like": is_power(f), "how": how,
            "permits": [{"number": n, "type": "air permit"} for n in f["permits"]],
            "applications": [["Air", AIR_CATEGORIES.get(d["category"], d["category"]), d["permit"], d["date"], "filed"]
                             for d in f["docs"] if d["category"] == "03M"],
            "docs": [{"name": f"{AIR_CATEGORIES.get(d['category'], d['category'])} {d['permit']} {d['subject']}".strip(),
                      "url": d.get("url", ""), "date": d["date"], "id": d["id"], "category": d["category"],
                      "pages": d.get("pages"), "state": d.get("state", ""), "facts": d.get("facts", {})}
                     for d in f["docs"]]}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--scope", required=True, help="batch folder name, e.g. us-il or us-il-dc")
    ap.add_argument("--plants", help="comma-separated GEM location IDs (default: the batch's plants)")
    ap.add_argument("--since", default=SINCE_DEFAULT, help="first ITEMDATE of the statewide pull, YYYY-MM-DD")
    ap.add_argument("--match-only", action="store_true", help="list matches, download no documents")
    ap.add_argument("--docs-per-facility", type=int, default=4, help="documents read per site (newest permits first)")
    ap.add_argument("--no-lookup", action="store_true", help="skip the Document Explorer address lookups")
    ap.add_argument("--workers", type=int, default=3, help="sites read at once (download plus OCR)")
    ap.add_argument("--pages", type=int, default=25, help="pages read per document at a matched site")
    ap.add_argument("--pages-unmatched", type=int, default=8,
                    help="pages read per document at an unmatched power-like site (the subject and equipment are up front)")
    ap.add_argument("--reuse-pull", action="store_true",
                    help="read the cabinet rows saved by the last run (_dw_air_docs.json) instead of asking again")
    args = ap.parse_args()

    out_dir = harvest_out(args.scope)
    hv_dir = REPO / "batches" / args.scope / "harvest"
    hv_dir.mkdir(parents=True, exist_ok=True)
    cache_root = out_dir / "docs"
    plants = load_plants(args)
    log(f"{len(plants)} GEM plants in scope {args.scope}")

    client = Client()
    pull_path = out_dir / "_dw_air_docs.json"
    saved = json.loads(pull_path.read_text(encoding="utf-8")) if args.reuse_pull and pull_path.exists() else None
    if saved and saved.get("since") == args.since:
        window, named = saved["window_rows"], saved["by_name_rows"]
        log(f"reusing the cabinet rows pulled {saved.get('pulled')}: {len(window)} in the window, {len(named)} by name")
    else:
        window = pull_window(client, args.since)
        named = pull_by_name(client, plants)
        pull_path.write_text(json.dumps(
            {"pulled": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "since": args.since, "categories": list(HARVEST_CATEGORIES),
             "window_rows": window, "by_name_rows": named}, indent=0), encoding="utf-8")
    de_cache_path = out_dir / "_de_sites.json"
    de_cache = json.loads(de_cache_path.read_text(encoding="utf-8")) if de_cache_path.exists() else {}
    facs = build_facilities(window + named)
    log(f"{len(facs)} sites with a cabinet entry")

    # Which sites get the address lookup and the documents: every GEM match, and every power-like name.
    power = {sid for sid, f in facs.items() if is_power(f)}
    matches = {}
    for p in plants:
        matches[p["id"]] = match(p, facs)
    if not args.no_lookup:
        todo = sorted(power | {f["ai"] for ms in matches.values() for f, _ in ms})
        log(f"looking up {len(todo)} sites in Document Explorer")
        for k, sid in enumerate(todo, 1):
            lookup_site(facs[sid], de_cache)
            if k % 50 == 0:
                log(f"  {k}/{len(todo)}")
                de_cache_path.write_text(json.dumps(de_cache, indent=0), encoding="utf-8")
        de_cache_path.write_text(json.dumps(de_cache, indent=0), encoding="utf-8")
        # City is known now, so the city rule can match.
        for p in plants:
            matches[p["id"]] = match(p, facs)
    matched_ids = {f["ai"] for ms in matches.values() for f, _ in ms}
    unmatched = [facs[s] for s in sorted(power - matched_ids)]
    log(f"{len(power)} power-like sites: {len(matched_ids)} sites matched to GEM plants, {len(unmatched)} unmatched")

    if args.match_only:
        for p in plants:
            for f, how in matches[p["id"]] or [({"name": "no match", "ai": "", "city": ""}, "")]:
                print(f"{p['id']}\t{p['name']}\t{f['name']}\t{f['ai']}\t{f.get('city', '')}\t{how}")
        for f in unmatched:
            print(f"UNMATCHED\t\t{f['name']}\t{f['ai']}\t{f.get('city', '')}\t{f['county']}")
        return

    read = sorted(matched_ids) + sorted(power - matched_ids)

    def one(k_sid):
        k, sid = k_sid
        f = facs[sid]
        n = len([d for d in f["docs"] if d["category"] in PERMIT_CATEGORIES])
        pages = args.pages if sid in matched_ids else args.pages_unmatched
        log(f"({k}/{len(read)}) reading {min(n, args.docs_per_facility)} of {n} permit documents of {f['name']} ({sid})")
        try:
            read_docs(client, f, cache_root, args.docs_per_facility, pages)
        except Exception as e:
            log(f"  {sid}: {e}")

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
        list(ex.map(one, enumerate(read, 1)))

    logf = (out_dir / "harvest_log.jsonl").open("a", encoding="utf-8")
    for p in plants:
        write_index(out_dir / f"{p['id']}.md", p, matches[p["id"]], args.since)
        logf.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "plant": p["id"], "name": p["name"],
                               "facilities": [{"name": f["name"], "ai": f["ai"], "how": how,
                                               "docs": {d["id"]: d.get("state", "not read") for d in f["docs"]}}
                                              for f, how in matches[p["id"]]]}) + "\n")
    logf.close()

    L = ["# Illinois sites that look like power or data center sites but match no GEM plant in this batch", "",
         "Each may be a plant outside this batch, a plant GEM lacks, a backup generator fleet, or not a power "
         "plant at all. Check engines or turbines of 50 MW or more in total (generating capacity only). The "
         "document lines come from the permit text; the record address is the one to cite.", ""]
    for f in sorted(unmatched, key=lambda f: f["name"]):
        L += fac_block(f) + [""]
    if not unmatched:
        L.append("None this run.")
    (out_dir / "_unmatched.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    apps = [(d, f) for f in facs.values() if f["ai"] in power | matched_ids
            for d in f["docs"] if d["category"] == "03M" and d["date"] >= args.since]
    L = [f"# Illinois air permit applications since {args.since} at power-like sites ({len(apps)} documents)", ""]
    for d, f in sorted(apps, key=lambda x: x[0]["date"], reverse=True):
        L.append(f"- {d['date']}: {f['name']} ({f['ai']}), {f.get('city', '')}, {f['county']} County: application "
                 f"{d['permit'] or 'number not shown'}, {d.get('pages') or '?'} pages: {d.get('url', '')}")
        for line in (d.get("facts") or {}).get("project", [])[:2]:
            L.append(f"    - {line}")
    (out_dir / "_applications.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    (hv_dir / "facilities.json").write_text(json.dumps({
        "harvested": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "since": args.since,
        "source": "Illinois EPA DocuWare cabinet (Document Explorer), scopes/us-il/harvest_permits.py",
        "window_documents": len(window), "sites": len(facs),
        "matches": {p["id"]: {"name": p["name"], "facilities": [{"ai": f["ai"], "name": f["name"], "how": how}
                                                                  for f, how in matches[p["id"]]]} for p in plants},
        "unmatched": [slim(f) for f in unmatched],
        "matched": [slim(facs[s]) for s in sorted(matched_ids)]}, indent=1), encoding="utf-8")

    S = [f"# Illinois air permit harvest, {time.strftime('%Y-%m-%d')}", "",
         f"Cabinet documents since {args.since} in categories {', '.join(HARVEST_CATEGORIES)}: {len(window)}. "
         f"Sites with an entry: {len(facs)}. Power-like: {len(power)}. Matched to GEM plants: {len(matched_ids)}. "
         f"Unmatched power-like: {len(unmatched)}.", "",
         "## Matches per GEM plant", ""]
    for p in plants:
        ms = matches[p["id"]]
        S.append(f"- {p['name']} ({p['id']}): " + ("; ".join(f"{f['name']} ({f['ai']}, {how})" for f, how in ms)
                                                   if ms else "no site matched"))
    S += ["", "## Unmatched power-like sites", ""]
    for f in sorted(unmatched, key=lambda f: f["name"]):
        S.append(f"- {f['name']} ({f['ai']}), {f.get('city', '')}, {f['county']} County, "
                 f"{len(f['docs'])} documents, permits {', '.join(f['permits'][:4]) or 'none listed'}")
    (hv_dir / "harvest_summary.md").write_text("\n".join(S) + "\n", encoding="utf-8")
    log("done")


if __name__ == "__main__":
    main()

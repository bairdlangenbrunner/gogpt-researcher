"""Interconnection queues that touch Mississippi, gas and oil only (pre-sweep step for scope us-ms).

A queue entry is a lead, not proof. A developer can file a request for a plant
that is never built, and the public lists leave out project names. Nothing from
here is cited as the source of a fact about a plant, except the queue page
itself when a brief says "queue entry J1249 lists a 600 MW combined cycle at
Morrow". The aggregators (interconnection.fyi, Cleanview, Ask the Grid) are never
used.

What was found per source (2026-10-23):

MISO general interconnection queue. Open JSON behind the public queue page,
`https://www.misoenergy.org/api/giqueue/getprojects`, one plain GET with no
login (about 2.3 MB, about 4,000 projects). Fields: project number, queue date,
in-service date, transmission owner, county, state, study cycle, point of
interconnection, summer and winter MW, fuel type, facility type, status. The
citation is the queue page
`https://www.misoenergy.org/planning/resource-utilization/GI_Queue/gi-interactive-queue/`.
About 300 of the newest entries have state, county, fuel and point of
interconnection blanked by MISO until a study is done. Those are kept as
leads when the transmission owner is Entergy Mississippi or Cooperative Energy,
with fuel marked unknown.

MISO ERAS (Expedited Resource Addition Study). MISO has no separate public ERAS
list. ERAS requests show up in the same JSON with a study cycle that starts
"ERAS Study Cycle". The script keeps every MS entry whatever the study cycle, so
ERAS entries are covered. At the time of writing the only ERAS row in the file
is J4182 (Entergy Arkansas, state blank), which is not Mississippi.

Southern Company (Southern Balancing Authority area, Mississippi Power and Alabama
Power and Georgia Power). The public list is a Power BI report, "Active OATT
Generator Interconnection Requests", embedded on
`https://www.southerncompany.info/power-bi/transmission-policy-services/index.html`
(that page sits behind a bot challenge that fetch.py clears with real Chrome).
The report is published to the web, so its data answers the same query the page
sends. The embed address is
`https://app.powerbi.com/view?r=<key>`. From it the script reads the report
layout (`modelsAndExploration`), takes the query of each table (Active,
Inactive, COD = built, Surplus) and posts it to `querydata` on the report's data
host with the resource key in `X-PowerBI-ResourceKey`. No login and no
Cloudflare step. Rows come back in Power BI's compressed form, which
`decode_dsr` unpacks. The Southern OASIS site itself (`oasis.oati.com/SOCO`)
only holds the procedures, not the queue.

TVA. NOT REACHED. TVA says its interconnection procedures and "all related
procedures and data" are on its OASIS (`https://www.oasis.oati.com/tva/`), which
is an ExtJS application inside a frame (`/webSmartOASIS/HomePage?ProviderName=TVA`).
The queue is posted there as a document or report that no static page or
search result points to. Tried: fetch.py on the TVA transmission page, which
links only to the OASIS; curl and real Chrome on the OASIS home page, which
gives the empty application shell and no menu text the script can read;
direct guesses at `woa/docs/TVA/TVAdocs/...` queue file names (all 404); the
LGIP and the Order 2023 FAQ (both mention an OASIS queue posting but give no
address); a web search. The aggregator pages say they copy a "TVA queue PDF",
which confirms it exists but not where. Hand-off: a person with the OASIS
open can save the queue document, and `--tva-file` reads a saved copy (PDF
text or CSV with a Mississippi county column). Found 2026-10-23: the files are
`woa/docs/TVA/TVAdocs/OASIS_CurrentQueue_<date>.pdf` and
`OASIS_ArchiveQueue_<date>.pdf` (plus the stale `AS_CurrentQ.pdf`); the dated
names change, so read them from the OASIS menu in real Chrome, download with
`curl -k`, and pass the tables saved from them (`work/tva_queue/tva_*.csv`,
header "Queue #") with one `--tva-file` each. `--match-only` with `--tva-file`
swaps the TVA rows of a saved queues.json for the new ones.

Output (batches/us-ms/harvest/): `queues.json` and `queues.md`. Downloads stay
out of the repo. Run with `--match-only FILE` to re-match a saved queues.json
without the network.
"""

import argparse
import base64
import copy
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch import CHROME_UA, fetch_page  # noqa: E402
from ms_match import OUT, clean_ws, known_hit, load_plants, norm_county  # noqa: E402

MISO_API = "https://www.misoenergy.org/api/giqueue/getprojects"
MISO_PAGE = "https://www.misoenergy.org/planning/resource-utilization/GI_Queue/gi-interactive-queue/"
SOUTHERN_PAGE = "https://www.southerncompany.info/power-bi/transmission-policy-services/index.html"
SOUTHERN_EMBED = ("https://app.powerbi.com/view?r=eyJrIjoiN2U3YjcxMDAtZTgzMy00N2RjLWFlZDctYmM0YzY2NGNmZTMzIiwi"
                  "dCI6ImMwYTAyZTJkLTExODYtNDEwYS04ODk1LTBhNGEyNTJlYmYxNyIsImMiOjN9")
TVA_OASIS = "https://www.oasis.oati.com/tva/"

GAS_OIL = re.compile(r"natural gas|\bgas\b|ulsd|fuel oil|\boil\b|diesel|syngas|combustion turbine|"
                     r"combined cycle|reciprocating", re.I)
NOT_FOSSIL = re.compile(r"solar|battery|batteries|storage|wind|hydro|biomass|photovoltaic|inverter", re.I)
OWNER_MS = re.compile(r"mississippi|emto|emmp|cooperative energy|\bsmep?\b|south mississippi", re.I)


def log(msg):
    print(f"[queues-ms] {msg}", file=sys.stderr, flush=True)


# ---------------------------------------------------------------- MISO ---

def is_gas_oil_miso(p):
    fuel = f"{p.get('fuelType') or ''} {p.get('facilityType') or ''}"
    if re.search(r"\b(gas|oil|diesel)\b", p.get("fuelType") or "", re.I):
        return True
    return bool(GAS_OIL.search(fuel)) and not NOT_FOSSIL.search(fuel)


def miso_entries(projects):
    """Mississippi entries, plus blank-state entries owned by a Mississippi utility."""
    out = []
    for p in projects:
        state = (p.get("state") or "").strip()
        hidden = not state and bool(OWNER_MS.search(p.get("transmissionOwner") or ""))
        if state != "MS" and not hidden:
            continue
        mw = p.get("summerNetMW")
        out.append({
            "source": "MISO",
            "queue_id": p.get("projectNumber"),
            "project_name": "",
            "county": (p.get("county") or "").strip(),
            "state": state or "(hidden by MISO)",
            "fuel": (p.get("fuelType") or "").strip() or "(not shown)",
            "facility_type": (p.get("facilityType") or "").strip(),
            "mw": mw,
            "status": p.get("applicationStatus") or "",
            "stage": " / ".join(x for x in [p.get("studyCycle"), p.get("studyPhase")] if x),
            "queue_date": (p.get("queueDate") or "")[:10],
            "in_service": (p.get("inService") or "")[:10],
            "withdrawn": (p.get("withdrawnDate") or "")[:10],
            "poi": clean_ws(p.get("poiName")),
            "owner": clean_ws(p.get("transmissionOwner")),
            "url": MISO_PAGE,
            "gas_oil": is_gas_oil_miso(p),
            "fuel_unknown": hidden and not (p.get("fuelType") or "").strip(),
        })
    return out


def fetch_miso():
    page = fetch_page(MISO_API, timeout=120)
    if page.status != "200":
        raise RuntimeError(f"MISO API HTTP {page.status}")
    return json.loads(page.text)


# ------------------------------------------------------------ Power BI ---

def embed_parts(embed_url):
    """(resource key, tenant) from the base64 `r` parameter of a Power BI embed address."""
    r = re.search(r"[?&]r=([A-Za-z0-9_\-=]+)", embed_url).group(1)
    d = json.loads(base64.b64decode(r + "=" * (-len(r) % 4)))
    return d["k"], d["t"]


def api_host_from_view(html_text):
    """Data host named in the report page ('...-redirect...' becomes '...-api...')."""
    m = re.search(r"(wabi-[a-z0-9-]+)-redirect\.analysis\.windows\.net", html_text)
    return f"https://{m.group(1)}-api.analysis.windows.net" if m else None


def _curl_json(args, body=None):
    cmd = ["curl", "-s", "--compressed", "-m", "120", "-A", CHROME_UA] + args
    if body is not None:
        cmd += ["-H", "Content-Type: application/json;charset=UTF-8", "-d", json.dumps(body)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(r.stdout)


def dsr_rows(resp):
    """Rows of one Power BI query response as dicts keyed by column name."""
    data = resp["results"][0]["result"]["data"]
    names = {}
    for s in data["descriptor"]["Select"]:
        names[s["Value"]] = s["Name"].split(".", 1)[-1]
    ds = data["dsr"]["DS"][0]
    dicts = ds.get("ValueDicts", {})
    dm = ds["PH"][0]["DM0"]
    if not dm or "S" not in dm[0]:
        return []
    schema = dm[0]["S"]
    prev = [None] * len(schema)
    rows = []
    for r in dm:
        c = r.get("C", [])
        rep, nul = r.get("R", 0), r.get("Ø", 0)
        cur, ci = [], 0
        for i, col in enumerate(schema):
            if nul >> i & 1:
                v = None
            elif rep >> i & 1:
                v = prev[i]
            else:
                v = c[ci]
                ci += 1
                dn = col.get("DN")
                if dn and isinstance(v, int) and dn in dicts:
                    v = dicts[dn][v]
            cur.append(v)
        rows.append(cur)
        prev = cur
    return [{names.get(col["N"], col["N"]): v for col, v in zip(schema, row)} for row in rows]


def table_commands(models):
    """{section name: query command of its table} from the report layout."""
    out = {}
    for s in models["exploration"]["sections"]:
        for v in s["visualContainers"]:
            if v.get("query") and json.loads(v["config"]).get("singleVisual", {}).get("visualType") == "tableEx":
                out.setdefault(s["displayName"], json.loads(v["query"])["Commands"][0]["SemanticQueryDataShapeCommand"])
    return out


def run_table(host, key, model, cmd, count=5000):
    cmd = copy.deepcopy(cmd)
    cmd["Binding"]["DataReduction"]["Primary"]["Window"]["Count"] = count
    body = {"version": "1.0.0", "queries": [{"Query": {"Commands": [{"SemanticQueryDataShapeCommand": cmd}]},
                                              "QueryId": "", "ApplicationContext": {
                                                  "DatasetId": model["dbName"], "Sources": [{"ReportId": key}]}}],
            "cancelQueries": [], "modelId": model["id"]}
    return _curl_json([host + "/public/reports/querydata?synchronous=true", "-H", f"X-PowerBI-ResourceKey: {key}"], body)


def ms_date(v):
    if isinstance(v, (int, float)):
        return dt.datetime.fromtimestamp(v / 1000, dt.timezone.utc).strftime("%Y-%m-%d")
    return ""


def is_ms_location(loc):
    return bool(re.search(r",\s*MS\b|mississippi", str(loc or ""), re.I))


def southern_entry(row, kind):
    """One normalized entry from a Southern Power BI table row."""
    loc = row.get("Gen Facility Location") or ""
    gtype = (row.get("Gen Type/Size ") or row.get("Generation Type") or "").strip()
    mw = row.get("Capacity MW") or row.get("Incremental Net MW")
    try:
        mw = float(mw)
    except (TypeError, ValueError):
        mw = None
    status = {"Active": "Active", "Inactive": "Withdrawn or terminated", "COD": "In service",
              "Surplus": "Surplus service request"}[kind]
    if kind == "Active" and row.get("Request Phase"):
        status = f"Active, {row['Request Phase']}"
    return {
        "source": "Southern",
        "queue_id": row.get("Request"),
        "project_name": clean_ws(row.get("Facility Name")),
        "county": loc.split(",")[0].replace(" County", "").strip(),
        "state": "MS" if is_ms_location(loc) else "",
        "fuel": re.sub(r"^\s*[\d.,]*\s*MVA\s*", "", gtype),
        "facility_type": gtype,
        "mw": mw,
        "status": status,
        "stage": kind,
        "queue_date": ms_date(row.get("Queue Date")),
        "in_service": ms_date(row.get("In-Service Requested")) or ms_date(row.get("COD (Actual)")),
        "withdrawn": ms_date(row.get("Withdrawn Date")),
        "poi": clean_ws(row.get("Proposed POI")),
        "owner": "Southern Company",
        "note": clean_ws(row.get("Comments") or row.get("Reason for Withdrawal") or ""),
        "url": SOUTHERN_PAGE,
        "gas_oil": bool(GAS_OIL.search(gtype)) and not NOT_FOSSIL.search(gtype),
        "fuel_unknown": False,
    }


def southern_entries(tables):
    """Mississippi entries from {kind: [row dicts]}."""
    out = []
    for kind, rows in tables.items():
        for row in rows:
            if is_ms_location(row.get("Gen Facility Location")):
                out.append(southern_entry(row, kind))
    return out


def fetch_southern():
    key, _tenant = embed_parts(SOUTHERN_EMBED)
    view = fetch_page(SOUTHERN_EMBED, timeout=60)
    host = api_host_from_view(view.text) if view.status == "200" else None
    if not host:
        raise RuntimeError(f"Power BI report page HTTP {view.status}, no data host in it")
    models_raw = _curl_json([f"{host}/public/reports/{key}/modelsAndExploration?preferReadOnlySession=true",
                             "-H", f"X-PowerBI-ResourceKey: {key}"])
    model = models_raw["models"][0]
    cmds = table_commands(models_raw)
    want = {"Active": "Active Gen IC Requests", "Inactive": "Inactive Gen IC Requests",
            "COD": "COD Gen IC Requests", "Surplus": "Surplus Gen IC Requests"}
    tables = {}
    for kind, section in want.items():
        if section not in cmds:
            log(f"Southern: table {section!r} not in the report any more")
            continue
        tables[kind] = dsr_rows(run_table(host, key, model, cmds[section]))
        log(f"Southern {kind}: {len(tables[kind])} rows")
    return tables


# ---------------------------------------------------------------- TVA ---

TVA_DOCS = "https://www.oasis.oati.com/woa/docs/TVA/TVAdocs/"
TVA_PDF_NAMES = {"tva_current_queue_": "OASIS_CurrentQueue_", "tva_archive_queue_": "OASIS_ArchiveQueue_"}


def tva_csv_entries(p):
    """Mississippi rows of a table saved from a TVA queue PDF (header starts "Queue #").
    The citable address is the PDF the table was read from, rebuilt from the file name."""
    import csv
    url = TVA_OASIS
    for prefix, pdf in TVA_PDF_NAMES.items():
        if p.name.startswith(prefix):
            url = TVA_DOCS + pdf + p.stem[len(prefix):] + ".pdf"
    out = []
    for r in csv.DictReader(p.open(newline="", errors="replace")):
        if (r.get("State") or "").strip() != "MS":
            continue
        fuel = (r.get("Generator Type") or r.get("Type") or "").strip()
        try:
            mw = float(r.get("Summer MW") or "")
        except ValueError:
            mw = None
        status = (r.get("Phase") or r.get("Project Status") or "").strip()
        out.append({"source": f"TVA {p.stem}", "queue_id": (r.get("Queue #") or "").strip(), "project_name": "",
                    "county": (r.get("County") or "").strip(), "state": "MS", "fuel": fuel, "facility_type": "",
                    "mw": mw, "status": status, "stage": status, "queue_date": (r.get("Queue Date") or "").strip(),
                    "in_service": (r.get("Forecasted ISD") or r.get("Requested / Forecasted In-Service Date") or "").strip(),
                    "withdrawn": "withdrawn" if "withdraw" in status.lower() else "", "poi": (r.get("POI") or "").strip(),
                    "owner": "", "note": clean_ws(", ".join(f"{k}: {v}" for k, v in r.items() if v))[:300], "url": url,
                    "gas_oil": bool(GAS_OIL.search(fuel)), "fuel_unknown": not fuel})
    return out


def tva_file_entries(path):
    """Mississippi entries from a saved TVA queue file (text of a PDF, or CSV)."""
    p = Path(path)
    if p.suffix.lower() == ".csv" and p.read_text(errors="replace").startswith("Queue #"):
        return tva_csv_entries(p)
    if p.suffix.lower() == ".pdf":
        from fetch import pdf_text
        text, _ = pdf_text(str(p))
    else:
        text = p.read_text(errors="replace")
    out = []
    for line in text.splitlines():
        if re.search(r",\s*MS\b|mississippi", line, re.I) and GAS_OIL.search(line):
            out.append({"source": "TVA (saved file)", "queue_id": "", "project_name": "", "county": "",
                        "state": "MS", "fuel": "", "facility_type": "", "mw": None, "status": "",
                        "stage": "", "queue_date": "", "in_service": "", "withdrawn": "", "poi": "",
                        "owner": "TVA", "note": clean_ws(line)[:300], "url": TVA_OASIS,
                        "gas_oil": True, "fuel_unknown": False})
    return out


# ---------------------------------------------------------------- match ---

def match_entry(plant, e):
    """[how] strings: the point of interconnection or name hits a hand-checked
    pattern, or the county is the plant's county for a gas or oil entry."""
    text = f"{e['poi']} {e['project_name']}"
    if known_hit(plant, text):
        return "point of interconnection or name matches the plant"
    if (plant["county"] and e["gas_oil"] and norm_county(e["county"]) == plant["county"]):
        return "same county, gas or oil, check it is this plant"
    return None


def match_all(plants, entries):
    by_plant = {p["id"]: [] for p in plants}
    matched = set()
    for i, e in enumerate(entries):
        e["matched"] = []
        if not e["gas_oil"] and not e.get("fuel_unknown"):
            continue
        if e.get("fuel_unknown"):
            continue
        for p in plants:
            how = match_entry(p, e)
            if how:
                e["matched"].append({"plant_id": p["id"], "plant": p["name"], "how": how})
                by_plant[p["id"]].append(i)
                matched.add(i)
    return by_plant, matched


# --------------------------------------------------------------- output ---

def fmt_mw(mw):
    return "" if mw in (None, "") else f"{mw:g} MW"


def entry_line(e):
    bits = [f"{e['source']} {e['queue_id']}", e["fuel"] or e["facility_type"], fmt_mw(e["mw"]),
            re.sub(r"(\s+County)?$", " County", e["county"]) if e["county"] else "", e["status"],
            f"queued {e['queue_date']}" if e["queue_date"] else "",
            f"in service {e['in_service']}" if e["in_service"] else "",
            f"point of interconnection: {e['poi']}" if e["poi"] else "", e["owner"]]
    return "; ".join(b for b in bits if b)


def write_outputs(out_dir, plants, entries, by_plant, matched, sources, today):
    out_dir.mkdir(parents=True, exist_ok=True)
    unmatched = [e for i, e in enumerate(entries) if e["gas_oil"] and i not in matched]
    unknown = [e for e in entries if e.get("fuel_unknown")]
    data = {"generated": today, "sources": sources, "entries": entries,
            "by_plant": {pid: [entries[i]["queue_id"] for i in ix] for pid, ix in by_plant.items()},
            "unmatched_gas_oil": [e["queue_id"] for e in unmatched],
            "hidden_fuel_leads": [e["queue_id"] for e in unknown]}
    (out_dir / "queues.json").write_text(json.dumps(data, indent=1, default=str))
    L = [f"# Mississippi interconnection queues, gas and oil ({today})", "",
         "A queue entry is a lead, not proof that a plant exists or will be built. The queue file or page below is the citation.", ""]
    L += ["## Sources", ""]
    for s in sources:
        L.append(f"- {s['name']}: {s['how']} ({s['url']})")
    L += ["", "## Matched to GEM plants", ""]
    for p in plants:
        ix = by_plant.get(p["id"], [])
        L.append(f"### {p['name']} ({p['id']}), {p['city']}, {p['county'].title()} County")
        L.append("")
        if not ix:
            L += ["No queue entry matched.", ""]
            continue
        for i in ix:
            e = entries[i]
            how = next(m["how"] for m in e["matched"] if m["plant_id"] == p["id"])
            L.append(f"- {entry_line(e)} ({how}). Citation: {e['url']}")
        L.append("")
    L += ["## Gas and oil entries that match no GEM plant (possible new plants or uprates)", ""]
    for e in sorted(unmatched, key=lambda x: (x["source"], str(x["queue_id"]))):
        L.append(f"- {entry_line(e)}. Citation: {e['url']}")
    L += ["", "## Entries with fuel hidden by MISO (Entergy Mississippi or Cooperative Energy, state blank)", "",
          "MISO blanks fuel, county and point of interconnection on its newest entries. Sizes of 100 MW or more are worth a look when the sweep reaches the plant's utility.", ""]
    for e in sorted(unknown, key=lambda x: -(x["mw"] or 0)):
        if (e["mw"] or 0) >= 50:
            L.append(f"- {entry_line(e)}")
    (out_dir / "queues.md").write_text("\n".join(L) + "\n")
    return unmatched, unknown


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--plants", help="comma-separated GEM location IDs")
    ap.add_argument("--tva-file", action="append", default=[],
                    help="saved TVA queue document (PDF, or a CSV table read from one); repeat for several")
    ap.add_argument("--match-only", metavar="QUEUES_JSON", help="re-match a saved queues.json, no network")
    a = ap.parse_args()
    plants = load_plants(wanted=set(a.plants.split(",")) if a.plants else None)
    today = dt.date.today().isoformat()
    sources = []
    if a.match_only:
        saved = json.loads(Path(a.match_only).read_text())
        entries, sources = saved["entries"], saved["sources"]
    else:
        entries = []
        try:
            projects = fetch_miso()
            ms = miso_entries(projects)
            entries += ms
            sources.append({"name": "MISO generator interconnection queue (includes ERAS rows)", "url": MISO_PAGE,
                            "how": f"open JSON {MISO_API}, plain GET; {len(projects)} projects, "
                                   f"{sum(1 for e in ms if e['state'] == 'MS')} in Mississippi, "
                                   f"{sum(1 for e in ms if e['state'] != 'MS')} state-hidden Mississippi-utility leads"})
        except Exception as e:  # noqa: BLE001
            log(f"MISO failed: {e}")
            sources.append({"name": "MISO", "url": MISO_PAGE, "how": f"NOT REACHED: {e}"})
        try:
            tables = fetch_southern()
            ss = southern_entries(tables)
            entries += ss
            sources.append({"name": "Southern Company active, inactive, in-service and surplus lists", "url": SOUTHERN_PAGE,
                            "how": "Power BI published-to-web report queried directly; "
                                   + ", ".join(f"{k} {len(v)} rows" for k, v in tables.items())
                                   + f"; {len(ss)} in Mississippi"})
        except Exception as e:  # noqa: BLE001
            log(f"Southern failed: {e}")
            sources.append({"name": "Southern Company", "url": SOUTHERN_PAGE, "how": f"NOT REACHED: {e}"})
        if not a.tva_file:
            sources.append({"name": "TVA", "url": TVA_OASIS,
                            "how": "NOT REACHED: the queue is inside the OASIS application and no address for it was found "
                                   "(see the module notes for what was tried); pass --tva-file with a saved copy"})
    if a.tva_file:
        entries = [e for e in entries if not e["source"].startswith("TVA")]
        sources = [s for s in sources if not s["name"].startswith("TVA")]
        for f in a.tva_file:
            te = tva_file_entries(f)
            entries += te
            sources.append({"name": "TVA saved queue file", "url": te[0]["url"] if te else TVA_OASIS,
                            "how": f"{f}: {len(te)} Mississippi rows"})
    by_plant, matched = match_all(plants, entries)
    unmatched, unknown = write_outputs(Path(a.out), plants, entries, by_plant, matched, sources, today)
    log(f"{len(entries)} entries; {sum(1 for e in entries if e['gas_oil'])} gas or oil; "
        f"{len(matched)} matched; {len(unmatched)} unmatched gas or oil; {len(unknown)} fuel-hidden leads")
    for p in plants:
        log(f"  {p['name']}: {len(by_plant[p['id']])}")


if __name__ == "__main__":
    main()

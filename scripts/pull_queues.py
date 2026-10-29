"""Interconnection queues that touch one US state, gas and oil only (pre-sweep step, any state with a settings entry).

    python pull_queues.py --state MI [--scope us-mi]

A queue entry is a lead, not proof. A developer can file a request for a plant
that is never built, and the public lists leave out project names. Nothing from
here is cited as the source of a fact about a plant, except the queue page
itself when a brief says "queue entry J3923 lists a 1,414 MW combined cycle in
Washtenaw County". The aggregators (interconnection.fyi, Cleanview, Ask the
Grid) are never used.

The state's markets, transmission owners and name patterns are settings in
`scopes/us-<st>/queues.json`, not logic. A new state is a new settings file
there. Michigan is the first. Mississippi's settings are carried over so the
Mississippi case (`scopes/us-ms/pull_queues_mississippi.py`, which also reads
Southern Company and TVA) can later move onto this script; until then that
script stays the one for scope us-ms and nothing here touches it.

What was found per source (2026-10-23):

MISO general interconnection queue. Same open JSON as the Mississippi script,
`https://www.misoenergy.org/api/giqueue/getprojects`, one plain GET with no
login (about 4,000 projects). Fields: project number, queue date, in-service
date, transmission owner, county, state, study cycle, point of interconnection,
summer and winter MW, fuel type, facility type, status. The citation is the queue
page `https://www.misoenergy.org/planning/resource-utilization/GI_Queue/gi-interactive-queue/`.
MISO blanks state, county, fuel and point of interconnection on its newest
entries until a study is done. Those are kept as leads, fuel unknown, when the
transmission owner is a Michigan-only owner in the settings (METC, ITC
Transmission, Consumers Energy, Wolverine and the like). American Transmission
Company serves Wisconsin as well as the Upper Peninsula, so its blanked entries
are only counted in the notes, not kept (settings key `shared_owner`). MISO has
no separate ERAS (Expedited Resource Addition Study) list. ERAS requests are in
the same JSON with a study cycle that starts "ERAS Study Cycle", so every
Michigan entry is kept whatever its study cycle.

PJM (southwest Michigan, the Indiana Michigan Power and American Electric Power
zone, plus the Michigan border counties served by ITC through PJM). PJM
publishes its queue as two open XML files, no login, no key, plain GET:
  1. `https://www.pjm.com/pjmfiles/media/planning/queues-data/PlanningQueues.xml`
     (about 23 MB, about 9,260 projects, rewritten daily, the file behind the
     "XML" button on the Serial Service Request Status page
     `https://www.pjm.com/planning/service-requests/serial-service-request-status`).
     Serial queues A01 through AJ1. Fields: project number, name (the
     interconnection point), commercial name, state, county, status,
     transmission owner, capacity and energy MW, fuel, submitted, withdrawal and
     in-service dates.
  2. The Cycle Service Request Status page
     `https://www.pjm.com/planning/m/cycle-service-request-status` serves the
     newer projects (Transition Cycle 1 and 2, and Cycle 1 which opened in 2026)
     from a form post, not a file. The "All" XML button posts an empty grid
     filter to `https://www.pjm.com/m/ProjectTransition/GenerateXMLTransitionProjectsAll`
     (field `jsonModel` with the grid name `ProjectTransition` and no filters)
     and gets back about 1,800 projects with state, county, cycle, stage,
     developer, fuel and dates. The two files do not share a project number, so
     every entry is kept once.
Tried and not used: the older static files `transitionProjects.xml` and
`clusterReports.xml` under `pjmfiles/media/planning/queues-data/` and
`pjmfiles/pub/planning/downloads/xml/` (last changed October 2024, stale); the
`services.pjm.com/PJMPlanningApi` host behind the serial page returns an error
page to a plain GET, and the post file above made it unnecessary. Both of the
files that are used came through the plain curl step of fetch.py with no
Cloudflare step. PJM fuel names: "Natural Gas", "Oil", "Natural Gas,Storage,Hybrid"
and similar count as gas or oil. "Methane" (landfill gas) does not. A blank or
"Not Specified" fuel is kept only when the project name or developer names a gas
or oil technology, as fuel unknown. Capacity is the capacity MW, or the energy MW
when capacity is zero.

Output (batches/us-<st>/harvest/): `queues.json` and `queues.md`, the shape
`build_state_brief.py --harvest` reads (same keys as the Mississippi output).
Downloads stay out of the repo. Run with `--match-only FILE` to re-match a saved
queues.json without the network.
"""

import argparse
import datetime as dt
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch import fetch_page  # noqa: E402
from harvest_lib import CSV, REPO, clean_ws, norm_county  # noqa: E402
from paths import SCOPES_DIR  # noqa: E402

MISO_API = "https://www.misoenergy.org/api/giqueue/getprojects"
MISO_PAGE = "https://www.misoenergy.org/planning/resource-utilization/GI_Queue/gi-interactive-queue/"
PJM_SERIAL_XML = "https://www.pjm.com/pjmfiles/media/planning/queues-data/PlanningQueues.xml"
PJM_SERIAL_PAGE = "https://www.pjm.com/planning/service-requests/serial-service-request-status"
PJM_CYCLE_POST = "https://www.pjm.com/m/ProjectTransition/GenerateXMLTransitionProjectsAll"
PJM_CYCLE_PAGE = "https://www.pjm.com/planning/m/cycle-service-request-status"

GAS_OIL = re.compile(r"natural gas|\bgas\b|ulsd|fuel oil|\boil\b|diesel|syngas|combustion turbine|"
                     r"combined cycle|reciprocating", re.I)
NOT_FOSSIL = re.compile(r"solar|battery|batteries|storage|wind|hydro|biomass|photovoltaic|inverter|methane|nuclear", re.I)

# One settings file per state, scopes/us-<st>/queues.json (moved out of this file 2026-10-29).
# Everything that differs by state lives there; its "_about" key explains each setting.
def load_states(root=None):
    """Postal code -> settings, from every scopes/*/queues.json."""
    out = {}
    for f in sorted((Path(root) if root else SCOPES_DIR).glob("*/queues.json")):
        cfg = json.loads(f.read_text(encoding="utf-8"))
        cfg["settings_file"] = str(f.relative_to(REPO)) if f.is_relative_to(REPO) else str(f)
        out[cfg["state"]] = cfg
    return out


STATES = load_states()


def log(msg):
    print(f"[queues] {msg}", file=sys.stderr, flush=True)


# ---------------------------------------------------------------- MISO ---

def is_gas_oil_miso(p):
    fuel = f"{p.get('fuelType') or ''} {p.get('facilityType') or ''}"
    if re.search(r"\b(gas|oil|diesel)\b", p.get("fuelType") or "", re.I):
        return True
    return bool(GAS_OIL.search(fuel)) and not NOT_FOSSIL.search(fuel)


def miso_entries(projects, cfg, state):
    """State entries, plus blank-state entries owned by one of the state's own owners.
    Returns (entries, count of blank-state entries held back as a shared owner's)."""
    owner_re = re.compile(cfg["owner"], re.I)
    shared_re = re.compile(cfg["shared_owner"], re.I)
    out, shared = [], 0
    for p in projects:
        st = (p.get("state") or "").strip()
        owner = clean_ws(p.get("transmissionOwner"))
        hidden = not st and bool(owner_re.search(owner))
        if not st and not hidden and shared_re.search(owner):
            shared += 1
        if st != state and not hidden:
            continue
        out.append({
            "source": "MISO",
            "queue_id": p.get("projectNumber"),
            "project_name": "",
            "county": (p.get("county") or "").strip(),
            "state": st or "(hidden by MISO)",
            "fuel": (p.get("fuelType") or "").strip() or "(not shown)",
            "facility_type": (p.get("facilityType") or "").strip(),
            "mw": p.get("summerNetMW"),
            "status": p.get("applicationStatus") or "",
            "stage": " / ".join(x for x in [p.get("studyCycle"), p.get("studyPhase")] if x),
            "queue_date": (p.get("queueDate") or "")[:10],
            "in_service": (p.get("inService") or "")[:10],
            "withdrawn": "",
            "poi": clean_ws(p.get("poiName")),
            "owner": owner,
            "url": MISO_PAGE,
            "gas_oil": is_gas_oil_miso(p),
            "fuel_unknown": hidden and not (p.get("fuelType") or "").strip(),
        })
    return out, shared


def fetch_miso():
    page = fetch_page(MISO_API, timeout=120)
    if page.status != "200":
        raise RuntimeError(f"MISO API HTTP {page.status}")
    return json.loads(page.text)


# ----------------------------------------------------------------- PJM ---

def pjm_date(s):
    """'4/24/2026' -> '2026-04-24'; anything else comes back as it was."""
    s = clean_ws(s)
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
    return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}" if m else s


def pjm_projects(xml_text):
    """[{tag: text}] from a PJM queue XML file (text, with or without the byte order mark)."""
    root = ET.fromstring(xml_text.lstrip("﻿").encode("utf-8"))
    return [{c.tag: (c.text or "").strip() for c in p} for p in root]


def pjm_fuel_class(p):
    """('gas_oil'|'unknown'|'other', fuel text)."""
    fuel = clean_ws(p.get("Fuel"))
    if re.search(r"natural gas|\bgas\b|\boil\b|diesel", fuel, re.I) and not re.fullmatch(r"methane", fuel, re.I):
        return "gas_oil", fuel
    if fuel in ("", "Not Specified", "Other") or "Other" in fuel.split(","):
        text = f"{p.get('Name', '')} {p.get('CommercialName', '')} {p.get('Developer', '')}"
        if GAS_OIL.search(text):
            return "unknown", fuel or "(not shown)"
    return "other", fuel


def pjm_mw(p):
    for key in ("MWCapacity", "MWEnergy"):
        try:
            v = float(p.get(key) or "")
        except ValueError:
            continue
        if v > 0:
            return v
    return None


def pjm_entries(projects, cfg, kind):
    """Gas, oil and thermal-unknown entries of the state's PJM states.
    `kind` is "serial" or "cycle" and picks the citation page."""
    out = []
    for p in projects:
        if clean_ws(p.get("State")) not in cfg["pjm_states"]:
            continue
        cls, fuel = pjm_fuel_class(p)
        if cls == "other":
            continue
        cycle = clean_ws(p.get("Cycle"))
        stage = " / ".join(x for x in [cycle, clean_ws(p.get("Stage"))] if x)
        notes = []
        if p.get("Developer"):
            notes.append(f"Developer: {clean_ws(p['Developer'])}")
        if p.get("MWEnergy") and p.get("MWCapacity"):
            notes.append(f"Energy MW {p['MWEnergy']}, capacity MW {p['MWCapacity']}")
        out.append({
            "source": "PJM",
            "queue_id": p.get("ProjectNumber"),
            "project_name": clean_ws(p.get("CommercialName")),
            "county": clean_ws(p.get("County")),
            "state": clean_ws(p.get("State")),
            "fuel": fuel,
            "facility_type": clean_ws(p.get("ProjectType")),
            "mw": pjm_mw(p),
            "status": clean_ws(p.get("Status")),
            "stage": stage,
            "queue_date": pjm_date(p.get("SubmittedDate")),
            "in_service": pjm_date(p.get("ActualInServiceDate") or p.get("ProjectedInServiceDate")
                                   or p.get("RequestedInServiceDate")),
            "withdrawn": pjm_date(p.get("WithdrawalDate") or p.get("WithdrawnDate")),
            "poi": clean_ws(p.get("Name")),
            "owner": clean_ws(p.get("TransmissionOwner")),
            "note": "; ".join(notes),
            "url": PJM_CYCLE_PAGE if kind == "cycle" else PJM_SERIAL_PAGE,
            "gas_oil": cls == "gas_oil",
            "fuel_unknown": cls == "unknown",
        })
    return out


def fetch_pjm():
    """(serial XML text, cycle XML text). The cycle file is a form post, so it goes through curl."""
    import subprocess
    from fetch import CHROME_UA
    serial = fetch_page(PJM_SERIAL_XML, timeout=180)
    if serial.status != "200":
        raise RuntimeError(f"PJM serial queue XML HTTP {serial.status}")
    model = json.dumps({"GridName": "ProjectTransition", "ItemType": 0, "Items": [], "Paginator": None,
                        "Sort": "", "SortDirection": "", "RelatedGridsFilters": ""})
    r = subprocess.run(["curl", "-s", "--compressed", "-m", "180", "-A", CHROME_UA, "-X", "POST",
                        "--data-urlencode", f"jsonModel={model}", PJM_CYCLE_POST],
                       capture_output=True, text=True)
    if "<Projects>" not in r.stdout:
        raise RuntimeError("PJM cycle XML post returned no projects")
    return serial.text, r.stdout


# ---------------------------------------------------------------- match ---

def load_plants(state_name, known, csv_path=None):
    """One dict per plant of the state in the scoped export (unit rows grouped)."""
    d = pd.read_csv(csv_path or CSV, low_memory=False, encoding="utf-8-sig")
    d = d[d["State/Province"] == state_name]
    plants = []
    for pid, rows in d.groupby("GEM location ID", sort=False):
        r = rows.iloc[0]
        if re.search(r"IRP power station", str(r["Plant name"])):
            continue
        city = r.get("City") if isinstance(r.get("City"), str) else ""
        county = r.get("Local area (taluk, county)")
        plants.append({"id": pid, "name": r["Plant name"], "city": city,
                       "county": norm_county(county) if isinstance(county, str) else "",
                       "known": known.get(pid, [])})
    return plants


def match_entry(plant, e):
    """A hand-checked pattern hits the point of interconnection, project name or developer,
    or a gas or oil entry is in the plant's county."""
    text = f"{e['poi']} {e['project_name']} {e.get('note', '')}"
    if any(re.search(p, text, re.I) for p in plant["known"]):
        return "point of interconnection or name matches the plant"
    if plant["county"] and e["gas_oil"] and norm_county(e["county"]) == plant["county"]:
        return "same county, gas or oil, check it is this plant"
    return None


def match_all(plants, entries):
    by_plant = {p["id"]: [] for p in plants}
    matched = set()
    for i, e in enumerate(entries):
        e["matched"] = []
        if not e["gas_oil"]:
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
            norm_county(e["county"]).title() + " County" if e["county"] else "", e["status"],
            f"queued {e['queue_date']}" if e["queue_date"] else "",
            f"in service {e['in_service']}" if e["in_service"] else "",
            f"point of interconnection: {e['poi']}" if e["poi"] else "", e["owner"]]
    return "; ".join(b for b in bits if b)


def write_outputs(out_dir, state_name, plants, entries, by_plant, matched, sources, today):
    out_dir.mkdir(parents=True, exist_ok=True)
    unmatched = [e for i, e in enumerate(entries) if e["gas_oil"] and i not in matched]
    unknown = [e for e in entries if e.get("fuel_unknown")]
    data = {"generated": today, "sources": sources, "entries": entries,
            "by_plant": {pid: [entries[i]["queue_id"] for i in ix] for pid, ix in by_plant.items()},
            "unmatched_gas_oil": [e["queue_id"] for e in unmatched],
            "hidden_fuel_leads": [e["queue_id"] for e in unknown]}
    (out_dir / "queues.json").write_text(json.dumps(data, indent=1, default=str))
    L = [f"# {state_name} interconnection queues, gas and oil ({today})", "",
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
    L += ["", "## Entries with fuel not shown (state's own transmission owner with the state blanked, or a PJM entry with no fuel)", "",
          "MISO blanks state, fuel, county and point of interconnection on its newest entries. Sizes of 100 MW or more are worth a look when the sweep reaches the plant's utility.", ""]
    for e in sorted(unknown, key=lambda x: -(x["mw"] or 0)):
        if (e["mw"] or 0) >= 50:
            L.append(f"- {entry_line(e)}")
    (out_dir / "queues.md").write_text("\n".join(L) + "\n")
    return unmatched, unknown


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--state", required=True, help="postal code with a scopes/us-<st>/queues.json, for example MI")
    ap.add_argument("--scope", help="batch scope, default us-<state>")
    ap.add_argument("--out", help="output folder, default batches/<scope>/harvest")
    ap.add_argument("--match-only", metavar="QUEUES_JSON", help="re-match a saved queues.json, no network")
    a = ap.parse_args()
    st = a.state.upper()
    if st not in STATES:
        sys.exit(f"ERROR: no settings for {st}; add scopes/us-{st.lower()}/queues.json (known: {', '.join(STATES)})")
    cfg = STATES[st]
    scope = a.scope or f"us-{st.lower()}"
    out_dir = Path(a.out) if a.out else REPO / "batches" / scope / "harvest"
    plants = load_plants(cfg["name"], cfg["known"])
    today = dt.date.today().isoformat()
    sources = []
    if a.match_only:
        saved = json.loads(Path(a.match_only).read_text())
        entries, sources = saved["entries"], saved["sources"]
    else:
        entries = []
        if "MISO" in cfg["markets"]:
            try:
                projects = fetch_miso()
                ms, shared = miso_entries(projects, cfg, st)
                entries += ms
                eras = sum(1 for e in ms if str(e["stage"]).startswith("ERAS"))
                sources.append({"name": "MISO generator interconnection queue (includes ERAS rows)", "url": MISO_PAGE,
                                "how": f"open JSON {MISO_API}, plain GET; {len(projects)} projects, "
                                       f"{sum(1 for e in ms if e['state'] == st)} in {cfg['name']}, "
                                       f"{sum(1 for e in ms if e['state'] != st)} state-hidden leads of the state's own owners, "
                                       f"{eras} ERAS rows, {shared} state-hidden entries of owners shared with other states not kept"})
            except Exception as e:  # noqa: BLE001
                log(f"MISO failed: {e}")
                sources.append({"name": "MISO", "url": MISO_PAGE, "how": f"NOT REACHED: {e}"})
        if "PJM" in cfg["markets"]:
            try:
                serial_xml, cycle_xml = fetch_pjm()
                ps = pjm_entries(pjm_projects(serial_xml), cfg, "serial")
                pc = pjm_entries(pjm_projects(cycle_xml), cfg, "cycle")
                seen = {e["queue_id"] for e in ps}
                pc = [e for e in pc if e["queue_id"] not in seen]
                entries += ps + pc
                sources.append({"name": "PJM serial queue (A01 through AJ1)", "url": PJM_SERIAL_PAGE,
                                "how": f"open XML {PJM_SERIAL_XML}, plain GET; {len(ps)} {cfg['name']} gas, oil or thermal-unknown entries"})
                sources.append({"name": "PJM cycle queue (Transition Cycle 1 and 2, Cycle 1)", "url": PJM_CYCLE_PAGE,
                                "how": f"open XML posted to {PJM_CYCLE_POST} with an empty grid filter; {len(pc)} {cfg['name']} gas, oil or thermal-unknown entries"})
            except Exception as e:  # noqa: BLE001
                log(f"PJM failed: {e}")
                sources.append({"name": "PJM", "url": PJM_SERIAL_PAGE, "how": f"NOT REACHED: {e}"})
    by_plant, matched = match_all(plants, entries)
    unmatched, unknown = write_outputs(out_dir, cfg["name"], plants, entries, by_plant, matched, sources, today)
    for src in sorted({e["source"] for e in entries}):
        es = [e for e in entries if e["source"] == src]
        log(f"{src}: {sum(1 for e in es if e['gas_oil'])} gas or oil, "
            f"{sum(1 for e in es if e['gas_oil'] and e['matched'])} matched, "
            f"{sum(1 for e in es if e['gas_oil'] and not e['matched'])} unmatched, "
            f"{sum(1 for e in es if e.get('fuel_unknown'))} fuel-unknown leads")
    log(f"{len(entries)} entries; {len(matched)} matched; {len(unmatched)} unmatched gas or oil; {len(unknown)} fuel-hidden leads")
    for p in plants:
        log(f"  {p['name']}: {len(by_plant[p['id']])}")


if __name__ == "__main__":
    main()

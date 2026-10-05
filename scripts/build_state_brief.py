"""
Build per-plant research briefs for one scope: a US state or a whole country
(the scope-sweep pipeline; contract in notes/us_state_agent_plan.md).

Usage (from scripts/):
    python build_state_brief.py --state Maryland --mode blind
    python build_state_brief.py --state Maryland --mode update
    python build_state_brief.py --country Germany --mode update
    python build_state_brief.py --state Maryland --mode update \\
        --plants L100000402511,L100000103962 --batch ../batches/us-md \\
        [--csv gem_export_gogpt_scoped.csv] [--worklist work/worklist_us-maryland.csv]

Reads:
    the GOGPT-scoped export (default scripts/gem_export_gogpt_scoped.csv;
    utf-8-sig, headers matched by exact name), filtered to Country/Area ==
    United States and State/Province == --state, or to Country/Area ==
    --country (case-insensitive);
    the worklist csv from worklist.py (default <repo>/work/worklist_us-<state-slug>.csv
    or <repo>/work/worklist_<country-slug>.csv, what `worklist.py --state` /
    `--country` writes; joined on GEM unit ID for priority and flag; optional);
    docs/country_notes/united_states/<state-slug>.md or
    docs/country_notes/<country-slug>.md (inlined when present).

Writes (batch dir default ../batches/us-<postal> or ../batches/<country-slug>):
    briefs/<GEM location ID>.md      one brief per plant
    briefs/_index.json               plants, brief paths, unit IDs, max priority
    briefs/_hidden/<L...>.json       blind mode only: the withheld GEM values
    shards/, staging/, deliverables/ created (with .gitkeep where empty)

Modes:
    update  full current values, existing Data Source URLs, Notes, worklist
            priority and flag, state notes, and a "What to check" block per
            unit built from the Editing Manual's ladder (in-development,
            shelved, mothballed, planned retirement, cancelled without a
            year) plus the gap list (blank fuel, status, technology, owner,
            coordinates, city; zero capacity; unknown technology; blank start
            year on an operating unit; inferred status without Latest
            Activity; missing EIA IDs, US only; a value whose Data Source is
            empty).
            The "Fields to report on" list is narrowed to the fields those
            tasks touch. Operating units with no task are not researched.
    blind   identity only (plant, location, IDs, unit IDs and names). Every
            GEM value, source, note, edit history, wiki URL and worklist
            priority is withheld and written to briefs/_hidden/ for the
            compare step. The one thing a blind brief cannot avoid is the
            exact header names in the report-on list (for example
            "Capacity (MW)"), which carry no plant data.

Scope (update mode only; blind always takes every plant):
    --scope ladder   (default) only plants where at least one unit has a task
                     or that have an entry in --extra-tasks. Plants left out
                     are listed under "not_tasked" in _index.json.
    --scope all      every plant; a plant with no task gets the full field
                     list and a note saying nothing specific was flagged.
    --extra-tasks F  JSON {"<GEM location ID>": [task, ...], "*": [task, ...]}
                     for backlog rows and scan hits. A task is a string
                     (grants the full field list) or {"text": ..., "fields":
                     [exact headers]}. "*" tasks go on every brief and do not
                     by themselves pull a plant into ladder scope.
"""
import argparse
import csv
import datetime
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from paths import REPO_ROOT, gogpt_scoped_csv, work_dir
from schema_constants import (OUT_OF_SCOPE_COLUMNS, READ_ONLY_COLUMNS, RESEARCH_FIELDS,
                              STATUSES_IN_DEVELOPMENT)
from build_review_package import ref_col_for

POSTAL = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR",
    "california": "CA", "colorado": "CO", "connecticut": "CT", "delaware": "DE",
    "district of columbia": "DC", "florida": "FL", "georgia": "GA", "hawaii": "HI",
    "idaho": "ID", "illinois": "IL", "indiana": "IN", "iowa": "IA", "kansas": "KS",
    "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
    "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS",
    "missouri": "MO", "montana": "MT", "nebraska": "NE", "nevada": "NV",
    "new hampshire": "NH", "new jersey": "NJ", "new mexico": "NM", "new york": "NY",
    "north carolina": "NC", "north dakota": "ND", "ohio": "OH", "oklahoma": "OK",
    "oregon": "OR", "pennsylvania": "PA", "rhode island": "RI",
    "south carolina": "SC", "south dakota": "SD", "tennessee": "TN", "texas": "TX",
    "utah": "UT", "vermont": "VT", "virginia": "VA", "washington": "WA",
    "west virginia": "WV", "wisconsin": "WI", "wyoming": "WY",
}

H_PLANT = "Plant name"
H_LOC = "GEM location ID"
H_UNIT = "GEM unit ID"
H_UNAME = "Unit name"
H_COUNTY = "Local area (taluk, county)"
H_MAJOR = "Major area (prefecture, district)"
H_OTHERNAMES = "Other Name(s)"
H_NOTES = "Notes"
URL_SPLIT = re.compile(r"[,;\s]+")
BLIND_UNIT_FIELDS = [H_UNIT, H_UNAME, "Other IDs (unit)"]


def is_source_col(h):
    return h.endswith("Data Source")


def value_cols(header):
    """Non-read-only, non-source columns shown in the per-unit value table."""
    skip = {H_NOTES}
    return [h for h in header
            if h not in READ_ONLY_COLUMNS and not is_source_col(h) and h not in skip]


def hidden_cols(header):
    """Everything a blind brief withholds: values, sources, notes, history."""
    cols = [h for h in header if h not in READ_ONLY_COLUMNS
            and h not in (H_LOC, H_UNIT)]
    cols += [h for h in header if is_source_col(h) and h not in OUT_OF_SCOPE_COLUMNS
             and h not in cols]
    cols += [h for h in ("Last Updated", "Researcher") if h in header]
    return cols


def split_urls(cell):
    seen, out = set(), []
    for u in URL_SPLIT.split(cell or ""):
        u = u.strip()
        if u and u not in seen:
            seen.add(u)
            out.append(u)
    return out


def blank(v):
    v = (v or "").strip()
    return v if v else "(blank)"


def cell(v):
    return blank(v).replace("|", "\\|").replace("\n", " ")


def state_slug(state):
    """Lowercase, spaces to hyphens: the tag worklist.py uses for a state or country."""
    return re.sub(r"\s+", "-", state.strip().lower())


def make_scope(state=None, country=None):
    """The batch scope: {kind, name, slug, country, postal}. One of state / country."""
    if state:
        postal = POSTAL.get(state.strip().lower())
        if not postal:
            sys.exit(f"ERROR: unknown state {state!r}")
        return {"kind": "state", "name": state.strip(), "slug": state_slug(state),
                "country": "United States", "postal": postal.lower()}
    return {"kind": "country", "name": country.strip(), "slug": state_slug(country),
            "country": country.strip(), "postal": ""}


def load_worklist(path):
    info = {}
    p = Path(path)
    if not p.exists():
        return None
    with open(p, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            try:
                pr = int(r["priority"])
            except (KeyError, ValueError):
                pr = None
            info[r["gem_unit_id"]] = (pr, r.get("flag", ""))
    return info


def state_notes(scope):
    """The inlined notes file: united_states/<state>.md or <country>.md."""
    d = REPO_ROOT / "docs" / "country_notes"
    if scope["kind"] == "state":
        d = d / "united_states"
    slug = scope["slug"]
    for name in (slug, slug.replace("-", "_")):
        p = d / f"{name}.md"
        if p.exists():
            return p.read_text(encoding="utf-8").rstrip() + "\n", p
    return None, None


def ws(v):
    return (v or "").strip()


def status_group(status):
    s = ws(status).lower()
    if s in STATUSES_IN_DEVELOPMENT:
        return "in development"
    if s.startswith("shelved"):
        return "shelved"
    if s == "mothballed":
        return "mothballed"
    if s.startswith("cancelled"):
        return "cancelled"
    if s == "retired":
        return "retired"
    if s == "operating":
        return "operating"
    return "unknown"


CAPTIVE_FIELDS = ("Captive industry use", "Captive industry type",
                  "Captive non-industry use")


def unit_tasks(r, year=None, us=True):
    """The manual's per-unit checks plus the gap list, as (text, fields).
    Latest Activity is offered only where the manual uses it: in-development
    units that have gone quiet, shelved units, cancelled-inferred units, and
    inferred statuses with the field blank, and never with a date less than a
    year old (docs/reference/lifecycle_rules.md; state_gate.py latest-activity).
    `us` adds the EIA identifier tasks, which only make sense in the United States."""
    year = year or datetime.date.today().year
    status = ws(r.get("Status")).lower()
    group = status_group(status)
    T = []

    def add(text, *fields):
        T.append((text, [f for f in fields if f]))

    if group == "in development":
        add("This unit is in development. Has the status moved? Look for a start "
            "year or a scheduled operating date, the turbine make and model, the "
            "owner and the capacity. Add a Latest Activity entry only if the project "
            "has gone quiet, meaning the newest report you can find is more than a "
            "year old. Then give the date and the source of that report. If the "
            "project is visibly moving, leave Latest Activity alone.",
            "Status", "Status Detail", "Start year", "Equipment Manufacturer/Model",
            "Turbine/Engine Technology", "Owner(s)", "Capacity (MW)", "Latest Activity")
    elif group == "shelved":
        add("This project is shelved. Was it revived, cancelled, or is it still quiet? "
            "If the newest dated report is more than a year old, record it in Latest "
            "Activity. A newer report goes in the note only. If the newest evidence "
            "of activity is more than four years old, the status becomes "
            "cancelled - inferred 4 y, with no source and the search described in the "
            "note.",
            "Status", "Status Detail", "Latest Activity", "Cancellation year")
    elif group == "mothballed":
        add("This unit is mothballed. Is it still mothballed, back in operation, or "
            "retired? A status change needs two independent publishers. Never fill a "
            "retired year while the status stays mothballed.",
            "Status", "Status Detail", "Retired year")
    if group == "cancelled" and "inferred" in status:
        add("This project was presumed cancelled after four years with no reports. "
            "Has anything been reported since? If so, say in the note whether the "
            "project looks revived, and record the report in Latest Activity only if "
            "it is more than a year old. If the search finds nothing newer, leave the "
            "status as it is."
            + ("" if ws(r.get("Latest Activity")) else
               " Latest Activity is blank, so record the date and source of the "
               "newest report of activity you can find, however old."),
            "Status", "Status Detail", "Latest Activity")
    if group == "cancelled" and not ws(r.get("Cancellation year")):
        add("This unit is cancelled but has no cancellation year. Find the year the "
            "project was dropped or its permit was finally denied, and the document "
            "that says so.",
            "Cancellation year")
    if group == "retired" and not ws(r.get("Retired year")):
        add("This unit is retired but has no retired year. Find it.", "Retired year")

    pr = ws(r.get("Planned retire"))
    if pr:
        try:
            pry = int(pr[:4])
        except ValueError:
            pry = None
        if pry is not None and pry < year:
            add(f"The planned retirement year {pry} is in the past. Did the unit "
                "retire? If so the status is retired with a retired year. If the plan "
                "moved, give the new year and its source.",
                "Status", "Retired year", "Planned retire")
        elif pry == year:
            add(f"Retirement is planned for {year}. Has it retired yet? If nothing "
                "confirms it by December, the manual says to move the planned year "
                "forward.",
                "Status", "Retired year", "Planned retire")
        elif pry is not None:
            add(f"Retirement is planned for {pry}. Does the plan still hold?",
                "Planned retire")
    if "inferred" in status and group != "cancelled" and not ws(r.get("Latest Activity")):
        add("The status was inferred from silence but Latest Activity is blank. "
            "Record the date and source of the newest evidence of activity.",
            "Latest Activity")

    # Gap list (QC checklist rows 8, 16, 17, 18, 19, 26, 38).
    for h in ("Fuel", "Status", "Turbine/Engine Technology", "Owner(s)"):
        if not ws(r.get(h)):
            add(f"{h} is blank. Find it.", h)
    if ws(r.get("Turbine/Engine Technology")).lower() == "unknown":
        add("Turbine/Engine Technology is unknown. Find the technology.",
            "Turbine/Engine Technology")
    cap = ws(r.get("Capacity (MW)"))
    try:
        capv = float(cap) if cap else None
    except ValueError:
        capv = None
    if capv is None or capv == 0:
        add("Capacity (MW) is blank or zero. Find the nameplate electric capacity.",
            "Capacity (MW)")
    if group == "operating" and ws(r.get("Start year")).lower() in ("", "unknown"):
        add("Start year is blank on an operating unit. Find the year it began "
            "commercial operation.", "Start year")
    if ws(r.get(H_UNAME)) in ("", "--"):
        add("Unit name is blank. Say in a question what the source calls this unit; "
            "do not report it as a value.")
    loc_blank = [h for h in ("Latitude", "Longitude", "Location accuracy")
                 if not ws(r.get(h))]
    if loc_blank:
        add(f"{', '.join(loc_blank)}: blank. Fill from a source that gives the "
            "plant's location. Never change a coordinate that is already present.",
            *loc_blank)
    if not ws(r.get("City")):
        add("City is blank. Fill it from a source that places the plant; the source "
            "goes in Location Data Source.", "City")
    if us and "eia" not in ws(r.get("Other IDs (location)")).lower():
        add("Other IDs (location) has no EIA plant code. If the plant appears in EIA "
            "data, give the plant code as a question, not a value.")
    if us and not ws(r.get("Other IDs (unit)")):
        add("Other IDs (unit) is blank. If the unit appears in EIA data, give the "
            "generator ID as a question, not a value.")

    # A value with no data source (Baird's fill-missing-references ask).
    by_src = {}
    for h in RESEARCH_FIELDS + ["City"]:
        v = ws(r.get(h))
        if not v:
            continue
        if h in CAPTIVE_FIELDS + ("CHP",) and v.lower() in ("no", "not found", "unknown"):
            continue
        src = ref_col_for(h)
        if src not in r or ws(r.get(src)):
            continue
        by_src.setdefault(src, []).append((h, v))
    for src, items in by_src.items():
        names = "; ".join(f"{h} (currently {v})" for h, v in items)
        add(f"{names}: the value is present but {src} is empty. Find a document that "
            "states it and report the value with that document. If the document gives "
            "a different value, say so.", *[h for h, _ in items])
    return T


def norm_extra(items):
    out = []
    for it in items or []:
        if isinstance(it, str):
            out.append((it, list(RESEARCH_FIELDS)))
        elif isinstance(it, dict) and it.get("text"):
            out.append((it["text"], list(it.get("fields") or RESEARCH_FIELDS)))
        else:
            sys.exit(f"ERROR: bad --extra-tasks item: {it!r}")
    return out


def identity_block(first, mode):
    lines = ["## Identity", ""]
    items = [("Other names", first.get(H_OTHERNAMES)),
             ("Country", first.get("Country/Area")),
             ("State or province", first.get("State/Province")),
             ("County", first.get(H_COUNTY)),
             ("Major area", first.get(H_MAJOR)),
             ("City", first.get("City")),
             ("Latitude", first.get("Latitude")),
             ("Longitude", first.get("Longitude")),
             ("Location accuracy", first.get("Location accuracy")),
             ("Other IDs (location)", first.get("Other IDs (location)"))]
    for k, v in items:
        lines.append(f"- {k}: {blank(v)}")
    if mode == "update":
        lines.append(f"- Wiki URL: {blank(first.get('Wiki URL'))} (for gap detection only; never cite it)")
    return lines


def plant_fields(unit_tasks_by_uid, plant_tasks):
    """Union of the fields the tasks touch, in RESEARCH_FIELDS order (+ City)."""
    touched = set()
    for tasks in list(unit_tasks_by_uid.values()) + [plant_tasks]:
        for _, fields in tasks:
            touched |= set(fields)
    order = RESEARCH_FIELDS + ["City"]
    return [h for h in order if h in touched]


def render_brief(plant_id, rows, header, mode, wl, notes_text, notes_path, scope,
                 tasks=None, plant_tasks=None):
    first = rows[0]
    kind = scope["kind"]            # "state" or "country"
    name = first.get(H_PLANT, "").strip() or plant_id
    tasks = tasks or {}
    plant_tasks = plant_tasks or []
    L = [f"# {name} ({plant_id})", ""]
    if mode == "blind":
        L += ["Blind calibration brief. GEM's current values are withheld on purpose. "
              "Research every field from scratch.", ""]
    fields = RESEARCH_FIELDS
    if mode == "update":
        n_tasks = sum(len(t) for t in tasks.values()) + len(plant_tasks)
        L += ["## What to check", "",
              "This is an update, not a full review. Do the tasks below and nothing "
              "else. A value you notice in passing that looks wrong goes in a "
              "question, not a change.", ""]
        if plant_tasks:
            L += ["### Whole plant", ""]
            L += [f"- {t}" for t, _ in plant_tasks]
            L.append("")
        for r in rows:
            uid = r.get(H_UNIT)
            ut = tasks.get(uid) or []
            L += [f"### Unit {blank(r.get(H_UNAME))} ({uid}), status "
                  f"{blank(r.get('Status'))}", ""]
            if ut:
                L += [f"- {t}" for t, _ in ut]
            else:
                L.append("- Nothing to check. Leave this unit alone unless a whole-plant "
                         "task above touches it.")
            L.append("")
        if n_tasks:
            fields = plant_fields(tasks, plant_tasks)
        else:
            L += ["Nothing specific was flagged for this plant. Report only a value "
                  "you can show has changed, with its source.", ""]
    L += ["## Fields to report on", "",
          "Report on these fields only, using the exact CSV headers as keys:", ""]
    # Blind briefs must hand over the coordinates to identify the plant, so
    # the location fields cannot be tested blind and are left off the list.
    skip = {"Latitude", "Longitude", "Location accuracy"} if mode == "blind" else set()
    L += [f"- {h}" for h in fields if h not in skip]
    L.append("")
    L += identity_block(first, mode)
    L.append("")

    if mode == "blind":
        L += ["## Units", ""]
        for r in rows:
            L.append(f"- {r.get(H_UNIT)}: {blank(r.get(H_UNAME))}"
                     f" (Other IDs (unit): {blank(r.get('Other IDs (unit)'))})")
        L.append("")
    else:
        vcols = value_cols(header)
        L += ["## Units", ""]
        for r in rows:
            uid = r.get(H_UNIT)
            L += [f"### Unit {blank(r.get(H_UNAME))} ({uid})", "",
                  "| Field | Current value |", "|---|---|"]
            for h in vcols:
                L.append(f"| {h} | {cell(r.get(h))} |")
            L.append("")
        L += ["## Existing sources", "",
              "Carry forward every URL here that is still valid. Do not drop any.", ""]
        for r in rows:
            L.append(f"### Unit {blank(r.get(H_UNAME))} ({r.get(H_UNIT)})")
            L.append("")
            any_src = False
            for h in header:
                if is_source_col(h) and h not in OUT_OF_SCOPE_COLUMNS and (r.get(h) or "").strip():
                    any_src = True
                    L.append(f"- {h}:")
                    for u in split_urls(r.get(h)):
                        L.append(f"  - {u}")
            if not any_src:
                L.append("(no existing sources)")
            L.append("")
        L += ["## Notes and history", ""]
        for r in rows:
            L += [f"### Unit {blank(r.get(H_UNAME))} ({r.get(H_UNIT)})", "",
                  f"- Last Updated: {blank(r.get('Last Updated'))}",
                  f"- Researcher: {blank(r.get('Researcher'))}",
                  "- Notes (verbatim):", "",
                  "```", (r.get(H_NOTES) or "").strip() or "(blank)", "```", ""]
        L += ["## Worklist", ""]
        if wl is None:
            L.append(f"No worklist was found for this {kind}.")
        else:
            for r in rows:
                pr, fl = wl.get(r.get(H_UNIT), (None, ""))
                L.append(f"- {blank(r.get(H_UNAME))} ({r.get(H_UNIT)}): priority "
                         f"{pr if pr is not None else 'none (not on worklist)'}; "
                         f"flag: {fl or 'none'}")
        L.append("")

    L += [f"## {kind.capitalize()} notes", ""]
    if notes_text:
        L += [f"(from {notes_path.relative_to(REPO_ROOT)})", "", notes_text]
    elif kind == "state":
        L.append(f"No state file for {scope['name']} yet. See "
                 "docs/country_notes/united_states.md for what is true of every state.")
    else:
        L.append(f"No country file for {scope['name']} yet. Start from the national "
                 "regulator's plant register and the transmission operator's reports.")
    L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    who = ap.add_mutually_exclusive_group(required=True)
    who.add_argument("--state", default=None, help="a US state, e.g. Maryland")
    who.add_argument("--country", default=None,
                     help="a whole country (Country/Area value), e.g. Germany")
    ap.add_argument("--mode", required=True, choices=["blind", "update"])
    ap.add_argument("--csv", default=str(gogpt_scoped_csv()))
    ap.add_argument("--worklist", default=None)
    ap.add_argument("--plants", default=None, help="comma-separated GEM location IDs")
    ap.add_argument("--batch", default=None)
    ap.add_argument("--scope", default="ladder", choices=["ladder", "all"],
                    help="update mode: ladder = only plants with a task (default); "
                         "all = every plant")
    ap.add_argument("--extra-tasks", default=None,
                    help="JSON file {plant_id: [task, ...], '*': [...]} of extra tasks")
    a = ap.parse_args()
    extra = {}
    if a.extra_tasks:
        ep = Path(a.extra_tasks)
        if not ep.exists():
            sys.exit(f"ERROR: {ep} not found")
        extra = {k: norm_extra(v) for k, v in
                 json.loads(ep.read_text(encoding="utf-8")).items()}

    scope = make_scope(state=a.state, country=a.country)
    name, slug = scope["name"], scope["slug"]
    is_us = scope["country"].lower() == "united states"
    csv_path = Path(a.csv).resolve()
    if not csv_path.exists():
        sys.exit(f"ERROR: {csv_path} not found; run scope_filter.py first")
    wl_tag = f"us-{slug}" if scope["kind"] == "state" else slug
    wl_path = Path(a.worklist) if a.worklist else work_dir() / f"worklist_{wl_tag}.csv"
    wl = load_worklist(wl_path)
    batch_tag = f"us-{scope['postal']}" if scope["kind"] == "state" else slug
    batch = Path(a.batch).resolve() if a.batch else (REPO_ROOT / "batches" / batch_tag)

    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        need = [H_LOC, H_UNIT, H_PLANT, "Country/Area", "State/Province"]
        miss = [h for h in need if h not in header]
        if miss:
            sys.exit(f"ERROR: columns missing from {csv_path}: {miss} (schema drift?)")
        plants = {}
        for r in reader:
            if r["Country/Area"].strip().lower() != scope["country"].lower():
                continue
            if (scope["kind"] == "state"
                    and r["State/Province"].strip().lower() != name.lower()):
                continue
            plants.setdefault(r[H_LOC].strip(), []).append(r)

    if a.plants:
        want = {p.strip() for p in a.plants.split(",") if p.strip()}
        unknown = want - set(plants)
        if unknown:
            sys.exit(f"ERROR: plants not found in {name}: {sorted(unknown)}")
        plants = {k: v for k, v in plants.items() if k in want}
    if not plants:
        sys.exit(f"ERROR: no rows for {name} in {csv_path}")
    unknown_extra = set(extra) - set(plants) - {"*"}
    if unknown_extra:
        sys.exit(f"ERROR: --extra-tasks plants not in {name}: {sorted(unknown_extra)}")

    # Tasks per unit and per plant; ladder scope keeps only tasked plants.
    tasks, plant_tasks, not_tasked = {}, {}, []
    for pid, rows in plants.items():
        tasks[pid] = ({r[H_UNIT]: unit_tasks(r, us=is_us) for r in rows}
                      if a.mode == "update" else {})
        own = extra.get(pid, [])
        plant_tasks[pid] = own + extra.get("*", [])
        has_task = any(tasks[pid].values()) or bool(own)
        if a.mode == "update" and a.scope == "ladder" and not has_task:
            not_tasked.append({"plant_id": pid, "plant_name": rows[0].get(H_PLANT, "").strip(),
                               "unit_ids": [r[H_UNIT] for r in rows]})
    if not_tasked:
        plants = {k: v for k, v in plants.items()
                  if k not in {p["plant_id"] for p in not_tasked}}
    if not plants:
        sys.exit(f"ERROR: no plant in {name} has a task; use --scope all")

    for sub in ("briefs", "shards", "staging", "deliverables"):
        (batch / sub).mkdir(parents=True, exist_ok=True)
    if a.mode == "blind":
        (batch / "briefs" / "_hidden").mkdir(exist_ok=True)
    for sub in ("shards", "deliverables"):
        d = batch / sub
        if not any(d.iterdir()):
            (d / ".gitkeep").touch()

    notes_text, notes_path = state_notes(scope)
    hcols = hidden_cols(header)
    index = []
    n_units = 0
    for pid, rows in plants.items():
        text = render_brief(pid, rows, header, a.mode, wl, notes_text, notes_path, scope,
                            tasks=tasks.get(pid), plant_tasks=plant_tasks.get(pid))
        bpath = batch / "briefs" / f"{pid}.md"
        bpath.write_text(text, encoding="utf-8")
        if a.mode == "blind":
            hidden = {"plant_id": pid, "plant_name": rows[0].get(H_PLANT, ""),
                      "units": {r[H_UNIT]: {h: r.get(h, "") for h in hcols} for r in rows}}
            (batch / "briefs" / "_hidden" / f"{pid}.json").write_text(
                json.dumps(hidden, indent=2, ensure_ascii=False), encoding="utf-8")
        prios = [wl[r[H_UNIT]][0] for r in rows
                 if wl and r[H_UNIT] in wl and wl[r[H_UNIT]][0] is not None]
        try:
            rel = str(bpath.relative_to(REPO_ROOT))
        except ValueError:
            rel = str(bpath)
        index.append({
            "plant_id": pid, "plant_name": rows[0].get(H_PLANT, "").strip(),
            "brief_path": rel, "unit_ids": [r[H_UNIT] for r in rows],
            "n_units": len(rows), "max_priority": min(prios) if prios else None,
            "wiki_url": None if a.mode == "blind" else (rows[0].get("Wiki URL") or None),
            "n_tasks": sum(len(t) for t in tasks.get(pid, {}).values())
                       + len(plant_tasks.get(pid, [])),
            "fields": (plant_fields(tasks.get(pid, {}), plant_tasks.get(pid, []))
                       if a.mode == "update" else list(RESEARCH_FIELDS)),
        })
        n_units += len(rows)
    index.sort(key=lambda p: (p["max_priority"] is None, p["max_priority"] or 0, p["plant_name"].lower()))
    idx_path = batch / "briefs" / "_index.json"
    # `state` / `postal` stay for US batches (older readers key on them); `where`
    # is the generic scope every reader should prefer.
    idx_path.write_text(json.dumps({
        "state": name if scope["kind"] == "state" else "",
        "postal": scope["postal"], "where": scope,
        "mode": a.mode, "csv": str(csv_path),
        "scope": "all" if a.mode == "blind" else a.scope,
        "generated": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "plants": index, "not_tasked": not_tasked}, indent=2, ensure_ascii=False),
        encoding="utf-8")

    tag = f" ({scope['postal'].upper()})" if scope["postal"] else ""
    print(f"{scope['kind']}: {name}{tag}  mode: {a.mode}  scope: {a.scope}")
    print(f"plants: {len(index)}  units: {n_units}  tasks: "
          f"{sum(p['n_tasks'] for p in index)}  not tasked (left out): {len(not_tasked)}  "
          f"worklist: {'yes (' + str(wl_path) + ')' if wl is not None else 'none'}")
    print(f"batch dir: {batch}")
    print(f"index: {idx_path}")


if __name__ == "__main__":
    main()

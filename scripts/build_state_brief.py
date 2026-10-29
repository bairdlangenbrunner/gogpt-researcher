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
    briefs/_index.json               plants, brief paths, unit IDs, max priority,
                                     and each plant's tasks (text, fields, and
                                     the QC/Country checklist rows they serve)
    briefs/_irp.md                   with --irp: the IRP block for the statewide agent
    (--existing-links)               adds a "links already in the database that are gone"
                                     section to each affected plant's brief
    briefs/_scope.md                 every scope: the add rule (when a project GEM lacks is a new
                                     record and when it is a watch item, Baird 2026-10-23), then
                                     with --ids or a docs/coverage/<scope>.json list the EIA
                                     plants missing from GEM (one task each) and the statewide
                                     sources to search, for the scope-wide agent; the gates
                                     `ids_followup`, `statewide-coverage` and `watch-case` check
                                     the answers
    briefs/_harvest.md               with --harvest: the PSC dockets and interconnection queue
                                     entries that match no GEM plant (leads for new plants,
                                     uprates or retirements), for the scope-wide agent
    briefs/_captive.md               with --captive: the captive LNG sheet block (rows 6
                                     and 44) and, for a US state, the data-center search
                                     block (row 39) for the scope-wide agent
    briefs/_data_centers.md          with --data-centers: one named add task per data center
                                     site at or above the threshold (or with unknown capacity),
                                     check tasks for sites GEM already has, one line per site
                                     that needs no record
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
            empty; conversion naming, fuel, technology and start year; waste
            heat that is not a steam turbine; a start year on a shelved or
            cancelled unit).
            The "Fields to report on" list is narrowed to the fields those
            tasks touch. With --scope ladder, operating units with no task
            are not researched.
    blind   identity only (plant, location, IDs, unit IDs and names). Every
            GEM value, source, note, edit history, wiki URL and worklist
            priority is withheld and written to briefs/_hidden/ for the
            compare step. The one thing a blind brief cannot avoid is the
            exact header names in the report-on list (for example
            "Capacity (MW)"), which carry no plant data.

Scope (update mode only; blind always takes every plant):
    --scope ladder   (default) only plants where at least one unit has a task,
                     that have an entry in --extra-tasks, or that have a gone
                     link in --existing-links. Plants left out
                     are listed under "not_tasked" in _index.json.
    --scope all      every plant, and every operating unit gets the narrow
                     last-minute check (still operating, retirement or owner
                     change; checklist rows 50 and 43). A plant still with no
                     task (all units retired or cancelled) is asked only whether
                     each status holds.
    --extra-tasks F  JSON {"<GEM location ID>": [task, ...], "*": [task, ...]}
                     for backlog rows and scan hits. A task is a string
                     (grants the full field list) or {"text": ..., "fields":
                     [exact headers], "checks": [checklist row numbers]}.
                     "*" tasks go on every brief and do not
                     by themselves pull a plant into ladder scope.
    --validation F   work/validation_<tag>.json from validation_report.py (the
                     database's validation errors, QC/Country checklist rows 7
                     and 54). Each "fix" item becomes a task on its unit, or a
                     whole-plant task when it has no unit in the export; a
                     missing data source the gap list already asks about is not
                     repeated. An item on a plant that has coal units in the
                     unfiltered export (--all-csv), or on a coal-to-gas conversion
                     unit, is marked optional under the manual. Web-UI-only items
                     are not briefed. A plant with a fix is in ladder scope.
    --data-centers [F]  work/permits/<tag>/_data_centers.json from data_center_fleets.py
                     (or the path F). Writes briefs/_data_centers.md and a check task
                     on each GEM plant a site matches. A missing file is reported and
                     skipped.
    --ids F          work/ids_<tag>.json from match_ids.py (EIA-860M, EIP and
                     Sierra Club matching, checklist row 38). Same shape and
                     handling as --validation. With --ids the two generic
                     "give the EIA code as a question" tasks are dropped: the
                     matcher has already looked the codes up, and what it could
                     not settle arrives as a specific task. Every EIA plant
                     the matcher lists as missing from GEM also becomes a named
                     task in briefs/_scope.md (add / below threshold / out of
                     scope / already in GEM under another name, with evidence).
    --promote D      a batch's staging dir (with review_log.jsonl and
                     staged_monitor.json): every watch item the review page
                     called "incorporate into database" becomes work for this
                     sweep. On a plant GEM tracks it is a whole-plant task that
                     names the watch reason, the reviewer's note and source, and
                     pulls the plant into ladder scope (checklist row 51 unless
                     the record carries its own rows). An item new to the
                     tracker has no plant to brief: it is listed under
                     "promoted_new" in _index.json and printed, so the discovery
                     lane writes the full new-plant record. Repeatable.
    --irp F          work/irp_us-<state-slug>.json from irp_sheet.py (the US IRPs
                     tab read for this state, checklist rows 34 and 37). Each
                     plant task in it becomes a whole-plant task on its brief and
                     pulls the plant into ladder scope; the tab's plain-language
                     block is written to briefs/_irp.md for the statewide agent
                     (build_sweep_args.py --extra-brief can inline it too), and
                     the index gets an "irp" entry (file, brief path, utilities,
                     plan links, skipped) that assemble_state.py uses to mark
                     records sourced from a plan. A state the tab does not cover
                     writes a brief that says the step was skipped.
"""
import argparse
import csv
import datetime
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from paths import REPO_ROOT, gem_export_csv, gogpt_scoped_csv, require_fresh_export, work_dir
from schema_constants import (CAPACITY_THRESHOLD_EU_UK_MW, CAPACITY_THRESHOLD_MW, EU_UK_COUNTRIES,
                              OUT_OF_SCOPE_COLUMNS, READ_ONLY_COLUMNS, RESEARCH_FIELDS,
                              STATUSES_IN_DEVELOPMENT)
from build_review_package import ref_col_for
import geo

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


def empty_source_values(r):
    """(field, value) pairs where the value is present but its Data Source is empty."""
    out = []
    # City is left out: with an exact point it needs no source of its own
    # (Baird 2026-10-21)
    for h in RESEARCH_FIELDS:
        v = ws(r.get(h))
        if not v:
            continue
        if h in CAPTIVE_FIELDS + ("CHP",) and v.lower() in ("no", "not found", "unknown"):
            continue
        src = ref_col_for(h)
        if src not in r or ws(r.get(src)):
            continue
        out.append((h, v))
    return out


TIMEPOINT_RE = re.compile(r", timepoint \d+$")
COAL_TECH = ("subcritical", "supercritical", "ultra-supercritical", "igcc", "cfb",
             "circulating fluidized bed")


def conversion_tasks(r, peers=None):
    """Checklist rows 12 and 13 for one unit, as (text, fields, checks).
    A conversion is a unit whose Conversion/replacement? says so, whose
    converted-from fuel is filled, or whose name carries "timepoint". The name
    must end "<name>, timepoint N" (docs/reference/unit_conventions.md), a coal
    conversion must carry gas fuel and a gas technology, and the gas start
    year must not precede the coal unit's retired year. `peers` maps GEM unit
    ID to the unfiltered export's row, so the coal unit can be looked up."""
    out = []
    uname = ws(r.get(H_UNAME))
    conv = ws(r.get("Conversion/replacement?")).lower()
    from_fuel = ws(r.get("Conversion from/replacement of (fuel)")).lower()
    from_uid = ws(r.get("Conversion from/replacement of (GEM unit ID)"))
    is_conv = conv == "conversion" or (from_fuel and conv != "replacement")
    has_tp = "timepoint" in uname.lower()
    if not (is_conv or has_tp):
        return out
    if is_conv and not has_tp:
        out.append((f'This unit is a conversion but its name "{uname}" has no timepoint. '
                    'The gas unit is named "<name>, timepoint 2" and the coal unit '
                    '"<name>, timepoint 1". Say in a question what both names should be.',
                    [], [12]))
    elif has_tp and not TIMEPOINT_RE.search(uname):
        out.append((f'The unit name "{uname}" does not follow the timepoint form '
                    '"<name>, timepoint N" (a comma, a space, then the word). Say in a '
                    "question what the name should be.", [], [12]))
    if has_tp and not conv:
        out.append(("The unit name says timepoint but the conversion fields are blank. "
                    "Find out whether this unit was converted from another fuel, which "
                    "unit it replaced, and the document that says so. Report "
                    "Conversion/replacement? with that document, and name the earlier "
                    "unit in a question.", ["Conversion/replacement?"], [12, 13]))
    if from_fuel.startswith("coal"):
        fuel = ws(r.get("Fuel")).lower()
        tech = ws(r.get("Turbine/Engine Technology")).lower()
        if "gas" not in fuel:
            out.append((f"This is a coal-to-gas conversion but the fuel is {fuel or 'blank'}. "
                        "Find the fuel the converted unit burns.", ["Fuel"], [13]))
        if tech in COAL_TECH:
            out.append((f"This is a coal-to-gas conversion but the technology is {tech}, "
                        "a coal technology. A converted boiler is usually a steam turbine. "
                        "Find the technology.", ["Turbine/Engine Technology"], [13]))
        coal = (peers or {}).get(from_uid) if from_uid else None
        sy = ws(r.get("Start year"))[:4]
        ry = ws((coal or {}).get("Retired year"))[:4]
        if sy.isdigit() and ry.isdigit() and int(sy) < int(ry):
            out.append((f"The gas start year {sy} is earlier than the coal unit's retired "
                        f"year {ry} ({from_uid}). The gas unit cannot start before the coal "
                        "unit stopped. Find the year the unit first ran on gas.",
                        ["Start year"], [13]))
    return out


def unit_tasks(r, year=None, us=True, peers=None, status_pass=False, location=False):
    """The manual's per-unit checks plus the gap list, as (text, fields, checks).
    `checks` are the row numbers of the QC/Country checklist tab each task
    serves (review_app/checklist.py ROWS); they ride through the shard into
    the staged records so the review page can file every edit under its box.
    Latest Activity is offered only where the manual uses it: in-development
    units that have gone quiet, shelved units, cancelled-inferred units, and
    inferred statuses with the field blank, and never with a date less than a
    year old (docs/reference/lifecycle_rules.md; state_gate.py latest-activity).
    `us` adds the EIA identifier tasks, which only make sense in the United
    States and are dropped when match_ids.py has already done the lookup (--ids).
    `peers` (GEM unit ID to unfiltered-export row) lets the conversion checks
    see the coal unit. `status_pass` (--scope all) gives every operating unit
    the narrow last-minute status and owner check, rows 50 and 43."""
    year = year or datetime.date.today().year
    status = ws(r.get("Status")).lower()
    group = status_group(status)
    T = []

    def add(text, *fields, checks=()):
        T.append((text, [f for f in fields if f], list(checks)))

    if group == "in development":
        add("This unit is in development. Has the status moved? Look for a start "
            "year or a scheduled operating date, the turbine make and model, the "
            "owner and the capacity. A projected start year is a scheduled event: the "
            "Event Year is the projected year and the Source Year is the year the "
            "source reported it, and the human adds it as a new entry, never by "
            "changing an existing one. A shelved or cancelled unit gets no scheduled "
            "operating event. Add a Latest Activity entry only if the project "
            "has gone quiet, meaning the newest report you can find is more than a "
            "year old. Then give the date and the source of that report. If the "
            "project is visibly moving, leave Latest Activity alone.",
            "Status", "Status Detail", "Start year", "Equipment Manufacturer/Model",
            "Turbine/Engine Technology", "Owner(s)", "Capacity (MW)", "Latest Activity",
            checks=[10] + ([49] if status == "construction" else []))
    elif group == "shelved":
        add("This project is shelved. Was it revived, cancelled, or is it still quiet? "
            "If the newest dated report is more than a year old, record it in Latest "
            "Activity. A newer report goes in the note only. If the newest evidence "
            "of activity is more than four years old, the status becomes "
            "cancelled - inferred 4 y. The inferred status carries the Latest Activity "
            "source as its data source and a milestone year equal to the Latest Activity "
            "date plus four years; describe the search in the note.",
            "Status", "Status Detail", "Latest Activity", "Cancellation year",
            checks=[24])
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
            "Status", "Status Detail", "Latest Activity", checks=[24])
    if group == "cancelled" and not ws(r.get("Cancellation year")):
        add("This unit is cancelled but has no cancellation year. Find the year the "
            "project was dropped or its permit was finally denied, and the document "
            "that says so.",
            "Cancellation year")
    if group == "retired" and not ws(r.get("Retired year")):
        add("This unit is retired but has no retired year. Find it.", "Retired year",
            checks=[22])

    pr = ws(r.get("Planned retire"))
    if pr:
        try:
            pry = int(pr[:4])
        except ValueError:
            pry = None
        if pry is not None and pry < year:
            add(f"The planned retirement year {pry} is in the past. Did the unit "
                "retire? If so the status is retired with a retired year. If the plan "
                "moved, give the new year and its source; it is a new scheduled "
                "retirement event (Event Year the new year, Source Year the year the "
                "source reported it), never a change to the old entry.",
                "Status", "Retired year", "Planned retire", checks=[21, 23])
        elif pry == year:
            add(f"Retirement is planned for {year}. Has it retired yet? If it has not and "
                f"no source confirms it by December, the manual adds a new scheduled "
                f"retirement event with Event Year {year + 1} and Source Year {year}. "
                "The existing entry is never edited; the action tells the human to add "
                "a new entry. A maintenance change to the retirement date is also a new "
                "scheduled retirement event, never a new operating milestone.",
                "Status", "Retired year", "Planned retire", checks=[21, 23])
        elif pry is not None:
            add(f"Retirement is planned for {pry}. Does the plan still hold?",
                "Planned retire", checks=[21])
    if "inferred" in status and group != "cancelled" and not ws(r.get("Latest Activity")):
        add("The status was inferred from silence but Latest Activity is blank. "
            "Record the date and source of the newest evidence of activity.",
            "Latest Activity", checks=[24])

    # Gap list (QC checklist rows 8, 16, 17, 18, 19, 26, 38).
    for h in ("Fuel", "Status", "Turbine/Engine Technology", "Owner(s)"):
        if not ws(r.get(h)):
            add(f"{h} is blank. Find it.", h,
                checks=[8] + ({"Owner(s)": [19], "Turbine/Engine Technology": [17]}
                              .get(h, [])))
    if ws(r.get("Turbine/Engine Technology")).lower() == "unknown":
        add("Turbine/Engine Technology is unknown. Find the technology.",
            "Turbine/Engine Technology", checks=[17])
    cap = ws(r.get("Capacity (MW)"))
    try:
        capv = float(cap) if cap else None
    except ValueError:
        capv = None
    if capv is None or capv == 0:
        add("Capacity (MW) is blank or zero. Find the nameplate electric capacity.",
            "Capacity (MW)", checks=[16])
    if group == "operating" and ws(r.get("Start year")).lower() in ("", "unknown"):
        add("Start year is blank on an operating unit. Find the year it began "
            "commercial operation.", "Start year", checks=[9, 18])
    if ws(r.get(H_UNAME)) in ("", "--"):
        add("Unit name is blank. Say in a question what the source calls this unit; "
            "do not report it as a value.", checks=[11])
    # with --location the location step (location_candidates.py) owns the
    # coordinate tasks, so the generic blank-location task is left out
    loc_blank = [h for h in ("Latitude", "Longitude", "Location accuracy")
                 if not ws(r.get(h))] if not location else []
    if loc_blank:
        add(f"{', '.join(loc_blank)}: blank. Fill from a source that gives the "
            "plant's location. Never change a coordinate that is already present.",
            *loc_blank, checks=[8, 25])
    # a blank City matters only while the point is not exact (Baird 2026-10-21)
    if not ws(r.get("City")) and not (
            ws(r.get("Location accuracy")).lower() == "exact"
            and ws(r.get("Latitude")) and ws(r.get("Longitude"))):
        add("City is blank. Fill it from a source that places the plant; the source "
            "goes in Location Data Source.", "City", checks=[26])
    if us and "eia" not in ws(r.get("Other IDs (location)")).lower():
        add("Other IDs (location) has no EIA plant code. If the plant appears in EIA "
            "data, give the plant code as a question, not a value.", checks=[38])
    if us and not ws(r.get("Other IDs (unit)")):
        add("Other IDs (unit) is blank. If the unit appears in EIA data, give the "
            "generator ID as a question, not a value.", checks=[38])

    # Conversions and waste heat (checklist rows 12, 13, 14) and the start-year
    # rule for shelved and cancelled units (row 20).
    for text, fields, checks in conversion_tasks(r, peers):
        add(text, *fields, checks=checks)
    fuel = ws(r.get("Fuel")).lower()
    tech = ws(r.get("Turbine/Engine Technology")).lower()
    if "waste heat" in fuel and tech and tech != "steam turbine":
        add(f"The fuel is waste heat but Turbine/Engine Technology is {tech}. A unit "
            "running on waste heat is a steam turbine. Find a document that describes "
            "the unit and report the technology with it.",
            "Turbine/Engine Technology", checks=[14])
    if group in ("shelved", "cancelled") and ws(r.get("Start year")):
        add(f"This unit is {status} but has a start year ({ws(r.get('Start year'))}). "
            "The manual says shelved and cancelled units never carry a start year. "
            "First confirm the status still holds. If it does, ask in a question for "
            "the start year to be cleared.", "Status", checks=[20])

    # Last-minute status pass (rows 49 and 50, with row 43): every operating unit
    # when the whole scope is briefed. Construction units already have the
    # in-development task above.
    if status_pass and group == "operating":
        add("Last check on an operating unit. Is it still operating? Look for a "
            "retirement, a planned retirement date, a mothballing, or a change of "
            "owner announced since the last update. Do not research anything else "
            "on this unit.",
            "Status", "Retired year", "Planned retire", "Owner(s)", checks=[50, 43])

    # A value with no data source (Baird's fill-missing-references ask).
    by_src = {}
    for h, v in empty_source_values(r):
        by_src.setdefault(ref_col_for(h), []).append((h, v))
    for src, items in by_src.items():
        names = "; ".join(f"{h} (currently {v})" for h, v in items)
        add(f"{names}: the value is present but {src} is empty. Find a document that "
            "states it and report the value with that document. If the document gives "
            "a different value, say so.", *[h for h, _ in items])
    return T


def norm_extra(items):
    """--extra-tasks items as (text, fields, checks). A dict item may carry
    "checks": [row numbers of the QC/Country checklist tab]."""
    out = []
    for it in items or []:
        if isinstance(it, str):
            out.append((it, list(RESEARCH_FIELDS), []))
        elif isinstance(it, dict) and it.get("text"):
            out.append((it["text"], list(it.get("fields") or RESEARCH_FIELDS),
                        [int(c) for c in it.get("checks") or []]))
        else:
            sys.exit(f"ERROR: bad --extra-tasks item: {it!r}")
    return out


def task_dicts(tasks):
    """(text, fields, checks) tuples as the dicts _index.json stores."""
    return [{"text": t, "fields": list(f), "checks": list(c)} for t, f, c in tasks]


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
    links = geo.links_for(first.get("Latitude"), first.get("Longitude"))
    if links:
        lines.append(f"- Satellite view: {links['satellite']}")
        lines.append(f"- Map pin: {links['pin']}")
    if mode == "update":
        lines.append(f"- Wiki URL: {blank(first.get('Wiki URL'))} (for gap detection only; never cite it)")
    return lines


def plant_fields(unit_tasks_by_uid, plant_tasks):
    """Union of the fields the tasks touch, in RESEARCH_FIELDS order (+ City),
    then any other column a task names (a validation error can touch CCS,
    Backup Power, Disrupted by conflict or Employment Notes)."""
    touched = set()
    for tasks in list(unit_tasks_by_uid.values()) + [plant_tasks]:
        for _, fields, _ in tasks:
            touched |= set(fields)
    order = RESEARCH_FIELDS + ["City"]
    return [h for h in order if h in touched] + sorted(touched - set(order))


def load_validation(path, scope, producer="validation_report.py"):
    """Fix items from validation_report.py (under "errors") or match_ids.py,
    irp_sheet.py, captive_lng.py (under "tasks") as {plant_id: [(unit_id or
    None, item)]}. Each item gets the checklist row it serves unless it names
    its own: row 7 (the validation report), 38 (the ID match), 37 (the IRP
    step) or 6 and 44 (the captive LNG sheet)."""
    default_checks = {"match_ids": [38], "irp_sheet": [37], "captive_lng": [6, 44],
                      "location_candidates": [25]}.get(producer.split(".")[0], [7])
    p = Path(path)
    if not p.exists():
        sys.exit(f"ERROR: {p} not found; run {producer} first")
    data = json.loads(p.read_text(encoding="utf-8"))
    where = data.get("where") or {}
    if (where.get("name", "").lower(), where.get("kind")) != (scope["name"].lower(),
                                                              scope["kind"]):
        sys.exit(f"ERROR: {p} is for {where.get('name')!r}, not {scope['name']!r}")
    out = {}
    for e in data.get("errors", []) + data.get("tasks", []):
        if e.get("kind") == "fix" and e.get("task"):
            e = dict(e)
            e["checks"] = [int(c) for c in e.get("checks") or default_checks]
            out.setdefault(e["plant_id"], []).append((e.get("unit_id"), e))
    return out


EIA_DECISIONS = ("add (stage it as a new plant in the newplants lane)",
                 "below_threshold (under the add threshold, with the capacity evidence)",
                 "out_of_scope (not a combustion plant GOGPT tracks, with the evidence)",
                 "already_in_gem (it sits under another name; give the GEM plant ID)")


def eia_lead_tasks(ids_path):
    """EIA plants of 50 MW or more that match_ids.py found in no GEM plant, as
    [{eia_id, name, capacity_mw, status, county, owner}]. Empty without the file."""
    if not ids_path or not Path(ids_path).exists():
        return []
    data = json.loads(Path(ids_path).read_text(encoding="utf-8"))
    out = []
    for d in data.get("leads") or []:
        if d.get("source") != "eia":
            continue
        m = re.search(r"\d+", d.get("ids") or "")
        out.append({"eia_id": m.group(0) if m else "", "name": d.get("name"),
                    "capacity_mw": d.get("capacity_mw"), "status": d.get("status"),
                    "county": d.get("county"), "owner": d.get("owner"),
                    "staged_in": d.get("staged_in")})
    return out


ADD_RULE = [
    "## When a project GEM lacks is added (Baird 2026-10-23)", "",
    "Write a new plant record (shards/_state.json, newplants) or a new unit at a tracked plant "
    "(newunits) as soon as ONE verified public source names a gas or oil generating project, "
    "places it in this scope, and gives a capacity at the threshold ({thr} MW; engine and "
    "aeroderivative sets summed), a unit count with a plant total, or no capacity at all. The "
    "manual adds a plant whose capacity cannot be found with the cell blank and removes it later "
    "if it proves small. A missing start year, owner, turbine model or exact point never holds "
    "an add back: leave the field blank and say in researcher_notes what was not found.", "",
    "The manual's status ladder decides the status, never the add. A long-range planning "
    "document, a grid-operator interconnection queue entry or a press announcement is "
    "announced. A permit application, land, financing, a prior-approval docket or a signed "
    "interconnection agreement is pre-construction. A project found already cancelled, shelved "
    "or retired since 2020 is an add with that status. A queue entry under a shell company's "
    "name is still an add at announced, named after the queue entry or its site; the database "
    "already holds such plants.", "",
    "A watch item (monitor, new to the tracker) is only for these cases, and names its case in "
    "watch_case: no_generation (a campus, site or program with no generating unit named yet), "
    "under_threshold (every unit under the bar and not an engine or aeroderivative set that sums "
    "to it), drive_or_storage (generator or mechanical drive, or thermal or storage, "
    "unresolved), duplicate_check (it may be a unit GEM already has; prefer a qa question), "
    "not_committed (a plan studies it only as an option), "
    "other_scope (another state or country; the evidence file lists it as a handoff), "
    "unverified (nothing passed the verifier yet). Anything else is an add.", "",
    "A data center is never a watch case for being a data center or for being backup power. "
    "A gas or diesel plant at a data center, routine power or a backup engine fleet, is an add "
    "when the summed electrical nameplate of its generators reaches the threshold ({thr} MW), "
    "with the capacity cell blank when no figure can be found. Name it \"<Operator> <Place> "
    "Data Center power station\", name the data center in Project Links, and set Backup Power "
    "yes at unit level only on backup engine units (briefs/_data_centers.md lists the sites "
    "when a permit harvest exists).", "",
    "Every new record uses exact export headers in fields and keys refs by Data Source column "
    "with a link for every filled field; a grid-operator spreadsheet is cited by the download "
    "address with the matching row quoted in researcher_notes.", "",
]


DC_ANSWER_VERDICTS = ("at_threshold", "unknown_capacity", "no_documents", "in_gem")

DC_CONVENTION = (
    "The convention (September 2026 manual, Baird 2026-10-27): a data center backup engine "
    "fleet is a plant when the summed electrical nameplate of its generators reaches the "
    "threshold ({thr} MW). A routine-power gas or diesel plant at a data center is an add too. "
    "Capacity unknown means add with the capacity cell blank. Never a watch item for being "
    "backup. Name it \"<Operator> <Place> Data Center power station\", name the data center "
    "in Project Links, one unit row per permit phase or building group, fuel diesel or gas as "
    "the permit says, technology internal combustion with Number Of Engines and Capacity Per "
    "Engine from the permit, Captive industry use power, Captive industry type data center, "
    "Backup Power yes at unit level on backup units only, Captive Data Source the permit.")


def load_data_centers(path):
    """The data center harvest file (contract in notes/data_center_backup_plan.md) or
    None, with a clear message, when it is missing."""
    p = Path(path)
    if not p.exists():
        print(f"NOTE: {p} not found; the data center step is skipped. Run data_center_fleets.py "
              "for this scope first.")
        return None
    data = json.loads(p.read_text(encoding="utf-8"))
    data["_path"] = str(p)
    data.setdefault("sites", [])
    return data


def _dc_facts(x):
    bits = []
    if x.get("address") or x.get("city"):
        bits.append("at " + ", ".join(v for v in (x.get("address"), x.get("city")) if v))
    if x.get("permit_numbers"):
        bits.append("permit " + ", ".join(x["permit_numbers"]))
    if x.get("issue_date"):
        bits.append(f"issued {x['issue_date']}")
    if x.get("engine_count") is not None:
        bits.append(f"{x['engine_count']} engines")
    if x.get("capacity_per_engine_mw") is not None:
        bits.append(f"{x['capacity_per_engine_mw']} MW per engine")
    bits.append(f"{x['summed_nameplate_mw']} MW summed" if x.get("summed_nameplate_mw") is not None
                else "no usable nameplate sum")
    if x.get("fuel"):
        bits.append(f"fuel {x['fuel']}")
    out = "; ".join(bits) + "."
    for ph in x.get("phases") or []:
        out += (f" Phase {ph.get('label')}: {ph.get('engines')} engines, {ph.get('mw')} MW"
                + (f", {ph['status_hint']}" if ph.get("status_hint") else "") + ".")
    if x.get("permit_urls"):
        out += " Permit links: " + ", ".join(x["permit_urls"]) + "."
    if x.get("source_notes"):
        out += " " + x["source_notes"]
    return out


def render_data_centers_brief(data, threshold_mw=50):
    thr = data.get("threshold_mw") or threshold_mw
    sites = data["sites"]
    by = lambda v: [x for x in sites if x.get("verdict") == v]
    L = ["# Data center sites", "",
         f"From the permit harvest for {data.get('scope', 'this scope')} dated "
         f"{data.get('generated', 'date not given')}. " + DC_CONVENTION.format(thr=thr), "",
         "Answer every site below that has a task by writing batches/<tag>/coverage.json under "
         "`data_centers`, keyed by the site id: `decision` is add (with the `record_id` of the "
         "newplants record), already_in_gem (with `plant_id`), update (with the `record_id` of "
         "the updates record, when the permit disagrees with GEM), below_threshold (with "
         "`summed_nameplate_mw`, the number you added up), no_generators, not_data_center or "
         "nothing_found, plus a plain `note` saying what was read or searched. A site the "
         "harvester summed at the threshold is an add unless the note names the GEM plant that "
         "already holds the fleet. A site with no usable sum, or no document on record, is an "
         "add once you find generators; close it another way only with the number or the "
         "search you did.", ""]
    L += ["## Add tasks", ""]
    adds = by("at_threshold") + by("unknown_capacity")
    if not adds:
        L += ["No site needs an add.", ""]
    for x in adds:
        what = ("The fleet sums to the threshold or more. Add it as a new plant."
                if x["verdict"] == "at_threshold" else
                "The permit lists generators but no usable nameplate. Add it as a new plant with the "
                "capacity cell blank, and say in the notes what was not found.")
        L += [f"- Site {x['site_id']}: {x.get('name') or 'unnamed'} (operator "
              f"{x.get('operator') or 'not given'}). {what} Verify the permit with the verifier, "
              f"sum the generator electrical MW yourself, and write a newplants record. Coverage "
              f"answer: `data_centers.{x['site_id']}`. Facts: {_dc_facts(x)}"]
    L += ["", "## Search tasks for sites with no document on record", ""]
    nod = by("no_documents")
    if not nod:
        L += ["None.", ""]
    for x in nod:
        L += [f"- Site {x['site_id']}: {x.get('name') or 'unnamed'} (operator "
              f"{x.get('operator') or 'not given'}). No permit or filing is on record. Search the "
              "state air permit portal, the county, the utility's filings and the operator's own "
              "announcements for the generator fleet or a routine-power plant. Generators found at the "
              "threshold, or found with no usable rating, mean a newplants record and the answer add. "
              "Otherwise answer below_threshold with the sum, no_generators, not_data_center or "
              f"nothing_found, and say in the note what you searched. Coverage answer: "
              f"`data_centers.{x['site_id']}`. Facts: {_dc_facts(x)}"]
    L += ["", "## Check tasks for sites GEM already has", ""]
    ing = by("in_gem")
    if not ing:
        L += ["None.", ""]
    for x in ing:
        L += [f"- Site {x['site_id']}: {x.get('name') or 'unnamed'} is GEM plant "
              f"{x.get('gem_plant_name') or 'name not given'} ({x.get('gem_plant_id')}). Compare "
              "the fleet size, the phases, the Backup Power box and the engine counts with the "
              "newest permit. If they agree, answer already_in_gem. If not, write an updates "
              f"record and answer update. Coverage answer: `data_centers.{x['site_id']}`. "
              f"Facts: {_dc_facts(x)}"]
    L += ["", "## Sites that need no record", ""]
    rest = by("below_threshold") + by("no_generators")
    if not rest:
        L += ["None.", ""]
    for x in rest:
        why = (f"below the threshold at {x.get('summed_nameplate_mw')} MW"
               if x["verdict"] == "below_threshold" else "the permit covers no generators")
        L.append(f"- {x['site_id']}: {x.get('name') or 'unnamed'}, {why}. Answer below_threshold "
                 "or no_generators in coverage.json if you cite it.")
    L.append("")
    return "\n".join(L)


def data_center_plant_items(data):
    """{plant_id: [(None, item)]}: a check task for each in_gem site's GEM plant, in the
    shape load_validation returns (whole-plant, checklist row 39)."""
    out = {}
    for x in data["sites"]:
        if x.get("verdict") != "in_gem" or not x.get("gem_plant_id"):
            continue
        task = (f"A permit harvest lists this plant's data center ({x.get('name') or x['site_id']}). "
                "Compare the fleet size, the phases, the Backup Power box and the engine counts "
                "with the newest permit and report each value that differs, with the permit link. "
                f"Facts: {_dc_facts(x)}")
        out.setdefault(x["gem_plant_id"], []).append((None, {
            "task": task, "kind": "fix", "section": "Data centers", "unit_id": None,
            "fields": ["Capacity (MW)", "Status", "Number Of Engines", "Capacity Per Engine",
                       "Backup Power", "Captive industry use", "Captive industry type",
                       "Captive non-industry use", "Status Detail"],
            "checks": [39]}))
    return out


def render_scope_brief(leads, coverage, batch_tag, threshold_mw=50):
    """briefs/_scope.md: the add rule and the scope-wide agent's two
    checklists. `leads` from eia_lead_tasks, `coverage` the
    docs/coverage/<scope>.json list (or None)."""
    L = ["# Scope-wide tasks", ""]
    L += [s.format(thr=threshold_mw) for s in ADD_RULE]
    L += ["## EIA plants missing from GEM", ""]
    if leads:
        L += ["The EIA-860M file lists these plants and no GEM plant matches them. "
              "Every one is a task. Decide each one and say why, with evidence:", ""]
        L += [f"- {d}" for d in EIA_DECISIONS]
        L += ["", "Stage an add as a record in the newplants lane. For any other answer, "
              f"write it in batches/{batch_tag}/coverage.json under `ids_followup`, keyed "
              "by EIA plant ID: `{\"decision\": \"below_threshold\", \"evidence\": "
              "\"...\", \"gem_plant_id\": \"\"}`. A plant with no answer fails the gate "
              "`ids_followup`.", ""]
        for d in leads:
            bits = [f"EIA plant {d['eia_id']}: {d['name']}",
                    f"{d['capacity_mw']} MW" if d.get("capacity_mw") not in (None, "") else "capacity not given",
                    f"status {d['status']}" if d.get("status") else "status not given"]
            extra = ", ".join(x for x in (d.get("county"), d.get("owner")) if x)
            L.append("- " + "; ".join(bits) + (f" ({extra})" if extra else "")
                     + (f". {d['staged_in']}" if d.get("staged_in") else ""))
        L.append("")
    else:
        L += ["The matcher found no EIA plant of 50 MW or more that GEM lacks.", ""]
    if coverage:
        L += ["## Statewide sources to search", "",
              f"Search every source below. For each, record an entry in batches/{batch_tag}/"
              "coverage.json under `sources`, keyed by the id: `{\"status\": \"searched\", "
              "\"how\": \"the script or pages read\", \"found\": \"what turned up, or that "
              "nothing did\"}`. A source you could not read is `blocked`, with an `access` note "
              "that says what fetch.py returned and what the Wayback lookup found. Never "
              "write \"not searched\" or \"skipped\". A search form, a script or a paged "
              "table is never a reason to stop.", ""]
        for c in coverage:
            L.append(f"- {c.get('id')}: {c.get('name')} ({c.get('url')}). {c.get('what')}")
        L.append("")
    return "\n".join(L)


def load_promotions(staging_dir):
    """Watch items the review page called "incorporate into database" or, for a lead,
    "research further", read from a batch's review log and its staged_monitor.json. Returns
    (existing, new): existing maps a GEM
    location ID to its (text, fields, checks) tasks; new lists the items with no GEM plant
    (new to the tracker) as dicts for _index.json."""
    d = Path(staging_dir)
    log, mon = d / "review_log.jsonl", d / "staged_monitor.json"
    if not log.exists():
        sys.exit(f"ERROR: {log} not found; nothing has been reviewed in that folder")
    if not mon.exists():
        sys.exit(f"ERROR: {mon} not found; that folder has no watch items")
    calls = {}
    for line in log.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if rec.get("flag"):
            continue
        rid = rec.get("record_id") or rec.get("key", "").split("::", 1)[-1]
        if rid:
            calls[rid] = rec           # the log is append-only; the last record per item speaks
    existing, new = {}, []
    for r in json.loads(mon.read_text(encoding="utf-8")).get("records", []):
        c = calls.get(r.get("record_id", ""))
        if not c or c.get("call") not in ("add_to_database", "research_further"):
            continue
        reason = (r.get("monitor_reason") or r.get("item") or "").strip()
        who, when = c.get("reviewer") or "the reviewer", str(c.get("ts") or "")[:10]
        links = list((r.get("refs") or {}).get("links") or [])
        said = ("said this lead needs more research before it can be added"
                if c.get("call") == "research_further" else "said this watch item belongs in the database now")
        parts = [f"The review on {when} by {who} {said}" + (f": {reason}" if reason else ".")]
        if c.get("note"):
            parts.append(f"Reviewer's note: {c['note']}")
        if c.get("reference"):
            parts.append(f"Source the reviewer gave: {c['reference']}")
            links.append(c["reference"])
        if links:
            parts.append("Sources already on the item: " + ", ".join(dict.fromkeys(links)) + ".")
        checks = [int(x) for x in r.get("checks") or []] or [51]
        pid = (r.get("gem_plant_id") or "").strip()
        if pid:
            text = " ".join(parts) + (" Research it and stage the full edit: a new unit row, or the "
                                      "cell changes on the units it concerns, with sources.")
            existing.setdefault(pid, []).append((text, list(RESEARCH_FIELDS), checks))
        else:
            new.append({"record_id": r.get("record_id"), "plant_name": r.get("plant_name") or "",
                        "country": r.get("country") or "", "reason": reason, "reviewer": who,
                        "reviewed_on": when, "note": c.get("note") or "", "links": list(dict.fromkeys(links)),
                        "checks": checks, "staging_dir": str(d),
                        "next_step": "write the full new-plant record (discovery lane) with sources"})
    return existing, new


def location_task_text(e):
    """The location step's task with the links the agent needs: GEM's point in
    satellite view and as a pin, and every dataset point the same way."""
    loc = e.get("location") or {}
    cur = loc.get("current") or {}
    parts = [e["task"]]
    links = geo.links_for(cur.get("lat"), cur.get("lon"))
    if links:
        parts.append(f"GEM's point in satellite view: {links['satellite']} (pin: {links['pin']}).")
    for p in loc.get("dataset_points") or []:
        pl = geo.links_for(p.get("lat"), p.get("lon"))
        if pl:
            parts.append(f"The {p.get('source')} point in satellite view: {pl['satellite']}.")
    parts.append("Follow the location ladder in the sweep instructions and report the "
                 "method, the distance moved and whether a second look is needed.")
    return " ".join(parts)


OPTIONAL_VALIDATION = ("Optional under the manual; answer it if cheap. The plant has coal "
                       "units or this unit is a coal-to-gas conversion, and the manual does "
                       "not require a fix for those errors. ")


def is_coal_conversion(r):
    """A unit converted from coal to gas (the converted-from fuel says coal)."""
    return ws(r.get("Conversion from/replacement of (fuel)")).lower().startswith("coal")


def coal_plant_ids(path):
    """Location IDs of plants that have a coal unit in the unfiltered export at
    `path` (any unit row whose Fuel contains coal); empty when the file is missing."""
    p = Path(path)
    if not p.exists():
        return set()
    with open(p, encoding="utf-8-sig", newline="") as f:
        return {r.get(H_LOC, "").strip() for r in csv.DictReader(f)
                if "coal" in (r.get("Fuel") or "").lower() and r.get(H_LOC)}


def validation_tasks(items, rows, coal_plant=False):
    """Split a plant's validation fixes into unit tasks and whole-plant tasks.
    A missing data source the gap list already asks about is not repeated.
    With `coal_plant` (the plant has coal units in the unfiltered export) or on
    a coal-to-gas conversion unit, a validation report item (row 7) is marked
    optional (manual lines 198 and 220)."""
    by_uid = {r[H_UNIT]: r for r in rows}
    per_unit, plant = {}, []
    for uid, e in items:
        r = by_uid.get(uid)
        if 7 in (e.get("checks") or []) and (coal_plant or (r is not None and is_coal_conversion(r))):
            e = dict(e, task=OPTIONAL_VALIDATION + e["task"])
        if r is None:
            who = f"Unit {e.get('unit_name') or uid} ({uid}): " if uid else ""
            plant.append((who + e["task"], list(e.get("fields") or []),
                          list(e.get("checks") or [])))
            continue
        if (e["section"] == "Data Sources" and e.get("fields")
                and set(e["fields"]) <= {h for h, _ in empty_source_values(r)}):
            continue
        per_unit.setdefault(uid, []).append((e["task"], list(e.get("fields") or []),
                                             list(e.get("checks") or [])))
    return per_unit, plant


VALIDATION_MARK = "**[Validation report]**"


def task_line(text, checks):
    """A brief task bullet; a validation report task (row 7) is marked so the
    research agent answers it even when nothing is found."""
    return f"{VALIDATION_MARK} {text}" if 7 in (checks or []) else text


def load_harvest(folder):
    """The pre-sweep harvest of one scope (psc_dockets.json from harvest_psc_mississippi.py and
    queues.json from pull_queues_mississippi.py, both in `folder`) as
    ({plant_id: [(None, item)]}, data). Each item is a whole-plant task that lists the dockets
    and queue entries matched to the plant; the unmatched ones go to briefs/_harvest.md."""
    folder = Path(folder)
    psc_p, q_p = folder / "psc_dockets.json", folder / "queues.json"
    if not psc_p.exists() and not q_p.exists():
        sys.exit(f"ERROR: neither psc_dockets.json nor queues.json is in {folder}; run "
                 "harvest_psc_mississippi.py and pull_queues_mississippi.py first")
    psc = json.loads(psc_p.read_text(encoding="utf-8")) if psc_p.exists() else {}
    queues = json.loads(q_p.read_text(encoding="utf-8")) if q_p.exists() else {}
    lines = {}
    for d in psc.get("dockets") or []:
        facts = d.get("facts") or {}
        bits = [f"PSC docket {d['docket']} ({d.get('utility') or 'applicant not shown'}, filed "
                f"{d.get('filed') or 'date not shown'}): {(d.get('title') or '')[:200]}"]
        for key, label in (("megawatts", "megawatts"), ("in_service", "in service"),
                           ("retirement", "retirements")):
            if facts.get(key):
                bits.append(f"{label}: {facts[key][0][:160]}")
        for m in d.get("matched") or []:
            lines.setdefault(m["plant_id"], []).append(". ".join(bits) + f". Match: {m['how']}.")
    for e in queues.get("entries") or []:
        for m in e.get("matched") or []:
            bits = [f"{e['source']} queue entry {e['queue_id']}", e.get("fuel") or e.get("facility_type"),
                    f"{e['mw']} MW" if e.get("mw") else "", e.get("status"),
                    f"queued {e['queue_date']}" if e.get("queue_date") else "",
                    f"in service {e['in_service']}" if e.get("in_service") else "",
                    f"point of interconnection {e['poi']}" if e.get("poi") else ""]
            lines.setdefault(m["plant_id"], []).append(
                "; ".join(b for b in bits if b) + f". A queue entry is a lead, not proof. Cite the queue page: {e['url']}")
    out = {}
    for pid, ls in lines.items():
        for text in ls:
            out.setdefault(pid, []).append((None, {
                "kind": "fix", "section": "Harvest", "fields": [], "checks": [],
                "task": "Pre-sweep harvest found this for the plant, read the source and use it when it "
                        "is evidence for a value: " + text}))
    return out, {"psc": psc, "queues": queues}


def render_harvest_brief(data):
    """briefs/_harvest.md: harvest items with no GEM plant, for the scope-wide agent."""
    psc, queues = data["psc"], data["queues"]
    by_id = {d["docket"]: d for d in psc.get("dockets") or []}
    L = ["# Pre-sweep harvest: items that match no GEM plant", "",
         "These are leads for new plants, uprates or retirements. A queue entry or a docket title is "
         "not proof. Read the source, then stage a new plant, a monitor item or nothing, and say which.", ""]
    L += ["## Public Service Commission dockets", ""]
    un = [by_id[k] for k in psc.get("unmatched_generation") or [] if k in by_id]
    if un:
        for d in un:
            L.append(f"- Docket {d['docket']}, {d.get('utility') or 'applicant not shown'}, filed "
                     f"{d.get('filed') or 'date not shown'}: {(d.get('title') or '')[:300]}")
    else:
        L.append("No unmatched generation dockets.")
    L += ["", "## Interconnection queue entries, gas and oil", ""]
    ent = {e["queue_id"]: e for e in queues.get("entries") or []}
    ids = list(queues.get("unmatched_gas_oil") or []) + list(queues.get("hidden_fuel_leads") or [])
    if ids:
        for qid in ids:
            e = ent.get(qid)
            if e:
                L.append(f"- {e['source']} {qid}: {e.get('project_name') or 'no project name'}; "
                         f"{e.get('fuel') or e.get('facility_type') or 'fuel not shown'}; "
                         f"{e['mw'] or 'size not shown'} MW; {e.get('status')}; {e.get('county') or 'county not shown'}; "
                         f"point of interconnection {e.get('poi') or 'not shown'}; {e.get('owner') or ''}. "
                         f"Citation page: {e['url']}")
    else:
        L.append("No unmatched entries.")
    return "\n".join(L) + "\n"


def load_existing_links(path, scope):
    """{plant_id: [row, ...]} from check_existing_links.py's existing_links.json: the
    Data Source links already in the database that are gone, with what each backs and
    whether a saved copy already showing the value is staged."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    where = data.get("where") or {}
    if where.get("slug") and where["slug"] != scope["slug"]:
        sys.exit(f"ERROR: {path} is for {where.get('name')!r}, not {scope['name']!r}")
    out = {}
    for item in data.get("urls") or []:
        if item.get("status") != "dead":
            continue
        for u in item.get("usages") or []:
            sc = u.get("saved_copy") or {}
            out.setdefault(u["plant_id"], []).append({
                "url": item["url"], "unit": u.get("unit_name") or u.get("unit_id"),
                "unit_id": u.get("unit_id"), "ds_column": u["ds_column"],
                "value_column": u.get("value_column"), "value": u.get("value"),
                "saved_copy": sc.get("snapshot") if sc.get("ok") else "",
                "no_copy": not item.get("snapshots")})
    return out


def gone_links_block(rows):
    """The brief's short section on a plant's gone links (empty list when none)."""
    if not rows:
        return []
    L = ["## Links already in the database that are gone", "",
         "These addresses sit in the Data Source boxes and no longer open. Never delete them. "
         "Where a saved copy already shows the value, nothing is needed. Where none does, find a "
         "live source that states the same value (search the document's title or file name, or the "
         "same document posted by another publisher) and report it as a new link for that box.", ""]
    for r in rows:
        box = f"{r['ds_column']}" + (f", value {r['value_column']}: {r['value']}" if r.get("value_column") and r.get("value") else "")
        if r["saved_copy"]:
            state = "a saved copy that shows the value is already staged"
        elif r["no_copy"]:
            state = "no saved copy exists, a replacement source is needed"
        else:
            state = "the saved copy does not show the value, a replacement source is needed"
        L.append(f"- Unit {r['unit']}, {box}: {r['url']} ({state})")
    L.append("")
    return L


def render_brief(plant_id, rows, header, mode, wl, notes_text, notes_path, scope,
                 tasks=None, plant_tasks=None, gone_links=None):
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
        if any(7 in c for ts in list(tasks.values()) + [plant_tasks] for _, _, c in ts):
            L += [f"{VALIDATION_MARK} tasks come from the database's validation report. "
                  "Every one needs an answer: a finding with its source, or a question "
                  "saying what you found or that nothing was found and where you looked.", ""]
        if plant_tasks:
            L += ["### Whole plant", ""]
            L += [f"- {task_line(t, c)}" for t, _, c in plant_tasks]
            L.append("")
        for r in rows:
            uid = r.get(H_UNIT)
            ut = tasks.get(uid) or []
            L += [f"### Unit {blank(r.get(H_UNAME))} ({uid}), status "
                  f"{blank(r.get('Status'))}", ""]
            if ut:
                L += [f"- {task_line(t, c)}" for t, _, c in ut]
            else:
                L.append("- Nothing to check. Leave this unit alone unless a whole-plant "
                         "task above touches it.")
            L.append("")
        if n_tasks:
            fields = plant_fields(tasks, plant_tasks)
        else:
            # every unit retired or cancelled with nothing flagged (--scope all)
            fields = ["Status", "Status Detail"]
            L += ["Nothing was flagged for this plant. Check only that each unit's "
                  "status still holds, for example a cancelled project revived. Report "
                  "a status change only with its source.", ""]
    L += gone_links_block(gone_links)
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
    ap.add_argument("--all-csv", default=str(gem_export_csv()),
                    help="the unfiltered export, for the coal side of conversions "
                         "(skipped with a warning when absent)")
    ap.add_argument("--worklist", default=None)
    ap.add_argument("--plants", default=None, help="comma-separated GEM location IDs")
    ap.add_argument("--batch", default=None)
    ap.add_argument("--scope", default="ladder", choices=["ladder", "all"],
                    help="update mode: ladder = only plants with a task (default); "
                         "all = every plant")
    ap.add_argument("--extra-tasks", default=None,
                    help="JSON file {plant_id: [task, ...], '*': [...]} of extra tasks")
    ap.add_argument("--validation", default=None,
                    help="work/validation_<tag>.json from validation_report.py; each "
                         "fix becomes a task on its unit (update mode)")
    ap.add_argument("--ids", default=None,
                    help="work/ids_<tag>.json from match_ids.py; each task lands on its "
                         "unit and the generic EIA-id tasks are dropped (update mode)")
    ap.add_argument("--promote", action="append", default=[],
                    help="a staging dir whose review log called watch items \"incorporate into "
                         "database\"; each becomes a whole-plant task (update mode; repeatable)")
    ap.add_argument("--irp", default=None,
                    help="work/irp_us-<state-slug>.json from irp_sheet.py: the IRP research "
                         "step (update mode, US states)")
    ap.add_argument("--harvest", default=None,
                    help="batches/<tag>/harvest folder with psc_dockets.json and queues.json (from "
                         "harvest_psc_mississippi.py and pull_queues_mississippi.py): each plant's "
                         "matched dockets and queue entries become tasks, the unmatched ones go to "
                         "briefs/_harvest.md (update mode)")
    ap.add_argument("--captive", default=None,
                    help="work/captive_<tag>.json from captive_lng.py: the captive LNG sheet "
                         "step, checklist rows 6 and 44, plus the data-center search block "
                         "(row 39) for a US state (update mode, any scope)")
    ap.add_argument("--data-centers", nargs="?", const="auto", default=None,
                    help="work/permits/<tag>/_data_centers.json (or the path given): one named add "
                         "task per data center site at or near the threshold in briefs/_data_centers.md, "
                         "a check task on each matched GEM plant (update mode; a missing file is "
                         "reported and skipped)")
    ap.add_argument("--data-centers-only", action="store_true",
                    help="with --data-centers: a narrow catch-up batch that holds only the data "
                         "center sites and the GEM plants they match; the index records "
                         "focus = data_centers and the statewide gates step aside (update mode)")
    ap.add_argument("--existing-links", default=None,
                    help="batches/<tag>/existing_links.json from check_existing_links.py: puts a short "
                         "section on each plant's brief listing its Data Source links that are gone "
                         "(update mode only)")
    ap.add_argument("--location", default=None,
                    help="work/location_<tag>.json from location_candidates.py: the location "
                         "step (docs/reference/location.md), checklist row 25 and row 42 for "
                         "operating plants; replaces the generic blank-coordinate task")
    ap.add_argument("--allow-stale-export", action="store_true",
                    help="warn instead of stopping when the export is over a day old")
    a = ap.parse_args()
    extra = {}
    if a.extra_tasks:
        ep = Path(a.extra_tasks)
        if not ep.exists():
            sys.exit(f"ERROR: {ep} not found")
        extra = {k: norm_extra(v) for k, v in
                 json.loads(ep.read_text(encoding="utf-8")).items()}
    promoted_new, n_promoted = [], 0
    if a.promote and a.mode != "update":
        sys.exit("ERROR: --promote is for update mode only")
    for pd in a.promote:
        ex, new = load_promotions(pd)
        for pid, ts in ex.items():
            extra[pid] = extra.get(pid, []) + ts
            n_promoted += len(ts)
        promoted_new += new

    scope = make_scope(state=a.state, country=a.country)
    name, slug = scope["name"], scope["slug"]
    is_us = scope["country"].lower() == "united states"
    csv_path = Path(a.csv).resolve()
    if not csv_path.exists():
        sys.exit(f"ERROR: {csv_path} not found; run scope_filter.py first")
    require_fresh_export(csv_path, a.allow_stale_export)
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
    if unknown_extra and a.promote:
        # a promoted watch item on a plant outside this scope is not an error: say so and go on
        outside = {k: extra.pop(k) for k in list(unknown_extra)}
        print(f"WARNING: promoted watch items on plants not in {name}, skipped: {sorted(outside)}")
        unknown_extra = set()
    if unknown_extra:
        sys.exit(f"ERROR: --extra-tasks plants not in {name}: {sorted(unknown_extra)}")

    if (a.validation or a.ids or a.irp or a.captive or a.location or a.existing_links or a.harvest
            or a.data_centers) and a.mode != "update":
        sys.exit("ERROR: --validation, --ids, --irp, --captive, --data-centers, --location, --harvest and --existing-links "
                 "are for update mode only")
    validation = load_validation(a.validation, scope) if a.validation else {}
    ids = load_validation(a.ids, scope, producer="match_ids.py") if a.ids else {}
    irp, irp_data = {}, None
    if a.irp:
        if not is_us:
            sys.exit("ERROR: --irp is for US states (the US IRPs tab)")
        irp = load_validation(a.irp, scope, producer="irp_sheet.py")
        irp_data = json.loads(Path(a.irp).read_text(encoding="utf-8"))
    harvest, harvest_data = {}, None
    if a.harvest:
        harvest, harvest_data = load_harvest(a.harvest)
    captive, captive_data = {}, None
    if a.captive:
        captive = load_validation(a.captive, scope, producer="captive_lng.py")
        captive_data = json.loads(Path(a.captive).read_text(encoding="utf-8"))
    dc_items, dc_data = {}, None
    if a.data_centers:
        dc_path = (work_dir() / "permits" / batch_tag / "_data_centers.json"
                   if a.data_centers == "auto" else Path(a.data_centers))
        dc_data = load_data_centers(dc_path)
        if dc_data is not None:
            dc_items = data_center_plant_items(dc_data)
    loc, loc_data = {}, None
    if a.location:
        loc = load_validation(a.location, scope, producer="location_candidates.py")
        loc_data = json.loads(Path(a.location).read_text(encoding="utf-8"))
        for items in loc.values():
            for _, e in items:
                e["task"] = location_task_text(e)
    gone_links = load_existing_links(a.existing_links, scope) if a.existing_links else {}
    missing_val = sorted(set(validation) - set(plants))
    if missing_val and not a.plants:
        print(f"WARNING: validation fixes on plants not in {csv_path.name}: {missing_val}. "
              "Check their tracker assignment; they are not briefed.")
    n_val = n_ids = n_irp = n_captive = n_loc = n_harv = n_dc = 0
    missing_loc = sorted(set(loc) - set(plants))
    if missing_loc and not a.plants:
        print(f"WARNING: location tasks on plants not in {csv_path.name}: {missing_loc}; not briefed.")
    missing_irp = sorted(set(irp) - set(plants))
    if missing_irp and not a.plants:
        print(f"WARNING: IRP tasks on plants not in {csv_path.name}: {missing_irp}; not briefed.")
    missing_cap = sorted(set(captive) - set(plants))
    if missing_cap and not a.plants:
        print(f"WARNING: captive LNG tasks on plants not in {csv_path.name}: {missing_cap}; not briefed.")

    coal_ids = coal_plant_ids(a.all_csv) if a.validation else set()
    peers = {}
    all_path = Path(a.all_csv)
    if a.mode == "update" and all_path.exists():
        with open(all_path, encoding="utf-8-sig", newline="") as f:
            peers = {r[H_UNIT].strip(): r for r in csv.DictReader(f) if r.get(H_UNIT)}
    elif a.mode == "update":
        print(f"WARNING: {all_path} not found; conversion start years are not checked "
              "against the coal unit's retired year.")

    # Tasks per unit and per plant; ladder scope keeps only tasked plants.
    tasks, plant_tasks, not_tasked = {}, {}, []
    for pid, rows in plants.items():
        tasks[pid] = ({r[H_UNIT]: unit_tasks(r, us=is_us and not a.ids, peers=peers,
                                             status_pass=a.scope == "all",
                                             location=bool(a.location))
                       for r in rows}
                      if a.mode == "update" else {})
        val_unit, val_plant = validation_tasks(validation.get(pid, []), rows,
                                               coal_plant=pid in coal_ids)
        for uid, vt in val_unit.items():
            tasks[pid][uid] = tasks[pid].get(uid, []) + vt
        n_val += sum(len(v) for v in val_unit.values()) + len(val_plant)
        id_unit, id_plant = validation_tasks(ids.get(pid, []), rows)
        for uid, it in id_unit.items():
            tasks[pid][uid] = tasks[pid].get(uid, []) + it
        n_ids += sum(len(v) for v in id_unit.values()) + len(id_plant)
        # IRP tasks are whole-plant by construction (unit_id is null in the file)
        irp_unit, irp_plant = validation_tasks(irp.get(pid, []), rows)
        for uid, it in irp_unit.items():
            tasks[pid][uid] = tasks[pid].get(uid, []) + it
        n_irp += sum(len(v) for v in irp_unit.values()) + len(irp_plant)
        # captive LNG sheet tasks are whole-plant too (unit_id null in the file)
        cap_unit, cap_plant = validation_tasks(captive.get(pid, []), rows)
        # data center sites: the matched GEM plant gets its check task (unit_id null in the file)
        dc_unit, dc_plant = validation_tasks(dc_items.get(pid, []), rows)
        for uid, it in dc_unit.items():
            tasks[pid][uid] = tasks[pid].get(uid, []) + it
        n_dc += sum(len(v) for v in dc_unit.values()) + len(dc_plant)
        cap_plant = cap_plant + dc_plant
        for uid, it in cap_unit.items():
            tasks[pid][uid] = tasks[pid].get(uid, []) + it
        n_captive += sum(len(v) for v in cap_unit.values()) + len(cap_plant)
        # pre-sweep harvest tasks (PSC dockets, queue entries) are whole-plant
        harv_unit, harv_plant = validation_tasks(harvest.get(pid, []), rows)
        n_harv += len(harv_plant)
        # location step tasks are whole-plant (unit_id null in the file)
        loc_unit, loc_plant = validation_tasks(loc.get(pid, []), rows)
        for uid, it in loc_unit.items():
            tasks[pid][uid] = tasks[pid].get(uid, []) + it
        n_loc += sum(len(v) for v in loc_unit.values()) + len(loc_plant)
        own = extra.get(pid, []) + val_plant + id_plant + irp_plant + cap_plant + loc_plant + harv_plant
        plant_tasks[pid] = own + extra.get("*", [])
        # a gone Data Source link already in the database is work too (its saved copy or replacement)
        has_task = any(tasks[pid].values()) or bool(own) or bool(gone_links.get(pid))
        if a.mode == "update" and a.scope == "ladder" and not has_task:
            not_tasked.append({"plant_id": pid, "plant_name": rows[0].get(H_PLANT, "").strip(),
                               "unit_ids": [r[H_UNIT] for r in rows]})
    if not_tasked:
        plants = {k: v for k, v in plants.items()
                  if k not in {p["plant_id"] for p in not_tasked}}
    if a.data_centers_only:
        if dc_data is None or a.mode != "update":
            sys.exit("ERROR: --data-centers-only needs --data-centers with a harvest file, in update mode")
        keep = {x.get("gem_plant_id") for x in dc_data["sites"] if x.get("gem_plant_id")}
        dropped = [pid for pid in plants if pid not in keep]
        plants = {k: v for k, v in plants.items() if k in keep}
        not_tasked = [p for p in not_tasked if p["plant_id"] in keep]
        print(f"narrow batch (data centers only): {len(plants)} matched GEM plants kept, {len(dropped)} others left out")
    dc_only = bool(dc_data) and any(x.get("verdict") in DC_ANSWER_VERDICTS for x in dc_data["sites"])
    if not plants and not dc_only:
        sys.exit(f"ERROR: no plant in {name} has a task; use --scope all")
    if not plants:
        print(f"NOTE: no plant in {name} has a task; the batch holds the data center sites only")

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
                            tasks=tasks.get(pid), plant_tasks=plant_tasks.get(pid),
                            gone_links=gone_links.get(pid))
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
            # the tasks themselves, so assemble_state.py can copy each task's
            # checklist rows onto the records its findings produce
            "tasks": {uid: task_dicts(ut) for uid, ut in tasks.get(pid, {}).items() if ut},
            "plant_tasks": task_dicts(plant_tasks.get(pid, [])),
        })
        n_units += len(rows)
    index.sort(key=lambda p: (p["max_priority"] is None, p["max_priority"] or 0, p["plant_name"].lower()))
    irp_index = None
    if irp_data is not None:
        irp_brief = batch / "briefs" / "_irp.md"
        irp_brief.write_text(irp_data.get("brief") or "", encoding="utf-8")
        try:
            irp_rel = str(irp_brief.relative_to(REPO_ROOT))
        except ValueError:
            irp_rel = str(irp_brief)
        links = []
        for u in irp_data.get("utilities") or []:
            links += [x for x in (u.get("links") or []) if x not in links]
        irp_index = {"file": str(Path(a.irp).resolve()), "brief_path": irp_rel,
                     "read": irp_data.get("read"), "skipped": bool(irp_data.get("skipped")),
                     "utilities": [{"utility": u.get("utility"), "irp_year": u.get("irp_year"),
                                    "is_draft": bool(u.get("is_draft")), "links": u.get("links") or [],
                                    "next_irp_due": u.get("next_irp_due"),
                                    "plant_ids": [p["plant_id"] for p in u.get("plants") or []]}
                                   for u in irp_data.get("utilities") or []],
                     "links": links,
                     "irp_box_units": [u["unit_id"] for u in irp_data.get("irp_units") or []]}
    harvest_index = None
    if harvest_data is not None:
        hv_brief = batch / "briefs" / "_harvest.md"
        hv_brief.write_text(render_harvest_brief(harvest_data), encoding="utf-8")
        harvest_index = {"folder": str(Path(a.harvest).resolve()), "plant_tasks": n_harv,
                         "unmatched_dockets": list(harvest_data["psc"].get("unmatched_generation") or []),
                         "unmatched_queue_entries": list(harvest_data["queues"].get("unmatched_gas_oil") or [])}
    captive_index = None
    if captive_data is not None:
        cap_brief = batch / "briefs" / "_captive.md"
        cap_brief.write_text(captive_data.get("brief") or "", encoding="utf-8")
        try:
            cap_rel = str(cap_brief.relative_to(REPO_ROOT))
        except ValueError:
            cap_rel = str(cap_brief)
        terms = captive_data.get("terminals") or []
        captive_index = {
            "file": str(Path(a.captive).resolve()), "brief_path": cap_rel,
            "read": captive_data.get("read"), "threshold_mw": captive_data.get("threshold_mw"),
            "terminals": [{"terminal": t.get("terminal"), "terminal_id": t.get("terminal_id"),
                           "qualifying": bool(t.get("qualifying")),
                           "mechanical_only": bool(t.get("mechanical_only")),
                           "plant_ids": [m["plant_id"] for m in t.get("matches") or []]}
                          for t in terms],
            "new_candidates": [t.get("terminal_id") for t in terms
                               if t.get("qualifying") and not t.get("matches")],
            "gem_only": [p.get("plant_id") for p in captive_data.get("gem_only") or []],
            # the row 39 block (US states): the data center search; adds go through briefs/_data_centers.md
            "data_center": captive_data.get("data_center") is not None}
    cov_list = REPO_ROOT / "docs" / "coverage" / f"{batch_tag}.json"
    coverage = json.loads(cov_list.read_text(encoding="utf-8")) if cov_list.exists() else None
    eia_leads = eia_lead_tasks(a.ids)
    # every scope: the add rule, then the EIA leads and the statewide source list when there are any
    scope_brief = batch / "briefs" / "_scope.md"
    thr = (CAPACITY_THRESHOLD_EU_UK_MW if scope["country"] in EU_UK_COUNTRIES
           else CAPACITY_THRESHOLD_MW)
    scope_brief.write_text(render_scope_brief(eia_leads, coverage, batch_tag, threshold_mw=thr),
                           encoding="utf-8")
    dc_index = None
    if dc_data is not None:
        dc_brief = batch / "briefs" / "_data_centers.md"
        dc_brief.write_text(render_data_centers_brief(dc_data, thr), encoding="utf-8")
        dc_index = {"file": str(Path(dc_data["_path"]).resolve()),
                    "brief_path": str(dc_brief.relative_to(REPO_ROOT)) if REPO_ROOT in dc_brief.parents else str(dc_brief),
                    "threshold_mw": dc_data.get("threshold_mw") or thr,
                    "answer_sites": [x["site_id"] for x in dc_data["sites"] if x.get("verdict") in DC_ANSWER_VERDICTS],
                    "plant_tasks": n_dc}
    location_index = None
    if loc_data is not None:
        location_index = {"file": str(Path(a.location).resolve()), "read": loc_data.get("read"),
                          "sources": loc_data.get("sources"),
                          "plants_checked": loc_data.get("plants_checked"),
                          "candidates": sorted({t.get("plant_id")
                                                for t in loc_data.get("tasks") or []})}
    idx_path = batch / "briefs" / "_index.json"
    # `state` / `postal` stay for US batches (older readers key on them); `where`
    # is the generic scope every reader should prefer.
    idx_path.write_text(json.dumps({
        "state": name if scope["kind"] == "state" else "",
        "postal": scope["postal"], "where": scope,
        "mode": a.mode, "csv": str(csv_path),
        "scope": "all" if a.mode == "blind" else a.scope,
        # a narrow catch-up batch for one checklist step; state_gate's statewide gates step aside
        "focus": "data_centers" if a.data_centers_only else None,
        "generated": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "plants": index, "not_tasked": not_tasked,
        # watch items called "incorporate into database" that have no GEM plant yet: the
        # discovery lane writes their full new-plant records; no brief can carry them
        "promoted_new": promoted_new,
        # the IRP step (irp_sheet.py): the statewide agent reads briefs/_irp.md; the
        # assembler marks records whose source is one of these plan links
        "irp": irp_index,
        # the captive LNG sheet step (captive_lng.py): the scope-wide agent reads
        # briefs/_captive.md; matched plants carry their task on their own brief
        "captive": captive_index,
        "harvest": harvest_index,
        # data center sites (data_center_fleets.py): briefs/_data_centers.md; the gate
        # `data-centers` wants a coverage.json `data_centers` answer for each answer_sites id
        "data_centers": dc_index,
        # the location step (location_candidates.py): the plants whose coordinates
        # the sweep follows the ladder for; state_gate gate `location` checks the result
        "location": location_index,
        # EIA plants missing from GEM (match_ids.py leads): one named task each in
        # briefs/_scope.md; state_gate gate `ids_followup` checks every one is answered
        "ids_followup": ([{k: d[k] for k in ("eia_id", "name", "capacity_mw", "status")}
                          for d in eia_leads] if a.ids else None),
        "coverage_list": (str(cov_list.relative_to(REPO_ROOT)) if coverage else None),
        "coverage_ids": [c.get("id") for c in coverage or []]}, indent=2, ensure_ascii=False),
        encoding="utf-8")

    tag = f" ({scope['postal'].upper()})" if scope["postal"] else ""
    print(f"{scope['kind']}: {name}{tag}  mode: {a.mode}  scope: {a.scope}")
    print(f"plants: {len(index)}  units: {n_units}  tasks: "
          f"{sum(p['n_tasks'] for p in index)}  not tasked (left out): {len(not_tasked)}  "
          f"worklist: {'yes (' + str(wl_path) + ')' if wl is not None else 'none'}")
    if a.validation:
        print(f"validation report tasks added: {n_val}")
    if a.ids:
        print(f"ID match tasks added: {n_ids}; EIA plants missing from GEM: {len(eia_leads)}")
    if scope_brief is not None:
        print(f"scope-wide block: {scope_brief}")
    if irp_index is not None:
        if irp_index["skipped"]:
            print("IRP step: the US IRPs tab has no rows for this state; briefs/_irp.md says so")
        else:
            print(f"IRP step: {len(irp_index['utilities'])} utility plan(s), {n_irp} plant task(s), "
                  f"{len(irp_index['irp_box_units'])} unit(s) already carry the IRP box; "
                  f"statewide block: {irp_index['brief_path']}")
    if harvest_index is not None:
        print(f"harvest step: {n_harv} plant task(s), {len(harvest_index['unmatched_dockets'])} unmatched "
              f"docket(s), {len(harvest_index['unmatched_queue_entries'])} unmatched queue entr(ies); "
              f"scope-wide block: briefs/_harvest.md")
    if captive_index is not None:
        nq = sum(1 for t in captive_index["terminals"] if t["qualifying"])
        print(f"captive LNG step: {len(captive_index['terminals'])} sheet row(s) in scope ({nq} qualifying), "
              f"{n_captive} plant task(s), {len(captive_index['new_candidates'])} qualifying terminal(s) GEM "
              f"lacks, {len(captive_index['gem_only'])} GEM LNG plant(s) with no sheet row"
              f"{'; data-center block (row 39) included' if captive_index['data_center'] else ''}; "
              f"scope-wide block: {captive_index['brief_path']}")
    if a.data_centers and dc_index is None:
        print("data center step: no _data_centers.json found; nothing added. Run "
              "data_center_fleets.py for this scope first.")
    elif dc_index is not None:
        print(f"data center step: {len(dc_index['answer_sites'])} site(s) need an answer, "
              f"{n_dc} plant check task(s); scope-wide block: {dc_index['brief_path']}")
    if location_index is not None:
        print(f"location step: {location_index['plants_checked']} plant(s) checked, "
              f"{len(location_index['candidates'])} candidate(s), {n_loc} plant task(s)")
    if a.promote:
        print(f"promoted watch items: {n_promoted} task(s) on tracked plants; "
              f"{len(promoted_new)} new to the tracker (listed under promoted_new in the index)")
        for p in promoted_new:
            print(f"  new to the tracker: {p['plant_name']} ({p['record_id']}): {p['reason'] or 'no reason recorded'}")
    print(f"batch dir: {batch}")
    print(f"index: {idx_path}")


if __name__ == "__main__":
    main()

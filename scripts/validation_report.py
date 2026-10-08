#!/usr/bin/env python3
"""
Read the GEM database's validation errors for one scope (a US state or a
country) and sort them for the research process. This is QC/Country checklist
rows 7 ("checked and fixed all errors from the validation report", during the
update) and 54 (the same, at the end of the update).

Usage (from scripts/):
    python validation_report.py --state "New York"
    python validation_report.py --country Germany
    python validation_report.py --state "New York" --closeout   # exit 1 if anything blocks

Source: `plant.validation` in the read-only GEM database, the per-project
"Validation Errors" that the web UI's GOGPT Validation Report lists. The site
writes it when a plant is saved, and every run here reads it live. Checked
2026-10-06: every status step without a date in the live status tables was
flagged, and nothing flagged had already been fixed.
Scope: combustion plants in the country (and state) whose fuels include fossil
gas or fossil liquids, the same as the web UI search with those two fuel
categories. Deleted plants are skipped.

Every error is sorted into one of three kinds:
  fix        research can clear it: a value with no data source, a required
             value that is blank, a status step with no date, a replacement
             link to a unit that does not exist, a fuel or owner share problem,
             a unit named "--" on a plant with several units.
  exception  the manual's optional, low-priority cases: an error on a unit with
             no oil or gas fuel (the coal side of a shared plant, or a coal
             phase before a conversion), or a plant-level data source on a
             plant that also has coal units.
  person     needs a click in the web UI, not research: plant-name rules, and
             hydrogen data sources (hydrogen columns are never researched here).
Only exceptions may be left at close-out (QC SOP §6); `--closeout` exits 1
when any fix or person item remains.

Writes:
  work/validation_<tag>.json   every error: kind, plant and unit IDs (L.../G...
                               as in the export), section, message, and for a
                               fix the brief task text and the export columns
                               it touches
  work/validation_<tag>.md     plain-language list for the person, by plant
<tag> is us-<state-slug> or <country-slug>, as worklist.py names it.
`build_state_brief.py --validation work/validation_<tag>.json` turns each fix
into a task on its unit's brief.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from paths import db_ops_repo, work_dir
from build_state_brief import make_scope

FOSSIL_GAS, FOSSIL_LIQUIDS, COAL = 3, 4, 2
CAPTIVE = ["Captive industry use", "Captive industry type", "Captive non-industry use"]
LOCATION = ["Latitude", "Longitude", "Location accuracy"]

# Data Sources error label (after 'Unit "<name>" - ') -> export value columns.
SOURCE_LABELS = {
    "Capacity": ["Capacity (MW)"],
    "Technology": ["Turbine/Engine Technology"],
    "Fuel": ["Fuel"],
    "CHP": ["CHP"],
    "CCS": ["CCS attachment?"],
    "Location": LOCATION,
    "Disrupted due to conflict": ["Disrupted by conflict"],
    "Backup Power": ["Backup Power"],
    "Latest Activity": ["Latest Activity"],
    "Employment Notes": ["Employment Notes"],
    "Captive": CAPTIVE,
    "Status": ["Status"],
}
REQUIRED_LABELS = {"Capacity": ["Capacity (MW)"], "Latitude": ["Latitude"],
                   "Longitude": ["Longitude"]}
# The year column that holds the date of a status step, when the step is current.
STEP_YEAR = {"operating": "Start year", "retired": "Retired year",
             "cancelled": "Cancellation year"}
LABEL_NAMES = {"CCS": "Carbon capture (CCS)", "CHP": "Combined heat and power (CHP)"}


def engine():
    sys.path.insert(0, str(db_ops_repo()))
    from gem_query import get_database_url, build_engine, DEFAULT_STATEMENT_TIMEOUT_MS
    return build_engine(get_database_url(), DEFAULT_STATEMENT_TIMEOUT_MS)


def fetch(scope):
    from sqlalchemy import text
    where = ['not coalesce(p.deleted, false)', 'p."projectType" = 1',
             'p."fuelCategorySearch" && array[3, 4]::bigint[]',
             'c."gemName" ilike :country']
    params = {"country": scope["country"]}
    if scope["kind"] == "state":
        where.append("p.subnational ilike :state")
        params["state"] = scope["name"]
    with engine().connect() as cx:
        plants = cx.execute(text(f"""
            select p.id, p.name, p."fuelCategorySearch", p.validation
            from plant p join country c on c.id = any(p."countrySearch")
            where {' and '.join(where)} order by p.name"""), params).fetchall()
        ids = [p[0] for p in plants]
        units = cx.execute(text("""
            select u.id, u.name, u.plant_id, u."fuelCategorySearch", u.status_id
            from powerplant_unit u where u.plant_id = any(:ids)
              and not coalesce(u.deleted, false)"""), {"ids": ids}).fetchall()
        uids = [u[0] for u in units]
        steps = cx.execute(text("""
            select unit_id, status, substatus, "eventYear", "makeCurrent"
            from milestone_timeline where unit_id = any(:uids)
            order by unit_id, "order", id"""), {"uids": uids}).fetchall()
        repl = cx.execute(text("""
            select unit_id, "unitReplacementId" from unit_replacement
            where unit_id = any(:uids) order by id"""), {"uids": uids}).fetchall()
    # Current status: the step marked current, else the last step by order
    # (gem-db-ops docs/ALL_FIELDS_STATUS.md, "GOGPT: status timelines").
    undated, current, marked = defaultdict(list), {}, set()
    for uid, status, sub, year, make_current in steps:
        if year is None:
            undated[uid].append(f"{status} - {sub}" if sub else status)
        if make_current:
            current[uid] = status
            marked.add(uid)
        elif uid not in marked:
            current[uid] = status
    replaced = defaultdict(list)
    for uid, rid in repl:
        replaced[uid].append(rid)
    return plants, {u[0]: u for u in units}, undated, replaced, current


def label_of(key):
    """'Unit "GT 1" - Capacity' -> 'Capacity'; plant-level keys pass through."""
    m = re.match(r'^Unit ".*" - (.+)$', key)
    return m.group(1) if m else key


def unit_name_of(key):
    m = re.match(r'^Unit "(.*)"(?: - .+)?$', key)
    return m.group(1) if m else ""


def classify(sec, key, warning, unit, plant_fuels, undated, replaced, current):
    """(kind, task text or None, export columns). Plain language: the task text
    lands in the brief a research agent reads and in the person's list."""
    label = label_of(key)
    base = re.sub(r"\s+\d+$", "", label)            # 'Owner 2' -> 'Owner'
    gas_or_oil = {FOSSIL_GAS, FOSSIL_LIQUIDS}
    if unit is not None and not (set(unit[3] or []) & gas_or_oil):
        return "exception", None, []
    if unit is None and sec == "Data Sources" and COAL in (plant_fuels or []):
        return "exception", None, []
    if base == "Hydrogen":
        return "person", None, []
    if sec == "Project Name":
        return "person", None, []

    if sec == "Data Sources":
        cols = SOURCE_LABELS.get(base) or {"Owner": ["Owner(s)"],
                                           "Operator": ["Operator(s)"]}.get(base, [])
        what = LABEL_NAMES.get(base, base)
        if cols:
            return "fix", (
                f"The database's validation report says {what} has no data source. "
                "Find a document that states the current value for this "
                f"{'unit' if unit is not None else 'plant'} and report the value "
                "with that document. If the document gives a different value, say so."
            ), cols
    if sec == "Required" and base in REQUIRED_LABELS:
        return "fix", (f"The database's validation report says {base} is required "
                       "but blank. Find it."), REQUIRED_LABELS[base]
    if sec == "Milestone Timeline" and warning == "Please supply a date" and unit is not None:
        out = []
        cols = []
        cur = (current.get(unit[0]) or "").lower()
        for step in undated.get(unit[0]) or ["(the database did not say which)"]:
            col = STEP_YEAR.get(step) if step == cur else None
            art = "an" if step[0] in "aeiou" else "a"
            if col:
                cols.append(col)
                out.append(f"The unit's status history has {art} \"{step}\" step with no "
                           f"date. Find the year it reached that step and report it "
                           f"as {col}, with the document that says so.")
            else:
                out.append(f"The unit's status history has {art} \"{step}\" step with no "
                           "date. Find the year, and the month if a document gives it, "
                           "when the unit reached that step. Give it as a question, "
                           "not a value, with the document that says so.")
        return "fix", " ".join(out), cols
    if sec == "Milestone Timeline":
        return "fix", ("The database's validation report says of the status history: "
                       f"\"{warning}\" Check the status steps and their dates against a "
                       "source, and say in a question what should change."), ["Status"]
    if sec == "Unit Replacement" and unit is not None:
        bad = ", ".join(str(r) for r in replaced.get(unit[0], [])) or "unknown"
        return "fix", ("This unit is recorded as replacing another unit, but the link "
                       f"points at a unit that does not exist (ID {bad}). Find which "
                       "unit it replaced, often an older unit at the same plant, which "
                       "may be a coal unit. Give that unit's GEM unit ID as a question, "
                       "not a value. If it replaced nothing, say so."), []
    if sec == "Unit name":
        return "fix", ("The unit is named \"--\" but the plant has more than one unit. "
                       "Say in a question what the sources call this unit; do not "
                       "report it as a value."), []
    if sec == "Fuels":
        return "fix", (f"The database's validation report says: \"{warning.strip()}\" "
                       "Check the fuels and their shares against a source."), ["Fuel"]
    if sec == "Owners":
        return "fix", (f"The database's validation report says: \"{warning.strip()}\" "
                       "Check the owners and their shares against a source."), ["Owner(s)"]
    return "fix", (f"The database's validation report says: {key}: \"{warning}\" "
                   "Check it and say in a question what should change."), []


def build(scope):
    plants, units, undated, replaced, current = fetch(scope)
    errors = []
    for pid, pname, pfuels, val in plants:
        for sec, items in (val or {}).items():
            if not isinstance(items, dict):
                items = {sec: items}
            for key, w in items.items():
                if isinstance(w, dict):
                    warning = str(w.get("warning", ""))
                    uid = w.get("unit_id")
                else:
                    warning, uid = str(w), None
                uid = int(uid) if uid not in (None, "") else None
                unit = units.get(uid) if uid else None
                kind, task, cols = classify(sec, key, warning, unit, pfuels,
                                            undated, replaced, current)
                errors.append({
                    "plant_id": f"L{pid}", "plant_name": pname,
                    "unit_id": f"G{uid}" if uid else None,
                    "unit_name": unit[1] if unit else unit_name_of(key) or None,
                    "unit_has_gas_or_oil": (bool(set(unit[3] or []) & {3, 4})
                                            if unit else None),
                    "section": sec, "item": key, "message": warning,
                    "kind": kind, "task": task, "fields": cols,
                })
    return plants, errors


def describe(e):
    """One plain sentence for the person's list."""
    label, sec, msg = label_of(e["item"]), e["section"], e["message"].strip()
    what = LABEL_NAMES.get(re.sub(r"\s+\d+$", "", label), label)
    if sec == "Data Sources":
        return f"{what} has no data source."
    if sec == "Required":
        return f"{what} is required but blank."
    if sec == "Unit Replacement" and msg == "Unit ID does not exist":
        return "The replacement link points at a unit that does not exist."
    if sec == "Milestone Timeline" and msg == "Please supply a date":
        return "A step in the status history has no date."
    return f"{sec}: {msg.rstrip('.')}."


def why_exception(e):
    if e["unit_id"]:
        return ("Optional: this unit burns no oil or gas. It is the coal side of the "
                "plant or a coal phase before a conversion.")
    return "Optional: a plant-wide data source on a plant that also has coal units."


def memo(scope, plants, errors, stamp):
    kinds = Counter(e["kind"] for e in errors)
    flagged = {e["plant_id"] for e in errors}
    L = [f"# Validation report: {scope['name']}", "",
         f"Read from the GEM database on {stamp}. Plants whose fuels include fossil gas "
         "or fossil liquids.", "",
         f"- Plants checked: {len(plants)}",
         f"- Plants with errors: {len(flagged)}",
         f"- To fix by research: {kinds['fix']}",
         f"- To fix by hand in the web UI: {kinds['person']}",
         f"- Optional under the manual's coal exception: {kinds['exception']}", ""]
    titles = {"fix": "To fix by research",
              "person": "To fix by hand in the web UI",
              "exception": "Optional: the manual's coal exception"}
    for kind in ("fix", "person", "exception"):
        rows = [e for e in errors if e["kind"] == kind]
        if not rows:
            continue
        L += [f"## {titles[kind]}", ""]
        by_plant = defaultdict(list)
        for e in rows:
            by_plant[(e["plant_name"], e["plant_id"])].append(e)
        for (pname, pid), es in sorted(by_plant.items()):
            L += [f"### {pname} ({pid})", ""]
            for e in es:
                name = e["unit_name"] or ""
                who = ((name if name.lower().startswith("unit") else f"Unit {name}")
                       + f" ({e['unit_id']})" if e["unit_id"] else "Whole plant")
                line = f"- {who}: {describe(e)}"
                if kind == "exception":
                    line += f" {why_exception(e)}"
                L.append(line)
            L.append("")
    if not errors:
        L += ["No validation errors.", ""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    who = ap.add_mutually_exclusive_group(required=True)
    who.add_argument("--state", help="a US state, e.g. New York")
    who.add_argument("--country", help="a country (Country/Area value), e.g. Germany")
    ap.add_argument("--closeout", action="store_true",
                    help="exit 1 if any fix or person item remains")
    ap.add_argument("--out-dir", default=None, help="default: <repo>/work")
    a = ap.parse_args()

    scope = make_scope(state=a.state, country=a.country)
    tag = f"us-{scope['slug']}" if scope["kind"] == "state" else scope["slug"]
    stamp = datetime.datetime.now().astimezone().isoformat(timespec="minutes")
    plants, errors = build(scope)
    if not plants:
        sys.exit(f"ERROR: no oil or gas plants found for {scope['name']} "
                 f"(country {scope['country']!r}); check the spelling")
    out = Path(a.out_dir) if a.out_dir else work_dir()
    out.mkdir(parents=True, exist_ok=True)
    jpath, mpath = out / f"validation_{tag}.json", out / f"validation_{tag}.md"
    jpath.write_text(json.dumps({"where": scope, "read": stamp,
                                 "plants_checked": len(plants), "errors": errors},
                                indent=2, ensure_ascii=False), encoding="utf-8")
    mpath.write_text(memo(scope, plants, errors, stamp), encoding="utf-8")

    kinds = Counter(e["kind"] for e in errors)
    print(f"{scope['kind']}: {scope['name']}  plants: {len(plants)}  "
          f"with errors: {len({e['plant_id'] for e in errors})}")
    print(f"fix: {kinds['fix']}  person: {kinds['person']}  "
          f"exception (optional): {kinds['exception']}")
    print(f"wrote {jpath}\nwrote {mpath}")
    if a.closeout:
        blocking = kinds["fix"] + kinds["person"]
        print("CLOSE-OUT CLEAN" if not blocking else
              f"CLOSE-OUT BLOCKED: {blocking} validation errors to resolve")
        sys.exit(1 if blocking else 0)


if __name__ == "__main__":
    main()

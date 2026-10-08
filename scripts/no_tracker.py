#!/usr/bin/env python3
"""
List the "no tracker found" combustion units for one scope (a US state or a
country). QC/Country checklist row 56 (end of update): the researcher reviews
the units the database has not assigned to GOGPT, GCPT or GBPT, because a unit
with no fuel, or several fuels and no primary one, drops out of every tracker's
export. Those units never appear in the scoped CSV, so this is the only way the
batch sees them.

Usage (from scripts/):
    python no_tracker.py --state Indiana
    python no_tracker.py --country Germany
    python no_tracker.py --state Indiana --include-deleted   # the web UI hides deleted rows

The query lives in the sibling gem-db-ops repo (gogpt/no_tracker.py); this
only scopes it and writes the result for the close-out panel:
  work/no_tracker_<tag>.json   the rows (unit and plant IDs as in the export,
                               fuels, capacity, status, likely reason)
  work/no_tracker_<tag>.md     a plain-language list for the person, or one
                               line saying nothing was found
<tag> is us-<state-slug> or <country-slug>, as validation_report.py names it.
Each live unit is a research task: find the unit's fuel (or pick the primary
fuel) so the database can assign it a tracker. The fix is typed in the web UI;
nothing here stages it.
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from paths import db_ops_repo, work_dir
from build_state_brief import make_scope


def fetch(scope, include_deleted=False):
    sys.path.insert(0, str(db_ops_repo()))
    sys.path.insert(0, str(db_ops_repo() / "gogpt"))
    from gem_query import get_database_url, build_engine, DEFAULT_STATEMENT_TIMEOUT_MS
    from no_tracker import fetch_no_tracker
    engine = build_engine(get_database_url(), DEFAULT_STATEMENT_TIMEOUT_MS)
    state = scope["name"] if scope["kind"] == "state" else None
    return fetch_no_tracker(engine, country=scope["country"], state=state,
                            include_deleted=include_deleted)


def markdown(scope, rows, include_deleted):
    today = datetime.date.today().isoformat()
    head = [f"# Units with no tracker, {scope['name']}", "",
            f"Read from the GEM database on {today}. The database gives a combustion unit "
            "a tracker from its primary fuel. A unit with no fuel, or several fuels and no "
            "primary fuel, gets none and is missing from every tracker's export. "
            "This is checklist row 56 at the end of the update."
            + (" Deleted units are included." if include_deleted else ""), ""]
    if not rows:
        return "\n".join(head + [f"Nothing to review: every combustion unit in {scope['name']} "
                                 "has a tracker.", ""])
    body = [f"{len(rows)} unit(s) to review. For each one, find the fuel and enter it in the "
            "web UI so the database can assign the tracker.", ""]
    for r in rows:
        cap = f"{r['capacity_mw']:g} MW" if r["capacity_mw"] is not None else "no capacity"
        fuels = r["unit_fuels"] or "no fuel recorded"
        flag = " Deleted." if (r["unit_deleted"] or r["plant_deleted"]) else ""
        body.append(f"- {r['plant']}, unit {r['unit'] or '(no name)'} ({r['unit_id']}, plant "
                    f"{r['plant_id']}). {cap}, {r['status'] or 'no status'}. Fuels on the unit: "
                    f"{fuels}. Why it has no tracker: {r['likely_reason']}.{flag}")
    return "\n".join(head + body + [""])


def main():
    p = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--state", help='US state, e.g. "New York"')
    g.add_argument("--country", help="country, e.g. Germany")
    p.add_argument("--include-deleted", action="store_true",
                   help="also list deleted units and units of deleted plants")
    args = p.parse_args()

    scope = make_scope(state=args.state, country=args.country)
    tag = f"us-{scope['slug']}" if scope["kind"] == "state" else scope["slug"]
    rows = fetch(scope, args.include_deleted)

    out_json = work_dir() / f"no_tracker_{tag}.json"
    out_md = work_dir() / f"no_tracker_{tag}.md"
    out_json.write_text(json.dumps({"scope": scope, "pulled": datetime.date.today().isoformat(),
                                    "include_deleted": args.include_deleted, "units": rows},
                                   indent=1), encoding="utf-8")
    out_md.write_text(markdown(scope, rows, args.include_deleted), encoding="utf-8")
    print(f"{scope['name']}: {len(rows)} unit(s) with no tracker. Wrote {out_json.name} and "
          f"{out_md.name} in work/.")
    for r in rows:
        print(f"  {r['unit_id']}  {r['plant']} unit {r['unit'] or '(no name)'}: {r['likely_reason']}")


if __name__ == "__main__":
    main()

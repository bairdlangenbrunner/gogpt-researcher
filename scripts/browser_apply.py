#!/usr/bin/env python3
"""
The plant-by-plant queue for a supervised Claude in Chrome apply, and the
record of each edit once it is saved (docs/sops/database-browser-edits.md).

Usage (from scripts/):
    python browser_apply.py queue --scope us-il               # live database
    python browser_apply.py queue --scope us-il --practice    # test database
    python browser_apply.py record --scope us-il --record-id <id> --readback - <<'EOF'
    {"Status Detail": "<the box as the page shows it after saving>"}
    EOF
    python browser_apply.py status --scope us-il

queue   reads the batch's staged lanes and the review log, keeps the accepted
        edits and new rows only (the same records `build_review_package.py
        --decisions` puts in the actions workbook), drops the ones already in
        applied_in_db.json, groups them by plant and writes
        work/browser_apply_<scope>.json (work/browser_apply_practice_<scope>.json
        with --practice). Refuses a batch with no review log. A plant with an
        entity record whose lookup did not find an existing entity is marked
        blocked: Baird creates the entity first.
record  checks the values read back from the page against the staged record
        and, when they match, appends the record to staging/applied_in_db.json
        with an `applied` block ({date, by: "claude-in-chrome", readback}).
        A practice run logs to work/browser_apply_practice_<scope>_log.json
        instead, so it never hides an edit from the live run. Exits 1 on a
        mismatch, and logs nothing.
status  counts what is applied and what is left, by plant.

Nothing here touches the database. The browser session types; this script
only plans and keeps the record.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from paths import repo_root, work_dir
from build_review_package import load_lanes, load_decisions, decision_of, EDIT_LANES
from schema_constants import ADDITIVE_TEXT_COLUMNS

LIVE_BASE = "https://gem-project-db.herokuapp.com"
PRACTICE_BASE = "https://testdata2-gem-project-db-9960d182aa9b.herokuapp.com"
ENTITY_EXISTS = re.compile(r"existing|found|no new entity", re.I)


def staging_dir(scope: str) -> Path:
    return repo_root() / "batches" / scope / "staging"


def edit_url(plant_id: str, base: str) -> str:
    """The web form's plant page: /projects/edit/<plant.id>, the L ID without its prefix.
    The page must still be checked to name this plant before anything is typed."""
    return f"{base}/projects/edit/{plant_id.lstrip('L')}"


def load_applied(staging: Path) -> dict:
    p = staging / "applied_in_db.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {"meta": {"about": "staged edits found already applied in the GEM database by hand; "
                               "kept out of the review page and the actions workbook"},
            "records": []}


def practice_log_path(scope: str) -> Path:
    return work_dir() / f"browser_apply_practice_{scope}_log.json"


def applied_ids(scope: str, staging: Path, practice: bool) -> set:
    if practice:
        p = practice_log_path(scope)
        data = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"records": []}
    else:
        data = load_applied(staging)
    return {r.get("record_id") for r in data.get("records", [])}


def accepted_records(staging: Path) -> list:
    """(lane, record) for every accepted edit and new row. Exits when the batch has no review log."""
    decisions = load_decisions(staging)
    if decisions is None:
        sys.exit(f"ERROR: no review_log.jsonl in {staging}. Only a reviewed batch is applied "
                 "in the browser (SOP §1).")
    lanes = load_lanes(staging)
    return [(lane, rec) for lane in EDIT_LANES for rec in lanes.get(lane, [])
            if decision_of(rec, decisions) == "accept"]


def build_queue(scope: str, practice: bool = False) -> dict:
    staging = staging_dir(scope)
    base = PRACTICE_BASE if practice else LIVE_BASE
    done = applied_ids(scope, staging, practice)
    plants: dict = {}
    for lane, rec in accepted_records(staging):
        if rec.get("record_id") in done:
            continue
        pid = rec.get("gem_plant_id") or ""
        p = plants.setdefault(pid, {"gem_plant_id": pid, "plant_name": rec.get("plant_name", ""),
                                    "edit_url": edit_url(pid, base), "blocked_by": [],
                                    "edits": [], "new_rows": []})
        item = {k: rec.get(k) for k in ("record_id", "gem_unit_id", "unit_name", "fields",
                                         "current", "refs", "action", "applies_to_all_units",
                                         "sibling_unit_ids")
                if rec.get(k) not in (None, "", [], {})}
        (p["new_rows"] if lane in ("newplants", "newunits") else p["edits"]).append(item)
    for ent in load_lanes(staging).get("entity", []):
        pid = ent.get("gem_plant_id")
        if pid in plants and not ENTITY_EXISTS.search(str(ent.get("lookup_result") or "")):
            plants[pid]["blocked_by"].append(
                f"{ent.get('entity_name')} ({ent.get('role')}) is not in the database yet")
    ordered = sorted(plants.values(), key=lambda p: p["plant_name"].lower())
    for p in ordered:
        p["edits"].sort(key=lambda e: (str(e.get("unit_name") or ""), ",".join(e.get("fields", {}))))
    return {"meta": {"scope": scope, "database": "practice" if practice else "live",
                     "base_url": base,
                     "built": datetime.datetime.now().isoformat(timespec="seconds"),
                     "plants": len(ordered),
                     "edits": sum(len(p["edits"]) for p in ordered),
                     "new_rows": sum(len(p["new_rows"]) for p in ordered),
                     "blocked_plants": sum(1 for p in ordered if p["blocked_by"])},
            "plants": ordered}


def queue_path(scope: str, practice: bool) -> Path:
    return work_dir() / (f"browser_apply_practice_{scope}.json" if practice
                         else f"browser_apply_{scope}.json")


def _norm(s) -> str:
    return re.sub(r"\s+", " ", str(s or "")).strip()


def readback_problems(rec: dict, readback: dict) -> list:
    """What the page shows that does not match the staged record. Value boxes must equal the
    proposed value (whitespace aside); a Data Source box must contain every staged link."""
    problems = []
    for col, want in (rec.get("fields") or {}).items():
        if col not in readback:
            problems.append(f"{col}: not read back from the page")
        elif _norm(readback[col]) != _norm(want):
            kind = "box" if col in ADDITIVE_TEXT_COLUMNS else "value"
            problems.append(f"{col}: the page shows {readback[col]!r}, the {kind} should be {want!r}")
    for col, urls in (rec.get("refs") or {}).items():
        if col in (rec.get("fields") or {}):
            continue                      # Status Detail carries its own links in its text
        if col not in readback:
            problems.append(f"{col}: not read back from the page")
            continue
        missing = [u for u in urls if u not in str(readback[col])]
        if missing:
            problems.append(f"{col}: missing {', '.join(missing)}")
    return problems


def find_record(staging: Path, record_id: str) -> dict:
    for lane, rec in accepted_records(staging):
        if rec.get("record_id") == record_id:
            return rec
    sys.exit(f"ERROR: {record_id} is not an accepted record of this batch")


def record(scope: str, record_id: str, readback: dict, practice: bool = False) -> list:
    staging = staging_dir(scope)
    rec = find_record(staging, record_id)
    problems = readback_problems(rec, readback)
    if problems:
        return problems
    entry = dict(rec)
    entry["applied"] = {"date": datetime.date.today().isoformat(), "by": "claude-in-chrome",
                        "readback": readback}
    if practice:
        path = practice_log_path(scope)
        data = (json.loads(path.read_text(encoding="utf-8")) if path.exists()
                else {"meta": {"about": "practice run on the test database"}, "records": []})
    else:
        path = staging / "applied_in_db.json"
        data = load_applied(staging)
    data["records"] = [r for r in data["records"] if r.get("record_id") != record_id] + [entry]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return []


def status(scope: str, practice: bool = False) -> str:
    staging = staging_dir(scope)
    done = applied_ids(scope, staging, practice)
    by_plant: dict = {}
    for lane, rec in accepted_records(staging):
        name = rec.get("plant_name") or rec.get("gem_plant_id")
        d = by_plant.setdefault(name, [0, 0])
        d[0 if rec.get("record_id") in done else 1] += 1
    lines = [f"{name}: {a} applied, {left} left" for name, (a, left) in sorted(by_plant.items())]
    total_a = sum(v[0] for v in by_plant.values())
    total_left = sum(v[1] for v in by_plant.values())
    lines.append(f"Total: {total_a} applied, {total_left} left")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("queue", "record", "status"):
        s = sub.add_parser(name)
        s.add_argument("--scope", required=True, help="batch folder name, e.g. us-il")
        s.add_argument("--practice", action="store_true", help="the test database, logged apart")
        if name == "record":
            s.add_argument("--record-id", required=True)
            s.add_argument("--readback", required=True,
                           help="JSON file of {column: value as the page shows it}, or - for stdin")
    a = ap.parse_args()
    if a.cmd == "queue":
        q = build_queue(a.scope, a.practice)
        out = queue_path(a.scope, a.practice)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(q, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        m = q["meta"]
        print(f"{m['database']} database: {m['plants']} plants, {m['edits']} edits, "
              f"{m['new_rows']} new rows, {m['blocked_plants']} plants waiting on an entity")
        print(f"wrote {out}")
    elif a.cmd == "record":
        raw = sys.stdin.read() if a.readback == "-" else Path(a.readback).read_text(encoding="utf-8")
        problems = record(a.scope, a.record_id, json.loads(raw), a.practice)
        if problems:
            print("NOT RECORDED. The page does not match the staged edit:")
            print("\n".join(f"  {p}" for p in problems))
            sys.exit(1)
        print(f"recorded {a.record_id}")
    else:
        print(status(a.scope, a.practice))


if __name__ == "__main__":
    main()

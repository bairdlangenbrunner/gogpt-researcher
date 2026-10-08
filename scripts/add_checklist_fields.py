#!/usr/bin/env python3
"""
Add the checklist bookkeeping fields to staged lane files that already exist,
in place, without rebuilding them from shards. For a staging folder that was
curated by hand after assembly (Maryland and New York, 2026-10-02 to 10-05) a
rebuild would undo the curation; this adds only the fields assemble_state.py
now writes, and never touches a record_id, a value or a note.

    python add_checklist_fields.py --staging ../batches/us-ny/staging [--staging ...] \
        [--csv gem_export_gogpt_scoped.csv] [--dry-run]

What it adds (docs/reference/staged_json_schema.md)
  qa        concern_type mapped onto the vocabulary (review_app/checklist.py
            normalize_concern_type); the shard's text kept in concern_type_raw
  monitor   monitor_reason (from the older `item` key or the note's first
            sentence), recheck_by (blank when missing; state_gate.py flags
            it), monitor_kind (existing_plant when gem_plant_id is set, else
            new_to_tracker)
  updates / qa
            checks: the QC/Country checklist rows of the brief task that would
            have asked for this field, derived from the export row with
            build_state_brief.unit_tasks (unit and sibling units)
  meta      checklist_fields: the date this ran

Idempotent: a second run changes nothing. Read-only on the export.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from assemble_state import load_export, ws  # noqa: E402
from build_state_brief import unit_tasks  # noqa: E402
from paths import gogpt_scoped_csv  # noqa: E402
from review_app.checklist import (  # noqa: E402
    CONCERN_VOCAB, MONITOR_KINDS, normalize_concern_type)

LANES = ("updates", "qa", "monitor", "newunits", "newplants", "entity")


def load(staging: Path):
    out = {}
    for lane in LANES:
        p = staging / f"staged_{lane}.json"
        if p.exists():
            out[lane] = json.loads(p.read_text(encoding="utf-8"))
    return out


def unit_ids(lanes):
    ids = set()
    for env in lanes.values():
        for r in env.get("records") or []:
            ids.add(r.get("gem_unit_id") or "")
            ids |= set(r.get("sibling_unit_ids") or [])
    return {u for u in ids if u}


def task_checks(export, uids, year, us):
    """(unit_id, field) -> checklist rows, from the brief's per-unit tasks."""
    out = {}
    for uid in uids:
        row = export.get(uid)
        if row is None:
            continue
        for _, fields, checks in unit_tasks(row, year=year, us=us):
            for f in fields:
                out.setdefault((uid, f), set()).update(checks)
    return out


def checks_for(tc, rec, field):
    rows = set()
    for u in [rec.get("gem_unit_id") or ""] + list(rec.get("sibling_unit_ids") or []):
        rows |= tc.get((u, field), set())
    return sorted(rows)


def annotate(lanes, export, year, us):
    n = {"concern_type": 0, "monitor": 0, "checks": 0}
    tc = task_checks(export, unit_ids(lanes), year, us)
    for r in (lanes.get("qa") or {}).get("records") or []:
        raw = ws(r.get("concern_type")) or "other"
        ct = raw if raw in CONCERN_VOCAB else normalize_concern_type(raw, r)
        if ct != raw:
            r.setdefault("concern_type_raw", raw)
            r["concern_type"] = ct
            n["concern_type"] += 1
        if ct in CONCERN_VOCAB and not r.get("checks"):
            rows = checks_for(tc, r, ct)
            if rows:
                r["checks"] = rows
                n["checks"] += 1
    for r in (lanes.get("monitor") or {}).get("records") or []:
        before = (r.get("monitor_reason"), r.get("recheck_by"), r.get("monitor_kind"))
        reason = ws(r.get("monitor_reason")) or ws(r.pop("item", ""))
        if not reason:
            reason = re.split(r"(?<=[.!?])\s+", ws(r.get("researcher_notes")), 1)[0][:200]
        r.pop("item", None)
        r["monitor_reason"] = reason
        r.setdefault("recheck_by", "")
        if r.get("monitor_kind") not in MONITOR_KINDS:
            r["monitor_kind"] = ("existing_plant" if ws(r.get("gem_plant_id"))
                                 else "new_to_tracker")
        if before != (r["monitor_reason"], r["recheck_by"], r["monitor_kind"]):
            n["monitor"] += 1
    for r in (lanes.get("updates") or {}).get("records") or []:
        if r.get("checks"):
            continue
        rows = set()
        for f in (r.get("fields") or {}):
            rows |= set(checks_for(tc, r, f))
        if rows:
            r["checks"] = sorted(rows)
            n["checks"] += 1
    return n


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--staging", action="append", required=True,
                    help="a staging or staging-discovery folder (repeatable)")
    ap.add_argument("--csv", default=None, help="scoped export (default: the "
                    "csv named in the lane meta, else scripts/gem_export_gogpt_scoped.csv)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    today = datetime.date.today().isoformat()
    for s in a.staging:
        staging = Path(s).resolve()
        lanes = load(staging)
        if not lanes:
            print(f"{staging}: no staged_*.json files; skipped")
            continue
        meta = next(iter(lanes.values())).get("meta") or {}
        scope = meta.get("scope") or {}
        us = (scope.get("country") or "United States").lower() == "united states"
        year = int((meta.get("generated") or today)[:4])
        csv_path = Path(a.csv) if a.csv else (
            Path(scope["csv"]) if scope.get("csv") and Path(scope["csv"]).exists()
            else gogpt_scoped_csv())
        _, export = load_export(csv_path, unit_ids(lanes))
        n = annotate(lanes, export, year, us)
        print(f"{staging}: question types mapped {n['concern_type']}, watch items "
              f"normalized {n['monitor']}, records given checklist rows {n['checks']}"
              f"{' (dry run, nothing written)' if a.dry_run else ''}")
        if a.dry_run:
            continue
        for lane, env in lanes.items():
            env.setdefault("meta", {})["checklist_fields"] = today
            (staging / f"staged_{lane}.json").write_text(
                json.dumps(env, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

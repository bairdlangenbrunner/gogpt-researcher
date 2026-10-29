#!/usr/bin/env python3
"""
Give the question records of a staging folder that already exists the four-part shape
(question, finding, recommendation, researcher_notes; docs/reference/notes_style.md,
"Questions"), in place, without rebuilding the folder from shards. A staging folder that was
curated by hand after assembly must never be reassembled; this touches only the three text
fields on qa records and never a record id, a note, a ref, a value or a call.

Two steps, because the drafting is a model's job and the writing is this script's:

    python add_question_fields.py --staging ../batches/us-ia/staging --list work/qa_rows.json
        writes the qa records that lack question or finding (id, plant, unit, concern type,
        note, recommendation) for a cheap model to draft from

    python add_question_fields.py --staging ../batches/us-ia/staging --drafts work/qa_drafts.json [--dry-run]
        reads {record_id: {question, finding, recommendation}}, checks each draft against the
        gate's rules (state_gate.gate_questions: a question that ends with a question mark, a
        finding of one to three sentences, a recommendation of at most two sentences that
        gives an instruction), prints a before-and-after table, and writes the fields. A
        recommendation that changed keeps the original in recommendation_raw. A draft that
        fails a check is printed and skipped, so the file can be fixed and the step rerun.

    python add_question_fields.py --staging ../batches/us-ia/staging --merge [--dry-run]
        folds a plant-level question from the statewide pass into the plant's own question on
        the same concern (assemble_state.merge_plant_question), the way the assembler now does
        at assembly time. The folded record is removed from the qa lane; the kept one gains
        merged_from and a second paragraph in its note.

Each write stamps meta.question_fields with the date, which makes state_gate's questions gate
hard for the folder. Idempotent: a second run with the same drafts changes nothing.
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from assemble_state import load_export, merge_plant_question, ws  # noqa: E402
from paths import gogpt_scoped_csv  # noqa: E402
from state_gate import gate_questions  # noqa: E402

DRAFT_KEYS = ("question", "finding", "recommendation")


def load_qa(staging: Path):
    p = staging / "staged_qa.json"
    if not p.exists():
        sys.exit(f"ERROR: {p} not found")
    return p, json.loads(p.read_text(encoding="utf-8"))


def needs_fields(r):
    return not ws(r.get("question")) or not ws(r.get("finding"))


def list_rows(env):
    return [{"record_id": r["record_id"], "plant_name": r.get("plant_name") or "",
             "unit_name": r.get("unit_name") or "", "concern_type": r.get("concern_type") or "",
             "researcher_notes": r.get("researcher_notes") or "",
             "recommendation": r.get("recommendation") or ""}
            for r in env.get("records") or [] if needs_fields(r)]


def check_draft(rid, draft):
    """The gate's reasons for refusing this draft, as if it were the record."""
    if not isinstance(draft, dict) or any(not ws(draft.get(k)) for k in DRAFT_KEYS):
        return ["draft needs question, finding and recommendation"]
    rec = {"record_id": rid}
    rec.update({k: ws(draft[k]) for k in DRAFT_KEYS})
    return [reason for _, reason in gate_questions({"qa": [rec]}, strict=True)]


def apply_drafts(env, drafts):
    """-> (changed records as (rid, before, after), skipped as (rid, reasons))."""
    changed, skipped = [], []
    for r in env.get("records") or []:
        rid = r["record_id"]
        d = drafts.get(rid)
        if d is None:
            continue
        reasons = check_draft(rid, d)
        if reasons:
            skipped.append((rid, reasons))
            continue
        before = {k: r.get(k) or "" for k in DRAFT_KEYS}
        after = {k: ws(d[k]) for k in DRAFT_KEYS}
        if before == after:
            continue
        if after["recommendation"] != before["recommendation"]:
            r.setdefault("recommendation_raw", before["recommendation"])
        for k in DRAFT_KEYS:
            r[k] = after[k]
        changed.append((rid, before, after))
    return changed, skipped


def plant_units(export):
    out = {}
    for uid, row in export.items():
        out.setdefault(row.get("GEM location ID") or "", []).append(uid)
    return out


def merge_lane(env, units_by_plant):
    """-> [(dropped id, kept id)]; the dropped records leave env."""
    recs = env.get("records") or []
    kept, merged = [], []
    for r in recs:
        if ws(r.get("gem_plant_id")) and not ws(r.get("gem_unit_id")):
            target = merge_plant_question(r, kept + [x for x in recs if x is not r and x not in kept],
                                          units_by_plant.get(ws(r.get("gem_plant_id")), []))
            if target is not None:
                merged.append((r["record_id"], target["record_id"]))
                continue
        kept.append(r)
    env["records"] = kept
    return merged


def show(label, text, width=110):
    text = ws(text)
    print(f"      {label:<8} {text[:width]}{'…' if len(text) > width else ''}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--staging", required=True, help="a staging folder")
    ap.add_argument("--list", metavar="OUT.json", help="write the records that need drafts")
    ap.add_argument("--drafts", metavar="IN.json", help="apply drafts keyed by record_id")
    ap.add_argument("--merge", action="store_true", help="fold plant-level duplicates into the plant's own question")
    ap.add_argument("--csv", default=None, help="scoped export for --merge (default: the lane meta's csv, else scripts/gem_export_gogpt_scoped.csv)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if not (a.list or a.drafts or a.merge):
        ap.error("pass --list, --drafts or --merge")
    staging = Path(a.staging).resolve()
    path, env = load_qa(staging)
    today = datetime.date.today().isoformat()
    dirty = False

    if a.list:
        rows = list_rows(env)
        Path(a.list).write_text(json.dumps(rows, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{staging.name}: {len(rows)} of {len(env.get('records') or [])} question records need a question and finding; wrote {a.list}")

    if a.drafts:
        drafts = json.loads(Path(a.drafts).read_text(encoding="utf-8"))
        changed, skipped = apply_drafts(env, drafts)
        for rid, before, after in changed:
            print(f"  {rid}")
            show("question", after["question"])
            show("finding", after["finding"])
            if after["recommendation"] != before["recommendation"]:
                show("was", before["recommendation"])
                show("suggest", after["recommendation"])
            else:
                show("suggest", after["recommendation"])
        for rid, reasons in skipped:
            print(f"  SKIPPED {rid}: " + "; ".join(reasons))
        missing = [r["record_id"] for r in env.get("records") or [] if needs_fields(r) and r["record_id"] not in drafts]
        print(f"{staging.name}: {len(changed)} records given question fields, {len(skipped)} drafts skipped, "
              f"{len(missing)} records still without a draft")
        dirty = bool(changed)

    if a.merge:
        meta = env.get("meta") or {}
        scope = meta.get("scope") or {}
        csv_path = Path(a.csv) if a.csv else (
            Path(scope["csv"]) if scope.get("csv") and Path(scope["csv"]).exists() else gogpt_scoped_csv())
        _, export = load_export(csv_path)
        merged = merge_lane(env, plant_units(export))
        for gone, kept in merged:
            print(f"  folded {gone} into {kept}")
        print(f"{staging.name}: {len(merged)} plant-level questions folded into the plant's own question")
        dirty = dirty or bool(merged)

    if a.dry_run:
        print("dry run, nothing written")
        return
    if dirty:
        env.setdefault("meta", {})["question_fields"] = today
        env["meta"].setdefault("counts", {})["records"] = len(env.get("records") or [])
        path.write_text(json.dumps(env, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {path}")
    else:
        print("nothing changed")


if __name__ == "__main__":
    main()

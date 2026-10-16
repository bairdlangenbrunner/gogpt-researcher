"""Every validation report item is answered in the batch (Baird 2026-10-16):
state_gate.gate_validation fails an unanswered item and a missing or stale
report, assemble_state keys a task with no fields on "validation" so the qa
answer keeps check 7, and the brief marks those tasks."""
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from assemble_state import Assembler  # noqa: E402
from build_state_brief import VALIDATION_MARK, task_line  # noqa: E402
from state_gate import gate_validation  # noqa: E402

NOW = datetime.datetime(2026, 10, 16, 13, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=-4)))
WHERE = {"kind": "state", "name": "Illinois", "slug": "illinois",
         "country": "United States", "postal": "il"}


def index(**extra):
    d = {"mode": "update", "where": WHERE, "plants": [
        {"plant_id": "L1", "unit_ids": ["G1", "G2"],
         "tasks": {"G1": [{"text": "Mothballed status step has no date.", "fields": [],
                           "checks": [7]},
                          {"text": "Capacity is blank.", "fields": ["Capacity (MW)"],
                           "checks": [12]}]},
         "plant_tasks": []},
        {"plant_id": "L2", "unit_ids": ["G3"], "tasks": {},
         "plant_tasks": [{"text": "Replacement link is broken.", "fields": [],
                          "checks": [7]}]}]}
    d.update(extra)
    return d


def report(tmp_path, errors, read=NOW - datetime.timedelta(hours=2)):
    p = tmp_path / "validation_us-illinois.json"
    p.write_text(json.dumps({"read": read.isoformat(), "errors": errors}), encoding="utf-8")
    return p


def answered(*recs):
    return {"qa": list(recs), "updates": []}


def qa(pid, uid, checks=(7,), siblings=()):
    return {"record_id": f"{pid}:{uid or 'plant'}:qa-validation-1", "gem_plant_id": pid,
            "gem_unit_id": uid, "concern_type": "validation", "checks": list(checks),
            "sibling_unit_ids": list(siblings)}


def test_passes_when_every_item_has_a_check_7_record(tmp_path):
    vp = report(tmp_path, [{"kind": "fix", "plant_id": "L1", "unit_id": "G2", "item": "Status"},
                           {"kind": "exception", "plant_id": "L9", "unit_id": "G9"}])
    lanes = answered(qa("L1", "G1", siblings=["G2"]), qa("L2", None))
    out, info = gate_validation(index(), lanes, vp, now=NOW)
    assert out == []
    assert "validation items to answer: 3" in info


def test_fails_on_an_unanswered_item(tmp_path):
    vp = report(tmp_path, [{"kind": "person", "plant_id": "L1", "unit_id": "G2", "item": "Fuel"}])
    lanes = answered(qa("L1", "G1"), qa("L2", None), qa("L1", "G2", checks=[12]))
    out, _ = gate_validation(index(), lanes, vp, now=NOW)
    assert [k for k, _ in out] == ["L1:G2"]
    assert "person: Fuel" in out[0][1]


def test_whole_plant_item_needs_a_record_on_that_plant(tmp_path):
    vp = report(tmp_path, [])
    out, _ = gate_validation(index(), answered(qa("L1", "G1")), vp, now=NOW)
    assert [k for k, _ in out] == ["L2:plant"]


def test_missing_and_stale_report(tmp_path):
    lanes = answered(qa("L1", "G1"), qa("L2", None))
    out, _ = gate_validation(index(), lanes, tmp_path / "nope.json", now=NOW)
    assert out and "run validation_report.py" in out[0][1]
    old = report(tmp_path, [], read=NOW - datetime.timedelta(days=3))
    out, _ = gate_validation(index(), lanes, old, now=NOW)
    assert out and "3.0 days old" in out[0][1]
    out, info = gate_validation(index(), lanes, old, allow_stale=True, now=NOW)
    assert out == [] and any(i.startswith("warning:") for i in info)


def test_skipped_outside_update_mode(tmp_path):
    out, info = gate_validation(index(mode="blind"), {}, tmp_path / "nope.json", now=NOW)
    assert out == [] and info == ["skipped: not an update batch"]


def test_assembler_keys_a_fieldless_task_on_validation(tmp_path):
    (tmp_path / "briefs").mkdir()
    (tmp_path / "briefs" / "_index.json").write_text(json.dumps(index()), encoding="utf-8")
    a = Assembler(tmp_path, tmp_path / "unused.csv", "2026Q4")
    assert a.checks_for("L1", "G1", "validation") == [7]
    assert a.checks_for("L1", "G1", "Capacity (MW)") == [12]
    assert a.checks_for("L1", "G2", "validation", siblings=["G1"]) == [7]
    assert a.checks_for("L2", None, "validation") == [7]
    assert a.checks_for("L2", "G3", "validation") == [7]


def test_task_line_marks_validation_tasks():
    assert task_line("Status step has no date.", [7, 12]) == f"{VALIDATION_MARK} Status step has no date."
    assert task_line("Capacity is blank.", [12]) == "Capacity is blank."
    assert task_line("Capacity is blank.", None) == "Capacity is blank."

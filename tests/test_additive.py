"""Status Detail and Notes are additive, newest on top (Baird 2026-10-07):
additive_value composes the cell, assemble_state.build_action words the
instruction, and validate / state_gate.gate_additive reject a rewrite."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from build_review_package import additive_value, validate  # noqa: E402
from assemble_state import build_action  # noqa: E402
from state_gate import gate_additive  # noqa: E402

OLD = "AM Jun26: No major 2026 announcement identified.\nDOB Nov25: Still mentioned on the site."
NEW = "Iqony named Bexbach as a possible site for a hydrogen-ready gas plant in September 2026."


def rec(col, value, current, **extra):
    r = {"record_id": f"L1:G1:{col.lower().replace(' ', '-')}", "gem_plant_id": "L1",
         "gem_unit_id": "G1", "fields": {col: value}, "current": {col: current},
         "refs": {"Status Data Source": ["https://example.com/a"]},
         "verifications": [{"url": "https://example.com/a", "ok": True}]}
    r.update(extra)
    return r


def test_additive_value_prepends_and_keeps_old_text():
    assert additive_value(NEW, OLD) == f"{NEW}\n{OLD}"
    assert additive_value(NEW, "") == NEW
    assert additive_value("", OLD) == OLD


def test_additive_value_is_a_match_when_the_box_already_says_it():
    assert additive_value("still mentioned on the site", OLD) == OLD


def test_action_says_add_at_the_top():
    s = build_action("change", "Status Detail", NEW, OLD, "unit 1 (G1)",
                     "Status Data Source", 1, additive=True)
    assert s.startswith("Add this at the top of the Status Detail box of unit 1 (G1), "
                        "above the text already there: ")
    assert "Keep the existing text below it, word for word." in s
    assert "Keep the links already there." in s


def test_validate_and_gate_reject_a_rewrite():
    bad = rec("Status Detail", NEW, OLD)
    good = rec("Status Detail", additive_value(NEW, OLD), OLD, additive=True)
    cleared = rec("Notes", "", "an old note", delete=True)
    errs = validate({"updates": [bad, good, cleared]})
    assert any("drops or rewrites" in e for e in errs)
    assert any("never cleared" in e for e in errs)
    assert not [e for e in errs if "G1: Status Detail" in e and "word for word" in e
                and additive_value(NEW, OLD) in e]
    gate = gate_additive({"updates": [bad, good, cleared]})
    assert [rid for rid, _ in gate] == [bad["record_id"], cleared["record_id"]]


def test_gate_checks_every_sibling_of_a_plant_wide_edit():
    r = rec("Status Detail", additive_value(NEW, OLD), OLD, additive=True,
            applies_to_all_units=True, sibling_unit_ids=["G2"],
            sibling_current={"G2": "a different note on unit 2"})
    gate = gate_additive({"updates": [r]})
    assert len(gate) == 1 and "of G2" in gate[0][1]

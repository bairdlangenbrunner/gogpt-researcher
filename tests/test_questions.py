"""A question a reviewer can read at a glance (Baird 2026-10-27, gem-review-app docs/questions.md):
every qa record carries question, finding and recommendation in the four-part shape, the gate
checks the shape, the assembler folds a statewide duplicate into the plant's own question, the
IRP brief tells the scope-wide agent not to write that duplicate, and add_question_fields.py
backfills a curated staging folder in place."""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import add_question_fields as aqf  # noqa: E402
import irp_sheet  # noqa: E402
from assemble_state import Assembler, merge_plant_question  # noqa: E402
from state_gate import gate_notes, gate_questions, question_strict, sentences_of  # noqa: E402

PLAN = "https://www.alliantenergy.com/-/media/2024-irp.pdf"
TENK = "https://www.sec.gov/Archives/edgar/data/0000352541/000035254126000043/lnt-20260630.htm"
GOOD = {"question": "Is the 430 MW combined cycle unit from the 2024 study still planned?",
        "finding": "The study, dated February 13, 2025, adds a 430 MW combined cycle unit in 2029. No later filing names it.",
        "recommendation": "Leave the unit as announced. Check again when Alliant files a combined cycle plan."}


def qa(rid="L1:G1:qa-existence-1", **over):
    rec = {"record_id": rid, "gem_plant_id": "L1", "gem_unit_id": "G1", "concern_type": "existence",
           "refs": {"links": [PLAN]}, "verifications": [{"url": PLAN, "ok": True}],
           "researcher_notes": "The study adds a 430 MW combined cycle unit in 2029. Nothing later names it."}
    rec.update(GOOD)
    rec.update(over)
    return rec


# ------------------------------------------------------------------ gate ---

def test_sentences_split_on_a_capital_after_a_period():
    assert len(sentences_of(GOOD["finding"])) == 2
    assert len(sentences_of("Keep it. Check again in 2027.")) == 2
    assert sentences_of("") == []
    assert len(sentences_of("Should Earl F. Wisdom Unit 1 be linked to Unit No. 2 of Corn Belt Power Co. in the U.S. tracker?")) == 1
    assert len(sentences_of("The unit is 40 MW. It burns gas.")) == 2


def test_a_four_part_question_passes():
    assert gate_questions({"qa": [qa()]}, strict=True) == []


def test_the_gate_names_each_broken_part():
    recs = [qa("L1:G1:qa-1", question="The unit is still planned."),
            qa("L1:G1:qa-2", question="Is it planned? Was it ever?"),
            qa("L1:G1:qa-3", finding="One. Two. Three. Four."),
            qa("L1:G1:qa-4", recommendation="Keep it. Check later. Ask the PM."),
            qa("L1:G1:qa-5", recommendation="The reviewer should decide whether it still belongs."),
            qa("L1:G1:qa-6", recommendation="")]
    out = dict(gate_questions({"qa": recs}, strict=True))
    assert out["L1:G1:qa-1"] == "question does not end with a question mark"
    assert out["L1:G1:qa-2"] == "question is more than one sentence"
    assert out["L1:G1:qa-3"].startswith("finding runs to 4 sentences")
    assert out["L1:G1:qa-4"].startswith("recommendation runs to 3 sentences")
    assert "hands the call back ('reviewer should decide')" in out["L1:G1:qa-5"]
    assert out["L1:G1:qa-6"].startswith("no recommendation")


def test_missing_question_and_finding_fail_only_when_strict():
    old = qa(question="", finding="")
    assert gate_questions({"qa": [old]}) == []
    reasons = [r for _, r in gate_questions({"qa": [old]}, strict=True)]
    assert any(r.startswith("no question") for r in reasons)
    assert any(r.startswith("no finding") for r in reasons)


def test_strictness_comes_from_the_flag_the_backfill_stamp_or_the_assembly_date():
    assert question_strict({"qa": {"generated": "2026-10-19"}}) is False
    assert question_strict({"qa": {"generated": "2026-10-19"}}, flag=True) is True
    assert question_strict({"qa": {"generated": "2026-10-19", "question_fields": "2026-10-27"}}) is True
    assert question_strict({"qa": {"generated": "2026-10-28"}}) is True
    assert question_strict({}) is False


def test_the_notes_gate_reads_the_question_fields_too():
    rec = qa(finding="The shard says the unit is staged — see the ref.")
    reasons = [r for _, r in gate_notes({"qa": [rec]})]
    assert any(r.startswith("finding") for r in reasons), reasons


# ----------------------------------------------------------------- merge ---

def statewide(**over):
    rec = {"record_id": "us-ia:plant:qa-existence-1", "gem_plant_id": "L1", "gem_unit_id": "",
           "concern_type": "existence", "refs": {"links": [TENK]},
           "verifications": [{"url": TENK, "ok": True}, {"url": PLAN, "ok": False}],
           "finding": "Alliant's quarterly report for June 30, 2026 lists only simple-cycle projects.",
           "recommendation": "Keep the placeholder for now.", "researcher_notes": "A long note.", "irp": True}
    rec.update(over)
    return rec


def test_a_statewide_question_folds_into_the_only_unit_question():
    target = qa()
    kept = merge_plant_question(statewide(), [target], ["G1"])
    assert kept is target
    assert kept["merged_from"] == "us-ia:plant:qa-existence-1"
    assert kept["refs"]["links"] == [PLAN, TENK]
    assert [v["url"] for v in kept["verifications"]] == [PLAN, TENK]
    assert kept["verifications"][0] == {"url": PLAN, "ok": True}
    assert kept["researcher_notes"].endswith(
        "A second check of the plan found: Alliant's quarterly report for June 30, 2026 lists only "
        "simple-cycle projects. Keep the placeholder for now.")
    assert kept["irp"] is True
    assert kept["question"] == GOOD["question"]


def test_no_fold_on_a_two_unit_plant_another_concern_or_a_unit_question():
    assert merge_plant_question(statewide(), [qa()], ["G1", "G2"]) is None
    assert merge_plant_question(statewide(concern_type="capacity"), [qa()], ["G1"]) is None
    assert merge_plant_question(statewide(gem_unit_id="G1"), [qa()], ["G1"]) is None
    plant_level = qa("L1:plant:qa-existence-1", gem_unit_id="")
    assert merge_plant_question(statewide(), [plant_level], ["G1", "G2"]) is plant_level


HEADER = ["Country/Area", "Plant name", "Unit name", "Status", "Capacity (MW)", "Latitude",
          "Longitude", "Location accuracy", "Location Data Source", "City", "State/Province",
          "GEM location ID", "GEM unit ID"]


def batch(tmp_path):
    (tmp_path / "briefs").mkdir()
    (tmp_path / "shards").mkdir()
    index = {"mode": "update", "where": {"kind": "state", "name": "Iowa", "slug": "iowa",
                                         "country": "United States", "postal": "ia"},
             "scope": "ladder", "plants": [{"plant_id": "L1", "plant_name": "IRP station 1",
                                            "unit_ids": ["G1"], "tasks": {}, "plant_tasks": []}]}
    (tmp_path / "briefs" / "_index.json").write_text(json.dumps(index), encoding="utf-8")
    csv_path = tmp_path / "export.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        w.writerow(["United States", "IRP station 1", "1", "announced", "430", "42.0", "-93.0",
                    "approximate", "", "Ames", "Iowa", "L1", "G1"])
    shard = {"meta": {"plant_id": "L1", "plant_name": "IRP station 1", "state": "Iowa", "mode": "update",
                      "model": "sonnet", "done": True},
             "units": [{"gem_unit_id": "G1", "unit_name": "1", "findings": {}, "not_found": [], "notes": ""}],
             "plant_findings": {},
             "qa": [{"gem_unit_id": "G1", "concern_type": "existence", "refs": [PLAN],
                     "verifications": [{"url": PLAN, "ok": True}], "note": "The plant's own note.", **GOOD}],
             "monitor": [], "newunits": [], "entities": [], "source_log": []}
    (tmp_path / "shards" / "L1.json").write_text(json.dumps(shard), encoding="utf-8")
    state = {"meta": {}, "qa": [{"gem_plant_id": "L1", "plant_name": "IRP station 1", "concern_type": "existence",
                                 "refs": [TENK], "verifications": [{"url": TENK, "ok": True}],
                                 "note": "The statewide note.", "finding": "The quarterly report lists only simple-cycle projects.",
                                 "recommendation": "Keep the placeholder for now."}],
             "monitor": [], "newplants": [], "newunits": [], "entities": [], "source_log": []}
    (tmp_path / "shards" / "_state.json").write_text(json.dumps(state), encoding="utf-8")
    return csv_path


def test_the_assembler_folds_the_statewide_duplicate_and_reports_it(tmp_path):
    csv_path = batch(tmp_path)
    a = Assembler(tmp_path, csv_path, "2026Q4")
    a.run()
    assert [r["record_id"] for r in a.lanes["qa"]] == ["L1:G1:qa-existence-1"]
    r = a.lanes["qa"][0]
    assert a.merged == [("us-ia:plant:qa-existence-1", "L1:G1:qa-existence-1")]
    assert r["merged_from"] == "us-ia:plant:qa-existence-1"
    assert r["question"] == GOOD["question"] and r["finding"] == GOOD["finding"]
    assert "A second check of the plan found: The quarterly report lists only simple-cycle projects. Keep the placeholder for now." in r["researcher_notes"]
    assert r["refs"]["links"] == [PLAN, TENK]
    assert gate_questions(a.lanes, strict=True) == []


# ----------------------------------------------------------------- brief ---

def test_the_irp_brief_sends_plant_questions_to_the_plant_brief():
    text = irp_sheet.render_brief("Iowa", {"skipped": False, "utilities": [], "state_links": [], "irp_units": []})
    assert "do not write a question about it here" in text
    assert "meta.irp_summary" in text


# -------------------------------------------------------------- backfill ---

def test_backfill_checks_each_draft_and_keeps_the_old_recommendation(tmp_path, capsys):
    env = {"meta": {"generated": "2026-10-19", "counts": {"records": 2}},
           "records": [qa("L1:G1:qa-1", question="", finding="", recommendation="Keep it. The reviewer should decide later."),
                       qa("L1:G2:qa-2", question="", finding="", recommendation="Keep it.")]}
    assert [r["record_id"] for r in aqf.list_rows(env)] == ["L1:G1:qa-1", "L1:G2:qa-2"]
    drafts = {"L1:G1:qa-1": dict(GOOD),
              "L1:G2:qa-2": {"question": "Is it planned", "finding": "Yes.", "recommendation": "Keep it."}}
    changed, skipped = aqf.apply_drafts(env, drafts)
    assert [c[0] for c in changed] == ["L1:G1:qa-1"]
    assert skipped == [("L1:G2:qa-2", ["question does not end with a question mark"])]
    r = env["records"][0]
    assert r["question"] == GOOD["question"] and r["recommendation"] == GOOD["recommendation"]
    assert r["recommendation_raw"] == "Keep it. The reviewer should decide later."
    assert r["researcher_notes"].startswith("The study adds")
    assert env["records"][1].get("question", "") == ""
    # a second pass with the same drafts changes nothing
    assert aqf.apply_drafts(env, {"L1:G1:qa-1": dict(GOOD)}) == ([], [])


def test_backfill_merge_removes_the_folded_record(tmp_path):
    env = {"meta": {}, "records": [qa(), statewide()]}
    merged = aqf.merge_lane(env, {"L1": ["G1"]})
    assert merged == [("us-ia:plant:qa-existence-1", "L1:G1:qa-existence-1")]
    assert [r["record_id"] for r in env["records"]] == ["L1:G1:qa-existence-1"]
    assert env["records"][0]["merged_from"] == "us-ia:plant:qa-existence-1"


# ------------------------------------------------------------ note drift ---

def test_note_drift_flags_a_database_note_written_after_the_brief(tmp_path):
    from state_gate import brief_notes, gate_note_drift
    batch = tmp_path / "batches" / "us-ia"
    (batch / "briefs").mkdir(parents=True)
    brief = batch / "briefs" / "L1.md"
    brief.write_text("# Plant (L1)\n\n## Notes and history\n\n### Unit 1 IRP (G1)\n\n- Last Updated: 2026-05-08\n"
                     "- Researcher: Andrew Mkali\n- Notes (verbatim):\n\n```\n(blank)\n```\n\n### Unit 2 (G2)\n\n"
                     "- Last Updated: 2026-05-08\n- Researcher: Andrew Mkali\n- Notes (verbatim):\n\n```\nAM: permit filed.\nSecond line.\n```\n\n"
                     "## Worklist\n\n- 1 IRP (G1): priority 1\n", encoding="utf-8")
    assert brief_notes(brief) == {"G1": "", "G2": "AM: permit filed.\nSecond line."}
    index = {"generated": "2026-10-16T16:19:52-04:00",
             "plants": [{"plant_id": "L1", "brief_path": "batches/us-ia/briefs/L1.md", "unit_ids": ["G1", "G2"]}]}
    export = {"G1": {"Notes": "Most likely related to the Bobcat and Cedar River projects"},
              "G2": {"Notes": "AM: permit filed.  Second line."}}
    out = gate_note_drift(batch, index, export)
    assert [rid for rid, _ in out] == ["L1:G1"]
    assert "since the brief of 2026-10-16" in out[0][1] and "Bobcat" in out[0][1]
    # a unit the export no longer has, or a brief that is missing, is not drift
    assert gate_note_drift(batch, index, {"G2": {"Notes": "AM: permit filed. Second line."}}) == []
    assert gate_note_drift(batch, {"plants": [{"plant_id": "L9", "brief_path": "nowhere.md"}]}, export) == []

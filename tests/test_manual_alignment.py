"""Gates, worklist and location selection after the September 2026 manual audit
(notes/manual_audit_2026-10-27.md): the data-centers gate, optional validation
items, the new worklist ladder, place-field selection, the backup-only chase rule,
the inferred-status source rule and notes_cleanup."""
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import location_candidates as lc  # noqa: E402
import build_state_brief as bsb  # noqa: E402
import qc_checks  # noqa: E402
import worklist as wl  # noqa: E402
from state_gate import (chase_hits, gate_concern_types, gate_data_centers,  # noqa: E402
                        gate_orphans, gate_validation)
from test_validation_gate import NOW, answered, index, qa, report  # noqa: E402


# ---- data-centers gate ----

def dc_setup(tmp_path, sites, answers=None):
    batch = tmp_path / "us-xx"
    batch.mkdir(exist_ok=True)
    permits = tmp_path / "permits"
    permits.mkdir(exist_ok=True)
    (permits / "_data_centers.json").write_text(json.dumps({"sites": sites}), encoding="utf-8")
    if answers is not None:
        (batch / "coverage.json").write_text(json.dumps({"data_centers": answers}), encoding="utf-8")
    return batch, permits


SITE = {"site_id": "S1", "name": "Alpha DC", "verdict": "at_threshold", "summed_nameplate_mw": 80}


def run_dc(tmp_path, answers, sites=(SITE,), lanes=None):
    batch, permits = dc_setup(tmp_path, list(sites), answers)
    return gate_data_centers({}, lanes or {}, batch, permits_dir=permits)


def test_dc_missing_file_is_a_warning(tmp_path):
    batch = tmp_path / "us-xx"
    batch.mkdir()
    out, info = gate_data_centers({}, {}, batch, permits_dir=tmp_path / "none")
    assert out == [] and info[0].startswith("warning:")


def test_dc_site_without_an_entry_fails(tmp_path):
    out, _ = run_dc(tmp_path, {})
    assert len(out) == 1 and "no entry" in out[0][1]


def test_dc_bad_decision_and_below_threshold(tmp_path):
    out, _ = run_dc(tmp_path, {"S1": {"decision": "skip"}})
    assert "not one of" in out[0][1]
    out, _ = run_dc(tmp_path, {"S1": {"decision": "below_threshold"}})
    assert "cannot be below_threshold" in out[0][1]


def test_dc_add_needs_a_real_record(tmp_path):
    out, _ = run_dc(tmp_path, {"S1": {"decision": "add", "record_id": "x:1"}})
    assert out and "record_id" in out[0][1]
    lanes = {"newplants": [{"record_id": "x:1"}]}
    out, _ = run_dc(tmp_path, {"S1": {"decision": "add", "record_id": "x:1"}}, lanes=lanes)
    assert out == []


def test_dc_unsized_site_may_close_with_a_number_or_a_search(tmp_path):
    unk = dict(SITE, site_id="U1", verdict="unknown_capacity", summed_nameplate_mw=None)
    nod = dict(SITE, site_id="N1", verdict="no_documents", summed_nameplate_mw=None)
    out, _ = run_dc(tmp_path, {"U1": {"decision": "below_threshold"}}, sites=(unk,))
    assert out and "summed_nameplate_mw" in out[0][1]
    out, _ = run_dc(tmp_path, {"U1": {"decision": "below_threshold", "summed_nameplate_mw": 31.5,
                                      "note": "x"}}, sites=(unk,))
    assert out == []
    out, _ = run_dc(tmp_path, {"N1": {"decision": "nothing_found", "note": "short"}}, sites=(nod,))
    assert out and "note" in out[0][1]
    out, _ = run_dc(tmp_path, {"N1": {"decision": "nothing_found", "note": "Searched the state permit "
                                      "portal and the county for the site; nothing lists a generator."}},
                    sites=(nod,))
    assert out == []
    out, _ = run_dc(tmp_path, {"N1": {"decision": "not_data_center", "note": "The permit is for a "
                                      "warehouse with one fire pump; the name match was wrong."}}, sites=(nod,))
    assert out == []
    # a fleet the harvester summed at the threshold is still never closed that way
    out, _ = run_dc(tmp_path, {"S1": {"decision": "nothing_found", "note": "a long enough note that "
                                      "says what was searched and what it showed"}})
    assert out and "cannot be nothing_found" in out[0][1]


def test_dc_already_in_gem_needs_a_plant_id(tmp_path):
    out, _ = run_dc(tmp_path, {"S1": {"decision": "already_in_gem"}})
    assert out and "plant_id" in out[0][1]
    out, _ = run_dc(tmp_path, {"S1": {"decision": "already_in_gem", "plant_id": "L1"}})
    assert out == []


# ---- optional validation items ----

def test_coal_plant_item_is_optional_but_must_be_answered_in_words(tmp_path):
    csv_path = tmp_path / "export.csv"
    csv_path.write_text("GEM location ID,Fuel\nL1,coal\nL1,gas\n", encoding="utf-8")
    vp = report(tmp_path, [{"kind": "fix", "plant_id": "L1", "unit_id": "G2", "item": "Status"}])
    base = [qa("L1", "G1"), qa("L2", None)]
    # G2 is not covered by a check 7 record
    out, info = gate_validation(index(), answered(*base), vp, now=NOW, unfiltered_csv=csv_path)
    assert out and "optional under the manual" in out[0][1]
    note = dict(qa("L1", "G1", checks=[12]), researcher_notes="This error is optional under the manual.")
    out, info = gate_validation(index(), answered(note, *base[1:]), vp, now=NOW,
                                unfiltered_csv=csv_path)
    assert out == []
    assert any("unanswered but optional" in i and "(0 " not in i for i in info)


def test_non_optional_item_still_fails(tmp_path):
    vp = report(tmp_path, [{"kind": "fix", "plant_id": "L1", "unit_id": "G2", "item": "Status"}])
    out, _ = gate_validation(index(), answered(qa("L1", "G1"), qa("L2", None)), vp, now=NOW,
                             unfiltered_csv=tmp_path / "none.csv")
    assert out and "no record with check 7" in out[0][1]


def test_coal_conversion_unit_is_optional(tmp_path):
    vp = report(tmp_path, [{"kind": "fix", "plant_id": "L1", "unit_id": "G2", "item": "Fuel"}])
    export = {"G2": {"Conversion/replacement?": "conversion",
                     "Conversion from/replacement of (fuel)": "coal"}}
    out, _ = gate_validation(index(), answered(qa("L1", "G1"), qa("L2", None)), vp, now=NOW,
                             export=export, unfiltered_csv=tmp_path / "none.csv")
    assert out and "optional under the manual" in out[0][1]


# ---- worklist ----

def test_priority_ladder():
    assert wl.priority_for("construction", "", 2026) == 1
    assert wl.priority_for("shelved - inferred 2 y", "", 2026) == 2
    assert wl.priority_for("operating", "2026", 2026) == 3
    assert wl.priority_for("operating", "2031", 2026) == 4
    assert wl.priority_for("mothballed", "", 2026) == 5
    assert wl.priority_for("retired", "", 2026) == 9
    assert wl.priority_for("cancelled", "", 2026) == 9


def test_evidence_date_and_inferred_flag():
    assert wl.evidence_date("Year: 2022, Month: 3, Day: 5", "") == datetime.date(2022, 3, 5)
    assert wl.evidence_date("Year: 2022", "") == datetime.date(2022, 12, 31)
    assert wl.evidence_date("", "") is None
    as_of = datetime.date(2026, 10, 27)
    assert wl.inferred_flag("construction", datetime.date(2024, 1, 1), as_of).startswith("shelved")
    assert wl.inferred_flag("announced", datetime.date(2022, 1, 1), as_of).startswith("cancelled")
    assert wl.inferred_flag("announced", datetime.date(2026, 1, 1), as_of) == ""
    assert wl.inferred_flag("shelved", datetime.date(2010, 1, 1), as_of) == ""
    assert wl.inferred_flag("operating", datetime.date(2010, 1, 1), as_of) == ""


# ---- location place fields ----

def test_blank_city_on_an_exact_plant_makes_a_place_task():
    from test_location_candidates import row
    r = row("L1", "G1", "Exact plant", acc="exact")
    r["City"] = ""
    res = lc.select_candidates([r], bsb.make_scope(state="Maryland"), lambda p: [])
    assert [t["plant_id"] for t in res["tasks"]] == ["L1"]
    t = res["tasks"][0]
    assert t.get("coordinates_locked") is True
    assert "City" in t["fields"] and 26 in t["checks"]


def test_blank_local_area_alone_does_not_select_a_plant():
    from test_location_candidates import row
    r = row("L1", "G1", "Exact plant", acc="exact")
    res = lc.select_candidates([r], bsb.make_scope(state="Maryland"), lambda p: [])
    assert res["tasks"] == []


# ---- chase, orphans, concern types ----

def test_backup_only_counts_only_without_a_mw_figure():
    assert chase_hits("Data center, backup generators only.")
    assert chase_hits("Data center, backup generators only, 120 MW summed.") == []


def test_inferred_status_needs_a_status_data_source():
    rec = {"record_id": "r1", "fields": {"Status": "shelved"}, "refs": {}, "inferred": True}
    out = gate_orphans({"updates": [rec]})
    assert out and "Status Data Source" in out[0][1]
    rec["refs"] = {"Status Data Source": ["https://a.example.com/x"]}
    assert gate_orphans({"updates": [rec]}) == []


def test_notes_cleanup_concern_type_passes():
    assert gate_concern_types({"qa": [{"record_id": "q", "concern_type": "notes_cleanup"}]}) == []


# ---- qc_checks unit fields ----

def test_run_staged_checks_unit_fields(tmp_path):
    import inspect
    assert "units" in inspect.getsource(qc_checks.run_staged)


def test_notes_cleanup_is_in_the_concern_vocabulary():
    from review_app.checklist import CONCERN_VOCAB, normalize_concern_type
    assert "notes_cleanup" in CONCERN_VOCAB
    assert normalize_concern_type("notes_cleanup") == "notes_cleanup"
    assert normalize_concern_type("Notes cleanup: the 2019 line is outdated") == "notes_cleanup"


def test_dc_at_threshold_site_may_close_only_with_an_audited_hand_count(tmp_path):
    permit = "https://webapps.illinois.gov/EPA/DocumentExplorer/Documents/Index/1?dwdocid=2"
    note = ("Read the final permit of May 29, 2025. It lists one 1,000 kWe, twelve 2,250 kWe and five "
            "2,500 kWe diesel emergency generator sets, 40.5 MW in all, under the 50 MW threshold.")
    fleet = [{"count": 1, "mw_each": 1.0}, {"count": 12, "mw_each": 2.25}, {"count": 5, "mw_each": 2.5}]
    good = {"decision": "below_threshold", "summed_nameplate_mw": 40.5, "fleet": fleet, "source": permit, "note": note}
    out, info = run_dc(tmp_path, {"S1": good})
    assert out == [] and any("overruled by a hand count" in i for i in info)
    # the lines must add up to the number given, the number must be under the threshold,
    # and the answer must name the permit and say what was read
    out, _ = run_dc(tmp_path, {"S1": dict(good, summed_nameplate_mw=41.0)})
    assert out and "cannot be below_threshold" in out[0][1]
    out, _ = run_dc(tmp_path, {"S1": dict(good, fleet=fleet + [{"count": 4, "mw_each": 3.0}], summed_nameplate_mw=52.5)})
    assert out and "cannot be below_threshold" in out[0][1]
    out, _ = run_dc(tmp_path, {"S1": dict(good, source="")})
    assert out and "cannot be below_threshold" in out[0][1]
    out, _ = run_dc(tmp_path, {"S1": dict(good, note="short")})
    assert out and "cannot be below_threshold" in out[0][1]

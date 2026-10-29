"""The add threshold and the watch list (Baird 2026-10-23): a watch item for a
project GEM lacks names one of schema_constants.WATCH_CASES, state_gate's
advisory gate `watch-case` flags one that names none or whose own values
contradict the case, assemble_state marks the leads it demotes itself, and the
scope-wide brief opens with the add rule."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from assemble_state import Assembler  # noqa: E402
from build_state_brief import render_scope_brief  # noqa: E402
from schema_constants import WATCH_CASES  # noqa: E402
from state_gate import gate_watch_case, scope_threshold_mw  # noqa: E402

US = {"mode": "update", "where": {"kind": "state", "name": "Kansas", "slug": "kansas",
                                  "country": "United States", "postal": "ks"}, "plants": []}
DE = {"mode": "update", "where": {"kind": "country", "name": "Germany", "slug": "germany",
                                  "country": "Germany", "postal": ""}, "plants": []}


def watch(**over):
    r = {"record_id": "us-ks:plant:monitor-1", "gem_plant_id": "", "plant_name": "Holcomb CT",
         "monitor_kind": "new_to_tracker", "monitor_reason": "Queue entry only.",
         "recheck_by": "2027-01", "capacity_mw": 600, "checks": [],
         "refs": {"links": ["https://opsportal.spp.org/Studies/GIActive"]},
         "verifications": [{"url": "https://opsportal.spp.org/Studies/GIActive", "ok": True,
                            "contains_value": True}]}
    r.update(over)
    return r


def offenders(*recs, index=US):
    return [reason for _, reason in gate_watch_case({"monitor": list(recs)}, index)]


def test_thresholds_follow_the_country():
    assert scope_threshold_mw(US) == 50
    assert scope_threshold_mw(DE) == 20


def test_every_case_is_described_in_plain_words():
    assert set(WATCH_CASES) == {"no_generation", "under_threshold", "drive_or_storage",
                                "duplicate_check", "not_committed",
                                "other_scope", "unverified"}
    assert all(len(v) > 20 for v in WATCH_CASES.values())


def test_new_to_tracker_item_without_a_case_is_flagged():
    out = offenders(watch())
    assert len(out) == 1 and "names no watch_case" in out[0]


def test_named_case_passes():
    assert offenders(watch(watch_case="drive_or_storage")) == []
    assert offenders(watch(watch_case="other_scope")) == []


def test_existing_plant_items_need_no_case():
    assert offenders(watch(monitor_kind="existing_plant", gem_plant_id="L1")) == []


def test_lead_needs_a_case_too():
    out = offenders(watch(monitor_kind="existing_plant", gem_plant_id="L1", lead_for="newunits"))
    assert len(out) == 1


def test_under_threshold_with_capacity_at_the_bar_is_an_add():
    out = offenders(watch(watch_case="under_threshold", capacity_mw=600))
    assert len(out) == 1 and "reaches the 50 MW threshold" in out[0]
    assert offenders(watch(watch_case="under_threshold", capacity_mw=40)) == []
    assert offenders(watch(watch_case="under_threshold", capacity_mw=None)) == []
    # the EU and UK bar is 20 MW
    assert len(offenders(watch(watch_case="under_threshold", capacity_mw=40), index=DE)) == 1


def test_unverified_with_a_passing_check_is_an_add():
    out = offenders(watch(watch_case="unverified"))
    assert len(out) == 1 and "passed the verifier" in out[0]
    assert offenders(watch(watch_case="unverified", verifications=[])) == []
    assert offenders(watch(watch_case="unverified",
                           verifications=[{"url": "x", "ok": False}])) == []


def test_backup_fleet_without_a_summed_figure_is_flagged():
    prose = "Data center with emergency diesel generators on site."
    out = offenders(watch(watch_case="other_scope", monitor_reason=prose))
    assert len(out) == 1
    ok = prose + " Summed nameplate is 120 MW."
    assert offenders(watch(watch_case="other_scope", monitor_reason=ok)) == []


def test_assembler_marks_a_demoted_lead_unverified():
    lane, item = Assembler.confirmed_or_lead("newplants", {"plant_name": "X", "fields": {},
                                                           "note": "thin"})
    assert lane == "monitor" and item["lead_for"] == "newplants"
    assert item["watch_case"] == "unverified"
    lane, item = Assembler.confirmed_or_lead(
        "newplants", {"plant_name": "X", "fields": {"Capacity (MW)": "600"},
                      "refs": {"Capacity Data Source": ["https://a"]},
                      "verifications": [{"url": "https://a", "ok": True}]})
    assert lane == "newplants" and "watch_case" not in item


def test_scope_brief_opens_with_the_add_rule():
    text = render_scope_brief([], None, "us-ks")
    assert text.index("When a project GEM lacks is added") < text.index("EIA plants missing")
    for case in WATCH_CASES:
        assert case in text
    assert "50 MW" in text and "announced" in text and "pre-construction" in text
    assert "20 MW" in render_scope_brief([], None, "germany", threshold_mw=20)


def test_unverified_with_a_link_that_only_confirms_the_request_passes():
    # a PJM queue page names the request and developer but not the size or fuel (Baird 2026-10-27)
    v = [{"url": "https://www.pjm.com/m/ProjectTransition/SISReportDetails?queueNumber=C01-2036", "ok": True,
          "contains_value": False, "name_found": True}]
    assert offenders(watch(watch_case="unverified", verifications=v)) == []
    assert len(offenders(watch(watch_case="unverified"))) == 1

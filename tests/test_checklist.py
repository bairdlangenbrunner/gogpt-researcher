"""Tests for review_app/checklist.py: the nine groups, the row table and tag()."""
import datetime
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from review_app import checklist as ck
from review_app.checklist import normalize_concern_type as nct  # noqa: E402

TODAY = datetime.date(2026, 10, 7)


def upd(col, value, current, verdict=None, **extra):
    r = {"record_id": f"L1:G1:{col.lower().replace(' ', '-')}", "gem_plant_id": "L1",
         "gem_unit_id": "G1", "fields": {col: value}, "current": {col: current},
         "verdict": verdict or ("fill" if current == "" else "change")}
    r.update(extra)
    return r


def t(rec, lane="updates", unit_row=None, us=True):
    return ck.tag(rec, lane, unit_row=unit_row, us=us, today=TODAY)


# ---- tables ----------------------------------------------------------------------------

def test_groups_cover_every_ticked_row_once_or_twice():
    rows = [r for g in ck.GROUPS for r in g["rows"]]
    assert set(rows) == set(ck.ROWS) - {42, 45, 46}       # 42, 45, 46 are optional rows no record ticks
    dup = {r for r in rows if rows.count(r) > 1}
    assert dup == {19, 34}                                 # owner (blank vs change), IRPs tab (US vs close-out)
    assert ck.group_of_row(19) == 2 and ck.group_of_row(34) == 7


def test_row_labels_present():
    for n, (label, question) in ck.ROWS.items():
        assert label and question, n
    assert ck.row_label(56).startswith('"No tracker found"')
    assert ck.row_question(7).startswith("Have you checked and fixed")


def test_groups_for_country_drops_us_group():
    assert [g["id"] for g in ck.groups_for(us=False)] == [1, 2, 3, 4, 5, 6, 8, 9]
    assert [g["id"] for g in ck.groups_for(us=True)] == list(range(1, 10))


# ---- updates lane -----------------------------------------------------------------------

def test_fill_blank_start_year_on_operating_unit():
    tag = t(upd("Start year", "1996", ""), unit_row={"Status": "operating"})
    assert tag == {"group": 2, "checks": [9, 18], "group_label": "Blanks and unknowns"}


def test_fill_unknown_start_year_on_construction_unit():
    tag = t(upd("Start year", "2027", "unknown"), unit_row={"Status": "construction"})
    assert tag["group"] == 2 and tag["checks"] == [18]


def test_start_year_change_on_in_development_unit_is_row_10():
    tag = t(upd("Start year", "2028", "2027"), unit_row={"Status": "construction"})
    assert tag["group"] == 3 and tag["checks"] == [10]


def test_start_year_deletion_on_shelved_unit():
    tag = t(upd("Start year", "", "2024", verdict="change", delete=True),
            unit_row={"Status": "shelved"})
    assert tag["group"] == 3 and tag["checks"] == [20]


def test_status_construction_to_operating():
    tag = t(upd("Status", "operating", "construction"), unit_row={"Status": "construction"})
    assert tag["group"] == 3 and tag["checks"] == [10, 49]


def test_status_operating_to_retired():
    tag = t(upd("Status", "retired", "operating"), unit_row={"Status": "operating"})
    assert tag["group"] == 3 and tag["checks"] == [50]


def test_status_to_inferred_cancelled():
    tag = t(upd("Status", "cancelled - inferred 4 y", "shelved - inferred 2 y"),
            unit_row={"Status": "shelved - inferred 2 y"})
    assert tag["group"] == 3 and tag["checks"] == [20, 24, 50]


def test_status_reverified_in_development_counts_row_10():
    tag = t(upd("Status", "construction", "construction", verdict="match", reverified=True),
            unit_row={"Status": "construction"})
    assert tag["group"] == 3 and tag["checks"] == [10]
    tag = t(upd("Status", "operating", "operating", verdict="match", reverified=True),
            unit_row={"Status": "operating"})
    assert tag["group"] == 3 and tag["checks"] == []


def test_latest_activity_on_inferred_status():
    tag = t(upd("Latest Activity", "Year: 2024, Month: 3, Day: 1", ""),
            unit_row={"Status": "shelved - inferred 2 y"})
    assert tag["group"] == 3 and tag["checks"] == [24]
    tag = t(upd("Latest Activity", "Year: 2024, Month: 3, Day: 1", ""),
            unit_row={"Status": "pre-construction"})
    assert tag["group"] == 3 and tag["checks"] == [10]


def test_planned_retire_in_the_past_adds_row_23():
    tag = t(upd("Planned retire", "2027", "2025"), unit_row={"Status": "operating"})
    assert tag["group"] == 3 and tag["checks"] == [21, 23]
    tag = t(upd("Planned retire", "2035", "2035", verdict="match", reverified=True))
    assert tag["checks"] == [21]


def test_retired_year_fill_on_retired_unit():
    tag = t(upd("Retired year", "2025", ""), unit_row={"Status": "retired"})
    assert tag["group"] == 2 and tag["checks"] == [22]


def test_owner_fill_is_blanks_and_owner_change_is_owners():
    tag = t(upd("Owner(s)", "Acme [100%]", ""), unit_row={"Status": "operating"})
    assert tag["group"] == 2 and tag["checks"] == [8, 19]
    tag = t(upd("Owner(s)", "Acme [100%]", "Beta [100%]"), unit_row={"Status": "operating"})
    assert tag["group"] == 6 and tag["checks"] == [19, 43]
    tag = t(upd("Owner(s)", "Acme [100%]", "Beta [100%]"), unit_row={"Status": "construction"})
    assert tag["group"] == 6 and tag["checks"] == [19]


def test_capacity_zero_counts_row_16_and_change_does_not():
    assert t(upd("Capacity (MW)", "55", "0"))["checks"] == [16]
    assert t(upd("Capacity (MW)", "55", ""))["checks"] == [16]
    tag = t(upd("Capacity (MW)", "60", "55"), unit_row={"Status": "operating"})
    assert tag["group"] == 2 and tag["checks"] == []


def test_technology_unknown_and_conversion():
    tag = t(upd("Turbine/Engine Technology", "combined cycle", "unknown"),
            unit_row={"Status": "operating"})
    assert tag["group"] == 2 and tag["checks"] == [8, 17]
    tag = t(upd("Turbine/Engine Technology", "combined cycle", "subcritical"),
            unit_row={"Status": "operating", "Conversion/replacement?": "conversion"})
    assert tag["group"] == 4 and tag["checks"] == [13]
    tag = t(upd("Turbine/Engine Technology", "steam turbine", "combined cycle"),
            unit_row={"Status": "operating", "Conversion/replacement?": "conversion"})
    assert tag["checks"] == [14]


def test_equipment_is_group_5_with_row_15_only_in_development():
    assert t(upd("Equipment Manufacturer/Model", "GE 7HA.02", ""),
             unit_row={"Status": "construction"}) == {"group": 5, "checks": [15],
                                                       "group_label": "Turbine make and model"}
    assert t(upd("Equipment Manufacturer/Model", "GE 7HA.02", ""),
             unit_row={"Status": "operating"})["checks"] == []


def test_unit_name_timepoint_is_a_conversion_row():
    assert t(upd("Unit name", "Unit 1 timepoint 2", "Unit 1"))["group"] == 4
    assert t(upd("Unit name", "Unit 1 timepoint 2", "Unit 1"))["checks"] == [12]
    assert t(upd("Unit name", "CT1", ""))["checks"] == [11]


def test_location_and_city():
    assert t(upd("Latitude", "38.7", ""))["checks"] == [8, 25]
    assert t(upd("Location accuracy", "exact", "approximate"))["checks"] == [25, 42]
    assert t(upd("City", "Baltimore", ""))["checks"] == [26]
    assert t(upd("City", "Baltimore", "Balto"))["group"] == 2


def test_us_only_columns_outside_the_us_fall_to_other():
    assert t(upd("Other IDs (location)", "EIA 1234", ""))["group"] == 7
    assert t(upd("Other IDs (location)", "EIA 1234", ""))["checks"] == [38]
    tag = t(upd("Other IDs (location)", "EIA 1234", ""), us=False)
    assert tag["group"] == "other" and tag["checks"] == []
    assert t(upd("Captive non-industry use", "data center", ""))["checks"] == [39]
    assert t(upd("Captive non-industry use", "data center", ""), us=False)["group"] == 2


def test_unmapped_column_falls_back_by_kind():
    assert t(upd("Notes", "x", ""))["group"] == 2
    assert t(upd("Notes", "x", "y"))["group"] == "other"
    assert t(upd("Employment Notes", "x", "y"))["group"] == "other"
    assert t(upd("Employment Notes", "x", ""))["group"] == 2


def test_plant_level_record_tags_from_its_field():
    rec = upd("Owner(s)", "Acme [100%]", "", applies_to_all_units=True,
              sibling_unit_ids=["G2"], sibling_current={"G2": ""})
    assert t(rec, unit_row={"Status": "operating"})["group"] == 2


# ---- provenance -------------------------------------------------------------------------

def test_provenance_wins_the_group_and_keeps_table_rows():
    rec = upd("Capacity (MW)", "60", "55", checks=[7])
    tag = t(rec, unit_row={"Status": "operating"})
    assert tag["group"] == 1 and tag["checks"] == [7]
    rec = upd("Start year", "1996", "", checks=[18])
    tag = t(rec, unit_row={"Status": "operating"})
    assert tag["group"] == 2 and tag["checks"] == [9, 18]
    rec = upd("Owner(s)", "Acme [100%]", "Beta [100%]", checks=[19])
    assert t(rec, unit_row={"Status": "operating"})["group"] == 6


def test_irp_record_lands_in_group_7():
    rec = upd("Status", "pre-construction", "announced", irp=True)
    tag = t(rec, unit_row={"Status": "announced"})
    assert tag["group"] == 7 and 37 in tag["checks"] and 50 in tag["checks"]
    tag = t(rec, unit_row={"Status": "announced"}, us=False)
    assert tag["group"] == 3 and 37 not in tag["checks"]


# ---- other lanes ------------------------------------------------------------------------

def test_new_plants_and_units():
    assert t({"plant_name": "Severn barge station", "fields": {}}, "newplants") == {
        "group": 8, "checks": [51], "group_label": "New to the tracker"}
    tag = t({"plant_name": "Calcasieu Pass LNG terminal power station"}, "newplants")
    assert tag["checks"] == [6, 44]
    tag = t({"plant_name": "Hyperion data center plant", "researcher_notes": "a 300 MW data center"},
            "newunits")
    assert tag["group"] == 8 and tag["checks"] == [39, 51]
    tag = t({"plant_name": "Hyperion plant", "researcher_notes": "a 300 MW data center"},
            "newunits", us=False)
    assert tag["checks"] == [51]


def test_entity_lane():
    assert t({"entity_name": "Acme Power LLC"}, "entity") == {
        "group": 6, "checks": [19], "group_label": "Owners and entities"}


def test_monitor_new_to_tracker():
    rec = {"gem_plant_id": "", "plant_name": "Chesapeake repowering", "monitor_reason": "no permit filed",
           "recheck_by": "2027-01"}
    assert t(rec, "monitor") == {"group": 8, "checks": [51], "group_label": "New to the tracker"}
    rec["monitor_kind"] = "new_to_tracker"
    assert t(rec, "monitor")["group"] == 8


def test_monitor_existing_plant_by_text():
    base = {"gem_plant_id": "L1", "plant_name": "Brandywine", "recheck_by": "2027-01",
            "monitor_kind": "existing_plant"}
    dc = dict(base, monitor_reason="Owner plans a data center behind the meter.")
    assert t(dc, "monitor") == {"group": 7, "checks": [39], "group_label": "IDs, IRPs and data centers"}
    assert t(dc, "monitor", us=False)["group"] == 3        # no group 7 outside the US
    exp = dict(base, monitor_reason="A second phase would add a new CC block.")
    assert t(exp, "monitor")["group"] == 8 and t(exp, "monitor")["checks"] == [51]
    quiet = dict(base, monitor_reason="Developer says financing closes next year.")
    assert t(quiet, "monitor", unit_row={"Status": "pre-construction"}) == {
        "group": 3, "checks": [10], "group_label": "Status and timeline"}
    assert t(quiet, "monitor", unit_row={"Status": "operating"})["checks"] == []


def test_monitor_without_kind_uses_plant_id():
    rec = {"gem_plant_id": "L1", "monitor_reason": "Repowering talk, nothing filed.", "recheck_by": "2027-01"}
    assert t(rec, "monitor", unit_row={"Status": "operating"})["group"] == 8


def test_qa_by_concern_type():
    assert t({"concern_type": "duplicate"}, "qa")["group"] == 8
    assert t({"concern_type": "identity"}, "qa") == {"group": 2, "checks": [11],
                                                     "group_label": "Blanks and unknowns"}
    # an identity question about whether two records are one thing is a record question, not a blank name
    assert t({"concern_type": "identity", "recommendation": "Confirm the two projects are meant to be separate records."}, "qa")["group"] == 8
    assert t({"concern_type": "identity", "recommendation": "Check unit naming against the regulator's list."}, "qa")["group"] == 2
    assert t({"concern_type": "conversion-link"}, "qa")["checks"] == [12, 13]
    assert t({"concern_type": "attribution"}, "qa")["group"] == 6
    assert t({"concern_type": "validation"}, "qa")["group"] == 1
    assert t({"concern_type": "other"}, "qa")["group"] == "other"
    assert t({}, "qa")["group"] == "other"


def test_qa_by_column_name():
    tag = t({"concern_type": "Owner(s)", "current": {"Owner(s)": ""}}, "qa", unit_row={"Status": "operating"})
    assert tag["group"] == 2 and tag["checks"] == [8, 19]
    tag = t({"concern_type": "Owner(s)"}, "qa", unit_row={"Status": "operating", "Owner(s)": "Beta"})
    assert tag["group"] == 6 and tag["checks"] == [19, 43]
    tag = t({"concern_type": "Capacity (MW)", "proposed_value": {"Capacity (MW)": "60"}}, "qa",
            unit_row={"Status": "operating", "Capacity (MW)": "55"})
    assert tag["group"] == 2 and tag["checks"] == []
    tag = t({"concern_type": "Status", "proposed_value": {"Status": "retired"}}, "qa",
            unit_row={"Status": "operating"})
    assert tag["group"] == 3 and tag["checks"] == [50]
    tag = t({"concern_type": "Other IDs (unit)"}, "qa")
    assert tag["group"] == 7 and tag["checks"] == [38]


def test_qa_with_validation_provenance():
    tag = t({"concern_type": "Capacity (MW)", "checks": [7]}, "qa", unit_row={"Capacity (MW)": "55"})
    assert tag["group"] == 1 and tag["checks"] == [7]


# ---- summary ----------------------------------------------------------------------------

def test_summarize_counts_groups_and_rows():
    tags = [t(upd("Start year", "1996", ""), unit_row={"Status": "operating"}),
            t(upd("Status", "operating", "construction"), unit_row={"Status": "construction"}),
            t(upd("Notes", "x", "y")),
            t({"entity_name": "Acme"}, "entity")]
    s = ck.summarize(tags)
    by = {g["id"]: g for g in s}
    assert [g["id"] for g in s] == [1, 2, 3, 4, 5, 6, 7, 8, 9, "other"]
    assert by[2]["count"] == 1 and by[3]["count"] == 1 and by[6]["count"] == 1 and by["other"]["count"] == 1
    rows = {r["row"]: r for r in by[2]["rows"]}
    assert rows[9]["count"] == 1 and rows[18]["count"] == 1
    assert rows[19]["count"] == 1          # row counts cross groups: the entity record ticks 19 too
    assert {r["row"]: r["count"] for r in by[3]["rows"]}[49] == 1
    assert by[9]["panel"] is True and by[9]["count"] == 0
    opt = {r["row"]: r["optional"] for r in by[6]["rows"]}
    assert opt[43] is True and opt[19] is False
    # no "other" bucket when nothing landed there, and no group 7 outside the US
    s2 = ck.summarize(tags[:2], us=False)
    assert [g["id"] for g in s2] == [1, 2, 3, 4, 5, 6, 8, 9]


# ---- normalize_concern_type -----------------------------------------------------------

@pytest.mark.parametrize("raw, want", [
    ("Capacity (MW)", "Capacity (MW)"),          # already a column
    ("duplicate", "duplicate"),                  # already a kind
    ("capacity", "Capacity (MW)"),
    ("uprate_request", "Capacity (MW)"),
    ("register_mismatch", "Capacity (MW)"),
    ("owner", "Owner(s)"),
    ("ownership", "Owner(s)"),
    ("status", "Status"),
    ("permit", "Status"),
    ("start_year", "Start year"),
    ("location", "location"),
    ("source", "source"),
    ("dead link", "source"),
    ("naming", "identity"),
    ("missing unit", "existence"),
    ("unit grouping", "scope"),
    ("data center", "Captive non-industry use"),
    ("", "other"),
    ("something odd", "other"),
])
def test_normalize_concern_type_words(raw, want):
    assert nct(raw) == want


def test_normalize_generic_word_takes_the_proposed_column():
    rec = {"proposed_value": {"Start year": "2019"}}
    assert nct("wrong_value", rec) == "Start year"
    assert nct("conflict", rec) == "Start year"
    assert nct("other", rec) == "Start year"
    # two proposed columns: no single column to take
    assert nct("conflict", {"proposed_value": {"Start year": "2019", "Status": "x"}}) == "other"


def test_vocabulary_covers_every_kind_and_column():
    assert set(ck.CONCERN_KINDS) <= ck.CONCERN_VOCAB
    assert set(ck.CONCERN_COLUMNS) <= ck.CONCERN_VOCAB
    for v in ck.CONCERN_VOCAB:
        assert nct(v) == v


def test_tag_normalizes_free_text_concern_types():
    rec = {"record_id": "L1:G1:qa-capacity-1", "concern_type": "capacity",
           "proposed_value": {"Capacity (MW)": "40"}, "current": {"Capacity (MW)": ""}}
    out = t(rec, lane="qa")
    assert out["group"] == 2 and 16 in out["checks"]


def test_name_key():
    assert ck.name_key("Gowanus & Narrows repowering (Alpha)") == "gowanusnarrowsrepoweringalpha"

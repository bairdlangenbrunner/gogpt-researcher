"""Offline tests for scripts/data_center_fleets.py (no network, no database)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import data_center_fleets as dcf  # noqa: E402

FIX = Path(__file__).parent / "fixtures" / "data_center_fleets"


def one(units):
    assert len(units) == 1, units
    return units[0]


def test_count_word_then_rating():
    u = one(dcf.parse_generator_lines("The site has forty-eight (48) 3,000 kW diesel-fired emergency generators."))
    assert u["count"] == 48 and u["mw_each"] == 3.0 and u["fuel"] == "diesel"
    assert dcf.sum_fleet([u]) == 144.0


def test_range_each():
    u = one(dcf.parse_generator_lines("Emergency Generators EU-001 through EU-032: Caterpillar 3516C, 2,500 kWe each"))
    assert u["count"] == 32 and u["mw_each"] == 2.5


def test_n_times_mw_natural_gas():
    u = one(dcf.parse_generator_lines("The plan is 12 x 2.5 MW natural gas-fired engine generator sets."))
    assert u["count"] == 12 and u["mw_each"] == 2.5 and u["fuel"] == "natural gas"
    assert dcf.sum_fleet([u]) == 30.0


def test_horsepower_only_is_unknown():
    units = dcf.parse_generator_lines("Four (4) 4,332 HP diesel-fired emergency generator engines.")
    assert units and all(u["mw_each"] is None for u in units)
    assert dcf.sum_fleet(units) is None
    assert dcf.classify(None, 50, True) == "unknown_capacity"


def test_mechanical_kw_is_not_electrical():
    units = dcf.parse_generator_lines("Two (2) 4,332 HP (3,230 mechanical kilowatts) diesel generator engines.")
    assert dcf.sum_fleet(units) is None


def test_stated_total():
    u = one(dcf.parse_generator_lines("installation of emergency back-up generators with a total power capacity of approximately 250 Megawatts and tanks"))
    assert u["mw_each"] == 250.0 and u.get("total_only")


def test_heat_input_only_counts_engines():
    u = one(dcf.parse_generator_lines("Fifteen diesel-powered emergency generators, each with a maximum heat input rating of 18.76 MMBtu/hr"))
    assert u["count"] == 15 and u["mw_each"] is None


def test_classify():
    assert dcf.classify(None, 50, False) == "no_generators"
    assert dcf.classify(49.9, 50, True) == "below_threshold"
    assert dcf.classify(50.0, 50, True) == "at_threshold"
    assert dcf.classify(20.0, 20, True) == "at_threshold"
    assert dcf.classify(30.0, 50, True, incomplete=True) == "unknown_capacity"
    assert dcf.classify(80.0, 50, True, incomplete=True) == "at_threshold"
    assert dcf.classify(None, 50, False, has_documents=False) == "no_documents"


def test_site_without_documents_is_no_documents():
    site = {"name": "Nimbus Data Center", "operator": "Nimbus", "address": "", "city": "Ames",
            "permits": [], "docs": [], "source": "lead", "lead_notes": "named in a county notice"}
    rec = dcf.analyze_site(site, {}, 50, 12, {}, offline=True)
    assert rec["verdict"] == "no_documents"
    assert "No permit document is on record" in rec["source_notes"]
    assert "Lead note: named in a county notice" in rec["source_notes"]


def test_threshold_eu():
    assert dcf.threshold_for({"country": "Germany"}) == 20.0
    assert dcf.threshold_for({"country": "United Kingdom"}) == 20.0
    assert dcf.threshold_for({"country": "United States"}) == 50.0


def test_genset_table_groups_and_no_double_count():
    r = dcf.parse_genset_specs((FIX / "ms_genset_table.txt").read_text())
    assert len(r["units"]) == 4
    assert round(sum(u["mw_each"] for u in r["units"]), 3) == 2.75 * 3 + 0.75
    labels = list(r["groups"])
    assert labels == ["Building 1", "Building 2"]
    assert r["groups"]["Building 1"]["engines"] == 3


def test_extract_fleet_prefers_unit_lines_and_builds_phases():
    f = dcf.extract_fleet((FIX / "ms_genset_table.txt").read_text())
    assert f["method"] == "numbered generator lines"
    assert dcf.sum_fleet(f["units"]) == 9.0  # 3 x 2.75 + 0.75
    assert [p["label"] for p in f["phases"]] == ["Building 1", "Building 2"]


def test_inventory_form_label_beats_design_capacity():
    units = dcf.parse_inventory_form((FIX / "mi_inventory_form.txt").read_text())
    assert len(units) == 4
    assert units[2]["mw_each"] == 1.25 and "design capacity" in units[2]["note"]
    assert units[3]["mw_each"] is None and units[3]["heat_input_only"]
    assert dcf.sum_fleet(units) == 3 + 3 + 1.25
    assert dcf.classify(dcf.sum_fleet(units), 50, True, incomplete=True) == "unknown_capacity"


def test_eu_rows_skip_fire_pump():
    units = dcf.parse_eu_rows((FIX / "mi_pti_rows.txt").read_text())
    assert len(units) == 2 and dcf.sum_fleet(units) == 5.5
    assert units[0]["fuel"] == "diesel"


def test_match_gem_by_brand_and_city():
    plants = {"L1": {"id": "L1", "name": "Amazon Web Services Ridgeland Data Center power station", "city": "Ridgeland",
                     "operator": "Amazon Data Services", "rows": [{}]},
              "L2": {"id": "L2", "name": "Compass Meridian", "city": "Meridian", "operator": "Compass", "rows": [{}]}}
    site = {"name": "Amazon Data Services Inc, JAN200", "operator": "Amazon Data Services Inc", "city": "Ridgeland", "address": ""}
    assert dcf.match_gem(site, plants)["id"] == "L1"
    other = {"name": "Amazon Data Services Inc, JAN250", "operator": "Amazon Data Services", "city": "Clinton", "address": ""}
    assert dcf.match_gem(other, plants) is None


def test_city_from_address():
    assert dcf.city_from_address("1001 Industrial Park Drive Clinton, MS 39056") == "Clinton"
    assert dcf.city_from_address("10 Main St, Saline, MI 48176") == "Saline"


def test_candidate_detection():
    assert dcf.looks_like_data_center("Compass Datacenters JAN I, LLC")
    assert dcf.looks_like_data_center("Amazon Data Services Inc, JAN250 Site")
    assert dcf.looks_like_data_center("Acme Plastics", "NAICS 518210")
    assert not dcf.looks_like_data_center("Acme Plastics")


def test_site_ids_are_stable_and_unique():
    sites = [{"operator": "Amazon", "name": "a", "city": "Canton"}, {"operator": "Amazon", "name": "b", "city": "Canton"}]
    dcf.assign_site_ids(sites)
    assert sites[0]["site_id"] == "amazon-canton" and sites[1]["site_id"] == "amazon-canton-2"


def test_writes_only_under_work(tmp_path):
    try:
        dcf.write_outputs({"name": "X", "tag": "x"}, 50.0, [], [], tmp_path)
    except SystemExit as e:
        assert "outside work" in str(e)
    else:
        raise AssertionError("expected refusal")

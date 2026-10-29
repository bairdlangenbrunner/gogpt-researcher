"""The data center step of build_state_brief.py (--data-centers), the optional
validation items on coal plants, and the December rule wording."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import build_state_brief as bsb  # noqa: E402
import captive_lng  # noqa: E402

SITES = {"scope": "Mississippi", "tag": "us-ms", "generated": "2026-10-27", "threshold_mw": 50,
         "sites": [
             {"site_id": "amazon-ridgeland", "name": "Amazon Data Services Ridgeland", "operator": "Amazon",
              "city": "Ridgeland", "permit_numbers": ["1720-00099"], "permit_urls": ["https://x.example/p.pdf"],
              "engine_count": 100, "capacity_per_engine_mw": 2.5, "summed_nameplate_mw": 250.0, "fuel": "diesel",
              "phases": [{"label": "Bldg 1-4", "engines": 40, "mw": 100, "status_hint": "operating"}],
              "verdict": "at_threshold", "source_notes": "Sum of the generator list."},
             {"site_id": "unk", "name": "Unk Campus", "verdict": "unknown_capacity", "summed_nameplate_mw": None},
             {"site_id": "have", "name": "Have Campus", "gem_plant_id": "L1", "gem_plant_name": "Have Data Center power station",
              "summed_nameplate_mw": 80, "verdict": "in_gem"},
             {"site_id": "nodoc", "name": "Nodoc Campus", "verdict": "no_documents", "summed_nameplate_mw": None},
             {"site_id": "small", "name": "Small", "summed_nameplate_mw": 12, "verdict": "below_threshold"},
             {"site_id": "none", "name": "None", "verdict": "no_generators"}]}


def test_data_center_brief_and_plant_items(tmp_path):
    p = tmp_path / "_data_centers.json"
    p.write_text(json.dumps(SITES))
    data = bsb.load_data_centers(p)
    text = bsb.render_data_centers_brief(data)
    assert "amazon-ridgeland" in text and "250.0 MW summed" in text
    assert "data_centers.unk" in text and "capacity cell blank" in text
    assert "data_centers.have" in text and "Backup Power box" in text
    assert "data_centers.nodoc" in text and "No permit or filing is on record" in text
    assert "small" in text and "below the threshold at 12 MW" in text
    assert "no generators" in text
    assert "Never a watch item for being backup" in text
    items = bsb.data_center_plant_items(data)
    assert list(items) == ["L1"] and items["L1"][0][1]["checks"] == [39]


def test_missing_file_is_reported_not_fatal(tmp_path, capsys):
    assert bsb.load_data_centers(tmp_path / "nope.json") is None
    assert "not found" in capsys.readouterr().out


def test_scope_brief_has_no_data_center_hold():
    text = bsb.render_scope_brief([], None, "us-ms")
    assert "data_center_hold" not in text
    assert "Data Center power station" in text


def test_validation_optional_on_coal_plant_and_conversion(tmp_path):
    rows = [{"GEM unit ID": "G1", "Unit name": "1", "Conversion from/replacement of (fuel)": ""},
            {"GEM unit ID": "G2", "Unit name": "2", "Conversion from/replacement of (fuel)": "coal: bituminous"}]
    item = lambda uid: (uid, {"task": "Fix it.", "fields": [], "checks": [7], "section": "Other"})
    unit, plant = bsb.validation_tasks([item("G1"), item("G2")], rows)
    assert not unit["G1"][0][0].startswith("Optional")
    assert unit["G2"][0][0].startswith("Optional under the manual")
    unit, plant = bsb.validation_tasks([item("G1"), item(None)], rows, coal_plant=True)
    assert unit["G1"][0][0].startswith("Optional") and plant[0][0].startswith("Optional")
    f = tmp_path / "all.csv"
    f.write_text("GEM location ID,Fuel\nL1,coal: bituminous\nL2,fossil gas: natural gas\n")
    assert bsb.coal_plant_ids(f) == {"L1"}


def test_december_rule_wording():
    r = {"Status": "operating", "Planned retire": "2026", "Fuel": "fossil gas: natural gas",
         "Turbine/Engine Technology": "steam turbine", "Capacity (MW)": "10", "Start year": "2000",
         "Unit name": "1", "Latitude": "1", "Longitude": "1", "Location accuracy": "exact", "City": "x"}
    t = bsb.unit_tasks(r, year=2026, us=False)
    text = " ".join(x for x, _, _ in t)
    assert "Event Year 2027 and Source Year 2026" in text


def test_captive_data_center_block_convention():
    L = "\n".join(captive_lng.render_data_center({"name": "Iowa"}, {"data_center": [], "threshold_mw": 50}))
    assert "Data center power, gas or diesel, routine or backup" in L
    assert "data_center_hold" not in L and "not watch items" not in L
    assert "Never write a watch item because a fleet is backup power" in L

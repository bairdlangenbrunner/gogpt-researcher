"""gate add-basics: each add checked against the GEM web form's validation (Baird 2026-11-07)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import state_gate as sg  # noqa: E402

MS = [{"status": "announced", "year": 2026, "period": "April", "sources": ["https://a.example/q"], "note": "filed"}]


def plant(name="Test Hub power station", **pf):
    fields = {"State/Province": "Illinois", "Latitude": "42.0742", "Longitude": "-89.2819",
              "Location accuracy": "approximate"}
    fields.update(pf)
    return {"record_id": "us-il:new:x", "plant_name": name, "country": "United States", "fields": fields,
            "refs": {"Location Data Source": ["https://a.example/q"]},
            "units": [{"unit_name": "1", "fields": {"Capacity (MW)": "347", "Fuel": "fossil gas: natural gas",
                                                    "Status": "announced",
                                                    "Turbine/Engine Technology": "unknown"},
                       "refs": {"Capacity Data Source": ["https://a.example/q"],
                                "Fuel Data Source": ["https://a.example/q"]},
                       "researcher_notes": "Searched the queue entry, the air permit system and the developer's site; no turbine type was found.",
                       "milestones": MS}]}


def reasons(lanes, names=frozenset()):
    return [r for _, r in sg.gate_add_web_validation(lanes, names=set(names))]


def test_complete_add_passes():
    assert reasons({"newplants": [plant()]}) == []


def test_unknown_technology_needs_the_search_in_the_note():
    p = plant()
    p["units"][0]["researcher_notes"] = "Capacity is from the queue entry."
    assert any("Technology is" in r for r in reasons({"newplants": [p]}))


def test_blank_coordinates_need_a_search_sentence():
    p = plant(Latitude="", Longitude="", **{"Location accuracy": ""})
    assert len(reasons({"newplants": [p]})) == 3
    p["not_found"] = {f: "Searched the queue file, the county records and the permit system; no site is named."
                      for f in ("Latitude", "Longitude", "Location accuracy")}
    assert reasons({"newplants": [p]}) == []


def test_plain_not_found_list_passes_with_notes_that_say_what_was_searched():
    p = plant(Latitude="", Longitude="", **{"Location accuracy": ""})
    p["not_found"] = ["Latitude", "Longitude", "Location accuracy"]
    assert len(reasons({"newplants": [p]})) == 3
    p["researcher_notes"] = "I searched the county records and the permit system; no site or coordinates were found."
    assert reasons({"newplants": [p]}) == []


def test_filled_value_needs_its_data_source():
    p = plant()
    p["fields"]["Owner(s)"] = "Test LLC [100%]"
    assert any("Owners Data Source" in r for r in reasons({"newplants": [p]}))


def test_name_rules():
    assert any("phase" in r for r in reasons({"newplants": [plant("Test Hub Phase 2 power station")]}))
    assert any("double space" in r for r in reasons({"newplants": [plant("Test  Hub power station")]}))
    assert any("already used" in r for r in reasons({"newplants": [plant()]}, {"test hub power station"}))
    p = plant()
    p["units"].append(dict(p["units"][0]))
    assert any("used twice" in r for r in reasons({"newplants": [p]}))


def test_adds_already_in_the_database_are_set_aside():
    lanes = {"newplants": [plant()]}
    kept, notes = sg.adds_not_yet_typed(lanes, applied_ids=(), names={"test hub power station"})
    assert kept["newplants"] == [] and "already in the database" in notes[0][1]
    kept, notes = sg.adds_not_yet_typed(lanes, applied_ids={"us-il:new:x"}, names=set())
    assert kept["newplants"] == [] and notes == []

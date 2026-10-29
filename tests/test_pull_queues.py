"""Offline tests for pull_queues.py (per-state interconnection queue pull): saved snippets of the
MISO JSON and the two PJM XML files, no network."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import pull_queues as q  # noqa: E402

MI = q.STATES["MI"]

MISO = [
    {"projectNumber": "J3923", "state": "MI", "county": "Washtenaw", "fuelType": "Gas", "facilityType": "Combined Cycle",
     "summerNetMW": 1414, "applicationStatus": "Active", "studyCycle": "DPP-2025", "queueDate": "2025-03-01T00:00:00",
     "poiName": "Majestic-Milan 345 kV Line", "transmissionOwner": "ITC"},
    {"projectNumber": "J10", "state": "MI", "county": "Ottawa", "fuelType": "Solar", "facilityType": "Photovoltaic",
     "summerNetMW": 100, "applicationStatus": "Active", "transmissionOwner": "METC"},
    {"projectNumber": "J4300", "state": "MI", "county": "Marquette", "fuelType": "Gas", "facilityType": "Piston",
     "summerNetMW": 20, "applicationStatus": "Active", "studyCycle": "ERAS Study Cycle 2", "transmissionOwner": "AMERICAN TRANSMISSION COMPANY"},
    {"projectNumber": "J4500", "state": "", "county": "", "fuelType": "", "summerNetMW": 800,
     "applicationStatus": "Active", "transmissionOwner": "METC"},
    {"projectNumber": "J4501", "state": "", "county": "", "fuelType": "", "summerNetMW": 300,
     "applicationStatus": "Active", "transmissionOwner": "ITC MIDWEST"},
    {"projectNumber": "J4502", "state": "", "county": "", "fuelType": "", "summerNetMW": 300,
     "applicationStatus": "Active", "transmissionOwner": "AMERICAN TRANSMISSION COMPANY"},
    {"projectNumber": "J4503", "state": "", "county": "", "fuelType": "", "summerNetMW": 60,
     "applicationStatus": "Active", "transmissionOwner": "ITC"},
    {"projectNumber": "J5", "state": "WI", "fuelType": "Gas", "transmissionOwner": "ATC"},
]

PJM_SERIAL = """﻿<?xml version="1.0" encoding="UTF-8"?>
<Projects>
  <Project><ProjectNumber>AA2-116</ProjectNumber><Name>Cook-East Elkhart 345kV</Name>
    <CommercialName>Indeck Niles Energy Center</CommercialName><State>MI</State><County>Cass</County>
    <Status>In Service</Status><TransmissionOwner>AEP</TransmissionOwner><MWEnergy>994</MWEnergy>
    <MWCapacity>994</MWCapacity><Fuel>Natural Gas</Fuel><SubmittedDate>3/1/2018</SubmittedDate>
    <ActualInServiceDate>12/27/2021</ActualInServiceDate><ProjectedInServiceDate>3/15/2022</ProjectedInServiceDate></Project>
  <Project><ProjectNumber>AB1-001</ProjectNumber><Name>Somewhere 138kV</Name><State>MI</State><County>Cass</County>
    <Status>Active</Status><Fuel>Solar</Fuel><MWCapacity>50</MWCapacity></Project>
  <Project><ProjectNumber>AB1-002</ProjectNumber><Name>Landfill 69kV</Name><State>MI</State><County>Cass</County>
    <Status>In Service</Status><Fuel>Methane</Fuel><MWCapacity>3</MWCapacity></Project>
  <Project><ProjectNumber>AB1-003</ProjectNumber><Name>Ohio CT 345kV</Name><State>OH</State><County>Lucas</County>
    <Status>Active</Status><Fuel>Natural Gas</Fuel><MWCapacity>300</MWCapacity></Project>
  <Project><ProjectNumber>AB1-004</ProjectNumber><Name>Mystery CC 345kV</Name><CommercialName>Combined Cycle Plant</CommercialName>
    <State>MI</State><County>Berrien</County><Status>Active</Status><Fuel>Not Specified</Fuel><MWCapacity>0</MWCapacity>
    <MWEnergy>400</MWEnergy></Project>
</Projects>"""

PJM_CYCLE = """<?xml version="1.0" encoding="UTF-8"?>
<Projects>
  <Project><ProjectNumber>C01-1678</ProjectNumber><Cycle>C01</Cycle><Stage>Phase 1</Stage><Name>Thomson 345 kV</Name>
    <Developer>Indeck Niles, LLC</Developer><State>MI</State><County>Cass</County><Status>Active</Status>
    <TransmissionOwner>AEP</TransmissionOwner><MWEnergy>0.0</MWEnergy><MWCapacity>9.6</MWCapacity>
    <Fuel>Natural Gas</Fuel><SubmittedDate>4/24/2026</SubmittedDate><RequestedInServiceDate>4/1/2027</RequestedInServiceDate></Project>
  <Project><ProjectNumber>C01-1203</ProjectNumber><Cycle>C01</Cycle><State>MI</State><County>Cass</County>
    <Status>Active</Status><Fuel>Solar</Fuel><MWCapacity>184</MWCapacity></Project>
</Projects>"""

PLANTS = [
    {"id": "L100000402411", "name": "Indeck Niles energy center", "city": "Niles", "county": "cass",
     "known": MI["known"]["L100000402411"]},
    {"id": "LX", "name": "Washtenaw plant", "city": "", "county": "washtenaw", "known": []},
    {"id": "LY", "name": "Marquette plant", "city": "", "county": "marquette", "known": []},
]


def test_miso_entries_filter_hidden_owners_and_flags():
    entries, shared = q.miso_entries(MISO, MI, "MI")
    out = {e["queue_id"]: e for e in entries}
    assert set(out) == {"J3923", "J10", "J4300", "J4500", "J4503"}
    assert shared == 1
    assert out["J3923"]["gas_oil"] and not out["J10"]["gas_oil"]
    assert out["J4500"]["fuel_unknown"] and out["J4500"]["state"] == "(hidden by MISO)"
    assert out["J4503"]["fuel_unknown"]
    assert out["J4300"]["stage"].startswith("ERAS")
    assert out["J3923"]["url"] == q.MISO_PAGE


def test_pjm_projects_handles_byte_order_mark_and_dates():
    ps = q.pjm_projects(PJM_SERIAL)
    assert len(ps) == 5 and ps[0]["ProjectNumber"] == "AA2-116"
    assert q.pjm_date("4/24/2026") == "2026-04-24" and q.pjm_date("") == ""


def test_pjm_entries_keep_michigan_gas_and_thermal_unknown_only():
    out = {e["queue_id"]: e for e in q.pjm_entries(q.pjm_projects(PJM_SERIAL), MI, "serial")}
    assert set(out) == {"AA2-116", "AB1-004"}
    assert out["AA2-116"]["gas_oil"] and out["AA2-116"]["in_service"] == "2021-12-27"
    assert out["AA2-116"]["project_name"] == "Indeck Niles Energy Center"
    assert out["AB1-004"]["fuel_unknown"] and not out["AB1-004"]["gas_oil"] and out["AB1-004"]["mw"] == 400
    assert out["AA2-116"]["url"] == q.PJM_SERIAL_PAGE


def test_pjm_cycle_entries_use_cycle_page_and_requested_date():
    out = q.pjm_entries(q.pjm_projects(PJM_CYCLE), MI, "cycle")
    assert [e["queue_id"] for e in out] == ["C01-1678"]
    e = out[0]
    assert e["url"] == q.PJM_CYCLE_PAGE and e["in_service"] == "2027-04-01" and e["mw"] == 9.6
    assert e["stage"] == "C01 / Phase 1" and "Indeck Niles" in e["note"]


def test_match_all_by_pattern_developer_and_county():
    miso, _ = q.miso_entries(MISO, MI, "MI")
    entries = miso + q.pjm_entries(q.pjm_projects(PJM_SERIAL), MI, "serial") + \
        q.pjm_entries(q.pjm_projects(PJM_CYCLE), MI, "cycle")
    by_plant, matched = q.match_all(PLANTS, entries)
    ids = lambda pid: sorted(entries[i]["queue_id"] for i in by_plant[pid])  # noqa: E731
    assert ids("L100000402411") == ["AA2-116", "C01-1678"]
    assert ids("LX") == ["J3923"]
    assert ids("LY") == ["J4300"]
    # fuel-unknown leads are never matched
    assert not any(e["queue_id"] in ("J4500", "AB1-004") for e in (entries[i] for i in matched))


def test_state_settings_carry_mississippi_and_michigan():
    assert q.STATES["MS"]["markets"] == ["MISO"] and q.STATES["MI"]["markets"] == ["MISO", "PJM"]
    ms_entries, _ = q.miso_entries([{"projectNumber": "J4176", "state": "", "fuelType": "", "summerNetMW": 1750,
                                     "transmissionOwner": "ENTERGY MISSISSIPPI, LLC."}], q.STATES["MS"], "MS")
    assert ms_entries[0]["fuel_unknown"]


def test_write_outputs_keys_match_what_the_brief_reads(tmp_path):
    entries, _ = q.miso_entries(MISO, MI, "MI")
    entries += q.pjm_entries(q.pjm_projects(PJM_CYCLE), MI, "cycle")
    by_plant, matched = q.match_all(PLANTS, entries)
    q.write_outputs(tmp_path, "Michigan", PLANTS, entries, by_plant, matched, [], "2026-10-23")
    data = json.loads((tmp_path / "queues.json").read_text())
    assert set(data) == {"generated", "sources", "entries", "by_plant", "unmatched_gas_oil", "hidden_fuel_leads"}
    assert "J4500" in data["hidden_fuel_leads"] and "J3923" not in data["unmatched_gas_oil"]
    md = (tmp_path / "queues.md").read_text()
    assert "Washtenaw County" in md and "County County" not in md
    import build_state_brief as b
    out, d = b.load_harvest(tmp_path)
    assert "L100000402411" in out and "LX" in out
    assert "J4500" in b.render_harvest_brief(d)

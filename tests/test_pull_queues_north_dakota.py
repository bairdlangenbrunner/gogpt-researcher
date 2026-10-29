"""Offline tests for the SPP reader in pull_queues.py and the North Dakota queue settings: a saved
snippet of the SPP active queue CSV and MISO rows, no network."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import pull_queues as q  # noqa: E402

ND = q.STATES["ND"]

SPP = '''"Last Updated On",10/28/2026,
Generation Interconnection Number,IFS Queue Number,Current Cluster,Cluster Group, Nearest Town or County,State,TO at POI,In-Service Date,Commercial Operation Date,Cessation Date,Original Generator Commercial Op Date,Capacity,MAX Summer MW,MAX Winter MW,Service Type,Requested Maximum Injection Capability (MW),Requested Network Resource Deliverability (MW),Nameplate Capacity,Generation Type,Fuel Type,Substation or Line,Request Received,Date Withdrawn,Status,JTIQ Participant,JTIQ Commitment,Cause of Delay
GEN-2024-081,,DISIS-2024-001,,Williams,ND,BEPC,4/1/2028,2/1/2029,,,745,745,,,,,760,Thermal,Gas,Springbrook - Tande 345 kV Line,10/30/2024,,DISIS STAGE,,,
GEN-2022-009,,DISIS-2022-001,,Williams,ND,BEPC,7/1/2023,4/11/2025,,,125,125,,,,,0,Thermal,,Judson Substation 345 kV,5/26/2022,,IA FULLY EXECUTED/COMMERCIAL OPERATION,,,
ERAS-2025-011,,ERAS-2025-001,,Stanton,ND,BEPC,9/27/2029,9/27/2030,,,750,750,,,,,750,Thermal,Combined Cycle,Leland Olds 345kV Substation,10/1/2025,,IA PENDING,,,
GEN-2024-141,,DISIS-2024-001,,Mercer,ND,BEPC,10/1/2031,12/31/2031,,,212,212,,,,,212,Wind,Wind,BASIN__-BE4 230 kV Substation,3/1/2025,,DISIS STAGE,,,
GEN-2025-900,,DISIS-2025-001,,Williams,ND,BEPC,1/1/2030,,,,300,300,,,,,0,Thermal,Gas,New Peaker 230 kV,3/1/2026,,DISIS STAGE,,,
GEN-2024-001,,DISIS-2024-001,,Lincoln,SD,WAPA,1/1/2028,,,,100,100,,,,,0,Thermal,Gas,Sioux Falls 115 kV,3/1/2025,,DISIS STAGE,,,
'''

PLANTS = [
    {"id": "L100001047848", "name": "Bison Generation Station", "city": "Wheelock Township", "county": "williams",
     "known": ND["known"]["L100001047848"]},
    {"id": "L100000401741", "name": "Pioneer generating station", "city": "Williston", "county": "williams",
     "known": ND["known"]["L100000401741"]},
    {"id": "L100001080387", "name": "River Run Energy Center", "city": "Stanton", "county": "mercer",
     "known": ND["known"]["L100001080387"]},
]


def test_spp_rows_skip_the_update_line_and_strip_headers():
    rows, updated = q.spp_rows("﻿" + SPP)
    assert updated == "2026-10-28" and len(rows) == 6
    assert rows[0]["Nearest Town or County"] == "Williams" and rows[0]["Generation Interconnection Number"] == "GEN-2024-081"


def test_spp_entries_flags_size_and_dates():
    rows, _ = q.spp_rows(SPP)
    es = {e["queue_id"]: e for e in q.spp_entries(rows, ND, "ND")}
    assert set(es) == {"GEN-2024-081", "GEN-2022-009", "ERAS-2025-011", "GEN-2024-141", "GEN-2025-900"}
    bison = es["GEN-2024-081"]
    assert bison["gas_oil"] and bison["mw"] == 760 and bison["in_service"] == "2028-04-01"
    assert bison["queue_date"] == "2024-10-30" and bison["url"] == q.SPP_PAGE and bison["source"] == "SPP"
    assert es["GEN-2022-009"]["fuel_unknown"] and not es["GEN-2022-009"]["gas_oil"] and es["GEN-2022-009"]["mw"] == 125
    assert es["ERAS-2025-011"]["gas_oil"] and es["ERAS-2025-011"]["stage"] == "ERAS-2025-001"
    assert not es["GEN-2024-141"]["gas_oil"] and not es["GEN-2024-141"]["fuel_unknown"]


def test_match_prefers_the_named_plant_over_county_neighbors():
    rows, _ = q.spp_rows(SPP)
    entries = q.spp_entries(rows, ND, "ND")
    by_plant, matched = q.match_all(PLANTS, entries)
    ids = lambda pid: sorted(entries[i]["queue_id"] for i in by_plant[pid])  # noqa: E731
    assert ids("L100001047848") == ["GEN-2024-081", "GEN-2025-900"]
    # Judson is Pioneer's substation; the thermal row with no fuel still matches it by name
    assert ids("L100000401741") == ["GEN-2022-009", "GEN-2025-900"]
    assert ids("L100001080387") == ["ERAS-2025-011"]


def test_blank_state_miso_rows_of_north_dakota_owners_are_leads():
    miso = [{"projectNumber": "J4333", "state": "", "fuelType": "", "summerNetMW": 490,
             "transmissionOwner": "GREAT RIVER ENERGY"},
            {"projectNumber": "J3163", "state": "ND", "county": "Cass", "fuelType": "Hybrid", "facilityType": "Combustion Turbine",
             "summerNetMW": 481, "transmissionOwner": "NORTHERN STATES POWER (XCEL ENERGY)", "poiName": "Bison 345kV"},
            {"projectNumber": "J4400", "state": "", "fuelType": "", "summerNetMW": 300, "transmissionOwner": "ITC MIDWEST"},
            {"projectNumber": "J9", "state": "MN", "fuelType": "Gas", "transmissionOwner": "OTTER TAIL POWER"}]
    es, shared = q.miso_entries(miso, ND, "ND")
    assert [e["queue_id"] for e in es] == ["J4333", "J3163"] and shared == 1
    assert es[0]["fuel_unknown"] and es[0]["state"] == "(hidden by MISO)"


def test_write_outputs_with_spp(tmp_path):
    rows, _ = q.spp_rows(SPP)
    entries = q.spp_entries(rows, ND, "ND")
    by_plant, matched = q.match_all(PLANTS, entries)
    q.write_outputs(tmp_path, "North Dakota", PLANTS, entries, by_plant, matched, [], "2026-10-29")
    data = json.loads((tmp_path / "queues.json").read_text())
    assert set(data) == {"generated", "sources", "entries", "by_plant", "unmatched_gas_oil", "hidden_fuel_leads"}
    assert data["hidden_fuel_leads"] == ["GEN-2022-009"] and data["unmatched_gas_oil"] == []
    md = (tmp_path / "queues.md").read_text()
    assert "nearest town or county: Stanton" in md and "Stanton County" not in md

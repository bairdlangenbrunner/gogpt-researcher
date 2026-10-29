"""Offline tests for scopes/us-ms/pull_queues_mississippi.py: saved snippets of the MISO JSON and the
Southern Company Power BI response, no network."""
import base64
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from paths import load_scope_module  # noqa: E402

q = load_scope_module("us-ms", "pull_queues_mississippi")

MISO = [
    {"projectNumber": "J1249", "state": "MS", "county": "Lamar", "fuelType": "Gas", "facilityType": "Combined Cycle",
     "summerNetMW": 600, "applicationStatus": "Done", "studyCycle": "DPP-2016", "queueDate": "2016-02-01T00:00:00",
     "inService": "2022-06-01T00:00:00", "poiName": "Morrow 161kV", "transmissionOwner": "COOPERATIVE ENERGY"},
    {"projectNumber": "J900", "state": "MS", "county": "Hinds", "fuelType": "Solar", "facilityType": "Photovoltaic",
     "summerNetMW": 100, "applicationStatus": "Active", "poiName": "X 230kV", "transmissionOwner": "ENTERGY MISSISSIPPI"},
    {"projectNumber": "J4176", "state": "", "county": "", "fuelType": "", "summerNetMW": 1750,
     "applicationStatus": "Withdrawn", "transmissionOwner": "ENTERGY MISSISSIPPI, LLC."},
    {"projectNumber": "J5", "state": "LA", "fuelType": "Gas", "transmissionOwner": "ENTERGY LOUISIANA"},
]


def test_miso_entries_filters_and_flags():
    out = {e["queue_id"]: e for e in q.miso_entries(MISO)}
    assert set(out) == {"J1249", "J900", "J4176"}
    assert out["J1249"]["gas_oil"] and out["J1249"]["in_service"] == "2022-06-01"
    assert not out["J900"]["gas_oil"]
    assert out["J4176"]["fuel_unknown"] and out["J4176"]["state"] == "(hidden by MISO)"
    assert out["J1249"]["url"] == q.MISO_PAGE


def test_embed_parts_and_host():
    key = base64.b64encode(json.dumps({"k": "abc-123", "t": "tenant-9"}).encode()).decode().rstrip("=")
    assert q.embed_parts(f"https://app.powerbi.com/view?r={key}") == ("abc-123", "tenant-9")
    html = "x https://wabi-us-north-central-e-primary-redirect.analysis.windows.net/y"
    assert q.api_host_from_view(html) == "https://wabi-us-north-central-e-primary-api.analysis.windows.net"
    assert q.api_host_from_view("nothing") is None


def test_dsr_rows_decodes_repeats_nulls_and_dictionaries():
    resp = {"results": [{"result": {"data": {
        "descriptor": {"Select": [{"Value": "G0", "Name": "T.Request"}, {"Value": "G1", "Name": "T.Capacity MW"},
                                  {"Value": "G2", "Name": "T.Gen Facility Location"}]},
        "dsr": {"DS": [{"ValueDicts": {"D0": ["Clarke County, MS", "Lee County, AL"]},
                        "PH": [{"DM0": [
                            {"S": [{"N": "G0", "T": 1}, {"N": "G1", "T": 3}, {"N": "G2", "T": 1, "DN": "D0"}],
                             "C": ["IC-1", 785, 0]},
                            {"C": ["IC-2", 9], "R": 4},
                            {"C": ["IC-3", 5], "Ø": 4},
                        ]}]}]}}}}]}
    rows = q.dsr_rows(resp)
    assert rows[0] == {"Request": "IC-1", "Capacity MW": 785, "Gen Facility Location": "Clarke County, MS"}
    assert rows[1]["Request"] == "IC-2" and rows[1]["Gen Facility Location"] == "Clarke County, MS"
    assert rows[2]["Gen Facility Location"] is None


def test_southern_entry_and_filter():
    row = {"Request": "26-IC-1489", "Facility Name": "Test CT", "Gen Facility Location": "Clarke County, MS",
           "Gen Type/Size ": "199.4 MW Natural Gas Combustion Turbine", "Capacity MW": "199.4",
           "Proposed POI": "Laurel East - Sykes 230 kV", "Request Phase": "Cluster Study"}
    e = q.southern_entry(row, "Active")
    assert e["gas_oil"] and e["mw"] == 199.4 and e["state"] == "MS" and e["county"] == "Clarke"
    assert e["status"] == "Active, Cluster Study"
    solar = dict(row, **{"Gen Type/Size ": "100 MW Solar"})
    assert not q.southern_entry(solar, "Active")["gas_oil"]
    other = dict(row, **{"Gen Facility Location": "Lee County, AL"})
    assert len(q.southern_entries({"Active": [row, other]})) == 1


def test_match_all_by_poi_name_and_county():
    plants = [{"id": "L100000104011", "name": "Morrow Generating Plant", "city": "Purvis", "county": "lamar",
               "owner": "", "statuses": [], "name_words": set()},
              {"id": "LX", "name": "Nowhere plant", "city": "", "county": "hinds",
               "owner": "", "statuses": [], "name_words": set()}]
    entries = q.miso_entries(MISO)
    by_plant, matched = q.match_all(plants, entries)
    assert [entries[i]["queue_id"] for i in by_plant["L100000104011"]] == ["J1249"]
    assert by_plant["LX"] == []
    assert q.entry_line(entries[0]).startswith("MISO J1249")

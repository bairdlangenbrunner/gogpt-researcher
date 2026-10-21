"""The review dataset's location block: a staged location record becomes a line with `location`."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from review_app import review_data  # noqa: E402


def record(**extra):
    r = {"record_id": "L100000402511:plant:location", "gem_plant_id": "L100000402511",
         "gem_unit_id": "G100000401771", "unit_name": "F701", "plant_name": "Brandywine power facility",
         "verdict": "change",
         "fields": {"Latitude": "38.69512", "Longitude": "-76.84071", "Location accuracy": "exact"},
         "current": {"Latitude": "38.7", "Longitude": "-76.8", "Location accuracy": "approximate"},
         "refs": {"Location Data Source": ["https://example.gov/permit.pdf"]},
         "tier": "high", "applies_to_all_units": True, "sibling_unit_ids": ["G100000401772"],
         "sibling_current": {"G100000401772": {"Latitude": "38.7", "Longitude": "-76.8",
                                               "Location accuracy": "approximate"}},
         "location_method": "address", "location_moved_m": 3900, "checks": [25]}
    r.update(extra)
    return r


def test_location_block():
    line = review_data.update_line(record(), "batches/us-ks/staging", {})
    loc = line["location"]
    assert loc["proposed"]["lat"] == 38.69512 and loc["proposed"]["accuracy"] == "exact"
    assert loc["proposed"]["pin"] == "https://www.google.com/maps/search/?api=1&query=38.69512,-76.84071"
    assert "basemap=satellite" in loc["proposed"]["satellite"]
    assert loc["current"]["lat"] == 38.7 and loc["current"]["accuracy"] == "approximate"
    assert loc["moved_m"] == 3900 and loc["method"] == "address" and loc["needs_review"] is False
    assert loc["image"] == "" and loc["control_points"] == []
    assert isinstance(line["sibling_current"]["G100000401772"], dict)


def test_blank_current_and_map_image():
    r = record(current={"Latitude": "", "Longitude": "", "Location accuracy": ""}, location_moved_m=None,
               location_method="map", location_image="staging/maps/L100000402511.jpg",
               location_control_points=[{"feature": "gate", "px": [1, 2], "lat": 38.69, "lon": -76.84}],
               location_fit_m=45, location_needs_review=True)
    loc = review_data.update_line(r, "batches/us-ks/staging", {})["location"]
    assert loc["current"]["lat"] is None and loc["current"]["pin"] is None
    assert loc["moved_m"] is None and loc["needs_review"] is True and loc["fit_m"] == 45
    assert loc["image"] == "batches/us-ks/staging/maps/L100000402511.jpg"


def test_other_lines_have_no_location():
    r = {"record_id": "L1:G1:start-year", "gem_plant_id": "L1", "gem_unit_id": "G1",
         "fields": {"Start year": "1996"}, "refs": {}, "tier": "high"}
    assert "location" not in review_data.update_line(r, "batches/us-ks/staging", {})

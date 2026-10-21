import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_state_brief as bsb  # noqa: E402
import geo  # noqa: E402
import location_candidates as lc  # noqa: E402

HEAD = ["GEM location ID", "GEM unit ID", "Plant name", "Unit name", "Country/Area",
        "State/Province", "City", "Local area (taluk, county)", "Major area (prefecture, district)",
        "Latitude", "Longitude", "Location accuracy", "Location Data Source",
        "Other IDs (location)", "Status", "Capacity (MW)"]


def row(loc, unit, plant, country="United States", state="Maryland", lat="38.7", lon="-76.8",
        acc="approximate", status="operating", other="", src=""):
    d = dict.fromkeys(HEAD, "")
    d.update({"GEM location ID": loc, "GEM unit ID": unit, "Plant name": plant, "Unit name": "U1",
              "Country/Area": country, "State/Province": state, "City": "Town",
              "Latitude": lat, "Longitude": lon, "Location accuracy": acc, "Status": status,
              "Other IDs (location)": other, "Location Data Source": src, "Capacity (MW)": "100"})
    return d


ROWS = [
    row("L1", "G1", "Exact plant", acc="exact"),
    row("L2", "G2", "Approx operating", other="EIA: 12345", src="https://a.example.com/x, https://www.google.com/maps/q"),
    row("L2", "G3", "Approx operating", other="EIA: 12345"),
    row("L3", "G4", "Blank plant", lat="", lon="", acc="exact", status="announced"),
    row("L4", "G5", "Approx proposed", acc="Approximate", status="announced"),
    row("L5", "G6", "Other state", state="Delaware"),
    row("L6", "G7", "German", country="Germany", state="Bavaria"),
]


def provider(plant):
    if "12345" in plant["eia_codes"]:
        return [{"source": "EIA-860 2025 Plant table", "lat": 38.69512, "lon": -76.84071,
                 "address": "12345 Brandywine Rd, Brandywine, MD 20613", "county": "Prince George's"},
                {"source": "EIA-860M july_generator2026.xlsx", "lat": 38.7001, "lon": -76.8001}]
    return []


def test_selection_state():
    scope = bsb.make_scope(state="Maryland")
    res = lc.select_candidates(ROWS, scope, provider)
    ids = [t["plant_id"] for t in res["tasks"]]
    assert ids == ["L2", "L3", "L4"]
    assert res["plants_checked"] == 4 and res["candidates"] == 3
    t = {x["plant_id"]: x for x in res["tasks"]}
    assert t["L2"]["checks"] == [25, 42] and t["L3"]["checks"] == [25] and t["L4"]["checks"] == [25]
    loc = t["L2"]["location"]
    assert loc["operating"] and loc["eia_codes"] == ["12345"]
    assert loc["location_hosts"] == ["a.example.com", "www.google.com"]
    p860 = loc["dataset_points"][0]
    assert abs(p860["distance_m"] - geo.distance_m(38.7, -76.8, 38.69512, -76.84071)) < 1
    assert loc["nearest"]["source"].startswith("EIA-860M") and not loc["far"]
    assert "12345 Brandywine Rd" in t["L2"]["task"] and "checklist row 42" in t["L2"]["task"]
    assert "http" not in t["L2"]["task"]
    blank = t["L3"]
    assert blank["location"]["current"]["lat"] is None and blank["location"]["current"]["links"] == {}
    assert "no coordinate" in blank["task"] and "No EIA or permit point is available." in blank["task"]


def test_far_flag():
    scope = bsb.make_scope(state="Maryland")
    far = lambda p: [{"source": "EIA-860 2025 Plant table", "lat": 39.2, "lon": -76.8}]
    res = lc.select_candidates(ROWS, scope, far)
    assert all(t["location"]["far"] for t in res["tasks"] if t["location"]["current"]["lat"] is not None)
    blank = [t for t in res["tasks"] if t["plant_id"] == "L3"][0]
    assert blank["location"]["nearest"] is None and not blank["location"]["far"]


def test_selection_country():
    scope = bsb.make_scope(country="germany")
    res = lc.select_candidates(ROWS, scope)
    assert [t["plant_id"] for t in res["tasks"]] == ["L6"]


def test_output_loads_in_brief_builder(tmp_path):
    scope = bsb.make_scope(state="Maryland")
    res = lc.select_candidates(ROWS, scope, provider)
    out = {"where": scope, "read": lc.now_et(), "csv": "x.csv",
           "sources": {"eia860m": None, "eia860": None}, **res}
    p = tmp_path / "location_us-md.json"
    p.write_text(json.dumps(out), encoding="utf-8")
    items = bsb.load_validation(p, scope, producer="location_candidates.py")
    assert set(items) == {"L2", "L3", "L4"}
    unit, item = items["L2"][0]
    assert unit is None and item["checks"] == [25, 42]
    assert items["L4"][0][1]["checks"] == [25]
    assert "+" in lc.now_et() or "-" in lc.now_et()[10:]


def test_memo_and_provider():
    scope = bsb.make_scope(state="Maryland")
    res = lc.select_candidates(ROWS, scope, provider)
    out = {"where": scope, "read": "now", "csv": "x", "sources": {"eia860m": "f.xlsx", "eia860": None}, **res}
    m = lc.memo(out)
    assert "Approx operating" in m and "Plants with a weak or missing location: 3" in m
    prov = lc.eia_provider(gens=None, idx860={"12345": {"name": "B", "address": "1 Rd", "city": "C",
                           "state": "MD", "zip": "2", "county": "K", "lat": 1.0, "lon": 2.0, "utility": ""}},
                           year860=2025)
    pts = prov({"eia_codes": ["12345"]})
    assert pts[0]["source"] == "EIA-860 2025 Plant table" and pts[0]["address"] == "1 Rd, C, MD 2"


def test_no_eia_cli(tmp_path, monkeypatch):
    p = tmp_path / "e.csv"
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEAD)
        w.writeheader()
        w.writerows(ROWS)
    monkeypatch.setattr(lc, "work_dir", lambda: tmp_path)
    monkeypatch.setattr(sys, "argv", ["x", "--state", "Maryland", "--csv", str(p),
                                      "--allow-stale-export", "--no-eia"])
    lc.main()
    d = json.loads((tmp_path / "location_us-md.json").read_text())
    assert d["candidates"] == 3 and d["sources"] == {"eia860m": None, "eia860": None}
    assert (tmp_path / "location_us-md.md").exists()

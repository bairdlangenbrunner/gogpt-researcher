import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import geocode  # noqa: E402

CENSUS = {"result": {"addressMatches": [
    {"matchedAddress": "1 MAIN ST, TOPEKA, KS, 66603", "coordinates": {"x": -95.67, "y": 39.05},
     "tigerLine": {"side": "L"}},
    {"matchedAddress": "1 MAIN ST, LAWRENCE, KS", "coordinates": {"x": -95.23, "y": 38.97},
     "tigerLine": {"side": "R"}}]}}
NOM = [{"display_name": "Jeffrey Energy Center, Kansas", "lat": "39.2863", "lon": "-96.1171",
        "importance": 0.41, "category": "power", "type": "plant"}]


def setup(monkeypatch, tmp_path, census=CENSUS, nom=NOM):
    calls = []

    def fake(url):
        calls.append(url)
        return census if "census.gov" in url else nom
    monkeypatch.setattr(geocode, "_fetch_json", fake)
    monkeypatch.setattr(geocode, "cache_dir", lambda: tmp_path)
    return calls


def test_census_ordered_by_near(monkeypatch, tmp_path):
    setup(monkeypatch, tmp_path)
    res = geocode.geocode("1 Main St", near=(38.97, -95.2), limit=5)
    assert [r["provider"] for r in res] == ["census", "census"]
    assert "LAWRENCE" in res[0]["label"]
    assert res[0]["distance_m"] < res[1]["distance_m"]
    assert res[0]["quality"] == "tiger line side R"


def test_fallback_to_nominatim(monkeypatch, tmp_path):
    calls = setup(monkeypatch, tmp_path, census={"result": {"addressMatches": []}})
    res = geocode.geocode("Jeffrey Energy Center", country="US")
    assert res[0]["provider"] == "nominatim" and res[0]["lat"] == 39.2863
    assert "countrycodes=us" in calls[-1]
    assert res[0]["quality"] == "importance 0.41" and res[0]["type"] == "power/plant"


def test_non_us_skips_census(monkeypatch, tmp_path):
    calls = setup(monkeypatch, tmp_path)
    geocode.geocode("Mannheim", country="DE")
    assert all("nominatim" in c for c in calls)


def test_cache_roundtrip(monkeypatch, tmp_path):
    calls = setup(monkeypatch, tmp_path)
    geocode.geocode("1 Main St", country="US")
    assert list(tmp_path.glob("*.json"))
    n = len(calls)
    geocode.geocode("1 Main St", country="US")
    assert len(calls) == n


def test_reverse(monkeypatch, tmp_path):
    payload = {"display_name": "x", "address": {"country_code": "us", "country": "United States",
                                                "state": "Kansas", "county": "Shawnee County",
                                                "town": "Topeka"}}
    monkeypatch.setattr(geocode, "_fetch_json", lambda url: payload)
    monkeypatch.setattr(geocode, "cache_dir", lambda: tmp_path)
    r = geocode.reverse(39.05, -95.67)
    assert r["country_code"] == "US" and r["state"] == "Kansas"
    assert r["county"] == "Shawnee County" and r["city"] == "Topeka"

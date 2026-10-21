"""End to end for the location step (docs/reference/location.md): a shard
that followed the ladder becomes one plant-level location record, the
record passes state_gate.gate_location and build_review_package.validate,
a second-look shard replaces the first one's location, and an untasked
move becomes a question."""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from assemble_state import Assembler  # noqa: E402
from build_review_package import validate  # noqa: E402
from state_gate import gate_location  # noqa: E402

WHERE = {"kind": "state", "name": "Kansas", "slug": "kansas",
         "country": "United States", "postal": "ks"}
HEADER = ["Country/Area", "Plant name", "Unit name", "Status", "Capacity (MW)", "Latitude",
          "Longitude", "Location accuracy", "Location Data Source", "City", "State/Province",
          "GEM location ID", "GEM unit ID"]
PIN = "https://www.google.com/maps/search/?api=1&query=38.50000,-97.50000"
DOC = "https://www.kdhe.ks.gov/permits/riverside-plant.pdf"


def setup(tmp_path, tasked=True, cur=("38.4", "-97.6", "approximate")):
    (tmp_path / "briefs").mkdir()
    (tmp_path / "shards").mkdir()
    task = {"text": "Location accuracy is approximate.", "fields": list(FIELDS), "checks": [25]}
    index = {"mode": "update", "where": WHERE, "scope": "ladder", "plants": [
        {"plant_id": "L1", "plant_name": "Riverside", "unit_ids": ["G1", "G2"],
         "tasks": {"G1": [{"text": "Capacity is blank.", "fields": ["Capacity (MW)"],
                           "checks": [12]}]},
         "plant_tasks": [task] if tasked else []}]}
    (tmp_path / "briefs" / "_index.json").write_text(json.dumps(index), encoding="utf-8")
    csv_path = tmp_path / "export.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        for uid, name in (("G1", "1"), ("G2", "2")):
            w.writerow(["United States", "Riverside", name, "operating", "100", cur[0], cur[1],
                        cur[2], "https://old.example.com/source", "Salina", "Kansas", "L1", uid])
    return csv_path


FIELDS = ("Latitude", "Longitude", "Location accuracy")


def finding(value):
    return {"value": value, "refs": [DOC, PIN],
            "verifications": [{"url": DOC, "ok": True, "contains_value": True, "name_found": True}],
            "tier": "high", "independent": False,
            "note": "The air permit application from May 2026 gives the plant's address."}


def shard(location=None, point=("38.50000", "-97.50000", "exact"), notes=None):
    s = {"meta": {"plant_id": "L1", "plant_name": "Riverside", "state": "Kansas",
                  "mode": "update", "model": "sonnet", "done": True},
         "units": [{"gem_unit_id": "G1", "unit_name": "1", "findings": {}, "not_found": [],
                    "notes": notes or ("The air permit application from May 2026 gives the "
                                       "address. The turbine hall and two stacks are visible "
                                       "in satellite imagery at the geocoded point.")},
                   {"gem_unit_id": "G2", "unit_name": "2", "findings": {}, "not_found": [],
                    "notes": "Same site as unit 1."}],
         "plant_findings": {f: finding(v) for f, v in zip(FIELDS, point)},
         "qa": [], "monitor": [], "newunits": [], "entities": [], "source_log": []}
    if location is not None:
        s["location"] = location
    return s


def run(tmp_path, csv_path):
    a = Assembler(tmp_path, csv_path, "2026Q4")
    a.run()
    return a


def test_ladder_shard_becomes_one_record(tmp_path):
    csv_path = setup(tmp_path)
    loc = {"method": "address", "moved_m": 0, "control_points": [], "fit_m": None,
           "image": "", "needs_review": False, "review_note": ""}
    (tmp_path / "shards" / "L1.json").write_text(json.dumps(shard(loc)), encoding="utf-8")
    a = run(tmp_path, csv_path)
    recs = [r for r in a.lanes["updates"] if "Latitude" in r.get("fields", {})]
    assert len(recs) == 1
    r = recs[0]
    assert r["record_id"] == "L1:plant:location"
    assert r["fields"] == {"Latitude": "38.50000", "Longitude": "-97.50000",
                           "Location accuracy": "exact"}
    assert r["verdict"] == "change"
    assert r["applies_to_all_units"] and r["sibling_unit_ids"] == ["G2"]
    assert set(r["sibling_current"]["G2"]) == set(FIELDS)
    assert r["location_method"] == "address"
    assert 13_000 < r["location_moved_m"] < 15_000
    assert r["checks"] == [25]
    assert PIN in r["refs"]["Location Data Source"] and DOC in r["refs"]["Location Data Source"]
    assert r["tier"] == "high"
    assert "Latitude" not in {f for u in a.lanes["updates"] for f in u.get("fields", {})
                              if u is not r}
    index = json.loads((tmp_path / "briefs" / "_index.json").read_text())
    assert gate_location(a.lanes, index, tmp_path) == []
    assert validate(a.lanes) == []


def test_nearby_point_on_approximate_plant_is_not_staged(tmp_path):
    csv_path = setup(tmp_path, cur=("38.501", "-97.501", "approximate"))
    loc = {"method": "address", "moved_m": 140, "needs_review": False}
    (tmp_path / "shards" / "L1.json").write_text(
        json.dumps(shard(loc, point=("38.50000", "-97.50000", "approximate"))), encoding="utf-8")
    a = run(tmp_path, csv_path)
    assert not [r for r in a.lanes["updates"] if "Latitude" in r.get("fields", {})]


def test_blank_point_is_a_fill(tmp_path):
    csv_path = setup(tmp_path, cur=("", "", ""))
    loc = {"method": "dataset", "moved_m": None, "needs_review": False}
    (tmp_path / "shards" / "L1.json").write_text(
        json.dumps(shard(loc, point=("38.50000", "-97.50000", "approximate"))), encoding="utf-8")
    a = run(tmp_path, csv_path)
    r = [r for r in a.lanes["updates"] if "Latitude" in r.get("fields", {})][0]
    assert r["verdict"] == "fill" and r["location_moved_m"] is None


def test_untasked_move_becomes_a_question(tmp_path):
    csv_path = setup(tmp_path, tasked=False)
    (tmp_path / "shards" / "L1.json").write_text(json.dumps(shard()), encoding="utf-8")
    a = run(tmp_path, csv_path)
    assert not [r for r in a.lanes["updates"] if "Latitude" in r.get("fields", {})]
    qa = [q for q in a.lanes["qa"] if q.get("concern_type") == "location"]
    assert len(qa) == 1 and qa[0]["proposed_value"]["Latitude"] == "38.50000"


def test_review_shard_replaces_the_location(tmp_path):
    csv_path = setup(tmp_path)
    first = shard({"method": "address", "moved_m": 14000, "needs_review": True,
                   "review_note": "The geocoder gave two candidates 3 km apart."})
    (tmp_path / "shards" / "L1.json").write_text(json.dumps(first), encoding="utf-8")
    second = shard({"method": "imagery", "moved_m": 600, "needs_review": False},
                   point=("38.40500", "-97.60000", "exact"),
                   notes="The plant footprint with two stacks is visible in satellite "
                         "imagery 600 m north of GEM's point.")
    second["units"][0]["findings"] = {}
    (tmp_path / "shards" / "L1.review.json").write_text(json.dumps(second), encoding="utf-8")
    a = run(tmp_path, csv_path)
    r = [r for r in a.lanes["updates"] if "Latitude" in r.get("fields", {})][0]
    assert r["fields"]["Latitude"] == "38.40500"
    assert r["location_method"] == "imagery" and r["location_needs_review"] is False
    assert a.shards["L1"]["meta"]["location_review"] == "L1.review.json"

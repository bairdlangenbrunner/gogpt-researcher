"""The duplicate check for new plants (Discovery SOP §5, Illinois 2026-10-30):
dedup_check.py searches the unfiltered export by name and by county or
distance and the batch's other records, and state_gate's hard gate `dedup`
fails a new plant with no current check or an unanswered hit."""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import dedup_check  # noqa: E402
from state_gate import gate_dedup  # noqa: E402

COLS = ["GEM location ID", "Plant name", "Other Name(s)", "Plant Name in Local Language / Script",
        "Country/Area", "State/Province", "Local area (taluk, county)", "Latitude", "Longitude",
        "Fuel", "Status"]
ROWS = [
    ["L1", "Will County Generating Station", "", "", "United States", "Illinois", "Will",
     "41.633", "-88.062", "coal: bituminous", "retired"],
    ["L2", "Prairie Energy Center", "", "", "United States", "Texas", "Hill County",
     "32.2", "-97.1", "fossil gas: natural gas", "pre-construction"],
    ["L3", "Hennepin power station", "", "", "United States", "Illinois", "Putnam",
     "41.3032", "-89.3154", "coal: bituminous", "retired"],
]


def new_plant(rid, name, county, lat="", lon=""):
    return {"record_id": rid, "plant_name": name, "country": "United States",
            "fields": {"State/Province": "Illinois", "Local area (taluk, county)": county,
                       "Latitude": lat, "Longitude": lon}, "units": []}


def setup(tmp_path, recs):
    csv_path = tmp_path / "export.csv"
    with open(csv_path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(COLS)
        w.writerows(ROWS)
    batch = tmp_path / "us-il"
    (batch / "staging").mkdir(parents=True)
    (batch / "staging" / "staged_newplants.json").write_text(json.dumps({"records": recs}))
    (batch / "coverage.json").write_text(json.dumps({"sources": {}}))
    return batch, csv_path


def checked(batch, csv_path):
    res = dedup_check.run(batch, csv_path, wiki=False)
    for e in res["records"].values():
        e["wiki"]["status"] = "ok"
    (batch / "dedup.json").write_text(json.dumps(res))
    return res


def lanes(batch):
    return {"newplants": json.loads((batch / "staging" / "staged_newplants.json").read_text())["records"]}


def test_name_county_and_distance_matches(tmp_path):
    recs = [new_plant("a", "Will County Facility power station", "Will"),
            new_plant("b", "Prairie Pulse power station", "LaSalle"),
            new_plant("c", "Putnam County power station", "", "41.31", "-89.32")]
    batch, csv_path = setup(tmp_path, recs)
    res = dedup_check.run(batch, csv_path, wiki=False)["records"]
    assert [h["gem_location_id"] for h in res["a"]["name"]] == ["L1"]
    assert [h["gem_location_id"] for h in res["a"]["nearby"]] == ["L1"]
    assert res["b"]["hits"] == 0, "a one-word match in another state is not a match"
    assert res["c"]["nearby"][0]["gem_location_id"] == "L3" and res["c"]["nearby"][0]["km"] < 2


def test_staged_same_name_and_same_county(tmp_path):
    recs = [new_plant("a", "Ogle County Hub power station", "Ogle"),
            new_plant("b", "Ogle Hub Expansion power station", "Ogle")]
    batch, csv_path = setup(tmp_path, recs)
    res = dedup_check.run(batch, csv_path, wiki=False)["records"]
    assert res["a"]["staged"][0]["record_id"] == "b"


def test_gate_missing_unanswered_answered_stale(tmp_path):
    batch, csv_path = setup(tmp_path, [new_plant("a", "Will County Facility power station", "Will")])
    out, _ = gate_dedup(lanes(batch), batch)
    assert out and "dedup.json is missing" in out[0][1]
    checked(batch, csv_path)
    out, _ = gate_dedup(lanes(batch), batch)
    assert out and "no answer" in out[0][1]
    (batch / "coverage.json").write_text(json.dumps({"sources": {}, "dedup": {
        "a": {"decision": "not_a_duplicate", "evidence": "Different site, 45 km apart."}}}))
    assert gate_dedup(lanes(batch), batch)[0] == []
    (batch / "coverage.json").write_text(json.dumps({"dedup": {"a": {"decision": "duplicate"}}}))
    assert "move the finding" in gate_dedup(lanes(batch), batch)[0][0][1]
    recs = lanes(batch)
    recs["newplants"][0]["plant_name"] = "Will County Energy power station"
    assert "rerun" in gate_dedup(recs, batch)[0][0][1]


def test_gate_wiki_not_run(tmp_path):
    batch, csv_path = setup(tmp_path, [new_plant("a", "Ogle County Hub power station", "Ogle")])
    res = dedup_check.run(batch, csv_path, wiki=False)
    (batch / "dedup.json").write_text(json.dumps(res))
    assert "gem.wiki" in gate_dedup(lanes(batch), batch)[0][0][1]


def test_no_new_plants_passes(tmp_path):
    assert gate_dedup({}, tmp_path)[0] == []

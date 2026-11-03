"""Links never land in the wrong box (North Dakota, 2026-11-03). A finding
keyed on a Data Source column becomes a re-verification of the value column
that box backs; a name column has no Data Source box, so its evidence goes
under the refs key "links"; the build and the gates reject both the old
patterns; repair_staged rule 3 fixes older staging in place."""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import repair_staged  # noqa: E402
from assemble_state import Assembler  # noqa: E402
from build_review_package import ref_col_for, validate, value_cols_for  # noqa: E402
from schema_constants import EVIDENCE_KEY  # noqa: E402
from state_gate import gate_headers, gate_orphans  # noqa: E402

WHERE = {"kind": "state", "name": "North Dakota", "slug": "north_dakota",
         "country": "United States", "postal": "nd"}
HEADER = ["Country/Area", "Plant name", "Unit name", "Other Name(s)", "Status",
          "Status Data Source", "Fuel", "Fuel Data Source", "Capacity (MW)",
          "Capacity Data Source", "Latitude", "Longitude", "Location accuracy",
          "Location Data Source", "City", "State/Province", "GEM location ID", "GEM unit ID"]
OLD = "https://old.example.com/gone.pdf"
NEW = "https://www.psc.nd.gov/docs/nakota-order.pdf"


def test_ref_col_for_never_invents_a_column():
    assert ref_col_for("Fuel") == "Fuel Data Source"
    assert ref_col_for("Fuel Data Source") == "Fuel Data Source"
    assert ref_col_for("Unit name") == EVIDENCE_KEY
    assert ref_col_for("Other Name(s)") == EVIDENCE_KEY
    assert ref_col_for("Plant name") == EVIDENCE_KEY
    assert ref_col_for("Status Detail") == "Status Detail"


def test_value_cols_for_is_the_reverse_map():
    assert value_cols_for("Fuel Data Source") == ["Fuel"]
    assert value_cols_for("Status Data Source") == ["Status"]
    loc = value_cols_for("Location Data Source")
    assert loc[:3] == ["Latitude", "Longitude", "Location accuracy"] and "City" in loc
    assert value_cols_for("Fuel Data Source Data Source") == []


def rec(**over):
    r = {"record_id": "L1:G1:fuel", "gem_plant_id": "L1", "gem_unit_id": "G1",
         "plant_name": "Nakota", "unit_name": "1", "verdict": "fill", "tier": "high",
         "fields": {"Fuel": "fossil gas: natural gas"}, "current": {"Fuel": ""},
         "refs": {"Fuel Data Source": [NEW]},
         "verifications": [{"url": NEW, "ok": True, "contains_value": True}],
         "researcher_notes": "The order names the fuel.", "action": "Fill Fuel."}
    r.update(over)
    return r


def test_validate_and_headers_gate_reject_a_box_as_a_field():
    bad = rec(record_id="L1:G1:fuel-data-source",
              fields={"Fuel Data Source": "fossil gas: natural gas"},
              refs={"Fuel Data Source Data Source": [NEW]})
    errs = validate({"updates": [bad]})
    assert any("Fuel Data Source" in e for e in errs)
    out = gate_headers({"updates": [bad]}, HEADER)
    assert any("not a value" in why for _, why in out)
    assert any("Fuel Data Source Data Source" in why for _, why in out)
    assert gate_headers({"updates": [rec()]}, HEADER) == []
    assert validate({"updates": [rec()]}) == []


def test_headers_gate_rejects_an_invented_name_box_and_accepts_links():
    bad = rec(record_id="L1:G1:unit-name", fields={"Unit name": "CT1"},
              refs={"Unit name Data Source": [NEW]})
    assert any("Unit name Data Source" in why for _, why in gate_headers({"updates": [bad]}, HEADER))
    good = rec(record_id="L1:G1:unit-name", fields={"Unit name": "CT1"}, refs={EVIDENCE_KEY: [NEW]})
    assert gate_headers({"updates": [good]}, HEADER) == []
    assert validate({"updates": [good]}) == []


def test_orphans_gate_lets_a_name_ride_on_the_record_links():
    unit = rec(record_id="L1:G1:new", fields={"Unit name": "CT1", "Capacity (MW)": "100"},
               refs={"Capacity Data Source": [NEW]})
    assert gate_orphans({"newunits": [unit]}) == []
    nameonly = rec(record_id="L1:G1:new", fields={"Unit name": "CT1"}, refs={EVIDENCE_KEY: [NEW]})
    assert gate_orphans({"newunits": [nameonly]}) == []
    bare = rec(record_id="L1:G1:new", fields={"Unit name": "CT1"}, refs={})
    assert [why for _, why in gate_orphans({"newunits": [bare]})] == \
        ["Unit name has a value but the record has no link"]


# --- the assembler ---------------------------------------------------------

def setup(tmp_path):
    (tmp_path / "briefs").mkdir()
    (tmp_path / "shards").mkdir()
    index = {"mode": "update", "where": WHERE, "scope": "ladder", "plants": [
        {"plant_id": "L1", "plant_name": "Nakota", "unit_ids": ["G1"],
         "tasks": {"G1": [{"text": "The Fuel link is gone.", "fields": ["Fuel"], "checks": [15]}]},
         "plant_tasks": []}]}
    (tmp_path / "briefs" / "_index.json").write_text(json.dumps(index), encoding="utf-8")
    csv_path = tmp_path / "export.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        w.writerow(["United States", "Nakota", "1", "", "pre-construction", OLD,
                    "fossil gas: natural gas", OLD, "100", OLD, "47.1", "-101.2", "exact",
                    OLD, "Williston", "North Dakota", "L1", "G1"])
    return csv_path


def finding(value):
    return {"value": value, "refs": [NEW],
            "verifications": [{"url": NEW, "ok": True, "contains_value": True, "name_found": True}],
            "tier": "high", "independent": False,
            "note": "The commission order from June 2026 states the fuel."}


def shard(findings):
    return {"meta": {"plant_id": "L1", "plant_name": "Nakota", "state": "North Dakota",
                     "mode": "update", "model": "sonnet", "done": True},
            "units": [{"gem_unit_id": "G1", "unit_name": "1", "findings": findings,
                       "not_found": [], "notes": "Nothing changed."}],
            "plant_findings": {}, "qa": [], "monitor": [], "newunits": [], "entities": [],
            "source_log": []}


def run(tmp_path, findings):
    csv_path = setup(tmp_path)
    (tmp_path / "shards" / "L1.json").write_text(json.dumps(shard(findings)), encoding="utf-8")
    a = Assembler(tmp_path, csv_path, "2026Q4")
    a.run()
    return a


def test_box_finding_becomes_a_reverification_of_the_value(tmp_path):
    a = run(tmp_path, {"Fuel Data Source": finding("fossil gas: natural gas")})
    recs = a.lanes["updates"]
    assert len(recs) == 1
    r = recs[0]
    assert r["record_id"] == "L1:G1:fuel" and r["reverified"] and r["verdict"] == "match"
    assert r["fields"] == {"Fuel": "fossil gas: natural gas"}
    assert r["refs"] == {"Fuel Data Source": [NEW]}
    assert "Fuel Data Source box" in r["action"] and "Leave Fuel" in r["action"]
    assert a.misplaced_remapped == 1 and a.misplaced_dropped == 0
    assert gate_headers(a.lanes, HEADER) == [] and validate(a.lanes) == []


def test_box_finding_with_a_foreign_value_is_dropped(tmp_path):
    a = run(tmp_path, {"Fuel Data Source": finding("coal")})
    assert a.lanes["updates"] == []
    assert a.misplaced_dropped == 1
    assert any("matches no value" in w for w in a.warnings)


# --- repair rule 3 ------------------------------------------------------------

def write_lane(path, records):
    path.write_text(json.dumps({"records": records}, indent=2), encoding="utf-8")
    return path


def test_repair_rekeys_a_box_record(tmp_path, monkeypatch):
    monkeypatch.setattr(repair_staged.Export, "rows",
                        {"G1": {"Fuel": "fossil gas: natural gas", "Status": "pre-construction"}})
    bad = rec(record_id="L1:G1:fuel-data-source",
              fields={"Fuel Data Source": "fossil gas: natural gas"},
              refs={"Fuel Data Source Data Source": [NEW]})
    p = write_lane(tmp_path / "staged_updates.json", [bad])
    inlined, promoted, problems, rekeyed, named = repair_staged.repair_file(p, True, rules=(3,))
    assert rekeyed == ["L1:G1:fuel-data-source -> L1:G1:fuel"] and not problems
    out = json.loads(p.read_text())["records"]
    assert len(out) == 1
    r = out[0]
    assert r["record_id"] == "L1:G1:fuel" and r["reverified"] and r["verdict"] == "match"
    assert r["fields"] == {"Fuel": "fossil gas: natural gas"} and r["refs"] == {"Fuel Data Source": [NEW]}
    assert "Fuel Data Source box" in r["action"]
    assert gate_headers({"updates": out}, HEADER) == [] and validate({"updates": out}) == []


def test_repair_merges_into_the_twin_and_skips_a_decided_id(tmp_path, monkeypatch):
    monkeypatch.setattr(repair_staged.Export, "rows", {"G1": {"Fuel": "fossil gas: natural gas"}})
    twin = rec(refs={"Fuel Data Source": ["https://www.eia.gov/860m"]})
    bad = rec(record_id="L1:G1:fuel-data-source",
              fields={"Fuel Data Source": "fossil gas: natural gas"},
              refs={"Fuel Data Source Data Source": [NEW]})
    p = write_lane(tmp_path / "staged_updates.json", [twin, bad])
    _, _, problems, rekeyed, _ = repair_staged.repair_file(p, True, rules=(3,))
    assert rekeyed == ["L1:G1:fuel-data-source merged into L1:G1:fuel"]
    out = json.loads(p.read_text())["records"]
    assert len(out) == 1 and out[0]["refs"]["Fuel Data Source"] == ["https://www.eia.gov/860m", NEW]
    # a record a reviewer already decided on is left alone
    (tmp_path / "review_log.jsonl").write_text(
        json.dumps({"record_id": "L1:G1:fuel-data-source", "decision": "accept"}) + "\n")
    p = write_lane(tmp_path / "staged_updates.json", [bad])
    _, _, problems, rekeyed, _ = repair_staged.repair_file(p, True, rules=(3,))
    assert rekeyed == [] and any("review decision" in x for x in problems)
    assert json.loads(p.read_text())["records"][0]["fields"] == bad["fields"]


def test_repair_moves_or_drops_identity_refs(tmp_path):
    kept = rec(record_id="L1:G1:new", fields={"Unit name": "CT1", "Capacity (MW)": "100"},
               refs={"Unit name Data Source": [NEW], "Capacity Data Source": [NEW]},
               action="Add the unit. Add the link below to the Unit name Data Source box. "
                      "Keep the links already there. Then save.")
    moved = rec(record_id="L1:G2:other-name-s", gem_unit_id="G2",
                fields={"Other Name(s)": "Nakota CT"}, refs={"Other Name(s) Data Source": [OLD]})
    p = write_lane(tmp_path / "staged_newunits.json", [kept, moved])
    _, _, problems, rekeyed, named = repair_staged.repair_file(p, True, rules=(3,))
    assert not problems and rekeyed == [] and named == ["L1:G1:new", "L1:G2:other-name-s"]
    out = {r["record_id"]: r for r in json.loads(p.read_text())["records"]}
    assert out["L1:G1:new"]["refs"] == {"Capacity Data Source": [NEW]}
    assert "evidence for the name" in out["L1:G1:new"]["action"]
    assert "Unit name Data Source box" not in out["L1:G1:new"]["action"]
    assert out["L1:G2:other-name-s"]["refs"] == {EVIDENCE_KEY: [OLD]}
    assert gate_headers({"newunits": list(out.values())}, HEADER) == []
    assert gate_orphans({"newunits": list(out.values())}) == []

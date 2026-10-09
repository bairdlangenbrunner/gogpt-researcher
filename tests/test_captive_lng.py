"""The captive LNG sheet step (checklist rows 6 and 44; row 39 for a US state)."""
import csv
import json
import sys
import warnings
from pathlib import Path

import openpyxl
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import captive_lng  # noqa: E402

HEADER = ["Plant name", "GEM location ID", "GEM unit ID", "Unit name", "Country/Area",
          "State/Province", "Status", "Capacity (MW)", "Start year", "Turbine/Engine Technology",
          "CHP", "Owner(s)", "Latitude", "Longitude", "Captive industry use",
          "Captive industry type", "Captive non-industry use", "Wiki URL"]


def _row(name, pid, uid, state, status, cap, lat, lon, use="", typ=""):
    return dict(zip(HEADER, [name, pid, uid, "Unit 1", "United States", state, status, cap, "",
                             "", "", "Owner Co", lat, lon, use, typ, "", ""]))


@pytest.fixture
def fixture_dir(tmp_path):
    # the captive workbook: an Americas pair of tabs and an EU qualifying tab
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Americas - Qualifying (>=50MW)"
    ws.append(["Terminal", "Terminal ID", "Country", "State", "Status", "Hardware Type",
               "Individual Unit MW", "Aggregate/Total MW", "Qualifying Basis", "References"])
    ws.append(["Cove Point LNG Terminal", "T1", "USA", "Maryland", "Operating",
               "2x65 MW steam turbine generators", "65 MW each", "130 MW", "Qualifies both ways",
               "https://dnr.maryland.gov/fact.pdf\nhttps://www.gem.wiki/Cove_Point"])
    ws.append(["Golden Pass LNG Terminal", "T2", "USA", "Texas", "Construction",
               "3x GE Frame 7 mechanical-drive", ">=50 MW (mechanical drive)",
               "n/a (mechanical drive, not summed)", "Individual >=50 MW (mechanical drive)",
               "https://example.org/gp"])
    ws.append(["Freeport LNG Terminal", "T3", "USA", "Texas", "Operating", "one 50 MW unit",
               "~50 MW", "~50 MW", "Individual >=50 MW", "https://example.org/fp"])
    ws.append(["Calcasieu Pass LNG Terminal", "T4", "USA", "Louisiana", "Operating",
               "GOGPT-matched captive power plant", "", "720 MW", "aggregate", ""])
    ws.append(["CP2 LNG Terminal", "T5", "USA", "Louisiana", "Construction",
               "GOGPT-matched captive power plant", "", "2,190 MW", "aggregate", ""])
    ex = wb.create_sheet("Americas - Excluded")
    ex.append(["Terminal", "Terminal ID", "Country", "None", "Reason Excluded", "MW Figure (if any)", "References"])
    ex.append(["Port Pelican LNG Terminal", "T6", "USA", "", "class rating only", "~54 MW", ""])
    eu = wb.create_sheet("EU - Qualifying (>=20MW)")
    eu.append(["Terminal", "Terminal ID", "Hardware Type", "Individual Unit MW", "Aggregate/Total MW",
               "Qualifying Basis", "Turbine/Genset Class", "References"])
    eu.append(["Wilhelmshaven LNG Terminal", "T7", "FSRU gensets", "6 MW", "30 MW", "aggregate", "medium", ""])
    wb.save(tmp_path / "captive_lng.xlsx")
    # the LNG tracker download: Project ID joins; one captive GEM ID; coordinates
    wb2 = openpyxl.Workbook()
    t = wb2.active
    t.title = "LNG tracker"
    t.append(["Researched?", "Captive gas power plant GEM ID (if applicable)", "Additional notes",
              "ProjectID", "UnitID", "Country/Area", "TerminalName", "Status", "FacilityType",
              "Owner", "Parent", "Operator", "Location", "State/Province", "Latitude", "Longitude"])
    t.append(["yes", "", "", "T1", "U1", "United States", "Cove Point LNG Terminal", "Operating",
              "Export", "Dominion", "", "", "Lusby", "Maryland", 38.39, -76.41])
    t.append(["", "", "", "T2", "U2", "United States", "Golden Pass LNG Terminal", "Construction",
              "Export", "QatarEnergy", "", "", "Sabine Pass", "Texas", 29.76, -93.92])
    t.append(["", "", "", "T3", "U3", "United States", "Freeport LNG Terminal", "Operating",
              "Export", "Freeport LNG", "", "", "Freeport", "Texas", 28.93, -95.32])
    t.append(["yes", "L100000000004 ", "", "T4", "U4", "United States", "Calcasieu Pass LNG Terminal", "Operating",
              "Export", "Venture Global", "", "", "Cameron", "Louisiana", 29.77, -93.33])
    t.append(["yes", "L100000000005", "", "T5", "U5", "United States", "CP2 LNG Terminal", "Construction",
              "Export", "Venture Global", "", "", "Cameron", "Louisiana", 29.78, -93.33])
    t.append(["", "", "", "T6", "U6", "United States", "Port Pelican LNG Terminal", "Cancelled",
              "Import", "", "", "", "", "Texas", 28.79, -91.28])
    t.append(["", "", "", "T7", "U7", "Germany", "Wilhelmshaven LNG Terminal", "Operating",
              "Import", "Uniper", "", "", "Wilhelmshaven", "", 53.6, 8.1])
    wb2.save(tmp_path / "lng_tracker.xlsx")
    (tmp_path / "meta.json").write_text(json.dumps({"read": "2026-10-08"}), encoding="utf-8")
    # the scoped export
    rows = [
        _row("Cove Point LNG Terminal power station", "L100000000001", "G1", "Maryland", "operating", "65", 38.39, -76.41,
             "power", "LNG production / liquefaction"),
        _row("Cove Point LNG Terminal power station", "L100000000001", "G2", "Maryland", "operating", "65", 38.39, -76.41,
             "power", "LNG production / liquefaction"),
        _row("Freeport energy center", "L100000000002", "G3", "Texas", "operating", "400", 29.1, -95.4),
        _row("Corpus Christi energy center", "L100000000003", "G4", "Texas", "operating", "500", 27.8, -97.4),
        _row("Calcasieu Pass LNG Terminal power station", "L100000000004", "G5", "Louisiana", "operating", "720", 29.77, -93.33,
             "power", "other"),
        _row("CP2 LNG Terminal power station", "L100000000005", "G6", "Louisiana", "construction", "2190", 29.78, -93.33,
             "power", "LNG production / liquefaction"),
        _row("Lake Charles LNG power station", "L100000000006", "G7", "Louisiana", "proposed", "100", 30.2, -93.2,
             "power", "LNG production / liquefaction"),
        _row("Data Hall power station", "L100000000007", "G8", "Texas", "construction", "200", 32.0, -97.0,
             "power", "data center"),
    ]
    with open(tmp_path / "export.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        w.writeheader()
        w.writerows(rows)
    return tmp_path


def run(fixture_dir, *args):
    out = fixture_dir / "out"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        captive_lng.main([*args, "--csv", str(fixture_dir / "export.csv"),
                          "--from-dir", str(fixture_dir), "--out-dir", str(out)])
    return out


def test_maryland_matches_cove_point_by_name(fixture_dir):
    out = run(fixture_dir, "--state", "Maryland")
    d = json.loads((out / "captive_us-maryland.json").read_text(encoding="utf-8"))
    assert d["read"] == "2026-10-08" and d["threshold_mw"] == 50
    assert [t["terminal_id"] for t in d["terminals"]] == ["T1"]
    t = d["terminals"][0]
    assert t["in_tracker"] and t["tracker_state"] == "Maryland" and not t["mechanical_only"]
    assert t["matches"][0]["plant_id"] == "L100000000001" and t["matches"][0]["confidence"] == "high"
    assert t["refs"] == ["https://dnr.maryland.gov/fact.pdf"]
    assert t["gem_refs"] == ["https://www.gem.wiki/Cove_Point"]
    assert len(d["tasks"]) == 1
    task = d["tasks"][0]
    assert task["plant_id"] == "L100000000001" and task["unit_id"] is None and task["kind"] == "fix"
    assert task["checks"] == [6, 44] and "Capacity (MW)" in task["fields"]
    assert "gem.wiki" not in task["task"]
    assert d["data_center"] == []            # a US state gets the row 39 block
    assert "checklist row 39" in d["brief"]
    assert (out / "captive_us-maryland.md").read_text(encoding="utf-8").startswith("## Captive power")


def test_texas_town_names_do_not_match_and_mechanical_is_flagged(fixture_dir):
    out = run(fixture_dir, "--state", "Texas")
    d = json.loads((out / "captive_us-texas.json").read_text(encoding="utf-8"))
    by_id = {t["terminal_id"]: t for t in d["terminals"]}
    assert set(by_id) == {"T2", "T3", "T6"}
    assert by_id["T2"]["mechanical_only"] and not by_id["T3"]["mechanical_only"]
    # "Freeport energy center" is in the same town but 25 km away: not the terminal's plant
    assert by_id["T3"]["matches"] == []
    assert not by_id["T6"]["qualifying"] and by_id["T6"]["reason_excluded"] == "class rating only"
    assert d["tasks"] == []
    assert "Golden Pass LNG Terminal (T2)" in d["brief"] and "mechanical drive only" in d["brief"]
    assert [p["plant_id"] for p in d["data_center"]] == ["L100000000007"]
    assert "Data Hall power station" in d["brief"]


def test_louisiana_tracker_ids_win_and_neighbors_stay_apart(fixture_dir):
    out = run(fixture_dir, "--state", "Louisiana")
    d = json.loads((out / "captive_us-louisiana.json").read_text(encoding="utf-8"))
    by_id = {t["terminal_id"]: t for t in d["terminals"]}
    # the two terminals sit 1 km apart; each keeps only the plant its tracker row names
    assert [m["plant_id"] for m in by_id["T4"]["matches"]] == ["L100000000004"]
    assert [m["plant_id"] for m in by_id["T5"]["matches"]] == ["L100000000005"]
    assert "ID column" in by_id["T4"]["matches"][0]["matched_by"][0]
    assert {t["plant_id"] for t in d["tasks"]} == {"L100000000004", "L100000000005"}
    # a GEM LNG plant with no sheet row is listed for the LNG team
    assert [p["plant_id"] for p in d["gem_only"]] == ["L100000000006"]
    assert "Lake Charles LNG power station" in d["brief"]


def test_country_scope_uses_eu_threshold_and_no_data_center_block(fixture_dir):
    # add a German plant so the scope has rows
    with open(fixture_dir / "export.csv", "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        r = _row("Wilhelmshaven power station", "L100000000008", "G9", "", "operating", "700", 53.5, 8.1)
        r["Country/Area"] = "Germany"
        w.writerow(r)
    out = run(fixture_dir, "--country", "Germany")
    d = json.loads((out / "captive_germany.json").read_text(encoding="utf-8"))
    assert d["threshold_mw"] == 20
    assert [t["terminal_id"] for t in d["terminals"]] == ["T7"]
    assert d["terminals"][0]["matches"] == []       # 11 km away, name without LNG: no match
    assert d["data_center"] is None and "row 39" not in d["brief"]
    assert "Wilhelmshaven LNG Terminal (T7)" in d["brief"]


def test_sheet_row_missing_from_tracker_falls_back_to_sheet_columns(fixture_dir, capsys):
    wb = openpyxl.load_workbook(fixture_dir / "captive_lng.xlsx")
    wb["Americas - Qualifying (>=50MW)"].append(
        ["Orphan LNG Terminal", "T9", "Puerto Rico (USA)", "", "Proposed", "gensets", "60 MW", "60 MW",
         "aggregate", ""])
    wb.save(fixture_dir / "captive_lng.xlsx")
    out = run(fixture_dir, "--country", "Puerto Rico")
    assert "not in the LNG tracker download: T9" in capsys.readouterr().out
    d = json.loads((out / "captive_puerto-rico.json").read_text(encoding="utf-8"))
    assert [t["terminal_id"] for t in d["terminals"]] == ["T9"]
    assert d["terminals"][0]["in_tracker"] is False


def test_mechanical_only_rule():
    base = {"qualifying": True, "aggregate_mw": "", "basis": ""}
    assert captive_lng.mechanical_only(dict(base, aggregate_mw="n/a (mechanical drive, not summed)"))
    assert captive_lng.mechanical_only(dict(base, basis="Individual >=50 MW (mechanical drive)"))
    assert not captive_lng.mechanical_only(dict(base, basis="Qualifies both ways (generation AND mechanical drive)"))
    assert not captive_lng.mechanical_only(dict(base, qualifying=False, basis="mechanical drive"))

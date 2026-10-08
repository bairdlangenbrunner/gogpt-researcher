"""match_ids.py: the pure matching rules, on synthetic rows (no network, no sheets)."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import match_ids as m  # noqa: E402
from build_state_brief import H_LOC, H_PLANT, H_UNAME, H_UNIT  # noqa: E402


def test_tag_parsing():
    assert m.parse_tags("EIA: 6137, EIP: rec_x") == [("EIA", "6137"), ("EIP", "rec_x")]
    assert m.tag_values("EIA: CT11, EIA: CT12, EIA: ST13", "EIA") == ["CT11", "CT12", "ST13"]
    assert m.tag_values("SEA: GEN1", "EIA") == []
    assert m.gen_eq("0001", "1") and m.gen_eq("GT1", "GT1") and not m.gen_eq("GT1", "GT2")


def test_status_compat():
    assert not m.groups_differ("operating", ["operating", "mothballed"])
    assert not m.groups_differ("mothballed", ["operating", "mothballed"])
    assert m.groups_differ("mothballed", ["retired"])
    assert not m.groups_differ("announced", "pre-construction")
    assert not m.groups_differ("cancelled", ["cancelled", "shelved"])
    assert m.groups_differ("operating", "cancelled")


def test_close_and_names():
    assert m.close(176, 180) and not m.close(176, 198.9)
    assert m.close(10, 14) and not m.close(10, 16)
    assert m.name_sim("Chalk Point Generating Station", "Chalk Point Power") >= 0.5
    assert m.name_sim("Caithness II power station", "SWM Fuel Cell") < 0.3


def gem_row(pid, uid, name, status="operating", cap="100", start="2000", ids="", loc="",
            lat="40.0", lon="-74.0"):
    return {H_LOC: pid, H_UNIT: uid, H_PLANT: "Test plant", H_UNAME: name, "Status": status,
            "Capacity (MW)": cap, "Start year": start, "Other IDs (unit)": ids,
            "Other IDs (location)": loc, "Latitude": lat, "Longitude": lon, "County": "",
            "City": "", "Retired year": "", "Planned retire": "", "Country/Area": "United States",
            "State/Province": "Maryland"}


def eia_rows(rows):
    cols = ["Plant ID", "Plant Name", "Plant State", "County", "Entity Name", "Generator ID",
            "Unit Code", "Nameplate Capacity (MW)", "Technology", "Energy Source Code",
            "Prime Mover Code", "Status", "Operating Year", "Planned Operation Year",
            "Retirement Year", "Planned Retirement Year", "Latitude", "Longitude", "sheet"]
    return pd.DataFrame([dict(zip(cols, r)) for r in rows], columns=cols)


def make(plants, gens, eip=None, sc=None):
    scope = {"name": "Maryland", "postal": "MD", "slug": "maryland", "kind": "state",
             "country": "United States"}
    for p in plants.values():
        first = p["rows"][0]
        p.setdefault("eia", m.tag_values(first["Other IDs (location)"], "EIA"))
        p.setdefault("eip", m.tag_values(first["Other IDs (location)"], "EIP"))
        p.setdefault("lat", m.num(first["Latitude"]))
        p.setdefault("lon", m.num(first["Longitude"]))
        p.setdefault("county", "")
        p.setdefault("city", "")
        p.setdefault("cap", sum(m.num(r["Capacity (MW)"]) or 0 for r in p["rows"]))
        p.setdefault("groups", {m.gem_group(r["Status"]) for r in p["rows"]})
        p.setdefault("other_ids", first["Other IDs (location)"])
    return m.Match(scope, plants, set(), gens, {"file": "august_generator2026.xlsx"},
                   eip or {"tab": "t", "date": "2026-07-28", "rows": []},
                   sc or {"tab": "MATCHED IDs", "status_col": "April '26 Status", "rows": []})


def test_eia_status_capacity_and_split_code():
    plants = {
        "L1": {"id": "L1", "name": "Chalk Point Generating Station", "rows": [
            gem_row("L1", "G1", "3", status="operating", cap="659", start="1975",
                    ids="EIA: 3", loc="EIA: 65285", lat="38.54", lon="-76.68"),
            gem_row("L1", "G2", "GT3", status="mothballed", cap="90", start="1991",
                    ids="EIA: GT3", loc="EIA: 65285", lat="38.54", lon="-76.68")]},
        "L2": {"id": "L2", "name": "Rock Springs station", "rows": [
            gem_row("L2", "G3", "2", cap="176", start="2003", ids="EIA: 2",
                    loc="EIA: 7835", lat="39.7", lon="-76.1")]},
    }
    gens = eia_rows([
        ["65285", "Chalk Point Steam", "MD", "Prince Georges", "X", "1", "", 340, "Coal",
         "BIT", "ST", "", 1964, None, 2021, None, 38.54, -76.68, "Retired"],
        ["1571", "Chalk Point Power", "MD", "Prince Georges", "X", "3", "", 659,
         "Natural Gas Steam Turbine", "NG", "ST", "(OP) Operating", 1975, None, None, None,
         38.54, -76.68, "Operating"],
        ["1571", "Chalk Point Power", "MD", "Prince Georges", "X", "GT3", "", 90,
         "Natural Gas Fired Combustion Turbine", "NG", "GT", "(OP) Operating", 1991, None,
         None, None, 38.54, -76.68, "Operating"],
        ["7835", "Rock Springs", "MD", "Cecil", "Y", "2", "", 198.9,
         "Natural Gas Fired Combustion Turbine", "NG", "GT", "(OP) Operating", 2003, None,
         None, None, 39.7, -76.1, "Operating"],
    ])
    mt = make(plants, gens)
    mt.run_eia()
    adds = [(i["plant_id"], i["add"]) for i in mt.ids_to_add]
    assert ("L1", "EIA: 1571") in adds            # the split code, not a lead
    assert not [d for d in mt.leads if d["ids"] == "EIA: 1571"]
    sections = {(t["plant_id"], t["unit_id"], t["section"]) for t in mt.tasks}
    assert ("L2", "G3", "Capacity") in sections   # 176 vs 198.9
    assert ("L1", "G2", "Status") in sections     # mothballed vs operating
    assert ("L1", "G1", "Status") not in sections


def test_eia_lead_and_unit_id_proposal():
    plants = {"L1": {"id": "L1", "name": "Wagner Generating Station", "rows": [
        gem_row("L1", "G1", "Unit 3, timepoint 2", cap="359", start="2023", loc="EIA: 1554",
                lat="39.18", lon="-76.53")]}}
    gens = eia_rows([
        ["1554", "Herbert A Wagner", "MD", "Anne Arundel", "Z", "3", "", 359,
         "Petroleum Liquids", "DFO", "ST", "(OP) Operating", 1966, None, None, None,
         39.18, -76.53, "Operating"],
        ["58207", "White Oak CUP", "MD", "Montgomery", "GSA", "G1", "", 60,
         "Natural Gas Internal Combustion Engine", "NG", "IC", "(OP) Operating", 2003, None,
         None, None, 39.03, -76.98, "Operating"],
    ])
    mt = make(plants, gens)
    mt.run_eia()
    # the conversion unit takes generator 3 even though the years differ
    assert [i["add"] for i in mt.ids_to_add if i["unit_id"] == "G1"] == ["EIA: 3"]
    assert [d["name"] for d in mt.leads] == ["White Oak CUP"]


def test_sierra_club_rows():
    plants = {"L1": {"id": "L1", "name": "Roseton generating facility", "rows": [
        gem_row("L1", "G1", "1", cap="600", start="1974", ids="EIA: 1", loc="EIA: 8006")]}}
    gens = eia_rows([
        ["8006", "Roseton", "NY", "Orange", "Q", "1", "", 600, "Natural Gas Steam Turbine",
         "NG", "ST", "(OP) Operating", 1974, None, None, None, 41.6, -74.0, "Operating"]])
    sc = {"tab": "MATCHED IDs", "status_col": "April '26 Status", "rows": [
        # a terminated repowering matched to the plant but not to a unit
        {"State": "MD", "Power Plant": "Roseton CC", "Unit Code": "1A", "ORIS Code": "8006",
         "GEM Location ID": "L1", "GEM Unit ID": "", "April '26 Status": "Terminated",
         "Check against Jan 26 SC data": "no changes", "Unit Nameplate Capacity (MW)": "600"},
        # the real unit, blank in the sheet: a fill, and a check flag
        {"State": "MD", "Power Plant": "Roseton", "Unit Code": "1", "ORIS Code": "8006",
         "GEM Location ID": "", "GEM Unit ID": "", "April '26 Status": "Operating",
         "Check against Jan 26 SC data": "CHECK- owner change",
         "Unit Nameplate Capacity (MW)": "600"},
        # a live row with no GEM match at all
        {"State": "MD", "Power Plant": "Somewhere New", "Unit Code": "1", "ORIS Code": "0",
         "GEM Location ID": "", "GEM Unit ID": "", "April '26 Status": "Planned",
         "Check against Jan 26 SC data": "ADDED", "Unit Nameplate Capacity (MW)": "300"},
        {"State": "MD", "Power Plant": "Old thing", "Unit Code": "1", "ORIS Code": "0",
         "GEM Location ID": "excluded", "GEM Unit ID": "", "April '26 Status": "Operating",
         "Check against Jan 26 SC data": "no changes", "Unit Nameplate Capacity (MW)": "3"},
    ]}
    mt = make(plants, gens, sc=sc)
    mt.run_sc()
    kinds = [(t["unit_id"], t["section"]) for t in mt.tasks]
    assert (None, "Unit 1A") in kinds             # not a status task on unit 1
    assert ("G1", "Check") in kinds
    assert ("G1", "Status") not in kinds
    fills = mt.sheet_fills["sierra_club"]
    assert len(fills) == 1 and fills[0]["gem_unit_id"] == "G1"
    assert [d["name"] for d in mt.leads] == ["Somewhere New"]
    for t in mt.tasks:
        assert "never cite the Sierra Club" in t["task"]


def test_eip_rows():
    plants = {"L1": {"id": "L1", "name": "Caithness II power station", "rows": [
        gem_row("L1", "G1", "1", status="announced", cap="600", start="2028",
                loc="EIP: rec_old, EIP: rec_old")]}}
    gens = eia_rows([])
    eip = {"tab": "t", "date": "2026-07-28", "rows": [
        {"facility__state": "MD", "facility__id": "abc-uuid", "facility__facility_name":
         "Caithness II Power Station", "facility__gaspower_gemlocationid": "L1",
         "project__gaspower_gemunitid": "G1", "GEM Location ID (for EIP blanks)": "",
         "GEM Unit ID (for EIP blanks)": "", "project__operatingstatus": "On Hold",
         "project__gaspower_generatingcapacity_mw": "600", "OGWLink": "https://x/abc",
         "project__currentexpectedoperatingyear": "2030", "GEM Notes": ""}]}
    mt = make(plants, gens, eip=eip)
    mt.run_eip()
    assert [i["add"] for i in mt.ids_to_add] == ["EIP: abc-uuid"]
    assert "older EIP record id rec_old" in mt.ids_to_add[0]["basis"]
    assert any("repeats the same EIP id" in x for x in mt.problems)
    sections = {t["section"] for t in mt.tasks}
    assert "Status" in sections and "Start year" in sections

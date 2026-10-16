"""Brief tasks for checklist rows the gap list did not cover: conversion naming,
fuel, technology and start year (rows 12 and 13), waste heat (row 14), start
year on shelved or cancelled units (row 20), and the last-minute status pass
for operating units under --scope all (rows 49, 50 and 43)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from build_state_brief import unit_tasks  # noqa: E402

BASE = {"Status": "operating", "Fuel": "fossil gas: natural gas",
        "Turbine/Engine Technology": "steam turbine", "Owner(s)": "Utility Co [100%]",
        "Capacity (MW)": "100", "Start year": "2016", "Unit name": "Unit 1",
        "Latitude": "41.0", "Longitude": "-93.0", "Location accuracy": "exact",
        "City": "Ames", "Other IDs (location)": "EIA: 1", "Other IDs (unit)": "EIA: 1"}


def row(**kw):
    r = dict(BASE)
    r.update({k.replace("_", " "): v for k, v in kw.items()})
    return r


def checks(tasks):
    return [c for _, _, cs in tasks for c in cs]


def conv(**kw):
    r = row(**kw)
    r["Conversion/replacement?"] = kw.get("conv", "conversion")
    r["Conversion from/replacement of (fuel)"] = kw.get("from_fuel", "coal: bituminous")
    r["Conversion from/replacement of (GEM unit ID)"] = kw.get("from_uid", "G1")
    return r


def test_plain_operating_unit_has_no_task_in_ladder_scope():
    assert unit_tasks(row(), year=2026) == []


def test_conversion_without_timepoint_in_name():
    t = unit_tasks(conv(), year=2026)
    assert 12 in checks(t)


def test_malformed_timepoint_name():
    t = unit_tasks(conv(**{"Unit name": "Unit 4- timepoint 2"}), year=2026)
    assert any("timepoint form" in x for x, _, _ in t)
    ok = unit_tasks(conv(**{"Unit name": "Unit 4, timepoint 2"}), year=2026)
    assert 12 not in checks(ok)


def test_timepoint_name_with_blank_conversion_fields():
    t = unit_tasks(row(**{"Unit name": "Unit 1, timepoint 2"}), year=2026)
    assert any("Conversion/replacement?" in f for _, f, _ in t)


def test_coal_conversion_with_coal_technology():
    r = conv(**{"Unit name": "Unit 1, timepoint 2", "Turbine/Engine Technology": "subcritical"})
    t = unit_tasks(r, year=2026)
    assert [c for c in checks(t)] == [13]


def test_gas_start_before_coal_retirement():
    r = conv(**{"Unit name": "Unit 7, timepoint 2", "Start year": "1968"})
    peers = {"G1": {"Retired year": "2015"}}
    t = unit_tasks(r, year=2026, peers=peers)
    assert any("earlier than the coal unit" in x for x, _, _ in t)
    later = unit_tasks(conv(**{"Unit name": "Unit 7, timepoint 2", "Start year": "2016"}),
                       year=2026, peers=peers)
    assert later == []


def test_waste_heat_not_steam_turbine():
    r = row(Fuel="waste heat from natural gas", **{"Turbine/Engine Technology": "gas turbine"})
    assert 14 in checks(unit_tasks(r, year=2026))


def test_start_year_on_cancelled_unit():
    r = row(Status="cancelled", **{"Cancellation year": "2022"})
    assert 20 in checks(unit_tasks(r, year=2026))
    r = row(Status="cancelled", **{"Cancellation year": "2022", "Start year": ""})
    assert 20 not in checks(unit_tasks(r, year=2026))


def test_status_pass_only_under_scope_all():
    t = unit_tasks(row(), year=2026, status_pass=True)
    assert checks(t) == [50, 43]
    assert "Owner(s)" in t[0][1]


def test_construction_task_carries_row_49():
    r = row(Status="construction", **{"Start year": "2027"})
    t = unit_tasks(r, year=2026)
    assert 49 in checks(t) and 10 in checks(t)

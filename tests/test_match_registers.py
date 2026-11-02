"""Offline tests for scripts/match_registers.py: saved rows of the EEA large combustion plant table and
an ENTSO-E unit document, no network."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import match_registers as m  # noqa: E402


def rows(lcp, name, city, lat, lon, mw, gas, coal=0.0, year=2024):
    base = {"LCPInspireId": lcp, "installationPartName": name, "City_Of_Facility": city,
            "Latitude": lat, "Longitude": lon, "reportingYear": year}
    out = [dict(base, featureType="LCPCharacteristics", unit="MW", featureValue=mw),
           dict(base, featureType="NaturalGas", unit="TJ", featureValue=gas),
           dict(base, featureType="Coal", unit="TJ", featureValue=coal)]
    return out


EEA = pd.DataFrame(
    rows("PL/1", "CCGT Grudziądz Sp. z o.o. - O-1", "Grudziądz", 53.47, 18.75, 1000, 9000)
    + rows("PL/2", "PGE GiEK - Oddział Elektrociepłownia Kielce - O-2", "Kielce", 50.87, 20.68, 193.5, 3000)
    + rows("PL/3", "OGP Gaz-System S.A. - Hołowczyce - O-3", "Klepaczew", 52.1, 23.2, 71, 500)
    + rows("PL/4", "Ciepłownia centralna K-173 w Opolu - O-4", "Opole", 50.68, 17.92, 90, 400)
    + rows("PL/5", "Elektrownia Węglowa - O-5", "Nowhere", 51.0, 19.0, 900, 50, coal=20000)
    + rows("PL/1", "CCGT Grudziądz Sp. z o.o. - O-1", "Grudziądz", 53.47, 18.75, 1000, 1, year=2023))

PLANTS = [{"id": "L100000401438", "name": "Grudziądz power station", "city": "Grudziądz", "lat": 53.475, "lon": 18.752,
           "cap": 560.0, "units": {"G1": {"name": "1", "cap": 560.0, "status": "construction"}},
           "eic": {"19W000000000035B": "G1"}}]


def test_parts_keep_newest_year_and_gas_share():
    parts = {p["lcp_id"]: p for p in m.parts_from_rows(EEA)}
    assert parts["PL/1"]["year"] == 2024 and parts["PL/1"]["fuels_tj"]["NaturalGas"] == 9000
    assert parts["PL/5"]["gas_share"] == 0.0


def test_classify_parts():
    parts = {p["lcp_id"]: m.classify_part(p) for p in m.parts_from_rows(EEA)}
    assert parts == {"PL/1": "power", "PL/2": "power", "PL/3": "mechanical", "PL/4": "heat_only", "PL/5": "power"}


def test_build_matches_by_distance_and_leads_only_power_plants():
    units = [{"eic": "19W000000000035B", "name": "Grudziadz 1", "mw": 600.0, "fuel": "fossil gas"},
             {"eic": "19W000000000999X", "name": "New CCGT", "mw": 450.0, "fuel": "fossil gas"}]
    d = m.build("Poland", PLANTS, m.parts_from_rows(EEA), units, "2026-10-29")
    assert [x["plant_id"] for x in d["eea_matches"]] == ["L100000401438"]
    assert {x["ids"] for x in d["leads"]} == {"PL/2", "ENTSO-E: 19W000000000999X"}
    assert all(x["capacity_mw"] is None for x in d["leads"] if x["source"] == "eea")
    assert len(d["tasks"]) == 0      # 600 vs 560 is within 10 percent
    units[0]["mw"] = 700.0
    d = m.build("Poland", PLANTS, m.parts_from_rows(EEA), units, "2026-10-29")
    assert d["tasks"][0]["unit_id"] == "G1" and "not cited for nameplate" in d["tasks"][0]["task"]
    assert d["where"] == {"kind": "country", "name": "Poland", "slug": "poland"}


def test_parse_entsoe_units():
    xml = ("<TimeSeries><registeredResource.mRID codingScheme=\"A01\">19W000000000035B</registeredResource.mRID>"
           "<registeredResource.name>GRUDZIADZ</registeredResource.name><Period><Point><quantity>563.3</quantity>"
           "</Point></Period></TimeSeries>")
    assert m.parse_entsoe(xml, "fossil gas") == [{"eic": "19W000000000035B", "name": "GRUDZIADZ", "mw": 563.3,
                                                  "fuel": "fossil gas"}]

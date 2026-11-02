"""Offline tests for scopes/poland/harvest_pse.py: saved rows of the PSE connection list and saved text
of three capacity auction results PDFs (2026, 2028 and 2030 layouts), no network."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scopes" / "poland"))
import harvest_pse as h  # noqa: E402


def row(oid, name, applicant, station, kind, inj, drawn, other, stage, conditions=None):
    r = [None] * 27
    r[0], r[1], r[3], r[4], r[7], r[8], r[9], r[15], r[16], r[19] = (
        oid, name, applicant, station, kind, inj, drawn, other, stage, conditions)
    return r


CONN = [
    row("-", "Blok Gazowy Pątnów Blok nr 9", "ZE PAK S.A.", "Pątnów", "BG", 464, 0, 464,
        "WARUNKI PRZYŁĄCZENIA wydane", "10.12.2025"),
    row("-", "Bloki Gazowo-Parowy CCGT Pątnów 1 i Pątnów 2 ", "ZE PAK S.A.", "Pątnów", "BGP", 1830, 0, "2x915",
        "WARUNKI PRZYŁĄCZENIA wydane"),
    row("-", "SD Duszniki", "Kogeneracja Szamotuły S.A.", "Plewiska", "OSD", 270.2484, 25, "-",
        "UMOWA O PRZYŁĄCZENIE obowiązująca"),
    row("-", "MEE Połaniec", "Magazyn Energii Tursko Wielkie", "Połaniec", "MEE", 70, 71.4, "-",
        "UMOWA O PRZYŁĄCZENIE obowiązująca"),
    row("-", "OCGT Peaker Połaniec", "Enea Elektrownia Połaniec S.A.", "Połaniec", "BG", 257.04, 0, 257.04,
        "WARUNKI PRZYŁĄCZENIA wydane"),
    row("-", "JGP CCGT Turów", "PGE Inwest 35 Sp. z o.o.", "Mikułowa", "BGP", 550, 0, 550,
        "WARUNKI PRZYŁĄCZENIA wydane"),
]

A2026 = """
  1.   JRM/601     nowa jednostka rynku mocy wytwórcza           518,370       17    CCGT Grudziądz sp. z o.o.         5842739599

  2.   JRM/700     istniejąca jednostka rynku mocy wytwórcza     278,000        1    Polski Koncern Naftowy ORLEN S.A.           7740001454
"""

A2028 = """
                                                  wytwórcza
                                                  nowa jednostka rynku mocy
29.    JRM/996     CHP Żory                                                                  2,924      5        ENGAZ ŻORY sp. z o.o.      9532652877
                                                  wytwórcza
                                                   istniejąca jednostka rynku mocy
96.     JRM/234     CCGT Włocławek                                                          300,000      1        ORLEN S.A.                        7740001454
                                                   wytwórcza
"""

A2030 = """
130.    JRM/125     modernizowana jednostka rynku mocy wytwórcza        4,986             7          PGE Energia Odnawialna S.A.                 5270019532
132.   JRM/2129     nowa jednostka rynku mocy wytwórcza                548,859            15         PGE Inwest 28 sp. z o.o.                    7011262836
133.   JRM/3000     nowa jednostka rynku mocy wytwórcza                 12,000            17         Magazyn Energii Sp. z o.o.                  1234567890
134.   JRM/3001     nowa jednostka rynku mocy wytwórcza                 50,000            17         Zahraniczni Dodavatel a.s.                  CZ12345678
"""

PLANTS = [
    {"id": "L100000401438", "name": "Grudziądz power station", "city": "Grudziądz", "known": ["grudziadz"]},
    {"id": "L100000103272", "name": "Polaniec power station", "city": "Tursko Małe", "known": ["polaniec"]},
    {"id": "L100000400812", "name": "Włocławek power station", "city": "Włocławek", "known": ["wloclawek"]},
]


def test_fold_handles_polish_letters():
    assert h.fold("Łaziska  Górne Pątnów") == "laziska gorne patnow"


def test_connection_list_keeps_gas_and_reads_block_pairs():
    es = {e["project_name"]: e for e in h.conn_entries(CONN)}
    assert set(es) == {"Blok Gazowy Pątnów Blok nr 9", "Bloki Gazowo-Parowy CCGT Pątnów 1 i Pątnów 2",
                       "OCGT Peaker Połaniec", "JGP CCGT Turów"}
    assert es["Bloki Gazowo-Parowy CCGT Pątnów 1 i Pątnów 2"]["mw"] == 1830
    p9 = es["Blok Gazowy Pątnów Blok nr 9"]
    assert p9["facility_type"] == "gas block" and p9["dates"]["conditions"] == "2025-12-10"
    assert p9["status"].startswith("connection conditions issued")


def test_installed_reads_pairs():
    assert h.installed("2x915") == 1830 and h.installed("279,5E") == 279.5 and h.installed("-") is None


def test_auction_rows_same_line_layout():
    rows = h.auction_rows(A2026, 2026, "u")
    assert [(r["code"], r["kind"], r["obligation"], r["years"]) for r in rows] == [
        ("JRM/601", "new unit", 518.37, 17), ("JRM/700", "existing unit", 278.0, 1)]
    assert rows[0]["supplier"] == "CCGT Grudziądz sp. z o.o." and not rows[0]["foreign"]


def test_auction_rows_wrapped_type_and_unit_name():
    rows = {r["code"]: r for r in h.auction_rows(A2028, 2028, "u")}
    assert rows["JRM/996"]["kind"] == "new unit" and rows["JRM/996"]["name"] == "CHP Żory"
    assert rows["JRM/234"]["kind"] == "existing unit" and rows["JRM/234"]["name"] == "CCGT Włocławek"


def test_auction_entries_never_carry_nameplate():
    es = {e["queue_id"]: e for e in h.auction_entries(h.auction_rows(A2026 + A2030, 2030, "u"))}
    assert set(es) == {"JRM/601 (2030)", "JRM/2129 (2030)"}   # existing, upgrade, storage, foreign dropped
    assert all(e["mw"] is None for e in es.values())
    assert es["JRM/601 (2030)"]["gas_oil"] and es["JRM/2129 (2030)"]["fuel_unknown"]
    assert "not nameplate" in es["JRM/2129 (2030)"]["status"]


def test_matching_prefers_named_patterns():
    entries = h.conn_entries(CONN) + h.auction_entries(h.auction_rows(A2026, 2026, "u"))
    by_plant, matched = h.match_all(PLANTS, entries)
    names = {entries[i]["project_name"] for i in by_plant["L100000103272"]}
    assert names == {"OCGT Peaker Połaniec"}
    assert [entries[i]["queue_id"] for i in by_plant["L100000401438"]] == ["JRM/601 (2026)"]
    assert not any(entries[i]["project_name"] == "JGP CCGT Turów" for i in matched)


def test_auction_links_prefer_final_results():
    html = ('<a href="/documents/20182/4028918961/Wst%C4%99pne+wyniki+aukcji+g%C5%82%C3%B3wnej+2028">x</a>'
            '<a href="/documents/20182/4028918961/Ostateczne+wyniki+aukcji+g%C5%82%C3%B3wnej+na+2028">y</a>'
            '<a href="https://www.pse.pl/documents/20182/98611984/2018-10-31_Instrukcja_Uzytkownika_PURM_Aukcje.pdf">z</a>')
    links = h.auction_links(html, "https://www.pse.pl/aukcja-glowna-na-rok-dostaw-2028")
    assert links == ["https://www.pse.pl/documents/20182/4028918961/Ostateczne+wyniki+aukcji+g%C5%82%C3%B3wnej+na+2028"]

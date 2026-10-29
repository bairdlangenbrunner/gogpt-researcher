"""Offline tests for harvest_psc_mississippi.py: saved snippets of a monthly docket PDF
(pdftotext -layout), portal rows and document text, no network and no Chrome."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import harvest_psc_mississippi as h  # noqa: E402

AGENDA = """\
2024-UA-18                                                  IN RE: PETITION OF ENTERGY MISSISSIPPI, LLC FOR A
ENTERGY MISSISSIPPI, LLC                                    CERTIFICATE OF PUBLIC CONVENIENCE AND NECESSITY FOR
                                                            A COMBINED CYCLE GAS TURBINE AT BAXTER WILSON  Filing Date: 3/4/24
2019-UN-1                                                   IN RE: NOTICE OF TOWN OF UTICA OF INTENT TO CHANGE
CITY OF UTICA                                               RATES FOR GAS SERVICE
                                                            Filing Date: 1/2/19
"""


def test_parse_docket_list():
    r = h.parse_docket_list(AGENDA)
    assert set(r) == {"2024-UA-18", "2019-UN-1"}
    a = r["2024-UA-18"]
    assert a["utility"] == "ENTERGY MISSISSIPPI, LLC"
    assert "COMBINED CYCLE GAS TURBINE AT BAXTER WILSON" in a["title"]
    assert "Filing Date" not in a["title"] and a["filed"] == "3/4/24"


def test_agenda_urls_filters_year_and_kind():
    page = ('<a href=/sites/default/files/2024-05/2024-05-UTILITY-DOCKET.pdf class="x">'
            '<a href=/sites/default/files/2021-05/2021-05-UTILITY-DOCKET.pdf>'
            '<a href=/sites/default/files/2024-05/something-else.pdf>')
    assert h.agenda_urls(page, 2022) == ["https://www.psc.ms.gov/sites/default/files/2024-05/2024-05-UTILITY-DOCKET.pdf"]


def test_parse_search_page():
    html_text = ("$.ajaxSetup({headers: {X-Valence-CSRF-Token: 'tok123'}}); "
                 '{"url":"/WidgetManagement/GenericGrid/ExecuteSearchProc2?a=b\\u0026c=d"}')
    assert h.parse_search_page(html_text) == ("tok123", "/WidgetManagement/GenericGrid/ExecuteSearchProc2?a=b&c=d")


def row(i, seq, name, comment, pages=5, num="0018", typ="UA", year=2024, date="/Date(1709510400000)/"):
    return {"Id": i, "DocYear": year, "DocType": typ, "DocNum": num, "DocSequence": seq, "DisplayName": name,
            "Comments": comment, "FilePageCount": pages, "DateReceived": date, "FileName": f"f{seq}.pdf",
            "DocumentTypeName": "Petition"}


ROWS = [
    row(1, 1, "Entergy Mississippi, LLC", "IN RE: PETITION OF ENTERGY MISSISSIPPI FOR A CERTIFICATE OF PUBLIC "
        "CONVENIENCE AND NECESSITY FOR A COMBINED CYCLE GAS TURBINE AT BAXTER WILSON"),
    row(2, 2, "Entergy Mississippi, LLC", "Direct testimony"),
    row(3, 1, "Gulf Coast Water", "IN RE: WATER RATES", num="0005", typ="UN"),
    row(4, 1, "Mississippi Power Company", "IN RE: SOLAR ARRAY AT A SCHOOL", num="0007"),
]


def test_group_and_docket_key():
    ds = {d["docket"]: d for d in h.group_dockets(ROWS)}
    assert set(ds) == {"2024-UA-18", "2024-UN-5", "2024-UA-7"}
    d = ds["2024-UA-18"]
    assert d["utility"] == "Entergy Mississippi, LLC" and d["title"].startswith("IN RE: PETITION")
    assert d["filed"] == "2024-03-04"
    assert [r["DocSequence"] for r in d["rows"]] == [1, 2]


def test_classify_generation_dockets():
    ds = {d["docket"]: d for d in h.group_dockets(ROWS)}
    rel, key, reasons, _ = h.classify(ds["2024-UA-18"])
    assert rel and key and reasons
    assert h.classify(ds["2024-UN-5"])[0] is False
    assert h.classify(ds["2024-UA-7"])[1] is False


DOC = """\
Entergy Mississippi proposes to build a 754 MW combined cycle plant at the Baxter Wilson site in Warren County,
Mississippi. The plant will use two General Electric 7HA.03 combustion turbines. Commercial operation is expected in 2028.
Baxter Wilson Unit 1 will retire in 2027 once the new unit is in service. The site is located near Vicksburg.
Baxter Wilson Unit 1        2027     371 MW
Plant Sweatt                2029     100 MW
"""


def test_doc_facts():
    f = h.doc_facts(DOC.replace("\n", " "), DOC)
    assert any("754 MW" in x for x in f["megawatts"])
    assert any("7HA" in x for x in f["equipment_maker_model"])
    assert any("2028" in x for x in f["in_service"])
    assert any("retire in 2027" in x for x in f["retirement"])
    assert "combined cycle" in f["technology"]
    assert any("Warren County" in x for x in f["location"])
    assert any("Plant Sweatt" in x for x in f["resource_plan_table_lines"])
    assert h.LATLON.search("32.3456, -90.8765")


def test_pick_docs_prefers_orders_and_petitions():
    rows = [row(i, i, "x", c, pages=p) for i, (c, p) in enumerate(
        [("cover letter", 1), ("Order granting certificate", 12), ("Direct testimony", 30), ("proof of publication", 1)], 1)]
    got = h.pick_docs(rows, 2)
    assert len(got) == 2 and {r["Comments"] for r in got} <= {"Order granting certificate", "Direct testimony", "cover letter"}
    assert "proof of publication" not in {r["Comments"] for r in got}


PLANTS = [
    {"id": "L100000401922", "name": "Baxter Wilson power station", "city": "Vicksburg", "county": "warren",
     "owner": "", "statuses": [], "name_words": set()},
    {"id": "L100000402097", "name": "Victor J Daniel Jr power station", "city": "Escatawpa", "county": "jackson",
     "owner": "", "statuses": [], "name_words": set()},
]


def test_match_all_title_and_text_and_noise():
    ds = h.group_dockets(ROWS)
    for d in ds:
        d["relevant"], d["key"], d["reasons"], d["comments_text"] = h.classify(d)
        d["facts"], d["text_blob"] = {}, ""
    by_plant, matched = h.match_all(PLANTS, ds)
    assert by_plant["L100000401922"] == ["2024-UA-18"]
    assert by_plant["L100000402097"] == []
    # a person's first name "daniel" in text alone must not match Plant Daniel
    ds[0]["text_blob"] = "witness daniel smith testified"
    assert h.match_docket(PLANTS[1], ds[0]) is None
    ds[0]["text_blob"] = "Plant Daniel unit 3 and Plant Daniel unit 4 and Plant Daniel unit 1"
    assert "named 3 times" in h.match_docket(PLANTS[1], ds[0])


def test_ms_date_forms():
    assert h.ms_date("/Date(1709510400000)/") == "2024-03-04"
    assert h.ms_date("2024-03-04T00:00:00") == "2024-03-04"
    assert h.ms_date(None) == ""


def test_label_sequences_do_not_break_grouping():
    rows = [row(1, "ORDER ", "Entergy Mississippi, LLC", "Final order"), row(2, 1, "Entergy Mississippi, LLC", "IN RE: X")]
    d = h.group_dockets(rows)[0]
    assert len(d["rows"]) == 2 and h.seq_int({"DocSequence": "ORDER "}, 99) == 99


def test_wires_dockets_are_not_key():
    d = h.group_dockets([row(9, 1, "Entergy Mississippi, LLC",
                             "IN RE: PETITION FOR A CERTIFICATE OF PUBLIC CONVENIENCE AND NECESSITY FOR A 115 KV TRANSMISSION LINE",
                             num="0044")])[0]
    rel, key, _, _ = h.classify(d)
    assert rel and not key

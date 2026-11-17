"""Offline tests for scopes/us-nm/harvest_prc.py: the case rows, classification, document
choice, request bodies, fact extraction and plant matching. No network. The fixtures are saved
PRCe360 answers (tests/fixtures/prc_new_mexico/) with filer names removed."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from paths import load_scope_module  # noqa: E402

h = load_scope_module("us-nm", "harvest_prc")
FIX = Path(__file__).resolve().parent / "fixtures" / "prc_new_mexico"
CASES = json.loads((FIX / "getAllCases.json").read_text())
DOCS = json.loads((FIX / "getAllDocuments.json").read_text())


def rows():
    return {r["docket"]: r for r in (h.case_row(x) for x in CASES["items"])}


def test_case_rows():
    r = rows()
    assert len(r) == 12
    c = r["25-00076-UT"]
    assert c["filed"] == "2025-11-18" and c["utility"] == "Southwestern Public Service Company"
    assert "2026 INTEGRATED RESOURCE PLAN" in c["title"]
    assert c["url"].endswith("screen=external-Case360&caseId=" + c["case_id"]) and c["case_id"]
    assert "\n" not in r["24-00260-UT"]["title"]            # a caption with line breaks becomes one line
    assert "filer" not in str(r)


def test_classify():
    r = rows()
    got = {k: h.classify(v)[:2] for k, v in r.items()}
    assert got["25-00076-UT"] == (True, True) and got["25-00022-UT"] == (True, True) and got["24-00260-UT"] == (True, True)
    assert got["26-0000114"] == (True, True)                # PPAs, a certificate and the Four Corners abandonment
    assert got["26-0000183"] == (True, True)                # a data center pilot tariff
    assert got["26-0000163"] == (False, False)              # a telephone company registration
    assert got["26-0000193"] == (False, False)              # an advice notice
    assert got["26-0000145"][1] is False                    # a planning rule, not a plant
    assert got["26-0000137"][1] is False and got["26-0000071"][1] is False   # a line and a DC converter, not a plant
    assert h.classify({"docket": "23-00403-UT", "title": "", "category": "", "utility": ""}) [:2] == (True, True)


def test_request_bodies():
    b = h.search_body("abandon", 2, 100)
    assert b["pageNo"] == 2 and b["pageSize"] == 100 and b["parameters"] == {"screen": "external-Dashboard", "searchTerm": "abandon"}
    assert b["gridInput"]["params"]["parameters"]["searchTerm"] == "abandon" and b["origin_key"] == "CaseX"
    d = h.docs_body("abc", 1, 100)
    assert d["parameters"] == {"caseId": "abc", "searchTerm": ""} and d["queryParams"] == ["caseId"]
    doc = h.doc_record(DOCS["items"][0])
    t = h.token_body(doc)
    assert t == {"context": "File", "documentId": doc["id"], "fileName": "DOC-000532299-26 [2026 INTEGRATED RESOURCE PLAN]",
                 "annotationType": "WITH_ANNOTATION", "isPreview": True}


def test_pick_docs_orders_and_plan_first():
    docs = [h.doc_record(x) for x in DOCS["items"]]
    assert docs[0]["number"] == "DOC-000532299-26" and docs[0]["date"] == "2026-10-23"
    assert "filedby" not in str(docs)
    picked = h.pick_docs(docs, cap=3)
    names = [d["name"] for d in picked]
    assert picked[0]["id"] == "f1f5a543-d072-43bf-a67d-b4ec01397c98"       # the 140 MB plan always goes first
    assert not any("ConfidentialityAgreement" in n or "Pro Hac" in n or "Screening" in n or "PROTECTIVE" in n.upper()
                   or "DEADLINE FOR RESPONSES" in n.upper() for n in names)
    assert len(picked) <= 4


def mk(i, name, typ, date):
    return {"id": i, "number": i, "name": name, "type": typ, "date": date, "docname": i, "contenttype": "application/pdf",
            "can_download": True}


def test_pick_docs_ranking():
    docs = [mk("a", "Notice of Hearing", "Notices", "2026-05-01"),
            mk("b", "Direct Testimony of A Witness", "Testimony", "2026-03-01"),
            mk("c", "Summary of Direct Testimony of A Witness", "Testimony", "2026-03-02"),
            mk("d", "Order Approving Certificate of Public Convenience and Necessity", "Orders", "2026-05-07"),
            mk("e", "Application for Approval of 2,088 MW of Gas Resources", "Application", "2025-11-01"),
            mk("f", "Certificate of Service", "Other", "2026-05-08"),
            mk("g", "Data Request 3-1", "Discovery", "2026-05-08"),
            mk("h", "Staff Report", "Report", "2026-04-01"),
            {**mk("i", "Workbook", "Exhibit", "2026-04-01"), "contenttype": "application/vnd.ms-excel"}]
    order = [d["id"] for d in h.pick_docs(docs, cap=10)]
    assert order[:2] == ["d", "e"] and order.index("c") < order.index("b")
    assert "f" not in order and "g" not in order and "i" not in order
    assert [d["id"] for d in h.pick_docs(docs, cap=2)] == ["d", "e"]


def test_orders_listed():
    docs = [h.doc_record(x) for x in DOCS["items"]]
    assert sum(h.is_order(d) for d in docs) == 7


def test_doc_facts():
    text = ("SPS proposes three 1,200 MW combined cycle units at the Hobbs generating station, in service 2029. "
            "Cunningham Unit 2 will retire in 2032. The Maddox station is located in Eddy County, New Mexico. "
            "Solar capacity of 300 MW is also proposed. Each unit uses a Siemens SGT6-9000HL turbine.\n"
            "The Pyramid Generating Station has four LM6000 units of 46.5 MW each fired on natural gas. ")
    f = h.doc_facts(text)
    assert any("1,200 MW" in s for s in f["megawatts"]) and not any("Solar capacity" in s for s in f["megawatts"])
    assert any("2032" in s for s in f["retirement"]) and any("2029" in s for s in f["in_service"])
    assert set(f["leads"]) >= {"Hobbs", "Cunningham", "Maddox", "Pyramid"}
    assert any("Eddy County" in s for s in f["location"])
    merged = h.merge_all([f, f])
    assert merged["leads"]["Pyramid"] == f["leads"]["Pyramid"]


def plant(pid, name):
    return {"id": pid, "name": name, "city": "", "county": "", "statuses": [], "name_words": h.words(name)}


def test_match_docket():
    rg, reeves, pyr = (plant("L1", "Rio Grande power station"), plant("L2", "Reeves generating station"),
                       plant("L3", "Pyramid power station"))
    case = {"docket": "23-00403-UT", "title": "EPE abandonment of Rio Grande Unit 7", "orders": [], "text_blob": "Reeves " * 9}
    assert h.match_docket(rg, case) == "on the hand-checked case list"
    assert h.match_docket(reeves, case) is None             # a hand-checked case ignores document mentions
    free = {"docket": "26-0000999", "title": "Application for a gas plant", "orders": [], "text_blob": "Reeves " * 6}
    assert h.match_docket(reeves, free).startswith("named 6 times")
    assert h.match_docket(reeves, free, others_by_title=True) is None
    named = {"docket": "26-0000998", "title": "Pyramid generating station purchase", "orders": [], "text_blob": ""}
    assert h.match_docket(pyr, named) == "name in the case title or an order"
    by_plant, matched = h.match_all([rg, reeves, pyr], [case, free, named])
    assert by_plant == {"L1": ["23-00403-UT"], "L2": ["26-0000999"], "L3": ["26-0000998"]}
    assert matched == {"23-00403-UT", "26-0000999", "26-0000998"}

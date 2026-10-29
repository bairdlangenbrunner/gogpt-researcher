"""Offline tests for scopes/us-mi/harvest_psc.py: saved snippets of the Michigan Public Service
Commission portal's Aura answers and of filing text (pdftotext -layout), no network."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from paths import load_scope_module  # noqa: E402

h = load_scope_module("us-mi", "harvest_psc")

BOOT = ('<script src="/s/sfsites/auraFW/javascript/x/aura_prod.js"></script>'
        '<script>var a="%7B%22mode%22%3A%22PROD%22%2C%22fwuid%22%3A%22FW123%22%2C%22loaded%22%3A%7B'
        '%22APPLICATION%40markup%3A%2F%2Fsiteforce%3AcommunityApp%22%3A%22APP456%22%7D%7D";</script>')


def list_answer(rows, more=True, offset=50, total=2000, drop=None):
    recs = {}
    for r in rows:
        if r["id"] == drop:
            continue
        recs[r["id"]] = {"Case": {"record": {"fields": {
            "CaseNumber": {"value": r["case"]}, "Open_Date__c": {"value": r["open"]},
            "Subject": {"value": r["subject"]}, "Industry__c": {"value": "Electric"},
            "On_Behalf_of_Company__r": {"displayValue": r["company"]}}}}}
    return {"actions": [{"state": "SUCCESS", "returnValue": {
        "recordIdActionsList": [{"recordId": r["id"]} for r in rows], "hasMoreData": more,
        "offset": offset, "totalCount": total}}],
        "context": {"globalValueProviders": [{"type": "$Record", "values": {"records": recs}}]}}


ROWS = [{"id": "500A", "case": "U-22127", "open": "2026-06-01", "company": "Consumers Energy Company",
         "subject": "Application of Consumers Energy Company for approval of an integrated resource plan"},
        {"id": "500B", "case": "U-21999", "open": "2025-11-02", "company": "DTE Electric Company",
         "subject": "Power supply cost recovery reconciliation"}]


def case(subject, company="Consumers Energy Company", num="U-20001", industry="Electric"):
    return {"id": "500X", "case": num, "open": "2025-01-01", "company": company, "subject": subject,
            "industry": industry}


def filing(seq, ftype, desc="", pages=10, public=True, by="Consumers Energy Company", date="2025-01-01"):
    return {"name": f"U-21090-{seq:04d}", "type": ftype, "date": date, "desc": desc, "pages": pages,
            "public": public, "url": f"https://mi-psc.my.site.com/sfc/servlet.shepherd/version/download/068{seq}",
            "by": by, "for": by}


def test_boot_context_reads_encoded_links_and_falls_back():
    assert h.boot_context(BOOT) == ("FW123", "APP456")
    assert h.boot_context("") == (h.FALLBACK_FWUID, h.FALLBACK_APP)


def test_parse_aura_strips_comment_prefix():
    ans = {"actions": [{"state": "SUCCESS", "returnValue": {"x": 1}}]}
    assert h.parse_aura("*/" + json.dumps(ans)) == ans
    assert h.parse_aura("<html>error</html>") is None
    assert h.action_value(ans) == ("SUCCESS", {"x": 1})
    assert h.action_value({}) == (None, None)


def test_list_page_reads_records_and_paging():
    rows, more, nxt, total = h.list_page(list_answer(ROWS))
    assert [r["case"] for r in rows] == ["U-22127", "U-21999"]
    assert rows[0]["company"] == "Consumers Energy Company" and rows[0]["industry"] == "Electric"
    assert (more, nxt, total) == (True, 50, 2000)


def test_list_page_without_a_record_is_retried():
    assert h.list_page(list_answer(ROWS, drop="500B")) is None
    bad = list_answer(ROWS)
    bad["context"]["globalValueProviders"] = []
    assert h.list_page(bad) is None


def test_filing_row_and_search_hit():
    f = h.filing_row({"filing": {"Name": "U-21090-0123", "Filing_Type__c": "Exhibits", "File_Date__c": "2021-06-01",
                                 "Filing_Description__c": "  Exhibit A-1  ", "Num_Pages__c": 0,
                                 "File_Link_URL__c": "https://x/068", "Filed_By__r": {"Name": "Jane Doe"}}})
    assert f["name"] == "U-21090-0123" and f["desc"] == "Exhibit A-1" and f["pages"] == 0 and f["by"] == "Jane Doe"
    assert h.seq_of(f["name"]) == 123
    # Confidential__c is the text "No" on ordinary filings, which must not read as sealed.
    base = {"Name": "U-22175-0002", "Num_Pages__c": 21, "Public__c": True}
    assert h.filing_row({"filing": dict(base, Confidential__c="No")})["public"] is True
    assert h.filing_row({"filing": base})["public"] is True
    assert h.filing_row({"filing": dict(base, Confidential__c="Yes")})["public"] is False
    assert h.filing_row({"filing": dict(base, Public__c=False)})["public"] is False
    s = h.search_hit({"Name": "U-22127-0009", "Filing_Type__c": "Application", "File_Date__c": "2026-06-01T00:00:00Z",
                      "Filing_Description__c": "Integrated resource plan"}, "Thetford")
    assert s["case"] == "U-22127" and s["date"] == "2026-06-01" and s["term"] == "Thetford"
    assert h.search_hit({"Name": "something"}, "x")["case"] == ""


def test_classify_cases():
    rel, key, why = h.classify(case("Application for approval of an integrated resource plan"),
                               {"type": "Integrated Resource Plan"})
    assert rel and key
    assert h.classify(case("Power supply cost recovery reconciliation", "DTE Electric Company"))[0] is False
    rel, key, why = h.classify(case("Application for approval of a power purchase agreement for a solar facility"))
    assert rel and not key and "renewables or storage only" in why
    assert h.classify(case("Gas cost recovery plan", "SEMCO Energy Gas Company", industry="Gas"))[0] is False
    rel, key, _ = h.classify(case("Contract to serve a natural gas power plant", "DTE Gas Company", industry="Gas"))
    assert rel and not key
    assert h.classify(case("anything", num="U-21090")) [:2] == (True, True)


def test_pick_docs_skips_sealed_and_keeps_wanted():
    fs = [filing(1, "Application", "Application and exhibits"),
          filing(2, "Proof of Service"),
          filing(3, "Testimony and Exhibits", "Direct testimony of a witness", pages=0),
          filing(4, "Testimony and Exhibits", "Direct testimony and exhibits", date="2021-06-01"),
          filing(5, "Comments", "Comments naming Covert", by="Someone Else"),
          filing(6, "Order", "Order approving settlement"),
          filing(7, "Exhibits", "Exhibit A-12 resource additions", date="2021-06-02")]
    names = [f["name"] for f in h.pick_docs(fs, 12, "Consumers Energy Company", wanted={"U-21090-0005"})]
    assert "U-21090-0001" in names and "U-21090-0006" in names
    assert "U-21090-0003" not in names and "U-21090-0002" not in names
    assert "U-21090-0005" not in names  # a comment stays out even when the search found it
    assert names == sorted(names)
    assert len(h.pick_docs(fs, 2, "Consumers Energy Company")) == 2


LAYOUT = ("Consumers Energy cover page\n"
          "\fExhibit A-12 (TEG-3)\n  1   Thetford simple cycle   919 MW   2031\n"
          "\fNo plants here\n"
          "\fExhibit A-13\n  The Thetford site in Genesee County.\n")


def test_plant_pages_counts_form_feeds_and_reads_exhibit():
    pages = h.plant_pages(LAYOUT, [r"\bthetford\b"])
    assert pages == [{"page": 2, "exhibit": "A-12 (TEG-3)"}, {"page": 4, "exhibit": "A-13"}]
    assert h.plant_pages(LAYOUT, [r"\bthetford\b"], limit=1) == [{"page": 2, "exhibit": "A-12 (TEG-3)"}]


GENESEE = {"id": "L100001083333", "name": "Genesee County power station"}
ZEELAND = {"id": "L100000401831", "name": "Zeeland power station"}
JACKSON = {"id": "L100000401830", "name": "Jackson power station"}


def docket(title, num="U-22127"):
    return {"docket": num, "title": title, "docs": []}


def test_match_case_records_where_the_plant_appears():
    texts = {"U-22127-0009": LAYOUT + "\fThetford Project 919 MW in 2031. The Thetford site again.\n"}
    how, where, facts = h.match_case(GENESEE, docket("Consumers integrated resource plan"), texts)
    assert "named" in how and "U-22127-0009 page 2 (Exhibit A-12 (TEG-3))" in how
    assert where[0]["pages"][0]["page"] == 2
    assert any("919 MW" in f for f in facts)
    assert h.match_case(GENESEE, docket("Consumers plan"), {"a": "Thetford Township, the Thetford site once"}) is None


def test_town_and_soil_names_are_not_plants():
    covert = {"id": "L100000402123", "name": "New Covert generating facility"}
    d = docket("Solar siting application")
    soils = {"a": "Covert-Pipestone sands, 0 to 6 percent slopes. Pipestone-Covert-Saugatuck. Covert Township. " * 3}
    assert h.match_case(covert, d, soils) is None
    assert h.match_case(GENESEE, d, {"a": "Thetford Township, Genesee County. " * 5}) is None
    assert h.match_case(covert, d, {"a": "the Covert plant " * 3})


def test_zeeland_board_of_public_works_and_jackson_address_are_not_plants():
    texts = {"a": "Zeeland Board of Public Works. " * 5 + "Zeeland BPW. " * 3,
             "b": "One Energy Plaza, Jackson, Michigan. " * 6,
             "c": "In Hudsonville and Zeeland combined, the share of renters. " * 4}
    d = docket("Consumers plan")
    assert h.match_case(ZEELAND, d, texts) is None
    assert h.match_case(JACKSON, d, texts) is None
    assert h.match_case(ZEELAND, d, {"a": "the Zeeland plant " * 3})


def test_match_all_needs_more_when_title_names_another_plant():
    plants = [GENESEE, ZEELAND]
    d = docket("Application for the Zeeland plant expansion", "U-21000")
    texts = {"U-21000": {"a": "Thetford site. " * 4}}
    by_plant, matched = h.match_all(plants, [d], texts)
    assert by_plant == {GENESEE["id"]: [], ZEELAND["id"]: ["U-21000"]} and matched == {"U-21000"}
    texts = {"U-21000": {"a": "Thetford site. " * 7}}
    by_plant, _ = h.match_all(plants, [d], texts)
    assert by_plant[GENESEE["id"]] == ["U-21000"]


def test_doc_facts_pulls_sizes_years_and_table_lines():
    text = ("The company proposes a 456 MW simple cycle combustion turbine facility at the D.E. Karn site. "
            "The plant is expected to be placed in service in 2031. "
            "Karn Units 3 and 4 will retire in 2031. "
            "The site is located in Bay County, Michigan.")
    layout = "  1   D.E. Karn CT    456 MW    2031\n  2   Lunch menu   2031\n"
    f = h.doc_facts(text, layout)
    assert any("456 MW" in s for s in f["megawatts"])
    assert any("2031" in s for s in f["retirement"])
    assert any("Bay County" in s for s in f["location"])
    assert "D.E. Karn CT 456 MW 2031" in f["resource_plan_table_lines"]
    assert not any("Lunch" in s for s in f["resource_plan_table_lines"])

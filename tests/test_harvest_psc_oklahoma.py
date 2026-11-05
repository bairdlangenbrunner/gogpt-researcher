"""Offline tests for scopes/us-ok/harvest_psc.py: the daily docket parser, WebLink result
parsing, cause building, classification, document choice and plant matching. No network."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from paths import load_scope_module  # noqa: E402

h = load_scope_module("us-ok", "harvest_psc")

PAD = " " * 30
DAILY = f"""                                    Oklahoma City Court Calendar                     3 total items
                                    Public Utility - Initial/Continued                www.oklahoma.gov.occ

OSF2026-000201{PAD}Judge: A JUDGE{PAD}Courtroom: C50{PAD}Thursday, October 29, 2026 8:30 AM

Parties: PERSON, SOME (Applicant){PAD}Legal: -{PAD}Attorney: LAWYER, A
Text: Hearing on the Merits{PAD}Court Reporter: A REPORTER
Relief Type: OUSF Assessment Relief Sought: APPLICATION OF SOME PERSON, ADMINISTRATOR
Result: RO | TUA

PUD2026-000073{PAD}Judge: A JUDGE{PAD}Courtroom: C50{PAD}Thursday, October 29, 2026 8:30 AM

Parties: OKLAHOMA GAS AND ELECTRIC COMPANY (Applicant) Legal: -{PAD}Attorney: LAWYER, B
Text: Hearing on the Merits{PAD}Court Reporter: A REPORTER
Relief Type: Bonds/Securities Relief Sought: IN THE MATTER OF THE APPLICATION OF OKLAHOMA GAS AND ELECTRIC COMPANY FOR AUTHORITY
TO ENTER INTO A GUARANTEE AGREEMENT
Result: RO | MR

{PAD}Page 1 of 2
   DIS: Dismissed DMOA: Dismissed on Motion of Applicant RO: Record Opened
                                    Public Utility - Motion                           www.oklahoma.gov.occ

PUD2026-000068{PAD}Judge: A JUDGE{PAD}Courtroom: C50{PAD}Thursday, October 29, 2026 8:30 AM

Parties: AEP OKLAHOMA TRANSMISSION COMPANY INC{PAD}Legal: -{PAD}Attorney: LAWYER, C
         (Applicant)
Text: Continued (1) | Motion to Intervene-Some Neighbor and Other Neighbor{PAD}Court Reporter: A REPORTER
Relief Type: Other: High Voltage Transmission COA Relief Sought: IN THE MATTER OF THE APPLICATION OF AEP OKLAHOMA TRANSMISSION
COMPANY, INC. REQUESTING A CERTIFICATE OF AUTHORITY FROM THE OKLAHOMA CORPORATION COMMISSION
Result: RO | MOR
"""

INDEX = ('<a href="/content/dam/ok/en/occ/documents/ajls/jls-courts/court-clerk/docket-results/2026/'
         '2026-10-29-pud.pdf">x</a> <a href="/content/dam/ok/en/occ/documents/ajls/jls-courts/court-clerk/'
         'docket-results/2026/2026-10-29-okc.pdf">y</a> <a href="/content/dam/ok/en/occ/documents/ajls/jls-courts/'
         'court-clerk/docket-results/2023/2023-05-01-pud.pdf">z</a> &lt;a href=&quot;/content/dam/ok/en/occ/'
         'documents/ajls/jls-courts/court-clerk/docket-results/2025/2025-02-03-pud.pdf&quot;&gt;')


def md(**kw):
    return [{"name": k.replace("_", " "), "values": [v], "isMvfg": False} for k, v in kw.items()]


ORDER = {"name": "760106", "entryId": 21288037, "type": -2, "isEdoc": False, "extension": "",
         "entryProperties": "8 pages ",
         "metadata": [{"name": "Case Number", "values": ["PUD2026-000048"]},
                      {"name": "ECF Case Number", "values": ["2026-000048"]},
                      {"name": "ECF Docket Date", "values": ["9/1/2026"]},
                      {"name": "ECF Document Type", "values": ["Final Order"]},
                      {"name": "ECF Order Number", "values": ["760106"]},
                      {"name": "ECF Relief Types", "values": ["Preapproval"]},
                      {"name": "Order Title", "values": ["Final Order Approving Preapproval of Horseshoe Lake Units 13 and 14"]},
                      {"name": "Relief Requested", "values": ["APPLICATION OF OKLAHOMA GAS AND ELECTRIC COMPANY FOR PREAPPROVAL OF NEW GENERATING CAPACITY"]}]}
FILING = {"name": "PUD2026-000048_1_Application_filed_on_behalf_of_OKLAHOMA_GAS_AND_ELECTRIC_COMPANY",
          "entryId": 21291313, "type": -2, "isEdoc": True, "extension": "pdf", "entryProperties": "0 pages - 579 KB ",
          "metadata": [{"name": "ECF Applicant", "values": ["OKLAHOMA GAS AND ELECTRIC COMPANY"]},
                       {"name": "ECF Case Number", "values": ["2026-000048"]},
                       {"name": "ECF Division", "values": ["PUD"]},
                       {"name": "ECF Docket Date", "values": ["3/2/2026"]},
                       {"name": "ECF Document Type", "values": ["Application"]}]}


def plant(pid, name):
    return {"id": pid, "name": name, "city": "", "county": "", "statuses": ["operating"], "name_words": h.words(name)}


def test_docket_links_only_pud_from_year():
    got = h.docket_links(INDEX, 2024)
    assert [d for d, _ in got] == ["2025-02-03", "2026-10-29"]
    assert got[1][1].startswith("https://oklahoma.gov/content/dam/") and got[1][1].endswith("-pud.pdf")


def test_parse_daily_keeps_utility_causes_without_names():
    es = h.parse_daily(DAILY, "2026-10-29", "u")
    assert [e["docket"] for e in es] == ["PUD2026-000073", "PUD2026-000068"]
    a, b = es
    assert a["hearing"] == "2026-10-29" and a["applicant"] == "OKLAHOMA GAS AND ELECTRIC COMPANY"
    assert a["relief_type"] == "Bonds/Securities"
    assert a["relief_sought"].endswith("FOR AUTHORITY TO ENTER INTO A GUARANTEE AGREEMENT")
    assert b["applicant"] == "AEP OKLAHOMA TRANSMISSION COMPANY INC"
    assert b["hearing_text"] == "Continued (1) | Motion to Intervene"
    text = json.dumps(es)
    for name in ("JUDGE", "LAWYER", "REPORTER", "Neighbor", "PERSON"):
        assert name not in text


def test_parse_result_order_and_filing():
    o = h.parse_result(ORDER)
    assert o["case"] == "PUD2026-000048" and o["kind"] == "imaged order" and o["order_number"] == "760106"
    assert o["date"] == "2026-09-01" and o["url"].endswith("DocView.aspx?id=21288037&dbid=0&repo=OCC")
    f = h.parse_result(FILING)
    assert f["case"] == "PUD2026-000048" and f["kind"] == "electronic filing" and f["docket_entry"] == 1
    assert f["title"] == "Application filed on behalf of OKLAHOMA GAS AND ELECTRIC COMPANY"
    assert f["bytes"] == 579000 and f["url"].endswith("ElectronicFile.aspx?docid=21291313&dbid=0&repo=OCC")


def test_order_search_syntax():
    import datetime as dt
    assert h.order_syn(dt.date(2026, 9, 1), dt.date(2026, 9, 30)) == (
        '{[ECF Document]:[ECF Division]="PUD", [ECF Docket Date]>="9/1/2026", [ECF Docket Date]<="9/30/2026"}')
    ws = list(h.month_windows(2025, dt.date(2026, 2, 10)))
    assert len(ws) == 14 and ws[-1] == (dt.date(2026, 2, 1), dt.date(2026, 2, 28))


def test_build_and_classify():
    causes = h.build_causes(h.parse_daily(DAILY, "2026-10-29", "u"), [h.parse_result(ORDER)])
    assert set(causes) == {"PUD2026-000073", "PUD2026-000068", "PUD2026-000048"}
    pre = causes["PUD2026-000048"]
    assert pre["utility"] == "OKLAHOMA GAS AND ELECTRIC COMPANY" and pre["relief_types"] == ["Preapproval"]
    assert pre["url"].endswith("id=21288037&dbid=0&repo=OCC")
    assert h.classify(pre)[:2] == (True, True)
    assert h.classify(causes["PUD2026-000073"])[0] is False
    rel, key, _ = h.classify(causes["PUD2026-000068"])
    assert not key


def test_pick_docs_skips_notices_and_prefers_the_application():
    docs = [h.parse_result(FILING), h.parse_result(ORDER),
            {**h.parse_result(FILING), "entry_id": 2, "name": "PUD2026-000048_5_Entry_of_Appearance", "title": "Entry of Appearance", "docket_entry": 5},
            {**h.parse_result(FILING), "entry_id": 3, "name": "PUD2026-000048_9_Big", "title": "Big", "bytes": 10**9, "docket_entry": 9}]
    got = h.pick_docs(docs, 5, 80_000_000)
    assert [d["entry_id"] for d in got] == [21291313, 21288037]


def test_match_by_known_pattern_and_body_count():
    causes = h.build_causes([], [h.parse_result(ORDER)])
    d = {**causes["PUD2026-000048"], "text_blob": ""}
    assert h.match_docket(plant("L100000402162", "Horseshoe Lake"), d) == "name in the relief sought or an order title"
    d2 = {**d, "title": "x", "orders": [], "relief_types": [], "utility": "",
          "text_blob": "Northeastern Station " * 3}
    assert h.match_docket(plant("L100000104126", "Northeastern"), d2).startswith("named 3 times")
    assert h.match_docket(plant("L100000104126", "Northeastern"), d2, others_by_title=True) is None


def test_doc_facts():
    f = h.doc_facts("OG&E proposes two GE 7HA.03 combined cycle units totaling 1,350 MW.\n"
                    "Commercial operation is expected in 2029.\n"
                    "The site is located in Oklahoma County, Oklahoma at 35.4147, -97.3866.\n")
    assert "combined cycle" in f["technology"]
    assert any("1,350 MW" in x for x in f["megawatts"])
    assert f["in_service"] and f["coords"] == ["35.4147, -97.3866"]


def test_write_outputs_contract(tmp_path):
    causes = h.build_causes([], [h.parse_result(ORDER)])
    ds = []
    for d in causes.values():
        d["relevant"], d["key"], d["reasons"] = h.classify(d)
        d.update(documents=[], facts={}, text_blob="")
        ds.append(d)
    plants = [plant("L100000402162", "Horseshoe Lake")]
    by_plant, matched = h.match_all(plants, ds)
    h.write_outputs(tmp_path, plants, ds, by_plant, matched, [{"name": "n", "how": "h", "url": "u"}], "2026-11-04", 2024)
    data = json.loads((tmp_path / "psc_dockets.json").read_text())
    for k in ("generated", "from_year", "sources", "dockets", "by_plant", "unmatched_generation"):
        assert k in data
    assert data["by_plant"]["L100000402162"] == ["PUD2026-000048"]
    assert "text_blob" not in data["dockets"][0]
    assert "PUD2026-000048" in (tmp_path / "psc_dockets.md").read_text()


def test_telephone_school_and_hospital_causes_are_dropped():
    base = {"relief_type": "", "relief_types": [], "orders": [], "utility": ""}
    school = {**base, "docket": "PUD2025-000276", "title": "REQUEST OF WELEETKA PUBLIC SCHOOLS FOR FUNDING FROM THE OKLAHOMA UNIVERSAL SERVICE FUND"}
    phone = {**base, "docket": "PUD2025-000002", "title": "APPLICATION OF NEXTCITY NETWORKS OKLAHOMA, LLC FOR A CERTIFICATE OF CONVENIENCE AND NECESSITY"}
    pso = {**base, "docket": "PUD2024-000057", "title": "APPLICATION OF PUBLIC SERVICE COMPANY OF OKLAHOMA FOR PREAPPROVAL OF THE PURCHASE OF THE GREEN COUNTRY GENERATING FACILITY"}
    assert h.classify(school)[0] is False and h.classify(phone)[0] is False
    assert h.classify(pso)[1] is True
    weleetka = {"id": "L100000402236", "name": "Weleetka power station", "name_words": {"weleetka"}}
    assert h.match_docket(weleetka, school) is None

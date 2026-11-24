"""Offline tests for scopes/us-wi/harvest_psc.py: the docket title and filing table parsers, the
statewide list and case page parsers, docket classification, document choice and plant matching.
No network. Fixtures in tests/fixtures/psc_wisconsin/ are trimmed copies of ERF pages (filer names
and e-mail addresses removed)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from paths import load_scope_module  # noqa: E402

h = load_scope_module("us-wi", "harvest_psc")
FIX = Path(__file__).parent / "fixtures" / "psc_wisconsin"
CE318 = (FIX / "docket_ce318.html").read_text()
CE315 = (FIX / "docket_ce315.html").read_text()


def test_split_docket_and_dates():
    assert h.split_docket("6630-CE-318") == ("6630", "CE", "318")
    assert h.split_docket("5-CE-161") == ("5", "CE", "161")
    assert h.split_docket("not a docket") is None
    assert h.us_date("11/16/2026 11:11:00 AM") == "2026-11-16"
    assert h.size_bytes("(131 KB)") == 131000


def test_parse_title_is_the_docket_title():
    docket, title = h.parse_title(CE318)
    assert docket == "6630-CE-318"
    assert title.startswith("Application of Wisconsin Electric Power Company for a Certificate of Authority")
    assert "Port Washington Generating Station Combustion Turbine Upgrade Project" in title
    assert h.utility_of(title) == "Wisconsin Electric Power Company"
    assert "Concord Generating Station Units 1, 2, 3, and 4" in h.parse_title(CE315)[1]
    assert h.parse_total(CE318) == 101 and h.parse_total(CE315) == 28
    assert h.parse_title("<html>a short error page</html>") == ("", "")


def test_parse_filings_drops_filer_and_size_suffix():
    rows = h.parse_filings(CE318)
    assert len(rows) == 5 and rows[0]["doc_id"] == "618547"
    r = rows[0]
    assert r["description"].startswith("Response-Data Request-PSC-Martinson-DMG-4.1")
    assert not r["description"].endswith("KB)")
    assert (r["format"], r["class"], r["received"], r["bytes"]) == ("XLSX", "P", "2026-11-16", 131000)
    assert r["has_link"] and r["docket"] == "6630-CE-318"
    assert "@" not in str(rows) and "Steinert" not in str(rows)
    assert not any("user_name" in k or "filer" in k for k in r)


def test_parse_docket_list_and_case_links():
    page = ("<a href='http://apps.psc.wi.gov/pages/docketDetail.htm?dockt_id=6630-CE-318'>x</a>"
            "<a href=\"http://apps.psc.wi.gov/pages/docketDetail.htm?dockt_id=5-CE-162\">x</a>"
            "<a href='...dockt_id=6630-CE-318'>again</a>")
    assert h.parse_docket_list(page) == ["5-CE-162", "6630-CE-318"]
    idx = ('<a href="https://psc.wi.gov:443/Pages/CommissionActions/CasePages/RedOakRidge.aspx">a</a>'
           '<a href="/Pages/CommissionActions/CasePages/FoundryRidgeEnergyCenter.aspx">b</a>'
           '<a href="/Pages/CommissionActions/HighlightedCases.aspx">c</a>')
    assert h.parse_case_links(idx) == [
        "https://psc.wi.gov/Pages/CommissionActions/CasePages/RedOakRidge.aspx",
        "https://psc.wi.gov/Pages/CommissionActions/CasePages/FoundryRidgeEnergyCenter.aspx"]


def test_parse_case_page():
    c = h.parse_case_page((FIX / "case_red_oak_ridge.html").read_text())
    assert c["docket"] == "9837-CE-100" and c["related"] == ["6630-BS-104"]
    assert c["title"].endswith("Kenosha County, Wisconsin.") and "​" not in c["title"]
    assert "five, 242 MW gas turbines" in c["summary"]


def d(docket, title):
    return {"docket": docket, "title": title, "utility": h.utility_of(title)}


def test_classify():
    gas = d("6630-CE-318", h.parse_title(CE318)[1])
    line = d("6630-CE-400", "Application of ATC for a Certificate of Authority to Construct a 345 kV Transmission Line")
    solar = d("6630-CE-401", "Application of A Solar LLC for a Certificate to Construct a 100 MW Solar Generating Facility")
    dc = d("6680-TE-115", "Application of Wisconsin Power and Light Company for Approval of a Data Center Service Agreement")
    rate = d("6630-UR-100", "Application for a Rate Increase")
    assert h.classify(gas)[:2] == (True, True)
    assert h.classify(line)[1] is False
    assert h.classify(solar) == (True, False, h.classify(solar)[2])
    assert h.classify(dc)[:2] == (True, True)
    assert h.classify(rate)[:2] == (False, False)
    assert h.classify(d("9999-ZZ-1", "Anything"))[:2] == (False, False)
    assert h.classify(d("5-CE-161", "Anything"))[:2] == (True, True)


def test_pick_docs_skips_confidential_and_non_text():
    base = {"has_link": True, "class": "P", "in_camera": False, "paper": False, "format": "PDF",
            "bytes": 1000, "received": "2026-01-01", "doc_type": "Application"}
    f = [dict(base, doc_id="1", description="Application for a Certificate of Authority"),
         dict(base, doc_id="2", description="Engineering Plan", bytes=5000),
         dict(base, doc_id="3", description="Certificate of Service"),
         dict(base, doc_id="4", description="Application Confidential", **{"class": "C"}),
         dict(base, doc_id="5", description="Cost workbook", format="XLSX"),
         dict(base, doc_id="6", description="Huge exhibit", bytes=200_000_000),
         dict(base, doc_id="7", description="Final Decision", doc_type="Order", received="2026-10-15"),
         dict(base, doc_id="8", description="No link", has_link=False)]
    got = [x["doc_id"] for x in h.pick_docs(f, 10, 60_000_000)]
    assert set(got) == {"1", "2", "7"} and len(h.pick_docs(f, 1, 60_000_000)) == 1


def test_doc_facts():
    text = ("The Project consists of five GE 7F.05 combustion turbines at 242 MW each. "
            "Commercial operation is planned for December 2030. The site is located in the Town of Paris, "
            "Kenosha County, Wisconsin. Coal Unit 3 will retire in 2031.")
    f = h.doc_facts(text)
    assert any("242 MW" in x for x in f["megawatts"])
    assert any("7F" in x for x in f["equipment_maker_model"])
    assert any("2030" in x for x in f["in_service"]) and any("2031" in x for x in f["retirement"])
    assert any("Kenosha" in x for x in f["location"])


def plant(pid, name):
    return {"id": pid, "name": name, "name_words": h.words(name)}


def test_match_all():
    plants = [plant("L100001062057", "Red Oak Ridge Energy Center"), plant("L100001047775", "Paris RICE power station"),
              plant("L100000402374", "Paris (WI) power station"), plant("L100000104693", "Port Washington power station"),
              plant("L100000401640", "Riverside energy center (WI)"), plant("L100000409999", "Unlisted Peaking Plant")]
    dockets = [d("9837-CE-100", "Application of Red Oak Ridge Energy Center LLC for a Certificate of Public Convenience "
                 "and Necessity to Construct a Large Electric Generating Facility"),
               d("6630-CE-318", h.parse_title(CE318)[1]),
               d("6630-CE-316", "Application of Wisconsin Electric Power Company for a Certificate of Authority to Construct "
                 "the Paris RICE Project in the Town of Paris"),
               d("6630-CE-500", "Application for authority to build the Unlisted Peaking Plant"),
               d("6630-CE-501", "Application for a new generating facility in Dane County")]
    by_plant, matched = h.match_all(plants, dockets)
    assert by_plant["L100001062057"] == ["9837-CE-100"]
    assert by_plant["L100000104693"] == ["6630-CE-318"]
    assert by_plant["L100001047775"] == ["6630-CE-316"] and by_plant["L100000402374"] == []
    assert by_plant["L100000409999"] == ["6630-CE-500"]
    assert matched == {"9837-CE-100", "6630-CE-318", "6630-CE-316", "6630-CE-500"}


def test_known_dockets_are_well_formed():
    assert all(h.split_docket(k) for k in h.KNOWN_DOCKETS)
    assert all(h.split_docket(f"{u}-CE-1") for u in h.UTILITIES)


def test_doc_facts_drops_boilerplate_keeps_facts():
    text = (Path(__file__).parent / "fixtures" / "psc_wisconsin" / "doc_facts_sample.txt").read_text()
    f = h.doc_facts(text)
    everything = " ".join(x for k, v in f.items() if k not in ("technology", "coords") for x in v)
    for junk in ("PSC REF#", "Secretary to the Commission", "certificate of service", "service list", "ambient sound",
                 "measurement points", "flood plain", "Notice of Investigation"):
        assert junk.lower() not in everything.lower(), junk
    assert any("100 MW" in x for x in f["megawatts"])
    assert any("Jefferson County" in x for x in f["location"]) and len(f["location"]) == 1
    assert any("$24,300,000" in x for x in f["cost"])
    assert any("placed in service in May 2022" in x for x in f["in_service"])
    assert len(f["retirement"]) == 1 and "retired in 2022" in f["retirement"][0]
    assert any("Wisconsin Electric Power Company" in x for x in f["owner"])
    assert "combustion turbine" in f["technology"]

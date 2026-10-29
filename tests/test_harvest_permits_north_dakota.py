"""Offline tests for scopes/us-nd/harvest_permits.py: saved snippets of the DEQ public comment page,
the DEQ notice list and feed, a Wayback index answer and CERIS-ND answers, no network."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from paths import load_scope_module  # noqa: E402

h = load_scope_module("us-nd", "harvest_permits")

PUBLICCOM = """
<div class="sectionGray" id="MarvinComposites">
<h3>Marvin Composites, LLC - Marvin Composites Facility</h3>
<h4>Window/Door Fiberglass Manufacturing </h4>
<h4>Cass County</h4>
<ul>
<li><b>Permit Type:</b> Permit to Construct-Synthetic Minor </li>
<li><b>Public Comment Period Begins:</b> October 27, 2026</li>
<li><b>Public Comment Period Ends:</b> November 26, 2026</li>
</ul>
<a href="Notices/MarvinComposites/20261021BjertnessLtr_NOI.pdf">Cover Letter and Notice of Public Comment</a>
<a href="Notices/MarvinComposites/DraftACP18354 v1_0.pdf">Draft Permit to Construct No. ACP-18354v1.0</a>
<a href="https://ceris.deq.nd.gov/ext/nsite/DEFAULT/map/results/detail/6152526369657274316/Documents">Application</a>
</div>
<div class="sectionGray" id="BasinElectricBison">
<h3>Basin Electric Power Cooperative - Bison Generation Station</h3>
<h4>Electric Generation (Natural Gas)</h4>
<h4>Williams County</h4>
<ul>
<li><b>Permit Type:</b> Prevention of Significant Deterioration Major Source</li>
<li><b>Public Comment Period Begins:</b> October 1, 2025</li>
<li><b>Public Comment Period Ends:</b> November 3, 2025</li>
</ul>
<a href="Notices/BasinElectricBison/DRAFT_ACP18300v1_0.pdf">Draft Permit to Construct</a>
</div>
<!--end content-->
"""

NOTICE_LIST = """
<li><a class=menulist target="_blank" href="https://deq.nd.gov/aq/PublicCom.aspx#MarvinComposites">Notice of Intent to issue an air pollution control Permit to Construct-Marvin Composites, LLC<span class="x"> (ID=4082)</span></a><br>
 Posted: Thursday, October 22, 2026</li>
<li><a class=menulist href="https://deq.nd.gov/AQ/PublicCom.aspx#BasinElectricBison">Notice of issuance - PSD air pollution control Permit to Construct and cancellation of public hearing \u2013 Basin Electric Bison Generation Station <span> (ID=3962)</span></a><br>
 Posted: Monday, December 29, 2025</li>
<li><a class=menulist href="/PublicComment/wq.pdf">Draft water discharge permit<span> (ID=4001)</span></a><br>
 Posted: Friday, August 1, 2025</li>
"""

RSS = ("\ufeff<rss><channel><item><title>Transfer Station - Devils Lake, ND</title>"
       "<link>https://deq.nd.gov/wm/PublicNotices/default.aspx</link><description>x</description>"
       "<pubDate>Thu, 29 Oct 2026 14:13:11 GMT</pubDate>"
       "<guid isPermaLink=\"false\">https://deq.nd.gov/PublicNoticesRSSFeed#4084</guid></item></channel></rss>")

CDX_ROWS = [
    ["20230327234752", "https://deq.nd.gov/AQ/Notices/Lonesome/BasinLCSFullT5RevApp.pdf", "200", "application/pdf"],
    ["20210101000000", "https://deq.nd.gov/AQ/Notices/Lonesome/BasinLCSFullT5RevApp.pdf", "200", "application/pdf"],
    ["20221010000000", "http://www.ndhealth.gov/AQ/Notices/Basin/PGSNoticeSOBDraftPermit.pdf", "200", "application/pdf"],
    ["20240101000000", "https://deq.nd.gov/AQ/Notices/RuleRevisions/rule.pdf", "200", "application/pdf"],
    ["20240101000000", "https://deq.nd.gov/AQ/Notices/", "200", "text/html"],
]

SITE_SEARCH = {"totalSiteCount": 3, "insertUpdateList": [
    {"siteId": None, "clusterCount": 12, "siteName": None},
    {"siteId": "-111", "siteName": "Applied Digital Polaris Forge 1 - AQ", "city": "Ellendale", "siteAddress": "1 Main St",
     "zip": "58436", "geographyWKT": "POINT(-98.52 46.0)"},
    {"siteId": "-222", "siteName": "Applied Digital Polaris Forge 1 - WQ", "city": "Ellendale", "geographyWKT": None}]}

TABS = {
    "details": [{"siteName": "X - AQ", "siteAddr": "4401 15th Ave. NW, Fargo, ND", "siteCnty": "Cass",
                 "siteSiteTypes": "Air Point Source"}],
    "codes": [{"siteSicCodes": "Computer Processing (7374)", "siteNaicsCodes": "Data Processing, Hosting (518210)"}],
    "permits": [{"prmtPrmtNum": "ACP-18181", "prmtRefPrmtCatgDescr": "Air Permit to Construct",
                 "prmtPrmtTypeDescr": "Construction Permit - Minor", "prmtRefPrmtStatDescr": "In Effect",
                 "prmtEfctvDate": "2023-03-29T00:00:00", "prmtExprDate": None}],
    "documents": [{"docMgmtDocurl": "https://ceris.deq.nd.gov/ext/ncore/downloadpdf/6338", "docMgmtDocName":
                   "Y:\\Eng\\Air\\Word\\Permit\\ACP18181.pdf", "docMgmtDocDescr": "Permit to Construct",
                   "docMgmtCategory": "Permits", "docMgmtDocRvcdCreatedDate": "2023-03-29T00:00:00",
                   "docMgmtSourceprogramarea": "Air Quality"},
                  {"docMgmtDocurl": None, "docMgmtDocName": "missing.pdf"}],
}


def plant(pid, name, city="", county=""):
    return {"id": pid, "name": name, "city": city, "county": county, "statuses": ["announced"],
            "name_words": h.words(name)}


def test_parse_publiccom_blocks():
    recs = {r["anchor"]: r for r in h.parse_publiccom(PUBLICCOM)}
    m = recs["MarvinComposites"]
    assert m["name"] == "Marvin Composites, LLC - Marvin Composites Facility"
    assert m["what"] == "Window/Door Fiberglass Manufacturing" and m["county"] == "Cass"
    assert m["permit_type"] == "Permit to Construct-Synthetic Minor"
    assert (m["begins"], m["ends"]) == ("2026-10-27", "2026-11-26")
    assert m["folder"] == "MarvinComposites" and m["ceris_sites"] == ["6152526369657274316"]
    urls = [d["url"] for d in m["docs"]]
    assert "https://deq.nd.gov/AQ/Notices/MarvinComposites/DraftACP18354%20v1_0.pdf" in urls
    assert m["docs"][0]["date"] == "2026-10-21"
    assert recs["BasinElectricBison"]["county"] == "Williams"


def test_notice_list_and_feed():
    items = h.parse_notice_list(NOTICE_LIST)
    assert [n["id"] for n in items] == [4082, 3962, 4001]
    assert items[1]["anchor"] == "BasinElectricBison" and items[1]["posted"] == "2025-12-29"
    assert items[2]["url"] == "https://deq.nd.gov/PublicComment/wq.pdf"
    assert [h.is_air_notice(n) for n in items] == [True, True, False]
    rss = h.parse_rss(RSS)
    assert rss[0]["id"] == 4084 and rss[0]["posted"].startswith("Thu, 29 Oct 2026")


def test_cdx_notice_files_keeps_newest_and_skips_rules():
    files = h.cdx_notice_files(CDX_ROWS)
    assert set(files) == {"lonesome", "basin"}
    lone = files["lonesome"]
    assert len(lone) == 1 and lone[0]["ts"] == "20230327234752"
    assert lone[0]["archive"].startswith("https://web.archive.org/web/20230327234752id_/")
    assert files["basin"][0]["url"] == "https://deq.nd.gov/AQ/Notices/Basin/PGSNoticeSOBDraftPermit.pdf"


def test_ceris_sites_profile_and_private_fields():
    sites = h.ceris_sites(SITE_SEARCH)
    assert [s["site_id"] for s in sites] == ["-111", "-222"]
    assert sites[0]["lat"] == 46.0 and sites[0]["lon"] == -98.52
    assert [h.is_air_site(s["name"]) for s in sites] == [True, False]
    prof = h.ceris_profile(TABS)
    assert prof["county"] == "Cass" and prof["permits"][0]["number"] == "ACP-18181"
    assert prof["permits"][0]["effective"] == "2023-03-29"
    assert len(prof["docs"]) == 1 and "Y:" not in prof["docs"][0]["name"] and "(ACP18181.pdf)" in prof["docs"][0]["name"]
    notices = h.slim_ceris_notices([{"siteName": "A", "assignedUserName": "Someone", "assignedPhone": "701",
                                     "contactNamePermit": "Someone Else", "permitNumber": "P1"}])
    assert "assignedUserName" not in notices[0] and "contactNamePermit" not in notices[0]
    assert notices[0]["permitNumber"] == "P1"


def test_build_match_and_power():
    pc = h.merge_publiccom(h.parse_publiccom(PUBLICCOM))
    saved = h.cdx_notice_files(CDX_ROWS)
    sites = h.ceris_sites(SITE_SEARCH)
    facs = h.build_facilities(pc, saved, [s for s in sites if h.is_air_site(s["name"])])
    loose = h.attach_list_items(facs, [n for n in h.parse_notice_list(NOTICE_LIST) if h.is_air_notice(n)])
    assert loose == []
    assert [n["id"] for n in facs["aq:basinelectricbison"]["list_items"]] == [3962]
    flist = list(facs.values())
    bison = h.match(plant("L100001047848", "Bison Generation Station", "Wheelock Township", "Williams"), flist)
    assert [(f["key"], how) for f, how in bison] == [("aq:basinelectricbison", "checked by hand")]
    pioneer = h.match(plant("L100000401741", "Pioneer Generating Station"), flist)
    assert [f["key"] for f, _ in pioneer] == ["aq:basin"]
    polaris = h.match(plant("L100001083334", "Polaris Forge 1"), flist)
    assert [f["key"] for f, _ in polaris] == ["ceris:-111"]
    assert h.is_power(facs["aq:basinelectricbison"]) and not h.is_power(facs["aq:marvincomposites"])
    coded = dict(facs["aq:marvincomposites"], codes=["Data Processing, Hosting (518210)"])
    assert h.is_power(coded)


def test_doc_facts():
    text = ("The project will consist of two Siemens SGT-800 combustion turbines rated 62 MW each.\n"
            "The facility is located in Section 12, Township 154 North, Range 101 West, Williams County.\n"
            "Permit to Construct No. ACP-18300 v1.0 is proposed.\n"
            "Coordinates 48.1234, -103.5678\n")
    f = h.doc_facts(text)
    assert "ACP-18300V1.0" in f["ids"]
    assert any("Siemens" in x for x in f["makers"]) and any("62 MW" in x for x in f["sizes"])
    assert any("Section 12" in x for x in f["location"]) and f["coords"] == ["48.1234, -103.5678"]


def test_fac_block_and_facilities_json_shape(tmp_path):
    f = h.new_fac("ceris:-111", "Applied Digital Polaris Forge 1 - AQ", "CERIS site")
    f.update(city="Ellendale", county="Dickey", ceris_ids=["-111"], codes=["Computer Processing (7374)"],
             permits=[{"number": "ACP-1", "type": "Air Permit to Construct", "kind": "Minor", "status": "In Effect",
                       "effective": "2025-01-01", "expires": ""}],
             docs=[{"name": "Permit", "url": "https://ceris.deq.nd.gov/ext/ncore/downloadpdf/1", "date": "2025-01-01",
                    "state": "saved", "facts": {"sizes": ["20 x 3 MW diesel generators"]}}])
    block = "\n".join(h.fac_block(f))
    assert block.startswith("- Applied Digital Polaris Forge 1 - AQ (CERIS site -111): Ellendale, Dickey County")
    assert "codes: Computer Processing (7374)" in block and "size: 20 x 3 MW" in block
    s = h.slim(f)
    json.dumps(s)
    assert s["permits"][0]["number"] == "ACP-1" and s["docs"][0]["url"].endswith("/1") and s["codes"]

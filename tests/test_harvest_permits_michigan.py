"""Parsers of the Michigan air permit harvester, on saved snippets (no network)."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from paths import load_scope_module  # noqa: E402

h = load_scope_module("us-mi", "harvest_permits")

LISTING = """<pre><A HREF="/aps/downloads/SRN/">[To Parent Directory]</A><br><br> 7/28/2015  6:41 PM       102411 <A HREF="/aps/downloads/SRN/B6527/B6527_FCE_20140612.pdf">B6527_FCE_20140612.pdf</A><br>  4/4/2024  3:45 PM       &lt;dir&gt; <A HREF="/aps/downloads/SRN/B6527/old/">old</A><br></pre>"""

ACTIVE = """                                     Active PTIs Approved since 1997 Sorted by State Registration No. (SRN)
Company                      SRN     Address                            City                     ZIP Code County    PTI No.    Approved Notes
DETROIT WATER & SEWERAGE             CORNER OF DUBOIS & ATWATER         DETROIT                   48207   WAYNE     254-00      1/16/2001
MIDLAND COGENERATION            B6527   100 E PROGRESS PLACE              MIDLAND                   48640   MIDLAND     103-12     4/23/2013 Rolled into ROP
MIDLAND COGENERATION            B6527   100 E PROGRESS PLACE              MIDLAND                   48640   MIDLAND     80-22      6/16/2022
"""

PENDING = """Company                                    SRN     Site Address         Site City            Site ZIP   Site County   APP / PTI No.    Received Reviewer
DTE ELECTRIC COMPANY                       B2796   4505 KING ROAD       CHINA                 48054     SAINT CLAIR   APP-2024-0273   11/8/2024 A PERSON
                                                   ROAD

Application Reason: CONVERT UTILITY BOILERS TO NATURAL GAS
"""

NOTICE_TOC = """               New Source Review Permits Open for Comment
The following permits are open for comment:
J. H. Campbell Plant – PKG-0000892................................................................................ 1
Submitting Comments ........................................................................................................ 2

J. H. Campbell Plant – PKG-0000892
EGLE is holding a public comment period. Air permit application package No. PKG-0000892 is a request
to install and operate a coal ash processing facility. Call 517-284-0900 or write EGLE-AQD@Michigan.gov.

Submitting Comments
Interested individuals may provide verbal comments.
"""

NOTICE_OLD = """                New Source Review Permits Open for Comment
Arauco North America – Permit to Install Application No. 59-16E
EGLE is holding a public comment period for Arauco North America located at 5851 Arauco Road, Grayling.
Example Power LLC – APP-2022-0079
The company proposes to install two natural gas combustion turbines.
"""

DOC = """The applicant proposes to construct two GE 7HA.02 combustion turbines in combined cycle.
Each turbine has a heat input of 3,500 MMBtu/hr and the plant is rated at 1,200 MW.
The facility is located at 1000 Example Road, Milan, Michigan 48160. PTI0000174 v1.0 and APP-2024-0273.
Coordinates 42.0852, -83.6821"""


def test_srn_and_wkt():
    assert h.split_srn("Midland Cogeneration Venture (B6527)") == ("Midland Cogeneration Venture", "B6527")
    assert h.split_srn("No srn here") == ("No srn here", "")
    assert h.parse_wkt("POINT(-88.6166085 46.7936854)") == (46.7936854, -88.6166085)
    assert h.parse_wkt(None) == (None, None)
    assert h.iso("2026-10-12T08:30:53-04:00") == "2026-10-12" and h.iso("6/16/2022") == "2022-06-16"


def test_cluster_rows():
    one = h.cluster_rows({"siteId": "-5", "siteName": "Zeeland Generating (N6521)", "city": "ZEELAND",
                          "geographyWKT": "POINT(-86.0 42.8)"})
    assert one["-5"]["lat"] == 42.8 and one["-5"]["city"] == "ZEELAND"
    many = h.cluster_rows({"clusterCount": 2, "clusterSites": '[{"siteId":"1","siteName":"A (B0001)"},'
                                                               '{"siteId":"2","siteName":"B (B0002)"}]'})
    assert set(many) == {"1", "2"}


def test_listing():
    r = h.parse_listing(LISTING)
    assert r[0]["date"] == "2015-07-28" and r[0]["url"].endswith("B6527_FCE_20140612.pdf")
    assert r[1]["size"] == "dir"


def test_active_ptis():
    r = h.parse_active_ptis(ACTIVE)
    assert [x["pti"] for x in r] == ["103-12", "80-22"]
    assert r[1]["approved"] == "2022-06-16" and r[1]["url"].endswith("/finpticon/2022/80-22.pdf")
    assert r[0]["note"] == "Rolled into ROP"


def test_pending_apps():
    r = h.parse_pending_apps(PENDING)
    assert r[0]["srn"] == "B2796" and r[0]["app"] == "APP-2024-0273" and r[0]["received"] == "2024-11-08"
    assert r[0]["reason"] == "CONVERT UTILITY BOILERS TO NATURAL GAS" and r[0]["county"] == "SAINT CLAIR"


def test_notice_list_with_contents():
    links = {0: ["https://www.egle.state.mi.us/aps/downloads/permits/PubNotice/PKG-0000892/PKG-0000892TFS.pdf",
                 "https://bit.ly/x"]}
    r = h.parse_notice_list(NOTICE_TOC, "open for comment", "20261015", links)
    assert len(r) == 1 and r[0]["facility"] == "J. H. Campbell Plant" and "PKG-0000892" in r[0]["ids"]
    assert "coal ash" in r[0]["text"] and "Interested individuals" not in r[0]["text"]
    assert "[phone]" in r[0]["text"] and "[email]" in r[0]["text"] and "517-284" not in r[0]["text"]
    assert [d["name"] for d in r[0]["docs"]] == ["PKG-0000892TFS.pdf"]


def test_notice_list_old_format_and_merge():
    r = h.parse_notice_list(NOTICE_OLD, "open for comment", "20201021")
    assert [x["facility"] for x in r] == ["Arauco North America", "Example Power LLC"]
    assert "turbines" in r[1]["text"] and "Arauco" not in r[1]["text"]
    again = h.parse_notice_list(NOTICE_OLD, "open for comment", "20201104")
    m = h.merge_notices(r + again)
    assert len(m) == 2 and m[0]["seen"] == {"20201021", "20201104"}


def test_doc_facts():
    f = h.doc_facts(DOC)
    assert "PTI0000174 v1.0" in f["ids"] and "APP-2024-0273" in f["ids"]
    assert f["sizes"] and f["makers"] and f["location"] and f["project"]
    assert f["coords"] == ["42.0852, -83.6821"]


def test_power_filter_and_match():
    gas = {"name": "Zeeland Generating Station", "city": "ZEELAND", "sources": ["name search 'Zeeland'"]}
    mill = {"name": "Example Sawmill Power House", "city": "ZEELAND", "sources": []}
    coded = {"name": "Example Lumber", "city": "X", "sources": ["NAICS 221112"]}
    dc = {"name": "Project Mitten", "city": "SALINE", "sources": []}
    assert h.is_power(gas) and not h.is_power(mill) and h.is_power(coded) and h.is_power(dc)
    plant = {"id": "L1", "name": "Zeeland", "city": "Zeeland", "name_words": h.words("Zeeland")}
    other = {"name": "Zeeland Board of Public Works Peaking", "city": "ZEELAND", "sources": []}
    got = h.match(plant, [gas, other, mill])
    assert (gas, "name match, check it is this plant") in got and (other, "name match, check it is this plant") in got
    city_only = {"id": "L2", "name": "Sumpter", "city": "Belleville", "name_words": h.words("Sumpter")}
    near = {"name": "Example Peaking Station", "city": "BELLEVILLE", "sources": []}
    assert h.match(city_only, [near]) == [(near, "same city, power-like name, check it is this plant")]


def test_known_patterns_win():
    h.KNOWN["L9"] = [r"\bkarn\b"]
    try:
        plant = {"id": "L9", "name": "Dan E Karn", "city": "Essexville", "name_words": h.words("Dan E Karn")}
        karn = {"name": "Consumers Energy D.E. Karn", "city": "ESSEXVILLE", "sources": []}
        other = {"name": "Essexville Peaking Power", "city": "ESSEXVILLE", "sources": []}
        assert h.match(plant, [karn, other]) == [(karn, "checked by hand")]
    finally:
        del h.KNOWN["L9"]


def test_known_srn_and_possible_sites():
    h.KNOWN["L8"] = [r"\(b2796\)", r"?\(n6945\)"]
    try:
        plant = {"id": "L8", "name": "Blue Water energy center", "city": "East China", "name_words": h.words("Blue Water")}
        br = {"name": "DTE St. Clair / Belle River Power Plant", "srn": "B2796", "city": "EAST CHINA", "sources": []}
        bw = {"name": "DTE Electric Company", "srn": "N6945", "city": "EAST CHINA", "sources": []}
        other = {"name": "Blue Water Peaker", "srn": "N0001", "city": "EAST CHINA", "sources": []}
        assert h.match(plant, [br, bw, other]) == [
            (br, "checked by hand"), (bw, "checked by hand as a possible site, check it is this plant")]
    finally:
        del h.KNOWN["L8"]


def test_watch_list_sites_count_as_power():
    assert h.is_power({"name": "Consumers Energy J H Campbell Complex", "srn": "B2835", "codes": []})
    assert all(re.fullmatch(r"[A-Z]\d{4}", k) for k in h.WATCH)
    for pid, pats in h.KNOWN.items():
        assert pid.startswith("L1000") and pats
        for p in pats:
            re.compile(p.lstrip("?"))
    assert {"B6527", "B2796", "N6945"} <= h.known_srns()


def test_notice_matches_site():
    site = {"name": "DTE St. Clair / Belle River Power Plant", "srn": "B2796"}
    assert h.notice_matches(site, {"facility": "DTE Electric Company – Belle River", "text": ""})
    assert h.notice_matches(site, {"facility": "Someone", "text": "SRN B2796 is"})
    assert not h.notice_matches(site, {"facility": "Marathon Petroleum Company LP", "text": ""})
    assert not h.notice_matches(site, {"srn": "N6631", "facility": "Belle River"})


def test_doc_ranking_and_cap():
    site = {"documents": [
        {"name": "Stack Test Report.pdf", "url": "u1", "category": "Air Compliance", "date": "2026-01-01",
         "number": "", "kind": ""},
        {"name": "PTI0000174 Final.pdf", "url": "u2", "category": "Air Permit to Install Documents",
         "date": "2026-01-14", "number": "PTI0000174", "kind": ""},
        {"name": "Technical Fact Sheet.pdf", "url": "u3", "category": "Air Application Documents",
         "date": "2025-10-01", "number": "APP-2025-0001", "kind": ""},
        {"name": "Technical Fact Sheet (Spanish).pdf", "url": "u4", "category": "Air Application Documents",
         "date": "2025-10-01", "number": "APP-2025-0001", "kind": ""}],
        "legacy_rop": []}
    ptis = [{"pti": "8-17", "approved": "2017-03-01", "url": "u5"}]
    read, rest = h.fac_docs(site, [], ptis, 2)
    assert [d["url"] for d in read] == ["u3", "u2"] and [d["url"] for d in rest] == ["u5"]

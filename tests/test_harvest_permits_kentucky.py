"""Offline tests for scopes/us-ky/harvest_permits.py: eSearch grouping and document keys, the
DAQ notices page, both Louisville APCD pages, plant matching and the sweep test. No network."""
import json
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from paths import load_scope_module  # noqa: E402

h = load_scope_module("us-ky", "harvest_permits")


def es_row(aid, name, county, code, year, num, issued="", milestone="", mdate="", docs=0, atype="Title V"):
    return {"AgencyId": aid, "AgencyName": name, "County": county, "Municipality": "Somewhere (City)",
            "ActivityCode": code, "ActivityYear": year, "ActivityNum": num, "ActivityType": atype,
            "CurrentMilestone": milestone, "MilestoneDate": mdate, "IssuedDate": issued, "DetailRows": docs}


def test_doc_key_is_percent_encoded_json():
    key = h.doc_key(es_row(183908, "Liberty Station", "Casey", "APE", 2024, 1))
    assert "%7B" in key and "{" not in key and " " not in key
    assert json.loads(urllib.parse.unquote(key)) == {"AgencyId": 183908, "ActivityCode": "APE",
                                                      "ActivityYear": 2024, "ActivityNumber": 1}


def test_esearch_groups_by_agency_interest():
    issued = [es_row(183908, "EKPC Liberty Station", "Casey", "APE", 2024, 1, issued="2025-06-02T00:00:00", docs=4),
              es_row(183908, "EKPC Liberty Station", "Casey", "APE", 2023, 7, issued="03/01/2024")]
    pending = [es_row(183908, "EKPC Liberty Station", "Casey", "APE", 2026, 2, milestone="Draft", mdate="2026-10-28T00:00:00"),
               {"AgencyId": "x"}]
    facs = h.esearch_facilities(issued, pending)
    assert list(facs) == ["ai-183908"]
    f = facs["ai-183908"]
    assert f["county"] == "Casey" and f["city"] == "Somewhere"
    assert [a["activity"] for a in f["activities"]] == ["APE 2026-2", "APE 2024-1", "APE 2023-7"]
    assert f["activities"][1]["issued"] == "2025-06-02" and f["activities"][2]["issued"] == "2024-03-01"
    assert f["activities"][0]["status"] == "pending"


NOTICES = ('<a href="/Environmental-Protection/Air/Draft%20Permit%20Documents/Bluegrass%20Generation%20Company%20-%20'
           'Draft%20Permit%20V-26-012.pdf">x</a> <a href="/Environmental-Protection/Air/Draft%20Permit%20Documents/'
           'Bluegrass%20Generation%20Company%20-%20Statement%20of%20Basis.pdf">y</a> <a href="/Environmental-Protection/'
           'Air/Draft%20Permit%20Documents/Bluegrass%20Generation%20Company%20-%20Draft%20Permit%20V-26-012.pdf">dup</a>'
           '<a href="/Environmental-Protection/Air/Draft%20Permit%20Documents/LoneName.pdf">z</a>')


def test_parse_notices_and_facilities():
    n = h.parse_notices(NOTICES)
    assert set(n) == {"Bluegrass Generation Company", "LoneName"}
    assert [d["kind"] for d in n["Bluegrass Generation Company"]] == ["Draft Permit V-26-012", "Statement of Basis"]
    assert n["LoneName"][0]["kind"] == "document"
    assert n["Bluegrass Generation Company"][0]["url"].startswith("https://eec.ky.gov/Environmental-Protection/")
    facs = h.notice_facilities(n)
    f = facs["daq-notice-bluegrass-generation-company"]
    assert f["permits"][0]["number"] == "V-26-012" and len(f["docs"]) == 2


ACTIVE = ("<p><strong>Louisville Gas and Electric - Mill Creek</strong><br>"
          '<a href="/sites/default/files/mc.pdf">Permit O-0127-23-V</a> Effective&nbsp;5/1/2024</p>'
          "<p><strong></strong></p>"
          "<p><strong>Louisville Gas and Electric - Mill Creek</strong><br>"
          '<a href="https://louisvilleky.gov/sites/default/files/mc2.pdf">Statement of Basis O-0127-23-V</a></p>')
PROPOSED = ("<main><table><tr><th>Action</th></tr><tr><td>Proposed Revision for Louisville Gas and Electric - Mill Creek, "
            '<a href="/sites/default/files/draft.pdf">Draft Permit O-0127-26-V</a></td>'
            "<td>10/1/2026 to 10/31/2026</td><td>No hearing requested</td></tr></table></main>")


def test_apcd_pages():
    act = h.parse_apcd_active(ACTIVE)
    assert len(act) == 2 and act[0]["effective"] == "2024-05-01"
    assert act[0]["permits"][0] == {"number": "O-0127-23-V", "kind": "Permit O-0127-23-V",
                                    "url": "https://louisvilleky.gov/sites/default/files/mc.pdf"}
    prop = h.parse_apcd_proposed(PROPOSED)
    assert prop[0]["action"] == "Proposed Revision" and prop[0]["name"] == "Louisville Gas and Electric - Mill Creek"
    assert prop[0]["comment_begins"] == "2026-10-01" and prop[0]["comment_ends"] == "2026-10-31"
    facs = h.apcd_facilities(act, prop)
    merged = facs["apcd-o-0127-23-v"]
    assert len(merged["links"]) == 2 and len(merged["permits"]) == 1 and merged["county"] == "Jefferson"
    assert facs["apcd-proposed-louisville-gas-and-electric-mill-creek"]["permits"][0]["number"] == "O-0127-26-V"


def plant(pid, name, county):
    return {"id": pid, "name": name, "city": "", "county": county, "statuses": [], "name_words": h.words(name)}


def test_match_known_and_by_name():
    facs = list(h.esearch_facilities([es_row(3808, "EKPC Cooper Station", "Pulaski", "APE", 2024, 1),
                                      es_row(99, "Newtown Power Station", "Hart", "APE", 2024, 1),
                                      es_row(98, "Newtown Water Plant", "Hart", "APE", 2024, 1)], []).values())
    facs += list(h.apcd_facilities(h.parse_apcd_active(ACTIVE), []).values())
    cooper = h.match(plant("L100000103935", "Cooper power station", "Pulaski"), facs)
    assert [(f["ai"], how) for f, how in cooper] == [(3808, "checked by hand")]
    mill = h.match(plant("L100000103945", "Mill Creek power station", "Jefferson"), facs)
    assert len(mill) == 1 and mill[0][1] == "checked by hand"
    new = h.match(plant("L999", "Newtown Generating Station", "Hart"), facs)
    assert [f["ai"] for f, _ in new] == [99]
    assert h.match(plant("L999", "Newtown Generating Station", "Barren"), facs) == []


def test_sweep_keep():
    assert h.sweep_keep("A hyperscale data center campus") == "names a data center"
    assert h.sweep_keep("Twelve emergency diesel generators, 3 MW each") == "lists generators or turbines"
    assert h.sweep_keep("One emergency generator at the pump house") == ""

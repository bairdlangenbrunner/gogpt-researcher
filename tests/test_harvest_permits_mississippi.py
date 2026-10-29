"""Parsers of the Mississippi permit harvester, on saved snippets (no network)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from paths import load_scope_module  # noqa: E402

h = load_scope_module("us-ms", "harvest_permits")

ACTIVE = """<table><tr><th>AI ID</th></tr>
<tr><td>86260</td><td><a href="ai_info.aspx?ai=86260">Entergy Mississippi LLC Delta Blues Advanced Power Station</a></td>
<td>2800-00142</td><td>Air - Construction PSD</td><td>Greenville</td><td>Washington</td></tr></table>"""

ACTIVITY = """<h2 class='countytitle'>Washington</h2>
<table id="uxReport"><tr><td><p class="countylist"><a href="ai_info.aspx?ai=86260">Entergy Delta Blues</a>, Greenville, MS applied for Air - Construction PSD permit 2800-00142 on 03/04/2024.</p></td></tr></table>"""

NOTICE = """<tr><td><a href="ai_info.aspx?ai=7">Chevron Pascagoula</a></td><td>Air - Construction Permit</td><td>Pascagoula</td><td>Jackson</td><td>11/13/2026</td>
<td><a href='get_doc.aspx?dt=pnotice&amp;id=11'>Notice</a></td><td><a href='get_doc.aspx?dt=dpermit&amp;id=12'>Draft</a></td><td></td></tr>"""

AGENDA = """Mississippi Environmental Quality Permit Board
September 25, 2025
Facility: Example Power LLC
Air Division: Air II Branch, Issuance of: Air Title V Operating Permit 1780-00080.
Facility: A Bakery
Water Division, NPDES permit.
"""

DOC = """The facility proposes to construct two simple cycle combustion turbines.
Each Siemens SGT-800 turbine is rated at 62 MW.
The site is located at 221 Stokes King Road in Greenville, Mississippi 38701.
Permit 2800-00142. Coordinates 33.4012, -91.0612"""


def test_active_rows():
    r = h.parse_active(ACTIVE)
    assert r[0]["ai"] == 86260 and r[0]["permit"] == "2800-00142" and r[0]["county"] == "Washington"


def test_activity_rows():
    r = h.parse_activity(ACTIVITY)
    assert r[0]["county"] == "Washington" and r[0]["date"] == "2024-03-04" and h.air_sentence(r[0])


def test_notice_rows():
    r = h.parse_notice_page(NOTICE)
    assert r[0]["end"] == "2026-11-13"
    assert [d["name"] for d in r[0]["docs"]] == ["public notice", "draft permit"]
    assert "get_doc.aspx?dt=pnotice&id=11" in r[0]["docs"][0]["url"]


def test_board_items_and_date():
    its = h.board_items(AGENDA)
    assert len(its) == 1 and its[0]["permits"] == ["1780-00080"] and its[0]["facility"] == "Example Power LLC"
    assert h.meeting_date(AGENDA, "") == "2025-09-25"


def test_doc_facts():
    f = h.doc_facts(DOC)
    assert f["ids"] == ["2800-00142"] and f["sizes"] and f["makers"] and f["location"] and f["coords"]


def test_power_filter_and_known():
    assert h.is_power({"name": "Entergy Mississippi LLC, Hinds County Plant", "sic_power": False})
    assert not h.is_power({"name": "Smith Lumber Co", "sic_power": False})
    plant = {"id": "L100001064651", "name": "Traceview", "city": "Ridgeland", "name_words": set()}
    facs = [{"name": "Entergy Mississippi LLC, Madison County Advanced Power Station", "city": "Ridgeland"}]
    assert h.match(plant, facs)[0][1] == "checked by hand"
    xai = {"id": "L100001047324", "name": "Colossus 2", "city": "", "name_words": set()}
    assert h.match(xai, [{"name": "MZX Tech LLC", "city": "Southaven"}])

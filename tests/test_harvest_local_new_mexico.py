"""Offline tests for scopes/us-nm/harvest_local.py: dates from file names and rows, the Legistar,
CivicClerk, AgendaCenter, IQM2, Granicus and San Juan County readers, and what a document is
searched for. No network."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from paths import load_scope_module  # noqa: E402

h = load_scope_module("us-nm", "harvest_local")
FX = Path(__file__).parent / "fixtures" / "harvest_local_new_mexico"
BODY = {"id": "test-body", "name": "Test County Commission", "county": "Lea", "reader": "pages", "site": "https://www.example.gov"}


class FakeNet:
    """Answers net.json(url) from a table keyed by a substring of the URL."""
    def __init__(self, table):
        self.table = table

    def json(self, url, params=None):
        for key, val in self.table.items():
            if key in url:
                return val
        return None


def fx(name):
    return json.loads((FX / name).read_text())


def test_date_of():
    cases = {"SCBOC2026311min": "2026-03-11", "SCBOC20261112min.pdf": "2026-11-12", "_01132026-452": "2026-01-13",
             "Agenda for November 3, 2026": "2026-11-03", "02082024-1745-agenda.pdf": "2024-02-08",
             "/wp-content/uploads/2025/05/agenda.pdf": "2025-05-01", "Nov 17, 2026 - 06:00 PM": "2026-11-17",
             "c301a58cf2d8457e92a64bc66b69b715.pdf": ""}
    assert {k: h.date_of(k) for k in cases} == cases


def test_county_names_normalize():
    assert {h.norm_nm_county(x) for x in ("Doña Ana", "Dona Ana County", "DONA ANA")} == {"Dona Ana"}
    assert h.norm_nm_county("Lea County") == "Lea"


def test_legistar_lists_files_and_power_items_only():
    body = {"id": "abq", "name": "Albuquerque City Council", "county": "Bernalillo", "client": "cabq", "body_id": 1}
    net = FakeNet({"/Events/7001/EventItems": fx("legistar_items_7001.json"), "/Events/7002/EventItems": fx("legistar_items_7002.json"),
                   "/Events": fx("legistar_events.json")})
    docs = h.list_legistar(net, body, "2026-01-01", "2026-11-17")
    got = [(d["date"], d["kind"]) for d in docs]
    assert got == [("2026-10-20", "agenda"), ("2026-10-20", "packet"), ("2026-09-15", "agenda"), ("2026-09-15", "minutes")]
    att = [d for d in docs if d["kind"] == "packet"][0]
    assert att["url"].endswith("/Matters/555/Attachments/901/File") and "data center" in att["item"]


def test_civicclerk_lists_published_files():
    body = {"id": "hobbs", "name": "Hobbs", "county": "Lea", "api": "https://hobbsnm.api.civicclerk.com/v1"}
    docs = h.list_civicclerk(FakeNet({"/Events": fx("civicclerk_events.json")}), body, "2026-01-01", "2026-11-17")
    assert [(d["date"], d["kind"]) for d in docs] == [("2026-11-09", "agenda"), ("2026-11-09", "packet")]
    assert docs[0]["url"] == "https://hobbsnm.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=493,plainText=false)"
    assert h.doc_file(Path("/x"), docs[0]).name == "2026-11-09_agenda_file493.pdf"


def test_parse_agendacenter():
    docs = h.parse_agendacenter((FX / "agendacenter_listing.html").read_text(), {**BODY, "site": "https://www.eddycountynm.gov"})
    assert [(d["date"], d["kind"], d["url"].rsplit("/", 1)[-1]) for d in docs] == [
        ("2026-01-13", "agenda", "_01132026-452"), ("2026-01-13", "minutes", "_01132026-452")]
    assert docs[0]["url"] == "https://www.eddycountynm.gov/AgendaCenter/ViewFile/Agenda/_01132026-452"


IQM2 = """<div class="Row MeetingRow"  id="divRow"><div class="RowTop"><div class="RowLink">
<a href="/Citizens/Detail_Meeting.aspx?ID=4051" title="TUESDAY, JANUARY 6, 2026  5:00 PM&#13;&#13;Board:&#09;Board of County Commissioners&#13;Type:&#09;Regular Meeting&#13;Status:&#09;Scheduled" >Jan 6</a></div>
<div class="RowRight MeetingLinks"><div>&nbsp;<a href='FileOpen.aspx?Type=14&ID=3664&Inline=True' target='_blank'>Agenda</a>&nbsp;</div>
<div>&nbsp;<a href='FileOpen.aspx?Type=12&ID=3282&Inline=True' target='_blank'>Verbatim Minutes</a>&nbsp;</div></div></div></div>
<div class="Row MeetingRow"  id="divRow"><div class="RowTop"><div class="RowLink">
<a href="/Citizens/Detail_Meeting.aspx?ID=4052" title="MONDAY, JANUARY 5, 2026  5:00 PM&#13;&#13;Board:&#09;Arts Board&#13;Type:&#09;Regular Meeting" >Jan 5</a></div>
<div class="RowRight MeetingLinks"><div><a href='FileOpen.aspx?Type=14&ID=1&Inline=True'>Agenda</a></div></div></div></div>"""


def test_iqm2_keeps_only_the_wanted_boards():
    body = {"id": "bc", "name": "Bernalillo County", "boards": r"Board of County Commissioners"}
    docs = h.parse_iqm2(IQM2, body, "https://bernalillocountynm.iqm2.com/Citizens")
    assert [(d["date"], d["kind"]) for d in docs] == [("2026-01-06", "agenda"), ("2026-01-06", "minutes")]
    assert docs[0]["url"] == "https://bernalillocountynm.iqm2.com/Citizens/FileOpen.aspx?Type=14&ID=3664&Inline=True"
    assert h.doc_file(Path("/x"), docs[0]).name == "2026-01-06_agenda_iqm2_type14_id3664.pdf"


GRANICUS = """<tr class="listingRow"><td class="listItem" headers="Name" scope="row">Planning and Zoning Board</td>
<td class="listItem" headers="Date">Nov&nbsp;17,&nbsp;2026 - 06:00&nbsp;PM</td>
<td class="listItem" headers="AgendaLink"><a href="//riorancho.granicus.com/AgendaViewer.php?view_id=14&event_id=2634">Agenda</a></td>
<td class="listItem" headers="AgendaPacketLink"><a href="https://d3n9.cloudfront.net/riorancho/x.pdf">Agenda
 Packet</a></td></tr>
<tr class="listingRow"><td class="listItem" headers="Name" scope="row">Parks and Recreation</td><td class="listItem" headers="Date">Nov 16, 2026</td>
<td><a href="//riorancho.granicus.com/AgendaViewer.php?view_id=14&event_id=9">Agenda</a></td></tr>"""


def test_granicus_rows():
    body = {"id": "rr", "name": "Rio Rancho", "site": "https://riorancho.granicus.com", "boards": r"Governing Body|Planning and Zoning"}
    docs = h.parse_granicus(GRANICUS, body)
    assert [(d["date"], d["kind"]) for d in docs] == [("2026-11-17", "agenda"), ("2026-11-17", "packet")]
    assert docs[0]["url"] == "https://riorancho.granicus.com/AgendaViewer.php?view_id=14&event_id=2634"
    assert h.doc_file(Path("/x"), docs[0]).name == "2026-11-17_agenda_agenda2634.pdf"


SJ = ("<tr><td class='title_column event_title'><a href=\"/x\"><span itemprop='summary'>San Juan County Commission Meeting</span></a></td>"
      "<td class='event_datetime'>11/10/2026 4:00 PM <time>x</time></td><td class='event_agenda'><span>Agenda:</span>"
      "<a class='agenda_minutes_link' href='/home/showpublisheddocument/10238/639294920794870000'>11.10.26 Agenda</a></td>"
      "<td class='event_minutes'>Not Included</td><td class='event_other'>Not Included</td></tr>")


def test_sjcounty_rows():
    docs = h.parse_sjcounty(SJ, {"id": "sj", "name": "San Juan", "site": "https://www.sjcounty.net"})
    assert [(d["date"], d["kind"]) for d in docs] == [("2026-11-10", "agenda")]
    assert docs[0]["url"] == "https://www.sjcounty.net/home/showpublisheddocument/10238/639294920794870000"


INDEX = """<a href="/wp-content/uploads/2025/05/05272025-123.pdf">May 27 agenda</a>
<a href="/Docs/2026 November Agenda.pdf?t=1">November Agenda</a><a href="/flyer.pdf">Flyer</a>"""


def test_parse_links():
    docs = h.parse_links(INDEX, "https://www.example.gov/agenda-center/", BODY, "2025-01-01")
    assert [d["date"] for d in docs] == ["2025-05-27", "2026-01-01"]


TEXT = """CALL TO ORDER. Approval of the minutes of the prior meeting.
The commission will hold a hearing on an industrial revenue bond for a data center with a 300 MW microgrid in Santa Teresa.
Staff reported on the Hobbs Generating Station and a request from El Paso Electric.
Approval to purchase a generator for the county garage.
The commission approved road paving on Main Street."""


def test_findings():
    pats = h.plant_patterns([{"id": "L100000402045", "name_words": {"hobbs"}}])
    f = h.findings(TEXT, pats, ["L100000402045", "L100000402297"])
    assert f["named"] == ["L100000402045"] and "Santa Teresa data centers" in f["leads"]
    assert not any("garage" in s or "paving" in s for s in f["sentences"])
    assert "industrial revenue bond" in f["context"] and f["nearby"] == ["L100000402297"]


def test_common_names_need_a_plant_word():
    pats = h.plant_patterns([{"id": "L100000402045", "name_words": {"hobbs"}}, {"id": "L100000401601", "name_words": {"luna"}}])
    people = "Mayor Sam Cobb of Hobbs and Luna County Commissioner Smith spoke about road paving."
    assert h.findings(people, pats, [])["named"] == []
    plant = "The Luna Energy Facility and the Hobbs Generating Station were discussed."
    assert sorted(h.findings(plant, pats, [])["named"]) == ["L100000401601", "L100000402045"]


def test_write_outputs(tmp_path):
    plants = [{"id": "L100000402045", "name": "Hobbs generating station", "county": "Lea"}]
    rec = {**h.doc(BODY, "https://www.example.gov/a.pdf", "Agenda", "2026-11-03"),
           **h.findings(TEXT, h.plant_patterns([{"id": "L100000402045", "name_words": {"hobbs"}}]), [])}
    bodies = [{"id": "test-body", "name": "Test County Commission", "county": "Lea", "reader": "pages", "state": "1 documents listed"}]
    h.write_outputs(tmp_path, plants, bodies, [rec], "2024-01-01", "2026-11-17")
    data = json.loads((tmp_path / "local_records.json").read_text())
    assert data["by_plant"] == {"L100000402045": [0]}
    assert any(n["county"] == "Lea" and n["plants"] == ["L100000402045"] for n in data["not_posted"])
    md = (tmp_path / "local_records.md").read_text()
    assert "### Hobbs generating station (L100000402045)" in md and "New Mexico local planning" in md


def test_bodies_and_leads():
    ids = [b["id"] for b in h.BODIES]
    assert len(ids) == len(set(ids)) and {"hobbs", "grant-county", "san-juan-county"} <= set(ids)
    assert all(b["reader"] in h.LISTERS for b in h.BODIES)
    assert re.search(h.LEADS["Lea County Data Center"], "New Era Energy and Digital", re.I)
    assert re.search(h.LEADS["Site Layer 1"], "Wärtsilä engines for the Grant County site", re.I)


def test_load_plants_reads_the_scoped_export():
    plants = h.load_plants()
    assert plants and all(p["id"].startswith("L1") for p in plants)
    assert {p["county"] for p in plants if p["name"].startswith("Project Jupiter")} <= {"Dona Ana"}

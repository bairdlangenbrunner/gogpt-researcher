"""Offline tests for scopes/us-ky/harvest_local.py: dates from file names and rows, the
AgendaCenter and index page readers, and what a document is searched for. No network."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from paths import load_scope_module  # noqa: E402

h = load_scope_module("us-ky", "harvest_local")
BODY = {"id": "test-body", "name": "Test County Fiscal Court", "county": "Henderson", "reader": "pages",
        "site": "https://www.example.gov"}


def test_date_of():
    cases = {"100826 CCregular.pdf": "2026-10-08", "Document Center/Minutes/2026/081326 CC regular.pdf": "2026-08-13",
             "_10262026-12": "2026-10-26", "Agenda for November 3, 2026": "2026-11-03", "Sept. 9, 2025 minutes": "2025-09-09",
             "/wp-content/uploads/2025/03/agenda.pdf": "2025-03-01", "2026-10-05 minutes": "2026-10-05",
             "FCM 9-8-26.pdf": "2026-09-08", "c301a58cf2d8457e92a64bc66b69b715.pdf": "", "13/45/2026": ""}
    assert {k: h.date_of(k) for k in cases} == cases


AC = """
<tr id="row5652d9592b4" class="catAgendaRow"><td><h3 class="noMargin" id="h411032026-565">
 <a id="_11032026-565" name="_11032026-565"></a><strong aria-label="Agenda for November 3, 2026">Nov 3, 2026</strong></h3>
 <p><a id="11032026-565" name="565" href="/AgendaCenter/ViewFile/Agenda/_11032026-565" target="_blank" aria-describedby="h411032026-565">
  Special Called Meeting</a></p></td><td class="minutes"></td>
 <td class="downloads"><ol><li><a class="pdf" href="/AgendaCenter/ViewFile/Agenda/_11032026-565">Agenda</a></li>
 <li><a href="/AgendaCenter/ViewFile/Agenda/_11032026-565?packet=true">Packet</a></li></ol></td></tr>
<tr id="row562ee50a477" class="catAgendaRow"><td><h3 class="noMargin" id="h410272026-562">
 <a id="_10272026-562" name="_10272026-562"></a></h3><p>
 <a id="10272026-562" name="562" href="/AgendaCenter/ViewFile/Agenda/_10272026-562" aria-describedby="h410272026-562">
  Regular Fiscal Court Meeting</a></p></td>
 <td class="minutes"><a href="/AgendaCenter/ViewFile/Minutes/_10272026-562" aria-label="Minutes"><img alt="Minutes"></a></td></tr>
"""


def test_parse_agendacenter():
    docs = h.parse_agendacenter(AC, BODY)
    got = [(d["date"], d["kind"], d["url"].rsplit("/", 1)[-1], d["title"]) for d in docs]
    assert got == [("2026-11-03", "agenda", "_11032026-565", "Special Called Meeting agenda"),
                   ("2026-11-03", "packet", "_11032026-565?packet=true", "Special Called Meeting packet"),
                   ("2026-10-27", "agenda", "_10272026-562", "Regular Fiscal Court Meeting agenda"),
                   ("2026-10-27", "minutes", "_10272026-562", "Regular Fiscal Court Meeting minutes")]
    assert docs[0]["url"] == "https://www.example.gov/AgendaCenter/ViewFile/Agenda/_11032026-565"


INDEX = """
<table><tr><th>Meeting Date</th><th>Agenda</th><th>Minutes</th></tr>
<tr><td>10/26/2026</td><td><a href="https://www.example.gov/assets/AgendaMinutes/c301a58c.pdf">Agenda</a></td>
 <td><a href="/assets/AgendaMinutes/d37a89b3.pdf">Meeting Minutes</a></td></tr>
<tr><td>3/9/2023</td><td><a href="/assets/AgendaMinutes/0477c11a.pdf">Agenda</a></td></tr></table>
<a href="/Document Center/Agendas/100826 CCregular.pdf?t=202610051103170">Agenda</a>
<a href="/files/2025 Minutes.pdf">2025 minutes</a>
<a href="/about.php">About</a> <a href="/flyer.pdf">Flyer</a>
"""


def test_parse_links_dates_from_rows_names_and_years():
    docs = h.parse_links(INDEX, "https://www.example.gov/AgendaMinutes", BODY, "2024-01-01")
    got = [(d["date"], d["kind"], d["url"].rsplit("/", 1)[-1]) for d in docs]
    assert got == [("2026-10-26", "agenda", "c301a58c.pdf"), ("2026-10-26", "minutes", "d37a89b3.pdf"),
                   ("2026-10-08", "agenda", "100826%20CCregular.pdf?t=202610051103170"),
                   ("2025-01-01", "minutes", "2025%20Minutes.pdf")]
    assert docs[1]["url"] == "https://www.example.gov/assets/AgendaMinutes/d37a89b3.pdf"
    # a year-only date passes a since date inside that year; a dated row before it does not
    later = h.parse_links(INDEX, "https://www.example.gov/", BODY, "2025-06-01")
    assert [d["date"] for d in later] == ["2026-10-26", "2026-10-26", "2026-10-08", "2025-01-01"]


TEXT = """CALL TO ORDER. Approval of the minutes of the prior meeting.
The Henderson City-County Planning Commission will hold a public hearing on a proposed two-year moratorium on data centers and a zoning text amendment.
Second reading of an ordinance approving industrial revenue bonds for Justified Datapower LLC.
A presentation on the Liberty Station combined cycle project was given by staff.
Approval to purchase a generator for the county garage.
The court approved road paving on Main Street."""


def test_findings():
    pats = {"L100001025720": [r"liberty station"], "L1": [r"\bnewtown\b"]}
    f = h.findings(TEXT, pats, ["L100001025720", "L1"])
    assert f["named"] == ["L100001025720"] and f["leads"] == ["Justified Datapower"] and f["nearby"] == ["L1"]
    assert len(f["sentences"]) == 3
    assert not any("garage" in s or "paving" in s for s in f["sentences"])
    assert "industrial revenue bond" in f["context"]
    assert h.findings("Road paving and a new generator for the jail.", pats, ["L1"]) == \
        {"named": [], "leads": [], "nearby": [], "context": [], "sentences": []}


def test_kind_of_and_doc():
    assert h.doc(BODY, "https://x.gov/assets/AgendaMinutes/abc.pdf", "Agenda", "2026-10-26")["kind"] == "agenda"
    assert h.doc(BODY, "https://x.gov/files/FCM_9-8-26.pdf", "", "2026-09-08")["kind"] == "minutes"
    assert h.doc(BODY, "https://x.gov/files/Staff_Report.pdf", "Docket 12", "2026-09-08")["kind"] == "packet"


def test_write_outputs(tmp_path):
    plants = [{"id": "L100001025720", "name": "Liberty Station", "county": "Casey"},
              {"id": "L1", "name": "Newtown Generating Station", "county": "Henderson"}]
    rec = {**h.doc(BODY, "https://www.example.gov/a.pdf", "Agenda", "2026-11-03"),
           **h.findings(TEXT, {"L100001025720": [r"liberty station"]}, ["L1"])}
    bodies = [{"id": "test-body", "name": "Test County Fiscal Court", "county": "Henderson", "reader": "pages",
               "state": "3 documents listed since 2024-01-01, 3 read"}]
    h.write_outputs(tmp_path, plants, bodies, [rec], "2024-01-01", "2026-11-04")
    data = json.loads((tmp_path / "local_records.json").read_text())
    assert data["by_plant"] == {"L100001025720": [0], "L1": []}
    assert any(n["county"] == "Casey" and n["plants"] == ["L100001025720"] for n in data["not_posted"])
    md = (tmp_path / "local_records.md").read_text()
    assert "### Liberty Station (L100001025720)" in md and "Justified Datapower" in md
    assert "Casey County Fiscal Court (Casey County)" in md and "GEM plants in the county: Liberty Station" in md


def test_common_names_need_a_plant_word():
    plants = [{"id": "L100000103937", "name_words": {"brown"}}, {"id": "L100000103951", "name_words": {"trimble"}}]
    pats = h.plant_patterns(plants)
    people = "Council Member Chappell introduced the Page for District 15, Colt Brown. Trimble County road paving was approved."
    assert h.findings(people, pats, [])["named"] == []
    plant = "LG&E and KU plan a new combined cycle unit at the E.W. Brown Generating Station near Trimble County Station."
    assert sorted(h.findings(plant, pats, [])["named"]) == ["L100000103937", "L100000103951"]


def test_legistar_file_names_are_unique():
    base = "https://webapi.legistar.com/v1/louisville/Matters/65913/Attachments/"
    a = h.doc_file(Path("/x"), {"url": base + "156372/File", "date": "2026-10-15", "kind": "packet"})
    b = h.doc_file(Path("/x"), {"url": base + "156373/File", "date": "2026-10-15", "kind": "packet"})
    assert a != b and a.name == "2026-10-15_packet_matter65913_attachment156372.pdf"


def test_parse_links_follows_the_base_tag():
    page = ('<base href="https://www.example.gov/" /><a href="Documents/Minutes/2026/October 20, 2026 Minutes.pdf?t=1">'
            'October 20, 2026 Minutes</a>')
    docs = h.parse_links(page, "https://www.example.gov/government/court/minutes.php", BODY, "2024-01-01")
    assert docs[0]["url"] == "https://www.example.gov/Documents/Minutes/2026/October%2020,%202026%20Minutes.pdf?t=1"


def test_franklin_and_simpson_bodies_and_todd_wall():
    ids = {b["id"]: b for b in h.BODIES}
    assert ids["franklin"]["reader"] == "pages" and ids["franklin"]["county"] == "Simpson"
    assert ids["simpson-county"]["reader"] == "wpmedia"
    assert any(n["county"] == "Todd" for n in h.NOT_POSTED)
    import re
    assert re.search(h.LEADS["TenKey LandCo"], "TenKey LandCo LLC rezoning", re.I)

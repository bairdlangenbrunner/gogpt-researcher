"""Offline tests for scopes/us-wi/harvest_local.py: dates from file names, the Legistar, CivicClerk,
AgendaCenter, Municode, Granicus and Brown County readers, the escaped-JSON and showpublisheddocument
link readers, and what a document is searched for. No network."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from paths import load_scope_module  # noqa: E402

h = load_scope_module("us-wi", "harvest_local")
FX = Path(__file__).parent / "fixtures" / "harvest_local_wisconsin"
BODY = {"id": "test-body", "name": "Test Village Board", "county": "Kenosha", "reader": "pages", "site": "https://www.example.gov"}


class FakeNet:
    """Answers net.json(url) and net.page(url) from tables keyed by a substring of the URL."""
    def __init__(self, table, pages=None):
        self.table, self.pages = table, pages or {}

    def json(self, url, params=None):
        for key, val in self.table.items():
            if key in url:
                return val
        return None

    def page(self, url, render=False):
        for key, val in self.pages.items():
            if key in url:
                return val
        return None


def fx(name):
    return json.loads((FX / name).read_text())


def txt(name):
    return (FX / name).read_text()


def test_date_of():
    cases = {"10-20-2026 Notice of Committee": "2026-10-20", "_01132026-452": "2026-01-13",
             "Minutes October 7, 2026": "2026-10-07", "cbagendaoctober28_2026(budget).pdf": "",
             "/i/agendas/d20c/agenda_10-26-2026.pdf": "2026-10-26", "c301a58cf2d8457e92a64bc66b69b715.pdf": ""}
    assert {k: h.date_of(k) for k in cases} == cases


def test_county_names_normalize():
    assert h.norm_wi_county("Racine County") == "Racine" and h.norm_wi_county("FOND DU LAC") == "Fond Du Lac"


def test_legistar_lists_files_and_power_items_only():
    body = {"id": "milwaukee-council", "name": "City of Milwaukee Common Council", "county": "Milwaukee", "client": "milwaukee", "body_id": 1}
    net = FakeNet({"/Events/7001/EventItems": fx("legistar_items_7001.json"), "/Events/7002/EventItems": fx("legistar_items_7002.json"),
                   "/Events": fx("legistar_events.json")})
    docs = h.list_legistar(net, body, "2026-01-01", "2026-11-17")
    assert [(d["date"], d["kind"]) for d in docs] == [("2026-10-20", "agenda"), ("2026-10-20", "packet"), ("2026-09-15", "agenda"), ("2026-09-15", "minutes")]
    assert [d["url"] for d in docs if d["kind"] == "packet"][0].endswith("/Matters/555/Attachments/901/File")


def test_civicclerk_lists_published_files():
    body = {"id": "rock-county", "name": "Rock County", "county": "Rock", "api": "https://rockcowi.api.civicclerk.com/v1"}
    docs = h.list_civicclerk(FakeNet({"/Events": fx("civicclerk_events.json")}), body, "2026-01-01", "2026-11-17")
    assert [(d["date"], d["kind"]) for d in docs] == [("2026-11-09", "agenda"), ("2026-11-09", "packet")]
    assert docs[0]["url"] == "https://rockcowi.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId=493,plainText=false)"


def test_parse_agendacenter():
    docs = h.parse_agendacenter(txt("agendacenter_listing.html"), {**BODY, "site": "https://www.kenoshacountywi.gov"})
    assert [(d["date"], d["kind"]) for d in docs] == [("2026-01-13", "agenda"), ("2026-01-13", "minutes")]
    assert docs[0]["url"] == "https://www.kenoshacountywi.gov/AgendaCenter/ViewFile/Agenda/_01132026-452"


def test_municode_rows_and_paging():
    body = {"id": "sheboygan", "name": "Sheboygan", "county": "Sheboygan", "site": "https://sheboygan-wi.municodemeetings.com",
            "index": "https://sheboygan-wi.municodemeetings.com/meetings3"}
    docs = h.parse_municode(txt("municode_table.html"), body, "2025-01-01", "2026-12-31")
    assert [(d["date"], d["kind"]) for d in docs] == [("2026-11-02", "agenda"), ("2026-11-02", "packet")]
    assert all(d["url"].endswith(".pdf") for d in docs)
    asked = []

    class Paged(FakeNet):
        def page(self, url, render=False):
            asked.append(url)
            return txt("municode_table.html")
    got = h.list_municode(Paged({}), body, "2025-01-01", "2026-12-31")
    assert len(got) == 2 and len(asked) == 1   # the oldest row is 2024, so paging stops after one page


def test_granicus_rows():
    row = ('<tr class="listingRow"><td class="listItem" headers="Name">Village Board</td><td class="listItem" headers="Date">Nov&nbsp;09,&nbsp;2026</td>'
           '<td><a href="//deforestwi.granicus.com/AgendaViewer.php?view_id=1&amp;event_id=77">Agenda</a></td></tr>')
    docs = h.parse_granicus(row.replace("//deforest", "https://deforest"), {"id": "d", "name": "D", "site": "https://deforestwi.granicus.com"})
    assert [(d["date"], d["kind"]) for d in docs] == [("2026-11-09", "agenda")]


def test_brown_county_two_level_read():
    base = "https://www.browncountywi.gov/government/minutes_and_agendas/agendas/county-board-of-supervisors/"
    rows = h.parse_brown_list(txt("brown_list.html"), base, "2025-01-01")
    assert [(d, u.rsplit("=", 1)[-1]) for u, _, d in rows] == [("2026-10-28", "d5852c615806"), ("2026-09-16", "6494984560b4")]
    pdfs = h.parse_brown_detail(txt("brown_detail.html"), rows[0][0])
    assert len(pdfs) == 1 and pdfs[0].startswith("https://www.browncountywi.gov/i/agendas/d20c97471382/")
    body = {"id": "brown-county", "name": "Brown", "county": "Brown", "site": "https://www.browncountywi.gov", "committees": ["county-board-of-supervisors"]}
    net = FakeNet({}, {"/agendas/county-board-of-supervisors/?i=": txt("brown_detail.html"),
                       "/agendas/county-board-of-supervisors/": txt("brown_list.html"), "/minutes/county-board": ""})
    docs = h.list_brown(net, body, "2025-01-01", "2026-11-17")
    assert [(d["date"], d["kind"]) for d in docs] == [("2026-10-28", "agenda")]


def test_escaped_json_page_links():
    body = {**BODY, "unescape": True}
    docs = h.parse_links(txt("wrightstown_escaped.html"), "https://www.wrightstown.us/page/agendas", body, "2025-01-01")
    assert [(d["date"], d["url"]) for d in docs] == [("2026-10-20", "https://aptg.co/pRt_yc"), ("2026-11-09", "https://aptg.co/xYh_zl")]


def test_showpublisheddocument_and_uploads_links():
    docs = h.parse_links(txt("showpublished.html"), "https://www.portwashingtonwi.gov/our-city/", BODY, "2025-01-01")
    assert [(d["date"], d["url"].rsplit("/", 2)[-2]) for d in docs] == [("2026-11-04", "4521"), ("2026-10-07", "uploads")]
    assert h.doc_file(Path("/x"), docs[0]).name == "2026-11-04_agenda_doc4521.pdf"


def test_follow_links_finds_committee_pages():
    text = '<a href="/departments/county-board/all-boards-and-committees/finance/">F</a><a href="/about">A</a><a href="/departments/county-board/all-boards-and-committees/finance/">F</a>'
    got = h.page_links(text, "https://www.racinecounty.gov/departments/county-board/all-boards-and-committees",
                       r"/all-boards-and-committees/[^/]+/?$")
    assert got == ["https://www.racinecounty.gov/departments/county-board/all-boards-and-committees/finance/"]


TEXT = """CALL TO ORDER. Approval of the minutes of the prior meeting.
The board will consider a conditional use permit and tax incremental financing for a data center with 244 backup generators in Mount Pleasant.
Staff reported on the Paris RICE power station and a request from We Energies.
Approval to purchase a generator for the village garage.
The board approved road paving on Main Street."""


def test_findings():
    pats = h.plant_patterns([{"id": "L100001047775"}, {"id": "L100000402374"}])
    f = h.findings(TEXT, pats, ["L100001047775", "L100001047813"])
    assert "L100001047775" in f["named"] and "Microsoft Mount Pleasant" not in f["leads"]
    assert not any("garage" in s or "paving" in s for s in f["sentences"])
    assert "conditional use" in f["context"] and f["nearby"] == ["L100001047813"]


def test_common_names_need_a_plant_word():
    pats = h.plant_patterns([{"id": "L100000402374"}, {"id": "L100000402372"}])
    people = "Paris Town Chair Smith and Concord resident Jones spoke about road paving."
    assert h.findings(people, pats, [])["named"] == []
    plant = "The Paris power station and the Concord power station were discussed."
    assert sorted(h.findings(plant, pats, [])["named"]) == ["L100000402372", "L100000402374"]


def test_write_outputs(tmp_path):
    plants = [{"id": "L100001047775", "name": "Paris RICE power station", "county": "Kenosha"}]
    rec = {**h.doc(BODY, "https://www.example.gov/a.pdf", "Agenda", "2026-11-03"), **h.findings(TEXT, h.plant_patterns(plants), [])}
    bodies = [{"id": "test-body", "name": "Test Village Board", "county": "Kenosha", "reader": "pages", "state": "1 documents listed"}]
    h.write_outputs(tmp_path, plants, bodies, [rec], "2024-01-01", "2026-11-17")
    data = json.loads((tmp_path / "local_records.json").read_text())
    assert data["by_plant"] == {"L100001047775": [0]}
    assert any(n["county"] == "Kenosha" for n in h.NOT_POSTED) or data["not_posted"]
    assert {n["name"] for n in data["not_posted"]} >= {"City of Janesville Council and Plan Commission"}
    md = (tmp_path / "local_records.md").read_text()
    assert "### Paris RICE power station (L100001047775)" in md and "Wisconsin local planning" in md


def test_bodies_and_leads():
    ids = [b["id"] for b in h.BODIES]
    assert len(ids) == len(set(ids)) and {"port-washington", "brown-county", "wrightstown", "sheboygan"} <= set(ids)
    assert all(b["reader"] in h.LISTERS for b in h.BODIES)
    assert re.search(h.LEADS["Meta Beaver Dam"], "Meta data center in Beaver Dam", re.I)
    assert re.search(h.LEADS["Forest Junction and Union Depot"], "Invenergy plans in Brillion", re.I)


def test_load_plants_reads_the_scoped_export():
    plants = h.load_plants()
    assert plants and all(p["id"].startswith("L1") for p in plants)
    assert {p["county"] for p in plants if p["name"].startswith("Forest Junction")} <= {"Calumet"}


# ---- readers added 2026-11-17 (Racine, Brillion, Somers, Paris, Menomonee Falls, Dodge, boards filter) ----

def test_date_of_year_first_month_name():
    assert h.date_of('Download "2025 October 6 Plan Commission Minutes.pdf"') == "2025-10-06"
    assert h.date_of("2026 November 19 Tourism Agenda") == "2026-11-19"


def test_swagit_rows_keep_agenda_links_in_range():
    body = {"id": "falls", "site": "https://menomoneefallswi.new.swagit.com"}
    docs = h.parse_swagit(txt("swagit_table.html"), body, "2024-01-01", "2026-12-31")
    assert [(d["date"], d["url"]) for d in docs] == [
        ("2026-11-02", "https://menomoneefallswi.new.swagit.com/videos/405670/agenda"),
        ("2024-03-04", "https://menomoneefallswi.new.swagit.com/videos/300001/agenda")]
    assert docs[0]["title"].startswith("Committee of the Whole") and docs[0]["kind"] == "agenda"


def test_wpmedia_lists_meeting_pdfs_since_date():
    net = FakeNet({}, {"/wp-json/wp/v2/media": json.dumps(fx("wpmedia_page1.json"))})
    docs = h.list_wpmedia(net, {"id": "somers", "site": "https://www.example.gov"}, "2025-01-01", "2026-11-17")
    assert [d["date"] for d in docs] == ["2026-11-16", "2026-10-21", "2025-04-07"]
    assert all(d["url"].endswith(".pdf") for d in docs)
    assert not any("map" in d["url"] for d in docs)


def test_wpmedia_returns_none_when_the_library_does_not_load():
    assert h.list_wpmedia(FakeNet({}, {}), {"id": "x", "site": "https://www.example.gov"}, "2025-01-01", "2026-11-17") is None


def test_legistar_calendar_rows_make_agenda_and_minutes():
    body = {"id": "racine-council", "name": "City of Racine Common Council", "client": "cityofracine"}
    docs = h.parse_legistar_calendar(txt("legistar_calendar.html"), body, "2024-01-01", "2026-12-31")
    assert [(d["kind"], d["date"]) for d in docs] == [("agenda", "2025-12-16"), ("minutes", "2025-12-16")]
    assert docs[0]["url"] == ("https://cityofracine.legistar.com/View.ashx?M=A&ID=1272297&GUID=787C0A1F-35B3-48D1-9F0A-B2D592267818")


def test_brillion_links_take_the_dated_title_and_skip_old_files():
    body = {"id": "brillion", "name": "City of Brillion"}
    docs = h.parse_links(txt("brillion_minutes.html"), "https://www.brillionwi.gov/minutes", body, "2024-01-01")
    assert [(d["date"], d["url"]) for d in docs] == [("2025-10-06", "https://www.brillionwi.gov/a/uploads/128170")]


def test_page_links_follow_by_query_and_drop_old_year_folders():
    page = txt("brillion_minutes.html")
    got = h.page_links(page, "https://www.brillionwi.gov/minutes", r"(/minutes-[a-z-]+|\?page=\d+)$")
    assert got == ["https://www.brillionwi.gov/minutes-plan-commission", "https://www.brillionwi.gov/minutes-library-board",
                   "https://www.brillionwi.gov/agendas?page=2"]
    folders = h.page_links(txt("racine_folders.html"), "https://www.racinecounty.gov/x/agendas", r"/-folder-\d+$", since_year=2024)
    assert [u[-4:] for u in folders] == ["2952", "2632"]


def test_list_pages_follows_levels():
    body = {"id": "racine-county", "county": "Racine", "pages": ["https://www.racinecounty.gov/index"],
            "follow": [r"/x/agendas$", r"/-folder-\d+$"]}
    net = FakeNet({}, {
        "/index": '<a href="/x/agendas">Agendas</a>',
        "/x/agendas/-folder-2952": '<a href="/files/2026/Agenda 11-04-2026.pdf">Agenda 11-04-2026</a>',
        "/x/agendas": '<a href="/x/agendas/-folder-2952">2026</a><a href="/x/agendas/-folder-2410">2022</a>'})
    docs = h.list_pages(net, body, "2024-01-01", "2026-11-17")
    assert [d["date"] for d in docs] == ["2026-11-04"]


def test_term_book_is_dated_to_its_end_year():
    page = '<a href="https://r.example/images/2024-2025OfficialBoardProceedingsBook.pdf"> </a><a href="https://r.example/images/2022-2023OfficialBoardProceedingsBook.pdf"> </a>'
    docs = h.parse_links(page, "https://co.example.gov/meetings", {"id": "dodge"}, "2024-01-01")
    assert [d["date"] for d in docs] == ["2025-01-01"]


def test_boards_filter_default_on_high_volume_bodies():
    by_id = {b["id"]: b for b in h.BODIES}
    for bid in ("rock-county", "green-bay", "beaver-dam"):
        keep = re.compile("|".join(by_id[bid]["boards"]), re.I)
        assert keep.search("Plan Commission Agenda Packet") and keep.search("City Council Minutes")
        assert not keep.search("Library Board Minutes") and not keep.search("Park and Recreation Commission Agenda")

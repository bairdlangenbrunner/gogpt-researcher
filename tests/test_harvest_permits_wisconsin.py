"""Offline tests for scopes/us-wi/harvest_permits.py on saved sample pages (contact emails redacted)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from paths import load_scope_module  # noqa: E402

h = load_scope_module("us-wi", "harvest_permits")
FX = Path(__file__).parent / "fixtures" / "harvest_wi"


def rd(n):
    return (FX / n).read_text(encoding="utf-8")


def test_search_results():
    rows = h.parse_results(rd("search_sic4911.html"))
    assert len(rows) == 5
    assert rows[1]["fid"] == "113016200" and rows[1]["county"] == "Dane"


def test_facility_and_permits():
    p = h.parse_facility_page(rd("facility_inactive_252304470.html"))
    assert p["fid"] == "252304470" and p["seq"] == "36662" and "Paris RICE" in p["name"]
    assert [x["number"] for x in p["permits"]] == ["24-DMM-064", "25230447A-P01"]
    assert p["permits"][0]["status"] == "Inactive" and p["permits"][0]["notice"] == "2025-03-20"
    assert any(c.startswith("4911") for c in p["sic"])


def test_documents_and_download_id():
    docs = h.parse_documents(rd("permit_252304470_0.html"))
    assert docs and all(not d["doc_id"] for d in docs)
    opened = h.parse_documents(rd("doc_252304470_0_0.html"))
    assert opened[0]["doc_id"] == "1224091"


def test_form_fields_and_hidden():
    page = rd("search_form.html")
    assert isinstance(h.form_fields(page), dict)
    assert all(k.startswith("__") for k in h.hidden_fields(page))


def test_feeds_keep_no_contacts():
    for n, kind in (("public_notice", "public notice"), ("apps_received", "application received"),
                    ("final_permit_decisions", "final decision")):
        rows = h.parse_feed(rd(n + ".html"), kind)
        assert rows and rows[0]["seq"].isdigit()
        assert "@" not in json.dumps(rows)
    notice = h.parse_feed(rd("public_notice.html"), "public notice")[0]
    assert notice["docs"][0]["doc_id"] == "1297621" and notice["comment_ends"] == "2026-11-26"


def test_notice_facility_opens_by_sequence():
    facs = h.notice_facilities(h.parse_feed(rd("public_notice.html"), "public notice"))
    f = next(iter(facs.values()))
    assert f["seq"] and f["docs"][0]["url"].startswith(h.DOWNLOAD)


def test_epa_parsers():
    echo = json.loads(rd("echo_wi.json"))["Results"]["Facilities"]
    assert len(h.echo_facilities(echo)) == 6
    rb = h.rblc_facilities(json.loads(rd("rblc_turbine.json"))["results"])
    assert len(rb) == 4 and rb[0]["facility"]


def test_matching_by_known_fid_and_name():
    plant = {"id": "L100001047775", "name": "Paris RICE", "county": "Kenosha", "name_words": h.words("Paris RICE")}
    f = h.new_fac("fid-252304470", "x", "DNR WARP")
    f["fid"] = "252304470"
    g = h.new_fac("k2", "WE ENERGIES PARIS RICE GENERATING STATION", "DNR WARP")
    h2 = h.new_fac("k3", "ACME CHEESE", "DNR WARP")
    got = h.match(plant, [f, g, h2])
    assert [x[0]["key"] for x in got] == ["fid-252304470", "k2"]


def test_power_filter_and_merge():
    assert h.is_power(h.new_fac("a", "Vantage Data Centers WI-1", "x"))
    assert not h.is_power(h.new_fac("b", "Valley Dairy Cheese Plant", "x"))
    facs = {}
    a = h.new_fac("fid-1", "ABC POWER", "DNR WARP"); a["fid"] = "1"
    b = h.new_fac("seq-9", "ABC POWER", "DNR notice feeds"); b["seq"] = "9"
    h.merge_into(facs, a); h.merge_into(facs, b)
    assert len(facs) == 1 and facs["fid-1"]["seq"] == "9"


def test_dates_and_ranking():
    assert h.iso_date("10/07/2026") == "2026-10-07"
    docs = [{"name": "public_comments_2025-04-10.pdf", "type": "", "date": ""},
            {"name": "preliminary_determination_2025-03-01.pdf", "type": "", "date": ""}]
    assert h.rank_docs(docs)[0]["name"].startswith("preliminary")

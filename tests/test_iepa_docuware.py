"""The Illinois EPA Document Explorer / DocuWare client, on saved snippets (no network)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import iepa_docuware as dw  # noqa: E402

SEARCH_PAGE = """<p>Your search returned 1,234 records.</p>
<table><tr><th>Name</th><th>Address</th><th>City</th><th>State</th><th>Zip</th></tr>
<tr><td><a href="/EPA/DocumentExplorer/Documents/Index/170002668842">CYRUSONE LLC</a></td>
<td>2725 Bilter Rd</td><td>Aurora</td><td>IL</td><td>60502</td></tr>
<tr><td>Not a record row</td><td>x</td></tr>
<tr><td><a href="/EPA/DocumentExplorer/Documents/Index/170002620180">EDGED &amp; CHICAGO LLC</a></td>
<td>2835 Bilter Rd</td><td>Aurora</td><td>IL</td><td>60502</td></tr></table>"""

RECORD_PAGE = """<div id="facilityAddress"><h4>Facility</h4><p>CYRUSONE LLC - 170002668842<br/>
2725 Bilter Rd<br>Aurora, IL 60502</p></div>
<table>
<tr><td>Final Air Permit</td><td>1</td><td>16</td><td>Air</td>
<td><a href="https://docuware7.illinois.gov/DocuWare/PlatformRO/WebClient/Integration?ep=AbCd_-=">open</a></td></tr>
<tr><td>Air Permit Application</td><td>1</td><td>219</td><td>Air</td>
<td><a href="https://docuware7.illinois.gov/DocuWare/PlatformRO/WebClient/Integration?ep=EfGh">open</a></td></tr>
<tr><td>no link here</td></tr>
</table>"""


def test_parse_de_rows_reads_the_count_and_only_linked_rows():
    rows, total = dw.parse_de_rows(SEARCH_PAGE)
    assert total == 1234
    assert [r["iepaid"] for r in rows] == ["170002668842", "170002620180"]
    assert rows[0] == {"name": "CYRUSONE LLC", "address": "2725 Bilter Rd", "city": "Aurora",
                       "state": "IL", "zip": "60502", "iepaid": "170002668842"}
    assert rows[1]["name"] == "EDGED & CHICAGO LLC"


def test_parse_de_record_reads_the_site_and_its_categories():
    rec = dw.parse_de_record(RECORD_PAGE, "170002668842")
    assert rec["name"] == "CYRUSONE LLC"
    assert rec["address"] == "2725 Bilter Rd, Aurora, IL 60502"
    assert rec["city"] == "Aurora"
    assert [c["label"] for c in rec["categories"]] == ["Final Air Permit", "Air Permit Application"]
    assert rec["categories"][0]["pages"] == "16"
    assert rec["categories"][0]["link"].endswith("Integration?ep=AbCd_-=")


def test_record_url_names_the_document():
    assert dw.de_record_url("170002668842") == f"{dw.DE}/Documents/Index/170002668842"
    assert dw.de_record_url("170002668842", "1465329").endswith("/170002668842?dwdocid=1465329")


def test_county_comes_from_the_site_id():
    assert dw.county_of_site_id("043407AEH") == "DuPage"
    assert dw.county_of_site_id("197445ACD") == "Will"
    assert dw.county_of_site_id("031600ABC") == "Cook"
    assert dw.county_of_site_id("") == ""


def test_jhash_is_stable_and_short():
    a, b = dw.jhash("/FileCabinets/x/Documents/1"), dw.jhash("/FileCabinets/x/Documents/2")
    assert a == dw.jhash("/FileCabinets/x/Documents/1")
    assert a != b
    assert str(a).lstrip("-").isdigit()


def test_dw_date_unwraps_the_wire_format():
    assert dw.dw_date("/Date(1733270400000)/") == "2024-12-04"
    assert dw.dw_date("plain") == "plain"
    assert dw.dw_date(None) is None


def test_looks_like_words_tells_ocr_garbage_from_text():
    assert dw.looks_like_words("CONSTRUCTION PERMIT for a NSPS and NESHAP SOURCE. The Permittee CyrusOne "
                               "proposes fifty-six diesel engine generators serving two data center buildings "
                               "on Bilter Road in Aurora, with emission limits stated below for each engine.")
    assert not dw.looks_like_words("ee cS a ee | . , ; : ' ` ~ ^ ^^ ,,, ... || ||| ''' ")


class _Stale:
    def __init__(self, status, text=""):
        self.status_code, self.text = status, text


def test_stale_session_is_recognized_on_401_and_on_the_cryptographic_500():
    assert dw.Client._stale(_Stale(401, "Unauthorized"))
    assert dw.Client._stale(_Stale(500, '{"Message":"Error occurred during a cryptographic operation."}'))
    assert not dw.Client._stale(_Stale(500, "Internal Server Error"))
    assert not dw.Client._stale(_Stale(403, "invalid signature"))
    assert not dw.Client._stale(_Stale(200, ""))


def test_cached_text_elsewhere_reuses_a_harvest_copy(tmp_path):
    scopes = tmp_path / "scopes"
    (scopes / "us-il" / "work" / "permits" / "docs" / "043407AEA").mkdir(parents=True)
    (scopes / "us-il" / "work" / "permits" / "docs" / "043407AEA" / "1442104.txt").write_text("CONSTRUCTION PERMIT Edged Chicago")
    work = tmp_path / "work"
    (work / "iepa_docs" / "170002620180").mkdir(parents=True)
    (work / "iepa_docs" / "170002620180" / "9.txt").write_text("   ")          # blank copies do not count
    assert dw.cached_text_elsewhere("1442104", roots=[scopes, work]) == "CONSTRUCTION PERMIT Edged Chicago"
    assert dw.cached_text_elsewhere("9", roots=[scopes, work]) is None
    assert dw.cached_text_elsewhere("1", roots=[scopes, work]) is None

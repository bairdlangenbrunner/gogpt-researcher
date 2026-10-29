"""Offline tests for scopes/us-nd/harvest_psc.py: saved snippets of the PSC case search, a case page
and a documents folder listing, no network."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from paths import load_scope_module  # noqa: E402
import build_state_brief as b  # noqa: E402

h = load_scope_module("us-nd", "harvest_psc")

RESULTS = """
<h2>2 Cases:</h2>
<!-- <tr><td>commented row</td></tr> -->
<table>
<tr>
  <td class="center">1</td>
  <td>
  	<strong class="nowrap"><a href="pscasedetail?getId=25&getId2=86" title="View case detail &amp; docket entries">PU-25-086</a></strong><br />
  	<small><strong>Bison Generation Station - Williams County        </strong></small>
  </td>
  <td>
  	Siting Application
  	<br /><small><strong>Electric</strong></small>
  </td>
  <td><ul><li>Basin Electric Power Cooperative</li></ul></td>
  <td class="center">68</td>
  <td>2025.03.05</td>
  <td></td>
</tr>
<tr>
  <td class="center">2</td>
  <td>
  	<strong class="nowrap"><a href="pscasedetail?getId=26&getId2=324" title="x">PU-26-324</a></strong><br />
  	<small><strong>Bison to Wheelock 230kV Transmission Project      </strong></small>
  </td>
  <td>Siting Application <br /><small><strong>Electric</strong></small></td>
  <td><ul><li>Basin Electric Power Cooperative</li></ul></td>
  <td class="center">1</td>
  <td>2026.10.29</td>
  <td>2026.10.30</td>
</tr>
</table>
"""

CASE = """
<h1>Case PU-25-086 Detail</h1>
<label>Date Filed:</label>03/05/2025<br />
<label>Date Closed:</label><br />
<label>Description:</label>Bison Generation Station - Williams County        <br />
<label>Type:</label>Siting Application            <br />
<label>Category:</label>Electric<br />
<h2>Entities:</h2>
  	Basin Electric Power Cooperative
 	<br />
	<input type="submit" name="return" value="Return" class="btn" />
<h2>2 Dockets:</h2>
<table class="resulttable">
<tr><th>2<br />Rows</th><th>Docket</th></tr>
<tr>
  <td class="center">1</td>
  <td class="center">1</td>
  <td>
  	<a href="psdocketdetail?getId=25&getId2=86&getId3=1" title="View docket detail">Application for Certificate of Site Compatibility</a>
  	<br /><strong><small>Application</small></strong>
  </td>
  <td class="center">345</td>
  <td>Basin Electric Power Cooperative</td>
  <td>A Person, CEO</td>
  <td>2025.03.05</td>
  <!--
  <td class="center"><span title="Basin Electric Power Cooperative">1720400</span></td>
	-->
</tr>
<tr>
  <td class="center">2</td>
  <td class="center">2</td>
  <td>
  	<a href="psdocketdetail?getId=25&getId2=86&getId3=2" title="View docket detail">Receipt# 12,309  $100,000.00  Application Fee</a>
  	<br /><strong><small>Receipt</small></strong>
  </td>
  <td class="center">1</td>
  <td>Basin Electric Power Cooperative</td>
  <td></td>
  <td>2025.03.10</td>
</tr>
</table>
"""

WEBDOCS = """
<tr><td><a href="/webdocs/case/">Parent Directory</a>       </td><td>&nbsp;</td><td align="right">  - </td></tr>
<tr><td><a href="001-010.pdf">001-010.pdf</a>            </td><td align="right">2025-03-06 10:24  </td><td align="right"> 74K</td></tr>
<tr><td><a href="001-020.pdf">001-020.pdf</a>            </td><td align="right">2025-03-06 10:24  </td><td align="right"> 44M</td></tr>
<tr><td><a href="002-010.pdf">002-010.pdf</a>            </td><td align="right">2025-03-10 14:45  </td><td align="right">1.1M</td></tr>
"""


def plant(pid, name):
    return {"id": pid, "name": name, "city": "", "county": "", "statuses": ["announced"],
            "name_words": h.words(name)}


def test_result_count_and_rows():
    assert h.result_count(RESULTS) == (2, 2)
    assert h.result_count("<h2>100 of 1,006 Cases:</h2>") == (100, 1006)
    rows = h.parse_results(RESULTS)
    assert [r["docket"] for r in rows] == ["PU-25-086", "PU-26-324"]
    r = rows[0]
    assert r["title"] == "Bison Generation Station - Williams County"
    assert (r["type"], r["category"]) == ("Siting Application", "Electric")
    assert r["entities"] == ["Basin Electric Power Cooperative"] and r["doc_count"] == 68
    assert r["filed"] == "2025-03-05" and r["closed"] == "" and rows[1]["closed"] == "2026-10-30"
    assert r["url"] == "https://apps.psc.nd.gov/cases/pscasedetail?getId=25&getId2=86"


def test_classify():
    rows = {r["docket"]: r for r in h.parse_results(RESULTS)}
    assert h.classify(rows["PU-25-086"])[1] is True
    relevant, key, _ = h.classify(rows["PU-26-324"])
    assert not key
    plan = {"docket": "PU-26-999", "title": "2026", "type": "Ten Year Plan", "category": "Electric"}
    assert h.classify(plan)[1] is True
    wind = {"docket": "PU-26-998", "title": "Prairie Winds ND 1 Project - Ward County", "type": "Siting Application",
            "category": "Electric"}
    assert h.classify(wind)[1] is False


def test_parse_case_drops_filer():
    c = h.parse_case(CASE)
    assert c["filed"] == "2025-03-05" and c["closed"] == ""
    assert c["title"] == "Bison Generation Station - Williams County"
    assert c["type"] == "Siting Application" and c["category"] == "Electric"
    assert c["entities"] == ["Basin Electric Power Cooperative"]
    assert [e["n"] for e in c["entries"]] == [1, 2]
    e = c["entries"][0]
    assert e["kind"] == "Application" and e["pages"] == 345 and e["filed"] == "2025-03-05"
    assert "A Person" not in str(c)


def test_webdocs_and_pick_docs():
    files = h.parse_webdocs(WEBDOCS)
    assert [(f["n"], f["attachment"], f["bytes"]) for f in files] == [(1, 10, 74000), (1, 20, 44000000), (2, 10, 1100000)]
    picked = h.pick_docs(h.parse_case(CASE)["entries"], files, 8, 120e6)
    assert [f["file"] for f in picked] == ["001-020.pdf", "001-010.pdf"]
    assert [f["file"] for f in h.pick_docs(h.parse_case(CASE)["entries"], files, 8, 10e6)] == ["001-010.pdf"]
    assert h.webdocs_url("PU-25-086") == "https://www.psc.nd.gov/webdocs/case/25-0086/"
    assert h.size_bytes("1.1M") == 1100000


def test_match_and_outputs_feed_the_brief(tmp_path):
    plants = [plant("L100001047848", "Bison"), plant("L100000401741", "Pioneer"), plant("LX", "Hidden Lake Generating")]
    rows = h.parse_results(RESULTS)
    d = rows[0]
    d.update(key=True, relevant=True, utility="Basin Electric Power Cooperative", documents=[],
             facts={"megawatts": ["The Bison Generation Station will be about 1,500 MW."]}, text_blob="")
    other = {"docket": "PU-26-500", "title": "Hidden Lake Generating Station", "entities": [], "url": "u",
             "key": True, "relevant": True, "utility": "", "documents": [], "facts": {}, "text_blob": ""}
    stray = {"docket": "PU-26-501", "title": "New peaking station", "entities": [], "url": "u",
             "key": True, "relevant": True, "utility": "", "documents": [], "facts": {},
             "text_blob": "Pioneer Generating Station " * 3}
    by_plant, matched = h.match_all(plants, [d, other, stray])
    assert by_plant["L100001047848"] == ["PU-25-086"]
    assert by_plant["LX"] == ["PU-26-500"] and "check" in other["matched"][0]["how"]
    assert by_plant["L100000401741"] == ["PU-26-501"] and "times in the documents" in stray["matched"][0]["how"]
    unmatched = h.write_outputs(tmp_path, plants, [d, other, stray], by_plant, matched,
                                [{"name": "s", "how": "h", "url": "u"}], "2026-10-29", 2022, ["Bison gas 1500 MW"])
    assert unmatched == []
    tasks, data = b.load_harvest(tmp_path)
    assert "L100001047848" in tasks and "1,500 MW" in tasks["L100001047848"][0][1]["task"]
    assert "Bison Generation Station" in (tmp_path / "psc_dockets.md").read_text()

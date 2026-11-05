"""Offline tests for scopes/us-ky/harvest_psc.py: the year list, filings and hearings parsers,
case classification, document choice and plant matching. No network. Names of filers and
public commenters are placeholders."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from paths import load_scope_module  # noqa: E402

h = load_scope_module("us-ky", "harvest_psc")
w = load_scope_module("us-ky", "harvest_permits").words


def year_block(docket, service, filed, category, utility, title):
    return (f"<div class='row' style=\"\">"
            f"<a href='/Case/ViewCaseFilings/{docket}' aria-label='Case Number: {docket}'>{docket}</a>"
            f"<span class=\"control-label\" id='lblLblServType'>Service Type:</span>\n <span>{service}</span> <br />"
            f"<span class=\"control-label\" id='lblLblFilingDt'>Filing Date:</span>\n <span>{filed}</span> <br />"
            f"<span class=\"control-label\" id='lblLblCategory'>Category:</span>\n <span>{category}</span> <br />"
            f"<span class=\"control-label\" id='lblLblUtils'>Utilities:</span>\n <span>{utility}</span> <br />"
            f"<p class=\"form-control-static\">\n <span>{title}</span></p></div>")


YEAR = "<html>" + "".join([
    year_block("2026-00325", "Water", "11/02/2026", "Complaint", "Kentucky-American Water", "A person v. a water company"),
    year_block("2026-00324", "Electric", "10/30/2026", "Certificate", "Kentucky Power Company",
               "Electronic Application of Kentucky Power Company for a Certificate of Public Convenience and Necessity "
               "to Construct a Natural Gas Combined Cycle Generating Facility"),
    year_block("2026-00290", "Electric", "09/15/2026", "Certificate", "Kentucky Utilities Company",
               "Application for a Certificate to Construct a 138 kV Transmission Line in Mason County"),
    year_block("2026-00280", "Electric", "09/01/2026", "Certificate", "A Solar LLC",
               "Application for a Construction Certificate for a 100 MW Solar Generating Facility"),
    year_block("2026-00200", "Electric", "07/01/2026", "Tariff", "East Kentucky Power Cooperative",
               "Electronic Tariff Filing for a new pole attachment rate"),
]) + "</html>"


def test_parse_year_and_classify():
    rows = h.parse_year(YEAR)
    assert [r["docket"] for r in rows] == ["2026-00325", "2026-00324", "2026-00290", "2026-00280", "2026-00200"]
    assert rows[1]["filed"] == "2026-10-30" and rows[1]["utility"] == "Kentucky Power Company"
    assert rows[1]["service"] == "Electric" and "Combined Cycle" in rows[1]["title"]
    got = {r["docket"]: h.classify(r)[:2] for r in rows}
    assert got["2026-00324"] == (True, True)            # on the hand list and about gas generation
    assert got["2026-00290"][1] is False                # a transmission line only
    assert got["2026-00280"] == (True, False)           # solar only
    assert got["2026-00325"] == (False, False) and got["2026-00200"] == (False, False)


def filing(date, desc, docs):
    links = "".join(f"<div><a href='{u}'\n style=\"text-align:left\">\n {n}\n </a>"
                    f"<p id='pDocDesc'>{dd}</p></div>" if dd else
                    f"<div><a href='{u}'\n style=\"text-align:left\">\n {n}\n </a></div>" for n, u, dd in docs)
    return (f"<tr>\n<td id='tdReceivedDt'><span style='font-weight:bold' id='spnRcvdDt'>\n<span>{date}</span>\n</span>"
            f"<p style=\"text-align:left\" id='pFileDesc'>\n {desc}\n</p>"
            f"<p id='pFiler'>A Filer Person</p></td>\n<td style=\"text-align:left\">{links}</td>\n</tr>")


BASE = "https://psc.ky.gov/pscecf/2024-00370/filer%40example.com"
FILINGS = '<tbody id="tblCaseFiles">' + "".join([
    filing("7/3/2025", "Final Order Entered: 1. The application is granted.",
           [("20250703_PSC_ORDER.pdf", "https://psc.ky.gov/pscscf/2024 Cases/2024-00370//20250703_PSC_ORDER.pdf", "")]),
    filing("4/21/2025", "PSC Response E-Mail to A Commenter",
           [("20250421_PSC Response.pdf", "https://psc.ky.gov/pscscf/2024 cases/2024-00370/Public Comments//x.pdf", "")]),
    filing("11/20/2024", "Application and Motion for Confidential Treatment",
           [("Application New Gen - Final to File.pdf", f"{BASE}/11202024010101/Application_New_Gen.pdf", "Application"),
            ("Motion for Confidential Treatment.pdf", f"{BASE}/11202024010101/Motion_CONF.pdf", "Motion for Confidential Treatment"),
            ("BY-4 - Project Feasibility Report.pdf", f"{BASE}/11202024010101/BY-4.pdf", "Exhibit BY-4 report"),
            ("Certificate of Service.pdf", f"{BASE}/11202024010101/Certificate_of_Service.pdf", "Certificate of Service")]),
    filing("11/1/2024", "Notice of Intent", [("NOI.pdf", f"{BASE}/11012024/NOI.pdf", "Notice of Intent")]),
]) + "</tbody>"


def test_parse_filings_drops_filer_and_encodes_urls():
    rows = h.parse_filings(FILINGS)
    assert [r["date"] for r in rows] == ["2025-07-03", "2025-04-21", "2024-11-20", "2024-11-01"]
    assert rows[0]["description"].startswith("Final Order Entered")
    assert "Filer" not in str(rows) and all("filer" not in k for r in rows for k in r)
    assert rows[0]["documents"][0]["url"] == "https://psc.ky.gov/pscscf/2024%20Cases/2024-00370//20250703_PSC_ORDER.pdf"
    assert [d["name"] for d in rows[2]["documents"]][0] == "Application New Gen - Final to File.pdf"
    assert rows[2]["documents"][1]["description"] == "Motion for Confidential Treatment"


def test_pick_docs_puts_the_order_and_application_first():
    docs = h.all_docs(h.parse_filings(FILINGS), "main")
    docs += [{"name": f"Quarterly Report {i}.pdf", "url": f"https://psc.ky.gov/post/q{i}.pdf", "description": "",
              "date": f"2026-0{i}-01", "filing": "Quarterly construction progress report", "tab": "post", "row": 0}
             for i in range(1, 6)]
    names = [d["name"] for d in h.pick_docs(docs, cap=10)]
    assert set(names[:2]) == {"20250703_PSC_ORDER.pdf", "Application New Gen - Final to File.pdf"}
    assert "Motion for Confidential Treatment.pdf" not in names and "Certificate of Service.pdf" not in names
    assert "NOI.pdf" not in names
    assert sum(n.startswith("Quarterly") for n in names) == 3
    assert "BY-4 - Project Feasibility Report.pdf" in names


HEARINGS = ("<a id='lnkVid' href='https://www.youtube.com/watch?v=abc' target='_blank'>Evidentiary Hearing (Mar 4, 2025)</a>"
            "<a id='lnkVid' href='https://www.youtube.com/watch?v=def'>Public Comment Hearing</a>")


def test_parse_hearings():
    got = h.parse_hearings(HEARINGS)
    assert got[0] == {"date": "2025-03-04", "title": "Evidentiary Hearing (Mar 4, 2025)",
                      "url": "https://www.youtube.com/watch?v=abc"}
    assert got[1]["date"] == ""


def plant(pid, name):
    return {"id": pid, "name": name, "city": "", "county": "", "statuses": [], "name_words": w(name)}


def test_match_docket():
    cooper, brown, newtown = (plant("L100000103935", "Cooper power station"), plant("L100000103937", "Brown power station"),
                              plant("L999", "Newtown Generating Station"))
    case = {"docket": "2024-00370", "title": "Application of EKPC for a new combined cycle at Cooper Station",
            "orders": [], "text_blob": "Brown station " * 9}
    assert h.match_docket(cooper, case) == "on the hand-checked case list"
    assert h.match_docket(brown, case) is None           # document mentions never add a plant to a hand-listed case
    free = {"docket": "2026-09999", "title": "Application for a gas plant", "orders": [], "text_blob": "Brown station " * 6}
    assert h.match_docket(brown, free).startswith("named 6 times")
    assert h.match_docket(brown, free, others_by_title=True) is None
    named = {"docket": "2026-09998", "title": "Newtown generating facility certificate", "orders": [], "text_blob": ""}
    assert h.match_docket(newtown, named).startswith("name words in the case title")
    by_plant, matched = h.match_all([cooper, brown, newtown], [case, free, named])
    assert by_plant == {"L100000103935": ["2024-00370"], "L100000103937": ["2026-09999"], "L999": ["2026-09998"]}
    assert matched == {"2024-00370", "2026-09999", "2026-09998"}

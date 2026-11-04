"""Offline tests for scopes/us-ok/harvest_permits.py: the ODEQ table parser, OnBase result
parsing, permit number bases and plant matching. No network."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from paths import load_scope_module  # noqa: E402

h = load_scope_module("us-ok", "harvest_permits")


def row(div, county, company, oid, facility, permit, tier, ptype, step, status):
    pad = " " * 20
    return (f"<tr><td>{div}{pad}</td>\n<td>{county}{pad}</td>\n<td>{company}{pad}</td>\n"
            f"<td><a href='/PermitsPublicReview/permitinformation.aspx?id={oid}'>{facility}{pad}</a></td>\n"
            f"<td>{permit}{pad}</td>\n<td>{tier}{pad}</td>\n<td>{ptype}{pad}</td>\n<td>{step}{pad}</td>\n"
            f"<td>Staff Person{pad}</td>\n<td>{status}{pad}</td>\n"
            f"<td><a href='/PermitsPublicReview/permitinformation.aspx?id={oid}'>Additional Documents</a>\n</td></tr>")


TABLE = "<table><tr><th>Division</th><th>County</th></tr>" + "\n".join([
    row("AQD", "Oklahoma", "OG AND E", "1073118", "Tinker Turbines", "2025-0595-C M-1", "Tier II",
        "Major Source Construction Permit", "Technical Review", "Under DEQ Review"),
    row("AQD", "Oklahoma", "Oklahoma Gas and Electric", "1073124", "Horseshoe Lake Generating Station",
        "2024-0324-ARR5 M-2", "Tier II", "Title V Operating Permit",
        'Public Review<br /><span style="font-size:12px;">(04/25/2026 - 07/24/2026)</span>', "Public Comment"),
    row("WQD", "Oklahoma", "OG&amp;E", "1077153", "OG&amp;E Horseshoe Lake", "OK0000442", "Tier II",
        "Major Discharge Permit (Renewal)", "Application Filed", "Under DEQ Review"),
    row("AQD", "Kingfisher", "Mustang Gas Products, LLC", "1073115", "Kingfisher East Compressor Station",
        "2026-0131-TVR5", "Tier II", "Title V Operating Permit", "Technical Review", "Under DEQ Review"),
    row("AQD", "Rogers", "Public Service Company of Oklahoma", "1153508", "Port of Inola Power Station",
        "PSD000139 v1.0", "Tier III", "Minor Source Construction Permit", "Administrative Review", "Under DEQ Review"),
    row("AQD", "Mayes", "Myall LLC", "1073054", "PRY Data Storage Facility", "2021-0235-TVR M-1", "Tier II",
        "Title V Operating Permit", "Technical Review", "Under DEQ Review"),
    row("AQD", "Rogers", "Public Service Company of Oklahoma", "1062053", "PSO Northeastern Power Station",
        "2019-0607-C M-2", "Tier II", "Major Source Construction Permit", "Technical Review", "Under DEQ Review"),
    row("AQD", "Rogers", "Public Service Company of Oklahoma", "1062056", "PSO Northeastern Power Station",
        "TV0000530 v6.0", "Tier II", "Title V Operating Permit", "Technical Review", "Under DEQ Review"),
]) + "</table>"


def plant(pid, name, county=""):
    return {"id": pid, "name": name, "city": "", "county": county, "statuses": ["operating"],
            "name_words": h.words(name)}


def test_parse_ppr_rows_and_dates():
    rows = h.parse_ppr(TABLE)
    assert len(rows) == 8
    r = rows[1]
    assert r["division"] == "AQD" and r["county"] == "Oklahoma"
    assert r["facility"] == "Horseshoe Lake Generating Station" and r["object_id"] == "1073124"
    assert r["permit"] == "2024-0324-ARR5 M-2"
    assert r["step"] == "Public Review"
    assert (r["comment_begins"], r["comment_ends"]) == ("2026-04-25", "2026-07-24")
    assert "Staff Person" not in str(rows)
    assert rows[2]["company"] == "OG&E"


def test_permit_base():
    assert h.permit_base("2019-0607-C M-2") == "2019-0607"
    assert h.permit_base("TV0000530 v6.0") == "TV0000530"
    assert h.permit_base("MAC000281 v1.2") == "MAC000281"
    assert h.permit_base("OK0045250") == "OK0045250"
    assert h.permit_base("pending") == ""


def test_build_facilities_groups_rows():
    facs = h.build_facilities(h.parse_ppr(TABLE))
    ne = [f for f in facs.values() if "Northeastern" in f["name"]]
    assert len(ne) == 1
    assert ne[0]["object_ids"] == ["1062053", "1062056"]
    assert ne[0]["permit_bases"] == ["2019-0607", "TV0000530"]


def test_match_known_patterns():
    facs = list(h.build_facilities(h.parse_ppr(TABLE)).values())
    hl = h.match(plant("L100000402162", "Horseshoe Lake", "Oklahoma"), facs)
    assert {f["name"] for f, _ in hl} == {"Horseshoe Lake Generating Station", "OG&E Horseshoe Lake"}
    assert all(how == "checked by hand" for _, how in hl)
    assert [f["name"] for f, _ in h.match(plant("L100000402164", "Mustang", "Canadian"), facs)] == []
    assert [f["name"] for f, _ in h.match(plant("L100001063385", "Tinker Air Force Base"), facs)] == ["Tinker Turbines"]
    assert [f["name"] for f, _ in h.match(plant("L100001089319", "Port of Inola", "Rogers"), facs)] == ["Port of Inola Power Station"]
    assert [f["name"] for f, _ in h.match(plant("L100000104126", "Northeastern Station"), facs)] == ["PSO Northeastern Power Station"]


def test_match_by_name_words_when_not_known():
    facs = list(h.build_facilities(h.parse_ppr(TABLE)).values())
    got = h.match(plant("L999", "Kingfisher East"), facs)
    assert [f["name"] for f, _ in got] == ["Kingfisher East Compressor Station"]
    assert "check" in got[0][1]


def test_is_power():
    facs = {f["name"]: f for f in h.build_facilities(h.parse_ppr(TABLE)).values()}
    assert h.is_power(facs["PRY Data Storage Facility"])
    assert h.is_power(facs["Port of Inola Power Station"])
    assert not h.is_power(facs["Kingfisher East Compressor Station"])


def test_parse_doc():
    d = h.parse_doc({"ID": "abc/def+==", "Name": "6293248 - DEQ Permits Public Application - 5/1/2026",
                     "DisplayColumnValues": [{"Value": "Application"}, {"Value": "5/1/2026"}]})
    assert d["number"] == "6293248" and d["type"] == "Application" and d["date"] == "2026-05-01"
    assert d["url"].endswith("/Document/abc%2Fdef%2B%3D%3D/?ViewerMode=PDF&ForceDownload=true")
    assert d["key"] == "6293248|Application|2026-05-01"
    d2 = h.parse_doc({"ID": "x", "Name": "123456 - Draft Permit 2025-0595-C - 1/2/2026", "DisplayColumnValues": []})
    assert d2["date"] == "2026-01-02" and d2["name_permits"] == ["2025-0595-C"]


def test_add_docs_dedups_by_key():
    f = h.new_fac("k", "x", "table")
    d = h.parse_doc({"ID": "1", "Name": "111111 - Memo - 1/1/2025", "DisplayColumnValues": [{"Value": "Memo"}, {"Value": "1/1/2025"}]})
    h.add_docs(f, [d], "object id 1")
    h.add_docs(f, [{**d, "url": "other"}], "permit 2019-0607")
    assert len(f["docs"]) == 1 and f["found_by"] == ["object id 1", "permit 2019-0607"]


def test_doc_facts_oklahoma():
    text = ("Permit No. 2025-0595-C\nThe applicant proposes to construct two simple cycle turbines.\n"
            "Two GE LM6000 combustion turbines rated 50 MW each.\n"
            "The facility is located at 3001 Tinker Road, Oklahoma County, Oklahoma.\n"
            "Coordinates 35.4147, -97.3866\n")
    f = h.doc_facts(text)
    assert "2025-0595-C" in f["ids"]
    assert any("LM6000" in x for x in f["makers"])
    assert any("50 MW" in x for x in f["sizes"])
    assert f["coords"] == ["35.4147, -97.3866"]
    assert f["location"]


def test_rank_docs_newest_application_first():
    docs = [{"type": "Letter", "date": "2026-05-01"}, {"type": "Application", "date": "2025-01-01"},
            {"type": "Draft Permit", "date": "2026-02-01"}]
    assert [d["type"] for d in h.rank_docs(docs)] == ["Draft Permit", "Application", "Letter"]


def test_slim_keeps_contract_fields():
    facs = h.build_facilities(h.parse_ppr(TABLE))
    s = h.slim(next(iter(facs.values())))
    for k in ("name", "codes", "permits", "docs", "address", "city"):
        assert k in s
    assert s["permits"][0]["number"] == "2025-0595-C M-1"

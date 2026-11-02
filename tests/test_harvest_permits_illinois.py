"""Matching and parsing of the Illinois air permit harvester, on saved snippets (no network)."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from paths import load_scope_module  # noqa: E402

h = load_scope_module("us-il", "harvest_permits")

DOC = """CONSTRUCTION PERMIT - NSPS SOURCE. PERMITTEE: CyrusOne LLC. Application No.: 24080019
I.D. No.: 043407AEH. Source Location: 2725 Bilter Road, Aurora, DuPage County, Illinois 60502.
The Permittee proposes to install fifty-six Caterpillar model 3516 emergency diesel engine generators,
each rated at 2,250 kW, and one generator rated at 1,250 kW, fired on ultra low sulfur diesel.
The site is at 41.7812, -88.2653."""


def fac(ai, name, city="", names=None):
    return {"ai": ai, "name": name, "names": names or [name], "city": city, "county": h.county_of_site_id(ai),
            "docs": [], "permits": [], "iepaids": [], "by": set()}


def plant(pid, name, city, owner=""):
    return {"id": pid, "name": name, "city": city, "name_words": h.words(name), "owner_words": h.owner_words(owner)}


def test_words_and_owner_words_drop_the_noise():
    assert h.words("Nelson Energy Center") == {"nelson"}
    assert h.words("Southeast Chicago Energy Project (SCEP)") == {"southeast", "chicago", "project"}
    assert h.owner_words("Invenergy Nelson LLC [100%]") == {"invenergy", "nelson"}
    assert h.owner_words("Dynegy Lee II LLC [100%]; Vistra Corp [parent]") == {"dynegy", "vistra"}


def test_power_filter():
    assert h.is_power(fac("043407AEH", "CYRUSONE LLC"))
    assert h.is_power(fac("103814AAC", "INVENERGY NELSON LLC"))
    assert h.is_power(fac("031600AAA", "PROJECT MITTEN DATA CENTER"))
    assert not h.is_power(fac("103800AAA", "ROCK FALLS GRAIN COOP"))
    assert not h.is_power(fac("103800AAB", "NELSON ELEMENTARY SCHOOL"))
    assert not h.is_power(fac("043407AAA", "1520 AURORA AVE"))
    assert not h.is_power(fac("043407AAB", "ACME PRINTING"))


def test_match_by_name_owner_and_city():
    p = plant("L1", "Nelson Energy Center", "Rock Falls", "Invenergy Nelson LLC [100%]")
    site = fac("103814AAC", "INVENERGY NELSON LLC", "ROCK FALLS")
    school = fac("103814AAD", "NELSON ELEMENTARY SCHOOL", "ROCK FALLS")
    street = fac("103814AAE", "1520 NELSON RD", "ROCK FALLS")
    peaker = fac("103814AAF", "ROCK FALLS PEAKING LLC", "ROCK FALLS")
    elsewhere = fac("201030AAA", "ROCKFORD PEAKING LLC", "ROCKFORD")
    got = h.match(p, {f["ai"]: f for f in (site, school, street, peaker, elsewhere)})
    assert got == [(site, "name match, check it is this plant"),
                   (peaker, "same city, power-like name, check it is this plant")]


def test_three_word_names_match_without_a_power_word_and_tolerate_one_miss():
    p = plant("L2", "Southeast Chicago Energy Project", "Calumet")   # the city's own words never count
    full = fac("031600AAA", "SOUTHEAST CHICAGO ENERGY PROJECT LLC", "CALUMET")
    most = fac("031600AAB", "SOUTHEAST CHICAGO POWER", "CALUMET")
    plain = fac("031600AAC", "SOUTHEAST CHICAGO MILL", "CALUMET")
    hows = {f["ai"]: how for f, how in h.match(p, {f["ai"]: f for f in (full, most, plain)})}
    assert hows["031600AAA"] == "name match, check it is this plant"
    assert hows["031600AAB"] == "most name words match a power-like site, check it is this plant"
    assert "031600AAC" not in hows


def test_owner_word_matches_a_power_site_in_the_same_city():
    p = plant("L3", "Lee energy facility", "Dixon", "Dynegy Lee II LLC [100%]")
    site = fac("103817AAH", "DYNEGY LEE II LLC", "DIXON")
    far = fac("103817AAI", "DYNEGY MIDWEST GENERATION", "BALDWIN")
    assert h.match(p, {site["ai"]: site, far["ai"]: far}) == [
        (site, "owner's name on a power-like site in the same city, check it is this plant")]


def test_known_site_ids_win_and_are_well_formed():
    h.KNOWN["L9"] = ["000000AAA"]
    try:
        p = plant("L9", "Example Peaker", "Nowhere")
        known = fac("000000AAA", "SOME HOLDING COMPANY", "ELSEWHERE")
        other = fac("000000AAB", "EXAMPLE PEAKER LLC", "NOWHERE")
        assert h.match(p, {known["ai"]: known, other["ai"]: other}) == [
            (known, "checked by hand"), (other, "name match, check it is this plant")]
    finally:
        del h.KNOWN["L9"]
    for pid, sids in h.KNOWN.items():
        assert pid.startswith("L1000") and sids
        assert all(re.fullmatch(r"\d{6}[A-Z]{3}", s) for s in sids), pid


def test_build_facilities_groups_documents_by_site():
    rows = [
        {"BUREAUID": "043407AEH", "SITENAME": "CYRUSONE  LLC", "IEPAID": "170002668842", "DWDOCID": 1465329,
         "CATEGORY": "03K", "ITEMDATE": "2024-12-04", "PERMITID": "24080019", "PERMITLOG": "", "COMMENTTEXT": "",
         "DWPAGECOUNT": 16, "_by": '[BUREAUID]="043407AEH"'},
        {"BUREAUID": "043407AEH", "SITENAME": "CYRUSONE LLC - CHI9", "IEPAID": "170002668842", "DWDOCID": 1465757,
         "CATEGORY": "03M", "ITEMDATE": "2024-08-22", "PERMITID": "24080019", "PERMITLOG": None, "COMMENTTEXT": None,
         "DWPAGECOUNT": 219},
        {"BUREAUID": "043407AEH", "SITENAME": "CYRUSONE LLC", "IEPAID": "170002668842", "DWDOCID": 1465329,
         "CATEGORY": "03K", "ITEMDATE": "2024-12-04", "PERMITID": "24080019", "DWPAGECOUNT": None},
        {"BUREAUID": "", "SITENAME": "NO SITE", "DWDOCID": 1},
        {"BUREAUID": "197110AEM", "SITENAME": "AMAZON HMW1", "IEPAID": "170002421500", "DWDOCID": 1365617,
         "CATEGORY": "03K", "ITEMDATE": "2021-06-01", "PERMITID": "21040002", "DWPAGECOUNT": 20},
    ]
    facs = h.build_facilities(rows)
    assert set(facs) == {"043407AEH", "197110AEM"}
    f = facs["043407AEH"]
    assert f["name"] == "CYRUSONE LLC" and f["names"] == ["CYRUSONE LLC", "CYRUSONE LLC - CHI9"]
    assert f["county"] == "DuPage" and f["iepaids"] == ["170002668842"]
    assert [d["id"] for d in f["docs"]] == ["1465329", "1465757"]
    assert f["docs"][0]["pages"] == 16 and f["permits"] == ["24080019"]
    assert facs["197110AEM"]["county"] == "Will"


def test_doc_facts():
    f = h.doc_facts(DOC)
    assert f["ids"] == ["043407AEH", "24080019"]
    assert f["fuel"] == ["diesel"]
    assert f["coords"] == ["41.7812, -88.2653"]
    assert any("2,250 kW" in s for s in f["sizes"])
    assert f["makers"] and f["equipment"] and f["project"]
    assert any("Bilter Road" in s for s in f["location"])

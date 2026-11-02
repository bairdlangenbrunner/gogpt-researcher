"""Guardrails added after the Illinois and Kansas audits: the statewide source
list (gate `statewide-coverage`), the chase gate, lead-only sources, and the
EIA plants missing from GEM (brief task + gate `ids_followup`)."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from build_state_brief import eia_lead_tasks, render_scope_brief  # noqa: E402
from state_gate import (chase_hits, gate_chase, gate_ids_followup, gate_lead_only,  # noqa: E402
                        gate_permit_system, gate_source_coverage)

WHERE = {"kind": "state", "name": "Mississippi", "slug": "mississippi",
         "country": "United States", "postal": "ms"}
WANTED = [{"id": "a", "name": "Source A", "url": "https://example.gov/a", "what": "x"},
          {"id": "b", "name": "Source B", "url": "https://example.gov/b", "what": "y"}]


def batch_dir(tmp_path, coverage=None, name="us-ms"):
    b = tmp_path / "batches" / name
    b.mkdir(parents=True)
    if coverage is not None:
        (b / "coverage.json").write_text(json.dumps(coverage), encoding="utf-8")
    return b


def cov_dir(tmp_path, wanted=WANTED, name="us-ms"):
    d = tmp_path / "coverage"
    d.mkdir()
    if wanted is not None:
        (d / f"{name}.json").write_text(json.dumps(wanted), encoding="utf-8")
    return d


def good(**kw):
    e = {"status": "searched", "how": "read the notices page", "found": "nothing new"}
    e.update(kw)
    return e


# ---------------------------------------------------------- source coverage ---

def test_coverage_passes_when_every_source_recorded(tmp_path):
    b = batch_dir(tmp_path, {"sources": {"a": good(), "b": good()}})
    out, _ = gate_source_coverage(b, {"where": WHERE}, cov_dir(tmp_path))
    assert out == []


def test_coverage_fails_on_missing_id(tmp_path):
    b = batch_dir(tmp_path, {"sources": {"a": good()}})
    out, _ = gate_source_coverage(b, {"where": WHERE}, cov_dir(tmp_path))
    assert [o[0] for o in out] == ["b"]


def test_coverage_fails_on_not_searched_and_skipped(tmp_path):
    b = batch_dir(tmp_path, {"sources": {"a": {"status": "not searched"},
                                         "b": {"status": "skipped"}}})
    out, _ = gate_source_coverage(b, {"where": WHERE}, cov_dir(tmp_path))
    assert {o[0] for o in out} == {"a", "b"}


def test_coverage_blocked_needs_access_record(tmp_path):
    bad = {"status": "blocked", "access": "the portal is a search form"}
    ok = {"status": "blocked", "access": "fetch.py returned 403 on every route; the Wayback lookup "
                                         "found no snapshot of this address"}
    b = batch_dir(tmp_path, {"sources": {"a": bad, "b": ok}})
    out, _ = gate_source_coverage(b, {"where": WHERE}, cov_dir(tmp_path))
    assert [o[0] for o in out] == ["a"]


def test_coverage_excuse_in_access_note_fails(tmp_path):
    e = {"status": "blocked", "access": "fetch.py failed and Wayback has nothing; it is a search "
                                        "form that needs a script"}
    b = batch_dir(tmp_path, {"sources": {"a": e, "b": good()}})
    out, _ = gate_source_coverage(b, {"where": WHERE}, cov_dir(tmp_path))
    assert [o[0] for o in out] == ["a"]


def test_coverage_searched_needs_how_and_found(tmp_path):
    b = batch_dir(tmp_path, {"sources": {"a": good(how=""), "b": good(found="")}})
    out, _ = gate_source_coverage(b, {"where": WHERE}, cov_dir(tmp_path))
    assert {o[0] for o in out} == {"a", "b"}


def test_coverage_no_list_or_no_file_is_one_finding(tmp_path):
    b = batch_dir(tmp_path)
    out, _ = gate_source_coverage(b, {"where": WHERE}, cov_dir(tmp_path, wanted=None))
    assert len(out) == 1 and "source list" in out[0][1]
    (tmp_path / "coverage" / "us-ms.json").write_text(json.dumps(WANTED), encoding="utf-8")
    out, _ = gate_source_coverage(b, {"where": WHERE}, tmp_path / "coverage")
    assert len(out) == 1 and "coverage.json" in out[0][0]


def test_coverage_accepts_list_form(tmp_path):
    b = batch_dir(tmp_path, [dict(good(), id="a"), dict(good(), id="b")])
    out, _ = gate_source_coverage(b, {"where": WHERE}, cov_dir(tmp_path))
    assert out == []


def test_coverage_checks_a_country_too(tmp_path):
    country = {"kind": "country", "name": "Poland", "slug": "poland", "country": "Poland"}
    b = batch_dir(tmp_path, {"sources": {"a": good()}}, name="poland")
    out, _ = gate_source_coverage(b, {"where": country}, cov_dir(tmp_path, name="poland"))
    assert [o[0] for o in out] == ["b"]


# ---------------------------------------------------------- permit system ---

NOTICES = {"id": "notices", "role": "permit_notices", "name": "Air permit public notices",
           "url": "https://example.gov/notices", "what": "Read every notice."}
RECORD = {"id": "records", "role": "permit_record", "name": "Air permit record system",
          "url": "https://example.gov/records",
          "what": "Use the index from scopes/us-ms/harvest_permits.py and read every permit."}


def _sub(tmp_path, name):
    d = tmp_path / name
    d.mkdir()
    return d


def test_permit_system_passes_with_harvester_or_by_name(tmp_path):
    b = batch_dir(tmp_path, {"sources": {}})
    out, info = gate_permit_system(b, cov_dir(tmp_path, wanted=[NOTICES, RECORD]))
    assert out == []
    assert info and "records" in info[0] and "notices" in info[0]
    by_name = dict(RECORD, what="Search the facility list by name for every GEM plant and every lead.")
    out, _ = gate_permit_system(b, cov_dir(_sub(tmp_path, "x"), wanted=[by_name]))
    assert out == []


def test_permit_system_fails_on_notices_only(tmp_path):
    b = batch_dir(tmp_path, {"sources": {}})
    out, _ = gate_permit_system(b, cov_dir(tmp_path, wanted=[NOTICES]))
    assert len(out) == 1 and "notice feed" in out[0][1] and "notices" in out[0][1]


def test_permit_system_fails_without_any_role(tmp_path):
    b = batch_dir(tmp_path, {"sources": {}})
    out, _ = gate_permit_system(b, cov_dir(tmp_path))
    assert len(out) == 1 and "permit_record" in out[0][1]


def test_permit_system_checks_what_url_and_gap(tmp_path):
    b = batch_dir(tmp_path, {"sources": {}})
    bad = dict(RECORD, what="Read the permits.", url="", gap="login needed")
    out, _ = gate_permit_system(b, cov_dir(tmp_path, wanted=[bad]))
    msgs = " | ".join(o[1] for o in out)
    assert [o[0] for o in out] == ["records"] * 3
    assert "no url" in msgs and "harvester" in msgs and "`gap`" in msgs
    ok = dict(RECORD, gap="Permit PDFs need a login; the public notice feed and a records request cover them.")
    out, _ = gate_permit_system(b, cov_dir(_sub(tmp_path, "y"), wanted=[ok]))
    assert out == []


def test_permit_system_missing_list_is_one_finding(tmp_path):
    b = batch_dir(tmp_path, {"sources": {}})
    out, _ = gate_permit_system(b, cov_dir(tmp_path, wanted=None))
    assert len(out) == 1 and "no scope source list" in out[0][1]


def test_permit_system_runs_on_narrow_batches(tmp_path):
    b = batch_dir(tmp_path, {"sources": {}}, name="us-ms-dc")
    out, _ = gate_permit_system(b, cov_dir(tmp_path, wanted=[NOTICES], name="us-ms"))
    assert len(out) == 1


def test_scope_lists_name_a_permit_record_system():
    for tag in ("us-il", "us-mi", "us-nd", "us-ms", "us-ks"):
        data = json.loads((ROOT / "scopes" / tag / "coverage.json").read_text(encoding="utf-8"))
        roles = [d.get("role") for d in data]
        assert "permit_record" in roles, tag
        assert "permit_notices" in roles, tag


def test_ms_source_list_is_well_formed():
    data = json.loads((ROOT / "scopes" / "us-ms" / "coverage.json").read_text(encoding="utf-8"))
    ids = [d["id"] for d in data]
    assert len(ids) == len(set(ids)) >= 10
    for d in data:
        assert set(d) >= {"id", "name", "url", "what"}
        assert d["url"].startswith("https://")
        assert "gem.wiki" not in d["url"] and "globalenergymonitor.org" not in d["url"]


# -------------------------------------------------------------- chase gate ---

KANSAS_NOTES = [
    "Noticed in passing that the owner may have changed. I did not research it.",
    "The unit looks retired, but that was not a task for this pass.",
    "Capacity may be wrong. This is outside the tasks I was given.",
    "I did not verify the start year.",
    "Worth a second look by a reviewer.",
    "Left unchanged.",
    "The owner question is not part of this task.",
    "I did not confirm the county.",
    "Other fields were not checked.",
    "This needs further research.",
]

LEGIT_NOTES = [
    "The state air permit lists 2 turbines of 45 MW each, so capacity stays at 90 MW.",
    "Searched the Kansas Department of Health and Environment notices and found no permit for this site.",
    "The utility's 2025 plan says the unit retires in 2031. No later date was found.",
    "The press release from March 2026 gives the commercial operation date.",
    "No change to the status. The January 2026 report still lists it as operating.",
    "A second source, a trade article from May 2026, agrees with the filing.",
    "The plant was checked against the EIA-860M table for July 2026 and matches.",
    "The permit was issued in a later year than first planned, in 2027.",
]


def test_chase_catches_every_kansas_note():
    for n in KANSAS_NOTES:
        assert chase_hits(n), n


def test_chase_leaves_legitimate_notes_alone():
    for n in LEGIT_NOTES:
        assert not chase_hits(n), n


def test_chase_ignores_urls():
    assert not chase_hits("See https://example.gov/in-passing/second look.pdf for the permit.")


def test_gate_chase_reports_record_and_key():
    lanes = {"qa": [{"record_id": "R1", "researcher_notes": KANSAS_NOTES[0]},
                    {"record_id": "R2", "researcher_notes": LEGIT_NOTES[0]}]}
    out = gate_chase(lanes)
    assert [o[0] for o in out] == ["R1"] and "researcher_notes" in out[0][1]


def test_gate_chase_checks_coverage_entries():
    out = gate_chase({}, {"a": {"how": "read it", "found": "not researched yet"}})
    assert out and out[0][0] == "coverage.json:a"


# ---------------------------------------------------------- lead-only gate ---

def test_lead_only_flags_value_lane_refs():
    lanes = {"updates": [{"record_id": "R1", "refs": ["https://cleanview.co/projects/x"]},
                         {"record_id": "R2", "refs": ["https://www.interconnection.fyi/x",
                                                      "https://www.misoenergy.org/q.xlsx"]},
                         {"record_id": "R3", "refs": ["https://www.psc.ms.gov/d"]}]}
    out = gate_lead_only(lanes)
    assert [o[0] for o in out] == ["R1", "R2"]


def test_lead_only_allows_watch_list():
    lanes = {"monitor": [{"record_id": "M1", "refs": ["https://cleanview.co/projects/x"]}]}
    assert gate_lead_only(lanes) == []


def test_lead_site_never_promotes_to_green():
    from build_review_package import validated_tier
    v = [{"url": "https://en.wikipedia.org/wiki/X", "ok": True, "name_found": True,
          "contains_value": True}]
    assert validated_tier("Capacity (MW)", "change", "medium",
                          ["https://en.wikipedia.org/wiki/X"], v) == "medium"
    v[0]["url"] = "https://www.psc.ms.gov/d"
    assert validated_tier("Capacity (MW)", "change", "medium", ["https://www.psc.ms.gov/d"], v) == "high"


# ------------------------------------------------------------ ids_followup ---

LEADS = [{"eia_id": "54044", "name": "University of Illinois Cogen Facility",
          "capacity_mw": 59.9, "status": "operating"},
         {"eia_id": "7760", "name": "Tilton", "capacity_mw": 188, "status": "operating"}]


def test_ids_followup_fails_unanswered(tmp_path):
    b = batch_dir(tmp_path, name="us-il")
    out, _ = gate_ids_followup({"where": WHERE, "mode": "update", "ids_followup": LEADS}, {}, b)
    assert [o[0] for o in out] == ["EIA:54044", "EIA:7760"]


def test_ids_followup_passes_with_staged_record_or_decision(tmp_path):
    cov = {"sources": {}, "ids_followup": {
        "7760": {"decision": "below_threshold", "evidence": "EIA lists 2 units of 20 MW"}}}
    b = batch_dir(tmp_path, cov, name="us-il")
    lanes = {"newplants": [{"record_id": "N1", "plant_name": "University of Illinois Cogen Facility",
                            "researcher_notes": "EIA plant 54044 is an operating cogeneration plant."}]}
    out, _ = gate_ids_followup({"where": WHERE, "mode": "update", "ids_followup": LEADS}, lanes, b)
    assert out == []


def test_ids_followup_decision_needs_evidence_and_gem_id(tmp_path):
    cov = {"sources": {}, "ids_followup": {
        "54044": {"decision": "out_of_scope", "evidence": ""},
        "7760": {"decision": "already_in_gem", "evidence": "same site as Tilton Energy"}}}
    b = batch_dir(tmp_path, cov, name="us-il")
    out, _ = gate_ids_followup({"where": WHERE, "mode": "update", "ids_followup": LEADS}, {}, b)
    assert len(out) == 2 and "evidence" in out[0][1] and "gem_plant_id" in out[1][1]


def test_ids_followup_reads_ids_file_without_index_key(tmp_path):
    f = tmp_path / "ids.json"
    f.write_text(json.dumps({"leads": [
        {"source": "eia", "name": "Alsey", "ids": "EIA: 7818", "capacity_mw": 173, "status": "operating"},
        {"source": "eip", "name": "Other", "ids": "EIP: 1"}]}), encoding="utf-8")
    b = batch_dir(tmp_path, name="us-il")
    out, _ = gate_ids_followup({"where": WHERE, "mode": "update"}, {}, b, ids_file=f)
    assert [o[0] for o in out] == ["EIA:7818"]


def test_ids_followup_missing_source_is_one_finding(tmp_path):
    b = batch_dir(tmp_path, name="us-zz")
    out, _ = gate_ids_followup({"where": dict(WHERE, slug="nowhere-zz"), "mode": "update"}, {}, b)
    assert len(out) == 1


# ------------------------------------------------------------- brief block ---

def test_scope_brief_has_one_line_per_eia_plant(tmp_path):
    f = tmp_path / "ids.json"
    f.write_text(json.dumps({"leads": [
        {"source": "eia", "name": "Alsey", "ids": "EIA: 7818", "capacity_mw": 173,
         "status": "operating", "county": "Scott"},
        {"source": "eip", "name": "Other", "ids": "EIP: 1"}]}), encoding="utf-8")
    leads = eia_lead_tasks(f)
    assert [d["eia_id"] for d in leads] == ["7818"]
    text = render_scope_brief(leads, WANTED, "us-il")
    lines = [ln for ln in text.splitlines() if ln.startswith("- EIA plant 7818")]
    assert len(lines) == 1 and "Alsey" in lines[0] and "173" in lines[0] and "operating" in lines[0]
    for word in ("add", "below_threshold", "out_of_scope", "already_in_gem", "ids_followup"):
        assert word in text
    assert "- a: Source A" in text and "coverage.json" in text


def test_scope_brief_without_leads_says_so():
    assert "no EIA plant" in render_scope_brief([], None, "us-ks")
    assert eia_lead_tasks(None) == []


def test_ids_followup_country_reads_register_leads(tmp_path):
    f = tmp_path / "ids.json"
    f.write_text(json.dumps({"leads": [
        {"source": "eea", "name": "Elektrociepłownia Kielce", "ids": "PL.MŚ/000000366.PART", "capacity_mw": None},
        {"source": "entsoe", "name": "Unit X", "ids": "ENTSO-E: 19W000000000294O", "capacity_mw": 450}]}),
        encoding="utf-8")
    cov = {"sources": {}, "ids_followup": {
        "19W000000000294O": {"decision": "already_in_gem", "evidence": "same unit", "gem_plant_id": "L1"}}}
    b = batch_dir(tmp_path, cov, name="poland")
    where = {"kind": "country", "name": "Poland", "slug": "poland"}
    out, _ = gate_ids_followup({"where": where, "mode": "update"}, {}, b, ids_file=f)
    assert [o[0] for o in out] == ["EEA:PL.MŚ/000000366.PART"]
    lanes = {"qa": [{"record_id": "Q1", "researcher_notes": "PL.MŚ/000000366.PART is a heat plant."}]}
    assert gate_ids_followup({"where": where, "mode": "update"}, lanes, b, ids_file=f)[0] == []


def test_ids_followup_country_without_file_is_skipped(tmp_path):
    b = batch_dir(tmp_path, name="atlantis")
    out, info = gate_ids_followup({"where": {"kind": "country", "name": "Atlantis", "slug": "atlantis"},
                                   "mode": "update"}, {}, b)
    assert out == [] and "skipped" in info[0]


def test_scope_brief_names_register_leads():
    leads = [{"eia_id": "PL.MŚ/000000366.PART", "register": "EEA combustion plant", "name": "EC Kielce",
              "capacity_mw": None, "status": "reported", "basis": "100% gas"}]
    text = render_scope_brief(leads, None, "poland", 20)
    assert "## Register plants missing from GEM" in text and "- EEA combustion plant PL.MŚ/000000366.PART: EC Kielce" in text
    assert "keyed by register ID" in text

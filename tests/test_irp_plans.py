"""Every resource plan read in full (Baird 2026-11-06, after the Kentucky batch missed the
KYMEA and Henderson plan options): irp_plans.py finds the gas lines and named sites in each
plan, and state_gate's hard gate `irp-plans` fails a scope with no plan list, a stale or
missing plan file, or a plan with no full answer in coverage.json."""
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import irp_plans as ip  # noqa: E402
from build_review_package import irp_notes_rows  # noqa: E402
from state_gate import gate_irp_plans  # noqa: E402

TODAY = dt.date(2026, 11, 6)
INDEX = {"where": {"kind": "state", "name": "Kentucky", "country": "United States", "postal": "ky"},
         "plants": []}
KEYS = {"east bend": [("L100000103938", "East Bend Generating Station", "Kentucky")],
        "carbon": [("L100000104221", "Carbon Power Plant", "Utah")],
        "wilson": [("L100000103953", "Wilson Station", "Kentucky")],
        "kymea i": [("L100001026095", "KYMEA Energy Center I", "Kentucky")]}


def test_scan_finds_table_rows_and_named_sites():
    text = ("Figure 1.2 Preferred Portfolio\nEast Bend CC (1x1) 664 664\n"
            "addition of a combined cycle (CC) at East Bend beginning in 2039.\n"
            "\fThe plan also studies KYMEA Energy Center II, a 92 MW engine plant.\n"
            "carbon capture on a combined cycle with 90% capture at 500 MW\n")
    hits, preferred, unmatched = ip.scan_text(text, KEYS, 1, home="Kentucky")
    assert preferred == ["1:1"]
    assert any(h["plants"] and h["plants"][0]["plant_id"] == "L100000103938" for h in hits)
    assert "KYMEA Energy Center II" in unmatched
    # "carbon capture" is not the Carbon plant in Utah: a one-word name away from home needs a site word
    assert not any(p["plant_id"] == "L100000104221" for h in hits for p in h["plants"])


def test_one_word_name_at_home_matches():
    assert ip.match_plants(" when wilson retires the model adds a cc ", KEYS, "Kentucky")[0]["plant_id"] == "L100000103953"
    assert ip.match_plants(" the carbon plant ct unit ", KEYS, "Kentucky")[0]["plant_id"] == "L100000104221"


def test_best_utility_prefers_longest_name():
    us = [{"utility": "Kentucky Power Company", "short": "KPCO"},
          {"utility": "East Kentucky Power Cooperative", "short": "EKPC"}]
    assert ip.best_utility("Integrated resource plan of East Kentucky Power Cooperative", us)["short"] == "EKPC"


def test_newer_hint_bounded_by_filing_and_this_year():
    text = "The 2024 Integrated Resource Plan. Next IRP due 2027. 2026 IRP filed."
    got = ip.newer_on_landing(text, 2024)
    assert 2024 not in got and all(y <= dt.date.today().year for y in got)


def write_batch(tmp, answers=None, generated="2026-11-06", **extra):
    b = tmp / "us-ky"
    (b / "harvest").mkdir(parents=True)
    u = {"utility": "Duke Energy Kentucky", "short": "Duke", "plan": "2024 IRP", "key": "plan Duke Energy Kentucky",
         "documents": [{"url": "https://x/duke.pdf", "reached": True}], "newer_hints": [], "overdue": False,
         "unmatched_names": {}}
    u.update(extra)
    (b / "harvest" / "irp_plans.json").write_text(json.dumps(
        {"generated": generated, "utilities": [u], "unlisted_cases": [], "owners_unlisted": {},
         "sheet_unlisted": [], "needs_answer": [u["key"]]}))
    (b / "coverage.json").write_text(json.dumps({"irp_plans": answers or {}}))
    settings = tmp / "irp_plans.json"
    settings.write_text("{}")
    return b, settings


GOOD = {"pages": "All 160 PDF pages; preferred plan Figure 1.2 on PDF page 4",
        "additions": [{"what": "East Bend combined cycle 2039", "plant_id": "L100000103938"}],
        "options": [{"what": "588 MW with carbon capture", "plant_id": "L100000103938"}],
        "evidence": "Duke Energy Kentucky's 2024 plan, Figure 1.2 on PDF page 4, adds a 664 MW combined cycle at East Bend in 2039."}


def test_gate_passes_full_answer(tmp_path):
    b, s = write_batch(tmp_path, {"plan Duke Energy Kentucky": GOOD})
    out, _ = gate_irp_plans(INDEX, {}, b, today=TODAY, settings=s)
    assert out == []


def test_gate_fails_missing_answer_and_stale_file(tmp_path):
    b, s = write_batch(tmp_path, {}, generated="2026-10-01")
    out = [m for _, m in gate_irp_plans(INDEX, {}, b, today=TODAY, settings=s)[0]]
    assert any("more than" in m for m in out) and any("no answer" in m for m in out)


def test_gate_fails_without_plan_list(tmp_path):
    b, _ = write_batch(tmp_path, {})
    out, _ = gate_irp_plans(INDEX, {}, b, today=TODAY, settings=tmp_path / "missing.json")
    assert out and "no plan list" in out[0][1]


def test_gate_option_needs_a_tie_and_names_need_checking(tmp_path):
    bad = dict(GOOD, options=[{"what": "a 92 MW engine plant"}])
    b, s = write_batch(tmp_path, {"plan Duke Energy Kentucky": bad},
                       unmatched_names={"KYMEA Energy Center II": "1:36"})
    out = [m for _, m in gate_irp_plans(INDEX, {}, b, today=TODAY, settings=s)[0]]
    assert any("tie it to" in m for m in out) and any("names_checked" in m for m in out)


def test_gate_watch_record_must_be_in_batch(tmp_path):
    ans = dict(GOOD, options=[{"what": "x", "record_id": "us-ky:plant:monitor-9"}])
    b, s = write_batch(tmp_path, {"plan Duke Energy Kentucky": ans})
    out, _ = gate_irp_plans(INDEX, {}, b, today=TODAY, settings=s)
    assert any("not in the batch" in m for _, m in out)
    lanes = {"monitor": [{"record_id": "us-ky:plant:monitor-9"}]}
    assert gate_irp_plans(INDEX, lanes, b, today=TODAY, settings=s)[0] == []


def test_notes_draft_names_plan_read_and_correction():
    irp = {"data": {"utilities": [{"utility": "Big Rivers Electric Corporation (BREC)", "irp_year": "2023 IRP",
                                   "links": [], "plants": []}]},
           "plans": {"utilities": [{"sheet": "Big Rivers Electric Corporation (BREC)", "utility": "Big Rivers",
                                    "plan": "2026 IRP", "case": "2026-00268"},
                                   {"utility": "Henderson Municipal Power & Light", "plan": "2026 IRP",
                                    "documents": [{"url": "https://x/hmpl.pdf"}], "sheet_note": "36 MW engines"}],
                     "sheet_corrections": [{"utility": "Big Rivers Electric Corporation (BREC)",
                                            "line": "tab shows 2023; newest is the 2026 IRP."}]}}
    rows = irp_notes_rows({}, irp, quarter="Q4 2026")
    assert "read 2026 IRP (case 2026-00268) in full" in rows[0][7] and "newest is the 2026" in rows[0][8]
    assert rows[1][0] == "Henderson Municipal Power & Light" and rows[1][8].startswith("Not on the tab")


def test_failed_fetch_keeps_text_saved_earlier(tmp_path, monkeypatch):
    """Oklahoma, 2026-11-06: ompa.com began refusing connections and a rerun overwrote the
    saved minutes with nothing. A failed fetch now returns the saved text and leaves it."""
    import fetch
    from types import SimpleNamespace
    saved = tmp_path / "1.txt"
    saved.write_text("minutes " * (ip.MIN_CHARS // 8 + 10), encoding="utf-8")
    monkeypatch.setattr(fetch, "fetch_page",
                        lambda url, timeout=0: SimpleNamespace(status="000", text="", is_pdf=False))
    ok, status, text = ip.read_document("https://example.org/a.pdf", saved)
    assert ok and status.startswith("saved") and text.startswith("minutes")
    assert saved.read_text(encoding="utf-8").startswith("minutes")
    fresh = tmp_path / "2.txt"
    ok, status, text = ip.read_document("https://example.org/b.pdf", fresh)
    assert not ok and status == "000" and fresh.read_text(encoding="utf-8") == ""


def test_read_document_local_path(tmp_path, monkeypatch):
    """A plan saved by a harvester is read from its repo path, never fetched."""
    import irp_plans
    monkeypatch.setattr(irp_plans, "REPO_ROOT", tmp_path)
    (tmp_path / "plan.txt").write_text("gas turbine " * 600, encoding="utf-8")
    ok, status, text = irp_plans.read_document("plan.txt", tmp_path / "out" / "0.txt")
    assert ok and status == "local" and "gas turbine" in text
    ok, status, _ = irp_plans.read_document("missing.pdf", tmp_path / "out" / "1.txt")
    assert not ok and status == "local file missing"

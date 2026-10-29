"""Offline tests for check_existing_links.py (the pre-sweep check of Data Source links
already in the export): URL splitting, the words a saved copy must hold, the live and
dead call, saved-copy staging that never duplicates, the cache, and the brief section."""
import csv
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import build_state_brief as bsb  # noqa: E402
import check_existing_links as cel  # noqa: E402

DEAD = "https://www.kdhe.ks.gov/DocumentCenter/View/52541/Viola-PSD.pdf"
LIVE = "https://www.eia.gov/electricity/page"
SNAP = "https://web.archive.org/web/20251203003910/" + DEAD
BLOCKED = "https://www.walled.example/doc"

HEADER = ["Country/Area", "State/Province", "GEM location ID", "Plant name", "GEM unit ID", "Unit name",
          "Fuel", "Fuel Data Source", "Equipment Manufacturer/Model", "Turbine/Engine Equipment Data Source",
          "Hydrogen Data Source", "Status", "Status Data Source"]


@pytest.fixture
def export(tmp_path):
    p = tmp_path / "export.csv"
    rows = [
        ["United States", "Kansas", "L1", "Viola Generating Station", "G1", "1", "fossil gas: natural gas",
         f"{LIVE}, {DEAD}", "Mitsubishi Power: M501JAC", DEAD, "https://h2.example/x", "operating", BLOCKED],
        ["United States", "Kansas", "L1", "Viola Generating Station", "G2", "2", "fossil gas: natural gas",
         f"{LIVE}; {DEAD}", "", "", "", "operating", ""],
        ["United States", "Missouri", "L9", "Other Plant", "G9", "1", "coal", "https://mo.example/a", "", "", "", "", ""],
    ]
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        w.writerows(rows)
    return p


def fake_net(monkeypatch, dead=(DEAD,), blocked=(BLOCKED,), snaps=None, holds=True, calls=None):
    calls = calls if calls is not None else {"live": [], "read": [], "lookup": []}
    snaps = {DEAD: [(SNAP, "20251203003910")]} if snaps is None else snaps

    def fetch(url, timeout=30):
        calls["live"].append(url)
        status = "404" if url in dead else "403" if url in blocked else "200"
        return status, "<html>ok</html>", False, []

    def check(url, expected, require_all, wayback_fallback=True, timeout=30):
        st = "404" if url in dead else "403" if url in blocked else "200"
        return (True, "OK") if st == "200" else (False, f"HTTP {st}")

    def lookup(url, limit=3, every=False):
        calls["lookup"].append(url)
        return snaps.get(url, [])

    def verify(url, expected, **kw):
        calls["read"].append((url, tuple(expected)))
        return (True, "OK") if holds else (False, f"missing expected content: {expected}")

    monkeypatch.setattr(cel.url_verifier, "_fetch", fetch)
    monkeypatch.setattr(cel.url_verifier, "_check", check)
    monkeypatch.setattr(cel.url_verifier, "_wayback_snapshots", lookup)
    monkeypatch.setattr(cel.url_verifier, "verify_url", verify)
    monkeypatch.setattr(cel, "_host_turn", lambda *a, **k: __import__("contextlib").nullcontext())
    return calls


def scope_ks():
    return bsb.make_scope(state="Kansas")


def test_split_urls_handles_commas_semicolons_and_query_commas():
    cell = "https://a.org/x?y=1,2, https://b.org/p.pdf; https://c.org/z"
    assert cel.split_urls(cell) == ["https://a.org/x?y=1,2", "https://b.org/p.pdf", "https://c.org/z"]
    assert cel.split_urls("") == []


def test_collect_dedupes_skips_hydrogen_and_other_states(export):
    rows, header = cel.read_scope(scope_ks(), export)
    assert len(rows) == 2
    m = cel.collect(rows, header)
    assert "https://h2.example/x" not in m
    assert "https://mo.example/a" not in m
    assert len(m) == 3                                   # LIVE, DEAD, BLOCKED
    cols = {(u["unit_id"], u["ds_column"]) for u in m[DEAD]}
    assert cols == {("G1", "Fuel Data Source"), ("G1", "Turbine/Engine Equipment Data Source"),
                    ("G2", "Fuel Data Source")}


def test_name_word_and_value_words():
    assert cel.name_word("Viola Generating Station") == "Viola"
    assert cel.name_word("Lawrence Energy Center (Kansas)") == "Lawrence"
    assert cel.value_words("Fuel", "fossil gas: natural gas") == ["natural gas"]
    assert cel.value_words("Equipment Manufacturer/Model", "Mitsubishi Power: M501JAC") == ["M501JAC"]
    assert cel.value_words("Owner(s)", "Kansas Power Pool [100%]; Other [0%]") == ["Kansas Power Pool"]
    assert cel.value_words("Start year", "2026.0") == ["2026"]
    assert cel.value_words("Status", "shelved - inferred 2 y") == []
    assert cel.value_words("CHP", "yes") == []
    assert cel.value_words("Fuel", "") == []


def test_run_checks_classifies_and_reads_saved_copy(export, monkeypatch, tmp_path):
    calls = fake_net(monkeypatch)
    rows, header = cel.read_scope(scope_ks(), export)
    items = cel.run_checks(cel.collect(rows, header), cel.Cache(tmp_path / "c.json", False), workers=2)
    by = {i["url"]: i for i in items}
    assert by[LIVE]["status"] == "live"
    assert by[BLOCKED]["status"] == "blocked"
    d = by[DEAD]
    assert d["status"] == "dead" and d["verified"] and d["snapshot"] == SNAP
    ok = {(u["unit_id"], u["ds_column"]): u["saved_copy"]["ok"] for u in d["usages"]}
    assert all(ok.values())
    assert (SNAP, ("Viola", "M501JAC")) in calls["read"]
    assert (SNAP, ("Viola", "natural gas")) in calls["read"]
    c = cel.tally(items)
    assert (c["distinct_urls"], c["live"], c["blocked"], c["dead"],
            c["dead_with_verified_snapshot"], c["dead_without"]) == (3, 1, 1, 1, 1, 0)


def test_dead_without_snapshot_or_value_goes_to_replacement(export, monkeypatch, tmp_path):
    fake_net(monkeypatch, snaps={})
    rows, header = cel.read_scope(scope_ks(), export)
    items = cel.run_checks(cel.collect(rows, header), cel.Cache(tmp_path / "c.json", False), workers=1)
    d = next(i for i in items if i["url"] == DEAD)
    assert d["status"] == "dead" and not d["verified"] and d["lookup"] == "none"
    assert len(cel.needs_replacement(items)) == 3
    fake_net(monkeypatch, holds=False)
    items = cel.run_checks(cel.collect(rows, header), cel.Cache(tmp_path / "d.json", False), workers=1)
    d = next(i for i in items if i["url"] == DEAD)
    assert not d["verified"] and d["snapshots"]
    assert all("missing expected" in r["why"] for r in cel.needs_replacement(items))


def test_stage_is_idempotent_and_keeps_staging_shape(export, monkeypatch, tmp_path):
    fake_net(monkeypatch)
    rows, header = cel.read_scope(scope_ks(), export)
    items = cel.run_checks(cel.collect(rows, header), cel.Cache(tmp_path / "c.json", False), workers=1)
    batch = tmp_path / "us-ks"
    (batch / "staging").mkdir(parents=True)
    existing = {"meta": {"lane": "updates", "counts": {"records": 1, "reverified": 0}},
                "records": [{"record_id": "keep-me"}]}
    path = batch / "staging" / "staged_updates.json"
    path.write_text(json.dumps(existing), encoding="utf-8")
    added, already, _ = cel.stage(items, scope_ks(), batch)
    assert (added, already) == (3, 0)
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["records"][0]["record_id"] == "keep-me"
    rec = next(r for r in data["records"] if r["record_id"] == "L1:G2:fuel-saved-copy")
    assert rec["refs"] == {"Fuel Data Source": [SNAP]}            # only the added copy; the build merges
    assert rec["fields"] == rec["current"] == {"Fuel": "fossil gas: natural gas"}
    assert rec["reverified"] and rec["verdict"] == "match" and rec["checks"] == [10]
    assert DEAD in rec["researcher_notes"] and "—" not in rec["researcher_notes"]
    assert data["meta"]["counts"] == {"records": 4, "reverified": 3}
    assert cel.stage(items, scope_ks(), batch)[:2] == (0, 3)
    assert len(json.loads(path.read_text(encoding="utf-8"))["records"]) == 4


def test_dry_run_writes_outputs_but_never_staging(export, monkeypatch, tmp_path):
    fake_net(monkeypatch)
    monkeypatch.setattr(cel, "work_dir", lambda: tmp_path)
    monkeypatch.setattr(cel, "require_fresh_export", lambda *a, **k: None)
    batch = tmp_path / "us-ks"
    assert cel.main(["--state", "Kansas", "--csv", str(export), "--batch", str(batch), "--dry-run"]) == 0
    assert (batch / "existing_links.json").exists() and (batch / "existing_links.md").exists()
    assert not (batch / "staging").exists()
    out = json.loads((batch / "existing_links.json").read_text(encoding="utf-8"))
    assert out["dry_run"] and out["counts"]["dead_with_verified_snapshot"] == 1
    assert "Gone links by site" in (batch / "existing_links.md").read_text(encoding="utf-8")


def test_cache_skips_refetch_within_seven_days(export, monkeypatch, tmp_path):
    calls = fake_net(monkeypatch)
    rows, header = cel.read_scope(scope_ks(), export)
    um = cel.collect(rows, header)
    cache = cel.Cache(tmp_path / "c.json", False)
    cel.run_checks(um, cache, workers=1)
    cache.save()
    n = len(calls["live"])
    cache2 = cel.Cache(tmp_path / "c.json", False)
    items = cel.run_checks(um, cache2, workers=1)
    # blocked addresses are not cached (worth another try); everything else is
    assert len(calls["live"]) == n + 1
    assert next(i for i in items if i["url"] == DEAD)["verified"]
    cache3 = cel.Cache(tmp_path / "c.json", True)         # --refresh
    cel.run_checks(um, cache3, workers=1)
    assert len(calls["live"]) == n + 1 + 3


def test_archive_refused_is_not_cached_or_called_none(export, monkeypatch, tmp_path):
    fake_net(monkeypatch)
    monkeypatch.setattr(cel.url_verifier, "_wayback_snapshots", lambda *a, **k: "lookup-failed")
    rows, header = cel.read_scope(scope_ks(), export)
    cache = cel.Cache(tmp_path / "c.json", False)
    items = cel.run_checks(cel.collect(rows, header), cache, workers=1)
    d = next(i for i in items if i["url"] == DEAD)
    assert d["lookup"] == "refused" and not d["verified"]
    assert cache.url(DEAD) is None


def test_brief_section_lists_gone_links(export, monkeypatch, tmp_path):
    fake_net(monkeypatch, snaps={})
    rows, header = cel.read_scope(scope_ks(), export)
    items = cel.run_checks(cel.collect(rows, header), cel.Cache(tmp_path / "c.json", False), workers=1)
    out = cel.build_output(scope_ks(), items, len(rows), True)
    p = tmp_path / "existing_links.json"
    p.write_text(json.dumps(out), encoding="utf-8")
    gone = bsb.load_existing_links(p, scope_ks())
    assert set(gone) == {"L1"} and len(gone["L1"]) == 3
    text = "\n".join(bsb.gone_links_block(gone["L1"]))
    assert "## Links already in the database that are gone" in text
    assert DEAD in text and "no saved copy exists" in text
    assert bsb.gone_links_block(None) == []
    with pytest.raises(SystemExit):
        bsb.load_existing_links(p, bsb.make_scope(state="Iowa"))

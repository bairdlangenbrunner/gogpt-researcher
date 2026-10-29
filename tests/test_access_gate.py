"""A page an agent gave up on is retried, and a form is never a reason to give
up (Baird 2026-10-19, after the Iowa sweep skipped the state's permit search):
access_audit reads every blocked or dead source_log entry and records its
retry, and state_gate.gate_access fails an excuse note, an unretried give-up
and one that loads on retry."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from access_audit import (EXCUSE, RETRY_FILE, classify, gave_up_outcome,  # noqa: E402
                          source_log_gave_up, unknown_outcome, write_retry)
from state_gate import gate_access  # noqa: E402

FORM = "https://example.gov/PublicComment"
DEAD = "https://example.com/gone.pdf"
WALL = "https://example.org/news"


def batch(tmp_path, entries, retried=None):
    (tmp_path / "shards").mkdir()
    (tmp_path / "shards" / "L1.json").write_text(json.dumps({"source_log": entries}))
    if retried is not None:
        (tmp_path / RETRY_FILE).write_text(json.dumps(retried))
    return tmp_path


def test_excuse_catches_give_ups_not_verifier_notes():
    assert EXCUSE.search("Page loads but is a search form that needs a script to run.")
    assert EXCUSE.search("The page is drawn by JavaScript.")
    assert EXCUSE.search("Results are in a paged table I did not search.")
    assert not EXCUSE.search("Not run through the URL checker.")
    assert not EXCUSE.search("not run through the verifier")
    assert not EXCUSE.search("The PDF form of the notice states 94 MW.")


def test_source_log_give_ups_are_read(tmp_path):
    b = batch(tmp_path, [{"url": DEAD, "outcome": "dead", "note": "HTTP 404"},
                         {"url": WALL, "outcome": "verified", "note": ""}])
    got = source_log_gave_up([b])
    assert list(got) == [DEAD]
    assert classify(got[DEAD]["reason"]) == "gone"
    assert classify("agent gave up: blocked: a search form") == "not_tried"


def test_write_retry_keeps_only_this_batch(tmp_path):
    b = batch(tmp_path, [{"url": DEAD, "outcome": "dead", "note": "HTTP 404"}])
    write_retry([b], {}, {DEAD: (False, "HTTP 404"), WALL: (True, "")})
    data = json.loads((b / RETRY_FILE).read_text())
    assert set(data) == {DEAD} and data[DEAD]["ok"] is False


def test_gate_fails_excuse_unretried_and_now_loading(tmp_path):
    b = batch(tmp_path, [
        {"url": FORM, "outcome": "blocked", "note": "A search form. I did not run a search."},
        {"url": DEAD, "outcome": "dead", "note": "HTTP 404"},
        {"url": WALL, "outcome": "blocked", "note": "HTTP 403"}],
        retried={WALL: {"ok": True, "reason": ""}})
    out, _ = gate_access(b)
    why = {w.split(": ", 1)[1]: r for w, r in out}
    assert "form" in why[FORM]
    assert "never retried" in why[DEAD]
    assert "loads now" in why[WALL]


def test_gate_passes_retried_failures(tmp_path):
    b = batch(tmp_path, [{"url": DEAD, "outcome": "dead", "note": "HTTP 404"},
                         {"url": WALL, "outcome": "verified", "note": ""}],
              retried={DEAD: {"ok": False, "reason": "HTTP 404",
                              "archive": {"checked": True, "snapshots": []}}})
    out, info = gate_access(b)
    assert out == []
    assert "still failing: 1" in info[0]


def test_dead_spellings_are_give_ups(tmp_path):
    # The Walnut shard wrote "dead_link", which the gate used to skip.
    assert gave_up_outcome("dead_link") == "dead"
    assert gave_up_outcome("Blocked by firewall") == "blocked"
    assert gave_up_outcome("verified") == "" and gave_up_outcome("not relevant") == ""
    assert unknown_outcome("gone") and not unknown_outcome("dead_link")
    b = batch(tmp_path, [{"url": DEAD, "outcome": "dead_link", "note": "HTTP 404"},
                         {"url": WALL, "outcome": "gone", "note": ""}])
    why = {w.split(": ", 1)[1]: r for w, r in gate_access(b)[0]}
    assert "never retried" in why[DEAD]
    assert "unknown outcome 'gone'" in why[WALL]


def test_dead_needs_a_wayback_lookup(tmp_path):
    b = batch(tmp_path, [{"url": DEAD, "outcome": "dead", "note": "HTTP 404"}],
              retried={DEAD: {"ok": False, "reason": "HTTP 404"}})
    out, _ = gate_access(b)
    assert "no Wayback lookup" in out[0][1]


def test_dead_with_saved_copy_must_be_cited(tmp_path):
    snap = "https://web.archive.org/web/20230329141358/" + DEAD
    retried = {DEAD: {"ok": False, "reason": "HTTP 404",
                      "archive": {"checked": True, "snapshots": [snap]}}}
    b = batch(tmp_path, [{"url": DEAD, "outcome": "dead", "note": "HTTP 404"}], retried=retried)
    out, _ = gate_access(b)
    assert "saved copies exist" in out[0][1] and snap in out[0][1]
    (tmp_path / "cited").mkdir()
    b = batch(tmp_path / "cited", [{"url": DEAD, "outcome": "dead", "note": "HTTP 404"},
                                   {"url": snap, "outcome": "verified", "note": "saved copy"}],
              retried=retried)
    out, _ = gate_access(b)
    assert out == []


def test_every_capture_lookup_skips_the_merge(monkeypatch):
    # The index merges captures it calls identical; every=True must not.
    import url_verifier as uv
    queries = []
    cdx = ("20230329141358 " + DEAD + "\n20231021230622 " + DEAD
           + "\n20240812065700 " + DEAD + "\n")
    monkeypatch.setattr(uv, "_archive_get", lambda u: queries.append(u) or cdx)
    uv._CACHE.clear()
    uv._wayback_snapshots(DEAD)
    every = uv._wayback_snapshots(DEAD, every=True)
    uv._CACHE.clear()
    assert "collapse=digest" in queries[0] and "collapse=digest" not in queries[1]
    assert len(every) == 3 and every[0][1] == "20240812065700"


def test_archive_check_records_lookup_only_for_dead(tmp_path, monkeypatch):
    import access_audit
    monkeypatch.setattr("url_verifier._wayback_snapshots",
                        lambda url, limit=3, every=False: [("https://web.archive.org/web/2023/" + url, "2023")])
    failures = {DEAD: {"url": DEAD, "outcome": "dead"}, WALL: {"url": WALL, "outcome": "blocked"}}
    got = access_audit.archive_check(failures)
    assert list(got) == [DEAD] and got[DEAD]["checked"] is True and got[DEAD]["snapshots"]


def test_fetch_log_keeps_to_the_batch(tmp_path, monkeypatch):
    """The fetch log is shared by every session: an entry counts only when tagged
    with this batch or, untagged, when its host appears in the batch's own files
    (Iowa and Illinois failures leaked into the Kansas audit, 2026-10-22)."""
    import access_audit
    b = tmp_path / "us-ks"
    (b / "briefs").mkdir(parents=True)
    (b / "briefs" / "L1.md").write_text("see https://kdhe.example.gov/doc/1")
    log = tmp_path / "failures.jsonl"
    rows = [{"url": "https://kdhe.example.gov/doc/2", "status": "404"},
            {"url": "https://iowa.example.com/story", "status": "403"},
            {"url": "https://iowa.example.com/tagged", "status": "403", "batch": "us-ks"},
            {"url": "https://kdhe.example.gov/other", "status": "404", "batch": "us-ia"}]
    log.write_text("".join(json.dumps({"ts": "2999-01-01T00:00:00", **r}) + "\n" for r in rows))
    monkeypatch.setattr(access_audit.fetch, "FAIL_LOG", log)
    got = access_audit._fetch_failures([b])
    assert set(got) == {"https://kdhe.example.gov/doc/2", "https://iowa.example.com/tagged"}


def test_retry_counts_a_soft_404_as_still_failing(monkeypatch):
    """A page that answers 200 with a "404 Not Found" title has not come back."""
    import access_audit
    from types import SimpleNamespace
    page = SimpleNamespace(status="200", notes="",
                           text="<html><title>404 Not Found | EIP Oil &amp; Gas Watch</title></html>")
    monkeypatch.setattr(access_audit.fetch, "fetch_page", lambda u, **k: page)
    got = access_audit.retry({"https://example.org/x": {"source": "fetch"}}, False)
    ok, reason = got["https://example.org/x"]
    assert not ok and "soft-error" in reason

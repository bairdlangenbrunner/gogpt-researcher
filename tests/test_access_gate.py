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

from access_audit import EXCUSE, RETRY_FILE, classify, source_log_gave_up, write_retry  # noqa: E402
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
              retried={DEAD: {"ok": False, "reason": "HTTP 404"}})
    out, info = gate_access(b)
    assert out == []
    assert "still failing: 1" in info[0]

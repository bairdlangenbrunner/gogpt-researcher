"""scopes/<tag>/ layout (repo layout audit, Baird 2026-10-29): one tag per scope,
the scope's files under scopes/<tag>/, the older homes read for one cycle."""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import paths  # noqa: E402


def test_scope_tag_one_form_for_every_spelling():
    assert paths.scope_tag(state="North Dakota") == "us-nd"
    assert paths.scope_tag(state="ND") == "us-nd"
    assert paths.scope_tag(state="us-nd") == "us-nd"
    assert paths.scope_tag(country="South Africa") == "south-africa"
    with pytest.raises(ValueError):
        paths.scope_tag(state="Atlantis")


def test_run_variants_share_the_scope_folder():
    assert paths.scope_base("us-il-dc") == "us-il"
    assert paths.scope_base("germany-permits") == "germany"
    assert paths.scope_base("us-ms") == "us-ms"
    assert paths.scope_dir("us-il-val") == paths.SCOPES_DIR / "us-il"


@pytest.fixture
def fake_repo(tmp_path, monkeypatch):
    monkeypatch.setattr(paths, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(paths, "SCOPES_DIR", tmp_path / "scopes")
    return tmp_path


def test_permits_folder_new_then_older(fake_repo):
    new = fake_repo / "scopes" / "us-ks" / "work" / "permits"
    old = fake_repo / "work" / "permits" / "us-ks"
    assert paths.scope_permits("us-ks") == new
    old.mkdir(parents=True)
    assert paths.scope_permits("us-ks") == old
    assert paths.scope_permits("us-ks", legacy=False) == new
    new.mkdir(parents=True)
    assert paths.scope_permits("us-ks") == new
    assert paths.scope_permits("us-ks-dc", legacy=False) == fake_repo / "scopes" / "us-ks" / "work" / "us-ks-dc" / "permits"


def test_note_and_coverage_new_then_older(fake_repo):
    old_note = fake_repo / "docs" / "country_notes" / "united_states" / "north_dakota.md"
    old_note.parent.mkdir(parents=True)
    old_note.write_text("old")
    assert paths.scope_note(state="North Dakota") == old_note
    (fake_repo / "scopes" / "us-nd").mkdir(parents=True)
    (fake_repo / "scopes" / "us-nd" / "note.md").write_text("new")
    assert paths.scope_note(state="North Dakota") == fake_repo / "scopes" / "us-nd" / "note.md"
    assert paths.scope_note(state="Ohio") is None

    old_cov = fake_repo / "docs" / "coverage" / "us-nd.json"
    old_cov.parent.mkdir(parents=True)
    old_cov.write_text("{}")
    assert paths.scope_coverage("us-nd") == old_cov
    (fake_repo / "scopes" / "us-nd" / "coverage.json").write_text("{}")
    assert paths.scope_coverage("us-nd") == fake_repo / "scopes" / "us-nd" / "coverage.json"
    # a run variant has no list of its own
    assert paths.scope_coverage("us-nd-dc") == fake_repo / "docs" / "coverage" / "us-nd-dc.json"


def test_every_queue_settings_file_is_read():
    import pull_queues
    states = pull_queues.load_states()
    assert {"MI", "MS"} <= set(states)
    for st, cfg in states.items():
        assert cfg["settings_file"] == f"scopes/us-{st.lower()}/queues.json"
        assert {"name", "markets", "owner", "shared_owner", "pjm_states", "known"} <= set(cfg)


def test_ms_match_reads_the_same_known_list():
    ms_match = paths.load_scope_module("us-ms", "ms_match")
    settings = json.loads((ROOT / "scopes" / "us-ms" / "queues.json").read_text(encoding="utf-8"))
    assert ms_match.KNOWN == settings["known"]


def test_access_audit_reads_the_scope_harvest(tmp_path, monkeypatch):
    """A failure on a host named only in the scope's permit harvest still counts."""
    import access_audit
    b = tmp_path / "batches" / "us-ks"
    (b / "briefs").mkdir(parents=True)
    (b / "briefs" / "L1.md").write_text("no links here")
    harvest = tmp_path / "scopes" / "us-ks" / "work" / "permits"
    harvest.mkdir(parents=True)
    (harvest / "L1.md").write_text("permit at https://keims.example.gov/doc/1")
    log = tmp_path / "failures.jsonl"
    log.write_text(json.dumps({"ts": "2999-01-01T00:00:00", "url": "https://keims.example.gov/doc/9",
                               "status": "403"}) + "\n")
    monkeypatch.setattr(access_audit.fetch, "FAIL_LOG", log)
    assert set(access_audit._fetch_failures([b])) == {"https://keims.example.gov/doc/9"}

"""The supervised Claude in Chrome apply (docs/sops/database-browser-edits.md):
browser_apply.py queues accepted edits only and records a save only when the page
matches, and the guard hook asks before clicks and refuses them when unsupervised."""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "scripts", ROOT / ".claude" / "hooks"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import browser_apply  # noqa: E402
from guard_browser_db import decide  # noqa: E402

LINK = "https://example.com/plan.pdf"


def rec(rid, pid, col, value, current="", **extra):
    r = {"record_id": rid, "gem_plant_id": pid, "gem_unit_id": rid.split(":")[1],
         "plant_name": f"Plant {pid}", "unit_name": "GT1", "fields": {col: value},
         "current": {col: current}, "refs": {f"{col} Data Source": [LINK]},
         "action": f"Set {col}."}
    r.update(extra)
    return r


@pytest.fixture
def batch(tmp_path, monkeypatch):
    staging = tmp_path / "batches" / "us-xx" / "staging"
    staging.mkdir(parents=True)
    updates = [rec("L1:G1:status", "L1", "Status", "retired", "operating"),
               rec("L1:G2:status", "L1", "Status", "retired", "operating"),
               rec("L2:G3:capacity", "L2", "Capacity (MW)", "300", "250")]
    (staging / "staged_updates.json").write_text(json.dumps({"records": updates}))
    (staging / "staged_entity.json").write_text(json.dumps({"records": [
        {"record_id": "L2:entity:acme", "gem_plant_id": "L2", "entity_name": "Acme Power",
         "role": "owner", "lookup_result": "No match in GEM."}]}))
    log = [{"record_id": "L1:G1:status", "decision": "accept"},
           {"record_id": "L1:G2:status", "decision": "reject"},
           {"record_id": "L2:G3:capacity", "decision": "accept"}]
    (staging / "review_log.jsonl").write_text("\n".join(json.dumps(x) for x in log) + "\n")
    monkeypatch.setattr(browser_apply, "repo_root", lambda: tmp_path)
    monkeypatch.setattr(browser_apply, "work_dir", lambda: tmp_path / "work")
    return staging


def test_queue_keeps_accepted_edits_and_blocks_a_missing_entity(batch):
    q = browser_apply.build_queue("us-xx")
    ids = [e["record_id"] for p in q["plants"] for e in p["edits"]]
    assert ids == ["L1:G1:status", "L2:G3:capacity"]
    plants = {p["gem_plant_id"]: p for p in q["plants"]}
    assert plants["L1"]["edit_url"] == "https://gem-project-db.herokuapp.com/projects/edit/1"
    assert plants["L2"]["blocked_by"] and not plants["L1"]["blocked_by"]


def test_queue_refuses_an_unreviewed_batch(batch):
    (batch / "review_log.jsonl").unlink()
    with pytest.raises(SystemExit):
        browser_apply.build_queue("us-xx")


def test_record_logs_a_matching_save_and_the_queue_drops_it(batch):
    readback = {"Status": "retired", "Status Data Source": f"https://old.example\n{LINK}"}
    assert browser_apply.record("us-xx", "L1:G1:status", readback) == []
    applied = json.loads((batch / "applied_in_db.json").read_text())["records"]
    assert applied[0]["applied"]["by"] == "claude-in-chrome"
    ids = [e["record_id"] for p in browser_apply.build_queue("us-xx")["plants"] for e in p["edits"]]
    assert "L1:G1:status" not in ids


def test_record_refuses_a_mismatch_and_a_missing_link(batch):
    problems = browser_apply.record("us-xx", "L1:G1:status",
                                    {"Status": "operating", "Status Data Source": "https://old.example"})
    assert len(problems) == 2
    assert not (batch / "applied_in_db.json").exists()


def test_practice_records_stay_out_of_the_live_log(batch, tmp_path):
    readback = {"Status": "retired", "Status Data Source": LINK}
    assert browser_apply.record("us-xx", "L1:G1:status", readback, practice=True) == []
    assert not (batch / "applied_in_db.json").exists()
    assert (tmp_path / "work" / "browser_apply_practice_us-xx_log.json").exists()
    live = [e["record_id"] for p in browser_apply.build_queue("us-xx")["plants"] for e in p["edits"]]
    assert "L1:G1:status" in live


def ev(tool, mode="default", **args):
    return {"tool_name": f"mcp__claude-in-chrome__{tool}", "tool_input": args,
            "permission_mode": mode}


def test_guard_asks_before_a_click_and_refuses_it_when_unsupervised():
    assert decide(ev("computer", action="left_click"))[0] == "ask"
    assert decide(ev("computer", action="key"))[0] == "ask"
    for mode in ("bypassPermissions", "auto", "dontAsk"):
        assert decide(ev("computer", mode, action="left_click"))[0] == "deny"
    assert decide({"tool_name": "mcp__claude-in-chrome__computer",
                   "tool_input": {"action": "left_click"}})[0] == "ask"


def test_guard_lets_reading_and_filling_through():
    assert decide(ev("computer", "bypassPermissions", action="screenshot"))[0] == "allow"
    assert decide(ev("read_page"))[0] == "allow"
    assert decide(ev("form_input"))[0] == "allow"
    assert decide(ev("navigate", url="https://gem-project-db.herokuapp.com/projects/edit/1"))[0] == "allow"


def test_guard_refuses_scripts_batches_and_delete_pages():
    for tool in ("javascript_tool", "browser_batch", "shortcuts_execute", "upload_image"):
        assert decide(ev(tool))[0] == "deny"
    assert decide(ev("navigate", url="https://gem-project-db.herokuapp.com/units/9/delete"))[0] == "deny"
    assert decide({"tool_name": "Bash", "tool_input": {}}) is None

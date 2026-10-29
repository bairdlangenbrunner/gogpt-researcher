"""Offline test for build_state_brief --harvest: the loader and the scope-wide block."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import build_state_brief as b  # noqa: E402


def make(tmp_path):
    psc = {"dockets": [
        {"docket": "2024-UA-18", "utility": "Entergy Mississippi", "filed": "2024-03-04", "title": "CPCN for a gas plant",
         "facts": {"megawatts": ["754 MW combined cycle"]}, "matched": [{"plant_id": "L1", "plant": "Baxter", "how": "name"}]},
        {"docket": "2025-UA-3", "utility": "Mississippi Power", "filed": "2025-01-02", "title": "Gas peaker", "matched": []}],
        "unmatched_generation": ["2025-UA-3"]}
    q = {"entries": [{"source": "MISO", "queue_id": "J888", "project_name": "", "fuel": "Gas", "mw": 25.0, "status": "Done",
                      "county": "George", "poi": "Benndale 69kV", "owner": "COOP", "url": "https://x", "queue_date": "",
                      "in_service": "", "matched": []},
                     {"source": "MISO", "queue_id": "J1", "fuel": "Gas", "mw": 600, "status": "Done", "url": "https://x",
                      "queue_date": "2016-02-01", "in_service": "2022-06-01", "poi": "Morrow", "county": "Lamar",
                      "matched": [{"plant_id": "L1", "plant": "Baxter", "how": "poi"}]}],
         "unmatched_gas_oil": ["J888"], "hidden_fuel_leads": []}
    (tmp_path / "psc_dockets.json").write_text(json.dumps(psc))
    (tmp_path / "queues.json").write_text(json.dumps(q))


def test_load_harvest_tasks_and_brief(tmp_path):
    make(tmp_path)
    tasks, data = b.load_harvest(tmp_path)
    assert list(tasks) == ["L1"] and len(tasks["L1"]) == 2
    uid, item = tasks["L1"][0]
    assert uid is None and "2024-UA-18" in item["task"] and "754 MW" in item["task"]
    assert "lead, not proof" in tasks["L1"][1][1]["task"]
    _, plant = b.validation_tasks(tasks["L1"], [])
    assert len(plant) == 2
    md = b.render_harvest_brief(data)
    assert "2025-UA-3" in md and "J888" in md and "2024-UA-18" not in md

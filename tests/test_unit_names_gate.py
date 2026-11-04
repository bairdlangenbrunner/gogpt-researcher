"""The unit-names gate: a new unit is named 1, 2, 3 (September 2026 Editing
Manual, Unit Naming Guidelines), never with a description of its generators."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from state_gate import gate_unit_names  # noqa: E402


def plant(*names):
    return {"plant_name": "Alpha Data Center power station", "record_id": "us-xx:new:alpha",
            "units": [{"unit_name": n, "fields": {}} for n in names]}


def test_manual_names_pass():
    ok = ["1", "2", "1-1", "Phase 1", "1 IRP", "5R", "GT1", "CC1", "CT31-1", "Unit 1"]
    lanes = {"newplants": [plant(*ok)],
             "newunits": [{"record_id": "L1:new:gt2", "unit_name": "GT2", "fields": {"Unit name": "GT2"}}]}
    assert gate_unit_names(lanes) == []


def test_fleet_descriptions_fail():
    bad = ["49 generators, 3,000 kW", "CH3 generators", "Units 1 to 66", "Backup generators 3 MW",
           "Building 8", "Engines 1-20", "Installed, 7 generators, 3.0 MW"]
    out = gate_unit_names({"newplants": [plant(*bad)],
                           "newunits": [{"record_id": "L1:new:x", "unit_name": "Jet turbines 5 and 6"}]})
    assert len(out) == len(bad) + 1
    assert out[0][0].endswith("/unit[0]") and "name them 1, 2, 3" in out[0][1]

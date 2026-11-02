"""The interconnection queue check (Baird 2026-10-30): pull_queues.py records how
complete each queue read was and lists the requests a batch must answer, and
state_gate's hard gate `queues` fails a live gas or oil request at the threshold
with no answer in coverage.json, a market that was not read, or a short file."""
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import pull_queues as q  # noqa: E402
from state_gate import gate_queues  # noqa: E402

TODAY = dt.date(2026, 10, 30)
INDEX = {"where": {"kind": "state", "name": "Illinois", "country": "United States", "postal": "il"},
         "plants": []}


def entry(source, qid, fuel="Natural Gas", mw=300.0, status="Active", gas_oil=True, fuel_unknown=False,
          matched=(), withdrawn=""):
    return {"source": source, "queue_id": qid, "fuel": fuel, "mw": mw, "status": status,
            "gas_oil": gas_oil, "fuel_unknown": fuel_unknown, "matched": list(matched), "withdrawn": withdrawn}


ENTRIES = [
    entry("PJM", "C01-2036", mw=1150.0),                                   # live gas, must answer
    entry("PJM", "AA1-001", status="Withdrawn", withdrawn="2020-01-01"),   # withdrawn, skipped
    entry("PJM", "AB1-001", mw=20.0),                                      # under 50 MW, skipped
    entry("PJM", "AC1-001", status="In Service", matched=[{"plant_id": "L1"}]),  # in GEM, skipped
    entry("PJM", "AD2-194", status="Partially in Service - Under Construction",
          matched=[{"plant_id": "L1"}]),                                   # still building, must answer
    entry("MISO", "J4443", fuel="(not shown)", mw=None, gas_oil=False, fuel_unknown=True),  # must answer
    entry("MISO", "J10", fuel="Solar", gas_oil=False),                     # not gas, skipped
]


def full(name, market, rows, floor):
    return q.source_record(name, market, "u", "h", rows=rows, state_rows=5, entries=[], floor=floor)


def setup(tmp_path, answers=None, sources=None, markets=("MISO", "PJM"), generated="2026-10-29",
          newplants=(), monitor=()):
    batch = tmp_path / "us-il"
    (batch / "harvest").mkdir(parents=True)
    settings = tmp_path / "queues_settings.json"
    settings.write_text(json.dumps({"state": "IL", "markets": list(markets)}))
    if sources is None:
        sources = [full("MISO queue", "MISO", 4000, "MISO"), full("PJM serial", "PJM", 9000, "PJM serial"),
                   full("PJM cycle", "PJM", 1800, "PJM cycle")]
    data = {"generated": generated, "sources": sources, "entries": ENTRIES,
            "needs_answer": [q.entry_key(e) for e in q.needs_answer(ENTRIES)]}
    (batch / "harvest" / "queues.json").write_text(json.dumps(data))
    (batch / "coverage.json").write_text(json.dumps({"queues": answers or {}}))
    lanes = {"newplants": [{"record_id": r} for r in newplants],
             "monitor": [{"record_id": r} for r in monitor]}
    return batch, lanes, settings


GOOD = {
    "PJM C01-2036": {"decision": "add", "record_id": "us-il:new:marquis-solar-power-station"},
    "PJM AD2-194": {"decision": "already_in_gem", "plant_id": "L1"},
    "MISO J4443": {"decision": "fuel_not_published",
                   "evidence": "Ameren Illinois and Illinois Commerce Commission filings searched, no gas project at this point."},
}


def run(tmp_path, **kw):
    batch, lanes, settings = setup(tmp_path, **kw)
    return gate_queues(INDEX, lanes, batch, today=TODAY, settings=settings)


def test_needs_answer_picks_live_gas_at_threshold():
    keys = [q.entry_key(e) for e in q.needs_answer(ENTRIES)]
    assert keys == ["PJM C01-2036", "PJM AD2-194", "MISO J4443"]


def test_all_answered_passes(tmp_path):
    out, info = run(tmp_path, answers=GOOD, newplants=["us-il:new:marquis-solar-power-station"])
    assert out == []
    assert "requests needing an answer: 3 of 7 entries" in info


def test_missing_answer_fails(tmp_path):
    answers = {k: v for k, v in GOOD.items() if k != "PJM C01-2036"}
    out, _ = run(tmp_path, answers=answers, newplants=["us-il:new:marquis-solar-power-station"])
    assert [o[0] for o in out] == ["queues:PJM C01-2036"]


def test_add_must_name_a_new_plant_record(tmp_path):
    out, _ = run(tmp_path, answers=GOOD)
    assert any("add must name" in r for _, r in out)


def test_watch_needs_monitor_record(tmp_path):
    answers = dict(GOOD, **{"PJM C01-2036": {"decision": "watch", "record_id": "us-il:mon:x"}})
    out, _ = run(tmp_path, answers=answers)
    assert any("watch must name" in r for _, r in out)
    out, _ = run(tmp_path / "b", answers=answers, monitor=["us-il:mon:x"])
    assert out == []


def test_fuel_not_published_only_for_hidden_fuel(tmp_path):
    answers = dict(GOOD, **{"PJM C01-2036": {"decision": "fuel_not_published", "evidence": "x" * 50}})
    out, _ = run(tmp_path, answers=answers)
    assert any("only for a request whose fuel" in r for _, r in out)


def test_close_needs_evidence(tmp_path):
    answers = dict(GOOD, **{"MISO J4443": {"decision": "not_gas_or_oil", "evidence": "solar"}})
    out, _ = run(tmp_path, answers=answers, newplants=["us-il:new:marquis-solar-power-station"])
    assert [r for _, r in out] == ["not_gas_or_oil needs `evidence` saying what was read and what it showed"]


def test_stale_file_fails(tmp_path):
    out, _ = run(tmp_path, answers=GOOD, generated="2026-10-01",
                 newplants=["us-il:new:marquis-solar-power-station"])
    assert any("more than 7 days old" in r for _, r in out)


def test_short_and_unreached_sources_fail(tmp_path):
    sources = [full("MISO queue", "MISO", 300, "MISO"),
               q.source_record("PJM", "PJM", "u", "NOT REACHED: HTTP 403")]
    out, _ = run(tmp_path, answers=GOOD, sources=sources, newplants=["us-il:new:marquis-solar-power-station"])
    reasons = " ".join(r for _, r in out)
    assert "only 300 rows" in reasons and "NOT REACHED" in reasons


def test_market_with_no_reader_needs_hand_answer(tmp_path):
    sources = [full("SPP", "SPP", 1000, "SPP"),
               q.source_record("ERCOT", "ERCOT", "", "NO READER: read it by hand")]
    out, _ = run(tmp_path, answers=GOOD, sources=sources, markets=("SPP", "ERCOT"),
                 newplants=["us-il:new:marquis-solar-power-station"])
    assert [o[0] for o in out] == ["ERCOT"]
    answers = dict(GOOD, **{"market ERCOT": {"decision": "read_by_hand",
                                             "evidence": "ERCOT GIS report for October 2026 read, two gas requests found."}})
    out, _ = run(tmp_path / "b", answers=answers, sources=sources, markets=("SPP", "ERCOT"),
                 newplants=["us-il:new:marquis-solar-power-station"])
    assert out == []


def test_market_missing_from_file_fails(tmp_path):
    out, _ = run(tmp_path, answers=GOOD, markets=("MISO", "PJM", "SPP"),
                 newplants=["us-il:new:marquis-solar-power-station"])
    assert [o[0] for o in out] == ["market SPP"]


def test_older_file_and_narrow_batch(tmp_path):
    batch, lanes, settings = setup(tmp_path)
    data = json.loads((batch / "harvest" / "queues.json").read_text())
    del data["needs_answer"]
    (batch / "harvest" / "queues.json").write_text(json.dumps(data))
    out, _ = gate_queues(INDEX, lanes, batch, today=TODAY, settings=settings)
    assert "older script" in out[0][1]
    out, info = gate_queues(dict(INDEX, focus="data_centers"), lanes, batch, today=TODAY, settings=settings)
    assert out == [] and info[0].startswith("skipped")
    country = {"where": {"kind": "country", "name": "Poland", "country": "Poland"}, "plants": []}
    out, info = gate_queues(country, lanes, batch, today=TODAY, settings=settings)
    assert out == [] and info[0].startswith("skipped")


def test_source_record_flags_short_download():
    s = q.source_record("MISO", "MISO", "u", "h", rows=100, state_rows=1, entries=[], floor="MISO")
    assert s["reached"] and s["short"] and s["min_rows"] == q.MIN_ROWS["MISO"]
    assert "SHORT" in q.completeness_line(s)
    s = q.source_record("ERCOT", "ERCOT", "", "NO READER: x")
    assert not s["reached"] and q.completeness_line(s) == "ERCOT: NO READER: x"


def test_miso_size_falls_back_to_study_mw():
    assert q.miso_mw({"summerNetMW": 0.0, "dp1NrisMw": 180.0, "dp2NrisMw": 180.0}) == 180.0
    assert q.miso_mw({"summerNetMW": 300.0}) == 300.0
    assert q.miso_mw({"summerNetMW": 0.0}) is None
    assert [q.entry_key(e) for e in q.needs_answer([entry("MISO", "J1", mw=0.0)])] == ["MISO J1"]

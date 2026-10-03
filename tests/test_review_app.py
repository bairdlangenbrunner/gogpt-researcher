"""Tests for the GOGPT review app (review_app/) and the build script's --decisions consumer.

Everything runs on a throwaway staging dir under tmp_path: no real batch, no network, and
nothing that could touch the GEM database (there is no code path for that anyway)."""
import json
import sys
import threading
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from review_app import review_data, server, store  # noqa: E402
import build_review_package as brp  # noqa: E402


def envelope(lane, records):
    return {"meta": {"lane": lane, "scope": {"country": "United States", "state": "Maryland", "quarter": "q4-2026"},
                     "generated": "2026-10-02T12:00:00-04:00", "counts": {"records": len(records)}},
            "records": records}


EIA = "https://www.eia.gov/electricity/data/eia860m/xls/august_generator2026.xlsx"
PR = "https://www.example.com/press/2026-05-18-brandywine"


def write_staging(d):
    """A small batch: a fill, a change on Status with one publisher, a plant-wide re-verified
    value, one concern, one monitor item with no GEM plant id."""
    d.mkdir(parents=True)
    updates = [
        {"record_id": "L1:G1:start-year", "gem_plant_id": "L1", "plant_name": "Brandywine power facility",
         "gem_unit_id": "G1", "unit_name": "F701", "country": "United States",
         "fields": {"Start year": "1996"}, "refs": {"Start Year Data Source": [EIA]},
         "verifications": [{"url": EIA, "ok": True, "contains_value": True, "name_found": True, "note": ""}],
         "current": {"Start year": ""}, "tier": "high", "verdict": "fill",
         "researcher_notes": "The EIA table for August 2026 lists 1996.", "action": "Type 1996 in Start year."},
        {"record_id": "L1:G1:status", "gem_plant_id": "L1", "plant_name": "Brandywine power facility",
         "gem_unit_id": "G1", "unit_name": "F701", "country": "United States",
         "fields": {"Status": "mothballed"}, "refs": {"Status Data Source": [PR]},
         "verifications": [{"url": PR, "ok": True, "contains_value": True, "name_found": True, "note": ""}],
         "current": {"Status": "operating"}, "tier": "medium", "verdict": "change"},
        {"record_id": "L1:G1:latitude", "gem_plant_id": "L1", "plant_name": "Brandywine power facility",
         "gem_unit_id": "G1", "unit_name": "F701", "country": "United States",
         "fields": {"Latitude": "38.70"}, "refs": {"Location Data Source": [EIA]},
         "verifications": [{"url": EIA, "ok": True, "contains_value": True, "name_found": True, "note": ""}],
         "current": {"Latitude": "38.70"}, "tier": "medium", "verdict": "match", "reverified": True,
         "applies_to_all_units": True, "sibling_unit_ids": ["G2"], "sibling_current": {"G2": "38.70"}},
    ]
    qa = [{"record_id": "L1:G1:qa-unverified-value-1", "gem_plant_id": "L1", "plant_name": "Brandywine power facility",
           "gem_unit_id": "G1", "unit_name": "F701", "country": "United States", "fields": {},
           "concern_type": "unverified_value", "recommendation": "Check the capacity against the EIA table.",
           "researcher_notes": "The capacity on the press release differs from the export."}]
    monitor = [{"record_id": "us-md:plant:monitor-1", "gem_plant_id": "", "plant_name": "Chesapeake repowering (Acme)",
                "country": "United States", "fields": {}, "item": "new plant candidate", "recheck_by": "2027-01",
                "refs": {"links": [PR]}, "researcher_notes": "Announced, no permit filed."}]
    (d / "staged_updates.json").write_text(json.dumps(envelope("updates", updates)))
    (d / "staged_qa.json").write_text(json.dumps(envelope("qa", qa)))
    (d / "staged_monitor.json").write_text(json.dumps(envelope("monitor", monitor)))
    return d


@pytest.fixture
def staging(tmp_path):
    return write_staging(tmp_path / "us-md" / "staging")


@pytest.fixture
def data(staging, tmp_path):
    csv = tmp_path / "export.csv"
    csv.write_text("GEM unit ID,GEM location ID,Start year,Start Year Data Source,Status,Status Data Source,Latitude,Location Data Source\n"
                   "G1,L1,,https://old.example.com/a,operating,,38.70,\n")
    return review_data.build([staging], export_csv=csv)


# ---- initials -------------------------------------------------------------------------

@pytest.mark.parametrize("who,want", [("Baird Langenbrunner", "BL"), ("baird.langenbrunner@globalenergymonitor.org", "BL"),
                                      ("amalia", "A"), ("BL", "BL"), ("", "")])
def test_initials(who, want):
    assert store.initials(who) == want


# ---- dataset ---------------------------------------------------------------------------

def test_dataset_shape(data, staging):
    assert data["scope"]["states"] == ["Maryland"] and data["scope"]["quarter"] == "q4-2026"
    assert data["dirs"] == [str(staging)]          # outside the repo: an absolute label
    plants = {p["pid"]: p for p in data["plants"]}
    assert set(plants) == {"L1", "new:chesapeake-repowering-acme"}
    p = plants["L1"]
    assert [u["gem_unit_id"] for u in p["units"]] == ["G1"]
    lines = {l["record_id"]: l for l in p["lines"]}
    assert lines["L1:G1:start-year"]["kind"] == "fill" and lines["L1:G1:start-year"]["severity"] == "major"
    assert lines["L1:G1:start-year"]["default"] == "accept"
    assert lines["L1:G1:start-year"]["current_ref"] == ["https://old.example.com/a"]   # from the export csv
    assert lines["L1:G1:start-year"]["proposed_refs"] == [EIA]
    assert lines["L1:G1:start-year"]["verifications"][EIA]["contains_value"] is True
    st = lines["L1:G1:status"]
    assert st["kind"] == "change" and st["publishers"] == 1 and st["default"] == "hold"
    pw = lines["L1:G1:latitude"]
    assert pw["kind"] == "plant" and pw["reverified"] and pw["severity"] == "minor"
    assert pw["sibling_unit_ids"] == ["G2"]
    items = {it["record_id"]: it for it in p["items"]}
    assert items["L1:G1:qa-unverified-value-1"]["kind"] == "concern"
    assert items["L1:G1:qa-unverified-value-1"]["concern_type"] == "unverified_value"
    cand = plants["new:chesapeake-repowering-acme"]
    assert cand["items"][0]["kind"] == "monitor" and cand["items"][0]["links"] == [PR]
    assert all(l["key"] == f"{staging}::{l['record_id']}" for l in p["lines"])


def test_severity_rule():
    assert review_data.line_kind({"verdict": "match"}) == "reverified"
    assert review_data.line_kind({"delete": True}) == "delete"
    assert review_data.line_kind({"applies_to_all_units": True}) == "plant"
    assert review_data.line_kind({"verdict": "change"}) == "change"
    assert review_data.line_kind({}) == "fill"


# ---- store -----------------------------------------------------------------------------

def test_store_round_trip(data, staging):
    key = f"{staging}::L1:G1:start-year"
    dirs = store.dir_paths(data)
    saved = store.decide([{"key": key, "decision": "accept"}], data, "BL", dirs)
    assert len(saved) == 1
    r = saved[0]
    assert {"key", "dir", "pid", "record_id", "column", "kind", "decision", "suggested_value", "note",
            "reviewer", "ts", "undecided"} <= set(r)
    assert r["decision"] == "accept" and r["reviewer"] == "BL" and r["undecided"] is False
    log = staging / "review_log.jsonl"
    assert log.exists() and len(log.read_text().splitlines()) == 1
    derived = json.loads((staging / "review_decisions.json").read_text())
    assert derived["decisions"][key]["decision"] == "accept"
    # suggest needs a value or a note
    with pytest.raises(store.Invalid):
        store.decide([{"key": key, "decision": "suggest"}], data, "BL", dirs)
    store.decide([{"key": key, "decision": "suggest", "suggested_value": "1997", "note": "typo"}], data, "BL", dirs)
    store.overlay(data, dirs)
    line = next(l for p in data["plants"] for l in p["lines"] if l["key"] == key)
    assert line["decision"] == "suggest" and line["suggested_value"] == "1997" and line["reviewed"] is True
    # undo: the log grows, the overlay clears
    store.decide([{"key": key, "undo": True}], data, "BL", dirs)
    assert len(log.read_text().splitlines()) == 3
    store.overlay(data, dirs)
    assert line["decision"] is None and line["reviewed"] is False
    # unknown key, bad decision
    with pytest.raises(store.Invalid):
        store.decide([{"key": "nope", "decision": "accept"}], data, "BL", dirs)
    with pytest.raises(store.Invalid):
        store.decide([{"key": key, "decision": "maybe"}], data, "BL", dirs)


def test_store_items(data, staging):
    key = f"{staging}::L1:G1:qa-unverified-value-1"
    dirs = store.dir_paths(data)
    saved = store.record_items([{"key": key, "call": "confirmed", "note": "stands"}], data, "BL", dirs)
    assert saved[0]["call"] == "confirmed" and saved[0]["kind"] == "concern"
    with pytest.raises(store.Invalid):
        store.record_items([{"key": key, "call": "noted"}], data, "BL", dirs)   # not in the concern vocabulary
    store.overlay(data, dirs)
    it = next(i for p in data["plants"] for i in p["items"] if i["key"] == key)
    assert it["call"] == "confirmed" and it["call_note"] == "stands" and it["decided_by"] == "BL"


# ---- server ----------------------------------------------------------------------------

def test_server_round_trip(data, staging, tmp_path):
    path = tmp_path / "review_data.json"
    path.write_text(json.dumps(data))
    app = server.App(path, "Baird Langenbrunner")
    srv = server.make_server(app, port=0)
    port = srv.server_address[1]
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    base = f"http://127.0.0.1:{port}"

    def call(path, body=None):
        req = urllib.request.Request(base + path, data=json.dumps(body).encode() if body is not None else None,
                                     headers={"Content-Type": "application/json"} if body is not None else {})
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read().decode())
    try:
        st, who = call("/api/whoami")
        assert st == 200 and who == {"reviewer": "BL", "caps": {"decide": True}}
        key = f"{staging}::L1:G1:status"
        st, body = call("/api/decide", [{"key": key, "decision": "hold"}])
        assert st == 200 and body["saved"][0]["decision"] == "hold" and body["saved"][0]["reviewer"] == "BL"
        st, body = call("/api/decide", [{"key": "nope", "decision": "hold"}])
        assert st == 400 and "unknown key" in body["error"]
        st, body = call("/api/item", [{"key": f"{staging}::L1:G1:qa-unverified-value-1", "call": "needs_research"}])
        assert st == 200 and body["saved"][0]["call"] == "needs_research"
        st, d = call("/api/data")
        line = next(l for p in d["plants"] for l in p["lines"] if l["key"] == key)
        assert line["decision"] == "hold" and line["decided_by"] == "BL"
        with urllib.request.urlopen(base + "/") as r:
            assert r.status == 200 and b"GOGPT reviewer" in r.read()
    finally:
        srv.shutdown()
        srv.server_close()
    assert (staging / "review_log.jsonl").exists()


def test_server_refuses_non_loopback():
    with pytest.raises(ValueError):
        server.ensure_loopback("0.0.0.0")


# ---- build script: --decisions -----------------------------------------------------------

def test_build_apply_decisions(data, staging):
    dirs = store.dir_paths(data)
    k = lambda rid: f"{staging}::{rid}"
    store.decide([{"key": k("L1:G1:start-year"), "decision": "accept"},
                  {"key": k("L1:G1:status"), "decision": "reject", "note": "one source"}], data, "BL", dirs)
    store.decide([{"key": k("L1:G1:latitude"), "decision": "suggest", "suggested_value": "38.71"}], data, "BL", dirs)
    store.record_items([{"key": k("L1:G1:qa-unverified-value-1"), "call": "confirmed"}], data, "BL", dirs)
    lanes = brp.load_lanes(staging)
    assert brp.validate(lanes) == []
    decisions = brp.load_decisions(staging)
    kept, left_out, counts = brp.apply_decisions(lanes, decisions)
    assert counts == {"accept": 1, "hold": 0, "reject": 1, "suggest": 1, "undecided": 0}
    assert [r["record_id"] for r in kept["updates"]] == ["L1:G1:start-year"]
    assert sorted(r["record_id"] for _, r, _ in left_out) == ["L1:G1:latitude", "L1:G1:status"]
    assert kept["qa"][0]["review_call"]["call"] == "confirmed"
    assert len(kept["monitor"]) == 1 and "review_call" not in kept["monitor"][0]
    texts = {r["record_id"]: brp.describe_decision(d) for _, r, d in left_out}
    assert texts["L1:G1:status"].startswith("rejected by BL on 20") and texts["L1:G1:status"].endswith(". one source")
    assert "suggested by BL" in texts["L1:G1:latitude"] and texts["L1:G1:latitude"].endswith(": 38.71")
    assert brp.describe_decision(None) == "not decided yet in the review app"
    # the checklist carries only the accepted edit
    rows = brp.checklist_rows(kept)
    assert len(rows) == 1 and rows[0][5] == "Start year" and rows[0][7] == "1996"


def test_build_no_log(staging):
    assert brp.load_decisions(staging) is None


# ---- single-file page: build_static.py, static_store.js, import_log.py ---------------------

from review_app import build_static, import_log  # noqa: E402
import shutil  # noqa: E402
import subprocess  # noqa: E402

NODE = shutil.which("node")

NODE_DRIVER = r"""
const fs = require("fs"), vm = require("vm");
const [, , cfgPath, jsPath] = process.argv;
const mem = {};
global.window = global;
global.localStorage = {getItem: k => (k in mem ? mem[k] : null), setItem: (k, v) => { mem[k] = v; }};
global.Intl = Intl;
window.REVIEW_STATIC = JSON.parse(fs.readFileSync(cfgPath, "utf8"));
vm.runInThisContext(fs.readFileSync(jsPath, "utf8"));
const S = window.StaticStore;
(async () => {
  const d0 = await S.load();
  const line = d0.plants[0].lines.find(l => l.record_id === "L1:G1:start-year");
  const status = d0.plants[0].lines.find(l => l.record_id === "L1:G1:status");
  const item = d0.plants[0].items.find(i => i.record_id === "L1:G1:qa-unverified-value-1");
  const out = {who: await S.whoami(), caps: S.caps, before: line.decision};
  await S.decide([{key: line.key, decision: "accept"}]);
  await S.decide([{key: status.key, decision: "suggest", suggested_value: "shelved", note: "one source"}]);
  await S.decide([{key: status.key, undo: true}]);
  await S.item([{key: item.key, call: "confirmed"}]);
  try { await S.decide([{key: item.key, decision: "accept"}]); out.itemAsLine = "allowed"; } catch (e) { out.itemAsLine = e.message; }
  try { await S.decide([{key: line.key, decision: "maybe"}]); out.badDecision = "allowed"; } catch (e) { out.badDecision = e.message; }
  const d1 = await S.load();   // a reload lays the browser log back over the data
  const l1 = d1.plants[0].lines.find(l => l.record_id === "L1:G1:start-year");
  const s1 = d1.plants[0].lines.find(l => l.record_id === "L1:G1:status");
  const i1 = d1.plants[0].items.find(i => i.record_id === "L1:G1:qa-unverified-value-1");
  out.after = {line: [l1.decision, l1.reviewed, l1.decided_by], status: [s1.decision, s1.reviewed], item: [i1.call, i1.reviewed]};
  out.log = S.log();
  out.stored = Object.keys(mem).length;
  process.stdout.write(JSON.stringify(out));
})();
"""


def test_static_page_renders(data):
    html = build_static.render(data, store.initials("Amalia Llano"))
    assert "<style>" in html and 'href="style.css"' not in html and 'src="app.js"' not in html
    assert "window.REVIEW_STATIC = " in html and "window.StaticStore" in html
    cfg = json.loads(html.split("window.REVIEW_STATIC = ", 1)[1].split(";</script>", 1)[0].replace("<\\/", "</"))
    assert cfg["reviewer"] == "AL" and len(cfg["data"]["plants"]) == len(data["plants"])
    assert 'id="export-btn"' in html


@pytest.mark.skipif(not NODE, reason="node not installed")
def test_static_store_round_trip(data, staging, tmp_path):
    cfg = tmp_path / "cfg.json"
    cfg.write_text(json.dumps({"reviewer": "AL", "data": data}))
    driver = tmp_path / "drive.js"
    driver.write_text(NODE_DRIVER)
    r = subprocess.run([NODE, str(driver), str(cfg), str(ROOT / "review_app" / "web" / "static_store.js")],
                       capture_output=True, text=True, check=True)
    out = json.loads(r.stdout)
    assert out["who"] == "AL" and out["caps"] == {"decide": True} and out["before"] is None
    assert out["itemAsLine"].endswith("is an item, not a line")
    assert "not one of accept, hold, reject, suggest" in out["badDecision"]
    assert out["after"] == {"line": ["accept", True, "AL"], "status": [None, False], "item": ["confirmed", True]}
    assert out["stored"] == 1
    log = out["log"]
    assert [r.get("decision") or r.get("call") for r in log] == ["accept", "suggest", "hold", "confirmed"]
    assert log[2]["undecided"] is True and log[2]["decision"] == "hold"      # an undo keeps the line's default
    assert all(r["reviewer"] == "AL" and r["ts"][:4] == "2026" and r["dir"] == str(staging) for r in log)
    # the download goes through import_log.py into the staging dir's log, exactly like the server
    f = tmp_path / "review_log_us-md_AL.jsonl"
    f.write_text("".join(json.dumps(r) + "\n" for r in log))
    import_log.main([str(f)])
    assert len(store.read_log(staging)) == 4 and (staging / store.DERIVED_NAME).exists()
    decisions = brp.load_decisions(staging)
    assert decisions["L1:G1:start-year"]["decision"] == "accept" and decisions["L1:G1:status"]["undecided"] is True
    # importing the same download again appends nothing
    planned = import_log.plan(log)
    assert [len(v[1]) for v in planned.values()] == [0] and [len(v[2]) for v in planned.values()] == [4]
    # a record the batch no longer has stops the import before anything is written
    bad = dict(log[0], record_id="L1:G1:gone", key=f"{staging}::L1:G1:gone")
    with pytest.raises(SystemExit, match="not in the staged lane files"):
        import_log.plan([bad])

"""The decision ledger (review_app/ledger.py): every decision lands in the Google store FIRST, in the
`log` tab's column shape, then in the staging-dir sidecars; import_log.py brings the artifact page's
records in the same way. A fake gws stands in for the sheet; nothing here touches Google."""
import json
import re
import threading
import urllib.error
import urllib.request
import uuid
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
import sys  # noqa: E402
for p in (ROOT, ROOT / "scripts", ROOT / "review_app"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import import_log  # noqa: E402
import ledger  # noqa: E402
import pull  # noqa: E402
import review_data  # noqa: E402
import server  # noqa: E402
import store  # noqa: E402
from test_review_app import write_staging  # noqa: E402

ME = "baird.langenbrunner@globalenergymonitor.org"
AL = "amalia.llano@globalenergymonitor.org"
SHEET = "store-sheet"


class FakeStore:
    """The store spreadsheet's `log` tab as gws would serve it: rows (header first) + every call."""

    def __init__(self, fail=None, clobber=0, email=ME):
        self.rows = [list(ledger.COLS)]
        self.calls = []
        self.fail = fail            # an exception class to raise on `append`
        self.clobber = clobber      # how many appends another writer "overwrites" (race simulation)
        self.email = email

    def __call__(self, profile, *args, parse=True):
        self.calls.append((profile, args))
        if args[:2] == ("drive", "about"):
            return {"user": {"emailAddress": self.email}}
        verb = args[3]
        params = json.loads(args[args.index("--params") + 1])
        if verb == "append":
            assert profile == pull.WRITE_PROFILE
            assert params["valueInputOption"] == "RAW" and params["range"] == "log!A:U"
            if self.fail:
                raise self.fail("boom")
            values = json.loads(args[args.index("--json") + 1])["values"]
            first = len(self.rows) + 1
            for v in values:
                assert len(v) == len(ledger.COLS) and all(isinstance(x, str) for x in v)
                self.rows.append(list(v))
            if self.clobber:
                self.clobber -= 1
                for r in self.rows[first - 1:]:
                    r[ledger.COLS.index("id")] = "someone-else"
            return {"updates": {"updatedRange": f"log!A{first}:U{first + len(values) - 1}"}}
        if verb == "get":
            assert profile == pull.READ_PROFILE
            m = re.match(r"log!([A-Z])(\d+):([A-Z])(\d+)$", params["range"])
            if m:
                c = ord(m.group(1)) - 65
                return {"values": [[r[c]] for r in self.rows[int(m.group(2)) - 1:int(m.group(4))]]}
            if params["range"] == "log!1:1":
                return {"values": [self.rows[0]]}
            m = re.match(r"log!([A-Z])1:([A-Z])$", params["range"])
            c = ord(m.group(1)) - 65
            return {"values": [[r[c]] for r in self.rows]}
        raise AssertionError(args)

    def records(self):
        j = ledger.COLS.index("json")
        return [json.loads(r[j]) for r in self.rows[1:]]

    def json_cells(self):
        j = ledger.COLS.index("json")
        return [r[j] for r in self.rows]


@pytest.fixture
def scope(tmp_path):
    """A small batch under <tmp>/batches/us-md/staging, built as a dataset, its dirs keyed by label."""
    staging = write_staging(tmp_path / "batches" / "us-md" / "staging")
    csv = tmp_path / "export.csv"
    csv.write_text("GEM unit ID,GEM location ID,Start year,Start Year Data Source,Status,Status Data Source,Latitude,Location Data Source\n"
                   "G1,L1,,https://old.example.com/a,operating,,38.70,\n")
    data = review_data.build([staging], export_csv=csv)
    return {"staging": staging, "csv": csv, "dataset": data, "dirs": store.dir_paths(data, tmp_path), "root": tmp_path}


def line(data, record_id):
    for p in data["plants"]:
        for l in p["lines"]:
            if l["record_id"] == record_id:
                return l
    raise AssertionError(record_id)


def item(data, record_id):
    for p in data["plants"]:
        for i in p["items"]:
            if i["record_id"] == record_id:
                return i
    raise AssertionError(record_id)


def logrecs(d):
    return [json.loads(x) for x in (Path(d) / store.LOG_NAME).read_text().splitlines()]


def made(fake, data, origin="local"):
    return ledger.Ledger(SHEET, *ledger.scope_of(data), origin, reviewer_email=ME, gws=fake)


# ---- the row shape ------------------------------------------------------------------------------

def test_cols_match_the_sheet_header_and_the_record_shape():
    assert len(ledger.COLS) == 21 and ledger.COLS[-1] == "json" and ledger.COLS[0] == "ts"
    assert {"record_id", "column", "reference", "flag", "on", "call", "decision"} <= set(ledger.COLS)


def test_row_for_mirrors_append_and_cell():
    rec = {"key": "batches/x::L1:G1:status", "dir": "batches/x", "pid": "L1", "record_id": "L1:G1:status", "column": "Status",
           "kind": "change", "decision": "accept", "suggested_value": "", "reference": "", "note": "=SUM(1)", "reviewer": ME,
           "ts": "t", "undecided": True, "batch": "b", "snapshot": "s", "id": "i", "scope": "us-md"}
    row = ledger.row_for(rec)
    assert len(row) == len(ledger.COLS)
    got = dict(zip(ledger.COLS, row))
    assert got["rec"] == "line" and got["undecided"] == "undone" and got["note"] == "'=SUM(1)" and got["on"] == ""
    assert got["record_id"] == "L1:G1:status" and got["column"] == "Status" and got["call"] == "" and json.loads(got["json"]) == rec
    it = dict(zip(ledger.COLS, ledger.row_for({"key": "k", "call": "confirmed", "kind": "concern", "record_id": None, "note": "x" * 2500})))
    assert it["rec"] == "item" and it["record_id"] == "" and it["decision"] == "" and len(it["note"]) == 2001
    fl = dict(zip(ledger.COLS, ledger.row_for({"key": "pm::k", "flag": "pm", "on": False, "kind": "plant"})))
    assert fl["rec"] == "flag" and fl["on"] == "off" and fl["flag"] == "pm"
    with pytest.raises(ledger.StoreError):
        ledger.row_for({"key": "k", "note": "x" * 50000})


def test_stamp_fields_fills_what_is_missing_and_keeps_an_id():
    recs = [{"key": "a", "ts": None}, {"key": "b", "id": "page-id", "snapshot": "older", "ts": "2001"}]
    ledger.stamp_fields(recs, "us-md", "snap", "artifact")
    a, b = recs
    assert len(a["id"]) == 36 and b["id"] == "page-id" and a["batch"] == b["batch"]
    assert (a["scope"], a["snapshot"], a["origin"]) == ("us-md", "snap", "artifact")
    assert b["snapshot"] == "older" and b["ts"] == "2001" and a["ts"]
    with pytest.raises(ValueError):
        ledger.stamp_fields([{"key": "c"}], "s", "", "typo")


def test_scope_of_joins_dir_labels():
    d = {"dirs": ["batches/us-md/staging", "batches/us-ny/staging", "batches/us-md/staging-discovery"], "built": "2026-10-08T09:00:00-04:00"}
    assert ledger.scope_of(d) == ("us-md+us-ny+us-md-discovery", "2026-10-08T09:00:00-04:00")
    assert ledger.scope_of({"dirs": ["/abs/batches/germany/staging"]}) == ("germany", "")


# ---- append: write, verify, retry ---------------------------------------------------------------

def test_append_writes_rows_and_verifies_ids():
    fake = FakeStore()
    recs = [{"key": "k1", "id": "id1", "ts": "t"}, {"key": "k2", "id": "id2", "ts": "t"}]
    assert ledger.append(recs, SHEET, gws=fake) == (2, 3)
    assert [r["row"] for r in recs] == [2, 3] and [r["key"] for r in fake.records()] == ["k1", "k2"]
    assert [a[3] for _, a in fake.calls] == ["append", "get"]


def test_append_retries_once_when_another_writer_lands_on_the_rows_then_refuses():
    fake = FakeStore(clobber=1)
    assert ledger.append([{"key": "k", "id": "i", "ts": "t"}], SHEET, gws=fake) == (3, 3)
    assert [a[3] for _, a in fake.calls] == ["append", "get", "append", "get"]
    with pytest.raises(ledger.StoreError, match="another writer"):
        ledger.append([{"key": "k", "id": "j", "ts": "t"}], SHEET, gws=FakeStore(clobber=5))


def test_append_turns_a_gws_failure_into_a_store_error():
    with pytest.raises(ledger.StoreError, match="could not be written"):
        ledger.append([{"key": "k", "id": "i"}], SHEET, gws=FakeStore(fail=pull.GwsError))


# ---- the sink: store first, sidecars second ------------------------------------------------------

def test_decide_through_the_ledger_lands_in_store_then_sidecar(scope):
    fake = FakeStore()
    led = made(fake, scope["dataset"])
    l = line(scope["dataset"], "L1:G1:start-year")
    saved = store.decide([{"key": l["key"], "decision": "accept", "note": "ok"}], scope["dataset"], "Baird Langenbrunner",
                         dirs=scope["dirs"], sink=led.sink)
    assert len(saved) == 1 and saved[0]["row"] == 2 and led.written == 1 and led.last_row == 2
    srec = fake.records()[0]
    assert srec["reviewer"] == ME and srec["key"] == l["key"] and srec["origin"] == "local"
    assert srec["scope"] == "us-md" and srec["snapshot"] == scope["dataset"]["built"] and srec["record_id"] == "L1:G1:start-year"
    local = logrecs(scope["dirs"][l["dir"]])
    assert len(local) == 1 and local[0]["reviewer"] == "BL" and local[0]["id"] == srec["id"] and "row" not in local[0]
    assert {k: v for k, v in local[0].items() if k != "reviewer"} == {k: v for k, v in srec.items() if k not in ("reviewer", "row")}
    assert dict(zip(ledger.COLS, fake.rows[1]))["reviewer"] == ME
    store.overlay(scope["dataset"], scope["dirs"])
    assert line(scope["dataset"], "L1:G1:start-year")["decided_by"] == "BL"


def test_a_pull_of_the_same_store_rows_writes_nothing_twice(scope):
    fake = FakeStore()
    led = made(fake, scope["dataset"])
    l = line(scope["dataset"], "L1:G1:start-year")
    store.decide([{"key": l["key"], "decision": "reject"}], scope["dataset"], "BL", dirs=scope["dirs"], sink=led.sink)
    res = pull.pull({"store_sheet_id": SHEET}, root=scope["root"], reader=lambda s: fake.json_cells())
    assert res["rows"] == 1 and res["new"] == 0 and len(logrecs(scope["dirs"][l["dir"]])) == 1


def test_store_failure_refuses_the_decision_and_writes_no_sidecar(scope):
    led = made(FakeStore(fail=pull.GwsError), scope["dataset"])
    l = line(scope["dataset"], "L1:G1:start-year")
    with pytest.raises(ledger.StoreError):
        store.decide([{"key": l["key"], "decision": "accept"}], scope["dataset"], "BL", dirs=scope["dirs"], sink=led.sink)
    assert not (scope["dirs"][l["dir"]] / store.LOG_NAME).exists()
    assert not store._LOCK.locked()


def test_an_unknown_dir_is_refused_before_the_store_is_touched(scope):
    fake = FakeStore()
    led = made(fake, scope["dataset"])
    with pytest.raises(store.Invalid):
        led.sink([{"key": "x::y", "dir": "batches/nowhere", "reviewer": "BL"}], scope["dirs"])
    assert fake.calls == []


def test_item_calls_and_flags_go_through_too(scope):
    fake = FakeStore()
    led = made(fake, scope["dataset"])
    it = item(scope["dataset"], "L1:G1:qa-unverified-value-1")
    store.record_items([{"key": it["key"], "call": "dismissed", "note": "n"}], scope["dataset"], "BL", dirs=scope["dirs"], sink=led.sink)
    store.record_flags([{"pid": "L1", "dir": it["dir"], "on": True, "note": "whole plant"}], scope["dataset"], "BL", dirs=scope["dirs"], sink=led.sink)
    recs = fake.records()
    assert recs[0]["call"] == "dismissed" and recs[0]["reviewer"] == ME and dict(zip(ledger.COLS, fake.rows[1]))["rec"] == "item"
    assert recs[1]["flag"] == "pm" and dict(zip(ledger.COLS, fake.rows[2]))["on"] == "on"
    assert [r["reviewer"] for r in logrecs(scope["dirs"][it["dir"]])] == ["BL", "BL"]


def test_to_store_restores_the_original_decider_for_a_copy():
    led = ledger.Ledger(SHEET, "s", "", "chat", reviewer_email=ME, gws=FakeStore(), emails={"id-1": AL})
    assert led.to_store({"id": "id-1", "reviewer": "AL"})["reviewer"] == AL
    assert led.to_store({"id": "fresh", "reviewer": "BL"})["reviewer"] == ME
    assert led.to_store({"id": "fresh", "reviewer": "push"})["reviewer"] == "push"


def test_backfill_brings_pre_ledger_sidecar_records_into_the_store_and_restamps_them(scope):
    fake = FakeStore()
    d = scope["staging"]
    l = line(scope["dataset"], "L1:G1:start-year")
    old = [{"key": l["key"], "dir": "batches/us-md/staging", "pid": "L1", "record_id": "L1:G1:start-year", "column": "Start year",
            "kind": "fill", "decision": "accept", "suggested_value": "", "note": "copied from a screenshot",
            "reviewer": "AL", "ts": "2026-10-05T17:51:02-04:00", "undecided": False}]
    (d / store.LOG_NAME).write_text(json.dumps(old[0]) + "\n")
    # a reviewer without an address stops the run before the store is touched
    with pytest.raises(SystemExit, match="no address for reviewer AL"):
        ledger.backfill(d, {}, SHEET, gws=fake, root=scope["root"])
    assert fake.calls == []
    # a dry run stamps nothing on disk
    plan = ledger.backfill(d, {"AL": AL}, SHEET, gws=fake, dry_run=True, root=scope["root"])
    assert len(plan) == 1 and plan[0]["id"] and fake.calls == [] and not logrecs(d)[0].get("id")
    done = ledger.backfill(d, {"AL": AL}, SHEET, gws=fake, root=scope["root"])
    assert len(done) == 1 and done[0]["row"] == 2
    srec = fake.records()[0]
    assert srec["reviewer"] == AL and srec["origin"] == "chat" and srec["scope"] == "us-md" and srec["snapshot"] == ""
    assert srec["ts"] == "2026-10-05T17:51:02-04:00" and srec["id"] == done[0]["id"] and srec["note"] == "copied from a screenshot"
    local = logrecs(d)
    assert len(local) == 1 and local[0]["reviewer"] == "AL" and local[0]["id"] == srec["id"] and "row" not in local[0]
    assert {k: v for k, v in local[0].items() if k != "reviewer"} == {k: v for k, v in srec.items() if k not in ("reviewer", "row")}
    assert json.loads((d / store.DERIVED_NAME).read_text())["decisions"][l["key"]]["id"] == srec["id"]
    # a second run has nothing to do, and a pull writes nothing twice
    assert ledger.backfill(d, {"AL": AL}, SHEET, gws=fake, root=scope["root"]) == []
    res = pull.pull({"store_sheet_id": SHEET}, root=scope["root"], reader=lambda s: fake.json_cells())
    assert res["rows"] == 1 and res["new"] == 0 and len(logrecs(d)) == 1


def test_backfill_leaves_the_sidecar_alone_when_the_store_fails(scope):
    d = scope["staging"]
    l = line(scope["dataset"], "L1:G1:start-year")
    text = json.dumps({"key": l["key"], "dir": "batches/us-md/staging", "reviewer": "AL", "decision": "accept", "ts": "2026-10-05T17:51:02-04:00"}) + "\n"
    (d / store.LOG_NAME).write_text(text)
    with pytest.raises(ledger.StoreError):
        ledger.backfill(d, {"AL": AL}, SHEET, gws=FakeStore(fail=pull.GwsError), root=scope["root"])
    assert (d / store.LOG_NAME).read_text() == text and not store._LOCK.locked()


def test_whoami_reads_the_store_account():
    assert ledger.whoami(gws=FakeStore()) == ME

    def down(profile, *a, parse=True):
        raise pull.GwsError("auth")
    assert ledger.whoami(gws=down) == ""


# ---- the server with a ledger ---------------------------------------------------------------------

def post(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def served(scope, fake):
    path = scope["root"] / "review_data.json"
    path.write_text(json.dumps(scope["dataset"]), encoding="utf-8")
    led = made(fake, scope["dataset"])
    app = server.App(path, "Baird Langenbrunner", root=scope["root"], ledger=led)
    httpd = server.make_server(app, "127.0.0.1", 0)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, f"http://127.0.0.1:{httpd.server_address[1]}", app


def test_server_decide_writes_the_store_and_reports_it(scope):
    fake = FakeStore()
    httpd, base, app = served(scope, fake)
    try:
        with urllib.request.urlopen(base + "/api/whoami") as r:
            assert json.loads(r.read())["store"] is True
        l = line(scope["dataset"], "L1:G1:start-year")
        st, body = post(base + "/api/decide", [{"key": l["key"], "decision": "accept"}])
        assert st == 200 and body["saved"][0]["row"] == 2 and fake.records()[0]["reviewer"] == ME
        assert logrecs(scope["dirs"][l["dir"]])[0]["reviewer"] == "BL"
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_server_refuses_with_502_when_the_store_is_down(scope):
    httpd, base, app = served(scope, FakeStore(fail=pull.GwsError))
    try:
        l = line(scope["dataset"], "L1:G1:start-year")
        st, body = post(base + "/api/decide", [{"key": l["key"], "decision": "accept"}])
        assert st == 502 and "nothing saved" in body["error"]
        assert not (scope["dirs"][l["dir"]] / store.LOG_NAME).exists()
        st, body = post(base + "/api/decide", [{"key": l["key"], "decision": "accept"}])      # the lock was released
        assert st == 502
    finally:
        httpd.shutdown()
        httpd.server_close()


def test_server_without_a_ledger_says_so(scope):
    path = scope["root"] / "review_data.json"
    path.write_text(json.dumps(scope["dataset"]), encoding="utf-8")
    assert server.App(path, "TR", root=scope["root"]).whoami()["store"] is False


# ---- import_log: the artifact page's records, store first ----------------------------------------

def page_records(data, staging):
    """What static_store.js would hold after four calls: an accept, a suggest then its undo, an item call, a flag."""
    l = line(data, "L1:G1:start-year")
    s = line(data, "L1:G1:status")
    it = item(data, "L1:G1:qa-unverified-value-1")
    base = {"dir": l["dir"], "pid": "L1", "reviewer": "AL", "undecided": False}
    t = "2026-10-07T10:00:0%d-04:00"
    return [
        dict(base, key=l["key"], record_id=l["record_id"], column=l["column"], kind=l["kind"], decision="accept", suggested_value="",
             reference="", note="", ts=t % 1, id="p1"),
        dict(base, key=s["key"], record_id=s["record_id"], column=s["column"], kind=s["kind"], decision="suggest", suggested_value="shelved",
             reference="", note="one source", ts=t % 2, id="p2"),
        dict(base, key=s["key"], record_id=s["record_id"], column=s["column"], kind=s["kind"], decision="hold", suggested_value="",
             reference="", note="", ts=t % 3, id="p3", undecided=True),
        dict(base, key=it["key"], record_id=it["record_id"], kind=it["kind"], call="confirmed", reference="", note="", ts=t % 4, id="p4"),
        dict(base, key="pm::" + l["key"], record_id=l["record_id"], kind=l["kind"], flag="pm", on=True, note="is 1996 right?", ts=t % 5, id="p5"),
    ]


def test_import_log_plans_and_writes_store_first(scope, tmp_path):
    recs = page_records(scope["dataset"], scope["staging"])
    f = tmp_path / "logs" / "viewer.json"
    f.parent.mkdir()
    f.write_text(json.dumps({"documents": [{"id": "logs/viewer", "data": {"reviewer": "AL", "built": scope["dataset"]["built"],
                                                                          "dirs": scope["dataset"]["dirs"], "records": recs}}]}))
    docs = import_log.read_docs(f)
    assert len(docs) == 1 and len(docs[0]["records"]) == 5
    ds, dirs = import_log.dataset([scope["staging"]], scope["csv"])
    with pytest.raises(SystemExit, match="carries no address"):
        import_log.plan(docs, ds, dirs)
    pl = import_log.plan(docs, ds, dirs, emails={"AL": AL})
    assert len(pl["new"]) == 5 and pl["dup"] == 0 and pl["stale"] == [] and pl["people"] == {"AL": AL}
    assert "AL (" + AL + "): 3 line decisions, 1 item calls, 1 flags, 1 of them undos" in import_log.report(pl)
    fake = FakeStore()
    saved = import_log.write(pl, ds, dirs, cfg={"store_sheet_id": SHEET}, gws=fake)
    assert [r["row"] for r in saved] == [2, 3, 4, 5, 6]
    srecs = fake.records()
    assert all(r["reviewer"] == AL and r["origin"] == "artifact" and r["scope"] == "us-md" for r in srecs)
    assert [r["id"] for r in srecs] == ["p1", "p2", "p3", "p4", "p5"] and srecs[0]["ts"] == recs[0]["ts"]
    local = logrecs(scope["staging"])
    assert [r["id"] for r in local] == ["p1", "p2", "p3", "p4", "p5"] and all(r["reviewer"] == "AL" for r in local)
    store.overlay(ds, dirs)
    assert line(ds, "L1:G1:start-year")["decision"] == "accept" and line(ds, "L1:G1:status")["reviewed"] is False
    assert line(ds, "L1:G1:start-year")["pm_flag"] is True
    # the same file again: every record is already in the log
    ds2, dirs2 = import_log.dataset([scope["staging"]], scope["csv"])
    pl2 = import_log.plan(docs, ds2, dirs2, emails={"AL": AL})
    assert pl2["new"] == [] and pl2["dup"] == 5
    # a later local decision on the same line supersedes an older page record
    store.decide([{"key": line(ds2, "L1:G1:start-year")["key"], "decision": "reject"}], ds2, "BL", dirs=dirs2)
    older = dict(recs[0], id="p9", ts="2026-10-07T10:00:00-04:00")
    ds3, dirs3 = import_log.dataset([scope["staging"]], scope["csv"])
    pl3 = import_log.plan([{"reviewer": "AL", "records": [older]}], ds3, dirs3, emails={"AL": AL})
    assert pl3["new"] == [] and len(pl3["stale"]) == 1


def test_import_log_derives_an_id_for_records_the_page_wrote_before_it_stamped_them(scope, tmp_path):
    recs = [{k: v for k, v in r.items() if k != "id"} for r in page_records(scope["dataset"], scope["staging"])]
    assert not any(r.get("id") for r in recs)
    ds, dirs = import_log.dataset([scope["staging"]], scope["csv"])
    pl = import_log.plan([{"reviewer": "AL", "records": [dict(r) for r in recs]}], ds, dirs, emails={"AL": AL})
    ids = [r["id"] for _, r in pl["new"]]
    assert len(ids) == 5 and len(set(ids)) == 5 and all(uuid.UUID(i).version == 5 for i in ids)
    # the same record always gets the same id, so a second import of the same file appends nothing
    fake = FakeStore()
    import_log.write(pl, ds, dirs, cfg={"store_sheet_id": SHEET}, gws=fake)
    assert [r["id"] for r in logrecs(scope["staging"])] == ids
    ds2, dirs2 = import_log.dataset([scope["staging"]], scope["csv"])
    pl2 = import_log.plan([{"reviewer": "AL", "records": [dict(r) for r in recs]}], ds2, dirs2, emails={"AL": AL})
    assert pl2["new"] == [] and pl2["dup"] == 5
    # a different call on the same line at another time is a different record
    other = dict(recs[0], ts="2026-10-07T11:00:00-04:00", decision="hold")
    assert import_log.legacy_id(other) != ids[0]
    with pytest.raises(SystemExit, match="needs key, reviewer, dir"):
        import_log.plan([{"records": [{k: v for k, v in recs[0].items() if k != "reviewer"}]}], ds2, dirs2, {"AL": AL})


def test_import_log_refuses_what_the_batch_cannot_take(scope):
    recs = page_records(scope["dataset"], scope["staging"])
    ds, dirs = import_log.dataset([scope["staging"]], scope["csv"])
    emails = {"AL": AL}
    with pytest.raises(SystemExit, match="not one of"):
        import_log.plan([{"records": [dict(recs[3], call="noted")]}], ds, dirs, emails)
    with pytest.raises(SystemExit, match="flag"):
        import_log.plan([{"records": [dict(recs[4], key=recs[0]["key"])]}], ds, dirs, emails)
    with pytest.raises(SystemExit, match="not in the current dataset"):
        import_log.plan([{"records": [dict(recs[0], key=f"{scope['staging']}::L1:G1:gone")]}], ds, dirs, emails)
    with pytest.raises(SystemExit, match="is an item"):
        import_log.plan([{"records": [dict(recs[0], key=recs[3]["key"])]}], ds, dirs, emails)
    with pytest.raises(SystemExit, match="needs key, reviewer, dir"):
        import_log.plan([{"records": [{k: v for k, v in recs[0].items() if k != "key"}]}], ds, dirs, emails)
    with pytest.raises(SystemExit, match="no usable time"):
        import_log.plan([{"records": [dict(recs[0], ts="yesterday")]}], ds, dirs, emails)
    with pytest.raises(SystemExit, match="not a person"):
        import_log.plan([{"records": [dict(recs[0], reviewer="push")]}], ds, dirs, emails)
    with pytest.raises(SystemExit, match="staging dir"):
        import_log.plan([{"records": [dict(recs[0], dir="batches/elsewhere")]}], ds, dirs, emails)


def test_import_log_store_failure_writes_no_sidecar(scope):
    recs = page_records(scope["dataset"], scope["staging"])
    ds, dirs = import_log.dataset([scope["staging"]], scope["csv"])
    pl = import_log.plan([{"reviewer": "AL", "records": recs}], ds, dirs, emails={"AL": AL})
    with pytest.raises(ledger.StoreError):
        import_log.write(pl, ds, dirs, cfg={"store_sheet_id": SHEET}, gws=FakeStore(fail=pull.GwsError))
    assert not (scope["staging"] / store.LOG_NAME).exists()
    with pytest.raises(SystemExit, match="no store configured"):
        import_log.write(pl, ds, dirs, cfg={}, gws=FakeStore())


def test_import_log_main_dry_run(scope, tmp_path, capsys):
    recs = page_records(scope["dataset"], scope["staging"])
    f = tmp_path / "download.json"
    f.write_text(json.dumps({"reviewer": "AL", "records": recs}))
    assert import_log.main([str(f), "--dirs", str(scope["staging"]), "--export-csv", str(scope["csv"]),
                            "--reviewer", AL, "--dry-run"]) == 0
    out = capsys.readouterr().out
    assert "5 new, 0 already in the log" in out and "dry run: nothing written" in out
    assert not (scope["staging"] / store.LOG_NAME).exists()

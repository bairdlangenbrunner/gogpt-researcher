"""review_app/pull.py mirrors the Google decision store into the staging dirs. The store is a list
of cell texts handed in through `reader`; nothing here calls gws."""
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "scripts", ROOT / "review_app"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import pull  # noqa: E402
import review_data  # noqa: E402
import store  # noqa: E402
from test_review_app import write_staging  # noqa: E402

AL = "amalia.llano@globalenergymonitor.org"


@pytest.fixture
def scope(tmp_path):
    staging = write_staging(tmp_path / "batches" / "us-md" / "staging")
    csv = tmp_path / "export.csv"
    csv.write_text("GEM unit ID,GEM location ID,Start year,Start Year Data Source,Status,Status Data Source,Latitude,Location Data Source\n"
                   "G1,L1,,https://old.example.com/a,operating,,38.70,\n")
    data = review_data.build([staging], export_csv=csv)
    return {"staging": staging, "dataset": data, "dirs": store.dir_paths(data, tmp_path), "root": tmp_path}


def rec(l, n, **kw):
    return dict({"key": l["key"], "dir": l["dir"], "pid": "L1", "record_id": l["record_id"], "column": l["column"],
                 "kind": l["kind"], "decision": "accept", "suggested_value": "", "reference": "", "note": "",
                 "reviewer": AL, "ts": "2099-01-01T01:00:0%d-05:00" % n,
                 "undecided": False, "id": "id%d" % n, "scope": "us-md", "batch": "b",
                 "snapshot": "s", "origin": "artifact"}, **kw)


def a_line(data):
    return next(l for p in data["plants"] for l in p["lines"] if l["record_id"] == "L1:G1:start-year")


def test_no_store_configured_is_cursor_one_and_reads_nothing():
    def boom(sheet):
        raise AssertionError("read the store with none configured")
    res = pull.pull({"store_sheet_id": ""}, reader=boom)
    assert (res["configured"], res["cursor"], res["new"]) == (False, 1, 0)
    assert "nothing to pull" in pull.report(res)
    assert pull.pull({"store_sheet_id": "x"}, reader=lambda s: [])["cursor"] == 1          # no log tab yet


def test_parse_rows_numbers_rows_and_reports_the_unreadable():
    good = {"id": "1", "key": "k", "dir": "d"}
    cells = ["json", json.dumps(good), "", "not json", json.dumps({"key": "k"}), json.dumps([1]), json.dumps(dict(good, id="2"))]
    recs, cursor, bad = pull.parse_rows(cells)
    assert [(r["id"], r["row"]) for r in recs] == [("1", 2), ("2", 7)] and cursor == 7 and bad == [4, 5, 6]
    assert pull.parse_rows(["json"]) == ([], 1, []) and pull.parse_rows([]) == ([], 1, [])


def test_mirror_appends_once_in_sheet_order_and_regenerates_the_derived_file(scope):
    l = a_line(scope["dataset"])
    cells = ["json", json.dumps(rec(l, 1, decision="hold")), json.dumps(rec(l, 2))]
    res = pull.pull({"store_sheet_id": "x"}, root=scope["root"], reader=lambda s: cells)
    assert (res["cursor"], res["rows"], res["new"], res["by_dir"]) == (3, 2, 2, {l["dir"]: 2})
    d = scope["dirs"][l["dir"]]
    log = store.read_log(d)
    assert [r["id"] for r in log] == ["id1", "id2"] and all("row" not in r for r in log)
    assert log[1] == rec(l, 2, reviewer="AL")    # as the sheet holds it, but for the initials
    assert "amalia" not in (d / "review_log.jsonl").read_text() + (d / "review_decisions.json").read_text()
    assert res["emails"] == {"id1": AL, "id2": AL}
    assert res["shared"] == {} and "SHARED" not in pull.report(res)
    derived = json.loads((d / "review_decisions.json").read_text())["decisions"]
    assert derived[l["key"]]["decision"] == "accept" and derived[l["key"]]["reviewer"] == "AL"
    cells.append(json.dumps(rec(l, 3, undecided=True)))
    res = pull.pull({"store_sheet_id": "x"}, root=scope["root"], reader=lambda s: cells)
    assert (res["cursor"], res["new"]) == (4, 1) and len(store.read_log(d)) == 3
    assert pull.pull({"store_sheet_id": "x"}, root=scope["root"], reader=lambda s: cells)["new"] == 0
    store.overlay(scope["dataset"], scope["dirs"])
    assert l["decision"] is None and l["reviewed"] is False             # the undo is the latest word


def test_dry_run_writes_nothing(scope):
    l = a_line(scope["dataset"])
    res = pull.pull({"store_sheet_id": "x"}, root=scope["root"], dry_run=True, reader=lambda s: ["json", json.dumps(rec(l, 1))])
    assert res["new"] == 1 and not (scope["dirs"][l["dir"]] / "review_log.jsonl").exists()
    assert "would append 1" in pull.report(res, dry_run=True)


def test_a_record_is_only_ever_written_under_batches(scope):
    l = a_line(scope["dataset"])
    root = scope["root"]
    (root / "elsewhere").mkdir()
    bad = ["elsewhere", "../" + root.name + "/elsewhere", "batches/us-md/staging/no-such-dir",
           "batches/../elsewhere", "/etc", "batches"]
    cells = ["json"] + [json.dumps(rec(l, i, dir=d)) for i, d in enumerate(bad)] + [json.dumps(rec(l, 9))]
    res = pull.pull({"store_sheet_id": "x"}, root=root, reader=lambda s: cells)
    assert res["new"] == 1 and set(res["skipped"]) == set(bad) and res["by_dir"] == {l["dir"]: 1}
    assert not list((root / "elsewhere").iterdir()) and "SKIPPED" in pull.report(res)


def test_two_reviewers_behind_one_set_of_initials_are_reported(scope):
    l = a_line(scope["dataset"])
    cells = ["json", json.dumps(rec(l, 1)), json.dumps(rec(l, 2, reviewer="andrea.lopez@globalenergymonitor.org")),
             json.dumps(rec(l, 3, reviewer="push"))]
    res = pull.pull({"store_sheet_id": "x"}, root=scope["root"], reader=lambda s: cells)
    assert res["shared"] == {"AL": [AL, "andrea.lopez@globalenergymonitor.org"]}
    assert "SHARED INITIALS AL stand for 2 reviewers" in pull.report(res)
    assert [r["reviewer"] for r in store.read_log(scope["dirs"][l["dir"]])] == ["AL", "AL", "push"]
    assert set(res["emails"]) == {"id1", "id2"}

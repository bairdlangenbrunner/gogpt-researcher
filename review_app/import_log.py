"""
Append a reviewer's downloaded decisions to the batch logs.

    python review_app/import_log.py review_log_us-md+us-ny_AL_20261003_0915_ET.jsonl [--dry-run]

The file is what the single-file review page (build_static.py) downloads: review_log.jsonl
records, possibly for several batches (each record names its `dir`). Per batch this appends
the records to <dir>/review_log.jsonl in order and regenerates review_decisions.json, exactly
as the local server would have. Rules:

  - a record is skipped when the log already holds it (same key, ts, reviewer and call), so
    importing the same download twice, or a later download that repeats the earlier one, is
    safe
  - a record whose `dir` is not a staging dir in this repo, or whose record_id is not in that
    dir's staged lane files, stops the import before anything is written (a stale page, or the
    batch was rebuilt since the page was made; rebuild the page and ask for a fresh review)
  - the GEM database, the staged_*.json files and the deliverables are not touched

Then build with the calls: python scripts/build_review_package.py ... --decisions
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for p in (ROOT / "scripts", HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import store  # noqa: E402

LANES = ("updates", "newplants", "newunits", "qa", "monitor", "entity")


def staged_ids(d):
    ids = set()
    for lane in LANES:
        f = Path(d) / f"staged_{lane}.json"
        if not f.exists():
            continue
        body = json.loads(f.read_text(encoding="utf-8"))
        recs = body.get("records", body) if isinstance(body, dict) else body
        for r in recs:
            if isinstance(r, dict) and r.get("record_id"):
                ids.add(r["record_id"])
    return ids


def fingerprint(r):
    return (r.get("key"), r.get("ts"), r.get("reviewer"), r.get("decision"), r.get("call"),
            bool(r.get("undecided")), r.get("suggested_value", ""), r.get("note", ""))


def plan(records, root=ROOT):
    """{dir label: (path, records to append, records skipped)} or SystemExit on a bad record."""
    by_dir = {}
    for i, r in enumerate(records):
        label = r.get("dir")
        if not label or not r.get("key") or not r.get("ts") or not r.get("reviewer"):
            raise SystemExit(f"line {i + 1}: not a review record (needs dir, key, ts, reviewer)")
        if "decision" in r and r["decision"] not in store.DECISIONS:
            raise SystemExit(f"line {i + 1}: decision {r['decision']!r} is not one of {sorted(store.DECISIONS)}")
        by_dir.setdefault(label, []).append(r)
    out = {}
    for label, recs in by_dir.items():
        d = Path(root) / label        # labels are repo-relative, or absolute outside the repo (store.dir_paths)
        if not d.is_dir() or ".." in Path(label).parts:
            raise SystemExit(f"{label}: not a staging dir")
        ids = staged_ids(d)
        if not ids:
            raise SystemExit(f"{label}: no staged lane files there")
        for r in recs:
            if r.get("record_id") not in ids:
                raise SystemExit(f"{label}: record_id {r.get('record_id')!r} is not in the staged lane files "
                                 f"(the batch was rebuilt since the page was made?)")
        have = {fingerprint(x) for x in store.read_log(d)}
        new, skipped = [], []
        for r in recs:
            (skipped if fingerprint(r) in have else new).append(r)
            have.add(fingerprint(r))
        out[label] = (d, new, skipped)
    return out


def read_records(path):
    """The records in a downloaded file: review_log .jsonl lines, or the .json document the
    artifact page keeps ({"records": [...]}, also what a download from the artifact gives)."""
    text = Path(path).read_text(encoding="utf-8").strip()
    try:
        body = json.loads(text)          # one document; a .jsonl with 2+ lines fails here
    except json.JSONDecodeError:
        return store.read_jsonl(path)
    if not isinstance(body, dict) or ("records" not in body and "data" not in body):
        return store.read_jsonl(path)
    body = body if "records" in body else body["data"]   # an ArtifactData get wraps the doc in data
    return [r for r in body.get("records", []) if isinstance(r, dict)]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("file", help="the downloaded review_log .jsonl")
    ap.add_argument("--dry-run", action="store_true", help="report only; write nothing")
    args = ap.parse_args(argv)
    records = read_records(args.file)
    if not records:
        raise SystemExit(f"{args.file}: no records")
    todo = plan(records)
    for label, (d, new, skipped) in todo.items():
        who = sorted({r.get("reviewer") for r in new})
        print(f"{label}: {len(new)} to append, {len(skipped)} already in the log"
              + (f" (by {', '.join(who)})" if who else ""))
        if args.dry_run or not new:
            continue
        with store._LOCK:
            store.append_jsonl(d / store.LOG_NAME, new)
            store.write_derived(d, store.now())
        print(f"  appended to {d / store.LOG_NAME}; {d / store.DERIVED_NAME} regenerated")
    if args.dry_run:
        print("dry run: nothing written")


if __name__ == "__main__":
    main()

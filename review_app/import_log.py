"""
Bring decisions made on the artifact page (build_static.py) into the decision ledger.

    python review_app/import_log.py <out_dir>/logs/<id>.json --dry-run
    python review_app/import_log.py FILE [FILE ...] --dirs batches/us-md/staging ... --reviewer EMAIL [--reviewer XX=EMAIL ...]

FILE is what the page's "download decisions" button saves, or the artifact's shared `logs`
collection saved as JSON (an ArtifactData list or get result). Either way it holds one or more
log documents, each {reviewer, records: [...]}. --dirs names the staging dirs the page was built
from (default: every dir the records name); the dataset is rebuilt from them so each record can
be checked against the current batch.

Every new record goes through the ledger like any other decision: appended to the store
spreadsheet's `log` tab first (origin 'artifact', under the reviewer's own address), then to the
staging dir's review_log.jsonl. Each record keeps the id and the time the page gave it. Rules:

  - a record whose id is already in a staging dir's log is skipped, so importing the same file
    twice, or a later download that repeats an earlier one, is safe. A record the page wrote
    before it stamped ids (pages built before 2026-10-08) gets one derived from its contents
    (reviewer, key, time, call), the same id every time, so those files re-import safely too
  - a record is skipped as superseded when the log already holds a later decision by a person on
    the same line, item or flag (someone decided it on the local server afterwards)
  - a record whose key is not in the current dataset, or whose staging dir is not, stops the
    import before anything is written (the batch was rebuilt since the page was made: rebuild the
    page and publish it again)
  - the page is not given reviewers' addresses, only their names, so name each one:
    --reviewer amalia.llano@globalenergymonitor.org (matched to the initials AL), or --reviewer AL=ADDRESS

This appends to the store `log` tab and to the sidecars. The GEM database, the staged_*.json
files and the deliverables are not touched; accepted edits reach GEM only through the actions
workbook that scripts/build_review_package.py --decisions builds and the reviewer applies by hand.
"""
import argparse
import json
import sys
import uuid
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for p in (ROOT / "scripts", HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import ledger  # noqa: E402
import pull  # noqa: E402
import review_data  # noqa: E402
import store  # noqa: E402

ORIGIN = "artifact"


def read_docs(path):
    """Every log document in a file, wherever it sits: the download, one document, or an
    ArtifactData result that wraps documents in its own envelope. A bare .jsonl of records is
    one document with no reviewer name."""
    text = Path(path).read_text(encoding="utf-8")
    try:
        body = json.loads(text)
    except json.JSONDecodeError:
        recs = store.read_jsonl(path)
        return [{"reviewer": "", "records": recs}] if recs else []
    docs = []

    def walk(x):
        if isinstance(x, dict):
            if isinstance(x.get("records"), list):
                docs.append(x)
            else:
                for v in x.values():
                    walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(body)
    return docs


def _when(ts):
    try:
        return datetime.fromisoformat(str(ts))
    except ValueError:
        return None


# records the page wrote before static_store.js stamped a uuid4 on each one (pages built before
# 2026-10-08) get this id instead: the same one every time, from what the record says
LEGACY_NS = uuid.UUID("6f1d2b2e-5c2a-4f6e-9c1b-0f2a8d3e7b41")
LEGACY_FIELDS = ("reviewer", "key", "dir", "ts", "decision", "call", "flag", "on", "undecided",
                 "note", "suggested_value", "reference")


def legacy_id(r):
    """A deterministic id for a page record that has none."""
    parts = [f"{k}={json.dumps(r.get(k), sort_keys=True, default=str)}" for k in LEGACY_FIELDS]
    return str(uuid.uuid5(LEGACY_NS, "\n".join(parts)))


def dataset(dirs, export_csv=None, root=ROOT):
    """The current dataset for these staging dirs, overlaid with their logs, and {label: Path}."""
    ds = review_data.build([Path(d) for d in dirs], export_csv)
    paths = store.dir_paths(ds, root)
    store.overlay(ds, paths)
    return ds, paths


def plan(docs, ds, dirs, emails=None):
    """-> {"new": [(email, record), ...] in time order, "dup": n, "stale": [records], "people": {initials: email}}.
    SystemExit on a record this dataset cannot take; nothing is written here."""
    idx = store.index(ds)
    plants = {store.plant_flag_key(p.get("dir"), p["pid"]) for p in ds.get("plants", [])}
    have, last = set(), {}
    for d in dirs.values():
        for r in store.read_log(d):
            if r.get("id"):
                have.add(str(r["id"]))
            t = _when(r.get("ts"))
            if r.get("key") and t and not store.is_machine(r) and (r["key"] not in last or t > last[r["key"]]):
                last[r["key"]] = t
    new, stale, people, dup, seen = [], [], {}, 0, set()
    for doc in docs:
        doc_email = str(doc.get("email") or "").strip()
        for i, r in enumerate(doc["records"]):
            where = f"{doc.get('reviewer') or '?'} record {i + 1}"
            if not isinstance(r, dict) or not r.get("key") or not r.get("reviewer") or not r.get("dir"):
                raise SystemExit(f"{where}: not a review record (needs key, reviewer, dir)")
            if not r.get("id"):
                r["id"] = legacy_id(r)
            t = _when(r.get("ts"))
            if t is None or t.tzinfo is None:
                raise SystemExit(f"{where}: no usable time ({r.get('ts')!r})")
            if store.is_machine(r) or not store._INITIALS_RE.match(str(r["reviewer"])):
                raise SystemExit(f"{where}: reviewer {r['reviewer']!r} is not a person's initials")
            if str(r["id"]) in have or str(r["id"]) in seen:
                dup += 1
                continue
            seen.add(str(r["id"]))
            key = str(r["key"])
            if r.get("flag"):
                if r["flag"] not in store.FLAGS or not key.startswith(store.FLAG_PREFIX):
                    raise SystemExit(f"{where}: not an ask-the-PM flag record")
                inner = key[len(store.FLAG_PREFIX):]
                if inner not in idx and key not in plants:
                    raise SystemExit(f"{where}: {key} flags nothing in the current dataset "
                                     "(rebuilt since the page was made? rebuild the page and publish it again)")
            else:
                if key not in idx:
                    raise SystemExit(f"{where}: {key} is not in the current dataset "
                                     "(rebuilt since the page was made? rebuild the page and publish it again)")
                grp = idx[key][2]
                if ("call" in r) != (grp == "items"):
                    raise SystemExit(f"{where}: {key} is {'an item' if grp == 'items' else 'a line'} "
                                     f"but the record is {'an item call' if 'call' in r else 'a line decision'}")
                if "decision" in r and r["decision"] not in store.DECISIONS:
                    raise SystemExit(f"{where}: decision {r['decision']!r} is not one of {sorted(store.DECISIONS)}")
                if "call" in r and not r.get("undecided"):
                    vocab = store.ITEM_CALLS.get(idx[key][1].get("kind"), store.OTHER_CALLS)
                    if r["call"] not in vocab:
                        raise SystemExit(f"{where}: call {r['call']!r} is not one of {list(vocab)} for a {idx[key][1].get('kind')} item")
            if r["dir"] not in dirs:
                raise SystemExit(f"{where}: staging dir {r['dir']} is not part of the current dataset")
            email = doc_email or (emails or {}).get(r["reviewer"]) or ""
            if not email:
                raise SystemExit(f"{where}: the log of {r['reviewer']} carries no address: pass --reviewer {r['reviewer']}=EMAIL")
            full = store.initials(email)         # a one-word profile name logs "B": record "BL"
            if len(r["reviewer"]) < 2 and full.startswith(r["reviewer"]):
                r["reviewer"] = full
            if people.setdefault(r["reviewer"], email) != email:
                raise SystemExit(f"{where}: {r['reviewer']} appears under two addresses ({people[r['reviewer']]}, {email})")
            if key in last and last[key] > t:
                stale.append(r)
                continue
            new.append((t, email, r))
    new.sort(key=lambda x: x[0])
    return {"new": [(e, r) for _, e, r in new], "dup": dup, "stale": stale, "people": people}


def runs(new):
    """Consecutive records of one address, so the log keeps time order across reviewers."""
    out = []
    for email, r in new:
        if out and out[-1][0] == email:
            out[-1][1].append(r)
        else:
            out.append((email, [r]))
    return out


def write(pl, ds, dirs, cfg=None, gws=pull.gws):
    """Append the planned records, store first. -> the saved records (each with its store `row`)."""
    saved = []
    for email, recs in runs(pl["new"]):
        led = ledger.Ledger.for_data(ds, ORIGIN, cfg=cfg, reviewer_email=email, gws=gws)
        if led is None:
            raise SystemExit("no store configured (review_app/google.json: store_sheet_id): nothing was recorded")
        saved += store.append_records([dict(r) for r in recs], dirs, sink=led.sink)
    return saved


def report(pl):
    out = []
    by = {}
    for email, r in pl["new"]:
        by.setdefault((r["reviewer"], email), []).append(r)
    for (who, email), recs in sorted(by.items()):
        n_item = sum(1 for r in recs if "call" in r and not r.get("flag"))
        n_flag = sum(1 for r in recs if r.get("flag"))
        undo = sum(1 for r in recs if r.get("undecided"))
        out.append(f"{who} ({email}): {len(recs) - n_item - n_flag} line decisions, {n_item} item calls, {n_flag} flags"
                   + (f", {undo} of them undos" if undo else "")
                   + (f"  [note: the address reads as {store.initials(email)}]" if store.initials(email) != who else ""))
    out.append(f"{len(pl['new'])} new, {pl['dup']} already in the log, {len(pl['stale'])} superseded by a later decision")
    for r in pl["stale"][:20]:
        out.append(f"  superseded: {r['key']} ({r['reviewer']}, {r.get('ts')})")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("file", nargs="+", help="the page's download, or the artifact's `logs` collection saved as JSON")
    ap.add_argument("--dirs", nargs="*", default=[], help="the staging dirs the page was built from (default: the dirs the records name)")
    ap.add_argument("--export-csv", default=None, help="scoped export csv (default: the batch's own)")
    ap.add_argument("--reviewer", action="append", default=[], metavar="EMAIL or XX=EMAIL",
                    help="a reviewer's address, for a log that carries none (the page is not given addresses); "
                         "repeat per reviewer. A bare EMAIL is matched to its own initials")
    ap.add_argument("--dry-run", action="store_true", help="report only; write nothing")
    a = ap.parse_args(argv)
    docs = [d for f in a.file for d in read_docs(f)]
    if not any(d["records"] for d in docs):
        raise SystemExit("no records in " + ", ".join(a.file))
    dirs = list(a.dirs) or sorted({str(r.get("dir")) for d in docs for r in d["records"] if isinstance(r, dict) and r.get("dir")})
    for d in dirs:
        if not (ROOT / d).is_dir() and not Path(d).is_dir():
            raise SystemExit(f"{d}: not a staging dir")
    ds, paths = dataset([(ROOT / d) if not Path(d).is_absolute() else Path(d) for d in dirs], a.export_csv)
    emails = {}
    for v in a.reviewer:
        who, _, addr = v.rpartition("=")
        emails[who.strip() or store.initials(addr.strip())] = addr.strip()
    pl = plan(docs, ds, paths, emails=emails)
    print(report(pl))
    if a.dry_run:
        print("dry run: nothing written")
        return 0
    if not pl["new"]:
        return 0
    try:
        saved = write(pl, ds, paths)
    except ledger.StoreError as e:
        sys.exit(f"{e}\nthe records of this run were not recorded; run the import again (earlier runs are skipped by id)")
    print(f"{len(saved)} records in the store (rows {min(r['row'] for r in saved)}-{max(r['row'] for r in saved)}) "
          f"and in {len({r['dir'] for r in saved})} staging dir(s). "
          "Then: python scripts/build_review_package.py ... --decisions")
    return 0


if __name__ == "__main__":
    sys.exit(main())

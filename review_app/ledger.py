"""
The decision ledger: ONE place every review decision lands, whoever makes it and however.

    python review_app/ledger.py status                       # store configured? who writes? last row
    python review_app/ledger.py backfill batches/us-ny/staging --reviewer AL=EMAIL [--dry-run]
                                                             # sidecar records older than the ledger -> store

The ledger IS the `log` tab of the store spreadsheet (review_app/google.json: store_sheet_id), one row per record, in the COLS columns below (the same model as pipelines-researcher's ledger, with the GOGPT record shape: record_id, column, reference, flag/on). Everything that writes a staging dir's review_log.jsonl writes HERE FIRST and the sidecars second:

    artifact page       -> import_log.py (the viewer's shared log; origin 'artifact')
    loopback server     -> store.decide(..., sink=Ledger.sink)   (origin 'local')
    pull.py             -> mirrors store rows into the sidecars (never writes the store)

so the store holds every decision, the sidecars are its committed mirror, and the actions workbook (build_review_package.py --decisions) reads one history. Appending to the `log` tab is the ONLY Google write this module makes, through gws-gem-write; nothing else in Drive is touched and the GEM database never is.

The rules (store first, verified appends in chunks of APPEND_CHUNK, ids, emails in the store and initials in the sidecars) and the code that keeps them are shared with pipelines-researcher in ../gem-review-app/review_core/ledger.py. This file holds the gogpt side: COLS, ORIGINS, row_of, scope_of, rec_type, dir_label, backfill and the CLI.

`backfill` is the one case where a sidecar is rewritten rather than appended to: a record written before the ledger existed (no `id`) is stamped (id, scope, batch, origin 'chat'; its own time is kept), appended to the store under the reviewer's address (--reviewer XX=EMAIL), and then the sidecar line is replaced by the stamped record, so the sidecar once again mirrors the store. Records that already carry an id are left alone, so a second run writes nothing.
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

import pull  # noqa: E402
import store  # noqa: E402
from review_core import ledger as core  # noqa: E402

# the store's `log` tab header, verbatim (tests assert the sheet set-up and this list agree)
COLS = ["ts", "reviewer", "rec", "pid", "record_id", "column", "kind", "decision", "call", "suggested_value",
        "reference", "note", "undecided", "flag", "on", "batch", "snapshot", "key", "id", "scope", "json"]
ORIGINS = ("local", "artifact", "chat")


def scope_of(data):
    """(scope id, snapshot) of a built dataset: the staging dir labels joined with "+" (batches/us-md/staging gives us-md; a staging-discovery dir keeps its suffix), and the dataset's build stamp."""
    labels = []
    for d in data.get("dirs") or []:
        parts = [x for x in str(d).split("/") if x]
        if parts and parts[-1] == "staging":
            parts.pop()
        elif len(parts) >= 2 and parts[-1].startswith("staging-"):
            parts[-2:] = [parts[-2] + "-" + parts[-1][len("staging-"):]]
        labels.append(parts[-1] if parts else str(d))
    return "+".join(labels), str(data.get("built") or "")


def rec_type(rec):
    return "flag" if rec.get("flag") else "item" if "call" in rec else "line"


def row_of(rec):
    """One sheet row (len(COLS) strings) for a record; the `json` column is the record."""
    j = core.record_json(rec)
    cell = core.cell
    on = "" if rec.get("on") is None else ("on" if rec.get("on") else "off")
    return [str(rec.get("ts") or ""), str(rec.get("reviewer") or ""), rec_type(rec), cell(rec.get("pid")),
            cell(rec.get("record_id")), cell(rec.get("column")), str(rec.get("kind") or ""),
            str(rec.get("decision") or ""), str(rec.get("call") or ""), cell(rec.get("suggested_value")),
            cell(rec.get("reference")), cell(rec.get("note")), "undone" if rec.get("undecided") else "",
            str(rec.get("flag") or ""), on if rec.get("flag") else "", str(rec.get("batch") or ""),
            cell(rec.get("snapshot")), cell(rec.get("key")), str(rec.get("id") or ""), str(rec.get("scope") or ""), j]


core.bind(sys.modules[__name__], pull=pull, store=store)


def dir_label(d, root=ROOT):
    """A staging dir's label as records name it: its path relative to the repo root."""
    d = Path(d)
    if not d.is_absolute():
        d = root / d
    try:
        return d.resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError:
        return d.as_posix()


def backfill(d, emails, sheet_id, gws=None, dry_run=False, root=ROOT):
    """Bring the records of <d>/review_log.jsonl that predate the ledger (no `id`) into the store,
    then rewrite the sidecar with the stamped records. `emails` maps initials to addresses; a
    person whose address is not given stops the run before anything is written. -> the records
    stamped (written unless dry_run), each with its store `row`."""
    d = Path(d) if Path(d).is_absolute() else root / d
    if not d.is_dir():
        raise SystemExit(f"{d}: not a staging dir")
    if not sheet_id:
        raise SystemExit("no store configured (review_app/google.json: store_sheet_id)")
    label = dir_label(d, root)
    with store._LOCK:
        recs = store.read_log(d)
        todo = [r for r in recs if not r.get("id")]
        if not todo:
            return []
        addrs = []
        for i, r in enumerate(todo):
            if not r.get("key") or not r.get("reviewer"):
                raise SystemExit(f"{label} record {i + 1} without an id is not a review record (needs key, reviewer)")
            if r.get("dir") != label:
                raise SystemExit(f"{label} record {i + 1} names another dir ({r.get('dir')!r})")
            who = r["reviewer"]
            if store.is_machine(r):
                addr = who
            else:
                addr = (emails or {}).get(who) or ""
                if not addr:
                    raise SystemExit(f"{label}: no address for reviewer {who}: pass --reviewer {who}=EMAIL")
            addrs.append(addr)
        scope, _ = scope_of({"dirs": [label]})
        stamp_fields(todo, scope, "", "chat")
        srows = [dict(r, reviewer=addr) for r, addr in zip(todo, addrs)]
        if dry_run:
            return todo
        append(srows, sheet_id, gws=gws)
        for r, s in zip(todo, srows):
            r["row"] = s.get("row")
        text = "".join(json.dumps({k: v for k, v in r.items() if k != "row"}, ensure_ascii=False) + "\n" for r in recs)
        store.atomic_write(d / store.LOG_NAME, text)
        store.write_derived(d, store.now())
    return todo


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status", help="store configured? who writes it? how many rows?")
    bf = sub.add_parser("backfill", help="append a staging dir's pre-ledger sidecar records (no id) to the store")
    bf.add_argument("dir", help="the staging dir, e.g. batches/us-ny/staging")
    bf.add_argument("--reviewer", action="append", default=[], metavar="XX=EMAIL",
                    help="the address behind a reviewer's initials in the sidecar; repeat per reviewer")
    bf.add_argument("--dry-run", action="store_true", help="report only; write nothing")
    a = ap.parse_args(argv)
    cfg = pull.config()
    sheet = cfg.get("store_sheet_id") or ""
    if a.cmd == "status":
        if not sheet:
            print("no store configured (review_app/google.json: store_sheet_id)")
            return 1
        me = whoami()
        rows = pull.read_store(sheet)
        print(f"store {sheet}: `{LOG_TAB}` tab, {max(0, len(rows) - 1)} records; writer {me or '(unknown: gws-gem-write auth?)'}")
        print(f"https://docs.google.com/spreadsheets/d/{sheet}/edit")
        return 0
    if a.cmd == "backfill":
        emails = {}
        for v in a.reviewer:
            who, _, addr = v.rpartition("=")
            emails[who.strip() or store.initials(addr.strip())] = addr.strip()
        try:
            done = backfill(a.dir, emails, sheet, dry_run=a.dry_run)
        except StoreError as e:
            sys.exit(f"{e}\nnothing was recorded; the sidecar is unchanged")
        if not done:
            print(f"{a.dir}: every sidecar record already carries an id; nothing to backfill")
            return 0
        for r in done:
            print(f"  {r['reviewer']} {r.get('decision') or r.get('call') or r.get('flag')} {r['key']} ({r.get('ts')})")
        if a.dry_run:
            print(f"dry run: {len(done)} records would be appended to the store and restamped in the sidecar; nothing written")
        else:
            print(f"{len(done)} records in the store (rows {min(r['row'] for r in done)}-{max(r['row'] for r in done)}) "
                  f"and restamped in {a.dir}/{store.LOG_NAME}")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())

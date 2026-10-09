"""
The decision ledger: ONE place every review decision lands, whoever makes it and however.

    python review_app/ledger.py status                       # store configured? who writes? last row
    python review_app/ledger.py backfill batches/us-ny/staging --reviewer AL=EMAIL [--dry-run]
                                                             # sidecar records older than the ledger -> store

The ledger IS the `log` tab of the store spreadsheet (review_app/google.json: store_sheet_id), one
row per record, in the COLS columns below (the same model as pipelines-researcher's ledger, with
the GOGPT record shape: record_id, column, reference, flag/on). Everything that writes a staging
dir's review_log.jsonl writes HERE FIRST and the sidecars second:

    artifact page       -> import_log.py (the viewer's shared log; origin 'artifact')
    loopback server     -> store.decide(..., sink=Ledger.sink)   (origin 'local')
    pull.py             -> mirrors store rows into the sidecars (never writes the store)

so the store holds every decision, the sidecars are its committed mirror, and the actions workbook
(build_review_package.py --decisions) reads one history. Appending to the `log` tab is the ONLY
Google write this module makes, through gws-gem-write; nothing else in Drive is touched and the
GEM database never is.

Rules
  * the store comes first. A record is appended to the sheet, read back by `id`, and only then
    written to the sidecar. If the store cannot be reached the decision is REFUSED (StoreError ->
    HTTP 502 on the server, exit 2 on the CLI) and nothing is written anywhere: there is no
    offline mode, because an offline decision is exactly the divergence this module exists to end.
    `--no-store` on server.py is for tests and dev only and says so on every start.
  * the store keeps the reviewer's EMAIL; the sidecars keep initials (store.initials). Machine
    reviewers are kept as is.
  * a record's `id` is a uuid4 stamped here (an id already present, as the artifact page gives
    every record, is kept), so pull.py's mirror, which dedupes by id, never writes the same record
    twice.
  * the sheet append is verified: the rows the API says it wrote are re-read and their `id` column
    must be these records' ids. A mismatch (another writer landing on the same rows in the same
    instant) is retried once, then refused.
  * `backfill` is the one case where a sidecar is rewritten rather than appended to: a record
    written before the ledger existed (no `id`) is stamped (id, scope, batch, origin 'chat'; its
    own time is kept), appended to the store under the reviewer's address (--reviewer XX=EMAIL),
    and then the sidecar line is replaced by the stamped record, so the sidecar once again mirrors
    the store. Records that already carry an id are left alone, so a second run writes nothing.
"""
import argparse
import json
import re
import sys
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for p in (ROOT / "scripts", HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import pull  # noqa: E402
import store  # noqa: E402

# the store's `log` tab header, verbatim (tests assert the sheet set-up and this list agree)
COLS = ["ts", "reviewer", "rec", "pid", "record_id", "column", "kind", "decision", "call", "suggested_value",
        "reference", "note", "undecided", "flag", "on", "batch", "snapshot", "key", "id", "scope", "json"]
LOG_TAB = pull.LOG_TAB
ORIGINS = ("local", "artifact", "chat")
MAX_JSON = 49000          # a cell holds 50k chars
_FORMULA = re.compile(r"^[=+\-@]")
_RANGE = re.compile(r"^'?(?P<tab>[^'!]+)'?!(?P<c1>[A-Z]+)(?P<r1>\d+)(?::(?P<c2>[A-Z]+)(?P<r2>\d+))?$")


class StoreError(RuntimeError):
    """The store could not be written (or read back as written): nothing was recorded anywhere."""


def scope_of(data):
    """(scope id, snapshot) of a built dataset: the staging dir labels joined with "+" (batches/us-md/staging
    -> us-md; a staging-discovery dir keeps its suffix), and the dataset's build stamp."""
    labels = []
    for d in data.get("dirs") or []:
        parts = [x for x in str(d).split("/") if x]
        if parts and parts[-1] == "staging":
            parts.pop()
        elif len(parts) >= 2 and parts[-1].startswith("staging-"):
            parts[-2:] = [parts[-2] + "-" + parts[-1][len("staging-"):]]
        labels.append(parts[-1] if parts else str(d))
    return "+".join(labels), str(data.get("built") or "")


def cell(v):
    """A display column is never a formula and never longer than a cell."""
    s = "" if v is None else str(v)
    if _FORMULA.match(s):
        s = "'" + s
    return s[:2000] + "…" if len(s) > 2000 else s


def rec_type(rec):
    return "flag" if rec.get("flag") else "item" if "call" in rec else "line"


def row_for(rec):
    """One sheet row (len(COLS) strings) for a record; the `json` column is the record."""
    j = json.dumps(rec, ensure_ascii=False, separators=(",", ":"))
    if len(j) > MAX_JSON:
        raise StoreError("a record is too long to store: shorten the note")
    on = "" if rec.get("on") is None else ("on" if rec.get("on") else "off")
    return [str(rec.get("ts") or ""), str(rec.get("reviewer") or ""), rec_type(rec), cell(rec.get("pid")),
            cell(rec.get("record_id")), cell(rec.get("column")), str(rec.get("kind") or ""),
            str(rec.get("decision") or ""), str(rec.get("call") or ""), cell(rec.get("suggested_value")),
            cell(rec.get("reference")), cell(rec.get("note")), "undone" if rec.get("undecided") else "",
            str(rec.get("flag") or ""), on if rec.get("flag") else "", str(rec.get("batch") or ""),
            cell(rec.get("snapshot")), cell(rec.get("key")), str(rec.get("id") or ""), str(rec.get("scope") or ""), j]


def stamp_fields(recs, scope, snapshot, origin, batch=None, ts=None):
    """Stamping for records written here: every record gets this `origin` and one `batch` uuid per
    call; `id`, `scope`, `snapshot` and `ts` are filled only where missing (a record from the
    artifact page keeps the id and time the page gave it). Returns recs."""
    if origin not in ORIGINS:
        raise ValueError(f"origin {origin!r} is not one of {ORIGINS}")
    batch = batch or str(uuid.uuid4())
    ts = ts or store.now()
    for r in recs:
        r["id"] = r.get("id") or str(uuid.uuid4())
        r["scope"] = r.get("scope") or scope
        r["batch"] = batch
        r["snapshot"] = r.get("snapshot") if r.get("snapshot") not in (None, "") else snapshot
        r["origin"] = origin
        if not r.get("ts"):
            r["ts"] = ts
    return recs


def _range_rows(rng):
    m = _RANGE.match(rng or "")
    if not m:
        raise StoreError(f"cannot read the range the store reports: {rng!r}")
    r1 = int(m.group("r1"))
    return r1, int(m.group("r2") or r1)


def append(recs, sheet_id, gws=pull.gws, profile=pull.WRITE_PROFILE, read_profile=pull.READ_PROFILE, retries=1):
    """Append the records to the store's `log` tab (one RAW row each, after the last row) and
    verify by re-reading the `id` column of the rows the API reports. -> (first row, last row).
    Raises StoreError (nothing to clean up: a failed append wrote nothing we can rely on, and a
    verified mismatch means our rows were overwritten, so the retry appends again)."""
    if not recs:
        return None
    rows = [row_for(r) for r in recs]
    ids = [r["id"] for r in recs]
    idc = pull._col_letter(COLS.index("id"))
    last_err = None
    for attempt in range(retries + 1):
        try:
            resp = gws(profile, "sheets", "spreadsheets", "values", "append",
                       "--params", json.dumps({"spreadsheetId": sheet_id, "range": f"{LOG_TAB}!A:{pull._col_letter(len(COLS) - 1)}",
                                               "valueInputOption": "RAW", "insertDataOption": "INSERT_ROWS",
                                               "includeValuesInResponse": False}),
                       "--json", json.dumps({"majorDimension": "ROWS", "values": rows}, ensure_ascii=False))
        except pull.GwsError as e:
            raise StoreError(f"the decision store could not be written: {e}") from e
        upd = (resp or {}).get("updates") or {}
        first, last = _range_rows(upd.get("updatedRange"))
        if last - first + 1 != len(rows):
            raise StoreError(f"the store reports {last - first + 1} rows written for {len(rows)} records ({upd.get('updatedRange')})")
        try:
            got = gws(read_profile, "sheets", "spreadsheets", "values", "get", "--params",
                      json.dumps({"spreadsheetId": sheet_id, "range": f"{LOG_TAB}!{idc}{first}:{idc}{last}",
                                  "majorDimension": "ROWS", "valueRenderOption": "UNFORMATTED_VALUE"}))
        except pull.GwsError as e:
            raise StoreError(f"written to the store (rows {first}-{last}) but the read-back failed: {e}") from e
        back = [(r[0] if r else "") for r in (got.get("values") or [])]
        back += [""] * (len(ids) - len(back))
        if back == ids:
            for r, i in zip(recs, range(first, last + 1)):
                r["row"] = i
            return first, last
        last_err = StoreError(f"the store's rows {first}-{last} do not hold these records after the append "
                              f"(another writer landed on them); " + ("retried once" if attempt else "retrying"))
    raise last_err


class Ledger:
    """A configured sink: `sink(recs, dirs, stamp=True)` has store._write's signature and is passed
    to store.decide / record_items / record_flags / append_records. `reviewer_email` is the
    address written on a person's store rows (the account that writes the store, by default)."""

    def __init__(self, sheet_id, scope, snapshot, origin, reviewer_email=None, gws=pull.gws, emails=None):
        if not sheet_id:
            raise ValueError("no store configured (review_app/google.json: store_sheet_id)")
        self.sheet_id, self.scope, self.snapshot, self.origin = sheet_id, scope, snapshot, origin
        self.reviewer_email = reviewer_email or ""
        self.emails = dict(emails or {})      # store record id -> address (pull.mirror's), for copies of others' records
        self.gws = gws
        self.written = 0
        self.last_row = 0                     # the last store row this ledger wrote

    @classmethod
    def for_data(cls, data, origin, cfg=None, reviewer_email=None, gws=pull.gws):
        """A ledger for a built dataset, or None when no store is configured."""
        cfg = pull.config() if cfg is None else cfg
        sheet = (cfg or {}).get("store_sheet_id") or ""
        if not sheet:
            return None
        sid, snap = scope_of(data)
        return cls(sheet, sid, snap, origin, reviewer_email=reviewer_email, gws=gws)

    def to_store(self, rec):
        """The store's copy of a record: a person's initials become an address, the original
        decider's when this is a copy of a store record (`emails`, by the id before `~`), else the
        writer's. A machine reviewer is kept as is."""
        r = dict(rec)
        who = r.get("reviewer")
        if who and who not in store.MACHINE_REVIEWERS:
            orig = self.emails.get(str(r.get("id") or "").split("~")[0])
            if orig or self.reviewer_email:
                r["reviewer"] = orig or self.reviewer_email
        return r

    def sink(self, recs, dirs, stamp=True):
        """Store first, sidecars second (caller holds store._LOCK). Stamps id/scope/batch/snapshot/
        origin (and ts unless the records bring their own). The local copy keeps the initials and
        every stamped field, exactly what pull.mirror would write for the same store row, so a later
        pull dedupes it by id. Raises StoreError before anything local is written."""
        recs = list(recs)
        if not recs:
            return []
        ts = store.now() if stamp else None
        for r in recs:
            if stamp:
                r["ts"] = ts
            r["reviewer"] = store.initials(r.get("reviewer"))
            if r["dir"] not in dirs:          # refuse an unknown dir BEFORE the store write, as _write would
                raise store.Invalid(f"staging dir not known to the server: {r['dir']}")
        stamp_fields(recs, self.scope, self.snapshot, self.origin, ts=ts)
        rows = [self.to_store(r) for r in recs]
        first, last = append(rows, self.sheet_id, gws=self.gws)
        store._write([dict(r) for r in recs], dirs, stamp=False)
        for r, s in zip(recs, rows):
            r["row"] = s.get("row")
        self.written += len(recs)
        self.last_row = max(self.last_row, last)
        return recs


def whoami(gws=pull.gws, profile=pull.WRITE_PROFILE):
    """The address of the account that writes the store (Drive `about.user`), or '' when it cannot
    be read. The store row's reviewer must be the account that wrote it, so this is the default."""
    try:
        body = gws(profile, "drive", "about", "get", "--params", json.dumps({"fields": "user"}))
    except pull.GwsError:
        return ""
    return str(((body or {}).get("user") or {}).get("emailAddress") or "")


def dir_label(d, root=ROOT):
    """A staging dir's label as records name it: its path relative to the repo root."""
    d = Path(d)
    if not d.is_absolute():
        d = root / d
    try:
        return d.resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError:
        return d.as_posix()


def backfill(d, emails, sheet_id, gws=pull.gws, dry_run=False, root=ROOT):
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

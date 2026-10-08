"""
The review app's decision store. Port of the pipelines-researcher store, reshaped for GOGPT:
every decision is a call on ONE staged record (by its stable `record_id`, written by
scripts/assemble_state.py), and the two sidecars live IN the staging dir and are committed
with the batch:

    review_log.jsonl        append-only truth: every decision and every undo, one record per line
    review_decisions.json   derived: {"generated": ts, "decisions": {key: latest record}}

Record shape: {key, dir, pid, record_id, column, kind, decision, suggested_value, reference, note,
reviewer, ts, undecided}; `reviewer` is a person's initials (initials()). An undo appends a
record with `undecided: true`; nothing is ever deleted from the log. Item calls (qa concerns,
watch items, entity notes) go to the same log with {key, dir, pid, record_id, kind, call,
reference, note, ...}; a watch item's calls are add_to_database / hold / possible_updates /
remove (review_app/checklist.py WATCH_CALLS). An ask-the-PM flag is a third record type,
{key: "pm::" + <line/item key> or "pm::" + dir + "::plant:" + pid, flag: "pm", on, note, ...}: a
flag sits beside a decision and never replaces it, so one line can be accepted AND flagged.

Nothing here touches the GEM database, the staged_*.json files or the deliverables: the
decisions are consumed by scripts/build_review_package.py --decisions when the actions
workbook is built.
"""
import json
import os
import re
import sys
import threading
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from review_app.checklist import WATCH_CALLS  # noqa: E402

ET = ZoneInfo("America/New_York")
DECISIONS = {"accept", "hold", "reject", "suggest"}
LOG_NAME = "review_log.jsonl"
DERIVED_NAME = "review_decisions.json"
# A person is recorded by their first and last initials, never their full name: "Baird
# Langenbrunner" and baird.langenbrunner@globalenergymonitor.org both record as "BL".
_INITIALS_RE = re.compile(r"^[A-Z]{1,3}$")
_EMAIL_RE = re.compile(r"^([^@\s]+)@[^@\s]+\.[^@\s]+$")
# Line kinds (review_data.py): fill = blank cell gets a value; change = a value is replaced;
# reverified = the current value was checked and stands (new Data Source link only);
# delete = a value is cleared; plant = a plant-level change applied to every unit row;
# new_row = a new unit or plant.
LINE_KINDS = ("fill", "change", "reverified", "delete", "plant", "new_row")
ITEM_KINDS = ("concern", "monitor", "entity", "other")
# The call vocabulary per item kind. A concern (qa lane) is confirmed (it stands and goes to
# the QA sheet), dismissed, or sent back for more research. A watch item (monitor lane) is
# added to the database now, held, sent to the possible-updates sheet, or removed from the
# watchlist (remove needs a note saying why). Everything else is noted / todo / dismissed.
# Items never write a cell.
CONCERN_CALLS = ("confirmed", "dismissed", "needs_research")
OTHER_CALLS = ("noted", "todo", "dismissed")
ITEM_CALLS = {k: (CONCERN_CALLS if k == "concern" else WATCH_CALLS if k == "monitor" else OTHER_CALLS)
              for k in ITEM_KINDS}
NOTE_REQUIRED = {("monitor", "remove")}       # (kind, call) pairs that need a note
FLAG_PREFIX = "pm::"
FLAGS = ("pm",)

_LOCK = threading.Lock()     # one process-wide lock around every read-modify-write of a sidecar


def initials(who):
    """A person -> their first + last initials, uppercased: "Baird Langenbrunner" -> "BL",
    baird.langenbrunner@globalenergymonitor.org -> "BL" (the local part split on . _ - +), a
    one-part name or address -> its first letter. A value already in initials form and an empty
    value come back unchanged, so applying it twice is a no-op."""
    v = str(who or "").strip()
    if not v or _INITIALS_RE.match(v):
        return who
    m = _EMAIL_RE.match(v)
    parts = [t for t in re.split(r"[._+\-]+" if m else r"\s+", m.group(1) if m else v) if t[:1].isalpha()]
    if not parts:
        return who
    return (parts[0][0] + (parts[-1][0] if len(parts) > 1 else "")).upper()


class Invalid(ValueError):
    """A request the store refuses before writing anything (HTTP 400)."""


# ---- reading ---------------------------------------------------------------------

def read_jsonl(path):
    """Records of a JSONL file; a torn last line (crash mid-append) is skipped, not fatal."""
    out = []
    path = Path(path)
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def read_log(d):
    return read_jsonl(Path(d) / LOG_NAME)


def latest(records, field="key"):
    """field value -> the last record carrying it (the log is append-only; latest wins)."""
    out = {}
    for r in records:
        if r.get(field):
            out[r[field]] = r
    return out


def read_decisions(d):
    """key -> latest record for a staging dir, from the log (the derived file is a convenience
    copy; the log is the truth)."""
    return latest(read_log(d))


def reviewed(rec):
    """True when the record is a person's live call (not an undo)."""
    return bool(rec) and not rec.get("undecided")


def dir_paths(data, root=None):
    """{dir label: Path}. Labels are relative to the repo root (review_data.rel), or absolute."""
    base = Path(root) if root else ROOT
    return {d: base / d for d in data.get("dirs", [])}


def plant_flag_key(label, pid):
    return f"{FLAG_PREFIX}{label}::plant:{pid}"


def overlay(data, dirs=None, root=None):
    """Fill `decision`, `reviewed`, `decided_by`, `decided_at` (+ `suggested_value`,
    `reference`, `decision_note` on a suggest) on every line, and `call`, `call_note`,
    `call_reference`, `reviewed`, `decided_by`, `decided_at` on every item of `data` (in place;
    returns it) from each dir's review_log.jsonl. The latest record per key speaks: `decision` /
    `call` is None after an undo or with no record. Ask-the-PM flags land as `pm_flag` /
    `pm_note` on lines, items and plants (a plant flag is kept in the plant's own dir)."""
    dirs = dirs if dirs is not None else dir_paths(data, root)
    logs = {}

    def last(d, key):
        if d not in logs:
            logs[d] = read_decisions(dirs[d]) if d in dirs else {}
        return logs[d].get(key)

    def flag(d, key, o):
        rec = last(d, FLAG_PREFIX + key)
        live = rec if reviewed(rec) and rec.get("on") else None
        o["pm_flag"] = bool(live)
        o["pm_note"] = live.get("note", "") if live else ""
        o["pm_by"] = live.get("reviewer") if live else None

    for p in data.get("plants", []):
        for grp in ("lines", "items"):
            for o in p.get(grp, []):
                rec = last(o.get("dir"), o["key"])
                live = rec if reviewed(rec) else None
                if grp == "lines":
                    o["decision"] = live["decision"] if live else None
                    o["suggested_value"] = live.get("suggested_value", "") if live and live.get("decision") == "suggest" else ""
                    o["reference"] = live.get("reference", "") if live and live.get("decision") == "suggest" else ""
                    o["decision_note"] = live.get("note", "") if live and live.get("decision") == "suggest" else ""
                else:
                    o["call"] = live.get("call") if live else None
                    o["call_note"] = live.get("note", "") if live else None
                    o["call_reference"] = live.get("reference", "") if live else ""
                o["reviewed"] = bool(live)
                o["decided_by"] = live.get("reviewer") if live else None
                o["decided_at"] = live.get("ts") if live else None
                flag(o.get("dir"), o["key"], o)
        rec = last(p.get("dir"), plant_flag_key(p.get("dir"), p["pid"]))
        live = rec if reviewed(rec) and rec.get("on") else None
        p["pm_flag"] = bool(live)
        p["pm_note"] = live.get("note", "") if live else ""
    return data


# ---- validation ------------------------------------------------------------------

def now():
    return datetime.now(ET).isoformat(timespec="seconds")


def index(data):
    """key -> (plant, object, group) for every line and item."""
    out = {}
    for p in data.get("plants", []):
        for grp in ("lines", "items"):
            for o in p.get(grp, []):
                out[o["key"]] = (p, o, grp)
    return out


def validate(records, data, reviewer=None):
    """Normalized decision records (ts stamped later), or Invalid; nothing is written for a bad
    request. A record is {key, decision, suggested_value?, note?} or {key, undo: true} (an undo
    is stored as undecided: true)."""
    if not isinstance(records, list) or not records:
        raise Invalid("expected a non-empty list of decision records")
    idx = index(data)
    out = []
    for i, r in enumerate(records):
        if not isinstance(r, dict):
            raise Invalid(f"record {i}: not an object")
        key = r.get("key")
        if key not in idx:
            raise Invalid(f"record {i}: unknown key {key!r}")
        plant, obj, grp = idx[key]
        if grp != "lines" or obj.get("kind") not in LINE_KINDS:
            raise Invalid(f"record {i}: {key!r} is an item, not a line (use /api/item)")
        undo = bool(r.get("undo") or r.get("undecided"))
        decision = r.get("decision")
        if undo and not decision:
            decision = obj.get("default") or "hold"      # an undo record still carries a decision field
        if not undo and not decision:
            raise Invalid(f"record {i}: no decision given (a bare key never defaults to accept)")
        if decision not in DECISIONS:
            raise Invalid(f"record {i}: decision {decision!r} is not one of {', '.join(sorted(DECISIONS))}")
        note = str(r.get("note") or "")
        sv = str(r.get("suggested_value") or "")
        ref = str(r.get("reference") or "").strip()
        if decision == "suggest" and not undo and not (sv.strip() or note.strip()):
            raise Invalid(f"record {i}: a suggestion needs a suggested_value or a note")
        if ref and not _URL_RE.match(ref):
            raise Invalid(f"record {i}: reference {ref!r} is not a web address (http or https)")
        out.append({"key": key, "dir": obj["dir"], "pid": plant["pid"], "record_id": obj.get("record_id"),
                    "column": obj.get("column") or "", "kind": obj["kind"],
                    "decision": decision, "suggested_value": sv, "reference": ref, "note": note,
                    "reviewer": reviewer, "ts": None, "undecided": undo})
    return out


_URL_RE = re.compile(r"^https?://\S+$")


def validate_flags(records, data, reviewer=None):
    """Normalized ask-the-PM flag records, or Invalid. A record is {key, on: bool, note?} where
    key is a line or item key, or {pid, dir, on, note?} for a whole plant. The stored key is
    "pm::" + the line/item key, or "pm::" + dir + "::plant:" + pid, so a flag never collides
    with the decision on the same record."""
    if not isinstance(records, list) or not records:
        raise Invalid("expected a non-empty list of flag records")
    idx = index(data)
    plants = {(p.get("dir"), p["pid"]): p for p in data.get("plants", [])}
    out = []
    for i, r in enumerate(records):
        if not isinstance(r, dict):
            raise Invalid(f"record {i}: not an object")
        on = bool(r.get("on", True))
        note = str(r.get("note") or "")
        key = r.get("key")
        if key:
            if key not in idx:
                raise Invalid(f"record {i}: unknown key {key!r}")
            plant, obj, grp = idx[key]
            out.append({"key": FLAG_PREFIX + key, "dir": obj["dir"], "pid": plant["pid"],
                        "record_id": obj.get("record_id"), "kind": obj.get("kind"), "flag": "pm", "on": on,
                        "note": note, "reviewer": reviewer, "ts": None, "undecided": False})
            continue
        pid, label = r.get("pid"), r.get("dir")
        plant = plants.get((label, pid)) or next((p for p in plants.values() if p["pid"] == pid), None)
        if plant is None:
            raise Invalid(f"record {i}: unknown plant {pid!r}")
        out.append({"key": plant_flag_key(plant["dir"], plant["pid"]), "dir": plant["dir"], "pid": plant["pid"],
                    "record_id": None, "kind": "plant", "flag": "pm", "on": on,
                    "note": note, "reviewer": reviewer, "ts": None, "undecided": False})
    return out


# ---- writing ---------------------------------------------------------------------

def atomic_write(path, text):
    path = Path(path)
    tmp = path.with_name(f".{path.name}.tmp")
    try:
        with open(tmp, "w", encoding="utf-8", newline="") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def append_jsonl(path, records):
    """Append records; returns the file's prior size so a failed step can roll it back."""
    path = Path(path)
    size = path.stat().st_size if path.exists() else 0
    with open(path, "a", encoding="utf-8", newline="") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())
    return size


def rollback(path, size):
    path = Path(path)
    if size == 0:
        path.unlink(missing_ok=True)
    else:
        with open(path, "r+b") as f:
            f.truncate(size)


def write_derived(d, ts):
    """Regenerate <d>/review_decisions.json from the whole log (latest record per key)."""
    body = {"generated": ts, "decisions": latest(read_log(d))}
    atomic_write(Path(d) / DERIVED_NAME, json.dumps(body, indent=1, ensure_ascii=False) + "\n")


def _write(recs, dirs):
    """Per touched dir (caller holds _LOCK): append to review_log.jsonl and regenerate
    review_decisions.json atomically; on failure roll every touched log back to its previous
    byte length. Returns recs with ts stamped."""
    ts = now()
    by_dir = {}
    for r in recs:
        r["ts"] = ts
        if r["dir"] not in dirs:
            raise Invalid(f"staging dir not known to the server: {r['dir']}")
        by_dir.setdefault(r["dir"], []).append(r)
    done = []          # (dir, log path, prior size) of dirs touched so far, for a multi-dir rollback
    try:
        for label, rs in by_dir.items():
            log = Path(dirs[label]) / LOG_NAME
            size = append_jsonl(log, rs)
            done.append((dirs[label], log, size))
            write_derived(dirs[label], ts)
    except Exception:
        for d, log, size in done:
            rollback(log, size)
        for d, log, size in done[:-1]:      # dirs whose derived file already moved: re-derive
            try:
                write_derived(d, ts)
            except Exception:
                pass
        raise
    return recs


def decide(records, data, reviewer, dirs=None, root=None):
    """Validate, then write (under the process lock) to each touched dir's sidecars. Returns
    the records written (with reviewer and ts)."""
    reviewer = initials(reviewer)
    dirs = dirs if dirs is not None else dir_paths(data, root)
    with _LOCK:
        return _write(validate(records, data, reviewer), dirs)


def validate_items(records, data, reviewer=None):
    """Normalized item call records, or Invalid. A record is {key, call, note?} or {key, undo: true}.
    The call must be in ITEM_CALLS for the item's kind."""
    if not isinstance(records, list) or not records:
        raise Invalid("expected a non-empty list of item records")
    idx = index(data)
    out = []
    for i, r in enumerate(records):
        if not isinstance(r, dict):
            raise Invalid(f"record {i}: not an object")
        key = r.get("key")
        if key not in idx:
            raise Invalid(f"record {i}: unknown key {key!r}")
        plant, obj, grp = idx[key]
        if grp != "items":
            raise Invalid(f"record {i}: {key!r} is a line, not an item (use /api/decide)")
        undo = bool(r.get("undo") or r.get("undecided"))
        call = "" if undo else str(r.get("call") or "")
        vocab = ITEM_CALLS.get(obj.get("kind"), OTHER_CALLS)
        if not undo and call not in vocab:
            raise Invalid(f"record {i}: call {call!r} is not one of {', '.join(vocab)} for a {obj.get('kind')} item")
        note = str(r.get("note") or "")
        if not undo and (obj.get("kind"), call) in NOTE_REQUIRED and not note.strip():
            raise Invalid(f"record {i}: {call.replace('_', ' ')} needs a note saying why")
        ref = str(r.get("reference") or "").strip()
        if ref and not _URL_RE.match(ref):
            raise Invalid(f"record {i}: reference {ref!r} is not a web address (http or https)")
        out.append({"key": key, "dir": obj["dir"], "pid": plant["pid"], "record_id": obj.get("record_id"),
                    "kind": obj["kind"], "call": call, "reference": ref, "note": note,
                    "reviewer": reviewer, "ts": None, "undecided": undo})
    return out


def record_items(records, data, reviewer, dirs=None, root=None):
    """Item calls into the SAME review_log.jsonl / review_decisions.json as line decisions (an item
    key and a line key never coincide). Returns the records written."""
    reviewer = initials(reviewer)
    dirs = dirs if dirs is not None else dir_paths(data, root)
    with _LOCK:
        return _write(validate_items(records, data, reviewer), dirs)


def record_flags(records, data, reviewer, dirs=None, root=None):
    """Ask-the-PM flags into the same log. Returns the records written."""
    reviewer = initials(reviewer)
    dirs = dirs if dirs is not None else dir_paths(data, root)
    with _LOCK:
        return _write(validate_flags(records, data, reviewer), dirs)

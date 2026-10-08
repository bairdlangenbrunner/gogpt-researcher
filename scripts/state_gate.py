#!/usr/bin/env python3
"""
Gate a US state batch before the deliverable is built. Read-only: it reports,
it never edits a shard or a staged file.

Contract: the Gate table in notes/us_state_agent_plan.md. Run after
assemble_state.py; it must print GATE CLEAN (exit 0) before
build_review_package.py.

    python state_gate.py --batch ../batches/us-md [--csv ...] \
        [--entity-check] [--entity-csv gem_export_gogpt.csv] [--no-qc] [--json]

Hard gates (any failure exits 1)
  coverage    every plant in briefs/_index.json has shards/<L...>.json that
              parses, has meta.done true, and reports every unit ID the index
              lists for it (a unit missing from the shard is silent loss)
  banned      no gem.wiki, globalenergymonitor.org or abarrelfull anywhere in
              any record's refs or verifications, any lane, case-insensitive.
              GEM-derived republishers cannot be detected mechanically; the
              reviewer still owns that check.
  verified    updates / newunits / newplants: every URL in refs has a
              verification with ok true. contains_value false is accepted only
              when researcher_notes is non-empty (the researcher explained the
              inference). Spreadsheet citations (URL ending .xlsx / .xls / .zip,
              or host eia.gov: EIA-860M, 860 and 923 files the verifier cannot
              text-match) are accepted when ok is true and researcher_notes is
              non-empty (the note quotes the matching row); they are listed on
              an informational line "spreadsheet citations confirmed by hand".
  orphans     every fields column has >=1 URL under its Data Source column
              (build_review_package.ref_col_for), and every refs key pairs with
              a fields column. Exempt: a value containing "inferred", and a
              delete record.
  fresh       every current[header] (and sibling_current[unit]) equals the
              export's cell for that unit, whitespace-normalized; a mismatch
              means the export changed after the shards were built
  headers     every fields key is an export header and not a read-only column
              (schema_constants.READ_ONLY_COLUMNS)
  cell-prose  a value holds a value: no "http", at most 120 characters, no
              sentence break (a lowercase word, a period, a space, a capital).
              Exempt columns: Status Detail, Latest Activity, Notes, Captive*,
              Equipment Manufacturer/Model.
  latest-activity
              a Latest Activity edit is only for a unit that is in development,
              shelved, or carries an inferred status (the export's Status, or
              the Status in the same batch), and its date is at least a year
              before today. A newer date means the project is moving and the
              field is not needed (docs/reference/lifecycle_rules.md).
  additive    Status Detail and Notes are running logs, newest entry first
              (Baird 2026-10-07): a staged value must end with the text the
              box already holds (whitespace-normalized), on this unit and on
              every sibling unit of a plant-wide edit, and a delete record may
              never name either column. assemble_state.py composes the value
              with build_review_package.additive_value.
  build       build_review_package.validate() on the lane files: the errors
              that would stop the build anyway (qa records with fields, etc.)
  qc_checks   qc_checks.py --staged on each lane file present must exit 0
              (skipped with --no-qc)

Advisory gates (reported, never fail the run)
  false-high    tier high on a Status change (current Status non-blank and
                different) with fewer than two distinct hosts among verified
                Status links
  independence  independent true with fewer than two verified links
  entities      with --entity-check: every proposed Owner(s) / Operator(s)
                name not already in the unit's current cell (share brackets
                stripped) is looked up with entity_lookup.lookup_local over the
                unfiltered export; not-found names are listed. Skipped cleanly
                without the flag or when the lookup cannot run.
  notes         researcher_notes or action containing repo jargon (lane,
                shard, tier, staged, ref, orphan, url_verifier, blue, green,
                yellow and the like) or an em dash, en dash or arrow;
                rewrite per docs/reference/notes_style.md
  concern-types a qa record whose concern_type is outside the vocabulary
                (a staged column name or one of review_app/checklist.py
                CONCERN_KINDS); assemble_state.py maps shard text onto it, so
                an offender here is text the mapping did not recognize
  monitor-fields
                a monitor record with no monitor_reason, no recheck_by, a
                recheck_by not of the form YYYY-MM, or a monitor_kind outside
                new_to_tracker / existing_plant

Output: one line per gate, `GATE <name> HARD|ADVISORY PASS|FAIL (n)`, then
up to 25 offenders (record_id and reason). Last line: `GATE CLEAN` or
`GATE FAILED: <names>`. --json prints the same result as JSON (exit code
unchanged).
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from review_app.checklist import CONCERN_VOCAB, MONITOR_KINDS  # noqa: E402
from assemble_state import (  # noqa: E402
    host_of, is_blank, load_export, load_index, norm_entities, norm_status,
    resolve_csv, ws)
from schema_constants import STATUSES_IN_DEVELOPMENT  # noqa: E402
from build_review_package import (  # noqa: E402
    additive_errors, load_lanes, ref_col_for, validate)
from schema_constants import ADDITIVE_TEXT_COLUMNS, READ_ONLY_COLUMNS  # noqa: E402

SCRIPTS = Path(__file__).resolve().parent
BANNED = ("gem.wiki", "globalenergymonitor.org", "abarrelfull")
VALUE_LANES = ("updates", "newunits", "newplants")
PROSE_OK = {"Status Detail", "Latest Activity", "Notes",
            "Equipment Manufacturer/Model"}
SENTENCE_RE = re.compile(r"(?<![A-Za-z])([a-z]{2,})[.!?]\s+[A-Z]")
ABBREVS = {"inc", "corp", "ltd", "co", "jr", "sr", "st", "mt", "no", "bros"}
JARGON_RE = re.compile(r"\b(lane|shard|tier|staged|stage|ref|refs|orphan|"
                       r"qa record|url_verifier|colmap|merge-never-replace|"
                       r"blue|green|yellow)\b", re.I)
DASH_RE = re.compile(r" — | – |->|→")
SPREADSHEET_EXT = (".xlsx", ".xls", ".zip")
CAP = 25


def rid_of(rec, lane, i):
    return rec.get("record_id") or f"{lane}[{i}]:{rec.get('gem_unit_id', '')}"


def iter_records(lanes, names=None):
    """Yield (lane, record_id, record) including newplants' unit sub-records."""
    for lane, recs in lanes.items():
        if names and lane not in names:
            continue
        for i, rec in enumerate(recs):
            rid = rid_of(rec, lane, i)
            yield lane, rid, rec
            for j, u in enumerate(rec.get("units") or []):
                yield lane, f"{rid}/unit[{j}]", u


def ref_urls(rec):
    refs = rec.get("refs") or {}
    if isinstance(refs, list):
        return [u for u in refs if ws(u)]
    return [u for us in refs.values() for u in (us or []) if ws(u)]


def is_spreadsheet(url):
    path = url.split("?", 1)[0].split("#", 1)[0].lower()
    return path.endswith(SPREADSHEET_EXT) or host_of(url).endswith("eia.gov")


def ok_urls(rec):
    return {v.get("url") for v in rec.get("verifications") or [] if v.get("ok")}


# ------------------------------------------------------------------ gates ---

def gate_coverage(batch, index):
    out = []
    for p in index["plants"]:
        pid = p["plant_id"]
        sp = batch / "shards" / f"{pid}.json"
        if not sp.exists():
            out.append((pid, "no shard file"))
            continue
        try:
            shard = json.loads(sp.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            out.append((pid, f"shard does not parse: {e}"))
            continue
        if (shard.get("meta") or {}).get("done") is not True:
            out.append((pid, "shard not marked done"))
        reported = {u.get("gem_unit_id") for u in shard.get("units") or []}
        for uid in p["unit_ids"]:
            if uid not in reported:
                out.append((pid, f"unit {uid} not reported in the shard"))
    return out


def gate_banned(lanes):
    out = []
    for lane, rid, rec in iter_records(lanes):
        strings = list(ref_urls(rec))
        for v in rec.get("verifications") or []:
            strings += [str(x) for x in v.values() if isinstance(x, str)]
        hits = sorted({s for s in strings for b in BANNED if b in s.lower()})
        for h in hits:
            out.append((rid, f"banned source: {h[:120]}"))
    return out


def gate_verified(lanes):
    out, by_hand = [], []
    for lane, rid, rec in iter_records(lanes, VALUE_LANES):
        notes = ws(rec.get("researcher_notes"))
        vers = rec.get("verifications") or []
        for u in ref_urls(rec):
            ok = [v for v in vers if v.get("url") == u and v.get("ok")]
            if not ok:
                out.append((rid, f"no passing verification for {u}"))
                continue
            if is_spreadsheet(u):
                if notes:
                    by_hand.append((rid, u))
                else:
                    out.append((rid, f"spreadsheet link with no note quoting "
                                     f"the matching row: {u}"))
                continue
            if all(v.get("contains_value") is False for v in ok) and not notes:
                out.append((rid, f"page does not state the value and no note "
                                 f"explains the inference: {u}"))
    return out, by_hand


def gate_orphans(lanes):
    out = []
    for lane, rid, rec in iter_records(lanes, VALUE_LANES):
        fields = rec.get("fields") or {}
        refs = rec.get("refs") or {}
        if isinstance(refs, list):
            out.append((rid, "refs is a list, not keyed by Data Source column"))
            continue
        for col, val in fields.items():
            if rec.get("delete") or "inferred" in str(val).lower():
                continue
            rc = ref_col_for(col)
            if not [u for u in refs.get(rc) or [] if ws(u)]:
                out.append((rid, f"{col} has a value but no link under {rc}"))
        paired = {ref_col_for(c) for c in fields}
        for rc, urls in refs.items():
            if rc not in paired and urls:
                out.append((rid, f"links under {rc} have no paired value"))
    return out


def gate_fresh(lanes, export):
    out = []
    for lane, rid, rec in iter_records(lanes, ("updates",)):
        uid = rec.get("gem_unit_id")
        cur = rec.get("current") or {}
        checks = [(uid, cur)]
        for sib, val in (rec.get("sibling_current") or {}).items():
            checks += [(sib, {h: val for h in cur})]
        for u, values in checks:
            row = export.get(u)
            if row is None:
                out.append((rid, f"unit {u} not in the export"))
                continue
            for h, v in values.items():
                if ws(v) != ws(row.get(h, "")):
                    out.append((rid, f"{u} {h}: record has {ws(v)!r}, export "
                                     f"has {ws(row.get(h, ''))!r}"))
    return out


def gate_headers(lanes, header):
    out, hset = [], set(header)
    for lane, rid, rec in iter_records(lanes, VALUE_LANES):
        for col in rec.get("fields") or {}:
            if col not in hset:
                out.append((rid, f"{col!r} is not an export header"))
            elif col in READ_ONLY_COLUMNS:
                out.append((rid, f"{col!r} is a read-only column"))
    return out


def prose_reason(col, val):
    if col in PROSE_OK or col.startswith("Captive"):
        return ""
    s = ws(val)
    if "http" in s.lower():
        return "contains a link"
    if len(s) > 120:
        return f"{len(s)} characters long"
    for m in SENTENCE_RE.finditer(s):
        if m.group(1).lower() not in ABBREVS:
            return "reads as a sentence"
    return ""


def gate_cell_prose(lanes):
    out = []
    for lane, rid, rec in iter_records(lanes, VALUE_LANES):
        for col, val in (rec.get("fields") or {}).items():
            why = prose_reason(col, val)
            if why:
                out.append((rid, f"{col} value {why}: {ws(val)[:80]!r}"))
    return out

DATE_RE = re.compile(r"^Year: \d{4}(, Month: \d{1,2}(, Day: \d{1,2})?)?$")
YEAR_COLS = ("Start year", "Retired year", "Cancellation year", "Planned retire")


def gate_dates(lanes):
    """Latest Activity is a date field in GEM (every value in the export reads
    'Year: 2024, Month: 6, Day: 17', month and day optional); the year columns
    hold a four-digit year. Free text in either is a value the web UI cannot take."""
    out = []
    for lane, rid, rec in iter_records(lanes, VALUE_LANES):
        for col, val in (rec.get("fields") or {}).items():
            v = ws(val)
            if not v:
                continue
            if col == "Latest Activity" and not DATE_RE.match(v):
                out.append((rid, f"Latest Activity is a date field; write Year: YYYY, Month: M, Day: D, not {v[:60]!r}"))
            elif col in YEAR_COLS and not re.fullmatch(r"\d{4}", v):
                out.append((rid, f"{col} must be a four-digit year, not {v[:40]!r}"))
    return out


def la_status_ok(status):
    s = ws(status).lower()
    return s in STATUSES_IN_DEVELOPMENT or s.startswith("shelved") or "inferred" in s


def gate_latest_activity(lanes, export, today=None):
    """Latest Activity tracks stalled projects only: units in development,
    shelved, or with an inferred status, and only once the newest report is
    more than a year old (docs/reference/lifecycle_rules.md)."""
    today = today or datetime.date.today()
    cutoff = today - datetime.timedelta(days=365)
    proposed = {}
    for lane, rid, rec in iter_records(lanes, VALUE_LANES):
        st = (rec.get("fields") or {}).get("Status")
        if st and rec.get("gem_unit_id"):
            proposed.setdefault(rec["gem_unit_id"], []).append(st)
    out = []
    for lane, rid, rec in iter_records(lanes, VALUE_LANES):
        fields = rec.get("fields") or {}
        v = ws(fields.get("Latest Activity"))
        m = DATE_RE.match(v) and re.findall(r"\d+", v)
        if not m:
            continue
        uid = rec.get("gem_unit_id")
        statuses = [fields.get("Status"), (export.get(uid) or {}).get("Status")]
        statuses += proposed.get(uid, [])
        statuses = [s for s in statuses if ws(s)]
        if not any(la_status_ok(s) for s in statuses):
            out.append((rid, "Latest Activity is only for units in development, shelved or "
                             f"with an inferred status; this unit is {ws(statuses[0]) if statuses else 'of unknown status'}"))
            continue
        nums = [int(x) for x in m] + [1, 1]
        try:
            day = datetime.date(nums[0], nums[1], nums[2])
        except ValueError:
            continue
        if day > cutoff:
            out.append((rid, f"Latest Activity {v!r} is less than a year old; the project "
                             "is still moving, so leave the field alone"))
    return out


def gate_additive(lanes):
    """Status Detail and Notes are running logs, newest entry first: a staged
    value is the new text placed above the text already in the box, which
    stays word for word on this unit and on every sibling unit of a plant-wide
    edit. Neither box is ever rewritten or cleared (Baird 2026-10-07)."""
    out = []
    for lane, rid, rec in iter_records(lanes, VALUE_LANES):
        if not any(c in (rec.get("fields") or {}) for c in ADDITIVE_TEXT_COLUMNS):
            continue
        for e in additive_errors(rec, rec, rid):
            out.append((rid, e.split(": ", 1)[1]))
    return out


def gate_build(lanes):
    return [("build", e) for e in validate(lanes)
            if " drops or rewrites the text already in the box" not in e
            and " is never cleared; new text is added above " not in e]


def gate_false_high(lanes):
    out = []
    for lane, rid, rec in iter_records(lanes, ("updates",)):
        fields, cur = rec.get("fields") or {}, rec.get("current") or {}
        if str(rec.get("tier", "")).lower() != "high" or "Status" not in fields:
            continue
        if is_blank(cur.get("Status")) or \
                norm_status(cur["Status"]) == norm_status(fields["Status"]):
            continue
        refs = (rec.get("refs") or {}).get(ref_col_for("Status")) or []
        good = ok_urls(rec)
        hosts = {host_of(u) for u in refs if u in good} - {""}
        if len(hosts) < 2:
            out.append((rid, f"high status change on {len(hosts)} host(s): "
                             f"{sorted(hosts)}"))
    return out


def gate_independence(lanes):
    out = []
    for lane, rid, rec in iter_records(lanes):
        if not rec.get("independent"):
            continue
        good = ok_urls(rec)
        n = len({u for u in ref_urls(rec) if u in good})
        if n < 2:
            out.append((rid, f"independent is true with {n} verified link(s)"))
    return out


def split_names(v):
    return [ws(re.sub(r"[\[(]\s*\d+(?:\.\d+)?\s*%\s*[\])]", "", p))
            for p in ws(v).split(";") if ws(p)]


def gate_entities(lanes, entity_csv):
    """-> (offenders, skip_reason or '')."""
    try:
        from entity_lookup import lookup_local
    except Exception as e:  # pragma: no cover
        return [], f"entity_lookup could not be imported ({e})"
    out, seen = [], set()
    for lane, rid, rec in iter_records(lanes, ("updates",)):
        if rec.get("reverified"):
            continue
        for col in ("Owner(s)", "Operator(s)"):
            val = (rec.get("fields") or {}).get(col)
            if is_blank(val):
                continue
            current = {n for n, _ in norm_entities((rec.get("current") or {})
                                                   .get(col, ""))}
            for name in split_names(val):
                if norm_entities(name)[0][0] in current or name in seen:
                    continue
                seen.add(name)
                try:
                    res = lookup_local(name, csv_path=str(entity_csv))
                except Exception as e:
                    return [], f"lookup failed ({type(e).__name__}: {e})"
                if res.get("result") != "found":
                    out.append((rid, f"{col} name not found in the export: "
                                     f"{name!r}"))
    return out, ""


def gate_notes(lanes):
    out = []
    for lane, rid, rec in iter_records(lanes):
        for key in ("researcher_notes", "action"):
            text = str(rec.get(key) or "")
            # a capitalized word followed by another one is a name
            # ("Green Rocks data center", "Blue Ridge"), not repo jargon
            words = sorted({m.group(0).lower() for m in JARGON_RE.finditer(text)
                            if not (m.group(0)[0].isupper()
                                    and re.match(r" [A-Z]", text[m.end():m.end() + 2]))})
            dashes = sorted(set(DASH_RE.findall(text)))
            if words:
                out.append((rid, f"{key} uses repo words: {', '.join(words)}"))
            if dashes:
                out.append((rid, f"{key} uses dashes or arrows: "
                                 f"{' '.join(repr(d) for d in dashes)}"))
    return out


def gate_concern_types(lanes):
    out = []
    for lane, rid, rec in iter_records(lanes, ("qa",)):
        ct = ws(rec.get("concern_type"))
        if ct not in CONCERN_VOCAB:
            out.append((rid, f"concern_type {ct!r} is outside the vocabulary"
                             + (f" (shard wrote {rec['concern_type_raw']!r})"
                                if rec.get("concern_type_raw") else "")))
    return out


def gate_monitor_fields(lanes):
    out = []
    for lane, rid, rec in iter_records(lanes, ("monitor",)):
        if not ws(rec.get("monitor_reason")):
            out.append((rid, "monitor_reason is empty"))
        rb = ws(rec.get("recheck_by"))
        if not rb:
            out.append((rid, "recheck_by is empty"))
        elif not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", rb):
            out.append((rid, f"recheck_by {rb!r} is not YYYY-MM"))
        if rec.get("monitor_kind") not in MONITOR_KINDS:
            out.append((rid, f"monitor_kind {rec.get('monitor_kind')!r} is not one of "
                             f"{' / '.join(MONITOR_KINDS)}"))
    return out


def gate_qc(staging):
    out, ran = [], []
    for p in sorted(staging.glob("staged_*.json")):
        r = subprocess.run([sys.executable, str(SCRIPTS / "qc_checks.py"),
                            "--staged", str(p)], cwd=SCRIPTS,
                           capture_output=True, text=True)
        ran.append((p.name, r.returncode))
        if r.returncode != 0:
            lines = [ln for ln in (r.stdout + r.stderr).splitlines()
                     if "ERROR" in ln or "Error" in ln or "Traceback" in ln]
            out.append((p.name, f"qc_checks exit {r.returncode}"))
            out += [(p.name, ln.strip()[:160]) for ln in lines[:5]]
    return out, ran


# ------------------------------------------------------------------- main ---

def run(args):
    batch = Path(args.batch).resolve()
    index = load_index(batch)
    staging = batch / "staging"
    lanes = load_lanes(staging) if staging.is_dir() else {}
    csv_path = resolve_csv(args.csv, index)
    ids = {u for p in index["plants"] for u in p["unit_ids"]}
    for _, _, rec in iter_records(lanes):
        ids.add(rec.get("gem_unit_id"))
        ids |= set(rec.get("sibling_unit_ids") or [])
    header, export = load_export(csv_path, ids)

    gates = []

    def add(name, hard, offenders, status=None, info=None):
        gates.append({"name": name, "hard": hard,
                      "status": status or ("FAIL" if offenders else "PASS"),
                      "count": len(offenders),
                      "offenders": [{"id": a, "reason": b} for a, b in offenders],
                      "info": info or []})

    add("coverage", True, gate_coverage(batch, index))
    add("banned", True, gate_banned(lanes))
    ver, by_hand = gate_verified(lanes)
    add("verified", True, ver,
        info=[f"spreadsheet citations confirmed by hand ({len(by_hand)})"])
    add("orphans", True, gate_orphans(lanes))
    add("fresh", True, gate_fresh(lanes, export))
    add("headers", True, gate_headers(lanes, header))
    add("cell-prose", True, gate_cell_prose(lanes))
    add("dates", True, gate_dates(lanes))
    add("latest-activity", True, gate_latest_activity(lanes, export))
    add("additive", True, gate_additive(lanes))
    add("build", True, gate_build(lanes))
    add("false-high", False, gate_false_high(lanes))
    add("independence", False, gate_independence(lanes))
    if args.entity_check:
        ent, skip = gate_entities(lanes, args.entity_csv)
        if skip:
            add("entities", False, [], status="SKIPPED", info=[f"skipped: {skip}"])
        else:
            add("entities", False, ent)
    else:
        add("entities", False, [], status="SKIPPED",
            info=["skipped: pass --entity-check to run the lookup"])
    add("notes", False, gate_notes(lanes))
    add("concern-types", False, gate_concern_types(lanes))
    add("monitor-fields", False, gate_monitor_fields(lanes))
    qc_ran = []
    if args.no_qc:
        add("qc_checks", True, [], status="SKIPPED", info=["skipped: --no-qc"])
    else:
        qc, qc_ran = gate_qc(staging)
        add("qc_checks", True, qc,
            status="FAIL" if any(rc for _, rc in qc_ran) else "PASS",
            info=[f"{name} exit {rc}" for name, rc in qc_ran])
        gates[-1]["count"] = sum(1 for _, rc in qc_ran if rc)

    failed = [g["name"] for g in gates if g["hard"] and g["status"] == "FAIL"]
    return {"batch": str(batch), "csv": str(csv_path),
            "lanes": {k: len(v) for k, v in lanes.items()},
            "spreadsheet_by_hand": [{"id": a, "url": b} for a, b in by_hand],
            "gates": gates, "failed": failed,
            "verdict": "CLEAN" if not failed else "FAILED"}


def report(res):
    print(f"state gate: {res['batch']}")
    print("  lane files: " + (", ".join(f"{k}={v}" for k, v in res["lanes"].items())
                              or "(none)"))
    for g in res["gates"]:
        kind = "HARD" if g["hard"] else "ADVISORY"
        print(f"GATE {g['name']} {kind} {g['status']} ({g['count']})")
        for line in g["info"]:
            print(f"    {line}")
        offs = g["offenders"]
        for o in offs[:CAP]:
            print(f"    {o['id']}: {o['reason']}")
        if len(offs) > CAP:
            print(f"    … and {len(offs) - CAP} more")
    print("GATE CLEAN" if not res["failed"]
          else f"GATE FAILED: {', '.join(res['failed'])}")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--batch", required=True)
    ap.add_argument("--csv", default=None,
                    help="fresh scoped export (default: _index.json csv, "
                         "else scripts/gem_export_gogpt_scoped.csv)")
    ap.add_argument("--entity-check", action="store_true")
    ap.add_argument("--entity-csv", default=str(SCRIPTS / "gem_export_gogpt.csv"),
                    help="export the entity lookup scans (default: the "
                         "unfiltered all-combustion export; entities are "
                         "shared across trackers)")
    ap.add_argument("--no-qc", action="store_true",
                    help="skip qc_checks.py --staged on the lane files")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    res = run(args)
    if args.json:
        print(json.dumps(res, indent=1, ensure_ascii=False))
    else:
        report(res)
    sys.exit(0 if not res["failed"] else 1)


if __name__ == "__main__":
    main()

"""
Build the batch deliverable pair — actions xlsx + evidence md — from the
staged-JSON lanes.

Reads `staged_<lane>.json` files (lanes: updates, qa, entity, monitor,
newplants, newunits — see docs/reference/staged_json_schema.md, THE contract)
from a staging dir and renders:

    gogpt_batch_<stamp>_<scope>_<mode>_actions.xlsx
    gogpt_batch_<stamp>_<scope>_<mode>_evidence.md

per docs/reference/workbook_conventions.md. The stamp is generated AT BUILD
TIME (America/New_York); an existing deliverable is never overwritten — every
rebuild is a new pair.

Hard guarantees enforced here:
  - read-only columns (schema_constants.READ_ONLY_COLUMNS) are never edit
    targets — a staged record touching one is a build ERROR
  - no orphan values/refs: every `fields` column needs its paired Data Source
    entry in `refs`, and vice versa (exception: a `delete: true` record, and a
    status proposal whose value contains "inferred" — inferences carry no ref
    by design, see confidence_tiers.md). A Status Detail link is keyed under
    "Status Detail" itself and written into the text, never merged into
    Status Data Source (schema_constants.INLINE_SOURCE_COLUMNS)
  - blocklist: gem.wiki / globalenergymonitor / abarrelfull / wikidot /
    theodora URLs anywhere in refs are a build ERROR
  - zero-verified-ref updates/newplants/newunits records (same exceptions)
    are a build ERROR — downgrade them to monitor/qa in staging instead

Run scripts/qc_checks.py --staged on each lane first; run scripts/recalc.py
on the built xlsx after.

Review decisions (--decisions): when the batch was reviewed in the review app
(review_app/), `<staging-dir>/review_log.jsonl` holds one call per record.
With --decisions, only ACCEPTED edit records (updates / newplants / newunits)
go into the workbook; held, rejected, suggested and not-yet-decided records
are left out and listed at the top of the evidence file with the reviewer's
note. Item records (qa / entity / monitor) are never cell edits, so they all
stay in the deliverable, each with the reviewer's call appended. Validation
runs on every staged record either way. A sidecar that is present but not
asked for is reported and ignored, so an unreviewed rebuild stays honest.

The IRP step (--irp, US states only): pass irp_sheet.py's JSON for the state
and the workbook gains two sheets. `irp_box` lists every record flagged `irp`
(its finding comes from a utility integrated resource plan) with the unit's
IRP box state read from the export (already ticked / not ticked / new row)
and the action to take in the web form, plus the units already ticked for
reference. `irp_notes_draft` has one row per utility on the US IRPs tab with
a draft Notes line for the batch; a person pastes it, the repo never writes
the tab. The evidence file gets a "Utility resource plans" section.

Usage (from scripts/):
    python build_review_package.py --staging-dir ../batches/nigeria/staging \
        --scope nigeria --mode update
    python build_review_package.py --staging-dir ../batches/us-ga/staging \
        --scope us-ga --mode update --decisions --irp ../work/irp_us-ga.json
    # add --dry-run to validate without writing files
"""
import argparse
import csv
import datetime
import json
import re
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from schema_constants import (ADDITIVE_TEXT_COLUMNS, INLINE_SOURCE_COLUMNS,
                              READ_ONLY_COLUMNS)
from colmap import load_colmap
from paths import gem_export_csv
from review_app.checklist import (OTHER, OPTIONAL_ROWS, WATCH_CALLS, group_label,
                                  groups_for, row_label, summarize, tag)

LANES = ["updates", "qa", "entity", "monitor", "newplants", "newunits"]

# The review page's calls on items, in the words the page shows (review_app/README.md).
CALL_LABELS = {"add_to_database": "incorporate into database", "hold": "hold",
               "possible_updates": "send to possible updates", "remove": "remove from watchlist",
               "confirmed": "confirmed", "dismissed": "dismissed", "needs_research": "needs research",
               "found": "found", "not_found": "not found", "ok": "ok"}

BLOCKLIST = ("gem.wiki", "globalenergymonitor", "abarrelfull", "wikidot",
             "theodora")

TIER_FILLS = {"high": "C6EFCE", "medium": "FFEB9C", "low": "FFC7CE",
              "reverified": "BDD7EE"}

SHEET_DESCRIPTIONS = {
    "checklist_summary": ("Start here. The QC/Country checklist groups of this batch: how many "
                          "edits and items sit under each group and each checkbox row, so "
                          "the batch can be ticked off box by box."),
    "edit_checklist": ("PRIMARY deliverable — one row per proposed cell edit "
                       "(current -> proposed), ordered plant -> unit -> column "
                       "the way the web UI is walked. Paste the value into the "
                       "column and the URLs into its Data Source column "
                       "(merge, never replace). 'done' column is yours. "
                       "checklist_group and checklist_rows say which checkbox "
                       "the edit helps tick."),
    "edit_backend_format": ("The updates-lane edits plus new plants/units "
                            "laid out in the export CSV's own table format: "
                            "one row per "
                            "affected unit, all 91 columns, in FINAL proposed "
                            "form. Colored cells are the changes (color = "
                            "confidence tier; blue = re-verified unchanged; "
                            "green+empty = staged deletion); Data Source "
                            "cells show existing URLs merged with the new "
                            "ones. Uncolored cells are untouched current "
                            "values."),
    "new_plants": "Candidate new plants (plant-level row, then its unit rows).",
    "new_units": "New units at existing plants (anchored to a T#### plant ID).",
    "entity_additions": ("New entities to create BEFORE plant edits that link "
                         "them. entity_lookup.py found no existing match."),
    "qa_review": "Read-and-flag concerns. Never a paste target.",
    "watch_new_to_tracker": ("Watch list, part 1: plants and projects GEM does not have yet "
                             "that did not clear the add threshold. Recheck by the date given. "
                             "Never a paste target."),
    "watch_existing_plants": ("Watch list, part 2: possible changes or expansions at plants "
                              "GEM already tracks, not yet confirmed. Never a paste target."),
    "promote_to_database": ("Watch items the reviewer marked 'incorporate into database'. "
                            "Each needs research and a full edit (a new row or a change) in "
                            "the next batch; build_state_brief.py --promote turns them into "
                            "tasks."),
    "possible_updates_rows": ("Watch items the reviewer sent to the possible-updates sheet, "
                              "laid out as rows to paste there."),
    "questions_for_pm": ("Everything the reviewer ticked 'ask the PM' on, with their note, "
                         "whatever its decision."),
    "irp_box": ("US only, when the IRP step ran (irp_sheet.py). Every edit, new row and item "
                "whose source is a utility integrated resource plan, with the utility it came "
                "from and whether the unit's IRP box in the database is already ticked. Tick the "
                "box in the web form on the rows that say so; units already ticked are listed "
                "for reference."),
    "irp_notes_draft": ("US only, when the IRP step ran. One row per utility on the US IRPs tab "
                        "for this state: the plan it lists, when the next one is due, and a "
                        "draft line for the tab's Notes column covering what this batch found. "
                        "Edit the draft, then paste it by hand; the repo never writes the tab."),
}

GROUP_PREFIX = "checklist group"


def load_lanes(staging_dir):
    lanes = {}
    for lane in LANES:
        p = staging_dir / f"staged_{lane}.json"
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
            lanes[lane] = data.get("records", data if isinstance(data, list) else [])
    return lanes


EDIT_LANES = ("updates", "newplants", "newunits")   # lanes whose records are cell edits


def load_decisions(staging_dir):
    """record_id -> the reviewer's latest call on it, from the review app's log in this
    staging dir (review_app/store.py writes it; the log is append-only and the last record
    per key speaks). None when the batch has no log."""
    log = staging_dir / "review_log.jsonl"
    if not log.exists():
        return None
    out = {}
    for line in log.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if rec.get("flag"):
            continue          # an ask-the-PM flag is not a decision (load_flags reads those)
        rid = rec.get("record_id") or rec.get("key", "").split("::", 1)[-1]
        if rid:
            out[rid] = rec
    return out


def load_flags(staging_dir):
    """record_id or plant id -> the latest live ask-the-PM flag record from the review app's
    log ({flag: "pm", on, note, ...}; store.validate_flags). Flags turned off again are
    dropped. {} when the batch has no log or no flags."""
    log = staging_dir / "review_log.jsonl"
    if not log.exists():
        return {}
    out = {}
    for line in log.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if not rec.get("flag"):
            continue
        rid = rec.get("record_id") or rec.get("pid") or ""
        if not rid:
            continue
        if rec.get("on") and not rec.get("undecided"):
            out[rid] = rec
        else:
            out.pop(rid, None)
    return out


def decision_of(rec, decisions):
    """'accept' | 'hold' | 'reject' | 'suggest' | 'undecided' for an edit record."""
    d = decisions.get(rec.get("record_id"))
    if not d or d.get("undecided") or "call" in d:
        return "undecided"
    return d.get("decision") or "undecided"


def call_of(rec):
    """The reviewer's call on an item record ('' when none)."""
    d = rec.get("review_call") or {}
    return str(d.get("call") or "") if not d.get("undecided") else ""


def apply_decisions(lanes, decisions):
    """Split the lanes by the reviewer's calls. Returns (kept_lanes, left_out, counts): kept
    has only accepted edit records (items untouched, each stamped with `review_call`); left_out
    is [(lane, record, decision record or None)] for every edit record not accepted and for
    every watch item the reviewer removed from the watch list (those leave the workbook too)."""
    kept, left_out = {}, []
    counts = {"accept": 0, "hold": 0, "reject": 0, "suggest": 0, "undecided": 0}
    for lane, recs in lanes.items():
        if lane in EDIT_LANES:
            keep = []
            for rec in recs:
                dec = decision_of(rec, decisions)
                counts[dec] += 1
                if dec == "accept":
                    keep.append(rec)
                else:
                    left_out.append((lane, rec, decisions.get(rec.get("record_id"))))
            kept[lane] = keep
        else:
            out = []
            for rec in recs:
                rec = dict(rec)
                d = decisions.get(rec.get("record_id"))
                if d and not d.get("undecided") and d.get("call"):
                    rec["review_call"] = d
                if lane == "monitor" and call_of(rec) == "remove":
                    left_out.append((lane, rec, d))
                    continue
                out.append(rec)
            kept[lane] = out
    return kept, left_out, counts


def describe_decision(d):
    """One plain sentence for the evidence file: who called what, when, and their note."""
    if not d or d.get("undecided"):
        return "not decided yet in the review app"
    if d.get("call"):
        return describe_call(d)
    who, when = d.get("reviewer") or "?", str(d.get("ts") or "")[:10]
    if d.get("decision") == "suggest":
        val = d.get("suggested_value") or ""
        txt = f"suggested by {who} on {when}" + (f": {val}" if val else " (note only)")
    else:
        verb = {"accept": "accepted", "hold": "held", "reject": "rejected"}.get(d.get("decision"), d.get("decision"))
        txt = f"{verb} by {who} on {when}"
    if d.get("note"):
        txt += f". {d['note']}"
    if d.get("reference"):
        txt += f" Source given: {d['reference']}"
    return txt


def describe_call(d):
    """The reviewer's call on an item in the review page's own words."""
    who, when = d.get("reviewer") or "?", str(d.get("ts") or "")[:10]
    call = str(d.get("call", ""))
    txt = f"{CALL_LABELS.get(call, call.replace('_', ' '))} by {who} on {when}"
    if d.get("note"):
        txt += f". {d['note']}"
    if d.get("reference"):
        txt += f" Source given: {d['reference']}"
    return txt


# ------------------------------------------------------- checklist groups ---

def is_us(lanes):
    return any(str(r.get("country", "")).strip().lower() == "united states"
               for recs in lanes.values() for r in recs)


def export_rows(export_csv, unit_ids):
    """{GEM unit ID: {header: cell}} for the units named, from the fresh export; {} when
    the export is not there. The header is read from the file, never assumed."""
    if not export_csv or not Path(export_csv).exists() or not unit_ids:
        return {}
    out = {}
    with open(export_csv, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if "GEM unit ID" not in (reader.fieldnames or []):
            return {}
        for row in reader:
            if row["GEM unit ID"] in unit_ids:
                out[row["GEM unit ID"]] = row
    return out


def tag_lanes(lanes, export_csv=None):
    """Sort every record into its QC/Country checklist group (review_app/checklist.py tag):
    each record gets `_tag` = {group, checks, group_label}. Returns the `us` flag the
    sort used. The export row of the unit (or of any unit of the plant) sharpens the
    sort; without the export the column and the value decide alone."""
    us = is_us(lanes)
    uids = {r.get("gem_unit_id") for recs in lanes.values() for r in recs if r.get("gem_unit_id")}
    rows = export_rows(export_csv, uids)
    by_plant = {}
    for row in rows.values():
        pid = row.get("GEM location ID") or row.get("GEM plant ID") or ""
        by_plant.setdefault(pid, row)
    for lane, recs in lanes.items():
        for r in recs:
            unit_row = rows.get(r.get("gem_unit_id") or "") or by_plant.get(r.get("gem_plant_id") or "") or {}
            r["_tag"] = tag(r, lane, unit_row=unit_row, us=us)
    return us


def group_cell(rec):
    """'3. Status and timeline' for the workbook; 'Other' for the catch-all."""
    t = rec.get("_tag") or {}
    g = t.get("group", OTHER)
    return "Other" if g == OTHER else f"{g}. {t.get('group_label') or group_label(g)}"


def rows_cell(rec):
    """'10, 24' : the checkbox rows (tab row numbers) the record helps tick."""
    return ", ".join(str(c) for c in (rec.get("_tag") or {}).get("checks", []))


def group_sort_key(rec):
    g = (rec.get("_tag") or {}).get("group", OTHER)
    return (1, 0) if g == OTHER else (0, int(g))


def checklist_summary_rows(lanes, us):
    """Rows for the checklist_summary sheet: one block per group (its count of edits and of
    items), then one row per checkbox of the group with how many records serve it."""
    tags_edit = [r["_tag"] for lane in EDIT_LANES for r in lanes.get(lane, []) if "_tag" in r]
    tags_item = [r["_tag"] for lane in ("qa", "entity", "monitor") for r in lanes.get(lane, [])
                 if "_tag" in r]
    out = []
    for g_e in summarize(tags_edit + tags_item, us):
        gid = g_e["id"]
        n_edit = sum(1 for t in tags_edit if t["group"] == gid)
        n_item = sum(1 for t in tags_item if t["group"] == gid)
        name = "Other" if gid == OTHER else f"{gid}. {g_e['label']}"
        if g_e.get("panel"):
            out.append([name, "", "", "", "", g_e["blurb"] + " Ticked by hand at close-out; "
                        "validation_report.py --closeout and no_tracker.py cover rows 54 and 56."])
            continue
        out.append([name, "", "", n_edit, n_item, g_e["blurb"]])
        for row in g_e["rows"]:
            out.append(["", row["row"], row["label"], "", row["count"], ""])
    return out


def monitor_kind(rec):
    k = rec.get("monitor_kind")
    if k in ("new_to_tracker", "existing_plant"):
        return k
    return "existing_plant" if str(rec.get("gem_plant_id") or "").strip() else "new_to_tracker"


def find_record(all_lanes, record_id):
    for lane in LANES:
        for r in all_lanes.get(lane, []):
            if r.get("record_id") == record_id:
                return lane, r
    return None, None


def pm_question_rows(all_lanes, flags):
    """Rows for questions_for_pm from the ask-the-PM flags (load_flags): the record or the
    plant flagged, what it is, the reviewer's note, who and when."""
    out = []
    for rid, f in flags.items():
        lane, rec = find_record(all_lanes, rid)
        who, when = f.get("reviewer") or "?", str(f.get("ts") or "")[:10]
        if rec is None:
            # a whole-plant flag: rid is the GEM location id, or "new:<slug>" for a plant
            # GEM does not have yet (review_data.candidate_key)
            slug = rid.split(":", 1)[1] if rid.startswith("new:") else None

            def is_plant(r):
                if r.get("gem_plant_id") == rid:
                    return True
                if slug is None:
                    return False
                base = re.sub(r"\s*\([^)]*\)", "", str(r.get("plant_name") or "")).lower()
                return re.sub(r"[^a-z0-9]+", "-", base).strip("-") == slug
            plant = next((r for recs in all_lanes.values() for r in recs if is_plant(r)), None) or {}
            out.append([plant.get("country", ""), plant.get("plant_name", "") or rid, "", rid, "",
                        "the whole plant", "", "", f.get("note", ""), who, when])
            continue
        if lane in EDIT_LANES:
            what = "; ".join(f"{c}: {(rec.get('current') or {}).get(c, '')!s} -> {v!s}"
                             for c, v in (rec.get("fields") or {}).items())
            kind = {"updates": "a change", "newplants": "a new plant", "newunits": "a new unit"}[lane]
        elif lane == "qa":
            what = rec.get("recommendation") or rec.get("researcher_notes") or ""
            kind = "a question about existing data"
        elif lane == "monitor":
            what = rec.get("monitor_reason") or rec.get("item") or ""
            kind = ("a watch item, new to the tracker" if monitor_kind(rec) == "new_to_tracker"
                    else "a watch item at an existing plant")
        else:
            what = f"{rec.get('role', '')}: {rec.get('entity_name', '')}"
            kind = "a new owner or operator to create"
        out.append([rec.get("country", ""), rec.get("plant_name", ""), rec.get("unit_name", ""),
                    rec.get("gem_plant_id", ""), rec.get("gem_unit_id", ""), kind, what,
                    group_cell(rec), f.get("note", ""), who, when])
    out.sort(key=lambda r: (r[0], r[1], r[2]))
    return out


def load_irp(irp_path, staging_dir=None):
    """The IRP step's findings for the workbook: irp_sheet.py's JSON (utilities, their plants,
    the units whose IRP box is ticked in the export) plus, when the assembler wrote it, the
    staging dir's irp_summary.json. None when no file is given. A missing file is an error:
    the flag says the step ran."""
    if not irp_path:
        return None
    path = Path(irp_path)
    if not path.exists():
        sys.exit(f"ERROR: --irp file not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    summary = {}
    if staging_dir is not None:
        sp = Path(staging_dir) / "irp_summary.json"
        if sp.exists():
            summary = json.loads(sp.read_text(encoding="utf-8"))
    return {"data": data, "summary": summary, "path": str(path)}


def irp_utility_of(irp, rec):
    """The utility row of the US IRPs tab a record belongs to: by GEM plant id first, then by
    one of the record's links being one of the utility's plan links. '' when none."""
    data = irp["data"]
    pid = str(rec.get("gem_plant_id") or "").strip()
    links = {u.rstrip("/") for us in (rec.get("refs") or {}).values()
             for u in (us if isinstance(us, list) else [us])}
    for unit in rec.get("units") or []:
        links |= {u.rstrip("/") for us in (unit.get("refs") or {}).values()
                  for u in (us if isinstance(us, list) else [us])}
    for row in data.get("utilities") or []:
        if pid and any(p.get("plant_id") == pid for p in row.get("plants") or []):
            return row.get("utility") or ""
    for row in data.get("utilities") or []:
        if links & {l.rstrip("/") for l in row.get("links") or []}:
            return row.get("utility") or ""
    return ""


def irp_box_rows(lanes, irp, export_csv=None):
    """Rows for the irp_box sheet: every record flagged `irp` (its finding comes from a
    utility resource plan), with the unit's IRP box state read from the export, then the
    units already ticked that the batch did not touch, for reference."""
    data = irp["data"]
    ticked = {u.get("unit_id"): u for u in data.get("irp_units") or [] if u.get("unit_id")}
    uids = {r.get("gem_unit_id") for recs in lanes.values() for r in recs if r.get("gem_unit_id")}
    rows_export = export_rows(export_csv, uids)
    out, seen = [], set()
    for lane in LANES:
        for rec in lanes.get(lane, []):
            if not rec.get("irp"):
                continue
            uid = rec.get("gem_unit_id") or ""
            row = rows_export.get(uid) or {}
            box = str(row.get("IRP") or "").strip().lower()
            if lane in ("newplants", "newunits"):
                state, action = "new row", "tick the IRP box on the new row when it is created"
            elif uid in ticked or box == "yes":
                state, action = "already ticked", "nothing to tick; keep the IRP box as it is"
            elif box == "no" or row:
                state, action = "not ticked", "tick the IRP box on this unit in the web form"
            else:
                state, action = "unknown (unit not in the export)", "open the unit in the web form and tick the IRP box if it is not"
            if lane in EDIT_LANES:
                what = "; ".join(f"{c}: {v!s}" for c, v in (rec.get("fields") or {}).items()) or record_word(lane, rec)
                for u in rec.get("units") or []:
                    what += "; " + "; ".join(f"{u.get('unit_name', '?')} {c}: {v!s}" for c, v in (u.get("fields") or {}).items())
            elif lane == "qa":
                what = rec.get("recommendation") or rec.get("researcher_notes") or record_word(lane, rec)
            elif lane == "monitor":
                what = rec.get("monitor_reason") or rec.get("item") or record_word(lane, rec)
            else:
                what = f"{rec.get('role', '')}: {rec.get('entity_name', '')}"
            out.append([rec.get("country", ""), rec.get("plant_name", ""), rec.get("unit_name", ""),
                        rec.get("gem_plant_id", ""), uid, record_word(lane, rec), what,
                        irp_utility_of(irp, rec), state, action, group_cell(rec), rows_cell(rec)])
            seen.add(uid)
    for uid, u in sorted(ticked.items(), key=lambda kv: (kv[1].get("plant_name") or "", kv[1].get("unit_name") or "")):
        if uid in seen:
            continue
        out.append([(data.get("where") or {}).get("country") or "United States", u.get("plant_name", ""), u.get("unit_name", ""), u.get("plant_id", ""), uid,
                    "unit already in the database", f"status {u.get('status', '')}, {u.get('capacity_mw', '')} MW",
                    u.get("matched_utility", ""), "already ticked", "for reference: the box is ticked in the export, nothing to do",
                    "", "37"])
    return out


IRP_BOX_HEADER = ["country", "plant", "unit", "gem_plant_id", "gem_unit_id", "what_it_is", "what",
                  "utility", "irp_box_now", "action", "checklist_group", "checklist_rows"]


def irp_notes_rows(lanes, irp, quarter=None):
    """Rows for irp_notes_draft: one per utility row of the tab for this state, with a draft
    Notes line in the tab's own 'Q4 2026 ...' style that says what the batch staged from the plan."""
    data = irp["data"]
    quarter = quarter or f"Q{(datetime.date.today().month - 1) // 3 + 1} {datetime.date.today().year}"
    staged = {}
    for lane in LANES:
        for rec in lanes.get(lane, []):
            if rec.get("irp"):
                staged.setdefault(irp_utility_of(irp, rec), []).append((lane, rec))
    out = []
    for row in data.get("utilities") or []:
        util = row.get("utility") or ""
        plans = staged.get(util, [])
        parts = []
        for lane, rec in plans:
            name = rec.get("plant_name") or rec.get("unit_name") or "?"
            if lane in ("newplants", "newunits"):
                parts.append(f"new row for {name}")
            elif lane == "updates":
                cols = ", ".join((rec.get("fields") or {}).keys())
                parts.append(f"{name} ({cols})" if cols else name)
            elif lane == "monitor":
                parts.append(f"{name} on the watch list")
            elif lane == "qa":
                parts.append(f"a question about {name}")
        plan = row.get("irp_year") or "the plan"
        draft = (f"{quarter}: read {plan}" + (" (draft)" if row.get("is_draft") else "") + ". ")
        if parts:
            draft += "Staged in this batch: " + "; ".join(parts) + "."
        else:
            n = len(row.get("plants") or [])
            draft += (f"No new gas project in the plan beyond the {n} plant{'s' if n != 1 else ''} already tracked."
                      if n else "No gas project in the plan is tracked yet; nothing new found.")
        latest = row.get("latest_note") or ""
        if isinstance(latest, dict):
            latest = " ".join(x for x in (latest.get("quarter"), latest.get("text")) if x)
        out.append([util, row.get("irp_year", ""), "yes" if row.get("is_draft") else "",
                    "; ".join(row.get("links") or []), row.get("next_irp_due", ""),
                    latest, len(plans), draft])
    return out


IRP_NOTES_HEADER = ["utility", "irp_year", "is_draft", "plan_links", "next_irp_due",
                    "latest_note_on_tab", "records_from_this_plan", "draft_notes_line"]


def ref_col_for(value_col):
    """Pair a value column with its Data Source column per the export layout.
    A column in INLINE_SOURCE_COLUMNS (Status Detail) is its own source: the
    link is written into its text."""
    if value_col in INLINE_SOURCE_COLUMNS:
        return value_col
    special = {
        "Status": "Status Data Source",
        "City": "Location Data Source",
        "Capacity (MW)": "Capacity Data Source",
        "Number Of Engines": "Capacity Data Source",
        "Capacity Per Engine": "Capacity Data Source",
        "Fuel": "Fuel Data Source",
        "Turbine/Engine Technology": "Turbine/Engine Technology Data Source",
        "Equipment Manufacturer/Model": "Turbine/Engine Equipment Data Source",
        "Start year": "Start Year Data Source",
        "Retired year": "Retired Year Data Source",
        "Planned retire": "Planned Retire Data Source",
        "Cancellation year": "Cancellation year Data Source",
        "Latest Activity": "Latest Activity Data Source",
        "Operator(s)": "Operators Data Source",
        "Owner(s)": "Owners Data Source",
        "CHP": "CHP Data Source",
        "CCS attachment?": "CCS Data Source",
        "Latitude": "Location Data Source",
        "Longitude": "Location Data Source",
        "Location accuracy": "Location Data Source",
        "Disrupted by conflict": "Disrupted by conflict Data Source",
        "Captive industry use": "Captive Data Source",
        "Captive industry type": "Captive Data Source",
        "Captive non-industry use": "Captive Data Source",
        "Employment Notes": "Employment Notes Data Source",
        "Conversion/replacement?": "Conversion/replacement Data Source",
    }
    return special.get(value_col, f"{value_col} Data Source")


URL_RE = re.compile(r"https?://\S+")


def inline_value(text, urls):
    """A Status Detail entry with its source links written in, GEM style:
    "Permit application not yet filed: https://...". Links the text already
    holds are not repeated."""
    text = str(text or "").strip()
    new = [u for u in urls if u and u not in text]
    if not new:
        return text
    return f"{text.rstrip(' .:;')}: {', '.join(new)}" if text else ", ".join(new)


# words in a researcher note that mean the source does not settle the value
CAVEAT_RE = re.compile(r"\b(conflict\w*|contest\w*|differ\w*|disagree\w*|impl(?:y|ies|ied)|"
                       r"unclear|uncertain|not sure|may be|might be)\b", re.I)


def validated_tier(field, verdict, tier, urls, verifications, notes=""):
    """One fully validated source is green (confidence_tiers.md, the
    pipelines-researcher rule of 2026-09-30, Baird 2026-10-02 and 2026-10-08).
    A `medium` record is promoted to `high` when one of its links has a
    verification that loaded (`ok`), names the plant (`name_found`) and states
    the value (`contains_value`). A Status change is never promoted: it needs
    two independent publishers. Status Detail is not a Status change, so it
    follows the one-source rule. `low` is the researcher's call that the
    source is weak and is never promoted, and neither is a record whose note
    says the sources disagree or the value is only implied (CAVEAT_RE): that
    is what medium is for. Returns the tier."""
    tier = str(tier or "medium").lower()
    if tier != "medium" or (field == "Status" and verdict == "change") \
            or CAVEAT_RE.search(str(notes or "")):
        return tier
    urls = set(urls or [])
    for v in verifications or []:
        if v.get("url") in urls and v.get("ok") and v.get("name_found") is True \
                and v.get("contains_value") is True:
            return "high"
    return tier


def is_inferred_only(rec):
    fields = rec.get("fields", {})
    status = str(fields.get("Status", "")) + str(fields.get("Status Detail", ""))
    return "inferred" in status.lower()


def _ws(v):
    return re.sub(r"\s+", " ", str(v or "")).strip()


def additive_value(new, current):
    """The cell to paste for Status Detail or Notes (schema_constants
    ADDITIVE_TEXT_COLUMNS). Both boxes are running logs in the GEM web form,
    newest entry first (Baird 2026-10-07): the new text goes on its own line
    above the existing text, and the existing text stays word for word. When
    the box already says what the new text says, the box comes back unchanged
    so the caller can treat it as a match."""
    new = str(new or "").strip()
    current = str(current or "").strip()
    if not current:
        return new
    if not new or _ws(new).lower() in _ws(current).lower():
        return current
    return f"{new}\n{current}"


def additive_errors(rec, r, ident):
    """Why a Status Detail or Notes edit breaks the additive rule, if it does:
    the record clears the box, or the proposed text does not end with the text
    already there (on this unit, and on every sibling unit of a plant-wide
    edit)."""
    out = []
    fields = r.get("fields", {})
    for col in ADDITIVE_TEXT_COLUMNS:
        if col not in fields:
            continue
        if rec.get("delete"):
            out.append(f"{ident}: {col} is never cleared; new text is added above "
                       "the existing text")
            continue
        new = _ws(fields[col])
        olds = {"": _ws(r.get("current", {}).get(col, ""))}
        for uid, v in (r.get("sibling_current") or {}).items():
            olds[uid] = _ws(v)
        for uid, old in olds.items():
            if old and not new.endswith(old):
                out.append(f"{ident}: {col}{' of ' + uid if uid else ''} drops or "
                           "rewrites the text already in the box; the new text goes "
                           "above it and the old text stays word for word")
    return out


def validate(lanes):
    errors = []
    for lane in ("updates", "newplants", "newunits"):
        for i, rec in enumerate(lanes.get(lane, [])):
            ident = rec.get("gem_unit_id") or rec.get("plant_name") or f"{lane}[{i}]"
            recs = [rec] + rec.get("units", [])
            for r in recs:
                for col in r.get("fields", {}):
                    if col in READ_ONLY_COLUMNS:
                        errors.append(f"{ident}: staged edit to READ-ONLY column {col!r}")
                errors += additive_errors(rec, r, ident)
                urls = [u for us in r.get("refs", {}).values() for u in us]
                for u in urls:
                    if any(b in u.lower() for b in BLOCKLIST):
                        errors.append(f"{ident}: blocklisted URL {u}")
                exempt = rec.get("delete") or is_inferred_only(r)
                if r.get("fields") and not urls and not exempt:
                    errors.append(f"{ident}: proposes values with zero refs "
                                  "(downgrade to monitor/qa, or mark delete/inferred)")
                verified = {v.get("url") for v in r.get("verifications", [])
                            if v.get("ok")}
                for u in urls:
                    if u not in verified:
                        errors.append(f"{ident}: ref URL not verified: {u}")
    for i, rec in enumerate(lanes.get("qa", [])):
        if rec.get("fields"):
            ident = rec.get("gem_unit_id") or f"qa[{i}]"
            errors.append(f"{ident}: qa records must not propose edits (fields non-empty)")
    return errors


def checklist_rows(lanes):
    rows = []
    for rec in lanes.get("updates", []):
        base = [rec.get("country", ""), rec.get("plant_name", ""),
                rec.get("unit_name", ""), rec.get("gem_plant_id", ""),
                rec.get("gem_unit_id", "")]
        for col, proposed in rec.get("fields", {}).items():
            refs = rec.get("refs", {}).get(ref_col_for(col), [])
            tier = ("reverified" if str(proposed) ==
                    str(rec.get("current", {}).get(col, object()))
                    else rec.get("tier", "medium"))
            if rec.get("delete"):
                proposed = "(DELETE — value unsupported)"
                tier = "high"
            rows.append(base + [col, rec.get("current", {}).get(col, ""),
                                proposed, tier, "; ".join(refs),
                                rec.get("action", ""), group_cell(rec), rows_cell(rec), ""])
    rows.sort(key=lambda r: (r[0], r[1], r[2], r[5]))
    return rows


CHECKLIST_HEADER = ["country", "plant", "unit", "gem_plant_id", "gem_unit_id",
                    "column", "current", "proposed", "confidence", "refs_to_paste",
                    "action", "checklist_group", "checklist_rows", "done"]


def _split_urls(cell):
    """Split an export Data Source cell into its URLs (', ' / ';' separated)."""
    return [u for u in (p.strip() for p in re.split(r"[;,]\s*", cell or "")) if u]


def backend_format_rows(lanes, export_csv):
    """The updates/newplants/newunits lanes rendered as full export-layout rows
    (edit_backend_format).

    One row per affected unit, every export column, in FINAL proposed form:
    staged values applied, Data Source cells merged (existing URLs kept, new
    ones appended — merge-never-replace). New plants/units start from a blank
    row (country filled from the record), one row per staged unit with the
    plant-level fields duplicated across its unit rows, mirroring how the
    export lays plants out. Returns (header, rows, fills) where fills maps
    (row_index, col_index) -> tier key for coloring.
    """
    updates = lanes.get("updates", [])
    new_recs = lanes.get("newplants", []) + lanes.get("newunits", [])
    if not (updates or new_recs):
        return None, [], {}
    colmap = load_colmap(export_csv)
    header = colmap["_header_columns"]
    col_idx = {h: i for i, h in enumerate(header)}
    i_uid = col_idx["GEM unit ID"]

    wanted = {r.get("gem_unit_id") for r in updates if r.get("gem_unit_id")}
    current_rows = {}
    with open(export_csv, encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) > i_uid and row[i_uid] in wanted:
                current_rows[row[i_uid]] = row

    rows, fills = [], {}
    for rec in sorted(updates, key=lambda r: (r.get("country", ""),
                                              r.get("plant_name", ""),
                                              r.get("unit_name", ""))):
        uid = rec.get("gem_unit_id", "")
        base = current_rows.get(uid)
        if base is None:
            print(f"  WARNING: {uid}: not in export CSV — "
                  "edit_backend_format row built from staged fields only")
            base = [""] * len(header)
            if uid and "GEM unit ID" in col_idx:
                base[i_uid] = uid
        row = list(base)
        r_i = len(rows)
        for col, proposed in rec.get("fields", {}).items():
            if col not in col_idx:
                print(f"  WARNING: {uid}: column {col!r} not in export header — "
                      "skipped in edit_backend_format")
                continue
            c_i = col_idx[col]
            current = rec.get("current", {}).get(col, base[c_i])
            if rec.get("delete"):
                row[c_i] = ""
                tier = "high"          # green + empty = staged deletion
            else:
                row[c_i] = proposed
                tier = ("reverified" if str(proposed) == str(current)
                        else rec.get("tier", "medium"))
            fills[(r_i, c_i)] = tier
            ref_col = ref_col_for(col)
            new_urls = rec.get("refs", {}).get(ref_col, [])
            if new_urls and ref_col in col_idx and ref_col != col:
                ds_i = col_idx[ref_col]
                merged = _split_urls(row[ds_i])
                merged += [u for u in new_urls if u not in merged]
                row[ds_i] = ", ".join(merged)
                fills[(r_i, ds_i)] = tier
        rows.append(row)

    def apply_staged(row, r_i, fields, refs, tier, ident):
        for col, val in fields.items():
            if col not in col_idx:
                print(f"  WARNING: {ident}: column {col!r} not in export "
                      "header — skipped in edit_backend_format")
                continue
            row[col_idx[col]] = val
            fills[(r_i, col_idx[col])] = tier
        for ref_col, urls in refs.items():
            if ref_col in INLINE_SOURCE_COLUMNS:
                continue        # the link is already in the text of the box
            if ref_col not in col_idx:
                print(f"  WARNING: {ident}: column {ref_col!r} not in export "
                      "header — skipped in edit_backend_format")
                continue
            ds_i = col_idx[ref_col]
            merged = _split_urls(row[ds_i])
            merged += [u for u in urls if u not in merged]
            row[ds_i] = ", ".join(merged)
            fills[(r_i, ds_i)] = tier

    for rec in sorted(new_recs, key=lambda r: (r.get("country", ""),
                                               r.get("plant_name", ""),
                                               r.get("unit_name", ""))):
        ident = rec.get("plant_name", "?")
        tier = rec.get("tier", "medium")
        base = [""] * len(header)
        # Identity columns come from the record itself, not from `fields`,
        # so the row is readable on its own (the export calls the plant ID
        # column "GEM location ID"; older exports said "GEM plant ID").
        for col, val in (("Country/Area", rec.get("country")),
                         ("Plant name", rec.get("plant_name")),
                         ("GEM location ID", rec.get("gem_plant_id")),
                         ("GEM plant ID", rec.get("gem_plant_id"))):
            if val and col in col_idx:
                base[col_idx[col]] = val
        for unit in rec.get("units") or [None]:
            row = list(base)
            r_i = len(rows)
            unit_name = (unit or rec).get("unit_name")
            if unit_name and "Unit name" in col_idx:
                row[col_idx["Unit name"]] = unit_name
            apply_staged(row, r_i, rec.get("fields", {}),
                         rec.get("refs", {}), tier, ident)
            if unit is not None:
                apply_staged(row, r_i, unit.get("fields", {}),
                             unit.get("refs", {}), tier,
                             f"{ident} / {unit.get('unit_name', '?')}")
            rows.append(row)
    return header, rows, fills


def build_xlsx(lanes, out_path, export_csv=None, flags=None, all_lanes=None, irp=None):
    """Write the actions workbook. `lanes` are the records that go in (after the review's
    decisions when --decisions); `all_lanes` are every staged record, used to look up what an
    ask-the-PM flag points at; `flags` is load_flags() (None: no questions_for_pm sheet);
    `irp` is load_irp() (None: no irp_box / irp_notes_draft sheets)."""
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill

    us = tag_lanes(lanes, export_csv)
    if all_lanes is not None and all_lanes is not lanes:
        tag_lanes(all_lanes, export_csv)
    wb = Workbook()
    bold = Font(bold=True)

    def add_sheet(name, header, rows, tier_col=None):
        if not rows:
            return
        ws = wb.create_sheet(name)
        ws.append(header)
        for c in ws[1]:
            c.font = bold
        for row in rows:
            ws.append(row)
            if tier_col is not None:
                tier = row[tier_col]
                fill = TIER_FILLS.get(str(tier).lower())
                if fill:
                    for j in (tier_col + 1, tier_col + 2):  # proposed + tier cells
                        ws.cell(row=ws.max_row, column=j - 0).fill = \
                            PatternFill("solid", fgColor=fill)
        for col_cells in ws.columns:
            width = min(60, max(10, max(len(str(c.value or "")) for c in col_cells) + 2))
            ws.column_dimensions[col_cells[0].column_letter].width = width

    # README first
    ws = wb.active
    ws.title = "README"
    ws.append(["GOGPT batch deliverable — see docs/reference/workbook_conventions.md"])
    ws["A1"].font = bold
    ws.append([])
    ws.append(["Color legend (per cell):"])
    for tier, hexcode in TIER_FILLS.items():
        ws.append(["", tier])
        ws.cell(row=ws.max_row, column=2).fill = PatternFill("solid", fgColor=hexcode)
    ws.append([])
    ws.append(["Sheets in this workbook:"])
    for name, desc in SHEET_DESCRIPTIONS.items():
        ws.append(["", name, desc])
    ws.append([])
    ws.append(["Read-only columns are never edit targets; Data Source cells are "
               "merge-never-replace; URLs go ONLY in Data Source columns."])
    ws.append(["Every row names the group of the GOGPT QC/Country checklist it belongs to "
               "(checklist_group) and the checkbox rows of that tab it helps tick "
               "(checklist_rows, the tab's row numbers)."])
    ws.column_dimensions["B"].width = 22
    ws.column_dimensions["C"].width = 100

    add_sheet("checklist_summary",
              ["checklist_group", "row", "checkbox", "edits", "items", "about"],
              checklist_summary_rows(lanes, us))

    add_sheet("edit_checklist", CHECKLIST_HEADER, checklist_rows(lanes), tier_col=7)

    # edit_backend_format: updates lane in the export CSV's own table layout,
    # per-cell tier coloring (workbook_conventions.md).
    if export_csv is not None:
        bf_header, bf_rows, bf_fills = backend_format_rows(lanes, export_csv)
        if bf_rows:
            ws = wb.create_sheet("edit_backend_format")
            ws.append(bf_header)
            for c in ws[1]:
                c.font = bold
            for r_i, row in enumerate(bf_rows):
                ws.append(row)
                for c_i in range(len(row)):
                    tier = bf_fills.get((r_i, c_i))
                    if tier:
                        ws.cell(row=r_i + 2, column=c_i + 1).fill = \
                            PatternFill("solid", fgColor=TIER_FILLS[tier])
            ws.freeze_panes = "A2"
            for i, h in enumerate(bf_header, start=1):
                letter = ws.cell(row=1, column=i).column_letter
                ws.column_dimensions[letter].width = min(
                    32, max(10, len(str(h)) + 2))

    def all_refs(rec):
        return "; ".join(u for us_ in rec.get("refs", {}).values()
                         for u in (us_ if isinstance(us_, list) else [us_]))

    def flat(rec, extra_cols, call=False):
        return ([rec.get("country", ""), rec.get("plant_name", ""),
                 rec.get("unit_name", ""), rec.get("gem_plant_id", ""),
                 rec.get("gem_unit_id", ""), group_cell(rec), rows_cell(rec)]
                + [rec.get(k, "") for k in extra_cols]
                + ([describe_call(rec["review_call"]) if rec.get("review_call") else ""] if call else [])
                + [json.dumps(rec.get("fields", {}), ensure_ascii=False), all_refs(rec),
                   rec.get("tier", ""), rec.get("researcher_notes", "")])

    base_hdr = ["country", "plant", "unit", "gem_plant_id", "gem_unit_id",
                "checklist_group", "checklist_rows"]
    tail_hdr = ["fields (json)", "refs", "confidence", "notes"]
    by_group = lambda recs: sorted(recs, key=lambda r: (group_sort_key(r), r.get("country", ""),  # noqa: E731
                                                         r.get("plant_name", ""), r.get("unit_name", "")))

    np_rows = []
    for rec in by_group(lanes.get("newplants", [])):
        np_rows.append(flat(rec, []))
        for u in rec.get("units", []):
            np_rows.append(flat({**u, "country": rec.get("country", ""),
                                 "plant_name": rec.get("plant_name", ""), "_tag": rec.get("_tag")}, []))
    add_sheet("new_plants", base_hdr + tail_hdr, np_rows)
    add_sheet("new_units", base_hdr + tail_hdr,
              [flat(r, []) for r in by_group(lanes.get("newunits", []))])
    add_sheet("entity_additions",
              base_hdr + ["entity_name", "role", "entity_country",
                          "lookup_result", "reviewer_call"] + tail_hdr,
              [flat(r, ["entity_name", "role", "entity_country", "lookup_result"], call=True)
               for r in by_group(lanes.get("entity", []))])
    add_sheet("qa_review",
              base_hdr + ["concern_type", "recommendation", "reviewer_call"] + tail_hdr,
              [flat(r, ["concern_type", "recommendation"], call=True)
               for r in by_group(lanes.get("qa", []))])

    # The watch list, split by what it watches. A watch item the reviewer promoted or sent
    # to the possible-updates sheet also stays on its watch sheet, with the call beside it.
    monitor = by_group(lanes.get("monitor", []))
    watch_hdr = base_hdr + ["monitor_reason", "recheck_by", "capacity_mw", "status",
                            "reviewer_call"] + tail_hdr
    for kind, sheet in (("new_to_tracker", "watch_new_to_tracker"),
                        ("existing_plant", "watch_existing_plants")):
        add_sheet(sheet, watch_hdr,
                  [flat(r, ["monitor_reason", "recheck_by", "capacity_mw", "status"], call=True)
                   for r in monitor if monitor_kind(r) == kind])
    add_sheet("promote_to_database",
              base_hdr + ["what_to_add", "monitor_reason", "reviewer_call", "refs", "notes",
                          "next_step"],
              [[r.get("country", ""), r.get("plant_name", ""), r.get("unit_name", ""),
                r.get("gem_plant_id", ""), r.get("gem_unit_id", ""), group_cell(r), rows_cell(r),
                ("a new plant" if monitor_kind(r) == "new_to_tracker" else "a change or new unit at this plant"),
                r.get("monitor_reason", "") or r.get("item", ""), describe_call(r["review_call"]),
                all_refs(r), r.get("researcher_notes", ""),
                "research it in the next batch and stage the full edit (build_state_brief.py --promote)"]
               for r in monitor if call_of(r) == "add_to_database"])
    add_sheet("possible_updates_rows",
              ["country", "plant", "unit", "gem_plant_id", "gem_unit_id", "what to check",
               "source links", "recheck_by", "reviewer_note", "added_by", "added_on"],
              [[r.get("country", ""), r.get("plant_name", ""), r.get("unit_name", ""),
                r.get("gem_plant_id", ""), r.get("gem_unit_id", ""),
                r.get("monitor_reason", "") or r.get("item", ""), all_refs(r), r.get("recheck_by", ""),
                r["review_call"].get("note", ""), r["review_call"].get("reviewer", ""),
                str(r["review_call"].get("ts") or "")[:10]]
               for r in monitor if call_of(r) == "possible_updates"])
    if flags:
        add_sheet("questions_for_pm",
                  ["country", "plant", "unit", "gem_plant_id", "gem_unit_id", "what_it_is",
                   "what", "checklist_group", "question", "asked_by", "asked_on"],
                  pm_question_rows(all_lanes or lanes, flags))
    if irp:
        add_sheet("irp_box", IRP_BOX_HEADER, irp_box_rows(lanes, irp, export_csv))
        add_sheet("irp_notes_draft", IRP_NOTES_HEADER, irp_notes_rows(lanes, irp))

    wb.save(out_path)


LANE_WORDS = {"updates": "change to an existing unit", "newplants": "new plant",
              "newunits": "new unit at an existing plant", "entity": "new owner or operator to create",
              "qa": "question about existing data", "monitor": "watch item"}


def record_word(lane, rec):
    if lane == "monitor":
        return ("watch item, new to the tracker" if monitor_kind(rec) == "new_to_tracker"
                else "watch item at an existing plant")
    return LANE_WORDS.get(lane, lane)


def build_evidence(lanes, out_path, stamp, scope, mode, left_out=None, flags=None,
                   all_lanes=None, export_csv=None, irp=None):
    """The evidence file, organized by QC/Country checklist group: what was left out by the
    review, the questions for the PM, then one section per group with every record under it
    (edits first, then questions and watch items) and the checkbox rows it helps tick."""
    us = tag_lanes(lanes, export_csv)
    if all_lanes is not None and all_lanes is not lanes:
        tag_lanes(all_lanes, export_csv)
    lines = [f"# Evidence — gogpt batch {stamp} ({scope}, {mode})", ""]
    lines.append("Each section below is one group of the GOGPT QC/Country checklist. The records "
                 "in it are the evidence for ticking that group's boxes; the row numbers are the "
                 "checklist tab's own.")
    lines.append("")
    if left_out is not None:
        lines.append("## Left out by the review")
        lines.append("")
        lines.append("These staged edits were not accepted in the review app, so they are not in "
                     "the actions workbook. A suggestion goes back to the researcher; a held or "
                     "undecided edit waits for a later batch. A watch item removed from the watch "
                     "list is listed here too and will not come back in a later sweep.")
        lines.append("")
        if not left_out:
            lines.append("- none: every staged edit was accepted")
        for lane, rec, d in sorted(left_out, key=lambda t: (t[1].get("plant_name", ""), t[1].get("unit_name", ""))):
            ident = " / ".join(x for x in (rec.get("gem_unit_id"), rec.get("plant_name"), rec.get("unit_name")) if x)
            cols = (", ".join(f"{c}: {v}" for c, v in rec.get("fields", {}).items())
                    or rec.get("monitor_reason") or record_word(lane, rec))
            lines.append(f"- {ident or '(unnamed record)'}: {cols}. {describe_decision(d)}")
        lines.append("")
    if flags:
        lines.append("## Questions for the PM")
        lines.append("")
        lines.append("Everything the reviewer ticked \"ask the PM\" on, with the note, whatever "
                     "the decision on it was.")
        lines.append("")
        for row in pm_question_rows(all_lanes or lanes, flags):
            country, plant, unit, pid, uid, kind, what, grp, note, who, when = row
            ident = " / ".join(x for x in (uid or pid, plant, unit) if x)
            lines.append(f"- {ident}: {kind}" + (f", {what}" if what else "")
                         + (f" ({grp})" if grp else "") + f". Asked by {who} on {when}"
                         + (f": {note}" if note else "."))
        lines.append("")
    if irp:
        data = irp["data"]
        lines.append("## Utility resource plans (checklist row 37)")
        lines.append("")
        utils = data.get("utilities") or []
        if data.get("skipped"):
            lines.append("The US IRPs tab has no row for this state, so no plan was read. "
                         "The IRP box stays as it is on every unit.")
        else:
            lines.append(f"The IRP step read {len(utils)} utility row{'s' if len(utils) != 1 else ''} of the "
                         "US IRPs tab for this state. The records below come from a plan; the actions "
                         "workbook's irp_box sheet says which units need the IRP box ticked, and its "
                         "irp_notes_draft sheet has a draft line per utility for the tab's Notes column.")
        lines.append("")
        for row in utils:
            plan = row.get("irp_year") or "plan"
            lines.append(f"- {row.get('utility', '')}: {plan}" + (" (a draft)" if row.get("is_draft") else "")
                         + (f", next plan due {row['next_irp_due']}" if row.get("next_irp_due") else "")
                         + (f". Tracked plants matched: {len(row.get('plants') or [])}" if row.get("plants") else ""))
        flagged = [(lane, r) for lane in LANES for r in lanes.get(lane, []) if r.get("irp")]
        if flagged:
            lines.append("")
            lines.append("Records from a plan:")
            for lane, r in flagged:
                ident = " / ".join(x for x in (r.get("gem_unit_id"), r.get("plant_name"), r.get("unit_name")) if x)
                util = irp_utility_of(irp, r)
                lines.append(f"- {ident}: {record_word(lane, r)}" + (f", from the {util} plan" if util else ""))
        lines.append("")

    def write_record(lane, rec):
        ident = " / ".join(x for x in (rec.get("gem_unit_id"), rec.get("plant_name"),
                                       rec.get("unit_name")) if x)
        lines.append(f"### {ident or '(unnamed record)'}")
        checks = (rec.get("_tag") or {}).get("checks", [])
        what = record_word(lane, rec)
        if checks:
            what += "; checklist rows " + ", ".join(f"{c} ({row_label(c)})" for c in checks)
        lines.append(f"*{what}*")
        if rec.get("action"):
            lines.append(f"**Action:** {rec['action']}")
        if lane == "monitor":
            if rec.get("monitor_reason") or rec.get("item"):
                lines.append(f"- what to watch: {rec.get('monitor_reason') or rec.get('item')}")
            if rec.get("recheck_by"):
                lines.append(f"- check again by: {rec['recheck_by']}")
        if lane == "qa":
            if rec.get("concern_type"):
                lines.append(f"- about: {rec['concern_type']}")
            if rec.get("recommendation"):
                lines.append(f"- recommendation: {rec['recommendation']}")
        if lane == "entity":
            lines.append(f"- entity: {rec.get('entity_name', '')} ({rec.get('role', '')}); "
                         f"lookup: {rec.get('lookup_result', '')}")
        for col, val in rec.get("fields", {}).items():
            cur = rec.get("current", {}).get(col, "")
            lines.append(f"- `{col}`: `{cur!s}` -> `{val!s}`")
        for u in rec.get("units", []) or []:
            for col, val in u.get("fields", {}).items():
                lines.append(f"- unit {u.get('unit_name', '?')} `{col}`: `{val!s}`")
        for ref_col, urls in rec.get("refs", {}).items():
            for u in (urls if isinstance(urls, list) else [urls]):
                v = next((v for v in rec.get("verifications", [])
                          if v.get("url") == u), {})
                lines.append(f"  - {ref_col}: {u} "
                             f"(ok={v.get('ok')}, contains_value={v.get('contains_value')})")
        tier = rec.get("tier", "")
        ind = rec.get("independent", "")
        if tier or ind:
            lines.append(f"- confidence: {tier} (independent: {ind})")
        if rec.get("researcher_notes"):
            lines.append(f"- notes: {rec['researcher_notes']}")
        if rec.get("review_call"):
            lines.append(f"- reviewer call: {describe_call(rec['review_call'])}")
        lines.append("")

    groups = [g for g in groups_for(us) if not g.get("panel")]
    order = [g["id"] for g in groups] + [OTHER]
    labels = {g["id"]: g["label"] for g in groups}
    labels[OTHER] = "Other"
    blurbs = {g["id"]: g["blurb"] for g in groups}
    for gid in order:
        members = [(lane, r) for lane in LANES for r in lanes.get(lane, [])
                   if (r.get("_tag") or {}).get("group", OTHER) == gid]
        if not members:
            continue
        name = "Other" if gid == OTHER else f"{gid}. {labels[gid]}"
        lines.append(f"## Checklist group {name}")
        lines.append("")
        if gid in blurbs:
            lines.append(blurbs[gid])
            lines.append("")
        for lane, rec in sorted(members, key=lambda t: (LANES.index(t[0]) if t[0] in EDIT_LANES else 9,
                                                        t[1].get("country", ""), t[1].get("plant_name", ""),
                                                        t[1].get("unit_name", ""))):
            write_record(lane, rec)
    closeout = next((g for g in groups_for(us) if g.get("panel")), None)
    if closeout:
        lines.append(f"## Checklist group {closeout['id']}. {closeout['label']}")
        lines.append("")
        lines.append(closeout["blurb"] + " These boxes are ticked by hand after the edits are "
                     "applied: validation_report.py --closeout must print CLOSE-OUT CLEAN "
                     "(row 54) and no_tracker.py lists the units with no tracker (row 56).")
        lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--staging-dir", required=True)
    p.add_argument("--scope", required=True, help="lowercase hyphenated slug")
    p.add_argument("--mode", required=True,
                   choices=["update", "discovery", "triage", "qc"])
    p.add_argument("--output-dir", default=None,
                   help="default: <staging-dir>/../deliverables")
    p.add_argument("--export-csv", default=str(gem_export_csv()),
                   help="fresh export CSV backing the edit_backend_format "
                        "sheet (default: the standard pull location)")
    p.add_argument("--decisions", action="store_true",
                   help="apply the review app's calls (<staging-dir>/review_log.jsonl): "
                        "only accepted edits go into the workbook")
    p.add_argument("--irp", default=None,
                   help="irp_sheet.py JSON for this state (work/irp_us-<st>.json): adds the "
                        "irp_box and irp_notes_draft sheets (US states only)")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    staging = Path(args.staging_dir)
    if not staging.is_dir():
        sys.exit(f"ERROR: staging dir not found: {staging}")
    lanes = load_lanes(staging)
    if not lanes:
        sys.exit(f"ERROR: no staged_<lane>.json files in {staging}")

    errors = validate(lanes)
    if errors:
        print(f"{len(errors)} build errors:")
        for e in errors:
            print(f"  ERROR: {e}")
        sys.exit(1)

    n = sum(len(v) for v in lanes.values())
    print(f"validated {n} records across lanes: "
          + ", ".join(f"{k}={len(v)}" for k, v in lanes.items()))

    left_out = None
    flags = None
    all_lanes = lanes
    decisions = load_decisions(staging)
    if args.decisions:
        if decisions is None:
            sys.exit(f"ERROR: --decisions but no review_log.jsonl in {staging} "
                     "(review the batch in the review app first, or drop the flag)")
        lanes, left_out, counts = apply_decisions(lanes, decisions)
        flags = load_flags(staging)
        calls = {}
        for r in lanes.get("monitor", []):
            c = call_of(r)
            if c:
                calls[c] = calls.get(c, 0) + 1
        print("review decisions: " + ", ".join(f"{k}={v}" for k, v in counts.items())
              + f"; {counts['accept']} edits go into the workbook, "
              f"{len(left_out)} left out (listed in the evidence file)")
        if calls or flags:
            print("watch-list calls: " + (", ".join(f"{CALL_LABELS.get(k, k)}={v}" for k, v in calls.items())
                                          or "none") + f"; questions for the PM: {len(flags)}")
        if not any(lanes.values()):
            sys.exit("ERROR: nothing left to build after the review decisions")
    elif decisions is not None:
        print(f"note: {staging / 'review_log.jsonl'} exists but --decisions was not given; "
              "building every staged record, the reviewer's calls are ignored")
    if args.dry_run:
        print("dry run — nothing written")
        return

    stamp = datetime.datetime.now(ZoneInfo("America/New_York")).strftime(
        "%Y%m%d_%H%M_ET")
    out_dir = Path(args.output_dir) if args.output_dir else \
        staging.parent / "deliverables"
    out_dir.mkdir(parents=True, exist_ok=True)
    base = f"gogpt_batch_{stamp}_{args.scope}_{args.mode}"
    xlsx_path = out_dir / f"{base}_actions.xlsx"
    md_path = out_dir / f"{base}_evidence.md"
    if xlsx_path.exists() or md_path.exists():
        sys.exit(f"ERROR: {base}_* already exists — never overwrite; rerun for "
                 "a fresh stamp")

    export_csv = Path(args.export_csv)
    if lanes.get("updates") and not export_csv.exists():
        sys.exit(f"ERROR: export CSV not found at {export_csv} — the "
                 "edit_backend_format sheet needs the fresh pull "
                 "(run the §1 pull chain, or pass --export-csv)")
    csv_or_none = export_csv if export_csv.exists() else None
    irp = load_irp(args.irp, staging)
    if irp and not is_us(all_lanes):
        sys.exit("ERROR: --irp is for US states (the US IRPs tab); this batch is not United States")
    build_xlsx(lanes, xlsx_path, export_csv=csv_or_none, flags=flags, all_lanes=all_lanes, irp=irp)
    build_evidence(lanes, md_path, stamp, args.scope, args.mode, left_out=left_out,
                   flags=flags, all_lanes=all_lanes, export_csv=csv_or_none, irp=irp)
    print(f"wrote {xlsx_path}\nwrote {md_path}\n"
          f"next: python recalc.py {xlsx_path}")


if __name__ == "__main__":
    main()

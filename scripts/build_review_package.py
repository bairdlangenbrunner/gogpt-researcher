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
    by design, see confidence_tiers.md)
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

Usage (from scripts/):
    python build_review_package.py --staging-dir ../batches/nigeria/staging \
        --scope nigeria --mode update
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
from schema_constants import READ_ONLY_COLUMNS
from colmap import load_colmap
from paths import gem_export_csv

LANES = ["updates", "qa", "entity", "monitor", "newplants", "newunits"]

BLOCKLIST = ("gem.wiki", "globalenergymonitor", "abarrelfull", "wikidot",
             "theodora")

TIER_FILLS = {"high": "C6EFCE", "medium": "FFEB9C", "low": "FFC7CE",
              "reverified": "BDD7EE"}

SHEET_DESCRIPTIONS = {
    "edit_checklist": ("PRIMARY deliverable — one row per proposed cell edit "
                       "(current -> proposed), ordered plant -> unit -> column "
                       "the way the web UI is walked. Paste the value into the "
                       "column and the URLs into its Data Source column "
                       "(merge, never replace). 'done' column is yours."),
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
    "monitor_list": "Below-add-threshold candidates with recheck dates.",
}


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
        rid = rec.get("record_id") or rec.get("key", "").split("::", 1)[-1]
        if rid:
            out[rid] = rec
    return out


def decision_of(rec, decisions):
    """'accept' | 'hold' | 'reject' | 'suggest' | 'undecided' for an edit record."""
    d = decisions.get(rec.get("record_id"))
    if not d or d.get("undecided") or "call" in d:
        return "undecided"
    return d.get("decision") or "undecided"


def apply_decisions(lanes, decisions):
    """Split the lanes by the reviewer's calls. Returns (kept_lanes, left_out, counts): kept
    has only accepted edit records (items untouched, each stamped with `review_call`); left_out
    is [(lane, record, decision record or None)] for every edit record not accepted."""
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
                out.append(rec)
            kept[lane] = out
    return kept, left_out, counts


def describe_decision(d):
    """One plain sentence for the evidence file: who called what, when, and their note."""
    if not d or d.get("undecided"):
        return "not decided yet in the review app"
    who, when = d.get("reviewer") or "?", str(d.get("ts") or "")[:10]
    if d.get("decision") == "suggest":
        val = d.get("suggested_value") or ""
        txt = f"suggested by {who} on {when}" + (f": {val}" if val else " (note only)")
    else:
        verb = {"accept": "accepted", "hold": "held", "reject": "rejected"}.get(d.get("decision"), d.get("decision"))
        txt = f"{verb} by {who} on {when}"
    if d.get("note"):
        txt += f". {d['note']}"
    return txt


def describe_call(d):
    who, when = d.get("reviewer") or "?", str(d.get("ts") or "")[:10]
    txt = f"{str(d.get('call', '')).replace('_', ' ')} by {who} on {when}"
    if d.get("note"):
        txt += f". {d['note']}"
    return txt


def ref_col_for(value_col):
    """Pair a value column with its Data Source column per the export layout."""
    special = {
        "Status": "Status Data Source",
        "Status Detail": "Status Data Source",
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


def is_inferred_only(rec):
    fields = rec.get("fields", {})
    status = str(fields.get("Status", "")) + str(fields.get("Status Detail", ""))
    return "inferred" in status.lower()


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
                                rec.get("action", ""), ""])
    rows.sort(key=lambda r: (r[0], r[1], r[2], r[5]))
    return rows


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
            if new_urls and ref_col in col_idx:
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
        if rec.get("country") and "Country/Area" in col_idx:
            base[col_idx["Country/Area"]] = rec["country"]
        if rec.get("gem_plant_id") and "GEM plant ID" in col_idx:
            base[col_idx["GEM plant ID"]] = rec["gem_plant_id"]
        for unit in rec.get("units") or [None]:
            row = list(base)
            r_i = len(rows)
            apply_staged(row, r_i, rec.get("fields", {}),
                         rec.get("refs", {}), tier, ident)
            if unit is not None:
                apply_staged(row, r_i, unit.get("fields", {}),
                             unit.get("refs", {}), tier,
                             f"{ident} / {unit.get('unit_name', '?')}")
            rows.append(row)
    return header, rows, fills


def build_xlsx(lanes, out_path, export_csv=None):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill

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
    ws.column_dimensions["B"].width = 22
    ws.column_dimensions["C"].width = 100

    add_sheet("edit_checklist",
              ["country", "plant", "unit", "gem_plant_id", "gem_unit_id",
               "column", "current", "proposed", "confidence", "refs_to_paste",
               "action", "done"],
              checklist_rows(lanes), tier_col=7)

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

    def flat(rec, extra_cols):
        return ([rec.get("country", ""), rec.get("plant_name", ""),
                 rec.get("unit_name", ""), rec.get("gem_plant_id", ""),
                 rec.get("gem_unit_id", "")]
                + [rec.get(k, "") for k in extra_cols]
                + [json.dumps(rec.get("fields", {}), ensure_ascii=False),
                   "; ".join(u for us in rec.get("refs", {}).values() for u in us),
                   rec.get("tier", ""), rec.get("researcher_notes", "")])

    base_hdr = ["country", "plant", "unit", "gem_plant_id", "gem_unit_id"]
    tail_hdr = ["fields (json)", "refs", "confidence", "notes"]

    np_rows = []
    for rec in lanes.get("newplants", []):
        np_rows.append(flat(rec, []))
        for u in rec.get("units", []):
            np_rows.append(flat({**u, "country": rec.get("country", ""),
                                 "plant_name": rec.get("plant_name", "")}, []))
    add_sheet("new_plants", base_hdr + tail_hdr, np_rows)
    add_sheet("new_units", base_hdr + tail_hdr,
              [flat(r, []) for r in lanes.get("newunits", [])])
    add_sheet("entity_additions",
              base_hdr + ["entity_name", "role", "entity_country",
                          "lookup_result"] + tail_hdr,
              [flat(r, ["entity_name", "role", "entity_country", "lookup_result"])
               for r in lanes.get("entity", [])])
    add_sheet("qa_review",
              base_hdr + ["concern_type", "recommendation"] + tail_hdr,
              [flat(r, ["concern_type", "recommendation"])
               for r in lanes.get("qa", [])])
    add_sheet("monitor_list",
              base_hdr + ["monitor_reason", "recheck_by"] + tail_hdr,
              [flat(r, ["monitor_reason", "recheck_by"])
               for r in lanes.get("monitor", [])])

    wb.save(out_path)


def build_evidence(lanes, out_path, stamp, scope, mode, left_out=None):
    lines = [f"# Evidence — gogpt batch {stamp} ({scope}, {mode})", ""]
    if left_out is not None:
        lines.append("## Left out by the review")
        lines.append("")
        lines.append("These staged edits were not accepted in the review app, so they are not in "
                     "the actions workbook. A suggestion goes back to the researcher; a held or "
                     "undecided edit waits for a later batch.")
        lines.append("")
        if not left_out:
            lines.append("- none: every staged edit was accepted")
        for lane, rec, d in sorted(left_out, key=lambda t: (t[1].get("plant_name", ""), t[1].get("unit_name", ""))):
            ident = " / ".join(x for x in (rec.get("gem_unit_id"), rec.get("plant_name"), rec.get("unit_name")) if x)
            cols = ", ".join(f"{c}: {v}" for c, v in rec.get("fields", {}).items()) or lane
            lines.append(f"- {ident or '(unnamed record)'}: {cols}. {describe_decision(d)}")
        lines.append("")
    for lane in LANES:
        recs = lanes.get(lane, [])
        if not recs:
            continue
        lines.append(f"## lane: {lane}")
        lines.append("")
        for rec in sorted(recs, key=lambda r: (r.get("country", ""),
                                               r.get("plant_name", ""),
                                               r.get("unit_name", ""))):
            ident = " / ".join(x for x in (rec.get("gem_unit_id"),
                                           rec.get("plant_name"),
                                           rec.get("unit_name")) if x)
            lines.append(f"### {ident or '(unnamed record)'}")
            if rec.get("action"):
                lines.append(f"**Action:** {rec['action']}")
            for col, val in rec.get("fields", {}).items():
                cur = rec.get("current", {}).get(col, "")
                lines.append(f"- `{col}`: `{cur!s}` -> `{val!s}`")
            for ref_col, urls in rec.get("refs", {}).items():
                for u in urls:
                    v = next((v for v in rec.get("verifications", [])
                              if v.get("url") == u), {})
                    lines.append(f"  - {ref_col}: {u} "
                                 f"(ok={v.get('ok')}, contains_value={v.get('contains_value')})")
            tier = rec.get("tier", "")
            ind = rec.get("independent", "")
            lines.append(f"- confidence: {tier} (independent: {ind})")
            if rec.get("researcher_notes"):
                lines.append(f"- notes: {rec['researcher_notes']}")
            if rec.get("review_call"):
                lines.append(f"- reviewer call: {describe_call(rec['review_call'])}")
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
    decisions = load_decisions(staging)
    if args.decisions:
        if decisions is None:
            sys.exit(f"ERROR: --decisions but no review_log.jsonl in {staging} "
                     "(review the batch in the review app first, or drop the flag)")
        lanes, left_out, counts = apply_decisions(lanes, decisions)
        print("review decisions: " + ", ".join(f"{k}={v}" for k, v in counts.items())
              + f"; {counts['accept']} edits go into the workbook, "
              f"{len(left_out)} left out (listed in the evidence file)")
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
    build_xlsx(lanes, xlsx_path,
               export_csv=export_csv if export_csv.exists() else None)
    build_evidence(lanes, md_path, stamp, args.scope, args.mode, left_out=left_out)
    print(f"wrote {xlsx_path}\nwrote {md_path}\n"
          f"next: python recalc.py {xlsx_path}")


if __name__ == "__main__":
    main()

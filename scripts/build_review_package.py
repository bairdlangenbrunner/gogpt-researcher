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

Usage (from scripts/):
    python build_review_package.py --staging-dir ../batches/nigeria/staging \
        --scope nigeria --mode update
    # add --dry-run to validate without writing files
"""
import argparse
import datetime
import json
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).parent))
from schema_constants import READ_ONLY_COLUMNS

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


def ref_col_for(value_col):
    """Pair a value column with its Data Source column per the export layout."""
    special = {
        "Status": "Status Data Source",
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
        "Disrupted due to conflict": "Disrupted due to conflict Data Source",
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


def build_xlsx(lanes, out_path):
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


def build_evidence(lanes, out_path, stamp, scope, mode):
    lines = [f"# Evidence — gogpt batch {stamp} ({scope}, {mode})", ""]
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

    build_xlsx(lanes, xlsx_path)
    build_evidence(lanes, md_path, stamp, args.scope, args.mode)
    print(f"wrote {xlsx_path}\nwrote {md_path}\n"
          f"next: python recalc.py {xlsx_path}")


if __name__ == "__main__":
    main()

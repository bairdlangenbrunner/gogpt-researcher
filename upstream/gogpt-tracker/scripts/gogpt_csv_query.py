#!/usr/bin/env python3
"""
GOGPT CSV Query Helper
======================
Extracts targeted slices from the GOGPT project XLSX/CSV instead of loading
the full file into context. Run from bash before each research session.

Usage:
  python3 gogpt_csv_query.py --country "Japan" --status in-development
  python3 gogpt_csv_query.py --country "Japan" --status operating
  python3 gogpt_csv_query.py --country "Japan" --status all --counts-only
  python3 gogpt_csv_query.py --country "Japan" --status in-development --region "Kanto"
  python3 gogpt_csv_query.py --country "Japan" --missing-fields

  # Cross-cutting checks (Q2 2026):
  python3 gogpt_csv_query.py --country "Japan" --status operating --ownership-scan
  python3 gogpt_csv_query.py --country "Japan" --in-progress-scan
  python3 gogpt_csv_query.py --country "Japan" --duplicate-scan
  python3 gogpt_csv_query.py --country "Japan" --possible-updates --pu-file "<PU csv OR Drive-read .md>"
  #   --pu-file accepts a local CSV (GEM_trackers__possible_updates__*.csv) OR the file
  #   the Drive read of the live multi-tab "GEM trackers - possible updates" sheet was
  #   saved to. Omit --pu-file to auto-glob the local CSV. For US states, add --state so
  #   the scan also matches "US-OH"-style tokens and the state's in-scope plant names.
  python3 gogpt_csv_query.py --country "Japan" --count-flags   # reads the working-copy card

  # US state work — country is "United States", state is the --state filter:
  python3 gogpt_csv_query.py --country "United States" --state "Arizona" --status in-development
  python3 gogpt_csv_query.py --country "United States" --state "Arizona" --counts-only
  python3 gogpt_csv_query.py --country "United States" --state "Arizona" --duplicate-scan

Output is printed as a compact markdown table and saved to /tmp/gogpt_query_output.md
"""

import argparse
import sys
import os
import glob

try:
    import pandas as pd
except ImportError:
    print("pandas not installed. Run: pip install pandas openpyxl --break-system-packages")
    sys.exit(1)

from gogpt_paths import DATA_DIR, DUMP_GLOBS, POSSIBLE_UPDATES_GLOB

# ── Config ────────────────────────────────────────────────────────────────────

# Auto-detect the newest GOGPT full-database export in the project directory.
# Prefers .xlsx; falls back to .csv for legacy exports. The filename carries a
# timestamp that changes every cycle, so resolving the most recent GOGPTall*.xlsx
# avoids any per-cycle edit here.
def _default_csv():
    # Prefer .xlsx; fall back to .csv for legacy exports
    for pattern in DUMP_GLOBS:
        matches = sorted(
            glob.glob(pattern),
            key=os.path.getmtime,
            reverse=True,
        )
        if matches:
            return matches[0]
    # last-resort fallback; pass --file explicitly if this isn't right
    return os.path.join(DATA_DIR, "GOGPTall*.xlsx")

DEFAULT_XLSX = _default_csv()

# Column name mappings — matched to the GOGPT full-database CSV export headers
COL_COUNTRY     = "Country/Area"
COL_STATE       = "State/Province"
COL_STATUS      = "Status"
COL_UNIT_ID     = "GEM unit ID"
COL_PLANT       = "Plant name"
COL_UNIT        = "Unit name"
COL_CAPACITY    = "Capacity (MW)"
COL_START_YEAR  = "Start year"
COL_TURBINE     = "Turbine/Engine Technology"
COL_TURBINE_MFR = "Equipment Manufacturer/Model"
COL_REGION      = "Region"
COL_COORDS_LAT  = "Latitude"
COL_COORDS_LON  = "Longitude"
COL_OWNER       = "Owner(s)"
COL_FUEL        = "Fuel"
COL_RET_YEAR    = "Planned retire"
COL_CHP         = "CHP"
COL_CONFLICT    = "Disrupted due to conflict"
COL_OPERATOR    = "Operator(s)"
COL_PARENT      = "Parent(s)"
COL_LOC_ID      = "GEM location ID"
COL_LOC_ACC     = "Location accuracy"
COL_STATUS_DT   = "Status Detail"

STATUS_GROUPS = {
    "in-development": ["announced", "pre-construction", "construction"],
    "shelved":        ["shelved", "shelved - inferred 2y"],
    "cancelled":      ["cancelled", "cancelled - inferred 4y"],
    "shelved-cancelled": ["shelved", "shelved - inferred 2y", "cancelled", "cancelled - inferred 4y"],
    "operating":      ["operating"],
    "retired":        ["retired", "mothballed"],
    "all":            None  # no filter
}

KEY_FIELDS = [COL_CAPACITY, COL_COORDS_LAT, COL_COORDS_LON, COL_START_YEAR]

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_data(path: str) -> pd.DataFrame:
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx", ".xlsm"):
        # Try to read the main data sheet; fall back to first sheet
        try:
            df = pd.read_excel(path, sheet_name="GOGPT", dtype=str)
        except Exception:
            df = pd.read_excel(path, sheet_name=0, dtype=str)
    elif ext == ".csv":
        df = pd.read_csv(path, dtype=str, low_memory=False)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    df.columns = [c.strip() for c in df.columns]
    df = df.fillna("")
    return df


def filter_country(df: pd.DataFrame, country: str) -> pd.DataFrame:
    col = next((c for c in df.columns if c.lower() == COL_COUNTRY.lower()), None)
    if col is None:
        # Fail loudly: never silently return the whole dataset.
        print(f"ERROR: Could not find '{COL_COUNTRY}' column. Columns found: {list(df.columns[:10])}")
        sys.exit(1)
    return df[df[col].str.strip().str.lower() == country.strip().lower()]


def filter_state(df: pd.DataFrame, state: str) -> pd.DataFrame:
    col = next((c for c in df.columns if c.lower() == COL_STATE.lower()), None)
    if col is None:
        print(f"ERROR: Could not find '{COL_STATE}' column. Columns found: {list(df.columns[:10])}")
        sys.exit(1)
    return df[df[col].str.strip().str.lower() == state.strip().lower()]


def filter_status(df: pd.DataFrame, status_key: str) -> pd.DataFrame:
    statuses = STATUS_GROUPS.get(status_key.lower())
    if statuses is None:
        return df
    col = next((c for c in df.columns if c.lower() == COL_STATUS.lower()), None)
    if col is None:
        print(f"WARNING: Could not find '{COL_STATUS}' column.")
        return df
    return df[df[col].str.strip().str.lower().isin([s.lower() for s in statuses])]


def filter_region(df: pd.DataFrame, region: str) -> pd.DataFrame:
    col = next((c for c in df.columns if c.lower() == COL_REGION.lower()), None)
    if col is None:
        print(f"WARNING: Could not find region column '{COL_REGION}'.")
        return df
    return df[df[col].str.strip().str.lower().str.contains(region.strip().lower(), na=False)]


def print_counts(df: pd.DataFrame, country: str):
    col = next((c for c in df.columns if c.lower() == COL_STATUS.lower()), None)
    if col is None:
        print("Could not produce counts — Status column not found.")
        return

    print(f"\n{'='*50}")
    print(f"UNIT COUNTS — {country.upper()}")
    print(f"{'='*50}")

    groups = {
        "Announced":       ["announced"],
        "Pre-construction":["pre-construction"],
        "Construction":    ["construction"],
        "Shelved":         ["shelved", "shelved - inferred 2y"],
        "Cancelled":       ["cancelled", "cancelled - inferred 4y"],
        "Operating":       ["operating"],
        "Retired/Mothballed": ["retired", "mothballed"],
    }
    total = 0
    in_dev = 0
    for label, statuses in groups.items():
        n = len(df[df[col].str.strip().str.lower().isin([s.lower() for s in statuses])])
        print(f"  {label:<25} {n}")
        total += n
        if label in ("Announced", "Pre-construction", "Construction"):
            in_dev += n

    print(f"  {'─'*35}")
    print(f"  {'In-development total':<25} {in_dev}")
    print(f"  {'GRAND TOTAL':<25} {total}")
    print()


def print_missing_fields(df: pd.DataFrame, country: str):
    print(f"\n{'='*50}")
    print(f"MISSING KEY FIELDS — {country.upper()}")
    print(f"{'='*50}")

    # Only check in-development units for turbine; all units for capacity/coords
    id_col  = next((c for c in df.columns if c.lower() == COL_UNIT_ID.lower()), None)
    st_col  = next((c for c in df.columns if c.lower() == COL_STATUS.lower()), None)

    for field in KEY_FIELDS:
        col = next((c for c in df.columns if c.lower() == field.lower()), None)
        if col is None:
            print(f"  {field}: column not found in data")
            continue
        missing = df[df[col].str.strip() == ""]
        n = len(missing)
        if n == 0:
            print(f"  {field}: ✅ None missing")
        else:
            ids = ""
            if id_col and n <= 10:
                ids = " — IDs: " + ", ".join(missing[id_col].tolist())
            print(f"  {field}: ⚠️  {n} missing{ids}")

    # Turbine: required for in-development units only. A unit counts as having
    # turbine info if EITHER the technology OR the manufacturer/model is filled.
    tech_col = next((c for c in df.columns if c.lower() == COL_TURBINE.lower()), None)
    mfr_col  = next((c for c in df.columns if c.lower() == COL_TURBINE_MFR.lower()), None)
    if st_col and (tech_col or mfr_col):
        in_dev_statuses = ["announced", "pre-construction", "construction"]
        in_dev = df[df[st_col].str.strip().str.lower().isin(in_dev_statuses)]
        tech_blank = in_dev[tech_col].str.strip() == "" if tech_col else True
        mfr_blank  = in_dev[mfr_col].str.strip()  == "" if mfr_col  else True
        missing_turb = in_dev[tech_blank & mfr_blank]
        n = len(missing_turb)
        if n == 0:
            print(f"  Turbine (in-dev only): ✅ None missing")
        else:
            ids = ""
            if id_col and n <= 10:
                ids = " — IDs: " + ", ".join(missing_turb[id_col].tolist())
            print(f"  Turbine (in-dev only): ⚠️  {n} missing{ids}")
    print()


def df_to_markdown(df: pd.DataFrame, cols: list) -> str:
    # Keep only cols that exist
    existing = [c for c in cols if any(dc.lower() == c.lower() for dc in df.columns)]
    col_map = {c: next(dc for dc in df.columns if dc.lower() == c.lower()) for c in existing}
    subset = df[[col_map[c] for c in existing]].copy()
    subset.columns = existing

    lines = []
    lines.append("| " + " | ".join(existing) + " |")
    lines.append("| " + " | ".join(["---"] * len(existing)) + " |")
    for _, row in subset.iterrows():
        lines.append("| " + " | ".join(str(v)[:80] for v in row) + " |")
    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="GOGPT targeted CSV query helper")
    parser.add_argument("--file",        default=DEFAULT_XLSX, help="Path to GOGPT XLSX or CSV")
    parser.add_argument("--country",     required=True,        help="Country/Area name (exact match), e.g. 'United States'")
    parser.add_argument("--state",       default=None,         help="State/Province name (exact match), e.g. 'Arizona'")
    parser.add_argument("--status",      default="all",
                        help="Status group: in-development | shelved | cancelled | shelved-cancelled | operating | retired | all")
    parser.add_argument("--region",      default=None,         help="Filter by province/region (partial match)")
    parser.add_argument("--counts-only", action="store_true",  help="Print unit counts and exit")
    parser.add_argument("--missing-fields", action="store_true", help="Print missing-field summary and exit")
    parser.add_argument("--verify-fields", action="store_true",
                        help="Re-verify the context card's 'current DB value' claims against the live CSV "
                             "(requires --context-card). Exits 2 if stale-blank captive/owner fields are found.")
    parser.add_argument("--context-card", default=None, help="Path to context card .md (for --verify-fields)")
    parser.add_argument("--ownership-scan", action="store_true",
                        help="Print the IMMEDIATE owner of each unit (vs parent) with the "
                             "closed→🔄 / upcoming→⏳ decision rule, then exit.")
    parser.add_argument("--in-progress-scan", action="store_true",
                        help="Find ⏳ in-progress units (status change expected in the update "
                             "window but not yet happened), then exit.")
    parser.add_argument("--duplicate-scan", action="store_true",
                        help="Flag likely duplicate plant entries within the country/state "
                             "(coords / capacity / owner / name / source), then exit.")
    parser.add_argument("--possible-updates", action="store_true",
                        help="Print the GEM possible-updates rows for the country "
                             "(requires --pu-file), then exit.")
    parser.add_argument("--pu-file", default=None,
                        help="Path to the GEM possible-updates source: either a "
                             "local CSV (GEM_trackers__possible_updates__*.csv) "
                             "or the file the Drive read of the live multi-tab "
                             "'GEM trackers - possible updates' sheet was saved "
                             "to (.md/.txt). Auto-globs the CSV if omitted.")
    parser.add_argument("--count-flags", action="store_true",
                        help="Count flag emoji in the working-copy context card "
                             "(auto-resolved, or pass --context-card), then exit.")
    parser.add_argument("--out",         default="/tmp/gogpt_query_output.md", help="Output file path")
    args = parser.parse_args()

    # ── Helpers that do NOT need the GOGPT CSV loaded ─────────────────────────
    # --possible-updates reads the separate possible-updates CSV; --count-flags
    # reads a context card. Handle both before touching the main database file.
    try:
        import gogpt_checks as gck
    except ImportError:
        gck = None

    if args.possible_updates:
        if gck is None:
            print("ERROR: gogpt_checks.py not found alongside this script.")
            sys.exit(1)
        pu = args.pu_file
        if not pu:
            import glob as _glob
            cands = sorted(
                _glob.glob(POSSIBLE_UPDATES_GLOB),
                key=lambda p: p, reverse=True)
            pu = cands[0] if cands else None
        if not pu:
            print("NO_LOCAL_PU_CSV — pass --pu-file pointing at a local CSV, "
                  "or at the file the Drive read of 'GEM trackers - possible "
                  "updates' (fileId 1GAXwGdI0UFeW9mFSxJhhR6MRBW7VDtlWBqsooVZyUzs) "
                  "was written to.")
            sys.exit(0)
        # Pull the in-scope plant names from the GOGPT DB so the flattened-sheet
        # scan can also catch geographically-unlabeled ownership rows (which name
        # the plant but carry no country cell). Best-effort: if the DB can't be
        # loaded here, fall back to a geo-only scan.
        plant_names = None
        try:
            df_all = load_data(args.file)
            df_scope = filter_country(df_all, args.country)
            if args.state:
                df_scope = filter_state(df_scope, args.state)
            if "Plant name" in df_scope.columns:
                plant_names = sorted(set(df_scope["Plant name"].dropna().tolist()))
        except Exception:
            plant_names = None
        print(gck.load_possible_updates(pu, args.country, args.state, plant_names))
        sys.exit(0)

    if args.count_flags:
        if gck is None:
            print("ERROR: gogpt_checks.py not found alongside this script.")
            sys.exit(1)
        card = args.context_card
        if not card:
            # auto-resolve the working-copy card via the updater's resolver
            try:
                import gogpt_card_update as gcu
                card = gcu.resolve_card(None, args.country)
            except Exception:
                card = None
        if not card or not os.path.exists(card):
            print("ERROR: no context card found. Pass --context-card or run setup first.")
            sys.exit(1)
        with open(card, encoding="utf-8") as f:
            counts, md = gck.count_card_flags(f.read())
        print(f"\nFLAG COUNTS — {os.path.basename(card)}")
        print(md)
        sys.exit(0)

    print(f"Loading {args.file} …")
    df = load_data(args.file)
    print(f"  Total rows loaded: {len(df)}")

    df_country = filter_country(df, args.country)
    print(f"  Rows for '{args.country}': {len(df_country)}")

    # Apply optional state/province filter (for US-state and similar work)
    label = args.country
    if args.state:
        df_country = filter_state(df_country, args.state)
        label = f"{args.state}, {args.country}"
        print(f"  Rows for '{label}': {len(df_country)}")

    if len(df_country) == 0:
        # Show available values to help debug
        if args.state:
            sp_col = next((c for c in df.columns if c.lower() == COL_STATE.lower()), None)
            if sp_col:
                # Limit to states within the chosen country for a useful hint
                cc_col = next((c for c in df.columns if c.lower() == COL_COUNTRY.lower()), None)
                scope = df[df[cc_col].str.strip().str.lower() == args.country.strip().lower()] if cc_col else df
                available = sorted([s for s in scope[sp_col].str.strip().unique().tolist() if s])
                print(f"\nState not found in '{args.country}'. Available (first 40): {available[:40]}")
        else:
            col = next((c for c in df.columns if c.lower() == COL_COUNTRY.lower()), None)
            if col:
                available = sorted([c for c in df[col].str.strip().unique().tolist() if c])
                print(f"\nCountry not found. Available countries (first 30): {available[:30]}")
        sys.exit(1)

    # ── Cross-cutting scans (operate on the country/state slice) ──────────────
    if args.ownership_scan or args.in_progress_scan or args.duplicate_scan:
        if gck is None:
            print("ERROR: gogpt_checks.py not found alongside this script.")
            sys.exit(1)
        # Scans normally run on a single status group when one is given
        # (e.g. operating units for an ownership scan), else the whole slice.
        scope = filter_status(df_country, args.status) if args.status != "all" else df_country
        out_blocks = []
        if args.ownership_scan:
            out_blocks.append(gck.ownership_scan(scope, label))
        if args.in_progress_scan:
            out_blocks.append(gck.in_progress_scan(scope, label))
        if args.duplicate_scan:
            # Duplicate detection always runs against the FULL country/state
            # slice (any status) — a duplicate often pairs an in-development
            # entry with an operating one.
            out_blocks.append(gck.duplicate_scan(df_country, label))
        text = "\n\n".join(out_blocks)
        print("\n" + text)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"\nOutput saved to: {args.out}")
        sys.exit(0)

    if args.verify_fields:
        if not args.context_card:
            print("ERROR: --verify-fields requires --context-card")
            sys.exit(1)
        if not os.path.exists(args.context_card):
            print(f"ERROR: context card not found: {args.context_card}")
            sys.exit(1)
        try:
            import gogpt_verify_fields as gvf
        except ImportError:
            print("ERROR: gogpt_verify_fields.py not found alongside this script.")
            sys.exit(1)
        # Verify against the full country dataframe (any status), so every
        # flagged unit ID is resolvable.
        with open(args.context_card, encoding="utf-8") as f:
            report = gvf.verify(f.read(), df_country)
        gvf.print_report(report)
        if report["stale_blank"]:
            print("RESULT: stale-blank captive/owner fields found — the dependent")
            print("flags should be trimmed from the QC report before export.")
            sys.exit(2)
        print("RESULT: no stale-blank captive/owner fields. Safe to export.")
        sys.exit(0)

    if args.counts_only:
        print_counts(df_country, label)
        sys.exit(0)

    if args.missing_fields:
        print_missing_fields(df_country, label)
        sys.exit(0)

    # Default: print counts + filtered table
    print_counts(df_country, label)
    print_missing_fields(df_country, label)

    df_filtered = filter_status(df_country, args.status)
    if args.region:
        df_filtered = filter_region(df_filtered, args.region)

    print(f"\nRows matching status='{args.status}'" + (f", region='{args.region}'" if args.region else "") + f": {len(df_filtered)}")

    if len(df_filtered) == 0:
        print("No matching units found.")
        sys.exit(0)

    # Output columns — ordered by usefulness for each status group
    output_cols = [
        COL_UNIT_ID, COL_PLANT, COL_UNIT, COL_STATUS,
        COL_CAPACITY, COL_START_YEAR, COL_TURBINE, COL_TURBINE_MFR,
        COL_STATE, COL_REGION, COL_COORDS_LAT, COL_COORDS_LON,
        COL_OWNER, COL_FUEL, COL_RET_YEAR, COL_CHP, COL_CONFLICT
    ]

    md = df_to_markdown(df_filtered, output_cols)

    output = f"# GOGPT Query — {label} — {args.status}\n\n"
    output += f"Generated: see terminal for date | Rows: {len(df_filtered)}\n\n"
    output += md + "\n"

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"\nOutput saved to: {args.out}")
    print("\n--- TABLE PREVIEW (first 5 rows) ---")
    preview_lines = md.split("\n")[:7]  # header + separator + 5 rows
    print("\n".join(preview_lines))
    if len(df_filtered) > 5:
        print(f"… ({len(df_filtered) - 5} more rows in output file)")


if __name__ == "__main__":
    main()

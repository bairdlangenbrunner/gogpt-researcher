"""
export_to_dump.py — bridge the fresh GOGPT pull into the upstream dump format
=============================================================================
Converts this repo's GOGPT-scoped CSV (from the fresh-pull chain, §1 of
docs/workflows.md) into a `GOGPTall<YYYYMMDD>T<HHMMSS>sheet.xlsx` dump in
`upstream/gogpt-tracker/data/`, so the upstream pipeline's scans
(gogpt_csv_query.py --ownership-scan / --in-progress-scan / --duplicate-scan /
--counts-only) run on data pulled this morning instead of the bundled cycle
dump. The upstream scripts auto-detect the NEWEST dump by filename date, so a
freshly bridged dump takes precedence automatically.

Header reconciliation (live pull → dump dialect), derived from the header row
every run — never from hard-coded offsets:

  * strip the UTF-8 BOM from the first header cell ("Last Updated")
  * "Disrupted due to conflict"              → "Disrupted by conflict"
  * "Disrupted due to conflict Data Source"  → "Disrupted by conflict Data Source"
  * append any dump-only column ("Backup Power", "Backup Power Data Source",
    "IRP") the pull lacks, empty. The 91-column pull (Oct 2026) already
    carries all three and uses the "Disrupted by conflict" names, so on a
    current pull the renames and the append are no-ops; they stay for older
    exports. Upstream scans look columns up by name and tolerate blanks.

The output timestamp comes from the input CSV's mtime (i.e. the pull time),
so the filename's cycle tag reflects when the data was pulled, not when this
script ran. Override with --stamp YYYYMMDDTHHMMSS if needed.

Usage (from scripts/, after the fresh-pull chain):

  python export_to_dump.py                          # scoped CSV → upstream data/
  python export_to_dump.py --input other.csv --outdir /elsewhere
  python export_to_dump.py --stamp 20260804T090000

The generated dump is gitignored (multi-MB, regenerable); the bundled upstream
dump stays as a pinned fixture. Nothing here touches the live GEM database.
"""

import argparse
import csv
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_INPUT = os.path.join(HERE, "gem_export_gogpt_scoped.csv")
DEFAULT_OUTDIR = os.path.normpath(
    os.path.join(HERE, "..", "upstream", "gogpt-tracker", "data")
)

# live-pull header → dump header (everything else passes through unchanged)
RENAMES = {
    "Disrupted due to conflict": "Disrupted by conflict",
    "Disrupted due to conflict Data Source": "Disrupted by conflict Data Source",
}
# present in the team dump but not in the live pull; appended empty
DUMP_ONLY_COLUMNS = ["Backup Power", "Backup Power Data Source", "IRP"]
SHEET_NAME = "GOGPT"  # gogpt_csv_query.py prefers a sheet with this name


def bridge(input_csv: str, outdir: str, stamp: str | None) -> str:
    from openpyxl import Workbook

    if stamp is None:
        stamp = time.strftime("%Y%m%dT%H%M%S", time.localtime(os.path.getmtime(input_csv)))
    out_path = os.path.join(outdir, f"GOGPTall{stamp}sheet.xlsx")
    if os.path.exists(out_path):
        sys.exit(f"refusing to overwrite existing dump: {out_path}")

    wb = Workbook(write_only=True)
    ws = wb.create_sheet(SHEET_NAME)

    n_rows = 0
    with open(input_csv, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        header = [RENAMES.get(h, h) for h in header]
        extra = [c for c in DUMP_ONLY_COLUMNS if c not in header]
        ws.append(header + extra)
        pad = [""] * len(extra)
        for row in reader:
            ws.append(row + pad)
            n_rows += 1

    os.makedirs(outdir, exist_ok=True)
    wb.save(out_path)
    print(f"wrote {out_path}")
    print(f"  {n_rows} unit rows, {len(header) + len(extra)} columns "
          f"({len(header)} from pull + {len(extra)} dump-only, empty)")
    return out_path


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--input", default=DEFAULT_INPUT,
                    help="GOGPT-scoped CSV from the fresh-pull chain")
    ap.add_argument("--outdir", default=DEFAULT_OUTDIR,
                    help="where to write the GOGPTall*.xlsx dump")
    ap.add_argument("--stamp", default=None,
                    help="override the YYYYMMDDTHHMMSS filename stamp "
                         "(default: input CSV mtime = pull time)")
    args = ap.parse_args()
    if not os.path.isfile(args.input):
        sys.exit(f"input not found: {args.input} — run the fresh-pull chain first "
                 "(docs/workflows.md §1)")
    bridge(args.input, args.outdir, args.stamp)


if __name__ == "__main__":
    main()

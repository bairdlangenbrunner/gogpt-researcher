"""
Shared colmap.json loader.

Ported from the LNG Terminals tracker's colmap.py, which consolidated a
column-map loader that had been copy-pasted with minor drift across several
scripts there. Keep it that way here: this is the single canonical
implementation any GOGPT script needing column-index lookups (entity_lookup.py
and future scripts alike) should import, rather than re-deriving its own copy.

pull_gem_db.py (this repo) writes the .colmap.json sibling of the export CSV
via `python pull_gem_db.py --map-only`; this loader reads it back, with a
helpful "run pull_gem_db.py --map-only first" error message, and BOM-safe
re-derivation of `_header_columns` from the CSV header row when
pull_gem_db.py has stripped it out of the serialized colmap.json.
"""
import csv
import json
from pathlib import Path


def load_colmap(csv_path):
    """Load the .colmap.json sibling of csv_path.

    Raises RuntimeError if the colmap file doesn't exist (with a pointer to
    `pull_gem_db.py --map-only`). If `_header_columns` is absent from the
    colmap (pull_gem_db.py strips it before serializing to disk), re-derive it
    from the CSV's own header row (encoding="utf-8-sig" — BOM-safe).
    """
    map_path = Path(csv_path).with_suffix(".colmap.json")
    if not map_path.exists():
        raise RuntimeError(
            f"colmap.json not found at {map_path}. Run pull_gem_db.py --map-only first."
        )
    colmap = json.loads(map_path.read_text())
    if "_header_columns" not in colmap:
        with open(csv_path, encoding="utf-8-sig") as f:
            colmap["_header_columns"] = next(csv.reader(f))
    return colmap

# data/

Database dumps and possible-updates source files. The scripts auto-detect the
**newest** dump here by the date encoded in its filename, so adding a new
cycle's files is usually all that's required — no code edit.

## Files

### `GOGPTall<YYYYMMDD>T<HHMMSS>sheet.xlsx`
The full GOGPT database export for a cycle. One row per plant unit, ~89 columns
(country/area, plant & unit names, fuel, capacity, status, ownership, location,
data-source URLs, start/retirement years, and so on). The 8-digit date in the
filename is the **cycle tag** — `gogpt_card_update.py` reads it to name and
version context cards, and `gogpt_csv_query.py` loads the newest one by default.

Currently bundled: `GOGPTall20260618T164506sheet.xlsx` (~15,300 rows).

> `gogpt_csv_query.py` reads the sheet named `GOGPT` if present, otherwise the
> first sheet. This export's sheet is `Sheet1`, which the fallback handles.

### `GEM_trackers__possible_updates__*.csv`
The "possible updates" queue — rows GEM researchers have flagged for review
(new proposals, status changes, ownership notes) with plant name, capacity,
project status, notes, source URL, and who added it. Consumed by
`gogpt_csv_query.py --possible-updates`, which filters to the country in scope
and drops rows already marked `done`.

The same flag also accepts a flattened read of the live multi-tab
"GEM trackers – possible updates" Google Sheet (a `.md`/`.txt` export); pass it
with `--pu-file`. See `load_possible_updates` in `scripts/gogpt_checks.py`.

### `gasDB_unitsHistory1.csv`
A units-history extract (per-unit change history: status, capacity, ownership,
retirement dates, coordinates over time). Reference data for auditing how a unit
has evolved across releases; not required by the core query/compile path.

## Adding a new cycle

1. Drop the new `GOGPTall<date>T<time>.xlsx` dump in here.
2. Drop the matching `GEM_trackers__possible_updates__<date>.csv` in here.
3. That's it — the scripts pick up the newest dump automatically.

## A note on size

Dumps are multi-megabyte. They're tracked in git by default so a clone is
immediately runnable. If you'd rather keep them out of version control, uncomment
the `data/GOGPTall*` lines in the repo `.gitignore` and distribute dumps
separately.

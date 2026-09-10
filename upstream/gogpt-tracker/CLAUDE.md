# CLAUDE.md — guidance for Claude Code

This repo is the research pipeline for Global Energy Monitor's Global Oil and
Gas Plant Tracker (GOGPT). Read this before making changes or running a session.

## What the pipeline is

A researcher works **one country (or one US state) per cycle** through a fixed
sequence of sessions, recording findings in a per-country **context card**
(`GOGPT_ContextCard_<Country>_<CycleTag>_v<N>.md`, built from
`templates/COUNTRY_CONTEXT_CARD_TEMPLATE.md`). The scripts slice the full
database to what one session needs, run quality scans, keep the card in sync,
and compile the reviewed database into GEM's published spreadsheet.

## The scripts (all in `scripts/`)

- **`gogpt_csv_query.py`** — main entry point. Filters the newest dump in
  `data/` by country/state/status and prints counts, missing-field summaries,
  and cross-cutting scans. Delegates to the two modules below.
- **`gogpt_checks.py`** — importable module: `ownership_scan`,
  `in_progress_scan`, `duplicate_scan`, `load_possible_updates`,
  `count_card_flags`. No I/O of its own. Self-test: `python3 gogpt_checks.py --test`.
- **`gogpt_verify_fields.py`** — re-checks the card's "current DB value" claims
  against live data so stale snapshots don't reach the QC report. Exit code `2`
  signals stale-blank captive/owner fields.
- **`gogpt_card_update.py`** — writes findings into the card's
  `<!-- SECTION:X:START/END -->` markers, marks sessions done, and handles Drive
  versioning (cycle tag = the dated dump; `v[N]` = progress within a cycle).
- **`gogpt_compile.py`** — turns a raw CSV database export into the multi-tab
  deliverable (Gas & Oil Units / sub-threshold / IRP), applying thresholds,
  dropping pre-2020 retirements, and removing H2 conversions.
- **`gogpt_paths.py`** — central path resolution. **Use it; never hardcode
  `/mnt/...` or absolute paths in the other scripts.**

## Conventions to preserve

- **Column names are load-bearing.** The constants at the top of
  `gogpt_csv_query.py` and `gogpt_checks.py` (`COL_UNIT_ID = "GEM unit ID"`,
  etc.) must match the dump's headers exactly. Column lookups are
  case-insensitive but name-sensitive — keep the two files' constants in sync.
- **Scans never auto-edit the database.** `duplicate_scan`, `ownership_scan`,
  and `in_progress_scan` only *surface* candidates for a human to confirm. Don't
  change them to write findings automatically.
- **Auto-trim is one-directional.** `gogpt_verify_fields.py` may auto-trim a
  flag only in the STALE_BLANK direction (card said blank, data populated) and
  only for captive/owner fields. A CHANGED value is warn-only — never auto-trim.
- **Section markers are the contract** between the template and
  `gogpt_card_update.py`. If you edit the template, keep every
  `<!-- SECTION:X:START -->` / `<!-- SECTION:X:END -->` pair intact.
- **`strings_to_urls=False`** in `gogpt_compile.py` is deliberate — the data has
  many long URLs and xlsxwriter caps hyperlinks per sheet at ~65k, silently
  blanking later columns. Leave it off.

## Running things

```bash
pip install -r requirements.txt          # add --break-system-packages if needed
cd scripts
python3 gogpt_csv_query.py --country "Japan" --counts-only
python3 gogpt_checks.py --test           # module self-test
```

Data locations are env-overridable (`GOGPT_DATA_DIR`, `GOGPT_OUTPUT_DIR`, …);
see the table in `README.md`. Defaults are repo-relative, so from a clean
checkout everything reads `data/` and writes `output/`.

## When adding a new cycle's data

Drop the new `GOGPTall<YYYYMMDD>T<time>.xlsx` dump and the matching
`GEM_trackers__possible_updates__*.csv` into `data/`. The scripts auto-detect
the **newest** dump by filename date, and `gogpt_card_update.py` derives the
cycle tag from it. No code edit needed per cycle.

## Testing changes

There's no formal test suite beyond `gogpt_checks.py --test`. Before committing
a change to any script, at minimum run:

```bash
cd scripts
python3 gogpt_checks.py --test
python3 gogpt_csv_query.py --country "China" --counts-only   # any country in the dump
```

and confirm both still succeed.

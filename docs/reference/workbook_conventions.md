# Deliverable conventions — the actions/evidence pair

Every batch's human-facing deliverable is a **two-file split** (the pipelines
repo's actions/evidence pattern, shaped for GOGPT as a per-plant/per-unit
web-UI edit checklist), built by `scripts/build_review_package.py` from the
staged-JSON lanes (`staged_json_schema.md`) and written to
`batches/<scope>/deliverables/`.

## File naming

```
gogpt_batch_<YYYYMMDD>_<HHMM>_ET_<scope>_<mode>_actions.xlsx
gogpt_batch_<YYYYMMDD>_<HHMM>_ET_<scope>_<mode>_evidence.md
```

- Stamp: `TZ=America/New_York date "+%Y%m%d_%H%M_ET"` — regenerated at build
  time, never reused from earlier in the session.
- `<scope>`: lowercase hyphenated country/region slug (`nigeria`,
  `us-gulf`); `<mode>`: `update` / `discovery` / `triage` / `qc`.
- **Never overwrite an existing deliverable** — every (re)build gets a new
  freshly-stamped pair, even for small iterative rebuilds. The user prunes.
- Triage and QC runs are memo-only (`batches/<scope>/deliverables/
  triage_<stamp>_ET.md` / `qc_<stamp>_ET.md`); they never produce a workbook.

## The actions workbook (xlsx)

Ordered the way a human walks the web UI (gem-project-db.herokuapp.com):
grouped by country → plant → unit → column. Empty sheets are omitted. Run
`scripts/recalc.py` on the built file before presenting (catches Excel error
strings / leaked formulas).

| sheet | from lane | contents |
|---|---|---|
| `README` | — | first tab: mode, color legend (real swatches), per-sheet definitions for every tab present, read-only column groups, input-summary stats |
| `edit_checklist` | `updates` | PRIMARY deliverable — one row per proposed cell edit: plant / unit / GEM IDs / column / **current → proposed** / confidence color / verified URLs to paste into the paired Data Source column / one-line `action`. A `done` checkbox column for the human. |
| `edit_backend_format` | `updates`, `newplants`, `newunits` | the same edits in the export CSV's own table layout: one row per affected unit, all 86 export columns, in **final proposed form**. Colored cells are the changes (per-cell tier colors below; green+empty = staged deletion); Data Source cells hold existing URLs merged with the new ones. Uncolored cells = untouched current values. New plants/units render as blank-based rows (country/plant ID filled, plant-level fields duplicated across unit rows, whole record colored by its tier). Built from the batch's fresh export (`--export-csv`). |
| `new_plants` | `newplants` | plant-level rows, each followed by its unit rows |
| `new_units` | `newunits` | unit rows anchored to an existing `T####` |
| `entity_additions` | `entity` | new entities to create first (entity edits precede plant edits in the UI) |
| `qa_review` | `qa` | read-and-flag concerns: concern type, recommendation — never a paste target |
| `monitor_list` | `monitor` | below-threshold candidates with recheck dates |

Read-only columns (`schema_constants.COMPUTED_COLUMNS` and the hydrogen
`OUT_OF_SCOPE_COLUMNS`) never appear as edit targets; underscore-prefixed meta
columns are reference-only and say so in the README tab.

## The evidence file (md)

One section per record, same ordering as the workbook, keyed by GEM ID:
sources with verification results (HTTP + value-present), the exact quote or
figure supporting each proposed value, independence assessment, conflicts and
how they were resolved, and the `researcher_notes` (including any
Background-worthy narrative the human may hand-place on the wiki page). The
reviewer should be able to accept or reject every action row without leaving
the evidence file.

## Color conventions (per cell, not per row)

- **Green** — high confidence: a primary/regulatory source OR ≥2 genuinely
  independent corroborating sources. Mirrors of one document = ONE source
  (yellow, not green); never list mirror URLs to manufacture a green.
- **Yellow** — single solid source that verifiably contains the value; or
  value implied/contested.
- **Red** — single weak source; prefer blank + a `qa_review` entry instead.
- **Blue** — value unchanged from the DB but re-verified this batch (the
  "no changes" outcome at cell granularity).
- **Green + empty cell** — staged deletion: the existing value is unsupported
  by any findable source; apply = clear the cell (and note in evidence).
  Scope: asserted factual values only, never GEM-computed columns.

See `confidence_tiers.md` for the rubric behind the colors.

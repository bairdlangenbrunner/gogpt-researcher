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
| `checklist_summary` | all | start here: the QC/Country checklist groups of the batch (`review_app/checklist.py`), how many edits and items sit under each group and each checkbox row, so the batch is ticked off box by box. Every edit and item row also carries `checklist_group` and `checklist_rows` columns |
| `edit_checklist` | `updates` | PRIMARY deliverable — one row per proposed cell edit: plant / unit / GEM IDs / column / **current → proposed** / confidence color / verified URLs to paste into the paired Data Source column / one-line `action`. A `done` checkbox column for the human. |
| `edit_backend_format` | `updates`, `newplants`, `newunits` | the same edits in the export CSV's own table layout: one row per affected unit, all 86 export columns, in **final proposed form**. Colored cells are the changes (per-cell tier colors below; green+empty = staged deletion); Data Source cells hold existing URLs merged with the new ones. Uncolored cells = untouched current values. New plants/units render as blank-based rows (country/plant ID filled, plant-level fields duplicated across unit rows, whole record colored by its tier). Built from the batch's fresh export (`--export-csv`). |
| `new_plants` | `newplants` | plant-level rows, each followed by its unit rows |
| `new_units` | `newunits` | unit rows anchored to an existing `T####` |
| `entity_additions` | `entity` | new entities to create first (entity edits precede plant edits in the UI) |
| `qa_review` | `qa` | read-and-flag concerns: concern type, recommendation — never a paste target |
| `watch_new_to_tracker` | `monitor` (`monitor_kind` = `new_to_tracker`) | plants and projects GEM does not have yet that did not clear the add threshold, with the reason and recheck date — never a paste target |
| `watch_existing_plants` | `monitor` (`monitor_kind` = `existing_plant`) | possible changes or expansions at plants GEM already tracks, not yet confirmed |
| `promote_to_database` | review calls | with `--decisions`: watch items the reviewer marked "incorporate into database"; each becomes a task in the next batch via `build_state_brief.py --promote` |
| `possible_updates_rows` | review calls | with `--decisions`: watch items sent to the possible-updates sheet, laid out as rows to paste there (the reviewer who owns the rows pastes) |
| `questions_for_pm` | review flags | with `--decisions`: everything the reviewer ticked "ask the PM" on, with the note, whatever its call |
| `irp_box` | any lane with `irp: true` | US only, with `--irp`: every edit, new row and item sourced from a utility integrated resource plan, the utility it came from, the unit's IRP box as the export shows it (`irp_box_now`: not ticked / already ticked / new row / unknown) and the web-form action; then the already-ticked units the batch did not touch, for reference (checklist row 37) |
| `irp_notes_draft` | IRP step | US only, with `--irp`: one row per utility on the US IRPs tab for the state: plan year, draft flag, plan links, next plan due, the tab's latest note, how many records this batch took from the plan, and a dated draft Notes line to paste onto the tab by hand (row 34). The repo never writes the tab |

Read-only columns (`schema_constants.COMPUTED_COLUMNS` and the hydrogen
`OUT_OF_SCOPE_COLUMNS`) never appear as edit targets; underscore-prefixed meta
columns are reference-only and say so in the README tab.

Status Detail and Notes rows are additive (Baird 2026-10-07): the **proposed** cell holds the whole box to paste, new text on top and the existing text below it word for word, and the `action` says to add at the top of the box. Neither box is ever rewritten or cleared. A Status Detail entry ends with its source link (Baird 2026-10-08), so nothing is pasted into Status Data Source for it.

## The evidence file (md)

With `--decisions` the file opens with the held, rejected, suggested and undecided edits and the reviewer's notes, then the questions for the PM; with `--irp` a "Utility resource plans (checklist row 37)" section lists each utility's plan, whether it is a draft, when the next one is due, the matched plants and the records taken from the plan. Then one section per record, same ordering as the workbook, keyed by GEM ID:
sources with verification results (HTTP + value-present), the exact quote or
figure supporting each proposed value, independence assessment, conflicts and
how they were resolved, and the `researcher_notes` (including any
Background-worthy narrative the human may hand-place on the wiki page). The
reviewer should be able to accept or reject every action row without leaving
the evidence file.

## Color conventions (per cell, not per row)

- **Green** — high confidence: one fully validated ref (clears
  `url_verifier.py`, names the plant/unit, states the value); a second
  independent source is preferred, not required (Baird 2026-10-02, adopting the pipelines-researcher ruling of 2026-09-30).
  A STATUS CHANGE is green only on 2+ genuinely independent publishers.
  Mirrors of one document = ONE source; never list mirror URLs to
  manufacture a second source.
- **Yellow** — a single-source status change; or a ref that validates only
  partially; or value implied/contested.
- **Red** — single weak/unvalidated ref; prefer blank + a `qa_review` entry instead.
- **Blue** — value unchanged from the DB but re-verified this batch (the
  "no changes" outcome at cell granularity).
- **Green + empty cell** — staged deletion: the existing value is unsupported
  by any findable source; apply = clear the cell (and note in evidence).
  Scope: asserted factual values only, never GEM-computed columns.

See `confidence_tiers.md` for the rubric behind the colors.

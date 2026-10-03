# Campaign q4-2026

Cycle window 2026-09-14 → 2026-12-24 (end-of-update checks 12-18 → 12-24).
Coordination source of truth: **Q4 2026 GOGPT Update V2** — link and tab
gids in `docs/reference/sop_pointers.md` (the kickoff doc still links an
earlier copy of the sheet; V2 is live). Kickoff/Guide doc linked there too.

## What is different this cycle

- **US assignments are per state**, not per country: the assignments tab has
  one row per `United States - <State>` with its own priority level, days
  allocated and status. `build_campaign_roster.py` keys on a `scope`
  column: one roster row per `United States - <State>` (split on
  `State/Province`), the country name elsewhere, plus an `indev_mw` column
  for the tab's in-development-MW sort. `worklist.py --state` and
  `qc_checks.py --state` take the same state names.
- **Priority level** (high / medium / low, by in-development capacity) sets
  how much effort the "country tips" questions get; it does not change the
  unit-level priority ladder.
- **Required deliverable**: operating units with unknown start year get
  re-researched (≤10 min per unit; decade known → midpoint year + internal
  note). Turbine make/model for in-development units: enter "not found" only
  after actually searching.
- **Status timeline** entry model is live in the DB: status changes are new
  *milestone* rows, projected years are *scheduled event* rows; nothing is
  overwritten (`docs/reference/lifecycle_rules.md` "How status edits are
  entered").
- **US-only QC items** (checklist tab): IRP checkbox on all IRP units; GEM
  IDs matched to EIA-860M, EIP and Sierra Club; data-center gas searched and
  captive data filled; US IRPs and United States research tabs updated.

## This repo's role this cycle

Supporting the US researcher's state assignments with agent-run batches that
produce the normal actions/evidence deliverable pair per state scope
(`batches/us-<st>/`). Texas (15 days, high, scheduled 11-05 → 12-01) is the
pilot: `notes/texas_pilot_plan.md`. The week-of-09-15 states on the
researcher's schedule (Hawaii, Maine, Maryland, Montana, New Hampshire, New
York, Oregon, Rhode Island, Washington, Alabama, Colorado, Florida, Illinois,
Iowa) are candidates for parallel small batches.

## Roster

Generate / refresh (counts update, manual columns survive):

    cd scripts
    python ../../gem-db-ops/gogpt/pull.py --output gem_export_gogpt.csv
    python scope_filter.py
    python build_campaign_roster.py --campaign q4-2026

Manual columns:

| column | meaning |
|---|---|
| `assignee_role` | who holds the assignment (per the 2026-09-15 ruling, names are allowed in committed content) |
| `assignment_status` | `unassigned` / `in-progress` / `close-out` / `done` |
| `packet_file` | the scope's deliverable pair basename in `batches/<scope>/deliverables/` |
| `applied` | date the human finished applying the packet in the web UI |
| `notes` | one-liners; anything longer goes in `docs/country_notes/` |

Close-out requires the QC/Country checklist tab (all applicable blocks) + the
DB validation report before a row moves to `done` (`docs/sops/qc.md` §6).

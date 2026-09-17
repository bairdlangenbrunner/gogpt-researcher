# Lifecycle Rules — Status Definitions and Review Priority

Distilled from the GOGPT Editing Manual (March 2026); fetched 2026-07-27.

Covers the ten `Status` values a GOGPT unit can carry, the disappearance-from-documents
tests behind the two inferred statuses, start/retired/cancellation-year conventions, the
conflict-damage rule, the December year-end rollover, and the priority order for working
through a country during a research pass. See `unit_conventions.md` for how status
interacts with unit naming (the "R" replacement suffix, conversion timepoints) and
`controlled_vocab.md` for the exact casing GOGPT's `Status` field uses in the live export.

## The ten statuses

| Status | Meaning |
|---|---|
| `announced` | Publicly reported but not yet moving forward — no permits, land, or financing sought. Includes a "Phase 2" at a site where "Phase 1" is under development, and projects that only appear in long-range company/government planning documents. |
| `pre-construction` | Actively moving forward: seeking government approvals, land rights, or financing. |
| `construction` | Physical construction (equipment or building) has begun — not just a groundbreaking ceremony or early site prep. |
| `operating` | Commercial operation date achieved. |
| `mothballed` | Deactivated / inactive for more than 1 year, but not retired. |
| `retired` | Permanently decommissioned, or converted to another fuel (see `unit_conventions.md` on conversion vs. replacement). |
| `shelved` | Officially shelved by the owner or a national government; construction officially put on hold also counts. |
| `shelved – inferred 2 y` | See "Inferred statuses" below. |
| `cancelled` | Officially cancelled by the owner or a national government. |
| `cancelled – inferred 4 y` | See "Inferred statuses" below. |

`announced` / `pre-construction` / `construction` are collectively "in-development" —
the research-priority tier during an update (see "Country-pass review priority" below).

## Inferred statuses: the disappearance test

Both inferred statuses use the same underlying test, applied only to units currently
`announced`, `pre-construction`, or `construction`:

> Projects with "announced", "pre-construction" or "construction" status that **disappear
> from company documents**, even if no announcement is made, and show no activity over a
> period of **2 years** → `shelved – inferred 2 y`.
> The same disappearance test over a period of **4 years** → `cancelled – inferred 4 y`.

Note the test is disappearance from documents / lack of activity, not an explicit
statement that the project was paused or killed — that's what makes it "inferred" rather
than `shelved`/`cancelled` proper (which require an explicit owner/government
announcement).

Use the unit's **Latest activity** field to track candidates: when a unit hasn't been
mentioned in media or company documents for a while, record the most recent source found
and the date it was last referenced there. That record is what a future pass uses to
decide whether the 2-year or 4-year threshold has been crossed.

## Tracking window: mothballed / retired / cancelled from 2020 forward

`mothballed`, `retired`, and `cancelled` are tracked **only from 2020 forward** — GOGPT
officially started at the beginning of 2020, and the manual's intent is to capture all
gas-plant changes since then, not to backfill history before the tracker existed.

## Start year rules

- Start year = the year the unit reached commercial operation.
- For a proposed plant with a planned start year, record the projected year and check the
  **Planned** checkbox. While the unit stays in-development, treat the year as an
  estimate; remove the checkmark once the unit actually becomes operational.
- **`shelved` and `cancelled` units never get a start year** — leave the Start Year field
  (and its reference column) blank. A start year doesn't make sense once a project is
  paused/killed rather than progressing toward operation.
- If a unit is replaced (a new turbine installed in place of the old one), the old unit is
  retired and the new unit gets its own new start year — see the "R" suffix convention in
  `unit_conventions.md`.
- Maintenance/upgrade without a turbine replacement does **not** get a new start year; the
  original start year stands (only capacity/technology/retirement year may change).
- **Operating units with an unknown start year** (Q4 2026 required deliverable, per the
  kickoff doc): re-research, capped at ~10 minutes per unit. If sources pin only the
  decade, enter the decade midpoint (e.g. "1975" for "the 1970s") and add an internal
  note saying the year is a decade estimate. Unit-level Other IDs (EIA-860M generator
  ID, national registries) are the fastest route to an exact year.

## Retired year / planned retire year

- **Retired Year** = the year the unit went offline. **Mothballed units must not have a
  retired year** — they haven't been retired, only deactivated.
- **Planned Retire Year**: when a source states a future retirement (often paired with a
  replacement unit coming online), record that year and check **Planned**. Note any
  replacement context in Status Details. Remove the Planned checkmark once the unit is
  actually retired.

## Cancellation year

Cancellation Year = the year the unit or phase is officially cancelled.

## Conflict-damage / disruption rules

When a plant or unit has been damaged by war/conflict, check the **"Disrupted due to
conflict"** checkbox (between Status and Status Details) and assign status as follows:

- **`mothballed`** + check the box — plant/unit completely destroyed, or rebuilding is
  likely to take many years with no indication reconstruction has begun or is imminent.
- **`operating`** + check the box — only partially damaged, appears partially
  operational, or likely to be repaired within roughly a year.
- **Keep `operating`**, no status change, if the extent of damage is unclear and there's
  no indication the plant has stopped operating — use best judgement and add a brief note
  in Status Details explaining the call.
- **`retired`** only when there is explicit indication the plant will not be rebuilt and
  has been decommissioned indefinitely.

## How status edits are entered: the status timeline (2026 DB change)

The DB no longer overwrites status or planned-year fields; every edit is a **new
timeline entry** and existing entries are never edited or deleted (Status Timeline
Training doc — link in `sop_pointers.md`). What we research is unchanged; how it is
entered is:

| entry type | what it records | year rule | fields |
|---|---|---|---|
| **Milestone** | a status change that has actually happened (announced → pre-construction, construction → operating, → retired, → cancelled …) | this year or earlier | status, year it happened, source, note |
| **Scheduled event** | a status the unit is projected to reach (planned operating year, planned construction start, planned retirement) | this year or later | status, event year, **source year** (when the schedule was reported), source |

- Current status = the most recent milestone; **Planned start year and planned retire
  year now live in the scheduled timeline** as `operating` / `retired` scheduled events.
- A pushed-back start year is a *new* scheduled `operating` event with the new year and
  the new source year — the old projection stays as history.
- One research finding often stages several entries (Case B in the training doc: a
  pre-construction milestone **plus** a scheduled `operating` 2029 event).
- For the actions workbook this means a status change stages `status + year + source`
  and a projected year stages `status + event year + source year + source`; the
  evidence.md says which entry type each staged row is. Whether inferred statuses carry
  the inference year or no year as their milestone year is answered in the training
  doc's Case D video — confirm before staging the first inferred batch under the new
  model.

## Year-end rollover rule

During the second annual research update (concludes in December): no in-development or
retiring plant should carry the current (ending) year as its start or retirement year
unless a source confirms the plant actually entered operation or was actually retired. If
no source confirms it, roll the start/retirement year forward to the following year.

## Country-pass review priority

Per the General Guidelines, work a country's units in this order:

1. **In-development units** — `announced`, `pre-construction`, `construction`.
2. **`shelved` and `shelved – inferred 2 y` units** — re-check whether the 2-year
   disappearance test now supports escalating to `cancelled – inferred 4 y`, or whether
   new activity has resurfaced.
3. **Units with planned retirement in the current year.**
4. **Units with planned retirement** (any year).
5. **Operating units** — lowest priority. Not separately itemized in the manual's
   priority list, but implied by the general instruction to "focus on in-development
   units" during an update pass; review these only as research time allows.

For an update specifically, filter the Status field to `announced` / `pre-construction` /
`construction` first — that's the researcher's default lens before working down the rest
of the list above.

## Cross-references

- `unit_conventions.md` — replaced ("R"-suffix) units, conversion timepoints (a
  conversion changes a unit's fuel without a `retired`/new-unit pair the way a
  replacement does), co-located coal/gas plants.
- `controlled_vocab.md` — exact `Status` casing as it appears in the live export vs. this
  manual's Title Case tables.
- `datasource_conventions.md` — every status change needs a datasource; the "add
  datasource" and fuel-conversion timepoint mechanics referenced above live there.

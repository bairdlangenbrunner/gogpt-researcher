# Lifecycle Rules — Status Definitions and Review Priority

Distilled from the GOGPT Editing Manual (September 2026); updated 2026-10-27.

Covers the ten `Status` values a GOGPT unit can carry, the disappearance-from-documents
tests behind the two inferred statuses, start/retired/cancellation-year conventions, the
conflict-damage rule, the December year-end check, and the priority order for working
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

Both inferred statuses use the same underlying test, applied only to units currently `announced`, `pre-construction`, or `construction`:

> Projects with "announced", "pre-construction" or "construction" status that **disappear from company documents**, even if no announcement is made, and show no activity over a period of **2 years** → `shelved – inferred 2 y`.
> The same disappearance test over a period of **4 years** → `cancelled – inferred 4 y`.

The test is disappearance from documents and lack of activity, not an explicit statement that the project was paused or killed. That is what makes it "inferred" rather than `shelved` or `cancelled` proper, which need an explicit owner or government announcement.

**An inferred status is a milestone entry with a datasource** (manual, Unit Milestone Timeline section). The datasource is the Latest Activity source, the newest report found. The milestone year is the Latest Activity date plus two years for `shelved – inferred 2 y`, or plus four years for `cancelled – inferred 4 y` (manual tip on inferred milestone entries). The staged record carries that source in its refs and the computed year. It is no longer an exception to the rule that every value needs a datasource.

Use the unit's **Latest activity** field to track candidates: when an in-development unit has not been mentioned in media or company documents for some time, record the most recent source found and the date it was last referenced there (manual, Latest activity section). A future pass uses that record to decide whether the two-year or four-year mark has been crossed.

**Which units get one** (Baird 2026-10-05, after Amalia Llano's New York review; the manual sets no age or status limit beyond in-development, so this is the repo's working reading of "for some time", kept at one year because the inferred statuses are computed from it): the briefs offer Latest Activity only for (1) in-development units that have gone quiet, (2) shelved and shelved-inferred units, which are still counting toward the four-year mark, (3) cancelled-inferred units, which are checked each pass for any newer report or a revival, and (4) any inferred status where the field is blank. In every case the date must be at least a year old: a report from the last twelve months means the project is moving, so it goes in the note and Latest Activity is left alone. It is never filled for operating, mothballed, retired or plainly cancelled units, or for planned-retirement checks. `build_state_brief.py` `unit_tasks` and the `state-sweep.js` prompt carry this, and `state_gate.py` fails an edit that breaks it (gate `latest-activity`).

**Format:** Latest Activity is a date field in the GEM database. The export renders it as `Year: 2024, Month: 6, Day: 17` (month and day optional), and every one of the ~2,100 filled values in the 2026-10-02 export has that form. Stage the date of the newest dated report; what happened goes in the researcher note and, if it changes the status story, in Status Detail, added above the text already in that box (Status Detail is a running log, newest entry first; it is never rewritten). Never move the date backward. `state_gate.py` fails any free-text Latest Activity value (gate `dates`).

## Tracking window: mothballed / retired / cancelled from 2020 forward

`mothballed`, `retired`, and `cancelled` are tracked **only from 2020 forward** — GOGPT
officially started at the beginning of 2020, and the manual's intent is to capture all
gas-plant changes since then, not to backfill history before the tracker existed.

## Start year rules

- Start year = the year the unit reached commercial operation. It is recorded as an operating milestone entry.
- A projected or planned start year is a **scheduled event** (status `operating`) with the projected year as the Event Year and the year the source reported it as the Source Year (manual, Start/Operating Year section). There is no Planned checkbox. The staged `Start year` value carries the Event Year and the action tells the human to add a new scheduled event entry. Every scheduled event needs an Event Year.
- **`shelved` and `cancelled` units never get a start year**, and never get a new scheduled operating event. Leave the Start Year field (and its reference column) blank. Scheduled events added before the unit was shelved or cancelled stay in the timeline as a record of what was planned.
- If a unit is replaced (a new turbine installed in place of the old one), the old unit is retired and the new unit gets its own new start year, never earlier than the old unit's retirement year (usually the same year). See the "R" suffix convention in `unit_conventions.md`.
- Maintenance or an upgrade without a turbine replacement does **not** get a new start year or a new operating milestone; the original start year stands (only capacity, technology or the retirement date may change). If the work changes the expected retirement date, add a new scheduled retirement event with the revised Event Year and the year it was reported as the Source Year.
- **Operating units with an unknown start year** (Q4 2026 required deliverable, per the kickoff doc): re-research, capped at about 10 minutes per unit. If sources pin only the decade, enter the decade midpoint (e.g. "1975" for "the 1970s") and add an internal note saying the year is a decade estimate. Unit-level Other IDs (EIA-860M generator ID, national registries) are the fastest route to an exact year.

## Retired year / planned retire year

- **Retired Year** = the year the unit went offline, recorded as a retired milestone entry. **Mothballed units must not have a retired year**, since they have not been retired, only deactivated.
- **Planned retire year**: when a source states a future retirement (often paired with a replacement unit coming online), record it as a scheduled event (status `retired`) with the projected year as the Event Year and the reported year as the Source Year. If the planned year changes, add a new scheduled event; never edit the existing one. Note any replacement context in Status Detail. There is no Planned checkbox.

## Cancellation year

Cancellation Year = the year the unit or phase is officially cancelled.

## Conflict-damage / disruption rules

When a plant or unit has been damaged by war/conflict, check the **"Disrupted due to conflict"** checkbox (between Status and Status Details) and assign status as follows:

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

- Current status = the most recent milestone; **planned start year and planned retire year live in the scheduled timeline** as `operating` / `retired` scheduled events.
- A pushed-back start year is a *new* scheduled `operating` event with the new year and the new source year; the old projection stays as history. A superseded scheduled event stays in place and the new status is recorded as a milestone.
- **Every scheduled event has an Event Year.** Never stage one without it.
- One research finding often stages several entries (Case B in the training doc: a pre-construction milestone **plus** a scheduled `operating` 2029 event).
- Every new timeline entry carries a datasource, inferred statuses included (see "Inferred statuses" above).
- **A wrong timeline entry is never edited by the researcher.** If an existing entry looks wrong, raise it to the project manager through a `qa` record (manual, Status Timeline section: consult the PM first).
- For the actions workbook this means a status change stages `status + year + source`, a projected year stages `status + event year + source year + source` (the `Start year` or `Planned retire` value is the Event Year and the action says to add a new scheduled event entry), an inferred status stages `status + computed year + Latest Activity source`, and the evidence.md says which entry type each staged row is.

## Year-end check (the December rule)

During the second annual research update, which concludes in December, check every in-development or retiring unit that has a scheduled operating or retired event falling in the current (ending) year. If no source confirms that the unit entered operation or was retired, add a **new** scheduled event with the following year as the Event Year and the current year as the Source Year (manual, Year-end note). Do not edit the existing entry.

## Research status and close-out

When you create a new unit or phase, choose "added" as its research status in the research-status section (manual, Research status section). If you start a unit and do not finish it, choose "in progress" so you can filter for it later. At the end of a country's research cycle, filter the database for every "in progress" unit in the country, review each, and change the research status to "updated" or "no changes".

## Country-pass review priority

Per the General Guidelines, work a country's units in this order:

1. **In-development units**: `announced`, `pre-construction`, `construction`.
2. **`shelved` and `shelved – inferred 2 y` units**: re-check whether new activity has resurfaced.
3. **Units with planned retirement in the current year.**
4. **Units with planned retirement** in any year.
5. **Everything else**, as research time allows. Operating and mothballed units have no tier of their own in the manual.

The cancelled-inferred test (four years) applies only to units that are `announced`, `pre-construction` or `construction`. Date arithmetic runs on the Latest Activity date, not on the calendar year.

For an update specifically, filter the Status field to `announced` / `pre-construction` / `construction` first, then work down the list above.

## Cross-references

- `unit_conventions.md` — replaced ("R"-suffix) units, conversion timepoints (a
  conversion changes a unit's fuel without a `retired`/new-unit pair the way a
  replacement does), co-located coal/gas plants.
- `controlled_vocab.md` — exact `Status` casing as it appears in the live export vs. this
  manual's Title Case tables.
- `datasource_conventions.md` — every status change needs a datasource; the "add
  datasource" and fuel-conversion timepoint mechanics referenced above live there.

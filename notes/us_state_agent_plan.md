# US state research agent: plan and contract

Written 2026-10-02 (Baird + Claude). This is the plan for the GOGPT research
agent that mirrors the pipelines and terminals engines: a worklist, one brief
per plant, a Workflow that fans out one subagent per plant, one JSON shard per
plant, an assemble step that turns shards into the staged lane files, a gate
that must print clean, then the normal deliverable build. It extends
`texas_pilot_plan.md` (Texas is the eventual scale target) and starts with one
of Amalia Llano's finished states as a calibration run.

Decisions already made (2026-10-02):

1. **Evidence bar**: one fully validated reference is enough; more are
   preferred, never owed; a status change is green only with two independent
   publishers (`docs/reference/confidence_tiers.md`).
2. **First run is one state**, producing a calibration memo plus a normal
   Update deliverable pair.
3. **The staging directory is the canonical pending-state store.** A review
   app (same pattern as the carriers and pipelines apps: a read-only loopback
   server over the staged JSON, a `decisions.csv` plus `review_log.jsonl`
   sidecar, accept / hold / reject / suggest per record) will read it later.
   Every staged record therefore carries a stable `record_id`.
4. **Subagents run on Sonnet or Opus**; the main loop does scope calls,
   scoring and merge decisions.
5. **Notes are written for people** (`docs/reference/notes_style.md`).

## Why Maryland first

The fresh pull of 2026-10-02 has 37 Maryland rows across 17 plants. Amalia
edited 7 of them between 2026-09-28 and 2026-09-30 (Brandywine, both
Constellation projects, Cove Point, Herbert Wagner, Morgantown, NRG Chalk
Point CT). The other 10 plants were last touched in 2021 to 2025. That split
gives two comparisons from one run: the agent against a researcher's fresh
work, and the agent against stale rows where it should find real updates.
Statuses present: 30 operating, 4 retired, 2 announced, 1 cancelled.

## Country mode (added 2026-10-05)

The same pipeline runs for a whole country, first used for Dan O'Beirne's
European countries (`notes/europe_batches_plan.md`). `build_state_brief.py
--country "<Country>"` replaces `--state`; the batch dir is the country slug
(`batches/germany/`; record IDs stay `<plant id>:<unit id>:<field>`); the note
read is `docs/country_notes/<slug>.md`; the two EIA "Other IDs" tasks are not
generated. The scope travels as a `where` object (`kind`, `name`, `slug`,
`country`, `postal`) in `_index.json`, `sweep_args.json` and the staged
records' `meta.scope`; old indexes with only `state`/`postal` still work. The
workflow prompt swaps the EIA and ISO ladder for a country ladder (regulator
register, transmission operator and ENTSO-E, capacity-market registers,
permit registers, owner pages, local-language press) and states the 20 MW
threshold for EU and UK countries. The scope-wide agent still writes
`shards/_state.json`. Everything below reads "state" but applies to a
country the same way.

## Directory layout per state

```
batches/us-<st>/                      <st> = two-letter postal code, lowercase (us-md)
                                      a country uses its slug instead: batches/germany/
  briefs/<Lxxxxxxxxxxxx>.md           one brief per plant (GEM location ID)
  briefs/_index.json                  list of plants, brief paths, unit IDs, worklist priority
  briefs/_hidden/<L...>.json          blind mode only: the withheld GEM values, for the compare step
  shards/<L...>.json                  one shard per plant, written by the subagent
  staging/staged_<lane>.json          assembled lane files (the canonical store)
  staging/blind/staged_<lane>.json    blind mode only: the full untrimmed lane files, parked after scoring
  staging/comparison.json             blind mode: per unit, per field: GEM value vs research value
  staging/sweep_args.json             the Workflow args used for the run
  calibration_<stamp>_ET.md           blind mode memo (scored by hand in the main loop)
  deliverables/                       actions.xlsx + evidence.md, built last, never overwritten
```

## Pipeline

```
# 1. fresh pull (from scripts/)
python ../../gem-db-ops/gogpt/pull.py --output gem_export_gogpt.csv
python pull_gem_db.py --map-only
python scope_filter.py
python export_to_dump.py                       # only if the upstream scans are wanted

# 2. worklist and briefs
python worklist.py --state Maryland --all
python build_state_brief.py --state Maryland --mode blind      # calibration only
python validation_report.py --state Georgia                     # checklist row 7
python match_ids.py --state Georgia                             # row 38
python irp_sheet.py --state Georgia --save-json ../work/irp_tab.json   # rows 34 and 37 (US IRPs tab)
python build_state_brief.py --state Georgia --mode update \
    --extra-tasks ../batches/us-ga/extra_tasks.json \
    --validation ../work/validation_us-ga.json --ids ../work/ids_us-ga.json \
    --irp ../work/irp_us-georgia.json \
    --promote ../batches/us-ny/staging                          # watch items a reviewer promoted; --scope ladder is the default
python build_sweep_args.py --batch ../batches/us-ga --model sonnet --group-max 5   # writes staging/sweep_args.json

# 3. fan out (Workflow tool, script .claude/workflows/state-sweep.js, args = that JSON);
#    in parallel, one Sonnet agent does the statewide search for newly announced
#    gas plants and gas-fired data centers, reads briefs/_irp.md and the promoted
#    candidates, and writes shards/_state.json (qa, monitor, newplants, newunits,
#    meta.irp_summary)

# 4. assemble, gate, QC, build
python assemble_state.py --batch ../batches/us-ga
python state_gate.py --batch ../batches/us-ga                   # must print GATE CLEAN
python qc_checks.py --staged ../batches/us-ga/staging/staged_updates.json   # and the other lanes
python build_review_package.py --staging ../batches/us-ga/staging --scope us-ga --mode update --irp ../work/irp_us-georgia.json
```

A staging folder curated by hand after assembly (Maryland, New York) is never
rebuilt from its shards; `add_checklist_fields.py --staging <dir>` adds the
checklist fields in place.

## Modes

**blind** (calibration). The brief gives the subagent only identity: plant
name, other names, state, county, city, coordinates, the EIA or other IDs in
"Other IDs (location)", and for each unit its GEM unit ID and unit name. It
withholds status, capacity, fuel, technology, years, owners, operator, CHP,
every Data Source cell, the Notes column and the edit history. The subagent
researches the full field set from scratch. The assemble step then compares
its findings with the withheld values and writes `comparison.json` and the
calibration memo skeleton. Scoring (match, GEM wrong, research wrong, both
defensible, unresolvable) is done in the main loop, by reading the sources.

**update** (the normal batch). The brief includes the current values, the
existing Data Source URLs (to harvest and carry forward), the Notes column,
the worklist priority and flags, and the state source ladder, plus a "What
to check" block per unit (built 2026-10-02 from the manual's ladder and the
gap list in `notes/qc_checklist_plan.md`): in-development, shelved,
mothballed and planned-retirement checks by status group; cancelled or
retired units missing their year; blank fuel, status, technology, owner,
coordinates or city; zero capacity; unknown technology; blank start year on
an operating unit; cancelled-inferred units (anything reported since);
inferred status with no Latest Activity; missing EIA IDs;
any value whose Data Source cell is empty. `--extra-tasks` adds the
possible-updates backlog rows and scan hits per plant. The "Fields to report
on" list shrinks to the fields those tasks touch, and with the default
`--scope ladder` a plant with no task gets no brief at all (listed under
`not_tasked` in `_index.json`). The subagent does the tasks and nothing
else; anything it notices in passing goes to `qa`. The prompt also carries
the Maryland lessons as rules: never change a present coordinate, the EIA
utility name is not the owner, never drop an EIA-860 fuel, conversion-unit
start year, engine fields only for reciprocating engines, captive fields
blank for grid plants. A statewide agent writes `shards/_state.json` (qa and
monitor items only) for newly announced plants and gas-fired data centers;
`assemble_state.py` passes it through with record IDs starting
`us-<postal>:plant`.

## Shard contract (`shards/<L...>.json`)

Written by the subagent. Keys are fixed; free text follows `notes_style.md`.

```json
{
  "meta": {
    "plant_id": "L100000402511", "plant_name": "Brandywine power facility",
    "state": "Maryland", "mode": "blind", "model": "sonnet",
    "generated": "2026-10-02T15:10:00-04:00", "done": true,
    "urls_attempted": 14, "urls_verified": 9
  },
  "units": [
    {
      "gem_unit_id": "G100000401771", "unit_name": "F701",
      "findings": {
        "Status": {
          "value": "operating",
          "refs": ["https://..."],
          "verifications": [{"url": "https://...", "ok": true,
                             "contains_value": true, "name_found": true}],
          "tier": "high", "independent": false,
          "note": "The EIA-860M table for July 2026 lists this unit as operating."
        },
        "Capacity (MW)": { "...": "same shape" }
      },
      "not_found": ["Start year"],
      "notes": "One or two plain sentences about this unit, including what was not found and why."
    }
  ],
  "plant_findings": { "Owner(s)": { "...": "same shape; applies to every unit" } },
  "qa": [ {"gem_unit_id": "G...", "concern_type": "duplicate",
           "recommendation": "...", "note": "...", "refs": []} ],
  "monitor": [], "newunits": [],
  "entities": [ {"entity_name": "...", "role": "owner", "lookup_result": "..."} ],
  "source_log": [ {"url": "https://...", "used_for": ["Status", "Capacity (MW)"],
                   "outcome": "verified", "note": "..."} ]
}
```

Rules the subagent must follow, repeated in its prompt: field keys are exact
CSV headers; values are cell content only, never prose and never a URL; every
URL in `refs` has a `verifications` entry produced by `url_verifier.py`;
`refs` may be empty only for an inferred status; hydrogen columns and
computed columns are never reported; a combined-cycle block is one unit;
capacity is electric generating MW; no start year for shelved or cancelled
units; no retired year for mothballed units; owners as `Name [share%]`, five
percent or more, top four plus other, never a national government.

## Staged record additions

`docs/reference/staged_json_schema.md` gains two optional fields on the common
core, for the review app and the assemble step:

- `record_id` (str): `<plant_id>:<unit_id>:<field slug>`; stable across
  rebuilds so a decision made in the review app survives a rebuild. The app
  keys its log on `<staging dir>::<record_id>`; a monitor record with no GEM
  plant id gets a card of its own under `new:<plant name slug>`.
- `reverified` (bool): the value is unchanged and a new source confirms it
  (the blue color in the workbook).

Added 2026-10-07 for the checklist work (`notes/review_app_checklist_plan.md`):
`checks` (checklist rows, copied from the brief task), normalized qa
`concern_type` (shard text kept in `concern_type_raw`), monitor
`monitor_reason` / `recheck_by` / `monitor_kind`, and `irp` (the value comes
from a utility resource plan: the shard finding carried `irp: true` or a ref
is one of the plan links in the brief index). A shard finding may carry
`"irp": true` next to `tier`; the statewide file may carry `newplants`,
`newunits` and `meta.irp_summary`.

## Gate (`state_gate.py`)

Read-only. Hard failures exit non-zero; advisory lines are informational.

| gate | hard? | checks |
|---|---|---|
| coverage | hard | every brief in `_index.json` has a shard with `meta.done: true` |
| banned | hard | no gem.wiki, globalenergymonitor.org, abarrelfull or GEM-derived republisher in any ref |
| verified | hard | every ref URL has a passing verification entry; `contains_value` false is allowed only with a note that explains the inference |
| orphans | hard | every `fields` column has its Data Source entry and vice versa, inferred statuses excepted |
| fresh | hard | every `current` value matches the fresh export (the export was not replaced mid-run) |
| headers | hard | every `fields` key is an export header and not a read-only column |
| cell prose | hard | a value cell holds a value, not a sentence or a URL |
| dates | hard | `Latest Activity` reads `Year: YYYY, Month: M, Day: D` (month and day optional); the year columns hold a four-digit year |
| latest activity | hard | a `Latest Activity` edit is only for a unit in development, shelved or with an inferred status, and its date is at least a year old |
| additive | hard | a `Status Detail` or `Notes` value is the new text placed above the text already in the box, which stays word for word, on the unit and on every sibling of a plant-wide edit; neither box is ever cleared (Baird 2026-10-07) |
| false high | advisory | a `high` status change with fewer than two independent hosts |
| independence | advisory | `independent: true` with fewer than two verified refs |
| entities | advisory | every new owner or operator name passes `entity_lookup.py` (skipped offline) |
| notes | advisory | notes that contain repo jargon or dashes flagged for rewrite |

Then `qc_checks.py --staged` on every lane file must exit 0.

## Calibration memo

`calibration_<stamp>_ET.md`. Per plant and per field: GEM value, research
value, source that resolved it, and a verdict column filled by hand. Totals
by verdict. A short section on which source types resolved which fields and
how long each plant took. Genuine GEM errors go into the Update deliverable
of the same run; the memo says which ones.

### Maryland result (2026-10-02)

Scored memo: `batches/us-md/calibration_20261002_1546_ET.md`. 851 unit
fields; 283 matched, 178 filled a blank, 59 disagreed. The 59 disagreements
held two real GEM errors (Rock Springs unit 2 capacity 176 versus 199 MW,
Wagner Unit 3 timepoint 2 technology unknown versus steam turbine) and a
handful of real questions (Morgantown 5 and 6 retired versus operating, a
probable duplicate SGT1 record at Chalk Point, which two Rock Springs units
Old Dominion Electric Cooperative owns). Everything else was the agent not
knowing a GEM convention: 24 Location accuracy downgrades from EIA
coordinates, 13 owner swaps to the EIA utility name or to parents already in
the Parent(s) column, 3 fuels dropped because the EIA monthly table lists one
fuel, the conversion timepoint start year, and a controlled-vocabulary word.
Of the 178 fills, 37 were worth entering (start, retired and cancellation
years, dated Latest Activity, turbine models, in-development status detail);
the rest were operators EIA does not state, captive "no" values and engine
counts on turbines. Lessons are in the memo and drive the update-mode
narrowing in `notes/qc_checklist_plan.md`. After scoring, the blind lane
files were parked in `staging/blind/` and the trimmed set in `staging/`
built `deliverables/gogpt_batch_20261002_1547_ET_us-md_update_*`
(41 edits, 15 questions, 2 watch items).
Rebuilt the same day as the 1633 pair after the New York review showed
that Latest Activity is a date field in GEM (every filled value in the export
reads `Year: 2026, Month: 6, Day: 29`); the 8 Maryland values were free text.
The gate now fails free text there (`dates`), the sweep prompt says so, and
`docs/reference/lifecycle_rules.md` records the format.
Narrowed again on 2026-10-05 after Amalia Llano's New York review: Latest
Activity is only for stalled projects (in development, shelved or inferred
status) and only with a date at least a year old. All 8 Maryland values and 4
of the 5 New York values were dropped and the gate `latest-activity` now
fails such edits.

### New York result (2026-10-02)

First run in narrowed update mode: `batches/us-ny/`, deliverable
`deliverables/gogpt_batch_20261002_1631_ET_us-ny_update_*`. The brief
builder tasked 20 of 74 plants (status ladder plus export gap list plus
three possible-updates rows in `extra_tasks.json`) and left 54 alone; 8
Sonnet agents wrote 20 shards and a ninth wrote the statewide shard. Result:
26 edits, 29 questions, 2 watch items. What the agents got right without
help: the Maryland-lesson rules held (no coordinate, owner, fuel or captive
changes from EIA tables; the Lotus and Constellation purchases stayed as
questions because no document named the new plant-holding entity). What the
main-loop review changed: five Latest Activity values written as prose were
rewritten as dates, one of them (Caithness II) moved from a 2018 article to
the April 2025 Department of Energy document GEM already cited, and one
(Astoria NRG) was dropped because it would have moved GEM's date backward.
Nothing else needed trimming. The statewide agent could not reach the
Department of Environmental Conservation notice bulletin or the Public
Service Commission document system; NYISO queue and EIA-860M covered the
new-plant search.

## Order of work

1. Build the tooling (brief builder, sweep workflow, assemble, gate). Done
   when a dry run on Maryland produces briefs, a stub shard assembles, and the
   gate reports on it.
2. Run Maryland blind. Score. Fix whatever the scoring exposes in the SOPs or
   prompt. Build the Update deliverable from the same shards. Done 2026-10-02;
   the prompt and brief fixes (Location accuracy, owner convention, EIA
   monthly fuel, timepoint units, engine and captive fields) and the
   update-mode narrowing landed 2026-10-02 and were first used on New York.
3. Run ahead of Amalia's schedule where it helps: Georgia (10-05), Indiana
   (10-07), Kentucky (10-13), in update mode.
4. Texas, per `texas_pilot_plan.md` Phases 1 and 2.
5. The review app, reading `batches/us-<st>/staging/`. Done 2026-10-02: `review_app/`
   (ported from the pipelines researcher's app), decisions in
   `staging/review_log.jsonl`, consumed by `build_review_package.py --decisions`.
   Not yet tried on a live review pass; a shared (Google-hosted) version is a
   later step if more than one reviewer needs it at once.

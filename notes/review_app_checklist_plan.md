# Plan: sort the review page and the deliverable by the researcher's checklist

Written 2026-10-07 from the 2026-10-06 call with Amalia Llano (Gemini notes and
transcript in the shared Google Doc) and the current state of `review_app/`,
`review_data.py`, `build_review_package.py` and the staged lanes. Status:
decided with Baird 2026-10-07 (nine groups, the ask-the-PM flag, the watch
item calls, the IRP step), ready to build. Companion:
`notes/qc_checklist_plan.md` maps the checklist onto the research process;
this note maps it onto the review page and the actions workbook.

## What Amalia asked for, in her words and ours

1. The page should be organized so that going through it means going through
   the QC/Country checklist. She suggested sections like validation errors,
   LNG, backfilling missing dates and data sources and start years ("things
   wrong with or missing from the data we already have"), matching other
   data sources (EIA, EIP, Sierra Club), and general discoveries from the
   press. Baird suggested a second row of tabs or an extra filter. Both
   agreed the four tabs (major, minor, items, everything) are useful and
   should stay.
2. The checklist itself is comprehensive but repetitive. She wants it more
   compact and ordered the way research actually happens. The page can do
   that even if the sheet does not change, as long as each page group names
   the sheet rows it ticks.
3. "Items" are confusing. What is a concern versus a monitor? What does
   severity mean? She worked out: a concern is "something may be wrong", a
   monitor is "watch this". Her instinct for monitor items: they belong in
   the possible-updates sheet, in a plant comment, or in the state notes.
4. Monitor mixes two things: plants not in GEM yet (Gowanus and Narrows,
   Obrigheim) and watch items on plants GEM already has (North Tonawanda
   expansion, Morgantown phase 2). Baird: "break it into monitor for
   discovery and monitor for other things".
5. The tool is a research assistant and a work log. The researcher is the
   last filter; "accept" means "I checked this and I am putting it in the
   database". Keep the word accept. Hold could double as "a question for my
   PI or PM". A suggest should be able to carry a reference link.
6. Later: sync accepts against a fresh pull to catch "marked accepted but not
   yet in the database" (the apply-check in the QC workflow), and a short
   state summary the agent drafts for the country tips row.

## Design in one paragraph

Give every staged record a mechanical `checks` tag (which checklist rows it
serves) and a `group` (one of nine compact groups below), computed in
`review_data.py` and `build_review_package.py` from facts the record already
carries: lane, column, kind, current value, the unit's status group, and
the brief task that produced it. The page gets a **checklist view** in the
left pane that lists the nine groups with open and total counts and acts as
a filter across all plants; a group shows a check mark when everything in it
is decided, and each group names the sheet rows it covers so Amalia can tick
them. The per-plant tabs stay as they are. Items stop being a separate
concept: a concern appears inside its checklist group next to the edits on
the same field, with its own call vocabulary. The monitor lane is split into
"new to the tracker" and "watch item on an existing plant", with calls that
name a destination (possible-updates sheet, plant comment, state note,
dismissed). The actions workbook and evidence file carry the same group on
every row and gain a checklist summary sheet.

## The nine groups and the sheet rows they tick

Row numbers are the QC/Country checklist tab of the Q4 2026 Update V2 sheet
(gid in `docs/reference/sop_pointers.md`). Rows that say the same thing twice
land in one group once; the group lists both numbers.

| # | Group (page label) | Sheet rows | What lands here |
|---|---|---|---|
| 1 | Validation report | 7, 54 | Every edit or question whose brief task came from `validation_report.py` (`--validation`), plus the validation errors still open at build time, listed so the "fixed all errors" box can be ticked honestly |
| 2 | Blanks and unknowns | 8, 9, 11, 16, 17, 18, 19, 22, 25, 26 | Fills on Fuel, Status, Technology, Owner(s), Capacity (blank or zero), Start year (blank or unknown), Unit name, Retired year on a retired unit, coordinates, Location accuracy, City, State/Province; concerns on the same fields where nothing was found |
| 3 | Status and timeline | 10, 20, 21, 23, 24, 49, 50 | Status changes of any kind, Planned retire edits, Latest Activity on inferred or quiet projects, Start year deletions on shelved or cancelled units, the in-development units touched (row 10) |
| 4 | Conversions | 12, 13, 14 | Edits and questions on Conversion/replacement?, unit names needing "timepoint", gas technology on coal-to-gas units, steam turbine on waste-heat units, replacement-link questions (the G0 case) |
| 5 | Turbine make and model | 15 | Equipment Manufacturer/Model edits on in-development units |
| 6 | Owners and entities | 19, 43 | Owner, operator and parent edits, ownership share questions, the entity lane (new owners or operators to create). Parent-level portfolio changes are flagged here as questions for Dan until he rules (Amalia's open question) |
| 7 | IDs, IRPs and data centers (US only) | 34, 37, 38, 39 | Other IDs edits and ID questions from `match_ids.py`; everything the IRP step (below) produces: new plants and units an IRP plans, edits an IRP moves, the list of projects whose IRP box must be ticked in the web UI, and the draft Notes text for the US IRPs tab; captive and data-center edits and candidates. Hidden for country batches |
| 8 | New to the tracker | 6, 31, 44, 51, 55 | New plants and new units ready to add (the newplants and newunits lanes), candidates to watch that failed the add threshold (monitor, no GEM plant id), captive LNG candidates, and the possible-updates backlog rows for the scope with their done / Q2 2027 call |
| 9 | Close-out | 29, 30, 32 to 36, 52, 53, 56 | Not record-level. One panel on the statewide card: units to mark updated or no changes, the three-sentence state summary drafted from the state note, the assignments-tab columns M and N from the roster, links to the US tabs, and the two open questions the export cannot see (IRP checkbox, "no tracker found") stated as such |

Watch items on existing plants (the other half of monitor) do not have a
checklist row. They go in the group of the field they would change (a
planned expansion is group 3, a possible new unit is group 8, a data center
conversion is group 7) so nothing sits outside the checklist.

Rows 41 to 46 (optional block) are covered by groups 2, 6 and 8 where the
batch happened to find something; the page marks them "optional" in the
group's row list and never counts them as open.

## How the tag is computed (no new prompting)

Precedence, first hit wins for the group; `checks` keeps every row that
matches:

1. **Provenance.** `build_state_brief.py` already knows which checklist row
   each task serves (its gap list cites rows 8, 16 to 19, 26, 38; the
   validation tasks come from `--validation`; the backlog rows from the
   possible-updates sheet). Give each task a `check` id when the brief is
   written, store the per-unit task list with its fields in
   `sweep_args.json` or the shard meta, and let `assemble_state.py` copy the
   matching task's `check` onto every staged record whose field that task
   named. No change to the subagent prompt; the subagent never sees the
   number.
2. **Column plus current value.** For records without provenance (older
   batches, discovery, Germany): map the staged column and the current
   value to rows with a small table in a new `review_app/checklist.py`
   (shared by `review_data.py` and `build_review_package.py`). Start year
   with current blank or unknown on an operating unit is rows 9 and 18;
   Status change is 49 or 50 by direction; Latest Activity is 24; and so on.
3. **Lane.** newplants and newunits are group 8; entity is group 6; monitor
   splits by `monitor_kind` (below); qa falls through to its field.
4. **Fallback.** Anything unmatched is group 2 if it fills a blank, else a
   tenth bucket "other" that the page shows but never hides. The build
   prints the count of unmatched records so the table gets extended, not
   worked around.

`checks` and `group` are derived fields written into the review dataset and
the workbook; they are not added to the staged-JSON contract, so no rebuild
of old batches is needed and `qc_checks.py` is untouched.

## Items: fewer concepts, plainer words

- **Drop the severity filter** from the filter bar (the tabs already split
  major and minor; Amalia and Baird agreed the dropdown is not useful).
  Replace that slot with the checklist group filter.
- **Rename on the page**, keep the lane names in the files:
  concern becomes "question about existing data" (something GEM has may be
  wrong or could not be confirmed; calls: confirmed, dismissed, needs
  research); monitor becomes two things (next section); entity check becomes
  "new owner or operator to create". The how-to page gets a short glossary
  with these four definitions and one example each.
- **Concern types need a vocabulary.** The contract says
  existence, duplicate, scope, capacity-threshold, conversion-link,
  attribution, other, but the shards wrote 60-plus free-text variants
  (capacity, owner, status, location, start_year, ids, uprate_request...).
  Normalize in `assemble_state.py` to a field-based vocabulary (the staged
  column names plus duplicate, scope, identity, conversion-link, other) and
  make `state_gate.py` flag anything outside it. The field-based type is
  what lets a concern land in the right checklist group.
- **Show concerns next to the edits.** In a checklist group the questions
  on a field appear under the edits on that field, not on a separate items
  tab. The items tab stays for the "everything on this plant" view.
- **Calls.** Keep accept, hold, reject, suggest. Add an optional reference
  URL to suggest (Baird: "I should probably do that").
- **Ask the PM is a flag, not a call** (Baird 2026-10-07). Every line, item
  and plant card gets a checkbox "ask the PM" with a note. It sits beside
  the call, so an accepted edit, a held edit or a rejected one can all carry
  the flag. The flag is its own record type in the log (`flag: pm`,
  `on/off`, note, record id or plant id), so undo and the import treat it
  like a call. The filter bar gets an "ask the PM" facet and the left pane
  shows a count per plant; the build collects every flagged record into a
  "questions for the PM" section at the top of the evidence file and a
  `questions_for_pm` sheet in the workbook. This is what Amalia wanted hold
  to mean, without overloading hold.
- **Accept language.** In the how-to, say what accept means for a
  researcher working the page: "I checked this and I am entering it in the
  database myself." Keep the actions workbook as the record of accepted
  edits; add the apply-check later (item 6 above).

## Monitor: split in two

Decide `monitor_kind` per record in `assemble_state.py`, with an explicit
field the shard may set and a default from the data:

- **new_to_tracker**: `gem_plant_id` is empty. A plant or project GEM does
  not have. Shown in group 8 under "watch, not ready to add", beside the
  newplants records under "ready to add". Each shows the add-threshold leg
  that failed (`monitor_reason`), the capacity if known, and `recheck_by`.
- **existing_plant**: `gem_plant_id` is set. A development at a plant GEM
  tracks: an expansion, a repowering, a data center conversion, a second
  phase. Shown on the plant's card in the group of the field it would
  change, labeled "watch item".

Watch items do not take accept, because accepting a watch item means
nothing (Baird 2026-10-07). Both kinds take four calls that say what happens
to the item:

- **add to the database now.** The reviewer thinks the evidence is already
  enough. The item has no proposed cell values, only a description, a
  reason and sources, so this call cannot write a workbook row by itself.
  What it does: the reviewer may type what they know in the note (status,
  capacity, start year, unit count) and a reference link, the same box
  suggest uses. The build puts the item on a `promote_to_database` sheet
  with every field the record carries, the reviewer's note, the sources,
  and a blank for each required field it lacks. Then
  `build_state_brief.py --promote` turns that sheet's rows into briefs for
  a short follow-up sweep that completes the record (a full new-plant or
  new-unit record for a new_to_tracker item, a cell edit or new unit for an
  existing_plant item). The completed records come back onto the page as
  ordinary lines with the normal calls, and the watch item is closed with a
  link to them. Baird can skip the follow-up sweep and complete the record
  by hand in the web form when it is small; the sheet carries enough to do
  that.
- **hold.** Keep watching. `recheck_by` stays, the item returns on the next
  rebuild, and the note says what would change the call.
- **send to possible updates.** Amalia's current habit for these. The build
  writes the row in the possible-updates sheet's column order on a
  `possible_updates_rows` sheet for pasting, and closes the item on this
  batch.
- **remove from watch list.** Not a real lead, duplicate, out of scope,
  below the threshold for good. A required reason so the next batch does
  not re-add it. `assemble_state.py` reads the review log and drops a
  removed candidate that a later shard proposes again, with a line in the
  build output saying why.

The default is hold for both kinds. The how-to names the four calls and
says in one sentence each when to use them. Where Amalia would rather
record an existing_plant item as a plant comment or in the state note than
in the possible-updates sheet, the note on hold covers it and the close-out
panel repeats held items with notes.

Data fixes the split needs:

- The three batches write monitor records three ways: New York staging has
  `item` and no `monitor_reason`; the discovery folders have
  `monitor_reason`; Germany has neither and carries `capacity_mw` and
  `status` instead. Normalize at assemble time: `monitor_reason` and
  `recheck_by` required, `capacity_mw` and `status` optional and shown when
  present, `item` folded into `monitor_reason`. `state_gate.py` flags a
  monitor record missing either required field.
- The same candidate can appear in `staging/` and `staging-discovery/`
  (Gowanus and Narrows twice, with two spellings and two recheck dates).
  `review_data.py` should detect candidates with the same normalized name or
  the same queue id across the folders, keep one card, and show the other
  record as a duplicate note rather than a second decision.

## New research step: utility IRPs (US states)

Checklist rows 34 and 37 and the "US IRPs" tab of the Update V2 sheet
(gid 560668239). The tab, read 2026-10-07: a State header row, then one row
per utility with Utility, IRP year, File (one or more links, often a PDF
and a regulator docket), Notes (a running log with quarter prefixes such as
"Q2 2026 ..." and "Q4 2025 ...") and a sparse Updated IRP column. Thirty-nine
states, 92 utility rows. New York and Maryland have no rows (restructured
markets, no utility IRPs). Georgia has 1 row, Indiana 8, Kentucky 7. The
database's IRP checkbox IS in the export (the `IRP` column, yes/no), so the
repo can tell which units already have it ticked; the column is not a
research field, so it is never staged. A record flagged `irp: true` says the
finding comes from a plan, and the workbook and page pair that flag with the
unit's box state to say where to tick.

What a researcher does today: open the state's rows, read the IRPs for
planned gas resources, add anything new to the tracker, tick the IRP box
on those projects, and append a dated line to Notes. The repo takes that
over as a batch step, in the Update workflow after `match_ids.py`:

1. `irp_sheet.py --state <State>` reads the tab through `gsheets.py`
   (read-only work profile) and writes `work/irp_us-<st>.json`: the state's
   utility rows, the links split out, the Notes log split into dated
   entries. A state with no rows writes an empty file and the brief says
   "no utility IRPs on the sheet for this state; step skipped".
2. `build_state_brief.py --irp work/irp_us-<st>.json` adds an "IRP review"
   section to the statewide brief: per utility, the IRP year, the links,
   the newest Notes entries, and the GEM plants in the state owned or
   operated by that utility (joined on the owner and operator columns, with
   the parent where the entity lookup knows it). Tasks: fetch each IRP file
   through the fetch ladder and extract it locally (`pdftotext -layout`);
   find the preferred or recommended plan's gas additions, conversions,
   co-firing and retirements with capacity and year; match each against
   the GEM units in the state; stage a new plant or new unit for every
   planned gas resource GEM lacks, a cell edit where the IRP moves a known
   unit (status, capacity, start year, planned retire), and a watch item
   where the IRP names capacity without a site or a year. The IRP file is
   the data source, cited by the page or table the value appears on, and
   the regulator docket is the second source when it exists. Every finding
   carries `check: 37` so the page puts it in group 7.
3. `assemble_state.py` marks every record whose source is an IRP file with
   `irp: true`. The build lists those plants on an `irp_box` sheet (plant,
   unit, utility, IRP year) for the human to tick in the web UI, the same
   way missing IDs are listed for typing. No staging lane, no cell.
4. The build drafts a Notes entry per utility row in the tab's own style
   ("Q4 2026 <two or three sentences>: what changed, what was added, next
   IRP due date") on a `irp_notes_draft` sheet. Baird pastes it or
   approves a `gws-gem-write` call per row; the repo never writes the sheet
   on its own.
5. The close-out panel shows the IRP section as done when every IRP row
   for the state has a fetched file, a finding or a "nothing new" line, and
   a drafted Notes entry.

Two rules to confirm with Amalia or Dan before the first run:

- The Georgia row shows the team added 10 CT and 12 CC "plants" from the
  2025 IRP's capacity expansion table, with Sierra Club's scenario as the
  base case, even though those are generic blocks without sites. So an IRP
  preferred-plan resource counts as an announced project with the utility
  as the owner. Confirm that this is the rule for every state, and how the
  units are named when the IRP gives no site (the Georgia row uses the
  IRP's own labels, CT1 to CT13).
- Which plan counts when the IRP has no preferred case.

Decided 2026-10-07 (Baird): a draft IRP is enough to add a project. Until
the unsited-capacity rule is confirmed, unsited capacity goes to the watch
list (new to the tracker) with the IRP as the source, which loses nothing.

## The deliverable

- `edit_checklist` sheet: add a `checklist group` column and a `sheet rows`
  column. Keep the plant, unit, column walking order (that is how the web
  form is worked), so the group is a filter in Excel, not a sort.
- New `checklist_summary` sheet: one row per sheet row 6 to 56, with the
  group, how many edits and questions landed there, how many were accepted,
  how many are open, and a "tick it" column that says yes when nothing is
  open. Row 56 ("no tracker found") says the batch cannot see it.
- `monitor_list` splits into `watch_new_to_tracker` and
  `watch_existing_plants`, each with the reviewer's call and note. Three
  sheets fed by the calls: `promote_to_database` (items called "add to the
  database now", with known fields, note, sources and the blanks to fill),
  `possible_updates_rows` (items sent to the sheet, in that sheet's column
  order, ready to paste) and the removed items listed in the evidence file
  with their reasons.
- `questions_for_pm`: every flagged line, item or plant with the note.
- `irp_box` and `irp_notes_draft` from the IRP step.
- Evidence file: sections in group order 1 to 9 instead of lane order;
  "questions for the PM" at the top; held, rejected and suggested edits
  listed per group.

## The page

Left pane gets a second mode, "checklist", next to the plant list:

```
checklist                                   plants
[x] 1 validation report        0 open / 6
[ ] 2 blanks and unknowns     11 open / 19
[ ] 3 status and timeline      4 open / 9
[x] 4 conversions              0 open / 2
[ ] 5 turbine make and model   1 open / 1
[ ] 6 owners and entities      5 open / 8
[ ] 7 IDs, IRPs, data centers  3 open / 7
[ ] 8 new to the tracker       6 open / 6
    9 close-out                      panel
```

Clicking a group filters the plant list and the card to that group across
every plant in the state, in the same walking order; `j` and `k` move
through the group's open changes plant by plant. A group's header line
says "ticks rows 8, 9, 11, 16, 17, 18, 19, 22, 25, 26 on the QC/Country
checklist". When a group has nothing open, the box is checked and a short
line says what to do on the sheet. The card's four tabs are unchanged; the
"everything" tab ignores the group filter as it ignores every filter today.

The filter bar loses severity and gains two facets: checklist group and
"ask the PM". Each line, item and the card header carries the ask-the-PM
checkbox with a note; the left pane shows a small count per plant. Watch
items show their four calls instead of accept, hold, reject, suggest.

The statewide card gets the close-out panel (group 9). It is read-only text
plus two lists: units to mark updated or no changes (from the Research
status column and the units the batch touched), and the possible-updates
rows with a done / Q2 2027 call. A "copy" button on the state summary and on
the columns M and N values so they can be pasted into the sheet.

## Order of work

1. `review_app/checklist.py`: the groups table, the row-mapping table, the
   tagging function, tests. Cheap model, well specified.
2. `build_state_brief.py` gives tasks a `check` id and writes the task list
   per unit; `assemble_state.py` copies it onto records, normalizes concern
   types and monitor fields, sets `monitor_kind`; `state_gate.py` flags the
   gaps. Rebuild New York and Maryland staging from their shards to pick up
   the tags (record ids are unchanged, so Amalia's calls survive).
3. `review_data.py`: tags, monitor split, candidate dedupe, drop severity
   from the filter list. `app.js` and `style.css`: checklist mode in the left
   pane, group header lines, items shown inside groups, glossary in the
   how-to, the four watch item calls, the ask-the-PM checkbox and facet,
   reference URL on suggest. `store.py` and `static_store.js`: the new call
   vocabularies and the flag record type; `import_log.py` carries flags.
4. `build_review_package.py`: group columns, checklist summary sheet, the
   two watch sheets, promote and possible-updates sheets, questions for the
   PM, evidence sections by group. `build_state_brief.py --promote`.
5. Close-out panel on the statewide card, fed by `validation_report.py`,
   the roster and the state note.
6. Rebuild the New York and Maryland page, publish to the same artifact URL
   from the work profile, tell Amalia on Slack. Her feedback decides whether
   the groups change before Germany gets the same treatment.
7. The IRP step (`irp_sheet.py`, the brief section, `irp: true` in assemble,
   the two sheets), first run on Georgia, Indiana or Kentucky, after the two
   IRP rules above are confirmed. New York and Maryland are unaffected.

All seven steps were built 2026-10-07 (tests in `tests/test_checklist.py`,
`tests/test_review_app.py`, `tests/test_irp_sheet.py`). The IRP step's first
live read covered Georgia, Indiana and Kentucky (`work/irp_us-*.json`); no
batch has run with it yet, so the two IRP sheets and the IRP chip have only
been exercised on synthetic data. The New York, Maryland and Germany pages
were rebuilt and republished the same day.

## Decided 2026-10-07

- Nine groups, as named above.
- Ask the PM is a checkbox beside the call, filterable, not a fifth call.
- Watch items take add to the database now, hold, send to possible
  updates, remove from watch list. No accept.
- The IRP checkbox is a research step read from the US IRPs tab, not a
  pull question. The workbook tells the human which boxes to tick.

- "No tracker found" (row 56) is the web UI's search choice for combustion
  units whose tracker marker is null (no fuel, or several fuels and no
  primary one). Built 2026-10-07: `gem-db-ops/gogpt/no_tracker.py` queries
  it, `scripts/no_tracker.py --state/--country` writes
  `work/no_tracker_<tag>.md` for the close-out panel. Six live units
  worldwide today, none in the United States or Germany.
- A draft IRP is enough to add a project.

## Still open

- The unsited IRP capacity rule for Amalia or Dan.
- Possible-updates rows: handed to Amalia on the workbook sheet, since she
  owns the rows for her states; Baird pastes only when asked.

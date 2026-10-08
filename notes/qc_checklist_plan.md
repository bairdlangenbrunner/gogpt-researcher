# Plan: fold the QC/Country checklist into the research process

Written 2026-10-02. Status: draft, waiting on the open questions at the end.
Source: the "QC/Country checklist" tab of the Q4 2026 GOGPT Update V2 sheet
(link hub: `docs/reference/sop_pointers.md`) and the September 2026 Editing
Manual. The checklist is the list every researcher ticks off per country or
US state. This note says, item by item, where each one lands in this repo.

## The shape of an update, per the manual

The September 2026 manual (General Guidelines, Starting Research, Finishing
Research) defines an update like this. Everything below hangs off it.

1. Mark the country "in progress" on the assignments tab. Read the country
   tips. Open the possible-updates sheet and filter to the country.
2. Review units in priority order: in-development units (announced,
   pre-construction, construction); shelved and shelved-inferred units;
   units with a planned retirement this year; other units with a planned
   retirement. Operating units are not re-researched as a group.
3. Search for newly announced plants.
4. Every value entered gets a data source. Old data sources are never
   removed. "Not found" is only written after an actual search.
5. At the end: set every "in progress" unit's Research status to "updated"
   or "no changes"; review Assigned Comments; clear the possible-updates
   rows; update country tips; tick the checklist; download the Validation
   Report for the country and fix its errors; write the next-cycle time
   estimate on the assignments tab; mark the country "done".

Baird's direction (2026-10-02): the agent checks what the manual says to
check, in that order. It does not re-verify every reference or every data
point the way the pipelines "deep sweep" does. Where a value has no data
source, the agent does search for one and fills it.

## What this changes in the state sweep

The Maryland run in progress is a blind calibration: every unit, every field.
That is a one-time accuracy test, not the production shape. Production
"update" mode narrows to:

- **Per unit, the task depends on its status group.** In-development: has the
  status moved, is there a start year or scheduled operating event, turbine
  make and model, owner, capacity, and a Latest Activity entry if nothing
  has been reported for more than a year. Shelved and shelved-inferred: revived,
  cancelled, or still quiet; Latest Activity if the newest report is more
  than a year old. Cancelled-inferred: anything reported since. Planned retirement this year:
  did it retire; if nothing confirms it by December, the manual says add a
  scheduled retired event for next year. Other planned retirement: does the
  plan still hold.
- **Plus the gap list for that unit**, drawn from the export by the checker
  described below (blank fuel, status, technology, coordinates, accuracy,
  owner; zero capacity; unknown technology; unknown start year on an
  operating unit; missing owner; value present but data source empty).
- **Plus newly announced plants** for the state (discovery lane, folded in).
- **Operating units with nothing on the gap list are not touched**, except
  by the end-of-update "last minute" status pass (construction to operating,
  operating to retired).

The unit brief and the subagent prompt therefore need a "what to check for
this unit" block generated from status group plus gap list, and the subagent
budget should shrink accordingly. The 23-field blind list stays only for
calibration runs. Built 2026-10-02: `build_state_brief.py` (`unit_tasks()`,
`--scope ladder`, `--extra-tasks`) generates the block and narrows the field
list; the sweep prompt tells the subagent to do only those tasks. First used
on New York the same day. The separate `state_checker.py` below is still
unwritten; the brief builder covers rows 8, 16 to 19, 22 to 24, 26 and 38
inline, and the close-out items (53, 56) are still open.

## Item-by-item mapping

Columns: checklist item (row number on the tab), where it lands, status.

### [DURING UPDATE] Database block

| Row | Item | Where it lands | Status |
|---|---|---|---|
| 6 | Captive LNG sheet checked for new plants | Discovery step: read the Americas Qualifying tab of the captive LNG workbook, match Terminal IDs to the state, compare against GEM plants named "... LNG terminal power station" | New step, sheet is readable (see sop_pointers) |
| 7, 54 | Validation report errors fixed | `validation_report.py` reads the stored errors (`plant.validation`) from the read-only DB at batch start; `build_state_brief.py --validation` turns the research fixes into unit tasks; `--closeout` is the row 54 gate | Covered (2026-10-06) |
| 8 | No blanks for fuel, status, technology, country, coordinates, accuracy, owner | Mechanical: a per-state checker run on the fresh export, output feeds the gap list | Partly in `qc_checks.py --csv`; extend |
| 9, 18 | Unknown start year rechecked (operating units especially) | Gap list research task | Research task |
| 11 | Every unit has a unit name (not blank, not "--") | Mechanical checker | New check |
| 12 | Conversions carry "timepoint XYZ" in the unit name | Mechanical checker on units with Conversion/replacement set | New check. Exact naming rule to confirm against the manual's Conversion section |
| 13 | Coal-to-gas conversion units have gas fuel and gas technology | Mechanical checker, needs the unfiltered export for the coal side | New check |
| 14 | "Waste heat from natural gas" fuel means technology "steam turbine" | Mechanical checker | New check |
| 15 | Turbine make and model searched for in-development units | Research task, already in the Q4 priorities (Update SOP §3.1) | Covered |
| 16 | Zero-capacity units rechecked | Gap list research task | New gap rule |
| 17 | Unknown technology rechecked | Gap list research task | New gap rule |
| 19 | Missing or unknown owner searched | Gap list research task | New gap rule |
| 20 | No start year on cancelled or shelved units | Mechanical, already in `qc_checks.py` | Covered |
| 21 | Planned retirements searched | Research task, ladder steps 3 and 4 | Covered |
| 22 | Retired units have a Retired Year | Mechanical checker | New check |
| 23 | Planned retirement year not in the past; roll to next year in December if unconfirmed | Mechanical flag plus a research task on each flagged unit | New check |
| 24 | Presumed shelved or cancelled units have a date and source in Latest Activity | Mechanical checker on the inferred statuses | New check |
| 25 | Location data for every entry | Mechanical checker (row 8 covers it) | Covered by 8 |
| 26 | City and State/Province filled | Mechanical checker | New check |

### Q4 2026 Update Docs block

These are Google Sheet and Doc edits. The repo never writes to work Drive
without an explicit OK per edit, so the agent prepares the text and Baird
pastes it, or approves a `gws-gem-write` call.

| Row | Item | Where it lands | Status |
|---|---|---|---|
| 29, 35 | Country tips row or "United States research" row reviewed and updated | Close-out: the agent drafts the row text from `docs/country_notes/united_states/<state>.md`; manual paste | Draft step to add |
| 30 | Columns M and N on the assignments tab | M = next-update time estimate in days, N = status. Mirrored in `campaigns/q4-2026/roster.csv`; manual paste | Covered by roster, paste is manual |
| 31, 55 | Possible-updates sheet reviewed; rows marked done or "Q2 2027" | Already a batch-start step (Update SOP §3). The "gas/oil plants" tab is readable; Maryland has 2 rows, the US 88 | Covered; add the done / Q2 2027 wording to the close-out |
| 32 | "Gas power plant data sources - by country" doc updated | Close-out draft from source_roster and state notes | Draft step to add |
| 33 | Europe workflow doc | Not applicable to US states | Skip |
| 34 | US IRPs tab updated for the state | The IRP step drafts a dated Notes entry per utility row for pasting: the `irp_notes_draft` sheet of `build_review_package.py --irp` (`notes/review_app_checklist_plan.md`, "New research step: utility IRPs") | Built 2026-10-07 |
| 36 | US Data/Research Guide updated for the state | Close-out draft | Draft step to add |
| 37 | IRP box checked on all IRP projects | Resolved 2026-10-07: the box IS in the export (the `IRP` column, yes or no) but is never staged. The US IRPs tab of the Update V2 sheet lists each state's utility IRPs. `irp_sheet.py` reads the tab and the column, the scope-wide agent researches the plans for planned gas resources and stages what GEM lacks (a draft plan is enough), the assembler flags those records `irp: true`, and the `irp_box` sheet and the review page's IRP chip tell the human which boxes to tick in the web UI | Built 2026-10-07 |
| 38 | GEM IDs matched to EIA-860M, EIP, Sierra Club | Covered 2026-10-06 by `match_ids.py --state`: joins the export to the EIA-860M file, the EIP sheet and the Sierra Club list; missing IDs are listed for the human to type, disagreements become brief tasks (`build_state_brief.py --ids`), blank sheet rows are listed with GEM IDs for Baird to paste | Covered |
| 39 | Gas-powered data centers searched, captive data entered | Discovery search per state; captive fields are in the export | Research task to add to the state prompt |

### [OPTIONAL] block

| Row | Item | Where it lands |
|---|---|---|
| 42 | Exact location for approximate operating units | Optional research task, off by default |
| 43 | Ownership changes for operating units | Upstream `--ownership-scan` already surfaces candidates |
| 44 | LNG terminals with captive plants | Same as row 6 |
| 45, 46 | Country files folder, GEM data sources sheet | Read at batch start if useful; no write |

### [END OF UPDATE] block

| Row | Item | Where it lands | Status |
|---|---|---|---|
| 49, 50 | Construction to operating; other last-minute status changes | A "last minute" pass: in-development and planned-retirement units only, status fields only | New narrow pass |
| 51 | Newly announced projects | Discovery search | Covered |
| 52 | Used AI to search for changes | This repo is that | Covered |
| 53 | All "in progress" units moved to "updated" or "no changes" | The export has a Research status column. The checker lists units still "in progress"; the actions workbook already ends each unit with its Record of Full Updates entry | Covered, add the listing |
| 56 | "No tracker found" units reviewed | `scripts/no_tracker.py --state <State>` (or `--country`) lists the combustion units whose tracker marker is null, via `gem-db-ops/gogpt/no_tracker.py`; each live one is a web-UI fuel fix | Covered (2026-10-07) |

## Proposed new script: `state_checker.py`

One script, run on the fresh export, per country or state, before research
and again at close-out. Output: a plain-language markdown report plus a CSV
gap list that the brief builder reads. Checks, in checklist order: blanks
(row 8), unit name (11), conversion naming (12), coal-to-gas fuel and
technology (13), waste heat means steam turbine (14), zero capacity (16),
unknown technology (17), unknown start year (18), missing owner (19), start
year on shelved or cancelled (20), retired year present (22), planned retire
in the past (23), Latest Activity on inferred statuses (24), city and state
filled (26), missing EIA IDs (38), Research status still in progress (53),
values with an empty data source (Baird's fill-missing-references ask).
It reports; it never stages. Each hit becomes a research task on that unit
or a line in the close-out memo.

## Open questions (do not guess)

1. **Validation Report.** Resolved 2026-10-06. The per-project "Validation"
   field is the `plant.validation` column, readable through the read-only
   database connection, so no download is needed. `validation_report.py`
   reads it per country or state and sorts each error by the manual's
   co-located-coal exception. One check is still worth doing once: compare
   its New York or Maryland memo against the web UI tab, in case the tab
   recomputes errors the stored field does not hold yet.
2. ~~IRP checkbox~~ Resolved 2026-10-07 (Baird): it is a web UI box, and the
   research input is the US IRPs tab. See row 37 above and the IRP step in
   `notes/review_app_checklist_plan.md`. Baird confirmed 2026-10-07 that a
   draft IRP is enough to add a project. Still to confirm with Amalia or
   Dan: whether unsited IRP capacity is added as announced (the Georgia row
   did that).
3. **EIP and Sierra Club matching.** Resolved 2026-10-06 (Baird pointed at
   the sheets). The EIP dataset is the GEM-held "EIP_GEM IDs matched" sheet,
   newest "data filtered" tab; the ID is EIP's `facility__id`, recorded in
   Other IDs (location) as `EIP: <id>`, and the sheet's own GEM ID columns
   record the match from the other side. Sierra Club matches are recorded
   only in that sheet's GEM Location ID and GEM Unit ID columns, never in
   the database. `match_ids.py` does both; links in `sop_pointers.md`.
4. ~~"No tracker found"~~ Resolved 2026-10-07 (Baird): it is a choice in the
   web UI's combustion tracker search, and in the database it is a
   combustion unit with `trackerSearch` null (no fuel, or several fuels and
   no primary one). `gem-db-ops/gogpt/no_tracker.py` queries it and
   `scripts/no_tracker.py` scopes it per state or country. Six live units
   worldwide on 2026-10-07, none in the United States.
5. **Conversion unit naming.** The checklist says conversions include
   "timepoint XYZ" in the unit name. The manual's Conversion of Unit section
   needs a close read to confirm the exact pattern before the checker
   enforces it.
6. ~~Research status in the export~~ Resolved: the column is populated.
   Maryland today: 9 units "updated", 1 "no changes", 2 "in progress", 25
   blank (never given an entry this cycle). The checker lists the blanks and
   the in-progress units at close-out.

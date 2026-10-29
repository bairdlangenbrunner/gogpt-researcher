# Matching GEM IDs to the Sierra Club and EIP lists: a plan to automate checklist row 38

Written 2026-10-27 after Amalia Llano said that matching GEM IDs against the Sierra Club list and the Environmental Integrity Project (EIP) list takes her the most time on the checklist. Nothing here is built yet. The numbers come from the October 26 export and the two sheets as cached on October 27.

## What the step is today

The GOGPT US Data and Research Guide says: Sierra Club shares its gas plant dataset every quarter (ask at the end of January, April, July and October); for each state, check the Sierra Club data and match GEM IDs in the "MATCHED IDs" tab, with priority on in-development units; the data is for reference only and is never cited or shared outside GEM. It also says that when adding or editing any unit, check the EIA plant and generator IDs against the newest EIA-860M file and add them to GEM if missing.

The human work per state is: for every Sierra Club row in the state, find the GEM plant and unit and type their IDs into the sheet; compare the row's status, capacity, technology and owner with GEM and fix GEM where Sierra Club knows more; for the EIP sheet, find the GEM plant and unit for every EIP project in the state, type the GEM IDs into the sheet, and add the EIP facility ID into the plant's Other IDs box in GEM. The guide says "fill in columns C-F", but today columns C to F of the MATCHED IDs tab are the "Change in Status?", "Change in capacity?", "Change in tech?" and "Change in owner?" flags, and the GEM ID columns are I and J. Amalia should say which she fills.

## What the repo does now

`scripts/match_ids.py --state <State>` (built 2026-10-06) reads the scoped export, the EIA-860M file, the newest "data filtered" tab of the EIP sheet and the MATCHED IDs tab of the Sierra Club sheet, and writes `work/ids_<tag>.json` and `.md` with five lists: tasks (disagreements for the briefs), ids_to_add (IDs for a person to type into GEM), sheet_fills (GEM IDs for blank sheet rows, for a person to paste), leads (list rows with no GEM plant) and problems. `build_state_brief.py --ids` puts the tasks on the briefs and the missing EIA plants into the scope brief, and `state_gate.py` gate `ids_followup` makes the agent answer every missing EIA plant.

It has run on nine states (Alabama, Florida, Illinois, Iowa, Kansas, Maryland, Michigan, Mississippi, New York). It produced zero sheet fills in eight of them and two in Mississippi. The reason is the matcher: a Sierra Club row only gets a GEM ID when its ORIS code equals a GEM EIA code or the plant name matches at 0.85 or better, and most blank rows have neither (they are proposals that never got an ORIS code, often with names GEM spells differently). An EIP row only matches through the sheet's own GEM ID columns or a name, city and capacity score. Nothing writes to either sheet; the fills are for Baird to paste, and so far there has been nothing to paste. The step therefore still costs Amalia the same time it always did.

## What the two sheets hold

Sierra Club sheet, tab "MATCHED IDs", 2121 unit rows, status column "April '26 Status":

| Rows | Count |
|---|---|
| GEM Location ID filled (starts with L) | 1424 |
| GEM Location ID blank | 373 |
| Marked "excluded" (316 rows, 311 of them under 50 MW) | 316 |
| Location filled but GEM Unit ID blank | 95 |
| Blank rows the current ORIS rule could fill (GEM already holds the EIA code) | 28 |
| Blank rows with a GEM plant within 1 km of the sheet's coordinates | 35 |
| Blank rows with neither | 310 |
| Blank rows under 50 MW (should be "excluded") | 22 |

Of the 310 blank rows with no ORIS or coordinate match, 264 are Terminated with no change this quarter (mostly proposals cancelled before 2020, which GEM does not track, plus GEM plants with no coordinates), 43 are Planned and unchanged, 26 are Planned rows Sierra Club added this quarter, and 2 are Operating. By state the blank rows sit in Texas (116), California (22), Virginia (15), Indiana (13), Arizona and Pennsylvania (12 each), North Carolina (11), Idaho, Michigan and New York (10 each).

The same sheet holds a tab "GOGPT 02_25_2026", a GEM export with "SC Plant Key" and "SC Unit Key" columns filled on 970 and 643 rows. That is a crosswalk from GEM IDs to Sierra Club keys that the script never reads. The quarterly raw drops ("SC tracker (Jul 24)" through "SC tracker (Apr 26)") and several "[OLD] MATCHED IDs" copies are also there.

EIP sheet, newest tab "EIP 07/28/26 data filtered", 592 project rows (Texas 215, Indiana 30, Missouri, Louisiana and Ohio 22 each), 532 of them Proposed:

| Rows | Count |
|---|---|
| GEM Location ID filled by GEM ("for EIP blanks" column) | 490 |
| GEM Location ID filled by EIP (facility__gaspower_gemlocationid) | 478 |
| Both filled and equal | 373 |
| Both filled and different (renames and moves, noted in GEM Notes) | 12 |
| Only EIP's column filled | 93 |
| Only GEM's column filled | 105 |
| Neither | 9 |
| GEM Unit ID filled | 576 |
| "skipped - only TEF NOI info" in GEM Notes | 67 |

On the GEM side, 460 United States plants carry an EIP tag in Other IDs, and 262 of them carry a stale Airtable-style `rec_` ID from EIP's old system (for example A. B. Brown: "EIA: 6137, EIP: rec_d4f1u50q7easr8ra1e7g"). The newest tab uses uuid facility IDs. The older tabs (December 2025, January and March 2026) still hold the `rec_` IDs next to GEM IDs, so a crosswalk exists: 255 of the 262 stale plants resolve to a uuid through the sheet, 7 do not. A further 49 plants are matched on the sheet to a uuid that GEM does not hold.

## What to build

### 1. Run nationally, once per quarterly drop, and slice by state

Both sheets are national and the Sierra Club drop is quarterly, so the matching unit is the drop, not the state. `match_ids.py --all` runs every state in one pass against the fresh export and writes `work/ids/national_<date>/` with the full result and one slice per state. The per-state run used in a batch reads the national result when it is fresh (under a week) and only redoes its own state otherwise. The main new output is a paste block per sheet: one line per sheet row that the script can fill, carrying the sheet row number, the row's key (Plant Key_Unit Code for Sierra Club, facility and project ID for EIP), the GEM Location ID, the GEM Unit ID, a confidence word and a one-sentence reason. Row-aligned so it drops into the sheet as two columns.

### 2. A matching ladder with a confidence per row

Plant level, in order, stopping at the first sure hit:

1. The sheet's own crosswalks: the "GOGPT 02_25_2026" tab's SC Plant Key and SC Unit Key columns, and any already-matched row with the same Plant Key (if one unit of a plant has a GEM Location ID, every unit of that plant gets it). This alone should fill most of the 95 location-only rows and many blank ones.
2. ORIS code equals a GEM EIA plant code, in the scoped export and in the unfiltered one (coal plants with gas conversions or additions live on the GCPT side).
3. ORIS code found in EIA-860M but not in GEM: take the EIA plant's coordinates and name, find the GEM plant by distance and name, and list the EIA code as an ID to add.
4. Sheet coordinates within 1 km of a GEM plant, plus name or owner similarity (owner and ultimate parent against GEM Owner and Parent, which the current script ignores).
5. Name, state, owner and capacity at a lower bar, for proposals that never got an ORIS code or coordinates.

Unit level: Unit Code equals the EIA generator ID in GEM Other IDs (unit); then capacity, year in service and technology. Sierra Club lists a combined-cycle block as separate turbine rows where GEM has one unit, so several sheet rows map to the same GEM unit and the script says so instead of leaving them blank.

Every match gets a tier: sure (crosswalk, ORIS, generator ID), likely (coordinates plus name, or name plus owner plus capacity), guess (name alone). Sure rows go into the paste block as they are, likely rows go in with a flag, guesses only reach the review list. Unmatched rows get a verdict too: "excluded" when the unit is under 50 MW; "not in GEM" when the row is Terminated and no GEM plant matches (GEM tracks cancellations from 2020 only); "candidate add" when the row is Planned, Operating or newly added at 50 MW or more and no GEM plant matches, which goes to the briefs as a named add task exactly as the missing EIA plants do now.

Calibration before anyone trusts it: the 1424 rows Amalia and the team already matched by hand are a labeled set. Run the ladder blind on them with the GEM ID columns hidden and measure how often each tier is right. The sure tier should be right on effectively every row before it feeds a paste block; the likely tier's measured rate decides whether it is pasted or reviewed.

### 3. EIP in particular

- Build the `rec_` to uuid crosswalk from the older tabs and the newest tab, and list the 255 stale GEM tags as "EIP: <uuid>" IDs to add, with the old `rec_` ID beside each, plus the 7 that need a hand match.
- List the 49 uuid IDs the sheet already ties to a GEM plant that GEM does not hold.
- Fill GEM's "GEM Location ID (for EIP blanks)" column from EIP's own column on the 93 rows where only EIP filled it, and run the ladder on the 9 rows where neither is filled. The 105 rows where only GEM's column is filled are EIP's import problem, not ours.
- Use `facility__gem_wiki_link` to find the GEM plant (477 rows point at a wiki page; detection only, never a citation) and `facility__statefacilityidnumbers` (TCEQ regulated entity numbers, for the Texas pilot).
- The status, capacity and expected-year comparisons already produce tasks; keep them.

### 4. How the IDs reach GEM

Today every ID is typed by hand from the ids_to_add list, and a Sierra Club quarter can add hundreds. Two choices:

- Keep it by hand. The list is the deliverable, nothing else changes.
- Give Other IDs a place in the `updates` lane so the IDs ride the review page and the supervised browser apply like any other edit. Other IDs is a plain text box on the web form; CLAUDE.md says IDs have no Data Source and no staging lane, so the orphan-value check would exempt the two Other IDs columns the way it exempts inferred statuses. The staged value merges into the existing text and never drops an ID, with one exception to decide: whether a stale `rec_` ID is replaced by the uuid or kept beside it. Files touched: `schema_constants.py`, `qc_checks.py`, `assemble_state.py`, `build_review_package.py`, the review app columns and the browser apply field map.

Recommendation: the second, since the browser apply step already exists and Baird approves every save.

### 5. Whether the script may write to the sheets

Today the repo never writes to either sheet; the fills are pasted by a person. Three choices, from least to most automated:

- The paste block only (built in step 1). Amalia or Baird pastes two columns per state.
- A tab the script owns in each sheet, named "GEM matches <date>", written under `gws-gem-write` with Baird's OK per run; a person copies the rows across. The team's columns are never touched by a script.
- The script writes the GEM ID columns in the team's tabs directly, into blank cells only, never over an existing value, logging each cell it wrote, with Baird's OK per run.

Recommendation: the paste block first, the owned tab once the calibration numbers are in. Direct writes only if Amalia asks for them. None of this gets a standing authorization; the ledger's `log` tab stays the only one.

### 6. Gate and checklist

Row 38 passes for a state when every Sierra Club and EIP row in the state has one of: a GEM ID in the sheet (or in the paste block), "excluded", "not in GEM" with the reason, or a candidate add answered in `coverage.json`. `state_gate.py` gate `ids_followup` grows to cover that. The review page's group 7 ("IDs, IRPs and data centers") links the state's paste block and the ids_to_add list, and, if step 4 is taken, shows the Other IDs edits as records.

### 7. Order of work

1. Done: the profiling above.
2. The ladder, the tiers, the national mode and the paste block, with the blind calibration on the 1424 matched rows. This is the bulk of the work and is well specified, so a cheaper model can build it with tests on the nine cached states.
3. The EIP crosswalk and the stale-ID refresh list.
4. A national run on the April 2026 drop; Amalia's states first (the week-of-September-15 and September-22 lists), Texas last since it holds 116 of the blank rows and the Texas pilot has its own schedule.
5. The Other IDs lane and the sheet-write mode, once Baird and Amalia have answered the questions below.
6. Docs and tests: `docs/sops/update.md` step 7, `docs/workflows.md` section 2, `docs/sops/qc.md`, `review_app/checklist.py` row 38, `tests/test_match_ids.py`, and the memory note on the US state plan.

## Questions for Baird and Amalia

1. Which sheet columns does Amalia fill: the GEM ID columns I and J, the change flags C to F, or both? The guide says C to F, which no longer match the GEM ID columns.
2. When GEM holds a stale `rec_` EIP ID and the sheet gives the uuid, replace it or keep both?
3. May Other IDs edits go through the review page and browser apply (step 4), or stay a typed list?
4. Which sheet-write mode (step 5): paste block, a script-owned tab, or direct writes into blank cells with an OK per run?
5. For terminated Sierra Club rows with no GEM plant, should the sheet say "not in GEM" (and should under-50 MW rows say "excluded"), or stay blank?
6. Is a quarterly national run, with Amalia pasting the two columns for her states, the cadence she wants, or does she want the per-state slice inside each state batch as now?

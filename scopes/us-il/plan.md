# Illinois full redo plan (Q4 2026)

Planned 2026-10-29 by comparing the North Dakota plan (`scopes/us-nd/plan.md`) with the Illinois runs of 2026-10-09 to 2026-10-27 (`batches/us-il/INDEX.md`, `batches/us-il-val`, `batches/us-il-dc`). Scope tag `us-il`, every plant (38 plants, 143 unit rows in the 2026-10-29 export). Reviewer is Baird; the new staging goes onto his existing review page (`illinois` in `review_app/artifacts.json`, https://claude.ai/artifact/8C7yTha7YC2eYUdWxJ5Eik). This plan is written to be run by another session, probably on a cheaper model for the sweep, so it repeats what that session needs and names every file. Run every script from the repo root as `python scripts/<name>.py` unless a step says otherwise.

## Rule one: Baird's decisions stay as they are

Baird has already decided 62 items on the review page (saved in the page's own database, not yet in the ledger on 2026-10-29): in `batches/us-il/staging` 21 accepts, 21 holds (all the Fisk and Waukegan oil peaker new units, L100000103859 and L100000103875), 1 add to database and 2 "ask the PM" flags on Broadwing; in `batches/us-il-val/staging` 13 accepts and 4 rejects (location records on Joliet 29, Joliet 9 and Marion). 85 earlier edits are already typed into the database and sit in `batches/us-il/staging/applied_in_db.json`.

1. **Sync first.** Read the page's `logs` collection with ArtifactData (`list`, `out_dir` under the scratchpad), then `python review_app/import_log.py <saved file> --dirs batches/us-il/staging batches/us-il-val/staging batches/us-il-dc/staging --reviewer baird.langenbrunner@globalenergymonitor.org`, then `python review_app/pull.py`. Ledger appends through `ledger.py` are under standing authorization. Re-run both at the end of the run, before republishing, because Baird may keep reviewing while the run goes.
2. **Never edit, re-assemble or rebuild** `batches/us-il/staging`, `batches/us-il-val/staging` or `batches/us-il-dc/staging`. No `assemble_state.py`, no `repair_staged.py`, no `add_question_fields.py --merge` on those folders. Their records keep their `record_id`, value and note, decided or not.
3. **All new work goes in a new batch folder, `batches/us-il-full/`**, added as a fourth entry in the `illinois` page's `dirs`. The page then shows the old cards with their calls plus the new cards.
4. **No duplicate cards.** Before assembly is final, run a prior-decisions check (build it as `scripts/prior_decisions.py` with a test, see New tooling): for each new record, look up the same plant, unit and column in the three old folders. If the old record is decided (any call, holds included), drop the new record unless the new source contradicts the decided value; a contradiction becomes a `qa` record that names the old card and quotes both values. If the old record is undecided and the new value is the same, drop the new record. If the old record is undecided and the new value differs, keep the new record and say in its note which older card it replaces, so Baird can reject the old one.
5. **Watch items Baird marked "add to database"** become tasks through `build_state_brief.py --promote batches/us-il/staging` (and the other two folders).

## What the first Illinois run did, and what North Dakota does that it did not

| Step | Illinois (2026-10-09 to 10-27) | North Dakota plan (2026-10-29) | Redo |
|---|---|---|---|
| Plants briefed | 17 tasked plants (`--scope ladder`); 21 plants never briefed | every plant (`--scope all`) | every plant |
| In-development units | edited where a task pointed; no full re-check | Latest Activity, scheduled events, equipment on every in-development unit | full re-check of every field, with a re-verified card for each field that stands (see below) |
| Permit harvest | none before the sweep; the 2026-10-21 audit read the Illinois EPA notice web service by hand | `harvest_permits.py` built and tested before the sweep | build `scopes/us-il/harvest_permits.py` |
| Utility commission | Illinois Commerce Commission e-Docket "behind a reCAPTCHA", full-text site search only | `harvest_psc.py` built and tested | build `scopes/us-il/harvest_icc.py`; a reCAPTCHA is a reason to script through the real-Chrome route, never a stop |
| Queues | read by hand in the audit (PJM cycle export, serial XML, MISO JSON) | `pull_queues.py --state ND` with `scopes/us-nd/queues.json` | write `scopes/us-il/queues.json`, run `pull_queues.py --state IL` |
| Existing links | not run (built 2026-10-23) | run before and after the sweep | run |
| Data centers | separate catch-up batch `us-il-dc` after the fact | `data_center_fleets.py` before briefs | run before briefs; the five `us-il-dc` adds are re-checked, not re-staged |
| Questions | free-text notes, older format | four-part `qa` records, gate `questions` hard | four parts, gate hard (assembled after 2026-10-28) |
| Watch items | 11 then 20, several with case "unverified" | seven named watch cases only, add threshold low | every old watch item re-decided under the add rule (new records only) |
| Turbine make and model | not asked | every unit (checklist row 15) | every unit |
| Coal side | not checked | each coal plant checked for a gas conversion or gas unit | check |
| Decisions section, export facts, lead list, done list | spread across INDEX lines | written up front | below |

## Decisions to confirm with Baird before the sweep (do not assume)

- Batch folder name `us-il-full` and adding it to the existing `illinois` page rather than a new page.
- Whether the PJM Cycle C01 gas requests (C01-1569, 1570, 1571, 2036) count as citable through each request's own PJM page (`https://www.pjm.com/m/ProjectTransition/SISReportDetails?queueNumber=<n>`) plus a cycle or study report that gives capacity and fuel. If yes, each is an add at `announced` under the add rule (Discovery SOP §3.1); if no, a watch item with case `nothing verified`. The 2026-10-23 run left this to him and he has not answered.
- Tilton and Alsey threshold calls (`ids_followup` in `batches/us-il/coverage.json`), also unanswered.
- Model per step: Sonnet for the per-plant sweep and for writing the harvesters, Opus for the statewide agent and any location review, the main loop for gate, prior-decision and merge calls.

## What the export shows (2026-10-29 pull, last row updated 2026-10-21)

- 38 plants, 143 unit rows. In development: Broadwing Energy Center L100000407695 (one unit, pre-construction) and Lincoln Land energy center L100000402416 (two units, pre-construction). Every other plant is operating or retired. Every plant's location is exact, so the location step has no candidates unless a new plant is added.
- Never briefed in the first run (21 plants, most last updated 2021 to 2023): Calumet Energy Team L100000401565, Cordova Energy L100000401836, Crete Energy Venture L100000401840, Elgin L100000401904, Energy Shelby County L100000402273, Freedom power project L100000402290 (retired), Gibson City L100000402074, Goose Creek L100000402336, Holland L100000401561, Interstate L100000401810, Jackson Generation L100000402412, Kendall County L100000401890, Kinmundy L100000402337, Lincoln Generating Facility L100000402049, MEPI GT Facility L100000401578 (retired), Morris cogeneration L100000402519, Pinckneyville L100000402340, Raccoon Creek L100000402341, Rocky Road L100000402254, Southeast Chicago Energy Project L100000401941 (retired), Venice L100000402342.
- Briefed once: Aurora, Broadwing, CPV Three Rivers, Elwood, Grand Tower, Joliet 29, Joliet 9, Lee, Lincoln Land, Marion, Rockford I and II, Nelson, Tate & Lyle Decatur, University Park North and South, Zion.
- Staged and undecided in the old folders: the five data center plants in `us-il-dc` (Aligned Elk Grove Village, Aligned Northlake, Compass Hoffman Estates, CyrusOne Aurora, Edged DeKalb Project Vector), the 20 or so watch items in `us-il` (PJM C01 requests, MISO J2656, the Ameren requests with fuel hidden, Garden Prairie, Byron to Wayne Thermal, three data center campuses, Nelson), and most `qa` records.
- Re-derive all of this from the fresh pull at run time; Baird may have typed more edits since.

## In-development units: check every field, even when nothing changes

This is new. The first run only touched the in-development fields a task named, so a plant with nothing to change showed nothing on the review page, and Baird could not tell whether it had been checked. For every in-development unit (Broadwing, Lincoln Land, any unit the run adds, and the five `us-il-dc` data center plants as candidates), the brief asks the agent to check each field below against a current source and stage either an edit or a re-verified record (`reverified: true`, verdict `match`, a fresh ref that states the value; blue in the workbook):

Status (and the 2-year shelved and 4-year cancelled tests from Latest Activity), Status Detail (additive, newest on top), Latest Activity and its source, Start year, Capacity (MW) nameplate, Turbine/Engine Technology, Equipment Manufacturer/Model, Number Of Engines and Capacity Per Engine where engines, Owner(s), Parent(s), Operator(s), Fuel, CHP, Captive and Backup Power fields, Location (city, county, coordinates and accuracy), Other IDs (EIA plant and generator codes, listed for Baird, never staged), the PJM or MISO queue numbers, the Illinois EPA permit numbers and dates, and any 2026 or 2027 scheduled event (financing close, construction start, permit expiry such as Lincoln Land's January 21, 2027 construction deadline). If no source newer than the current Latest Activity exists, say so in a `qa` record in four parts, with what was searched.

Apply a lighter version to every operating plant too: owner and parent, PJM or MISO deactivation notices and withdrawals, status, capacity against EIA-860M, turbine make and model (row 15), and a re-verified record for each field checked.

## State context

`scopes/us-il/note.md` holds it (two grid operators, PJM deactivation page, the 2021 Climate and Equitable Jobs Act deadlines and the 2026 Clean and Reliable Grid Affordability Act, regulators, recent events, gotchas). Update its "Still open" section at the end of the run. Do not repeat it in briefs beyond what `build_state_brief.py` inlines.

## New tooling (build and test before the sweep)

Same shape as the North Dakota and Michigan tools, on `scripts/harvest_lib.py`, tests in `tests/` on saved sample pages following `tests/test_harvest_permits_north_dakota.py` and `tests/test_pull_queues.py`.

1. `scopes/us-il/harvest_permits.py --scope us-il` writes `scopes/us-il/work/permits/<plant_id>.md`, `_unmatched.md` and `index.json`. Sources: the Illinois EPA public notice web service (`https://webapps.illinois.gov/EPA/WebSiteApi/api/PublicNotices/`, about 2,185 notices on 2026-10-21; read every Bureau of Air notice, current and archived, and open each construction, PSD, Title V and Clean Air Act Permit Program document); the Bureau of Air permit pages and any permit document database the agency publishes (find it, script it); the EPA RACT/BACT/LAER Clearinghouse (RBLC) for Illinois gas turbine and engine entries; Wayback CDX prefix listings for notice folders whose live index is closed. Match by facility name words, city, county and Illinois EPA site number. Power facilities with no GEM match go to `_unmatched.md` with equipment, MW, maker, model and dates.
2. `scopes/us-il/harvest_icc.py` writes `batches/us-il-full/harvest/icc_dockets.json` in the contract `build_state_brief.py --harvest` reads (`{"dockets": [{"docket", "utility", "filed", "title", "url", "facts", "matched", "documents"}]}`) plus `.md`. The e-Docket search sits behind a reCAPTCHA: go through `fetch.py`'s real-Chrome route, replay the session with curl as the Mississippi commission harvester does, and use direct docket-number addresses where known. Search by entity (ComEd, Ameren Illinois, MidAmerican, Dairyland, NRG, Constellation, Vistra, LS Power, Hull Street, Rockland, Invenergy, Competitive Power Ventures, Southern Illinois Power Cooperative, Prairie Power, Illinois Municipal Electric Agency, every data center operator above) and by filed date from 2024-01-01. Most gas plants are merchant and file nothing here; the targets are utility resource filings under the 2026 act's planning process, certificates for gas lines to plants, and data center tariff cases.
3. `scopes/us-il/queues.json` for `pull_queues.py --state IL`: `name` "Illinois", `markets` ["PJM", "MISO"], `pjm_states` ["IL"], `owner` for Ameren Illinois and the other Illinois-only MISO transmission owners, `shared_owner` for owners shared with neighbors, `known` patterns from the PJM and MISO entries the 2026-10-21 audit matched (Nelson, Broadwing, Lincoln Land, Elwood, Lee, Zion and so on). Make sure the PJM reader covers the cycle requests (the audit found C01 requests only in the cycle export; `scopes/us-il/coverage.json` entry `pjm-cycle-queue` says where to cite them). Output `batches/us-il-full/harvest/queues.json` and `.md`.
4. `scripts/prior_decisions.py --new batches/us-il-full/staging --old batches/us-il/staging batches/us-il-val/staging batches/us-il-dc/staging` implements rule one step 4: reads each old folder's `review_decisions.json`, `applied_in_db.json` and staged files, prints and writes `batches/us-il-full/prior_decisions.md`, and with `--apply` removes dropped records from the new folder only and turns contradictions into `qa` records. Test it on a copy of the current staging. It never writes to an old folder.

## Known leads the run must settle (each becomes a record or a coverage answer)

- The PJM Cycle C01 gas requests at Braidwood, Byron and LaSalle (346 MW each) and Putnam (1,150 MW): decided as above once Baird answers.
- AB1-089 near Nelson: duplicate check; settle against the queue pages and permits, then a duplicate question or nothing. MISO J1839 was settled 2026-10-30 as Broadwing's grid request (a duplicate question on Broadwing in the qa file).
- MISO J2656 (Latham, Macon County) and the Ameren-area requests with fuel hidden: re-read the MISO JSON; a filled fuel decides it.
- Nelson 38 MW uprate (PJM, May 2026): an uprate on an existing unit is a capacity question, not a new unit.
- Lee sale to Hull Street (one POWER article says closed August 26, 2026): find a second publisher or a PJM or FERC filing; owner edit or question.
- Zion parent after the Constellation and Calpine deal; Elwood owners per unit and plant codes 55199 and 69979.
- NRG fleet and Midwest Generation reliability extensions through May 31, 2031: whether NRG accepted, any new deactivation letter since July 2026.
- Lincoln Land: construction start before the January 21, 2027 permit deadline, financing, a new offtaker after Eagle Rock left, the 1,276 against 1,100 MW question.
- Broadwing: construction start, equipment, the 452 MW gross capacity edit already staged.
- Fisk and Waukegan peakers: Baird holds every new unit; research nothing new on them unless a source contradicts a held value, then a `qa` record.
- The five `us-il-dc` data center plants: re-check each against the fresh permit harvest and `data_center_fleets.py` output; new facts go in as new records under rule one.
- Joliet Technology Center, Monarch Rock Air in Rockford, Hut 8 Illinois Project 4, Garden Prairie, Byron to Wayne Thermal: decide each under the add rule and the seven watch cases.
- Tilton and Alsey: Baird's threshold call.
- The 21 never-briefed plants: full operating checks as above.
- Coal side from the unfiltered export (Powerton, Will County, Waukegan, Joliet, Kincaid, Baldwin, Newton, Prairie State, Dallman and the rest): any gas conversion, gas unit added at the site, or gas replacement plan.
- Every EIA-860M Illinois gas or oil plant not in GEM: answered in `coverage.json` under `ids_followup` as add, below threshold, out of scope or already in GEM.

## The run

A. Start. Rule one step 1 (sync). From `scripts/`: `python ../../gem-db-ops/gogpt/pull.py --output gem_export_gogpt.csv`, `python pull_gem_db.py --map-only`, `python scope_filter.py`, `python export_to_dump.py`. Back at the root: `python scripts/validation_report.py --state Illinois`, `python scripts/assigned_comments.py --state Illinois`, `python scripts/no_tracker.py --state Illinois`, `python scripts/worklist.py --state Illinois --all`, the upstream scans (`python3 upstream/gogpt-tracker/scripts/gogpt_csv_query.py --country "United States" --state Illinois` with `--counts-only`, `--ownership-scan`, `--in-progress-scan`, `--duplicate-scan`, `--possible-updates`), `python scripts/irp_sheet.py --state Illinois`, `python scripts/captive_lng.py --state Illinois`, `python scripts/eia860m.py --check` then `python scripts/match_ids.py --state Illinois`, `python scripts/location_candidates.py --state Illinois`. Compare the fresh export with the facts above and list every row Baird changed since 2026-10-21. Write `batches/us-il-full/extra_tasks.json`: the in-development field list as a task on Broadwing and Lincoln Land, the operating checks on every other plant, and the leads above.

B. Build and test the four tools in New tooling, then harvest: `python scopes/us-il/harvest_permits.py --scope us-il`, `python scopes/us-il/harvest_icc.py --scope us-il`, `python scripts/pull_queues.py --state IL --out batches/us-il-full/harvest`, `python scripts/check_existing_links.py --state Illinois --batch batches/us-il-full`, `python scripts/data_center_fleets.py --state Illinois`. Read the EIA-860M operating, planned, retired and canceled sheets for Illinois and the EIA-860 plant, generator and owner tables. Every give-up goes in the access log, never in a note.

C. Briefs and sweep. `python scripts/build_state_brief.py --state Illinois --mode update --scope all --batch batches/us-il-full --extra-tasks batches/us-il-full/extra_tasks.json --validation work/validation_us-illinois.json --ids work/ids_us-illinois.json --irp work/irp_us-illinois.json --captive work/captive_us-illinois.json --existing-links batches/us-il-full/existing_links.json --harvest batches/us-il-full/harvest --data-centers <the data_center_fleets.py json> --promote batches/us-il/staging --promote batches/us-il-val/staging --promote batches/us-il-dc/staging` (check each flag against the script's `--help`; paths moved into `scopes/` on 2026-10-29). Copy `scopes/us-il/coverage.json` as the statewide source list; add entries for the new harvesters. Then `python scripts/build_sweep_args.py --batch batches/us-il-full --model sonnet --group-max 5` and run the Workflow with `scriptPath: .claude/workflows/state-sweep.js` as `docs/workflows.md` §7 step 4 describes. The statewide agent (Opus) reads every `_*.md` brief and writes `shards/_state.json` and `batches/us-il-full/coverage.json`, answering every source, every data center and every EIA plant. Re-run any plant whose shard was not written.

D. Location pass only for plants handed back with `location_needs_review` and for new plants: `python scripts/build_sweep_args.py --batch batches/us-il-full --location-review --model opus`.

E. Assemble and gate, new folder only. `python scripts/assemble_state.py --batch batches/us-il-full`, `python scripts/check_existing_links.py --state Illinois --batch batches/us-il-full` again, `python scripts/prior_decisions.py ... --apply` (rule one step 4), `python scripts/access_audit.py batches/us-il-full --retry`, `python scripts/state_gate.py --batch batches/us-il-full --validation work/validation_us-illinois.json --entity-check --strict-questions` until GATE CLEAN, `python scripts/qc_checks.py --staged batches/us-il-full/staging` with zero errors, `python scripts/validation_report.py --state Illinois --closeout` must print CLOSE-OUT CLEAN, `python scripts/assigned_comments.py --state Illinois --closeout` must print COMMENTS CLEAN. Read the `note-drift` line and fix questions it touches.

F. Deliverables and the page. Stamp with `TZ=America/New_York date "+%Y%m%d_%H%M_ET"`; `python scripts/build_review_package.py --staging-dir batches/us-il-full/staging --scope us-il --mode update` (never overwrite an earlier stamp). Add `batches/us-il-full/staging` to the `illinois` page's `dirs` in `review_app/artifacts.json`, sync decisions again (rule one step 1), `python review_app/build_all.py --check`, rebuild and republish the page from the work profile, `--mark-published illinois`. Open the page and confirm every old call still shows. Add a line to `batches/us-il/INDEX.md` pointing at the new folder, and refresh the roster row in `campaigns/q4-2026/roster.csv`.

G. Drafts for a person, never written to Drive by the repo: research status per unit, the IDs list for Baird to type, EIP and Sierra Club rows to fill, possible-updates notes, the United States research tab line for Illinois naming both grid operators, the "used AI" tick.

## What done looks like

- Every one of the 38 plants has a brief, a shard and at least one card on the page, an edit or a re-verified record, and both in-development plants have a card for every field in the list above.
- No decided card changed, and no new card repeats a decided one (`batches/us-il-full/prior_decisions.md` says so).
- `batches/us-il-full/coverage.json` answers every statewide source, every data center and every EIA plant.
- Every lead above is a staged record, a four-part `qa` record or a coverage answer with the source read.
- GATE CLEAN, zero `qc_checks.py` errors, CLOSE-OUT CLEAN, COMMENTS CLEAN, no unretried give-up.
- The note's "Still open" section lists only what Baird must decide.

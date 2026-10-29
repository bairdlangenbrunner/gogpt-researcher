# Michigan update batch plan (Q4 2026)

Drafted 2026-10-23. Scope `us-mi`, all 32 plants (61 units in the 2026-10-23 10:33 export; the roster row says 60). Built the same way as the Mississippi plan (`scopes/us-ms/plan.md`) and on the same lessons from Kansas and Illinois. Checked against the export only so far; the Editing Manual, kickoff doc, United States data guide, QC/Country checklist tab and possible-updates sheet are read in step A.

## Decisions (Baird 2026-10-23)

- Amalia Llano finished her own Michigan pass on 2026-10-23. This batch is a full update of every plant and unit on a fresh pull taken after her edits, to find what she has not caught yet. Her edits are the starting point, not something to redo.
- Michigan goes on the shared review page for Amalia, https://claude.ai/artifact/7bnX9RMity3Yw5mdaojNaL.
- Queue tooling: a new `pull_queues.py --state MI` that takes the state as an argument (MISO plus PJM), so later states reuse it. `scopes/us-ms/pull_queues_mississippi.py` and its Mississippi output stay as they are.
- Models: same split as Mississippi. Sonnet for the per-plant sweep and scripted harvesting, Opus for the statewide agent and the second location look, the main loop for gate and merge calls.

## What the export already shows

- Status mix: 6 pre-construction, 1 construction, 1 mothballed, 53 operating. No announced, shelved or cancelled units.
- Possible duplicate: "48th Street power station" (L100000401789, unit 9, 84 MW, 2000, City of Holland) and "491 E 48th Street power station" (L100000409227, unit 9, 83.5 MW, 2000, City of Holland). Run the upstream duplicate scan and settle it first; a merge is a web form fix for a person.
- Midland Cogeneration Venture unit 2 is a 380 MW fuel oil unit marked mothballed, last touched December 2023. Unit 1 is 1849 MW combined cycle. Check the mothball date (tracked from 2020 only) and whether unit 2 still exists.
- Dan E Karn units 3 and 4 (693 and 710 MW steam, Consumers Energy) have a planned retirement of 2031. Check it against the newest Consumers Energy resource plan.
- Belle River: the coal to gas conversion is already in the database as timepoint 2 units (unit 1 operating on gas from 2026, unit 2 in construction). Check the conversion fields pair up on the coal side (row 12) and that unit 2's coal row still says operating with a 2026 planned retirement.
- New since the last cycle and all marked approximate location: Bay County (450 MW), Genesee County (900 MW), Handy Township (1400 MW, DTE) and Milan Township (700 MW, DTE). Technology is unknown on Bay County and Genesee County. These four are the location step's whole list (rows 25, 42). The IRP box is yes on three of them; Milan Township says no, check it (rows 34, 37).
- MEC North and MEC South (500 MW each, Development Partners Group, 2034, Siemens H class) were last edited by Dan O'Beirne on 2026-08-04. Confirm with a primary source; the owner looks like a single-purpose developer.
- Turbine make and model is blank on 58 of 61 rows (row 15). This is the biggest fill job.
- No unit has a Latest Activity entry.
- Other IDs (unit) is blank on 5 rows: the four new plants and the Delta RICE set (row 38). `match_ids.py` should cover them.
- 30 of 61 rows were last touched in October 2021. Operating units come after the priority work.
- Ownership to check, from memory, not yet verified: Consumers Energy may now own New Covert (listed as New Covert Generating Co LLC), and the Dearborn Industrial Generation owner should be checked against EIA-860.
- Coal side, from the unfiltered export: Campbell, Monroe, Karn 1 and 2, Presque Isle, Eckert, Erickson, Shiras, River Rouge, Harbor Beach, Marysville, Cobb, Endicott and the cancelled Karn/Weadock expansion. Watch Campbell and Monroe for gas replacements or conversions, and check the Escanaba mill's gas share (rows 12, 13).
- Grid: most of the Lower Peninsula is MISO Zone 7 (DTE Electric, Consumers Energy), the Upper Peninsula is MISO Zone 2 (Upper Michigan Energy Resources, UPPCO, Marquette), and the southwest corner is in PJM through Indiana Michigan Power. Check which plants sit in PJM (Indeck Niles and New Covert are the likely ones). The United States research tab needs a Michigan line that names both markets (row 35).

## Guardrails (already built for Mississippi, carried over)

1. Statewide coverage gate. Write `scopes/us-mi/coverage.json` before the sweep. Sources: EGLE Air Quality Division permits to install and the MiEnviro portal, Michigan Public Service Commission electronic dockets (DTE Electric and Consumers Energy integrated resource plans and certificates of necessity, Wolverine Power, Michigan Public Power Agency and Lansing Board of Water and Light filings), the MISO queue and ERAS entries, the PJM queue for southwest Michigan, EIA-860M and EIA-860, the DTE, Consumers Energy, Wolverine and Upper Michigan Energy Resources newsrooms, the possible-updates sheet, the captive LNG sheet (likely nothing for Michigan) and data center campuses (Saline Township and any others with on-site gas, watch list only).
2. Existing-link check before the sweep (`check_existing_links.py --state Michigan`).
3. Chase gate, lead-site rule, two-publisher rule for status changes, every missing EIA plant a named brief task. No changes needed.

## New tooling

1. `scopes/us-mi/harvest_permits.py`. Scout EGLE first: the MiEnviro portal, the older permit to install search and the Air Quality Division public notice pages. Script whatever search form or paged table the portal uses and read every document for each GEM plant and every unmatched power or data center facility. Write the unmatched list for the coverage entry, as Mississippi does.
2. `scopes/us-mi/harvest_psc.py`. Scout the Commission's docket site and script its search. Priority dockets: the current DTE Electric and Consumers Energy resource plans and any certificate of necessity cases for the four new plants.
3. `pull_queues.py --state MI`, built from `scopes/us-ms/pull_queues_mississippi.py` (MISO JSON plus the PJM queue file), with the state's utilities and markets as settings rather than hard-coded.
4. Tests for each, following the Mississippi tests.

## The run

A. Start. Assignment set to in progress (person). Fresh pull, `pull_gem_db.py --map-only`, `scope_filter.py`, `export_to_dump.py`. Then `validation_report.py --state Michigan` (row 7), `assigned_comments.py --state Michigan`, `no_tracker.py --state Michigan` (row 56), `worklist.py`, the four upstream scans (the duplicate scan settles 48th Street), `irp_sheet.py --state Michigan` (row 34), `captive_lng.py --state Michigan` (rows 6, 39, 44), `match_ids.py --state Michigan` (row 38), `location_candidates.py`. Draft `scopes/us-mi/note.md` with the grid structure and the regulators (rows 29, 35, 36).

B. Harvest. Start the EGLE harvester first, since it will be slow. Then the Commission harvester, the queue pull and `check_existing_links.py --state Michigan`, plus EIA-860M and EIA-860.

C. Briefs and sweep. `build_state_brief.py --scope all` with `--validation --irp --captive --ids --location --existing-links ../batches/us-mi/existing_links.json --harvest ../batches/us-mi/harvest`. Brief tasks: the 48th Street duplicate, Midland unit 2, Karn 3 and 4 retirement year, the Belle River coal side, technology for Bay County and Genesee County, MEC North and South, owners at New Covert and Dearborn, turbine make and model on every unit (row 15), Latest Activity, 2026 scheduled events and the December rule, retirements and planned retirements (rows 21 to 23). Sweep order: in development, planned retirements, mothballed, then the operating fleet.

D. Statewide agent on Opus. Newly announced projects (row 51), especially utility plants named in the DTE and Consumers Energy plans and queue entries in MISO and PJM; data centers to the watch list only (row 39); the `match_ids.py` leftovers; the Campbell and Monroe replacement checks.

E. Assemble and gate. `assemble_state.py`, `qc_checks.py --staged` with zero errors, `state_gate.py` with every gate, `access_audit.py --retry`, `validation_report.py --closeout` must print CLOSE-OUT CLEAN (row 54), last-minute status pass (rows 49, 50).

F. Deliverables. `build_review_package.py --irp` for the actions and evidence pair, then add Michigan to the shared review page for Amalia.

G. Drafts for a person, never written to Drive by the repo: research status per unit (row 53), columns M and N time estimate (row 30), the United States research tab line for Michigan (row 35), possible-updates notes (rows 31, 55), the Q4 2026 country tips row, IRP Notes lines (row 37), the "used AI" tick (row 52).

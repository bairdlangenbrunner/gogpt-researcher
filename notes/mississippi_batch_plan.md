# Mississippi update batch plan (Q4 2026)

Planned 2026-10-23 for Amalia Llano's Mississippi assignment. Scope `us-ms`, all 24 plants (53 units in the 2026-10-22 export). Checked against the September 2026 Editing Manual, the Q4 2026 kickoff doc, the GOGPT United States data guide, the QC/Country checklist tab and the possible-updates sheet. Built on what went wrong in Kansas and Illinois (`batches/us-il/audit/`, `batches/us-ks/access_audit.md`).

## Decisions (Baird 2026-10-23)

- Build the guardrails below before any research runs.
- Re-research Andrew Mkali's April 2026 "no changes" units in full (Colossus 2, Delta Blues, New Caledonia, Traceview, Vicksburg).
- Mississippi goes on the shared review page, https://claude.ai/artifact/7bnX9RMity3Yw5mdaojNaL.
- Use the cheapest model that is good enough at each step: Sonnet for the per-plant sweep and for scripted harvesting, Opus for the statewide agent and the second location look, the main loop for gate and merge calls.

## What the export already shows

- Clean today, re-check at the end: no blank fuel, status, technology, coordinates, location accuracy, owner, unit name, city or start year; no unknown technology, zero capacity or "not found" start year (checklist rows 8, 9, 11, 16 to 19, 26).
- Moselle 3 is operating with a planned retirement of 2025, which is in the past (row 23).
- Traceview Unit 1 has no turbine make and model (row 15) and is the only plant with an approximate location (rows 25, 42).
- New Caledonia's six 83.3 MW units are GE 7E.03 heavy-duty frames, so six units is right; the aeroderivative set rule does not apply.
- Colossus 2 unit 2 is 1240.5 MW of Solar Titan 350 turbines. Check it against the set rule and the state air permit.
- Other IDs (unit) is blank on 10 rows: both Colossus 2 units, the six New Caledonia units, Traceview and Vicksburg 1A. Required for the US (row 38).
- The IRP box is "no" on all 53 rows. Delta Blues, Vicksburg and Traceview came out of Entergy Mississippi planning, so each needs an IRP check (rows 34, 37).
- No unit has a Latest Activity entry. Every in-development unit should get one where a dated event exists.
- 35 of 53 rows were last touched in October 2021. Operating units come after the priority work.
- Chevron Pascagoula (101 MW, at the refinery) has blank captive fields. Optional check.
- Baxter Wilson 2 has a retired year of 2018, before the 2020 tracking floor. Amalia added it in July 2025, likely as the link for the Vicksburg replacement. Ask her before any change.
- Coal side, from the unfiltered export: Daniel coal Unit 2 has a planned retirement of 2029 (watch for a gas conversion); Jack Watson's timepoint pairs are correct (row 12); Kemper Project is a cancelled coal IGCC (check that the gas-fired Kemper units are tracked correctly); Morrow coal retired 2018 with its gas replacement in place.
- Operator is optional in the manual ("do not specifically search for it"). Blank operator sources are not a gap.
- Possible-updates sheet: four Mississippi rows, all marked done. The TVA carbon capture study at Ackerman (Quantum Choctaw) says "check next cycle", so it is live work (rows 31, 55).
- The United States research tab lists Mississippi as MISO only. Southern Company (Mississippi Power) and TVA are missing (row 35).
- The "by country" data sources doc has no US entries (row 32).

## Guardrails, built first

1. Statewide coverage gate. A fixed list of Mississippi sources in the country notes: the MDEQ Permit Board and its air permit archive, Mississippi Public Service Commission dockets (Entergy Mississippi certificates and IRPs, the Mississippi Power IRP), the MISO queue and ERAS list, the Southern Company and TVA interconnection queues, TVA environmental reviews, EIA-860M and EIA-860. `state_gate.py` fails if any source on the list is not marked searched with what was found.
2. Pre-sweep harvesters. `harvest_permits_mississippi.py` for MDEQ, a Public Service Commission docket harvester, and a MISO queue pull. Every document read, the agents start from documents.
3. Existing-link check before the sweep. Generalize `stage_saved_copies.py` so every Data Source link already in the database goes through `fetch.py` and a Wayback lookup, with saved copies staged before research starts.
4. Chase gate. A qa note saying a thing was noticed in passing or not researched fails `state_gate.py`.
5. Lead sites (Cleanview, interconnection.fyi, gridstatus, GridInfo, Wikipedia, the Global Energy Observatory, the WRI database) start a search. A value resting only on one of them stays yellow; the `lead-only` gate is advisory (Baird 2026-10-23). gem.wiki and globalenergymonitor.org are never cited.
6. A status change is green only on two independent publishers. EIA alone leaves it yellow.
7. Every EIA plant `match_ids.py` lists as missing from GEM becomes a named brief task.

## The run

A. Start. Assignment set to in progress (person). Fresh pull, `pull_gem_db.py --map-only`, `scope_filter.py`, `export_to_dump.py`. Then `validation_report.py --state Mississippi` (row 7), `assigned_comments.py --state Mississippi`, `no_tracker.py --state Mississippi` (row 56), `worklist.py`, the four upstream scans, `irp_sheet.py --state Mississippi` (row 34), `captive_lng.py --state Mississippi` (rows 6, 39, 44: Gulf LNG Pascagoula, xAI, Amazon), `match_ids.py --state Mississippi` (row 38), `location_candidates.py`. Draft `docs/country_notes/united_states/mississippi.md` with the grid structure (Entergy Mississippi and Cooperative Energy in MISO South, Mississippi Power under Southern Company, TVA in the north) and the regulators (rows 29, 35, 36).

B. Harvest. `harvest_permits_mississippi.py --scope us-ms` (over an hour, start it first), `harvest_psc_mississippi.py`, `pull_queues_mississippi.py` and `check_existing_links.py --state Mississippi`, plus TVA environmental reviews and EIA-860M and EIA-860. The TVA queue is not scripted: read the newest queue file in the TVA OASIS document folder or its Wayback copy (`docs/reference/site_access.md`).

C. Briefs and sweep. `build_state_brief.py --scope all` with `--validation --irp --captive --ids --location --existing-links ../batches/us-ms/existing_links.json --harvest ../batches/us-ms/harvest`. Brief tasks: 2026 scheduled events and the December rule, turbine make and model (row 15), Latest Activity, retirements and planned retirements (rows 21 to 23), conversions (rows 12, 13), the Ackerman carbon capture study, the Colossus 2 set count and permit. Sweep order: in development, planned retirements, then the operating fleet.

D. Statewide agent on Opus. Newly announced projects (row 51), data centers to the watch list only (row 39), the match_ids leftovers, the Daniel 2 and Kemper conversion checks.

E. Assemble and gate. `assemble_state.py`, `qc_checks.py --staged` with zero errors, `state_gate.py` with every gate including coverage and chase, `access_audit.py --retry`, `validation_report.py --closeout` must print CLOSE-OUT CLEAN (row 54), last-minute status pass (rows 49, 50).

F. Deliverables. `build_review_package.py --irp` for the actions and evidence pair with the IRP sheets, then add Mississippi to the shared review page.

G. Drafts for a person, never written to Drive by the repo: research status per unit (row 53), columns M and N time estimate (row 30), the United States research tab text adding Southern Company and TVA (row 35), possible-updates notes (rows 31, 55), the Q4 2026 country tips row, IRP Notes lines (row 37), the "used AI" tick (row 52).

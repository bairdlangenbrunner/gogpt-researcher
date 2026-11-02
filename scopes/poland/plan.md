# Poland update batch plan (Q4 2026)

Planned 2026-10-29 for Dan O'Beirne's Poland assignment. Scope tag `poland`, every plant (45 plants, 60 unit rows in the 2026-10-29 export). Built on the North Dakota plan (`scopes/us-nd/plan.md`) with the US-only steps removed and Polish sources in their place. Written to be run by another session, probably on a cheaper model, so it names every file. Run every script from the repo root as `python scripts/<name>.py`. The umbrella plan for Dan's countries is `notes/europe_batches_plan.md`.

## Decisions (settled by Baird 2026-10-29)

- Poland runs first of Dan's countries. The packet should be ready by about 2026-11-06, before Dan reaches Poland on 2026-11-09.
- Dan is the reviewer. The staging goes onto his existing review page, the `germany` entry in `review_app/artifacts.json`: add `batches/poland/staging` to its `dirs`, rebuild with `review_app/build_all.py` and republish.
- Baird tells Dan about the batch himself. Baird is registering the ENTSO-E API token; until it arrives, the ENTSO-E step is skipped and recorded as waiting for the token, not as blocked.
- Model per step: Sonnet for the per-plant sweep and the scripted harvesting, Opus for the country-wide agent and the second location look, the main loop for gate and merge calls.
- **Not yet settled: the PSE connection list leads.** It names about ten large gas projects GEM lacks. That is over the five-candidate line in CLAUDE.md, and some are only connection requests. Research them and stage `qa` records with the facts; ask Baird and Dan before staging any as `newplants`.

## What the export already shows (2026-10-29 pull)

- 45 plants, 60 unit rows. Operating 30, pre-construction 13, construction 11, announced 4, shelved 1 (PGE Solidarity), cancelled by inference 1. Last Updated is mostly 2023-05 (18 rows) and 2025-10 (12 rows).
- `worklist.py --country Poland` (`work/worklist_poland.csv`): priority 1 (in development) 28 rows, priority 2 one, priority 4 two, priority 5 (the rest) 28, priority 9 one.
- Validation report (`work/validation_poland.json` and `.md`, 2026-10-29): 33 plants with errors, 45 fix items, 411 optional. 38 fixes are "A step in the status history has no date". Owner 1 has no source at Gdańsk-2 and Krakow-Leg. Location has no source at three plants, including Krakow-Leg. Jaworzno phase 2 unit 1 timepoint 2 (G100001017887) has blank latitude and longitude; Jaworzno GT1 (G100001090157) has no source for the disrupted-by-conflict field. Łagisza unit 8 (G100000106102) has no source for capacity, technology, combined heat and power, or carbon capture. Wierzchowice unit 1 has no source for combined heat and power.
- Assigned comments (`work/comments_poland.md`): 4 open of 14. Rybnik G100000401340 status, nearing completion (assigned to Dan). Pomorzany G100001090292 status, Dan set pre-construction against another source's announced. Dolna Odra G100000102397, units 7 and 8 retire in 2026. Bydgoszcz, plant name, and "Coal units replaced by new gas capacity?".
- `no_tracker.py` lists no units. `captive_lng.py` finds no task (the Polish Baltic Sea Coast floating terminal T100000130731 is excluded).
- Location (`work/location_poland.md`): 12 plants. Approximate: Grudziądz, Jaworzno, Makowisko, Ostrów Wielkopolski, PGE Solidarity, Pelplin, Turek, Ursus. No source: Bydgoszcz, Dąbrowa Górnicza, Lodz-4, Zachód.
- Upstream scans: unit counts 59 total and 28 in development; the in-progress scan flags most in-development units; the duplicate scan is noise (936 pairs); possible-updates has 4 open rows (Nowa Sarzyna sold to Axpo, renewablesnow; PGE contracts for new gas plants, ceenergynews 6 March 2026).
- Coal side (unfiltered export, 307 Poland rows, 232 coal): 25 rows linked to a conversion, 46 live coal plants to check for gas units (Bełchatów, Opole, Łaziska, Bielsko-Biała, Katowice, Tychy, Wrocław, Łódź-3, Szczecin, Puławy, Chorzów Elcho, Zabrze, Nowa, Białystok, Mielec, Świecie, Konin, Pątnów, Turów and others).

## Country context

In `scopes/poland/note.md` (inlined into every brief): grid operator, regulator, who issues environmental decisions and integrated permits, owners, the two drivers of new gas plants, and the sources probed on 2026-10-29.

## Guardrails

1. Country coverage gate: `scopes/poland/coverage.json` (15 entries, shipped with this plan). `state_gate.py` fails if any is not answered in `batches/poland/coverage.json`.
2. Harvesters run before the sweep; agents start from documents, not search results.
3. Existing-link check before the sweep, saved copies staged first.
4. Chase gate, lead-site rule, two-publisher rule for status changes, seven watch cases only, `qa` records in four parts, additive Status Detail and Notes. All exist.
5. Access audit: `access_audit.py batches/poland --retry`; gate `access` fails on an unretried give-up. The URE register site is the one to watch.
6. Capacity auction MW and connection MW are never staged as nameplate capacity (note gotcha). The brief says so and the gate check below enforces it.

## New tooling

Items 1 and 3 were built on 2026-10-29; item 2 is next. Tests keep saved rows and page text inline, following `tests/test_pull_queues_north_dakota.py`.

1. Built: `scopes/poland/harvest_pse.py`, tests in `tests/test_harvest_pse_poland.py`. First run (2026-10-29, list dated 2026-09-30, auctions 2021 to 2030): 96 entries, 48 matched to GEM plants, 6 gas connection requests with no GEM plant (Pątnów block 9, Pątnów combined cycle 1 and 2, Turów, Opole, Łaziska 1 and 2) plus a small engine at Żory, and 41 new units on 15 to 17 year contracts with no fuel shown. Settings are in `scopes/poland/harvest_pse.json`, not `queues.json`, because `pull_queues.py` reads every `scopes/*/queues.json` as a US state. Writes `batches/poland/harvest/queues.json` in the contract `build_state_brief.py --harvest` reads: `{"entries": [{"source", "queue_id", "fuel", "facility_type", "mw", "status", "queue_date", "in_service", "poi", "url", "matched": [{"plant_id", "how"}]}]}`, plus `queues.md`.
   - PSE connection list: download the XLSX, save a dated copy to `scopes/poland/work/pse/connection_list_<YYYYMMDD>.xlsx`, read sheet `Wykaz wspólny`, keep rows whose type is `BG`, `BGP`, `SG`, `JS` or `MIX` or whose name has a gas word (gaz, CCGT, OCGT, BGP, silnik). `source` is `pse-8l`, `queue_id` the object ID, `mw` the injected MW, `status` the connection stage, dates from the conditions and agreement columns.
   - Capacity auctions: scrape each delivery-year page from the index and archive pages, download every final-results PDF to `scopes/poland/work/pse/auctions/`, parse with `pdftotext -layout` one row per line. Keep new and upgraded units. `source` is `pse-auction-<year>`, `queue_id` the `JRM/` code, `mw` the obligation (marked `obligation_mw` so the brief never shows it as nameplate), `in_service` the delivery year, `facility_type` new, upgraded or existing, plus contract years and supplier.
   - Match to GEM plants by name words with and without diacritics, owner and town, plus hand-checked patterns in `scopes/poland/harvest_pse.json` (`known`: plant ID to regexes, for example `grudzi` for L100000401438, `ostro[lł][eę]k` for L100000103234, `vivos 2|pelplin` for L100001081028, `vivos 3|makowisko` for L100001083279, `elkogaz|kozienice` for L100000103233). Every match still says check.
2. `scopes/poland/harvest_permits.py`. Writes `scopes/poland/work/permits/<plant_id>.md`, `_unmatched.md` and `index.json`, same shape as `scopes/us-nd/harvest_permits.py`. Sources:
   - Marshal office integrated permit lists for every region holding a GEM plant or a candidate. Start from the region list page (Kujawsko-Pomorskie at the address in `coverage.json`); find the others from each marshal BIP. Download every gas or oil combustion permit from 2020 on and extract MW electric, MW thermal, unit list and dates.
   - gov.pl search API for each plant and candidate name, kept to the RDOŚ, GDOŚ and ministry paths, with attachments read (PDF and Word).
   - Ekoportal list by municipality for every plant in development, recording the case number and office of each environmental decision found.
3. Built: `scripts/match_registers.py --country Poland` (the European counterpart of `match_ids.py`, shared with Romania and the UK), tests in `tests/test_match_registers.py`. It reads the EEA large combustion plant table (bulk zip cached in `work/eea/`) and, when `ENTSOE_API_TOKEN` is set, the ENTSO-E per-unit list, joined on the ENTSO-E codes already in GEM's Other IDs. Writes `work/ids_poland.json` and `.md` in the `match_ids.py` contract. `build_state_brief.py --ids` and `state_gate.py` gate `ids_followup` now take leads with source `eea` or `entsoe` and a country's `ids_<tag>.json`; a country batch with no such file is skipped. First run: 44 gas-burning combustion plant parts matched, 7 leads (Kielce, Katowice and Bielsko-Biała heat and power plants, Mondi Świecie, two Grupa Azoty sites). The ENTSO-E reader has not seen a live response yet.
4. `data_center_fleets.py --country Poland` already handles the 20 MW threshold. Check its Polish campus list against the probe's (Atman, Equinix, Data4, Vantage, EdgeConneX, VPLS, Beyond.pl).

## Known leads the run must settle (each becomes a record or a coverage answer)

- PSE connection list gas projects GEM lacks: Turów CCGT (PGE, 550 MW), OCGT Kraków Wanda and OCGT Lublin Abramowice (300 MW each), OCGT Opole Dobrzeń (880 MW), Pątnów block 9 (464 MW) and Pątnów CCGT 1 and 2 (1,830 MW), Łaziska OCGT 1 and 2 (200 MW each) and Łaziska gas engines (120 MW), Połaniec peaker (257 MW). Research each, then `qa` records until Baird and Dan settle the add question.
- Capacity auction units: two PGE Inwest units (JRM/2126 and JRM/2129, 548.9 MW obligation each, 2030, which may be Turów or Rybnik II), Łagisza (Tauron, JRM/2356, 538 MW, 2030, against GEM's 100 MW unit), Włocławek CCGT (Orlen, JRM/234, 299 MW), Gorzów (63.7 MW), Kraków and Gdynia gas engines (45.4 MW each), Veolia Poznań (105 MW) and Łódź (175 MW), PGE Energia Ciepła units of 137 and 140 MW, Encos (45.6 MW) and an unnamed 40 MW unit (JRM/385). Identify each and match it to a GEM unit or answer it.
- Possible adds from the probes: Tauron's three gas engines at Czechowice-Dziedzice (about 30 MW, contract May 2025); KGHM Polkowice gas-steam plant (about 40 MW, 2014; check whether GEM has it); Tauron Tychy unit (50 MW, fuel unknown); Orlen Południe at Trzebinia (61 MW, fuel split unknown).
- Grudziądz: unit 1 is 563.34 MW electric in the integrated permit of 30 June 2026 (GEM has 560 MW); the second block's environmental decision is still to find, probably on the city site.
- Adamów: GEM has GT1 600 MW under construction for 2027; the ministry decision of 24 March 2026 on its gas pipelines and the 2026 auction row (PAK CCGT, 493 MW obligation) are the documents to read.
- Ostrów Wielkopolski (600 MW in GEM): find the developer and the source. The PSE connection list has a row there.
- Kozienice: two blocks of 668 MW gross against GEM's 700 MW each.
- The four open comment threads, the possible-updates rows (Nowa Sarzyna to Axpo; PGE contracts) and the coal side list above.

## The run

A. Refresh (an hour). Fresh pull chain (`../../gem-db-ops/gogpt/pull.py`, `pull_gem_db.py --map-only`, `scope_filter.py`, `export_to_dump.py`), then `validation_report.py --country Poland`, `assigned_comments.py --country Poland`, `no_tracker.py --country Poland`, `worklist.py --country Poland`, `captive_lng.py --country Poland`, `location_candidates.py --country Poland`, `match_registers.py --country Poland`. Compare with the facts above and note any row Dan changed. Write `batches/poland/extra_tasks.json` with the leads above as plant tasks.

B. Harvest (a day). `python scopes/poland/harvest_pse.py --scope poland`, `python scopes/poland/harvest_permits.py --scope poland`, `check_existing_links.py --country Poland --batch batches/poland`, `data_center_fleets.py --country Poland`. Retry the URE register site. Every give-up goes in the access log.

C. Briefs and sweep (a day). `build_state_brief.py --country Poland --mode update --scope all --extra-tasks batches/poland/extra_tasks.json --validation work/validation_poland.json --ids --captive --location --existing-links batches/poland/existing_links.json --harvest batches/poland/harvest --data-centers` (no `--irp`). Brief tasks beyond the leads: 2026 scheduled events and the December rule; turbine or engine make and model on every in-development unit; Latest Activity on every in-development unit; a date for every status history step the validation report lists. Then `build_sweep_args.py --batch batches/poland --model sonnet --group-max 5` and the Workflow with `scriptPath: .claude/workflows/state-sweep.js` (`docs/workflows.md` §7). The country-wide agent (Opus) reads `briefs/_state.md`, `_harvest.md`, `_data_centers.md`, `_captive.md`, `_existing_links.md` and writes `shards/_state.json` and `batches/poland/coverage.json`.

D. Location pass. `build_sweep_args.py --batch batches/poland --location-review --model opus` for plants handed back with `location_needs_review`, per `docs/reference/location.md`. Integrated permits and environmental decisions carry parcel numbers (działka); the national parcel map (geoportal.gov.pl) places them.

E. Assemble and gate. `assemble_state.py --batch batches/poland`, `check_existing_links.py` again, `access_audit.py batches/poland --retry`, `state_gate.py --batch batches/poland --validation work/validation_poland.json --entity-check --strict-questions` until GATE CLEAN, `qc_checks.py --staged batches/poland/staging` with zero errors, `validation_report.py --country Poland --closeout` CLOSE-OUT CLEAN, `assigned_comments.py --country Poland --closeout` COMMENTS CLEAN.

F. Deliverables. Stamp with `TZ=America/New_York date "+%Y%m%d_%H%M_ET"`; `build_review_package.py --staging-dir batches/poland/staging --scope poland --mode update`; `recalc.py` on the workbook; a line in `batches/poland/INDEX.md`; the roster row in `campaigns/q4-2026/roster.csv`; add `batches/poland/staging` to the `germany` page's `dirs` in `review_app/artifacts.json`, rebuild with `review_app/build_all.py` from the work profile, republish and `--mark-published`.

G. Drafts for Dan, never written to Drive by the repo: research status per unit, a time estimate, possible-updates notes, the Q4 2026 country tips row, the "used AI" tick.

## What done looks like

- `batches/poland/coverage.json` answers all 15 entries of `scopes/poland/coverage.json` and every data center.
- Every lead above is a staged record, a four-part `qa` record, or a coverage answer with the source read.
- GATE CLEAN, zero `qc_checks.py` errors, CLOSE-OUT CLEAN, COMMENTS CLEAN, no unretried give-up.
- The Poland staging shows on Dan's review page, and Baird has the link to send.

# Germany redo batch plan (Q4 2026)

Planned 2026-11-04, the day after the Bundesnetzagentur published the first capacity tender awards. Scope tag `germany`, run folder `batches/germany-redo` (the `-redo` run suffix in `scripts/paths.py`, so work files land in `scopes/germany/work/germany-redo/`). Every plant: 208 plants, 359 unit rows in the 2026-11-04 export. Built on the Poland plan (`scopes/poland/plan.md`) and the North Dakota blueprint (`scopes/us-nd/plan.md`). Run every script from the repo root. The umbrella plan for Dan O'Beirne's countries is `notes/europe_batches_plan.md`.

## Decisions

- Baird 2026-10-29: redo Germany North Dakota style once the awards are out, every plant, every current step.
- Baird 2026-11-04: the redo runs now, ahead of Poland, Romania and the United Kingdom.
- The October packets stay as they are. `batches/germany/` (2026-10-05 1741 pair, Dan's 22 review calls in `staging/review_log.jsonl`) and `batches/germany-permits/` (2026-10-06 1434 pair) are never rebuilt or moved, because the review log is keyed by their staging paths. The redo writes to `batches/germany-redo/`.
- Nothing October proposed is proposed again. Each of the 81 plants October touched carries a brief task listing what was staged and Dan's call, and a field is staged again only with newer or different evidence, with a note saying it replaces the October record.
- Dan is the reviewer. The redo staging goes onto his existing review page, the `germany` entry in `review_app/artifacts.json`, like every country in the umbrella plan.
- Model per step: Sonnet for the per-plant sweep, Opus for the country-wide agent and the second location look, the main loop for gate and merge calls. ENTSO-E stays skipped until Baird's token arrives.

## What the export shows (2026-11-04 pull)

- 208 plants, 359 unit rows. Operating 299, pre-construction 15, announced 12, retired 12, mothballed 6, construction 5, cancelled by inference 5, shelved by inference 2, cancelled 2, shelved 1. Last Updated is mostly 2023-10 (242 rows). Researchers: Harvey Hassan 306 rows, Andrew Mkali 36, Dan O'Beirne 14.
- Worklist (`work/worklist_germany.csv`): priority 1 (in development) 32 rows, priority 2 three, priority 4 four, priority 5 (the rest) 301, priority 9 nineteen.
- Validation report (`work/validation_germany.json`): 83 plants with errors, 140 fix items, 1 person item, 542 optional.
- Assigned comments (`work/comments_germany.md`): 16 threads, 4 open. Maxau Mill duplicates and Dan's rename proposal; Lippendorf owners twice (EP Energy Transition from January 2026; Vereinigte Energiewerke dissolved into Vattenfall GmbH, E100001000092); Krefeld-Uerdingen captive use.
- `no_tracker.py`: none. `captive_lng.py`: three qualifying terminals with no GEM plant (Brunsbüttel T100000130460, Mukran T100000131141, Wilhelmshaven T100000130458). Location (`work/location_germany.md`): 20 candidates. `match_registers.py` (`work/ids_germany.md`): 341 matched, 67 leads from the EEA large combustion plant table, all in thermal MW, which are never staged as electrical capacity.
- `data_center_fleets.py` first run: only the 4 GEM data center plants (Frank Cube, IQ Energy Center, KMW, Mainz). Germany has no harvested permit list of data center engines yet, so the country-wide agent searches the hubs (task in `extra_tasks.json`) and the step runs again after the harvest.

## The award list (3 November 2026)

Bundesnetzagentur press release https://www.bundesnetzagentur.de/SharedDocs/Pressemitteilungen/DE/2026/20261103_StromVKG.html and award list `Kapazitaetsmarkt/Ausschreibung/Gebotstermin_Sep26/_DL/Zuschlagsliste.pdf` (address in `coverage.json`, entry `stromvkg-tenders`). Eleven awards, 5,160 MW, effective 2026-11-10, delivery by 2031. Register records for all 24 units: `scopes/germany/work/stromvkg/award_units_mastr_20261104.json`.

| Bid | Project | Register gross MW | GEM now |
|---|---|---|---|
| LZK-0926-5 | RWE GuD Gersteinwerk (GT 559.04 + steam 278.86) | 837.9 | CC1 800, pre-construction, 2030 |
| LZK-0926-16 | RWE GuD Weisweiler (GT 555.12 + steam 278.68) | 833.8 | CC 800, pre-construction, 2030 |
| LZK-0926-20 | RWE GuD Voerde | 880.4 | unit 1 850, announced, 2030 |
| LZK-0926-13, -17, -21, -40 | LEAG Gaskraftwerk Jänschwalde 20, 40, 30, 10 | 560 each | one CC1 900, pre-construction, 2028 |
| LZK-0926-34, -41 | LEAG Gaskraftwerk Boxberg 20, 10 | 560 each | no gas unit (Boxberg is a coal plant, L100000101978) |
| LZK-0926-33 | Gasturbinen Kraftwerk Leipheim 20 (open cycle) | 322.7 | GT2 550, pre-construction, no year |
| LZK-0926-35 | Stadtwerke Karlsruhe HKW-West, 12 engines | 54.0 | West unit 1 42 operating; RDK CC1-12 50 with no owner |

An award is a capacity contract, not construction. Status follows the lifecycle rules; the award goes in Status Detail with the list as its link. Capacity is the gross figure.

## Guardrails

1. Country coverage gate: `scopes/germany/coverage.json`, 15 entries with access proof (`batches/germany-redo/access_proof.json`, 15 of 15 on 2026-11-04), including the permit record system (`uvp-verbund`, role `permit_record`) and the local planning records (role `local_records`).
2. Harvest before the sweep: `scopes/germany/harvest_permits.py --scope germany-redo --all-plants`.
3. Existing-link check before the sweep (716 distinct links); saved copies staged first.
4. Retry the 42 pages the October batches gave up on; `access_audit.py batches/germany-redo --retry`.
5. Thermal MW from the EEA table and capacity tender MW are never staged as nameplate electrical capacity.

## The run

A. Refresh (done 2026-11-04). Pull chain, `export_to_dump.py`, `validation_report.py`, `assigned_comments.py`, `no_tracker.py`, `worklist.py`, `captive_lng.py`, `location_candidates.py`, `match_registers.py`, all `--country Germany`; `access_check.py`; `batches/germany-redo/extra_tasks.json` (award units, open comments, October baseline, four country-wide tasks).

B. Harvest. `harvest_permits.py --scope germany-redo --all-plants --attempts 40`, `check_existing_links.py --country Germany --batch batches/germany-redo`, then `data_center_fleets.py --country Germany --out-dir scopes/germany/work/germany-redo/permits` again.

C. Briefs and sweep. `build_state_brief.py --country Germany --mode update --scope all --batch batches/germany-redo --extra-tasks batches/germany-redo/extra_tasks.json --validation work/validation_germany.json --ids work/ids_germany.json --captive work/captive_germany.json --location work/location_germany.json --existing-links batches/germany-redo/existing_links.json --data-centers scopes/germany/work/germany-redo/permits/_data_centers.json --all-csv scripts/gem_export_gogpt.csv` (no `--irp`), `build_sweep_args.py --batch batches/germany-redo --model sonnet --group-max 5`, then the Workflow `.claude/workflows/state-sweep.js`.

D. Location pass. `build_sweep_args.py --batch batches/germany-redo --location-review --model opus`.

E. Assemble and gate. `assemble_state.py`, `dedup_check.py`, `access_audit.py --retry`, `state_gate.py --batch batches/germany-redo --validation work/validation_germany.json --entity-check --strict-questions` to GATE CLEAN, `qc_checks.py --staged` zero errors, `validation_report.py --country Germany --closeout` and `assigned_comments.py --country Germany --closeout` clean.

F. Deliverables. `build_review_package.py --staging-dir batches/germany-redo/staging --scope germany-redo --mode update`, `recalc.py`, `batches/germany-redo/INDEX.md`, the roster row, `batches/germany-redo/staging` added to the `germany` page's `dirs`, rebuilt with `review_app/build_all.py` and republished.

## What done looks like

- Every award unit is a staged record or a four-part question; Boxberg's two units are adds.
- `batches/germany-redo/coverage.json` answers all 15 source entries and every data center site.
- GATE CLEAN, zero QC errors, CLOSE-OUT CLEAN, COMMENTS CLEAN, no unretried give-up.
- The redo shows on Dan's review page beside the October records, with no record repeated.

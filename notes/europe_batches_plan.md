# Europe batches for Dan O'Beirne's Q4 2026 countries

First drafted 2026-10-03 (Germany then Ireland). Rewritten 2026-10-29 after Baird's ruling: Dan's remaining countries are run one at a time on the North Dakota blueprint (`scopes/us-nd/plan.md`), each with its own harvesters, coverage list and gates. Germany's first packet (2026-10-05, `batches/germany/INDEX.md`) is the model for the review page; its redo comes after the tender awards.

## Order and dates (Baird 2026-10-29)

Dan's weekly schedule (Update V2 sheet, "Weekly schedule" tab, read 2026-10-29): Ireland to 11-02, Italy 11-02 to 11-09, Poland 11-09 to 11-13, Romania 11-13 to 11-19, United Kingdom 11-19 to 12-04.

| order | country | packet ready by | plan |
|---|---|---|---|
| 1 | Poland | about 11-06 | `scopes/poland/plan.md` |
| 2 | Romania | about 11-12 | to write |
| 3 | United Kingdom | about 11-18 | to write |
| 4 | Germany redo | after the StromVKG awards (due by 11-03) | `scopes/germany/` |

Ireland and Italy are Dan's before a packet could land, so they run only as follow-up passes after he finishes them.

## How the review works (Baird 2026-10-29)

- Dan makes the calls. Every country's staging goes onto his existing review page, the `germany` entry in `review_app/artifacts.json` (https://claude.ai/artifact/3YnJ2C36PwrTJ8qYgUxbuW): add `batches/<country>/staging` to its `dirs`, rebuild with `review_app/build_all.py`, republish.
- Baird messages Dan about each batch himself.

## What carries over from North Dakota unchanged

`validation_report.py`, `assigned_comments.py`, `no_tracker.py`, `worklist.py`, `captive_lng.py`, `location_candidates.py`, `check_existing_links.py`, `data_center_fleets.py` (20 MW threshold for the EU and UK), `build_state_brief.py --country`, `build_sweep_args.py`, `.claude/workflows/state-sweep.js`, `assemble_state.py`, `state_gate.py`, `qc_checks.py`, `build_review_package.py` and the review page. Country mode in these scripts was built for Germany on 2026-10-05.

US-only and skipped: `irp_sheet.py` and `match_ids.py` (EIA, EIP and Sierra Club). `state_gate.py`'s ID follow-up gate reads `match_registers.py` output for a country and skips a country without it.

## Shared pieces to build (once, used by every country)

1. Built 2026-10-29: `scripts/match_registers.py --country <name>`, the European counterpart of `match_ids.py`. Joins the export to the European Environment Agency large combustion plant tables and the ENTSO-E per-unit capacity list, plus any national register a country adds. Writes `work/ids_<tag>.json` and `.md` in the `match_ids.py` contract; `build_state_brief.py --ids` and `state_gate.py`'s `ids_followup` gate read it. A national register a country adds goes in as another lead source.
2. A per-country queue or auction reader at `scopes/<tag>/harvest_<source>.py` writing `batches/<tag>/harvest/queues.json` in the existing contract, so `build_state_brief.py --harvest` briefs it with no change. Settings go in `scopes/<tag>/harvest_<source>.json`, never `queues.json` (`pull_queues.py` reads those as US states). Poland's `harvest_pse.py` is the model.
3. An ENTSO-E API token, registered by Baird and kept outside the repo as `ENTSOE_API_TOKEN`.

## Per country

`scopes/<tag>/` with `note.md`, `coverage.json`, `plan.md`, a permit harvester and a grid operator or capacity market harvester, each with tests on saved pages. Then steps A to G of the North Dakota plan: refresh and scripts, harvest, briefs and sweep, location, assemble and gate, deliverables, drafts for Dan. About five working days each.

Country sources to start from:

- **Poland**: probed 2026-10-29, see `scopes/poland/note.md`.
- **Romania**: ANRE license register, Transelectrica connection approvals and adequacy reports, environmental agency (ANPM) decisions, OMV Petrom, Romgaz and Hidroelectrica releases, Modernisation Fund awards.
- **United Kingdom**: the Transmission Entry Capacity register (National Energy System Operator), capacity market register and T-4 results, Planning Inspectorate national infrastructure projects, Environment Agency and SEPA permits, Department for Energy Security and Net Zero section 36 consents, data center backup fleets in the London area.
- **Germany redo**: Bundesnetzagentur Kraftwerksliste and the national unit register (Marktstammdatenregister), the StromVKG tender awards, the existing country note.

## Open questions

- Beyond Fossil Fuels is the GEM team's main partner dataset for European gas plants. Ask Dan whether the repo may read the dashboard and the GEM to Beyond Fossil Fuels ID sheet; if yes it becomes a register in `match_registers.py`.
- Poland's grid connection list names about ten large gas projects GEM lacks. Settle with Dan whether a connection request alone is enough to add a European project before any is staged.

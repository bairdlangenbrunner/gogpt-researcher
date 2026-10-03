---
name: gogpt
description: Operating scaffolding for the GEM Global Oil and Gas Plant Tracker (GOGPT) research project — five workflows; the doers produce a two-file actions/evidence deliverable per batch that the user applies to the live GEM database manually. The workflows are (1) update existing plants/units in a country scope, (2) discover new plants/units (including the captive-power backlog inherited from the LNG repo), (3) triage (worklist + inferred-status sweep — memo only), (4) QC (audit data health and applied edits — memo only), and (5) campaign roster refresh (the quarterly country-assignment cycle). Use this skill whenever the user asks for a GOGPT batch, a country update, a discovery run, a triage pass, a qc pass, a quarterly roster refresh, the captive-power backlog, or any work that produces or modifies the staged deliverables (gogpt_batch_<stamp>_ET_<scope>_<mode>_actions.xlsx). Also use it when the user mentions "the oil and gas plant tracker", "GOGPT", "the Editing Manual", a country-level plant sweep, inferred shelved/cancelled statuses, or gas plant statuses/capacities/ownership. The skill is the executable scaffolding — the research rules live in GEM's GOGPT Editing Manual (Google Doc, authoritative); the SOPs here are operational, citing the manual rather than restating it.
---

# GOGPT — Backend Scaffolding

## What this is

Scaffolding for an agentic research workflow that helps a GEM researcher update the Global Oil and Gas Plant Tracker. The user has direct edit access to the live GEM database (gem-project-db.herokuapp.com web UI) but does NOT delegate writes to the agent — every batch produces an actions/evidence deliverable pair that the user reviews and applies by hand. Agent write footprint on the live DB: zero.

Where things live — **read on demand as the workflow dictates, not at session start**:

- **The GOGPT Editing Manual** (Google Doc) — the authoritative methodology. Not in the repo; `docs/reference/sop_pointers.md` is the **editable link hub** for it, the current cycle's Update sheet + kickoff doc, and every other GEM doc (referenced, not copied — the live doc wins on conflict).
- **SOPs** — `docs/sops/`: `update.md` (bread-and-butter country batch), `discovery.md`, `triage.md`, `qc.md` (memo only; includes the country close-out checklist).
- **Workflow recipes** — `docs/workflows.md`: step-by-step command sequences for every workflow below.
- **Reference docs** — `docs/reference/` (`lifecycle_rules.md`, `unit_conventions.md`, `controlled_vocab.md`, `gem_db_schema.md`, `source_roster.md`, `datasource_conventions.md`, `wiki_pages.md`, `staged_json_schema.md`, `workbook_conventions.md`, `confidence_tiers.md`, `sop_pointers.md`) and `docs/country_notes/` (US states under `docs/country_notes/united_states/`; US scopes are per state — see Update SOP §3.1).
- **Scripts** — `scripts/` (each script's docstring is its manual).
- **Upstream pipeline** — `upstream/gogpt-tracker/`: verbatim import of the GOGPT leads' own tooling (see "Upstream" section below).
- **Backlog** — `notes/backlog_captive_power_candidates.md`: the seeded first discovery input, pointing at candidate JSONs in the sibling LNG repo.
- **NOT a GOGPT workflow** — `emissions/`: CREA scoping of NOx/SOx/PM emissions evidence (EIAs, air permits) for proposed gas plants. Self-contained: its own README, methods and plan; none of the SOPs, lanes, deliverable contract or hard requirements below govern it, and none of its rules belong in `docs/`. Trigger phrases: "CREA", "emissions scoping", "find the EIA / air permit".

## The batch input (and THE scope gotcha)

Fresh GEM export, pulled at the start of every batch (from `scripts/`):

```
python ../../gem-db-ops/gogpt/pull.py --output gem_export_gogpt.csv
python pull_gem_db.py --map-only          # derive the 91-column index map (.colmap.json)
python scope_filter.py                    # derive gem_export_gogpt_scoped.csv
```

The pull engine lives ONLY in the sibling `../gem-db-ops` repo (no engine copies here); auth via `GEM_READONLY_DB_URL`. `pull_gem_db.py` only derives the column map — the canonical 91-column expected-header map is `GOGPT_EXPECTED_COLUMNS` in `../gem-db-ops/gem_colmap.py`, so **new GEM columns get added there**, with `schema_constants.py`'s `COMPUTED_COLUMNS`/`OUT_OF_SCOPE_COLUMNS` updated in the same pass.

**Scope gotcha — the export is NOT GOGPT-only.** It contains ALL combustion units: oil + gas, but also coal (GCPT) and bioenergy (GBPT) units, ~34.5k rows. `scope_filter.py` derives the GOGPT-scoped view (authoritative `trackerSearch='GOGPT'` query when the DB is reachable; fuel heuristic with `--offline`). Research and worklists run on the SCOPED csv; **keep the unfiltered csv** — coal-to-gas conversions, replacements, and shared plants need the GCPT/GBPT side visible.

## Upstream: the GOGPT leads' own pipeline (`upstream/gogpt-tracker/`)

`upstream/gogpt-tracker/` is a verbatim import (2026-08) of the pipeline the GOGPT team leads built and run: session-based country research recorded in per-country context cards, cross-cutting scans, and the compile step that builds GEM's published spreadsheet. Treat it as vendored upstream code:

- **Never edit files under `upstream/` as part of this repo's workflows.** Refinements intended for the leads are deliberate, discussed-first changes made there so they stay clean diffs to hand back.
- **This repo's output contract is unchanged** — batches produce the actions/evidence deliverable pair. The upstream context-card/QC-report flow is their deliverable, not this repo's.
- **What the research process adopts from upstream** (wired into the Update SOP §3 and `docs/workflows.md` §2): the cross-cutting scans (`--ownership-scan`, `--in-progress-scan`, `--duplicate-scan`, `--possible-updates`), the unit-counts baseline check against the assignments tab, and full-country coverage by status group (their session order). Scans surface candidates only — they never auto-stage anything (upstream invariant, kept).
- **The bridge**: `scripts/export_to_dump.py` converts the fresh scoped pull into a `GOGPTall*.xlsx` dump in `upstream/gogpt-tracker/data/`; the upstream scripts auto-detect the newest dump, so after bridging they run on batch-fresh data instead of the bundled cycle dump. Run it right after the §1 pull chain whenever a workflow calls the scans.
- `upstream/gogpt-tracker/docs/METHODOLOGY.md` is the leads' distilled methodology; the Editing Manual remains authoritative and conflicts escalate per the rule below. Upstream has its own `requirements.txt` (pandas/xlsxwriter — not merged into this repo's).
- The upstream data files stay untracked — multi-MB regenerable dumps and a Drive export that is refreshed each run (`.gitignore`). Personal names in committed content are allowed (user ruling 2026-09-15); credentials and third-party confidential material still never are.

## Read the manual + relevant SOPs first

Before any batch: (1) confirm the Editing Manual's rules are available — the distilled versions in `docs/reference/` carry the working rules, `sop_pointers.md` has the links if the source is needed; (2) read the SOP for the workflow being run; (3) if an SOP contradicts the manual, flag to the user before proceeding — the manual is what GEM staff review edits against.

## Workflow router

Full recipes in `docs/workflows.md` — **read the relevant section before starting a batch.** Subagent model choice follows the global dispatch-time rule (user-level CLAUDE.md); the Model selection block at the top of `docs/workflows.md` maps it onto this repo.

| Workflow | Trigger phrases | Recipe + rules |
|---|---|---|
| **Update existing plants** (most common) | "update [country]", "refresh the [country] gas plants", "work the [country] assignment", "fill blank data sources in [country]" | `docs/workflows.md` §2 + Update SOP |
| **Discovery** (new plants/units; incl. captive backlog) | "find new plants in [region]", "discovery run", "work the captive-power backlog", "what's missing in [country]" | `docs/workflows.md` §3 + Discovery SOP |
| **Triage** (plan the batch) | "what should we work on", "run the worklist for [country]", "what's stale", "inferred-status sweep" | `docs/workflows.md` §4 + Triage SOP; output is a markdown memo, not a deliverable |
| **QC** (backward-looking checker) | "qc pass", "validation report", "country close-out", "did my edits land", "link-rot sweep" | `docs/workflows.md` §5 + QC SOP; memo only; fixes route to a follow-on Update batch |
| **Campaign roster** (quarterly cycle bookkeeping) | "refresh the roster", "start the [quarter] campaign", "campaign status" | `docs/workflows.md` §6 + `campaigns/<quarter>/README.md` |
| **Review** (decide on a batch's staged edits) | "review the [state] batch", "open the review app", "build from the decisions" | `docs/workflows.md` §8 + `review_app/README.md`; decisions land in `review_log.jsonl` in the staging dir; build with `--decisions` |

Routing notes that prevent the most common mistakes:

- **Triage is script-first**: `worklist.py` orders each country by the manual's priority ladder (in-development → shelved review → planned-retirement-this-year → mothballed → operating) and flags shelved-inferred (≥2y no evidence) / cancelled-inferred (≥4y) candidates. Work the worklist top-down; don't invent a different ordering.
- **An inferred status is a date-arithmetic conclusion, not a research finding** — it carries no new source URL by design (`docs/reference/lifecycle_rules.md`). Everything else staged needs refs.
- Work the **possible-updates backlog rows for a country DURING that country's Update batch**, not as a separate pass (Update SOP).
- Discovery candidates that fail the capacity threshold or evidence bar go to the `monitor` lane with a `recheck_by` date — not to the trash.
- **No wiki lane.** GOGPT wiki pages are auto-generated; only the "Background" section is hand-editable and it is out of the staging contract (`docs/reference/wiki_pages.md`). There are exactly six lanes: `updates|qa|entity|monitor|newplants|newunits`.
- QC never edits: it audits, emits a memo + the close-out validation report, and routes fixes to an Update batch.
- **The review app never edits either**: it records accept / hold / reject / suggest per staged record in `batches/<scope>/staging/review_log.jsonl` (append-only, committed with the batch). `build_review_package.py --decisions` then builds the workbook from accepted edits only and lists the rest in the evidence file. Keys are the stable `record_id` every staged record carries, so a rebuild keeps the calls.
- `qc_checks.py --staged` must pass with **zero errors** before any deliverable is built.

## Output deliverable

Two files per batch in `batches/<scope>/deliverables/`: `gogpt_batch_<YYYYMMDD>_<HHMM>_ET_<scope>_<mode>_actions.xlsx` (per-plant/per-unit web-UI edit checklist: current → proposed → evidence, colored by confidence) + `..._evidence.md` (the reasoning). Stamp via `TZ=America/New_York date "+%Y%m%d_%H%M_ET"`; `<mode>` ∈ `update`/`discovery`; triage and QC produce memos, not deliverables. **Never overwrite an existing deliverable** — every rebuild gets a fresh stamp. Cell colors = per-cell source confidence (green = one fully validated ref, or 2+ independent for a status change; yellow = single validated ref on a status change, or a ref that validates only partially; red = single weak/unvalidated — prefer blank + qa; blue re-verified unchanged; green+empty = staged deletion): `docs/reference/workbook_conventions.md` + `confidence_tiers.md`.

## Hard requirements (these override anything below)

- **Never modify the live GEM database.** Deliverables are applied manually by the user.
- **Every URL passes `url_verifier.py` before staging** — verification means the specific claimed value appears on the page/PDF, not just HTTP 200. A bare domain/homepage is never a citation.
- **NEVER cite gem.wiki or globalenergymonitor.org — anywhere, in any lane.** GEM-derived republishers (Wikipedia/IEEFA/news footnoting GEM) are likewise not independent evidence — chase and cite the primary source. gem.wiki may be used to *detect* gaps, never as the citation.
- **Banned source: abarrelfull** (`abarrelfull.wikidot.com`, `abarrelfull.co.uk`) — never, even alongside corroboration (user directive 2026-07-17, all GEM researcher projects).
- **One fully validated ref is sufficient; a second independent source is preferred, never required** (Baird 2026-10-02, adopting the pipelines-researcher ruling of 2026-09-30). A ref is fully validated when it clears `url_verifier.py`, names this plant/unit, and states the value (within rounding; status-by-inference counts) — that closes the data point at green. Take a second source when cheap and record it via `independent`, but never hold a unit open for one. **Exception: a STATUS CHANGE is green only on 2+ independent publishers; a single-source status change is yellow.** Mirrors/copies of one document = ONE source; GEM-derived republishers never count. A single ref that does not fully validate → red, prefer blank + qa lane.
- **Fresh pull + `scope_filter.py` at the start of every batch; re-derive the colmap from the header every run** — never hard-code offsets, never research against a stale CSV.
- **Data Source cells MERGE, never replace** — carry forward every still-valid existing URL; datasources are never deleted (manual rule). No orphan refs (a Data Source edit needs its paired value) and no orphan values (a staged value needs its Data Source, inferred statuses excepted).
- **A URL belongs ONLY in a Data Source column**; Status/Capacity/Fuel/Owner columns hold values, never links. The build script enforces this.
- **Project-level field changes apply to ALL unit rows of the plant** — the export duplicates plant-level fields across unit rows; updates must too.
- **Capacity is GENERATING MW only (MWe, nameplate)** — never shaft/mechanical-drive MW, never MWt. Captive plants are in scope, but only their electric generating capacity is recorded. Ranges record the high end.
- **Start year is NEVER filled for shelved or cancelled units; mothballed units never get a retired year.** Mothballed/retired/cancelled statuses are tracked from 2020 forward only.
- **Hydrogen columns are do-not-research** (the 10 columns in `schema_constants.OUT_OF_SCOPE_COLUMNS`) — read-only, never staged.
- **Don't create duplicate entities** — `entity_lookup.py` before staging any new owner/operator/parent; entities are shared across all GEM trackers and countries. Ownership: ≥5% shares only, top-4 + "other", never national governments directly.
- **CC block = one unit** — never split a combined-cycle block into its component turbines (`docs/reference/unit_conventions.md` for all naming rules).
- **Every note a person will read is written in plain language** (Baird 2026-10-02): `researcher_notes`, `action`, evidence markdown, calibration memos, country notes, QC memos, subagent shard text. Short sentences, sources named by what they are, no repo jargon (lane, shard, tier, ref, staged), no unexplained abbreviations, no em-dashes or arrows. Rules and a before/after example in `docs/reference/notes_style.md`; `state_gate.py` flags offenders.

## When to escalate to the user

- A whole class of GEM values looks systematically wrong (schema misunderstanding, not a research finding).
- A manual rule and an SOP/reference doc conflict.
- A discovery batch surfaces more than ~5 candidate plants in one country (systematic gap — talk before staging).
- The capacity threshold call is genuinely ambiguous on a candidate (units straddling 50 MW, EU/UK 20 MW edge cases, generating-vs-shaft ambiguity).
- An entity that should exist in the GEM entity system isn't found.
- A QC pass finds >10% of sampled cells unsupported, or an apply-check shows multiple diverged edits.
- The export's column set drifts (`pull_gem_db.py --map-only` reports missing/unknown columns).

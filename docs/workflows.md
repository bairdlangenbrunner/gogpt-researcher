# Workflow recipes

Step-by-step command sequences for the workflows routed from `CLAUDE.md`. The GOGPT Editing Manual is authoritative for research rules; the SOPs (`docs/sops/`) are the operational rules; this file is the glue — which commands, in which order. Read the section for the workflow you're running, plus the relevant SOP(s).

**Fresh-pull shorthand used throughout** (from `scripts/`):

```
python ../../gem-db-ops/gogpt/pull.py --output gem_export_gogpt.csv
python pull_gem_db.py --map-only
python scope_filter.py
```

→ fresh all-combustion CSV (~35k rows, 91 cols) + column-index map (`gem_export_gogpt.csv.colmap.json`) + GOGPT-scoped CSV (`gem_export_gogpt_scoped.csv`). The pull engine lives ONLY in the sibling `../gem-db-ops` repo; auth via `GEM_READONLY_DB_URL`. **Re-derive the colmap every run** — the schema can drift; `--map-only` errors loudly on missing/unknown columns (escalate drift to the user). `scope_filter.py` uses the authoritative `trackerSearch='GOGPT'` DB query when `GEM_READONLY_DB_URL` is set, else pass `--offline` for the fuel heuristic (weaker — note it in the batch record). **Keep the unfiltered CSV**: conversion/replacement checks need the coal/bioenergy side (shared plants, R-suffix replacement units, timepoint links).

**How the workflows fit together.** Triage is the forward-looking chooser — `worklist.py` + the inferred-status sweep produce a *memo* recommending what to work. The doers turn a chosen scope into the actions/evidence *deliverable pair*: Update (§2) and Discovery (§3). QC (§5) is the backward-looking checker — memo + validation report, fixes route back into Update ("QC detects, Update fixes"). The campaign roster (§6) is the quarterly bookkeeping wrapper around all of it. So: **Triage (memo) → Update / Discovery (deliverables) → QC (memo → back to Update)**, inside a `campaigns/<quarter>/` cycle.

**Model selection (who runs on what).** Subagent model choice follows the global dispatch-time rule (user-level CLAUDE.md — cheapest model genuinely good enough, chosen per dispatch, never pinned). In this repo the judgment-heavy work that stays in the top-tier main loop: scope calls, threshold/scope-gate judgments on discovery candidates, escalations, and the pre-build QC gate on any subagent output. Mechanical fan-out (per-plant source sweeps from a clear brief, URL verification passes, per-country worklist summarization) can go down-tier. Subagent output is never pre-trusted regardless of model — `qc_checks.py --staged`, the gem.wiki/banned-domain scan, and a URL spot-check run the same either way.

**Batch artifact conventions.** Per-batch staging JSON lives in `batches/<scope>/staging/` (`staged_<lane>.json`, lanes and record shapes in `docs/reference/staged_json_schema.md`) — committed as the audit trail. When a scope runs a second mode in the same cycle (e.g. a discovery pass after an update batch), stage it in a separate per-mode dir — `batches/<scope>/staging-discovery/` — so the build doesn't re-include the other mode's lanes; point `--staging-dir` and `URL_VERIFIER_LOG` there. Deliverables land in `batches/<scope>/deliverables/` named `gogpt_batch_<YYYYMMDD>_<HHMM>_ET_<scope>_<mode>_{actions.xlsx,evidence.md}` (stamp via `TZ=America/New_York date "+%Y%m%d_%H%M_ET"`; naming rules in `docs/reference/workbook_conventions.md`; xlsx gitignored, evidence md committed; never overwrite). When running `url_verifier.py`, export `URL_VERIFIER_LOG=<path into the batch's staging dir>` so every verification attempt lands in an append-only JSONL next to the staged JSON. Each batch gets one line in `batches/<scope>/INDEX.md` and (for cross-scope runs) a small md in `batches/run_records/`.

## §1 Fresh pull + scope filter (start of every batch)

1. Fresh-pull shorthand above. Confirm: CSV mtime changed, `--map-only` reports 86/86 known columns, scope filter prints kept/dropped counts (scoped view ≈ oil+gas only).
2. If the pull fails on auth, ask the user to check `GEM_READONLY_DB_URL` (see `env.example`); never fall back to a stale CSV silently.
3. For triage-only sessions this section plus §4 is the whole recipe.

## §2 Update existing plants (most common)

1. Fresh pull (§1).
2. Confirm scope per Update SOP §2 — which country/countries (usually the quarter's assignment from `campaigns/<quarter>/roster.csv`), whether Data-Source backfill is in scope. Create `batches/<scope>/staging/` if new.
3. `python worklist.py --country "<Country>"` → the priority-ordered worklist (`work/worklist_<tag>.csv`): in-development first, then shelved review, planned-retirement-this-year, mothballed, operating; 2y/4y inferred-status candidates flagged. Work it top-down. For a full-country assignment, the ladder sets priority but not coverage — after it's exhausted, sweep the remaining status groups in the upstream session order (new proposals → in-development → shelved/cancelled → operating → retired/mothballed) per Update SOP §3.
4. **Cross-cutting scans** (adopted from the upstream pipeline — CLAUDE.md "Upstream"): `python export_to_dump.py` bridges the fresh scoped CSV into `upstream/gogpt-tracker/data/`, then from `upstream/gogpt-tracker/scripts/`:
   - `python3 gogpt_csv_query.py --country "<Country>" --counts-only` — unit-counts baseline; reconcile a mismatch vs the roster/assignments tab before researching.
   - `... --status operating --ownership-scan`, `... --in-progress-scan`, `... --duplicate-scan` — candidates fold into the worklist as extra rows/notes. Scans surface candidates only; nothing is staged from a scan without the normal research + verification path.
   - `... --possible-updates [--pu-file <file>]` — the country's backlog rows (input to step 5c; takes the local CSV or a flattened Drive read of the live sheet).
5. Per plant/unit on the worklist:
   a. Source-search per Update SOP §4, using `docs/reference/source_roster.md` (tiering) and `docs/country_notes/<country>.md`. Harvest the record's EXISTING Data Source cells first — re-verifying a known-good source beats finding a new one (`confidence_tiers.md`).
   b. Apply lifecycle rules per `docs/reference/lifecycle_rules.md` — status vocab, start-year/retired-year logic, the 2020-forward rule, inferred 2y/4y arithmetic.
   c. Check the possible-updates backlog rows for this country (sheet ID in `sop_pointers.md`) and fold them into the same batch.
   d. Conversion/replacement checks against the UNFILTERED export — a gas unit replacing a coal unit at a shared plant needs the GCPT side read (unit_conventions.md, R-suffix + timepoint rules).
   e. Stage findings as `staged_updates.json` (+ `staged_qa.json` / `staged_entity.json` / `staged_monitor.json` as needed) per `staged_json_schema.md`. Project-level fields: set `applies_to_all_units` + `sibling_unit_ids`.
6. `python url_verifier.py "<url>" "<claimed value>" ...` on every URL before it enters a staged record; record the verification result in the record's `verifications`.
7. `python entity_lookup.py "<owner name>"` before staging any new owner/operator/parent (entities are shared across trackers and countries; a match anywhere = reuse the existing entity ID).
8. `python qc_checks.py --staged batches/<scope>/staging/staged_updates.json` (and each other lane file) → must exit 0. Fix errors in the staging JSON, not by relaxing the checker.
9. From `scripts/`: `python build_review_package.py --staging-dir ../batches/<scope>/staging --scope <scope> --mode update --output-dir ../batches/<scope>/deliverables` (use `--dry-run` first) → actions xlsx + evidence md.
10. `python recalc.py ../batches/<scope>/deliverables/<actions.xlsx>` → zero formula errors.
11. Add the INDEX.md line, update the campaign roster's `packet_file`, `present_files`.

## §3 Discover new plants/units

1. Fresh pull (§1). Confirm parameters per Discovery SOP §2 (region/country; threshold reminders: ≥50 MW generating, EU+UK ≥20 MW).
2. **First standing input: the captive-power backlog** — `notes/backlog_captive_power_candidates.md` points at candidate JSONs in the sibling LNG repo. Dedup the lists against each other and against the scoped export before any web research (steps in that file).
3. Sweeps per Discovery SOP: country regulator (country_notes + source_roster), trade press, sponsor IR. Candidates need named operator + specific site + concrete evidence.
4. Dedup every candidate against the scoped export (GEM unit ID, name+coords) AND the unfiltered export (the plant may already exist with only coal units — then it's `newunits` on the existing plant, not `newplants`).
5. Screen: capacity threshold on GENERATING MW only (never shaft/mechanical-drive); scope fuels per `controlled_vocab.md`. Passing candidates → `staged_newplants.json` (nested units) / `staged_newunits.json`; near-misses and thin-evidence candidates → `staged_monitor.json` with `recheck_by`, never discarded.
6. `url_verifier.py` on all URLs; `entity_lookup.py` on every new entity name.
7. `qc_checks.py --staged` on every lane file → exit 0; then build + recalc + INDEX.md as §2 steps 8–10 with `--mode discovery`.

## §4 Triage (decide what to work on)

1. Fresh pull (§1).
2. `python worklist.py --all` (or per candidate country) → per-country priority counts + the inferred-status sweep (shelved-inferred ≥2y, cancelled-inferred ≥4y candidates with their evidence ages).
3. Pull triage inputs per Triage SOP §3: the worklist, the quarter's roster state (`campaigns/<quarter>/roster.csv` — what's assigned/unworked), the possible-updates backlog volume per country, the captive-power backlog status, recent-quarter news signal.
4. Produce a triage memo (markdown, not a deliverable): `batches/triage_<stamp>_ET.md` — recommended batch composition, each option naming the workflow and scope. The user decides before any batch starts.

## §5 Quality control (QC pass / country close-out)

Memo only; stages no edits. Full rules in the QC SOP — including the GC/Country checklist + validation report required before a roster row moves to `done`.

1. Fresh pull (§1) — for a post-apply check the pull must postdate the user's apply.
2. **Mechanical integrity**: `python qc_checks.py --csv gem_export_gogpt_scoped.csv --country "<Country>"` → vocab/threshold/year-logic/ownership violations in the live data.
3. **Citation spot-check**: re-verify a stratified sample of existing Data Source URLs via `url_verifier.py` (dead / bot-blocked / value-missing verdicts). >25% dead in a country → recommend a Data-Source backfill Update there.
4. **Accuracy spot-check** (agent-driven): ~20 unit sample (recently-edited, high-capacity operating, in-development); re-verify Status/Capacity/Fuel/Owner against cited refs + one fresh corroboration each. >10% unsupported → systemic flag, stop and discuss.
5. **Post-apply check**: diff the batch's staged values against the fresh export — applied / not-applied / diverged per edit.
6. Memo to `batches/qc_<stamp>_ET.md`; for a close-out, attach the validation report per QC SOP and update the roster row. Stop and ask before spinning up recommended follow-ups.

## §6 Campaign roster refresh (quarterly cycle)

1. New quarter: create `campaigns/<quarter>/` (copy the README from the prior quarter, update the slug).
2. Fresh pull (§1), then `python build_campaign_roster.py --campaign <quarter>` → `campaigns/<quarter>/roster.csv` (per-scope in-development/status counts, US split per state, sorted by in-dev volume; the manual columns `assignee_role`/`assignment_status`/`packet_file`/`applied`/`notes` survive refreshes).
3. Mirror the quarter's "Researcher Country Assignments" tab (link in `sop_pointers.md`) into `assignee_role` — names are fine (ruling 2026-09-15). For US rows the tab is per state (`United States - <State>`); the roster has one row per state under its `scope` key, so match on that (`campaigns/q4-2026/README.md`).
4. Re-run step 2 anytime mid-quarter to refresh counts; roster edits beyond the manual columns belong in the generator, not the CSV.

## §7 State sweep (US)

Per-plant agent research for one US state; contract, shard shape and gate in `notes/us_state_agent_plan.md`. Modes: `blind` (calibration, GEM values withheld) or `update` (normal batch).

1. Fresh pull (§1), then from `scripts/`: `python worklist.py --state <State> --all`. Write or refresh `docs/country_notes/united_states/<state>.md` first; it is inlined into every brief. Read the possible-updates sheet rows for the state and the upstream scans (§2) and put the ones worth a task into `batches/us-<st>/extra_tasks.json` (`{"<L...>": [{"text": ..., "fields": [exact headers]}], "*": [...]}`).
2. `python build_state_brief.py --state <State> --mode update --extra-tasks ../batches/us-<st>/extra_tasks.json` → `batches/us-<st>/briefs/`. Update mode is the manual's ladder plus the gap list, not a deep sweep: each unit gets a "What to check" block, the field list shrinks to what the tasks touch, and with the default `--scope ladder` plants with no task are left out (listed under `not_tasked` in `_index.json`; `--scope all` briefs every plant). `--mode blind` is calibration only.
3. `python build_sweep_args.py --batch ../batches/us-<st> --model sonnet --group-max 5` → `staging/sweep_args.json`. Pick the model at dispatch time (cheapest genuinely good enough); `--group-max N` packs small plants into one agent.
4. Workflow tool: `scriptPath: .claude/workflows/state-sweep.js`, `args` = that JSON as an object. One subagent per group writes `shards/<plant_id>.json` plus a verifier log `shards/<plant_id>.urls.jsonl`; downloads go to `work/sweep_<st>/`. In parallel, one Sonnet Agent does the statewide search (newly announced gas plants, gas-fired data centers, NYISO-style queue and EIA-860M planned sheet) and writes `shards/_state.json` with qa and monitor items only.
5. Check the returned summaries for `shard_written: false` and re-run only those plants (`build_sweep_args.py --plants L...`).
6. `python assemble_state.py --batch ../batches/us-<st>`, then `python state_gate.py --batch ../batches/us-<st>` (must print GATE CLEAN), then `qc_checks.py --staged` on every lane file and the normal build (§2 steps 8 to 11). Blind runs also get the calibration memo. Close out with the state note's open questions, the roster row and the batch INDEX.md.

## §8 Review a batch (the review app)

Decide on a batch's staged edits one by one before the deliverable is built. Plain-language
guide in `review_app/README.md`. The app never touches the GEM database; its only output is
the decision log in the staging dir.

1. From the repo root: `python review_app/server.py --scope us-md --scope us-ny` (any number of batches; `--dirs` for explicit staging folders, `--reviewer "Name"` to override the git user). The page opens on 127.0.0.1:8767.
2. Work the queue: accept / hold / reject / suggest each change (`a` `h` `r` `s`), calls and notes on the concerns, watch-list entries and entity checks. The minor tab (value checked and stands, only a link added) has an accept-all button. Every call is appended to `batches/<scope>/staging/review_log.jsonl` at once; `review_decisions.json` is the derived latest-per-record copy. Both are tracked and committed with the batch.
3. Build from the calls, from `scripts/`: `python build_review_package.py --staging-dir ../batches/us-<st>/staging --scope us-<st> --mode update --decisions`. Only accepted edits reach the actions workbook; held, rejected, suggested and undecided edits are listed at the top of the evidence file with the reviewer's note, and items carry their call. A build without `--decisions` ignores the log and says so.
4. Suggestions go back to the researcher (a follow-on sweep or a hand edit of the shard, then `assemble_state.py` again). The `record_id` is stable across rebuilds, so the log still applies.
5. Colleague without the repo: `python review_app/build_static.py --scope us-md --scope us-ny --reviewer "Name" --export-csv scripts/gem_export_gogpt_scoped.csv` writes one html file under `work/`; send it, they review in a browser and press "download decisions", then `python review_app/import_log.py <their file>` appends the calls to the staging logs (safe to re-run) and step 3 builds as usual. Published as a claude.ai artifact instead (capabilities `db`, `downloads`, `user`; reviewer invited by email as editor, no link sharing), the page saves the calls to the artifact's database and `import_log.py` takes the `logs/<initials>` document read with ArtifactData. Details in `review_app/README.md`.

# Repo layout audit (2026-10-29)

Written before planning North Dakota, at Baird's request: should states and countries get their own folders for harvesting, analysis, references and source building? Assessment only; nothing was moved. The second half is a critical read of the Iowa batch, which Baird asked not to treat as the template.

## What the repo looks like today

Scope-specific material sits in six places, keyed by five different name forms:

- `scripts/` holds the per-scope harvesters next to the generic engines: `harvest_permits_iowa.py`, `harvest_permits_kansas.py`, `harvest_permits_michigan.py`, `harvest_permits_mississippi.py`, `harvest_permits.py` (Germany), `harvest_psc_michigan.py`, `harvest_psc_mississippi.py`, `pull_queues_mississippi.py`, `ms_match.py`. `pull_queues.py` is the generic queue reader but its `STATES` table has only Michigan and Mississippi, and it has no Southwest Power Pool reader.
- `docs/country_notes/united_states/<state>.md` holds the state note (ten states so far). `docs/country_notes/united_states.md` holds the rules true of every state.
- `docs/coverage/<tag>.json` holds the statewide source list the gate enforces, but only for Illinois, Kansas, Michigan and Mississippi. Older states have none.
- `notes/<state>_batch_plan.md` holds the plan (Michigan, Mississippi, Texas pilot), with the Kansas handoff and the data center plan next to repo-wide plans.
- `batches/<tag>/` holds the run outputs: briefs, shards, staging, deliverables, harvest, coverage.json, existing_links, extra_tasks, access_retry.
- `work/` (gitignored, 795 entries) holds the script outputs as flat files keyed by tag (`captive_<tag>`, `ids_<tag>`, `irp_<tag>`, `location_<tag>`, `validation_<tag>`, `worklist_<tag>`), plus `work/permits/<tag>/`, `work/sweep_<tag>/`, `psc_mi/`, `psc_ms/`, `captive/`, `eia/`.

The tags are not consistent. `worklist.py` writes `worklist_us-north-dakota.csv` while every other script writes `us-nd`. `batches/` has both `us-il` and `us-il-dc` and `us-il-val` for one state. `README.md`'s layout section predates most of this.

Code that knows about scope files by path: `build_state_brief.py` (country notes at line 251, the harvest folder contract at 998 to 1007 still names the Mississippi scripts in its error text), `state_gate.py` (`docs/coverage/<scope>.json` at 1193 to 1201), `data_center_fleets.py`, `location_candidates.py` (the permit folder at 291), `.claude/workflows/state-sweep.js` (`work/permits/${SCOPE_TAG}/`). `scripts/paths.py` fixes the layout relative to `scripts/`.

## Verdict: yes, give each scope a home, but keep the engines where they are

The present layout grew one state at a time and it works, because every path is derived from the tag. The costs are real but they are costs of finding things, not of running things:

- A new scope needs files in five directories before the sweep starts, and nothing lists them. The Iowa run skipped two of the five (coverage list and harvester) because they were not yet part of the recipe; a scope folder with a fixed set of expected files makes a gap visible.
- Scope harvesters are one-offs that live forever in `scripts/`, so `scripts/` reads as 63 entries of mixed generic and specific code. A cheaper model running a plan has to tell them apart by name.
- The handoff for a scope (plan, note, coverage, harvester, work files) is a scavenger hunt. The pipelines repo and the LNG repo have the same problem for the same reason.

Recommendation: a `scopes/` tree, one folder per tag, holding the scope-specific files and nothing generic.

```
scopes/us-nd/
  note.md             the state note (moves from docs/country_notes/united_states/north_dakota.md)
  coverage.json       the statewide source list (moves from docs/coverage/us-nd.json)
  plan.md             the batch plan (moves from notes/north_dakota_batch_plan.md)
  harvest_permits.py  the scope's permit harvester (moves from scripts/harvest_permits_<state>.py)
  harvest_psc.py      the scope's docket harvester, when one exists
  queues.json         the queue settings for pull_queues.py (the STATES entry, moved out of the code)
  work/               gitignored: permits, dockets, saved pages, script outputs for this scope
```

Keep `scripts/` for the engines (pull, scope filter, brief builder, sweep, assemble, gate, build, fetch, verifier, generic harvest helpers), `batches/<tag>/` for the committed audit trail of each run, `docs/` for rules that apply to every scope, `notes/` for repo-wide plans. `batches/` and `scopes/` stay separate on purpose: a scope is permanent, a batch is one run.

Cheap alternative if a new top-level tree feels heavy: `docs/country_notes/united_states/north_dakota/` as a folder instead of a file, holding the same set. It keeps the country tree Amalia and Dan already know. The downside is that Python harvesters then live under `docs/`, which is odd and will confuse the next person.

Why not do it inside `batches/<tag>/`: the batch folder is the audit trail of a run and gets archived or duplicated (`us-il`, `us-il-dc`, `us-il-val`). The note, coverage list and harvester outlive runs.

Decision (Baird 2026-10-29): adopt the `scopes/<tag>/` tree, then run North Dakota on it.

## Migration

1. `scripts/paths.py`: add `scope_dir(tag)` and `scope_work(tag)`; `work_dir()` for a scoped script returns `scopes/<tag>/work/`. Add `scope_tag(state_or_country)` so every script derives the same tag (fixes the worklist name).
2. Point the readers at the new locations with the old ones as fallback for one cycle: `build_state_brief.py` (country note, harvest folder), `state_gate.py` (`coverage_list_path`), `data_center_fleets.py`, `location_candidates.py`, `state-sweep.js` (`work/permits`).
3. Move the generic parts of the four permit harvesters (fetch with retries, PDF text, size and maker regexes, matching to GEM plants) into one `scripts/harvest_lib.py`; the per-scope file keeps only the portal logic. Mississippi and Michigan are already close to this.
4. Move `pull_queues.py` `STATES` entries into `scopes/<tag>/queues.json`; add the SPP reader (needed for North Dakota anyway).
5. Move the existing scope files for the ten states and Germany, update `docs/workflows.md` §7 and §2, CLAUDE.md "Where things live", `batches/README.md`, `README.md`, `.gitignore` (`scopes/*/work/`), and the tests that build paths by hand (`tests/test_brief_harvest.py`, `tests/test_access_gate.py`, `tests/test_location_gate.py`, `tests/test_pull_queues.py`).
6. Run North Dakota as the pilot. Its plan below is written for the current layout and names the file that moves at each step, so it runs either way.

Rough size: a day of work including tests. Do it before Michigan and Mississippi run, or after North Dakota as a single move; not during a run.

## The Iowa batch, read critically

Iowa is not the template. What it got right is the state note (`docs/country_notes/united_states/iowa.md`): grid context, regulator and docket forms, the permit portal mapped page by page, recent events with dates, watch items, open items, gotchas. That structure carries over. What went wrong:

- The first run (2026-10-16, Sonnet, every plant) skipped the Iowa Department of Natural Resources permit site as a "search form" and missed the March 2026 Burlington engine permits. Amalia found them by hand. The harvester and the 2026-10-19 follow-on were built after the fact. Rule since 2026-10-19: harvesters run before the sweep, and a search form is never a stop.
- The Iowa Utilities Commission filing system was never reached. For a state whose new plants each need a generating certificate, that is the primary source for status and dates.
- No coverage list, no access audit, no chase gate: the gates did not exist yet. The run cannot show what was and was not searched.
- The watch list held seven MISO queue entries (Killdeer 787 MW, Haskins 525 MW, Emery 98 MW, Hills 350 MW, three 160 MW engine entries) and three threshold plants (Coralville 72 MW, River Hills 128 MW, Roquette 50 MW). Under the rules in force since 2026-10-23 and 2026-10-27, queue entries at or above 50 MW are `newplants` at announced and a plant whose summed units reach 50 MW is an add; the watch list is for seven named cases only.
- Data centers were not searched (Microsoft Ginger East and West, Osmium, QTS); the `us-ia-dc` catch-up ran 2026-10-27.
- The review log shows 39 accepts and 7 rejects, with every sub-50 MW new unit left as "a reviewer call". Those should have been a decision in the record, not a question.
- The qa records were backfilled into the four-part form on 2026-10-27; the sweep did not produce them that way.

What North Dakota does differently, in one list: note, coverage list and harvesters exist before the sweep; the permit portal, the Public Service Commission case search and both queues are scripted and read in full; queue entries, data center fleets and threshold plants are adds, not watch items; every gate runs; qa records are four parts from the start; the run is checked against Amalia's edits of the same week, since she is editing North Dakota now.

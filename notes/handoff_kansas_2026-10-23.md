# Handoff: Kansas rerun under the add rule, 2026-10-23

Written for a fresh chat. Nothing in this list is committed. Run `git status` first; the working tree holds the add-rule implementation, the Kansas rerun and several doc changes from one long session.

## What was decided today (Baird)

- A project GEM lacks is added on one verified source. Queue entries count. Status comes from the manual's ladder (planning document, queue entry or press = announced; permit application, land, financing, prior-approval docket or signed interconnection agreement = pre-construction). The watch list is for the eight `watch_case` values only (`scripts/schema_constants.py` `WATCH_CASES`). Baird approved five cases; `not_committed`, `other_scope` and `unverified` were added as bookkeeping cases and Baird has not yet said yes or no to those three.
- Queue-only entries are adds, and entries filed by a single-purpose company are added at announced with owner blank unless a parent is named. Baird answered both himself; no Slack question to the project manager. Recorded in `docs/sops/discovery.md` §3.1, `docs/country_notes/united_states.md` and the memory file `add-threshold-one-source.md`.
- The manual (September 2026) says nothing about interconnection queues. The live database already holds 18 US units whose only status source is an ERCOT, MISO, SPP or PJM document, so queue-only adds are existing practice.

## Files changed for the rule

`scripts/schema_constants.py`, `scripts/assemble_state.py`, `scripts/state_gate.py` (gate `watch-case`, `scope_threshold_mw`), `scripts/build_state_brief.py` (`ADD_RULE`), `scripts/build_review_package.py` (`ref_col_for` now maps State/Province and Local area to Location Data Source), `scripts/captive_lng.py`, `scripts/irp_sheet.py`, `.claude/workflows/state-sweep.js`, `docs/reference/staged_json_schema.md`, `docs/sops/discovery.md`, `docs/workflows.md`, `CLAUDE.md`, `docs/country_notes/united_states.md`, `docs/coverage/us-ks.json`, `tests/test_watch_case_gate.py` (13 tests). The full suite was 347 passed before the last few edits; rerun `python3 -m pytest tests -q`.

## Kansas batch state (`batches/us-ks`)

- Fresh pull 2026-10-23 10:33. Already in the database since the 10-21 run: Chisholm Trail Energy Center (was Viola), Crooked Creek Energy Center L100001088911, Sherlock Generation Project L100001088900, Clifton unit 2 G100001101129. Placeholder L100001063349 is gone; the assembler skips it with a warning. Crooked Creek and Sherlock are not in the batch's plant index (built 10-21).
- Staged: updates 80, qa 61, monitor 6, newunits 2, newplants 1. New: Labette County power station (announced, 969 MW, SPP GEN-2024-129), Quindaro Diesel 1 (announced, 165.84 MW, ERAS-2025-031), McPherson 3 unit 2 (announced, 123.7 MW, ASGI-2024-020, unit placement is a guess). Watch items: Clifton existing plant, Buchanan Bluffs (other scope, Missouri), Leavenworth GEN-2024-253 (drive or storage), BPU 237 MW turbine for 2039 (not committed), Riverton (under threshold), Flint Hills Digital Campus (data center hold). New questions: Crooked Creek location and start year, Clifton capacity threshold (three 33 MW turbines on one 98 MW interconnection, escalate to Baird), Jeffrey GEN-2024-249 duplicate, Sherlock duplicate.
- `qc_checks.py --staged`: zero errors, zero warnings.
- Gate (`python3 scripts/state_gate.py --batch batches/us-ks`): everything passes except two hard gates and one advisory.
  - `access` fixed later the same day: `access_audit.py --host` never wrote `access_retry.json`; it now does. The old Kansas Power Pool address is logged as not relevant (newest saved copy is the 2016 home page; the site moved to kpp.energy). Gate passes.
  - `chase` FAIL 17: question records from the 10-21 run whose notes say "did not research", "in passing", "not part of the check" and so on. Plants: L100000401936 (4), L100000103924, L100000409214 (2), L100000401930 (3), L100000402306, L100000401933, L100000401931 (2), L100000103925, L100000103927 (2). Fixed by the chase pass the same day; gate passes.
  - `notes` ADVISORY 6: plant-level location-source records at L100000103924, L100001023601, L100000103925, L100000401935, L100000103926, L100000103927 name a source without a link.
- Review page republished as version 82 after the chase pass (`https://claude.ai/artifact/7bnX9RMity3Yw5mdaojNaL`, built 11:48, 415 records across Maryland, New York, Iowa, Kansas) and marked published. A second session was publishing the Illinois page at the same time; leave Illinois to it. The Germany page is stale and optional.
- The 2026-10-23 INDEX entry is written. Still optional: a line in `docs/country_notes/united_states/kansas.md` about Crooked Creek, Sherlock and Clifton unit 2 now being in the database.

## Open questions for Baird

All four answered 2026-10-23: keep the three bookkeeping watch cases; run the chase pass (done, gate clean, updates now 77); Clifton stays one 99 MW unit; rerun Illinois under the add rule (in progress).

## Model for the next session

Opus 5.5. The remaining work is mechanical: the access gate fix, the chase pass, the INDEX entry, tests, a commit when Baird asks. Use Fable only if rule-making resumes.

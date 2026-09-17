# Texas pilot plan (Q4 2026)

Goal: prove the researcher logic and SOPs on a small random sample of Texas
gas plants before scaling to the full state (277 plants / 587 unit rows) and
then to the other assigned US states. Working notes; edit freely.

## Phase 0 — intake and structure

- [x] Coordination check — Texas is assigned to the US researcher, 15 days,
      high priority, scheduled 2026-11-05 → 12-01 (Q4 Update V2 sheet).
      2026 edits on Texas rows came from two other researchers, so their
      conventions (EIA/EIP IDs in Other IDs, TCEQ citations) are the baseline.
- [x] Doc intake — kickoff, manual, Update V2 sheet, US guide, status-timeline
      training read; links in `docs/reference/sop_pointers.md`; rules that
      changed folded into `lifecycle_rules.md`, `update.md`, `qc.md`.
- [x] State-level notes — `docs/country_notes/united_states/texas.md`.
- [ ] `--state` filter for `worklist.py`, `scope_filter.py`/`qc_checks.py
      --country`, and a `Country/State` key in `build_campaign_roster.py`.
- [ ] gem-researcher-core boundary — decide what migrates (url_verifier,
      entity_lookup, normalize, generic staged-JSON checks) and how this repo
      consumes it (editable install of the sibling checkout). Run the pilot
      on local copies first; migrate after the pilot shows what the verifier
      needs for permit PDFs.
- [ ] Confirm Other IDs system names for TCEQ RN / ERCOT IRN in the DB.
- [ ] Agree a Texas-specific discovery escalation threshold.

## Phase 1 — calibration pilot (new workflow, not Update, not QC)

- Stratified sample, fixed seed, committed list: ~4 in-development, 3
  operating, 1 recently cancelled/retired, 1 captive/cogeneration.
- Blind protocol: the researcher agent gets plant name, coordinates, county
  and nothing else; produces the full field set with sources; only then the
  comparison step opens GEM's values.
- Scoring per field: match / GEM wrong / research wrong / both defensible /
  unresolvable. Per plant: minutes, URLs attempted, URLs verified, which
  source type resolved each field.
- Output: calibration memo (`batches/us-tx/calibration_<stamp>_ET.md`).
  Genuine GEM errors route to a normal Update batch afterward.
- Iterate: fix SOPs, draw a second disjoint sample, confirm the fixes held.

## Phase 2 — scale to Texas

- Bulk diff script: join EIA-860M + ERCOT GIS to GEM rows via the IDs already
  in Other IDs; divergences become worklist rows. Design the pilot's scoring
  output as this script's spec.
- Work the worklist by the manual's ladder (in-development first), then the
  status-group sweep for full coverage.

## Phase 3 — other assigned states

- Same pattern, smaller: state notes file + `batches/us-<st>/`; run several
  low-priority states as parallel small batches (this week's schedule:
  HI, ME, MD, MT, NH, NY, OR, RI, WA, AL, CO, FL, IL, IA).

## Things not to forget

- Permits state heat input or ISO turbine ratings, not net MWe.
- An issued air permit = pre-construction, not construction; renewals reset
  the inferred-status clock.
- TCEQ Records Online URLs rot — cite stable document URLs + Wayback.
- Sierra Club data is reference-only, never cited.
- Two Q4 Update sheets exist; V2 is live.

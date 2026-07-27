# Seed backlog: captive-power GOGPT candidates from the LNG repo

The first ready-made discovery input for this repo. The LNG terminals
researcher's captive-power workflow (2026-07) surfaced oil/gas power units
co-located with LNG terminals and industrial facilities that likely belong in
GOGPT — but that repo has no GOGPT write path, so the candidates were parked
in its staging tree. They are now THIS repo's backlog.

## Where the candidates live (sibling repo, read-only from here)

`lng-terminals-researcher/batches/staging/captive_power/<scope>/captive_gogpt_candidates.json`

| scope | candidates | notes |
|---|---|---|
| `europe` | 144 | broadest sweep |
| `americas-all` | 64 | supersedes/extends `americas` (45) — dedup against it |
| `americas` | 45 | earlier pass, overlaps americas-all |
| `louisiana` | 10 | LNG-corridor deep dive |
| `texas` | 5 | LNG-corridor deep dive |
| `us-gulf` | 4 | earliest pass, overlaps texas/louisiana |

Context memos from the same runs sit in the LNG repo's 2026-07 captive-power
staging dirs (`meta.json`, `captive_terminal_first.json`,
`captive_neighboring_plants.json` alongside each candidates file).

## How to work this backlog (first discovery batch)

1. Fresh pull + `scope_filter.py`; keep the UNFILTERED export handy (captive
   units sometimes sit on plants shared with coal/GCPT units).
2. Dedup the six candidate lists against each other (us-gulf ⊂ texas/
   louisiana ⊂ americas ⊂ americas-all, roughly) and against the scoped
   export (`GEM unit ID` / name+coords).
3. Screen per the Discovery SOP: ≥50 MW nameplate GENERATING capacity (never
   shaft/mechanical-drive MW), EU+UK ≥20 MW for the `europe` list; named
   operator + specific site + concrete evidence.
4. Stage survivors into `batches/<scope>/staging/` lanes (`newplants` /
   `newunits` / `monitor`), captive fields filled per
   `docs/reference/controlled_vocab.md`.
5. Candidates that fail the threshold or evidence bar go to `monitor` with a
   `recheck_by`, not to the trash — the LNG repo already did real work
   finding them.

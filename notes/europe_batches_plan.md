# Europe batches for Dan O'Beirne's Q4 2026 countries

Drafted 2026-10-03. Status: Baird agreed to start with Germany on 2026-10-05; the
Germany packet was built the same day (`batches/germany/INDEX.md`, 215 edits, 122
questions, 12 watch items) and awaits review. Not yet discussed with Dan. Open
questions 1 to 3 below are still unanswered.

## Who and when

Dan O'Beirne holds every European row on the Q4 2026 assignments tab (plus Armenia,
Azerbaijan, Georgia, Cyprus and Türkiye). His weekly schedule (Update V2 sheet,
"Weekly schedule" tab, 0.5 day per working day):

| dates | country | priority | days | in-dev units | total rows | backlog rows still open |
|---|---|---|---|---|---|---|
| 10-02 to 10-07 | Czech Republic | medium | 1.25 | 17 | 32 | 0 |
| 10-07 to 10-08 | Greece | medium | 0.75 | 10 | 58 | 3 |
| 10-08 to 10-09 | Hungary | medium | 0.5 | 3 | 26 | 0 |
| 10-09 to 10-21 | Germany | high | 3.5 | 35 | 355 | 1 |
| 10-21 to 11-02 | Ireland | high | 4.0 | 33 | 90 | 9 |
| 11-02 to 11-09 | Italy | high | 2.5 | 8 | 225 | 1 |
| 11-09 to 11-13 | Poland | high | 1.25 | 28 | 59 | 0 |
| 11-13 to 11-19 | Romania | high | 2.0 | 17 | 64 | 2 |
| 11-19 to 12-04 | United Kingdom | high | 5.0 | 50 | 235 | 2 |

Counts are from `campaigns/q4-2026/roster.csv` (pull of 2026-10-02) and the
"gas/oil plants" tab of the possible-updates sheet (rows with a blank Status
cell). Every one of his rows still reads "to do" in column N, including the small
September countries, so the status column is not a reliable progress signal.

## Which countries first

Recommended pair: **Germany, then Ireland.**

- Germany starts 10-09. Biggest fleet on his list after the UK, the best regulator
  data in Europe (Bundesnetzagentur Kraftwerksliste), a country note already in the
  repo, and a live news hook: the capacity tenders under the StromVKG law (passed
  July 2026). Round one closed on 8 September 2026 for 4,500 MW, awards are due by
  3 November 2026, round two is 29 December 2026 for another 4,500 MW, and a 2,000 MW
  round follows on 18 May 2027. (The Q2 2026 trend row's "9 GW on 8 September and
  22 December" figures were the earlier draft; the country note has the checked
  dates and sources.) Newly awarded projects are exactly the "newly announced"
  class the manual asks for.
- Ireland starts 10-21. Compact fleet, English-language sources, nine open backlog
  rows (the most of any of his countries), and strong public registers (EPA
  industrial emissions licenses and LEAP documents, EirGrid capacity statement, T-4
  capacity auction results, An Bord Pleanala planning files).

Optional shakedown before Germany: **Greece** (58 rows, 10 in-development units,
RAE license register, energypress.gr). It is small enough to run in a day and
catches country-mode bugs cheaply. It only pays off if the pipeline work is done by
Monday 10-05, since Dan reaches Greece on 10-07.

Not now: Czech Republic (he is on it this week), Hungary (3 units), Italy, Poland,
Romania and the UK (all November; pick up after the first two land).

## Step 1: country mode for the research agent

The state sweep (`docs/workflows.md` §7) is keyed on US states. Audit of
2026-10-03, changes needed:

- `build_state_brief.py`: add `--country` (exclusive with `--state`); skip the
  postal-code lookup; filter rows on Country/Area only; batch dir
  `batches/<country-slug>/`; worklist default `work/worklist_<country-slug>.csv`
  (what `worklist.py --country` already writes); read
  `docs/country_notes/<slug>.md`; drop the two EIA "Other IDs" tasks outside the
  US; relabel the identity block; write a `scope` key into `_index.json` alongside
  the existing `state`/`postal` keys.
- `build_sweep_args.py`: pass `scope` through; stop requiring `state`/`postal`.
- `.claude/workflows/state-sweep.js`: generic intro; a country research ladder in
  place of the EIA / ISO ladder (below); EIA-specific rules gated to the US; state
  the 20 MW EU and UK threshold; work dir and labels keyed on the slug.
- `assemble_state.py`: replace the hard-coded `COUNTRY = "United States"` with the
  scope's country (record IDs stay `<plant id>:<unit id>:<field>`; the slug names
  the batch dir and the staged `meta.scope`).
- `state_gate.py`, `build_review_package.py`, `worklist.py`, `qc_checks.py`: no
  change (the 20 MW threshold is already applied by `qc_checks.py` from the
  record's country).
- Docs: §7 of `docs/workflows.md` becomes "Scope sweep (US state or country)";
  `notes/us_state_agent_plan.md` gets a country-mode paragraph.

Country research ladder for the prompt (replaces EIA / PJM / NYISO):

1. The country note (inlined) and the record's existing Data Source links.
2. The national regulator's plant register or license register.
3. The transmission operator: connection queue, capacity statement, generation
   adequacy report; ENTSO-E transparency as the cross-check.
4. Capacity market registers where they exist (Ireland, Poland, Italy, UK, Belgium).
5. Planning and permit registers (environmental permits, EIA decisions).
6. Owner and sponsor investor pages and annual reports.
7. Trade press, searched in the local language with the local word for power plant.

Beyond Fossil Fuels (BFF) is the GEM team's main partner dataset for European gas
plants (Europe Workflow Map). Ask Dan whether the BFF dashboard and the GEM-BFF id
mapping sheet are something we may read; if yes they become ladder step 2.

## Step 2: country notes

- `docs/country_notes/germany.md`: refreshed 2026-10-05 (status vocabulary of the
  June 2026 Kraftwerksliste with the GEM mapping, the StromVKG tenders, the search
  vocabulary, and the rule to keep tender projects separate from CHP, district
  heating, industrial captive and data-center backup projects). Done.
- `docs/country_notes/ireland.md`: new. Sources: EPA industrial emissions license
  database (search by address, not operator; "View Applicant Documents", the
  non-technical summary gives turbine counts), EPA LEAP annual environmental
  reports (manufacturer details), EirGrid and SONI All-Island Generation Capacity
  Statement and Resource Adequacy statement, SEM Committee T-4 capacity auction
  results, An Bord Pleanala, CRU. Data-center gas and oil engine gensets are the
  growth story.
- `docs/country_notes/greece.md` only if the shakedown runs: RAE license register
  and annual report, IPTO (ADMIE) market statistics, energypress.gr.

## Step 3: what each batch checks

Update mode per the September 2026 manual, not a deep sweep:

- the ladder: in-development, shelved review, planned retirement this year, planned
  retirement, mothballed; 2 year and 4 year inferred-status candidates from
  `worklist.py`;
- newly announced plants (Germany: the tender awards; Ireland: data-center
  generation and the latest T-4 results);
- the open backlog rows for the country, folded in as extra tasks;
- the Q4 required item: operating units with no start year (Germany 1, Ireland 3);
- missing Data Source cells on the units touched;
- turbine make and model on in-development units ("not found" only after a search).

Upstream scans (`export_to_dump.py`, then `gogpt_csv_query.py --counts-only`,
`--ownership-scan`, `--in-progress-scan`, `--duplicate-scan`, `--possible-updates`)
run before the briefs are built; the unit-count baseline is reconciled against the
assignments tab row.

## Step 4: hand-off to Dan

- Output is the normal pair in `batches/<slug>/deliverables/` plus the review page
  (`review_app/build_static.py`, published as a claude.ai artifact from the work
  profile and shared with Dan by email as an editor), so Dan can accept or reject
  each change in a browser, his calls save on the page, and we rebuild from them.
  Germany's page: https://claude.ai/artifact/3YnJ2C36PwrTJ8qYgUxbuW (published
  2026-10-05, not yet shared).
- Before any run, tell Dan which countries we are taking and when the packet lands,
  so he does not research the same units. Ask: packet format he prefers, whether he
  wants to make the review calls himself, where on Drive to put the files, and the
  BFF access question above.
- The Country tips trends tab needs a Q4 2026 row per country from him; the
  evidence file's summary section is written so he can lift it.

## Timeline (proposed)

| day | work |
|---|---|
| Mon 10-05 | country mode in the four scripts and the workflow; Germany note refresh; Germany fresh pull, scans, briefs, sweep, gate and packet (all done) |
| Tue 10-06 to Thu 10-08 | Germany: Baird reviews, packet to Dan by 10-08; Ireland note; Greece shakedown skipped unless Baird asks |
| week of 10-12 | Ireland: same steps, packet by 10-16 |
| after | pick the next pair from Italy, Poland, Romania, UK based on what Dan says helped |

## Open questions for Baird

1. Confirm the pair (Germany, Ireland) and whether to run the Greece shakedown.
2. Message Dan before the pipeline work starts, or after Greece proves it works?
3. Who makes the accept and reject calls in the review app: Baird, Dan, or both?

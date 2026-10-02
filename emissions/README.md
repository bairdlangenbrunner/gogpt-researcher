# Gas plant air-pollutant emissions scoping (with CREA)

A **separate workstream** from the GOGPT tracker research this repo otherwise
exists for. It lives here only because it starts from the same fresh GOGPT pull.

**What it is.** GEM and CREA are preparing a grant proposal on the health
impacts of planned gas power expansion. CREA needs plant-level emissions of
**NOx, SOx/SO2 and PM** for proposed gas plants. GEM's part of the scoping is to
find out, country by country, whether environmental assessments / air permits
for in-development plants can be found and whether they carry usable emissions
data. The first scoping pass is a small random sample in two countries CREA
flagged as hard: **Vietnam and Brazil**.

## Boundary with the GOGPT workflows

- Nothing here is a GOGPT batch. There is **no staging, no lanes, no
  actions/evidence deliverable, no `qc_checks.py` gate**, and none of the
  Update / Discovery / Triage / QC SOPs apply.
- Nothing found here is staged into GEM. If this research turns up a genuine
  tracker correction (status, capacity, owner, a duplicate unit), write it under
  "tracker leads" in the plant's findings file and route it to a normal Update
  batch later.
- The GOGPT docs (`docs/sops/`, `docs/workflows.md`, `docs/reference/`) must
  not pick up emissions-research rules, and this directory must not pick up
  tracker-editing rules. Emissions methodology lives in
  `methods_and_fields.md`; it is CREA's, not the Editing Manual's.
- What carries over from the repo's hard requirements, because it is just good
  practice: fresh pull before sampling; a fetch failure is never evidence about
  the document; never cite gem.wiki / globalenergymonitor.org or abarrelfull;
  quote values exactly as written with page/table; unknown is not zero.
- The 86-column GEM schema has no emissions fields. Output here is findings
  files and a scoping memo, handed to CREA — not database edits.

## Layout

| Path | What |
|---|---|
| `search_plan.md` | **The current plan** (2026-09-18): systematic coverage — Vietnam as a census, Brazil all plants resolved to a licensor and a subset document-hunted |
| `build_coverage.py` | Builds / refreshes `coverage/<country>.csv` from the fresh scoped export; hand-kept search columns survive a rebuild |
| `portal_inventory.py` | Enumerates Vietnam's ministry consultation portal (every ĐTM and GPMT entry) into `coverage/vietnam_portal_all.csv`, with details for power / gas hits in `coverage/vietnam_portal_inventory.csv` |
| `coverage/` | The frame: one row per fossil-gas plant, GEM facts + search state (licensor, outcome, document, evidence, rungs tried). Vocabulary in `search_plan.md` |
| `scoping_plan.md` | The first plan and the record of the two 3 + 3 sampling probes of 2026-09-17: search ladders, what goes back to CREA, open questions |
| `methods_and_fields.md` | Distilled from CREA's methods doc: the evidence ladder (which kind of number is best), the fields to capture, QC rules |
| `draw_sample.py` | Seeded plant-level random sample from the fresh scoped export (used for the 2026-09-17 probes) |
| `countries/` | Living index of **where** emissions data can be found, one file per country (`README.md` is the index; Brazil and Vietnam so far). Locations and access methods only — values stay in `findings/` |
| `findings/` | One file per sampled plant (`_template.md` is the capture form), plus per-country scout notes and pilots. A pilot's `.py` rebuilds its `.csv` |
| `sources/` | What was downloaded and accessed: `downloads.csv` (every saved file, with URL, date, sha256), `access_log.csv` (every web request, by session), `get.py` to download. Files in `sources/raw/`, not in git. See `sources/README.md` |

Downloaded EIAs/permits are large third-party PDFs. Fetch them with
`sources/get.py`, which saves them to `sources/raw/` (not in git) and adds a
row to `sources/downloads.csv`. Findings cite the URL plus page numbers, not
the local copy.

## Source docs (live docs win over anything distilled here)

- CREA methods doc — *Gas power emissions: calculation methods and data requirements*: https://docs.google.com/document/d/1rNFKCIi5wJa0mYnoJ9EShWAII0zmvyBJE15mBEWvO2E/edit
- Regional prioritization (GEM questions, CREA answers): https://docs.google.com/document/d/1ObccNs34PI9DtW_xs1e9UqTeWRJ0-1MMU5IMLLrRFXM/edit
- CREA/GEM priority country ranking: https://docs.google.com/spreadsheets/d/1SNFMc3YwVOrxo1sMZ3w5WXp1GymJoyYcw-FyzyIOMIM/edit
- Timeline and budget: https://docs.google.com/spreadsheets/d/19_cs55ngTB7tl0QRC7miMMedbqJcQ92k6bJRrLiJPRU/edit
- Concept note (PDF): https://drive.google.com/file/d/1fZAZFf2k9RUWncmFHB_aW_zeEdaRZK_6/view
- Draft application form: https://docs.google.com/document/d/1PT1SMhUvU0B9XKZqCRVQIoC2FItef4hLVFYgznIlULk/edit

Read via `gws-gem` (work profile, read-only). Budget figures and draft
application text stay in those docs — this repo is public; don't copy them in.

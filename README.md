# GOGPT researcher

Operational repository for an LLM research assistant that helps maintain
[GEM's Global Oil and Gas Plant Tracker (GOGPT)](https://globalenergymonitor.org/projects/global-oil-gas-plant-tracker/).

This repo is designed to be used with [Claude Code](https://docs.claude.com/en/docs/claude-code).
The assistant produces staged deliverables for review; it never edits the live
database directly.

## Five workflows

| Workflow | When to use | Output |
|---|---|---|
| **Triage** | "What should we work on?" — priority worklist + inferred-status sweep | Markdown memo |
| **Update** | Refresh a country's plants/units (the quarterly bread-and-butter) | actions xlsx + evidence md |
| **Discovery** | Find plants/units missing from GEM (incl. the captive-power backlog) | actions xlsx + evidence md |
| **QC** | Audit data health; country close-out validation report | Markdown memo; fixes route to Update |
| **Campaign roster** | Track the quarterly country-assignment cycle | `campaigns/<quarter>/roster.csv` |

See `CLAUDE.md` for the routing logic and `docs/sops/` for the full procedures.

## Setup

```bash
pip install -r requirements.txt
brew install poppler        # optional: pdftotext, for verifying values inside PDFs
```

**Environment variables** (put them in `.env`, gitignored; `env.example` is the
template — copy it to `.env`). None are needed to read the repo — they gate the
live-data scripts:

| Variable | Needed by | What it is |
|---|---|---|
| `GEM_READONLY_DB_URL` | `../gem-db-ops/gogpt/pull.py` (the canonical pull, in the sibling repo), `scope_filter.py` (authoritative mode) | Postgres connection string for GEM's read-only replica. Ask GEM staff. |
| `URL_VERIFIER_LOG` | `url_verifier.py` (optional) | Path to an append-only JSONL log of verification attempts; set per batch. |

**Access prerequisites:** the GOGPT Editing Manual (Google Doc) is the
authoritative methodology and is NOT in this repo — the working rules are
distilled into `docs/reference/`, and every GEM doc/sheet ID lives in
`docs/reference/sop_pointers.md`. The sibling
[`gem-db-ops`](../gem-db-ops) repo must be checked out next to this one (or set
`GEM_DB_OPS_REPO`).

## Getting started

1. Read `CLAUDE.md` — the workflow router and hard rules; it is the assistant's
   entry point and the fastest orientation for a human too.
2. Skim `docs/reference/lifecycle_rules.md` and `unit_conventions.md` — the two
   files that encode most of what makes GOGPT different.
3. Run a **Triage** batch first (`docs/workflows.md` §4). It is memo-only —
   the lowest-risk way to exercise the pipeline end to end.

Smoke-check the setup (from `scripts/`, needs `GEM_READONLY_DB_URL`):

```bash
python ../../gem-db-ops/gogpt/pull.py --output gem_export_gogpt.csv   # fresh pull (~34.5k rows)
python pull_gem_db.py --map-only                                     # column-index map, 86/86 known
python scope_filter.py                                               # GOGPT-scoped view
python worklist.py --country "Nigeria"                               # a priority worklist
```

## The scope gotcha (read this once, remember it forever)

The GOGPT export contains **all combustion units** — oil and gas, but also coal
(GCPT) and bioenergy (GBPT) — because the upstream query doesn't filter on
tracker. `scope_filter.py` derives the GOGPT-only view that research and
worklists run on. The unfiltered CSV is kept deliberately: coal-to-gas
conversions, replacement units, and plants shared across trackers need the
coal side visible.

## Repository layout

In plain terms: **docs tell the assistant *how* to work, scripts do the
mechanical work, batches holds the output, campaigns tracks the quarterly cycle.**

```
CLAUDE.md                    Entry point for Claude Code — workflow router, hard rules
README.md                    This file
requirements.txt             Python deps (pip install -r)
env.example                  Template for .env (copy it there)
.gitignore                   Keeps data pulls, scratch outputs, and xlsx out of git

.claude/                     Claude Code settings notes; its README explains the choices

docs/
  workflows.md               Step-by-step command recipes for every workflow
  sops/                      The procedures
    update.md                Refresh a country's plants/units
    discovery.md             Find plants/units missing from GEM
    triage.md                Decide what to work on (worklist-driven)
    qc.md                    Audit data health; country close-out checklist
  reference/                 Lookup tables and rules (read on demand)
    lifecycle_rules.md       Status vocab, inferred 2y/4y rules, year-field logic
    unit_conventions.md      Unit definition (CC block = one unit), naming, conversions
    controlled_vocab.md      Fuels, technologies, capacity + ownership rules
    gem_db_schema.md         GOGPT-relevant tables in the GEM database
    source_roster.md         Where to look, by source type and tier
    datasource_conventions.md  Citation mechanics (from the GEM Project Database Manual)
    wiki_pages.md            Why there is no wiki lane (pages are auto-generated)
    staged_json_schema.md    THE staging contract — six lanes, record shapes, QC gates
    workbook_conventions.md  Deliverable naming, sheets, cell colors
    confidence_tiers.md      What earns green/yellow/red/blue
    sop_pointers.md          Which rule lives where + every GEM doc/sheet ID
  country_notes/             One research-notes file per country

scripts/                     Python tools called by the workflows
  paths.py                   Repo-relative path helpers (no hard-coded absolutes)
  pull_gem_db.py             Column-index map + schema-drift detection (both the engine and the
                             canonical 91-column map live in ../gem-db-ops/gem_colmap.py)
  scope_filter.py            Derive the GOGPT-only view from the all-combustion export
  worklist.py                Priority-ladder triage worklist + inferred-status sweep
  qc_checks.py               Mechanical validation of CSV slices and staged records
  schema_constants.py        Controlled vocab, thresholds, out-of-scope columns
  colmap.py                  Load the derived column map
  url_verifier.py            Verify a URL works and shows the claimed value
  export_to_dump.py          Bridge the fresh scoped pull into the upstream dump format
  entity_lookup.py           Check whether a company already exists in GEM's entity system
  normalize.py               Standardize country/entity names, parse ownership shares
  build_review_package.py    Assemble staged JSON into the actions xlsx + evidence md
  build_campaign_roster.py   Generate/refresh the quarterly campaign roster
  recalc.py                  Sanity-check a built xlsx before it's presented

review_app/                  Local page for deciding on a batch's staged edits (README inside);
                             writes only review_log.jsonl in the staging dir, consumed by
                             build_review_package.py --decisions
tests/                       pytest suite (python -m pytest tests/)

batches/                     Everything a batch produces (see batches/README.md)
  <scope>/staging/           TRACKED: staged_<lane>.json — the audit trail, plus the review
                             app's review_log.jsonl / review_decisions.json once reviewed
  <scope>/deliverables/      actions xlsx (gitignored) + evidence md (tracked)
  run_records/               Dated cross-scope run logs

campaigns/                   One dir per quarter; roster.csv tracks the country cycle
notes/                       Ad-hoc memos; the captive-power seed backlog lives here
work/                        Scratch — worklists and derived outputs (gitignored)

upstream/
  gogpt-tracker/             Verbatim import of the GOGPT leads' own pipeline —
                             scans, context cards, publish compile. Never edited
                             by this repo's workflows; see CLAUDE.md "Upstream".
                             Its data dumps are gitignored (regenerate via
                             scripts/export_to_dump.py after a fresh pull).
```

## Hard rules

A non-exhaustive list (full list in `CLAUDE.md`):

- Never edit the live GEM database. All outputs are staged deliverables.
- Pull a fresh export + re-derive the column map at the start of every batch.
- Verify every URL before staging it — the claimed value must appear on the page.
- One fully validated ref per staged value suffices; a second independent source is preferred, and a status change needs 2+ for green. Mirrors of one document count once.
- Never cite gem.wiki / globalenergymonitor.org / GEM-derived republishers; abarrelfull is banned outright.
- Data Source cells merge, never replace — existing citations are never deleted.
- Capacity is generating MW only (MWe, nameplate) — never shaft/mechanical-drive MW.
- Start year is never filled for shelved/cancelled units; hydrogen columns are do-not-research.
- Run `entity_lookup.py` before staging any new entity — the entity system is shared across all GEM trackers.

## Methodology

This scaffolding follows GEM's GOGPT Editing Manual. The manual is
authoritative; this repo encodes how the agent applies it operationally.

The GOGPT team leads' own research pipeline is imported verbatim at
`upstream/gogpt-tracker/` — its cross-cutting scans and counts baseline are
wired into the Update workflow, and its `docs/METHODOLOGY.md` is their
distilled statement of the manual's scope and status rules.

## Sibling repos

Part of a family: `lng-terminals-researcher`, `pipelines-researcher`,
`refineries-researcher`, with `gem-db-ops` as the shared pull engine. This repo
is the GOGPT write path the LNG repo's captive-power workflow refers to; its
first discovery backlog was seeded from that workflow's candidates
(`notes/backlog_captive_power_candidates.md`).

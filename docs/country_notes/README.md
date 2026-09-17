# Country research notes

One file per country, distilled from research experience on the Global Oil and Gas
Plant Tracker (GOGPT). Use `_template.md` as the starting point for new countries.

**Subnational scopes** (research assigned per state/province — currently the United
States) get a subfolder named after the country file: `united_states.md` holds what is
true nationwide, `united_states/<state>.md` holds the state's source ladder, regulator
stack and gotchas. Use the same `_template.md`; the state file's scope line names the
ISO/RTO and the cycle's priority level / days from the assignments tab.

## Origin

These notes descend from GEM's team-wide crowdsourced Google Doc, **"Gas/oil power
plant data sources - by country"**
(Doc ID `1J4JHu_Sy5190nMGCUqw8B_0UQwVgopcNo8UJTXE-cRw`). That doc remains the
living, team-wide source list across all countries GEM tracks (it covers far more
countries than this repo has seeded notes for) and is the place to add a new
source lead if you're not sure it belongs in a repo-local file yet.

This directory is the repo-local **distillation** of that doc: a smaller, curated
set of country files scoped to what a GOGPT researcher actually needs at the start
of a batch, kept close to the code/data it supports and versioned with the rest of
the repo. Personal names and researcher attributions may be kept when pulling material
in (ruling 2026-09-15); credentials and third-party confidential material still
never go in.

## How to use

1. **Before starting a batch**, check `<country>.md` for the countries in scope:
   known regulator URLs, preferred sources, research tips, and gotchas from prior
   batches. This should save you from re-discovering the same sources or
   re-tripping the same known data-quality traps (e.g. dual-fuel plants
   miscategorized as gas-only).

2. **During the batch**, take notes on new resources, search patterns, dead
   links, and anything that would have been useful to know at the start.

3. **At batch close**, fold the batch's country-notes contributions back into the
   relevant `<country>.md` file(s) under "Update notes" (and update other
   sections directly if something durable changed — a source went dead, a new
   preferred source emerged, a gotcha was confirmed or resolved). Keep entries
   dated and terse; this is a working reference, not a narrative log.

## Currently seeded

- `nigeria.md`, `south_africa.md`, `india.md`, `germany.md`, `vietnam.md`,
  `brazil.md`, `united_states.md`, `russia.md`
- US states: `united_states/texas.md`

Countries not listed should be created from `_template.md` when first researched.

## A note on staleness

Much of the sourcing in the upstream Google Doc dates to 2019-2022. Government
portals, regulator page structures, and even agency names change; a link or
observation flagged "as of <year>, re-verify" in a country file should be checked
against the current source before being relied on, not assumed still accurate.

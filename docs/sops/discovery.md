# GOGPT Discovery SOP

Last revised: 2026-07-27 (rev 1 — initial GOGPT adaptation from lng-terminals-researcher discovery.md rev 3)

Operational rules for finding gas/oil combustion plants and units that are NOT yet in the GEM Global Oil and Gas Plant Tracker (GOGPT) — new announcements, capacity expansions at existing plants, and captive plants at industrial facilities. Discovery stages candidates into the `newplants` / `newunits` lanes for human review and addition to the live DB.

The GOGPT Editing Manual is authoritative for what counts as a trackable unit, the ≥50 MW inclusion threshold, and plant/unit naming conventions. This SOP is operational — it describes how to execute discovery work, citing the manual rather than restating it.

## §1 When to run this SOP

Trigger conditions:
- Country research (Update SOP) hits the manual's standing instruction to "search for newly announced plants and add them to the database" — discovery is folded into ordinary country research, not only a standalone batch
- Triage/QC flags a coverage gap or an industrial sector (steel, cement, refining, petrochemicals, data centers, mining) not yet swept for captive generation
- A specific news event suggests new plant activity (an FID, a groundbreaking, an industrial facility announcing on-site generation)
- The user explicitly requests a discovery sweep for a country, region, or industrial sector
- A "catch-up sweep" after a long period without coverage of a particular country

## §2 What it produces

Discovery candidates land in the same staging structure as an update batch (`batches/<country-scope>/staging/`), in the `newplants` (new plant, one or more new units) and `newunits` (new unit(s) at an existing plant) lanes. They are built into the same two-file deliverable as any other batch — actions workbook + evidence workbook — by `build_review_package.py`; there is no separate discovery-only workbook format. A discovery-only batch (no update work) still produces the standard two files, just with `newplants`/`newunits` as the only populated lanes.

Candidates that don't yet meet the threshold (§3) are not staged — see §3's monitoring guidance.

## §3 The ≥50 MW inclusion threshold

Apply this **before** building a candidate row:

- **Capacity test**: nameplate/installed generating capacity ≥50 MW per unit (or per IC/AGT engine set, summed across engines). The **EU and UK use a <20 MW per-unit exception** — a smaller unit still qualifies there.
- **Generating MW only. Never shaft/mechanical-drive MW.** This is the single most common trap at industrial sites: a compressor-drive gas turbine at an LNG terminal, refinery, or pipeline compressor station is out of scope even at large mechanical ratings — only the electricity-generating capacity counts, and only if a generator is actually attached.
- **Ranges take the high end**, rounded to the nearest whole MW.
- Capacity is **MWe (electrical), never MWt (thermal)**.

A candidate that's real but under threshold, or where capacity can't yet be pinned down, is not staged — note it in `docs/country_notes/<country>.md` as a watch item with what's missing (usually capacity or a concrete construction step) so the next sweep doesn't re-discover it from scratch.

## §4 Discovery sweep — where to look

Adapted for GOGPT from the family's ring model; work roughly in this order, each ring catching what the last missed.

### §4.1 Regulatory / government sources

The most authoritative ring — national energy ministries, grid/system operators, electricity regulators, and IPP procurement authorities publish plant lists, capacity registries, and generation licenses that establish both existence and several fields at once. `docs/country_notes/<country>.md` is the working memory for country-specific regulator URLs and filing patterns — check it first, and contribute back what you find.

### §4.2 Trade press and local news

Search in English and, per the manual, the **local language** for the country (plant names and generic terms — see the manual's local-terminology reference). Search patterns that work: `"<country>" "gas power plant" "announced" "<year>"`, `"<country>" "IPP" "gas turbine" "FID"`, `"<owner/developer>" "power station" "<country>"`.

### §4.3 Owner / operator IR and company disclosures

Utilities' and IPPs' annual reports, investor decks, and press releases often disclose new capacity before it hits trade press or a regulator filing. This is also the source for datasource short-names per the manual's convention (§6).

### §4.4 Captive-plant sweep at industrial facilities

**Captive plants ARE in scope**, and are the ring most likely to be missed by a plant-name-driven search, because they're rarely named "X power station" — they surface as a line item in an industrial facility's own disclosures. For each in-scope country, sweep industrial sectors with on-site generation: oil & gas processing/refining, petrochemicals, steel, cement, mining, and large data centers. Look for:
- Environmental permits / emissions filings for on-site generators
- The facility's own sustainability or annual report ("self-generation," "captive power")
- Grid-interconnection or islanding disclosures

Apply §3's generating-MW-only rule with extra care here — captive turbines are often mechanical-drive units with no generator, which are correctly excluded, alongside true captive generators of the same nameplate rating that are correctly included. When a captive plant qualifies, flag it as captive at staging time (§6) so the actions workbook carries the Captive fields alongside the core plant/unit fields.

### §4.5 Broader scan (optional, when prior rings underyield)

Financier/ECA disclosures, EPC contractor project-win announcements, and equipment-supplier (turbine OEM) order books occasionally surface projects ahead of any public plant-level announcement. Treat these as leads needing the most verification before staging.

## §5 Dedup against existing GEM

Before staging anything as new:

1. Check the country's **scoped CSV** (`scope_filter.py` output) for a plant already at or near the candidate's name/location — coordinates are often more reliable than name matching for this.
2. Check the **unfiltered CSV** too — a "new" gas plant is sometimes actually a coal-to-gas conversion or a co-located unit at an existing coal (GCPT) or bioenergy (GBPT) plant, which should route to the Update SOP's conversion/co-location handling (update.md §4.3, §9.3), not a new-plant stage.
3. Look up the candidate name in gem.wiki to check whether it's already tracked under a different name or linked to a related coal plant / LNG terminal / steel plant (the manual's own dedup tip). **gem.wiki is used here only to detect a possible existing record — never cited as a source or `[ref]`** — the anti-circularity rule applies to dedup lookups exactly as it does to research citations.
4. A match at either step routes the finding to the Update SOP (it's an existing record needing a fix, not a new one); no match → proceed to build the candidate row (§6).

## §6 Building a candidate row

For a genuinely new plant, minimum fields to stage in `newplants` (plus one row per unit in `newunits`):

- **Plant Name** — per the manual's naming convention (ends in "power station" unless a non-conforming name supersedes it; disambiguate same-name/same-area plants by owner or state in parentheses)
- **Country**
- **Location** — coordinates with `Accuracy` (`exact` ≥3 decimals, else `approximate`); plant-level only, never per-unit
- **Capacity** — generating MWe, whole MW, high end of any range (§3)
- **Technology** and **Fuel** — from the manual's controlled vocabularies (CC, GT, AGT, ST, IC, ICCC, ISCC, AFC; fossil gas / fossil liquids / industrial by-product / hydrogen)
- **Status** — almost always `announced`, `pre-construction`, or `construction` for a genuinely new find; `operating` only when the plant has clearly been running undetected
- **Owner** — entity lookup mandatory before staging (§7)
- **Captive fields** (if applicable) — Captive checkbox, Captive Industry Type, Captive Industry Use / Non-Industry Use (§4.4)
- At least one datasource covering plant existence, location, and capacity

A **new unit at an existing plant** (a capacity expansion, a new turbine at a plant already in GOGPT) only needs the unit-level fields — plant-level fields (name, country, location, plant-level owner) are already set and shouldn't be re-staged.

## §7 Entity discipline

Per update.md §8: before staging any new Owner/Operator, run `python entity_lookup.py "<entity name>" --pg` **bare, no country filter** — entities are shared across GEM trackers and countries. A match anywhere means use the existing entity ID; no match routes to the `entity` lane with the lookup attempts logged, for the human to create via the web UI before applying dependent edits.

## §8 URL verification gate

Every staged URL passes `url_verifier.py` per update.md §7.1 — no exceptions. Discovery's specific risk: a source that mentions a project name without actually establishing the threshold facts (a developer's investor day deck listing "potential opportunities including a plant in X" reads like a hit but doesn't establish existence). Choose `expected_string` arguments that verify the plant/site name, the capacity or a concrete development step, and the country — not just the name in isolation. `≥2 independent working URLs per staged value` and the anti-circularity source rules (never gem.wiki/globalenergymonitor.org, never abarrelfull) apply exactly as in update.md §7.2.

## §9 Workflow (linear)

1. Confirm country/sector scope with the user
2. Fresh pull chain: `python ../../gem-db-ops/gogpt/pull.py` → `python pull_gem_db.py --map-only` → `python scope_filter.py` (keep the unfiltered CSV per §5.2)
3. Work the rings in order (§4), sweeping the captive-industry ring explicitly rather than only searching by plant name
4. For each lead, dedup (§5) — route matches to Update, proceed with the rest
5. Apply the ≥50 MW / EU-UK 20 MW threshold (§3) — under-threshold leads go to `docs/country_notes/<country>.md` as watch items, not staged
6. Build the candidate row(s) into `newplants`/`newunits` (§6)
7. `python entity_lookup.py` for every new entity reference (§7)
8. `python url_verifier.py` on every staged URL (§8)
9. `python qc_checks.py` on the staging dir — same mechanical gate as any batch (`docs/sops/qc.md`)
10. `python build_review_package.py --inputs-dir batches/<country-scope>/staging --mode update` (or the country's active batch mode) → actions + evidence workbooks
11. Present the deliverables; the human applies the actions workbook by hand in the web UI

## §10 Hard rules

- **Generating MW only — never shaft/mechanical-drive MW.** The single highest-risk error at captive/industrial sites (§3, §4.4).
- **≥50 MW threshold (EU/UK <20 MW exception)** before staging any candidate (§3).
- **Captive plants ARE in scope** — don't skip a site because it's industrial rather than utility-owned (§4.4).
- **Dedup before staging** — scoped CSV, unfiltered CSV, and a gem.wiki name check, every candidate (§5).
- **gem.wiki is a dedup check only, never a citation** (§5.3).
- **Entity lookup bare + `--pg` before staging any new owner** — no duplicate entities (§7).
- **Every URL passes `url_verifier.py`; one fully validated ref per value suffices (2+ independent preferred; 2+ for a status change to be green); never gem.wiki/globalenergymonitor.org/abarrelfull** (§8).
- **Never write the live GEM database** — output is always the staged lanes feeding the two-workbook deliverable for human application.

## §11 Pause-and-ask triggers

Stop and consult the user when:

- A candidate's capacity can't be pinned down closely enough to know which side of the 50/20 MW line it falls on
- A captive plant's generator vs. mechanical-drive configuration is ambiguous from available sources (misclassifying this either way is a scope error, not a data-quality one)
- Discovery would add more than a handful of new plants to a country in one batch (suggests a systematic prior gap worth flagging, not silently absorbing)
- A candidate looks like it might be a coal-to-gas conversion or a co-located unit at an existing coal/bioenergy plant rather than a genuinely new plant
- `entity_lookup.py` finds no match for an owner that obviously should already exist in GEM

---

## Quick-reference card

| Ring | What | Use when |
|---|---|---|
| Regulatory | Ministries, grid operators, IPP registries | Always — most authoritative |
| Trade press / local news | English + local-language search | Always |
| Owner/operator IR | Annual reports, investor decks | Always |
| Captive-industrial sweep | Oil & gas, petrochemical, steel, cement, mining, data centers | Always — easiest ring to skip |
| Broader scan | Financiers, EPC, equipment OEMs | When prior rings underyield |

| Check | Threshold |
|---|---|
| Capacity (most countries) | ≥50 MW nameplate, generating MWe only |
| Capacity (EU + UK) | ≥20 MW per unit |
| Range values | High end, whole MW |

| Finding | Route |
|---|---|
| New plant, passes threshold | `newplants` (+ `newunits` per unit) |
| New unit at existing plant | `newunits` only |
| Matches an existing record | Update SOP, not a new stage |
| Under threshold / capacity unknown | Note in country notes as a watch item |

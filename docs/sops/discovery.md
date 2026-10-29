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

Candidates that cannot be added yet go to the `monitor` lane with a `watch_case` (§3.1). The bar for adding is low on purpose, because the manual's is: one verified source that names the project, places it in scope and gives a capacity (or none) is an add.

## §3 The ≥50 MW inclusion threshold

Apply this **before** building a candidate row:

- **Capacity test**: nameplate or installed electrical capacity ≥50 MW per unit (or per IC/AGT engine set, summed across engines; a data center's backup engine fleet is summed too). The **EU and UK threshold is 20 MW** (the manual's "<20MW per unit" reads as a typo; whether 20 MW applies per engine or to the summed set is asked of Dan O'Beirne, and the repo sums meanwhile).
- **Electrical nameplate only. Never shaft/mechanical-drive MW** (M603). This is the single most common trap at industrial sites: a compressor-drive gas turbine at an LNG terminal, refinery, or pipeline compressor station is out of scope even at large mechanical ratings — only the electricity-generating capacity counts, and only if a generator is actually attached.
- **Ranges take the high end.** Record the figure the source gives, at most one decimal; rounding to the whole MW is allowed, never required.
- Capacity is **MWe (electrical), never MWt (thermal)**.

A candidate that is real but under threshold is a `monitor` record with `watch_case` `under_threshold` and a `recheck_by` date, so the next sweep does not rediscover it from scratch. A candidate whose capacity cannot be found at all is **added with the capacity blank**: the manual says to leave the cell empty and remove the plant later if it turns out to be small.

### §3.1 The add threshold: one source, and the status ladder sets the status (Baird 2026-10-23)

The manual's bar for a new row is the `announced` definition: a project that is publicly reported, including one that appears only in a long-range company or government planning document. It adds a plant with no capacity found, no owner found ("if it is a very new or vague proposal and you cannot find this info, leave this field blank") and no start year. So a project GEM lacks is an add, in `newplants` or `newunits`, as soon as **one verified public source** names a gas or oil generating project, places it in the scope, and gives a capacity at the threshold (engine and aeroderivative sets summed), a unit count with a plant total, or no capacity at all.

- **Status comes from the manual's ladder, never from how much was found.** A planning document, a grid-operator interconnection queue entry or a press announcement is `announced`. A permit application, land, financing, a prior-approval docket or a signed interconnection agreement is `pre-construction`. A project found already cancelled, shelved or retired since 2020 is an add with that status.
- **Missing start year, owner, turbine model or exact coordinates never hold an add back.** Leave the field blank and say in `researcher_notes` what was not found. Coordinates follow the location ladder; a town alone is `approximate`.
- **A queue entry under a shell company name is still an add** at `announced`, named after the queue entry or its site. The live database already records plants this way (18 US units whose only status source is an ERCOT, MISO, SPP or PJM document, counted 2026-10-23). The manual says nothing about interconnection queues either way; the team's practice is to add, and Baird confirmed on 2026-10-23 that queue-only entries are adds and that shell-company entries keep going in at `announced`, owner blank unless a parent is named.
- **The watch list is for seven cases only**, each named in the record's `watch_case` (`docs/reference/staged_json_schema.md`): no generating unit named yet; every unit under the threshold and not a qualifying set; generator versus mechanical drive, or thermal versus storage, unresolved; a possible duplicate of a GEM record (prefer a `qa` question); a plan option that commits to nothing; a find in another state or country (listed as a handoff in the evidence file); nothing verified yet. A project that fits none of them is an add. `state_gate.py` gate `watch-case` flags a watch item that names no case or whose capacity or verifications contradict it.
- **Data centers are adds** (Baird 2026-10-27). A backup engine fleet at the summed nameplate threshold (50 MW, 20 MW in the EU and UK) is a plant, and capacity unknown means add with capacity blank (M597). A gas-fired data center plant is added like any other project, with its status from the ladder; there is no hold. Convention: name it "<Operator> <Place> Data Center power station" (M237); one unit row per permit phase or building group, or one unit when the permit does not split the fleet; internal combustion with Number Of Engines and Capacity Per Engine from the permit; fuel diesel, natural gas or both; Captive industry type data center, Captive industry use power, Captive non-industry use none, Backup Power yes, at unit level; the data center in Project Links (M378). `data_center_fleets.py` sums the fleets and `state_gate.py` gate `data-centers` requires every site at or above the threshold to be answered (Update SOP §3.9).
- **A verified captive LNG plant at the threshold is an add.** The LNG team's captive workbook is a lead list and its Qualifying rows are checked first; a plant with no name of its own is "XYZ LNG terminal power station", with the terminal in Project Links. Compressor drives stay excluded.
- **One source is green for every value of an add.** The status-change rule (two independent publishers for green) is for changing the status of an existing unit, not for a new row.

## §4 Discovery sweep — where to look

Adapted for GOGPT from the family's ring model; work roughly in this order, each ring catching what the last missed.

### §4.1 Regulatory / government sources

The most authoritative ring — national energy ministries, grid/system operators, electricity regulators, and IPP procurement authorities publish plant lists, capacity registries, and generation licenses that establish both existence and several fields at once. `docs/country_notes/<country>.md` is the working memory for country-specific regulator URLs and filing patterns — check it first, and contribute back what you find.

### §4.2 Trade press and local news

Search in English and, per the manual, the **local language** for the country (plant names and generic terms — see the manual's local-terminology reference). Search patterns that work: `"<country>" "gas power plant" "announced" "<year>"`, `"<country>" "IPP" "gas turbine" "FID"`, `"<owner/developer>" "power station" "<country>"`.

### §4.3 Owner / operator IR and company disclosures

Utilities' and IPPs' annual reports, investor decks, and press releases often disclose new capacity before it hits trade press or a regulator filing. This is also the source for datasource short-names per the manual's convention (§6).

### §4.4 Captive-plant sweep at industrial facilities

**Captive plants ARE in scope**, and are the ring most likely to be missed by a plant-name-driven search, because they're rarely named "X power station" — they surface as a line item in an industrial facility's own disclosures. For each in-scope country, sweep industrial sectors with on-site generation: oil & gas processing/refining, petrochemicals, steel, cement, mining, and large data centers (backup engine fleets included; run `data_center_fleets.py`). Look for:
- Environmental permits / emissions filings for on-site generators
- The facility's own sustainability or annual report ("self-generation," "captive power")
- Grid-interconnection or islanding disclosures

Apply §3's electrical-nameplate rule with extra care here — captive turbines are often mechanical-drive units with no generator, which are correctly excluded, alongside true captive generators of the same nameplate rating that are correctly included. When a captive plant qualifies, flag it as captive at staging time (§6) so the actions workbook carries the Captive fields alongside the core plant/unit fields.

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
- **Location** — coordinates with `Accuracy` (`exact` ≥3 decimals, else `approximate`); plant-level only, never per-unit. Found through the location ladder in `docs/reference/location.md`: an address or site sentence in a document, geocoded and checked in satellite imagery, earns `exact`; a town alone is `approximate`. The coordinate is written as a Google Maps link wherever a person reads it Look for the street address of every new station: use it to get the exact point, name it in the staged note and tell the reviewer, but never enter it in a cell (Baird 2026-10-21).
- **Capacity** — electrical nameplate MWe, high end of any range (§3)
- **Technology** and **Fuel** — from the manual's controlled vocabularies (CC, GT, AGT, ST, IC, ICCC, ISCC, AFC; fossil gas / fossil liquids / industrial by-product / hydrogen)
- **Status** — almost always `announced`, `pre-construction`, or `construction` for a genuinely new find; `operating` only when the plant has clearly been running undetected
- **Owner** — entity lookup mandatory before staging (§7)
- **Captive fields** (if applicable) — Captive checkbox, Captive Industry Type, Captive Industry Use / Non-Industry Use (§4.4)
- At least one datasource covering plant existence, location, and capacity

A **new unit at an existing plant** (a capacity expansion, a new turbine at a plant already in GOGPT) only needs the unit-level fields — plant-level fields (name, country, location, plant-level owner) are already set and shouldn't be re-staged.

## §7 Entity discipline

Per update.md §8: before staging any new Owner/Operator, run `python entity_lookup.py "<entity name>" --pg` **bare, no country filter** — entities are shared across GEM trackers and countries. A match anywhere means use the existing entity ID; no match routes to the `entity` lane with the lookup attempts logged, for the human to create via the web UI before applying dependent edits.

## §8 URL verification gate

Every staged URL passes `url_verifier.py` per update.md §7.1 — no exceptions. Discovery's specific risk: a source that mentions a project name without actually establishing the threshold facts (a developer's investor day deck listing "potential opportunities including a plant in X" reads like a hit but doesn't establish existence). Choose `expected_string` arguments that verify the plant/site name, the capacity or the development step that sets the status, and the country — not just the name in isolation. One fully validated source closes a value at green (a second is preferred, never required; Baird 2026-10-02), and the anti-circularity source rules (never gem.wiki/globalenergymonitor.org, never abarrelfull) apply exactly as in update.md §7.2.

## §9 Workflow (linear)

1. Confirm country/sector scope with the user
2. Fresh pull chain: `python ../../gem-db-ops/gogpt/pull.py` → `python pull_gem_db.py --map-only` → `python scope_filter.py` (keep the unfiltered CSV per §5.2)
3. Work the rings in order (§4), sweeping the captive-industry ring explicitly rather than only searching by plant name
4. For each lead, dedup (§5) — route matches to Update, proceed with the rest
5. Apply the ≥50 MW / EU-UK 20 MW threshold (§3) and the add threshold (§3.1) — a lead that fits one of the seven watch cases goes to the `monitor` lane with its `watch_case` and `recheck_by`; everything else is an add, with blanks for what was not found
6. Build the candidate row(s) into `newplants`/`newunits` (§6)
7. `python entity_lookup.py` for every new entity reference (§7)
8. `python url_verifier.py` on every staged URL (§8)
9. `python qc_checks.py` on the staging dir — same mechanical gate as any batch (`docs/sops/qc.md`)
10. `python build_review_package.py --inputs-dir batches/<country-scope>/staging --mode update` (or the country's active batch mode) → actions + evidence workbooks
11. Present the deliverables; the human applies the actions workbook by hand in the web UI

## §10 Hard rules

- **Electrical nameplate MW only — never shaft/mechanical-drive MW.** The single highest-risk error at captive/industrial sites (§3, §4.4).
- **≥50 MW threshold (20 MW in the EU and UK)** before staging any candidate (§3).
- **Captive plants ARE in scope** — don't skip a site because it's industrial rather than utility-owned (§4.4).
- **Dedup before staging** — scoped CSV, unfiltered CSV, and a gem.wiki name check, every candidate (§5).
- **gem.wiki is a dedup check only, never a citation** (§5.3).
- **Entity lookup bare + `--pg` before staging any new owner** — no duplicate entities (§7).
- **Every URL passes `url_verifier.py`; one fully validated ref per value suffices (2+ independent preferred; 2+ for a status change to be green); never gem.wiki/globalenergymonitor.org/abarrelfull** (§8).
- **Never write the live GEM database** — output is always the staged lanes feeding the two-workbook deliverable for human application.

## §11 Pause-and-ask triggers

Stop and consult the user when:

- A candidate's stated capacity sits close to the 50/20 MW line (units straddling the bar, a set whose summed figure is uncertain). A candidate with no capacity stated at all is not a pause: it is added with the cell blank (§3.1)
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
| Capacity (most countries) | ≥50 MW electrical nameplate |
| Capacity (EU + UK) | ≥20 MW (per engine or summed: asked of Dan O'Beirne) |
| Range values | High end, at most one decimal |

| Finding | Route |
|---|---|
| New plant, passes threshold | `newplants` (+ `newunits` per unit) |
| New unit at existing plant | `newunits` only |
| Matches an existing record | Update SOP, not a new stage |
| Under threshold, no generation named, drive or storage unresolved, possible duplicate, plan option, other scope, nothing verified | `monitor` with `watch_case` and `recheck_by` (§3.1) |
| Capacity unknown, start year, owner or site unknown | Still an add, with those cells blank and the note saying what was not found (§3.1) |
| Found already cancelled, shelved or retired (2020 on) | Add with that status |

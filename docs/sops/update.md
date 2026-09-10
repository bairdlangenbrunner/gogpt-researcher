# GOGPT Update SOP

Last revised: 2026-08-04 (rev 2 — adopted the upstream pipeline's cross-cutting scans, counts baseline, and status-group coverage sweep; rev 1 2026-07-27 was the initial GOGPT adaptation from lng-terminals-researcher rev 2)

Operational rules for updating existing plants and units in the GEM Global Oil and Gas Plant Tracker (GOGPT). This is the bread-and-butter workflow of the quarterly cycle: working an assigned country's units in priority order, refreshing statuses and values, filling missing datasources, and processing inferred-shelved/cancelled candidates.

The GOGPT Editing Manual is authoritative for the underlying research rules (statuses, unit definition, capacity thresholds, fuel/technology vocabularies). This SOP is operational — it describes how to execute the work, citing the manual rather than restating it.

## §1 When to run this SOP

Trigger conditions:
- A country assignment from the quarterly roster (`campaigns/<quarter>/roster.csv`, mirroring the "Researcher Country Assignments" tab) moves to `in progress`
- Triage SOP has selected a country/scope for update this batch
- A QC memo (`docs/sops/qc.md`) routed fixes here — dead citations to replace, unsupported values to re-research, not-applied/diverged edits to re-stage ("QC detects, Update fixes")
- `worklist.py` flagged shelved-inferred-2y or cancelled-inferred-4y candidates
- A specific news event triggers a known-needed update (a confirmed construction start, a cancellation, a conflict-damage report)
- The user explicitly requests an update batch ("refresh the Vietnam gas plants", "process the retirement backlog")

Research is organized in **quarterly cycles with per-country assignments**. A country moves `not started` → `in progress` → `done` → PM review. One country-scope = one batch directory (`batches/<country-scope>/`).

## §2 What it produces

An update batch produces a **two-file deliverable** in `batches/<country-scope>/deliverables/`:

1. **Actions workbook** — a per-plant / per-unit edit checklist: current value → proposed value → evidence. This is what the human works through, applying each edit **by hand in the gem-project-db.herokuapp.com web UI**. Nothing in this repo ever writes to the live database.
2. **Evidence workbook** — the audit trail: every staged record with its sources, verification results, confidence color, and researcher notes.

Both are built by `build_review_package.py` from the staged JSON lanes in `batches/<country-scope>/staging/`. The lanes are `updates | qa | entity | monitor | newplants | newunits`. There is **no wiki lane** — GOGPT wiki pages are auto-generated from the database; only the "Background" section is ever hand-edited, and wiki work is generally out of scope for update batches (the exception is coal-to-gas conversions, where a wiki note helps future cycles — flag those in `qa`, don't stage wiki text). Applied batches move to `batches/<country-scope>/archive/`.

## §3 Data pull and worklist

Every batch starts from a fresh pull — never a cached CSV:

1. `python ../../gem-db-ops/gogpt/pull.py` — raw export from the read-only mirror. **The raw export contains ALL combustion units** — oil, gas, coal (GCPT), bioenergy (GBPT) — because the trackers share one combustion database.
2. `python pull_gem_db.py --map-only` — re-derive the column-index map from the fresh header row.
3. `python scope_filter.py` — produce the **GOGPT-scoped CSV** (oil/gas units only). This is what research works from. **Keep the unfiltered CSV** — it's needed for coal-conversion and co-located coal/gas cross-checks (§9.3).
4. `python worklist.py --country <name>` — the priority-ordered worklist:
   1. **In-development units** — `announced`, `pre-construction`, `construction` (the manual's update focus)
   2. **Shelved review** — `shelved` and `shelved - inferred 2 y` units
   3. **Units with planned retirement in the current year**
   4. **Other units with planned retirement**

   The worklist also flags **shelved-inferred-2y** and **cancelled-inferred-4y candidates**: in-development units that have disappeared from company documents with no activity for 2 / 4 years (§4.1). Units outside the worklist are left untouched unless the user scopes them in — **except on a full-country assignment**, where the ladder sets priority but coverage must be complete: after the ladder is exhausted, sweep the remaining status groups in the upstream session order (new proposals → in-development → shelved/cancelled → operating → retired/mothballed), so every unit ends the batch with a Record of Full Updates entry (§5).

5. **Cross-cutting scans** (adopted from the upstream pipeline, `upstream/gogpt-tracker/` — see CLAUDE.md "Upstream"). Bridge the fresh scoped CSV with `python export_to_dump.py`, then run from `upstream/gogpt-tracker/scripts/`:
   - `--counts-only` — the unit-counts baseline. A mismatch against the quarter's assignments tab is a discrepancy to reconcile *before* researching (upstream's Session-1 check).
   - `--ownership-scan` (operating units), `--in-progress-scan`, `--duplicate-scan` — surface stale-ownership candidates, stuck in-progress units, and likely duplicate plant entries. Fold hits into the worklist as extra rows. **Scans surface candidates only** — a scan hit gets the normal research + verification path before anything is staged; never stage directly from scan output.
   - `--possible-updates` — see the backlog rule below.

**Work the "GEM trackers – possible updates" backlog DURING country research, not after.** Filter the backlog to the country at batch start and fold its items into the worklist — researching them alongside the country pass prevents duplicate review of the same plants. The upstream loader (`gogpt_csv_query.py --possible-updates`, optionally `--pu-file` with a flattened Drive read of the live sheet) does this filtering, including dropping rows already marked done.

## §4 Update sub-types

### §4.1 Status updates

The most rule-bound sub-type. The manual's status vocabulary: `announced`, `pre-construction`, `construction`, `operating`, `mothballed`, `retired`, `shelved`, `shelved - inferred 2 y`, `cancelled`, `cancelled - inferred 4 y`.

- **Announced vs pre-construction**: announced = publicly reported but not actively moving (permits, land, financing); pre-construction = actively seeking approvals/land/financing.
- **Construction** requires physical construction of equipment or buildings — a ground-breaking ceremony or early site prep does not count.
- **Inferred statuses**: an in-development unit that disappears from company documents with no activity for **2 years** → `shelved - inferred 2 y`; for **4 years** → `cancelled - inferred 4 y`. The date of the most recent source found drives the call. Record the last-seen source and date in the Latest Activity field (staged in the `updates` lane) so the next cycle can re-run the clock.
- **Mothballed vs retired**: mothballed = deactivated (inactive >1 year) but not retired; retired = permanently decommissioned or converted to another fuel. **Mothballed units never carry a Retired Year.**
- **From-2020 rule**: mothballed/retired/cancelled units are only tracked from 2020 forward — don't research pre-2020 closures.
- **Conflict damage**: check "Disrupted due to conflict", then — destroyed or multi-year rebuild with no reconstruction underway → `mothballed`; partially damaged / likely repaired within ~1 year → `operating`; `retired` **only** with explicit confirmation the plant will never be rebuilt. Unclear damage with no sign of stoppage stays `operating`, with a Status Details note.

**Never punt a confirmed status change to a qa note.** If research establishes a transition happened, stage it in `updates` with its paired year fields and datasource — a qa record is correct only when the question is genuinely unresolved, and a "reviewer should confirm…" hedge in your own note is the signal you haven't finished the research.

### §4.2 Year fields

- **Start Year** exists in the past only for `operating`, `mothballed`, `retired` units. For **in-development** units it is a *projected* year and the **Planned checkbox must be checked** (unchecked once operational). **Shelved and cancelled units never have a Start Year** — blank the year and its reference if staging one of those statuses.
- **Retired Year** — the year the unit went offline; never on mothballed units. **Planned Retire Year** carries the Planned checkbox until the retirement actually happens.
- **Year-end cycle rule**: during the second annual update (concluding in December), no in-development or retiring unit may keep the current (ending) year as its start/retirement year without a source confirming it happened — push unconfirmed current-year dates to the following year.
- A **replaced unit** (new turbine, old one scrapped) is a retirement + a new unit (`newunits` lane, name suffixed "R"), not an edit to the old unit's start year. Maintenance/upgrades never change the start year (capacity/technology may change; retirement year may extend).

### §4.3 Value updates (capacity, ownership, fuel, technology, etc.)

- **Capacity** — nameplate/installed MW, rounded to the nearest MW; ranges take the high end. **GENERATING MW only — never shaft/mechanical-drive MW** (compressor-drive turbines are out of scope). Electrical MWe, never thermal MWt. Threshold: units (or IC-engine / aeroderivative sets) ≥50 MW; the EU and UK use a <20 MW per-unit exception. IC/aero sets stage the engine count + per-engine MW (the DB computes the total).
- **Ownership** — immediate (lowest-level) owner; SPVs are fine as-is; never the national government itself (find the owning entity within it); never a PPA offtaker. Only stakes ≥5% (smaller ones aggregate as "small shareholder(s)"); individuals as "natural person(s)"; list the four largest owners + "other" for the rest; a sole owner gets an explicit 100%. Owner in the process of acquisition/merger → note it, add to the possible-updates backlog, revisit next cycle. Operator only when it differs from the lowest-level owner.
- **Fuel / technology** — use the manual's controlled vocabularies exactly (fuel categories: fossil gas, fossil liquids, industrial by-product, other/hydrogen; technologies: CC, GT, AGT, ST, IC, ICCC, ISCC, AFC). Associated gas = "natural gas". Primary checkbox only when a unit burns more than one fuel, and only on one fuel; it's mandatory when the two fuels sit in different trackers (coal vs gas).
- **Coordinates** — WGS 84 decimal; Accuracy `exact` (≥3 decimals) or `approximate`; plant-level location, no per-unit coordinates.
- **CCS / CHP** — mostly "yes" or "not found"; "no" only when a comprehensive (e.g. government) dataset explicitly says so. Hydrogen field: do not research.
- **Fuel conversions** — a unit converting fuels (coal-to-gas most commonly) uses the timepoint convention (existing unit → ", timepoint 1"; cloned unit → ", timepoint 2") and the Conversion-of dropdown, staged as an explicit multi-step instruction in the actions workbook. Distinguish conversion (boiler/repowering of the same unit) from replacement (retire + new unit). A converted-from-coal unit must be `retired` in GCPT; its gas start year must not precede the coal retired year.

### §4.4 Datasource fills

For any populated value missing a datasource, source-search and stage the fill. **Rule F (no orphan citations)**: never stage a reference without a paired data value. **Never remove outdated datasources** — old sources document data history; reference edits are merge-never-replace (§7.3).

## §5 Field conventions

- **Blank = not yet researched. "Not found/unknown" only after actively searching the field.** Never write "unknown" into a field you didn't research; never leave blank a field you researched and came up empty on.
- **Record of Full Updates**: every worklist unit gets an entry at close-out — `updated` (data changed), `no changes` (researched, nothing changed), or `in progress` (unfinished). The actions workbook includes this as the final per-unit action.
- Optional fields (Operator, Employment Notes, Other IDs outside US/EU, Street Address, Hydrogen) are recorded when encountered, not hunted.

## §6 Confidence labeling

Cell-color convention in the actions workbook, per cell not per row:

- **Green** — primary/regulatory source (government dataset, regulator filing, owner IR) OR ≥2 independent corroborating sources agreeing on the value
- **Yellow** — single non-primary source; value implied or contested
- **Red** — single weak source. **Prefer leaving the cell blank** and logging a `qa` record instead — red signals work needed, not work done
- **Blue** — re-verified this batch, unchanged from the DB value (the "no changes" outcome at cell granularity; pairs with the manual's "no changes" Record entry)

A cell with no color means the agent searched but found no confirming source — a research gap, not a confirmation.

## §7 URL verification gate and source rules (mandatory)

### §7.1 Verification

Every URL in every lane passes `url_verifier.py` before the batch is presented — no exceptions, even for URLs that worked before:

```bash
python url_verifier.py <url> <expected_string_1> <expected_string_2> ...
```

Checks: HTTP 200, not a soft-error page (Cloudflare "Just a moment", paywall stub, soft-404), and body contains every expected string. Expected strings should include the **plant name**, the **value being cited**, and ideally the owner or country. A citation must be the **specific page** containing the value — a bare domain/homepage is never a citation. **Bot-block ≠ dead**: a 401/403/429 or interstitial means live-but-refusing-bots; the verifier falls back to the newest Wayback snapshot for the content check (a pass keeps the LIVE URL citable — never cite the web.archive.org address). Only a hard 404/410/DNS failure, or a live page without the cited value, fails; a 301/302 to a live page survives as the redirect target.

### §7.2 Source rules (family-wide, non-negotiable)

- **Never cite gem.wiki or globalenergymonitor.org**, and never cite republishers whose data is GEM-derived (anti-circularity — GEM data must never source itself).
- **abarrelfull is banned** as a source in any lane.
- **Every staged value needs ≥2 independent working URLs, each explicitly containing the value.** One primary/regulatory source may stand alone only under the green rules in §6, but two independent sources is the default bar.
- **Mirrors/syndications of one document count as ONE source** — a press release and three wire re-publishings of it are one source, not four.
- **URLs live only in reference/datasource columns** — never embedded in value, name, or notes fields.

### §7.3 Reference edits use MERGE semantics — never drop a surviving URL

An edit to a reference/datasource field carries forward **every still-valid existing URL** plus any new ones: new value = (surviving existing URLs, original order) + (new URLs). Reference edits only ever (a) fix genuinely dead/wrong URLs or (b) add corroboration — never swap a good existing citation for the agent's own find. An existing URL may be dropped ONLY if proven dead per §7.1 (a bot-block that fails even the Wayback check goes to `qa`, not a silent drop), and the drop is declared in the staged record's `dropped_urls_dead` key. This also honors the manual's rule to keep outdated datasources for data-history purposes.

## §8 Entity discipline

GEM's owner/operator entity system is shared across all trackers; duplicate entities are real cleanup work. Before staging any new Owner/Operator/Parent:

1. `python entity_lookup.py "<entity name>" --remote` — run it **bare (no country filter)**; entities are shared across countries and trackers.
2. Match found anywhere → use the existing entity ID; do NOT stage a new entity.
3. No match locally or remotely → stage in the `entity` lane with the lookup attempts logged. The human creates the entity via the web UI ("Adding a New Owner" flow in the manual) before applying the dependent edits.
4. Check spelling variants deliberately — the manual's canonical warning is the same entity under a slightly different spelling.
5. **Parent findings are never unit edits.** `Parent(s)` is a computed column
   (derived from `company.gemParents`, the ownership-tracker team's curated
   chain — see `gem_db_schema.md`); the build script rejects it as an edit
   target. Stage a parent correction as a `qa` record (`concern_type:
   attribution`) recommending the entity-record change, with the verified
   sources in `researcher_notes`.

## §9 Project-level vs unit-level edits

1. **Project-level field edits** (plant name, country, location, plant-level owner/operator, captive fields) **apply to ALL unit rows of the plant**. The actions workbook shows the edit once with a "project-level: applies to N unit rows" note.
2. **Unit-level field edits** apply only to the target unit ID.
3. **Co-located coal + gas plants** share one Project ID and one wiki URL; only the gas/oil units are GOGPT rows. Cross-check the **unfiltered** export (§3.3) before editing project-level fields at such plants — the coal rows are affected too, and coordination with GCPT researchers applies. Gas unit names must never reuse coal unit numbers.

## §10 Mechanical QC before build

`python qc_checks.py` validates every staged record against the manual's rules before `build_review_package.py` runs:

- capacity ≥50 MW (with the EU/UK <20 MW per-unit exception)
- Start Year blank for shelved/cancelled units
- no Retired Year on mothballed units
- Planned-checkbox logic on start/retire years (checked while projected, cleared once actual)
- fuel category/detail and technology values inside the controlled vocabularies
- ownership shares (≥5% rule, sums, four-plus-other structure)

Fix every failure before building; a deliberate exception gets a `qa` record explaining it.

## §11 Workflow (linear)

1. Confirm scope with the user; mark the roster row `in progress`; create `batches/<country-scope>/{staging,deliverables,archive}` with a `meta.json`
2. Fresh pull chain: `python ../../gem-db-ops/gogpt/pull.py` → `python pull_gem_db.py --map-only` → `python scope_filter.py` (§3)
3. `python worklist.py --country <name>` → priority-ordered worklist + inferred-status flags
4. `python export_to_dump.py`, then the upstream cross-cutting scans — counts baseline, ownership / in-progress / duplicate — folding hits into the worklist, and pull the country's "GEM trackers – possible updates" items in via `--possible-updates` (§3.5)
5. For each worklist unit, in priority order: source-search (start from `docs/country_notes/` and the manual's country resources), apply §4 rules, stage records into the lanes, color per §6
6. `python url_verifier.py` on every staged URL (§7.1); re-verify pre-existing URLs on touched rows
7. `python entity_lookup.py` for every new entity reference (§8)
8. `python qc_checks.py` on the staging dir (§10) — fix failures
9. `python build_review_package.py --inputs-dir batches/<country-scope>/staging --mode update` → actions + evidence workbooks in `deliverables/` (Eastern timestamp via `TZ=America/New_York date "+%Y%m%d_%H%M_ET"`)
10. `python recalc.py` → confirm zero formula errors in both workbooks
11. Present the deliverables; the human applies the actions workbook by hand in the web UI

## §12 Country close-out

When the human has applied the batch, the country isn't done until:

- Every worklist unit has a Record of Full Updates entry — `updated` or `no changes` (§5)
- Unit counts re-run on a freshly bridged dump (`--counts-only`) and reconciled against the assignments tab — the close-out counts must be explainable by the batch's own staged changes
- Assigned Comments in the database are reviewed and resolved
- The country's "GEM trackers – possible updates" items are cleared (researched + annotated with initials/date/notes)
- Country Tips are updated with anything learned (mirror durable findings into `docs/country_notes/`)
- The GC/Country Checklist is completed
- The **DB Validation Report** for the country is run (Projects tab → country search → "GOGPT Validation Report") and errors resolved — validation errors on co-located coal/gas project fields or coal-to-gas-conversion unit fields are **low priority / optional**
- A time estimate for the next cycle is logged in the roster's notes
- The roster row moves to `done`; the PM reviews and may flag fields — process flags as a small follow-up batch

## §13 Hard rules (these override anything below)

- **Never modify the live GEM database.** Outputs are always the two-workbook deliverable for human application in the web UI.
- **Every URL passes the §7.1 verification gate** — no exceptions.
- **Never cite gem.wiki / globalenergymonitor.org / GEM-derived republishers; abarrelfull is banned** (§7.2).
- **≥2 independent working URLs, each explicitly containing the value; mirrors of one document = one source** (§7.2).
- **Reference edits merge, never replace; no orphan citations; URLs only in reference columns** (§7.2–§7.3, §4.4).
- **Fresh pull chain at the start of every batch**, column map re-derived (§3).
- **Project-level field changes apply to ALL unit rows** — and check the unfiltered CSV at co-located coal/gas plants (§9).
- **Start Year never on shelved/cancelled; Retired Year never on mothballed; Planned-checkbox logic enforced** (§4.2, `qc_checks.py`).
- **Generating MW only — never shaft/mechanical-drive MW; never thermal MWt** (§4.3).
- **Don't create duplicate entities** — `entity_lookup.py` before staging any new owner/operator (§8).
- **Blank = not researched; "not found/unknown" only after searching** (§5).
- **`qc_checks.py` passes before every build** (§10).

## §14 Pause-and-ask triggers

Stop and consult the user when:

- A whole class of GEM values looks systematically wrong (suggests methodology misunderstanding or schema drift)
- Corroboration is too thin for even yellow on a key field after primary + secondary sources are exhausted
- A capacity update would change a plant total by more than ~20%
- An ownership update would change the controlling owner (verify with filings before staging)
- A unit's fuel-assignment is ambiguous between trackers (coal/gas primary-fuel judgment call — the manual says coordinate with GCPT)
- A unit's existing URLs all fail re-verification and no replacements exist (project may be dormant — candidate for the inferred-status clock, but confirm first)
- `entity_lookup.py` finds no match for an entity that obviously should exist

---

## Quick-reference card

| Sub-type | Primary action | Required scripts |
|---|---|---|
| Status update | Stage status + paired year/checkbox changes | `worklist.py`, `url_verifier.py`, `qc_checks.py`, `build_review_package.py` |
| Value update | Capacity/owner/fuel/technology edits | `url_verifier.py`, `entity_lookup.py`, `qc_checks.py`, `build_review_package.py` |
| Datasource fill | Add references to unreferenced values (merge semantics) | `url_verifier.py`, `build_review_package.py` |
| Inferred-dormancy sweep | Process 2y/4y flags from `worklist.py` | `worklist.py`, `url_verifier.py`, `build_review_package.py` |

| Color | Meaning | When to use |
|---|---|---|
| Green | Primary/regulatory or ≥2 independent | Government dataset, regulator filing, owner IR |
| Yellow | Single non-primary | Single trade-press article |
| Red | Single weak source | Prefer blank + `qa` record |
| Blue | Re-verified, unchanged | The "no changes" outcome at cell level |
| (none) | Searched, nothing found | Research gap, not confirmation |

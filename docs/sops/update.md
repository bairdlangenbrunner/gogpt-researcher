# GOGPT Update SOP

Last revised: 2026-10-02 (rev 3 — evidence bar: one fully validated ref suffices, 2+ preferred; status changes still need 2+ for green; rev 2 2026-08-04 — adopted the upstream pipeline's cross-cutting scans, counts baseline, and status-group coverage sweep; rev 1 2026-07-27 was the initial GOGPT adaptation from lng-terminals-researcher rev 2)

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

1. **Actions workbook** — a per-plant / per-unit edit checklist: current value → proposed value → evidence. This is what the human works through, applying each edit **by hand in the gem-project-db.herokuapp.com web UI**, or having Claude type the accepted edits in through Claude in Chrome with Baird approving every save (`database-browser-edits.md`). No script in this repo ever writes to the live database.
2. **Evidence workbook** — the audit trail: every staged record with its sources, verification results, confidence color, and researcher notes.

Both are built by `build_review_package.py` from the staged JSON lanes in `batches/<country-scope>/staging/`. The lanes are `updates | qa | entity | monitor | newplants | newunits`. There is **no wiki lane** — GOGPT wiki pages are auto-generated from the database; only the "Background" section is ever hand-edited, and wiki work is generally out of scope for update batches (the exception is coal-to-gas conversions, where a wiki note helps future cycles — flag those in `qa`, don't stage wiki text). Applied batches move to `batches/<country-scope>/archive/`.

## §3 Data pull and worklist

Every batch starts from a fresh pull — never a cached CSV:

1. `python ../../gem-db-ops/gogpt/pull.py --output gem_export_gogpt.csv` (from `scripts/`; without `--output` the pull lands in gem-db-ops and research keeps reading the old file) — raw export from the read-only mirror. **The raw export contains ALL combustion units** — oil, gas, coal (GCPT), bioenergy (GBPT) — because the trackers share one combustion database.
2. `python pull_gem_db.py --map-only` — re-derive the column-index map from the fresh header row.
3. `python scope_filter.py` — produce the **GOGPT-scoped CSV** (oil/gas units only). This is what research works from. **Keep the unfiltered CSV** — it's needed for coal-conversion and co-located coal/gas cross-checks (§9.3).
4. `python worklist.py --country <name>` — the priority-ordered worklist:
   1. **In-development units** — `announced`, `pre-construction`, `construction` (the manual's update focus)
   2. **Shelved review** — `shelved` and `shelved - inferred 2 y` units
   3. **Units with planned retirement in the current year**
   4. **Units with planned retirement in any other year**
   5. **The rest** (the manual's ladder; mothballed and operating units come last)

   The worklist also flags **shelved-inferred-2y** and **cancelled-inferred-4y candidates**: units that have disappeared from company documents with no activity for 2 years (shelved-inferred) or 4 years (cancelled-inferred, tested only on announced, pre-construction and construction units), counted from the Latest Activity date, not the calendar year (§4.1). Units outside the worklist are left untouched unless the user scopes them in — **except on a full-country assignment**, where the ladder sets priority but coverage must be complete: after the ladder is exhausted, sweep the remaining status groups in the upstream session order (new proposals → in-development → shelved/cancelled → operating → retired/mothballed), so every unit ends the batch with a Record of Full Updates entry (§5).

5. **Cross-cutting scans** (adopted from the upstream pipeline, `upstream/gogpt-tracker/` — see CLAUDE.md "Upstream"). Bridge the fresh scoped CSV with `python export_to_dump.py`, then run from `upstream/gogpt-tracker/scripts/`:
   - `--counts-only` — the unit-counts baseline. A mismatch against the quarter's assignments tab is a discrepancy to reconcile *before* researching (upstream's Session-1 check).
   - `--ownership-scan` (operating units), `--in-progress-scan`, `--duplicate-scan` — surface stale-ownership candidates, stuck in-progress units, and likely duplicate plant entries. Fold hits into the worklist as extra rows. **Scans surface candidates only** — a scan hit gets the normal research + verification path before anything is staged; never stage directly from scan output.
   - `--possible-updates` — see the backlog rule below.

6. **Validation report** (QC/Country checklist row 7). `python validation_report.py --country <name>` (or `--state <State>`) reads the database's own validation errors for the scope's oil and gas plants, live from the read-only DB, and sorts each one: *fix* (research can clear it: a value with no data source, a blank required value, a status step with no date, a broken replacement link), *exception* (the manual's optional coal cases, M198 and M220: a project-level error on a plant that also has coal units, a unit-level error on a coal-to-gas conversion, and an error on a coal unit with no oil or gas fuel), or *person* (a web-UI click: plant-name rules, hydrogen data sources, and any error on a unit with no fuel at all, usually a blank unit to delete or fill in). The fixes go into the batch: `build_state_brief.py --validation work/validation_<tag>.json` puts each on its unit's brief, marked **[Validation report]**, and a hand-worked batch treats `work/validation_<tag>.md` as extra worklist rows. Person items go to the human in the evidence file. **Every fix and person item must be answered before the build** (Baird 2026-10-16), and an exception item may be answered "optional under the manual": an edit that clears it, or a question with `concern_type` `validation` that gives the answer (or says what was searched and not found), each carrying check 7 on the unit, a sibling unit or the plant. `state_gate.py` (gate `validation`) fails the batch on any unanswered item, and on a validation file over a day old, so rerun `validation_report.py` right before the gate. Edits the human already made by hand in the web UI since the batch was staged go to `staging/applied_in_db.json` (with an `applied` note), out of the lane files, so the gate and the workbook do not show them again; a moved record that carried check 7 still counts as that item's answer (the gate reads `applied_in_db.json` too, since 2026-10-22).

7. **ID matching, US states only** (QC/Country checklist row 38). `python match_ids.py --state <State>` joins every GEM plant and unit to the EIA-860M generator file, the EIP (Oil and Gas Watch) sheet and the Sierra Club GEM-IDs-matched list and writes `work/ids_us-<st>.json` + `.md`. What it finds goes three ways: a confident missing code (an `EIA: <plant id>` or `EIP: <facility id>` in Other IDs (location), an `EIA: <generator id>` in Other IDs (unit)) is listed for the human to type into the web UI, since an ID has no Data Source and is never staged; a disagreement on status, capacity or a year becomes a research task on the brief (`build_state_brief.py --ids`); an EIP or Sierra Club row whose GEM ID columns are blank is listed with the GEM IDs for Baird to paste into that sheet. The Sierra Club list is reference only: it points at what to check, it is never cited and never leaves GEM. EIA's own codes are a public fact and the EIA-860M file is a normal citation.

8. **Utility resource plans, US states only** (QC/Country checklist rows 34 and 37). `python irp_sheet.py --state <State>` reads the "US IRPs" tab of the Update sheet (one row per utility with the plan year, plan links and a running Notes log) through the read-only work profile, matches each utility to the state's GEM plants, reads the export's `IRP` column (the database's IRP checkbox) for the units already ticked, and writes `work/irp_us-<state-slug>.json` + `.md`. `build_state_brief.py --irp` puts a whole-plant task on each matched plant that a plan can plausibly move and writes `briefs/_irp.md` for the scope-wide agent, which reads every listed plan for new gas resources: a gas project in a plan is added as a new plant or unit, and a draft plan is enough (Baird 2026-10-07). The assembler flags each record sourced from a plan `irp: true`. The build's `--irp` adds the `irp_box` sheet (which units need the IRP box ticked in the web form, which are already ticked, which are new rows) and `irp_notes_draft` (a dated Notes line per utility to paste onto the tab by hand; the repo never writes the tab). The tab's saved values hold a colleague's working notes and stay under `work/`.

9. **Captive power at LNG terminals and data center power, every scope** (QC/Country checklist rows 6, 39 and 44). `python captive_lng.py --state <State>` (or `--country <name>`) reads the LNG team's captive LNG workbook and the LNG tracker download it was built from (both through the read-only work profile, cached a week under `work/captive/`), joins the sheet's rows to the tracker by Terminal ID (the tracker's Project ID), keeps the scope's rows and matches each to GEM's plants (the tracker's captive plant ID column first, then a plant name with LNG in it, then location), and writes `work/captive_<tag>.json` + `.md`. `build_state_brief.py --captive` puts a whole-plant task on each matched plant (check the capacity, status, start year, technology and captive fields against the sheet's sources) and writes `briefs/_captive.md` for the scope-wide agent: the qualifying terminals GEM lacks are new-plant candidates, and GEM LNG plants with no sheet row are reported back to the LNG team. **The workbook is a lead list**: its Qualifying rows are checked first, but any verified captive LNG plant at the add threshold (50 MW, 20 MW in the EU and UK) is an add, named "XYZ LNG terminal power station" when it has no name of its own, with the terminal in Project Links. Capacity is electrical nameplate only: a row the sheet qualifies on compressor-drive turbines (mechanical drive) is flagged, and the agent has to find generator sets at the threshold before adding anything. Both workbooks hold a colleague's working notes and stay under `work/`.

    **Data centers, every scope** (Baird 2026-10-27). Run `python data_center_fleets.py --state <State>` (or `--country <name>`) right after the permit harvest and before `build_state_brief.py`. It writes `scopes/<tag>/work/permits/_data_centers.md` and `.json`: one row per data center site with the generators summed in electrical MW. `build_state_brief.py --data-centers` briefs the sites. A backup engine fleet is a plant like any other: at the summed nameplate threshold (50 MW, 20 MW in the EU and UK) it is an add, and capacity unknown means add with capacity blank. A gas-fired data center plant is an add too, with no hold. Every site at or above the threshold, or with generators and unknown capacity, is answered in `coverage.json` under `data_centers` (add, already in GEM, update, below the threshold with the sum, or no generators), and `state_gate.py` gate `data-centers` enforces it. When the scope's data center work ran as its own catch-up batch (`us-il-dc` beside `us-il`), the statewide batch copies those answers and each `add` names the catch-up folder in `batch`, so the gate finds the record there. A `no_documents` or `nothing_found` answer is true only once the scope's permit record system (the `permit_record` entry of `scopes/<tag>/coverage.json`) was searched by the operator's name and the site's address; the public notice feed is not enough, because a data center's generator permit rarely goes to notice (Illinois, 2026-10-30). Never write "backup only" without the summed nameplate beside it. How to enter one: name it "<Operator> <Place> Data Center power station"; one unit row per permit phase or building group, or one unit when the permit does not split the fleet; internal combustion, with Number Of Engines and Capacity Per Engine from the permit; Captive industry type data center, Captive industry use power, Captive non-industry use none, Backup Power yes, all at unit level; the data center named in Project Links; Captive Data Source the permit.

10. **Interconnection queues, US states only** (Baird 2026-10-30). Run `python pull_queues.py --state <ST>` after the permit harvest; its settings are `scopes/us-<st>/queues.json` (markets, the state's transmission owners, name patterns for known plants), and a state with no settings file gets one before its first sweep. It writes `batches/<tag>/harvest/queues.json` and `.md`, which `build_state_brief.py --harvest` puts on the briefs, with a completeness line per source (rows read, the state's rows, gas or oil, fuel not shown, and SHORT when a file came back far smaller than usual). Every request in its `needs_answer` list is answered in `coverage.json` under `queues` (Discovery SOP §3.1), and `state_gate.py` gate `queues` enforces it.

**Work the "GEM trackers – possible updates" backlog DURING country research, not after.** Filter the backlog to the country at batch start and fold its items into the worklist — researching them alongside the country pass prevents duplicate review of the same plants. The upstream loader (`gogpt_csv_query.py --possible-updates`, optionally `--pu-file` with a flattened Drive read of the live sheet) does this filtering, including dropping rows already marked done.

### §3.1 Cycle priorities — Q4 2026

Read the cycle's kickoff doc (link hub: `docs/reference/sop_pointers.md`, "Current cycle") at batch start; the standing ladder above is unchanged, but the cycle adds emphasis and one required deliverable:

1. **Newly announced plants** (discovery lane, folded into the country pass) and the **in-development review**.
2. **Shelved / cancelled review** — record Latest Activity (stalled projects: the newest source and the date it last mentioned the unit; `docs/reference/lifecycle_rules.md`), Shelved Year, Cancelled Year when a unit is moved.
3. **Retirements and planned retirements** — enter as timeline milestones / scheduled events (§4.1, §4.2).
4. **In-development units with no start year** — a start year is expected; leave blank only after a search.
5. **Turbine make/model for in-development units** — enter "not found" only after actually searching.
6. **REQUIRED: operating units with unknown start year** — re-research, ≤10 min/unit, decade midpoint + internal note when only the decade is known (`lifecycle_rules.md` "Start year rules").

The assignments tab gives each country / US state a **priority level** (high / medium / low, by in-development capacity). It scales how deep the "country tips" and discovery effort goes — it never reorders the unit ladder. A **Country tips trends** row for this cycle is required output for every country closed out.

**United States scopes are per state.** `worklist.py` filters on `--country "United States"` only; until a `--state` filter lands, subset the scoped CSV on `State/Province` (full state name, e.g. `Texas`) before running the worklist and cross-cutting scans. US-only rules (ID matching, IRP checkbox) are in `docs/country_notes/united_states.md`; state source ladders under `docs/country_notes/united_states/`.

## §4 Update sub-types

### §4.1 Status updates

The most rule-bound sub-type. The manual's status vocabulary: `announced`, `pre-construction`, `construction`, `operating`, `mothballed`, `retired`, `shelved`, `shelved - inferred 2 y`, `cancelled`, `cancelled - inferred 4 y`.

- **Announced vs pre-construction**: announced = publicly reported but not actively moving (permits, land, financing); pre-construction = actively seeking approvals/land/financing.
- **Construction** requires physical construction of equipment or buildings — a ground-breaking ceremony or early site prep does not count.
- **Inferred statuses**: an in-development unit that disappears from company documents with no activity for **2 years** → `shelved - inferred 2 y`; for **4 years** → `cancelled - inferred 4 y`. The date of the most recent source found drives the call. Record the last-seen source and date in the Latest Activity field (staged in the `updates` lane) so the next cycle can re-run the clock; the manual (M691) uses the field for in-development units that are not progressing, and the working reading of "for some time" is one year for shelved and inferred units. Never for operating, mothballed, retired or plainly cancelled units (`docs/reference/lifecycle_rules.md`). **An inferred status is a milestone entry with a datasource**: the Latest Activity source, with the milestone year equal to the Latest Activity date plus two years (shelved) or four years (cancelled), per M637.
- **Mothballed vs retired**: mothballed = deactivated (inactive >1 year) but not retired; retired = permanently decommissioned or converted to another fuel. **Mothballed units never carry a Retired Year.**
- **From-2020 rule**: mothballed/retired/cancelled units are only tracked from 2020 forward — don't research pre-2020 closures.
- **Conflict damage**: check "Disrupted by conflict", then — destroyed or multi-year rebuild with no reconstruction underway → `mothballed`; partially damaged / likely repaired within ~1 year → `operating`; `retired` **only** with explicit confirmation the plant will never be rebuilt. Unclear damage with no sign of stoppage stays `operating`, with a Status Details note.

**Never punt a confirmed status change to a qa note.** If research establishes a transition happened, stage it in `updates` with its paired year fields and datasource — a qa record is correct only when the question is genuinely unresolved, and a "reviewer should confirm…" hedge in your own note is the signal you haven't finished the research.

### §4.2 Year fields

- **Start Year** exists in the past only for `operating`, `mothballed`, `retired` units. For **in-development** units it is a *projected* year — under the 2026 status-timeline model it is entered as a **scheduled `operating` event** (Event Year is the projected year, Source Year is the year the source reported it, plus the source), not by overwriting a field; the staged `Start year` carries the Event Year and the action tells the human to add a new scheduled event entry, never to change an existing one; a pushed-back year is a new scheduled event, never an edit of the old one (`lifecycle_rules.md` "How status edits are entered"). **Shelved and cancelled units never have a Start Year** — blank the year and its reference if staging one of those statuses.
- **Operating units with an unknown Start Year** are a required Q4 2026 deliverable: ≤10 min of research per unit; decade known → midpoint year + internal note ("decade estimate"). Stage the note text alongside the year.
- **Retired Year** — the year the unit went offline; never on mothballed units. A planned retirement is a scheduled `retired` event the same way (Event Year, Source Year); there is no Planned checkbox. A maintenance change that moves the retirement date is a new scheduled retirement event, never a new operating milestone. Shelved and cancelled units get no scheduled operating event, and earlier ones stay as history. Every scheduled event has an Event Year.
- **Year-end cycle rule**: during the second annual update (concluding in December), an in-development or retiring unit with a scheduled event in the ending year and no source confirming it happened gets a new scheduled event with the following year as Event Year and the current year as Source Year (M192). The existing entry is never edited.
- A **replaced unit** (new turbine, old one scrapped) is a retirement + a new unit (`newunits` lane, name suffixed "R"), not an edit to the old unit's start year. Maintenance/upgrades never change the start year (capacity/technology may change; retirement year may extend).

### §4.3 Value updates (capacity, ownership, fuel, technology, etc.)

- **Capacity** — nameplate or installed electrical capacity in MW (M603), never the lower operational figure; record the figure the source gives, at most one decimal (rounding to the whole MW is allowed, never required); ranges take the high end. **Never shaft/mechanical-drive MW** (compressor-drive turbines are out of scope), never thermal MWt. Threshold: units (or IC-engine / aeroderivative sets, summed) ≥50 MW; the EU and UK threshold is 20 MW (the manual's "<20MW per unit" reads as a typo; whether 20 MW applies per engine or to the summed set is asked of Dan O'Beirne, and the repo sums meanwhile). Number Of Engines and Capacity Per Engine are staged for internal combustion sets and aeroderivative gas turbine sets (the DB computes the total); a frame gas turbine is one turbine per unit with its capacity in Capacity (MW). Captive fields are filled for every captive plant, including one that exports; Captive non-industry use records the export (power, heat, both, none).
- **Ownership** — immediate (lowest-level) owner; SPVs are fine as-is; never the national government itself (find the owning entity within it); never a PPA offtaker. Only stakes ≥5% (smaller ones aggregate as "small shareholder(s)"); individuals as "natural person(s)"; list the four largest owners + "other" for the rest; a sole owner gets an explicit 100%. Owner in the process of acquisition/merger → the pending acquisition goes in Notes (additive, newest on top) and on the "GEM trackers – possible updates" sheet (M322); revisit next cycle. Equal-share owners are entered as equal shares; an unknown owner is entered as "unknown"; a vague proposal with no owner leaves the owner blank. Operator only when it differs from the lowest-level owner.
- **Fuel / technology** — use the manual's controlled vocabularies exactly (fuel categories: fossil gas, fossil liquids, industrial by-product, other/hydrogen; technologies: CC, GT, AGT, ST, IC, ICCC, ISCC, AFC). Associated gas = "natural gas". Primary checkbox only when a unit burns more than one fuel, and only on one fuel; it's mandatory when the two fuels sit in different trackers (coal vs gas).
- **Coordinates** — WGS 84 decimal; Accuracy `exact` (≥3 decimals) or `approximate`; plant-level location, no per-unit coordinates. A plant whose accuracy is `approximate` or whose coordinates are blank goes through the location ladder in `docs/reference/location.md` (address or site sentence, geocode, satellite look, then an official map georeferenced); an `exact` plant's coordinates are never reopened. A proposed plant with only a city gets an approximate point in an open area near that city, Location Data Source the Google Maps link plus the source that named the city. Every coordinate a person reads is a Google Maps link, and one source is enough for the Location box: a document with the specific street address, a Maps link to the exact project, or an EIA document (Baird 2026-10-21). City, Local area, Major area and Subnational are filled when blank on every plant in scope, exact plants included (Local area and Major area without "county", "township" or "district", one nearest city, city-states repeated in City and Subnational); any City, county or street change goes on the single Location card with the point.
- **CCS / CHP** — mostly "yes" or "not found"; "no" only when a comprehensive (e.g. government) dataset explicitly says so. Hydrogen field: do not research.
- **Fuel conversions** — a unit converting fuels (coal-to-gas most commonly) uses the timepoint convention (existing unit → ", timepoint 1"; cloned unit → ", timepoint 2") and the Conversion-of dropdown, staged as an explicit multi-step instruction in the actions workbook. Distinguish conversion (boiler/repowering of the same unit) from replacement (retire + new unit). A converted-from-coal unit must be `retired` in GCPT; its gas start year must not precede the coal retired year.

### §4.4 Datasource fills

For any populated value missing a datasource, source-search and stage the fill. **Rule F (no orphan citations)**: never stage a reference without a paired data value. **Never remove outdated datasources** — old sources document data history; reference edits are merge-never-replace (§7.3).

## §5 Field conventions

- **Blank = not yet researched. "Not found/unknown" only after actively searching the field.** Never write "unknown" into a field you didn't research; never leave blank a field you researched and came up empty on.
- **Record of Full Updates**: every worklist unit gets an entry at close-out — `updated` (data changed), `no changes` (researched, nothing changed), or `in progress` (unfinished). The actions workbook includes this as the final per-unit action. A new unit's research status is `added`. At the end of the cycle, filter the country's leftover `in progress` units in the database and set each to `updated` or `no changes` (M191).
- **Project Links** records the names of related projects: the LNG terminal for an LNG power station, the data center for a plant that supplies one (M378). **Plant names**: "XYZ Data Center power station" or "XYZ LNG terminal power station" when the plant has no name of its own (M237).
- Optional fields (Operator, Employment Notes, Other IDs outside US/EU, Hydrogen) are recorded when encountered, not hunted. Street Address is never entered in a cell; it is hunted only as a tool for the precise point (approximate-location plants and new stations), then named in the staged note and reported to the reviewer (Baird 2026-10-21).

## §6 Confidence labeling

Cell-color convention in the actions workbook, per cell not per row:

- **Green** — one fully validated ref: it clears `url_verifier.py`, names this plant/unit, and states the value (see `docs/reference/confidence_tiers.md`). A second independent source is preferred, never required (Baird 2026-10-02, adopting the pipelines-researcher ruling of 2026-09-30). **Exception: a status change is green only on 2+ independent publishers.**
- **Yellow** — a single-source status change; or a ref that validates only partially (e.g. names the plant but the value is implied, or the value is contested)
- **Red** — single weak or unvalidated ref (doesn't name the plant, value not on the page). **Prefer leaving the cell blank** and logging a `qa` record instead — red signals work needed, not work done
- **Blue** — re-verified this batch, unchanged from the DB value (the "no changes" outcome at cell granularity; pairs with the manual's "no changes" Record entry)

A cell with no color means the agent searched but found no confirming source — a research gap, not a confirmation.

## §7 URL verification gate and source rules (mandatory)

### §7.1 Verification

Every URL in every lane passes `url_verifier.py` before the batch is presented — no exceptions, even for URLs that worked before:

```bash
python url_verifier.py <url> <expected_string_1> <expected_string_2> ...
```

Checks: HTTP 200, not a soft-error page (Cloudflare "Just a moment", paywall stub, soft-404), and body contains every expected string. Expected strings should include the **plant name**, the **value being cited**, and ideally the owner or country. A citation must be the **specific page** containing the value — a bare domain/homepage is never a citation. **Bot-block ≠ dead**: a 401/403/429 or interstitial means live-but-refusing-bots. The verifier fetches through the shared ladder in `scripts/fetch.py` (curl → on a plain 429, wait and retry with growing pauses, because that is a rate limit and a disguise does not help → `curl_cffi` browser-fingerprint impersonation on any 401/403 or a 429 that outlasts the retries → real-Chrome clearance cookie for JavaScript challenges, via `cf_clearance.py` → a full page load in real Chrome when a 401/403/406/429 or wall page survives all of that (note `browser_render`); hosts that needed any of these are remembered in `work/fetch_routes.json` and start on the step that worked; hosts known to throttle, such as the German permit register, get one request at a time across all agents and a 30-day local copy in `work/fetch_cache/`; sec.gov gets SEC's required declared-identity User-Agent, `GEM_SEC_UA` overrides it), and only then falls back to up to three distinct Wayback snapshots, newest first, for the content check (a pass keeps the LIVE URL citable; a web.archive.org snapshot address is also always citable, Baird 2026-10-22; a refused or offline archive lookup reports "try again later", never a verdict). A dead page (404/410, no connection, 5xx) also gets the archive check: the live URL still fails, and the reason names the archived copy that shows the value. **Cite that web.archive.org snapshot address** (run `url_verifier.py` on the snapshot address itself; it passes when the page shows the value) in the Data Source box, and say in the note that it is a saved copy. A free sign-in wall (energate's full text) is passed by a person signing in once with `python scripts/cf_clearance.py --login <url>`; creating the account is the user's call. When one host still refuses, look for the same document re-posted elsewhere (permit authority, gazette, town, regulator, trade press) by searching its exact file name or title; the copy is a full citation, and copies of one document count as one source. Every failure class and what to do about it: `docs/reference/site_access.md`; `python scripts/access_audit.py <batch dir> --retry` re-runs a batch's failed checks and tables them by host. A WebFetch failure is never a verdict: `python scripts/fetch.py <url> --head 3000` is the ad-hoc route, and its `notes:` line names what worked. `LNGCT_NO_BROWSER=1` forbids the Chrome step for unattended runs. Only a hard 404/410/DNS failure, or a live page without the cited value, fails; a 301/302 to a live page survives as the redirect target.

**Dead needs the full ladder.** No shard, agent or batch may mark a URL `dead` (or `blocked`) after one failed fetch. Run the whole escalation ladder in `scripts/fetch.py` (`docs/reference/site_access.md`), then look the exact address up in the Wayback Machine (the availability API and the CDX index), and only when every route fails record it as dead, with a note that lists each step tried. Any snapshot that shows the value is cited under §7.2. A 429 from the archive means wait and retry.

### §7.2 Source rules (family-wide, non-negotiable)

- **Never cite gem.wiki or globalenergymonitor.org**, and never cite republishers whose data is GEM-derived (anti-circularity — GEM data must never source itself).
- **abarrelfull is banned** as a source in any lane.
- **One fully validated working URL is sufficient for a staged value; a second independent source is preferred but never required** (Baird 2026-10-02, adopting the pipelines-researcher ruling of 2026-09-30). Take the second when it is cheap (document already open, one quick search) and set `independent`; never hold a unit open or spend another search for it. **A status change needs 2+ independent publishers for green; single-source = yellow.**
- **Mirrors/syndications of one document count as ONE source** — a press release and three wire re-publishings of it are one source, not four.
- **URLs live only in reference/datasource columns** — never embedded in value, name, or notes fields.

### §7.3 Reference edits use MERGE semantics — never drop a surviving URL

An edit to a reference/datasource field carries forward **every still-valid existing URL** plus any new ones: new value = (surviving existing URLs, original order) + (new URLs). Reference edits only ever (a) fix genuinely dead/wrong URLs or (b) add corroboration — never swap a good existing citation for the agent's own find. An existing URL may be dropped ONLY if proven dead per §7.1 (a bot-block that fails even the Wayback check goes to `qa`, not a silent drop), and the drop is declared in the staged record's `dropped_urls_dead` key. This also honors the manual's rule to keep outdated datasources for data-history purposes.

## §8 Entity discipline

GEM's owner/operator entity system is shared across all trackers; duplicate entities are real cleanup work. Before staging any new Owner/Operator/Parent:

1. `python entity_lookup.py "<entity name>" --pg` — run it **bare (no country filter)**; entities are shared across countries and trackers.
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

- capacity ≥50 MW (20 MW in the EU and UK)
- Start Year blank for shelved/cancelled units
- no Retired Year on mothballed units
- scheduled-event logic on projected start/retire years (Event Year and Source Year, never a Planned checkbox; no scheduled operating event on shelved or cancelled units)
- fuel category/detail and technology values inside the controlled vocabularies
- ownership shares (≥5% rule, sums, four-plus-other structure)

Fix every failure before building; a deliberate exception gets a `qa` record explaining it.

## §11 Workflow (linear)

1. Confirm scope with the user; mark the roster row `in progress`; create `batches/<country-scope>/{staging,deliverables,archive}` with a `meta.json`
2. Fresh pull chain: `python ../../gem-db-ops/gogpt/pull.py --output gem_export_gogpt.csv` → `python pull_gem_db.py --map-only` → `python scope_filter.py` (§3)
3. `python worklist.py --country <name>` → priority-ordered worklist + inferred-status flags
4. `python export_to_dump.py`, then the upstream cross-cutting scans — counts baseline, ownership / in-progress / duplicate — folding hits into the worklist, and pull the country's "GEM trackers – possible updates" items in via `--possible-updates` (§3.5); `python validation_report.py --country <name>` and fold its fixes into the worklist (§3.6); after the permit harvest run `python data_center_fleets.py --country <name>` and answer every site in `coverage.json` under `data_centers` (§3.9); `python check_existing_links.py --country <name>` checks every Data Source link already in the export, stages a saved-copy record for each dead link whose Wayback copy still states the value, and lists the rest as tasks (rerun it after any step that rewrites `staged_updates.json`)
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
- Assigned Comments in the database are reviewed and resolved: `python assigned_comments.py --state <State>` (or `--country <name>`) lists every comment thread on the scope's plants from the read-only database (`thread` and `comment` tables) into `work/comments_<tag>.md`, open threads first; run it at batch start so open threads become tasks, and at close-out `--closeout` must print COMMENTS CLEAN. Comment text is a colleague's words and stays under `work/`
- The country's "GEM trackers – possible updates" items are cleared (researched + annotated with initials/date/notes)
- Country Tips are updated with anything learned (mirror durable findings into `docs/country_notes/`)
- The GC/Country Checklist is completed — including the cycle-doc items (Country tips trends row for this cycle; assignments-tab status columns) and, for US states, the USA-only block (`docs/sops/qc.md` §6)
- The **DB Validation Report** for the country is clean (checklist row 54): after the human's apply (it reads the live DB, no pull needed), `python validation_report.py --country <name> --closeout` prints CLOSE-OUT CLEAN. Only the coal exceptions (co-located coal/gas project fields, coal units and pre-conversion coal phases) may remain; they are **low priority / optional**. The web UI's "GOGPT Validation Report" tab (Projects tab, country search) shows the same stored errors
- The **"no tracker found" units** for the scope are reviewed (checklist row 56): `python no_tracker.py --country <name>` (or `--state <State>`) lists the combustion units the database could not assign to a tracker because the unit has no fuel, or several fuels and no primary one. They are missing from every export, so this is the only place the batch sees them. Each live one is a web-UI fix (enter the fuel); the list usually prints nothing
- Notes for the next cycle go in the "Additional notes" column of the Researcher Country Assignments tab, with an estimate of the time the country needs next update (M199), and the estimate is logged in the roster's notes
- Leftover `in progress` units are filtered in the database and set to `updated` or `no changes` (§5)
- The roster row moves to `done`; the PM reviews and may flag fields — process flags as a small follow-up batch

## §13 Hard rules (these override anything below)

- **Never modify the live GEM database**, except through the supervised browser session in `database-browser-edits.md`. Outputs are always the two-workbook deliverable, applied in the web UI by hand or through that session.
- **Every URL passes the §7.1 verification gate** — no exceptions.
- **Never cite gem.wiki / globalenergymonitor.org / GEM-derived republishers; abarrelfull is banned** (§7.2).
- **One fully validated URL suffices (2+ independent preferred; a status change needs 2+ for green); mirrors of one document = one source** (§7.2).
- **Reference edits merge, never replace; no orphan citations; URLs only in reference columns** (§7.2–§7.3, §4.4).
- **Status Detail and Notes are additive, newest on top** (Baird 2026-10-07): new text goes above the existing text, which stays word for word; never a rewrite or a deletion. The manual lets a human clean up old Notes (M272); the researcher flags an outdated note in a `qa` record with `concern_type` `notes_cleanup`. `state_gate.py` gate `additive` enforces it.
- **A Status Detail entry carries its own source links** in its text: the entry, a blank line, then one link per line (Baird 2026-10-08, layout 2026-10-09; `build_review_package.inline_value` writes it, and a blank line separates the new entry from the older text below). The link never goes in Status Data Source, which feeds the milestone and scheduled-event timeline. One fully validated source makes it green: it is not a status change.
- **Fresh pull chain at the start of every batch**, column map re-derived (§3).
- **Project-level field changes apply to ALL unit rows** — and check the unfiltered CSV at co-located coal/gas plants (§9).
- **Start Year never on shelved/cancelled; Retired Year never on mothballed; scheduled-event logic enforced** (§4.2, `qc_checks.py`).
- **Electrical nameplate MW only — never shaft/mechanical-drive MW; never thermal MWt** (§4.3).
- **Don't create duplicate entities** — `entity_lookup.py` before staging any new owner/operator (§8).
- **Blank = not researched; "not found/unknown" only after searching** (§5).
- **`qc_checks.py` passes before every build** (§10).
- **Notes are written for people, in plain language** (`docs/reference/notes_style.md`, Baird 2026-10-02): `researcher_notes` and `action` must read as a colleague's explanation, with sources named by what they are and no repo jargon.

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
| Green | One fully validated ref (2+ independent for a status change) | Any ref that clears the verifier, names the unit, states the value |
| Yellow | Single-source status change, or partial validation | Value implied or contested |
| Red | Single weak/unvalidated ref | Prefer blank + `qa` record |
| Blue | Re-verified, unchanged | The "no changes" outcome at cell level |
| (none) | Searched, nothing found | Research gap, not confirmation |

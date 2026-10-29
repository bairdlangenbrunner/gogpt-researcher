# Data center backup engine fleets: what the agent misses and how to fix it

Written 2026-10-27 after Amalia Llano's Slack note that the review app missed the Amazon Web Services Canton and Ridgeland data centers in Mississippi, each with hundreds of diesel engines as backup power.

## What happened

The agent found those sites and dismissed them. The Mississippi permit harvest listed Amazon Data Services at Ridgeland (air construction permit 1720-00099) and at the Madison Mega Site in Canton (permit 1720-00098) and Compass Datacenters in Meridian (permit 1460-00133). The statewide agent wrote in `batches/us-ms/coverage.json` that "the data center notices for Amazon and Compass cover emergency diesel generator sets only" and staged nothing. Amalia added all three plants by hand on October 24 and 25: Canton at 896.5 MW under construction, Ridgeland at 286 MW operating plus 770 MW under construction, Meridian Compass at 800 MW under construction, each as diesel internal combustion with the Backup Power box ticked.

The same thing happened in every state batch so far:

- Iowa (batch of October 16): Microsoft Ginger East and West, Microsoft Osmium and QTS Cedar Rapids were added by Amalia on October 20 and 21, during her review. The Iowa sweep never mentioned them.
- Illinois (batch of October 9): the statewide agent wrote that the Compass, Aligned and CyrusOne permits "cover diesel backup only" and staged nothing.
- Michigan (delivered October 27, in Amalia's review app now): the agent dismissed the Saline Township campus (Project Mitten), the Google campus in Van Buren Township, Gibraltar, Metrobloks Southfield and Microsoft Gaines Township as "diesel backup only", and read the possible-updates sheet rows for them the same way.
- Mississippi also has an Amazon site at Clinton (JAN250, draft permit 1080-00275, public comment September 2026) in the harvest output that nobody answered.

## Why the agent does this

The rule is written into the research step itself. `scripts/captive_lng.py`, function `render_data_center`, rule 3: "Emergency or backup generator sets at a data center are not captive power plants and are not watch items; only generation that supplies routine power counts." The same sentence is in `docs/sops/update.md` step 9, `docs/workflows.md` section 2, and `docs/country_notes/united_states.md`. It went in with the captive step on 2026-10-09 as a reading of the manual's Emergency/Backup checkbox text. It was never a ruling by Baird or the GOGPT leads, and it is the opposite of what GEM does.

GEM's actual practice, read from the October 26 export: 62 United States unit rows at data centers are backup fleets, either with Backup Power set to yes (the newer records, April to October 2026) or with "(backup)" in the unit name (the older ones, such as Cloud HQ MCC Campus, Google Lenoir, Vantage Ashburn, Microsoft CCO06). They were added by the GOGPT team, including Amalia, across Georgia, Virginia, North Carolina, Indiana, Ohio, Texas, Colorado, Iowa and Mississippi.

The September 2026 Editing Manual supports that practice without naming it: internal combustion engine sets are added when the nameplate total is 50 MW or more (20 MW per unit in the EU and the United Kingdom); the Emergency/Backup checkbox exists for units that are backup generators at a data center; a plant serving a data center is named "XYZ Data Center power station". The QC checklist row 39 still says "gas-powered data centers", which is the wording Amalia's screenshot shows; she says the team also includes reciprocating engines that serve as backup, since data centers that cannot get gas turbines are building large engine fleets.

A second, smaller problem: the `data_center_hold` watch case (Baird 2026-10-08) parks every gas-fired data center plant on the watch list until a reviewer promotes it. The leads add such plants directly (ABI-1, Adams Fork, Apollo, Beacon, Blue Valley and about 60 more are in the export at announced or pre-construction). The hold predates the one-source add rule of 2026-10-23 and now just delays adds the team wants. Illinois holds three such projects (Monarch Rock Air, Hut 8 Project 4, Joliet Technology Center), Kansas one (Flint Hills Digital Campus), Michigan one (Dowagiac).

## The convention to encode (as the existing records do it)

- Plant name: "<Operator> <Place> Data Center power station" (Amazon Web Services Ridgeland Data Center power station; Meridian Compass Data Center power station; Microsoft Ginger West Data Center power station).
- One unit row per permit phase or building group (Ridgeland has Bldg 1-4 operating at 286 MW and Bldg 5-14 under construction at 770 MW), or a single unit "1" when the permit does not split the fleet. A separate small unit is sometimes carried for a different engine type (Ridgeland Unit 15 at 4.1 MW).
- Fuel: fossil liquids: diesel for diesel engines; fossil gas: natural gas for gas engines or turbines; both when dual fuel (the Iowa Microsoft rows carry diesel and fuel oil).
- Turbine/Engine Technology: internal combustion. Number Of Engines and Capacity Per Engine filled from the permit.
- Capacity: the nameplate sum of the generators in the row, in MW electrical. Permits list generator kW or kWe; convert and add. Engine horsepower or mechanical kW is not the figure.
- Status: the campus's build state, operating when the buildings run, construction when the permit is issued and the site is being built, pre-construction on an issued permit alone, announced on an application or notice.
- Captive industry type data center, Captive industry use power, Captive non-industry use none, Backup Power yes, all at unit level so the checkbox shows; Captive Data Source the permit.
- Start year: the year the buildings were commissioned, when known. Location exact from the permit's street address through the location ladder.
- Threshold: the fleet's summed nameplate at 50 MW or more (20 MW in the EU and United Kingdom). One verified source, usually the state air permit, is enough.

## Questions for Amalia (and Dan for Europe) before the rule is final

1. Confirm the threshold is the summed nameplate of the backup fleet, not per engine, and that generator electrical kW is the figure.
2. Confirm the unit grouping: one row per permit phase or building group when the permit splits them, otherwise one row.
3. Confirm the status mapping to the campus build phase, and whether an application alone is announced.
4. Whether a gas-fired routine-power data center plant should also be added directly rather than held on the watch list. This is Baird's own hold from October 8, so it is Baird's call, but the leads' records say add.
5. Whether the checklist row 39 and the manual should say "gas or diesel, including backup engine fleets" so the written rule matches the practice.
6. Whether Dan's European countries apply the same rule at 20 MW; Frankfurt, Dublin and Amsterdam campuses would qualify in large numbers.

## The fix, in order

### 1. Rewrite the rule everywhere it lives

- `scripts/captive_lng.py`, `render_data_center`: replace rules 1 to 4 with the convention above. Rule 1 (watch list only) goes if Baird lifts the hold; otherwise it stays for routine-power gas plants only and never applies to backup fleets, which are adds. Rename the heading from "Gas-powered data centers" to "Data center power, gas or diesel, routine or backup".
- `scripts/build_state_brief.py` (the watch-case paragraph near line 650 and the scope brief): drop or narrow `data_center_hold`; add a line that a backup engine fleet at the threshold is an add.
- `.claude/workflows/state-sweep.js` (watch-case list near line 556, captive-fields note near line 390): same, and tell the plant subagents that a tracked data center plant's Backup Power box and engine counts are research fields.
- `scripts/schema_constants.py` `WATCH_CASES`: remove `data_center_hold`, or redefine it as "a data center campus named with no generation figure yet" (which is really `no_generation`). `scripts/state_gate.py` `gate_watch_case` and `tests/test_watch_case_gate.py` follow.
- Docs: `docs/sops/update.md` step 9, `docs/sops/discovery.md` section 3.1 and the captive sweep table, `docs/workflows.md` sections 2 and 3, `docs/country_notes/united_states.md` line 49, `docs/reference/controlled_vocab.md` Emergency/Backup line, `docs/reference/staged_json_schema.md`, the CLAUDE.md router line on the captive sheet and data centers, and the memory note `captive-lng-and-data-centers`.
- `review_app/checklist.py` row 39: keep the checklist's wording (it is GEM's) but the blurb for group 7 should say backup fleets count.

### 2. Make the harvest sum the fleet instead of leaving it to the agent

A new `scripts/data_center_fleets.py --state <State>` (or a function each harvester calls): for every permit facility whose industry code or name says data center (SIC 7374, NAICS 518210, "data center", "data services", "digital", the hyperscalers' names), open the permit or application, list the emission units that are generators, sum the generator nameplate in MW, count the engines, record fuel, building or phase grouping, permit number, issue date and street address, and write `work/permits/<tag>/_data_centers.md` and `.json` with one row per site and a verdict column: at threshold, below threshold, already in GEM (matched by name and address to a GEM data center plant), no generators listed. The Mississippi, Michigan and Iowa harvesters already identify data center sites; Iowa reads the application forms (equipment, manufacturer, nameplate), which is the model. Other lead lists feed the same table: the possible-updates sheet rows that name data centers, state air permit notices, DatacenterDynamics and local press, the EIA-860M planned generators (rarely, since backup sets are not reported), and a GEM export check for an existing plant at the address.

`build_state_brief.py --captive` reads that table and writes every at-threshold site into `briefs/_scope.md` as a named add task, every below-threshold site as a one-line record, and every GEM data center plant in the scope as a plant task (check the fleet size, the phase, the Backup Power box, the engine counts against the newest permit).

The file contract (fixed 2026-10-27 so the harvester, the brief builder and the gate agree):

`work/permits/<tag>/_data_centers.json` is one object: `scope` (the state or country name), `tag` (`us-mi`), `generated` (ISO date), `threshold_mw` (50, or 20 for EU and UK scopes), and `sites`, a list. Each site has `site_id` (a slug the harvester keeps stable across runs, built from operator and place), `name`, `operator`, `address`, `city`, `permit_numbers` (list), `permit_urls` (list, every URL verified or marked with the fetch route that failed), `issue_date`, `fuel` (`diesel`, `natural gas`, `dual`, `unknown`), `engine_count` (integer or null), `capacity_per_engine_mw` (number or null), `summed_nameplate_mw` (number or null, electrical), `phases` (list of `{label, engines, mw, status_hint}`, empty when the permit does not split the fleet), `gem_plant_id` and `gem_plant_name` (null unless a GEM data center plant matches by name or address), `verdict` and `source_notes` (plain language, what the permit says and where the numbers come from). `verdict` is one of `at_threshold` (sum at or above the threshold), `unknown_capacity` (generators listed, no usable nameplate; the manual adds with capacity blank), `below_threshold`, `in_gem` (a GEM plant already covers the fleet; the site still gets a check task comparing the fleet, phases and Backup Power box with the permit), `no_generators` (the permit covers no generators).

`batches/<tag>/coverage.json` gains a `data_centers` object keyed by `site_id`: `decision` is `add` (with `record_id` of the newplants record), `already_in_gem` (with `plant_id`), `update` (with `record_id` of the updates record, when the permit disagrees with the GEM rows), `below_threshold` (with `summed_nameplate_mw`) or `no_generators`, plus `note`. The gate `data-centers` requires an answer for every site whose verdict is `at_threshold`, `unknown_capacity` or `in_gem`; `add` is the only valid decision for `at_threshold` and `unknown_capacity` sites unless the note names the GEM plant that already holds the fleet.

### 3. Gate it

`state_gate.py`: a new gate `data-centers`, like `ids_followup`: every site in `_data_centers.json` at or above the threshold is answered in `coverage.json` under `data_centers` with `decision` add (and the `newplants` record id), already_in_gem (with the plant id), below_threshold (with the sum) or no_generation. The `chase` gate already rejects "noticed but not researched" notes; add "backup only" and "emergency generators only" to the phrases it flags when no sum is given.

`qc_checks.py` and `assemble_state.py`: make sure `Backup Power`, `Number Of Engines` and `Capacity Per Engine` are accepted in a `newplants` unit's fields and carry through to the workbook; `review_app/checklist.py` already lists Backup Power among the captive columns.

### 4. Catch up the delivered states

One catch-up batch per delivered scope, or one combined `batches/us-dc-catchup/` with a state column, running only the data center step: Michigan first (it is in Amalia's review now and the five dismissed campuses are named), then Illinois (Compass, Aligned, CyrusOne), Mississippi (Amazon JAN250 Clinton, plus a check that the three hand-added plants match the permits), Iowa (confirm the four hand-added plants and look for any the harvest did not surface), Kansas, Maryland and New York. Each produces `newplants` records in the convention above, goes through the gate, and lands on the review page as new plants. Any site Amalia already added becomes an update record only where the permit disagrees with what she typed.

### 5. Then the standing step

Every state batch runs `data_center_fleets.py` right after the permit harvest, before the briefs. The agent never writes "backup only" without the summed nameplate beside it.

## Where it stands (2026-10-27, end of day)

Steps 1 to 3 are built and the test suite passes (one unrelated failure in `tests/test_irp_sheet.py` from another session's review page work). `scripts/data_center_fleets.py` takes `--state` or `--country`, plus `--leads` (a CSV of extra sites with permit URLs), `--offline`, `--max-docs` and `--csv`; it reads candidates from the harvest's `facilities.json`, falls back to the permit markdown lists, adds every GEM data center plant in the scope, reads each document four ways (application inventory form, numbered generator lines, permit emission unit rows, prose) and never converts horsepower, mechanical kilowatts or heat input to MW. Tests are in `tests/test_data_center_fleets.py` with fixtures under `tests/fixtures/data_center_fleets/`.

First real runs, outputs under `work/permits/us-ms/` and `work/permits/us-mi/`:

- Mississippi: Ridgeland (391 engines, 1,060 MW), Canton (336 engines, 904 MW) and Compass Meridian (420 engines, 813 MW) all match the plants Amalia added, verdict in GEM; the Ridgeland sum agrees with her 286 + 770 + 4.1. Amazon Clinton JAN250 is at threshold at about 250 MW on the September 2026 public notice found through Wayback (engine count unknown, draft permit not on the state site, not in GEM): the one open add. Colossus 2 Southaven gets a GEM-only check row. A NASA Stennis site is flagged by industry code with seven engines in horsepower only; probably a false positive.
- Michigan: MI GRR in Grand Rapids (78 engines, 214 MW) and Google Van Buren Township under Panattoni (24 engines, 66 MW) are at threshold and not in GEM. Project Mitten in Saline sums to 38.5 MW on the application inventory form (below threshold; one unit's label and design capacity disagree, the note says so). Five sites have engines with no electrical rating (123Net Southfield, Sanhua, DXC, FCA, Alliance Cloud Services Dowagiac with 15 diesel sets in heat input only). Gibraltar, Metrobloks Southfield and Microsoft Gaines Township are not in the Michigan harvest by name and need `--leads` rows with their permit URLs.

Step 4 (the catch-up batches) started on 2026-10-27 as one narrow batch per state (`batches/us-<st>-dc/`, recipe in `docs/workflows.md` §2 step 4): the harvester reruns with a lead CSV under `work/dc_leads/` naming every campus the earlier batch noticed, `build_state_brief.py --data-centers-only` builds a batch that holds only the data center sites and the GEM plants they match, and the gate's statewide checks step aside for it (`focus: data_centers` in the index). A named site with no document on record is now `no_documents` (a search task), and a site the harvester could not size may be closed `below_threshold` with the number the researcher added up, or `no_generators`, `not_data_center` or `nothing_found` with a note; a fleet summed at the threshold is still only an add or already in GEM. Step 5 is written into CLAUDE.md, the Update and Discovery SOPs and `docs/workflows.md`.

### Next steps for the catch-up batches (handoff, 2026-10-27 afternoon)

The code, gates, docs and tests for the catch-up batches are done (test suite 435 passed). The harvester run for all seven states was started in the background by the runner script that writes `work/permits/us-<st>-dc/_data_centers.json` and `.md` for Mississippi, Michigan, Illinois, Iowa, Kansas, Maryland and New York, with lead lists in `work/dc_leads/us-<st>.csv`. If a `_data_centers.json` is missing for a state, rerun `python scripts/data_center_fleets.py --state <State> --leads work/dc_leads/us-<st>.csv --out-dir work/permits/us-<st>-dc` from the repo root. Then, per state, from `scripts/`:

1. `python build_state_brief.py --state <State> --mode update --batch ../batches/us-<st>-dc --data-centers ../work/permits/us-<st>-dc/_data_centers.json --data-centers-only` (add `--allow-stale-export` if the 2026-10-27 pull is over a day old, or pull fresh).
2. One Sonnet agent per state: it reads `batches/us-<st>-dc/briefs/_data_centers.md`, `_scope.md` and every plant brief in `briefs/`, follows the shard contract in `notes/us_state_agent_plan.md` (the Michigan `batches/us-mi/shards/_state.json` Hancock record is the shape for a `newplants` record), verifies every URL with `url_verifier.py`, reads permits through `fetch.py`, writes `shards/_state.json` (meta, qa, monitor, newplants, newunits, source_log), a shard per matched GEM plant, and `coverage.json` with a `data_centers` answer for every site in the brief. Plain-language notes, no gem.wiki, Wayback citable.
3. `python assemble_state.py --batch ../batches/us-<st>-dc`, then `python state_gate.py --batch ../batches/us-<st>-dc` until GATE CLEAN, then `python qc_checks.py --staged` and the review page per `docs/workflows.md` §8.
4. Sites Amalia already added (the Mississippi three, the Iowa four) become update records only where the permit disagrees with what she typed.


### Catch-up batches run (2026-10-27, evening)

All seven batches (`batches/us-<st>-dc/`) are researched, assembled and GATE CLEAN; not yet on a review page. New plants: Mississippi 1 (Amazon Clinton, about 250 MW, announced) plus a 7.8 MW unit of small generators at Canton; Michigan 3 (Switch Grand Rapids 106.9 MW, Google Van Buren 66 MW, Raeden Gibraltar capacity blank); Illinois 5 (Compass Hoffman Estates, Aligned Elk Grove Village and Northlake, CyrusOne Aurora, Edged Project Vector); Iowa 4 (Meta Altoona 328 MW, Google Council Bluffs, Microsoft Grand Avenue, Microsoft Willow Creek) plus updates raising Ginger West to 130 engines and Ginger East to 96; Maryland 3 (Aligned Frederick 508 MW, Amazon Frederick and Amazon IAD-534, each 257.75 MW); Kansas and New York none. Lessons: the harvester double counts flexible engine groups (MI GRR read 213.7 MW, the permit sums 106.9) and misses kWe ratings on small sites; `fetch.py` and `url_verifier.py` read Word notices as raw XML, so a phrase split across text runs fails to match; the Google and Meta "Kansas City" campuses are in Missouri.

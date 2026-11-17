# New Mexico update plan

New Mexico is a full-state update for Amalia Llano's review page, planned 2026-11-17 on the Kentucky and Oklahoma pattern (`scopes/us-ky/plan.md`, `scopes/us-ok/plan.md`). Every plant in the scoped export, every lead, every permit, every commission filing, every council and commission record and every news story gets read and cited or answered. Scope tag `us-nm`. This plan is written to be run by another session, probably on a cheaper model, so it names every file and repeats what that session needs. Run every script from the repo root as `python scripts/<name>.py` unless a step says `scripts/`.

## Decisions

Settled by the request (Baird 2026-11-17):

- The batch stages into Amalia's page (`new-york-maryland` in `review_app/artifacts.json`, https://claude.ai/artifact/7bnX9RMity3Yw5mdaojNaL). Add `batches/us-nm/staging` to that page's dirs before the rebuild.
- Mode is `update`, every plant, in the order `worklist.py` gives (25 priority-1 rows first).

Defaults this plan takes unless Baird says otherwise:

- **Amalia is working New Mexico right now.** Her "ALQ42026" notes and 30-odd rows were edited 2026-11-09 and 2026-11-10 (Cunningham, Maddox, Reeves, Rio Grande 7 and 8, NTEC, Westside, Site Layer 1, Clean Path, Lea County Data Center, Roswell Information Park, Project Jupiter, the PNM and SPS IRP placeholders, SWPP ERAS Hobbs). Re-pull at run time and treat her values as the baseline. Stage an edit against one of her values only when a verified document disagrees, and say which document. If her edits are still landing on the run day, wait until her row on the assignments tab says done or ask her.
- **Project Jupiter stays cancelled.** Amalia marked both units cancelled on 2026-11-10 because the developer withdrew the two gas turbine permit applications in April 2026 and switched to a gas-fed Bloom fuel cell microgrid (2.4 GW planned, capped at 1,600 MW, NMED permit 10883, hearing vacated on 2026-11-06). Fuel cells are not combustion. The run only checks that her cancellation has two independent publishers and a dated step. It also asks one question: does the fuel cell plant have backup diesel or gas engines at 50 MW summed? If it does, that fleet is an add. **This is the one call for Baird to confirm**: whether GEM records the fuel cell plant at all is a manual question, and this plan follows Amalia's reading.
- Models per step follow `docs/workflows.md`. The harvesters and the per-plant sweep run on Sonnet. The scope-wide agent, the resource plan reading and the location review run on Opus. Gates and merge calls stay in the main loop.

## What the export already shows (2026-11-17 pull)

52 scoped rows at 24 plants: 19 operating, 15 pre-construction, 9 announced, 7 cancelled (one inferred), 1 construction, 1 retired. The roster row says 22 in development, 6,216.4 MW.

- In development: NTEC gas plant (18 LM6000 units, 60.5 MW each, pre-construction, 2028; EIA 66478), Westside (63 MW, Jenbacher engines, construction, 2028; EIA 70261), Site Layer 1 Data Center (300.8 MW Wärtsilä engines, Grant County, pre-construction), Lea County Data Center (2,000 MW, New Era Energy & Digital, announced), Roswell Information Park Data Center (700 MW, announced), SPS 2023 IRP power plants (2,088 MW, pre-construction), SWPP ERAS Hobbs (234 MW, announced), PNM 2023 IRP power stations 1 to 3 (132, 164 and 164 MW, two timepoints each).
- Planned retirements: Cunningham 2 (2027), 3 and 4 (2040); Maddox 1 (2028) and 2 (2034); Rio Grande 6 (2026), 7 (2027) and 8 (2033); Valencia CTG1 (2028); Afton, Lordsburg GT1 and GT2 and Rio Bravo (2039); Reeves 3 (2044).
- Start scripts, run 2026-11-17: the validation report has 0 errors. There are 0 open Assigned Comments threads, 0 no-tracker units and 0 captive LNG rows. Location has 7 candidates: the five in-development placeholders and the two data center plants with approximate points. The ID join found 8 tasks, 1 ID to type (Lordsburg EIA 7967) and 1 possible new plant (Pyramid).
- The unfiltered export also carries Four Corners 4 and 5 (coal, retire 2038), San Juan 1 to 4 (retired coal), Escalante (retired coal), Desert Rock and the NTEC 8 Rivers coal plant. Keep them visible for the San Juan and Escalante site-reuse checks.

## State context the sweep needs

The full version is in `note.md`. In short:

- **Grids.** The east (Xcel's Southwestern Public Service, SPS, in Lea, Eddy, Chaves, Roosevelt and Curry counties) is in the Southwest Power Pool. The rest is outside any market: PNM, El Paso Electric (EPE, the Las Cruces area), Tri-State and its member cooperatives, Farmington Electric Utility System, and Los Alamos County.
- **Regulator.** The New Mexico Public Regulation Commission regulates PNM, SPS and EPE. That covers resource plans every three years, certificates for new plants and abandonment approvals for retirements. Cooperatives file plans too.
- **Air permits.** NMED's Air Quality Bureau covers the state outside Bernalillo County. The City of Albuquerque Air Quality Program covers Bernalillo County (Reeves, Rio Bravo). EPA Region 9 covers the Navajo Nation (NTEC), and EPA Region 6 covers other tribal land.

## Access, probed 2026-11-17

A Sonnet probe opened every source family. Notes are in the planning session's scratchpad (`/private/tmp/claude-501/nm-probe/`, which will not survive). What matters is repeated here.

- **NMED air permits, the complete record (`permit_record`).** The APMAP facility map at https://rsmt.air.net.env.nm.gov/ has an anonymous REST backend at `https://rsmt-api-c4cwg2h3a2ewdjf4.westus2-01.azurewebsites.net/`. Use `get-facility-name-wildcards?facility=<name>` for names, `get-facility-locations` for the AI number (Cunningham is 604, Maddox 588) and `get-facility-popup?ai=<n>` for permit numbers. Each facility's documents are a public collection: `cloud.env.nm.gov/air/plugins/api_search/index.php?key=<public key from the page's utils.js>&search_type=public_collections&search=AI%20<n>`, sent with `Referer: https://rsmt.air.net.env.nm.gov/` (403 without it). That points to `cloud.env.nm.gov/resources/collection/<id>`, which lists every PDF (34 for Cunningham). The PDFs download through `fetch.py`.
- **NMED notices and pending work (`permit_notices`).** https://www.env.nm.gov/public-notices/ works with plain curl and links PDFs. The comment portal is https://nmed.commentinput.com/comment/search. The "Current Permitting Actions Under Review" Coda table has 301 records, but it is virtualized, so a page render shows only about 10 rows. Its siblings "AQB NSR Issued Report" and "AQB Facilities Lat Long Report" are not probed yet. Read all three through Coda's export or API in Stage A.
- **Albuquerque.** https://www.cabq.gov/airquality/pending-air-permit-applications lists 5 pending applications. The monthly notice report `aqn-report.pdf` has a text layer. Permits are under `documents.cabq.gov/environmental-health/airquality/`. Plain curl works for all of it.
- **EPA.** ECHO REST works with plain curl (27 active New Mexico electric facilities). NTEC is Region 9 docket EPA-R09-OAR-2024-0028. The draft is a synthetic minor permit for 742 MW from 18 LM6000 turbines, with comment closed 2026-05-18. The docket documents are listed by `api.regulations.gov/v4/documents` (DEMO_KEY, 10 calls an hour; pace or get a free key).
- **Public Regulation Commission.** The old e-docket is dead. PRCe360 at https://e360.prc.nm.gov/portal/public/ needs no sign-in ("Continue as Guest"). Anonymous JSON POSTs do the work:
  - Case search: `/core/api/_q/v1/prc/nm/intake/dashboard/getAllCases`.
  - Document list: `/core/api/apiflow/v1/prc/nm/intake/casepublicdocument/getAll`.
  - Download: `/core/api/apiflow/v1/casex/cms/downloadToken`, then `GET /core/api/document/v1/previewDocument?token=`. `downloadDocument` answers 401, so use the token flow.
  - The SPS 2026 resource plan downloaded this way (140 MB, 2,425 pages).
- **Queues.**
  - SPP: `opsportal.spp.org/Studies/GenerateActiveCSV` is anonymous (1,016 rows, 56 in New Mexico; the header is row 2). `pull_queues.py` already reads SPP.
  - El Paso Electric posts its active queue as a PDF with text: `epelectric.com/el-paso-electric/uploads/epe-interconnection-queue-active.pdf`.
  - LBNL's Queued Up file (`emp.lbl.gov`, through `fetch.py`) covers PNM, Tri-State and EPE as non-market areas.
  - PNM's and Tri-State's own queue pages are not found yet. That is a Stage A task, not a wall.
- **Local records.**
  - Albuquerque and Los Alamos County use Legistar, with an open JSON API (`webapi.legistar.com/v1/cabq`, `/losalamos`).
  - Hobbs uses CivicClerk, with open OData (`hobbsnm.api.civicclerk.com`), and also posts packets under `hobbsnm.org/files/public_meetings/`.
  - CivicPlus AgendaCenter sites: Grant County (`grantcountynm.gov`, download proven), Los Lunas, Farmington and Roswell. Lea County (`leacounty.gov`) is CivicPlus too, but its AgendaCenter path answered 404; use its Commission Meeting Documents page.
  - Revize sites: Doña Ana County (`donaana.gov` BOCC agendas and the approved docket) and Chaves County.
  - San Juan County needs `cf_impersonate`.
  - Valencia County (`valencianm.gov`), Bernalillo County (IQM2 at `bernco.iqm2.com`), Las Cruces, Sandoval County and Rio Rancho load, but their list and download paths are not proven yet.
- **News.** Plain curl works for the Albuquerque Journal, Santa Fe New Mexican, Searchlight New Mexico, the Carlsbad Current-Argus and the Hobbs News-Sun. Source NM needs `cf_impersonate`. The Las Cruces Sun-News answers 402, so use `--render` or Wayback. Article pages are not tested yet.
- **Public notices.** nmpress.org has a statewide notice page and an RSS feed. The search request is not proven yet.
- **Secretary of State business search** (`enterprise.sos.nm.gov`) is a React page with a CAPTCHA reference. The search endpoint is not found yet. If the search truly needs a CAPTCHA, it is a human wall: Baird looks up the named LLCs by hand.
- **Dead or wrong hosts replaced:** `edocket.prc.nm.gov` and `e-docket.nmprc.state.nm.us` (now `e360.prc.nm.gov`); the NMED air-permit pages under `/air-quality/` (now `/public-notices/` plus APMAP); `leacounty.net` (now `leacounty.gov`); `valenciacounty.org` (now `valencianm.gov`); `donaanacounty.org` (now `donaana.gov`); `fmtn.org` (now `farmingtonnm.gov`); `grantcountynm.com` (now `grantcountynm.gov`).

## Human walls (expected)

Each becomes a `human_wall` sentence in `coverage.json`. No script signs in with Baird's credentials.

- The Secretary of State search, if the CAPTCHA is real.
- The regulations.gov full pull, if DEMO_KEY pacing is too slow: Baird registers a free key.
- RBLC: the determination search runs only in a browser; Baird exports the New Mexico table.
- County records not posted online: an email to the clerk, drafted for Baird.

## Manual rules the run leans on

The repo CLAUDE.md hard requirements apply in full. New Mexico leans on these:

- **Adds.** An add needs one verified source (a queue row, a commission filing, an NMED application, a county record). A data center backup fleet at 50 MW summed nameplate is an add with Backup Power yes. Owner goes on every add: the project LLC at 100 percent until a parent is named.
- **Status changes.** Green needs two independent publishers. The commission order and the utility's filing count as two.
- **Units.** A combined cycle block is one unit (Afton CC1, Hobbs CC1, Luna CC1, Bluffview CC1). Capacity is electrical nameplate only; compressor drives in the Permian and San Juan basins never count.
- **Status Detail and Notes** are additive, newest on top, and Status Detail carries its own links.
- **Dates.** Start year never goes on shelved or cancelled units, and retired year never goes on mothballed ones.
- **Sources.** Wayback copies are citable. gem.wiki is never cited, and the Sierra Club list is reference only.

## Guardrails (all exist; nothing to build)

`access_check.py --scope us-nm` before anything else reads the web. Gates `access-proof`, `statewide-coverage`, `permit-system`, `local-records`, `chase`, `ids_followup`, `dedup`, `queues`, `data-centers`, `irp-plans`, `validation`, `location`, `additive`, `questions`, `watch-case`, `add-basics`, `access`, `unit-names` and `headers` in `state_gate.py`. `qc_checks.py --staged` with zero errors, `url_verifier.py` on every URL, `entity_lookup.py` before every new owner, and `access_audit.py batches/us-nm --retry` on every give-up.

## New tooling (build in Stage A, each with an offline test on saved sample pages)

Follow the Kentucky and Oklahoma harvesters and their tests (`tests/test_harvest_permits_kentucky.py`, `tests/test_harvest_psc_kentucky.py`, `tests/test_harvest_local_kentucky.py`). Build on `scripts/harvest_lib.py` (`get`, `wayback_url`, `harvest_out`, `docket_cache`, `report_failure`, `tag_batch`). When a server answers a document request with an HTML page, detect it by content type and the `%PDF` bytes and fall back to Wayback.

1. **`scopes/us-nm/harvest_permits.py`**
   - For every GEM plant, every owner and every lead name: APMAP name search, then the AI number, permit numbers and the cloud.env.nm.gov public collection.
   - Download each permit, application and statement of basis under `scopes/us-nm/work/permits/docs/<AI>/` and extract it with `pdftotext -layout`. Pull facts: units, megawatts, make and model, engine counts and dates.
   - Also sweep the APMAP facility list for power-like names (power, generating, station, energy, data center, microgrid, turbine, engine) with no GEM match into `_unmatched.md`, the way Oklahoma's does.
   - Read the NMED public notices page, all three Coda tables and the Albuquerque pending list and notice report.
   - Read the EPA Region 9 NTEC docket through regulations.gov.
   - Write `scopes/us-nm/work/permits/<plant_id>.md` and `.json` plus `index.json`.
2. **`scopes/us-nm/harvest_prc.py`**
   - Search PRCe360 for every case since 2021 about a resource plan, a certificate for a gas or oil plant, an abandonment, a data center tariff or a large-load contract. Also search for every utility (PNM, SPS, EPE, Tri-State, the cooperatives) and every lead name.
   - Add the cases named below.
   - List each case's documents, download the order, the application and the plan through the token flow into `scopes/us-nm/work/prc/<case>/`, and extract them.
   - Write `batches/us-nm/harvest/prc_dockets.json` in the `build_state_brief.py --harvest` contract.
3. **`scopes/us-nm/harvest_local.py`**
   - Read every agenda, packet and minutes file since 2024-01-01:
     - Legistar: Albuquerque and Los Alamos.
     - CivicClerk: Hobbs.
     - AgendaCenter: Grant County, Los Lunas, Farmington, Roswell, and Lea County through its documents page.
     - Revize: Doña Ana and Chaves.
     - San Juan County through `cf_impersonate`.
     - Valencia, Bernalillo, Las Cruces, Sandoval, Rio Rancho, Eddy County and Carlsbad once Stage A finds their paths.
   - Record the sentences that name a plant, a lead, a power or data center project, an industrial revenue bond or a rezoning.
   - Write `batches/us-nm/harvest/local_records.json` and `.md`.
   - Bodies with nothing posted go to `not_posted`.
4. **`scopes/us-nm/queues.json`**
   - Market SPP, plus `lbnl_entities` for PNM, EPE and Tri-State so `pull_queues.py --state NM` lists their rows from the LBNL file.
   - The EPE queue PDF is read by hand and answered as `market EPE`.
   - Give `known` patterns for Cunningham, Maddox, Hobbs, the SWPP ERAS Hobbs request, NTEC, Westside and Pyramid.
5. **`scopes/us-nm/irp_plans.json`** and `irp_sheet.py` aliases if needed. Plans, newest first:
   - PNM 2026 IRP (filed 2026-09-01, case 25-00022-UT; https://www.pnm.com/2026-irp, report and appendices PDFs; a 172 MW gas placeholder pending an RFP).
   - SPS 2026 IRP (filed 2026-10-23, case 25-00076-UT, through PRCe360 document id f1f5a543-d072-43bf-a67d-b4ec01397c98), plus the approved 2023 plan and its 2025 portfolio (2,088 MW gas, approved 2026-05-07).
   - EPE 2025 IRP (case 24-00260-UT) and EPE's 2026 New Mexico all-source RFP.
   - Tri-State's newest resource plan (Colorado proceeding 23A-0585E) and its 2026 resource adequacy table.
   - Farmington Electric Utility System, Los Alamos County, Kit Carson Electric and each cooperative that owns or buys from a plant here.
   - Every plan is read from start to end, including the alternative portfolios. The tab's 2023 rows are older than the newest plans, so the placeholders are checked against the newest plans.
6. **`fetch.py` host rules** in `work/fetch_routes.json`: sourcenm.com and sjcounty.net need `cf_impersonate`, lcsun-news.com needs `--render`, and cloud.env.nm.gov needs the Referer header. Add a New Mexico row to `docs/reference/site_access.md` for each.

## Known leads the run must settle (each becomes a record or a coverage answer)

- **Pyramid Generating Station** (Tri-State, Hidalgo County, EIA 7975; four 46.5 MW LM6000 turbines operating since 2003, 186 MW). An add on the EIA record plus one document. Find Tri-State's page and the NMED permit through APMAP.
- **SPS gas from the approved resource plan** (2,088 MW, PRC approval 2026-05-07, in service 2028 to 2030) and the 2026 IRP filed 2026-10-23. Split the placeholder into named plants where the certificate filings name sites. Texas sites go to the Texas scope, not here. Also settle the SWPP ERAS Hobbs request (234 MW), Xcel's August 2026 selection of one gas plant, and the life extensions or retirements at Cunningham 2 to 4 and Maddox 1 and 2 (the ID join says EIA gives Cunningham 1's retirement as 2024, GEM 2023).
- **PNM 2026 IRP** against the three 2023 placeholders: replace, rename or retire them, and record the 172 MW placeholder. The La Luz expansion is 40 MW and under the threshold; record it only if the plant total crosses 50 MW. Read Reeves 3's 2044 date and every PNM retirement date.
- **El Paso Electric.**
  - Rio Grande 6 is retired 2025 in EIA, abandonment was approved in case 20-00194-UT, and GEM still says operating. Status change with two publishers.
  - Rio Grande 7 abandonment (case 23-00403-UT, asked for 2026-01-01).
  - Rio Grande 8 (2033).
  - The Sierra Club list's "Rio Grande CT G10", 87 MW, terminated: find a public source and say what it was.
  - The 2026 RFP (100 to 400 MW by 2030) is a watch item until a gas bid is named.
- **NTEC gas plant.** The EPA Region 9 final permit decision, the 742 MW total against GEM's 1,089 MW (18 times 60.5), and the unit naming (GEN13-18 as one row of 363 MW is a unit-naming problem to raise as a question).
- **Westside** (Saddle Butte, Kirtland). The NMED application from September 2025 lists 16 engines, while GEM and EIA list 3. Get engine count, capacity per engine and construction evidence.
- **Lea County Data Center** (New Era Energy & Digital), **Roswell Information Park** (E2B4, Sustany, 700 MW, an offer on a 736 MW plant) and **Site Layer 1** (Grant County, Wärtsilä engines; the county passed a data center moratorium 4-1). Check permits, county records and filings for each. A two-year-old announcement with nothing new is an inferred-status question, not a deletion.
- **Zenith Volts data center** (Chaves County, 1.24 to 1.3 GW load, county approval August 2025, gas generators named but no MW): an add if a document gives gas generation; otherwise a watch item with case `no_generation_named`.
- **Google's Lea County data center** (1,890 acres near Hobbs, power plan not final): a watch item until a document names gas generation.
- **Meta Los Lunas** (Greater Kudu LLC, Valencia County; 22 diesel emergency engines in an NMED notice). Sum the fleet's nameplate from the permit. At 50 MW or more it is an add with Backup Power yes.
- **Santa Teresa data centers** (one hyperscale and one enterprise in NMED's July 2026 legislative deck). Name them and check APMAP.
- **Project Jupiter.** Confirm the cancellation has two publishers and a dated step, and run the backup fleet check (see Decisions). The EIP "YGI Microgrid" id goes to a question.
- **Cleanview queue leads** (Hobbs 160 MW 2029, Kirtland 180 MW 2030, Bloomfield 60 MW 2027). Each is answered from the SPP CSV or the LBNL file, never cited from Cleanview alone.
- **Clean Path Energy Center** (cancelled-inferred). Amalia found the site reused; confirm with two publishers or keep the inferred status.
- **Ownership checks.** Hobbs Generating Station (Lea Power Partners or SPS; check EIA-860 schedule 4 and the commission record). Lordsburg's owner is "PNM Resources Inc"; check that the operating company, Public Service Company of New Mexico, is the right entity. Luna's three owners.
- **Every EIA plant missing from GEM** in `work/ids_us-new-mexico.md` (gate `ids_followup`), every queue row in `needs_answer` (gate `queues`), every data center site `data_center_fleets.py` lists (gate `data-centers`), and every resource plan (gate `irp-plans`).

## The run

A. **Start and build.**
   - From `scripts/`: fresh pull, `pull_gem_db.py --map-only`, `scope_filter.py`, `export_to_dump.py`.
   - Check Amalia's latest edits against the 2026-11-17 list above and record what changed in this plan.
   - Run `worklist.py --state "New Mexico"`, `validation_report.py --state "New Mexico"`, `assigned_comments.py`, `no_tracker.py`, `eia860m.py`, `match_ids.py`, `irp_sheet.py`, `captive_lng.py` and `location_candidates.py`.
   - Write `scopes/us-nm/note.md` updates, `coverage.json` (every source above, each probed live, with `permit_record`, `permit_notices` and `local_records` roles), `queues.json`, `irp_plans.json` and `batches/us-nm/extra_tasks.json`.
   - Settle the open probe items: PNM and Tri-State queues, the Coda export, Lea County AgendaCenter, Valencia, Bernalillo, Las Cruces and Sandoval paths, the SOS search, the nmpress search, and article routes.
   - Build the three harvesters with tests.
   - Run `access_check.py --scope us-nm` and fix or wall every unproven entry.
B. **Harvest.**
   - `scopes/us-nm/harvest_permits.py`, `harvest_prc.py` and `harvest_local.py`.
   - `pull_queues.py --state NM`, then `data_center_fleets.py --state "New Mexico"`.
   - `irp_plans.py --state "New Mexico"`.
   - `check_existing_links.py --state "New Mexico" --batch batches/us-nm`.
   - `access_audit.py batches/us-nm --retry`.
C. **Briefs and sweep.**
   - `build_state_brief.py --state "New Mexico" --mode update --scope all --batch batches/us-nm --worklist work/worklist_us-nm.csv --extra-tasks batches/us-nm/extra_tasks.json --validation work/validation_us-new-mexico.json --ids work/ids_us-new-mexico.json --irp work/irp_us-new-mexico.json --captive work/captive_us-new-mexico.json --location work/location_us-nm.json --existing-links batches/us-nm/existing_links.json --harvest batches/us-nm/harvest --data-centers`.
   - `build_sweep_args.py --batch batches/us-nm`.
   - The `state-sweep` workflow: Sonnet per plant or plant group, and Opus for the scope-wide agent. The scope-wide agent reads `briefs/_irp.md`, every plan in `irp_plans.json`, the queue answers, the data center list, the local records index and every statewide `coverage.json` entry, recording `read` and `date` for each.
D. **Location.** Run the seven candidates, plus any plant handed back with `location_needs_review: true`, through `docs/reference/location.md`. Then `build_sweep_args.py --location-review` for the short Opus pass.
E. **Assemble and gate.**
   - `assemble_state.py --batch batches/us-nm` and `dedup_check.py --batch batches/us-nm`.
   - `state_gate.py --batch batches/us-nm --validation work/validation_us-new-mexico.json --entity-check --strict-questions --strict-proof`.
   - `qc_checks.py --staged` with zero errors.
   - `entity_lookup.py` for Tri-State, Greater Kudu LLC, Zenith Volts and each project LLC.
F. **Deliverables and page.**
   - `build_review_package.py --staging-dir batches/us-nm/staging --scope us-nm --mode update --irp` with a fresh stamp.
   - Add `batches/us-nm/staging` to the `new-york-maryland` page dirs, then `review_app/build_all.py --only new-york-maryland`.
   - Publish to https://claude.ai/artifact/7bnX9RMity3Yw5mdaojNaL from the work profile, then `build_all.py --mark-published new-york-maryland`.
G. **Drafts for a person.**
   - IDs to type: Lordsburg EIA 7967, Pyramid's codes once added, and the Project Jupiter EIP id.
   - The EIP sheet row to paste, the IRP boxes to tick and the Notes lines per utility.
   - Clerk emails for any county with nothing posted, the RBLC export and any LLC lookups the SOS wall leaves.
   - The close-out checks before the roster row moves: `validation_report.py --closeout` prints CLOSE-OUT CLEAN and `assigned_comments.py --closeout` prints COMMENTS CLEAN.

## What done looks like

- Every one of the 52 rows has a record or a re-verification, and every in-development unit has a dated status step and a Latest Activity.
- Every lead above is a record or a coverage answer.
- Every `coverage.json` entry carries `read` and `date` or a human wall.
- Every queue request, missing EIA plant, data center site, resource plan and dedup hit is answered.
- The gates pass with `--strict-proof`, and `qc_checks.py --staged` is clean.
- The deliverable pair is built with a fresh stamp, and Amalia's page is rebuilt and published with New Mexico on it.

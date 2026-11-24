# Kentucky update plan

Kentucky is a full-state update for Baird's own review page, planned 2026-11-04 on the Oklahoma pattern (`scopes/us-ok/plan.md`): every plant in the scoped export, every lead, every permit, every commission filing, every council and fiscal court record, every news story, read and cited or answered. The scope folder holds `note.md` (inlined into every brief), `coverage.json` (the statewide source list, 48 entries, each probed live before it was listed), `queues.json` (the PJM and MISO settings with the probed matches), `extra_tasks.json` under `batches/us-ky/` (36 tasks from the export, the IRP tab and the ID join), and this plan.

## Decisions (settled by Baird 2026-11-04)

- The batch stages into Baird's own review page (the `baird` page in `review_app/artifacts.json`, reviewer Baird Langenbrunner, https://claude.ai/artifact/8C7yTha7YC2eYUdWxJ5Eik); add `batches/us-ky/staging` to that page's dirs before the rebuild. Nothing goes to Amalia's New York and Maryland page.
- Mode is `update`, every plant, in-development units first (the manual's ladder through `worklist.py`), then planned retirements (Big Sandy 1 in 2041, Green 1 and 2 in 2029), then mothballed (Marshall CT4 to CT8), then the operating rest.
- Persistence is the rule: a search form, a portal, a paged table or a bot challenge is never "blocked"; it is scripted (the harvesters below) or read through the fetch ladder, and only a sign-in wall is a human wall, written in `coverage.json` as a sentence that says what a person does.
- Models per step follow the dispatch rule in `docs/workflows.md`: harvesters and the cheap sweep on Sonnet, the location review and the scope-wide pass on Opus or Fable, assembly and gates in the main loop.

## What the export already shows (2026-11-04 pull)

72 scoped rows at 23 plants. In development (16 units, 7,895.9 MW): BREC 2023 IRP power station 1 (announced, 635 MW), Cooper 2 second timepoint (pre-construction, 225) and Cooper 3 (pre-construction, 745; construction commencement notice filed October 30, 2026), E.W. Brown 12 (pre-construction, 681), East Bend 3 (announced, 664) and East Bend 2 second timepoint (pre-construction, 600, retire 2038), Elmer Smith 1 (announced, 545; Green River East GenCo), KPCO 2023 IRP power station 1 (announced, 480; superseded by case 2026-00324), KYMEA Energy Center I 1 (construction, 75.2), Liberty Station 1 (construction, 217.2), Mill Creek MC5 (construction, 740) and MC6 (pre-construction, 680), Spurlock 1 to 4 second timepoints (pre-construction, 357.6, 592.1, 329.4, 329.4). Planned retirements: Big Sandy 1 (280.5 MW, 2041), Green 1 and 2 (293 MW each, 2029). Mothballed: Marshall CT4 to CT8 (86 MW each). Every Latest Activity is blank. The validation report lists 22 fix items (undated status-history steps on every in-development unit and on Marshall CT4 to CT8; Elmer Smith's location has no data source) and 105 optional coal-side items. Location candidates: the two IRP placeholders. Captive LNG: none. No-tracker units: none. Assigned comments: none open. The possible-updates sheet's Kentucky rows are all marked done. The unfiltered export also carries Hawesville Mill (88 MW bioenergy and gas) and Shawnee 1 to 9 (coal, retire 2035), kept visible for the conversion and shared-site checks.

## State context the sweep needs

See `note.md`: four grids (PJM, MISO, the LG&E and KU balancing area, TVA); the Public Service Commission for the five regulated utilities and the siting board for merchant plants; the Division for Air Quality's eSearch record outside Jefferson County and the Louisville APCD inside it; seven utilities and three merchant owners; the data center cases.

## Access, probed 2026-11-04

Every entry in `coverage.json` was opened live before it was listed. Plain fetch works for the commission (year lists, filings pages, both PDF stores, the siting board, the UMS directory), DAQ notices and draft permit PDFs, the eSearch API (JSON POSTs and the document download), PJM's planning XML and cycle POST, MISO's JSON, ECHO, CAMPD with the demo key, EIA, LG&E and KU, PPL, Kentucky Power, Duke, EKPC, Big Rivers, KYMEA, Middle River, NRG, kypublicnotice.com and the Secretary of State search, and most county sites. The browser-fingerprint route is needed for Louisville APCD, tva.com, omu.org, Kentucky Lantern, NKyTribune, louisvilleky.gov planning pages and Union County; the full Chrome page load for Louisville Business First, WHAS11 and webstercountyky.com; `fetch.py --render` for the Gannett and McClatchy papers (402); `insecure` for paducahpower.com and both OASIS sites. Louisville's Legistar has an open JSON API, Madisonville's CivicClerk an open OData API; CivicPlus AgendaCenter sites (Henderson, Clark, Marshall, Hardin) follow one file pattern; Revize sites (Owensboro, Maysville, Mason, Boone, Elizabethtown) post PDFs under Documents paths; several counties post scans that need OCR. Dead or wrong hosts found and replaced: caseycountyky.gov, hopkinscounty.net, madisonvilleky.gov, mercercountyky.gov, web.sos.ky.gov, kypublicnotices.com, ompc.org, bigrivers.com/press-releases (500).

## Access proof, run 2026-11-04

See the "Access proof result" section at the end of this plan, written after `python scripts/access_check.py --scope us-ky` ran; `batches/us-ky/access_proof.json` is the record and `scopes/us-ky/work/access/` holds the samples.

## Human walls

Each is a `human_wall` sentence in `coverage.json`; no script signs in with Baird's credentials.

- CAMPD: a real API key (free registration) for the full annual pull; the demo key proves the service.
- RBLC: the determination search runs only in a browser; Baird exports the Kentucky table.
- TVA OASIS and LGEE OASIS: OATI accounts; a request number is read by a person only if it matters.
- County minutes not posted online (Lawrence, Casey, Mercer, Trimble, Muhlenberg, Hancock, Hopkins, Bullitt, Christian): an email to the county clerk; the Warren County Google Drive folders and the Owensboro, Paducah and Hopkinsville Laserfiche portals opened by a person.
- The DAQ notice email list (AIRKentucky@ky.gov) and an open records request to Louisville APCD (apcd@louisvilleky.gov) for superseded permits.

## Manual rules the run must follow

The repo CLAUDE.md hard requirements, plus the ones Kentucky leans on: a project GEM lacks is added on one verified source (a queue row, a commission application, a permit, a council packet), with the status from the manual's ladder; a status change is green only on two independent publishers (the commission order and the utility's release count as two; the application and the order in the same case count as one filer and one regulator, which is two); a combined cycle block is one unit (Cooper CC1, the Lawrence County block, Mill Creek 5 and 6, Brown 12); a data center backup fleet at 50 MW summed nameplate is an add with Backup Power yes; electrical nameplate only (Domtar's 52 MW cogeneration counts, compressor drives do not); Status Detail and Notes additive, newest on top, Status Detail carrying its own links; owner on every add (Green River East GenCo, LLC at 100 percent until a parent is named); the conversion-year convention on every second-timepoint row (Cooper 2, East Bend 2, Spurlock 1 to 4, Big Sandy 1, Green 1 and 2); start year never on shelved or cancelled; retired year never on mothballed; Wayback copies citable; gem.wiki never cited; Sierra Club reference only.

## Guardrails, built first

1. **Coverage gate.** `coverage.json` names two `permit_record` entries (DEP eSearch statewide, Louisville APCD for Jefferson County), two `permit_notices` entries (DAQ notices, APCD proposed actions) and one `local_records` entry whose `what` says the records are opened for every lead and every in-development plant; `state_gate.py` gates `permit-system`, `local-records` and `statewide-coverage` (every entry searched with `read` and `date`, or truly blocked) run on every build.
6. **Access proof, before anything else reads the web:** `python scripts/access_check.py --scope us-ky` opens every entry, checks the body is what the proof promises, saves a sample under `scopes/us-ky/work/access/` and writes `batches/us-ky/access_proof.json`. Gate `access-proof` fails the batch when the proof is missing or over seven days old, or when an unproven entry has no `human_wall` sentence.
2. **Harvesters** (below) run before the briefs, so every permit, docket and queue row is on the brief as a fact, not a search task.
3. **Existing-link check:** `check_existing_links.py` runs every Data Source link in the 72 rows through the ladder and Wayback, stages saved copies and turns the rest into brief tasks.
4. **Existing rules:** `qc_checks.py --staged` zero errors; every gate in `state_gate.py` (access-proof, statewide-coverage, permit-system, local-records, chase, ids_followup, dedup, queues, data-centers, validation, location, additive, questions, watch-case, access, unit-names, headers); `url_verifier.py` on every URL.
5. **Access audit:** `access_audit.py --retry` re-runs every give-up the harvesters and the sweep tagged `us-ky`; gate `access` fails on an unretried give-up or an excuse note.

## New tooling

- `scopes/us-ky/harvest_permits.py` (built 2026-11-04, on `scripts/harvest_lib.py`): searches the DEP eSearch API for every GEM plant and every lead by name, by known agency interest id and by county, issued and pending approvals with Program Air; downloads each approval's documents under `scopes/us-ky/work/permits/docs/<agency id>/` and extracts them; reads the DAQ notices page and both Louisville APCD pages through `cf_impersonate`; writes `scopes/us-ky/work/permits/<plant_id>.md` and `.json`. Give-ups are tagged `us-ky` through `report_failure`. Tests in `tests/test_harvest_permits_kentucky.py`.
- `scopes/us-ky/harvest_psc.py` (built 2026-11-04): reads the commission's year list for 2021 to 2026 and keeps every case about gas or oil generation, a resource plan, a retirement, a conversion or a data center; adds the cases this plan names and the siting board's merchant plant list (the Category 8 search answers 500); reads each case's filings, Public, Hearings and Post tabs; downloads the order, the application and the reports that matter into `scopes/us-ky/work/psc/<case>/`; matches cases to plants and writes `batches/us-ky/harvest/psc_dockets.json` in the `build_state_brief.py --harvest` contract. Tests in `tests/test_harvest_psc_kentucky.py`.
- `scopes/us-ky/harvest_local.py` (built 2026-11-04): lists every agenda, packet and minutes file since 2024-01-01 for the bodies in its `BODIES` list (Louisville Legistar bodies 138, 195, 196, 139, 154, 165, 333 and 180; Madisonville CivicClerk; AgendaCenter for Henderson County, City of Henderson, Clark, Marshall, Hardin and Boyd; the WordPress media API for Pulaski, Daviess and Somerset; index pages for Mason, Maysville, Harrodsburg, Oldham, Boone, iompc.org, Elizabethtown and McCracken); reads each file, with OCR for scans; records by plant the sentences naming a plant, a lead, a power or data center project or a rezoning, bond or tax deal; writes `scopes/us-ky/work/local/<body>/` and `batches/us-ky/harvest/local_records.json` and `.md`. Bodies with no posted minutes go to its `not_posted` list, the human wall. Tests in `tests/test_harvest_local_kentucky.py`.
- `pull_queues.py --state KY` with `scopes/us-ky/queues.json` (PJM and MISO readers exist; the LGEE and TVA areas are answered as `market LGEE` and `market TVA`).
- `irp_sheet.py` aliases if the "US IRPs" tab names differ from the export (Kentucky Power, EKPC, LG&E and KU, Big Rivers, KYMEA, OMU, TVA); check with `irp_sheet.py --state Kentucky` first.
- `fetch.py` host rules in `work/fetch_routes.json` for louisvilleky.gov, tva.com, omu.org, kentuckylantern.com, nkytribune.com, unioncountyky.org (`cf_impersonate`), bizjournals.com, whas11.com, webstercountyky.com (full Chrome page load), courier-journal.com, kentucky.com, thegleaner.com (`--render` on 402), paducahpower.com and oasis.oati.com (`insecure`), pulaskigov.com, mccrackencountyky.gov and kypublicnotice.com (Chrome User-Agent). `docs/reference/site_access.md` gets a Kentucky row for each.
- `data_center_fleets.py --state Kentucky` after the permit harvest, then `build_state_brief.py --data-centers`.

## Known leads the run must settle (each becomes a record or a coverage answer)

- Kentucky Power's Lawrence County combined cycle (case 2026-00324, notice of intent October 30, 2026; PJM C01-1131 and C01-1325 at Baker 345 kV; the Big Sandy News public notice of October 7, 2026): rename or replace the KPCO 2023 IRP placeholder; capacity, turbine model, schedule from the application.
- EKPC's Mason County request (PJM C01-1227, 758 MW gas, Spurlock to Meldahl Dam 345 kV): a new plant or new Spurlock unit on the queue row alone; chase the commission and the eSearch record for more.
- Green River East GenCo at Elmer Smith (545 MW; the OMU board record, the siting board, the Secretary of State profile, the Owensboro Times story): owner, status, the lease or sale, the siting certificate.
- Big Rivers 2026 IRP (2026-00268) against the BREC 2023 IRP placeholder; the Reid combustion turbine retirement and Green backup fuel (2026-00291).
- Cooper CC1 (construction commencement notice October 30, 2026 in the 2024-00370 Post tab): construction status on two publishers; the Cooper 2 co-firing date.
- Liberty Station (groundbreaking May 20, 2026; permit V-25-006; EIA's twelve planned 18.1 MW engines for 2028; EIA 69726 to add): construction, 217.2 MW, start year.
- KYMEA Energy Center I (permit V-25-010; MISO S1073; Madisonville council record): construction, 75.2 MW, 2027.
- Mill Creek 5 and 6, Brown 12 (2025-00045; APCD construction permits; the 2026 application to run Mill Creek 2 longer): statuses, years, Mill Creek 2's retirement year.
- East Bend 2 diesel co-firing 2030 and unit 3 combined cycle 2039 (Duke IRP 2024-00197).
- Spurlock 1 to 4 co-firing (EKPC IRP 2025-00087; eSearch agency interest 3004).
- Bluegrass Title V revision V-21-048 R1 (draft at notice to November 27, 2026).
- The Meta data center in Mason County (public notice October 23, 2026, gas turbine or small reactor), the TeraWulf sites (2026-00115, 2026-00323), the PPL and Blackstone Louisville sites, every other campus `data_center_fleets.py` lists.
- Domtar Hawesville 52 MW cogeneration (2023-00312) and the other industrial sites in the `industrial-cogeneration` entry.
- Big Sandy Peaker's state (EIA says West Virginia).
- Marshall CT4 to CT8 operation (CAMPD hours) and the undated mothball steps.
- J K Smith nameplates (EKPC annual report, EIA-860).
- Every EIA plant missing from GEM in `work/ids_us-kentucky.md` (gate `ids_followup`), and every queue row in `needs_answer` (gate `queues`).

## The run

A. **Start.** From `scripts/`: fresh pull, `pull_gem_db.py --map-only`, `scope_filter.py`, `export_to_dump.py`; `worklist.py --state Kentucky`; `validation_report.py --state Kentucky` to `work/validation_us-kentucky.json`; `assigned_comments.py --state Kentucky`; `no_tracker.py --state Kentucky`; `eia860m.py` then `match_ids.py --state Kentucky`; `irp_sheet.py --state Kentucky`; `irp_plans.py --state Kentucky` (every plan in `scopes/us-ky/irp_plans.json`, read in full and answered under `irp_plans`); `captive_lng.py --state Kentucky`; `location_candidates.py --state Kentucky`; `check_existing_links.py --state Kentucky`; `python scripts/access_check.py --scope us-ky` (fresh, under seven days).

B. **Harvest.** `scopes/us-ky/harvest_permits.py`, `scopes/us-ky/harvest_psc.py`, `scopes/us-ky/harvest_local.py`, `pull_queues.py --state KY`, `data_center_fleets.py --state Kentucky`; `access_audit.py --retry` on the give-ups.

C. **Briefs and sweep.** `build_state_brief.py --state Kentucky --mode update --scope all --batch batches/us-ky --worklist work/worklist_us-ky.csv --extra-tasks batches/us-ky/extra_tasks.json --validation work/validation_us-kentucky.json --ids work/ids_us-kentucky.json --irp work/irp_us-kentucky.json --captive work/captive_us-kentucky.json --location work/location_us-ky.json --existing-links batches/us-ky/existing_links.json --harvest batches/us-ky/harvest --data-centers` (the harvest folder carries the dockets, the queues and the local records, and each plant's brief gets its newest eight local records); `build_sweep_args.py --batch batches/us-ky`; the `state-sweep` workflow (one Sonnet agent per plant or plant group; the scope-wide agent on Opus reads `briefs/_irp.md`, `briefs/_captive.md`, the queue answers, the data center list, the local records index and every statewide entry in `coverage.json`, recording `read` and `date` for each).

D. **Location pass.** The two placeholders and any plant handed back with `location_needs_review: true` go through the ladder in `docs/reference/location.md` (`geocode.py`, `site_image.py`, `georef.py`); `build_sweep_args.py --location-review` for the short Opus pass.

E. **Assemble and gate.** `assemble_state.py --batch batches/us-ky`; `dedup_check.py --batch batches/us-ky`; `python scripts/state_gate.py --batch batches/us-ky --validation work/validation_us-kentucky.json --entity-check --strict-questions --strict-proof`; `qc_checks.py --staged` zero errors; `entity_lookup.py` before any new owner (Green River East GenCo, LLC; the Lawrence County project company; each data center entity).

F. **Deliverables.** `python scripts/build_review_package.py --staging-dir batches/us-ky/staging --scope us-ky --mode update --irp` with a fresh stamp; add `batches/us-ky/staging` to the `baird` page in `review_app/artifacts.json`; `review_app/build_all.py --only baird`; publish to https://claude.ai/artifact/8C7yTha7YC2eYUdWxJ5Eik from the work profile; `build_all.py --mark-published baird`.

G. **Drafts for a person.** The IDs to type into Other IDs (Liberty EIA 69726, Reid GEN2, Cooper's EIP id, the EIA codes for Cooper, East Bend, Elmer Smith and Spurlock that are coal-only today), the IRP boxes to tick and the Notes lines per utility (`irp_box`, `irp_notes_draft`), the clerk emails for the counties with no posted minutes, the RBLC export, and the `validation` close-out and `COMMENTS CLEAN` checks before the roster row moves.

## What done looks like

Every one of the 72 rows has a record or a re-verification; every in-development unit has a dated status step and a Latest Activity; every lead above is a record or a coverage answer; every entry in `coverage.json` carries `read` and `date` or a human wall; every queue request in `needs_answer`, every EIA plant missing from GEM, every data center site, every dedup hit and every validation fix item is answered; the gates pass with `--strict-proof`; `qc_checks.py --staged` is clean; the deliverable pair is built with a fresh stamp; the review page is rebuilt and published; the roster row stays open until the close-out prints CLOSE-OUT CLEAN and COMMENTS CLEAN.

## Access proof result (2026-11-04, 17:02 local)

`python scripts/access_check.py --scope us-ky`: 48 of 48 sources proven, none behind a person's action. Routes that worked: plain curl for 33 entries (the commission's year list, filings page, both PDF stores, the IRP motion, the siting board and the UMS directory; DAQ notices and the Bluegrass draft; the eSearch document download; PJM's 23 MB queue XML; MISO's 2.4 MB JSON; ECHO, CAMPD, RBLC, EIA, EIP; LG&E and KU, PPL, Kentucky Power, Duke, EKPC, Big Rivers, KYMEA, Paducah Power, Middle River, NRG; the Secretary of State search; kypublicnotice.com; the Louisville Metro Council action summary PDF), a direct POST for the eSearch issued-approvals search (JSON) and the PJM cycle list, the browser-fingerprint route for the three Louisville APCD entries, omu.org, the three tva.com entries and Kentucky Lantern, the full Chrome page load for the data center search, the declared-identity route for EDGAR, the work gws profile for the two Google Sheets, and certificate verification off for the two OASIS sign-in pages (listed with human walls). The two `permit_record` entries, the two `permit_notices` entries and the `local_records` entry all proved. Samples are under `scopes/us-ky/work/access/`; the record is `batches/us-ky/access_proof.json`.

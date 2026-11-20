# New Mexico: things a person does by hand

Written 2026-11-18 for the New Mexico batch. Nothing here was done by a script. Each item says where to do it.

## IDs to type into the web form

These have no Data Source and are not part of the review page. Type them into Other IDs, keeping what is already there.

- Lordsburg Generating Station (L100001083303): add `EIA: 7967` at the plant level. The EIA-860M file for September 2026 lists plant 7967 "Lordsburg Generating" in Hidalgo County at GEM's coordinates.
- Pyramid Generating Station (new plant in this batch): once the plant exists, add `EIA: 7975`. The same EIA file lists plant 7975 "Pyramid", Tri-State, four 46.5 MW gas turbines.
- Project Jupiter Microgrid power station (L100001080450): add the Environmental Integrity Project facility id `107ebccf-3e9e-48b1-a8d6-d5a09af92d7a` only if you agree that its "YGI Microgrid" record is this plant. The batch has a question on it.

## EIP sheet row to paste

On the EIP tab "EIP 07/28/26 data filtered", the YGI Microgrid row (facility id `107ebccf-3e9e-48b1-a8d6-d5a09af92d7a`, proposed, 2,462 MW) has a blank GEM id. Paste `L100001080450` as the location id. Leave the unit id blank, since GEM has two units and the EIP row is one facility. This is a medium-confidence match by name, so skip it if you reject the Project Jupiter question.

## IRP boxes and Notes lines

Both are in the actions workbook, [gogpt_batch_20261119_1947_ET_us-nm_update_actions.xlsx](deliverables/gogpt_batch_20261119_1947_ET_us-nm_update_actions.xlsx).

- The `irp_box` sheet lists each unit whose box to tick. The units not yet ticked are Afton CC1, Lordsburg GT1 and GT2, Reeves 3, Rio Bravo GT1 and Rio Grande 7. Every new row from a plan also gets the box when it is created: La Luz Energy Center and Reeves units 1, 2 and 4.
- The `irp_notes_draft` sheet has one Notes line per utility for the "US IRPs" tab. The tab still shows the 2023 plans for PNM and Southwestern Public Service. PNM filed its 2026 plan on 2026-09-01 in case 25-00022-UT, and Southwestern Public Service filed its 2026 plan on 2026-10-23 in case 25-00076-UT. Three utilities are not on the tab at all: Tri-State (2023 Electric Resource Plan), the Farmington Electric Utility System (2022) and Los Alamos County (2022). El Paso Electric's 2025 plan is already there.
- Southwestern Public Service's 2026 plan has no public copy a link can point to. Xcel's plan page sends the file through a Salesforce viewer that gives no text. Only the commission case copy exists, so the plan link on the tab is the case number.

## Done by script on 2026-11-19

These were on this list before. Nothing is left for a person.

- The three Air Quality Bureau tables on Coda were read in full in Chrome by `scopes/us-nm/coda_browser.py` and the permit harvester reread them. The 11 oil field power sites they added were checked against their permit files. All are under 50 megawatts. The two Devon Todd pads, 600 meters apart and about 75 megawatts together, are a watch item.
- The EPA RACT/BACT/LAER Clearinghouse was read through its own data service: 252 New Mexico entries, none newer than 2014.
- The Albuquerque Development Commission's older records were read through the OnBase search service: 168 documents, no power project.
- The TC NM Development microgrid notice is described in two Valencia County News-Bulletin articles, which the watch item now cites. It is a fuel cell plant, which is out of scope.
- Valencia County's agenda packets were read from its public Google Drive folder, so no email to the clerk is needed. Lea County has no plant in development or add in this batch, so that email is dropped too.
- The Secretary of State company lookups are not needed. Every owner staged is named in a primary document.

## Close-out checks, after the edits are in the database

The roster row moves to done only after both of these pass. Neither can pass until the accepted edits are applied.

- `python scripts/validation_report.py --state "New Mexico" --closeout` prints CLOSE-OUT CLEAN.
- `python scripts/assigned_comments.py --state "New Mexico" --closeout` prints COMMENTS CLEAN.

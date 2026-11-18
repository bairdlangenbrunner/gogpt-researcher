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

Both are in the actions workbook, [gogpt_batch_20261118_1017_ET_us-nm_update_actions.xlsx](file:///Users/baird/Dropbox/_git_ALL/_github-repos-gem/gogpt-researcher/batches/us-nm/deliverables/gogpt_batch_20261118_1017_ET_us-nm_update_actions.xlsx).

- The `irp_box` sheet lists each unit whose box to tick. The units not yet ticked are Afton CC1, Lordsburg GT1 and GT2, Reeves 3, Rio Bravo GT1 and Rio Grande 7. Every new row from a plan also gets the box when it is created: La Luz Energy Center and Reeves units 1, 2 and 4.
- The `irp_notes_draft` sheet has one Notes line per utility for the "US IRPs" tab. The tab still shows the 2023 plans for PNM and Southwestern Public Service. PNM filed its 2026 plan on 2026-09-01 in case 25-00022-UT, and Southwestern Public Service filed its 2026 plan on 2026-10-23 in case 25-00076-UT. Three utilities are not on the tab at all: Tri-State (2023 Electric Resource Plan), the Farmington Electric Utility System (2022) and Los Alamos County (2022). El Paso Electric's 2025 plan is already there.
- Southwestern Public Service's 2026 plan has no public copy a link can point to. Xcel's plan page sends the file through a Salesforce viewer that gives no text. Only the commission case copy exists, so the plan link on the tab is the case number.

## Company lookups on the Secretary of State site

The business search at https://enterprise.sos.nm.gov/search/business is behind a Cloudflare check no script passes. For each company below, paste the registered name, formation date and principal office into its question on the review page.

- Greater Kudu LLC (Greater Kudu Los Lunas data center, Valencia County).
- Zenith Volts Infrastructure LLC (Zenith Volts Roswell data center, Chaves County).
- TC NM Development (the November 2026 microgrid notice).
- Site Layer 1 LLC (Site Layer 1 data center, Grant County).

## Pages a person opens

- The TC NM Development microgrid notice on https://www.newmexicopublicnotices.com/. The full text opens only after a Cloudflare check. Copy the site, the fuel, and the engine or turbine count into the watch item for that microgrid.
- The three Air Quality Bureau tables on Coda: Current Permitting Actions Under Review, the NSR Issued Report, and the Facilities Lat Long Report. Export each as CSV into `scopes/us-nm/work/permits/coda/`, then rerun `scopes/us-nm/harvest_permits.py` so every row is read.
- The EPA RACT/BACT/LAER Clearinghouse at https://cdxoarapps.epa.gov/oar-rblc/?tabIndex=0. Run the New Mexico search, export the table, and save it under `scopes/us-nm/work/rblc/`.
- The Albuquerque Development Commission's records before July 2026, in the city's OnBase portal at https://onbase.cabq.gov/publicaccess/?CQID=136.

## Emails to county clerks

Lea, Luna and Hidalgo counties post no agendas or minutes online, and Valencia County keeps its agendas after May 2025 in a Google Drive folder that no script can list. Lea and Valencia hold projects in development, so those two emails are drafted. Send them from your own address.

**To the Lea County Clerk**

Subject: request for commission records on two power projects near Hobbs

Hello,

I research power plants for Global Energy Monitor, a nonprofit that tracks energy infrastructure. Could you send me, or point me to, any county commission or planning records from 2025 and 2026 on these two projects?

- A data center in Lea County with its own gas-fired generation, which may appear under a developer or project company name.
- A 234 MW gas combustion turbine that Southwestern Public Service plans near Hobbs, tied to a Hobbs to Andrews 345 kV line.

Agendas, minutes, zoning or special use permits, industrial revenue bond resolutions and development agreements would all help. Thank you.

**To the Valencia County Clerk**

Subject: request for commission records on power projects near Belen and Los Lunas

Hello,

I research power plants for Global Energy Monitor, a nonprofit that tracks energy infrastructure. Could you send me the county commission and planning commission agendas and minutes from June 2025 to now, or a link to the folder that holds them? I am looking for records on these projects:

- The Greater Kudu data center near Los Lunas and any gas-fired generation planned for it.
- PNM's La Luz Energy Center near Belen, including a second gas unit.

Zoning or special use permits, industrial revenue bond resolutions and development agreements would all help. Thank you.

## Close-out checks, after the edits are in the database

The roster row moves to done only after both of these pass. Neither can pass until the accepted edits are applied.

- `python scripts/validation_report.py --state "New Mexico" --closeout` prints CLOSE-OUT CLEAN.
- `python scripts/assigned_comments.py --state "New Mexico" --closeout` prints COMMENTS CLEAN.

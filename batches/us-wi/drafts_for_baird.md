# Wisconsin: things a person does by hand

Written 2026-11-19 for the Wisconsin batch. Nothing here was done by a script. Each item says where to do it.

## IDs to type into the web form

These have no Data Source and are not part of the review page. Type each into Other IDs, keeping what is already there.

- Red Oak Ridge Energy Center (L100001062057): add `EIA: 70453` at the plant level. The September 2026 federal generator file lists plant 70453 in Kenosha County, 0.9 km from GEM's point, with five 242 MW gas turbines planned for 2029.
- Riverside energy center (WI) (L100000401640): add `EIA: 64020`, and keep `EIA: 55641`. The file lists the three Riverside generators under plant 64020 "West Riverside Energy Center" in Rock County.
- South Oak Creek Combustion Turbine Project (L100001025603): add `EIA: 4041`, and keep the two EIP codes. The file lists plant 4041 in Milwaukee County with five 236.3 MW gas turbines planned for 2028.
- Weston Power Plant: do not add 4130. That plant is New Lisbon in Juneau County, 116 km away.
- Fitchburg power station (new plant): once it exists, add `EIA: 3991`. Two 28.8 MW gas turbines, Madison Gas and Electric.
- Elk Mound power station (new plant): once it exists, add `EIA: 7863`. Two 35.5 MW gas turbines, Dairyland Power Cooperative.
- Red Oak Ridge units 1 to 5 and South Oak Creek units 1 to 5 have no EIA generator id. The file lists the generators (CT4, CT5, RDOR1 to RDOR3 at Red Oak Ridge; 11 to 15 at South Oak Creek) but cannot say which belongs to which unit. Leave them blank.

## IRP boxes and Notes lines

Both are in the actions workbook, [gogpt_batch_20261119_1324_ET_us-wi_update_actions.xlsx](./deliverables/gogpt_batch_20261119_1324_ET_us-wi_update_actions.xlsx).

- The `irp_box` sheet lists the units to tick: Paris RICE unit 1 and Weston unit 4 (timepoint 2). Tick the box on each new plant that came from a plan when it is created. Three watch items have no unit yet.
- The `irp_notes_draft` sheet has one Notes line for each of eight utilities for the "US IRPs" tab. None of the seven beyond WEC Energy Group is on the tab: the state commission's draft energy assessment, WEC's two operating companies, Wisconsin Power and Light, Madison Gas and Electric, Xcel's Wisconsin company, Dairyland and WPPI Energy. Add a row for each.
- Three files were not found. Dairyland's own plan, WEC's November 2026 investor deck and Alliant's third quarter slides. The notes lines say so.

## Replies to the three open comment threads

Natalia Fretz holds all three. Post each in the database comment box. The close-out check prints COMMENTS CLEAN only after they are answered.

**Edgewater Generating Station, unit 5 start year (Jeanette Lim, 2026-03-31)**

Hi Jeanette, thanks for the Sheboygan Press link. Alliant's report for the quarter ended September 30, 2026 says Wisconsin Power and Light plans to keep running coal at Edgewater Unit 5 at least through 2030. I added that to Status Detail with the link. The start year stays as it is, because no document gives a firm gas date. Please check the 2029 in the March article against Alliant's own report before we change it.

**Weston Power Plant, unit 4 retirement year (Natalia Fretz, 2025-11-04)**

Hi Natalia, the 2030 retirement year was agreed in November 2025 and I did not change it. WEC's plan keeps coal only as a backup fuel after 2030, so the unit does not retire. I suggest we close this thread.

**Elm Road power station, unit 1 retirement year (Natalia Fretz, 2025-11-04)**

Hi Natalia, the 2028 conversion year from the commission document you cited is still the best source, and I made no change to it. In this batch I filled the capacity from the federal generator file (701.3 MW) and left a question on the other unit. I suggest we close this thread.

## Company lookups

The Wisconsin Department of Financial Institutions business search at https://apps.dfi.wi.gov/apps/CorpSearch/Search.aspx sits behind Cloudflare, and the detail page was not proven from a script. The question on Union Depot Energy Center LLC needs the registered name, formation date and principal office. Paste them into that question. Invenergy is already an entity used on seven units, so check there first and do not create a duplicate.

## Emails to local clerks

Janesville and Beloit post agendas in portals that list no meetings a script can read. Open them yourself for 2024 onward. They matter for the Riverside plant in Rock County and the Beloit plant.

Caledonia and Darien post nothing a script can use. Both have projects in development (Caledonia holds L100001089674, Darien holds Foundry Ridge, L100001047813), so both emails are drafted. Send them from your own address.

**To the Village of Caledonia clerk**

Subject: request for board and plan commission records on a power project

Hello,

I research power plants for Global Energy Monitor, a nonprofit that tracks energy infrastructure. Could you send me, or point me to, any village board or plan commission agendas, minutes, staff reports, zoning actions and development agreements from 2025 and 2026 on a gas-fired power project or a data center with its own generation in Caledonia? It may appear under a developer or project company name. Thank you.

**To the Village of Darien clerk**

Subject: request for board and plan commission records on the Foundry Ridge energy project

Hello,

I research power plants for Global Energy Monitor, a nonprofit that tracks energy infrastructure. Could you send me, or point me to, any village board or plan commission agendas, minutes, zoning actions and development agreements from 2024 to 2026 on the Foundry Ridge Energy Center, a planned gas-fired plant in Walworth County? Thank you.

## Pages a person opens

- The EPA RACT/BACT/LAER Clearinghouse moved to https://cdxoarapps.epa.gov/oar-rblc/ and has an open search, so no export is needed.
- Three meeting lists returned nothing to a script: the Town of Kronenwetter, the Madison Capital Area Regional Planning Commission and the Waukesha Committee of the Whole. Open each for 2025 and 2026.
- Brown County listed 297 documents but a script read only 25, and a later rerun failed to connect (status 000). Retry it, or open the county site in a browser.
- Milwaukee council file 260971, the Potawatomi data center expansion, gives no generator figure. Open the file and read the attachments.

## Close-out checks

Run these after the accepted edits are in the database.

- `python scripts/validation_report.py --state Wisconsin --closeout` must print CLOSE-OUT CLEAN. On 2026-11-19 it printed BLOCKED with 14 errors, which the batch's edits are meant to clear.
- `python scripts/assigned_comments.py --state Wisconsin --closeout` must print COMMENTS CLEAN. On 2026-11-19 it printed OPEN with 3 threads, the three above.

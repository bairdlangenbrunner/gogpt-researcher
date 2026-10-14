# United States — Alabama

Scope: 76 unit rows across 30 plants in the pull of 2026-10-09 (12 announced placeholder units on one IRP plant, 3 pre-construction, 59 operating, 2 retired). Assigned to Amalia Llano for the Q4 2026 cycle (status "to do", estimate a fifth of a day). The "US IRPs" tab has Alabama Power's 2022 and 2025 plans and a Southern Company row; no captive LNG sheet rows. First run as a state research pass in update mode on 2026-10-09.

## State context

- No independent system operator. Alabama Power (a Southern Company subsidiary) runs its own balancing area and does its own resource planning every three years, reviewed with the Alabama Public Service Commission. PowerSouth Energy Cooperative owns its own plants (Lowman, McIntosh, McWilliams) and its load is folded into Alabama Power's dispatch. The Tennessee Valley Authority serves north Alabama and is federally owned, so its plants (Colbert) have no Alabama commission orders.
- Alabama Power resource plans: the 2022 plan (alabamapower.com, IRP.pdf) proposed 780 MW of combustion turbines to cover retiring Gaston units 1 to 4 by the end of 2028, Barry unit 4 repowered to gas only, Barry unit 5 off coal by the end of 2028, and Gaston unit 5 to gas only by the end of 2028. The 2025 plan (2025-irp.pdf) names no new gas plant; it says near-term needs are covered by resources already certified and keeps the Barry 5 and Gaston 5 dates. Southern Company said in 2026 that Alabama Power has requests for proposals out, mostly for company-owned gas, with selections expected by the end of 2026.
- The commission's filings are in its public access portal (pscpublicaccess.alabama.gov). Docket 32953 is the 2020 certificate case for Barry unit 8, the Central Alabama purchase and the Hog Bayou power purchase agreement. Docket 33513 covers Gaston (subject not confirmed). New plants and purchases need a certificate of convenience and necessity.
- Air permits: the Alabama Department of Environmental Management's eFile system (app.adem.alabama.gov/eFile), searchable by facility name and county. Draft permits get a 30 day comment period and are posted under adem.alabama.gov/sites/default/files/.
- Alabama Power's own SEC filings are under CIK 3153; quarterly reports carry plant milestones (the third quarter 2025 report gives the Lindsay Hill approval and closing dates). Fetch them through the repo's fetch script so the declared-identity header is sent.
- TVA's 2025 draft plan was never finalized (the board lost its quorum in 2025). The preliminary final 2026 plan, released June 2026, considers 4 to 13 GW of new combined cycle and 3 to 13 GW of combustion turbines through 2040, with no named Alabama site.
- Data center load: Southern Company reported about 17 GW of contracted large load across Alabama, Georgia and Mississippi by mid-2026.

## Recent events 2024 to 2026

- Barry unit 5 (Mobile County, 785 MW): Alabama Power applied on November 14, 2025 to convert the coal unit to gas; the state issued a draft permit on May 18, 2026; construction was planned to start October 2026.
- Lindsay Hill (Autauga County, 855 to 895 MW depending on source): Alabama Power filed for a certificate October 30, 2024; FERC approved June 6, 2025; the commission approved in August 2025 (August 5 in the news, August 13 in the SEC filing); the $622 million purchase from Tenaska Alabama Partners closed September 30, 2025. The possible-updates sheet marks this done, but the export still shows Tenaska Alabama Partners LP as owner.
- Lowman (Leroy, Washington County): PowerSouth announced on June 3, 2026 a second Mitsubishi M501JAC turbine, lifting winter capacity from 696 MW to over 1 GW, no date given. GEM has it as CC_set 2, pre-construction, 454 MW; EIA-860M lists LEC3 planned for 2029 and the EIP sheet says 2028.
- Gaston units 1 to 4: Alabama Power filed on September 17, 2025 to drop the 2028 coal cessation path; Southern Company's filing says the units are extended through December 31, 2034. GEM carries gas "timepoint 2" rows for these units with no owner.
- Colbert (Tuscumbia): TVA's three new 250 MW turbines entered commercial operation July 25, 2023.
- Calhoun: Alabama Power took over the four turbines from Harbert Power on September 30, 2022 (ownership only).

## Still open after the 2026-10-09 run

- Filled in from the batch evidence file after the run.

## Gotchas

- Barry mixes trackers: units 1, 2 and 4 are converted gas steam units, unit 5 is coal until its conversion (a coal to gas record), units 6 and 7 are combined cycle, unit 8 is one combined cycle block (636 MW nameplate in the 2025 plan, 726 to 774 MW elsewhere).
- Gaston units 1 to 4 belong to Southern Electric Generating Company (Alabama Power and Georgia Power, half each); Alabama Power owns unit 5 and operates all five.
- Greene County: the 2025 plan lists "unit 2" in both the coal and the turbine tables. GT2 to GT10 are the 80 MW oil turbines from 1995 and 1996; units 1 and 2 are the converted steam units.
- Capacity entitlement is not ownership. A power purchase agreement (Hog Bayou) or a shared entitlement does not make Alabama Power the owner.
- Calhoun burns gas in summer and oil in winter.
- Tenaska Central Alabama and Tenaska Lindsay Hill sit about 1,000 feet apart with separate EIA plant codes (55440 and 55271). They are two plants; both now belong to Alabama Power and the "Tenaska" prefix is stale.
- Plant names vary: "Plant Barry", "Barry Steam Electric Generating Plant", "Ernest C. Gaston".

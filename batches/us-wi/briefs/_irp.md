## Integrated resource plans for Wisconsin (checklist rows 34 and 37)

Utilities in this state file integrated resource plans (IRPs) that name the gas units they intend to build, convert or retire. GEM records a planned unit from a plan's preferred portfolio as a project with the utility as owner, and ticks the unit's IRP box. A draft plan counts (Baird, October 2026).

What to do for each utility below:

1. Open the plan links. Download a PDF with curl and read it with pdftotext. Find the preferred, recommended or base portfolio and its table of additions, conversions, co-firing and retirements, with capacity and year.
2. Compare with the GEM plants listed under the utility, and with the whole state list in the briefs. A unit GEM already has: report only a value the plan changes (status, capacity, start year, planned retirement), with the plan page as the source. A plant marked below as carrying an IRP task on its own brief gets its questions from that brief: do not write a question about it here. Put what the plan says about it in meta.irp_summary instead.
3. A named gas unit the plan commits to that GEM lacks: write a new plant record (or a new unit at an existing plant) with the plan as the source, status announced unless the plan says construction has begun, the high end of any capacity range, and the utility as owner. Set irp true on the record.
4. Capacity the plan commits to without a site: GEM's convention is a placeholder plant named "<utility short name> <plan year> IRP power station <n>" (see the existing names below). Write it as a new plant record with irp true. Capacity the plan only studies as an option, outside the preferred portfolio, goes on the watch list as new to the tracker, with the plan as the source and "watch_case": "not_committed".
5. Say what the plan does not contain. A utility whose plan adds no gas gets one sentence in your summary so the tab's Notes can record it.
6. Never stage the IRP column itself. The irp true flag on a finding tells the build which plants need the box ticked in the web form.

### WEC Energy Group (Investor Updates)

Plan files: https://investor.wecenergygroup.com/investors/presentations/default.aspx

GEM plants in the state tied to this utility:

- Concord power station (L100000402372): 4 unit(s), operating; matched by parent; IRP box ticked on 0 of 4 units; no task of its own, compare it here
- De Pere energy center (L100000402378): 1 unit(s), operating; matched by parent; IRP box ticked on 0 of 1 units; no task of its own, compare it here
- Elm Road power station (L100000104274): 2 unit(s), pre-construction; matched by parent; IRP box ticked on 0 of 2 units; its own brief carries an IRP task
- Fox energy center (L100000402379): 1 unit(s), operating; matched by parent; IRP box ticked on 0 of 1 units; no task of its own, compare it here
- Fox North Energy Center (L100001089648): 1 unit(s), pre-construction; matched by parent; IRP box ticked on 0 of 1 units; its own brief carries an IRP task
- Germantown power station (L100000402373): 5 unit(s), operating; matched by parent; IRP box ticked on 0 of 5 units; no task of its own, compare it here
- Paris (WI) power station (L100000402374): 4 unit(s), operating; matched by parent; IRP box ticked on 0 of 4 units; no task of its own, compare it here
- Paris RICE power station (L100001047775): 1 unit(s), construction; matched by parent; IRP box ticked on 0 of 1 units; its own brief carries an IRP task
- Port Washington power station (L100000104693): 2 unit(s), operating; matched by parent; IRP box ticked on 0 of 2 units; no task of its own, compare it here
- Pulliam Power Plant (L100000104276): 1 unit(s), operating; matched by parent; IRP box ticked on 0 of 1 units; no task of its own, compare it here
- Riverside energy center (WI) (L100000401640): 1 unit(s), operating; matched by parent; IRP box ticked on 0 of 1 units; no task of its own, compare it here
- South Oak Creek Combustion Turbine Project (L100001025603): 5 unit(s), construction; matched by parent; IRP box ticked on 0 of 5 units; its own brief carries an IRP task
- Valley Power Plant (L100000104279): 2 unit(s), operating; matched by parent; IRP box ticked on 0 of 2 units; no task of its own, compare it here
- West Marinette power station (L100000402381): 1 unit(s), operating; matched by parent; IRP box ticked on 0 of 1 units; no task of its own, compare it here
- Weston Power Plant (L100000104280): 3 unit(s), announced, retired; matched by parent; IRP box ticked on 0 of 3 units; its own brief carries an IRP task
- Weston RICE power station (L100000409253): 1 unit(s), operating; matched by parent; IRP box ticked on 0 of 1 units; no task of its own, compare it here

Output: findings on tracked plants go in that plant's shard as usual. New plants, new units and watch items from the plans go in shards/_state.json under newplants, newunits and monitor, each with "irp": true. Then write one plain sentence per utility in meta.irp_summary of _state.json: what the plan adds, what was staged, and the next plan's due date if the plan or the tab gives one.


## Every resource plan, read in full

Read each plan below completely: the preferred plan and every alternative portfolio, the action plan, and the tables of new resources. Every gas or oil addition or option becomes an update on its GEM plant, a new plant, or a watch item. Answer each plan in coverage.json under `irp_plans` (Update SOP §3, step 8); gate `irp-plans` checks it.

# Utility resource plans: us-wi

Read every plan below in full. For each one, find the preferred or recommended portfolio and every alternative portfolio that names a gas or oil plant. Match each gas or oil addition to a GEM unit, stage an update, add it, or put it on the watch list. A plan option that the board has not chosen is a watch item with watch case not_committed. Answer each utility in coverage.json under irp_plans with the key shown.

## Public Service Commission of Wisconsin (Strategic Energy Assessment): Draft Strategic Energy Assessment 2026 to 2032, case 5-ES-113
Answer key: `plan Public Service Commission of Wisconsin (Strategic Energy Assessment)`.
- Document 1: https://apps.psc.wi.gov/ERF/ERFview/viewdoc.aspx?docid=595734 (read, 189 pages; text saved at scopes/us-wi/work/irp/psc-sea/1.txt)
- Document 2: https://apps.psc.wi.gov/ERF/ERFview/viewdoc.aspx?docid=595738 (read, 3 pages; text saved at scopes/us-wi/work/irp/psc-sea/2.txt)
- 82 lines name gas or oil with a megawatt figure. The first ones:
  - 1:5: Gas Prices ($/MMBTU), 2044 ......................................................... 44
  - 1:8: Gas Customers 2021–2025 (Annual Report Data) ......................... 108
  - 1:11: Table A-5 Gas Generation Units by Total CO2 Emissions, 2023 and 2024 .......... 138
  - 1:11: Table A-6 Gas Generation Units CO2 Emissions Rate, 2023 and 2024 .............. 140
  - 1:11: Table B-3 Annual Unit Selection for High Gas Price (4.04 $/MMBTU), MW .......... 144
  - 1:11: Table B-4 Annual Unit Selection for Low Gas Price (2.43 $/MMBTU), MW .......... 145
  - 1:14: 54 percent in 2015 to 33 percent in 2025. Natural gas resources increased in generation
  - 1:15: units will be replaced by natural gas fired combustion turbine units, a construction project
  - 1:15: replaced by new electric generation units with natural gas fueled resources at the same
  - 1:15: existing electric generation facilities to burn natural gas instead of coal by 2032.
  - 1:15: of new natural gas capacity or upgrades to existing natural gas facilities, nearly 1,370 MW
  - 1:15: percent of Wisconsin generation in 2024 to 3 percent in 2032, natural gas will increase
  - 1:16: The capacity expansion models selected a significant amount of natural gas initially, only
  - 1:16: during the transition period from natural gas units to new nuclear, as shown in Figure 2-8.
  - 1:21: gas generation increased as coal fired generation declined, with no plans for new coal
  - 1:30: zero greenhouse gas emissions by 2050 goal and most have set interim goals to achieve a
  - 1:35: also emits methane, a more potent greenhouse gas that eventually converts into CO2
  - 1:36: Oak Creek coal units will be replaced by natural gas fired combustion turbine units, a
  - 1:36: listed below will also be replaced by new electric generation units with natural gas fueled
  - 1:36: 2025 Wheaton 1, 2, 3, 4, 6 56, 68, 56, 61, 70 Natural Gas and Fuel Oil NSPW [GEM: Wheaton power station L100000409233]
  - 1:36: 2030 French Island 3, 4 157 (total) Natural Gas NSPW [GEM: French Island power station L100000409271]
  - 1:37: approximately 3,400 MW of existing electric generation facilities to burn natural gas
  - 1:37: 2029 Elm Road 1, 246 650, 650 Coal Natural Gas WEPCO [GEM: Elm Road power station L100000104274]
  - 1:37: 2030 Columbia 1, 2 47 566, 565 Coal Natural Gas WP&L, WPSC, MGE [GEM: Columbia Energy Center L100000104268]
  - 1:37: 2030 Edgewater 548 406 Coal Natural Gas WP&L [GEM: Edgewater Generating Station L100000104269]

## Wisconsin Electric Power Company and Wisconsin Public Service Corporation (WEC Energy Group): Investor Update, September 2026
Answer key: `plan Wisconsin Electric Power Company and Wisconsin Public Service Corporation (WEC Energy Group)`.
- Document 1: https://www.wpr.org/wp-content/uploads/2026/09/09-2026-September-Final-1.pdf (read, 54 pages; text saved at scopes/us-wi/work/irp/wec/1.txt)
- Document 2: https://www.sec.gov/Archives/edgar/data/783325/000078332525000063/a112025november-final.htm (read, 1 pages; text saved at scopes/us-wi/work/irp/wec/2.txt)
- 41 lines name gas or oil with a megawatt figure. The first ones:
  - 1:8: 1,100 MW CTs (left)
  - 1:11: January 1, 2027 & 2028 ** Gas proposed increases exclude the impact of the costs directly assigned to natural gas
  - 1:20: 5,000 946 973 Gas Distribution**
  - 1:23: Combustion Turbines RICE Generation LNG Storage Facilities
  - 1:23: CCGT Summer Upgrades Coal to Gas Conversions
  - 1:23: 150 MW and Fuel Oil Backup
  - 1:28:  Exploring conversion of both units to natural gas
  - 1:35: Oak Creek CTs 6630-CE-317 1,100 1,200E 2027/2028 [GEM: Coal Creek Station L100000104090]
  - 1:35: Paris RICE generation 6630-CE-316 128 300E 2027 [GEM: Paris RICE power station L100001047775, Paris energy center L100000402195]
  - 1:35: Foundry Ridge CTs 6630-BS-103 Q4 2026 270 550E 2028 [GEM: Foundry Ridge Energy Center L100001047813]
  - 1:35: Red Oak Ridge CTs 6630-BS-104 1,125 1,700E 2029/2030 [GEM: Red Oak Ridge Energy Center L100001062057, Red Oak power station L100000401603]
  - 1:38: store and discharge energy for up to Liquid is converted back to gas to power
  - 1:41: Wisconsin Gas 257.5 296.3 257.7
  - 1:41: Peoples Gas 512.7 680.7 700.0
  - 1:41: North Shore Gas 53.9 57.7 44.0
  - 1:41: Michigan Gas Utilities 52.2 43.2 47.8
  - 1:50: Wisconsin Gas 50.50%-55.50% 9.80%
  - 1:50: Peoples Gas 50.79% 9.38%
  - 1:50: North Shore Gas 52.58% 9.38%
  - 1:50: Michigan Gas Utilities 50.00% 9.86%
  - 1:51: Gas Pipeline Replacement Rider MGU
  - 2:1: 2 Cautionary Statement Regarding Forward-Looking Information Much of the information contained in this presentation is forward-looking information based upon management&#8217;s current expectations an
  - 2:1: 9 Longer-Term Sales and Load Growth Remain Strong Wisconsin Segment Year-Over-Year 2028-2030 Electric 6.0%-7.0% Gas 0.7%-1.0% Sales Growth Forecast (weather-normalized) 2026-2030 expecting to add 3.4 
  - 2:1: 12 Wisconsin Very Large Customer (VLC) Tariff Meets the unique needs of very large customers while protecting other customers and shareholders &#61607; Applies to customers with 500 MW or more of fore
  - 2:1: 13 2026-2030 Capital Plan Capital Plan &#8212; Key Drivers Identified $8.5 billion of additional investments compared to previous five-year plan: &#61607; Generation &#61607; Natural gas generation &#

## Wisconsin Power and Light Company (Alliant Energy): Generation resource plan refresh with Q3 2026 results
Answer key: `plan Wisconsin Power and Light Company (Alliant Energy)`.
- Document 1: https://www.sec.gov/Archives/edgar/data/352541/000035254126000045/lnt-20261029.htm (NOT READ (status saved): read it by hand; text saved at scopes/us-wi/work/irp/alliant-wpl/1.txt)
- 0 lines name gas or oil with a megawatt figure. The first ones:

## Madison Gas and Electric Company (MGE Energy): 2025 Annual Report and 2025 10-K (Energy 2050 goal)
Answer key: `plan Madison Gas and Electric Company (MGE Energy)`.
- Document 1: https://www.mgeenergy.com/news/reports/annual-reports/2025-annual-report (read, 1 pages; text saved at scopes/us-wi/work/irp/mge/1.txt)
- Document 2: https://www.mgeenergy.com/MGEEnergy/media/Library/documents/sec-reports/sec-filings/20260227-8k.pdf (read, 37 pages; text saved at scopes/us-wi/work/irp/mge/2.txt)
- Named sites in gas lines that match no GEM plant (document:page): Darien Solar Energy Center (1:1); Forward Energy Center (1:1); West Riverside Energy Center (1:1)
- 18 lines name gas or oil with a megawatt figure. The first ones:
  - 1:1: MGE Energy (MGEE) Year at a Glance (Thousands, except per-share amounts and shares outstanding) 2025 2024 Increase / (Decrease) % Change Total Market Value (Dec. 31) $ 2,877,671 $ 3,443,892 $ (566,221
  - 1:1: From investing in sustainable generation and battery energy storage to building a more dynamic electric grid, to enhancing the customer experience and equipping our workforce for new challenges, your 
  - 1:1: An evolving energy supply Growing our use of carbon-free energy generation is one of the ways in which we continue to work toward net-zero carbon electricity. In 2025, a number of new generation proje [GEM: Paris RICE power station L100001047775, RockGen energy center L100000402253]
  - 1:1: Earnings growth In 2025, we reported GAAP (Generally Accepted Accounting Principles) earnings of $3.72 per share, compared to $3.33 per share in 2024. Earnings for 2025 were positively impacted by an  [GEM: Paris RICE power station L100001047775]
  - 1:1: Another way MGE works with customers to manage electricity demand is behind the wheel—or rather, behind the charger—as the number of electric vehicles (EVs) on the road continues to grow. The electrif
  - 1:1: 2026 Annual Shareholder Meeting Tuesday, May 19, 2026 Please see the Proxy Statement for annual meeting information. Stock Listing MGE Energy common stock trades on The Nasdaq Stock Market ® Stock sym
  - 1:1: MGE Electric Services Generation and Distribution &nbsp; Customers: 170,000 Population: 376,000 Area: 264 square miles Communities served: Cross Plains, Fitchburg, Madison, Maple Bluff, McFarland, Mid [GEM: Columbia Energy Center L100000104268, Elm Road power station L100000104274, Manitowoc power station L100000201364]
  - 2:7: • Natural gas to ~180,000 customers • Premium service territory with constructive regulation
  - 2:7: from natural gas distribution system by 2035
  - 2:13: MGE to acquire 168 MW (33.4%) of the RockGen natural gas-fired plant from Dairyland Power Cooperative [GEM: RockGen energy center L100000402253]
  - 2:13: • Cost-effective natural gas plants add needed reliability and balance to the electric system while MGE continues to
  - 2:18: Rockgen4,5 Natural Gas 168 MW $203 33% 2027
  - 2:18: Elm Road4,6 Natural Gas Conversion 106 MW $11 8% 2028
  - 2:21: Average Gas Rate Base $375,594 $393,558
  - 2:25: • Exploring converting the Columbia Energy Center from coal to natural gas [GEM: Columbia Energy Center L100000104268]
  - 2:26: gas system through the evolution of new technologies, it will.
  - 2:35: 15 5. In February 2026, MGE executed an asset purchase agreement to acquire 33.34% ownership interest in the Rockgen Energy Center, an existing natural gas-fired generating plant near Cambridge, Wisco [GEM: RockGen energy center L100000402253]
  - 2:35: 6. In October 2025, MGE and other co-owners filed a joint application with the PSCW for upgrades to the non-regulated Elm Road Units. The project would convert existing coal-fired boilers to natural g [GEM: Elm Road power station L100000104274]

## Northern States Power Company, Wisconsin (Xcel Energy): 2024 to 2040 Upper Midwest Integrated Resource Plan, case E002/RP-24-67
Answer key: `plan Northern States Power Company, Wisconsin (Xcel Energy)`.
- Document 1: scopes/us-wi/work/irp/xcel/20242-203027-01.pdf (read, 203 pages; text saved at scopes/us-wi/work/irp/xcel-nsp-w/1.txt)
- The next plan was due 2026-11. Look for it before using this one.
- Pages that name the preferred or recommended plan (document:page): 1:1, 1:2, 1:9, 1:10, 1:11, 1:12, 1:16, 1:17, 1:18, 1:19, 1:20, 1:23, 1:24, 1:26, 1:27, 1:30, 1:36, 1:37, 1:38, 1:39, 1:40, 1:42, 1:49, 1:50, 1:51, 1:52, 1:62, 1:74, 1:82, 1:83
- 21 lines name gas or oil with a megawatt figure. The first ones:
  - 1:29: shows that we need to add over 2,200 MWs of firm peaking capacity—emergency
  - 1:53: 2) Regulations for new natural gas generating units pursuant to Clean Air Act
  - 1:117: (CT) allowed for selection on the Sherco generation tie-line; and
  - 1:120: • 374 MW gas-fired CT unit,
  - 1:120: • 225 MW gas-fired CT unit,
  - 1:120: • 108 MW reciprocating engine peaking unit (RICE),
  - 1:121: • CT allowed for selection on Sherco Tie-Line.
  - 1:133: percent and any new CT annual capacity factor to under 20 percent.
  - 1:137: 2 includes the same amount of cumulative firm peaking resources through 2040, those
  - 1:146: Firm Peaking 748 748 - 748
  - 1:152: EnCompass to select. The model allows hydrogen blending with natural gas in firm
  - 1:152: dispatchable resources (modeled as generic CTs) up to 100 percent starting in 2030
  - 1:153: EnCompass to select starting in 2035. The depreciation life of generic CTs is
  - 1:154: Firm Peaking 2,244 1,122 - (3,366) 13 -
  - 1:154: select starting in 2035. The depreciation life of generic CTs is shortened to be fully
  - 1:154: 13 All firm peaking resources are retired by 2050 in this study.
  - 1:155: 2035. The model allows hydrogen blending with natural gas up to 100 percent in firm
  - 1:155: dispatchable resources (modeled as a CT) starting in 2030 based on economic signals
  - 1:157: Firm Peaking 3,592 3,592 4,488 2,618 3,592
  - 1:158: peaking capacity additions, and battery capacity additions are reduced by 60 MW
  - 1:172: Combustion Turbine $1,026 $1,026 / $1,026 100.0% 0.0%

## Dairyland Power Cooperative: Optional integrated resource plan, Minnesota docket 25-271 (order June 30, 2026), case 25-271
Answer key: `plan Dairyland Power Cooperative`.
- Document 1: https://dairylandpower.com/sites/default/files/PDFs/Annual%20Reports/DPC_AnnualReport2025-WEB.pdf (read, 41 pages; text saved at scopes/us-wi/work/irp/dairyland/1.txt)
- 4 lines name gas or oil with a megawatt figure. The first ones:
  - 1:13: 1,270 MW of additional natural gas capacity. These facilities are considered
  - 1:29: Accounting for Energy Contracts—The Cooperative does not have any attributable to Rocky Road. Elgin is a 483 MW natural gas‑fired generating [GEM: Rocky Road power station L100000402254]
  - 1:29: energy contracts that are required to be accounted for at fair value as of station located in Elgin, Illinois, and Rocky Road is a 334 MW natural gas‑fired [GEM: Rocky Road power station L100000402254]
  - 1:33: two-year terms, as well as natural gas contracts which extend to 2032. determined, under the Pension Protection Act (PPA) of 2006. In addition, the

## WPPI Energy: State of WPPI 2025 resource planning and 400 MW by 2033 article
Answer key: `plan WPPI Energy`.
- Document 1: https://wppienergy.org/wp-content/uploads/2025/09/State-of-WPPI-2025.pdf (NOT READ (status saved): read it by hand; text saved at scopes/us-wi/work/irp/wppi/1.txt)
- Document 2: https://wppienergy.org/powering-ahead/ (NOT READ (status saved): read it by hand; text saved at scopes/us-wi/work/irp/wppi/2.txt)
- 0 lines name gas or oil with a megawatt figure. The first ones:

## Corrections for the US IRPs tab

- WEC Energy Group: the tab shows Investor Updates, but the newest plan is the Investor Update, September 2026, filed 2026-09 (https://www.wpr.org/wp-content/uploads/2026/09/09-2026-September-Final-1.pdf); next plan due 2027-11; the November 2026 update with the 2027 to 2031 plan of $47.5 billion, with $6.8 billion more for gas generation, was reported after the Q3 call but its deck was not found as a file; check the landing pages.


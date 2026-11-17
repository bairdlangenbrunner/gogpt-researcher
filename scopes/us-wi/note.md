# United States — Wisconsin

Scope tag `us-wi`. The scoped export pulled on 2026-11-17 holds 82 unit rows at 39 plants: 48 operating, 18 pre-construction, 8 construction, 5 retired, 2 announced and 1 cancelled. The roster row counts 21 units in development, 7,154.9 MW. The batch goes onto Amalia Llano's review page. Amalia edited about 27 Wisconsin rows from November 11 to 15, 2026, and tagged her notes "ALQ42026". Her values are the starting point. Change one only when a document says otherwise, and name the document.

## State context

- **Grid.** The whole state is in MISO. American Transmission Company owns the eastern and central grid. Xcel's Northern States Power-Wisconsin and Dairyland Power Cooperative are in the west. MISO's queue is an open JSON file. Newer requests often have the state blank, so they are matched by transmission owner.
- **Regulator.** The Public Service Commission of Wisconsin (PSC) approves any plant of 100 MW or more, utility or merchant, with a Certificate of Public Convenience and Necessity (case type CE). Smaller utility plants come under a Certificate of Authority (case type CA). Docket numbers start with the utility's number:
  - 6630: Wisconsin Electric (We Energies).
  - 6690: Wisconsin Public Service.
  - 6680: Wisconsin Power and Light (Alliant).
  - 3270: Madison Gas and Electric.
  - 5: joint dockets.
  - 9835 and 9837: Invenergy's project companies.

  Its filing system is ERF (`apps.psc.wi.gov/ERF`), open without a sign-in.
- **No integrated resource plan rule.** Wisconsin utilities do not file resource plans. What plays that role:
  - the PSC's Strategic Energy Assessment (the 2026 draft came out in June 2026 and counts 5.4 GW of planned new or upgraded gas);
  - the utilities' investor updates and capital plans;
  - the CE dockets themselves;
  - Dairyland's and WPPI's own plans;
  - Xcel's Upper Midwest plan, filed in Minnesota.

  All of them are listed in `scopes/us-wi/irp_plans.json` and read in full each batch.
- **Air permits.** The Department of Natural Resources (DNR) permits the whole state, Milwaukee included. Its complete record is WARP permit tracking (`apps.dnr.wi.gov/warp_ext/`), searched by facility name or industry code. Each facility has a facility ID (FID), and every permit document downloads from it. Notices of draft permits are on the DNR public notice page. Tribal land goes to EPA Region 5.
- **Utilities and owners to read.**
  - We Energies and WPS (WEC Energy Group): South Oak Creek turbines, Paris RICE, Fox North, Elm Road, Weston, Valley, Port Washington, Concord, Germantown, Paris, Pulliam, De Pere, Fox, West Marinette and Weston RICE. We Energies is also applying to buy Red Oak Ridge and Foundry Ridge.
  - Alliant (Wisconsin Power and Light): Edgewater 5, Columbia, Neenah, Sheboygan Falls, Riverside and Rock River.
  - Madison Gas and Electric: Blount Street, West Campus, the diesel generators, Fitchburg (which GEM lacks), and its shares of Elm Road, Columbia, West Marinette 34 and RockGen.
  - Xcel (Northern States Power-Wisconsin): French Island and Wheaton.
  - Dairyland: Elk Mound (which GEM lacks), Madgett, Genoa and Nemadji Trail.
  - WPPI Energy: South Fond du Lac and Island Street.
  - Invenergy: Forest Junction, Union Depot, Red Oak Ridge and Foundry Ridge.
  - Merchant owners: RockGen, LSP-Whitewater and Port Washington Generating Station LLC.
  - Municipal: Marshfield.
- **Data centers.**
  - Already in GEM: Microsoft Mount Pleasant (diesel backup fleets in three units) and Vantage Lighthouse WI-1 in Port Washington (45 diesel engines, about 87 MW).
  - Not in GEM: Microsoft Kenosha and Caledonia, later Vantage phases, Meta Beaver Dam (Alliant service agreement, docket 6680-TE-115) and any other campus `data_center_fleets.py` lists.
  - Each is answered under `data_centers`.

## Recent events 2024 to 2026

- **2024:**
  - Alliant set the Edgewater 5 gas conversion for 2028.
  - The Nemadji Trail approval was upheld in the Wisconsin courts.
- **2025:**
  - The PSC approved the South Oak Creek turbines and Paris RICE in May.
  - Elm Road's owners filed in October to end coal as the primary fuel (docket 5-CE-161).
  - Minnesota Power left Nemadji Trail in December.
- **2026:**
  - Edgewater 5's conversion was reported delayed to 2029 in March.
  - We Energies delayed the retirement of South Oak Creek 7 and 8 to the end of 2027 in April.
  - DNR issued the Vantage generator permits on June 12.
  - The draft Strategic Energy Assessment came out in June.
  - Invenergy filed the engineering plan for Forest Junction and Union Depot on August 20.
  - The PSC approved Alliant's Rock County LNG storage on September 3.
  - We Energies filed the Fox North engineering plan in October.
  - The PSC approved Red Oak Ridge on October 15, and approved Foundry Ridge in October.
  - Nemadji Trail's owners gave up its approvals on October 28.

## Watch items to raise with the reviewer

- **Weston:** the ID join's EIA 4130 is a wrong match to New Lisbon. Do not type it.
- **Coal-to-gas conversion rows:** Elm Road, Edgewater 5 and Weston 4 are conversion rows, so EIA's "operating" coal generator is not a status conflict. The same goes for Blount Street and Valley: their start years are the conversion years.
- **Germantown:** EIA gives 71.2 and 105.9 MW, while GEM gives 61.2 and 91.
- **Red Oak Ridge:** up to 1,186 MW on the PSC page, against 1,210 in GEM. It also sits in the Town of Paris on the PSC page, but in Somers in GEM.
- **Port Washington docket 6630-CE-318:** may be new generation GEM lacks.
- **Fitchburg** (MGE, 57.6 MW) and **Elk Mound** (Dairyland, 71 MW) are operating plants GEM lacks.
- **Natalia Fretz's three open comment threads:** Edgewater 5, Weston 4 and Elm Road.

## Still open

See `scopes/us-wi/plan.md`, Stage A. Still to find: the RBLC address, the DFI detail page, the meeting record paths for Beaver Dam, Dodge and Brown counties, Caledonia, Beloit and the host towns (Brillion, Paris, Somers, Darien, Wrightstown), and the titles of dockets 6630-CE-315 and 6630-CE-318.

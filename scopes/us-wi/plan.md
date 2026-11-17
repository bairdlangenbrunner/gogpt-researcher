# Wisconsin update plan

Wisconsin is a full-state update for Amalia Llano's review page, planned 2026-11-17 on the New Mexico, Kentucky and Oklahoma pattern (`scopes/us-nm/plan.md`, `scopes/us-ky/plan.md`, `scopes/us-ok/plan.md`). Every plant in the scoped export gets read and cited or answered, and so does every lead, permit, commission filing, council and county record and news story. Scope tag `us-wi`. This plan is written to be run by another session, probably on a cheaper model, so it names every file and repeats what that session needs. Run every script from the repo root as `python scripts/<name>.py` unless a step says otherwise.

## Decisions

Settled by the request (Baird 2026-11-17):

- The batch stages into Amalia's page (`amalia` in `review_app/artifacts.json`, https://claude.ai/artifact/7bnX9RMity3Yw5mdaojNaL). Add `batches/us-wi/staging` to that page's dirs before the rebuild.
- Mode is `update`, every plant, in the order `worklist.py` gives (28 priority-1 rows first, then French Island's 2030 retirements, then the operating rest).

Confirmed by Baird 2026-11-17:

- **Amalia is working Wisconsin right now.** 27 rows carry her "ALQ42026" notes, edited 2026-11-11 to 2026-11-15: Edgewater 5, Elm Road, Forest Junction, Foundry Ridge, Fox North, Microsoft Mount Pleasant, Neenah, Nemadji Trail, Paris RICE, Red Oak Ridge, Sheboygan Falls, South Oak Creek, Union Depot, Vantage Lighthouse and Weston 4. Re-pull at run time and treat her values as the baseline. Stage an edit against one of her values only when a verified document disagrees, and say which document. Proceed without waiting for her or checking with her (Baird 2026-11-17).
- **Nemadji Trail stays cancelled.** Amalia set it from the owners' October 28, 2026 letter to the Public Service Commission giving up the construction approvals in dockets 9698-CE-100 and 9698-CE-101. Minnesota Power had left in December 2025. The run only adds a second publisher and a dated step, and answers the EIA plant 8057 "Superior Generation Energy Center" match in a question. The EIP and Sierra Club "proposed" rows are stale; say so, never cite them.
- **Natalia Fretz's three open comment threads** (Edgewater 5 start year, Weston 4 retirement year, Elm Road retirement year) are answered with an edit or a question on each unit. The Weston and Elm Road threads look settled in the thread itself; the run confirms the current document and says the thread can be closed. Closing a thread is a web-form step for a person.
- Models per step follow `docs/workflows.md`. The harvesters and the per-plant sweep run on Sonnet. The scope-wide agent, the resource plan reading and the location review run on Opus. Gates and merge calls stay in the main loop.

## What the export already shows (2026-11-17 pull, 07:49)

82 scoped rows at 39 plants: 48 operating, 18 pre-construction, 8 construction, 5 retired, 2 announced and 1 cancelled. The roster row says 21 in development, 7,154.9 MW.

- **In development:**
  - Forest Junction Energy Center, Brillion, Calumet County: five GE 7F.05 turbines at 240.6 MW each, pre-construction, 2031. GEM gives the owner as Invenergy.
  - Union Depot Energy Center, same site: a 750 MW combined cycle plant, pre-construction, 2031.
  - Red Oak Ridge Energy Center, Kenosha County: five turbines at 242 MW, pre-construction, 2030. Docket 9837-CE-100, with the certificate approved 2026-10-15.
  - Foundry Ridge Energy Center, Darien, Walworth County: three turbines at 108 MW, pre-construction, 2028. Docket 9835-CE-100.
  - Fox North Energy Center, Wrightstown: a 750 MW combined cycle plant, pre-construction, 2032. Docket 6630-CE-319, pre-application.
  - South Oak Creek Combustion Turbine Project: five turbines at 220 MW, construction, 2028. Docket 6630-CE-317.
  - Paris RICE: 131.6 MW, construction, 2027. Docket 6630-CE-316.
  - Coal-to-gas conversions, each the second timepoint of a coal unit: Elm Road 1 and 2 (701.3 MW each, pre-construction, 2028), Edgewater 5 (413.7 MW, announced, 2030) and Weston 4 (595 MW, announced, 2030).
  - Data center backup fleets: Microsoft Mount Pleasant (three units, 672 MW, Amalia's note gives 244 generators and 687 MW in the August 2026 application) and Vantage Lighthouse WI-1 in Port Washington (87 MW, construction).
- **Planned retirements:** French Island 3 and 4 (78.8 MW each, oil, 2030). The coal side shows South Oak Creek 7 and 8 (2027), Columbia 1 and 2 (2029), Edgewater 5 (2029), Weston 3 (2031) and Weston 4 (2030).
- **Every Latest Activity is blank.**
- **Start scripts, run 2026-11-17:**
  - **Validation report:** 14 fix items, at Blount Street, Elm Road, Pulliam and Valley:
    - Blount Street: no data source for owner or location; no carbon capture source on units 6 and 7.
    - Elm Road: no source for capacity or technology on units 1 and 2, and no carbon capture source on unit 2.
    - Pulliam: no data source for owner or location.
    - Valley: no source for owner, and no carbon capture source on units 1 and 2.

    90 items are on coal-only units and are ignored.
  - **Assigned Comments:** 3 open threads (see Decisions).
  - **No-tracker units and captive LNG rows:** none.
  - **Location:** 2 candidates, Forest Junction and Union Depot, both approximate.
  - **IRP tab:** one utility row only, WEC Energy Group investor updates.
  - **ID join:** 43 tasks, 4 IDs to type, 3 possible new plants and 2 problems.
- **The unfiltered export** also carries South Oak Creek Plant 5 to 8, Columbia 1 and 2, John Madgett, Genoa, Pleasant Prairie, Alma, Nelson Dewey, Stoneman and the coal timepoints at Blount Street, Edgewater, Elm Road, Valley and Weston. It also carries the bioenergy units at Bay Front, Manitowoc, French Island 1 and 2, Rothschild and the paper mills. Keep them visible for the conversion and site-reuse checks.

## ID join results to read with care

`work/ids_us-wisconsin.md` has three kinds of false alarm the sweep must answer, not stage:

- **Weston, EIA 4130, is a wrong match. Do not type it.** The join matched Weston unit 4's gas timepoint to generator 4 at plant 4130, "New Lisbon," in Juneau County, 116 km away (0.3 MW of oil, retired 2003). Weston's code stays 4078 only. The two status and start-year tasks on that unit come from the same wrong match. Weston 4's real questions are the conversion year and the coal backup fuel.
- **Conversion timepoints compared with a coal generator.** Elm Road 1 and 2 and Edgewater 5 read as "operating in EIA, pre-construction or announced in GEM." EIA lists the coal generator, and GEM's row is the planned gas conversion. The join says so under Problems. The conversion row keeps its status unless a document changes the conversion. Elm Road's co-owners filed in docket 5-CE-161 to end coal as the primary fuel, with coal kept as backup to 2030 and ended by 2032. Settle the gas start year from that docket. For Edgewater 5, settle 2028, 2029 or 2030 from Alliant's newest filing or release.
- **Conversion start years.** Blount Street 6 and 7 (2011) and Valley 1 and 2 (2014, 2015) are the gas conversion years. EIA's 1957, 1961, 1968 and 1969 are the original coal years. GEM's convention keeps the conversion year on the second timepoint. Answer each task with the source for the conversion year, which also clears the start-year part of the validation items.

The rest are real tasks:

- **IDs to type:** Red Oak Ridge EIA 70453, Riverside EIA 64020 (West Riverside, alongside 55641) and South Oak Creek CT project EIA 4041. Leave out Weston 4130.
- **Generator IDs** for Red Oak Ridge (CT4, CT5, RDOR1 to RDOR3), South Oak Creek (11 to 15), Foundry Ridge (EIA 70360, FNDRD, FNRD2, FNRD3) and Wheaton 8. Each goes in a question; never a value.
- **Capacity:**
  - Germantown: EIA gives 71.2 MW for units 1 to 4 and 105.9 MW for unit 5, while GEM gives 61.2 and 91.
  - Neenah and Sheboygan Falls: EIA gives 185.5 and 173.4 MW, while GEM gives 220. Amalia set 220 from Alliant's "about 440 MW after 2025 upgrades" for each plant; check that her notes give the source and leave her value unless a document disagrees.
- **Paris "Internal Combustion Project" units 5 to 11** (seven at 19 MW) are the Paris RICE engines GEM holds as one 131.6 MW unit at Paris RICE power station. Answer in a question that names the docket. No new units.
- **Wheaton:** unit 6's EIP "under construction" is the repowering. Settle unit 7 (249.1 MW, operating 2026) and unit 8 (49 MW, operating 2025) from Xcel's Wisconsin filings and EIA, and say whether the repowering replaced unit 6.
- **Possible new plants:**
  - **Fitchburg:** MGE, Dane County, EIA 3991, two 28.8 MW combustion turbines from 1973, 57.6 MW, operating. An add on the EIA record plus one document.
  - **Elk Mound:** Dairyland, Chippewa County, EIA 7863, two 35.5 MW turbines from 2001, 71 MW, operating. An add; DNR facility 13798522.
  - **Foundry Ridge** is the GEM plant already listed; it is a match, not an add.

## State context the sweep needs

The full version is in `note.md`. In short:

- **Grids.** The whole state is in MISO. American Transmission Company (ATC) owns the eastern and central grid. Xcel's Northern States Power-Wisconsin and Dairyland are in the west, in the MISO West study group.
- **Regulator.** The Public Service Commission of Wisconsin (PSC) issues a Certificate of Public Convenience and Necessity (CPCN, case type CE) for any plant of 100 MW or more, utility or merchant. Smaller utility plants come under a Certificate of Authority (CA). Wisconsin has no integrated resource plan rule. What plays that role is the PSC's Strategic Energy Assessment (2026 draft released June 2026), the utilities' investor updates and capital plans, the CE dockets, Dairyland's and WPPI's own plans, and MISO's planning survey.
- **Air permits.** The Department of Natural Resources (DNR) permits everything outside tribal land. There is no separate county air agency, so Milwaukee is DNR too. Tribal land goes to EPA Region 5.

## Access, probed 2026-11-17

A Sonnet probe opened every source family. Notes and samples are in the planning session's scratchpad (`/private/tmp/claude-501/wi-probe/`, which will not survive). What matters is repeated here.

- **PSC Electronic Regulatory Filing (ERF), the commission record.** No session is needed.
  - **Docket list:** a plain GET on `https://apps.psc.wi.gov/ERF/ERFsearch/content/searchResult.aspx?UTIL=<util>&CASE=<type>&SEQ=<seq>&START=none&END=none&TYPE=none&SERVICE=none&KEY=none&NON=N&EXM=N`. The first row carries the docket title, and the rows link `viewdoc.htm?docid=N`.
  - **Download:** `https://apps.psc.wi.gov/ERF/ERFview/viewdoc.aspx?docid=<n>`. PDFs have a text layer.
  - **Statewide lists:** `UTIL=0&CASE=CE&SEQ=0&START=2025-01-01&END=none&SERVICE=ELE` lists 150 CE dockets, and `KEY=natural%20gas` lists 197. These pages run 70 to 110 MB and carry no titles, so the harvester takes the docket numbers and fetches each title separately.
  - **Commission case pages:** `psc.wi.gov/Pages/CommissionActions/CasePages/<Name>.aspx` (Red Oak Ridge, Foundry Ridge, Nemadji Trail) work with plain curl.
  - **Known dockets:**
    - 6630-CE-315: Concord, 28 documents. The title is not read yet.
    - 6630-CE-316: Paris RICE, 1,768 documents.
    - 6630-CE-317: South Oak Creek, 1,852 documents.
    - 6630-CE-318: Port Washington, 101 documents. The title is not read yet, and this may be a project GEM lacks (see leads).
    - 6630-CE-319: Fox North pre-application, 6 documents.
    - 5-CE-161: Elm Road gas fuel flexibility.
    - 5-CE-162: Forest Junction and Union Depot, 140 documents. The engineering plan is filing 606657 of 2026-08-20.
    - 9837-CE-100: Red Oak Ridge, 1,112 documents, with related docket 6630-BS-104.
    - 9835-CE-100: Foundry Ridge.
    - 9698-CE-100 and 9698-CE-101: Nemadji Trail.
    - 6680-TE-115: Alliant's Meta Beaver Dam service agreement.
    - 5-ES-110: the 2026 Strategic Energy Assessment. The number is unconfirmed.
  - A plain curl from the planning session got a short error page on CE-315, CE-318 and CE-319, though the probe's requests worked. Use `fetch.py` and record the route.
- **DNR air permits, the complete record (`permit_record`).** WARP permit tracking is at `https://apps.dnr.wi.gov/warp_ext/AM_PermitTrackingSearch.aspx`.
  - **Search:** an ASP.NET postback. GET the form, then POST every input with `__EVENTTARGET=ctl00$ContentPlaceHolder1$btnSearch`, by name (`txtFacName`, with `grpName` set to contains, starts with or exact) or by SIC code (`txtSic`). SIC 4911 returns 128 facilities, and NAICS 2211 returns 155. A single hit redirects to `am_permittracking2.aspx?id=<FID>`.
  - **Documents:** POST `Select$n` on `gvPermits`, then `Select$n` on `gvDocuments`. That reveals `AM_DownloadObject.aspx?id=N`, which downloads with a plain GET (HEAD answers 500). Some files are .docx. Old scans have weak text, so OCR them.
  - **Facility IDs found:**
    - Oak Creek: 241007690 and 241219440.
    - Paris: 230094810, and 252304470 for Paris RICE.
    - Weston: 737009020.
    - Port Washington: 246004000.
    - Microsoft Mount Pleasant: 252302490 (permits 24-DMM-092 and 25-MIN-113).
    - Vantage WI-1: 246185280 (construction permit 25-MIN-094, operation permit 24618528A-F01, 45 diesel emergency generators, about 87 MW, issued 2026-06-12, under a lawsuit).
    - Foundry Ridge: 265200320 and 265200430.
    - Riverside: 13490124.
    - Elk Mound: 13798522.
- **DNR notices (`permit_notices`).** `public_notice.aspx` embeds every live notice as JSON in the `pubstring` script variable (about 15 rows). `apps_received.aspx` and `final_permit_decisions.aspx` cover 180 days. The DNR environmental analysis pages, such as `dnr.wisconsin.gov/topic/EIA/PortWashington.html`, work with plain curl.
- **EPA.**
  - ECHO REST works with plain curl. `air_rest_services.get_facilities?output=JSON&p_st=WI&p_sic=4911&p_act=Y` returns 45 rows, and `get_download?output=CSV&qid=` returns a CSV. The limit is 300 calls an hour.
  - The RBLC addresses under `cfpub.epa.gov/rblc/` answered 404. Find the current address in Stage A or wall it.
- **Queue.** MISO's `https://www.misoenergy.org/api/giqueue/getprojects` is open (4,097 projects). It has 245 rows with state WI: 55 active, 29 of them gas, combined cycle or hybrid. The active Wisconsin gas rows include J4164 (Dane County, 1,203 MW), J3156 (Rock County, 100 MW), S1090, J4115, J4116, J3936, J4014, J4028 and J4165. 479 newer rows have a blank state, among them J4179 (ATC, 735 MW, 2030) and J4184 (ATC, 755 MW, 2030), so the `owner` setting catches them. `pull_queues.py` already reads MISO.
- **Local records.**
  - **Legistar, open JSON API (`webapi.legistar.com/v1/<client>`):** milwaukee, madison, racine, dane and waukesha. Matters can be searched by title, for example `$filter=substringof('data center',MatterTitle)`. These clients answered 500: kenosha, ozaukee, eauclaire, sheboygan, dodge, brown, walworth, rock, greenbay and mtpleasant.
  - **CivicPlus AgendaCenter, proven:** mtpleasantwi.gov, ozaukeecounty.gov, calumetcounty.org, superiorwi.gov, douglascountywi.gov, menomonie-wi.gov and co.walworth.wi.us. Search is a GET (a POST answers 411): `/AgendaCenter/Search/?term=<term>&CIDs=all&startDate=&endDate=&dateRange=&dateSelector=`. Download is `/AgendaCenter/ViewFile/Agenda/_MMDDYYYY-ID`.
  - **Cloudflare, reachable through `fetch.py`:** portwashingtonwi.gov, racinecounty.gov, co.rock.wi.us, janesvillewi.gov, kenoshacountywi.gov and sheboyganwi.gov (`cf_clearance`). Their AgendaCenter paths are not tested yet.
  - **Platform not found yet:**
    - Beaver Dam, Menomonee Falls, Green Bay and DeForest show an empty AgendaCenter.
    - Beloit uses Laserfiche behind Cloudflare.
    - Caledonia has an "eboard" site.
    - Dodge County answered a 261-byte page.
    - Brown County, the Town of Brillion, the Village of Somers, the Village of Paris, the Town of Paris (townofparis.org, WordPress behind Cloudflare), Wrightstown, Darien and Yorkville are not identified yet.
- **News.**
  - **Gannett** (Milwaukee Journal Sentinel, Sheboygan Press, Green Bay Press-Gazette) answers 402 to plain requests. `curl_cffi` with chrome impersonation, or `fetch.py --render`, reads the articles, and the `news-sitemap.xml` lists them (strip the whitespace in `<loc>`).
  - **Plain curl works for:** madison.com, wpr.org, urbanmilwaukee.com, journaltimes.com, kenoshanews.com and ozaukeepress.com.
  - **Wisconsin Examiner** needs `cf_impersonate`.
- **Utilities.**
  - Plain curl works for wecenergygroup.com, we-energies.com, alliantenergy.com, mge.com, dairylandpower.com, wppienergy.org and psc.wi.gov.
  - investor.wecenergygroup.com answers 403, so use the ladder. The IRP tab's own link is the Q4 S3 file store (`q4live.s22.clientfiles...`), which an older note cites.
- **Business entity search (DFI).** `https://apps.dfi.wi.gov/apps/CorpSearch/Search.aspx` sits behind Cloudflare. The form loads with `curl_cffi`, and the results page `Results.aspx?type=Simple&q=<name>` loads only through `fetch.py`'s browser render. No CAPTCHA was seen. Prove the detail page in Stage A.

## Human walls (expected)

Each becomes a `human_wall` sentence in `coverage.json`. No script signs in with Baird's credentials.

- RBLC, if no current address exists: Baird exports the Wisconsin table in a browser.
- The DFI search, if the browser render cannot reach a detail page: Baird looks up the named LLCs by hand.
- Town records not posted online (Brillion, Paris, Somers, Darien, Wrightstown if nothing is found): an email to the clerk, drafted for Baird.

## Manual rules the run leans on

The repo CLAUDE.md hard requirements apply in full. Wisconsin leans on these:

- **Adds.** One verified source is enough: a MISO queue row, a CE or CA docket, a DNR application or a town or county record. A data center backup fleet at 50 MW summed nameplate is an add with Backup Power yes. Owner goes on every add.
- **Merchant plants.** Red Oak Ridge, Foundry Ridge, Forest Junction and Union Depot are Invenergy's, with We Energies applying to buy the first two. Keep the project LLC or Invenergy at 100 percent until the PSC approves a sale, and say in Notes that a sale is pending, with the docket.
- **Status changes.** Green needs two independent publishers. The PSC order and the utility's filing or release count as two.
- **Conversions.** Every coal-to-gas row is a second timepoint, carrying the conversion year (Elm Road, Edgewater 5, Weston 4, Blount Street, Valley). If Columbia gets a conversion filing, it becomes a second timepoint on that unit.
- **Units.** A combined cycle block is one unit (Fox CC1, Fox North CC1, Union Depot, Riverside, West Campus, Whitewater, Combined Locks). Capacity is electrical nameplate only.
- **Status Detail and Notes** are additive, newest on top, and Status Detail carries its own links.
- **Dates.** Start year never goes on shelved or cancelled units, and retired year never goes on mothballed ones.
- **Sources.** Wayback copies are citable. gem.wiki is never cited, and the Sierra Club list is reference only. Cleanview, interconnection.fyi and everydatacenter.com start a search but never carry a value alone.

## Guardrails (all exist; nothing to build)

- Run `access_check.py --scope us-wi` before anything else reads the web.
- `state_gate.py` gates: `access-proof`, `statewide-coverage`, `permit-system`, `local-records`, `chase`, `ids_followup`, `dedup`, `queues`, `data-centers`, `irp-plans`, `validation`, `location`, `additive`, `questions`, `watch-case`, `add-basics`, `access`, `unit-names` and `headers`.
- `qc_checks.py --staged` with zero errors.
- `url_verifier.py` on every URL.
- `entity_lookup.py` before every new owner.
- `access_audit.py batches/us-wi --retry` on every give-up.

## New tooling (build in Stage A, each with an offline test on saved sample pages)

Follow the Kentucky, Oklahoma and New Mexico harvesters and their tests (`tests/test_harvest_permits_kentucky.py`, `tests/test_harvest_psc_kentucky.py`, `tests/test_harvest_local_kentucky.py`). Build on `scripts/harvest_lib.py` (`get`, `wayback_url`, `harvest_out`, `docket_cache`, `report_failure`, `tag_batch`). When a server answers a document request with an HTML page, detect it by content type and the `%PDF` bytes and fall back to Wayback.

1. **`scopes/us-wi/harvest_permits.py`**
   - For every GEM plant, every owner and every lead name: a WARP search by name, the facility page, every permit, and every document through the two postbacks. The probe's `dnrsearch.py` pattern is the start.
   - Also pull the whole SIC 4911 and NAICS 2211 facility lists. Any power-like name with no GEM match (power, generating, energy center, RICE, peaking, data center, turbine, engine) goes to `_unmatched.md`, the way Oklahoma's does.
   - Also search WARP for data center names: Microsoft, Vantage, Meta, Greater Kudu, QTS, Cloverleaf, Oracle and "data". The SIC for data centers is 7374, so search it too.
   - Read the `pubstring` notice JSON, `apps_received.aspx` and `final_permit_decisions.aspx`.
   - Download under `scopes/us-wi/work/permits/docs/<FID>/`, extract with `pdftotext -layout` (and `python-docx` for .docx), and OCR scans. Pull units, MW, make and model, engine counts and dates.
   - Write `scopes/us-wi/work/permits/<plant_id>.md` and `.json` plus `index.json`.
2. **`scopes/us-wi/harvest_psc.py`**
   - List every CE and CA electric docket since 2021 from the statewide ERF query, and fetch each docket's title. Keep those about a gas or oil plant, a conversion, a retirement, a data center tariff or service agreement (TE), an acquisition (AE or BS), the Strategic Energy Assessment or LNG storage. Also search by every utility's number: 6630 WEPCO, 6690 WPS, 6680 WPL, 3270 MGE, 5 for joint dockets, Dairyland, Xcel 4220 NSP-W and WPPI. Add the dockets named above.
   - Download the application, the engineering plan, the final decision and each data request answer that names a unit, into `scopes/us-wi/work/psc/<docket>/`, and extract them.
   - Also read the case pages under `psc.wi.gov/Pages/CommissionActions/CasePages/`.
   - Write `batches/us-wi/harvest/psc_dockets.json` in the `build_state_brief.py --harvest` contract.
3. **`scopes/us-wi/harvest_local.py`**
   - Read every agenda, packet and minutes file since 2024-01-01:
     - Legistar: Milwaukee, Madison, Racine, Dane and Waukesha.
     - AgendaCenter: Mount Pleasant, Ozaukee County, Calumet County, Superior, Douglas County, Menomonie and Walworth County, plus Port Washington, Racine County, Rock County, Janesville, Kenosha County and Sheboygan through `fetch.py`.
     - Beaver Dam, Dodge County, Brown County, Caledonia, Beloit, Brillion, Somers, the Village and Town of Paris, Darien, Wrightstown, Oak Creek, Rothschild and Kronenwetter once Stage A finds their paths.
   - Search each for the plant names, the leads, "data center", "generator", "power plant", "gas", "Invenergy", "We Energies", "Alliant", tax incremental financing and rezoning.
   - Write `batches/us-wi/harvest/local_records.json` and `.md`. Bodies with nothing posted go to `not_posted`.
4. **`scopes/us-wi/queues.json`**
   - `markets`: MISO.
   - `owner`: American Transmission, ATC, Wisconsin Electric, We Energies, Wisconsin Public Service, Wisconsin Power and Light, Alliant East, Madison Gas, Dairyland, WPPI, Northern States Power Wisconsin and Xcel Wisconsin. Check the exact strings against the JSON.
   - `shared_owner`: Northern States Power (Minnesota), ITC, Great River Energy and Alliant West (Iowa).
   - `known` patterns:
     - Red Oak Ridge, Foundry Ridge, Forest Junction (Cleanview has a 650 MW 2030 MISO row), Union Depot and Fox North.
     - South Oak Creek, Paris RICE, Port Washington and Elm Road.
     - Riverside, Wheaton, Nemadji Trail and Fitchburg.
5. **`scopes/us-wi/irp_plans.json`** and `irp_sheet.py` aliases. Wisconsin has no IRP rule, so the list holds what plays that role, newest first:
   - The PSC 2026 Strategic Energy Assessment (draft June 2026, final if issued). It gives 5.4 GW of planned new or upgraded gas.
   - WEC Energy Group's Q3 2026 investor update (the 2027 to 2031 plan of $47.5 billion, with $6.8 billion more for gas generation) and its rate case generation spreadsheet (Forest Junction December 2031).
   - Alliant Energy's Q3 2026 update and WPL's Clean Energy Blueprint successor (Columbia coal ends 2029 with a gas study; Rock County LNG storage approved 2026-09-03).
   - MGE's 2025 annual report and newest Energy 2050 plan (one-third of RockGen bought 2026).
   - Xcel's Upper Midwest resource plan (Minnesota docket, covering NSP-Wisconsin) for French Island and Wheaton.
   - Dairyland Power Cooperative's resource plan (Madgett retire by 2032; Elgin and Rocky Road in Illinois bought 2025, out of scope here).
   - WPPI Energy's power supply plan, and Upper Michigan Energy Resources if it owns a Wisconsin unit.
   - Every plan is read from start to end, including alternatives. Add each utility as a row on the US IRPs tab draft for Baird (the repo never writes the tab).
6. **`fetch.py` host rules** in `work/fetch_routes.json`:
   - Gannett hosts (jsonline.com, sheboyganpress.com, greenbaypressgazette.com) use impersonate chrome or `--render`.
   - wisconsinexaminer.com and the Cloudflare city and county hosts use `cf_impersonate`.
   - apps.dfi.wi.gov uses `--render`.
   - investor.wecenergygroup.com uses the ladder.

   Add a Wisconsin row to `docs/reference/site_access.md` for each.

## Known leads the run must settle (each becomes a record or a coverage answer)

- **Port Washington, docket 6630-CE-318.** Read the title and the application. If it is new We Energies generation at or near the Port Washington site for the Vantage and Oracle campus, it is an add or a new unit at Port Washington power station. Settle the same way for Concord, docket 6630-CE-315 (a new unit, an upgrade or a conversion).
- **Forest Junction and Union Depot** (docket 5-CE-162). Get the CPCN application, if filed, the MW per unit (up to 1.2 GW and 750 MW), the alternate Woodville site and the in-service dates. Owner: Invenergy, or the project LLCs, until We Energies files to buy. Location is a candidate; the engineering plan's site map places it. Check that Forest Junction is not double counted against the Cleanview 650 MW queue row.
- **Red Oak Ridge.**
  - **Capacity:** the PSC page says up to 1,186 MW, while GEM gives 5 × 242 = 1,210 MW. Use nameplate from the application.
  - **Location:** the PSC page says the Town of Paris, while GEM says Somers. Check the site.
  - **Status Detail and Latest Activity:** the CPCN vote of 2026-10-15 and the written order.
  - **Sale:** We Energies' purchase application, with its docket.
- **Foundry Ridge.** The CPCN of October 2026, docket 9835-CE-100, and We Energies' purchase application. Answer EIA 70360 in a question.
- **Fox North** (6630-CE-319): construction 2029, operation late 2032. Read the engineering plan for the turbine model and MW.
- **South Oak Creek CTs and Paris RICE.** Construction progress, and the in-service date (winter 2027 or summer 2028). The 2 Bcf LNG storage at Oak Creek is storage, not a power plant; GEM's "fossil gas: LNG" fuel on the CT rows is worth a question only if no document says the turbines burn regasified LNG.
- **South Oak Creek coal 7 and 8.** Retirement delayed to the end of 2027 (announced April 2026). This is the coal side, so note it for the conversion and site context only.
- **Elm Road conversion** (5-CE-161). Settle the gas start year (2028 in the October 2025 filing, coal backup to 2030, no coal after 2032), and fill the validation report's capacity, technology and carbon capture sources.
- **Edgewater 5.** Alliant's May 2024 release says conversion in 2028, the March 2026 Sheboygan Press story says delayed to 2029, and GEM says 2030. Settle from Alliant's newest filing and answer Natalia's thread.
- **Weston 4.** The conversion year (2029 in EIA-860 2025, 2030 in WEC's May 2025 update), coal kept as backup, and Natalia's thread. Weston 3 retirement 2031 is coal-side context.
- **Columbia Energy Center** (Alliant, WPS and MGE). Coal ends at the end of 2029, with a gas conversion study. A unit-level conversion becomes a second timepoint only with a filing or a utility statement that commits to it; otherwise it is a watch item with case `plan_option`.
- **Burlington RICE is Iowa**, not Wisconsin. It is already in GEM and not a lead here.
- **Data centers.**
  - **Microsoft Mount Pleasant:** reconcile the three units with permits 24-DMM-092 and 25-MIN-113, and the 244 generators and 687 MW of the August 2026 application. The third site proposes about 150 more generators.
  - **Microsoft Kenosha and Caledonia:** status and any generator permits.
  - **Vantage Lighthouse WI-1:** 45 engines, 87 MW, permit 25-MIN-094. Check engine count and capacity per engine, and whether later phases (WI-2 and on) have permits.
  - **Meta Beaver Dam** (Alliant service agreement 6680-TE-115, up to 220 MW load): check for a backup fleet permit.
  - **QTS, Cloverleaf and any other Wisconsin campus** `data_center_fleets.py` lists.
  - Every site at 50 MW summed nameplate or with unknown capacity is answered under `data_centers`.
- **MISO queue rows.** J4164 (Dane County, 1,203 MW, which Cleanview names North Madison), J3156 (Rock County, 100 MW), J4179 and J4184 (ATC, 735 and 755 MW, 2030), and the other active gas rows. Each is matched to a GEM plant or a lead, or added at announced on the queue row (the add threshold is one source).
- **Wheaton** (Xcel). The repowering units, 7 and 8, and unit 6's retirement.
- **French Island 3 and 4.** The 2030 retirement and any replacement in Xcel's plan.
- **Ownership.**
  - RockGen: MGE bought one-third in 2026; stage it at 33 percent if the closing is confirmed.
  - Riverside: two EIA codes.
  - Port Washington: the owner LLC and WEC parent.
  - Elm Road shares: WEPCO 83 percent, plus WPPI and MGE.
  - West Campus: MGE and the University of Wisconsin.
  - LSP-Whitewater: the owners and their shares.
  - Sheboygan Falls: Sheboygan Power LLC, leased to Alliant.
- **Fitchburg and Elk Mound.** Adds on the EIA record plus one document each.
- **Every EIA plant missing from GEM** in `work/ids_us-wisconsin.md` (gate `ids_followup`), every queue row in `needs_answer` (gate `queues`), every data center site `data_center_fleets.py` lists (gate `data-centers`), and every plan in `irp_plans.json` (gate `irp-plans`).

## The run

A. **Start and build.**
   - From `scripts/`: fresh pull, `pull_gem_db.py --map-only`, `scope_filter.py`, `export_to_dump.py`.
   - Check Amalia's latest edits against the 2026-11-17 list above and record what changed in this plan.
   - Rerun `worklist.py --state Wisconsin`, `validation_report.py --state Wisconsin`, `assigned_comments.py`, `no_tracker.py`, `eia860m.py`, `match_ids.py`, `irp_sheet.py`, `captive_lng.py` and `location_candidates.py`.
   - Write `scopes/us-wi/note.md` updates, `coverage.json` (every source above, each probed live, with `permit_record` for WARP, `permit_notices` for the DNR notice JSON, and `local_records`), `queues.json`, `irp_plans.json` and `batches/us-wi/extra_tasks.json`. The extra tasks are the three comment threads, the ID false alarms with the answer to give, the 6630-CE-315 and 6630-CE-318 reads, and the leads above.
   - Settle the open probe items: the ERF title route that works from a script, the RBLC address, the DFI detail page, AgendaCenter on the Cloudflare hosts, and the town and village paths.
   - Build the three harvesters with tests.
   - Run `access_check.py --scope us-wi` and fix or wall every unproven entry.
B. **Harvest.**
   - `scopes/us-wi/harvest_permits.py`, `harvest_psc.py` and `harvest_local.py`.
   - `pull_queues.py --state WI`, then `data_center_fleets.py --state Wisconsin`.
   - `irp_plans.py --state Wisconsin`.
   - `check_existing_links.py --state Wisconsin --batch batches/us-wi`.
   - `access_audit.py batches/us-wi --retry`.
C. **Briefs and sweep.**
   - `build_state_brief.py --state Wisconsin --mode update --scope all --batch batches/us-wi --worklist work/worklist_us-wi.csv --extra-tasks batches/us-wi/extra_tasks.json --validation work/validation_us-wisconsin.json --ids work/ids_us-wisconsin.json --irp work/irp_us-wisconsin.json --captive work/captive_us-wisconsin.json --location work/location_us-wi.json --existing-links batches/us-wi/existing_links.json --harvest batches/us-wi/harvest --data-centers`.
   - `build_sweep_args.py --batch batches/us-wi`.
   - The `state-sweep` workflow: Sonnet per plant or plant group, and Opus for the scope-wide agent. The scope-wide agent reads `briefs/_irp.md`, every plan in `irp_plans.json`, the queue answers, the data center list, the local records index, the PSC docket index and every statewide `coverage.json` entry, recording `read` and `date` for each.
D. **Location.** Run Forest Junction and Union Depot, plus any plant handed back with `location_needs_review: true`, through `docs/reference/location.md`. Then `build_sweep_args.py --location-review` for the short Opus pass. Red Oak Ridge's Paris-or-Somers question goes in the same pass.
E. **Assemble and gate.**
   - `assemble_state.py --batch batches/us-wi` and `dedup_check.py --batch batches/us-wi`.
   - `state_gate.py --batch batches/us-wi --validation work/validation_us-wisconsin.json --entity-check --strict-questions --strict-proof`.
   - `qc_checks.py --staged` with zero errors.
   - `entity_lookup.py` for Invenergy's project LLCs, Dairyland, MGE, Vantage's and Meta's site LLCs, and every new owner.
F. **Deliverables and page.**
   - `build_review_package.py --staging-dir batches/us-wi/staging --scope us-wi --mode update --irp` with a fresh stamp.
   - Add `batches/us-wi/staging` to the `amalia` page dirs, then `review_app/build_all.py --only amalia`.
   - Publish to https://claude.ai/artifact/7bnX9RMity3Yw5mdaojNaL from the work profile, then `build_all.py --mark-published amalia`.
G. **Drafts for a person.**
   - IDs to type: Red Oak Ridge EIA 70453, Riverside EIA 64020, South Oak Creek EIA 4041 (not Weston 4130), and the codes for Fitchburg and Elk Mound once added.
   - The IRP boxes to tick, and draft US IRPs tab rows and Notes lines for each utility beyond WEC.
   - Comment-thread replies for Natalia's three threads.
   - Clerk emails for any town with nothing posted, the RBLC export and any LLC lookups the DFI route leaves.
   - The close-out checks before the roster row moves: `validation_report.py --closeout` prints CLOSE-OUT CLEAN and `assigned_comments.py --closeout` prints COMMENTS CLEAN.

## What done looks like

- Every one of the 82 rows has a record or a re-verification, and every in-development unit has a dated status step and a Latest Activity.
- Every lead above is a record or a coverage answer.
- Every `coverage.json` entry carries `read` and `date` or a human wall.
- Every queue request, missing EIA plant, data center site, resource plan and dedup hit is answered.
- The gates pass with `--strict-proof`, and `qc_checks.py --staged` is clean.
- The deliverable pair is built with a fresh stamp, and Amalia's page is rebuilt and published with Wisconsin on it.

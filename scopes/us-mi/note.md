# United States, Michigan

Scope: 61 unit rows across 32 plants in the pull of 2026-10-23 14:09. By status that is 6 pre-construction, 1 construction, 1 mothballed and 53 operating. Amalia Llano finished her own Michigan pass on 2026-10-23, touching 13 rows; this batch is a full update on top of her edits to find what is still missing. Two utility rows are on the US IRPs tab: Consumers Energy and DTE Electric. No captive LNG sheet rows for the state. The validation report has two research fixes (Belle River location source, Lansing Board of Water and Light owner source). Both Assigned Comments threads are closed.

## State context

- Most of the Lower Peninsula is in MISO, the Midcontinent Independent System Operator, Zone 7. The two big utilities are DTE Electric in the southeast and Consumers Energy in the rest of the Lower Peninsula. The Upper Peninsula is MISO Zone 2, served by Upper Michigan Energy Resources (a WEC Energy company), UPPCO and municipal utilities such as Marquette. The southwest corner is served by Indiana Michigan Power, part of AEP, and sits in PJM. Check which market each southwest plant connects to before reading a queue.
- The utility regulator is the Michigan Public Service Commission, called the MPSC. Cases are numbered like U-21090. Its electronic docket system is a Salesforce site at mi-psc.my.site.com; plan files on the US IRPs tab link there. Integrated resource plans are filed at least every five years and name new gas plants and coal retirements.
- Air permits come from the Michigan Department of Environment, Great Lakes, and Energy, called EGLE, Air Quality Division. A new turbine or engine needs a Permit to Install, called a PTI, numbered like APP-2024-0273. Large plants also hold a Renewable Operating Permit, Michigan's name for the federal Title V permit. Every source has a State Registration Number, called an SRN, which joins the permit records. Current permits are in the MiEnviro Portal. EGLE posts applications for big projects under "applications of interest" on michigan.gov. `scopes/us-mi/harvest_permits.py` reads these ahead of a sweep.
- Consumers Energy's plan in Case U-21090 was settled in 2022. The tab notes that Consumers said on March 11, 2026 that it would file a new plan in June 2026 with two new gas plants. GEM holds those as Bay County power station (450 MW) and Genesee County power station (900 MW), both pre-construction with approximate locations and unknown technology.
- DTE Electric's plan was approved in July 2023 in Case U-21193. DTE will file its next plan by December 2026. In October 2025 DTE said it would seek bids for a new combined cycle plant to replace the Monroe coal plant, and that it expects about 1.5 GW of gas additions from 2026 to 2032. GEM holds Handy Township power station (1400 MW, owner listed as DTE Energy Co) and Milan Township power station (700 MW) as pre-construction. Check the owner entity on Handy Township, since every other DTE plant is owned by DTE Electric Co.
- Belle River is DTE's coal plant converting to gas. The gas phase is in GEM as "Unit 1, timepoint 2" (operating from 2026) and "Unit 2, timepoint 2" (construction), with the coal units as timepoint 1. EGLE's permit application for the conversion, APP-2024-0273, is gone from michigan.gov; a saved copy from September 2025 is on the Wayback Machine and has been staged.
- MEC North and MEC South (500 MW each, Development Partners Group, Siemens H class) are the gas project near Marshall in Calhoun County. GEM says 2034; the Environmental Integrity Project's Oil and Gas Watch says 2028.
- Consumers Energy has been buying merchant plants. Check the owner of New Covert (listed as New Covert Generating Co LLC) and Dearborn Industrial Generation against EIA-860 and the MPSC record.

## Watch items to raise with the reviewer

- "48th Street power station" (L100000401789) and "491 E 48th Street power station" (L100000409227) are both City of Holland, unit 9, about 84 MW, from 2000. They look like one plant entered twice.
- The EIA-860M file for September 2026 lists nine gas or oil plants in Michigan that match no GEM plant: T B Simon (Michigan State University), Fermi peakers, Hancock, Northeast and Superior (DTE), George Johnson and Gaylord (Wolverine), University of Michigan, and Livingston (CMS Generation). Several are sets of small units, so check each against the 50 MW threshold the manual applies.
- Midland Cogeneration Venture: EIA-860M gives 1468.6 MW nameplate for unit 1's generators, GEM says 1849 MW. Unit 2 is a 380 MW fuel oil unit marked mothballed.
- Zeeland 1A: EIA-860M says 188.7 MW, GEM says 239 MW. A closed comment from May 2025 says Consumers expected a 50 MW upgrade in June 2025.

## Gotchas

- Coal-to-gas conversions are separate units named "<name>, timepoint 2", with the coal unit as timepoint 1. Belle River follows this.
- The J C Weadock site in Bay County (EIA plant 1720) sits 0.2 km from GEM's point for Bay County power station. That is a retired 18.6 MW turbine, not the new plant; it only shows the new plant's approximate point is on the old Karn and Weadock site.
- freep.com and livingstondaily.com answer 402 and mlive.com 403 to scripts. Run them through `fetch.py`'s full ladder and the Wayback Machine before calling any of them blocked.

# Calibration memo: Maryland, blind run

Stamp 20261002_1535_ET. Built by assemble_state.py from 17 plant reports out of 17 plants in the brief index.

This memo compares what the research found for each plant with what the GEM database already says. The research was done blind. The researcher saw only each plant's name, location and IDs, not the GEM values. Each table row is one field of one unit.

Rows where the two sides agree are already marked match. Every other row has a question mark in the Verdict column. Score it by reading the source, then write one of these: match, GEM wrong, research wrong, both defensible, unresolvable. A row scored GEM wrong is a real error in the database. It should go into the update deliverable from this same run. Fields that are blank on both sides are counted in the totals but not listed.

## Totals

| Verdict | What it means | Count |
|---|---|---|
| match | GEM and the research agree | 283 |
| fill | GEM is blank and the research found a value | 178 |
| change | GEM and the research disagree | 59 |
| research_blank | GEM has a value and the research found nothing | 20 |
| both_blank | both are blank | 303 |
| not_reported | GEM has a value and the research did not mention the field | 8 |
| total | | 851 |

## Constellation (Project 1) power station (L100001080785)

| Unit | Field | GEM value | Research value | Source that resolved it | Verdict |
|---|---|---|---|---|---|
| 1 (G100001090726) | Status | announced | announced | marylandmatters.org | match |
| 1 (G100001090726) | Capacity (MW) | 150.0 | 150.0 | marylandmatters.org | match |
| 1 (G100001090726) | Fuel | fossil gas: natural gas | fossil gas: natural gas | marylandmatters.org | match |
| 1 (G100001090726) | Turbine/Engine Technology | gas turbine | gas turbine | marylandmatters.org | match |
| 1 (G100001090726) | Start year | (blank) | 2029 | marylandmatters.org | ? |
| 1 (G100001090726) | Latest Activity | (blank) | Approved for expedited permitting by the Maryland Public Service Commission in December 2025; permit application due by July 1, 2027 | psc.maryland.gov | ? |
| 1 (G100001090726) | Status Detail | (blank) | Approved for the state's expedited permit process; permit application not yet filed; target commercial operation June 2029 | psc.maryland.gov | ? |
| 1 (G100001090726) | Latitude | 39.4415900 | (blank) | (none) | ? |
| 1 (G100001090726) | Longitude | -76.2187700 | (blank) | (none) | ? |
| 1 (G100001090726) | Location accuracy | approximate | (blank) | (none) | ? |
| 1 (G100001090726) | Owner(s) | Constellation Energy Generation LLC | Constellation Energy Generation, LLC [100%] | marylandmatters.org | match |
| 1 (G100001090726) | Operator(s) | (blank) | Constellation Energy Generation, LLC | marylandmatters.org | ? |

## Constellation (Project 2) power station (L100001080791)

| Unit | Field | GEM value | Research value | Source that resolved it | Verdict |
|---|---|---|---|---|---|
| 1 (G100001090730) | Status | announced | announced | marylandmatters.org | match |
| 1 (G100001090730) | Capacity (MW) | 564.0 | 564.0 | marylandmatters.org | match |
| 1 (G100001090730) | Fuel | fossil gas: natural gas | fossil gas: natural gas | marylandmatters.org | match |
| 1 (G100001090730) | Turbine/Engine Technology | gas turbine | gas turbine | marylandmatters.org | match |
| 1 (G100001090730) | Start year | (blank) | 2029 | marylandmatters.org | ? |
| 1 (G100001090730) | Latest Activity | (blank) | Approved for expedited permitting by the Maryland Public Service Commission in December 2025; permit application due by July 1, 2027 | psc.maryland.gov | ? |
| 1 (G100001090730) | Status Detail | (blank) | Approved for the state's expedited permit process; permit application not yet filed; target commercial operation June 2029 | psc.maryland.gov | ? |
| 1 (G100001090730) | Latitude | 39.4415900 | (blank) | (none) | ? |
| 1 (G100001090730) | Longitude | -76.2187700 | (blank) | (none) | ? |
| 1 (G100001090730) | Location accuracy | approximate | (blank) | (none) | ? |
| 1 (G100001090730) | Owner(s) | Constellation Energy Generation LLC | Constellation Energy Generation, LLC [100%] | marylandmatters.org | match |
| 1 (G100001090730) | Operator(s) | (blank) | Constellation Energy Generation, LLC | marylandmatters.org | ? |

## Brandywine power facility (L100000402511)

| Unit | Field | GEM value | Research value | Source that resolved it | Verdict |
|---|---|---|---|---|---|
| F701 (G100000401771) | Status | operating | operating | eia.gov | match |
| F701 (G100000401771) | Capacity (MW) | 289.0 | 288.8 | eia.gov | match |
| F701 (G100000401771) | Fuel | fossil gas: natural gas, fossil liquids: fuel oil | fossil gas: natural gas, fossil liquids: fuel oil | eia.gov | match |
| F701 (G100000401771) | Turbine/Engine Technology | combined cycle | combined cycle | eia.gov | match |
| F701 (G100000401771) | Capacity Per Engine | (blank) | 98.7 | eia.gov | ? |
| F701 (G100000401771) | Start year | (blank) | 1996 | eia.gov | ? |
| F701 (G100000401771) | CHP | yes | yes | eia.gov | match |
| F701 (G100000401771) | Latest Activity | (blank) | Acquired by Alpha Generation and ArcLight Capital Partners from Onward Energy Holdings, May 2026 | lw.com | ? |
| F701 (G100000401771) | Latitude | 38.6681000 | (blank) | (none) | ? |
| F701 (G100000401771) | Longitude | -76.8678000 | (blank) | (none) | ? |
| F701 (G100000401771) | Owner(s) | Alpha Generation LLC [100%] | Alpha Generation [100%] | lw.com | ? |
| F701 (G100000401771) | Operator(s) | (blank) | Alpha Generation | lw.com | ? |
| F701 (G100000401771) | Location accuracy | exact | exact | eia.gov | match |

## Chalk Point Generating Station (L100000103962)

| Unit | Field | GEM value | Research value | Source that resolved it | Verdict |
|---|---|---|---|---|---|
| 3 (G100000402920) | Status | operating | operating | eia.gov | match |
| 3 (G100000402920) | Capacity (MW) | 659.0 | 659.0 | eia.gov | match |
| 3 (G100000402920) | Start year | 1975 | 1975 | eia.gov | match |
| 3 (G100000402920) | Fuel | fossil gas: natural gas, fossil liquids: fuel oil | fossil gas: natural gas | eia.gov | ? |
| 3 (G100000402920) | Turbine/Engine Technology | steam turbine | steam turbine | eia.gov | match |
| 3 (G100000402920) | Number Of Engines | (blank) | 1 | eia.gov | ? |
| 3 (G100000402920) | Capacity Per Engine | (blank) | 659.0 | eia.gov | ? |
| 3 (G100000402920) | CHP | no | no | eia.gov | match |
| 3 (G100000402920) | Captive industry use | (blank) | no | eia.gov | ? |
| 3 (G100000402920) | Captive non-industry use | (blank) | no | eia.gov | ? |
| 3 (G100000402920) | Owner(s) | Lanyard Power Holdings LLC [100%] | Chalk Point Power, LLC [100%] | eia.gov | ? |
| 3 (G100000402920) | Operator(s) | (blank) | Chalk Point Power, LLC | eia.gov | ? |
| 3 (G100000402920) | Latitude | 38.5438810 | 38.5444 | eia.gov | match |
| 3 (G100000402920) | Longitude | -76.6859580 | -76.6861 | eia.gov | match |
| 3 (G100000402920) | Location accuracy | exact | approximate | eia.gov | ? |
| 4 (G100000402921) | Status | operating | operating | eia.gov | match |
| 4 (G100000402921) | Capacity (MW) | 659.0 | 659.0 | eia.gov | match |
| 4 (G100000402921) | Start year | 1981 | 1981 | eia.gov | match |
| 4 (G100000402921) | Fuel | fossil gas: natural gas, fossil liquids: fuel oil | fossil gas: natural gas | eia.gov | ? |
| 4 (G100000402921) | Turbine/Engine Technology | steam turbine | steam turbine | eia.gov | match |
| 4 (G100000402921) | Number Of Engines | (blank) | 1 | eia.gov | ? |
| 4 (G100000402921) | Capacity Per Engine | (blank) | 659.0 | eia.gov | ? |
| 4 (G100000402921) | CHP | no | no | eia.gov | match |
| 4 (G100000402921) | Captive industry use | (blank) | no | eia.gov | ? |
| 4 (G100000402921) | Captive non-industry use | (blank) | no | eia.gov | ? |
| 4 (G100000402921) | Owner(s) | Lanyard Power Holdings LLC [100%] | Chalk Point Power, LLC [100%] | eia.gov | ? |
| 4 (G100000402921) | Operator(s) | (blank) | Chalk Point Power, LLC | eia.gov | ? |
| 4 (G100000402921) | Latitude | 38.5438810 | 38.5444 | eia.gov | match |
| 4 (G100000402921) | Longitude | -76.6859580 | -76.6861 | eia.gov | match |
| 4 (G100000402921) | Location accuracy | exact | approximate | eia.gov | ? |
| GT3 (G100000402922) | Status | operating | operating | eia.gov | match |
| GT3 (G100000402922) | Capacity (MW) | 103.0 | 103.0 | eia.gov | match |
| GT3 (G100000402922) | Start year | 1991 | 1991 | eia.gov | match |
| GT3 (G100000402922) | Fuel | fossil gas: natural gas, fossil liquids: fuel oil | fossil gas: natural gas, fossil liquids: fuel oil | eia.gov | match |
| GT3 (G100000402922) | Turbine/Engine Technology | gas turbine | gas turbine | eia.gov | match |
| GT3 (G100000402922) | Number Of Engines | (blank) | 1 | eia.gov | ? |
| GT3 (G100000402922) | Capacity Per Engine | (blank) | 103.0 | eia.gov | ? |
| GT3 (G100000402922) | CHP | no | no | eia.gov | match |
| GT3 (G100000402922) | Captive industry use | (blank) | no | eia.gov | ? |
| GT3 (G100000402922) | Captive non-industry use | (blank) | no | eia.gov | ? |
| GT3 (G100000402922) | Owner(s) | Lanyard Power Holdings LLC [100%] | Chalk Point Power, LLC [100%] | eia.gov | ? |
| GT3 (G100000402922) | Operator(s) | (blank) | Chalk Point Power, LLC | eia.gov | ? |
| GT3 (G100000402922) | Latitude | 38.5438810 | 38.5444 | eia.gov | match |
| GT3 (G100000402922) | Longitude | -76.6859580 | -76.6861 | eia.gov | match |
| GT3 (G100000402922) | Location accuracy | exact | approximate | eia.gov | ? |
| GT4 (G100000402923) | Status | operating | operating | eia.gov | match |
| GT4 (G100000402923) | Capacity (MW) | 103.0 | 103.0 | eia.gov | match |
| GT4 (G100000402923) | Start year | 1991 | 1991 | eia.gov | match |
| GT4 (G100000402923) | Fuel | fossil gas: natural gas, fossil liquids: fuel oil | fossil gas: natural gas, fossil liquids: fuel oil | eia.gov | match |
| GT4 (G100000402923) | Turbine/Engine Technology | gas turbine | gas turbine | eia.gov | match |
| GT4 (G100000402923) | Number Of Engines | (blank) | 1 | eia.gov | ? |
| GT4 (G100000402923) | Capacity Per Engine | (blank) | 103.0 | eia.gov | ? |
| GT4 (G100000402923) | CHP | no | no | eia.gov | match |
| GT4 (G100000402923) | Captive industry use | (blank) | no | eia.gov | ? |
| GT4 (G100000402923) | Captive non-industry use | (blank) | no | eia.gov | ? |
| GT4 (G100000402923) | Owner(s) | Lanyard Power Holdings LLC [100%] | Chalk Point Power, LLC [100%] | eia.gov | ? |
| GT4 (G100000402923) | Operator(s) | (blank) | Chalk Point Power, LLC | eia.gov | ? |
| GT4 (G100000402923) | Latitude | 38.5438810 | 38.5444 | eia.gov | match |
| GT4 (G100000402923) | Longitude | -76.6859580 | -76.6861 | eia.gov | match |
| GT4 (G100000402923) | Location accuracy | exact | approximate | eia.gov | ? |
| GT5 (G100000402924) | Status | operating | operating | eia.gov | match |
| GT5 (G100000402924) | Capacity (MW) | 125.0 | 125.0 | eia.gov | match |
| GT5 (G100000402924) | Start year | 1991 | 1991 | eia.gov | match |
| GT5 (G100000402924) | Fuel | fossil gas: natural gas, fossil liquids: fuel oil | fossil gas: natural gas, fossil liquids: fuel oil | eia.gov | match |
| GT5 (G100000402924) | Turbine/Engine Technology | gas turbine | gas turbine | eia.gov | match |
| GT5 (G100000402924) | Number Of Engines | (blank) | 1 | eia.gov | ? |
| GT5 (G100000402924) | Capacity Per Engine | (blank) | 125.0 | eia.gov | ? |
| GT5 (G100000402924) | CHP | no | no | eia.gov | match |
| GT5 (G100000402924) | Captive industry use | (blank) | no | eia.gov | ? |
| GT5 (G100000402924) | Captive non-industry use | (blank) | no | eia.gov | ? |
| GT5 (G100000402924) | Owner(s) | Lanyard Power Holdings LLC [100%] | Chalk Point Power, LLC [100%] | eia.gov | ? |
| GT5 (G100000402924) | Operator(s) | (blank) | Chalk Point Power, LLC | eia.gov | ? |
| GT5 (G100000402924) | Latitude | 38.5438810 | 38.5444 | eia.gov | match |
| GT5 (G100000402924) | Longitude | -76.6859580 | -76.6861 | eia.gov | match |
| GT5 (G100000402924) | Location accuracy | exact | approximate | eia.gov | ? |
| GT6 (G100000402925) | Status | operating | operating | eia.gov | match |
| GT6 (G100000402925) | Capacity (MW) | 125.0 | 125.0 | eia.gov | match |
| GT6 (G100000402925) | Start year | 1991 | 1991 | eia.gov | match |
| GT6 (G100000402925) | Fuel | fossil gas: natural gas, fossil liquids: fuel oil | fossil gas: natural gas, fossil liquids: fuel oil | eia.gov | match |
| GT6 (G100000402925) | Turbine/Engine Technology | gas turbine | gas turbine | eia.gov | match |
| GT6 (G100000402925) | Number Of Engines | (blank) | 1 | eia.gov | ? |
| GT6 (G100000402925) | Capacity Per Engine | (blank) | 125.0 | eia.gov | ? |
| GT6 (G100000402925) | CHP | no | no | eia.gov | match |
| GT6 (G100000402925) | Captive industry use | (blank) | no | eia.gov | ? |
| GT6 (G100000402925) | Captive non-industry use | (blank) | no | eia.gov | ? |
| GT6 (G100000402925) | Owner(s) | Lanyard Power Holdings LLC [100%] | Chalk Point Power, LLC [100%] | eia.gov | ? |
| GT6 (G100000402925) | Operator(s) | (blank) | Chalk Point Power, LLC | eia.gov | ? |
| GT6 (G100000402925) | Latitude | 38.5438810 | 38.5444 | eia.gov | match |
| GT6 (G100000402925) | Longitude | -76.6859580 | -76.6861 | eia.gov | match |
| GT6 (G100000402925) | Location accuracy | exact | approximate | eia.gov | ? |
| SGT1 (G100000409452) | Status | operating | operating | eia.gov | match |
| SGT1 (G100000409452) | Capacity (MW) | 94.0 | 94.0 | eia.gov | match |
| SGT1 (G100000409452) | Start year | 1990 | 1990 | eia.gov | match |
| SGT1 (G100000409452) | Fuel | fossil gas: natural gas, fossil liquids: fuel oil | fossil liquids: fuel oil, fossil gas: natural gas | eia.gov | match |
| SGT1 (G100000409452) | Turbine/Engine Technology | gas turbine | gas turbine | eia.gov | match |
| SGT1 (G100000409452) | Number Of Engines | (blank) | 1 | eia.gov | ? |
| SGT1 (G100000409452) | Capacity Per Engine | (blank) | 94.0 | eia.gov | ? |
| SGT1 (G100000409452) | CHP | no | no | eia.gov | match |
| SGT1 (G100000409452) | Captive industry use | (blank) | no | eia.gov | ? |
| SGT1 (G100000409452) | Captive non-industry use | (blank) | no | eia.gov | ? |
| SGT1 (G100000409452) | Owner(s) | NRG Chalk Point CT LLC [100%] | Chalk Point Power, LLC [100%] | eia.gov | ? |
| SGT1 (G100000409452) | Operator(s) | (blank) | Chalk Point Power, LLC | eia.gov | ? |
| SGT1 (G100000409452) | Latitude | 38.5438810 | 38.5444 | eia.gov | match |
| SGT1 (G100000409452) | Longitude | -76.6859580 | -76.6861 | eia.gov | match |
| SGT1 (G100000409452) | Location accuracy | exact | approximate | eia.gov | ? |

## Cove Point LNG Terminal power station (L100000401847)

| Unit | Field | GEM value | Research value | Source that resolved it | Verdict |
|---|---|---|---|---|---|
| CC1-5STA (G100000409442) | Capacity (MW) | 65.0 | 65 | psc.maryland.gov | match |
| CC1-5STA (G100000409442) | Turbine/Engine Technology | steam turbine | steam turbine | psc.maryland.gov | match |
| CC1-5STA (G100000409442) | Equipment Manufacturer/Model | (blank) | GE Frame 7EA gas turbines (heat source) | psc.maryland.gov | ? |
| CC1-5STA (G100000409442) | Fuel | fossil gas: natural gas | fossil gas: natural gas | psc.maryland.gov | match |
| CC1-5STA (G100000409442) | Start year | (blank) | 2018 | lngindustry.com | ? |
| CC1-5STA (G100000409442) | Status | operating | operating | lngindustry.com | match |
| CC1-5STA (G100000409442) | Captive industry use | (blank) | power | psc.maryland.gov | ? |
| CC1-5STA (G100000409442) | CHP | no | (blank) | (none) | ? |
| CC1-5STA (G100000409442) | Captive industry type | LNG production / liquefaction | (blank) | (none) | ? |
| CC1-5STA (G100000409442) | Latitude | 38.3854560 | (blank) | (none) | ? |
| CC1-5STA (G100000409442) | Longitude | -76.4098000 | (blank) | (none) | ? |
| CC1-5STA (G100000409442) | Location accuracy | exact | (blank) | (none) | ? |
| CC1-5STA (G100000409442) | Owner(s) | Cove Point LNG LP [100%] | BHE GT&S [75%]; Brookfield Infrastructure [25%] | ogj.com | ? |
| CC1-5STA (G100000409442) | Operator(s) | (blank) | BHE GT&S | ogj.com | ? |
| CC1-5STB (G100000409441) | Capacity (MW) | 65.0 | 65 | psc.maryland.gov | match |
| CC1-5STB (G100000409441) | Turbine/Engine Technology | steam turbine | steam turbine | psc.maryland.gov | match |
| CC1-5STB (G100000409441) | Equipment Manufacturer/Model | (blank) | GE Frame 7EA gas turbines (heat source) | psc.maryland.gov | ? |
| CC1-5STB (G100000409441) | Fuel | fossil gas: natural gas | fossil gas: natural gas | psc.maryland.gov | match |
| CC1-5STB (G100000409441) | Start year | (blank) | 2018 | lngindustry.com | ? |
| CC1-5STB (G100000409441) | Status | operating | operating | lngindustry.com | match |
| CC1-5STB (G100000409441) | Captive industry use | (blank) | power | psc.maryland.gov | ? |
| CC1-5STB (G100000409441) | CHP | no | (blank) | (none) | ? |
| CC1-5STB (G100000409441) | Captive industry type | LNG production / liquefaction | (blank) | (none) | ? |
| CC1-5STB (G100000409441) | Latitude | 38.3854560 | (blank) | (none) | ? |
| CC1-5STB (G100000409441) | Longitude | -76.4098000 | (blank) | (none) | ? |
| CC1-5STB (G100000409441) | Location accuracy | exact | (blank) | (none) | ? |
| CC1-5STB (G100000409441) | Owner(s) | Cove Point LNG LP [100%] | BHE GT&S [75%]; Brookfield Infrastructure [25%] | ogj.com | ? |
| CC1-5STB (G100000409441) | Operator(s) | (blank) | BHE GT&S | ogj.com | ? |

## CPV St. Charles energy center (L100000401837)

| Unit | Field | GEM value | Research value | Source that resolved it | Verdict |
|---|---|---|---|---|---|
| G601 (G100000402033) | Status | operating | operating | eia.gov | match |
| G601 (G100000402033) | Capacity (MW) | 775.0 | 775.3 | eia.gov | match |
| G601 (G100000402033) | Fuel | fossil gas: natural gas | fossil gas: natural gas | eia.gov | match |
| G601 (G100000402033) | Turbine/Engine Technology | combined cycle | combined cycle | eia.gov | match |
| G601 (G100000402033) | Equipment Manufacturer/Model | (blank) | GE 7F.05 gas turbine (x2); GE D402 steam turbine | powermag.com | ? |
| G601 (G100000402033) | Number Of Engines | (blank) | 2 | powermag.com | ? |
| G601 (G100000402033) | Capacity Per Engine | (blank) | 223.6 | eia.gov | ? |
| G601 (G100000402033) | Start year | 2017 | 2017 | eia.gov | match |
| G601 (G100000402033) | CHP | no | no | eia.gov | match |
| G601 (G100000402033) | Owner(s) | CPV Maryland LLC [100%] | Competitive Power Ventures [25%]; Marubeni [25%]; Toyota Tsusho [25%]; Osaka Gas USA [25%] | energymonitor.ai | ? |
| G601 (G100000402033) | Operator(s) | (blank) | EthosEnergy Power Plant Services | powermag.com | ? |
| G601 (G100000402033) | Latitude | 38.5686000 | 38.5686 | eia.gov | match |
| G601 (G100000402033) | Longitude | -76.8919000 | -76.8919 | eia.gov | match |
| G601 (G100000402033) | Location accuracy | exact | approximate | eia.gov | ? |
| G601 (G100000402033) | Captive industry use | (blank) | none | eia.gov | ? |

## Dickerson Generating Station (L100000103964)

| Unit | Field | GEM value | Research value | Source that resolved it | Verdict |
|---|---|---|---|---|---|
| GT2 (G100000402929) | Status | operating | operating | eia.gov | match |
| GT2 (G100000402929) | Capacity (MW) | 163.0 | 163.0 | eia.gov | match |
| GT2 (G100000402929) | Fuel | fossil gas: natural gas, fossil liquids: fuel oil | fossil gas: natural gas, fossil liquids: fuel oil | eia.gov | match |
| GT2 (G100000402929) | Turbine/Engine Technology | gas turbine | gas turbine | eia.gov | match |
| GT2 (G100000402929) | Equipment Manufacturer/Model | (blank) | General Electric Frame 7F | mde.maryland.gov | ? |
| GT2 (G100000402929) | Number Of Engines | (blank) | 1 | mde.maryland.gov | ? |
| GT2 (G100000402929) | Capacity Per Engine | (blank) | 163.0 | eia.gov | ? |
| GT2 (G100000402929) | Start year | 1992 | 1992 | eia.gov | match |
| GT2 (G100000402929) | Latest Activity | (blank) | Operated 1,103 hours in 2025 | mde.maryland.gov | ? |
| GT2 (G100000402929) | CHP | no | no | eia.gov | match |
| GT2 (G100000402929) | Captive industry use | (blank) | no | eia.gov | ? |
| GT2 (G100000402929) | Captive non-industry use | (blank) | no | eia.gov | ? |
| GT2 (G100000402929) | Owner(s) | Dickerson Power LLC [100%] | Dickerson Power, LLC [100%] | eia.gov | match |
| GT2 (G100000402929) | Operator(s) | (blank) | Dickerson Power, LLC | mde.maryland.gov | ? |
| GT2 (G100000402929) | Latitude | 39.2092670 | 39.2097 | eia.gov | match |
| GT2 (G100000402929) | Longitude | -77.4640280 | -77.4644 | eia.gov | match |
| GT2 (G100000402929) | Location accuracy | exact | approximate | eia.gov | ? |
| GT3 (G100000402930) | Status | operating | operating | eia.gov | match |
| GT3 (G100000402930) | Capacity (MW) | 163.0 | 163.0 | eia.gov | match |
| GT3 (G100000402930) | Fuel | fossil gas: natural gas, fossil liquids: fuel oil | fossil gas: natural gas, fossil liquids: fuel oil | eia.gov | match |
| GT3 (G100000402930) | Turbine/Engine Technology | gas turbine | gas turbine | eia.gov | match |
| GT3 (G100000402930) | Equipment Manufacturer/Model | (blank) | General Electric Frame 7F | mde.maryland.gov | ? |
| GT3 (G100000402930) | Number Of Engines | (blank) | 1 | mde.maryland.gov | ? |
| GT3 (G100000402930) | Capacity Per Engine | (blank) | 163.0 | eia.gov | ? |
| GT3 (G100000402930) | Start year | 1992 | 1992 | eia.gov | match |
| GT3 (G100000402930) | Latest Activity | (blank) | Operated 1,096 hours in 2025 | mde.maryland.gov | ? |
| GT3 (G100000402930) | CHP | no | no | eia.gov | match |
| GT3 (G100000402930) | Captive industry use | (blank) | no | eia.gov | ? |
| GT3 (G100000402930) | Captive non-industry use | (blank) | no | eia.gov | ? |
| GT3 (G100000402930) | Owner(s) | Dickerson Power LLC [100%] | Dickerson Power, LLC [100%] | eia.gov | match |
| GT3 (G100000402930) | Operator(s) | (blank) | Dickerson Power, LLC | mde.maryland.gov | ? |
| GT3 (G100000402930) | Latitude | 39.2092670 | 39.2097 | eia.gov | match |
| GT3 (G100000402930) | Longitude | -77.4640280 | -77.4644 | eia.gov | match |
| GT3 (G100000402930) | Location accuracy | exact | approximate | eia.gov | ? |

## Essential Power Rock Springs station (L100000401929)

| Unit | Field | GEM value | Research value | Source that resolved it | Verdict |
|---|---|---|---|---|---|
| 1 (G100000402859) | Status | operating | operating | eia.gov | match |
| 1 (G100000402859) | Capacity (MW) | 199.0 | 198.9 | eia.gov | match |
| 1 (G100000402859) | Fuel | fossil gas: natural gas | fossil gas: natural gas | eia.gov | match |
| 1 (G100000402859) | Turbine/Engine Technology | gas turbine | gas turbine | stg-mde.maryland.gov | match |
| 1 (G100000402859) | Equipment Manufacturer/Model | (blank) | General Electric 7FA | stg-mde.maryland.gov | ? |
| 1 (G100000402859) | Number Of Engines | (blank) | 1 | stg-mde.maryland.gov | ? |
| 1 (G100000402859) | Capacity Per Engine | (blank) | 198.9 | eia.gov | ? |
| 1 (G100000402859) | Start year | 2003 | 2003 | eia.gov | match |
| 1 (G100000402859) | CHP | no | no | eia.gov | match |
| 1 (G100000402859) | Owner(s) | Essential Power Rock Springs LLC [100%] | Essential Power Rock Springs LLC [50%]; Old Dominion Electric Cooperative [50%] | cogentrix.com | ? |
| 1 (G100000402859) | Operator(s) | (blank) | Essential Power Operating Services LLC | eia.gov | ? |
| 1 (G100000402859) | Latitude | 39.7190100 | 39.71901 | eia.gov | match |
| 1 (G100000402859) | Longitude | -76.1597600 | -76.15976 | eia.gov | match |
| 1 (G100000402859) | Location accuracy | exact | approximate | eia.gov | ? |
| 1 (G100000402859) | Captive industry use | (blank) | no | eia.gov | ? |
| 1 (G100000402859) | Captive non-industry use | (blank) | no | eia.gov | ? |
| 2 (G100000402860) | Status | operating | operating | eia.gov | match |
| 2 (G100000402860) | Capacity (MW) | 176.0 | 198.9 | eia.gov | ? |
| 2 (G100000402860) | Fuel | fossil gas: natural gas | fossil gas: natural gas | eia.gov | match |
| 2 (G100000402860) | Turbine/Engine Technology | gas turbine | gas turbine | stg-mde.maryland.gov | match |
| 2 (G100000402860) | Equipment Manufacturer/Model | (blank) | General Electric 7FA | stg-mde.maryland.gov | ? |
| 2 (G100000402860) | Number Of Engines | (blank) | 1 | stg-mde.maryland.gov | ? |
| 2 (G100000402860) | Capacity Per Engine | (blank) | 198.9 | eia.gov | ? |
| 2 (G100000402860) | Start year | 2003 | 2003 | eia.gov | match |
| 2 (G100000402860) | CHP | no | no | eia.gov | match |
| 2 (G100000402860) | Owner(s) | Essential Power Rock Springs LLC [100%] | Essential Power Rock Springs LLC [50%]; Old Dominion Electric Cooperative [50%] | cogentrix.com | ? |
| 2 (G100000402860) | Operator(s) | (blank) | Essential Power Operating Services LLC | eia.gov | ? |
| 2 (G100000402860) | Latitude | 39.7190100 | 39.71901 | eia.gov | match |
| 2 (G100000402860) | Longitude | -76.1597600 | -76.15976 | eia.gov | match |
| 2 (G100000402860) | Location accuracy | exact | approximate | eia.gov | ? |
| 2 (G100000402860) | Captive industry use | (blank) | no | eia.gov | ? |
| 2 (G100000402860) | Captive non-industry use | (blank) | no | eia.gov | ? |
| 3 (G100000402861) | Status | operating | operating | eia.gov | match |
| 3 (G100000402861) | Capacity (MW) | 199.0 | 198.9 | eia.gov | match |
| 3 (G100000402861) | Fuel | fossil gas: natural gas | fossil gas: natural gas | eia.gov | match |
| 3 (G100000402861) | Turbine/Engine Technology | gas turbine | gas turbine | stg-mde.maryland.gov | match |
| 3 (G100000402861) | Equipment Manufacturer/Model | (blank) | General Electric 7FA | stg-mde.maryland.gov | ? |
| 3 (G100000402861) | Number Of Engines | (blank) | 1 | stg-mde.maryland.gov | ? |
| 3 (G100000402861) | Capacity Per Engine | (blank) | 198.9 | eia.gov | ? |
| 3 (G100000402861) | Start year | 2003 | 2003 | eia.gov | match |
| 3 (G100000402861) | CHP | no | no | eia.gov | match |
| 3 (G100000402861) | Owner(s) | Essential Power Rock Springs LLC [100%] | Essential Power Rock Springs LLC [50%]; Old Dominion Electric Cooperative [50%] | cogentrix.com | ? |
| 3 (G100000402861) | Operator(s) | (blank) | Essential Power Operating Services LLC | eia.gov | ? |
| 3 (G100000402861) | Latitude | 39.7190100 | 39.71901 | eia.gov | match |
| 3 (G100000402861) | Longitude | -76.1597600 | -76.15976 | eia.gov | match |
| 3 (G100000402861) | Location accuracy | exact | approximate | eia.gov | ? |
| 3 (G100000402861) | Captive industry use | (blank) | no | eia.gov | ? |
| 3 (G100000402861) | Captive non-industry use | (blank) | no | eia.gov | ? |
| 4 (G100000402862) | Status | operating | operating | eia.gov | match |
| 4 (G100000402862) | Capacity (MW) | 199.0 | 198.9 | eia.gov | match |
| 4 (G100000402862) | Fuel | fossil gas: natural gas | fossil gas: natural gas | eia.gov | match |
| 4 (G100000402862) | Turbine/Engine Technology | gas turbine | gas turbine | stg-mde.maryland.gov | match |
| 4 (G100000402862) | Equipment Manufacturer/Model | (blank) | General Electric 7FA | stg-mde.maryland.gov | ? |
| 4 (G100000402862) | Number Of Engines | (blank) | 1 | stg-mde.maryland.gov | ? |
| 4 (G100000402862) | Capacity Per Engine | (blank) | 198.9 | eia.gov | ? |
| 4 (G100000402862) | Start year | 2003 | 2003 | eia.gov | match |
| 4 (G100000402862) | CHP | no | no | eia.gov | match |
| 4 (G100000402862) | Owner(s) | Essential Power Rock Springs LLC [100%] | Essential Power Rock Springs LLC [50%]; Old Dominion Electric Cooperative [50%] | cogentrix.com | ? |
| 4 (G100000402862) | Operator(s) | (blank) | Essential Power Operating Services LLC | eia.gov | ? |
| 4 (G100000402862) | Latitude | 39.7190100 | 39.71901 | eia.gov | match |
| 4 (G100000402862) | Longitude | -76.1597600 | -76.15976 | eia.gov | match |
| 4 (G100000402862) | Location accuracy | exact | approximate | eia.gov | ? |
| 4 (G100000402862) | Captive industry use | (blank) | no | eia.gov | ? |
| 4 (G100000402862) | Captive non-industry use | (blank) | no | eia.gov | ? |

## Herbert Wagner Generating Station (L100000103965)

| Unit | Field | GEM value | Research value | Source that resolved it | Verdict |
|---|---|---|---|---|---|
| 1 (G100000402976) | Status | retired | retired | eia.gov | match |
| 1 (G100000402976) | Capacity (MW) | 133.0 | 132.8 | eia.gov | match |
| 1 (G100000402976) | Fuel | fossil gas: natural gas, fossil liquids: fuel oil | fossil liquids: fuel oil | eia.gov | ? |
| 1 (G100000402976) | Turbine/Engine Technology | steam turbine | steam turbine | eia.gov | match |
| 1 (G100000402976) | Start year | (blank) | 1956 | eia.gov | ? |
| 1 (G100000402976) | CHP | no | no | eia.gov | match |
| 1 (G100000402976) | Retired year | (blank) | 2025 | eia.gov | ? |
| 1 (G100000402976) | Status Detail | AL: October 2025 report has this as retired JM: EIA June 2025 has this as retired NF 5/22/25: Retirement delayed until May 2029. PJM is looking to pushback retirement to 2028, https://www.powermag.com/pjm-urges-delayed-retirement-of-840-mw-fossil-fuel-power-plant-citing-reliability-impacts/?utm_source=CP&utm_medium=email&utm_id=02072024&oly_enc_id=2515H1512489C1W | (blank) | (none) | ? |
| 1 (G100000402976) | Owner(s) | H.A. Wagner LLC [100%] | H.A. Wagner LLC [100%] | eia.gov | match |
| 1 (G100000402976) | Latitude | 39.1788330 | 39.1781 | eia.gov | match |
| 1 (G100000402976) | Longitude | -76.5273300 | -76.5268 | eia.gov | match |
| 1 (G100000402976) | Location accuracy | exact | approximate | eia.gov | ? |
| 4 (G100000414261) | Status | operating | operating | eia.gov | match |
| 4 (G100000414261) | Capacity (MW) | 414.7 | 414.7 | eia.gov | match |
| 4 (G100000414261) | Fuel | fossil liquids: fuel oil | fossil liquids: fuel oil | eia.gov | match |
| 4 (G100000414261) | Turbine/Engine Technology | steam turbine | steam turbine | eia.gov | match |
| 4 (G100000414261) | Start year | 1972 | 1972 | eia.gov | match |
| 4 (G100000414261) | CHP | no | no | eia.gov | match |
| 4 (G100000414261) | Planned retire | 2029 | 2029 | eia.gov | match |
| 4 (G100000414261) | Latest Activity | (blank) | Maryland reliability agreement keeps units running to May 2029 | powermag.com | ? |
| 4 (G100000414261) | Status Detail | NF 5/22/25: Retirement delayed until May 2029. PJM is looking to pushback retirement to 2028, https://www.powermag.com/pjm-urges-delayed-retirement-of-840-mw-fossil-fuel-power-plant-citing-reliability-impacts/?utm_source=CP&utm_medium=email&utm_id=02072024&oly_enc_id=2515H1512489C1W | (blank) | (none) | ? |
| 4 (G100000414261) | Owner(s) | H.A. Wagner LLC [100%] | H.A. Wagner LLC [100%] | eia.gov | match |
| 4 (G100000414261) | Latitude | 39.1788330 | 39.1781 | eia.gov | match |
| 4 (G100000414261) | Longitude | -76.5273300 | -76.5268 | eia.gov | match |
| 4 (G100000414261) | Location accuracy | exact | approximate | eia.gov | ? |
| Unit 3, timepoint 2 (G100001028230) | Status | operating | operating | eia.gov | match |
| Unit 3, timepoint 2 (G100001028230) | Capacity (MW) | 359.0 | 359.0 | eia.gov | match |
| Unit 3, timepoint 2 (G100001028230) | Fuel | fossil liquids: fuel oil | fossil liquids: fuel oil | eia.gov | match |
| Unit 3, timepoint 2 (G100001028230) | Turbine/Engine Technology | unknown | steam turbine | eia.gov | ? |
| Unit 3, timepoint 2 (G100001028230) | Start year | 2023 | 1966 | eia.gov | ? |
| Unit 3, timepoint 2 (G100001028230) | CHP | (blank) | no | eia.gov | ? |
| Unit 3, timepoint 2 (G100001028230) | Planned retire | 2029 | 2029 | eia.gov | match |
| Unit 3, timepoint 2 (G100001028230) | Conversion/replacement? | conversion | yes | powermag.com | ? |
| Unit 3, timepoint 2 (G100001028230) | Latest Activity | (blank) | Maryland reliability agreement keeps units running to May 2029 | powermag.com | ? |
| Unit 3, timepoint 2 (G100001028230) | Status Detail | NF 5/22/25: Retirement delayed until May 2029. Converted to fuel oil in late 2023 | (blank) | (none) | ? |
| Unit 3, timepoint 2 (G100001028230) | Owner(s) | H.A. Wagner LLC [100%] | H.A. Wagner LLC [100%] | eia.gov | match |
| Unit 3, timepoint 2 (G100001028230) | Latitude | 39.1788330 | 39.1781 | eia.gov | match |
| Unit 3, timepoint 2 (G100001028230) | Longitude | -76.5273300 | -76.5268 | eia.gov | match |
| Unit 3, timepoint 2 (G100001028230) | Location accuracy | exact | approximate | eia.gov | ? |

## Keys energy center (L100000402218)

| Unit | Field | GEM value | Research value | Source that resolved it | Verdict |
|---|---|---|---|---|---|
| CC1 (G100000402089) | Status | operating | operating | eia.gov | match |
| CC1 (G100000402089) | Capacity (MW) | 831.0 | 830.6 | eia.gov | match |
| CC1 (G100000402089) | Fuel | fossil gas: natural gas | fossil gas: natural gas | eia.gov | match |
| CC1 (G100000402089) | Turbine/Engine Technology | combined cycle | combined cycle | eia.gov | match |
| CC1 (G100000402089) | Equipment Manufacturer/Model | (blank) | Siemens SGT6-5000F | power-technology.com | ? |
| CC1 (G100000402089) | Start year | 2018 | 2018 | eia.gov | match |
| CC1 (G100000402089) | CHP | no | no | eia.gov | match |
| CC1 (G100000402089) | Latest Activity | (blank) | operating | gridinfo.com | ? |
| CC1 (G100000402089) | Status Detail | NF 7/22/25: GTs upgrades to increase capacity by 56 MW. Could be completed in 2027 https://www.prnewswire.com/news-releases/alphagen-projects-selected-by-pjm-for-expedited-interconnection-302449180.html PJM Project ID - AH1-744. | (blank) | (none) | ? |
| CC1 (G100000402089) | Owner(s) | Alpha Generation LLC [100%] | Parkway Generation Keys Energy Center LLC [100%] | eia.gov | ? |
| CC1 (G100000402089) | Operator(s) | Alpha Generation | Parkway Generation Keys Energy Center LLC | eia.gov | ? |
| CC1 (G100000402089) | Latitude | 38.6955190 | 38.695519 | eia.gov | match |
| CC1 (G100000402089) | Longitude | -76.8277900 | -76.82779 | eia.gov | match |
| CC1 (G100000402089) | Location accuracy | exact | exact | eia.gov | match |

## Morgantown Generating Station (L100000103967)

| Unit | Field | GEM value | Research value | Source that resolved it | Verdict |
|---|---|---|---|---|---|
| 3 (G100000414155) | Status | operating | operating | eia.gov | match |
| 3 (G100000414155) | Capacity (MW) | 65.0 | 65.0 | eia.gov | match |
| 3 (G100000414155) | Fuel | fossil liquids: fuel oil | fossil liquids: fuel oil | eia.gov | match |
| 3 (G100000414155) | Turbine/Engine Technology | gas turbine | gas turbine | mde.maryland.gov | match |
| 3 (G100000414155) | Equipment Manufacturer/Model | (blank) | General Electric Frame 7 | mde.maryland.gov | ? |
| 3 (G100000414155) | Number Of Engines | (blank) | 1 | mde.maryland.gov | ? |
| 3 (G100000414155) | Capacity Per Engine | (blank) | 65.0 | mde.maryland.gov | ? |
| 3 (G100000414155) | Start year | 1973 | 1973 | eia.gov | match |
| 3 (G100000414155) | CHP | no | no | eia.gov | match |
| 3 (G100000414155) | Owner(s) | Lanyard Power Holdings LLC [100%] | Morgantown Power, LLC [100%] | eia.gov | ? |
| 3 (G100000414155) | Operator(s) | (blank) | Lanyard Power Holdings, LLC | eia.gov | ? |
| 3 (G100000414155) | Latitude | 38.3595940 | 38.3592 | eia.gov | match |
| 3 (G100000414155) | Longitude | -76.9757250 | -76.9767 | eia.gov | match |
| 3 (G100000414155) | Location accuracy | exact | approximate | eia.gov | ? |
| 3 (G100000414155) | Captive industry use | (blank) | no | eia.gov | ? |
| 3 (G100000414155) | Captive non-industry use | (blank) | no | eia.gov | ? |
| 4 (G100000414154) | Status | operating | operating | eia.gov | match |
| 4 (G100000414154) | Capacity (MW) | 65.0 | 65.0 | eia.gov | match |
| 4 (G100000414154) | Fuel | fossil liquids: fuel oil | fossil liquids: fuel oil | eia.gov | match |
| 4 (G100000414154) | Turbine/Engine Technology | gas turbine | gas turbine | mde.maryland.gov | match |
| 4 (G100000414154) | Equipment Manufacturer/Model | (blank) | General Electric Frame 7 | mde.maryland.gov | ? |
| 4 (G100000414154) | Number Of Engines | (blank) | 1 | mde.maryland.gov | ? |
| 4 (G100000414154) | Capacity Per Engine | (blank) | 65.0 | mde.maryland.gov | ? |
| 4 (G100000414154) | Start year | 1973 | 1973 | eia.gov | match |
| 4 (G100000414154) | CHP | no | no | eia.gov | match |
| 4 (G100000414154) | Owner(s) | Lanyard Power Holdings LLC [100%] | Morgantown Power, LLC [100%] | eia.gov | ? |
| 4 (G100000414154) | Operator(s) | (blank) | Lanyard Power Holdings, LLC | eia.gov | ? |
| 4 (G100000414154) | Latitude | 38.3595940 | 38.3592 | eia.gov | match |
| 4 (G100000414154) | Longitude | -76.9757250 | -76.9767 | eia.gov | match |
| 4 (G100000414154) | Location accuracy | exact | approximate | eia.gov | ? |
| 4 (G100000414154) | Captive industry use | (blank) | no | eia.gov | ? |
| 4 (G100000414154) | Captive non-industry use | (blank) | no | eia.gov | ? |
| 5 (G100000414153) | Status | retired | operating | eia.gov | ? |
| 5 (G100000414153) | Capacity (MW) | 65.0 | 65.0 | eia.gov | match |
| 5 (G100000414153) | Fuel | fossil liquids: fuel oil | fossil liquids: fuel oil | eia.gov | match |
| 5 (G100000414153) | Turbine/Engine Technology | gas turbine | gas turbine | mde.maryland.gov | match |
| 5 (G100000414153) | Equipment Manufacturer/Model | (blank) | General Electric Frame 7 | mde.maryland.gov | ? |
| 5 (G100000414153) | Number Of Engines | (blank) | 1 | mde.maryland.gov | ? |
| 5 (G100000414153) | Capacity Per Engine | (blank) | 65.0 | mde.maryland.gov | ? |
| 5 (G100000414153) | Start year | (blank) | 1973 | eia.gov | ? |
| 5 (G100000414153) | CHP | no | no | eia.gov | match |
| 5 (G100000414153) | Owner(s) | Lanyard Power Holdings LLC [100%] | Morgantown Power, LLC [100%] | eia.gov | ? |
| 5 (G100000414153) | Operator(s) | (blank) | Lanyard Power Holdings, LLC | eia.gov | ? |
| 5 (G100000414153) | Latitude | 38.3595940 | 38.3592 | eia.gov | match |
| 5 (G100000414153) | Longitude | -76.9757250 | -76.9767 | eia.gov | match |
| 5 (G100000414153) | Location accuracy | exact | approximate | eia.gov | ? |
| 5 (G100000414153) | Captive industry use | (blank) | no | eia.gov | ? |
| 5 (G100000414153) | Captive non-industry use | (blank) | no | eia.gov | ? |
| 6 (G100000414152) | Status | retired | operating | eia.gov | ? |
| 6 (G100000414152) | Capacity (MW) | 65.0 | 65.0 | eia.gov | match |
| 6 (G100000414152) | Fuel | fossil liquids: fuel oil | fossil liquids: fuel oil | eia.gov | match |
| 6 (G100000414152) | Turbine/Engine Technology | gas turbine | gas turbine | mde.maryland.gov | match |
| 6 (G100000414152) | Equipment Manufacturer/Model | (blank) | General Electric Frame 7 | mde.maryland.gov | ? |
| 6 (G100000414152) | Number Of Engines | (blank) | 1 | mde.maryland.gov | ? |
| 6 (G100000414152) | Capacity Per Engine | (blank) | 65.0 | mde.maryland.gov | ? |
| 6 (G100000414152) | Start year | (blank) | 1973 | eia.gov | ? |
| 6 (G100000414152) | CHP | no | no | eia.gov | match |
| 6 (G100000414152) | Owner(s) | Lanyard Power Holdings LLC [100%] | Morgantown Power, LLC [100%] | eia.gov | ? |
| 6 (G100000414152) | Operator(s) | (blank) | Lanyard Power Holdings, LLC | eia.gov | ? |
| 6 (G100000414152) | Latitude | 38.3595940 | 38.3592 | eia.gov | match |
| 6 (G100000414152) | Longitude | -76.9757250 | -76.9767 | eia.gov | match |
| 6 (G100000414152) | Location accuracy | exact | approximate | eia.gov | ? |
| 6 (G100000414152) | Captive industry use | (blank) | no | eia.gov | ? |
| 6 (G100000414152) | Captive non-industry use | (blank) | no | eia.gov | ? |

## NRG Chalk Point CT power station (L100001047726)

| Unit | Field | GEM value | Research value | Source that resolved it | Verdict |
|---|---|---|---|---|---|
| SGT1 (G100001054395) | Status | operating | operating | eia.gov | match |
| SGT1 (G100001054395) | Capacity (MW) | 94.0 | 94.0 | eia.gov | match |
| SGT1 (G100001054395) | Fuel | fossil liquids: diesel | fossil liquids: fuel oil, fossil gas: natural gas | eia.gov | ? |
| SGT1 (G100001054395) | Turbine/Engine Technology | gas turbine | gas turbine | eia.gov | match |
| SGT1 (G100001054395) | Number Of Engines | (blank) | 1 | eia.gov | ? |
| SGT1 (G100001054395) | Capacity Per Engine | (blank) | 94.0 | eia.gov | ? |
| SGT1 (G100001054395) | Start year | (blank) | 1990 | eia.gov | ? |
| SGT1 (G100001054395) | CHP | no | no | eia.gov | match |
| SGT1 (G100001054395) | Location accuracy | exact | (blank) | (none) | ? |
| SGT1 (G100001054395) | Owner(s) | NRG Chalk Point CT LLC | NRG Chalk Point CT [100%] | eia.gov | ? |
| SGT1 (G100001054395) | Operator(s) | (blank) | NRG Chalk Point CT | eia.gov | ? |
| SGT1 (G100001054395) | Latitude | 38.5444000 | 38.5444 | eia.gov | match |
| SGT1 (G100001054395) | Longitude | -76.6861000 | -76.6861 | eia.gov | match |

## Perryman power station (L100000401827)

| Unit | Field | GEM value | Research value | Source that resolved it | Verdict |
|---|---|---|---|---|---|
| GT1 (G100000414212) | Status | operating | operating | eia.gov | match |
| GT1 (G100000414212) | Capacity (MW) | 53.1 | 53.1 | eia.gov | match |
| GT1 (G100000414212) | Fuel | fossil liquids: fuel oil | fossil liquids: fuel oil | eia.gov | match |
| GT1 (G100000414212) | Turbine/Engine Technology | gas turbine | gas turbine | eia.gov | match |
| GT1 (G100000414212) | Equipment Manufacturer/Model | (blank) | Siemens | industrialinfo.com | ? |
| GT1 (G100000414212) | Number Of Engines | (blank) | 1 | eia.gov | ? |
| GT1 (G100000414212) | Capacity Per Engine | (blank) | 53.1 | eia.gov | ? |
| GT1 (G100000414212) | Start year | 1972 | 1972 | eia.gov | match |
| GT1 (G100000414212) | CHP | no | no | eia.gov | match |
| GT1 (G100000414212) | Location accuracy | exact | (blank) | (none) | ? |
| GT1 (G100000414212) | Owner(s) | Constellation Power Source Generation LLC [100%] | Constellation Power Source Generation, LLC [100%] | eia.gov | match |
| GT1 (G100000414212) | Operator(s) | (blank) | Constellation Power Source Generation, LLC | eia.gov | ? |
| GT1 (G100000414212) | Latitude | 39.4428360 | 39.442836 | eia.gov | match |
| GT1 (G100000414212) | Longitude | -76.2217610 | -76.22176 | eia.gov | match |
| GT1 (G100000414212) | Captive industry use | (blank) | no | eia.gov | ? |
| GT1 (G100000414212) | Captive non-industry use | (blank) | no | eia.gov | ? |
| GT3 (G100000414211) | Status | operating | operating | eia.gov | match |
| GT3 (G100000414211) | Capacity (MW) | 53.1 | 53.1 | eia.gov | match |
| GT3 (G100000414211) | Fuel | fossil liquids: fuel oil | fossil liquids: fuel oil | eia.gov | match |
| GT3 (G100000414211) | Turbine/Engine Technology | gas turbine | gas turbine | eia.gov | match |
| GT3 (G100000414211) | Equipment Manufacturer/Model | (blank) | Siemens | industrialinfo.com | ? |
| GT3 (G100000414211) | Number Of Engines | (blank) | 1 | eia.gov | ? |
| GT3 (G100000414211) | Capacity Per Engine | (blank) | 53.1 | eia.gov | ? |
| GT3 (G100000414211) | Start year | 1972 | 1972 | eia.gov | match |
| GT3 (G100000414211) | CHP | no | no | eia.gov | match |
| GT3 (G100000414211) | Location accuracy | exact | (blank) | (none) | ? |
| GT3 (G100000414211) | Owner(s) | Constellation Power Source Generation LLC [100%] | Constellation Power Source Generation, LLC [100%] | eia.gov | match |
| GT3 (G100000414211) | Operator(s) | (blank) | Constellation Power Source Generation, LLC | eia.gov | ? |
| GT3 (G100000414211) | Latitude | 39.4428360 | 39.442836 | eia.gov | match |
| GT3 (G100000414211) | Longitude | -76.2217610 | -76.22176 | eia.gov | match |
| GT3 (G100000414211) | Captive industry use | (blank) | no | eia.gov | ? |
| GT3 (G100000414211) | Captive non-industry use | (blank) | no | eia.gov | ? |
| GT4 (G100000414210) | Status | operating | operating | eia.gov | match |
| GT4 (G100000414210) | Capacity (MW) | 53.1 | 53.1 | eia.gov | match |
| GT4 (G100000414210) | Fuel | fossil liquids: fuel oil | fossil liquids: fuel oil | eia.gov | match |
| GT4 (G100000414210) | Turbine/Engine Technology | gas turbine | gas turbine | eia.gov | match |
| GT4 (G100000414210) | Equipment Manufacturer/Model | (blank) | Siemens | industrialinfo.com | ? |
| GT4 (G100000414210) | Number Of Engines | (blank) | 1 | eia.gov | ? |
| GT4 (G100000414210) | Capacity Per Engine | (blank) | 53.1 | eia.gov | ? |
| GT4 (G100000414210) | Start year | 1972 | 1972 | eia.gov | match |
| GT4 (G100000414210) | CHP | no | no | eia.gov | match |
| GT4 (G100000414210) | Location accuracy | exact | (blank) | (none) | ? |
| GT4 (G100000414210) | Owner(s) | Constellation Power Source Generation LLC [100%] | Constellation Power Source Generation, LLC [100%] | eia.gov | match |
| GT4 (G100000414210) | Operator(s) | (blank) | Constellation Power Source Generation, LLC | eia.gov | ? |
| GT4 (G100000414210) | Latitude | 39.4428360 | 39.442836 | eia.gov | match |
| GT4 (G100000414210) | Longitude | -76.2217610 | -76.22176 | eia.gov | match |
| GT4 (G100000414210) | Captive industry use | (blank) | no | eia.gov | ? |
| GT4 (G100000414210) | Captive non-industry use | (blank) | no | eia.gov | ? |
| GT5 (G100000402639) | Status | operating | operating | eia.gov | match |
| GT5 (G100000402639) | Capacity (MW) | 192.0 | 192.0 | eia.gov | match |
| GT5 (G100000402639) | Turbine/Engine Technology | gas turbine | gas turbine | eia.gov | match |
| GT5 (G100000402639) | Fuel | fossil gas: natural gas, fossil liquids: fuel oil | fossil gas: natural gas | eia.gov | ? |
| GT5 (G100000402639) | Equipment Manufacturer/Model | (blank) | General Electric | industrialinfo.com | ? |
| GT5 (G100000402639) | Number Of Engines | (blank) | 1 | eia.gov | ? |
| GT5 (G100000402639) | Capacity Per Engine | (blank) | 192.0 | eia.gov | ? |
| GT5 (G100000402639) | Start year | 1995 | 1995 | eia.gov | match |
| GT5 (G100000402639) | CHP | no | no | eia.gov | match |
| GT5 (G100000402639) | Location accuracy | exact | (blank) | (none) | ? |
| GT5 (G100000402639) | Owner(s) | Constellation Power Source Generation LLC [100%] | Constellation Power Source Generation, LLC [100%] | eia.gov | match |
| GT5 (G100000402639) | Operator(s) | (blank) | Constellation Power Source Generation, LLC | eia.gov | ? |
| GT5 (G100000402639) | Latitude | 39.4428360 | 39.442836 | eia.gov | match |
| GT5 (G100000402639) | Longitude | -76.2217600 | -76.22176 | eia.gov | match |
| GT5 (G100000402639) | Captive industry use | (blank) | no | eia.gov | ? |
| GT5 (G100000402639) | Captive non-industry use | (blank) | no | eia.gov | ? |
| GT6 (G100000402640) | Status | operating | operating | eia.gov | match |
| GT6 (G100000402640) | Capacity (MW) | 141.0 | 141.0 | eia.gov | match |
| GT6 (G100000402640) | Turbine/Engine Technology | gas turbine | gas turbine | eia.gov | match |
| GT6 (G100000402640) | Fuel | fossil gas: natural gas, fossil liquids: fuel oil | fossil gas: natural gas, fossil liquids: fuel oil | industrialinfo.com | match |
| GT6 (G100000402640) | Equipment Manufacturer/Model | (blank) | Pratt & Whitney FT4000 SWIFTPAC | industrialinfo.com | ? |
| GT6 (G100000402640) | Number Of Engines | (blank) | 1 | eia.gov | ? |
| GT6 (G100000402640) | Capacity Per Engine | (blank) | 141.0 | eia.gov | ? |
| GT6 (G100000402640) | Start year | 2015 | 2015 | eia.gov | match |
| GT6 (G100000402640) | CHP | no | no | eia.gov | match |
| GT6 (G100000402640) | Location accuracy | exact | (blank) | (none) | ? |
| GT6 (G100000402640) | Owner(s) | Constellation Power Source Generation LLC [100%] | Constellation Power Source Generation, LLC [100%] | eia.gov | match |
| GT6 (G100000402640) | Operator(s) | (blank) | Constellation Power Source Generation, LLC | eia.gov | ? |
| GT6 (G100000402640) | Latitude | 39.4428360 | 39.442836 | eia.gov | match |
| GT6 (G100000402640) | Longitude | -76.2217600 | -76.22176 | eia.gov | match |
| GT6 (G100000402640) | Captive industry use | (blank) | no | eia.gov | ? |
| GT6 (G100000402640) | Captive non-industry use | (blank) | no | eia.gov | ? |

## Vienna Operations power station (L100000409301)

| Unit | Field | GEM value | Research value | Source that resolved it | Verdict |
|---|---|---|---|---|---|
| 8 (G100000414447) | Status | operating | operating | eia.gov | match |
| 8 (G100000414447) | Capacity (MW) | 162.0 | 162.0 | eia.gov | match |
| 8 (G100000414447) | Fuel | fossil liquids: fuel oil, fossil liquids: heavy fuel oil | fossil liquids: heavy fuel oil, fossil liquids: fuel oil | eia.gov | match |
| 8 (G100000414447) | Turbine/Engine Technology | steam turbine | steam turbine | eia.gov | match |
| 8 (G100000414447) | Start year | 1972 | 1972 | eia.gov | match |
| 8 (G100000414447) | CHP | no | no | eia.gov | match |
| 8 (G100000414447) | Latest Activity | (blank) | Named in a January 2026 Department of Energy emergency order as an available oil-fired unit | energy.gov | ? |
| 8 (G100000414447) | Owner(s) | Vienna Power LLC [100%] | Vienna Power LLC [100%] | eia.gov | match |
| 8 (G100000414447) | Operator(s) | NRG Vienna Operations | NRG Vienna Operations Inc | eia.gov | ? |
| 8 (G100000414447) | Latitude | 38.4878000 | 38.4878 | eia.gov | match |
| 8 (G100000414447) | Longitude | -75.8208000 | -75.8208 | eia.gov | match |
| 8 (G100000414447) | Location accuracy | exact | approximate | eia.gov | ? |
| 8 (G100000414447) | Captive industry use | (blank) | no | eia.gov | ? |

## Wildcat Point generation facility (L100000402170)

| Unit | Field | GEM value | Research value | Source that resolved it | Verdict |
|---|---|---|---|---|---|
| CC1 (G100000402074) | Status | operating | operating | eia.gov | match |
| CC1 (G100000402074) | Capacity (MW) | 1114.0 | 1113.6 | eia.gov | match |
| CC1 (G100000402074) | Fuel | fossil gas: natural gas | fossil gas: natural gas | eia.gov | match |
| CC1 (G100000402074) | Turbine/Engine Technology | combined cycle | combined cycle | eia.gov | match |
| CC1 (G100000402074) | Equipment Manufacturer/Model | (blank) | Mitsubishi M501GAC | mde.maryland.gov | ? |
| CC1 (G100000402074) | Number Of Engines | (blank) | 2 | mde.maryland.gov | ? |
| CC1 (G100000402074) | Capacity Per Engine | (blank) | 310.3 | eia.gov | ? |
| CC1 (G100000402074) | Start year | 2018 | 2018 | eia.gov | match |
| CC1 (G100000402074) | CHP | no | no | eia.gov | match |
| CC1 (G100000402074) | Owner(s) | Old Dominion Electric Cooperative [100%] | Old Dominion Electric Cooperative [100%] | eia.gov | match |
| CC1 (G100000402074) | Operator(s) | (blank) | Old Dominion Electric Cooperative | mde.maryland.gov | ? |
| CC1 (G100000402074) | Latitude | 39.7193640 | 39.719364 | eia.gov | match |
| CC1 (G100000402074) | Longitude | -76.1616300 | -76.16163 | eia.gov | match |
| CC1 (G100000402074) | Location accuracy | exact | approximate | eia.gov | ? |
| CC1 (G100000402074) | Captive industry use | (blank) | no | eia.gov | ? |

## Mattawoman energy center (L100000402417)

| Unit | Field | GEM value | Research value | Source that resolved it | Verdict |
|---|---|---|---|---|---|
| CGT11 (G100000403822) | Status | cancelled | cancelled | dnr.maryland.gov | match |
| CGT11 (G100000403822) | Capacity (MW) | 1008.0 | 1008.0 | eia.gov | match |
| CGT11 (G100000403822) | Fuel | fossil gas: natural gas | fossil gas: natural gas | eia.gov | match |
| CGT11 (G100000403822) | Turbine/Engine Technology | combined cycle | combined cycle | eia.gov | match |
| CGT11 (G100000403822) | Cancellation year | (blank) | 2021 | dnr.maryland.gov | ? |
| CGT11 (G100000403822) | Status Detail | cancelled in 2021 | Developer told the Maryland Public Service Commission in January 2021 that it would not proceed | dnr.maryland.gov | ? |
| CGT11 (G100000403822) | Latest Activity | (blank) | January 2021: developer notified the Maryland Public Service Commission it would not proceed | dnr.maryland.gov | ? |
| CGT11 (G100000403822) | CHP | no | no | eia.gov | match |
| CGT11 (G100000403822) | Owner(s) | Mattawoman Energy LLC [100%] | Mattawoman Energy, LLC [100%] | eia.gov | match |
| CGT11 (G100000403822) | Latitude | 38.6924970 | 38.692497 | eia.gov | match |
| CGT11 (G100000403822) | Longitude | -76.8421500 | -76.84215 | eia.gov | match |
| CGT11 (G100000403822) | Location accuracy | exact | approximate | eia.gov | ? |

## Westport power station (L100000401828)

| Unit | Field | GEM value | Research value | Source that resolved it | Verdict |
|---|---|---|---|---|---|
| GT5 (G100000402641) | Status | retired | retired | eia.gov | match |
| GT5 (G100000402641) | Capacity (MW) | 122.0 | 121.5 | eia.gov | match |
| GT5 (G100000402641) | Fuel | fossil gas: natural gas | fossil gas: natural gas | eia.gov | match |
| GT5 (G100000402641) | Turbine/Engine Technology | gas turbine | gas turbine | eia.gov | match |
| GT5 (G100000402641) | Start year | 1969 | 1969 | eia.gov | match |
| GT5 (G100000402641) | Retired year | 2020 | 2020 | eia.gov | match |
| GT5 (G100000402641) | CHP | no | no | eia.gov | match |
| GT5 (G100000402641) | Latest Activity | (blank) | retired June 2020 | eia.gov | ? |
| GT5 (G100000402641) | Owner(s) | Constellation Power Source Generation LLC [100%] | Constellation Power Source Generation, LLC [100%] | eia.gov | match |
| GT5 (G100000402641) | Operator(s) | (blank) | Constellation Power Source Generation, LLC | eia.gov | ? |
| GT5 (G100000402641) | Latitude | 39.2660400 | 39.26604 | eia.gov | match |
| GT5 (G100000402641) | Longitude | -76.6295400 | -76.62954 | eia.gov | match |
| GT5 (G100000402641) | Location accuracy | exact | exact | eia.gov | match |
| GT5 (G100000402641) | Captive industry use | (blank) | no | eia.gov | ? |
| GT5 (G100000402641) | Captive non-industry use | (blank) | no | eia.gov | ? |

## What resolved what

How many unit fields each website settled, by field. A plant-wide finding counts once for each unit.

| Field | Website | Unit fields |
|---|---|---|
| CHP | eia.gov | 33 |
| Cancellation year | dnr.maryland.gov | 1 |
| Capacity (MW) | eia.gov | 33 |
| Capacity (MW) | marylandmatters.org | 2 |
| Capacity (MW) | psc.maryland.gov | 2 |
| Capacity Per Engine | eia.gov | 22 |
| Capacity Per Engine | mde.maryland.gov | 4 |
| Captive industry use | eia.gov | 26 |
| Captive industry use | psc.maryland.gov | 2 |
| Captive non-industry use | eia.gov | 23 |
| Conversion/replacement? | powermag.com | 1 |
| Equipment Manufacturer/Model | mde.maryland.gov | 7 |
| Equipment Manufacturer/Model | industrialinfo.com | 5 |
| Equipment Manufacturer/Model | stg-mde.maryland.gov | 4 |
| Equipment Manufacturer/Model | psc.maryland.gov | 2 |
| Equipment Manufacturer/Model | powermag.com | 1 |
| Equipment Manufacturer/Model | power-technology.com | 1 |
| Fuel | eia.gov | 32 |
| Fuel | marylandmatters.org | 2 |
| Fuel | psc.maryland.gov | 2 |
| Fuel | industrialinfo.com | 1 |
| Latest Activity | psc.maryland.gov | 2 |
| Latest Activity | mde.maryland.gov | 2 |
| Latest Activity | powermag.com | 2 |
| Latest Activity | lw.com | 1 |
| Latest Activity | gridinfo.com | 1 |
| Latest Activity | energy.gov | 1 |
| Latest Activity | dnr.maryland.gov | 1 |
| Latest Activity | eia.gov | 1 |
| Latitude | eia.gov | 32 |
| Location accuracy | eia.gov | 27 |
| Longitude | eia.gov | 32 |
| Number Of Engines | eia.gov | 13 |
| Number Of Engines | mde.maryland.gov | 7 |
| Number Of Engines | stg-mde.maryland.gov | 4 |
| Number Of Engines | powermag.com | 1 |
| Operator(s) | eia.gov | 24 |
| Operator(s) | mde.maryland.gov | 3 |
| Operator(s) | marylandmatters.org | 2 |
| Operator(s) | ogj.com | 2 |
| Operator(s) | lw.com | 1 |
| Operator(s) | powermag.com | 1 |
| Owner(s) | eia.gov | 27 |
| Owner(s) | cogentrix.com | 4 |
| Owner(s) | marylandmatters.org | 2 |
| Owner(s) | ogj.com | 2 |
| Owner(s) | lw.com | 1 |
| Owner(s) | energymonitor.ai | 1 |
| Planned retire | eia.gov | 2 |
| Retired year | eia.gov | 2 |
| Start year | eia.gov | 32 |
| Start year | marylandmatters.org | 2 |
| Start year | lngindustry.com | 2 |
| Status | eia.gov | 32 |
| Status | marylandmatters.org | 2 |
| Status | lngindustry.com | 2 |
| Status | dnr.maryland.gov | 1 |
| Status Detail | psc.maryland.gov | 2 |
| Status Detail | dnr.maryland.gov | 1 |
| Turbine/Engine Technology | eia.gov | 25 |
| Turbine/Engine Technology | stg-mde.maryland.gov | 4 |
| Turbine/Engine Technology | mde.maryland.gov | 4 |
| Turbine/Engine Technology | marylandmatters.org | 2 |
| Turbine/Engine Technology | psc.maryland.gov | 2 |

## Run facts per plant

The plant reports record only when they finished, not when they started, so time per plant is not shown.

| Plant | Model | Finished | Links tried | Links that checked out |
|---|---|---|---|---|
| Constellation (Project 1) power station | sonnet | 2026-10-02T15:40:00-04:00 | 2 | 2 |
| Constellation (Project 2) power station | sonnet | 2026-10-02T15:40:00-04:00 | 2 | 2 |
| Brandywine power facility | sonnet | 2026-10-02T15:40:00-04:00 | 10 | 3 |
| Chalk Point Generating Station | sonnet | 2026-10-02T15:28:28-04:00 | 4 | 3 |
| Cove Point LNG Terminal power station | sonnet | 2026-10-02T15:28:18-04:00 | 8 | 5 |
| CPV St. Charles energy center | sonnet | 2026-10-02T15:28:18-04:00 | 7 | 4 |
| Dickerson Generating Station | sonnet | 2026-10-02T15:29:58-04:00 | 9 | 4 |
| Essential Power Rock Springs station | sonnet | 2026-10-02T15:27:42-04:00 | 7 | 5 |
| Herbert Wagner Generating Station | sonnet | 2026-10-02T15:27:59-04:00 | 4 | 4 |
| Keys energy center | sonnet | 2026-10-02T15:25:41-04:00 | 5 | 4 |
| Morgantown Generating Station | sonnet | 2026-10-02T15:33:00-04:00 | 6 | 6 |
| NRG Chalk Point CT power station | sonnet | 2026-10-02T15:30:25-04:00 | 2 | 2 |
| Perryman power station | sonnet | 2026-10-02T12:32:52-07:00 | 6 | 3 |
| Vienna Operations power station | sonnet | 2026-10-02T12:35:09-07:00 | 4 | 4 |
| Wildcat Point generation facility | sonnet | 2026-10-02T12:35:09-07:00 | 11 | 9 |
| Mattawoman energy center | sonnet | 2026-10-02T12:35:09-07:00 | 7 | 4 |
| Westport power station | sonnet | 2026-10-02T12:35:00-04:00 | 1 | 1 |

## Not found

- **Constellation (Project 1) power station, unit 1 (G100001090726)**: Equipment Manufacturer/Model, Number Of Engines, Capacity Per Engine, Retired year, Planned retire, Cancellation year, CHP, Captive industry use, Captive industry type, Captive non-industry use, Conversion/replacement?.
  Everything comes from the Maryland Public Service Commission orders on the Next Generation Energy Act. The orders give no turbine make, model or count, and no coordinates were reported. The turbines are already owned by Constellation and would be moved from other Constellation property. Project 1 is the 150 MW option.
- **Constellation (Project 2) power station, unit 1 (G100001090730)**: Equipment Manufacturer/Model, Number Of Engines, Capacity Per Engine, Retired year, Planned retire, Cancellation year, CHP, Captive industry use, Captive industry type, Captive non-industry use, Conversion/replacement?.
  Everything comes from the Maryland Public Service Commission orders on the Next Generation Energy Act. The orders give no turbine make, model or count, and no coordinates were reported. The turbines are already owned by Constellation and would be moved from other Constellation property. Project 2 is the 564 MW option.
- **Brandywine power facility, unit F701 (G100000401771)**: Equipment Manufacturer/Model, Number Of Engines, Retired year, Planned retire, Cancellation year, Status Detail, Captive industry use, Captive industry type, Captive non-industry use, Conversion/replacement?.
  Status, capacity, fuel, technology, start year and CHP come from the EIA tables. A trade magazine profile says the plant has two GE Frame 7EA gas turbines and one GE steam turbine, but the verifier could not open that page, so the model is raised as a question. No retirement or cancellation was found. The plant sells power to the grid and is not captive.
- **Chalk Point Generating Station, unit 3 (G100000402920)**: Equipment Manufacturer/Model, Retired year, Planned retire, Cancellation year, Latest Activity, Status Detail, Captive industry type, Conversion/replacement?.
  EIA tables give status, capacity, start year, fuel and technology. I did not find the turbine maker or model, because the sources I could open do not state it. No retirement is planned in the EIA tables.
- **Chalk Point Generating Station, unit 4 (G100000402921)**: Equipment Manufacturer/Model, Retired year, Planned retire, Cancellation year, Latest Activity, Status Detail, Captive industry type, Conversion/replacement?.
  EIA tables give status, capacity, start year, fuel and technology. I did not find the turbine maker or model, because the sources I could open do not state it. No retirement is planned in the EIA tables.
- **Chalk Point Generating Station, unit GT3 (G100000402922)**: Equipment Manufacturer/Model, Retired year, Planned retire, Cancellation year, Latest Activity, Status Detail, Captive industry type, Conversion/replacement?.
  EIA tables give status, capacity, start year, fuel and technology. I did not find the turbine maker or model, because the sources I could open do not state it. No retirement is planned in the EIA tables.
- **Chalk Point Generating Station, unit GT4 (G100000402923)**: Equipment Manufacturer/Model, Retired year, Planned retire, Cancellation year, Latest Activity, Status Detail, Captive industry type, Conversion/replacement?.
  EIA tables give status, capacity, start year, fuel and technology. I did not find the turbine maker or model, because the sources I could open do not state it. No retirement is planned in the EIA tables.
- **Chalk Point Generating Station, unit GT5 (G100000402924)**: Equipment Manufacturer/Model, Retired year, Planned retire, Cancellation year, Latest Activity, Status Detail, Captive industry type, Conversion/replacement?.
  EIA tables give status, capacity, start year, fuel and technology. I did not find the turbine maker or model, because the sources I could open do not state it. No retirement is planned in the EIA tables.
- **Chalk Point Generating Station, unit GT6 (G100000402925)**: Equipment Manufacturer/Model, Retired year, Planned retire, Cancellation year, Latest Activity, Status Detail, Captive industry type, Conversion/replacement?.
  EIA tables give status, capacity, start year, fuel and technology. I did not find the turbine maker or model, because the sources I could open do not state it. No retirement is planned in the EIA tables.
- **Chalk Point Generating Station, unit SGT1 (G100000409452)**: Equipment Manufacturer/Model, Retired year, Planned retire, Cancellation year, Latest Activity, Status Detail, Captive industry type, Conversion/replacement?.
  EIA tables give status, capacity, start year, fuel and technology. I did not find the turbine maker or model, because the sources I could open do not state it. No retirement is planned in the EIA tables.
- **Cove Point LNG Terminal power station, unit CC1-5STA (G100000409442)**: Number Of Engines, Capacity Per Engine, Retired year, Planned retire, Cancellation year, Latest Activity, Status Detail, CHP, Conversion/replacement?, Captive industry type, Captive non-industry use, Latitude, Longitude, Location accuracy.
  EIA does not list this plant in its August 2026 monthly table, because it is a captive plant. So several fields could not be sourced. Each unit is one of two 65 MW steam turbine generators.
- **Cove Point LNG Terminal power station, unit CC1-5STB (G100000409441)**: Number Of Engines, Capacity Per Engine, Retired year, Planned retire, Cancellation year, Latest Activity, Status Detail, CHP, Conversion/replacement?, Captive industry type, Captive non-industry use, Latitude, Longitude, Location accuracy.
  EIA does not list this plant in its August 2026 monthly table, because it is a captive plant. So several fields could not be sourced. Each unit is one of two 65 MW steam turbine generators.
- **CPV St. Charles energy center, unit G601 (G100000402033)**: Retired year, Planned retire, Cancellation year, Latest Activity, Status Detail, Conversion/replacement?, Captive industry type, Captive non-industry use.
  Retirement, cancellation and conversion fields do not apply or were not found: the EIA table shows no planned retirement, and nothing suggests this was a conversion. I did not find a dated recent news item for latest activity or status detail.
- **Dickerson Generating Station, unit GT2 (G100000402929)**: Retired year, Planned retire, Cancellation year, Status Detail, Conversion/replacement?, Captive industry type.
  EIA calls this unit GT2 and the state air permit calls it HCT-1. Not found: no retirement, planned retirement or cancellation exists in the sources, and no source speaks to status detail or to a conversion or replacement. Captive industry type does not apply.
- **Dickerson Generating Station, unit GT3 (G100000402930)**: Retired year, Planned retire, Cancellation year, Status Detail, Conversion/replacement?, Captive industry type.
  EIA calls this unit GT3 and the state air permit calls it HCT-2. Not found: no retirement, planned retirement or cancellation exists in the sources, and no source speaks to status detail or to a conversion or replacement. Captive industry type does not apply.
- **Essential Power Rock Springs station, unit 1 (G100000402859)**: Retired year, Planned retire, Cancellation year, Latest Activity, Status Detail, Conversion/replacement?, Captive industry type.
  Status, capacity, technology and start year come from the EIA-860M table for August 2026. There is no planned retirement in that table. I found no recent news on this unit beyond the plant-level items.
- **Essential Power Rock Springs station, unit 2 (G100000402860)**: Retired year, Planned retire, Cancellation year, Latest Activity, Status Detail, Conversion/replacement?, Captive industry type.
  Status, capacity, technology and start year come from the EIA-860M table for August 2026. There is no planned retirement in that table. I found no recent news on this unit beyond the plant-level items.
- **Essential Power Rock Springs station, unit 3 (G100000402861)**: Retired year, Planned retire, Cancellation year, Latest Activity, Status Detail, Conversion/replacement?, Captive industry type.
  Status, capacity, technology and start year come from the EIA-860M table for August 2026. There is no planned retirement in that table. I found no recent news on this unit beyond the plant-level items.
- **Essential Power Rock Springs station, unit 4 (G100000402862)**: Retired year, Planned retire, Cancellation year, Latest Activity, Status Detail, Conversion/replacement?, Captive industry type.
  Status, capacity, technology and start year come from the EIA-860M table for August 2026. There is no planned retirement in that table. I found no recent news on this unit beyond the plant-level items.
- **Herbert Wagner Generating Station, unit 1 (G100000402976)**: Equipment Manufacturer/Model, Number Of Engines, Capacity Per Engine, Cancellation year, Status Detail, Planned retire, Latest Activity, Conversion/replacement?, Operator(s), Captive industry use, Captive industry type, Captive non-industry use.
  Unit 1 retired in June 2025 according to EIA. A Power magazine article calls it a natural gas unit, but EIA lists distillate oil with gas for startup, so I used the EIA fuel.
- **Herbert Wagner Generating Station, unit 4 (G100000414261)**: Equipment Manufacturer/Model, Number Of Engines, Capacity Per Engine, Cancellation year, Status Detail, Retired year, Conversion/replacement?, Operator(s), Captive industry use, Captive industry type, Captive non-industry use.
  Unit 4 is a 414.7 MW oil-fired steam unit from 1972 with planned retirement in June 2029. I found no turbine manufacturer, operator or conversion information.
- **Herbert Wagner Generating Station, unit Unit 3, timepoint 2 (G100001028230)**: Equipment Manufacturer/Model, Number Of Engines, Capacity Per Engine, Cancellation year, Status Detail, Retired year, Operator(s), Captive industry use, Captive industry type, Captive non-industry use.
  Unit 3 is a 359 MW steam unit from 1966, converted from coal to oil at the end of 2023. I could not tell what the timepoint 2 label means, so I treated it as the same Unit 3 that EIA lists as generator 3.
- **Keys energy center, unit CC1 (G100000402089)**: Number Of Engines, Capacity Per Engine, Retired year, Planned retire, Cancellation year, Status Detail, Captive industry use, Captive industry type, Captive non-industry use, Conversion/replacement?.
  One combined cycle block of three generators, running since July 2018. I found no retirement, cancellation or conversion information, and no source for engine counts or captive use.
- **Morgantown Generating Station, unit 3 (G100000414155)**: Retired year, Planned retire, Cancellation year, Latest Activity, Status Detail, Captive industry type, Conversion/replacement?.
  I could not find a planned retirement for this unit. The EIA table leaves the planned retirement blank. I found no news on activity at the plant, so latest activity and status detail are not sourced. No retired year applies because the unit is operating.
- **Morgantown Generating Station, unit 4 (G100000414154)**: Retired year, Planned retire, Cancellation year, Latest Activity, Status Detail, Captive industry type, Conversion/replacement?.
  I could not find a planned retirement for this unit. The EIA table leaves the planned retirement blank. I found no news on activity at the plant, so latest activity and status detail are not sourced. No retired year applies because the unit is operating.
- **Morgantown Generating Station, unit 5 (G100000414153)**: Planned retire, Cancellation year, Latest Activity, Status Detail, Captive industry type, Conversion/replacement?, Retired year.
  I could not find a planned retirement for this unit. The EIA table leaves the planned retirement blank. I found no news on activity at the plant, so latest activity and status detail are not sourced. The retired year is not reported because EIA currently shows the unit as operating again after a June 2024 retirement.
- **Morgantown Generating Station, unit 6 (G100000414152)**: Planned retire, Cancellation year, Latest Activity, Status Detail, Captive industry type, Conversion/replacement?, Retired year.
  I could not find a planned retirement for this unit. The EIA table leaves the planned retirement blank. I found no news on activity at the plant, so latest activity and status detail are not sourced. The retired year is not reported because EIA currently shows the unit as operating again after a June 2024 retirement.
- **NRG Chalk Point CT power station, unit SGT1 (G100001054395)**: Equipment Manufacturer/Model, Retired year, Planned retire, Cancellation year, Latest Activity, Status Detail, Conversion/replacement?, Location accuracy, Captive industry use, Captive industry type, Captive non-industry use.
  The EIA tables confirm one operating 94 MW oil and gas turbine that started in 1990. I could not find the turbine maker, because the EIA files do not give it and two web searches turned up no air permit for this unit.
- **Perryman power station, unit GT1 (G100000414212)**: Retired year, Planned retire, Cancellation year, Latest Activity, Status Detail, Conversion/replacement?, Location accuracy, Captive industry type.
  EIA data covers status, size, fuel, start year and location. I found no retirement, cancellation or conversion information for this unit, and no turbine model details beyond the manufacturer.
- **Perryman power station, unit GT3 (G100000414211)**: Retired year, Planned retire, Cancellation year, Latest Activity, Status Detail, Conversion/replacement?, Location accuracy, Captive industry type.
  EIA data covers status, size, fuel, start year and location. I found no retirement, cancellation or conversion information for this unit, and no turbine model details beyond the manufacturer.
- **Perryman power station, unit GT4 (G100000414210)**: Retired year, Planned retire, Cancellation year, Latest Activity, Status Detail, Conversion/replacement?, Location accuracy, Captive industry type.
  EIA data covers status, size, fuel, start year and location. I found no retirement, cancellation or conversion information for this unit, and no turbine model details beyond the manufacturer.
- **Perryman power station, unit GT5 (G100000402639)**: Retired year, Planned retire, Cancellation year, Latest Activity, Status Detail, Conversion/replacement?, Location accuracy, Captive industry type.
  EIA data covers status, size, fuel, start year and location. I found no retirement, cancellation or conversion information for this unit, and no turbine model details beyond the manufacturer. The GE match is uncertain.
- **Perryman power station, unit GT6 (G100000402640)**: Retired year, Planned retire, Cancellation year, Latest Activity, Status Detail, Conversion/replacement?, Location accuracy, Captive industry type.
  EIA data covers status, size, fuel, start year and location. I found no retirement, cancellation or conversion information for this unit, and no turbine model details beyond the manufacturer. The 2015 article says 120 MW, but EIA says 141 MW. I used the EIA figure.
- **Vienna Operations power station, unit 8 (G100000414447)**: Equipment Manufacturer/Model, Number Of Engines, Capacity Per Engine, Retired year, Planned retire, Cancellation year, Status Detail, Conversion/replacement?, Captive industry type, Captive non-industry use.
  I could not find a turbine maker or model, an engine count, or a conversion history for unit 8. No retirement date is on file in the EIA tables. Unit 8 burns oil and is operating.
- **Wildcat Point generation facility, unit CC1 (G100000402074)**: Retired year, Planned retire, Cancellation year, Latest Activity, Status Detail, Conversion/replacement?, Captive industry type, Captive non-industry use.
  The unit is one combined cycle block of two combustion turbines and one steam turbine. I found no planned retirement and no conversion history. The steam turbine maker was not found.
- **Mattawoman energy center, unit CGT11 (G100000403822)**: Equipment Manufacturer/Model, Number Of Engines, Capacity Per Engine, Start year, Retired year, Planned retire, Conversion/replacement?, Operator(s), Captive industry use, Captive industry type, Captive non-industry use.
  The project was never built. I did not find a turbine maker, an operator, or an engine count. No start year applies to a cancelled unit.
- **Westport power station, unit GT5 (G100000402641)**: Equipment Manufacturer/Model, Number Of Engines, Capacity Per Engine, Planned retire, Cancellation year, Status Detail, Captive industry type, Conversion/replacement?.
  All main values come from one EIA table. I did not find the turbine maker, any engine counts, or any note on why the unit retired, because the table does not carry them and I did not search further.

## GEM errors to carry into the update deliverable

Fill this in after scoring. List each row scored GEM wrong, with the unit ID, the field and the source.

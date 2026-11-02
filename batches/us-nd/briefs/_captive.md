## Captive power at LNG terminals in North Dakota (checklist rows 6 and 44)

The LNG team keeps a sheet of LNG terminals whose on-site gas-fired generation reaches the GOGPT threshold (50 MW here). Read on 2026-10-23: https://docs.google.com/spreadsheets/d/19YvVT918PYHq_DkdvKWtoXYJ2Xl7l7R3. The rows below are the ones in North Dakota, joined to the LNG tracker by Terminal ID. The sheet is a lead list, not the whole answer. Check its Qualifying rows first, but any captive LNG plant you verify at the threshold is an add, whether or not the sheet lists it (Baird, October 2026).

Rules:

1. Capacity is generating capacity only. Gas turbines that drive the refrigerant compressors (mechanical drive, shaft MW) are not power plant capacity. A row the sheet qualifies on mechanical drive alone needs its own generator sets found before anything is added; if there are none at the threshold, write a watch item saying so (drive_or_storage).
2. Captive fields: captive industry use power (or both when heat is also supplied), captive industry type LNG liquefaction. Unit naming follows GEM's existing LNG plants ("<Terminal name> power station"), one unit per generator set or per combined-cycle block.
3. Never cite gem.wiki; the sheet's own gem.wiki references are listed as not citable. Every other link must pass the verifier and state the value.
4. Terminals under "GEM lacks" are new plant candidates: research them and write a full new-plant record (shards/_state.json, newplants) with "captive_lng": true and "checks": [6, 44] as soon as one verified source names generator sets at the threshold at the terminal (the manual's ladder sets the status; a missing start year or turbine model never holds the add back). A watch item (monitor) with the same two keys, new to the tracker, with the reason, a recheck date and a watch_case, only when the generation is unnamed, under the threshold, or mechanical drive is unresolved.
5. Terminals under "Excluded" stay out unless you verify generator sets at the threshold; then it is an add like any other.
6. Captive fields are filled for every captive plant, including one that also sends power or heat out. Captive non-industry use records what is exported: power, heat, both or none.

The sheet has no row for North Dakota. Nothing to add from it; if an LNG terminal in North Dakota has on-site generation at the threshold, add it; a lead without a verified source is a watch item.

## Data center power, gas or diesel, routine or backup, in North Dakota (checklist row 39)

Search for generation built or planned to serve data centers: backup engine fleets (diesel or gas engines listed in an air permit), on-site turbines or engines that supply routine power, and utility plants announced for a campus. Look in the air permit register and the sources in the state note, EIA-860M planned generators whose owner is a data center developer, the grid operator queue, utility filings and press. When a data center permit harvest file exists, briefs/_data_centers.md lists its sites by name; those are tasks too.

Rules (Baird 2026-10-27, from the September 2026 manual):

1. A backup engine fleet is a plant. Add it when the summed electrical nameplate of its generators reaches 50 MW, with one verified source such as the air permit. A routine-power gas or diesel plant at a data center is an add under the same rule. Capacity unknown means add with the capacity cell blank and say so in the notes. Never write a watch item because a fleet is backup power.
2. Name the plant "<Operator> <Place> Data Center power station" and name the data center in Project Links. Use one unit row per permit phase or building group, or one unit when the permit does not split the fleet.
3. Captive fields at unit level: Captive industry use power, Captive industry type data center, Captive non-industry use none (or what is exported). Backup Power is yes only for a unit that is a backup engine set; a unit that supplies routine power does not get it. Internal combustion sets carry Number Of Engines and Capacity Per Engine from the permit.
4. Capacity is generator electrical MW added up across the fleet, never engine horsepower or mechanical kilowatts. Status comes from the manual's ladder: operating when the buildings run, construction when the site is being built, pre-construction on an issued permit alone, announced on an application or notice.
5. Each new plant or unit goes in shards/_state.json under newplants or newunits with "checks": [39]. A watch item is only for the named watch cases, such as no generation named yet.

GEM plants in North Dakota already marked as data-center captive. Check each one's fleet size, phases, Backup Power box and engine counts against the newest permit:

- Applied Digital ELN Generation Plant (L100001089074): pre-construction, 779.5 MW, owners Applied Digital Corp [100%].
- Applied Digital FAR Generation Plant (L100001089073): pre-construction, 576.0 MW, owners Applied Digital Corp [100%].
- Base Electron power station (L100001089055): pre-construction, 1200.0 MW, owners Base Electron Corp [100%].
- Nakota Data Center Campus Power Plant (L100001084854): announced, pre-construction, 1014.0 MW, owners Tachyon9 Corporation [50%]; Nixxy Inc [50%].
- Polaris Forge 1 power station (L100001083334): construction, 400.0 MW, owners Babcock & Wilcox Enterprises Inc [50%]; Minnkota Power Cooperative Inc [50%].
- Polaris Forge 2 power station (L100001083335): construction, 280.0 MW, owners Babcock & Wilcox Enterprises Inc [50%]; Minnkota Power Cooperative Inc [50%].
- River Run Energy Center (L100001080387): pre-construction, 1450.0 MW, owners NextEra Energy Inc [50%]; Basin Electric Cooperative [50%].

Output: findings on tracked plants go in that plant's shard as usual. New plants and watch items from this block go in shards/_state.json under newplants and monitor, each with "captive_lng": true and "checks": [6, 44].

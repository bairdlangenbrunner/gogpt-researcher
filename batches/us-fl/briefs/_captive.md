## Captive power at LNG terminals in Florida (checklist rows 6 and 44)

The LNG team keeps a sheet of LNG terminals whose on-site gas-fired generation reaches the GOGPT threshold (50 MW here). Read on 2026-10-08: https://docs.google.com/spreadsheets/d/19YvVT918PYHq_DkdvKWtoXYJ2Xl7l7R3. The rows below are the ones in Florida, joined to the LNG tracker by Terminal ID. The sheet's Qualifying rows are the only LNG captive plants at the add threshold (Baird, October 2026); any other LNG captive generation you find goes to the watch list.

Rules:

1. Capacity is generating capacity only. Gas turbines that drive the refrigerant compressors (mechanical drive, shaft MW) are not power plant capacity. A row the sheet qualifies on mechanical drive alone needs its own generator sets found before anything is added; if there are none at the threshold, write a watch item saying so.
2. Captive fields: captive industry use power (or both when heat is also supplied), captive industry type LNG liquefaction. Unit naming follows GEM's existing LNG plants ("<Terminal name> power station"), one unit per generator set or per combined-cycle block.
3. Never cite gem.wiki; the sheet's own gem.wiki references are listed as not citable. Every other link must pass the verifier and state the value.
4. Terminals under "GEM lacks" are new plant candidates: research them and write a full new-plant record (shards/_state.json, newplants) with "captive_lng": true and "checks": [6, 44] when the sources support generating capacity at the threshold and a concrete development step; otherwise a watch item (monitor) with the same two keys, new to the tracker, with the reason and a recheck date.
5. Terminals under "Excluded" stay out unless you find new evidence; then a watch item.

The sheet has no row for Florida. Nothing to add from it; if an LNG terminal in Florida has on-site generation you come across, write a watch item.

## Gas-powered data centers in Florida (checklist row 39, US only)

Search for gas-fired generation built or planned to serve data centers in the state: on-site turbines or reciprocating engines behind the meter, utility plants announced for a data center campus, and existing GEM plants gaining a data center as their customer. Look in the state's air permit register and the sources in the state note, EIA-860M planned generators whose owner is a data center developer, the ISO queue, utility filings and press.

Rules (Baird 2026-10-08):

1. Everything from this search goes to the watch list only: shards/_state.json, monitor, never newplants or newunits. A data-center plant is added to the database in a later batch once a reviewer promotes the watch item.
2. Each watch item: monitor_kind new_to_tracker when GEM has no plant (gem_plant_id blank), existing_plant with gem_plant_id when a tracked plant gains a data-center customer or an expansion for one; monitor_reason says what was found and what is still missing to add it (capacity, site, developer, a concrete step); recheck_by within six months; "checks": [39]; the links under refs; capacity_mw when stated.
3. Emergency or backup generator sets at a data center are not captive power plants and are not watch items; only generation that supplies routine power counts.
4. When the plant is later added, GEM's captive fields are captive industry use power and captive industry type data center; say so in the note so the reviewer sees it.

GEM has no plant in Florida marked as data-center captive yet.

Output: findings on tracked plants go in that plant's shard as usual. New plants and watch items from this block go in shards/_state.json under newplants and monitor, each with "captive_lng": true and "checks": [6, 44].

# Data center sites

From the permit harvest for Maryland dated 2026-10-27. The convention (September 2026 manual, Baird 2026-10-27): a data center backup engine fleet is a plant when the summed electrical nameplate of its generators reaches the threshold (50.0 MW). A routine-power gas or diesel plant at a data center is an add too. Capacity unknown means add with the capacity cell blank. Never a watch item for being backup. Name it "<Operator> <Place> Data Center power station", name the data center in Project Links, one unit row per permit phase or building group, fuel diesel or gas as the permit says, technology internal combustion with Number Of Engines and Capacity Per Engine from the permit, Captive industry use power, Captive industry type data center, Backup Power yes at unit level on backup units only, Captive Data Source the permit.

Answer every site below that has a task by writing batches/<tag>/coverage.json under `data_centers`, keyed by the site id: `decision` is add (with the `record_id` of the newplants record), already_in_gem (with `plant_id`), update (with the `record_id` of the updates record, when the permit disagrees with GEM), below_threshold (with `summed_nameplate_mw`, the number you added up), no_generators, not_data_center or nothing_found, plus a plain `note` saying what was read or searched. A site the harvester summed at the threshold is an add unless the note names the GEM plant that already holds the fleet. A site with no usable sum, or no document on record, is an add once you find generators; close it another way only with the number or the search you did.

## Add tasks

No site needs an add.


## Search tasks for sites with no document on record

- Site aligned-adamstown: Aligned Frederick Data Center (operator Aligned). No permit or filing is on record. Search the state air permit portal, the county, the utility's filings and the operator's own announcements for the generator fleet or a routine-power plant. Generators found at the threshold, or found with no usable rating, mean a newplants record and the answer add. Otherwise answer below_threshold with the sum, no_generators, not_data_center or nothing_found, and say in the note what you searched. Coverage answer: `data_centers.aligned-adamstown`. Facts: at Adamstown; no usable nameplate sum; fuel unknown. No permit document is on record for this site yet. Search the state's permit portal, the county and the operator's filings for one before deciding. Lead note: Tenant campus at Quantum Frederick; check the permitted generator fleet.
- Site quantum-loophole-adamstown: Quantum Frederick data center campus (operator Quantum Loophole). No permit or filing is on record. Search the state air permit portal, the county, the utility's filings and the operator's own announcements for the generator fleet or a routine-power plant. Generators found at the threshold, or found with no usable rating, mean a newplants record and the answer add. Otherwise answer below_threshold with the sum, no_generators, not_data_center or nothing_found, and say in the note what you searched. Coverage answer: `data_centers.quantum-loophole-adamstown`. Facts: at Adamstown; no usable nameplate sum; fuel unknown. No permit document is on record for this site yet. Search the state's permit portal, the county and the operator's filings for one before deciding. Lead note: Campus on the former Alcoa Eastalco site; check tenant generator fleets.
- Site rowan-digital-infrastruc-frederick: Rowan Digital Infrastructure Frederick Data Center (operator Rowan Digital Infrastructure). No permit or filing is on record. Search the state air permit portal, the county, the utility's filings and the operator's own announcements for the generator fleet or a routine-power plant. Generators found at the threshold, or found with no usable rating, mean a newplants record and the answer add. Otherwise answer below_threshold with the sum, no_generators, not_data_center or nothing_found, and say in the note what you searched. Coverage answer: `data_centers.rowan-digital-infrastruc-frederick`. Facts: at Frederick; no usable nameplate sum; fuel unknown. No permit document is on record for this site yet. Search the state's permit portal, the county and the operator's filings for one before deciding. Lead note: Check the permitted generator fleet.

## Check tasks for sites GEM already has

None.


## Sites that need no record

None.


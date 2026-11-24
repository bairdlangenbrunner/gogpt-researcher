# Data center sites

From the permit harvest for Germany dated 2026-11-04. The convention (September 2026 manual, Baird 2026-10-27): a data center backup engine fleet is a plant when the summed electrical nameplate of its generators reaches the threshold (20.0 MW). A routine-power gas or diesel plant at a data center is an add too. Capacity unknown means add with the capacity cell blank. Never a watch item for being backup. Name it "<Operator> <Place> Data Center power station", name the data center in Project Links, one unit row per permit phase or building group, fuel diesel or gas as the permit says, technology internal combustion with Number Of Engines and Capacity Per Engine from the permit, Captive industry use power, Captive industry type data center, Backup Power yes at unit level on backup units only, Captive Data Source the permit.

Answer every site below that has a task by writing batches/<tag>/coverage.json under `data_centers`, keyed by the site id: `decision` is add (with the `record_id` of the newplants record), already_in_gem (with `plant_id`), update (with the `record_id` of the updates record, when the permit disagrees with GEM), below_threshold (with `summed_nameplate_mw`, the number you added up), no_generators, not_data_center or nothing_found, plus a plain `note` saying what was read or searched. A site the harvester summed at the threshold is an add unless the note names the GEM plant that already holds the fleet. A site with no usable sum, or no document on record, is an add once you find generators; close it another way only with the number or the search you did.

## Add tasks

No site needs an add.


## Search tasks for sites with no document on record

None.


## Check tasks for sites GEM already has

- Site argaman-group-gmbh-100-birstein: Frank Cube power station is GEM plant Frank Cube power station (L100001062490). Compare the fleet size, the phases, the Backup Power box and the engine counts with the newest permit. If they agree, answer already_in_gem. If not, write an updates record and answer update. Coverage answer: `data_centers.argaman-group-gmbh-100-birstein`. Facts: at Birstein; 135.0 MW summed; fuel natural gas. This is a GEM data center plant in the scope (1 unit rows, 135.0 MW in GEM). No permit in the harvest matched it, so the check against the newest permit is still to do. Backup Power in GEM: no.
- Site e-on-se-100-frankfurt: IQ Energy Center power plant is GEM plant IQ Energy Center power plant (L100001047916). Compare the fleet size, the phases, the Backup Power box and the engine counts with the newest permit. If they agree, answer already_in_gem. If not, write an updates record and answer update. Coverage answer: `data_centers.e-on-se-100-frankfurt`. Facts: at Frankfurt; 61.0 MW summed; fuel natural gas. This is a GEM data center plant in the scope (1 unit rows, 61.0 MW in GEM). No permit in the harvest matched it, so the check against the newest permit is still to do. Backup Power in GEM: no.
- Site kraftwerke-mainz-wiesbad-mainz: KMW Gas Engine Power Plant is GEM plant KMW Gas Engine Power Plant (L100001062418). Compare the fleet size, the phases, the Backup Power box and the engine counts with the newest permit. If they agree, answer already_in_gem. If not, write an updates record and answer update. Coverage answer: `data_centers.kraftwerke-mainz-wiesbad-mainz`. Facts: at Mainz; 12 engines; 54.0 MW summed; fuel natural gas. This is a GEM data center plant in the scope (1 unit rows, 54.0 MW in GEM). No permit in the harvest matched it, so the check against the newest permit is still to do. Backup Power in GEM: no.
- Site kraftwerke-mainz-wiesbad-mainz-2: Mainz power station is GEM plant Mainz power station (L100000101972). Compare the fleet size, the phases, the Backup Power box and the engine counts with the newest permit. If they agree, answer already_in_gem. If not, write an updates record and answer update. Coverage answer: `data_centers.kraftwerke-mainz-wiesbad-mainz-2`. Facts: at Mainz; 250.0 MW summed; fuel natural gas. This is a GEM data center plant in the scope (1 unit rows, 250.0 MW in GEM). No permit in the harvest matched it, so the check against the newest permit is still to do. Backup Power in GEM: no.

## Sites that need no record

None.


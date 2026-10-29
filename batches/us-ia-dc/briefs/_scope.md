# Scope-wide tasks

## When a project GEM lacks is added (Baird 2026-10-23)

Write a new plant record (shards/_state.json, newplants) or a new unit at a tracked plant (newunits) as soon as ONE verified public source names a gas or oil generating project, places it in this scope, and gives a capacity at the threshold (50 MW; engine and aeroderivative sets summed), a unit count with a plant total, or no capacity at all. The manual adds a plant whose capacity cannot be found with the cell blank and removes it later if it proves small. A missing start year, owner, turbine model or exact point never holds an add back: leave the field blank and say in researcher_notes what was not found.

The manual's status ladder decides the status, never the add. A long-range planning document, a grid-operator interconnection queue entry or a press announcement is announced. A permit application, land, financing, a prior-approval docket or a signed interconnection agreement is pre-construction. A project found already cancelled, shelved or retired since 2020 is an add with that status. A queue entry under a shell company's name is still an add at announced, named after the queue entry or its site; the database already holds such plants.

A watch item (monitor, new to the tracker) is only for these cases, and names its case in watch_case: no_generation (a campus, site or program with no generating unit named yet), under_threshold (every unit under the bar and not an engine or aeroderivative set that sums to it), drive_or_storage (generator or mechanical drive, or thermal or storage, unresolved), duplicate_check (it may be a unit GEM already has; prefer a qa question), not_committed (a plan studies it only as an option), other_scope (another state or country; the evidence file lists it as a handoff), unverified (nothing passed the verifier yet). Anything else is an add.

A data center is never a watch case for being a data center or for being backup power. A gas or diesel plant at a data center, routine power or a backup engine fleet, is an add when the summed electrical nameplate of its generators reaches the threshold (50 MW), with the capacity cell blank when no figure can be found. Name it "<Operator> <Place> Data Center power station", name the data center in Project Links, and set Backup Power yes at unit level only on backup engine units (briefs/_data_centers.md lists the sites when a permit harvest exists).

Every new record uses exact export headers in fields and keys refs by Data Source column with a link for every filled field; a grid-operator spreadsheet is cited by the download address with the matching row quoted in researcher_notes.

## EIA plants missing from GEM

The matcher found no EIA plant of 50 MW or more that GEM lacks.

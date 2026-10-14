## Integrated resource plans for Florida (checklist rows 34 and 37)

Utilities in this state file integrated resource plans (IRPs) that name the gas units they intend to build, convert or retire. GEM records a planned unit from a plan's preferred portfolio as a project with the utility as owner, and ticks the unit's IRP box. A draft plan counts (Baird, October 2026).

What to do for each utility below:

1. Open the plan links. Download a PDF with curl and read it with pdftotext. Find the preferred, recommended or base portfolio and its table of additions, conversions, co-firing and retirements, with capacity and year.
2. Compare with the GEM plants listed under the utility, and with the whole state list in the briefs. A unit GEM already has: report only a value the plan changes (status, capacity, start year, planned retirement), with the plan page as the source.
3. A named gas unit the plan commits to that GEM lacks: write a new plant record (or a new unit at an existing plant) with the plan as the source, status announced unless the plan says construction has begun, the high end of any capacity range, and the utility as owner. Set irp true on the record.
4. Capacity the plan commits to without a site: GEM's convention is a placeholder plant named "<utility short name> <plan year> IRP power station <n>" (see the existing names below). Write it as a new plant record with irp true. Capacity the plan only studies as an option, outside the preferred portfolio, goes on the watch list as new to the tracker, with the plan as the source.
5. Say what the plan does not contain. A utility whose plan adds no gas gets one sentence in your summary so the tab's Notes can record it.
6. Never stage the IRP column itself. The irp true flag on a finding tells the build which plants need the box ticked in the web form.

### Florida Public Service Commission (List of Site Plans (2025))

Plan files: https://www.psc.state.fl.us/ten-year-site-plans

GEM has no plant in the state tied to this utility by owner, operator, parent or an IRP placeholder name. Anything the plan commits to is new.

Units with the IRP box ticked that no utility row above matched:

- Duke Energy IRP Power station 1 (L100001064466), unit Unit 1 IRP, announced, owners: Duke Energy Florida LLC [100%]
- Duke Energy IRP Power station 1 (L100001064466), unit Unit 2 IRP, announced, owners: Duke Energy Florida LLC [100%]
- Seminole 2025 IRP power station 1 (L100001064460), unit Unit 1 IRP, announced, owners: Seminole Electric Cooperative Inc [100%]
- Seminole 2025 IRP power station 2 (L100001064461), unit Unit 1 IRP, announced, owners: Seminole Electric Cooperative Inc [100%]
- Seminole 2025 IRP power station 3 (L100001064462), unit Unit 1 IRP, announced, owners: Seminole Electric Cooperative Inc [100%]
- Tampa Electric IRP power station (L100001080280), unit Unit 1 IRP, announced, owners: Tampa Electric Co [100%]

Output: findings on tracked plants go in that plant's shard as usual. New plants, new units and watch items from the plans go in shards/_state.json under newplants, newunits and monitor, each with "irp": true. Then write one plain sentence per utility in meta.irp_summary of _state.json: what the plan adds, what was staged, and the next plan's due date if the plan or the tab gives one.

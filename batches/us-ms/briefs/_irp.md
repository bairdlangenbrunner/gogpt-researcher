## Integrated resource plans for Mississippi (checklist rows 34 and 37)

Utilities in this state file integrated resource plans (IRPs) that name the gas units they intend to build, convert or retire. GEM records a planned unit from a plan's preferred portfolio as a project with the utility as owner, and ticks the unit's IRP box. A draft plan counts (Baird, October 2026).

What to do for each utility below:

1. Open the plan links. Download a PDF with curl and read it with pdftotext. Find the preferred, recommended or base portfolio and its table of additions, conversions, co-firing and retirements, with capacity and year.
2. Compare with the GEM plants listed under the utility, and with the whole state list in the briefs. A unit GEM already has: report only a value the plan changes (status, capacity, start year, planned retirement), with the plan page as the source.
3. A named gas unit the plan commits to that GEM lacks: write a new plant record (or a new unit at an existing plant) with the plan as the source, status announced unless the plan says construction has begun, the high end of any capacity range, and the utility as owner. Set irp true on the record.
4. Capacity the plan commits to without a site: GEM's convention is a placeholder plant named "<utility short name> <plan year> IRP power station <n>" (see the existing names below). Write it as a new plant record with irp true. Capacity the plan only studies as an option, outside the preferred portfolio, goes on the watch list as new to the tracker, with the plan as the source and "watch_case": "not_committed".
5. Say what the plan does not contain. A utility whose plan adds no gas gets one sentence in your summary so the tab's Notes can record it.
6. Never stage the IRP column itself. The irp true flag on a finding tells the build which plants need the box ticked in the web form.

### Mississippi Power Company (2024 IRP)

Plan files: https://www.synapse-energy.com/mississippi-power-company-2024-integrated-resource-plan

Notes already on the tab, newest first:

- In progress.

GEM plants in the state tied to this utility:

- Chevron Oil power station (L100000402094): 1 unit(s), operating; matched by owner; IRP box ticked on 0 of 1 units; no task of its own, compare it here
- Jack Watson Generating Plant (L100000104009): 2 unit(s), operating; matched by owner; IRP box ticked on 0 of 2 units; no task of its own, compare it here
- Ratcliffe power plant (L100000402096): 1 unit(s), operating; matched by owner; IRP box ticked on 0 of 1 units; no task of its own, compare it here
- Victor J Daniel Jr power station (L100000402097): 2 unit(s), operating; matched by owner; IRP box ticked on 0 of 2 units; no task of its own, compare it here

### Entergy Mississippi (2024 IRP)

Plan files: https://www.psc.ms.gov/sites/default/files/2023-07/EML-2024-IRP-Notice-Initial-Public-Workshop.pdf

GEM plants in the state tied to this utility:

- Attala power station (L100000401921): 1 unit(s), operating; matched by owner; IRP box ticked on 0 of 1 units; no task of its own, compare it here
- Baxter Wilson power station (L100000401922): 2 unit(s), retired; matched by owner; IRP box ticked on 0 of 2 units; no task of its own, compare it here
- Choctaw County power station (L100000401923): 1 unit(s), operating; matched by owner; IRP box ticked on 0 of 1 units; no task of its own, compare it here
- Delta Blues Advanced Power Station (L100001025781): 1 unit(s), construction; matched by operator, owner; IRP box ticked on 0 of 1 units; its own brief carries an IRP task
- Gerald Andrus power station (L100000401924): 1 unit(s), operating; matched by owner; IRP box ticked on 0 of 1 units; no task of its own, compare it here
- Hinds energy facility (L100000401925): 1 unit(s), operating; matched by owner; IRP box ticked on 0 of 1 units; no task of its own, compare it here
- Traceview Advanced power station (L100001064651): 1 unit(s), announced; matched by operator, owner; IRP box ticked on 0 of 1 units; its own brief carries an IRP task
- Vicksburg Advanced power station (L100001080981): 1 unit(s), construction; matched by owner; IRP box ticked on 0 of 1 units; its own brief carries an IRP task

### Mississippi PSC (year not given)

Plan files: https://www.mississippipower.com/company/energy-sources.html

Notes already on the tab, newest first:

- IRPs are reviewed by Mississippi PSC

GEM has no plant in the state tied to this utility by owner, operator, parent or an IRP placeholder name. Anything the plan commits to is new.

Output: findings on tracked plants go in that plant's shard as usual. New plants, new units and watch items from the plans go in shards/_state.json under newplants, newunits and monitor, each with "irp": true. Then write one plain sentence per utility in meta.irp_summary of _state.json: what the plan adds, what was staged, and the next plan's due date if the plan or the tab gives one.

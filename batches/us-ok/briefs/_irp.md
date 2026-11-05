## Integrated resource plans for Oklahoma (checklist rows 34 and 37)

Utilities in this state file integrated resource plans (IRPs) that name the gas units they intend to build, convert or retire. GEM records a planned unit from a plan's preferred portfolio as a project with the utility as owner, and ticks the unit's IRP box. A draft plan counts (Baird, October 2026).

What to do for each utility below:

1. Open the plan links. Download a PDF with curl and read it with pdftotext. Find the preferred, recommended or base portfolio and its table of additions, conversions, co-firing and retirements, with capacity and year.
2. Compare with the GEM plants listed under the utility, and with the whole state list in the briefs. A unit GEM already has: report only a value the plan changes (status, capacity, start year, planned retirement), with the plan page as the source. A plant marked below as carrying an IRP task on its own brief gets its questions from that brief: do not write a question about it here. Put what the plan says about it in meta.irp_summary instead.
3. A named gas unit the plan commits to that GEM lacks: write a new plant record (or a new unit at an existing plant) with the plan as the source, status announced unless the plan says construction has begun, the high end of any capacity range, and the utility as owner. Set irp true on the record.
4. Capacity the plan commits to without a site: GEM's convention is a placeholder plant named "<utility short name> <plan year> IRP power station <n>" (see the existing names below). Write it as a new plant record with irp true. Capacity the plan only studies as an option, outside the preferred portfolio, goes on the watch list as new to the tracker, with the plan as the source and "watch_case": "not_committed".
5. Say what the plan does not contain. A utility whose plan adds no gas gets one sentence in your summary so the tab's Notes can record it.
6. Never stage the IRP column itself. The irp true flag on a finding tells the build which plants need the box ticked in the web form.

### OG&E (2024 IRP, 2025 Draft IRP Update, draft)

Plan files: https://www.oge.com/wps/wcm/connect/4a1affa2-a1d9-4ef4-99c0-2a39802daa9f/OGE%2B2025%2BIRP%2BUpdate%2BDRAFT.pdf?CVID=prKiz-k&MOD=AJPERES, https://www.oge.com/documents/d/portal/2025-integrated-resource-plan?_gl=1*1b8xsdi*_ga*MTM0MzIzOTEwMi4xNzcwNjY3NjM1*_ga_HNEDJFDKRD*czE3NzA3MzYwNDUkbzIkZzEkdDE3NzA3MzYwNDYkajU5JGwwJGgw

Notes already on the tab, newest first:

- As a result of 2025 RFP, the projects were selected, including units 13 and 14 at Horseshoepower station https://ogeenergy.gcs-web.com/static-files/c9e24009-45c5-4cd3-9278-e97a6a2abc9c

GEM plants in the state tied to this utility:

- Frontier power station (L100000402493): 1 unit(s), operating; matched by owner; IRP box ticked on 0 of 1 units; no task of its own, compare it here
- Horseshoe Lake power station (L100000402162): 10 unit(s), operating, pre-construction, retired; matched by operator, owner; IRP box ticked on 0 of 10 units; its own brief carries an IRP task
- McClain energy facility (L100000401594): 1 unit(s), operating; matched by owner; IRP box ticked on 0 of 1 units; no task of its own, compare it here
- Muskogee Generating Station (L100000104124): 2 unit(s), operating; matched by owner; IRP box ticked on 0 of 2 units; no task of its own, compare it here
- Mustang (OK) power station (L100000402164): 1 unit(s), operating; matched by owner; IRP box ticked on 0 of 1 units; no task of its own, compare it here
- Redbud power plant (L100000401595): 4 unit(s), operating; matched by owner; IRP box ticked on 0 of 4 units; no task of its own, compare it here
- Seminole (OK) power station (L100000402165): 3 unit(s), operating; matched by owner; IRP box ticked on 0 of 3 units; no task of its own, compare it here
- Tinker Air Force Base power station (L100001063385): 2 unit(s), operating, retired; matched by operator, owner; IRP box ticked on 0 of 2 units; no task of its own, compare it here

Output: findings on tracked plants go in that plant's shard as usual. New plants, new units and watch items from the plans go in shards/_state.json under newplants, newunits and monitor, each with "irp": true. Then write one plain sentence per utility in meta.irp_summary of _state.json: what the plan adds, what was staged, and the next plan's due date if the plan or the tab gives one.

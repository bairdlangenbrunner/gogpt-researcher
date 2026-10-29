## Integrated resource plans for Michigan (checklist rows 34 and 37)

Utilities in this state file integrated resource plans (IRPs) that name the gas units they intend to build, convert or retire. GEM records a planned unit from a plan's preferred portfolio as a project with the utility as owner, and ticks the unit's IRP box. A draft plan counts (Baird, October 2026).

What to do for each utility below:

1. Open the plan links. Download a PDF with curl and read it with pdftotext. Find the preferred, recommended or base portfolio and its table of additions, conversions, co-firing and retirements, with capacity and year.
2. Compare with the GEM plants listed under the utility, and with the whole state list in the briefs. A unit GEM already has: report only a value the plan changes (status, capacity, start year, planned retirement), with the plan page as the source.
3. A named gas unit the plan commits to that GEM lacks: write a new plant record (or a new unit at an existing plant) with the plan as the source, status announced unless the plan says construction has begun, the high end of any capacity range, and the utility as owner. Set irp true on the record.
4. Capacity the plan commits to without a site: GEM's convention is a placeholder plant named "<utility short name> <plan year> IRP power station <n>" (see the existing names below). Write it as a new plant record with irp true. Capacity the plan only studies as an option, outside the preferred portfolio, goes on the watch list as new to the tracker, with the plan as the source and "watch_case": "not_committed".
5. Say what the plan does not contain. A utility whose plan adds no gas gets one sentence in your summary so the tab's Notes can record it.
6. Never stage the IRP column itself. The irp true flag on a finding tells the build which plants need the box ticked in the web form.

### Consumers Energy IRP (Case U-21090)

Plan files: https://mi-psc.my.site.com/sfc/servlet.shepherd/version/download/0688y00000CW7dcAAD

Notes already on the tab, newest first:

- The company said on March 11, 2026 that it plans to file its IRP in June 2026, and that plan includes two new natural gas plants alongside major additions of renewables and storage.

GEM plants in the state tied to this utility:

- Bay County power station (L100001083332): 1 unit(s), pre-construction; matched by owner; IRP box ticked on 1 of 1 units; its own brief carries an IRP task
- Dan E Karn power station (L100000401829): 2 unit(s), operating; matched by owner; IRP box ticked on 0 of 2 units; no task of its own, compare it here
- Genesee County power station (L100001083333): 1 unit(s), pre-construction; matched by owner; IRP box ticked on 1 of 1 units; its own brief carries an IRP task
- Jackson generating station (L100000401830): 1 unit(s), operating; matched by owner; IRP box ticked on 0 of 1 units; no task of its own, compare it here
- Zeeland generating station (L100000401831): 3 unit(s), operating; matched by owner; IRP box ticked on 0 of 3 units; no task of its own, compare it here

### DTE Electric (2022 IRP)

Plan files: https://mi-psc.my.site.com/sfc/servlet.shepherd/version/download/068cs000013UnylAAC

Notes already on the tab, newest first:

- Approved in July 2023 (Case U-21193). DTE updates this plan at least every five years, and we will file the next one by December 2026. In oct 2025, the utility said it will be submitting a competitive bid for its 2026 Integrated Resource Plan, including an all-source request for proposals for a new combined cycle gas plant to replace its retiring Monroe coal power plant. DTE expects generation additions from 2026 to 2032 that include 2.5 GW of batteries (including those at data centers), 8 GW of renewables and 1.5 GW of gas generation. https://www.utilitydive.com/news/dte-data-center-deal-transformational-growth-earnings/804231/ Also planning to add more generation resources to support a new data center.

GEM plants in the state tied to this utility:

- Belle River Power Plant (L100000103973): 5 unit(s), construction, operating; matched by owner; IRP box ticked on 0 of 5 units; its own brief carries an IRP task
- Blue Water energy center (L100000402393): 1 unit(s), operating; matched by owner; IRP box ticked on 0 of 1 units; no task of its own, compare it here
- Dean power station (L100000401855): 4 unit(s), operating; matched by owner; IRP box ticked on 0 of 4 units; no task of its own, compare it here
- Delray power station (L100000401856): 2 unit(s), operating; matched by owner; IRP box ticked on 0 of 2 units; no task of its own, compare it here
- Greenwood (MI) power station (L100000401857): 4 unit(s), operating; matched by owner; IRP box ticked on 0 of 4 units; no task of its own, compare it here
- Milan Township power station (L100001088928): 1 unit(s), pre-construction; matched by owner; IRP box ticked on 0 of 1 units; its own brief carries an IRP task
- Renaissance power plant (L100000401858): 4 unit(s), operating; matched by owner; IRP box ticked on 0 of 4 units; no task of its own, compare it here

Units with the IRP box ticked that no utility row above matched:

- Handy Township power station (L100001082478), unit 1, pre-construction, owners: DTE Energy Co [100%]

Output: findings on tracked plants go in that plant's shard as usual. New plants, new units and watch items from the plans go in shards/_state.json under newplants, newunits and monitor, each with "irp": true. Then write one plain sentence per utility in meta.irp_summary of _state.json: what the plan adds, what was staged, and the next plan's due date if the plan or the tab gives one.

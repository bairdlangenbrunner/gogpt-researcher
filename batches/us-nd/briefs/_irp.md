## Integrated resource plans for North Dakota (checklist rows 34 and 37)

Utilities in this state file integrated resource plans (IRPs) that name the gas units they intend to build, convert or retire. GEM records a planned unit from a plan's preferred portfolio as a project with the utility as owner, and ticks the unit's IRP box. A draft plan counts (Baird, October 2026).

What to do for each utility below:

1. Open the plan links. Download a PDF with curl and read it with pdftotext. Find the preferred, recommended or base portfolio and its table of additions, conversions, co-firing and retirements, with capacity and year.
2. Compare with the GEM plants listed under the utility, and with the whole state list in the briefs. A unit GEM already has: report only a value the plan changes (status, capacity, start year, planned retirement), with the plan page as the source. A plant marked below as carrying an IRP task on its own brief gets its questions from that brief: do not write a question about it here. Put what the plan says about it in meta.irp_summary instead.
3. A named gas unit the plan commits to that GEM lacks: write a new plant record (or a new unit at an existing plant) with the plan as the source, status announced unless the plan says construction has begun, the high end of any capacity range, and the utility as owner. Set irp true on the record.
4. Capacity the plan commits to without a site: GEM's convention is a placeholder plant named "<utility short name> <plan year> IRP power station <n>" (see the existing names below). Write it as a new plant record with irp true. Capacity the plan only studies as an option, outside the preferred portfolio, goes on the watch list as new to the tracker, with the plan as the source and "watch_case": "not_committed".
5. Say what the plan does not contain. A utility whose plan adds no gas gets one sentence in your summary so the tab's Notes can record it.
6. Never stage the IRP column itself. The irp true flag on a finding tells the build which plants need the box ticked in the web form.

### Montana-Dakota Utilities (MDU) (ND 2024 IRP Vol. IV)

Plan files: https://www.montana-dakota.com/wp-content/uploads/PDFs/Rates-Tariffs/2024-ND-IRP-Volume-4-non-print.pdf

Notes already on the tab, newest first:

- ND volumes posted publicly by the utility.

GEM plants in the state tied to this utility:

- Heskett Station (L100000104092): 2 unit(s), operating; matched by owner; IRP box ticked on 0 of 2 units; no task of its own, compare it here

### Otter Tail Power (OTP) (IRP approved by ND PSC (Dec 4, 2024))

Plan files: https://www.otpco.com/about-us/energy-generation/resource-plan/

GEM has no plant in the state tied to this utility by owner, operator, parent or an IRP placeholder name. Anything the plan commits to is new.

### Minnkota Power Cooperative (2022 INTEGRATED RESOURCE PLAN (2022 – 2036))

Plan files: https://www.minnkota.com/minnkota-website/our-power/integrated-resource-plan

GEM plants in the state tied to this utility:

- Minnkota Power Cass power station (L100001089086): 1 unit(s), announced; matched by owner, parent; IRP box ticked on 0 of 1 units; its own brief carries an IRP task
- Polaris Forge 1 power station (L100001083334): 1 unit(s), construction; matched by owner, parent; IRP box ticked on 0 of 1 units; its own brief carries an IRP task
- Polaris Forge 2 power station (L100001083335): 1 unit(s), construction; matched by owner, parent; IRP box ticked on 0 of 1 units; its own brief carries an IRP task

Output: findings on tracked plants go in that plant's shard as usual. New plants, new units and watch items from the plans go in shards/_state.json under newplants, newunits and monitor, each with "irp": true. Then write one plain sentence per utility in meta.irp_summary of _state.json: what the plan adds, what was staged, and the next plan's due date if the plan or the tab gives one.

## Integrated resource plans for Kansas (checklist rows 34 and 37)

Utilities in this state file integrated resource plans (IRPs) that name the gas units they intend to build, convert or retire. GEM records a planned unit from a plan's preferred portfolio as a project with the utility as owner, and ticks the unit's IRP box. A draft plan counts (Baird, October 2026).

What to do for each utility below:

1. Open the plan links. Download a PDF with curl and read it with pdftotext. Find the preferred, recommended or base portfolio and its table of additions, conversions, co-firing and retirements, with capacity and year.
2. Compare with the GEM plants listed under the utility, and with the whole state list in the briefs. A unit GEM already has: report only a value the plan changes (status, capacity, start year, planned retirement), with the plan page as the source.
3. A named gas unit the plan commits to that GEM lacks: write a new plant record (or a new unit at an existing plant) with the plan as the source, status announced unless the plan says construction has begun, the high end of any capacity range, and the utility as owner. Set irp true on the record.
4. Capacity the plan commits to without a site: GEM's convention is a placeholder plant named "<utility short name> <plan year> IRP power station <n>" (see the existing names below). Write it as a new plant record with irp true. Capacity the plan only studies as an option, outside the preferred portfolio, goes on the watch list as new to the tracker, with the plan as the source.
5. Say what the plan does not contain. A utility whose plan adds no gas gets one sentence in your summary so the tab's Notes can record it.
6. Never stage the IRP column itself. The irp true flag on a finding tells the build which plants need the box ticked in the web form.

### Evergy Kansas Central (2025 IRP Update)

Plan files: https://investors.evergy.com/2025IRPUpdate, https://kskcc.my.site.com/s/case/500cr00000YjcjMAAR/24ekce387cpl?tabset-d4b00=2, https://shareus11.springcm.com/Public/Document/35150/e56d0963-88e0-4e4b-999a-0587e0573f89/ba249c18-eec2-f011-b84a-48df377ee718

Notes already on the tab, newest first:

- In 2025 IRP Update (May 2025), Evergy Kansas Central: 355 MW CC in 2029 (iViola Generating station - shared ownership with Evergy Missouri West), 355MW CC in 203 (MvNew Generating Station - shared ownership with Evergy Missouri West), 710 MW CC in 2031, 2033, 2039, 2040, 400 MW GT in 2044.

GEM plants in the state tied to this utility:

- Emporia energy center (L100000401930): 7 unit(s), operating; matched by owner; IRP box ticked on 0 of 7 units; no task of its own, compare it here
- Evergy Kansas Central 2025 IRP power station 1 (L100001063349): 1 unit(s), announced; matched by owner, plant name; IRP box ticked on 1 of 1 units; its own brief carries an IRP task
- Evergy Kansas Central 2025 IRP power station 2 (L100001063350): 1 unit(s), announced; matched by owner, plant name; IRP box ticked on 1 of 1 units; its own brief carries an IRP task
- Evergy Kansas Central 2025 IRP power station 3 (L100001063351): 1 unit(s), announced; matched by owner, plant name; IRP box ticked on 1 of 1 units; its own brief carries an IRP task
- Evergy Kansas Central 2025 IRP power station 4 (L100001063352): 1 unit(s), announced; matched by owner, plant name; IRP box ticked on 1 of 1 units; its own brief carries an IRP task
- Evergy Kansas Central 2025 IRP power station 5 (L100001063353): 1 unit(s), announced; matched by owner, plant name; IRP box ticked on 1 of 1 units; its own brief carries an IRP task
- Hutchinson energy center (L100000401931): 4 unit(s), operating; matched by owner; IRP box ticked on 0 of 4 units; no task of its own, compare it here
- Jeffrey Energy Center (L100000103922): 1 unit(s), announced; matched by owner; IRP box ticked on 0 of 1 units; its own brief carries an IRP task
- Lawrence Energy Center (Kansas) (L100000103924): 2 unit(s), announced; matched by owner; IRP box ticked on 0 of 2 units; its own brief carries an IRP task
- McNew Generating Station (L100001023601): 1 unit(s), pre-construction; matched by owner; IRP box ticked on 0 of 1 units; its own brief carries an IRP task
- Viola Generating Station (L100001043000): 1 unit(s), pre-construction; matched by owner; IRP box ticked on 0 of 1 units; its own brief carries an IRP task

### Evergy Metro (2025 IRP Update)

Plan files: https://www.efis.psc.mo.gov/Document/Display/822210?utm

Notes already on the tab, newest first:

- The most recent IRP filing for Evergy’s Missouri Kansas is the 2025 IRP Annual Update to 2024 IRP, submitted on March 14, 2025 by Evergy Metro (Missouri Metro and Kansas Metro cover areas surrounding Kansas City). Evergy Metro proposed gas additons in its 2025 update: 440 MW GT in 2031, followed by 355 MW CC in 2032, 2033, 2037, 2039, and 2040 (additional 735 MW of gas units across 2031-2033 compared to the original 2024 IRP) https://investors.evergy.com/2025IRPUpdate Those additions might be in MO or KS.

GEM plants in the state tied to this utility:

- Osawatomie power station (L100000401935): 1 unit(s), operating; matched by owner; IRP box ticked on 0 of 1 units; no task of its own, compare it here
- West Gardner power station (L100000401936): 4 unit(s), operating; matched by owner; IRP box ticked on 0 of 4 units; no task of its own, compare it here

### Kansas City Board of Public Utilities (BPU) (2024 IRP)

Plan files: https://www.bpu.com/Portals/0/pdf/2024-BPU_IRP_Report-2024_11-4-2024.pdf

Notes already on the tab, newest first:

- 2024 IRP includes potential gas power additions in different scenarios. No need in the new generation over the next five years. "New conventional thermal generation did not appear appreciably in the results of this IRP, but as needs for new energy generation and capacity develop, and the wider energy market continues to change, it is recommendedthat new and highly efficient natural gas-fired thermal power plants still be included as possible options to meet some of BPU’s future needs."

GEM has no plant in the state tied to this utility by owner, operator, parent or an IRP placeholder name. Anything the plan commits to is new.

Output: findings on tracked plants go in that plant's shard as usual. New plants, new units and watch items from the plans go in shards/_state.json under newplants, newunits and monitor, each with "irp": true. Then write one plain sentence per utility in meta.irp_summary of _state.json: what the plan adds, what was staged, and the next plan's due date if the plan or the tab gives one.

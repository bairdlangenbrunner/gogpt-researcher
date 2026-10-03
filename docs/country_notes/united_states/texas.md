# United States — Texas

Scope: the largest single GOGPT research assignment anywhere (Q4 2026: 15
researcher-days, priority **high**, ~122 GW in development per the assignments
tab). ERCOT-dominant, deregulated, data-center-driven gas boom. The
air-permit route (TCEQ) is the distinctive Texas source and is already
established in the data: TCEQ is the second most-cited domain in Texas Data
Source cells after EIA.

Snapshot from the scoped export (pull of 2026-08-05; re-derive at batch start):

| | |
|---|---|
| unit rows / plants | 587 / 277 |
| operating | 344 |
| pre-construction / announced / construction | 155 / 36 / 8 |
| cancelled / retired / shelved / mothballed | 31 / 8 / 3 / 2 |
| rows flagged captive ("power" or "both") | 102 |
| rows with an ERCOT or EIA unit ID in Other IDs (unit) | 384 |

## State context

- Grid operator: **ERCOT** (≈90% of Texas load; not FERC-jurisdictional —
  regulated by the PUCT and the Legislature). Panhandle and East Texas edges
  sit in SPP and MISO; a plant's ISO matters for which interconnection queue
  it appears in.
- Regulator stack: **PUCT** (generator registration, CCNs, Texas Energy Fund
  loans), **TCEQ** (air permits — NSR, PSD, Title V), **RRC** (gas supply
  side only).
- Policy signals this cycle: **SB 6** (2025) — data centers co-locating with
  existing plants need PUCT approval; **SB 388** (passed Senate) would require
  half of new capacity to be dispatchable non-battery; the **Texas Energy
  Fund** In-ERCOT Loan Program is financing new dispatchable gas (PUCT
  control number 56896).
- Large state — research by status group first (in-development is ~200 rows),
  then by ISO edge cases; consider splitting operating-unit sweeps by region
  (Gulf Coast industrial / DFW / Permian / Panhandle) if a batch is split.

## Source ladder (Texas-specific; tiers per `docs/reference/source_roster.md`)

**Tier 1 — stand-alone for green**

- **ERCOT monthly GIS Report** (Generator Interconnection Status; EMIL product
  `pg7-200-er`, https://www.ercot.com/mp/data-products/data-product-details?id=pg7-200-er)
  — the backbone for in-development units. Use the *Project Details – Large
  Gen* tab, filter Fuel = Gas; record the IRN (`xxINRxxxx`) in Other IDs
  (unit). **JS-gated**: the monthly `docLookupId` rotates and hard-coded
  mirror URLs 404; download the latest xlsx in a browser or via the ERCOT
  Public API for `pg7-200-er`. Also the **CDR** (Capacity, Demand and
  Reserves) report for planned units with signed IAs.
- **TCEQ air permits** — RN (regulated entity) is the join key.
  - Central Registry / Records Online search by RN:
    https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_SEARCH
  - NSR permit search (Initial Permit Review → Electric Generating
    Facilities lists RNs): https://www2.tceq.texas.gov/airperm/index.cfm
  - NSR pending permits:
    https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/nsr-pending-permits.html
  - Title V operating permit notices:
    https://www.tceq.texas.gov/assets/public/permitting/air/Title_V/announcements/pnwebrpt.htm
  - Public notices search:
    https://www14.tceq.texas.gov/epic/eNotice/index.cfm?fuseaction=main.PublicNoticeShortResults
- **PUCT Interchange** filings (https://interchange.puc.texas.gov) — Texas
  Energy Fund NOI list (June 2024) and due-diligence list (Aug 2024), loan
  agreements, generator registrations.
- **EIA-860M** monthly inventory — status backbone for operating / retired /
  under-construction; EIA plant code → Other IDs (location), generator ID →
  Other IDs (unit). EIA-860 annual for ownership shares.
- **EPA CAMPD / ECHO** — unit-level CEMS emissions are the strongest
  "actually operating" evidence; ICIS-Air for federal permit status.

**Tier 2 — validates alone only if it names the plant and states the value; corroborate when cheap**

- Owner/developer IR and press releases; trade press (Power Engineering,
  Utility Dive, Data Center Dynamics); PRNewswire; local news.
- **Oil & Gas Watch** (Environmental Integrity Project) — its record IDs
  (`EIP: rec_…`) are already in Other IDs (location) for many plants; a good
  finder for permit-stage projects, cite the underlying TCEQ document.
- Data-center trackers (wattbridge, DCD) — finder only.

## Permit semantics → GEM status (proposed; confirm against the manual before staging)

| evidence | supports at most |
|---|---|
| air permit **application** filed / public notice | `announced` (moving toward `pre-construction` if land/financing also evidenced) |
| NSR/PSD permit **issued** | `pre-construction` — a permit is an approval, not construction |
| ERCOT IA signed + financial security posted | `pre-construction` |
| notice of construction start, TCEQ construction-commencement notice, CEMS certification | `construction` |
| first CEMS data / EIA-860M "operating" / ERCOT commercial operations | `operating` |
| permit **voided / expired / withdrawn** with no successor | evidence for `shelved`/`cancelled` clocks (record in Latest Activity) |
| permit **renewal / amendment** | "still alive" evidence — resets the 2y/4y inferred clock |

Permits state **heat input (MMBtu/hr) or turbine ISO ratings**, not net MWe.
Never copy a permit MW into Capacity without a generating-MW source; Gulf
Coast cogeneration permits mix steam and electric output.

## Research tips

- Start every plant from its IDs: EIA plant code + generator IDs, ERCOT IRN,
  TCEQ RN. If any is missing, adding it is in scope (US-only rule: match GEM
  IDs to EIA-860M, EIP, Sierra Club).
- CC blocks: EIA lists CTG-1/CTG-2/STG-1 separately with a shared Unit Code;
  GEM tracks the block as one unit (`docs/reference/unit_conventions.md`).
  The existing Other IDs (unit) cells already hold the comma-joined EIA
  generator IDs for the block — keep that pattern.
- Data-center gas: mark **captive** + industry type Data Centre; the
  Emergency/Backup checkbox is unit-level and only for true backup gensets.
  Many Texas announcements are behind-the-meter — still in scope if ≥50 MW
  generating.
- TCEQ Records Online URLs are query/session links that rot — cite the
  stable document URL and let `url_verifier.py` capture a Wayback snapshot.
- Similarly named plants elsewhere in the US carry the state abbreviation in
  the plant name (`Riverside (OK) power station`).

## Gotchas

- Export `State/Province` is `Texas` (never `TX`); the assignments tab uses
  `United States - Texas`.
- Capacity: shaft/mechanical-drive turbines at compressor stations and LNG
  terminals show up in TCEQ permits — out of scope unless they generate.
- Many pre-construction rows date from the 2024–2025 data-center rush and
  may already be stale; the 2y inferred-shelved clock will start biting in
  Q4 2026–Q2 2027. Check ERCOT GIS withdrawal before inferring.
- Another researcher's tooling (Supabase / Xata storage URLs) appears in some
  2026 Data Source cells — they are file mirrors, not independent sources.

## Open items

- Which Other IDs system names exist in the DB for TCEQ RN and ERCOT IRN —
  confirm the exact `System name` values before staging IDs (new systems
  need a PM/Asana request per the manual).
- Texas-specific discovery escalation threshold (the default "more than ~5
  candidates → stop and talk" will trip on the ERCOT queue alone).
- Pilot: calibration sample of ~9 plants (stratified by status group), blind
  research, then diff against GEM — see `notes/texas_pilot_plan.md`.

## Update notes

- *2026-09-15* — created from the Q4 2026 Update sheet's "United States
  research" Texas row, the GOGPT US Data/Research Guide, and the 2026-08-05
  scoped export profile. Texas is scheduled 2026-11-05 → 2026-12-01 on the
  assigned researcher's weekly plan; this repo's pilot runs ahead of that.

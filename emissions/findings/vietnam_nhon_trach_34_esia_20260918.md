# Nhơn Trạch 3 & 4 (Vietnam)

- GEM location ID / unit IDs: L100000405443 (GEM carries Nhơn Trạch 1–4 as one
  plant; units 3 and 4 are the 2025 start years)
- Local-language name(s) / earlier project names: Nhà máy điện Nhơn Trạch 3 và
  Nhơn Trạch 4 (NT3&4, "NT34" in the ESIA)
- GEM status, capacity, technology (from pull of 2026-09-18): operating, 2 × 812
  MW combined cycle, GE Vernova 9HA.02
- Licensing body and process / licence numbers: ministry (ĐTM pre-dates the
  portal); GPMT report on the portal, id 2462 (stack parameters only)
- Time spent: lender sweep by subagent; values re-checked against the PDF by
  hand, 20 min

## Documents

| # | Title | Type | Issuer | Year | URL | Retrieved | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Nhon Trach 3 and Nhon Trach 4 Power Plant — ESIA according to International Standards (Vol. 1–4 in one PDF, 994 pp.) | ESIA (lender) | Fichtner GmbH & Co. KG for PV Power; disclosed by SERV (Swiss export credit) as a Category A project, 17.07.2024 | Vol. 1 approved 08.03.2024 | https://www.serv-ch.com/fileadmin/user_upload/files/Projektliste/A-Projekte/ESIA_Nhon_Trach_3_and_Nhon_Trach_4_Power_Plant.pdf | 2026-09-18 | Text layer. Vol. 3 (Impact Assessment) starts at PDF p. 478; the air-quality chapter is repeated in a later annex (PDF pp. 812–813) |
| 2 | Project Description — Nhon Trach Petrovietnam | project summary | SERV | 2024 | https://www.serv-ch.com/fileadmin/user_upload/files/Projektliste/A-Projekte/Project_Description_Nhon_Trach_Petrovietnam.pdf | 2026-09-18 | 2 pp. |

Lenders (press): SMBC with SACE cover; Citi / ING with K-SURE and SERV cover;
Vietcombank. SERV is the only one of these found to post the ESIA.

## Emissions evidence

Doc 1. All concentrations dry, 15 % O2, 273.15 K, 101.3 kPa. Operating case OP5
= the normal-operation load with the largest flue-gas flow (the worst case for
the dispersion model), natural gas.

| Pollutant (and PM fraction) | Value + unit (verbatim) | Type | Status | Per | Ref. O2, dry/wet, normalised? | Operating basis | Doc # + page/table |
|---|---|---|---|---|---|---|---|
| NOx (as NO2) | 51 [mg/Nm3] | limit/guarantee | permitted (OEM guarantee) | unit | 15 %, dry, 0 °C | — | 1, PDF p. 492, Table 3 |
| SO2 | 5 [mg/Nm3] | limit/guarantee | permitted (OEM guarantee) | unit | same | — | 1, p. 492, Table 3 |
| Dust (TSP) | 20.0 [mg/Nm3] | limit/guarantee | permitted (OEM guarantee) | unit | same | — | 1, p. 492, Table 3 |
| PM10 / PM2.5 | 18 / 14 [mg/Nm3] | derived | calculated from TSP (90 % / 70 %, Ehrlich et al. 2007) | unit | same | — | 1, p. 492, Table 3 |
| NO2 | 51.3 mg/Nm³ | C | predicted | stack | dry, 15 % O2, 273.15 K | OP5 | 1, p. 498, Table 7 |
| SO2 | 5.4 mg/Nm³ | C | predicted | stack | same | OP5 | 1, p. 498, Table 7 |
| TSP / dust | 20 mg/Nm³ | C | predicted | stack | same | OP5 | 1, p. 498, Table 7 |
| NO2 | 66.2 g/s per unit | B | predicted | unit (one stack each) | — | OP5 | 1, p. 498, Table 7 |
| SO2 | 7.0 g/s per unit | B | predicted | unit | — | OP5 | 1, p. 498, Table 7 |
| TSP / dust | 25.8 g/s per unit | B | predicted | unit | — | OP5 | 1, p. 498, Table 7 |
| PM10 / PM2.5 | 23.2 / 18.1 g/s per unit | B | predicted (90 % / 70 % of TSP) | unit | — | OP5 | 1, p. 498, Table 7 |

Check: 1,289.9 Nm³/s (dry, 15 % O2) × 51.3 mg/Nm³ = 66.2 g/s. The rates and
concentrations agree, unlike Hải Lăng and Cà Ná.

## Stack and technology

- Stacks (Table 7): 2, one per unit, 60 m, internal diameter 8 m, exit 353.8 K,
  21.0 m/s; flow per stack 813.9 Nm³/s wet (11.8 % H2O, actual O2 10.6 %) or
  1,289.9 Nm³/s dry at 15 % O2. Coordinates in WGS 84 zone 48N: 700890 E
  1176932 N and 700708 E 1176912 N.
- Turbine: 2 × GE 9HA.02 single-shaft, each with one HRSG (PDF p. 20).
- NOx controls: low-NOx burners, pre-mix combined with diffusion (p. 20). No
  SCR. The ESIA suggests the client "may consider" SCR to cut NO2 by up to
  50 %, because of cumulative 1-hour NO2 (PDF p. 504).
- Backup fuel: diesel oil, below 500 h/yr and outside normal operation, so it
  was not modelled (pp. 491, 498).
- Hours: "about 9.7 billion kWh each year (with maximum operating hours per
  year, Tmax = 6000h)" (PDF p. 9).
- Mapping to GEM: the ESIA's two units are GEM's NT3 and NT4 units.

## Verdict

- Best evidence type available: **B + C + stack + hours**, `design-hours`
  (Tmax 6,000 h is stated). The only Vietnamese document so far with non-zero
  SO2 and dust **and** consistent rates. PM10 and PM2.5 are derived from TSP by
  a literature split, not measured.
- NOx 51 mg/Nm³ is the 25 ppmv OEM guarantee again, as in most of the ĐTMs.
- Dead ends: SACE and K-SURE disclosure (not listed); the portal GPMT report
  (id 2462) has stack geometry only.
- Next: measured values once NT3&4 has operated long enough to appear in a
  GPMT or monitoring report.

## Tracker leads (route to a normal GOGPT Update batch — not handled here)

- None from this document.

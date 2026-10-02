# Environmental-permit (GPMT) reports for three operating gas plants (Vietnam pilot)

Run 2026-09-18. Vietnam has nothing like Brazil's RAPP: no public per-plant
annual emissions. So this pilot tests the next-best source for operating
plants. Operators applying for an environmental permit (giấy phép môi trường,
GPMT) post a report on the ministry's consultation portal, and that report
should carry the plant's recent monitoring. Three gas plants have one there:
Nhơn Trạch 2, Bà Rịa and Cà Mau 1&2. The five Phú Mỹ plants have none (full
portal inventory, `../coverage/vietnam_portal_all.csv`).

The values are in [`vietnam_gpmt_pilot_20260918.csv`](vietnam_gpmt_pilot_20260918.csv):
one row per test, stack and pollutant, then the design values, then my
derived annual figures. [`vietnam_gpmt_pilot_20260918.py`](vietnam_gpmt_pilot_20260918.py)
holds the typed-in document values with their pages and rebuilds the csv. The
PDFs are scanned or use a legacy font, so the values could not be parsed from
them directly.

Sources (full rows in `../sources/downloads.csv`):
- Nhơn Trạch 2 GPMT report, portal id 4530: https://thamvan.mae.gov.vn/Uploads/18122024/3DBao%20cao%20GPMT%20Nhon%20Trach%202.pdf
- NT2 annual report 2024: https://static2.vietstock.vn/vietstock/2025/4/3/20250403_20250403___nt2___cbtt_bao_cao_thuong_nien_nam_2024.pdf
- Bà Rịa GPMT report, portal id 5807 (scanned): https://thamvan.mae.gov.vn/Uploads/23072025/04BC%20De%20xuat%20cap%20GPMT%20Cong%20ty%20CP%20Nhiet%20dien%20Ba%20Ria.pdf
- Cà Mau 1&2 GPMT report, portal id 5894, main volume: https://thamvan.mae.gov.vn/Uploads/21092025/UMBC%20DTM%20PD.pdf.
  The annexes are `BC%20DTM%20PD_1.pdf` to `_5.pdf` in the same folder;
  part 1 holds the 2004 Cà Mau 1 ĐTM.
- PV Power annual report 2024 (Cà Mau gas use): http://pvpower.vn/pow-media/to-ir/18-4-25---BCTN-2024---VIET.pdf

Page numbers below are PDF pages unless marked "printed".

## Result

| Plant | GEM ID | MW | Monitoring in the report | Best evidence | Rough 2024 NOx (my arithmetic) | Usable? |
|---|---|---|---|---|---|---|
| Nhơn Trạch 2 | L100000405443 (GEM's Nhơn Trạch, 2,839 MW, includes NT2) | — | Quarterly stack tests, 2 stacks, 11 rounds 2022–24 (Bảng 5.9, pp. 150–151) | C, `measured`, + real CO2, gas and generation from the annual report | **≈300–340 t** (0.11–0.12 t/GWh) | **yes** |
| Bà Rịa | L100000405433 | 389 (271.8 MW of it gas turbines) | One campaign, 6 GTs, June 2024, + GT7 retest Dec 2024 (pp. 90, 182) | C, `measured`, one campaign; utilisation from generation × heat rate | ≈86 t/yr, 2022–24 average generation (≈0.6 t/GWh) | **yes, rough**: one snapshot, and the plant runs rarely |
| Cà Mau 1&2 | L100000405435 | 1,500 | CEMS on all 6 stacks, **no values published**; no periodic tests (p. 129) | 2004 design concentrations × 2024 gas use (`rate-only` + real fuel) | ≈630 t (CM1) + ≈950 t (CM2) | **design only**: the measured data exist and are not in the report |
| Phú Mỹ 1, 2.1, 2.2, 3, 4 | L100000405445–449 | 4,007 | no GPMT report on the portal | World Bank design values only (not re-read here) | — | **no** measured source found |

One of the three plants yields a usable measured series. Nhơn Trạch 2 is the
only one tested every quarter. Neither Bà Rịa nor Cà Mau 1&2 asks for an
air-emissions component in its permit. Both say they need no treatment
system, so neither plans periodic stack tests from now on. What gets measured
from here on is Cà Mau's CEMS feed, which goes to the province and is not
published, and nothing at all at Bà Rịa.

## Nhơn Trạch 2

Two gas turbines, each exhausting through its own main stack (KT1 =
GT11, KT2 = GT12): 60 m × 6.8 m, a combined 1,373.7 m³/s at 97 °C (Bảng 1.3,
p. 17). The bypass stacks are 35 m and were not tested.

Tests are quarterly, on gas, by an accredited lab, 2022 Q1 to 2024 Q3 (Bảng
5.9, pp. 150–151). Concentrations are in mg/Nm³ with the reference O2 and the
dry/wet basis not stated. Flow is in m³/h, actual. Ranges over the 22 stack
tests:

| Pollutant | Range | 2024 mean (6 tests) | QCVN 22:2009 col. B limit (Kp 0.85) |
|---|---|---|---|
| NOx | <1.88 – 74.1 mg/Nm³ | 19.0 | 212.5 |
| Dust (total) | 19 – 31.5 | 22.4 | 42.5 |
| CO | <1.14 – 478 | 246.5 | (QCVN 19 col. B) |
| SO2 | <2.62 in every test | — | 255 |
| CO2 | 2.48 – 3.72 % | 3.35 % | — |

Annual tonnes, 2024, three ways (my arithmetic; all use the 2024 mean
concentration):

| Method | Flue volume, bn Nm³ | NOx t | Dust t | CO t |
|---|---|---|---|---|
| A. The annual report's flue-gas volume, 38,624,522,040 m³ (p. 50), read as actual m³ at 97 °C | 28.5 | 542 | 639 | 7,025 |
| B. Reported 1,177,038 t CO2e (p. 46) ÷ measured 3.35 % CO2 | 17.8 | 337 | 398 | 4,377 |
| C. Reported gas use, 530.7 M Sm³ (p. 48), × ~1 Nm³ CO2/Sm³ ÷ 3.35 % | 15.8 | 301 | 355 | 3,901 |

B and C agree to 12 %: the reported CO2 is 1.12 Nm³ per Sm³ of gas, which is
plausible for a gas with some CO2 in it. **A is the outlier, and I would not
use it.** The report's flue volume is 72.8 m³ per Sm³ of gas, more than twice
what 3.35 % CO2 implies. Divided by the mean 2024 test flow for both stacks
(2.82 M m³/h), it gives 13,700 operating hours in a year of 8,760. So the
headline is **≈300–340 t NOx in 2024 (0.11–0.12 t/GWh on 2,742 GWh, p. 31)**:
`measured` concentration × `reported-actual` fuel and CO2.

Checks and caveats:
- Test flows average 57 % of the design flow, so the plant was at part load or
  the flow is under-read. Methods B and C do not depend on it.
- The reference O2 is not stated. If the concentrations were already corrected
  to 15 % O2, dividing by the measured CO2 % would be the wrong flue volume.
  At ~3.35 % CO2 the stack is near 15 % O2 anyway, so the error is small.
- Dust of 19–31.5 mg/Nm³ on gas is high for a gas turbine. It is consistent
  across 22 tests, but it may include condensables or a sampling artefact.
  The ĐTMs predict ~0.
- CO climbs through 2023–24 (up to 478 mg/Nm³) while NOx falls. Some tests
  look like part-load running. The CO tonnes swing most with method and
  should be quoted with care.
- 2023 Q4 KT2 ran at 421,174 m³/h with NOx below detection: likely a start-up
  or near-idle test.

## Bà Rịa

Ten units on one site (p. 18): GT1–2 (GE Frame 5, 23.4 MW each, simple
cycle), GT3–8 (Frame 6, 37.5 MW each, simple or combined cycle), and two steam
turbines, ST9 (58 MW, 1999) and ST10 (59.1 MW, 2002), which emit nothing. HRSG
stacks are 25 m (p. 21). Heat rates are 13,019–13,551 BTU/kWh for GT3–8 and
17,868 for GT1–2 (p. 24). Average generation for 2022–24 is 137 GWh a year
(p. 21; the first digit is smudged in the scan), about a 4 % capacity factor.

Tests (Bảng 24, p. 90). The lab is Công ty CP An toàn – Sức khỏe – Môi trường
Nam Việt, VIMCERTS 314, report 0073-06.2024/KQTN, sampled 4 June 2024; its
certificate is on p. 164. Dust is by US EPA Method 5.

| Unit | Flow m³/h | °C | NOx | Dust | CO | SO2 | CO2 % |
|---|---|---|---|---|---|---|---|
| GT3 | 131,957 | 125 | 29.5 | 10 | 52.4 | <2.62 | 1.45 |
| GT4 | 146,592 | 128 | 71.3 | 13 | 31.9 | <2.62 | 4.25 |
| GT5 | 159,861 | 147 | 73.8 | 11 | 30.8 | <2.62 | 4.55 |
| GT6 | 175,009 | 139 | 68.0 | 15 | 22.8 | <2.62 | 4.50 |
| GT7 | 146,637 | 122 | 80.0 | 10 | 34.2 | <2.62 | 5.15 |
| GT8 | 156,874 | 131 | 81.2 | 13 | 36.5 | <2.62 | 5.37 |
| GT7, 26 Dec 2024 (p. 182, report 0412.12.2024/KQTN) | 141,135 | 115 | 79.6 | 6.2 | 39.9 | n.d. | 5.2 |

All values are mg/Nm³, with the reference O2 not stated. The limits the report
compares against are QCVN 19 col. B (NOx 544, dust 128, CO 640) and QCVN 22
col. B gas (NOx 170, dust 34, SO2 204). GT1–2 were not tested. The text says
monitoring is intermittent because the plant only runs when dispatched.

Annual figure (my arithmetic, `rate-only` + real generation): 137 GWh ×
13,050 BTU/kWh ≈ 1.89 M GJ, which is ≈106 kt CO2, or 1.27 bn Nm³ of flue gas
at the mean 4.21 % CO2. With the mean concentrations that gives **≈86 t NOx,
15 t dust and 44 t CO a year**, or 0.62 t NOx/GWh. The simple-cycle heat rate
makes this an upper bound, because combined-cycle hours need less fuel per
kWh. The June tests are the only concentration data, and they are one day.

Measured flows are ~40 % of what a Frame 6 at full load implies (~440,000 m³/h
actual). So the units were at part load, or the flow is under-read, and
GT3's 1.45 % CO2 points to a unit barely loaded.

## Cà Mau 1&2

Two 750 MW combined-cycle plants with six stacks: four main stacks (60 m ×
7 m) and two CM1 bypass stacks (35 m). There are also two auxiliary-boiler
stacks (Bảng 3.12, p. 85; permit request pp. 111–112).

- **No periodic stack tests**: "Nhà máy không thực hiện quan trắc khí thải
  định kỳ" (p. 129). The proposed programme keeps it that way. Periodic
  monitoring is not required under Art. 98 of Decree 08/2022 (amended by
  Decree 05/2025) (p. 141).
- **CEMS on all six stacks**, measuring dust, O2, CO, CO2, SO2 and NOx, sent
  every 5 minutes to the Cà Mau Department of Agriculture and Environment.
  The report gives only data completeness (97.87–99.98 % received), outage
  lists and counts of abnormal values (Bảng 5.14–5.16, pp. 130–137). For
  example, stack 21 in 2024 had 4,907 abnormal SO2 values (4.76 %). **No
  concentrations anywhere.**
- The company asks that the permit cover no air emissions: "Công ty đề nghị
  không cấp phép đối với khí thải của nhà máy" (pp. 111–112). Its argument is
  that fuel quality makes treatment unnecessary.

The only concentrations in the package are the January 2004 Cà Mau 1 ĐTM,
inside annex part 1 (pp. 59–62): per stack, NOx 52.5 mg/Nm³ on gas (630 on
DO, 126 on DO with water injection), CO 30, dust 10, SO2 151 on DO (S 0.35 %).
The design flue on gas is 665 m³/s at 100 °C, with O2 11.57 %, CO2 4.015 % and
H2O 10.86 %. DO firing is capped at 7 days a year.

Annual figure (my arithmetic, `rate-only` + real fuel): 2024 gas use was
480.06 M Sm³ at CM1 and 729.50 M Sm³ at CM2 (PV Power annual report, printed
p. 88 = PDF p. 44). Divided by 4.015 % CO2, that is 12.0 and 18.2 bn Nm³ of
flue gas, so **≈630 t and ≈950 t NOx**. This is a 2004 design value for
CM1, applied to CM2 as well, with the reference O2 not stated. If 52.5 is at
15 % O2, the actual-O2 concentration would be ~1.6 × higher and so would the
tonnes. Treat it as an order of magnitude.

## Verdict

- **GPMT reports are worth reading, but they are uneven.** They only have
  measured stack data where the permit regime still requires periodic tests.
  Plants with CEMS (Cà Mau) or claiming low risk (Bà Rịa) report
  completeness, or one campaign, and propose nothing further.
- **Nhơn Trạch 2 is Vietnam's one measured anchor for a gas CCGT**: 0.11–0.12
  t NOx/GWh in 2024. The NT3&4 ESIA's design figure is 51 mg/Nm³ at
  15 % O2; NT2 measured 19 mg/Nm³ in 2024 and 35–74 in 2022–23.
- **Cà Mau's measured data exist and are not published.** They are held by
  the Cà Mau department and the ministry, which makes them the obvious target
  for an information request: `exists, not public`.
- A plant-reported annual flue-gas volume (NT2) should not be trusted without
  a carbon-balance check. Here it is ~70 % too high.

## Tracker leads (route to a normal GOGPT Update batch — not handled here)

- **Bà Rịa unit count.** GEM carries L100000405433 as "operating x1; cancelled
  - inferred 4 y x1", 389 MW. The GPMT report (p. 18) lists ten units, GT1–8 and
  ST9–10, totalling 388.9 MW, all apparently still in service (dispatched
  rarely). Worth checking how the units are split.

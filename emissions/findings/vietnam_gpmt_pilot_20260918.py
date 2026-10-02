#!/usr/bin/env python3
"""Build vietnam_gpmt_pilot_20260918.csv: stack values from environmental-permit
(GPMT) reports for three operating Vietnamese gas plants, plus derived checks.

The values are typed in from the documents (scanned or legacy-font PDFs, so
there is no clean table to parse); each row carries its document and PDF page.
The documents are in sources/downloads.csv. Why each number is used, and what
is wrong with it, is in vietnam_gpmt_pilot_20260918.md.

row_type:
  test     a stack test as reported (concentration mg/Nm3, flow m3/h actual)
  design   a design value from an EIA (no operating year)
  derived  my arithmetic, never a document value. Annual tonnes combine a
           reported concentration with a real year's flue volume, fuel or
           generation; basis says which.

kg_h (tests only) = flow x 273/(273+T) x concentration. Flow is reported as
actual m3/h; concentration as mg/Nm3 with the reference O2 and moisture basis
not stated, so kg_h is an estimate, not a reported rate. Where the test gives
no temperature, the design exit temperature is used and noted.
"""
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'vietnam_gpmt_pilot_20260918.csv')

NT2 = ('Nhon Trach 2', 'L100000405443', 'nhontrach2_gpmt_2024.pdf')
BR = ('Ba Ria', 'L100000405433', 'baria_gpmt_2025.pdf')
CM = ('Ca Mau 1&2', 'L100000405435', 'camau12_gpmt_2025_part1.pdf')

# --- NT2 GPMT (portal id 4530), Bảng 5.9, PDF pp. 150-151. On gas. No test
# temperature: design exit 97 C (Bảng 1.3, PDF p. 17). CO2 in % vol.
# (date, stack, flow m3/h, dust, SO2, NOx, CO, CO2 %); '<x' = below detection
NT2_TESTS = [
    ('2022-03-30', 'KT1 (GT11)', 1021560, 28.5, '<2.62', 35, 22, 2.92),
    ('2022-03-30', 'KT2 (GT12)', 1231055, 27.9, '<2.62', 29, 18, 2.9),
    ('2022-06-16', 'KT1 (GT11)', 1092117, 25.8, '<2.62', 35, 15, 2.64),
    ('2022-06-16', 'KT2 (GT12)', 1325110, 30.6, '<2.62', 37, 19, 2.48),
    ('2022-09-21', 'KT1 (GT11)', 1109224, 27.3, '<2.62', 41.6, 24, 2.7),
    ('2022-09-21', 'KT2 (GT12)', 1319006, 29.5, '<2.62', 41.5, 20.5, 2.81),
    ('2022-12-05', 'KT1 (GT11)', 1016913, 23.1, '<2.62', 23.7, 30.8, 2.74),
    ('2022-12-05', 'KT2 (GT12)', 1820724, 27.5, '<2.62', 42.1, 163, 2.86),
    ('2023-03-27', 'KT1 (GT11)', 1413000, 28.2, '<2.62', 47.9, 14.8, 2.67),
    ('2023-03-27', 'KT2 (GT12)', 1457550, 31.5, '<2.62', 54.5, 76.4, 2.71),
    ('2023-06-12', 'KT1 (GT11)', 1629278, 22.6, '<2.62', 53.6, 105, 3.57),
    ('2023-06-12', 'KT2 (GT12)', 1788604, 27.5, '<2.62', 40, 150, 3),
    ('2023-09-06', 'KT1 (GT11)', 1490772, 24, '<2.62', 74.1, 17.1, 3.72),
    ('2023-09-06', 'KT2 (GT12)', 1519215, 30, '<2.62', 52.3, 27.4, 3.58),
    ('2023-12-12', 'KT1 (GT11)', 1397910, 19, '<2.62', 5.64, 212, 3.4),
    ('2023-12-12', 'KT2 (GT12)', 421174, 24, '<2.62', '<1.88', '<1.14', 2.79),
    ('2024-03-26', 'KT1 (GT11)', 1264027, 23, '<2.62', 18.8, 135, 3.22),
    ('2024-03-26', 'KT2 (GT12)', 1432225, 20, '<2.62', 23.5, 109, 3.17),
    ('2024-06-13', 'KT1 (GT11)', 1332102, 27.3, '<2.62', 23.3, 478, 3.29),
    ('2024-06-13', 'KT2 (GT12)', 1384156, 23.1, '<2.62', 27.4, 326, 3.3),
    ('2024-09-19', 'KT1 (GT11)', 1526580, 21.9, '<2.62', 9.21, 309, 3.51),
    ('2024-09-19', 'KT2 (GT12)', 1516402, 19.3, '<2.62', 11.8, 122, 3.63),
]
NT2_T = 97
NT2_DESIGN_FLOW_M3H = 1373.7 * 3600    # both main stacks, Bảng 1.3, PDF p. 17
# NT2 annual report 2024 (vietstock.vn), page numbers of the PDF
NT2_FLUE_M3 = 38624522040     # "lưu lượng khí thải", p. 50; basis (actual/normal) not stated
NT2_GAS_SM3 = 530.7e6         # p. 48
NT2_CO2_T = 1177038           # t CO2e, p. 46
NT2_GWH = 2742                # p. 31 (2.74 billion kWh, p. 11)

# --- Bà Rịa GPMT (portal id 5807), scanned. Bảng 24, PDF p. 90 (June 2024,
# lab certificate p. 164, report 0073-06.2024/KQTN, VIMCERTS 314); GT-7 retest
# 26/12/2024, report 0412.12.2024/KQTN, PDF p. 182.
# (date, unit, flow m3/h, T C, dust, SO2, NOx, CO, CO2 %)
BR_TESTS = [
    ('2024-06-04', 'GT3', 131957, 125, 10, '<2.62', 29.5, 52.4, 1.45),
    ('2024-06-04', 'GT4', 146592, 128, 13, '<2.62', 71.3, 31.9, 4.25),
    ('2024-06-04', 'GT5', 159861, 147, 11, '<2.62', 73.8, 30.8, 4.55),
    ('2024-06-04', 'GT6', 175009, 139, 15, '<2.62', 68.0, 22.8, 4.50),
    ('2024-06-04', 'GT7', 146637, 122, 10, '<2.62', 80.0, 34.2, 5.15),
    ('2024-06-04', 'GT8', 156874, 131, 13, '<2.62', 81.2, 36.5, 5.37),
    ('2024-12-26', 'GT7', 141135, 115, 6.2, 'not detected', 79.6, 39.9, 5.2),
]
BR_PAGE = {'2024-06-04': 'PDF p. 90 (Bảng 24); certificate p. 164', '2024-12-26': 'PDF p. 182'}
BR_GWH = 137               # 2022-24 average, PDF p. 21 (first digit smudged)
BR_HEAT_RATE = 13050       # BTU/kWh, Frame 6 units GT3-8, PDF p. 24 (13,019-13,551)

# --- Cà Mau 1 ĐTM (Jan 2004), inside GPMT annex part 1, PDF pp. 59-62. Per
# stack, 2 stacks; reference O2 not stated; flue on gas O2 11.57 %, CO2
# 4.015 %, H2O 10.86 % (so a wet, actual-O2 composition).
CM_DESIGN = [('NOx', 52.5, 'gas'), ('CO', 30, 'gas'), ('dust', 10, 'gas'),
             ('NOx', 630, 'DO'), ('NOx', 126, 'DO, water injection'), ('CO', 100, 'DO'),
             ('SO2', 151, 'DO, S 0.35 %'), ('dust', 25, 'DO')]
CM_CO2_FRAC = 0.04015
# POW annual report 2024, printed p. 88 (PDF p. 44): 2024 gas use, million Sm3
CM_GAS = {'Ca Mau 1': 480.06e6, 'Ca Mau 2': 729.50e6}

N_CO2 = 1.9768       # kg per Nm3 of CO2 at 0 C
CO2_PER_GJ = 56.1    # kg CO2 per GJ of natural gas (IPCC 2006 default)


def num(v):
    return v if isinstance(v, (int, float)) else None


def row(p, **k):
    r = dict(plant=p[0], gem_location_id=p[1], doc=p[2], unit='', date='', pollutant='',
             value='', uom='', row_type='', basis='', flow_m3h='', temp_c='', kg_h='', page='', note='')
    r.update(k)
    return r


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs)


out = []
POLS = ['dust', 'SO2', 'NOx', 'CO']
for d, u, flow, *conc, co2 in NT2_TESTS:
    for pol, v in zip(POLS, conc):
        c = num(v)
        out.append(row(NT2, unit=u, date=d, pollutant=pol, value=v, uom='mg/Nm3', row_type='test',
                       basis='measured', flow_m3h=flow, temp_c=f'{NT2_T} (design)',
                       kg_h=round(flow * 273 / (273 + NT2_T) * c / 1e6, 1) if c else '',
                       page='PDF pp. 150-151, Bảng 5.9', note='quarterly test, on gas'))
    out.append(row(NT2, unit=u, date=d, pollutant='CO2', value=co2, uom='% vol', row_type='test',
                   basis='measured', flow_m3h=flow, page='PDF pp. 150-151, Bảng 5.9'))
for d, u, flow, t, *conc, co2 in BR_TESTS:
    for pol, v in zip(POLS, conc):
        c = num(v)
        out.append(row(BR, unit=u, date=d, pollutant=pol, value=v, uom='mg/Nm3', row_type='test',
                       basis='measured', flow_m3h=flow, temp_c=t,
                       kg_h=round(flow * 273 / (273 + t) * c / 1e6, 2) if c else '',
                       page=BR_PAGE[d], note='one-off campaign; plant proposes no further stack tests'))
    out.append(row(BR, unit=u, date=d, pollutant='CO2', value=co2, uom='% vol', row_type='test',
                   basis='measured', flow_m3h=flow, temp_c=t, page=BR_PAGE[d]))
for pol, v, fuel in CM_DESIGN:
    out.append(row(CM, unit='Ca Mau 1, per stack', pollutant=pol, value=v, uom='mg/Nm3', row_type='design',
                   basis='rate-only', flow_m3h=665 * 3600 if fuel == 'gas' else 700 * 3600,
                   temp_c=100 if fuel == 'gas' else 127, page='annex part 1, PDF pp. 59-62',
                   note=f'2004 DTM design value, fuel {fuel}; reference O2 not stated'))


def derived(p, unit, pol, t, basis, note, year='2024', page=''):
    out.append(row(p, unit=unit, date=year, pollutant=pol, value=round(t), uom='t/yr',
                   row_type='derived', basis=basis, page=page, note=note))


# NT2: 2024 means of the three 2024 test rounds, both stacks
t24 = [x for x in NT2_TESTS if x[0].startswith('2024')]
m = {pol: mean([num(x[3 + i]) for x in t24]) for i, pol in enumerate(POLS) if pol != 'SO2'}  # SO2 all below detection
co2 = mean([x[7] for x in t24]) / 100
flue_a = NT2_FLUE_M3 * 273 / (273 + NT2_T)         # method A: reported volume, read as actual at 97 C
flue_b = NT2_CO2_T * 1000 / N_CO2 / co2            # method B: reported CO2 / measured CO2 %
flue_c = NT2_GAS_SM3 * 1.0 / co2                   # method C: gas use, ~1 Nm3 CO2 per Sm3 gas
for tag, flue, basis in [('A: reported flue volume', flue_a, 'reported-actual volume x measured conc'),
                         ('B: reported CO2 / measured CO2 %', flue_b, 'reported-actual CO2 x measured conc'),
                         ('C: reported gas use / measured CO2 %', flue_c, 'reported-actual fuel x measured conc')]:
    for pol in ['NOx', 'dust', 'CO']:
        t = flue * m[pol] / 1e9
        derived(NT2, 'plant (GT11+GT12)', pol, t, basis,
                f'method {tag}; flue {flue / 1e9:.1f} bn Nm3; 2024 mean {m[pol]:.1f} mg/Nm3; '
                f'{t / NT2_GWH:.3f} t/GWh', page='annual report 2024 pp. 46, 48, 50; GPMT Bảng 5.9')
test_flow = mean([x[2] for x in t24]) * 2           # both stacks
derived_rows_nt2 = dict(
    flue_per_sm3=NT2_FLUE_M3 / NT2_GAS_SM3,
    equiv_hours=NT2_FLUE_M3 / test_flow,
    test_vs_design=test_flow / NT2_DESIGN_FLOW_M3H,
    co2_per_sm3=NT2_CO2_T * 1000 / N_CO2 / NT2_GAS_SM3)

# Bà Rịa: generation x heat rate -> CO2 -> flue at the mean measured CO2 %
june = [x for x in BR_TESTS if x[0] == '2024-06-04']
co2_br = mean([x[8] for x in june]) / 100
gj = BR_GWH * 1e6 * BR_HEAT_RATE * 1.055056e-6
flue_br = gj * CO2_PER_GJ / N_CO2 / co2_br
for pol, i in [('NOx', 6), ('dust', 4), ('CO', 7)]:
    c = mean([num(x[i]) for x in june])
    t = flue_br * c / 1e9
    derived(BR, 'plant (GT3-8)', pol, t, 'rate-only + real generation',
            f'{BR_GWH} GWh x {BR_HEAT_RATE} BTU/kWh -> {gj * CO2_PER_GJ / 1e6:.0f} kt CO2 -> '
            f'{flue_br / 1e9:.2f} bn Nm3 at {co2_br * 100:.2f} % CO2; mean {c:.1f} mg/Nm3; '
            f'{t / BR_GWH:.3f} t/GWh; heat rate is simple-cycle, so an upper bound',
            year='2022-24 average', page='PDF pp. 21, 24, 90')

# Cà Mau: 2024 gas use -> flue at the design CO2 % -> design NOx on gas
for u, gas in CM_GAS.items():
    flue = gas / CM_CO2_FRAC
    for pol, c in [('NOx', 52.5), ('dust', 10), ('CO', 30)]:
        derived(CM, u, pol, flue * c / 1e9, 'rate-only + real fuel',
                f'{gas / 1e6:.2f} M Sm3 gas / {CM_CO2_FRAC * 100} % CO2 = {flue / 1e9:.1f} bn Nm3 x '
                f'{c} mg/Nm3 (2004 design, ref O2 not stated)',
                page='POW annual report 2024 p. 88 (PDF p. 44); annex part 1 PDF pp. 59-62')

with open(OUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, list(out[0]))
    w.writeheader()
    w.writerows(out)
print(f'wrote {OUT} ({len(out)} rows)')
print('NT2 2024 means', {k: round(v, 1) for k, v in m.items()}, 'CO2 %', round(co2 * 100, 2))
print('NT2 checks', {k: round(v, 2) for k, v in derived_rows_nt2.items()})
print('BR mean CO2 %', round(co2_br * 100, 2), 'flue bn Nm3', round(flue_br / 1e9, 2))
for r in out:
    if r['row_type'] == 'derived':
        print(r['plant'], r['unit'], r['pollutant'], r['value'], '|', r['note'][:110])

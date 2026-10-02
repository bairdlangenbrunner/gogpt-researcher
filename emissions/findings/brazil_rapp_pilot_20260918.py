#!/usr/bin/env python3
"""Build brazil_rapp_pilot_20260918.csv: IBAMA RAPP air-emission reports for 10 pilot plants.

Input: IBAMA RAPP emissoesPoluentesAtmosfericos/relatorio.csv (sources/raw, see
sources/downloads.csv). Each plant maps to the CNPJ(s) that report its thermal
generation; the mapping and why is in brazil_rapp_pilot_20260918.md.

value_class: value | reported-zero (0.00 filed) | placeholder (a CNPJ-year where
every pollutant filed is <=0.05 t: token entries before or at start-up, not real
figures; a lone 0.01 t SOx next to real NOx is a real value for a gas plant).
t_per_gwh_full_cf: tonnes / (MW x 8.76 GWh), i.e. the intensity if the plant had
run all year. It is a floor on the true intensity; >2 means the figure is too
high for a gas plant at any load, and needs checking against generation.
"""
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
RAPP = os.path.join(HERE, '..', 'sources', 'raw', 'brazil', 'dadosabertos.ibama.gov.br', 'relatorio_emissoes.csv')
OUT = os.path.join(HERE, 'brazil_rapp_pilot_20260918.csv')
THERMAL = ('Produção de energia termoelétrica', 'Usina Termoelétrica')

# plant, gem_location_id, MW (GEM operating), match_type, [CNPJs]
PLANTS = [
    ('GNA I', 'L100000406493', 1338, 'clean', ['23.449.511/0001-90']),
    ('Porto de Sergipe', 'L100000406527', 1593, 'clean', ['23.758.522/0001-52']),
    ('Parnaiba', 'L100000406523', 1906, 'complex-sum',
     ['11.744.699/0001-10', '14.578.002/0001-77', '10.536.701/0001-01', '15.842.091/0001-80', '15.743.303/0001-71']),
    ('Norte Fluminense', 'L100000406520', 827, 'clean', ['03.258.983/0002-30']),
    ('Termopernambuco', 'L100000406543', 533, 'reported-zero', ['03.795.050/0001-09', '03.795.050/0002-81']),
    ('Uruguaiana', 'L100000406540', 640, 'reported-zero', ['01.600.202/0001-37', '00.350.763/0025-30']),
    ('Governador Leonel Brizola (Termorio)', 'L100000406489', 989, 'probable', ['33.000.167/0092-49']),
    ('Termomacae', 'L100000408547', 922, 'clean', ['02.290.787/0001-07']),
    ('Maua 3', 'L100000406511', 591, 'clean', ['17.957.780/0007-50', '00.350.763/0012-15']),
    ('Karkey 013', 'L100000408546', 259, 'none', []),
]


def pol(p):
    p = p.lower()
    if 'nitrog' in p: return 'NOx'
    if 'enxofre' in p: return 'SOx'
    if 'partic' in p: return 'PM'
    if 'monóxido de carbono' in p: return 'CO'


rows = list(csv.DictReader(open(RAPP, encoding='utf-8'), delimiter=';'))
yearmax = {}
for x in rows:
    if x['Detalhe'] in THERMAL and pol(x['Poluente emitido']):
        k = (x['CNPJ'], x['Ano'])
        yearmax[k] = max(yearmax.get(k, 0), float(x['Quantidade'].replace(',', '')))
out = []
for plant, gid, mw, match, cnpjs in PLANTS:
    for x in rows:
        if x['CNPJ'] in cnpjs and x['Detalhe'] in THERMAL and pol(x['Poluente emitido']):
            t = float(x['Quantidade'].replace(',', ''))
            vc = 'placeholder' if 0 < yearmax[(x['CNPJ'], x['Ano'])] <= 0.05 else 'reported-zero' if t == 0 else 'value'
            out.append(dict(plant=plant, gem_location_id=gid, mw=mw, year=x['Ano'], pollutant=pol(x['Poluente emitido']),
                            tonnes=round(t, 2), method={'Medição': 'measured', 'Calculo': 'calculated', 'Estimativa': 'estimated'}.get(x['Metodologia utilizada'], x['Metodologia utilizada']),
                            value_class=vc, cnpj=x['CNPJ'], razao_social=x['Razão Social'], municipio=x['Município'],
                            match_type=match, t_per_gwh_full_cf=round(t / (mw * 8.76), 3)))
    if not cnpjs:
        out.append(dict(plant=plant, gem_location_id=gid, mw=mw, match_type=match))
out.sort(key=lambda r: (r['plant'], r.get('year', ''), r.get('pollutant', ''), r.get('cnpj', '')))
F = ['plant', 'gem_location_id', 'mw', 'year', 'pollutant', 'tonnes', 'method', 'value_class', 'cnpj', 'razao_social',
     'municipio', 'match_type', 't_per_gwh_full_cf']
with open(OUT, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=F); w.writeheader(); w.writerows(out)
print(len(out), 'rows')

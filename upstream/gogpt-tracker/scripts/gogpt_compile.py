#!/usr/bin/env python3
"""
GOGPT compile: turn a raw GOGPT database CSV export into the compiled
multi-tab xlsx deliverable.

Faithful port of GOGPT_database_to_dl_file-withH2criteria.ipynb with one
addition: an "IRP" tab containing units with status == 'announced' and
"IRP" in the plant name. Those units are MOVED OUT of the main tab.

Tabs written:
  - "Gas & Oil Units"     : threshold-passing units (IRP units removed)
  - "sub-threshold units" : units below the capacity threshold
  - "IRP"                 : announced units with "IRP" in the plant name

Usage:
  python3 gogpt_compile.py --input <raw_export.csv> [--h2 <H2_units_to_exclude.xlsx>] [--outdir <dir>]
"""
import argparse
import os
import time
import pandas as pd

from gogpt_paths import H2_EXCLUDE_FILE, OUTPUT_DIR

EU_THRESHOLD_COUNTRIES = [
    'Albania', 'Austria', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria',
    'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland',
    'France', 'Germany', 'Greece', 'Hungary', 'Ireland', 'Italy', 'Kosovo',
    'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Montenegro',
    'Netherlands', 'North Macedonia', 'Norway', 'Poland', 'Portugal',
    'Romania', 'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden',
    'Switzerland', 'Türkiye', 'Ukraine', 'United Kingdom',
]

RETIRED_YEARS_TO_KEEP = ['not found', 2020, 2021, 2022, 2023, 2024, 2025, 2026, 'NaN', '']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True, help='Raw GOGPT database CSV export')
    ap.add_argument('--h2', default=H2_EXCLUDE_FILE,
                    help='H2 units to exclude xlsx (default: bundled list in assets/)')
    ap.add_argument('--outdir', default=OUTPUT_DIR, help='Output directory')
    args = ap.parse_args()

    h2 = pd.read_excel(pd.ExcelFile(args.h2))
    h2_ids = h2['GEM Unit ID'].to_list()

    df = pd.read_csv(args.input, dtype={'Unit name': str})
    print(f"Loaded rows: {len(df)}")

    # --- remove retired pre-2020 ---
    mask = df[(df['Status'] == 'retired') & (~df['Retired year'].isin(RETIRED_YEARS_TO_KEEP))]
    df = df.merge(mask, how='left', indicator=True)
    df = df[df['_merge'] == 'left_only']
    print(f"After dropping retired pre-2020: {len(df)}")

    df['Unit name'] = df['Unit name'].astype(str)

    # --- capacity threshold ---
    df['Capacity (MW)'] = df['Capacity (MW)'].replace('not found', 0).astype(float)
    eu = df[df['Country/Area'].isin(EU_THRESHOLD_COUNTRIES) & (df['Capacity (MW)'] >= 20)]
    non_eu = df[~df['Country/Area'].isin(EU_THRESHOLD_COUNTRIES) & (df['Capacity (MW)'] >= 50)]
    # WSTH-NG = waste heat from natural gas; matched on the spelled-out Fuel value
    WSTH_NG_FUEL = 'fossil gas: waste heat from natural gas'
    non_eu_all = df[~df['Country/Area'].isin(EU_THRESHOLD_COUNTRIES)]
    non_eu_wsthng = non_eu_all[(non_eu_all['Fuel'] == WSTH_NG_FUEL) & (non_eu_all['Capacity (MW)'] < 50)]

    gas = pd.concat([eu, non_eu, non_eu_wsthng], axis=0)
    print(f"Threshold-passing units: {len(gas)}")

    # --- sub-threshold tab ---
    sub_threshold = df[~df.isin(gas)].dropna(how='all')
    print(f"Sub-threshold units: {len(sub_threshold)}")

    # --- fill 'not found' for blank year fields ---
    # cast to object so string sentinels can coexist with numeric years
    gas['Retired year'] = gas['Retired year'].astype(object)
    gas['Start year'] = gas['Start year'].astype(object)
    for row in gas.index:
        status = gas.at[row, 'Status']
        if status == 'retired' and pd.isna(gas.at[row, 'Retired year']):
            gas.at[row, 'Retired year'] = 'not found'
        if status in ('operating', 'mothballed', 'announced', 'pre-construction', 'construction') \
                and pd.isna(gas.at[row, 'Start year']):
            gas.at[row, 'Start year'] = 'not found'
    gas['Retired year'] = gas['Retired year'].replace('Not found', 'not found')
    gas['Start year'] = gas['Start year'].replace('Not found', 'not found')

    # --- remove H2 conversions ---
    gas = gas[~gas['GEM unit ID'].isin(h2_ids)]
    print(f"After removing H2 conversions: {len(gas)}")

    # --- IRP tab: announced + "IRP" in plant name, MOVED OUT of main tab ---
    irp_mask = (gas['Status'] == 'announced') & (gas['Plant name'].astype(str).str.contains('IRP', case=False, na=False))
    irp = gas[irp_mask].copy()
    gas = gas[~irp_mask].copy()
    print(f"IRP units (moved to IRP tab): {len(irp)}")
    print(f"Final Gas & Oil Units: {len(gas)}")

    # --- clean up ---
    gas = gas.drop('_merge', axis=1)
    for d in (gas, sub_threshold, irp):
        for col in d.columns:
            d[col] = d[col].fillna('').replace('nan', '')

    # --- export ---
    ts = time.strftime('%Y-%m-%d', time.localtime())
    out = os.path.join(args.outdir, f'Global Oil and Gas Plant Tracker (GOGPT) compiled {ts}.xlsx')
    # strings_to_urls=False: xlsxwriter auto-converts URL-shaped cells to hyperlinks
    # and a worksheet caps at 65,530 hyperlinks. The *Data Source columns hold many
    # long URLs; without this, later columns (Start Year/Captive/Owners/Location...)
    # silently write blank once the cap is hit. Keep them as plain text.
    writer = pd.ExcelWriter(out, engine='xlsxwriter',
                            engine_kwargs={'options': {'strings_to_urls': False}})

    def write_tab(d, name):
        d.to_excel(writer, sheet_name=name, index=False)
        for column in d:
            width = max(d[column].astype(str).map(len).max() if len(d) else 0, len(str(column)))
            writer.sheets[name].set_column(d.columns.get_loc(column), d.columns.get_loc(column), width)

    write_tab(gas, 'Gas & Oil Units')
    write_tab(sub_threshold, 'sub-threshold units')
    write_tab(irp, 'IRP')
    writer.close()
    print(f"WROTE: {out}")


if __name__ == '__main__':
    main()

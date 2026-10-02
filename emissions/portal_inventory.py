#!/usr/bin/env python3
"""Inventory Vietnam's ministry consultation portal (thamvan.mae.gov.vn).

Step 1 of the Vietnam census in search_plan.md. Pages through the whole ĐTM
list (/Home/DSDTM) and the whole environmental-permit list (/Home/DSGiayPhep),
keeps every row, then pulls the detail JSON (/XemChiTiet/XemChiTiet?id=N:
owner, consultant, dates, file list) for rows that look like power / gas /
LNG projects.

    python portal_inventory.py                 # list + details
    python portal_inventory.py --details-only  # reuse the saved list

Outputs (coverage/):
    vietnam_portal_all.csv        every row of both lists (list columns only)
    vietnam_portal_inventory.csv  the power / gas / LNG subset, with details

The portal drops about every other TLS handshake (curl exit 35). That is
flakiness, not a block: one request at a time, up to 8 retries. HTTPS only.
"""
import argparse
import csv
import datetime as dt
import html
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_ALL = os.path.join(HERE, 'coverage', 'vietnam_portal_all.csv')
OUT_INV = os.path.join(HERE, 'coverage', 'vietnam_portal_inventory.csv')
BASE = 'https://thamvan.mae.gov.vn'
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/128.0 Safari/537.36')
LISTS = {'DTM': '/Home/DSDTM', 'GPMT': '/Home/DSGiayPhep'}

# Matched against the lower-cased, accent-kept title. Broad on purpose: the
# join (step 2) is where false positives are dropped.
KEYWORDS = ['lng', 'điện khí', 'nhiệt điện', 'nhà máy điện', 'tua bin khí', 'tuabin khí',
            'chu trình hỗn hợp', 'khí hóa lỏng', 'khí thiên nhiên', 'trung tâm điện',
            'điện lực', 'phú mỹ', 'nhơn trạch', 'cà mau', 'ô môn', 'bà rịa',
            'khí - điện', 'khí điện', 'kho khí', 'kho cảng khí']
ROW_RE = re.compile(r'<tr id="row_(\d+)">(.*?)</tr>', re.S)
TD_RE = re.compile(r'<td[^>]*>(.*?)</td>', re.S)
TOTAL_RE = re.compile(r'Tổng số:\s*<b>(\d+)</b>')


def fetch(path, tries=8):
    url = BASE + path
    for i in range(tries):
        r = subprocess.run(['curl', '-sS', '--max-time', '90', '-A', UA, url],
                           capture_output=True)
        if r.returncode == 0 and r.stdout:
            return r.stdout.decode('utf-8', 'replace')
        time.sleep(2 + i)
    raise RuntimeError(f'gave up after {tries} tries: {url}')


def clean(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()


def parse_list(text, kind):
    rows = []
    for rid, body in ROW_RE.findall(text):
        tds = TD_RE.findall(body)
        if len(tds) < 6:
            continue
        rows.append({'id': rid, 'list': kind, 'title': clean(tds[1]),
                     'location': clean(tds[2]), 'owner': clean(tds[3]),
                     'posted': clean(tds[4]), 'state': clean(tds[5])})
    return rows


def enumerate_lists():
    out = []
    for kind, path in LISTS.items():
        first = fetch(f'{path}?page=1')
        total = int(TOTAL_RE.search(first).group(1))
        pages = (total + 9) // 10
        print(f'{kind}: {total} rows, {pages} pages', flush=True)
        rows = parse_list(first, kind)
        for p in range(2, pages + 1):
            rows += parse_list(fetch(f'{path}?page={p}'), kind)
            if p % 20 == 0:
                print(f'  {kind} page {p}/{pages}, {len(rows)} rows', flush=True)
        if len(rows) != total:
            print(f'  WARNING {kind}: parsed {len(rows)} of {total}', flush=True)
        out += rows
    return out


def ms_date(v):
    m = re.search(r'\d+', v or '')
    if not m:
        return ''
    return dt.datetime.fromtimestamp(int(m.group()) / 1000, dt.timezone.utc).date().isoformat()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--details-only', action='store_true')
    a = ap.parse_args()

    fields_all = ['id', 'list', 'title', 'location', 'owner', 'posted', 'state']
    if a.details_only:
        with open(OUT_ALL, newline='', encoding='utf-8') as f:
            rows = list(csv.DictReader(f))
    else:
        rows = enumerate_lists()
        with open(OUT_ALL, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fields_all)
            w.writeheader()
            w.writerows(rows)
        print(f'wrote {OUT_ALL} ({len(rows)} rows)', flush=True)

    hits = [r for r in rows if any(k in r['title'].lower() for k in KEYWORDS)]
    print(f'{len(hits)} keyword hits; fetching details', flush=True)
    fields = fields_all + ['matched', 'consult_type', 'consultant', 'owner_detail',
                           'owner_address', 'site', 'status_code', 'deadline',
                           'opinion_date', 'files', 'retrieved']
    today = dt.date.today().isoformat()
    for n, r in enumerate(hits, 1):
        r['matched'] = '; '.join(k for k in KEYWORDS if k in r['title'].lower())
        j = json.loads(fetch(f"/XemChiTiet/XemChiTiet?id={r['id']}"))
        d = j.get('data') or {}
        r.update({'consult_type': d.get('IdLoaiThamVan', ''),
                  'consultant': d.get('DonViTuVan') or '',
                  'owner_detail': d.get('TenChuDuAn') or '',
                  'owner_address': d.get('DiaChiChuDA') or '',
                  'site': d.get('DiaDiemThucHien') or '',
                  'status_code': d.get('TrangThai', ''),
                  'deadline': ms_date(d.get('NgayHetHanYKien')),
                  'opinion_date': ms_date(d.get('NgayPheDuyetYKien')),
                  'files': ' | '.join(BASE + h['Path'] for h in j.get('hs') or []),
                  'retrieved': today})
        if n % 10 == 0:
            print(f'  details {n}/{len(hits)}', flush=True)
    with open(OUT_INV, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fields)
        w.writeheader()
        w.writerows(hits)
    print(f'wrote {OUT_INV} ({len(hits)} rows)', flush=True)


if __name__ == '__main__':
    sys.exit(main())

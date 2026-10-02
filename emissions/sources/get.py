#!/usr/bin/env python3
"""Download a source file into raw/ and record it in downloads.csv.

Every file saved for the emissions workstream goes through here, so that
downloads.csv is the complete list of what was downloaded, from where, when,
and by which route. It records the sha256, so any copy can be checked later.

    # fetch: curl with a browser UA first, then curl_cffi Chrome impersonation
    python get.py URL --to brazil/ibama/litos_eia_vol1.pdf \
        --publisher IBAMA --title "UTE Litos EIA, volume 1" --session 1565c1b9

    # register a file fetched another way (SharePoint REST, form POST, Drive)
    python get.py URL --register /path/to/file.pdf --route sharepoint_rest \
        --to brazil/ibama/suape5_ras.pdf --publisher IBAMA --title "..."

    # record a read without keeping the file (e.g. private or huge)
    python get.py URL --no-keep --publisher ... --title ... --notes "why"

Rules it enforces:
- Refuses gem.wiki, globalenergymonitor.org and abarrelfull.
- Never overwrites a file in raw/; pick a new --to name instead.
- raw/ is gitignored and downloads.csv is committed, so never put private
  or confidential material in raw/. Record it with --no-keep.
"""
import argparse
import csv
import datetime as dt
import hashlib
import os
import shutil
import subprocess
import sys
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, 'raw')
REGISTER = os.path.join(HERE, 'downloads.csv')
FIELDS = ['retrieved', 'session', 'country', 'kind', 'publisher', 'title', 'url', 'route',
          'http_status', 'bytes', 'sha256', 'local_path', 'confidence', 'notes']
BANNED = ('gem.wiki', 'globalenergymonitor.org', 'abarrelfull')
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def via_curl(url, dest):
    r = subprocess.run(['curl', '-sL', '--compressed', '-A', UA, '-H', 'Accept-Language: en-US,en;q=0.9',
                        '--max-time', '900', '-o', dest, '-w', '%{http_code}', url],
                       capture_output=True, text=True)
    return r.stdout.strip() or '000'


def via_curl_cffi(url, dest):
    from curl_cffi import requests  # optional dependency
    r = requests.get(url, impersonate='chrome', timeout=900, allow_redirects=True)
    with open(dest, 'wb') as f:
        f.write(r.content)
    return str(r.status_code)


def fetch(url, dest):
    status = via_curl(url, dest)
    if status == '200' and os.path.getsize(dest) > 0:
        return 'curl', status
    try:
        status = via_curl_cffi(url, dest)
        return 'curl_cffi', status
    except ImportError:
        return 'curl', status


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('url')
    ap.add_argument('--to', help='path under raw/, e.g. brazil/ibama/litos_eia_vol1.pdf')
    ap.add_argument('--register', metavar='FILE', help='copy and record an already-fetched file')
    ap.add_argument('--no-keep', action='store_true', help='record the access only, keep no copy')
    ap.add_argument('--route', help='how it was fetched (default: detected)')
    ap.add_argument('--publisher', required=True)
    ap.add_argument('--title', required=True)
    ap.add_argument('--country', help='default: first part of --to (e.g. vietnam)')
    ap.add_argument('--kind', default='document',
                    choices=['document', 'dataset', 'api-response', 'page', 'probe-group', 'private'])
    ap.add_argument('--session', default='')
    ap.add_argument('--notes', default='')
    a = ap.parse_args()

    host = urlparse(a.url).netloc.lower()
    if any(b in host for b in BANNED):
        sys.exit(f'refused: {host} is a banned source')

    country = a.country or (a.to.split('/')[0] if a.to else '')
    if not country:
        sys.exit('--country is required with --no-keep')
    row = dict(retrieved=dt.date.today().isoformat(), session=a.session[:8], country=country,
               kind=a.kind, publisher=a.publisher, title=a.title, url=a.url, route=a.route or '',
               http_status='', bytes='', sha256='', local_path='', confidence='', notes=a.notes)

    if not a.no_keep:
        if not a.to:
            sys.exit('--to is required unless --no-keep')
        dest = os.path.join(RAW, a.to)
        if os.path.exists(dest):
            sys.exit(f'refused: raw/{a.to} exists; choose a new name')
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if a.register:
            shutil.copy2(a.register, dest)
            row['route'] = a.route or 'manual'
        else:
            route, status = fetch(a.url, dest)
            row['route'] = a.route or route
            row['http_status'] = status
        row['bytes'] = os.path.getsize(dest)
        row['sha256'] = sha256(dest)
        row['local_path'] = a.to
        if row['bytes'] == 0:
            row['notes'] = (row['notes'] + '; ' if row['notes'] else '') + '0 bytes - failed'

    new = not os.path.exists(REGISTER)
    with open(REGISTER, 'a', newline='') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)
    print(row['route'], row['http_status'], row['bytes'], row['local_path'] or '(not kept)')


if __name__ == '__main__':
    main()

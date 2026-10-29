"""
Download every EIA-860 annual generator release (1990 to the newest, incl. the early release) into
<repo>/data/eia860/ and unpack each into data/eia860/<year>/. Existing zips are skipped.

    python eia860_download.py            # fetch what is missing
    python eia860_download.py --check    # list what the page offers, fetch nothing

The monthly EIA-860M files live in data/eia860m/ (see eia860_history.py, --monthly).
"""
from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from fetch import download, fetch_text  # noqa: E402

BASE = "https://www.eia.gov/electricity/data/eia860/"
DATA = Path(__file__).resolve().parent.parent / "data" / "eia860"


def offered():
    status, html = fetch_text(BASE, timeout=60)
    out = {}
    for href in sorted(set(re.findall(r'href="\s*([^"]*\.zip)"', html))):
        name = href.rsplit("/", 1)[-1]
        m = re.match(r"eia860([ab]?)(\d{4})(ER)?\.zip$", name)
        if m:
            out[name] = BASE + href.strip()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    DATA.mkdir(parents=True, exist_ok=True)
    files = offered()
    print(f"{len(files)} annual files offered")
    if a.check:
        for n, u in files.items():
            print(n, u)
        return
    for name, url in files.items():
        z = DATA / name
        if not z.exists():
            try:
                download(url, str(z), timeout=300)
            except Exception as e:
                print("FAIL", name, str(e)[:100])
                continue
        dest = DATA / z.stem
        if not dest.exists() and zipfile.is_zipfile(z):
            with zipfile.ZipFile(z) as zf:
                zf.extractall(dest)
        print("ok", name, z.stat().st_size)


if __name__ == "__main__":
    main()

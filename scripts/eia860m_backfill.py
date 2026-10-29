"""
Download every EIA-860M monthly generator file still missing from data/eia860m/ (2015 to the newest).

    python eia860m_backfill.py

Tries archive/xls then xls for each month; months EIA does not publish are listed at the end.
"""
import datetime as dt
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from fetch import download  # noqa: E402

MONTHS = "january february march april may june july august september october november december".split()
OUT = Path(__file__).resolve().parent.parent / "data" / "eia860m"
OUT.mkdir(parents=True, exist_ok=True)
today = dt.date.today()
missing = []
for y in range(2015, today.year + 1):
    for i, m in enumerate(MONTHS):
        if (y, i + 1) > (today.year, today.month):
            break
        f = OUT / f"{m}_generator{y}.xlsx"
        if f.exists():
            continue
        for base in ("archive/xls", "xls"):
            try:
                download(f"https://www.eia.gov/electricity/data/eia860m/{base}/{m}_generator{y}.xlsx", str(f))
                if f.read_bytes()[:2] == b"PK":
                    print("ok", m, y, flush=True)
                    break
                f.unlink()
            except Exception:
                f.unlink(missing_ok=True)
        else:
            missing.append(f"{m} {y}")
print("not published or not found:", ", ".join(missing) or "none")

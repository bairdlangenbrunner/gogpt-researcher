"""
Status timeline of one EIA plant's generators across every local EIA-860 annual release and EIA-860M monthly file.

    python eia860_history.py 976                    # every generator at plant 976, status per release, changes marked
    python eia860_history.py 976 --gen 5 6          # only these generator IDs
    python eia860_history.py 976 --no-monthly       # annual releases only
    python eia860_history.py 976 --changes          # print only the releases where a status changed (and the first/last)

Reads data/eia860/eia860<year>/ (python eia860_download.py) and data/eia860m/<month>_generator<year>.xlsx.
Status codes: OP operating, SB standby/backup, OS out of service (cannot be brought back in the next year),
OA out of service (could be back within the next year), RE retired; monthly files put retired units on the Retired sheet.
The annual file is as of 31 December of its year; the monthly file is as of its month. A change is dated to the
window between the last release that shows the old value and the first that shows the new one.
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import sys
from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
MONTHS = "january february march april may june july august september october november december".split()
PLANT = ("Plant Code", "PLNTCODE", "Plant ID")
GEN = ("Generator ID", "GENID", "GENCODE")
STATUS = ("Status", "STATUS")
OPYR = ("Operating Year", "YEAR", "INITYEAR")
RETYR = ("Retirement Year", "RETIREYEAR", "RETYEAR")


def _frame(raw):
    for i in range(10):
        vals = [str(v).strip() for v in raw.iloc[i]]
        if any(v in PLANT for v in vals):
            df = raw.iloc[i + 1:].copy()
            df.columns = vals
            return df
    return None


def _col(df, names):
    return next((c for c in df.columns if c in names), None)


def _rows(path, plant, sheets_re):
    x = pd.ExcelFile(path)
    out = []
    for sh in x.sheet_names:
        if not re.search(sheets_re, sh) or sh.endswith("_PR"):
            continue
        df = _frame(x.parse(sh, header=None))
        if df is None:
            continue
        pc, gc = _col(df, PLANT), _col(df, GEN)
        if not (pc and gc):
            continue
        g = df[pd.to_numeric(df[pc], errors="coerce") == plant]
        sc, oc, rc = _col(df, STATUS), _col(df, OPYR), _col(df, RETYR)
        for _, r in g.iterrows():
            st = str(r[sc]).strip() if sc else ""
            m = re.match(r"\(([A-Z]{2})\)", st)
            st = m.group(1) if m else st
            if sh.startswith("Retired") and not st:
                st = "RE"
            out.append((re.sub(r"^GEN", "", str(r[gc]).strip()), st or "?", r[oc] if oc else "", r[rc] if rc else ""))
    return out


def releases(monthly=True):
    """(sortkey, label, path, sheet regex) oldest first."""
    rel = []
    for d in glob.glob(str(DATA / "eia860" / "eia860[0-9][0-9][0-9][0-9]")):
        y = int(d[-4:])
        pat = "Gen*" if y < 2011 else "*[Gg]enerator*"
        fs = [p for p in glob.glob(d + "/**/" + pat, recursive=True)
              if p.endswith((".xls", ".xlsx")) and not os.path.basename(p).startswith(("~", "Layout"))
              and "PCGen" not in p and "PRGen" not in p]
        if fs:
            rel.append(((y, 12.5), f"annual {y}", fs[0], "Operable|Operating|Retired|Existing|Gen"))
    if monthly:
        for p in glob.glob(str(DATA / "eia860m" / "*_generator*.xlsx")):
            m = re.match(r"([a-z]+)_generator(\d{4})", os.path.basename(p))
            rel.append(((int(m.group(2)), MONTHS.index(m.group(1)) + 1), f"{m.group(2)}-{MONTHS.index(m.group(1)) + 1:02d}", p, "Operating|Retired"))
    return sorted(rel)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plant", type=int)
    ap.add_argument("--gen", nargs="*")
    ap.add_argument("--no-monthly", action="store_true")
    ap.add_argument("--changes", action="store_true")
    a = ap.parse_args()
    last = {}
    for _, label, path, sheets in releases(not a.no_monthly):
        try:
            rows = _rows(path, a.plant, sheets)
        except Exception as e:
            print(label, "ERR", str(e)[:80], file=sys.stderr)
            continue
        seen = {}
        for gid, st, op, ret in rows:
            if a.gen and gid not in a.gen:
                continue
            seen[gid] = (st, op, ret)
        for gid in sorted(set(seen) | set(last)):
            now = seen.get(gid)
            prev = last.get(gid)
            changed = (now[0] if now else "absent") != (prev[0] if prev else None)
            if (not a.changes) or changed:
                st = now[0] if now else "absent"
                extra = f"  op {now[1]}  ret {now[2]}" if now else ""
                print(f"{label:12} gen {gid:>4}  {st}{extra}{'   <-- change' if changed and prev else ''}")
            if now:
                last[gid] = now
            else:
                last.pop(gid, None)


if __name__ == "__main__":
    main()

"""
Read an NMED Air Quality Bureau Coda table in full and save it as CSV, with no Coda sign-in.

The three tables (Current Permitting Actions Under Review, AQB NSR Issued Report, AQB Facilities Lat
Long Report) are published Coda docs. Coda draws only the rows on screen and its API needs a token,
so this opens the page in the installed Chrome through Playwright, uses a very wide window so every
column is drawn, scrolls the table's own scroll box and keeps each row by its data-row-id until the
scrolling stops. Built 2026-11-19; it read 276 pending rows and 9,764 facilities. The issued table
was empty at the source that day.

The CSV goes where harvest_permits.py reads it, scopes/us-nm/work/permits/coda/<name>.csv; rerun
the harvester afterwards.

Usage (from the repo root):
    python scopes/us-nm/coda_browser.py <coda table address> pending
    python scopes/us-nm/coda_browser.py <coda table address> facilities
"""
import csv
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent / "work" / "permits" / "coda"

ROWS_JS = '''() => {
  const res = [];
  document.querySelectorAll('[data-coda-ui-id="row"]').forEach(r => {
    const cells = {};
    r.querySelectorAll('[role=gridcell]').forEach(c => {
      cells[c.getAttribute('aria-colindex')] = c.innerText.replace(/\\u200b/g, '').trim();
    });
    res.push({id: r.getAttribute('data-row-id'), idx: +r.getAttribute('aria-rowindex'), cells});
  });
  const hd = [...document.querySelectorAll('[data-coda-ui-id="grid-column-header-container"] [role=columnheader]')]
    .map(h => [h.getAttribute('aria-colindex'), h.innerText.trim()]);
  return {res, hd};
}'''

SCROLL_JS = '''(d) => {
  let e = document.querySelector('[data-coda-ui-id="row"]');
  while (e) {
    if (e.scrollHeight > e.clientHeight + 5 && ['auto', 'scroll'].includes(getComputedStyle(e).overflowY)) break;
    e = e.parentElement;
  }
  if (!e) return null;
  const before = e.scrollTop;
  e.scrollTop += d;
  return [before, e.scrollTop];
}'''


def read_table(url):
    rows, hd, stall = {}, {}, 0
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 4500, "height": 1000})
        pg.goto(url, wait_until="networkidle", timeout=90000)
        pg.wait_for_selector("[data-coda-ui-id=row]", timeout=60000)
        pg.wait_for_timeout(3000)
        for _ in range(3000):
            d = pg.evaluate(ROWS_JS)
            hd.update({k: v for k, v in d["hd"] if k and v})
            n = len(rows)
            for r in d["res"]:
                rows.setdefault(r["id"], r)["cells"].update(r["cells"])
            pos = pg.evaluate(SCROLL_JS, 500)
            pg.wait_for_timeout(250)
            if pos is None:
                break
            stall = stall + 1 if len(rows) == n and pos[0] == pos[1] else 0
            if stall >= 4:
                break
        b.close()
    return rows, hd


def main():
    url, name = sys.argv[1], sys.argv[2]
    rows, hd = read_table(url)
    cols = sorted(hd, key=int)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.csv"
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow([hd[c] for c in cols])
        for r in sorted(rows.values(), key=lambda r: r["idx"]):
            w.writerow([r["cells"].get(c, "") for c in cols])
    print(f"{len(rows)} rows, {len(cols)} columns -> {path}")


if __name__ == "__main__":
    main()

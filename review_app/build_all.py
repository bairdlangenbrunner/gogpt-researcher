"""
Rebuild every review page listed in artifacts.json from the one interface in web/.

    python review_app/build_all.py [--only NAME]

Writes one stamped html per page into work/ and prints a table of name, reviewer, url and file,
so each file can be published to its url (Artifact tool, work profile, capabilities carried
forward). Run it after ANY change under review_app/web/ or to build_static.py, so every page
keeps the same interface. Add a page by adding an entry to artifacts.json.
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for p in (ROOT / "scripts", HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import build_static  # noqa: E402
import paths  # noqa: E402
import store  # noqa: E402

EXPORT = ROOT / "scripts" / "gem_export_gogpt_scoped.csv"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--only", help="build just this page name")
    args = ap.parse_args(argv)
    pages = json.loads((HERE / "artifacts.json").read_text(encoding="utf-8"))["pages"]
    if args.only:
        pages = [p for p in pages if p["name"] == args.only]
        if not pages:
            raise SystemExit(f"no page named {args.only} in artifacts.json")
    stamp = datetime.now(store.ET).strftime("%Y%m%d_%H%M")
    rows = []
    for pg in pages:
        dirs = [ROOT / d for d in pg["dirs"]]
        html, data = build_static.build(dirs, pg["reviewer"], str(EXPORT) if EXPORT.exists() else None,
                                     pg.get("title"))
        out = paths.work_dir() / f"gogpt_review_{pg['name']}_{stamp}_ET.html"
        out.write_text(html, encoding="utf-8")
        rows.append((pg["name"], pg["reviewer"], pg["url"], out))
    for name, rev, url, out in rows:
        print(f"{name}\t{rev}\t{url}\t{out}")


if __name__ == "__main__":
    main()

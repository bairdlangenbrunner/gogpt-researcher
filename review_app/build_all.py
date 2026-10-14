"""
Rebuild every review page listed in artifacts.json from the shared interface in the sibling
gem-review-app repo (review_core/web plus trackers/gogpt/web), and say which live pages are stale.

    python review_app/build_all.py --check               # fresh / stale (why) / unmarked per page; exit 1 if any is not fresh
    python review_app/build_all.py [--only NAME] [--all] # build the stale or unmarked pages (--all: every page)
    python review_app/build_all.py --mark-published NAME # after publishing NAME's file to its url
    python review_app/build_all.py --hook EVENT          # Claude Code hook (SessionStart, UserPromptSubmit, Stop)

Writes one stamped html per page into work/ and prints a table of name, reviewer, url and file,
so each file can be published to its url (Artifact tool, work profile, capabilities carried
forward), then --mark-published NAME records what that page was built from. Run --check after ANY
change in gem-review-app or in a batch's staged files. Add a page by adding an entry to artifacts.json.
Logic: ../gem-review-app/review_core/pages.py; plan: ../gem-review-app/docs/refresh.md.
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
from review_core import hooks, pages  # noqa: E402

EXPORT = ROOT / "scripts" / "gem_export_gogpt_scoped.csv"
REGISTRY = HERE / "artifacts.json"
LAST_BUILD = ROOT / pages.LAST_BUILD


def adapter():
    return pages.PageAdapter(
        root=ROOT,
        resolve_dirs=lambda e: [ROOT / d for d in e.get("dirs", [])],
        staged_files=lambda d: sorted(p.name for p in Path(d).glob("staged_*.json")),
        decision_files=("review_log.jsonl",),
        extra_inputs=lambda e: {"export": pages.sha_file(EXPORT)},
        builder_files=("review_app/review_data.py", "review_app/build_static.py", "review_app/store.py"))


def reports():
    return pages.check(pages.load_entries(REGISTRY), adapter(), store.CONFIG)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--only", help="build just this page name")
    ap.add_argument("--all", action="store_true", help="build every page, not just the stale or unmarked ones")
    ap.add_argument("--check", action="store_true", help="report which pages are stale; exit 1 if any is not fresh")
    ap.add_argument("--mark-published", metavar="NAME", help="record the last build of NAME as published")
    ap.add_argument("--hook", metavar="EVENT", help="Claude Code hook mode")
    args = ap.parse_args(argv)
    if args.hook:
        out = hooks.hook(args.hook, sys.stdin.read(), reports(), paths.work_dir())
        if out:
            print(out)
        return
    if args.mark_published:
        try:
            pub = pages.mark_published(REGISTRY, args.mark_published, LAST_BUILD, adapter(), store.CONFIG)
        except (pages.PublishError, KeyError) as e:
            raise SystemExit(f"not marked: {e}")
        print(f"{args.mark_published} marked published ({pub['profile']} profile, built {pub['built']})")
        return
    if args.check:
        bad = False
        for r in reports():
            print(f"{r['name']}\t{r['status']}" + (f"\t{'; '.join(r['reasons'])}" if r["reasons"] else ""))
            bad = bad or r["status"] != "fresh"
        sys.exit(1 if bad else 0)
    entries = pages.load_entries(REGISTRY)
    if args.only:
        entries = [p for p in entries if p["name"] == args.only]
        if not entries:
            raise SystemExit(f"no page named {args.only} in artifacts.json")
    elif not args.all:
        todo = {r["name"] for r in reports() if r["status"] != "fresh"}
        entries = [p for p in entries if p["name"] in todo]
        if not entries:
            print("every page is fresh; nothing to build (--all to rebuild anyway)")
            return
    stamp = datetime.now(store.ET).strftime("%Y%m%d_%H%M")
    rows = []
    for pg in entries:
        dirs = [ROOT / d for d in pg["dirs"]]
        fp, parts = pages.fingerprint(pg, adapter(), store.CONFIG)
        html, data = build_static.build(dirs, pg["reviewer"], str(EXPORT) if EXPORT.exists() else None,
                                     pg.get("title"))
        out = paths.work_dir() / f"gogpt_review_{pg['name']}_{stamp}_ET.html"
        out.write_text(html, encoding="utf-8")
        pages.record_build(LAST_BUILD, pg["name"], fp, parts, data.get("built") or datetime.now(store.ET).isoformat(timespec="seconds"), out)
        rows.append((pg["name"], pg["reviewer"], pg["url"], out))
    for name, rev, url, out in rows:
        print(f"{name}\t{rev}\t{url}\t{out}")


if __name__ == "__main__":
    main()

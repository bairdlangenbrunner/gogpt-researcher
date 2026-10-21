"""
Rebuild every review page listed in artifacts.json from the shared interface in the sibling
gem-review-app repo (review_core/web plus trackers/gogpt/web), and say which live pages are stale.

    python review_app/build_all.py --check               # fresh / stale (why) / unmarked per page; exit 1 if any is not fresh
    python review_app/build_all.py [--only NAME] [--all] [--no-pull] # pull the store, then build the stale or unmarked pages (--all: every page)
    python review_app/build_all.py --list                # the page table: name, reviewer, url, published at
    python review_app/build_all.py --mark-published NAME # after publishing NAME's file to its url
    python review_app/build_all.py --hook EVENT          # Claude Code hook (SessionStart, UserPromptSubmit, Stop): one JSON object

Writes one stamped html per page into work/ and prints a table of name, reviewer, url and file,
so each file can be published to its url (Artifact tool, work profile, capabilities carried
forward), then --mark-published NAME records what that page was built from. Run --check after ANY
change in gem-review-app or in a batch's staged files. Add a page by adding an entry to artifacts.json.

A build pulls the decision store before the stale check, because pulled calls change what a page is built from; a failed pull warns and the build goes on from the local logs. The command line itself is review_core.pages.cli and the hook output is the JSON contract in review_core/hooks.py. The check and the hook keep work/.review_pages_cache.json (pages.FileCache), so the 34 MB export and other inputs whose size and modification time did not change are not read again.

Logic: ../gem-review-app/review_core/pages.py; plan: ../gem-review-app/docs/refresh.md.
"""
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
from review_core import pages  # noqa: E402

EXPORT = ROOT / "scripts" / "gem_export_gogpt_scoped.csv"
NO_URL = "(not yet published)"
SOP_POINTERS = ROOT / "docs" / "reference" / "sop_pointers.md"
_MEMO = pages.FileCache()        # for this process, when no saved cache is passed in
REGISTRY = HERE / "artifacts.json"
LAST_BUILD = ROOT / pages.LAST_BUILD


def sha_cached(path, cache=None):
    """pages.sha_file, remembered by path, size and modification time (in `cache`, else for this process): the export is 34 MB and the hook asks once per page."""
    return pages.sha_file(path, cache or _MEMO)


def adapter(cache=None):
    return pages.PageAdapter(
        root=ROOT,
        resolve_dirs=lambda e: [ROOT / d for d in e.get("dirs", [])],
        staged_files=lambda d: sorted(p.name for p in Path(d).glob("staged_*.json")),
        decision_files=("review_log.jsonl",),
        extra_inputs=lambda e: {"export": sha_cached(EXPORT, cache), "sop_pointers": sha_cached(SOP_POINTERS, cache)},
        builder_files=("review_app/review_data.py", "review_app/build_static.py", "review_app/store.py",
                       "review_app/checklist.py", "scripts/build_review_package.py"),
        cache=cache)


def reports():
    return pages.check(pages.load_entries(REGISTRY), adapter(), store.CONFIG)


def main(argv=None):
    state = {"stamp": datetime.now(store.ET).strftime("%Y%m%d_%H%M")}

    def pull(args):
        state["cfg"] = build_static.pull.config()
        build_static.pull_first(state["cfg"], args.no_pull)

    def build_page(pg, args):
        dirs = [ROOT / d for d in pg.get("dirs", [])]
        html, data = build_static.build(dirs, pg.get("reviewer", ""), str(EXPORT) if EXPORT.exists() else None,
                                        pg.get("title"), cfg=state.get("cfg"))
        out = paths.work_dir() / f"gogpt_review_{pg['name']}_{state['stamp']}_ET.html"
        out.write_text(html, encoding="utf-8")
        return out, data.get("built") or datetime.now(store.ET).isoformat(timespec="seconds")

    cache = pages.FileCache(paths.work_dir() / pages.CACHE)
    return pages.cli(adapter(cache), REGISTRY, build_page, argv, config=store.CONFIG, last_build=LAST_BUILD,
                     work=paths.work_dir(), description=__doc__.split("\n\n")[0], pull=pull,
                     columns=(("reviewer", lambda p: p.get("reviewer", "")), ("url", lambda p: p.get("url") or NO_URL)))


if __name__ == "__main__":
    main()

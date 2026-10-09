"""
Build the review app as ONE html file to send to a colleague who does not run the repo.

    python review_app/build_static.py --scope us-md --scope us-ny --reviewer "Amalia Llano"
        [--export-csv PATH] [--out PATH]

The page is built by the shared builder in ../gem-review-app (review_core/build_static.py): the shared page and the GOGPT extension, with the dataset review_data.py builds from the staging dirs (the calls already in each review_log.jsonl laid over it) gzipped into one block, and the browser-side store (review_core/web/static_store.js). Published as a claude.ai artifact (the normal way) the page saves every call to the artifact's database; opened from disk the calls stay in the browser and "download decisions" hands them over as a file. Either way review_app/import_log.py brings them into the decision ledger (the store spreadsheet first, then the staging dirs).

Default output: work/gogpt_review_<scopes>_<YYYYMMDD>_<HHMM>_ET.html (work/ is not tracked). Every build gets a fresh stamp; an existing file is never overwritten.
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for p in (ROOT / "scripts", HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import paths  # noqa: E402
import pull  # noqa: E402
import review_data  # noqa: E402
import store  # noqa: E402
from review_core import build_static as core  # noqa: E402


def ledger_url(cfg=None):
    """The decision store spreadsheet's link, for the page's "push to log" tip ('' when none is configured)."""
    cfg = pull.config() if cfg is None else cfg
    sid = (cfg or {}).get("store_sheet_id") or ""
    return f"https://docs.google.com/spreadsheets/d/{sid}/edit" if sid else ""


def render(data, reviewer, title=None, cfg=None):
    """The page as one html string, from the shared builder with the GOGPT config."""
    return core.render(data, reviewer, store.CONFIG, title=title, ledger_url=ledger_url(cfg))


def build(dirs, reviewer, export_csv=None, title=None, cfg=None):
    data = review_data.build(dirs, export_csv)
    store.overlay(data, {label: Path(d) for label, d in zip(data["dirs"], dirs)})
    return render(data, store.initials(reviewer), title, cfg), data


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--scope", action="append", default=[], help="batch scope, e.g. us-md (repeatable)")
    ap.add_argument("--dirs", nargs="*", default=[], help="explicit staging dirs")
    ap.add_argument("--reviewer", required=True, help="who will review; recorded by initials")
    ap.add_argument("--export-csv", default=None, help="scoped export csv for current Data Source cells")
    ap.add_argument("--out", default=None, help="output html (default work/gogpt_review_<scopes>_<stamp>_ET.html)")
    ap.add_argument("--config", default=None, help="store config (default review_app/google.json): the log link on the page")
    args = ap.parse_args(argv)
    dirs = [ROOT / "batches" / s / "staging" for s in args.scope] + [Path(d) for d in args.dirs]
    if not dirs:
        raise SystemExit("name at least one --scope or --dirs")
    html, data = build(dirs, args.reviewer, args.export_csv, cfg=pull.config(args.config))
    if args.out:
        out = Path(args.out)
    else:
        stamp = datetime.now(store.ET).strftime("%Y%m%d_%H%M")
        slug = "+".join(Path(d).parent.name if Path(d).name == "staging" else Path(d).name for d in dirs)
        out = paths.work_dir() / f"gogpt_review_{slug}_{stamp}_ET.html"
    if out.exists():
        raise SystemExit(f"refusing to overwrite {out}; pass a new --out or wait a minute for a fresh stamp")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    nl = sum(len(p["lines"]) for p in data["plants"])
    ni = sum(len(p["items"]) for p in data["plants"])
    print(f"wrote {out} ({out.stat().st_size // 1024} KB: {len(data['plants'])} plants, {nl} changes, "
          f"{ni} items, reviewer {store.initials(args.reviewer)})")
    print("publish it as a claude.ai artifact from the work profile (review_app/README.md), or send the file; "
          "the calls come back through: python review_app/import_log.py <file> --reviewer EMAIL")
    return out


if __name__ == "__main__":
    main()

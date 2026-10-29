"""
Build the review app as ONE html file to send to a colleague who does not run the repo.

    python review_app/build_static.py --scope us-md --scope us-ny [--discovery] --reviewer "Amalia Llano"
        [--no-pull] [--export-csv PATH] [--out PATH] [--artifact URL]

It first pulls the decision store into the local logs (--no-pull skips that; a failed pull warns and the build goes on).

The page is built by the shared builder in ../gem-review-app (review_core/build_static.py): the shared page and the GOGPT extension, with the dataset review_data.py builds from the staging dirs (the calls already in each review_log.jsonl laid over it) gzipped into one block, and the browser-side store (review_core/web/static_store.js). Published as a claude.ai artifact (the normal way) the page saves every call to the artifact's database; opened from disk the calls stay in the browser and "download decisions" hands them over as a file. Either way review_app/import_log.py brings them into the decision ledger (the store spreadsheet first, then the staging dirs).

Default output: work/gogpt_review_<scopes>_<YYYYMMDD>_<HHMM>_ET.html (work/ is not tracked). Every build gets a fresh stamp; an existing file is never overwritten.

Map pictures: a location line's saved map render is an artifact asset (review_data.map_render copies it to work/review_assets/). The build fills each picture's url from review_app/assets.json for the page at --artifact (build_all.py passes the registry url) and writes <page>.assets.json beside the page: every picture the page shows and the ones that page has not uploaded yet (an image with no url shows its caption and "image not uploaded"). Upload those with the Artifact tool and record them with review_app/map_assets.py, then rebuild.
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

import paths  # noqa: E402
import pull  # noqa: E402
import review_data  # noqa: E402
import store  # noqa: E402
from review_core import assets as core_assets  # noqa: E402
from review_core import build_static as core  # noqa: E402

ASSETS = HERE / "assets.json"        # the map pictures uploaded to each page (review_core/assets.py; map_assets.py writes it)


def ledger_url(cfg=None):
    """The decision store spreadsheet's link, for the page's "push to log" tip ('' when none is configured)."""
    cfg = pull.config() if cfg is None else cfg
    sid = (cfg or {}).get("store_sheet_id") or ""
    return f"https://docs.google.com/spreadsheets/d/{sid}/edit" if sid else ""


def pull_first(cfg, skip=False, puller=None):
    """Bring the decision store's calls into the local logs before a build, so the page is not built behind the store.
    A failed pull (no network, expired login) warns and the build goes on from the logs as they are. -> True when it pulled."""
    if skip:
        return False
    try:
        res = (puller or pull.pull)(cfg)
    except pull.GwsError as e:
        print(f"warning: pull failed, building from the local logs as they are: {e}", file=sys.stderr)
        return False
    print(pull.report(res), file=sys.stderr)
    return True


def render(data, reviewer, title=None, cfg=None):
    """The page as one html string, from the shared builder with the GOGPT config."""
    return core.render(data, reviewer, store.CONFIG, title=title, ledger_url=ledger_url(cfg), root=store.ROOT)


def build(dirs, reviewer, export_csv=None, title=None, cfg=None, artifact=""):
    """-> (html, data, pictures). pictures is {"artifact", "shown", "missing"}: the map pictures the page shows (asset names)
    and the ones page `artifact` has not uploaded yet; the urls of the uploaded ones are filled into the data from ASSETS."""
    data = review_data.build(dirs, export_csv)
    store.overlay(data, {label: Path(d) for label, d in zip(data["dirs"], dirs)})
    shown = list(dict.fromkeys(i["asset"] for i in core_assets.images_in(data)))
    missing = core_assets.fill_urls(data, core_assets.load_manifest(ASSETS), artifact) if shown else []
    return render(data, store.initials(reviewer), title, cfg), data, {"artifact": artifact, "shown": shown, "missing": missing}


def write_pictures(path, pictures):
    """Write the picture list of a build ({artifact, shown, missing} asset names) to `path`; build_all.py reads `shown` for the stale check."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(pictures, indent=1) + "\n", encoding="utf-8")
    return path


def pictures_note(pictures):
    """One line on the build's map pictures, or '' when the page shows none."""
    if not pictures["shown"]:
        return ""
    return (f"{len(pictures['shown'])} map pictures, {len(pictures['missing'])} not uploaded for "
            f"{pictures['artifact'] or 'any page (no --artifact)'}; list: build_all.py --assets <page>")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--scope", action="append", default=[], help="batch scope, e.g. us-md (repeatable)")
    ap.add_argument("--discovery", action="store_true", help="with --scope, also include batches/<scope>/staging-discovery")
    ap.add_argument("--no-pull", action="store_true", help="skip the pull from the decision store; build from the local logs as they are")
    ap.add_argument("--dirs", nargs="*", default=[], help="explicit staging dirs")
    ap.add_argument("--reviewer", required=True, help="who will review; recorded by initials")
    ap.add_argument("--export-csv", default=None, help="scoped export csv for current Data Source cells")
    ap.add_argument("--out", default=None, help="output html (default work/gogpt_review_<scopes>_<stamp>_ET.html)")
    ap.add_argument("--config", default=None, help="store config (default review_app/google.json): the log link on the page")
    ap.add_argument("--artifact", default="", help="the artifact url the page goes to: fills the map pictures' urls from review_app/assets.json")
    args = ap.parse_args(argv)
    dirs = [ROOT / "batches" / s / "staging" for s in args.scope]
    if args.discovery:
        dirs += [ROOT / "batches" / s / "staging-discovery" for s in args.scope]
    dirs += [Path(d) for d in args.dirs]
    if not dirs:
        raise SystemExit("name at least one --scope or --dirs")
    cfg = pull.config(args.config)
    pull_first(cfg, args.no_pull)
    html, data, pictures = build(dirs, args.reviewer, args.export_csv, cfg=cfg, artifact=args.artifact)
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
    write_pictures(out.with_name(out.stem + ".assets.json"), pictures)
    nl = sum(len(p["lines"]) for p in data["plants"])
    ni = sum(len(p["items"]) for p in data["plants"])
    print(f"wrote {out} ({out.stat().st_size // 1024} KB: {len(data['plants'])} plants, {nl} changes, "
          f"{ni} items, reviewer {store.initials(args.reviewer)})")
    if pictures_note(pictures):
        print("  " + pictures_note(pictures))
    print("publish it as a claude.ai artifact from the work profile (review_app/README.md), or send the file; "
          "the calls come back through: python review_app/import_log.py <file> --reviewer EMAIL")
    return out


if __name__ == "__main__":
    main()

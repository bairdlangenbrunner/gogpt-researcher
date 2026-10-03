"""
Build the review app as ONE html file to send to a colleague who does not run the repo.

    python review_app/build_static.py --scope us-md --scope us-ny --reviewer "Amalia Llano"
        [--export-csv PATH] [--out PATH]

The file holds the page (index.html, style.css, app.js), the dataset review_data.py builds
from the staging dirs (with the calls already in each review_log.jsonl laid over it) and the
browser-side store (web/static_store.js). The reviewer opens it from disk; nothing is fetched.
Their calls go to a log in their browser, and "download decisions" gives them a
review_log.jsonl to send back; review_app/import_log.py appends it to the staging dirs.

Default output: work/gogpt_review_<scopes>_<YYYYMMDD>_<HHMM>_ET.html (work/ is not tracked).
Every build gets a fresh stamp; an existing file is never overwritten.
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
WEB = HERE / "web"
for p in (ROOT / "scripts", HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import paths  # noqa: E402
import review_data  # noqa: E402
import store  # noqa: E402


def render(data, reviewer):
    """The page as one html string: css inlined, the dataset and reviewer embedded, then the
    static store and the app. `</script>` inside the JSON is escaped so it cannot end the tag."""
    html = (WEB / "index.html").read_text(encoding="utf-8")
    css = (WEB / "style.css").read_text(encoding="utf-8")
    static_js = (WEB / "static_store.js").read_text(encoding="utf-8")
    app_js = (WEB / "app.js").read_text(encoding="utf-8")
    cfg = json.dumps({"reviewer": reviewer, "data": data}, ensure_ascii=False).replace("</", "<\\/")
    html = html.replace('<link rel="stylesheet" href="style.css">', "<style>\n" + css + "\n</style>")
    html = html.replace('<script src="app.js"></script>',
                        "<script>window.REVIEW_STATIC = " + cfg + ";</script>\n"
                        "<script>\n" + static_js + "\n</script>\n"
                        "<script>\n" + app_js + "\n</script>")
    if "app.js" in html.split("<script>")[0]:
        raise SystemExit("index.html changed shape: the script tag was not replaced")
    return html


def build(dirs, reviewer, export_csv=None):
    data = review_data.build(dirs, export_csv)
    store.overlay(data, {label: Path(d) for label, d in zip(data["dirs"], dirs)})
    return render(data, store.initials(reviewer)), data


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--scope", action="append", default=[], help="batch scope, e.g. us-md (repeatable)")
    ap.add_argument("--dirs", nargs="*", default=[], help="explicit staging dirs")
    ap.add_argument("--reviewer", required=True, help="who will review; recorded by initials")
    ap.add_argument("--export-csv", default=None, help="scoped export csv for current Data Source cells")
    ap.add_argument("--out", default=None, help="output html (default work/gogpt_review_<scopes>_<stamp>_ET.html)")
    args = ap.parse_args(argv)
    dirs = [ROOT / "batches" / s / "staging" for s in args.scope] + [Path(d) for d in args.dirs]
    if not dirs:
        raise SystemExit("name at least one --scope or --dirs")
    html, data = build(dirs, args.reviewer, args.export_csv)
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
    print("send that one file; the reviewer opens it in a browser and sends back the downloaded "
          "review_log .jsonl, then: python review_app/import_log.py <file>")
    return out


if __name__ == "__main__":
    main()

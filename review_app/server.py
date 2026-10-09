"""
Local review server for staged GOGPT research: the shared server in ../gem-review-app (review_core/server.py) bound to the GOGPT store and config.

    python review_app/server.py --scope us-md --scope us-ny [--port 8767] [--no-open] [--no-build]
    python review_app/server.py --dirs batches/us-md/staging ... [--data PATH] [--reviewer NAME]

It binds 127.0.0.1 and refuses anything but loopback (the data is unreleased). Without --no-build it first runs review_data.main for the scopes given into --data (default work/review_data.json); with --no-build it serves that file as it is.

    GET  /                 the shared page, titled "GOGPT reviewer" (core files under /core/, the GOGPT extension under /tracker/)
    GET  /api/data         the dataset JSON with every staging dir's decisions laid over it
    GET  /api/whoami       {"reviewer": ..., "caps": {"decide": true}, "store": true|false}
    GET  /api/decisions?dir=<label>   that staging dir's latest-per-key records
    POST /api/decide       [{key, decision, suggested_value?, reference?, note?} | {key, undo: true}, ...] -> {"saved": [record, ...]}
    POST /api/item         [{key, call, reference?, note?} | {key, undo: true}, ...] -> {"saved": [...]}; the call must be in store.ITEM_CALLS[kind]
    POST /api/flag         [{key, on, note?} | {pid, dir, on, note?}, ...] -> {"saved": [...]}; ask-the-PM flags on a line, item or whole plant

Every decision goes to the Google decision store first (review_app/ledger.py: the `log` tab of the spreadsheet in review_app/google.json, under the writer's address) and then to the two decision sidecars inside the staging dir. A store that cannot be written refuses the decision (502, nothing recorded anywhere). --no-store (tests, dev) writes the sidecars alone and says so. Nothing else is ever written: not the GEM database, not the staged_*.json files, not the deliverables; accepted edits reach GEM only through the actions workbook that scripts/build_review_package.py --decisions builds and the reviewer applies by hand.
"""
import argparse
import json
import subprocess
import sys
import webbrowser
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for p in (ROOT / "scripts", HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import ledger  # noqa: E402
import paths  # noqa: E402
import pull  # noqa: E402
import review_data  # noqa: E402
import store  # noqa: E402
from review_core import server as core  # noqa: E402

CAPS = dict(store.CONFIG.caps)
ensure_loopback = core.ensure_loopback
make_handler = core.make_handler
_ledger = ledger      # App takes a `ledger` argument, which hides the module inside __init__


class App(core.App):
    """Server state: the dataset and who is reviewing."""

    def __init__(self, data_path, reviewer, root=None, ledger=None):
        super().__init__(data_path, reviewer, store, root=root or ROOT, ledger=ledger,
                         scope_of=_ledger.scope_of, store_errors=(_ledger.StoreError,))

    def flag(self, records):
        return self.record("flag", records)



def make_server(app, host="127.0.0.1", port=8767):
    return core.make_server(app, host, port, server_version="gogpt_review_app/1")


def git_user():
    try:
        return subprocess.run(["git", "config", "user.name"], capture_output=True, text=True,
                              cwd=ROOT).stdout.strip() or "reviewer"
    except OSError:
        return "reviewer"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--scope", action="append", default=[], help="batch scope, e.g. us-md (repeatable)")
    ap.add_argument("--dirs", nargs="*", default=[], help="explicit staging dirs")
    ap.add_argument("--export-csv", default=None, help="scoped export csv (default: the batch's own)")
    ap.add_argument("--data", default=None, help="dataset path (default work/review_data.json)")
    ap.add_argument("--reviewer", default=None, help="default: git config user.name; recorded as initials")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8767)
    ap.add_argument("--no-open", action="store_true", help="do not open the browser")
    ap.add_argument("--no-build", action="store_true", help="serve --data as it is; do not rebuild")
    ap.add_argument("--reviewer-email", default=None,
                    help="the address written on this reviewer's store rows (default: the gws-gem-write account's)")
    ap.add_argument("--no-store", action="store_true",
                    help="dev/tests only: write the staging-dir sidecars alone, skipping the decision store")
    args = ap.parse_args(argv)
    try:
        ensure_loopback(args.host)
    except ValueError as e:
        raise SystemExit(str(e))
    data_path = Path(args.data) if args.data else paths.work_dir() / "review_data.json"
    if not args.no_build:
        if not (args.scope or args.dirs):
            raise SystemExit("name at least one --scope or --dirs (or pass --no-build with --data)")
        build = [x for s in args.scope for x in ("--scope", s)] + ["--out", str(data_path)]
        if args.dirs:
            build += ["--dirs", *args.dirs]
        if args.export_csv:
            build += ["--export-csv", args.export_csv]
        review_data.main(build)
    elif not data_path.exists():
        raise SystemExit(f"{data_path} not found: run without --no-build, or pass --data")
    led = None
    if args.no_store:
        print("review app: --no-store: decisions go to the staging-dir sidecars ONLY and will not be in the "
              "decision store (dev/tests only)", file=sys.stderr)
    else:
        cfg = pull.config()
        if not cfg.get("store_sheet_id"):
            raise SystemExit("no decision store configured (review_app/google.json: store_sheet_id); "
                             "pass --no-store only for dev/tests")
        email = args.reviewer_email or ledger.whoami()
        if not email:
            raise SystemExit("cannot read the store account's address (gws-gem-write auth?): pass --reviewer-email, "
                             "or --no-store for dev/tests")
        data0 = json.loads(data_path.read_text(encoding="utf-8"))
        led = ledger.Ledger(cfg["store_sheet_id"], *ledger.scope_of(data0), "local", reviewer_email=email)
    app = App(data_path, args.reviewer or git_user(), ledger=led)
    httpd = make_server(app, args.host, args.port)
    url = f"http://{args.host}:{httpd.server_address[1]}/"
    where = (f"the decision store (log tab, as {led.reviewer_email}) and then each staging dir's review_log.jsonl"
             if led else "each staging dir's review_log.jsonl ONLY (--no-store)")
    print(f"review app: {url}  (reviewer: {app.reviewer}; decisions write to {where}; "
          f"the GEM database is never touched; Ctrl-C to stop)", file=sys.stderr)
    if not args.no_open:
        webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()

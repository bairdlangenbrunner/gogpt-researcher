"""
Local review server for staged GOGPT research (the backend behind review_app/web/).

    python review_app/server.py --scope us-md --scope us-ny [--port 8767] [--no-open] [--no-build]
    python review_app/server.py --dirs batches/us-md/staging ... [--data PATH] [--reviewer NAME]

Standard library only; binds 127.0.0.1 and refuses anything but loopback (the data is
unreleased). Without --no-build it first runs review_data.main for the scopes given into
--data (default work/review_data.json); with --no-build it serves that file as it is.

    GET  /                 static front end (review_app/web/)
    GET  /api/data         the dataset JSON with every staging dir's decisions laid over it
    GET  /api/whoami       {"reviewer": ..., "caps": {"decide": true}}
    GET  /api/decisions?dir=<label>   that staging dir's latest-per-key records
    POST /api/decide       [{key, decision, suggested_value?, note?} | {key, undo: true}, ...]
                           -> {"saved": [record, ...]}; reviewer and ts are stamped here, never
                           taken from the client. Appends to <dir>/review_log.jsonl and
                           regenerates <dir>/review_decisions.json. 400 = refused, nothing written.
    POST /api/item         [{key, call, note?} | {key, undo: true}, ...] -> {"saved": [...]};
                           the call must be in store.ITEM_CALLS[kind]; same sidecars.

The only things this server ever writes are the two decision sidecars inside the staging dirs
named by the dataset. It never touches the GEM database, the staged_*.json files or the
deliverables; accepted edits reach GEM only through the actions workbook that
scripts/build_review_package.py --decisions builds and the reviewer applies by hand.
"""
import argparse
import gzip
import ipaddress
import json
import mimetypes
import subprocess
import sys
import threading
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
WEB = HERE / "web"
for p in (ROOT / "scripts", HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import paths  # noqa: E402
import review_data  # noqa: E402
import store  # noqa: E402

CAPS = {"decide": True}


def ensure_loopback(host):
    """Raise ValueError unless `host` is a loopback address."""
    if host == "localhost":
        return
    try:
        if ipaddress.ip_address(host).is_loopback:
            return
    except ValueError:
        pass
    raise ValueError(f"refusing to bind {host!r}: the review server is loopback-only")


class App:
    """Server state: the dataset and who is reviewing."""

    def __init__(self, data_path, reviewer, root=None):
        self.data_path = Path(data_path)
        self.reviewer = store.initials(reviewer)     # people are recorded by initials
        self.root = Path(root) if root else ROOT
        self.lock = threading.Lock()
        self.load()

    def load(self):
        raw = self.data_path.read_bytes()
        self.data = json.loads(raw.decode("utf-8"))   # refuse to serve a file that is not JSON

    def dirs(self):
        return store.dir_paths(self.data, self.root)

    def current(self):
        """(raw, gz) of the dataset with every staging dir's sidecars laid over it right now."""
        with self.lock:
            store.overlay(self.data, self.dirs())
            raw = json.dumps(self.data, ensure_ascii=False).encode("utf-8")
        return raw, gzip.compress(raw, 6)

    def decide(self, records):
        with self.lock:
            return store.decide(records, self.data, self.reviewer, self.dirs())

    def item(self, records):
        with self.lock:
            return store.record_items(records, self.data, self.reviewer, self.dirs())

    def decisions(self, label):
        d = self.dirs().get(label)
        if d is None:
            return None
        return store.read_decisions(d)

    def whoami(self):
        return {"reviewer": self.reviewer, "caps": dict(CAPS)}


def make_handler(app):
    class Handler(BaseHTTPRequestHandler):
        server_version = "gogpt_review_app/1"

        def log_message(self, fmt, *args):
            sys.stderr.write("%s %s\n" % (self.command, self.path))

        def _host_ok(self):
            # DNS-rebinding guard: only answer requests addressed to a loopback host
            host = (self.headers.get("Host") or "").rsplit(":", 1)[0].strip("[]")
            try:
                ensure_loopback(host)
                return True
            except ValueError:
                return False

        def _send(self, body, ctype, status=HTTPStatus.OK, extra=None):
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            for k, v in (extra or {}).items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(body)

        def _json(self, obj, status=HTTPStatus.OK):
            self._send(json.dumps(obj, ensure_ascii=False).encode("utf-8"),
                       "application/json; charset=utf-8", status)

        def _file(self, base, rel):
            """Serve base/rel if it resolves inside base (no traversal, no symlink escape)."""
            base = base.resolve()
            try:
                f = (base / rel).resolve()
            except (OSError, ValueError):
                return self._json({"error": "not found"}, HTTPStatus.NOT_FOUND)
            if base not in f.parents or not f.is_file():
                return self._json({"error": "not found"}, HTTPStatus.NOT_FOUND)
            ctype = mimetypes.guess_type(f.name)[0] or "application/octet-stream"
            if ctype.startswith("text/") or ctype in ("application/javascript", "text/javascript", "application/json"):
                ctype += "; charset=utf-8"
            self._send(f.read_bytes(), ctype)

        def do_GET(self):
            if not self._host_ok():
                return self._json({"error": "bad host"}, HTTPStatus.FORBIDDEN)
            path = unquote(self.path.split("?", 1)[0])
            if path == "/api/data":
                raw, gz = app.current()
                if "gzip" in (self.headers.get("Accept-Encoding") or ""):
                    return self._send(gz, "application/json; charset=utf-8", extra={"Content-Encoding": "gzip"})
                return self._send(raw, "application/json; charset=utf-8")
            if path == "/api/whoami":
                return self._json(app.whoami())
            if path == "/api/decisions":
                label = (parse_qs(urlsplit(self.path).query).get("dir") or [""])[0]
                recs = app.decisions(label)
                if recs is None:
                    return self._json({"error": "unknown dir"}, HTTPStatus.NOT_FOUND)
                return self._json({"dir": label, "decisions": recs})
            if path.startswith("/api/"):
                return self._json({"error": "not found"}, HTTPStatus.NOT_FOUND)
            return self._file(WEB, "index.html" if path in ("/", "") else path.lstrip("/"))

        def do_POST(self):
            if not self._host_ok():
                return self._json({"error": "bad host"}, HTTPStatus.FORBIDDEN)
            path = unquote(self.path.split("?", 1)[0])
            if path in ("/api/decide", "/api/item"):
                try:
                    n = int(self.headers.get("Content-Length") or 0)
                    body = json.loads(self.rfile.read(n).decode("utf-8") or "null")
                except (ValueError, UnicodeDecodeError):
                    return self._json({"error": "body is not JSON"}, HTTPStatus.BAD_REQUEST)
                try:
                    return self._json({"saved": (app.decide if path == "/api/decide" else app.item)(body)})
                except store.Invalid as e:
                    return self._json({"error": str(e)}, HTTPStatus.BAD_REQUEST)
                except Exception as e:     # a failed write (the log was rolled back): say so loudly
                    print(f"review app: write failed: {e!r}", file=sys.stderr)
                    return self._json({"error": f"write failed: {e}"}, HTTPStatus.INTERNAL_SERVER_ERROR)
            return self._json({"error": "not found"}, HTTPStatus.NOT_FOUND)

    return Handler


def make_server(app, host="127.0.0.1", port=8767):
    ensure_loopback(host)
    return ThreadingHTTPServer((host, port), make_handler(app))


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
    app = App(data_path, args.reviewer or git_user())
    httpd = make_server(app, args.host, args.port)
    url = f"http://{args.host}:{httpd.server_address[1]}/"
    print(f"review app: {url}  (reviewer: {app.reviewer}; decisions write to each staging dir's "
          f"review_log.jsonl ONLY; the GEM database is never touched; Ctrl-C to stop)", file=sys.stderr)
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

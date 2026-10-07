"""
Which Chrome window modes pass which bot walls, and whether Chrome ever
came to the front while it worked.

Opens one known walled page per kind of wall (the hosts in
docs/reference/site_access.md) in each requested mode through
cf_clearance.render, and prints a table: HTTP status, whether the wall
cleared, seconds taken, and the frontmost app seen while Chrome ran
(polled every half second with macOS `lsappinfo`, which needs no
permission). Only the probe's own Chrome counts, matched by process id, so
a personal Chrome window in front is not mistaken for it. A mode is safe as
the default when it clears every wall the visible mode clears and Chrome
never shows up as the front app.

    python scripts/browser_mode_probe.py                         # background and headless
    python scripts/browser_mode_probe.py --modes visible         # the old baseline (pops up)
    python scripts/browser_mode_probe.py --modes background https://example.org/page

Each page opens in a fresh, empty Chrome profile, so a wall has to be
solved again rather than passed on a cookie earned earlier. Cookies Chrome
earns still go into the normal store, as with any render.
"""
import argparse
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

import cf_clearance

PAGES = (
    ("Cloudflare", "https://www.marinetraffic.org/"),
    ("AWS WAF", "https://investors.seatrium.com/"),
    ("DataDome", "https://www.waz.de/"),
    ("puzzle wall", "https://www.energate-messenger.de/"),
    ("script-built page", "https://web2.cylex.de/"),
)


def front_pid() -> int | None:
    try:
        asn = subprocess.run(["lsappinfo", "front"], capture_output=True, text=True,
                             timeout=5).stdout.strip()
        out = subprocess.run(["lsappinfo", "info", "-only", "pid", asn],
                             capture_output=True, text=True, timeout=5).stdout
        return int(out.split("=", 1)[-1].strip())
    except (OSError, subprocess.SubprocessError, ValueError):
        return None


def port_pid(port: int) -> int | None:
    """The process listening on the DevTools port: the probe's own Chrome."""
    try:
        out = subprocess.run(["lsof", "-nP", "-t", f"-iTCP:{port}", "-sTCP:LISTEN"],
                             capture_output=True, text=True, timeout=10).stdout
        return int(out.split()[0])
    except (OSError, subprocess.SubprocessError, ValueError, IndexError):
        return None


def watch_front(stop: threading.Event, front: set, ours: set) -> None:
    while not stop.is_set():
        front.add(front_pid())
        ours.add(port_pid(cf_clearance.CDP_PORT))
        time.sleep(0.5)


def probe(url: str, mode: str, wait: int) -> dict:
    stop, front, ours = threading.Event(), set(), set()
    t = threading.Thread(target=watch_front, args=(stop, front, ours), daemon=True)
    t.start()
    t0 = time.time()
    keep = cf_clearance.profile_dir
    with tempfile.TemporaryDirectory(prefix="probe_profile_") as prof:
        cf_clearance.profile_dir = lambda: Path(prof)
        try:
            r = cf_clearance.render(url, wait=wait, mode=mode)
            res = {"status": r["status"], "cleared": not r["challenge"],
                   "title": r["title"][:40]}
        except cf_clearance.ClearanceError as e:
            res = {"status": "err", "cleared": False, "title": str(e)[:40]}
        finally:
            cf_clearance.profile_dir = keep
    stop.set()
    t.join()
    res["seconds"] = round(time.time() - t0)
    res["chrome_in_front"] = bool((front & ours) - {None})
    return res


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("urls", nargs="*", help="pages to try instead of the built-in list")
    p.add_argument("--modes", nargs="+", default=["background", "headless"],
                   choices=cf_clearance.BROWSER_MODES)
    p.add_argument("--wait", type=int, default=45, help="seconds per page")
    args = p.parse_args()
    pages = [("given", u) for u in args.urls] or list(PAGES)
    print(f"{'mode':10s} {'wall':18s} {'status':6s} {'cleared':7s} {'secs':>4s} "
          f"{'in front':8s} title")
    for mode in args.modes:
        for kind, url in pages:
            r = probe(url, mode, args.wait)
            print(f"{mode:10s} {kind:18s} {r['status']:6s} {str(r['cleared']):7s} "
                  f"{r['seconds']:4d} {'YES' if r['chrome_in_front'] else 'no':8s} "
                  f"{r['title']}", flush=True)


if __name__ == "__main__":
    sys.exit(main())

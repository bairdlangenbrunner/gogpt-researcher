"""
Bot-wall clearance cookies: Cloudflare's JS "Just a moment..." managed
challenge (marinetraffic.org, marinevesseltraffic.com, ...), AWS WAF
(investors.seatrium.com — answers curl with an empty HTTP 202 and only serves
the page to a browser holding its `aws-waf-token`) and Imperva/Incapsula.

Why this exists (2026-09-16): the challenge cannot be passed by curl, by
TLS-fingerprint impersonation, or by any browser Playwright launches (headless
or headed, Chromium/Chrome/Firefox — Turnstile spots the automation flags).
It IS passed, in about five seconds, by a real Google Chrome that we launch
ourselves with a scratch profile and drive over the DevTools protocol using
only the Target/DOM/Storage domains (never `Runtime.enable`, the tell that
Turnstile looks for). The `cf_clearance` cookie Chrome receives is valid for a
year and is honoured for plain `curl` requests as long as the User-Agent
string matches the Chrome that earned it (it is also bound to our egress IP,
so it silently stops working when the laptop changes networks — refresh again).

Library usage (fetch.py calls these; nothing else should need to):
    from cf_clearance import cookie_for, refresh, ClearanceError

    hit = cookie_for("https://www.marinetraffic.org/...")   # (cookie header, ua) | None
    refresh([url])          # opens Chrome, waits for the challenge, stores the cookies

CLI:
    python scripts/cf_clearance.py https://www.marinetraffic.org/ https://www.marinevesseltraffic.com/
    python scripts/cf_clearance.py --show

Store: work/cf_clearance.json (gitignored — the cookie is a credential-like
token for this IP; never commit it). Set LNGCT_NO_BROWSER=1 to forbid the
Chrome launch (CI, unattended runs): fetch.py then reports the wall as blocked.

Window mode (2026-10-07), env LNGCT_BROWSER_MODE:
    background  (default) the same real Chrome, started with no window and
                given its pages as background tabs, so it never takes focus
                or comes to the front; the window sits in the far corner
                behind everything else. Unfocused
                windows would normally slow their timers, so the
                background-throttling switches are turned off.
    headless    Chrome's --headless=new, with the normal Chrome User-Agent
                so the stored cookies still replay through curl.
    visible     the old behavior: a Chrome window opens in front.
`--login` always opens a visible window, because a person has to sign in.
`scripts/browser_mode_probe.py` checks which modes pass which walls.
"""
import base64
import contextlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

from paths import work_dir

CHROME_CANDIDATES = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
)
CDP_PORT = int(os.environ.get("LNGCT_CDP_PORT", "9333"))
BROWSER_MODES = ("background", "headless", "visible")
# Keep a hidden or headless page running its scripts at full speed, so a
# bot challenge clears as fast as it does in a window in front.
QUIET_SWITCHES = ("--disable-backgrounding-occluded-windows",
                  "--disable-renderer-backgrounding",
                  "--disable-background-timer-throttling")
CHALLENGE_TITLES = ("just a moment", "verify you are human", "attention required",
                    "checking your browser", "please wait", "are you a robot",
                    "access denied", "human verification", "hold on",
                    # the same interstitials in the languages GEM sources use
                    "bitte warten", "einen moment", "un instant", "un momento",
                    "even geduld", "aguarde", "chwileczk", "подождите")
# Titles that mark a waiting page on their own, whatever the body holds
# (energate-messenger.de's proof-of-work page is titled "Bitte warten...").
INTERSTITIAL_TITLES = ("just a moment", "please wait", "hold on", "checking your browser",
                       "bitte warten", "einen moment", "un instant", "un momento",
                       "even geduld", "aguarde", "chwileczk", "подождите")
# A challenge page can have an empty title (AWS WAF, Imperva) — Chrome then
# reports the URL as the title — so the rendered DOM is checked as well.
CHALLENGE_BODY_MARKERS = ("challenge-platform", "cf-chl", "cf_chl_",           # Cloudflare
                          "awswaf", "challenge-container",                    # AWS WAF
                          "_incapsula_resource", "incapsula incident",        # Imperva
                          "px-captcha",                                       # PerimeterX
                          "captcha-delivery.com",                             # DataDome
                          "_plcdn_pow", "proof-of-work")                      # proof-of-work walls
# Cookie families that carry a bot-wall clearance. Everything else the browser
# holds (analytics, consent) stays out of the store.
WALL_COOKIE_PREFIXES = ("cf_clearance",                      # Cloudflare
                        "aws-waf-token",                     # AWS WAF
                        "incap_ses_", "visid_incap_", "nlbi_", "reese84",   # Imperva
                        "_px", "px",                          # PerimeterX
                        "datadome",                           # DataDome (waz-online.de)
                        "_plcdn_pow")                         # proof-of-work wall (energate-messenger.de)


class ClearanceError(RuntimeError):
    pass


def store_path() -> Path:
    return work_dir() / "cf_clearance.json"


def profile_dir() -> Path:
    return work_dir() / "chrome_profile"


def browser_allowed() -> bool:
    return os.environ.get("LNGCT_NO_BROWSER", "") not in ("1", "true", "yes")


def browser_mode() -> str:
    """LNGCT_BROWSER_MODE, one of BROWSER_MODES; anything else is background."""
    m = os.environ.get("LNGCT_BROWSER_MODE", "").strip().lower()
    return m if m in BROWSER_MODES else "background"


def is_wall_cookie(name: str) -> bool:
    return any(name.startswith(p) for p in WALL_COOKIE_PREFIXES)


def load_store() -> dict:
    """{"ua": str, "cookies": {domain: {"cookies": {name: value}, "expires": float, "saved": float}}}

    Entries written before 2026-09-16 (evening) hold a single "value" (the
    cf_clearance cookie) instead of "cookies"; both shapes are read.
    """
    try:
        d = json.loads(store_path().read_text())
        d.setdefault("cookies", {})
        return d
    except (OSError, ValueError):
        return {"ua": "", "cookies": {}}


def save_store(store: dict) -> None:
    p = store_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(store, indent=1))


def _domain_matches(host: str, domain: str) -> bool:
    d = domain.lstrip(".").lower()
    return host == d or host.endswith("." + d)


def _entry_cookies(entry: dict) -> dict[str, str]:
    if entry.get("cookies"):
        return {k: v for k, v in entry["cookies"].items() if v}
    if entry.get("value"):                       # pre-generalisation shape
        return {"cf_clearance": entry["value"]}
    return {}


def cookie_for(url: str, store: dict | None = None) -> tuple[str, str] | None:
    """
    (Cookie header value, User-Agent it was earned with) for url's host, or
    None. Cookies from every matching domain (host, then each parent) are
    joined, so an Imperva site whose cookies sit on both `www.x.com` and
    `.x.com` replays as one header.
    """
    host = (urlsplit(url).hostname or "").lower()
    if not host:
        return None
    store = store if store is not None else load_store()
    now = time.time()
    jar: dict[str, str] = {}
    for domain, c in store.get("cookies", {}).items():
        if _domain_matches(host, domain) and c.get("expires", 0) > now:
            jar.update(_entry_cookies(c))
    if not jar:
        return None
    return "; ".join(f"{k}={v}" for k, v in jar.items()), store.get("ua", "")


def forget(url: str) -> None:
    """Drop the stored cookie for url's host (it stopped working)."""
    store = load_store()
    host = (urlsplit(url).hostname or "").lower()
    for domain in [d for d in store["cookies"] if _domain_matches(host, d)]:
        if store["cookies"][domain].get("login"):
            continue                 # a signed-in session is only dropped by hand
        del store["cookies"][domain]
    save_store(store)


# ---------------------------------------------------------------------------
# Chrome over the DevTools protocol
# ---------------------------------------------------------------------------

def _chrome_binary() -> str:
    for c in CHROME_CANDIDATES:
        if os.path.isabs(c) and os.path.exists(c):
            return c
        if not os.path.isabs(c) and shutil.which(c):
            return c
    raise ClearanceError(
        "Google Chrome not found — install it (https://www.google.com/chrome/) or "
        "add its path to CHROME_CANDIDATES in scripts/cf_clearance.py")


class _CDP:
    """Minimal DevTools client: one browser websocket, flat sessions."""

    def __init__(self, ws_url: str):
        try:
            import websocket  # websocket-client
        except ImportError as e:
            raise ClearanceError("pip install websocket-client (needed to drive Chrome)") from e
        self.ws = websocket.create_connection(ws_url, suppress_origin=True, timeout=60)
        self._id = 0
        self.events: list[dict] = []      # protocol events seen while waiting for replies

    def send(self, method: str, params: dict | None = None, session: str | None = None) -> dict:
        self._id += 1
        msg = {"id": self._id, "method": method, "params": params or {}}
        if session:
            msg["sessionId"] = session
        self.ws.send(json.dumps(msg))
        while True:
            r = json.loads(self.ws.recv())
            if "method" in r and "id" not in r:
                if len(self.events) < 5000:
                    self.events.append(r)
                continue
            if r.get("id") == self._id:
                if "error" in r:
                    raise ClearanceError(f"CDP {method}: {r['error']}")
                return r.get("result", {})

    def close(self) -> None:
        try:
            self.ws.close()
        except Exception:
            pass


def _desktop_ua(binary: str, platform: str = sys.platform) -> str:
    """The User-Agent the windowed Chrome sends (Chrome's reduced form,
    Chrome/<major>.0.0.0), for headless mode, which would otherwise say
    HeadlessChrome and earn cookies that curl cannot replay."""
    try:
        out = subprocess.run([binary, "--version"], capture_output=True, text=True,
                             timeout=20).stdout
        major = re.search(r"(\d+)\.\d+\.\d+\.\d+", out).group(1)
    except (OSError, subprocess.SubprocessError, AttributeError):
        major = "140"
    os_part = {"darwin": "Macintosh; Intel Mac OS X 10_15_7",
               "win32": "Windows NT 10.0; Win64; x64"}.get(platform, "X11; Linux x86_64")
    return (f"Mozilla/5.0 ({os_part}) AppleWebKit/537.36 (KHTML, like Gecko) "
            f"Chrome/{major}.0.0.0 Safari/537.36")


def _chrome_command(binary: str, prof: Path, port: int, mode: str,
                    platform: str = sys.platform) -> list[str]:
    """The command that starts Chrome in `mode` (see the module docstring)."""
    args = [f"--user-data-dir={prof}", f"--remote-debugging-port={port}",
            "--no-first-run", "--no-default-browser-check", "--window-size=1200,900"]
    if mode == "visible":
        return [binary, *args, "about:blank"]
    args += QUIET_SWITCHES
    if mode == "headless":
        return [binary, *args, "--headless=new",
                f"--user-agent={_desktop_ua(binary, platform)}", "about:blank"]
    # background: Chrome makes itself the front app when it opens its first
    # window at startup, so it starts with none and _new_tab opens each page.
    return [binary, *args, "--no-startup-window"]


def _new_tab(cdp: "_CDP", url: str, mode: str) -> str:
    """Open url without bringing Chrome to the front unless visible. A
    background target never activates the app (checked 2026-10-07 on macOS
    with lsappinfo). Its window is pushed toward the far bottom-right; macOS
    keeps a corner of it on screen, behind every other window."""
    params = {"url": url}
    if mode != "visible":
        params.update(background=True, newWindow=True, left=20000, top=20000)
    return cdp.send("Target.createTarget", params)["targetId"]


def _launch_chrome(port: int, mode: str | None = None) -> tuple[subprocess.Popen, dict]:
    mode = mode or browser_mode()
    binary = _chrome_binary()
    prof = profile_dir()
    prof.mkdir(parents=True, exist_ok=True)
    proc = subprocess.Popen(_chrome_command(binary, prof, port, mode),
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    version = None
    for _ in range(80):
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=2) as r:
                version = json.load(r)
            break
        except Exception:
            time.sleep(0.25)
    if version is None:
        proc.terminate()
        raise ClearanceError(f"Chrome did not open its DevTools port {port} "
                             f"(another Chrome on that port? set LNGCT_CDP_PORT)")
    # the stored cookies replay with this string, so it must be the windowed one
    version["User-Agent"] = version.get("User-Agent", "").replace("HeadlessChrome", "Chrome")
    return proc, version


def _is_challenge_title(title: str) -> bool:
    t = (title or "").lower()
    return not t or any(f in t for f in CHALLENGE_TITLES)


def _is_challenge_body(html: str) -> bool:
    h = (html or "")[:20000].lower()
    return not h.strip() or any(m in h for m in CHALLENGE_BODY_MARKERS)


def _page_html(cdp: "_CDP", session: str) -> str:
    """Rendered document via the DOM domain (no Runtime.enable)."""
    try:
        root = cdp.send("DOM.getDocument", {"depth": 0}, session=session)["root"]
        return cdp.send("DOM.getOuterHTML", {"nodeId": root["nodeId"]}, session=session)["outerHTML"]
    except ClearanceError:
        return ""


def merge_cookies(store: dict, cookies: list[dict], ua: str, now: float | None = None) -> int:
    """
    Merge the browser's cookie list (DevTools Storage.getCookies shape) into the
    store, keeping only bot-wall cookies, grouped by domain. Session cookies
    (no expiry) get 30 minutes. Returns the number of cookies kept.
    """
    now = time.time() if now is None else now
    store["ua"] = ua or store.get("ua", "")
    by_domain: dict[str, dict] = {}
    for c in cookies:
        name, value = c.get("name", ""), c.get("value", "")
        if not (value and is_wall_cookie(name)):
            continue
        exp = float(c.get("expires") or 0)
        exp = exp if exp > now else now + 1800
        e = by_domain.setdefault(c["domain"], {"cookies": {}, "expires": 0.0, "saved": now})
        e["cookies"][name] = value
        e["expires"] = max(e["expires"], exp)
    kept = 0
    for domain, e in by_domain.items():
        old = store.setdefault("cookies", {}).get(domain)
        if old and old.get("login"):
            # never drop a signed-in session when a wall cookie is refreshed
            old.setdefault("cookies", {}).update(e["cookies"])
            old["expires"] = max(float(old.get("expires", 0)), e["expires"])
        else:
            store["cookies"][domain] = e
        kept += len(e["cookies"])
    return kept


def login(url: str, wait: int = 900, port: int = CDP_PORT) -> int:
    """
    Open url in the scratch Chrome profile for a PERSON to sign in (a free
    registration wall such as energate-messenger.de, or a subscription GEM
    holds). When they close the tab, or after `wait` seconds, every cookie
    the browser holds for that site is stored as a login entry, so fetch.py
    and render() read the pages as that signed-in reader. Returns the number
    of cookies kept. Never fills in credentials itself.
    """
    if not browser_allowed():
        raise ClearanceError("browser launch forbidden by LNGCT_NO_BROWSER")
    host = (urlsplit(url).hostname or "").lower()
    site = ".".join(host.split(".")[-2:])          # cookies often sit on the parent domain
    with _browser_lock():
        proc, version = _launch_chrome(port, mode="visible")
        cdp = _CDP(version["webSocketDebuggerUrl"])
        cookies: list[dict] = []
        try:
            tid = cdp.send("Target.createTarget", {"url": url})["targetId"]
            print(f"Sign in to {host} in the Chrome window, then close that tab "
                  f"(waiting up to {wait // 60} minutes).", file=sys.stderr)
            deadline = time.time() + wait
            while time.time() < deadline:
                time.sleep(3)
                try:
                    cookies = cdp.send("Storage.getCookies").get("cookies", [])
                    open_ids = {t["targetId"] for t in cdp.send("Target.getTargets")["targetInfos"]}
                except Exception:
                    break                                # the person closed Chrome itself
                if tid not in open_ids:
                    break
        finally:
            _stop_chrome(cdp, proc)
    now = time.time()
    store = load_store()
    store["ua"] = version.get("User-Agent", "") or store.get("ua", "")
    kept = 0
    for c in cookies:
        dom = c.get("domain", "")
        d = dom.lstrip(".").lower()
        if not c.get("value") or not (d == site or d.endswith("." + site)):
            continue
        exp = float(c.get("expires") or 0)
        e = store.setdefault("cookies", {}).setdefault(
            dom, {"cookies": {}, "expires": 0.0, "saved": now})
        e["login"] = True
        e["cookies"][c["name"]] = c["value"]
        e["expires"] = max(float(e.get("expires", 0)), exp if exp > now else now + 30 * 86400)
        kept += 1
    save_store(store)
    return kept


@contextlib.contextmanager
def _browser_lock():
    """One Chrome at a time across processes: parallel research agents share
    the scratch profile and the DevTools port. Without fcntl, no locking."""
    try:
        import fcntl
    except ImportError:
        yield
        return
    p = work_dir() / "chrome.lock"
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a+") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


def _stop_chrome(cdp: "_CDP", proc: subprocess.Popen) -> None:
    try:                                         # a clean exit saves the profile
        cdp.ws.settimeout(5)
        cdp.send("Browser.close")
    except Exception:
        pass
    cdp.close()
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()


def _main_document(events: list[dict], session: str, frame: str) -> dict | None:
    """The last top-level document response seen on this tab (after any
    challenge reloads), from Network.responseReceived events. Only the tab's
    own frame counts: Chrome's PDF viewer loads its own page in a subframe."""
    main = None
    for ev in events:
        p = ev.get("params", {})
        if (ev.get("method") == "Network.responseReceived" and ev.get("sessionId") == session
                and p.get("type") == "Document" and p.get("frameId") == frame
                and p.get("response", {}).get("url", "").startswith("http")):
            main = p
    return main


def render(url: str, wait: int = 45, port: int = CDP_PORT, mode: str | None = None) -> dict:
    """
    Open url in a real Chrome and return what a person would see once any bot
    challenge has run: {"status", "mime", "final_url", "title", "html",
    "body" (bytes for a PDF or other file, else None), "challenge" (True if the
    wall never cleared), "cookie" (every cookie the browser holds for the host,
    as a header), "ua"}. Bot-wall cookies are also merged into the store, so
    later plain requests to the host may pass without a browser.

    This is the last rung for walls that only a real browser passes
    (proof-of-work pages, DataDome, script-built pages). Network.enable is
    used to read the real HTTP status; Runtime.enable never is. `mode`
    overrides LNGCT_BROWSER_MODE.
    """
    if not browser_allowed():
        raise ClearanceError("browser launch forbidden by LNGCT_NO_BROWSER")
    host = (urlsplit(url).hostname or "").lower()
    mode = mode or browser_mode()
    with _browser_lock():
        proc, version = _launch_chrome(port, mode)
        cdp = _CDP(version["webSocketDebuggerUrl"])
        try:
            tid = _new_tab(cdp, "about:blank", mode)
            session = cdp.send("Target.attachToTarget",
                               {"targetId": tid, "flatten": True})["sessionId"]
            cdp.send("Network.enable", {}, session=session)
            cdp.send("Page.navigate", {"url": url}, session=session)
            deadline = time.time() + wait
            html, title, last_len, stable, challenge = "", "", -1, 0, True
            while time.time() < deadline:
                time.sleep(2.0)
                info = [t for t in cdp.send("Target.getTargets")["targetInfos"]
                        if t["targetId"] == tid]
                title = info[0]["title"] if info else ""
                page_url = info[0].get("url", "") if info else ""
                if title and title in (page_url, page_url.split("://", 1)[-1]):
                    title = ""
                html = _page_html(cdp, session)
                challenge = _is_challenge_title(title) and _is_challenge_body(html)
                if title.strip().lower().startswith(INTERSTITIAL_TITLES):
                    challenge = True             # a waiting page that carries a body
                main = _main_document(cdp.events, session, tid)
                if challenge or main is None:
                    stable = 0
                    continue
                if (main.get("response", {}).get("mimeType") or "").startswith("text/html"):
                    stable = stable + 1 if len(html) == last_len else 0
                    last_len = len(html)
                    if stable >= 1:              # same DOM on two polls: settled
                        break
                else:
                    break                        # a PDF or other file: no DOM to settle
            main = _main_document(cdp.events, session, tid) or {}
            resp = main.get("response", {})
            mime = (resp.get("mimeType") or "").lower()
            body = None
            if main and not mime.startswith("text/html"):
                try:
                    r = cdp.send("Network.getResponseBody", {"requestId": main["requestId"]},
                                 session=session)
                    data = r.get("body", "")
                    body = base64.b64decode(data) if r.get("base64Encoded") else data.encode()
                except ClearanceError:
                    body = None                  # caller re-requests with the cookies
                if body is not None and "pdf" in mime and not body.startswith(b"%PDF"):
                    body = None                  # the PDF viewer's stub, not the file
            cookies = cdp.send("Storage.getCookies").get("cookies", [])
            cdp.send("Target.closeTarget", {"targetId": tid})
        finally:
            _stop_chrome(cdp, proc)
    ua = version.get("User-Agent", "")
    store = load_store()
    merge_cookies(store, cookies, ua)
    save_store(store)
    jar = {c["name"]: c["value"] for c in cookies
           if c.get("value") and _domain_matches(host, c.get("domain", ""))}
    return {"status": str(resp.get("status") or "000"), "mime": mime,
            "final_url": resp.get("url") or url, "title": title, "html": html,
            "body": body, "challenge": challenge, "ua": ua,
            "cookie": "; ".join(f"{k}={v}" for k, v in jar.items())}


def refresh(urls: list[str], wait: int = 60, port: int = CDP_PORT) -> dict:
    """
    Open each URL in a real Chrome, wait for its bot challenge to clear (title
    no longer a challenge title — a real 404 counts as cleared), harvest every
    bot-wall cookie the browser now holds and merge them into the store.
    Returns the store. Raises ClearanceError when Chrome is missing,
    the browser is forbidden (LNGCT_NO_BROWSER), or no URL cleared.
    """
    if not browser_allowed():
        raise ClearanceError("browser launch forbidden by LNGCT_NO_BROWSER")
    with _browser_lock():
        return _refresh(urls, wait, port)


def _refresh(urls: list[str], wait: int, port: int) -> dict:
    mode = browser_mode()
    proc, version = _launch_chrome(port, mode)
    cdp = _CDP(version["webSocketDebuggerUrl"])
    cleared: list[str] = []
    try:
        for url in urls:
            tid = _new_tab(cdp, url, mode)
            session = cdp.send("Target.attachToTarget", {"targetId": tid, "flatten": True})["sessionId"]
            title = ""
            deadline = time.time() + wait
            while time.time() < deadline:
                time.sleep(2.5)
                info = [t for t in cdp.send("Target.getTargets")["targetInfos"]
                        if t["targetId"] == tid]
                title = info[0]["title"] if info else ""
                page_url = info[0].get("url", "") if info else ""
                if title and title in (page_url, page_url.split("://", 1)[-1]):
                    title = ""                       # untitled page: Chrome shows the URL
                if title.strip().lower().startswith(INTERSTITIAL_TITLES):
                    continue
                if _is_challenge_title(title) and _is_challenge_body(_page_html(cdp, session)):
                    continue
                cleared.append(url)
                break
            print(f"  [cf_clearance] {url} -> {title!r}", file=sys.stderr)
            cdp.send("Target.closeTarget", {"targetId": tid})
        cookies = cdp.send("Storage.getCookies").get("cookies", [])
    finally:
        _stop_chrome(cdp, proc)
    store = load_store()
    merge_cookies(store, cookies, version.get("User-Agent", ""))
    save_store(store)
    if not cleared:
        raise ClearanceError("no URL cleared the challenge within the wait "
                             f"({wait}s) — is the site down, or the network captive?")
    return store


def main():
    import argparse
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("urls", nargs="*", help="URLs whose bot challenge to clear")
    p.add_argument("--show", action="store_true", help="print the stored cookies and exit")
    p.add_argument("--wait", type=int, default=60, help="seconds to wait per URL")
    p.add_argument("--login", action="store_true",
                   help="open the first URL for a person to sign in, then keep that "
                        "site's cookies (registration and subscription walls)")
    args = p.parse_args()
    if args.login and args.urls:
        try:
            n = login(args.urls[0])
        except ClearanceError as e:
            print(f"error: {e}", file=sys.stderr)
            sys.exit(1)
        print(f"kept {n} cookie(s) for {urlsplit(args.urls[0]).hostname} in {store_path()}")
        return
    store = load_store()
    if args.show or not args.urls:
        print(f"store: {store_path()}")
        print(f"ua: {store.get('ua') or '(none)'}")
        for d, c in sorted(store.get("cookies", {}).items()):
            left = c.get("expires", 0) - time.time()
            names = ", ".join(sorted(_entry_cookies(c)))
            print(f"  {d:36s} expires in {left/86400:6.1f} d  {names}")
        if not args.urls:
            return
    try:
        store = refresh(args.urls, wait=args.wait)
    except ClearanceError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"stored {len(store['cookies'])} cookie(s) in {store_path()}")


if __name__ == "__main__":
    main()

"""Offline tests for the access ladder added 2026-10-06: 406 handling, the
real-Chrome render rung, learned routes, the wider disk cache, signed-in
cookie entries, and the verifier's archive fallback."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import cf_clearance  # noqa: E402
import fetch  # noqa: E402
import url_verifier  # noqa: E402

URL = "https://www.example-news.de/artikel/kraftwerk"
HOST = "www.example-news.de"
BODY = b"<html><title>Gaskraftwerk</title><body>Leistung 1.200 MW</body></html>"
GOOD = ("200", "text/html", URL, BODY)
DENIED = ("403", "text/html", URL, b"<html><title>Access denied</title></html>")
NOT_ACCEPTABLE = ("406", "text/html", URL, b"<html>Not Acceptable</html>")


@pytest.fixture
def net(monkeypatch, tmp_path):
    state = {"responses": [], "calls": 0, "impersonate": [], "render": [],
             "impersonated": 0, "rendered": 0}

    def fake_curl_attempts(url, tmp, timeout, ua, headers, cookie, notes):
        state["calls"] += 1
        r = state["responses"].pop(0) if state["responses"] else DENIED
        Path(tmp).write_bytes(r[3])
        return r

    def fake_impersonate(*a, **k):
        state["impersonated"] += 1
        return state["impersonate"].pop(0) if state["impersonate"] else None

    def fake_render(url, timeout, tmp, notes):
        state["rendered"] += 1
        r = state["render"].pop(0) if state["render"] else None
        if r:
            notes.append("browser_render")
        return r

    monkeypatch.setattr(fetch, "_curl_attempts", fake_curl_attempts)
    monkeypatch.setattr(fetch, "_impersonate", fake_impersonate)
    monkeypatch.setattr(fetch, "_render", fake_render)
    monkeypatch.setattr(fetch, "_clearance_cookie", lambda url: (None, None))
    monkeypatch.setattr(fetch, "_earn_clearance", lambda url: (None, None))
    monkeypatch.setattr(fetch.time, "sleep", lambda s: None)
    monkeypatch.setattr(fetch, "CACHE_DIR", tmp_path / "cache")
    monkeypatch.setattr(fetch, "ROUTES_PATH", tmp_path / "routes.json")
    monkeypatch.setattr(fetch, "FAIL_LOG", tmp_path / "failures.jsonl")
    monkeypatch.setattr(fetch, "_IMPERSONATE_HOSTS", set())
    monkeypatch.delenv("GEM_FETCH_NO_CACHE", raising=False)
    return state


def routes():
    return json.loads(fetch.ROUTES_PATH.read_text())


def test_406_escalates_to_impersonation_and_the_route_is_learned(net):
    net["responses"] = [NOT_ACCEPTABLE]
    net["impersonate"] = [GOOD]
    page = fetch.fetch_page(URL)
    assert page.status == "200" and "cf_impersonate" in page.notes
    assert routes()[HOST]["route"] == "cf_impersonate"


def test_learned_impersonation_route_skips_plain_curl(net):
    fetch.ROUTES_PATH.write_text(json.dumps({HOST: {"route": "cf_impersonate"}}))
    net["impersonate"] = [GOOD]
    page = fetch.fetch_page(URL)
    assert page.status == "200" and net["calls"] == 0


def test_render_rung_runs_when_the_wall_survives_impersonation(net):
    net["responses"] = [DENIED]
    net["render"] = [GOOD]
    page = fetch.fetch_page(URL)
    assert page.status == "200" and "browser_render" in page.notes
    assert net["impersonated"] == 1 and net["rendered"] == 1
    assert routes()[HOST]["route"] == "browser_render"
    # a page that cost a Chrome render is kept on disk
    again = fetch.fetch_page(URL)
    assert "disk_cache" in again.notes and net["rendered"] == 1


def test_learned_browser_route_goes_straight_to_chrome(net):
    fetch.ROUTES_PATH.write_text(json.dumps({HOST: {"route": "browser_render"}}))
    net["responses"] = [DENIED]
    net["render"] = [GOOD]
    page = fetch.fetch_page(URL)
    assert page.status == "200"
    assert net["impersonated"] == 0 and net["rendered"] == 1


def test_a_blocked_render_does_not_replace_the_answer(net):
    net["responses"] = [DENIED]
    net["render"] = [("403", "text/html", URL, b"<title>blocked</title>")]
    page = fetch.fetch_page(URL)
    assert page.status == "403" and not fetch.ROUTES_PATH.exists()


def test_plain_successes_are_neither_cached_nor_recorded(net):
    net["responses"] = [GOOD]
    page = fetch.fetch_page(URL)
    assert page.status == "200" and net["rendered"] == 0
    assert not fetch.ROUTES_PATH.exists()
    assert not list(fetch.CACHE_DIR.glob("*.bin"))


def test_merge_keeps_a_signed_in_entry():
    store = {"cookies": {"energate-messenger.de": {
        "cookies": {"session": "abc"}, "expires": 9e9, "login": True}}}
    cf_clearance.merge_cookies(store, [{"name": "_plcdn_pow", "value": "x",
                                        "domain": "energate-messenger.de", "expires": 0}],
                               "ua", now=1000.0)
    e = store["cookies"]["energate-messenger.de"]
    assert e["login"] and e["cookies"] == {"session": "abc", "_plcdn_pow": "x"}


def test_forget_leaves_signed_in_entries(monkeypatch):
    store = {"ua": "", "cookies": {
        "energate-messenger.de": {"cookies": {"s": "1"}, "expires": 9e9, "login": True},
        "waz.de": {"cookies": {"datadome": "2"}, "expires": 9e9}}}
    monkeypatch.setattr(cf_clearance, "load_store", lambda: store)
    monkeypatch.setattr(cf_clearance, "save_store", lambda s: None)
    cf_clearance.forget("https://www.energate-messenger.de/news/1")
    cf_clearance.forget("https://www.waz.de/a")
    assert set(store["cookies"]) == {"energate-messenger.de"}


def test_main_document_ignores_the_pdf_viewer_subframe():
    def ev(frame, url, mime):
        return {"method": "Network.responseReceived", "sessionId": "S",
                "params": {"type": "Document", "frameId": frame,
                           "response": {"url": url, "mimeType": mime, "status": 200}}}
    events = [ev("TOP", "https://x.de/a.pdf", "application/pdf"),
              ev("SUB", "chrome-extension://viewer/index.html", "text/html"),
              ev("SUB", "https://x.de/viewer.html", "text/html")]
    main = cf_clearance._main_document(events, "S", "TOP")
    assert main["response"]["mimeType"] == "application/pdf"


# --- Chrome window modes (2026-10-07) ----------------------------------------

@pytest.mark.parametrize("env,mode", [(None, "background"), ("headless", "headless"),
                                      ("VISIBLE", "visible"), ("bogus", "background")])
def test_browser_mode_defaults_to_background(monkeypatch, env, mode):
    if env is None:
        monkeypatch.delenv("LNGCT_BROWSER_MODE", raising=False)
    else:
        monkeypatch.setenv("LNGCT_BROWSER_MODE", env)
    assert cf_clearance.browser_mode() == mode


def test_background_chrome_starts_without_a_window():
    cmd = cf_clearance._chrome_command("/x/chrome", Path("/p"), 9333, "background")
    assert "--no-startup-window" in cmd and "about:blank" not in cmd
    assert set(cf_clearance.QUIET_SWITCHES) <= set(cmd)
    assert not any(a.startswith("--headless") for a in cmd)


def test_headless_chrome_sends_the_windowed_user_agent():
    cmd = cf_clearance._chrome_command("/no/such/chrome", Path("/p"), 9333, "headless")
    ua = next(a for a in cmd if a.startswith("--user-agent="))
    assert "--headless=new" in cmd and "HeadlessChrome" not in ua and "Chrome/" in ua


def test_visible_chrome_is_unchanged():
    cmd = cf_clearance._chrome_command("/x/chrome", Path("/p"), 9333, "visible")
    assert cmd[-1] == "about:blank" and "--no-startup-window" not in cmd
    assert not set(cf_clearance.QUIET_SWITCHES) & set(cmd)


class _FakeCDP:
    def __init__(self):
        self.sent = []

    def send(self, method, params=None, session=None):
        self.sent.append((method, params or {}))
        return {"targetId": "T"}


@pytest.mark.parametrize("mode,background", [("background", True), ("headless", True),
                                             ("visible", False)])
def test_new_tab_stays_behind_unless_visible(mode, background):
    cdp = _FakeCDP()
    cf_clearance._new_tab(cdp, "https://x.de/", mode)
    method, params = cdp.sent[0]
    assert method == "Target.createTarget"
    assert params.get("background", False) is background


def test_login_always_opens_a_visible_window(monkeypatch, tmp_path):
    monkeypatch.setenv("LNGCT_BROWSER_MODE", "background")
    seen = {}

    def fake_launch(port, mode=None):
        seen["mode"] = mode
        raise cf_clearance.ClearanceError("stop here")

    monkeypatch.setattr(cf_clearance, "_launch_chrome", fake_launch)
    monkeypatch.setattr(cf_clearance, "work_dir", lambda: tmp_path)
    with pytest.raises(cf_clearance.ClearanceError):
        cf_clearance.login("https://www.energate-messenger.de/")
    assert seen["mode"] == "visible"


# --- the verifier's archive fallback ----------------------------------------

@pytest.fixture
def archive(monkeypatch):
    url_verifier._CACHE.clear()
    monkeypatch.setattr(url_verifier.time, "sleep", lambda s: None)
    state = {"lookups": [], "pages": {}}

    def fake_get(api):
        return state["lookups"].pop(0) if state["lookups"] else None

    def fake_fetch(url, timeout=30):
        return state["pages"].get(url, ("404", "", False, []))

    monkeypatch.setattr(url_verifier, "_archive_get", fake_get)
    monkeypatch.setattr(url_verifier, "_fetch", fake_fetch)
    return state


def test_offline_archive_page_counts_as_a_refused_lookup(monkeypatch):
    offline = subprocess.CompletedProcess([], 0, "<html><title>Internet Archive: "
                                          "Temporarily Offline</title>", "")
    monkeypatch.setattr(url_verifier.subprocess, "run", lambda *a, **k: offline)
    assert url_verifier._archive_get("http://web.archive.org/cdx/search/cdx?url=x") is None


def test_no_answer_at_all_is_lookup_failed_not_a_verdict(archive):
    assert url_verifier._wayback_snapshots(URL) == "lookup-failed"
    ok, reason = url_verifier._check_wayback(URL, ["1.200 MW"], True, "HTTP 403")
    assert not ok and "try again later" in reason.lower()


def test_empty_availability_answer_is_not_final_while_the_index_is_down(archive):
    archive["lookups"] = [None, '{"archived_snapshots": {}}'] * 4
    assert url_verifier._wayback_snapshots(URL) == "lookup-failed"


def test_an_older_snapshot_with_the_value_passes(archive):
    archive["lookups"] = [f"20220101000000 {URL}\n20250101000000 {URL}\n"]
    new = f"https://web.archive.org/web/20250101000000/{URL}"
    old = f"https://web.archive.org/web/20220101000000/{URL}"
    archive["pages"] = {new: ("200", "<title>x</title>neu 900 MW", False, []),
                        old: ("200", "<title>x</title>alt 1.200 MW", False, [])}
    ok, reason = url_verifier._check_wayback(URL, ["1.200 MW"], True, "HTTP 403")
    assert ok and "20220101000000" in reason


def test_a_dead_page_names_the_archived_copy_but_still_fails(archive):
    archive["lookups"] = [f"20220101000000 {URL}\n"]
    snap = f"https://web.archive.org/web/20220101000000/{URL}"
    archive["pages"] = {snap: ("200", "<title>x</title>1.200 MW", False, [])}
    ok, reason = url_verifier._check_wayback(URL, ["1.200 MW"], True, "HTTP 000", dead=True)
    assert not ok and snap in reason


def test_unreadable_snapshots_say_the_archive_was_unavailable(archive):
    archive["lookups"] = [f"20220101000000 {URL}\n"]
    ok, reason = url_verifier._check_wayback(URL, ["1.200 MW"], True, "HTTP 403")
    assert not ok and "archive unavailable" in reason


def test_a_number_inside_a_title_is_not_a_status_code(monkeypatch):
    url_verifier._CACHE.clear()
    title = ("<title>Bekanntmachung Gasmotoren-Anlage, Flur-Nrn. 2404 und 2408, "
             "89355 Gundremmingen</title>")
    monkeypatch.setattr(url_verifier, "_fetch",
                        lambda u, timeout=30: ("200", title + "RWE Generation SE", False, []))
    ok, _ = url_verifier.verify_url(URL, ["RWE Generation SE"])
    assert ok
    monkeypatch.setattr(url_verifier, "_fetch",
                        lambda u, timeout=30: ("200", "<title>Error 404</title>RWE", False, []))
    url_verifier._CACHE.clear()
    ok, reason = url_verifier.verify_url(URL, ["RWE"], wayback_fallback=False)
    assert not ok and "soft-error" in reason


EMPTY = ("200", "text/html", URL,
         b"<html><title>Detailansicht</title><body>Keine Detailinformationen verf\xc3\xbcgbar"
         b"</body></html>")


def test_an_empty_record_page_is_not_cached_and_drops_an_old_copy(net):
    fetch._cache_put(URL, "text/html", URL, EMPTY[3])
    page = fetch.fetch_page(URL)
    assert "empty_answer" in page.notes
    assert fetch._cache_get(URL) is None
    net["responses"] = [EMPTY]
    page = fetch.fetch_page(URL)
    assert "empty_answer" in page.notes and fetch._cache_get(URL) is None


def test_the_verifier_reports_an_empty_record_page_as_unread(monkeypatch):
    url_verifier._CACHE.clear()
    monkeypatch.setattr(url_verifier, "_fetch", lambda u, timeout=30: (
        "200", EMPTY[3].decode(), False, ["empty_answer"]))
    ok, reason = url_verifier.verify_url(URL, ["Lippendorf"])
    assert not ok and reason.startswith("empty record page")


def test_failed_reads_are_logged_and_the_audit_lists_them(net, tmp_path):
    import access_audit
    batch = tmp_path / "batch"
    (batch / "briefs").mkdir(parents=True)
    (batch / "briefs" / "P1.md").write_text("brief")
    (batch / "shards").mkdir()
    cited = "https://www.example-news.de/cited"
    (batch / "shards" / "P1.urls.jsonl").write_text(json.dumps(
        {"url": cited, "ok": True, "reason": "OK", "ts": "2099-01-01"}) + "\n")
    net["responses"] = [("429", "text/html", URL, b"<title>429 Too Many Requests</title>")]
    fetch.fetch_page(URL, rate_limit_attempts=0)
    net["responses"] = [DENIED]
    fetch.fetch_page(cited)                     # a page the verifier already passed
    failed = access_audit.load_failures([batch])
    assert set(failed) == {URL}
    assert access_audit.classify(failed[URL]["reason"]) == "rate_limited"

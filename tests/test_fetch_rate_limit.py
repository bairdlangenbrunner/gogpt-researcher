"""Offline tests for fetch.py's rate-limit waiting, host pacing and disk cache."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import fetch  # noqa: E402

PERMIT_URL = "https://www.uvp-verbund.de/trefferanzeige?docuuid=abc"
OTHER_URL = "https://example.org/page"
BODY = b"<html><title>Gaskraftwerk</title><body>1.200 MW</body></html>"
LIMITED = ("429", "text/html", "", b"<h1>429 Too Many Requests</h1>")
GOOD = ("200", "text/html", "", BODY)


@pytest.fixture
def net(monkeypatch, tmp_path):
    """Replace curl with a scripted list of responses; count calls and sleeps."""
    state = {"responses": [], "calls": 0, "sleeps": [], "impersonated": 0}

    def fake_curl_attempts(url, tmp, timeout, ua, headers, cookie, notes):
        state["calls"] += 1
        r = state["responses"].pop(0) if state["responses"] else LIMITED
        Path(tmp).write_bytes(r[3])
        return r

    def fake_impersonate(*a, **k):
        state["impersonated"] += 1
        return None

    monkeypatch.setattr(fetch, "_curl_attempts", fake_curl_attempts)
    monkeypatch.setattr(fetch, "_impersonate", fake_impersonate)
    monkeypatch.setattr(fetch, "_clearance_cookie", lambda url: (None, None))
    monkeypatch.setattr(fetch.time, "sleep", lambda s: state["sleeps"].append(s))
    monkeypatch.setattr(fetch, "CACHE_DIR", tmp_path / "cache")
    monkeypatch.setattr(fetch, "_IMPERSONATE_HOSTS", set())
    monkeypatch.delenv("GEM_FETCH_NO_CACHE", raising=False)
    return state


@pytest.mark.parametrize("host,paced", [
    ("www.uvp-verbund.de", True), ("uvp-verbund.de", True),
    ("uvp.niedersachsen.de", True), ("www.uvp.sachsen.de", True),
    ("www.enbw.com", False), ("notuvp-verbund.de.example.com", False),
])
def test_paced_hosts(host, paced):
    assert (fetch._paced(host)[0] is not None) == paced


def test_429_is_waited_out_without_impersonation(net):
    net["responses"] = [LIMITED, LIMITED, LIMITED, GOOD]
    page = fetch.fetch_page(OTHER_URL)
    assert page.status == "200"
    assert "rate_limit_wait" in page.notes
    assert net["calls"] == 4
    assert net["impersonated"] == 0
    waits = [s for s in net["sleeps"] if s >= fetch._RATE_LIMIT_PAUSE_START]
    assert len(waits) == 3 and waits[0] < waits[1] < waits[2]


def test_429_gives_up_after_the_budget_then_tries_impersonation_once(net):
    page = fetch.fetch_page(OTHER_URL, rate_limit_attempts=3)
    assert page.status == "429"
    assert net["calls"] == 4            # first request + 3 retries
    assert net["impersonated"] == 1


def test_cloudflare_429_is_not_waited_out(net, monkeypatch):
    net["responses"] = [("429", "text/html", "", b"<title>Just a moment...</title> cloudflare")]
    monkeypatch.setattr(fetch, "_earn_clearance", lambda url: (None, None))
    page = fetch.fetch_page(OTHER_URL)
    assert page.status == "429"
    assert net["calls"] == 1
    assert net["impersonated"] == 1


def test_paced_host_success_is_cached_and_reused(net):
    net["responses"] = [LIMITED, GOOD]
    first = fetch.fetch_page(PERMIT_URL)
    assert first.status == "200" and "disk_cache" not in first.notes
    calls = net["calls"]
    second = fetch.fetch_page(PERMIT_URL)
    assert second.status == "200" and "disk_cache" in second.notes
    assert second.text == first.text
    assert net["calls"] == calls        # no request sent for the cached read


def test_other_hosts_and_failures_are_not_cached(net):
    net["responses"] = [GOOD]
    fetch.fetch_page(OTHER_URL)
    fetch.fetch_page(PERMIT_URL, rate_limit_attempts=1)     # stays 429
    assert not list((fetch.CACHE_DIR).glob("*.bin"))


def test_cache_can_be_bypassed(net, monkeypatch):
    net["responses"] = [GOOD, GOOD]
    fetch.fetch_page(PERMIT_URL)
    monkeypatch.setenv("GEM_FETCH_NO_CACHE", "1")
    page = fetch.fetch_page(PERMIT_URL)
    assert "disk_cache" not in page.notes and net["calls"] == 2


def test_host_turn_enforces_the_minimum_gap(net):
    with fetch._host_turn("gap-test", 3.0):
        pass
    net["sleeps"].clear()
    with fetch._host_turn("gap-test", 3.0):
        pass
    assert net["sleeps"] and 0 < net["sleeps"][0] <= 3.0

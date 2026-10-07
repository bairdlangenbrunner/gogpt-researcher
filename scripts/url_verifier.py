"""
URL verification harness for the GOGPT workflow.

Per Update SOP §7: every URL cited in a reference/datasource cell or candidate
row MUST be verified to (1) return HTTP 200, AND (2) contain the entities/
values it's cited for, AND (3) not be a soft-error page (200 with
"404"/"429"/Cloudflare interstitial in the title).

Ported from the LNG Terminals tracker's url_verifier.py (itself ported from
the carrier project), generalized for GOGPT plant/unit citations. The
soft-error title list is a generic set (paywall/SSO/Cloudflare/rate-limit
signals); nothing here is LNG-tracker-specific.

Fetching goes through the shared escalation ladder in fetch.py (2026-10-02):
curl with a browser UA, then curl_cffi browser-fingerprint impersonation on
any 401/403/429 or bot wall, then a real-Chrome clearance cookie for JS
challenges; sec.gov gets SEC's declared-identity User-Agent instead. PDFs
(regulator filings, permits, IR decks) are verified on their extracted text
(pdftotext -> pypdf -> OCR), zip bundles on their members' text. A PDF with
no recoverable text fails with a clear reason rather than a misleading
"missing expected content". A passing reason names any escalation used,
e.g. "OK (via cf_impersonate)".

Two modes:
  - strict=True: raises CitationError on failure (use in build scripts where
    a broken URL is a hard error)
  - strict=False: returns (False, reason) — caller drops the URL silently

A per-process cache prevents re-fetching the same URL multiple times in one
build. Clear between builds.

CLI usage:
    python url_verifier.py <url> <expected1> [<expected2> ...]
    # exits 0 if URL passes, 1 if not

Library usage:
    from url_verifier import verify_url, verify_and_format
    ok, reason = verify_url("https://...", ["Cheniere", "Sabine Pass", "23 MTPA"])
    url_or_none = verify_and_format(url, expected)

Audit log (optional): set env URL_VERIFIER_LOG=<path> or pass --log <path> on the
CLI to append one JSONL line per check ({ts, url, expected, ok, reason}). This is
the durable record of which URLs were verified with which tokens — without it a
batch's verification evidence lives only in scrollback.

Bot-block ≠ dead (Wayback fallback, the LAST rung): when the whole fetch.py
ladder still ends on a 401/403/429 — or a 200 serving a Cloudflare/paywall
interstitial — the page is LIVE but refusing bots, not gone. Dropping such a citation is a real-miss class. When the live fetch hits
one of these, the verifier now falls back to the newest Wayback Machine
snapshot and runs the same content check against it; a pass returns ok=True
with a reason string naming the snapshot, so a bot-blocked but value-verified
URL is a PASSING citation (keep the live URL in the cell — never cite the
web.archive.org address). Disable with wayback_fallback=False / --no-wayback.
"""
import json
import re
import os
import subprocess
import sys
import time
import urllib.parse

from fetch import _host_turn, fetch_page


class CitationError(Exception):
    pass


_CACHE = {}

# JSONL audit-log path; None = disabled. Set via URL_VERIFIER_LOG or --log.
_LOG_PATH = os.environ.get("URL_VERIFIER_LOG") or None


def set_log_path(path):
    """Enable/disable the JSONL audit log (None disables)."""
    global _LOG_PATH
    _LOG_PATH = path or None


def _log_check(url, expected, ok, reason):
    """Append one audit line; never let logging break verification."""
    if not _LOG_PATH:
        return
    try:
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "url": url,
            "expected": list(expected),
            "ok": ok,
            "reason": reason,
        }
        with open(_LOG_PATH, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError as e:
        print(f"  WARNING: url_verifier log write failed ({e}); continuing", file=sys.stderr)

_DEFAULT_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

# Soft-error signals: HTTP 200 but title indicates an error / paywall / SSO template
_SOFT_ERROR_TITLES = (
    "404", "429", "503",
    "not found", "page not found",
    "too many requests",
    "access denied", "forbidden",
    "temporarily unavailable",
    "just a moment",         # Cloudflare interstitial
    "attention required",    # Cloudflare block
    "sign in",               # paywall / SSO
    "log in to continue",
    "subscribe to continue",
    "members only",          # member-only portal redirect
    "login required",
    "this page is restricted",
)


def _fetch(url, timeout=30):
    """Fetch URL through the shared escalation ladder (fetch.py: curl ->
    curl_cffi browser-fingerprint impersonation -> real-Chrome clearance
    cookie; sec.gov gets SEC's declared-identity User-Agent). PDFs come back
    as extracted text (pdftotext -> pypdf -> OCR) and zip bundles as their
    members' text. Returns (status_code, body_text, is_pdf, notes); cached per
    URL per process. notes name the route a bot-walled page needed, so the OK
    reason records it."""
    if url in _CACHE:
        return _CACHE[url]
    page = fetch_page(url, timeout=timeout)
    result = (page.status, page.text, page.is_pdf, page.notes)
    _CACHE[url] = result
    return result


# Live-fetch outcomes that mean "bot-blocked, page presumptively live" — these
# route to the Wayback fallback instead of a hard fail.
_BOT_BLOCK_STATUSES = ("401", "403", "429")
# Outcomes that mean the live page is gone, moved, or the server is broken
# ("000" = no connection at all, e.g. a domain that no longer resolves). A
# person would open the archived copy, so these also try the Wayback copies,
# but a pass only names the archived address; the live url still fails.
_DEAD_STATUSES = ("000", "400", "404", "410", "500", "502", "503", "504", "520",
                  "521", "522", "523", "525", "526")
_BOT_BLOCK_TITLES = (
    "just a moment", "attention required", "access denied", "forbidden",
    "too many requests",
)


def _archive_get(api):
    """GET an archive.org lookup through the shared archive.org lock (parallel
    verifiers take turns, one second apart). Returns the body text, or None
    when the service refused or answered with its "Temporarily Offline" page."""
    try:
        with _host_turn("archive.org", 1.0):
            r = subprocess.run(["curl", "-sL", "-A", _DEFAULT_UA, "--max-time", "30", api],
                               capture_output=True, text=True, timeout=35)
    except subprocess.SubprocessError:
        return None
    out = r.stdout or ""
    if r.returncode != 0 or "Temporarily Offline" in out[:600] or out.lstrip().startswith("<"):
        return None
    return out


def _wayback_snapshots(url, limit=3):
    """Up to `limit` Wayback snapshots of `url` that differ in content, newest
    first, as [(snapshot_url, timestamp)]. "lookup-failed" when neither lookup
    service answered (not cached: an archived copy may exist). Cached per process.

    Two services, because each fails differently (October 2026): the
    availability API throttles (429) fully percent-encoded addresses and often
    reports nothing for addresses with a query string; the CDX index is more
    complete but goes "Temporarily Offline" for minutes at a time. Older
    captures matter because a page's numbers change: the value a source was
    cited for may only be on an earlier copy.
    """
    key = ("__wayback__", url, limit)
    if key in _CACHE:
        return _CACHE[key]
    light = urllib.parse.quote(url, safe=":/?=%~,+@;!$'()*")
    full = urllib.parse.quote(url, safe="")
    # The index is the authority on "no copy". An empty answer from the
    # availability service is not: it misses addresses the index has. So a
    # run ends with "none" only when the index itself answered.
    snaps, index_answered = [], False
    for round_no in range(4):
        out = _archive_get("http://web.archive.org/cdx/search/cdx?url=" + light
                           + "&filter=statuscode:200&collapse=digest"
                           + "&fl=timestamp,original&limit=-" + str(limit))
        if out is not None:
            index_answered = True
            for line in reversed(out.strip().splitlines()):
                ts, _, orig = line.partition(" ")
                if ts.isdigit() and orig:
                    snaps.append((f"https://web.archive.org/web/{ts}/{orig}", ts))
            break
        for api in ("https://archive.org/wayback/available?url=" + light,
                    "https://archive.org/wayback/available?url=" + full):
            out = _archive_get(api)
            try:
                data = json.loads(out) if out else None
            except ValueError:
                data = None
            if data is None:
                continue
            closest = (data.get("archived_snapshots") or {}).get("closest") or {}
            if closest.get("available") and closest.get("url"):
                u = closest["url"].replace("http://web.archive.org", "https://web.archive.org", 1)
                snaps.append((u, closest.get("timestamp", "")))
            break
        if snaps:
            break
        time.sleep(10 * 2 ** round_no)        # 10, 20, 40, 80 seconds
    if not snaps and not index_answered:
        return "lookup-failed"                 # not cached: a copy may exist
    _CACHE[key] = snaps
    return snaps


def _wayback_snapshot(url):
    """Newest snapshot as (snapshot_url, timestamp), (None, None) if there is
    none, or ("lookup-failed", None). Kept for callers of the old form."""
    snaps = _wayback_snapshots(url, limit=1)
    if snaps == "lookup-failed":
        return ("lookup-failed", None)
    return snaps[0] if snaps else (None, None)


_WS_RE = re.compile(r"\s+")


def _norm(s):
    """Lowercase and collapse every whitespace run to one space.

    PDF extraction wraps lines mid-phrase, so a token that IS present verbatim
    fails a raw substring match purely because pdftotext put a newline inside
    it -- a false FAIL on exactly the regulatory PDFs the SOP prefers as
    primary sources. Normalising both haystack and needle kills that class
    without loosening the match otherwise.
    """
    return _WS_RE.sub(" ", s).lower()


def _check_wayback(url, expected, require_all, live_reason, dead=False):
    """Archive fallback: run the content check against up to three Wayback
    snapshots, newest first. For a blocked live page (dead=False) a pass means
    the LIVE url stays citable. For a dead or moved page (dead=True) the live
    url is never citable, so the result is a FAIL that names the archived
    address carrying the value as a lead (the Update SOP never cites
    web.archive.org addresses)."""
    snaps = _wayback_snapshots(url)
    if snaps == "lookup-failed":
        return False, (f"{live_reason}; the Wayback lookup itself was refused, "
                       "so an archived copy may exist. Try again later")
    if not snaps:
        return False, f"{live_reason}; no Wayback snapshot to verify against"
    unavailable, checked = 0, []
    for snap_url, ts in snaps:
        status, text, _is_pdf, _notes = _fetch(snap_url)
        if status != "200" or "Temporarily Offline" in (text or "")[:3000]:
            unavailable += 1
            continue
        text_lower = _norm(text)
        missing = [s for s in expected if _norm(s) not in text_lower]
        found = [s for s in expected if _norm(s) in text_lower]
        if (require_all and missing) or (not require_all and not found):
            checked.append((ts, missing if require_all else expected))
            continue
        if dead:
            return False, (f"{live_reason}; the live page is gone, but the archived copy "
                           f"{snap_url} still shows the value. Use it as a lead to a live "
                           f"source; citing an archived address is not an approved route")
        return True, (f"bot-blocked live ({live_reason}); value verified via "
                      f"Wayback snapshot {ts}")
    if not checked:
        return False, (f"{live_reason}; the Wayback snapshots could not be read "
                       f"(archive unavailable). Try again later")
    ts, miss = checked[0]
    more = f" and {len(checked) - 1} older snapshot(s)" if len(checked) > 1 else ""
    return False, (f"{live_reason}; Wayback snapshot {ts}{more} missing expected "
                   f"content: {miss}")


def verify_url(url, expected, strict=False, require_all=True, wayback_fallback=True,
               timeout=30):
    """Verify URL passes three checks:
      1. HTTP 200
      2. Not a soft-error page
      3. Body contains the strings in `expected` (case-insensitive)

    A bot-blocked live page (401/403/429, or a 200 Cloudflare/paywall
    interstitial) is NOT treated as dead when wayback_fallback is on: the same
    content check runs against the newest Wayback snapshot, and a pass counts
    as verification of the live URL (bot-block ≠ dead).

    Args:
      url: the URL to verify
      expected: list of substrings that must appear in the page body.
                For GOGPT: typically [PlantName, Owner, value-being-cited]
      strict: raise CitationError on failure instead of returning False
      require_all: every expected substring must be present (default True)
      wayback_fallback: on bot-block, verify against the newest Wayback snapshot
      timeout: seconds per fetch; raise it for very large files (the 22 MB PJM
               queue XML takes ~30 s)

    Returns: (ok: bool, reason: str)
    """
    ok, reason = _check(url, expected, require_all, wayback_fallback, timeout)
    _log_check(url, expected, ok, reason)
    if not ok and strict:
        raise CitationError(f"URL failed verification ({reason}): {url}")
    return ok, reason


def _check(url, expected, require_all, wayback_fallback=True, timeout=30):
    """The three checks; returns (ok, reason) with no side effects."""
    status, text, is_pdf, notes = _fetch(url, timeout)

    if status != "200":
        if wayback_fallback and status in _BOT_BLOCK_STATUSES:
            return _check_wayback(url, expected, require_all, f"HTTP {status}")
        # A web firewall that answers with an error status and a page saying the
        # request was blocked (hamburger-energiewerke.de sends HTTP 500 with
        # "The URL you requested has been blocked") is a block, not a dead link.
        if wayback_fallback and re.search(
                r"<title>[^<]*(URL you requested has been blocked|Request Rejected)",
                text or "", re.I):
            return _check_wayback(url, expected, require_all,
                                  f"HTTP {status} firewall block page")
        if wayback_fallback and status in _DEAD_STATUSES:
            # Gone, moved, or the server is broken: a person would open the
            # archived copy, so look for one that carries the value.
            return _check_wayback(url, expected, require_all, f"HTTP {status}", dead=True)
        return False, f"HTTP {status}"

    if "empty_answer" in (notes or []) and not all(_norm(s) in _norm(text) for s in expected):
        # The server's "no record" template: either the record was taken down
        # or a loaded register sent it for a real record. Not evidence either way.
        return False, ('empty record page: the server showed its "no details" '
                       "template. The record may have been taken down, or the server "
                       "was under load. Try again later, and look for the documents "
                       "by their own addresses")

    if is_pdf:
        # No HTML <title> to soft-error-check; require a usable text layer instead.
        if not text.strip():
            return False, ("PDF has no extractable text (scanned/image PDF, or the "
                           "poppler pdftotext CLI is unavailable)")
    else:
        # Soft-error detection via title (HTML only)
        title_match = re.search(r"<title[^>]*>([^<]+)</title>", text, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).lower()
            for bad in _SOFT_ERROR_TITLES:
                # status codes only as whole numbers: a parcel "Flur-Nr. 2404"
                # or a postcode in a permit notice's title is not a 404
                hit = (re.search(rf"(?<![\d.,]){bad}(?![\d.,])", title) if bad.isdigit()
                       else bad in title)
                if hit:
                    reason = f"soft-error page (title: {title_match.group(1).strip()!r})"
                    if wayback_fallback and any(b in title for b in _BOT_BLOCK_TITLES):
                        # Bot-wall/paywall interstitial served as 200 — same
                        # bot-block ≠ dead treatment as a 401/403.
                        return _check_wayback(url, expected, require_all, reason)
                    return False, reason

    # Content check
    text_lower = _norm(text)
    found = [s for s in expected if _norm(s) in text_lower]
    missing = [s for s in expected if _norm(s) not in text_lower]

    if require_all and missing:
        return False, f"missing expected content: {missing}"
    if not require_all and not found:
        return False, f"none of expected content found: {expected}"

    route = [n for n in notes if n in ("cf_impersonate", "cf_clearance", "browser_render",
                                       "sec_declared_ua", "pdf_ocr", "insecure_tls",
                                       "rate_limit_wait", "disk_cache")]
    return True, f"OK (via {', '.join(route)})" if route else "OK"


def verify_and_format(url, expected):
    """Verify a URL. If it passes, return the URL. If not, return None.
    Logs the failure reason to stderr.
    """
    ok, reason = verify_url(url, expected, strict=False)
    if ok:
        return url
    print(f"  [CITATION DROPPED] {url}\n    reason: {reason}", file=sys.stderr)
    return None


def clear_cache():
    """Clear the in-memory cache. Call between builds."""
    _CACHE.clear()


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    if "--log" in argv:
        i = argv.index("--log")
        try:
            set_log_path(argv[i + 1])
        except IndexError:
            print("Usage: python url_verifier.py [--log <path>] [--no-wayback] <url> [<expected1> ...]")
            sys.exit(2)
        del argv[i:i + 2]
    timeout = 30
    if "--timeout" in argv:
        i = argv.index("--timeout")
        try:
            timeout = int(argv[i + 1])
        except (IndexError, ValueError):
            print("Usage: python url_verifier.py [--log <path>] [--no-wayback] [--timeout <s>] <url> [<expected1> ...]")
            sys.exit(2)
        del argv[i:i + 2]
    wayback = True
    if "--no-wayback" in argv:
        wayback = False
        argv.remove("--no-wayback")
    if len(argv) < 1:
        print("Usage: python url_verifier.py [--log <path>] [--no-wayback] [--timeout <s>] <url> [<expected1> <expected2> ...]")
        sys.exit(2)
    url = argv[0]
    expected = argv[1:]
    ok, reason = verify_url(url, expected, strict=False, require_all=True,
                            wayback_fallback=wayback, timeout=timeout)
    print(f"  URL: {url}")
    print(f"  Expected: {expected}")
    print(f"  Result: {'PASS' if ok else 'FAIL'}  ({reason})")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

"""
Access audit: which sources a batch could not read, why, and whether the
current fetch ladder gets them now.

Every research batch logs each URL check to `shards/*.urls.jsonl`, and fetch.py
logs every read it could not finish to `work/fetch_failures.jsonl`. This script
reads both (latest result per URL; fetch failures from the batch's run window
that no citation check saw), sorts each failure into an access
class, and prints a per-host table with the route `fetch.py` has learned for
that host. With `--retry` it re-runs the failures through the verifier as it is
today (the full ladder plus the archive fallback) and reports what changed.
With `--render-missing` it also reopens pages that loaded but lacked the
expected value in a real Chrome, which catches pages that fill in their text
with JavaScript.

Use it at the end of a batch and whenever a new country starts: the classes say
what kind of fix each host needs, and the results feed the per-country access
notes and docs/reference/site_access.md.

    python scripts/access_audit.py ../batches/germany            # table only
    python scripts/access_audit.py ../batches/germany --retry    # re-run failures
    python scripts/access_audit.py ../batches/germany --retry --render-missing \
        --out ../batches/germany/access_audit.md
    python scripts/access_audit.py --routes                      # learned routes

Access classes (what a person would do differs for each):
  rate_limited      HTTP 429 that outlasted the waits. Retry later; fetch.py paces it.
  bot_wall          401/403/406 or a challenge page. The ladder (impersonation,
                    clearance cookie, Chrome render) should pass it; if not, archive.
  firewall          a block page even real Chrome gets (geographic or IP filter).
                    Archive, or an in-country connection via https_proxy.
  gone              404/410 or a "page not found" page. Archive, or search the
                    site for the moved page. Official notices are often withdrawn
                    after the display period; look for the permit register copy.
  dead_host         no connection at all (domain gone, DNS failure). Archive.
  server_error      400/5xx. Try again later; if it persists, find the new address.
  empty_record      a 200 that is the site's "no record" template (uvp-verbund.de's
                    "Keine Detailinformationen"). Taken down, or sent under load.
                    Retry later; fetch the documents by their own addresses.
  pdf_no_text       a scanned PDF and OCR found nothing. Check the OCR language packs.
  archive_refused   the archive lookup itself failed. Try again later.
  value_missing     the page loaded but the claimed value is not on it. Usually a
                    research question, sometimes a page that loads text with
                    JavaScript (see --render-missing).
"""
import argparse
import json
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fetch  # noqa: E402

CLASSES = ("rate_limited", "bot_wall", "firewall", "gone", "dead_host", "server_error",
           "empty_record", "pdf_no_text", "archive_refused", "value_missing", "other")


def classify(reason: str) -> str:
    r = reason or ""
    if "Wayback lookup itself was refused" in r or "archive unavailable" in r:
        return "archive_refused"
    if r.startswith("empty record page"):
        return "empty_record"
    if "firewall block page" in r:
        return "firewall"
    m = re.match(r"(?:bot-blocked live \()?HTTP (\d{3})", r)
    code = m.group(1) if m else ""
    if code == "429":
        return "rate_limited"
    if code in ("401", "403", "406"):
        return "bot_wall"
    if code in ("404", "410") or "soft-error page" in r:
        return "gone"
    if code == "000":
        return "dead_host"
    if code.startswith("5") or code == "400":
        return "server_error"
    if r.startswith("PDF has no extractable text"):
        return "pdf_no_text"
    if "missing expected content" in r or "none of expected content" in r:
        return "value_missing"
    return "other"


def load_failures(batch_dirs: list[Path]) -> dict[str, dict]:
    """Latest logged result per URL across the batches; failures only. Adds
    the reads fetch.py logged as failed while the batch ran (from its briefs'
    timestamp on) that the verifier logs never saw: pages a research agent
    tried to open and gave up on, which no citation check records."""
    latest = _verifier_results(batch_dirs)
    failed = {u: r for u, r in latest.items() if not r.get("ok")}
    for url, rec in _fetch_failures(batch_dirs).items():
        if url not in latest:
            failed[url] = rec
    return failed


def _fetch_failures(batch_dirs: list[Path]) -> dict[str, dict]:
    starts = [p.stat().st_mtime for d in batch_dirs for p in (d / "briefs").glob("*")]
    if not starts or not fetch.FAIL_LOG.exists():
        return {}
    since = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(min(starts)))
    out: dict[str, dict] = {}
    for line in fetch.FAIL_LOG.read_text(errors="replace").splitlines():
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if rec.get("ts", "") < since or not rec.get("url"):
            continue
        reason = ("empty record page" if "empty_answer" in rec.get("notes", []) else f"HTTP {rec.get('status')}")
        out[rec["url"]] = {"url": rec["url"], "ok": False, "reason": reason,
                           "expected": [], "ts": rec["ts"], "source": "fetch"}
    return out


def _verifier_results(batch_dirs: list[Path]) -> dict[str, dict]:
    latest: dict[str, dict] = {}
    for d in batch_dirs:
        for f in sorted(d.glob("**/*.urls.jsonl")):
            for line in f.read_text(errors="replace").splitlines():
                try:
                    rec = json.loads(line)
                except ValueError:
                    continue
                url = rec.get("url")
                if url and rec.get("ts", "") >= latest.get(url, {}).get("ts", ""):
                    latest[url] = rec
    return latest


def host_of(url: str) -> str:
    return (urlsplit(url).hostname or "").lower()


def retry(failures: dict[str, dict], render_missing: bool) -> dict[str, tuple[bool, str]]:
    from url_verifier import verify_url
    out = {}
    for n, (url, rec) in enumerate(sorted(failures.items()), 1):
        expected = rec.get("expected") or []
        print(f"  [{n}/{len(failures)}] {url[:100]}", file=sys.stderr)
        if rec.get("source") == "fetch":         # a page read, no value to check
            page = fetch.fetch_page(url)
            ok = page.status == "200" and "empty_answer" not in page.notes
            out[url] = (ok, "OK" if ok else (
                "empty record page" if "empty_answer" in page.notes else f"HTTP {page.status}"))
            continue
        try:
            ok, reason = verify_url(url, expected)
        except Exception as e:          # one bad page must not stop the audit
            ok, reason = False, f"error: {e}"
        if not ok and render_missing and classify(reason) == "value_missing":
            page = fetch.fetch_page(url, force_render=True)
            text = re.sub(r"\s+", " ", page.text or "").lower()
            if page.status == "200" and expected and all(
                    re.sub(r"\s+", " ", e).lower() in text for e in expected):
                ok, reason = True, "value found once the page ran its scripts in Chrome"
        out[url] = (ok, reason)
    return out


def report(failures: dict[str, dict], retried: dict | None) -> str:
    routes = fetch._load_routes()
    by_host: dict[str, list[str]] = defaultdict(list)
    for url in failures:
        by_host[host_of(url)].append(url)
    lines = ["# Access audit", ""]
    totals = Counter(classify(r["reason"]) for r in failures.values())
    lines.append(f"Failed checks in the batch logs: {len(failures)}")
    lines += [f"- {c}: {totals[c]}" for c in CLASSES if totals[c]]
    if retried is not None:
        fixed = sum(ok for ok, _ in retried.values())
        lines.append(f"- passing now with the current ladder: {fixed}")
        now = Counter(classify(r) for ok, r in retried.values() if not ok)
        lines.append("- still failing, by class: "
                     + (", ".join(f"{c} {now[c]}" for c in CLASSES if now[c]) or "none"))
    lines += ["", "| Host | Failed | Classes then | Now | Learned route |",
              "|---|---|---|---|---|"]
    for host, urls in sorted(by_host.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        then = Counter(classify(failures[u]["reason"]) for u in urls)
        now = "not retried"
        if retried is not None:
            still = Counter(classify(retried[u][1]) for u in urls if not retried[u][0])
            passed = sum(retried[u][0] for u in urls)
            now = ", ".join([f"{passed} pass"] * bool(passed)
                            + [f"{c} {k}" for c, k in still.items()]) or "-"
        lines.append(f"| {host} | {len(urls)} | "
                     + ", ".join(f"{c} {k}" for c, k in then.items())
                     + f" | {now} | {(routes.get(host) or {}).get('route', '')} |")
    if retried is not None:
        lines += ["", "## Each failure now", ""]
        for url in sorted(retried):
            ok, reason = retried[url]
            lines.append(f"- {'PASS' if ok else classify(reason)}: {url}  \n  {reason}")
    return "\n".join(lines) + "\n"


def print_routes() -> None:
    routes = fetch._load_routes()
    if not routes:
        print(f"No learned routes yet ({fetch.ROUTES_PATH}).")
        return
    print(f"{'host':40} {'route':16} {'last ok':11} successes")
    for host, e in sorted(routes.items()):
        print(f"{host:40} {e.get('route', ''):16} {e.get('last_ok', ''):11} "
              f"{e.get('successes', '')}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("batches", nargs="*", type=Path, help="batch directories")
    ap.add_argument("--retry", action="store_true", help="re-run each failure now")
    ap.add_argument("--render-missing", action="store_true",
                    help="with --retry, reopen value-missing pages in Chrome")
    ap.add_argument("--host", help="only URLs on this host (substring match)")
    ap.add_argument("--out", type=Path, help="also write the report to this markdown file")
    ap.add_argument("--routes", action="store_true", help="print the learned routes and exit")
    a = ap.parse_args(argv)
    if a.routes or not a.batches:
        print_routes()
        return 0
    failures = load_failures(a.batches)
    if a.host:
        failures = {u: r for u, r in failures.items() if a.host in host_of(u)}
    retried = retry(failures, a.render_missing) if a.retry else None
    text = report(failures, retried)
    print(text)
    if a.out:
        a.out.write_text(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

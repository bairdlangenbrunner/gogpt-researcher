"""Shared parts of the scope harvesters (scopes/<tag>/harvest_permits.py, harvest_psc.py and the
scope queue readers). A scope's own file keeps only its portal logic: the site's search calls,
its page parsers, its name patterns and its hand-checked KNOWN table. Everything here is the same
for every scope.

    from harvest_lib import REPO, CSV, get, clean, pick, wayback_url, harvest_out

A harvester in scopes/<tag>/ puts scripts/ on sys.path first:

    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

Output folders come from paths.py: harvest_out(scope) is scopes/<tag>/work/permits/ (the plain-text
per-plant indexes the sweep agents read), scope_work(scope) / "psc" the docket document cache.
Nothing here is cited; it fetches and reads.
"""
from __future__ import annotations

import re
import time
from pathlib import Path

import html
import requests

from fetch import fetch_page
from paths import REPO_ROOT, gogpt_scoped_csv, scope_permits, scope_work

REPO = REPO_ROOT
CSV = gogpt_scoped_csv()
CDX = "http://web.archive.org/cdx/search/cdx"

# Size and maker patterns. SIZE is the permit-document form (engine and boiler ratings in hp and
# MMBtu too); DOCKET_SIZE and DOCKET_MAKER are the commission-filing forms, which name turbine
# models and stay in MW.
SIZE = re.compile(r"\d[\d,.]*\s*(MW|MWe|megawatt|kW|kilowatt|MMBtu|mmbtu|hp|horsepower|bhp)\b")
DOCKET_SIZE = re.compile(r"\d[\d,.]*\s*(MW|MWe|megawatt|MWac|kW)\b", re.I)
DOCKET_MAKER = re.compile(r"general electric|\bGE\b|siemens|mitsubishi|solar turbines|wartsila|w[äa]rtsil[äa]|"
                          r"rolls[- ]royce|caterpillar|pratt|hitachi|ansaldo|\b7H[AF]\b|7HA|7FA|SGT[- ]?\d|"
                          r"\bM501|\bLM ?\d{4}|\b501[GJ]|\b6B\b|titan \d|model\b|manufactur", re.I)
YEAR = re.compile(r"\b20[2-5]\d\b")


def harvest_out(scope: str) -> Path:
    """Where a permit harvester writes: scopes/<tag>/work/permits/ (never the older work/permits/)."""
    d = scope_permits(scope, legacy=False)
    d.mkdir(parents=True, exist_ok=True)
    return d


def docket_cache(scope: str) -> Path:
    """Where a docket harvester keeps the documents it read (never committed)."""
    d = scope_work(scope) / "psc"
    d.mkdir(parents=True, exist_ok=True)
    return d


# ---------------------------------------------------------------- fetch ---

def get(url, timeout=120):
    """One page through fetch.py's whole access ladder."""
    return fetch_page(url, timeout=timeout)


def wayback_url(url):
    """Newest saved copy of an address (id_ form, so the original bytes), or ''."""
    for i in range(3):
        try:
            r = requests.get(CDX, params={"url": url.split("://", 1)[-1], "output": "json",
                                          "fl": "timestamp,original", "filter": "statuscode:200",
                                          "limit": 5}, timeout=120)
            rows = r.json()[1:]
            if not rows:
                return ""
            ts, orig = max(rows)
            return f"https://web.archive.org/web/{ts}id_/{orig}"
        except (requests.RequestException, ValueError):
            time.sleep(8 * (i + 1))
    return ""


# ----------------------------------------------------------------- text ---

def clean(s):
    """HTML to one line of plain text."""
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s or "", flags=re.S | re.I)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def clean_ws(s):
    return re.sub(r"\s+", " ", str(s or "")).strip()


def norm_county(s):
    """'Madison County' / 'madison' / 'Jackson County, MS' -> 'madison';
    "Prince George's" and 'St. Clair' match 'Prince Georges' and 'St Clair'."""
    s = re.sub(r",.*$", "", str(s or "")).strip().lower()
    s = re.sub(r"\s+", " ", re.sub(r"['\u2019.]", "", s))
    return re.sub(r"\s+(county|cnty)$", "", s).strip()


def lines_of(text):
    return [re.sub(r"\s+", " ", ln).strip() for ln in text.splitlines()]


def pick(text, rx, limit, lo=12, hi=260):
    """Up to `limit` distinct document lines that match rx (permit documents)."""
    out = []
    for s in lines_of(text):
        if rx.search(s) and lo < len(s) < hi and s not in out:
            out.append(s)
            if len(out) >= limit:
                break
    return out


def sentences(text):
    """A filing's text as sentences (hyphenated line breaks joined)."""
    t = re.sub(r"-\n(?=[a-z])", "", text)
    t = re.sub(r"\s+", " ", t)
    return [s.strip() for s in re.split(r"(?<=[.;:!?])\s+(?=[A-Z(\"])", t) if s.strip()]


def merge_facts(parts):
    """Facts from several documents, each key's lines kept once in order, 14 at most."""
    out = {}
    for f in parts:
        for k, v in f.items():
            cur = out.setdefault(k, [])
            for x in v:
                if x not in cur:
                    cur.append(x)
    return {k: v[:14] for k, v in out.items()}

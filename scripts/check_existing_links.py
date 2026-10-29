"""Check every Data Source link already in the GEM export for a scope, before the sweep.

A link that is gone from its old address (Kansas, 2026-10-23: 138 links, 95 of them on
the state health department's site) is cheaper to deal with up front than after the
plant agents have run. This script:

  1. reads the fresh scoped export for a state or a country,
  2. splits every Data Source cell (every column ending in "Data Source", except the
     hydrogen columns in schema_constants.OUT_OF_SCOPE_COLUMNS) into addresses and
     lists each distinct address once, with the units and columns it backs,
  3. checks each address through the repo's access ladder (fetch.py: curl, browser
     fingerprint, Chrome clearance; sec.gov gets its declared identity),
  4. for an address that is gone, looks for saved copies at the Internet Archive for
     the exact address and reads them against the plant name and the value the box
     supports (url_verifier.verify_url),
  5. when a saved copy shows the value, writes one unchanged-value record per unit and
     column into staging/staged_updates.json. The record adds the web.archive.org
     address; the build merges it with the links already in the box, and the old
     link stays (Data Source cells merge, never replace),
  6. lists every other gone link, and every gone link whose saved copy does not show
     the value, so the brief can tell the plant agent to find a replacement source.

A page that refuses bots (401, 403, 429, a firewall page) is not gone; it is listed
as "blocked" for the sweep's normal route, never as dead.

    python check_existing_links.py --state Mississippi
    python check_existing_links.py --country Germany --dry-run

Writes batches/<tag>/existing_links.json and existing_links.md (tag us-<postal> for a
state, the country slug for a country; --batch overrides). --dry-run writes only
those two files and never touches staging. The rest of the run is polite: modest
concurrency, one request at a time per host with a gap, and a seven-day cache of each
address's outcome in work/existing_links_cache.json (--refresh ignores it).

Run it right after the brief step. build_state_brief.py --existing-links <that json>
adds a short section to each affected plant's brief. assemble_state.py writes
staged_updates.json fresh from the shards, so run this script again after the
assembler (the cache makes that free) to put the saved-copy records into staging.
Safe to re-run: records are keyed on record_id and never duplicated.

This supersedes stage_saved_copies.py, which held the Kansas items by hand.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from itertools import zip_longest
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
import url_verifier  # noqa: E402
from access_audit import classify  # noqa: E402
from build_state_brief import make_scope  # noqa: E402
from fetch import _host_turn  # noqa: E402
from paths import REPO_ROOT, gogpt_scoped_csv, require_fresh_export, work_dir  # noqa: E402
from schema_constants import OUT_OF_SCOPE_COLUMNS  # noqa: E402

H_LOC, H_PLANT = "GEM location ID", "Plant name"
H_UNIT, H_UNAME = "GEM unit ID", "Unit name"
CACHE_DAYS = 7
HOST_GAP = 0.5            # seconds between requests to one host
WORKERS = 6
OUTPUTS = ("existing_links.json", "existing_links.md")

# Data Source column -> the value column it supports
VALUE_COLUMN = {
    "Fuel Data Source": "Fuel",
    "Capacity Data Source": "Capacity (MW)",
    "Status Data Source": "Status",
    "Disrupted by conflict Data Source": "Disrupted by conflict",
    "Latest Activity Data Source": "Latest Activity",
    "Cancellation year Data Source": "Cancellation year",
    "Turbine/Engine Technology Data Source": "Turbine/Engine Technology",
    "Turbine/Engine Equipment Data Source": "Equipment Manufacturer/Model",
    "CHP Data Source": "CHP",
    "CCS Data Source": "CCS attachment?",
    "Conversion/replacement Data Source": "Conversion/replacement?",
    "Start Year Data Source": "Start year",
    "Retired Year Data Source": "Retired year",
    "Planned Retire Data Source": "Planned retire",
    "Operators Data Source": "Operator(s)",
    "Owners Data Source": "Owner(s)",
    "Location Data Source": "Location accuracy",
    "Captive Data Source": "Captive industry use",
    "Backup Power Data Source": "Backup Power",
    "Employment Notes Data Source": "Employment Notes",
}
# value columns whose text a saved copy can be read against
CHECKABLE = {"Fuel", "Capacity (MW)", "Status", "Cancellation year", "Turbine/Engine Technology",
             "Equipment Manufacturer/Model", "Start year", "Retired year", "Planned retire",
             "Operator(s)", "Owner(s)"}
AFTER_COLON = {"Fuel", "Equipment Manufacturer/Model", "Turbine/Engine Technology"}
GENERIC = {"power", "station", "plant", "energy", "center", "centre", "generating", "generation",
           "facility", "project", "electric", "the", "of", "and", "unit", "units", "cogeneration",
           "solar", "gas", "turbine", "combined", "cycle", "company", "co", "llc", "inc", "corp",
           "complex", "site", "works", "works", "cc", "ct", "gt", "data", "center", "peaking"}

URL_RX = re.compile(r"https?://\S+?(?=[;,]\s*https?://|[;\s]|$)")
ROUTE_NOTES = ("cf_impersonate", "cf_clearance", "browser_render", "sec_declared_ua",
               "rate_limit_wait")
WAYBACK = "web.archive.org/web/"
SIGN_IN_HOSTS = {"drive.google.com", "docs.google.com"}


# ------------------------------------------------------------------ reading
def ws(v):
    return (v or "").strip()


def split_urls(cell: str) -> list[str]:
    """The web addresses in a Data Source cell (separated by ';', or ',' before the next http)."""
    return [u.rstrip(",;") for u in URL_RX.findall(cell or "")]


def source_columns(header: list[str]) -> list[str]:
    return [h for h in header if h.endswith("Data Source") and h not in OUT_OF_SCOPE_COLUMNS]


def read_scope(scope: dict, csv_path: Path) -> tuple[list[dict], list[str]]:
    rows = []
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        header = rd.fieldnames or []
        for r in rd:
            if scope["kind"] == "state":
                if (ws(r.get("Country/Area")).lower() != "united states"
                        or ws(r.get("State/Province")).lower() != scope["name"].lower()):
                    continue
            elif ws(r.get("Country/Area")).lower() != scope["country"].lower():
                continue
            rows.append(r)
    return rows, header


def collect(rows: list[dict], header: list[str]) -> dict[str, list[dict]]:
    """{address: [usage, ...]}: each unit row and Data Source column that holds it."""
    cols = source_columns(header)
    out: dict[str, list[dict]] = {}
    for r in rows:
        for col in cols:
            seen = set()
            for u in split_urls(r.get(col, "")):
                if u in seen:
                    continue
                seen.add(u)
                vcol = VALUE_COLUMN.get(col, "")
                out.setdefault(u, []).append({
                    "plant_id": ws(r.get(H_LOC)), "plant_name": ws(r.get(H_PLANT)),
                    "unit_id": ws(r.get(H_UNIT)), "unit_name": ws(r.get(H_UNAME)),
                    "ds_column": col, "value_column": vcol, "value": ws(r.get(vcol)) if vcol else ""})
    return out


# ------------------------------------------------------------------ what a copy must hold
def name_word(plant_name: str) -> str:
    """The first word of the plant name that is not generic ('Viola' from 'Viola Generating Station')."""
    base = re.sub(r"\([^)]*\)", " ", plant_name or "")
    tokens = [t for t in re.findall(r"[A-Za-z0-9][A-Za-z0-9'&.-]*", base)]
    for t in tokens:
        if t.lower().strip(".") not in GENERIC and len(t) >= 3:
            return t
    return tokens[0] if tokens else ""


def value_words(value_col: str, value: str) -> list[str]:
    """What the saved copy must say about the value; [] when the value cannot be read
    against a page (a yes/no box, a date, an inferred status)."""
    v = ws(value)
    if not v or value_col not in CHECKABLE:
        return []
    if value_col == "Status" and "inferred" in v.lower():
        return []
    if value_col in AFTER_COLON and ":" in v:
        v = v.rsplit(":", 1)[1].strip()
    if value_col in ("Owner(s)", "Operator(s)"):
        v = re.sub(r"\[[^\]]*\]", "", v.split(";")[0]).strip()
    if value_col in ("Capacity (MW)", "Start year", "Retired year", "Planned retire",
                     "Cancellation year") and re.fullmatch(r"\d+\.0+", v):
        v = v.split(".")[0]
    return [v] if v else []


def record_id(plant_id: str, unit_id: str, value_col: str) -> str:
    slug = value_col.lower().replace("(", "").replace(")", "").replace("/", "-").replace(" ", "-")
    return f"{plant_id}:{unit_id}:{slug}-saved-copy"


# ------------------------------------------------------------------ checking
def host_of(url: str) -> str:
    try:
        return (urlsplit(url).hostname or "").lower()
    except ValueError:
        return ""


def check_live(url: str) -> dict:
    """Live status through the repo ladder. status: live | dead | blocked | unclear."""
    with _host_turn("links-" + host_of(url), HOST_GAP):
        _status, _text, _pdf, notes = url_verifier._fetch(url)
    ok, reason = url_verifier._check(url, [], True, wayback_fallback=False)
    klass = "ok" if ok else classify(reason)
    if not ok and host_of(url) in SIGN_IN_HOSTS:
        klass = "sign_in"               # a private Drive link answers 404 to a visitor
    elif not ok and reason.startswith("HTTP 402"):
        klass = "bot_wall"              # a paywall: the page is there, we are not let in
    if ok or klass == "pdf_no_text":
        status = "live"
    elif klass in ("gone", "dead_host"):
        status = "dead"
    elif klass in ("bot_wall", "rate_limited", "firewall", "sign_in"):
        status = "blocked"
    else:
        status = "unclear"
    route = next((n for n in ROUTE_NOTES if n in (notes or [])), "")
    return {"status": status, "class": klass, "reason": reason, "route": route}


def find_snapshots(url: str) -> tuple[list[dict], str]:
    """Up to three saved copies of the exact address: ([{url, timestamp}], lookup) where
    lookup is 'found', 'none' or 'refused'."""
    if WAYBACK in url:
        return [], "none"
    snaps = url_verifier._wayback_snapshots(url, limit=3)
    if snaps == "lookup-failed":
        return [], "refused"
    return [{"url": u, "timestamp": ts} for u, ts in snaps], ("found" if snaps else "none")


def read_snapshot(snap_url: str, words: list[str]) -> tuple[bool, str]:
    with _host_turn("links-web.archive.org", HOST_GAP):
        return url_verifier.verify_url(snap_url, words, wayback_fallback=False)


class Cache:
    """work/existing_links_cache.json: {address: {...outcome, "checked": iso}} plus read results."""

    def __init__(self, path: Path, refresh: bool):
        self.path, self.refresh = path, refresh
        self.data = {"urls": {}, "reads": {}}
        if path.exists() and not refresh:
            try:
                self.data = json.loads(path.read_text(encoding="utf-8"))
            except ValueError:
                pass

    @staticmethod
    def _fresh(entry) -> bool:
        try:
            return (dt.datetime.now() - dt.datetime.fromisoformat(entry["checked"])
                    ) < dt.timedelta(days=CACHE_DAYS)
        except (KeyError, TypeError, ValueError):
            return False

    def url(self, u):
        e = self.data["urls"].get(u)
        return e if e and self._fresh(e) else None

    def put_url(self, u, entry):
        if entry.get("lookup") == "refused" or entry.get("status") in ("unclear", "blocked"):
            return                      # worth another try next run
        self.data["urls"][u] = {**entry, "checked": dt.datetime.now().isoformat(timespec="seconds")}

    def read(self, snap, words):
        e = self.data["reads"].get(snap + "|" + "|".join(words))
        return e if e and self._fresh(e) else None

    def put_read(self, snap, words, ok, why):
        if not ok and ("unavailable" in why or "refused" in why or "Temporarily Offline" in why):
            return
        self.data["reads"][snap + "|" + "|".join(words)] = {
            "ok": ok, "reason": why, "checked": dt.datetime.now().isoformat(timespec="seconds")}

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=1, ensure_ascii=False), encoding="utf-8")


def check_address(url: str, cache: Cache) -> dict:
    hit = cache.url(url)
    if hit:
        return {k: v for k, v in hit.items() if k != "checked"}
    out = check_live(url)
    out.update({"snapshots": [], "lookup": ""})
    if out["status"] == "dead":
        out["snapshots"], out["lookup"] = find_snapshots(url)
    cache.put_url(url, out)
    return out


def read_usage(usage: dict, snaps: list[dict], cache: Cache) -> dict:
    """Read the saved copies against this usage's plant name and value. Returns the usage's
    saved-copy result: {snapshot, ok, reason, checked: bool}."""
    words = value_words(usage["value_column"], usage["value"])
    name = name_word(usage["plant_name"])
    if not words or not name or not snaps:
        why = ("no saved copy" if not snaps else
               "the value cannot be read against a page (a yes or no box, a date or an inferred status)")
        return {"snapshot": "", "ok": False, "reason": why, "checked": False}
    need = [name] + words
    last = ""
    for s in snaps:
        hit = cache.read(s["url"], need)
        ok, why = (hit["ok"], hit["reason"]) if hit else read_snapshot(s["url"], need)
        if not hit:
            cache.put_read(s["url"], need, ok, why)
        if ok:
            return {"snapshot": s["url"], "ok": True, "reason": why, "checked": True, "words": need}
        last = why
    return {"snapshot": snaps[0]["url"], "ok": False, "reason": last, "checked": True, "words": need}


def interleave(urls: list[str]) -> list[str]:
    """Round-robin by host so one big host does not tie up every worker."""
    by_host: dict[str, list[str]] = {}
    for u in urls:
        by_host.setdefault(host_of(u), []).append(u)
    return [u for grp in zip_longest(*by_host.values()) for u in grp if u]


def run_checks(usage_map: dict[str, list[dict]], cache: Cache, workers: int = WORKERS) -> list[dict]:
    order = interleave(sorted(usage_map))
    done = {}

    def one(u):
        try:
            res = check_address(u, cache)
        except Exception as e:                      # one bad address must not stop the run
            res = {"status": "unclear", "class": "other", "reason": f"check failed: {e}",
                   "route": "", "snapshots": [], "lookup": ""}
        usages = []
        for use in usage_map[u]:
            entry = dict(use)
            if res["status"] == "dead":
                entry["saved_copy"] = read_usage(use, res["snapshots"], cache)
            usages.append(entry)
        return u, res, usages

    with ThreadPoolExecutor(max_workers=workers) as ex:
        for i, (u, res, usages) in enumerate(ex.map(one, order), 1):
            done[u] = (res, usages)
            if i % 25 == 0:
                print(f"  checked {i}/{len(order)}", file=sys.stderr)
    out = []
    for u in sorted(done):
        res, usages = done[u]
        item = {"url": u, "host": host_of(u), "status": res["status"], "class": res["class"],
                "reason": res["reason"], "route": res["route"],
                "snapshots": res.get("snapshots", []), "lookup": res.get("lookup", ""),
                "usages": usages}
        if res["status"] == "dead":
            good = [x for x in usages if x["saved_copy"]["ok"]]
            item["verified"] = bool(good)
            item["snapshot"] = (good[0]["saved_copy"]["snapshot"] if good else
                                (res["snapshots"][0]["url"] if res["snapshots"] else ""))
        out.append(item)
    return out


# ------------------------------------------------------------------ staging
def saved_copy_note(item: dict, use: dict) -> str:
    return (f"The value is unchanged. The source box already holds a link to a page that is gone "
            f"from its old address ({item['url']}). The Internet Archive kept a saved copy of that "
            "page, which was read and states the value. The saved copy is added to the box next "
            "to the old link.")


def make_record(item: dict, use: dict, scope: dict) -> dict:
    col, vcol, val = use["ds_column"], use["value_column"], use["value"]
    snap = use["saved_copy"]["snapshot"]
    return {
        "gem_unit_id": use["unit_id"], "gem_plant_id": use["plant_id"],
        "plant_name": use["plant_name"], "unit_name": use["unit_name"],
        "country": scope["country"], "record_id": record_id(use["plant_id"], use["unit_id"], vcol),
        "cluster": use["unit_id"], "verdict": "match", "reverified": True,
        "fields": {vcol: val}, "current": {vcol: val}, "refs": {col: [snap]},
        "verifications": [{"url": snap, "ok": True, "contains_value": True, "name_found": True}],
        "tier": "high", "independent": False, "source_language": "en",
        "researcher_notes": saved_copy_note(item, use),
        "action": (f"Leave {vcol} of unit {use['unit_name']} ({use['unit_id']}) as it is. Add the 1 link "
                   f"below to the {col} box. Keep the links already there."),
        "checks": [10],
    }


def stage(items: list[dict], scope: dict, batch: Path) -> tuple[int, int, Path]:
    """Add one record per verified usage to staging/staged_updates.json. Returns (added, already there, path)."""
    path = batch / "staging" / "staged_updates.json"
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
    else:
        data = {"meta": {"lane": "updates", "scope": {
                    "country": scope["country"], "state": scope["name"] if scope["kind"] == "state" else "",
                    "postal": scope["postal"], "kind": scope["kind"], "slug": scope["slug"]},
                         "generated": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
                         "mode": "update", "counts": {"records": 0}},
                "records": []}
    have = {r["record_id"] for r in data["records"]}
    added = already = 0
    for item in items:
        for use in item["usages"]:
            sc = use.get("saved_copy") or {}
            if not sc.get("ok"):
                continue
            rec = make_record(item, use, scope)
            if rec["record_id"] in have:
                already += 1
                continue
            have.add(rec["record_id"])
            data["records"].append(rec)
            use["staged"] = True
            added += 1
    counts = data["meta"].setdefault("counts", {})
    counts["records"] = len(data["records"])
    counts["reverified"] = sum(bool(r.get("reverified")) for r in data["records"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return added, already, path


# ------------------------------------------------------------------ outputs
def tally(items: list[dict]) -> dict:
    dead = [i for i in items if i["status"] == "dead"]
    return {"distinct_urls": len(items),
            "live": sum(i["status"] == "live" for i in items),
            "blocked": sum(i["status"] == "blocked" for i in items),
            "unclear": sum(i["status"] == "unclear" for i in items),
            "dead": len(dead),
            "dead_with_verified_snapshot": sum(bool(i.get("verified")) for i in dead),
            "dead_without": sum(not i.get("verified") for i in dead),
            "dead_no_snapshot": sum(not i["snapshots"] for i in dead),
            "dead_snapshot_lookup_refused": sum(i["lookup"] == "refused" for i in dead)}


def needs_replacement(items: list[dict]) -> list[dict]:
    """Every usage of a dead address whose saved copy did not show the value (or has none)."""
    rows = []
    for i in items:
        if i["status"] != "dead":
            continue
        for u in i["usages"]:
            if (u.get("saved_copy") or {}).get("ok"):
                continue
            rows.append({"url": i["url"], "plant_id": u["plant_id"], "plant_name": u["plant_name"],
                         "unit_id": u["unit_id"], "unit_name": u["unit_name"],
                         "ds_column": u["ds_column"], "value_column": u["value_column"],
                         "value": u["value"], "why": u["saved_copy"]["reason"],
                         "snapshot": u["saved_copy"]["snapshot"]})
    return rows


def build_output(scope: dict, items: list[dict], n_rows: int, dry: bool) -> dict:
    return {"where": {k: scope[k] for k in ("kind", "name", "slug", "country", "postal")},
            "read": dt.date.today().isoformat(), "dry_run": dry, "unit_rows": n_rows,
            "counts": tally(items), "urls": items, "needs_replacement": needs_replacement(items)}


def plain(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def memo(out: dict) -> str:
    c = out["counts"]
    L = [f"# Links already in the database: {out['where']['name']}", "",
         f"Read {out['read']}. {out['unit_rows']} unit rows, {c['distinct_urls']} distinct web addresses "
         "in the Data Source boxes (hydrogen boxes skipped).", "",
         f"- Live: {c['live']}",
         f"- Gone from the old address: {c['dead']}",
         f"  - With a saved copy that shows the value: {c['dead_with_verified_snapshot']}",
         f"  - Without one: {c['dead_without']} ({c['dead_no_snapshot']} of the gone addresses have no saved copy at all"
         + (f", {c['dead_snapshot_lookup_refused']} could not be looked up because the archive refused"
            if c["dead_snapshot_lookup_refused"] else "") + ")",
         f"- Refuse robots or need a sign-in, so not judged: {c['blocked']}",
         f"- Could not tell (server errors and similar, try again later): {c['unclear']}", ""]
    hosts: dict[str, dict] = {}
    for i in out["urls"]:
        h = hosts.setdefault(i["host"], {"dead": 0, "saved": 0, "all": 0})
        h["all"] += 1
        if i["status"] == "dead":
            h["dead"] += 1
            h["saved"] += bool(i.get("verified"))
    bad = sorted(((h, v) for h, v in hosts.items() if v["dead"]), key=lambda x: -x[1]["dead"])
    if bad:
        L += ["## Gone links by site", "", "| Site | Addresses | Gone | With a saved copy that shows the value |",
              "|---|---|---|---|"]
        L += [f"| {h} | {v['all']} | {v['dead']} | {v['saved']} |" for h, v in bad]
        L.append("")
    staged = [(i, u) for i in out["urls"] for u in i["usages"] if u.get("staged")]
    ok = [(i, u) for i in out["urls"] for u in i["usages"] if (u.get("saved_copy") or {}).get("ok")]
    if ok:
        L += [f"## Saved copies that show the value ({len(ok)} unit boxes)", "",
              ("These were added to the staging file." if staged else
               "These are ready to stage. Run again without --dry-run, after the assembler, to stage them."), ""]
        for i, u in ok:
            L.append(f"- {u['plant_name']}, unit {u['unit_name']}, {u['ds_column']}: {i['url']}  ")
            L.append(f"  saved copy: {u['saved_copy']['snapshot']}")
        L.append("")
    need = out["needs_replacement"]
    if need:
        L += [f"## Gone links the sweep must replace ({len(need)} unit boxes)", "",
              "Each of these needs a new source for the same value. The old link stays in the box.", ""]
        for r in need:
            L.append(f"- {r['plant_name']}, unit {r['unit_name']}, {r['ds_column']} ({r['value_column'] or 'no value box'}"
                     f"{': ' + r['value'] if r['value'] else ''}): {r['url']}  ")
            L.append(f"  {plain(r['why'])}")
        L.append("")
    other = [i for i in out["urls"] if i["status"] in ("blocked", "unclear")]
    if other:
        L += ["## Not judged", ""]
        L += [f"- {i['status']}: {i['url']}  \n  {plain(i['reason'])}" for i in other]
        L.append("")
    return "\n".join(L)


def default_batch(scope: dict) -> Path:
    tag = f"us-{scope['postal']}" if scope["kind"] == "state" else scope["slug"]
    return REPO_ROOT / "batches" / tag


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    who = ap.add_mutually_exclusive_group(required=True)
    who.add_argument("--state", help="a US state, e.g. Mississippi")
    who.add_argument("--country", help="a country (Country/Area value), e.g. Germany")
    ap.add_argument("--csv", default=str(gogpt_scoped_csv()))
    ap.add_argument("--batch", default=None, help="batch directory (default batches/us-<postal> or batches/<country-slug>)")
    ap.add_argument("--dry-run", action="store_true", help="report only; never write staging")
    ap.add_argument("--refresh", action="store_true", help="ignore the seven-day cache")
    ap.add_argument("--workers", type=int, default=WORKERS)
    ap.add_argument("--allow-stale-export", action="store_true")
    a = ap.parse_args(argv)

    scope = make_scope(state=a.state, country=a.country)
    require_fresh_export(a.csv, a.allow_stale_export)
    rows, header = read_scope(scope, Path(a.csv))
    if not rows:
        sys.exit(f"ERROR: no {scope['name']} rows in {a.csv}; check the spelling")
    usage_map = collect(rows, header)
    print(f"{scope['name']}: {len(rows)} unit rows, {len(usage_map)} distinct addresses", file=sys.stderr)

    cache = Cache(work_dir() / "existing_links_cache.json", a.refresh)
    items = run_checks(usage_map, cache, a.workers)
    cache.save()

    batch = Path(a.batch) if a.batch else default_batch(scope)
    batch.mkdir(parents=True, exist_ok=True)
    staged = None
    if not a.dry_run:
        staged = stage(items, scope, batch)
    out = build_output(scope, items, len(rows), a.dry_run)
    (batch / "existing_links.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (batch / "existing_links.md").write_text(memo(out), encoding="utf-8")

    c = out["counts"]
    print(f"distinct URLs: {c['distinct_urls']}  live: {c['live']}  blocked: {c['blocked']}  "
          f"unclear: {c['unclear']}  dead: {c['dead']} "
          f"(verified snapshot: {c['dead_with_verified_snapshot']}, without: {c['dead_without']})")
    if staged:
        print(f"staged {staged[0]} saved-copy record(s) ({staged[1]} already there) in {staged[2]}")
    print(f"wrote {batch / 'existing_links.json'}\nwrote {batch / 'existing_links.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

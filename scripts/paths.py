"""Central path resolution — so nothing hard-codes /Users/baird/... .

Repo layout is fixed relative to this file (scripts/paths.py). Scope files
(note, coverage list, plan, harvesters, work outputs) live in scopes/<tag>/;
the scope_* helpers below are the only place that knows. Sibling repos
(gem-db-ops, lng-terminals-researcher) default to siblings of this repo and can
be overridden by env vars (see .env.example).
"""
from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def repo_root() -> Path:
    return REPO_ROOT


def _sibling(name: str, env: str) -> Path:
    override = os.environ.get(env)
    if override:
        return Path(override).expanduser().resolve()
    return (REPO_ROOT.parent / name).resolve()


def db_ops_repo() -> Path:
    """Local gem-db-ops repo — the pull engine (single source of truth)."""
    return _sibling("gem-db-ops", "GEM_DB_OPS_REPO")


def lng_repo() -> Path:
    """Local lng-terminals-researcher repo — captive-power cross-tracker inputs."""
    return _sibling("lng-terminals-researcher", "GEM_LNG_REPO")


def gem_export_csv() -> Path:
    """Default location of the fresh all-combustion export (never committed)."""
    return REPO_ROOT / "scripts" / "gem_export_gogpt.csv"


def gogpt_scoped_csv() -> Path:
    """Default location of the GOGPT-scoped view derived by scope_filter.py."""
    return REPO_ROOT / "scripts" / "gem_export_gogpt_scoped.csv"


EXPORT_MAX_AGE_HOURS = 24


def require_fresh_export(csv_path, allow_stale: bool = False) -> None:
    """Refuse to work from an export older than EXPORT_MAX_AGE_HOURS.

    Checks the given csv and, when it is the default scoped view, the full
    export it was filtered from (re-running scope_filter.py on an old pull
    gives a new file with old data). With allow_stale it only warns, for a
    deliberate rebuild of an earlier batch.
    """
    import sys
    import time
    csv_path = Path(csv_path).resolve()
    checks = [csv_path]
    if csv_path == gogpt_scoped_csv().resolve():
        checks.append(gem_export_csv())
    stale = []
    for p in checks:
        if p.exists():
            hours = (time.time() - p.stat().st_mtime) / 3600
            if hours > EXPORT_MAX_AGE_HOURS:
                stale.append(f"{p.name} is {hours / 24:.1f} days old")
    if not stale:
        return
    msg = "GEM export is stale: " + "; ".join(stale) + "."
    pulled_elsewhere = db_ops_repo() / "gogpt" / "gem_export_gogpt.csv"
    if (pulled_elsewhere.exists() and gem_export_csv().exists()
            and pulled_elsewhere.stat().st_mtime > gem_export_csv().stat().st_mtime):
        msg += (f"\n  A newer pull sits in {pulled_elsewhere}: pull.py was run without"
                " --output, so it never reached scripts/.")
    msg += ("\n  Run the fresh pull chain from scripts/ (docs/workflows.md §1):"
            "\n    python ../../gem-db-ops/gogpt/pull.py --output gem_export_gogpt.csv"
            "\n    python pull_gem_db.py --map-only"
            "\n    python scope_filter.py")
    if allow_stale:
        print("WARNING: " + msg + "\n  Continuing because --allow-stale-export was given.",
              file=sys.stderr)
        return
    sys.exit("ERROR: " + msg + "\n  (--allow-stale-export overrides, for a deliberate"
             " rebuild of an earlier batch only.)")


def work_dir(tag: str | None = None) -> Path:
    """The gitignored work folder: repo-wide `work/`, or with a scope tag that
    scope's own `scopes/<tag>/work/` (see scope_work)."""
    if tag:
        return scope_work(tag)
    d = REPO_ROOT / "work"
    d.mkdir(exist_ok=True)
    return d


# ------------------------------------------------------------------ scopes ---
# One folder per state or country under scopes/<tag>/ (repo layout audit,
# Baird 2026-10-29): note.md, coverage.json, plan.md, the scope's harvesters,
# queues.json, and a gitignored work/. batches/<tag>/ stays the record of each run.

SCOPES_DIR = REPO_ROOT / "scopes"

US_POSTAL = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR", "california": "CA",
    "colorado": "CO", "connecticut": "CT", "delaware": "DE", "district of columbia": "DC",
    "florida": "FL", "georgia": "GA", "hawaii": "HI", "idaho": "ID", "illinois": "IL",
    "indiana": "IN", "iowa": "IA", "kansas": "KS", "kentucky": "KY", "louisiana": "LA",
    "maine": "ME", "maryland": "MD", "massachusetts": "MA", "michigan": "MI", "minnesota": "MN",
    "mississippi": "MS", "missouri": "MO", "montana": "MT", "nebraska": "NE", "nevada": "NV",
    "new hampshire": "NH", "new jersey": "NJ", "new mexico": "NM", "new york": "NY",
    "north carolina": "NC", "north dakota": "ND", "ohio": "OH", "oklahoma": "OK", "oregon": "OR",
    "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC", "south dakota": "SD",
    "tennessee": "TN", "texas": "TX", "utah": "UT", "vermont": "VT", "virginia": "VA",
    "washington": "WA", "west virginia": "WV", "wisconsin": "WI", "wyoming": "WY",
}

# A batch folder can be one run of a scope: us-il-dc (data center catch-up),
# us-il-val (validation answers), germany-permits. These share the scope's folder.
RUN_SUFFIXES = ("-dc", "-val", "-permits")


def scope_tag(state: str | None = None, country: str | None = None) -> str:
    """The one tag every script uses for a scope: `us-nd` for a US state (name
    or postal code), the hyphenated lowercase name for a country (`germany`,
    `south-africa`). An existing tag is returned as is."""
    import re
    if state:
        s = state.strip()
        if re.fullmatch(r"us-[a-z]{2}", s.lower()):
            return s.lower()
        if len(s) == 2 and s.upper() in US_POSTAL.values():
            return f"us-{s.lower()}"
        postal = US_POSTAL.get(s.lower())
        if not postal:
            raise ValueError(f"unknown US state {state!r}")
        return f"us-{postal.lower()}"
    if country:
        return re.sub(r"\s+", "-", country.strip().lower())
    raise ValueError("scope_tag needs a state or a country")


def scope_base(tag: str) -> str:
    """The scope a batch folder name belongs to: us-il-dc -> us-il, germany-permits -> germany."""
    tag = Path(str(tag)).name
    for suf in RUN_SUFFIXES:
        if tag.endswith(suf) and len(tag) > len(suf):
            return tag[: -len(suf)]
    return tag


def scope_dir(tag: str) -> Path:
    """scopes/<tag>/ for a scope tag or any batch folder name of that scope."""
    return SCOPES_DIR / scope_base(tag)


def scope_work(tag: str) -> Path:
    """The scope's gitignored work folder, created on first use. A run variant
    (us-il-dc) gets its own subfolder so its outputs never mix with the scope's."""
    tag = Path(str(tag)).name
    base = scope_base(tag)
    d = SCOPES_DIR / base / "work"
    if tag != base:
        d = d / tag
    d.mkdir(parents=True, exist_ok=True)
    return d


def scope_permits(tag: str, legacy: bool = True) -> Path:
    """The permit harvest folder of a scope or run: scopes/<scope>/work/permits/.
    With legacy (the default, for one cycle) an older harvest still sitting in
    work/permits/<tag>/ is returned when the new folder does not exist."""
    tag = Path(str(tag)).name
    base = scope_base(tag)
    new = SCOPES_DIR / base / "work" / ("permits" if tag == base else f"{tag}/permits")
    old = REPO_ROOT / "work" / "permits" / tag
    if legacy and not new.exists() and old.exists():
        return old
    return new


def scope_note(state: str | None = None, country: str | None = None) -> Path | None:
    """The scope note: scopes/<tag>/note.md, else (one cycle) the older
    docs/country_notes/united_states/<state>.md or docs/country_notes/<country>.md.
    None when there is none."""
    import re
    tag = scope_tag(state=state, country=country)
    new = scope_dir(tag) / "note.md"
    if new.exists():
        return new
    name = re.sub(r"\s+", "-", (state or country).strip().lower())
    d = REPO_ROOT / "docs" / "country_notes"
    if state:
        d = d / "united_states"
    for n in (name, name.replace("-", "_")):
        if (d / f"{n}.md").exists():
            return d / f"{n}.md"
    return None


def scope_coverage(tag: str) -> Path:
    """The statewide source list for a batch folder name: scopes/<tag>/coverage.json
    for the scope's own batch. Older lists in docs/coverage/<tag>.json are read
    for one cycle. A run variant (us-il-dc) has no list of its own, as before."""
    tag = Path(str(tag)).name
    legacy = REPO_ROOT / "docs" / "coverage" / f"{tag}.json"
    if tag != scope_base(tag):
        return legacy
    new = scope_dir(tag) / "coverage.json"
    return legacy if (not new.exists() and legacy.exists()) else new


def load_scope_module(tag: str, name: str, alias: str | None = None):
    """Import scopes/<tag>/<name>.py (a harvester) under a unique module name so
    two scopes' harvest_permits.py can be loaded in one process (tests). The
    scope folder and scripts/ are put on sys.path for the file's own imports."""
    import importlib.util
    import sys
    folder = scope_dir(tag)
    for p in (str(REPO_ROOT / "scripts"), str(folder)):
        if p not in sys.path:
            sys.path.insert(0, p)
    alias = alias or f"scope_{scope_base(tag).replace('-', '_')}_{name}"
    if alias in sys.modules:
        return sys.modules[alias]
    spec = importlib.util.spec_from_file_location(alias, folder / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[alias] = mod
    spec.loader.exec_module(mod)
    return mod

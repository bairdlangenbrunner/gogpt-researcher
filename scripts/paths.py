"""Central path resolution — so nothing hard-codes /Users/baird/... .

Repo layout is fixed relative to this file (scripts/paths.py). Sibling repos
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


def work_dir() -> Path:
    d = REPO_ROOT / "work"
    d.mkdir(exist_ok=True)
    return d

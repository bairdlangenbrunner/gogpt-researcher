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


def work_dir() -> Path:
    d = REPO_ROOT / "work"
    d.mkdir(exist_ok=True)
    return d

"""
gogpt_paths.py — central directory resolution for the GOGPT pipeline
====================================================================
Keeps the pipeline portable between:
  • a local Claude Code repo (data/ and assets/ live next to scripts/), and
  • the original hosted environment (/mnt/project, /mnt/user-data/...).

Every path can be overridden with an environment variable, so nothing here is
hardcoded to one machine. Resolution order for each directory:

    1. explicit environment variable (e.g. GOGPT_DATA_DIR)
    2. the repo-relative default (../data, ../assets, ...)
    3. a legacy /mnt fallback, kept so the scripts still run unchanged in the
       original hosted setup.

Environment variables
---------------------
  GOGPT_DATA_DIR     where GOGPTall*.xlsx / *.csv dumps + possible-updates live
  GOGPT_ASSETS_DIR   bundled reference lists (H2_units_to_exclude.xlsx)
  GOGPT_OUTPUT_DIR   where compiled files + updated cards are written
  GOGPT_WORK_DIR     persistent working copy of the context card
  GOGPT_UPLOADS_DIR  where freshly-uploaded cards/dumps are looked for
"""
import os

# Repo root = parent of this scripts/ directory.
_HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(_HERE)


def _resolve(env_var: str, repo_rel: str, legacy: str) -> str:
    """Pick a directory: env override → repo-relative → legacy /mnt fallback."""
    env = os.environ.get(env_var)
    if env:
        return os.path.abspath(os.path.expanduser(env))
    repo_path = os.path.join(REPO_ROOT, repo_rel)
    if os.path.isdir(repo_path):
        return repo_path
    return legacy


DATA_DIR = _resolve("GOGPT_DATA_DIR", "data", "/mnt/project")
ASSETS_DIR = _resolve("GOGPT_ASSETS_DIR", "assets", os.path.join(REPO_ROOT, "assets"))
OUTPUT_DIR = _resolve("GOGPT_OUTPUT_DIR", "output", "/mnt/user-data/outputs")
WORK_DIR = _resolve("GOGPT_WORK_DIR", ".gogpt_work", "/home/claude/gogpt_work")
UPLOADS_DIR = _resolve("GOGPT_UPLOADS_DIR", "uploads", "/mnt/user-data/uploads")

# Dirs the pipeline writes to should exist.
for _d in (OUTPUT_DIR, WORK_DIR):
    try:
        os.makedirs(_d, exist_ok=True)
    except OSError:
        pass

# Convenience globs used by more than one script.
DUMP_GLOBS = (
    os.path.join(DATA_DIR, "GOGPTall*.xlsx"),
    os.path.join(DATA_DIR, "GOGPTall*.csv"),
)
POSSIBLE_UPDATES_GLOB = os.path.join(
    DATA_DIR, "GEM_trackers__possible_updates__*.csv"
)
H2_EXCLUDE_FILE = os.path.join(ASSETS_DIR, "H2_units_to_exclude.xlsx")

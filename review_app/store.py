"""
The GOGPT review app's decision store: the shared store in ../gem-review-app (review_core/store.py) bound to the GOGPT config (trackers/gogpt/config.py).

Every decision is a call on one staged record, by its stable `record_id`. The two sidecars live in the staging dir and are committed with the batch: review_log.jsonl (append-only truth) and review_decisions.json (derived, latest record per key). Line records are {key, dir, pid, record_id, column, kind, decision, suggested_value, reference, note, reviewer, ts, undecided}. Item calls (qa concerns, watch items, entity notes) go to the same log as {key, dir, pid, record_id, kind, call, reference, note, ...}. An ask-the-PM flag is {key: "pm::" + line or item key, or "pm::" + dir + "::plant:" + pid, flag: "pm", on, note, ...} and never replaces a decision.

The sidecars are a mirror: every decision lands first in the `log` tab of the Google decision store (review_app/ledger.py), and pull.py copies store rows back. Nothing here touches the GEM database, the staged_*.json files or the deliverables; scripts/build_review_package.py --decisions reads the decisions when the actions workbook is built.

Every name this module has always exported is still here (decide, record_items, record_flags, overlay, index, initials, dir_paths, read_log, _write, _LOCK, Invalid, ITEM_CALLS, FLAG_PREFIX and the rest), whether it is imported as `store` or as `review_app.store`.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
import review_app  # noqa: E402,F401  (puts ../gem-review-app on sys.path)
from review_core.store import bind  # noqa: E402
from trackers.gogpt.config import CONFIG  # noqa: E402

globals().update(bind(CONFIG, ROOT))

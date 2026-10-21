"""
Bring decisions made on the artifact page (build_static.py) into the decision ledger.

    python review_app/import_log.py <out_dir>/logs/<id>.json --dry-run
    python review_app/import_log.py FILE [FILE ...] --dirs batches/us-md/staging ... --reviewer EMAIL [--reviewer XX=EMAIL ...]

FILE is what the page's "download decisions" button saves, or the artifact's shared `logs` collection saved as JSON (an ArtifactData list or get result). Either way it holds one or more log documents, each {reviewer, records: [...]}. --dirs names the staging dirs the page was built from (default: every dir the records name); the dataset is rebuilt from them so each record can be checked against the current batch.

Every new record goes through the ledger like any other decision: appended to the store spreadsheet's `log` tab first (origin 'artifact', under the reviewer's own address), then to the staging dir's review_log.jsonl. Each record keeps the id and the time the page gave it. Rules:

  - a record whose id is already in a staging dir's log is skipped, so importing the same file twice, or a later download that repeats an earlier one, is safe. A record the page wrote before it stamped ids (pages built before 2026-10-08) gets one derived from its contents (reviewer, key, time, call), the same id every time, so those files re-import safely too
  - a record is skipped as superseded when the log already holds a later decision by a person on the same line, item or flag (someone decided it on the local server afterwards)
  - a record whose key is not in the current dataset, or whose staging dir is not, stops the import before anything is written (the batch was rebuilt since the page was made: rebuild the page and publish it again)
  - the page is not given reviewers' addresses, only their names, so name each one: --reviewer analyst.lead@globalenergymonitor.org (matched to the initials AL), or --reviewer AL=ADDRESS

This appends to the store `log` tab and to the sidecars. The GEM database, the staged_*.json files and the deliverables are not touched; accepted edits reach GEM only through the actions workbook that scripts/build_review_package.py --decisions builds and the reviewer applies by hand.

The plan, write and report code is shared with pipelines-researcher in ../gem-review-app/review_core/import_log.py. This file holds the gogpt rules: what a line, item or flag record must match (Rules), legacy_id, and the --dirs dataset.
"""
import json
import sys
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for p in (ROOT / "scripts", HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import ledger  # noqa: E402
import review_data  # noqa: E402
import store  # noqa: E402
from review_core import import_log as core  # noqa: E402


# records the page wrote before static_store.js stamped a uuid4 on each one (pages built before
# 2026-10-08) get this id instead: the same one every time, from what the record says
LEGACY_NS = uuid.UUID("6f1d2b2e-5c2a-4f6e-9c1b-0f2a8d3e7b41")
LEGACY_FIELDS = ("reviewer", "key", "dir", "ts", "decision", "call", "flag", "on", "undecided",
                 "note", "suggested_value", "reference")


def legacy_id(r):
    """A deterministic id for a page record that has none."""
    parts = [f"{k}={json.dumps(r.get(k), sort_keys=True, default=str)}" for k in LEGACY_FIELDS]
    return str(uuid.uuid5(LEGACY_NS, "\n".join(parts)))


def dataset(dirs, export_csv=None, root=ROOT):
    """The current dataset for these staging dirs, overlaid with their logs, and {label: Path}."""
    ds = review_data.build([Path(d) for d in dirs], export_csv)
    paths = store.dir_paths(ds, root)
    store.overlay(ds, paths)
    return ds, paths


class Rules:
    """What a gogpt record must match in the current dataset: a flag record an item, line or plant it can flag; a line or item record its own key, of the right kind, with a call or decision from the vocabulary; and a staging dir of the dataset. Anything else stops the import. Nothing is parked."""

    def __init__(self, ds, dirs):
        self.dirs = dirs
        self.idx = store.index(ds)
        self.plants = {store.plant_flag_key(p.get("dir"), p["pid"]) for p in ds.get("plants", [])}

    def place(self, r, where, email):
        idx, key = self.idx, str(r["key"])
        if r.get("flag"):
            if r["flag"] not in store.FLAGS or not key.startswith(store.FLAG_PREFIX):
                raise SystemExit(f"{where}: not an ask-the-PM flag record")
            inner = key[len(store.FLAG_PREFIX):]
            if inner not in idx and key not in self.plants:
                raise SystemExit(f"{where}: {key} flags nothing in the current dataset "
                                 "(rebuilt since the page was made? rebuild the page and publish it again)")
        else:
            if key not in idx:
                raise SystemExit(f"{where}: {key} is not in the current dataset "
                                 "(rebuilt since the page was made? rebuild the page and publish it again)")
            grp = idx[key][2]
            if ("call" in r) != (grp == "items"):
                raise SystemExit(f"{where}: {key} is {'an item' if grp == 'items' else 'a line'} "
                                 f"but the record is {'an item call' if 'call' in r else 'a line decision'}")
            if "decision" in r and r["decision"] not in store.DECISIONS:
                raise SystemExit(f"{where}: decision {r['decision']!r} is not one of {sorted(store.DECISIONS)}")
            if "call" in r and not r.get("undecided"):
                vocab = store.ITEM_CALLS.get(idx[key][1].get("kind"), store.OTHER_CALLS)
                if r["call"] not in vocab:
                    raise SystemExit(f"{where}: call {r['call']!r} is not one of {list(vocab)} for a {idx[key][1].get('kind')} item")
        if r["dir"] not in self.dirs:
            raise SystemExit(f"{where}: staging dir {r['dir']} is not part of the current dataset")
        return r

    def extra(self):
        return {}


def _add_args(ap):
    ap.add_argument("--dirs", nargs="*", default=[], help="the staging dirs the page was built from (default: the dirs the records name)")
    ap.add_argument("--export-csv", default=None, help="scoped export csv (default: the batch's own)")


def _dataset_for(a, docs):
    dirs = list(a.dirs) or sorted({str(r.get("dir")) for d in docs for r in d["records"] if isinstance(r, dict) and r.get("dir")})
    for d in dirs:
        if not (ROOT / d).is_dir() and not Path(d).is_dir():
            raise SystemExit(f"{d}: not a staging dir")
    return dataset([(ROOT / d) if not Path(d).is_absolute() else Path(d) for d in dirs], a.export_csv)


core.bind(sys.modules[__name__], required=("key", "reviewer", "dir"), rules=Rules, fill_id=lambda r: legacy_id(r),
          flags=True, bare_jsonl=True, add_args=_add_args, dataset_for=_dataset_for,
          next_step="Then: python scripts/build_review_package.py ... --decisions")

if __name__ == "__main__":
    sys.exit(main())  # noqa: F821  (bound above)

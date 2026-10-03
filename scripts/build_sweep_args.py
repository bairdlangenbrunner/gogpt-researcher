"""
Build the Workflow args for a state sweep from a batch's briefs/_index.json.

Usage (from scripts/):
    python build_sweep_args.py --batch ../batches/us-md [--model sonnet]
        [--plants L...,L...] [--group-max 1] [--extra-brief path.md]

Reads:  <batch>/briefs/_index.json and every brief it lists (all must exist).
Writes: <batch>/staging/sweep_args.json, and prints the same JSON to stdout.

Output keys: repo, batch, state, postal, mode, model, csv, plants (plant_id,
plant_name, brief_path, unit_ids, shard_path; all paths absolute), groups
(lists of plant IDs; one plant per group by default, --group-max N packs
plants together while a group's total units stay at or under N, and a plant
with more than N units gets a group of its own), extra_brief (file contents).
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from paths import REPO_ROOT


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--batch", required=True)
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--plants", default=None)
    ap.add_argument("--group-max", type=int, default=1)
    ap.add_argument("--extra-brief", default=None)
    a = ap.parse_args()

    batch = Path(a.batch).resolve()
    idx_path = batch / "briefs" / "_index.json"
    if not idx_path.exists():
        sys.exit(f"ERROR: {idx_path} not found; run build_state_brief.py first")
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    plants = idx["plants"]
    if a.plants:
        want = [p.strip() for p in a.plants.split(",") if p.strip()]
        have = {p["plant_id"] for p in plants}
        unknown = [w for w in want if w not in have]
        if unknown:
            sys.exit(f"ERROR: plants not in index: {unknown}")
        plants = [p for p in plants if p["plant_id"] in set(want)]

    out_plants = []
    for p in plants:
        bp = Path(p["brief_path"])
        bp = bp if bp.is_absolute() else REPO_ROOT / bp
        if not bp.exists():
            sys.exit(f"ERROR: brief missing: {bp}")
        out_plants.append({
            "plant_id": p["plant_id"], "plant_name": p["plant_name"],
            "brief_path": str(bp), "unit_ids": p["unit_ids"],
            "shard_path": str(batch / "shards" / f"{p['plant_id']}.json")})

    groups, cur, cur_units = [], [], 0
    for p in out_plants:
        n = len(p["unit_ids"])
        if cur and (a.group_max <= 1 or cur_units + n > a.group_max):
            groups.append(cur)
            cur, cur_units = [], 0
        cur.append(p["plant_id"])
        cur_units += n
    if cur:
        groups.append(cur)

    extra = ""
    if a.extra_brief:
        ep = Path(a.extra_brief)
        if not ep.exists():
            sys.exit(f"ERROR: extra brief not found: {ep}")
        extra = ep.read_text(encoding="utf-8")

    args = {"repo": str(REPO_ROOT), "batch": str(batch), "state": idx["state"],
            "postal": idx["postal"], "mode": idx["mode"], "model": a.model,
            "csv": str(Path(idx["csv"]).resolve()), "plants": out_plants,
            "groups": groups, "extra_brief": extra}
    text = json.dumps(args, indent=2, ensure_ascii=False)
    (batch / "staging").mkdir(exist_ok=True)
    (batch / "staging" / "sweep_args.json").write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

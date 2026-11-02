"""Backfill milestone timeline entries into a batch's staged records (Baird 2026-11-02).

Two modes:

  python add_milestones.py --list ../batches/us-mi [--out todo.json]
      Lists every staged record (and newplants unit) whose Status has no milestone entry for
      that status, the same test as state_gate.py gate `milestones`. Each row carries what a
      researcher needs: record_id, unit index, plant and unit name, status, start year, the
      Status Data Source links and the verification notes already on the record.

  python add_milestones.py --apply ../batches/us-mi proposals.json
      Writes proposals into the staged files. proposals.json is a list of
        {"lane", "record_id", "unit": int or null,
         "milestones": [{"status","year","period","sources","note","period_note"?}],
         "action": "Milestone timeline: ...",            # appended unless one is there
         "verifications": [{"url","ok","contains_value","name_found","note"}]}  # new sources only
      Every milestone source must already be a loaded verification on the record or come with
      a new one (passed url_verifier.py first). Sources are merged into Status Data Source,
      never replacing a link. Only changed lane files are rewritten, keeping each file's own indent, so the diff stays small.
"""
import argparse
import json
import sys
from pathlib import Path

LANES = ("updates", "newunits", "newplants")


def load(staging):
    out = {}
    for lane in LANES:
        p = staging / f"staged_{lane}.json"
        if p.exists():
            text = p.read_text(encoding="utf-8")
            second = text.split("\n", 2)[1] if "\n" in text else ""
            indent = len(second) - len(second.lstrip(" ")) or 2
            out[lane] = (p, json.loads(text), indent)
    return out


def records(data):
    return data["records"] if isinstance(data, dict) else data


def needs(rec):
    st = str((rec.get("fields") or {}).get("Status") or "").strip().lower()
    if not st or rec.get("delete"):
        return None
    if any(str(m.get("status") or "").strip().lower() == st for m in rec.get("milestones") or []):
        return None
    return st


def status_refs(rec):
    refs = rec.get("refs") or {}
    return refs if isinstance(refs, list) else refs.get("Status Data Source") or []


def do_list(staging, out):
    rows = []
    for lane, (_, data, _i) in load(staging).items():
        for rec in records(data):
            subs = [(None, rec)] + [(j, u) for j, u in enumerate(rec.get("units") or [])]
            for j, u in subs:
                st = needs(u)
                if not st:
                    continue
                f = u.get("fields") or {}
                rows.append({
                    "lane": lane, "record_id": rec.get("record_id"), "unit": j,
                    "plant": rec.get("plant_name") or (rec.get("fields") or {}).get("Plant Name"),
                    "unit_name": u.get("unit_name") or f.get("Unit Name"),
                    "gem_unit_id": u.get("gem_unit_id"), "status": st,
                    "start_year": f.get("Start Year"),
                    "status_refs": status_refs(u),
                    "verifications": [{"url": v.get("url"), "note": (v.get("note") or "")[:300]}
                                      for v in u.get("verifications") or [] if v.get("ok")],
                })
    text = json.dumps(rows, indent=1, ensure_ascii=False)
    if out:
        Path(out).write_text(text + "\n", encoding="utf-8")
        print(f"{len(rows)} records need a milestone; written to {out}")
    else:
        print(text)


def do_apply(staging, proposals):
    files = load(staging)
    props = json.loads(Path(proposals).read_text(encoding="utf-8"))
    errors, done, touched = [], 0, set()
    for p in props:
        lane, rid, j = p["lane"], p["record_id"], p.get("unit")
        recs = records(files[lane][1])
        rec = next((r for r in recs if r.get("record_id") == rid), None)
        if rec is None:
            errors.append(f"{rid}: record not found in {lane}")
            continue
        u = rec if j is None else rec["units"][j]
        have = {v.get("url") for v in u.get("verifications") or [] if v.get("ok")}
        new = {v["url"]: v for v in p.get("verifications") or []}
        bad = [s for m in p["milestones"] for s in m.get("sources") or [] if s not in have and s not in new]
        if bad:
            errors.append(f"{rid}/{j}: sources with no verification: {bad}")
            continue
        u["milestones"] = p["milestones"]
        act = (p.get("action") or "").strip()
        if act and "Milestone timeline" not in (u.get("action") or ""):
            u["action"] = ((u.get("action") or "").rstrip() + " " + act).strip()
        u.setdefault("verifications", [])
        for url, v in new.items():
            if url not in have:
                u["verifications"].append(v)
        refs = u.setdefault("refs", {})
        sds = refs if isinstance(refs, list) else refs.setdefault("Status Data Source", [])
        for m in p["milestones"]:
            for s in m.get("sources") or []:
                if s not in sds:
                    sds.append(s)
        done += 1
        touched.add(lane)
    for lane in touched:
        path, data, indent = files[lane]
        path.write_text(json.dumps(data, indent=indent, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"applied {done} of {len(props)}")
    for e in errors:
        print("ERROR", e)
    return 1 if errors else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", metavar="BATCH")
    ap.add_argument("--out")
    ap.add_argument("--apply", nargs=2, metavar=("BATCH", "PROPOSALS"))
    a = ap.parse_args()
    if a.list:
        do_list(Path(a.list) / "staging", a.out)
    elif a.apply:
        sys.exit(do_apply(Path(a.apply[0]) / "staging", a.apply[1]))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()

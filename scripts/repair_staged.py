#!/usr/bin/env python3
"""Bring older staging up to two rules (Baird 2026-10-08, 2026-10-09).

1. Status Detail carries its own links. A Status Detail record whose links
   sit under Status Data Source (which feeds the milestone and scheduled-event
   timeline in the web form) gets them keyed under "Status Detail" instead,
   and every new Status Detail entry is laid out as its text, a blank line,
   then one link per line (build_review_package.inline_value; the older
   "text: https://..." form is reflowed). The action is rewritten to match.
   The text already in the box is untouched.
2. One fully validated source is green. A `medium` record with a link whose
   verification loaded, names the plant and states the value is raised to
   `high` (build_review_package.validated_tier). A Status change is never
   raised, nor `low`, nor a record whose note says the sources disagree or
   the value is only implied.

A deterministic repair, not new research: no value other than the link, no
verification and no `independent` flag changes. record_id stays the same, so
review decisions keep their keys. Dry run by default; --apply writes. Rebuild
the review page and any deliverable afterwards (a fresh stamp, never an
overwrite).

Usage (from the repo root):
    python scripts/repair_staged.py batches/us-md/staging batches/us-ny/staging
    python scripts/repair_staged.py --all --apply
"""
import argparse
import glob
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from assemble_state import build_action  # noqa: E402
from build_review_package import (_ws, additive_value, inline_value,  # noqa: E402
                                  validated_tier)

ROOT = Path(__file__).resolve().parent.parent
VALUE_LANES = ("updates", "newplants", "newunits")


ACTION_TARGET = re.compile(r"^(?:Set Status Detail of (?P<a>.+?) to |Add (?:this|the entry "
                           r"below) at the top of the Status Detail box of (?P<b>.+?), above)")


def inline_status_detail(r, problems, rid):
    fields, refs = r.get("fields") or {}, r.get("refs") or {}
    if "Status Detail" not in fields or "Status" in fields:
        return False
    key = "Status Detail" if refs.get("Status Detail") else "Status Data Source"
    urls = [u for u in refs.get(key) or [] if u]
    if not urls:
        return False
    value = str(fields["Status Detail"])
    current = str((r.get("current") or {}).get("Status Detail") or "").strip()
    if current:
        if not _ws(value).endswith(_ws(current)):
            problems.append(f"{rid}: Status Detail does not end with the current text; left alone")
            return False
        new_part = value.rstrip()[:len(value.rstrip()) - len(current)].rstrip()
    else:
        new_part = value.strip()
    new_inline = inline_value(new_part, urls)
    new_value = additive_value(new_inline, current)
    if key == "Status Detail" and new_value == value:
        return False
    m = ACTION_TARGET.match(str(r.get("action") or ""))
    if not m:
        problems.append(f"{rid}: action text not in the expected form; rewrite it by hand")
        return False
    fields["Status Detail"] = new_value
    refs.pop("Status Data Source", None)
    refs["Status Detail"] = urls
    r["action"] = build_action("change" if current else "fill", "Status Detail",
                               new_inline, current, m.group("a") or m.group("b"),
                               "Status Detail", len(urls), additive=bool(current),
                               inline=True)
    return True


def repair_file(path, apply):
    text = path.read_text(encoding="utf-8")
    data = json.loads(text)
    # keep the file's own indent so the diff shows only what changed
    m = re.search(r"\n( +)\S", text)
    indent = len(m.group(1)) if m else 2
    recs = data.get("records") if isinstance(data, dict) else data
    inlined, promoted, problems = [], [], []
    for rec in recs or []:
        rid = rec.get("record_id") or rec.get("gem_unit_id") or "?"
        for r in [rec] + list(rec.get("units") or []):
            if inline_status_detail(r, problems, rid):
                inlined.append(rid)
        # a Status change as the gate reads it: the box has a status and
        # the record proposes a different one
        fields = rec.get("fields") or {}
        cur = _ws((rec.get("current") or {}).get("Status"))
        if "Status" in fields and cur and cur.lower() != _ws(fields["Status"]).lower():
            continue
        urls = [u for us in (rec.get("refs") or {}).values() for u in us]
        if validated_tier("", "fill", rec.get("tier"), urls, rec.get("verifications"),
                          rec.get("researcher_notes")) != str(rec.get("tier") or "").lower():
            rec["tier"] = "high"
            promoted.append(rid)
    if apply and (inlined or promoted):
        path.write_text(json.dumps(data, indent=indent, ensure_ascii=False) + "\n", encoding="utf-8")
    return inlined, promoted, problems


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("staging", nargs="*", help="staging dirs")
    ap.add_argument("--all", action="store_true", help="every batches/*/staging dir")
    ap.add_argument("--apply", action="store_true", help="write the changes")
    args = ap.parse_args(argv)
    dirs = [Path(d) for d in args.staging]
    if args.all:
        dirs += [Path(d) for d in sorted(glob.glob(str(ROOT / "batches" / "*" / "staging")))]
    if not dirs:
        ap.error("give staging dirs or --all")
    for d in dirs:
        for lane in VALUE_LANES:
            p = d / f"staged_{lane}.json"
            if not p.exists():
                continue
            inlined, promoted, problems = repair_file(p, args.apply)
            if not (inlined or promoted or problems):
                continue
            print(f"{p}: Status Detail entries laid out with their links {len(inlined)}, "
                  f"raised medium to high {len(promoted)}"
                  f"{'' if args.apply else ' (dry run)'}")
            for rid in promoted:
                print(f"  raised {rid}")
            for msg in problems:
                print(f"  PROBLEM {msg}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Bring older staging up to three rules (Baird 2026-10-08, 2026-10-09; 2026-11-03).

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
3. Links sit under real Data Source columns (2026-11-03). A name column
   (schema_constants.IDENTITY_COLUMNS: Plant name, Unit name, Other Name(s))
   has no Data Source column, so a refs key like "Unit name Data Source" is
   dropped when its links already sit under the record's other keys and
   renamed to "links" otherwise. A record whose `fields` key is itself a Data
   Source column ("Fuel Data Source": "fossil gas: natural gas", the agent
   offering a link for a box whose link had died) becomes a re-verification
   of the value column that box backs: the value stays what the export holds
   and the links merge into the box. Its record_id changes to the value
   column's slug, the one change of key this script makes; it is only made
   where no review decision names the old id.

A deterministic repair, not new research: no value other than the link, no
verification and no `independent` flag changes. record_id stays the same
(rule 3's rekeyed re-verifications excepted), so review decisions keep their
keys. Dry run by default; --apply writes. Rebuild the review page and any
deliverable afterwards (a fresh stamp, never an overwrite).

Usage (from the repo root):
    python scripts/repair_staged.py batches/us-md/staging batches/us-ny/staging
    python scripts/repair_staged.py --all --apply
    python scripts/repair_staged.py --all --rules 3 --apply   # one rule only
"""
import argparse
import glob
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from assemble_state import (build_action, field_slug, load_export, unit_label,  # noqa: E402
                            values_equal)
from build_review_package import (_ws, additive_value, inline_value,  # noqa: E402
                                  validated_tier, value_cols_for)
from paths import gogpt_scoped_csv  # noqa: E402
from schema_constants import EVIDENCE_KEY, IDENTITY_COLUMNS, is_data_source_column  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
VALUE_LANES = ("updates", "newplants", "newunits")
IDENTITY_KEYS = {f"{c} Data Source" for c in IDENTITY_COLUMNS}
NAME_BOX = re.compile(r" Add (?P<links>the link below|the \d+ links below) to the "
                      r"(?:" + "|".join(re.escape(c) for c in IDENTITY_COLUMNS)
                      + r") Data Source box(?: on each unit)?\. Keep the links already there\.")


def _all_urls(rec, skip=()):
    out = set()
    for h in [rec] + list(rec.get("units") or []):
        for key, urls in (h.get("refs") or {}).items():
            if key not in skip:
                out |= {u for u in (urls or []) if u}
    return out


def fix_identity_refs(rec, problems, rid):
    """Rule 3a: a refs key named after a name column is dropped when its links
    sit elsewhere in the record, else renamed to EVIDENCE_KEY."""
    changed = False
    elsewhere = _all_urls(rec, skip=IDENTITY_KEYS)
    for r in [rec] + list(rec.get("units") or []):
        refs = r.get("refs") or {}
        for key in [k for k in refs if k in IDENTITY_KEYS]:
            urls = [u for u in (refs.pop(key) or []) if u]
            missing = [u for u in urls if u not in elsewhere]
            if missing:
                kept = refs.setdefault(EVIDENCE_KEY, [])
                kept += [u for u in missing if u not in kept]
                elsewhere |= set(missing)
            changed = True
        if r.get("action"):
            m = NAME_BOX.search(r["action"])
            if m:
                n = 1 if m.group("links") == "the link below" else int(m.group("links").split()[1])
                r["action"] = r["action"][:m.start()] + (
                    f" {m.group('links').capitalize()} {'are' if n > 1 else 'is'} the evidence "
                    "for the name. A name has no Data Source box, so there is no link to "
                    "add.") + r["action"][m.end():]
                changed = True
    return changed


class Export:
    """The scoped export, loaded once and only when rule 3b needs it."""
    rows = None

    @classmethod
    def row(cls, uid):
        if cls.rows is None:
            p = gogpt_scoped_csv()
            cls.rows = load_export(p)[1] if p.exists() else {}
        return cls.rows.get(uid) or {}


def rekey_box_record(rec, problems, rid, decided):
    """Rule 3b: a record whose fields are keyed on a Data Source column becomes
    a re-verification of the value column the box backs. Returns the new
    record, None to drop it, or False when nothing applies."""
    fields = rec.get("fields") or {}
    boxes = [c for c in fields if is_data_source_column(c)]
    if not boxes:
        return False
    if len(fields) != 1 or rec.get("units"):
        problems.append(f"{rid}: fields mix a Data Source column with others; left alone")
        return False
    box, value = boxes[0], _ws(fields[boxes[0]])
    uid = rec.get("gem_unit_id") or ""
    row = Export.row(uid)
    cands = value_cols_for(box)
    fits = [c for c in cands if row.get(c) and values_equal(c, row.get(c), value)]
    if not fits and not row:
        if len(cands) == 1:
            fits = cands
        elif value.lower() in ("exact", "approximate"):
            fits = ["Location accuracy"]
    if not fits:
        problems.append(f"{rid}: {box} value {value!r} matches no value column in the "
                        "export; left alone")
        return False
    if rid in decided:
        problems.append(f"{rid}: a review decision names this id; left alone")
        return False
    col = fits[0]
    current = row.get(col) or value
    urls = []
    for us in (rec.get("refs") or {}).values():
        urls += [u for u in (us or []) if u and u not in urls]
    pid = rec.get("gem_plant_id") or ""
    new = dict(rec)
    new.update({
        "record_id": f"{pid}:{uid}:{field_slug(col)}", "verdict": "match",
        "reverified": True, "fields": {col: current}, "current": {col: current},
        "refs": {box: urls},
        "action": build_action("reverified", col, current, current,
                               unit_label(rec.get("unit_name", ""), uid), box, len(urls))})
    return new


def decided_ids(path):
    log = path.parent / "review_log.jsonl"
    if not log.exists():
        return set()
    out = set()
    for line in log.read_text(encoding="utf-8").splitlines():
        try:
            out.add(json.loads(line).get("record_id"))
        except ValueError:
            pass
    return out


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


def repair_file(path, apply, rules=(1, 2, 3)):
    text = path.read_text(encoding="utf-8")
    data = json.loads(text)
    # keep the file's own indent so the diff shows only what changed
    m = re.search(r"\n( +)\S", text)
    indent = len(m.group(1)) if m else 2
    recs = data.get("records") if isinstance(data, dict) else data
    inlined, promoted, problems, rekeyed, named = [], [], [], [], []
    decided = decided_ids(path)
    ids = {r.get("record_id") for r in recs or []}
    kept = []
    for rec in recs or []:
        rid = rec.get("record_id") or rec.get("gem_unit_id") or "?"
        new = rekey_box_record(rec, problems, rid, decided) if 3 in rules else False
        if new:
            if new["record_id"] in ids:
                # the value column already has a record: give it the links
                twin = next(r for r in recs if r.get("record_id") == new["record_id"])
                box = next(iter(new["refs"]))
                have = twin.setdefault("refs", {}).setdefault(box, [])
                have += [u for u in new["refs"][box] if u not in have]
                twin.setdefault("verifications", [])
                twin["verifications"] += [v for v in rec.get("verifications") or []
                                          if v not in twin["verifications"]]
                rekeyed.append(f"{rid} merged into {new['record_id']}")
                continue
            ids.add(new["record_id"])
            rekeyed.append(f"{rid} -> {new['record_id']}")
            rec = new
        kept.append(rec)
        if 3 in rules and fix_identity_refs(rec, problems, rid):
            named.append(rid)
        for r in [rec] + list(rec.get("units") or []):
            if 1 in rules and inline_status_detail(r, problems, rid):
                inlined.append(rid)
        if 2 not in rules:
            continue
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
    changed = bool(inlined or promoted or rekeyed or named)
    if changed:
        if isinstance(data, dict):
            data["records"] = kept
        else:
            data = kept
    if apply and changed:
        path.write_text(json.dumps(data, indent=indent, ensure_ascii=False) + "\n", encoding="utf-8")
    return inlined, promoted, problems, rekeyed, named


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("staging", nargs="*", help="staging dirs")
    ap.add_argument("--all", action="store_true", help="every batches/*/staging dir")
    ap.add_argument("--apply", action="store_true", help="write the changes")
    ap.add_argument("--rules", default="1,2,3",
                    help="which rules to apply, comma-separated (default all three)")
    args = ap.parse_args(argv)
    rules = tuple(int(x) for x in args.rules.split(",") if x.strip())
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
            inlined, promoted, problems, rekeyed, named = repair_file(p, args.apply, rules)
            if not (inlined or promoted or problems or rekeyed or named):
                continue
            print(f"{p}: Status Detail entries laid out with their links {len(inlined)}, "
                  f"raised medium to high {len(promoted)}, box findings rekeyed "
                  f"{len(rekeyed)}, name-column links moved or dropped {len(named)}"
                  f"{'' if args.apply else ' (dry run)'}")
            for rid in promoted:
                print(f"  raised {rid}")
            for msg in rekeyed:
                print(f"  rekeyed {msg}")
            for rid in named:
                print(f"  name links {rid}")
            for msg in problems:
                print(f"  PROBLEM {msg}")


if __name__ == "__main__":
    main()

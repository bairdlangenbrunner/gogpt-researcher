#!/usr/bin/env python3
"""
List the comment threads left on one scope's plants in the GEM database (the
web form's Assigned Comments), so the update can answer them. This is the
manual's close-out step "Assigned Comments in the database are reviewed and
resolved" (Update SOP close-out, QC SOP §6).

Usage (from scripts/):
    python assigned_comments.py --state Iowa
    python assigned_comments.py --country Germany
    python assigned_comments.py --state Iowa --closeout   # exit 1 if any thread is open

Source: the `thread` and `comment` tables in the read-only GEM database. A
thread hangs on one plant (`project_id`, the number in the plant's L... ID) and
one form element (for example `units-100001071244-status_id`, a unit's status
box; the number is the unit's G... ID). Scope is the same as
validation_report.py: combustion plants in the country (and state) whose fuels
include fossil gas or fossil liquids. Deleted threads and comments are skipped.

Open threads (not marked completed) are the work: answer each in the batch or
list it for the person. Completed threads are listed too, newest first, since
a closed thread can still carry a lead (a link nobody followed up).

Writes work/comments_<tag>.json and work/comments_<tag>.md. Comment text is a
colleague's words: it stays under work/ (gitignored), and the memo names the
assignee and the writer by name, never by email.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from paths import work_dir
from build_state_brief import make_scope
from validation_report import engine

ELEMENT_UNIT = re.compile(r"^units-(\d+)-(.+)$")


def fetch(scope):
    from sqlalchemy import text
    where = ['not coalesce(p.deleted, false)', 'p."projectType" = 1',
             'p."fuelCategorySearch" && array[3, 4]::bigint[]',
             'c."gemName" ilike :country', 'not coalesce(t.deleted, false)']
    params = {"country": scope["country"]}
    if scope["kind"] == "state":
        where.append("p.subnational ilike :state")
        params["state"] = scope["name"]
    with engine().connect() as cx:
        threads = cx.execute(text(f"""
            select t.id, t.completed, t.element, t.created, t.modified, p.id, p.name,
                   trim(coalesce(a.first_name, '') || ' ' || coalesce(a.last_name, ''))
            from thread t
            join plant p on p.id = t.project_id
            join country c on c.id = any(p."countrySearch")
            left join auth_user a on a.id = t.assignee_id
            where {' and '.join(where)}
            order by t.completed, t.created desc"""), params).fetchall()
        ids = [t[0] for t in threads]
        comments = cx.execute(text("""
            select c.thread_id, c.created, c.comment,
                   trim(coalesce(a.first_name, '') || ' ' || coalesce(a.last_name, ''))
            from comment c left join auth_user a on a.id = c.creator_id
            where c.thread_id = any(:ids) and not coalesce(c.deleted, false)
            order by c.thread_id, c.id"""), {"ids": ids}).fetchall()
    by_thread = {}
    for tid, created, body, who in comments:
        by_thread.setdefault(tid, []).append(
            {"created": created.date().isoformat(), "by": who or "unknown",
             "text": (body or "").strip()})
    out = []
    for tid, done, element, created, modified, pid, pname, assignee in threads:
        m = ELEMENT_UNIT.match(element or "")
        out.append({"thread_id": tid, "open": not done, "plant_id": f"L{pid}",
                    "plant_name": pname, "unit_id": f"G{m.group(1)}" if m else None,
                    "box": m.group(2) if m else (element or ""),
                    "assignee": assignee or None,
                    "created": created.date().isoformat(),
                    "modified": modified.date().isoformat() if modified else None,
                    "comments": by_thread.get(tid, [])})
    return out


def memo(scope, threads, stamp):
    open_ = [t for t in threads if t["open"]]
    L = [f"# Assigned comments: {scope['name']}", "",
         f"Read from the GEM database on {stamp}. Plants whose fuels include fossil gas "
         "or fossil liquids.", "",
         f"- Open threads: {len(open_)}",
         f"- Completed threads: {len(threads) - len(open_)}", ""]
    for title, items in (("Open", open_),
                         ("Completed, newest first", [t for t in threads if not t["open"]])):
        L += [f"## {title}", ""]
        if not items:
            L += ["None.", ""]
            continue
        for t in items:
            where = f"unit {t['unit_id']}, box {t['box']}" if t["unit_id"] else f"box {t['box']}"
            L.append(f"- {t['plant_name']} ({t['plant_id']}), {where}. Started {t['created']}"
                     + (f", assigned to {t['assignee']}" if t["assignee"] else ", no assignee")
                     + ".")
            for c in t["comments"]:
                text = " ".join(c["text"].split())
                L.append(f"  - {c['created']}, {c['by']}: {text}")
        L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    who = ap.add_mutually_exclusive_group(required=True)
    who.add_argument("--state", help="a US state, e.g. Iowa")
    who.add_argument("--country", help="a country (Country/Area value), e.g. Germany")
    ap.add_argument("--closeout", action="store_true", help="exit 1 if any thread is open")
    ap.add_argument("--out-dir", default=None, help="default: <repo>/work")
    a = ap.parse_args()

    scope = make_scope(state=a.state, country=a.country)
    tag = f"us-{scope['slug']}" if scope["kind"] == "state" else scope["slug"]
    stamp = datetime.datetime.now().astimezone().isoformat(timespec="minutes")
    threads = fetch(scope)
    out = Path(a.out_dir) if a.out_dir else work_dir()
    out.mkdir(parents=True, exist_ok=True)
    jpath, mpath = out / f"comments_{tag}.json", out / f"comments_{tag}.md"
    jpath.write_text(json.dumps({"where": scope, "read": stamp, "threads": threads},
                                indent=2, ensure_ascii=False), encoding="utf-8")
    mpath.write_text(memo(scope, threads, stamp), encoding="utf-8")
    n_open = sum(t["open"] for t in threads)
    print(f"{scope['kind']}: {scope['name']}  threads: {len(threads)}  open: {n_open}")
    print(f"wrote {jpath}\nwrote {mpath}")
    if a.closeout:
        print("COMMENTS CLEAN" if not n_open else f"COMMENTS OPEN: {n_open} thread(s) to answer")
        sys.exit(1 if n_open else 0)


if __name__ == "__main__":
    main()

"""
Read a work Google Sheet through the gws CLI, work profile, read-only.

    from gsheets import list_tabs, read_tab
    tabs = list_tabs(spreadsheet_id)            # [{"title", "sheetId", "rows", "cols"}]
    rows = read_tab(spreadsheet_id, "MATCHED IDs")   # list of lists, row 1 first

Never a public export URL (user rule: anonymous access to work docs is withdrawn).
The work profile is ~/.config/gws-gem with the file keyring backend; if the
directory is missing or the token has expired, ask Baird to run the login in
his own shell (`gws-gem auth login`), never headless here.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

GEM_PROFILE = Path(os.environ.get("GWS_GEM_CONFIG_DIR", Path.home() / ".config" / "gws-gem"))


def _env():
    if not GEM_PROFILE.is_dir():
        sys.exit(f"ERROR: work gws profile {GEM_PROFILE} not found; set up gws-gem first")
    if not shutil.which("gws"):
        sys.exit("ERROR: gws CLI not on PATH (brew install gws)")
    env = dict(os.environ)
    env["GOOGLE_WORKSPACE_CLI_CONFIG_DIR"] = str(GEM_PROFILE)
    env["GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND"] = "file"
    return env


def _call(args, params):
    cmd = ["gws"] + args + ["--params", json.dumps(params)]
    p = subprocess.run(cmd, env=_env(), capture_output=True, text=True)
    out = p.stdout.strip()
    # gws prints a "Using keyring backend" line before the JSON on some versions.
    start = out.find("{")
    if p.returncode != 0 or start < 0:
        msg = (p.stderr or out).strip().splitlines()
        tail = " | ".join(msg[-3:]) if msg else "no output"
        if "401" in tail or "invalid_grant" in tail or "expired" in tail.lower():
            sys.exit("ERROR: the gws-gem login has expired; ask Baird to run "
                     "`gws-gem auth login` in his shell, then retry")
        sys.exit(f"ERROR: gws {' '.join(args)} failed: {tail}")
    return json.loads(out[start:])


def list_tabs(spreadsheet_id):
    d = _call(["sheets", "spreadsheets", "get"],
              {"spreadsheetId": spreadsheet_id,
               "fields": "properties.title,sheets.properties(title,sheetId,"
                         "gridProperties(rowCount,columnCount))"})
    out = []
    for s in d.get("sheets", []):
        p = s["properties"]
        g = p.get("gridProperties", {})
        out.append({"title": p["title"], "sheetId": p.get("sheetId"),
                    "rows": g.get("rowCount", 0), "cols": g.get("columnCount", 0)})
    return out


def read_tab(spreadsheet_id, tab, last_col="ZZ", last_row=None):
    """All values of a tab (trailing blank cells are omitted per row, as the API does)."""
    rng = f"'{tab}'!A1:{last_col}{last_row or ''}"
    d = _call(["sheets", "spreadsheets", "values", "get"],
              {"spreadsheetId": spreadsheet_id, "range": rng})
    return d.get("values", [])


def as_dicts(rows):
    """Row 1 is the header; later rows become dicts (missing cells → "")."""
    if not rows:
        return []
    hdr = [h.strip() for h in rows[0]]
    out = []
    for r in rows[1:]:
        out.append({h: (r[i].strip() if i < len(r) else "") for i, h in enumerate(hdr)})
    return out

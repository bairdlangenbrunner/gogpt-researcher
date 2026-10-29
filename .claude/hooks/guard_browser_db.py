#!/usr/bin/env python3
"""PreToolUse guard for Claude in Chrome tools in this repo
(docs/sops/database-browser-edits.md).

- Reading a page (screenshots, page text, finding elements, scrolling) is allowed
  without a prompt.
- Filling a field (form_input) is allowed: nothing is saved until a click.
- A click or a keystroke can save a change, so it always asks Baird, and it is
  refused outright in bypass, auto, or don't-ask mode. That ask is the approval
  before each save.
- Running page scripts, uploading files, running extension shortcuts, and batched
  browser actions are refused: each could change the database without its own ask.
- Opening a URL is allowed unless the path deletes, destroys, or merges something.

Reads the hook event JSON on stdin and prints a decision as JSON.
"""
import json
import re
import sys
from urllib.parse import urlparse

PREFIX = "mcp__claude-in-chrome__"
READ_TOOLS = {"tabs_context_mcp", "tabs_create_mcp", "tabs_close_mcp", "read_page", "find",
              "get_page_text", "read_console_messages", "read_network_requests",
              "resize_window", "gif_creator", "update_plan", "shortcuts_list"}
READ_ACTIONS = {"screenshot", "wait", "scroll", "scroll_to", "zoom", "hover", "mouse_move",
                "cursor_position"}
FILL_TOOLS = {"form_input"}
NEVER = {"javascript_tool", "upload_image", "shortcuts_execute", "browser_batch"}
UNSUPERVISED_MODES = {"bypassPermissions", "auto", "dontAsk"}
RISKY_PATH = re.compile(r"delete|destroy|remove|merge", re.I)
SOP = "docs/sops/database-browser-edits.md"


def decide(event: dict):
    """(decision, reason) for one tool call, or None to leave it to the normal rules."""
    tool = event.get("tool_name", "")
    if not tool.startswith(PREFIX):
        return None
    name = tool[len(PREFIX):]
    args = event.get("tool_input") or {}
    mode = event.get("permission_mode")
    if name in NEVER:
        return "deny", (f"{name} is not used in this repo: it could change the database "
                        f"without its own approval ({SOP} §4).")
    if name == "navigate":
        url = str(args.get("url") or "")
        if RISKY_PATH.search(urlparse(url).path):
            return "deny", f"That address looks like a delete or merge page ({SOP} §4)."
        return "allow", "Opening a page."
    if name in READ_TOOLS or (name == "computer" and args.get("action") in READ_ACTIONS):
        return "allow", "Reading the page."
    if name in FILL_TOOLS:
        return "allow", "Filling a field. Nothing is saved until a click."
    if mode in UNSUPERVISED_MODES:
        return "deny", (f"Clicks and keystrokes in the browser need Baird's approval, and this "
                        f"session is in {mode} mode. Ask Baird to switch to default mode "
                        f"(shift+tab) or to relaunch with --permission-mode default ({SOP} §2).")
    return "ask", ("This click or keystroke may save a change to the GEM database. Approve it "
                   "only if it matches the step Claude just described in the chat.")


def main():
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return
    result = decide(event)
    if result is None:
        return
    decision, reason = result
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                             "permissionDecision": decision,
                                             "permissionDecisionReason": reason}}))


if __name__ == "__main__":
    main()

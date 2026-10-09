#!/usr/bin/env python3
"""Rebuild access_log.csv: every web request made for the emissions workstream.

Reads the Claude Code session transcripts listed in sessions.txt (main
conversation plus subagents) and records each web fetch, web search, URL in
a shell command, and Google Workspace read. One row per distinct
(session, agent, tool, target), with first-seen time and hit count.

What it records and what it doesn't:
- URLs only. Local paths, command text and response bodies are not copied.
- Google reads name the file id or Gmail query/thread id, never the content.
- URLs built from shell variables ($BASE/...) are kept as written and flagged
  `unresolved`; downloads.csv carries the resolved URL for anything saved.

Usage (from emissions/sources/):
    python build_access_log.py            # rewrite access_log.csv
    python build_access_log.py --check    # print counts, write nothing

Add a line to sessions.txt at the end of every working session.
"""
import argparse
import csv
import glob
import json
import os
import re
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
TRANSCRIPTS = os.path.expanduser(
    '~/.claude/projects/-Users-baird-Dropbox--git-ALL--github-repos-gem-gogpt-researcher/')
URL = re.compile(r"https?://[^\s'\"\\)<>`|]+")
FIELDS = ['first_seen_utc', 'session', 'agent', 'tool', 'host', 'target', 'hits', 'flag']


def sessions():
    out = []
    for line in open(os.path.join(HERE, 'sessions.txt')):
        line = line.split('#', 1)[0].strip()
        if line:
            out.append(line)
    return out


def tool_uses(session):
    main = os.path.join(TRANSCRIPTS, session + '.jsonl')
    subs = sorted(glob.glob(os.path.join(TRANSCRIPTS, session, '**', '*.jsonl'), recursive=True))
    for path in [main] + subs:
        if not os.path.exists(path):
            continue
        agent = 'main' if path == main else 'subagent'
        for line in open(path):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            msg = d.get('message')
            content = msg.get('content') if isinstance(msg, dict) else None
            if not isinstance(content, list):
                continue
            for b in content:
                if b.get('type') == 'tool_use':
                    yield d.get('timestamp', ''), agent, b.get('name', ''), b.get('input') or {}


def gws_targets(cmd):
    """Google Workspace reads, counted by kind only. File IDs, thread IDs, and search
    queries are not recorded: they name colleagues and internal files, and this log
    is published in a public repo."""
    out = []
    for m in re.finditer(r'"(?:fileId|spreadsheetId)"\s*:\s*\\?"([\w-]{20,})', cmd):
        out.append(('gws-drive', 'drive file (id withheld)'))
    for m in re.finditer(r'\bfor (?:id|t) in ([\w\s-]+?);', cmd):
        for tok in m.group(1).split():
            if len(tok) >= 25:
                out.append(('gws-drive', 'drive file (id withheld)'))
            elif re.fullmatch(r'[0-9a-f]{16}', tok):
                out.append(('gws-gmail', 'gmail thread (id withheld)'))
    if 'gmail users threads list' in cmd:
        for m in re.finditer(r"for q in ((?:'[^']*'\s*)+);", cmd):
            for q in re.findall(r"'([^']*)'", m.group(1)):
                out.append(('gws-gmail', 'gmail search (query withheld)'))
    return out


def rows_for(session):
    seen = {}

    def add(ts, agent, tool, target, flag=''):
        host = urlparse(target).netloc if target.startswith('http') else ''
        key = (agent, tool, target)
        if key in seen:
            seen[key]['hits'] += 1
        else:
            seen[key] = dict(first_seen_utc=ts[:19].replace('T', ' '), session=session[:8], agent=agent,
                             tool=tool, host=host, target=target, hits=1, flag=flag)

    for ts, agent, name, inp in tool_uses(session):
        if name == 'WebFetch':
            add(ts, agent, 'webfetch', inp.get('url', ''))
        elif name == 'WebSearch':
            add(ts, agent, 'websearch', inp.get('query', ''))
        elif name == 'Bash':
            cmd = inp.get('command', '')
            # Skip this script's own runs and transcript-mining one-offs.
            if 'build_access_log' in cmd or '.jsonl' in cmd:
                continue
            for u in URL.findall(cmd):
                u = u.rstrip('.,;')
                add(ts, agent, 'shell', u, 'unresolved' if '$' in u else '')
            if re.search(r'\bgws\b', cmd):
                for tool, target in gws_targets(cmd):
                    add(ts, agent, tool, target)
        elif name.startswith('mcp__') and 'Docs' in name and name.rsplit('__', 1)[-1] in ('read', 'export'):
            cid = (inp.get('container') or {}).get('id') or (inp.get('ref') or {}).get('id', '')
            add(ts, agent, 'claude-docs', 'own draft doc ' + cid)
    return sorted(seen.values(), key=lambda r: r['first_seen_utc'])


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    rows = [r for s in sessions() for r in rows_for(s)]
    by_tool = {}
    for r in rows:
        by_tool[r['tool']] = by_tool.get(r['tool'], 0) + 1
    print(len(rows), 'rows', by_tool)
    if args.check:
        return
    with open(os.path.join(HERE, 'access_log.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


if __name__ == '__main__':
    main()

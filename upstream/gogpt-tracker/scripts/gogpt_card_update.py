#!/usr/bin/env python3
"""
GOGPT Context Card Updater
==========================
Reads an existing context card .md file, replaces or appends content into
a named section, marks that session as done in the session log, and writes
the updated card to /mnt/user-data/outputs/ for download.

Usage (Claude calls this automatically at the end of each session):

  python3 gogpt_card_update.py \\
    --card   "/mnt/user-data/uploads/GOGPT_ContextCard_Japan_Q2_2026.md" \\
    --section "6b" \\
    --session "3" \\
    --content-file "/tmp/gogpt_session_output.txt"

  # Or pass content inline (for short blocks):
  python3 gogpt_card_update.py \\
    --card   "/mnt/user-data/uploads/GOGPT_ContextCard_Japan_Q2_2026.md" \\
    --section "6b" \\
    --session "3" \\
    --content "🔄 UPDATE — ..."

  # Preview diff without writing:
  python3 gogpt_card_update.py ... --dry-run

  # Drive sync metadata (first call each session — drives cycle/version naming):
  python3 gogpt_card_update.py --country "Japan" --drive-meta
  python3 gogpt_card_update.py --country "Japan" --drive-meta --current-version 3
  python3 gogpt_card_update.py --country "Texas" --drive-meta --cycle-tag 20260530

Drive versioning
----------------
The durable card lives in the Google Drive folder "GOGPT Context Cards" as
GOGPT_ContextCard_[Country]_[CycleTag]_v[N].md.

Two separate ideas:
  • CycleTag (YYYYMMDD) — which research cycle, defined by the dated GEM data
    dump it is built on. A RERUN against a fresh dump is a NEW cycle (new tag)
    and restarts at v1, so it never collides with the prior cycle's files.
  • v[N] — progress within a cycle. Each session pulls the highest-N file for
    the current cycle, edits it, and pushes back as v[N+1].

"Current card" = highest v[N] within the LATEST CycleTag. Older versions and
older whole cycles stay in the folder as an audit trail.

Legacy untagged names stay resolvable as history and always sort older than any
dated cycle: GOGPT_ContextCard_[Country]_v[N].md and the original single-cycle
GOGPT_ContextCard_[Country]_Q2_2026.md (= v1). --drive-meta reports CYCLE_TAG,
the cycle-scoped SEARCH_PATTERN, the read/write filenames and the local
WORK_PATH; the skill passes --cycle-tag (or it is derived from the latest dump)
and --current-version with the highest version its cycle-scoped Drive search found.

Sections
--------
  1       Unit counts          (replaces placeholder table)
  2       Country context      (replaces placeholder fields)
  3       Sources & keywords   (replaces placeholder fields)
  4       Regions              (replaces placeholder table)
  5       Flag counts          (replaces placeholder table)
  6a      New proposals
  6b      In-development flags
  6c      Shelved/cancelled flags
  6d      Operating flags
  6e      Retired/mothballed flags
  6f      GEM possible updates
  6g      In-progress (⏳) units + duplicate (⚠️) candidates
  7       Wrap-up notes

Session log tokens (for --session flag)
---------------------------------------
  0, 1, 2, 2b, 2c, 3, 4, 5, 6, 7, 8
"""

# CHANGELOG 2026-05-30: card naming moved from bare GOGPT_ContextCard_[Country]_v[N].md
# to cycle-tagged GOGPT_ContextCard_[Country]_[CycleTag]_v[N].md (CycleTag = YYYYMMDD of
# the GEM dump). 'Current card' = highest v within the latest cycle. Reruns against a new
# dump start a new cycle at v1. Legacy untagged names still resolve and sort oldest.
import argparse, os, re, sys, textwrap
from datetime import date

# ── Section markers ────────────────────────────────────────────────────────────
# Each section in the template is bounded by two comment markers.
# The updater replaces everything between <!-- SECTION:X:START --> and
# <!-- SECTION:X:END --> with the new content.

SECTION_MARKERS = {
    "1":  ("<!-- SECTION:1:START -->",  "<!-- SECTION:1:END -->"),
    "2":  ("<!-- SECTION:2:START -->",  "<!-- SECTION:2:END -->"),
    "3":  ("<!-- SECTION:3:START -->",  "<!-- SECTION:3:END -->"),
    "4":  ("<!-- SECTION:4:START -->",  "<!-- SECTION:4:END -->"),
    "5":  ("<!-- SECTION:5:START -->",  "<!-- SECTION:5:END -->"),
    "6a": ("<!-- SECTION:6a:START -->", "<!-- SECTION:6a:END -->"),
    "6b": ("<!-- SECTION:6b:START -->", "<!-- SECTION:6b:END -->"),
    "6c": ("<!-- SECTION:6c:START -->", "<!-- SECTION:6c:END -->"),
    "6d": ("<!-- SECTION:6d:START -->", "<!-- SECTION:6d:END -->"),
    "6e": ("<!-- SECTION:6e:START -->", "<!-- SECTION:6e:END -->"),
    "6f": ("<!-- SECTION:6f:START -->", "<!-- SECTION:6f:END -->"),
    "6g": ("<!-- SECTION:6g:START -->", "<!-- SECTION:6g:END -->"),
    "7":  ("<!-- SECTION:7:START -->",  "<!-- SECTION:7:END -->"),
}

# Session log row tokens — matched by the | N | ... | ☐ | pattern
SESSION_LOG_TOKENS = {
    "0": "0", "1": "1", "2": "2", "2b": "2b", "2c": "2c",
    "3": "3", "4": "4",  "5": "5", "6": "6", "7": "7", "8": "8",
}

from gogpt_paths import OUTPUT_DIR, WORK_DIR, UPLOADS_DIR, DATA_DIR

# OUTPUT_DIR : where compiled files + updated cards are written (download copy)
# WORK_DIR   : persistent working copy of the context card, so the researcher
#              never has to re-download/re-upload it between sessions. Every
#              write is mirrored to OUTPUT_DIR so a fresh download is on demand.
# UPLOADS_DIR: where freshly-uploaded cards/dumps are looked for.
# All three are resolved by gogpt_paths (env-overridable, repo-relative
# defaults, legacy /mnt fallback).

CARD_GLOB = "GOGPT_ContextCard_*.md"

# ── Drive context-card versioning ───────────────────────────────────────────────
# The durable card lives in Google Drive under a cycle-tagged, versioned name:
#   GOGPT_ContextCard_[Country]_[CycleTag]_v[N].md
#
# Two independent concepts are kept separate:
#   • CycleTag  — which research cycle this card belongs to. It is the dated GEM
#                 data dump the cycle is built on (YYYYMMDD, e.g. 20260530). A
#                 RERUN against a fresh dump is a NEW cycle (new tag), NOT a
#                 continuation of the old one — so it starts again at v1 and can
#                 never collide with the prior cycle's files.
#   • v[N]      — progress WITHIN a cycle. Each session pulls the highest-N file
#                 for the current cycle, edits it, and pushes back as v[N+1].
#
# "Current card" = highest v[N] within the LATEST CycleTag (latest = newest date).
# Older versions, and entire older cycles, remain in the folder as an audit trail
# and are only ever removed by a human.
#
# Legacy names (no cycle tag) are still recognised so older cards stay resolvable:
#   • GOGPT_ContextCard_[Country]_v[N].md   — bare versioned (pre-cycle-tag scheme)
#   • GOGPT_ContextCard_[Country]_Q2_2026.md — original single-cycle name (= v1)
# Legacy cards are treated as belonging to a sentinel "legacy" cycle that always
# sorts OLDER than any dated cycle, so any new dated-cycle card supersedes them
# as the current card without overwriting them.
DRIVE_FOLDER_ID = "15u00c_NMYyokIfbzWoDXBvcix3sqm-h4"   # "GOGPT Context Cards"

# Cycle-tagged versioned name: ..._[CycleTag]_v[N].md  (CycleTag = 8-digit date).
_CYCLE_RE   = re.compile(
    r"^GOGPT_ContextCard_(?P<country>.+)_(?P<tag>\d{8})_v(?P<n>\d+)\.md$")
# Legacy bare-versioned name: ..._v[N].md  (no cycle tag).
_VERSION_RE = re.compile(r"^GOGPT_ContextCard_(?P<country>.+)_v(?P<n>\d+)\.md$")
# Legacy original single-cycle name (treated as v1).
_LEGACY_RE  = re.compile(r"^GOGPT_ContextCard_(?P<country>.+)_Q2_2026\.md$")

# Sentinel cycle tag for legacy (untagged) cards. Sorts older than any real date.
_LEGACY_TAG = "00000000"


def _safe_country(country: str) -> str:
    """Filename-safe country/state token: spaces -> underscores, trimmed."""
    return country.strip().replace(" ", "_")


def parse_card_name(filename: str):
    """Decode a card filename into (country, cycle_tag, version).

    - '..._Texas_20260530_v2.md'  -> ('Texas', '20260530', 2)
    - '..._Texas_v9.md'           -> ('Texas', '00000000', 9)   (legacy, untagged)
    - '..._Texas_Q2_2026.md'      -> ('Texas', '00000000', 1)   (legacy original)
    - anything else               -> None
    Legacy cards use the sentinel tag so they sort older than any dated cycle.
    """
    base = os.path.basename(filename)
    m = _CYCLE_RE.match(base)
    if m:
        return m.group("country"), m.group("tag"), int(m.group("n"))
    m = _VERSION_RE.match(base)
    if m:
        return m.group("country"), _LEGACY_TAG, int(m.group("n"))
    m = _LEGACY_RE.match(base)
    if m:
        return m.group("country"), _LEGACY_TAG, 1
    return None


def parse_version(filename: str):
    """Return the integer version encoded in a card filename (or None).

    Kept for back-compat. Use parse_card_name for cycle-aware decoding.
    """
    decoded = parse_card_name(filename)
    return decoded[2] if decoded else None


def versioned_name(country: str, n: int, cycle_tag: str = None) -> str:
    """Build a card filename for a country, version and (optional) cycle tag.

    With a cycle tag -> the new scheme: ..._[tag]_v[N].md.
    Without (or sentinel) -> legacy bare-versioned: ..._v[N].md.
    """
    safe = _safe_country(country)
    if cycle_tag and cycle_tag != _LEGACY_TAG:
        return f"GOGPT_ContextCard_{safe}_{cycle_tag}_v{n}.md"
    return f"GOGPT_ContextCard_{safe}_v{n}.md"


def highest_version(filenames, country: str = None, cycle_tag: str = None):
    """Return (best_filename, best_n) for the current card among `filenames`.

    "Current" = highest version within the latest cycle. Selection order:
      1. If `cycle_tag` is given, consider ONLY cards in that cycle, and return
         the highest version within it (0 if none — a fresh cycle starts at v1).
      2. Otherwise, find the latest cycle tag present (dated tags beat the legacy
         sentinel; newest date wins) and return the highest version within it.
    If `country` is given, only that country's cards are considered. Returns
    (None, 0) when nothing matches.
    """
    safe = _safe_country(country) if country else None
    best_name, best_tag, best_n = None, None, 0
    for f in filenames:
        decoded = parse_card_name(f)
        if not decoded:
            continue
        c, tag, n = decoded
        if safe and c != safe:
            continue                      # avoid Japan vs Japan_North bleed
        if cycle_tag is not None and tag != cycle_tag:
            continue                      # restricted to one cycle
        # Order by (cycle tag, version). Dated tags sort naturally; the legacy
        # sentinel "00000000" sorts oldest. Within a tie on tag, higher version
        # wins; on a tie there too, prefer a real cycle-tagged file over legacy.
        is_tagged = bool(_CYCLE_RE.match(os.path.basename(f)))
        if best_name is None:
            better = True
        elif tag != best_tag:
            better = tag > best_tag
        elif n != best_n:
            better = n > best_n
        else:
            better = is_tagged and best_tag == _LEGACY_TAG
        if better:
            best_name, best_tag, best_n = f, tag, n
    return best_name, best_n


def latest_cycle_tag(filenames, country: str = None):
    """Return the latest cycle tag present among `filenames` (or None).

    Dated tags (YYYYMMDD) beat the legacy sentinel; newest date wins.
    """
    safe = _safe_country(country) if country else None
    best = None
    for f in filenames:
        decoded = parse_card_name(f)
        if not decoded:
            continue
        c, tag, _ = decoded
        if safe and c != safe:
            continue
        if best is None or tag > best:
            best = tag
    return best


# Matches a GEM data dump filename and captures its 8-digit date:
#   GOGPTall20260530T153641.xlsx  ->  20260530
_DUMP_RE = re.compile(r"GOGPTall(?P<tag>\d{8})T\d+\.(?:xlsx|csv)$", re.IGNORECASE)


def derive_cycle_tag(search_dirs=None):
    """Derive the current cycle tag (YYYYMMDD) from the latest GEM data dump.

    The cycle a card belongs to is defined by the dated dump it is built on, so
    the tag is read from the newest GOGPTall<date>T<time>.(xlsx|csv) file found in
    the project / uploads directories. Returns the tag string, or None if no dump
    is present (caller then falls back to today's date or an explicit --cycle-tag).
    """
    import glob
    if search_dirs is None:
        search_dirs = (DATA_DIR, UPLOADS_DIR, WORK_DIR, OUTPUT_DIR)
    best_tag = None
    for d in search_dirs:
        for ext in ("xlsx", "csv"):
            for f in glob.glob(os.path.join(d, f"GOGPTall*.{ext}")):
                m = _DUMP_RE.search(os.path.basename(f))
                if not m:
                    continue
                tag = m.group("tag")
                if best_tag is None or tag > best_tag:
                    best_tag = tag
    return best_tag


def _newest(paths):
    """Return the most recently modified path from a list, or None."""
    paths = [p for p in paths if p and os.path.exists(p)]
    if not paths:
        return None
    return max(paths, key=os.path.getmtime)


def resolve_card(card_arg: str = None, country: str = None) -> str:
    """Resolve the authoritative working-copy path for the context card.

    Resolution order (first hit wins):
      1. An explicit --card path that already lives in WORK_DIR.
      2. A card already in WORK_DIR (highest version if several) — the persisted copy.
      3. An explicit --card path elsewhere (uploads/outputs) -> copied into WORK_DIR.
      4. Highest-version matching card in OUTPUT_DIR -> copied into WORK_DIR.
      5. Highest-version matching card in UPLOADS_DIR -> copied into WORK_DIR.

    The returned path is ALWAYS inside WORK_DIR, so all reads and writes happen
    against one persistent copy. Country, if given, narrows the glob.

    "Highest version" beats "most recently modified": cards are named
    GOGPT_ContextCard_[Country]_v[N].md (legacy _Q2_2026 = v1), and the current
    card is the one with the largest N, regardless of file mtime.
    """
    import glob, shutil
    os.makedirs(WORK_DIR, exist_ok=True)

    pattern = CARD_GLOB
    if country:
        pattern = f"GOGPT_ContextCard_{_safe_country(country)}_*.md"

    def _pick(globbed):
        """Highest-version card from a glob list, falling back to newest mtime."""
        if not globbed:
            return None
        best, n = highest_version(globbed, country)
        return best if best else _newest(globbed)

    # 1 & 2: explicit arg already in WORK_DIR, or any existing WORK_DIR copy
    if card_arg and os.path.dirname(os.path.abspath(card_arg)) == WORK_DIR \
            and os.path.exists(card_arg):
        return card_arg
    work_hit = _pick(glob.glob(os.path.join(WORK_DIR, pattern)) or
                     glob.glob(os.path.join(WORK_DIR, CARD_GLOB)))
    if work_hit and not card_arg:
        return work_hit

    # 3: explicit arg elsewhere -> copy into WORK_DIR
    if card_arg and os.path.exists(card_arg):
        dest = os.path.join(WORK_DIR, os.path.basename(card_arg))
        # Only copy in if the working copy is missing or older than the source.
        if not os.path.exists(dest) or os.path.getmtime(card_arg) > os.path.getmtime(dest):
            shutil.copy2(card_arg, dest)
        return dest
    if work_hit:
        return work_hit

    # 4 & 5: discover highest-version card in outputs, then uploads
    for search_dir in (OUTPUT_DIR, UPLOADS_DIR):
        hit = _pick(glob.glob(os.path.join(search_dir, pattern)) or
                    glob.glob(os.path.join(search_dir, CARD_GLOB)))
        if hit:
            dest = os.path.join(WORK_DIR, os.path.basename(hit))
            if not os.path.exists(dest) or os.path.getmtime(hit) > os.path.getmtime(dest):
                shutil.copy2(hit, dest)
            return dest

    return None  # nothing found anywhere


def read_card(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_card(path: str, content: str, dry_run: bool = False) -> str:
    """Write the updated card to BOTH the persistent working copy and OUTPUT_DIR.

    `path` is expected to already be the WORK_DIR copy (see resolve_card). We
    write there first (authoritative, survives to the next session in this
    conversation) and mirror to OUTPUT_DIR so a download link is always fresh.
    Returns the OUTPUT_DIR path (what gets presented to the researcher).
    """
    filename = os.path.basename(path)
    work_path = os.path.join(WORK_DIR, filename)
    out_path  = os.path.join(OUTPUT_DIR, filename)
    if not dry_run:
        os.makedirs(WORK_DIR, exist_ok=True)
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        with open(work_path, "w", encoding="utf-8") as f:
            f.write(content)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
    return out_path


def update_section(card: str, section: str, new_content: str) -> str:
    """Replace content between section markers."""
    if section not in SECTION_MARKERS:
        raise ValueError(f"Unknown section '{section}'. Valid: {list(SECTION_MARKERS)}")

    start_marker, end_marker = SECTION_MARKERS[section]

    if start_marker not in card:
        raise ValueError(
            f"Start marker for section {section} not found in card.\n"
            f"Expected: {start_marker}\n"
            f"Make sure you are using the latest COUNTRY_CONTEXT_CARD_TEMPLATE.md"
        )
    if end_marker not in card:
        raise ValueError(f"End marker for section {section} not found in card.")

    # Build replacement — keep markers, replace content between them
    before = card[:card.index(start_marker) + len(start_marker)]
    after  = card[card.index(end_marker):]

    new_content = new_content.strip("\n")
    updated = f"{before}\n\n{new_content}\n\n{after}"
    return updated


def mark_session_done(card: str, session: str) -> str:
    """Replace ☐ with ✅ and add today's date in the session log row."""
    if session not in SESSION_LOG_TOKENS:
        print(f"  ⚠️  Unknown session '{session}' — session log not updated.")
        return card

    token = SESSION_LOG_TOKENS[session]
    today = date.today().strftime("%-d %b %Y")

    # Match the row: | 2b | ... | ☐ | |
    # We match on the session number in the first cell, then replace ☐ with ✅ and fill date
    pattern = rf'(\|\s*{re.escape(token)}\s*\|[^|]*\|[^|]*\|)\s*☐\s*(\|)\s*(\|)'
    replacement = rf'\g<1> ✅ \g<2> {today} \g<3>'
    updated, n = re.subn(pattern, replacement, card)

    if n == 0:
        # Try simpler pattern — ☐ might already be on separate columns
        pattern2 = rf'(\|\s*{re.escape(token)}\s*\|)(.*?)(☐)(.*?\|)(.*?\|)'
        replacement2 = rf'\g<1>\g<2>✅\g<4> {today} |'
        updated, n = re.subn(pattern2, replacement2, card)

    if n == 0:
        print(f"  ⚠️  Could not find session {session} row in session log — log not updated.")
        return card

    return updated


def diff_summary(original: str, updated: str, section: str) -> None:
    """Print a brief summary of what changed."""
    orig_lines = original.splitlines()
    upd_lines  = updated.splitlines()
    added   = sum(1 for l in upd_lines  if l not in orig_lines)
    removed = sum(1 for l in orig_lines if l not in upd_lines)
    print(f"  Section {section}: +{added} lines, -{removed} lines")


def main():
    parser = argparse.ArgumentParser(description="GOGPT Context Card Updater")
    parser.add_argument("--card",         default=None,   help="Path to context card .md (optional — auto-resolved to the persistent working copy if omitted)")
    parser.add_argument("--country",      default=None,   help="Country/state name — narrows auto-resolution when --card is omitted")
    parser.add_argument("--section",      default=None,   help="Section to update: 1, 2, 3, 4, 5, 6a–6f, 7")
    parser.add_argument("--session",      default=None,   help="Session number to mark done in session log: 0–8, 2b, 2c")
    parser.add_argument("--content",      default=None,   help="Content string to write into section")
    parser.add_argument("--content-file", default=None,   help="Path to file containing content to write")
    parser.add_argument("--dry-run",      action="store_true", help="Preview changes without writing")
    parser.add_argument("--append",       action="store_true", help="Append to existing section content instead of replacing")
    parser.add_argument("--resolve-card", action="store_true", help="Resolve and print the working-copy card path, then exit (no update)")
    parser.add_argument("--drive-meta",   action="store_true", help="Print Drive sync metadata (filenames, paths, versions) for the country, then exit")
    parser.add_argument("--current-version", default=None, type=int, help="Highest version found in Drive for this country WITHIN THE CURRENT CYCLE (passed by the skill from its Drive search); used to compute the next version")
    parser.add_argument("--cycle-tag", default=None, help="Cycle tag (YYYYMMDD) identifying the research cycle = the dated GEM dump it is built on. Defaults to the latest GOGPTall dump found, else today's date. A rerun against a new dump is a new cycle and restarts at v1.")
    args = parser.parse_args()

    # ── --drive-meta: report Drive sync metadata and exit ─────────────────────
    # This is the FIRST call every skill makes. It tells the skill:
    #   • SEARCH_PATTERN  — what to look for in the Drive folder
    #   • CURRENT_VERSION — the highest version we believe exists (0 = brand-new)
    #   • CURRENT_FILENAME / NEXT_FILENAME — read this, push that
    #   • WORK_PATH       — where to write the pulled card locally (versioned name)
    #   • DRIVE_FOLDER_ID — the "GOGPT Context Cards" folder
    # Version source priority: explicit --current-version (from the skill's Drive
    # search) > highest version among local working/output/upload copies > 0.
    if args.drive_meta:
        if not args.country:
            print("ERROR: --drive-meta requires --country")
            sys.exit(1)
        import glob as _glob
        safe = _safe_country(args.country)

        # Resolve the cycle tag this card belongs to: explicit flag > latest GEM
        # dump found locally > today's date (last-resort for a brand-new env).
        cycle_tag = args.cycle_tag or derive_cycle_tag() or date.today().strftime("%Y%m%d")

        # Determine the current (highest) version WITHIN THIS CYCLE.
        #   • explicit --current-version (from the skill's cycle-scoped Drive search)
        #   • else highest version among local copies for THIS cycle tag
        # A fresh cycle has no prior version -> cur = 0 -> first push is v1.
        if args.current_version is not None:
            cur = max(0, args.current_version)
        else:
            local = []
            for d in (WORK_DIR, OUTPUT_DIR, UPLOADS_DIR):
                local += _glob.glob(os.path.join(d, f"GOGPT_ContextCard_{safe}_*.md"))
            _, cur = highest_version(local, args.country, cycle_tag=cycle_tag)

        # Detect whether any LEGACY (untagged) card exists locally — used to warn
        # that a mid-cycle migration may be in play. The skill should confirm with
        # the researcher whether this dump is genuinely a NEW cycle (start v1 under
        # the dated tag) or a continuation of a legacy cycle (in which case pass
        # --cycle-tag matching the legacy dump, or keep using the legacy name).
        local_all = []
        for d in (WORK_DIR, OUTPUT_DIR, UPLOADS_DIR):
            local_all += _glob.glob(os.path.join(d, f"GOGPT_ContextCard_{safe}_*.md"))
        legacy_present = any(
            parse_card_name(f) and parse_card_name(f)[1] == _LEGACY_TAG
            for f in local_all
        )

        nxt = cur + 1 if cur >= 1 else 1   # fresh cycle starts at v1
        current_filename = versioned_name(args.country, cur, cycle_tag) if cur >= 1 else None
        next_filename    = versioned_name(args.country, nxt, cycle_tag)
        work_path        = os.path.join(WORK_DIR, next_filename if cur == 0
                                        else (current_filename or next_filename))

        print(f"DRIVE_FOLDER_ID={DRIVE_FOLDER_ID}")
        print(f"CYCLE_TAG={cycle_tag}")
        # Cycle-scoped search first (current cycle's versions), then a broad
        # fallback pattern so the skill can still discover legacy/older-cycle
        # cards when the current cycle has no card yet.
        print(f"SEARCH_PATTERN=GOGPT_ContextCard_{safe}_{cycle_tag}_v*.md")
        print(f"SEARCH_PATTERN_ALL=GOGPT_ContextCard_{safe}_*.md")
        print(f"LEGACY_NAME=GOGPT_ContextCard_{safe}_Q2_2026.md")
        print(f"CURRENT_VERSION={cur}")
        print(f"CURRENT_FILENAME={current_filename or '(none — fresh cycle)'}")
        print(f"NEXT_FILENAME={next_filename}")
        print(f"WORK_PATH={work_path}")
        print(f"CARD_FILENAME={next_filename}")   # back-compat alias: what we WRITE
        print(f"LEGACY_PRESENT={'yes' if legacy_present else 'no'}")
        if legacy_present and cur == 0:
            print("MIGRATION_NOTE=Only legacy/untagged cards found locally and no "
                  f"card for cycle {cycle_tag} yet. If this dump is a NEW cycle, "
                  "the first push migrates to the dated name at v1 (legacy stays as "
                  "history). If it is a CONTINUATION of the legacy cycle, confirm "
                  "with the researcher and pass --cycle-tag for that cycle instead.")
        sys.exit(0)

    # Always operate on the persistent copy in WORK_DIR so the researcher never
    # has to re-upload the card between sessions in this conversation.
    card_path = resolve_card(args.card, args.country)

    # --resolve-card: just report the path (or absence) and exit.
    if args.resolve_card:
        if card_path:
            print(card_path)
            sys.exit(0)
        print("NO_CARD_FOUND")
        sys.exit(2)

    if card_path is None:
        print("ERROR: No context card found. Looked in:")
        print(f"  working copy: {WORK_DIR}")
        print(f"  outputs:      {OUTPUT_DIR}")
        print(f"  uploads:      {UPLOADS_DIR}")
        print("Run 'Set up [country]' first, or upload the renamed context card once.")
        sys.exit(1)

    # ── Validate inputs ───────────────────────────────────────────────────────
    if not args.section:
        print("ERROR: --section is required for an update.")
        sys.exit(1)

    if args.content is None and args.content_file is None:
        print("ERROR: Provide either --content or --content-file")
        sys.exit(1)

    if args.content_file:
        if not os.path.exists(args.content_file):
            print(f"ERROR: Content file not found: {args.content_file}")
            sys.exit(1)
        with open(args.content_file, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = args.content

    # ── Read card (from the persistent working copy) ──────────────────────────
    original = read_card(card_path)
    updated  = original

    # ── Handle append mode ────────────────────────────────────────────────────
    if args.append:
        start_marker, end_marker = SECTION_MARKERS.get(args.section, (None, None))
        if start_marker and start_marker in original and end_marker in original:
            # Extract existing content between markers
            start_idx = original.index(start_marker) + len(start_marker)
            end_idx   = original.index(end_marker)
            existing  = original[start_idx:end_idx].strip()
            # Strip placeholder text
            placeholder_patterns = [
                r"\*\(paste [^)]+\)\*",
                r"_\(paste [^)]+\)_",
                r"\(paste [^)]+\)",
                r"\*\(no output yet[^)]*\)\*",
            ]
            for pat in placeholder_patterns:
                existing = re.sub(pat, "", existing).strip()
            if existing:
                content = existing + "\n\n---\n\n" + content.strip()

    # ── Update section ────────────────────────────────────────────────────────
    try:
        updated = update_section(updated, args.section, content)
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    # ── Mark session done ─────────────────────────────────────────────────────
    if args.session:
        updated = mark_session_done(updated, args.session)

    # ── Output ────────────────────────────────────────────────────────────────
    print(f"\n{'DRY RUN — ' if args.dry_run else ''}Context card update: {os.path.basename(card_path)}")
    print(f"  Working copy: {card_path}")
    diff_summary(original, updated, args.section)

    if args.session:
        print(f"  Session log: session {args.session} marked ✅")

    out_path = write_card(card_path, updated, dry_run=args.dry_run)

    if not args.dry_run:
        print(f"\n  ✅ Card updated in place (working copy + download copy).")
        print(f"  Download copy: {out_path}")
        print(f"  No re-upload needed — the next session reads the working copy automatically.\n")
    else:
        print(f"\n  [dry run — no file written]\n")


if __name__ == "__main__":
    main()

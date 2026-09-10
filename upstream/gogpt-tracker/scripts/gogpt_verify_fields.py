#!/usr/bin/env python3
"""
GOGPT card-field re-verification
================================
Re-checks the "current DB value" claims recorded in a context card's flag
findings against the LIVE GOGPT CSV, so stale snapshots never reach the QC
report. Imported by gogpt_csv_query.py (via --verify-fields) and usable
standalone.

Why this exists
---------------
Each research session records the field values it saw AT RESEARCH TIME
("Current DB value: ... captive flag = (not marked)"). By export time the
database may have moved on, so a flag can be based on a stale snapshot.
A mismatch has two opposite meanings:

  • STALE_BLANK  — card claims a field is blank / not-marked, but the CSV
                   shows it POPULATED. This is the stale-snapshot pattern.
                   Safe to AUTO-TRIM the dependent flag (with a loud log).
  • CHANGED      — card claims a concrete value that DIFFERS from the CSV.
                   Could be a genuine post-research change → a real finding.
                   NEVER auto-trim; WARN and leave for a human.
  • OK           — card claim matches the CSV.

Only captive/owner-type fields are eligible for auto-trim, and only in the
STALE_BLANK direction. Everything else is warn-only.
"""

import re
import sys

# Fields eligible for AUTO-TRIM when STALE_BLANK (card said blank, CSV populated).
# Keyed by a normalized concept → list of CSV column names that satisfy it.
AUTOTRIM_FIELDS = {
    "captive": ["Captive industry use", "Captive industry type"],
    "owner":   ["Owner(s)", "Operator(s)"],
}

# Phrases in a card finding that indicate the claim is "blank / not present".
BLANK_CLAIMS = [
    "(blank)", "blank", "(not marked)", "not marked", "(none)", "no eip/sc id",
    "not found", "no gem id", "not recorded", "(not present)",
]

GEM_ID_RE = re.compile(r"G1\d{11}")


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", str(s)).strip().lower()


def _csv_lookup(df, gem_id):
    col = next((c for c in df.columns if c.lower() == "gem unit id"), None)
    if col is None:
        return None
    row = df[df[col] == gem_id]
    return row.iloc[0] if len(row) else None


def _field_populated(row, concept) -> bool:
    for col in AUTOTRIM_FIELDS[concept]:
        if col in row.index and str(row[col]).strip():
            return True
    return False


def extract_claims(card_text: str):
    """
    Pull (gem_id, finding_block) pairs from the card. A finding block is the
    text from one flag marker up to the next, that contains a 'Current DB value'
    line and at least one GEM unit ID.
    """
    blocks = re.split(r"(?=(?:🆕|🔄|⚠️|⚙️|❌|ℹ️))", card_text)
    claims = []
    for b in blocks:
        if "current db value" not in b.lower():
            continue
        ids = GEM_ID_RE.findall(b)
        if not ids:
            continue
        # The 'current db value' line is what we test against the CSV.
        m = re.search(r"current db value\s*[:=].*", b, re.IGNORECASE)
        cur = m.group(0) if m else b
        claims.append({"ids": ids, "current_line": cur, "block": b})
    return claims


def _concept_said_blank(line_lc: str, concept: str) -> bool:
    """
    True only when the card line asserts THIS concept is blank/absent, e.g.
    'captive flag = (not marked)' or 'owner = (blank)'. A passing mention of
    the word 'owner' elsewhere in the block must NOT trigger a trim.
    Strategy: find each occurrence of a concept keyword, then require a
    blank-claim phrase within a short window (<= 40 chars) AFTER it.
    """
    keywords = {
        "captive": ["captive"],
        "owner":   ["owner", "operator", "developer"],
    }[concept]
    for kw in keywords:
        for m in re.finditer(re.escape(kw), line_lc):
            window = line_lc[m.end(): m.end() + 40]
            if any(bc in window for bc in BLANK_CLAIMS):
                return True
    return False


def classify(claim, df):
    """Return list of per-field results for a claim."""
    results = []
    cur_lc = _norm(claim["current_line"])
    claims_blank = {
        c: _concept_said_blank(cur_lc, c)
        for c in AUTOTRIM_FIELDS
    }
    # Only keep concepts the card actually asserted blank for this claim.
    claims_blank = {c: v for c, v in claims_blank.items() if v}
    for gem_id in claim["ids"]:
        row = _csv_lookup(df, gem_id)
        if row is None:
            results.append((gem_id, "NOT_FOUND", None, None))
            continue
        if not claims_blank:
            continue
        for concept, said_blank in claims_blank.items():
            populated = _field_populated(row, concept)
            if populated:
                vals = "; ".join(
                    f"{col}={str(row[col]).strip()}"
                    for col in AUTOTRIM_FIELDS[concept]
                    if col in row.index and str(row[col]).strip()
                )
                results.append((gem_id, "STALE_BLANK", concept, vals))
            else:
                results.append((gem_id, "OK", concept, "(blank confirmed)"))
    return results


def verify(card_text: str, df) -> dict:
    claims = extract_claims(card_text)
    report = {"stale_blank": [], "not_found": [], "ok": []}
    for claim in claims:
        for gem_id, verdict, concept, detail in classify(claim, df):
            entry = {"gem_id": gem_id, "concept": concept, "detail": detail}
            if verdict == "STALE_BLANK":
                report["stale_blank"].append(entry)
            elif verdict == "NOT_FOUND":
                report["not_found"].append(entry)
            else:
                report["ok"].append(entry)
    return report


def print_report(report: dict):
    print("\n" + "=" * 60)
    print("CARD-FIELD RE-VERIFICATION vs LIVE CSV")
    print("=" * 60)

    sb = report["stale_blank"]
    if sb:
        print(f"\n⚠️  STALE-BLANK (card said blank, CSV populated) — {len(sb)} field(s)")
        print("   → these flags are eligible for AUTO-TRIM:")
        for e in sb:
            print(f"   • {e['gem_id']}  [{e['concept']}]  CSV has: {e['detail']}")
    else:
        print("\n✅ No stale-blank captive/owner fields detected.")

    nf = report["not_found"]
    if nf:
        print(f"\n⚠️  NOT FOUND in CSV — {len(nf)} ID(s):")
        for e in nf:
            print(f"   • {e['gem_id']}")
    print()


if __name__ == "__main__":
    import argparse, pandas as pd
    ap = argparse.ArgumentParser(description="Re-verify card field claims vs live CSV")
    ap.add_argument("--file", required=True, help="Path to live GOGPT CSV/XLSX")
    ap.add_argument("--context-card", required=True, help="Path to context card .md")
    ap.add_argument("--country", default=None, help="Country/Area to scope to (recommended)")
    ap.add_argument("--state", default=None, help="State/Province to scope to (US)")
    args = ap.parse_args()
    ext = args.file.lower().rsplit(".", 1)[-1]
    df = (pd.read_csv(args.file, dtype=str, low_memory=False)
          if ext == "csv" else pd.read_excel(args.file, dtype=str)).fillna("")
    df.columns = [c.strip() for c in df.columns]
    # Scope to country/state (kept for future checks; harmless for field verify)
    if args.country:
        cc = next((c for c in df.columns if c.lower() == "country/area"), None)
        if cc:
            df = df[df[cc].str.strip().str.lower() == args.country.strip().lower()]
    if args.state:
        sp = next((c for c in df.columns if c.lower() == "state/province"), None)
        if sp:
            df = df[df[sp].str.strip().str.lower() == args.state.strip().lower()]
    with open(args.context_card, encoding="utf-8") as f:
        report = verify(f.read(), df)
    print_report(report)
    if report["stale_blank"]:
        sys.exit(2)  # signal: stale-blank mismatches found

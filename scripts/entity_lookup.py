"""
Look up entities in the GEM entity system to avoid creating duplicates.

Per Update SOP §8: the GEM entity system is shared across all trackers.
Creating a duplicate entity is real cleanup work for the Ownership Team.
Always run this before staging a new entity.

Two lookup modes:
  - Local: scan the current GOGPT export for the entity in existing rows
           (catches entities that already appear as Owner/Operator/Parent
           on some existing plant)
  - --pg:  query `entity_history` in GEM's read-only Postgres through the
           sibling gem-db-ops engine (catches entities that exist in the
           entity system but aren't linked to any plant in our local data).
           This is the authoritative check, the same one the sibling
           lng-terminals repo uses. The old `--remote` web-endpoint check was
           removed 2026-10-08: it put live session cookies on the curl
           command line and false-negatived intermittently.

WHY --country DOES NOT FILTER MATCHES (lesson from a real duplicate in the
sibling LNG Terminals tracker, 2026-06-24): GEM entities are SHARED across all
trackers and across countries — the developer of a new plant in one country
very often already appears on a project in another. In the LNG tracker,
`entity_lookup.py "LNG Alliance" --country Singapore` once returned not_found
because LNG Alliance only appeared on an India terminal, and the entity got
wrongly staged as new — a duplicate. So `--country` NEVER hides a match: the
local scan ALWAYS walks every row, reports the entity as `found` if it exists
ANYWHERE, and uses --country only to ANNOTATE which matches are in-country vs.
elsewhere (with a loud cross_country_warning when the only matches are elsewhere).
Before staging any new entity, run this BARE (no --country) and with --pg.

Usage:
    python entity_lookup.py "TotalEnergies"                 # the check to trust
    python entity_lookup.py "TotalEnergies" --pg            # also query the entity system (authoritative)
    python entity_lookup.py "TotalEnergies" --country "France"  # annotate only, never filters
"""
import argparse
import csv
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from normalize import normalize_entity, normalize_country
from colmap import load_colmap as _load_colmap
from paths import gem_export_csv, db_ops_repo




DEFAULT_CSV = str(gem_export_csv())

def lookup_local(name, country=None, csv_path=DEFAULT_CSV):
    """Search the GOGPT CSV for the entity across Owner(s)/Operator(s)/Parent(s) fields.

    ALWAYS scans every row regardless of `country`. The entity is reported as
    `found` if it exists ANYWHERE in the export; `country` only annotates which
    matches are in that country vs. elsewhere. This is deliberate: a `--country`
    filter that skipped other-country rows once produced a false `not_found` and a
    duplicate entity (see module docstring). `--country` must never gate a match.

    Returns dict with:
      - canonical_name: normalize_entity(name)
      - distinct_unit_ids: deduplicated GEM unit IDs where this entity appears
        (across ALL countries)
      - matched_countries: normalized countries where the entity appears
      - in_filter_country / other_country_matches / cross_country_warning:
        country-annotation fields, populated only when `country` is given
      - parent_entity_ids_seen: if entity appears as Owner with a Parent Entity ID, those IDs
    """
    canonical = normalize_entity(name)
    country_norm = normalize_country(country) if country else None

    colmap = _load_colmap(csv_path)
    fields_to_search = ["owner", "operator", "parent"]
    field_indices = {f: colmap.get(f) for f in fields_to_search if colmap.get(f) is not None}

    ci_uid = colmap["gem_unit_id"]
    ci_country = colmap["country"]
    ci_parent_id = colmap.get("parent_entity_id")

    field_match_counts = Counter()
    unit_matches = set()
    raw_variants = Counter()
    parent_entity_ids = set()
    matched_countries = set()           # normalized countries where the entity appears
    in_filter_uids = set()              # matches inside the --country filter
    other_country_uids = set()          # matches in any OTHER country
    other_countries = set()

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) < colmap["_total_columns"]:
                continue
            # NB: NO country-based `continue` here — every row is always scanned.
            row_country = row[ci_country]
            row_country_norm = normalize_country(row_country)
            row_uid = row[ci_uid]

            for field, idx in field_indices.items():
                val = row[idx]
                if not val:
                    continue
                # JV owner/parent strings separate entities with ";" (the
                # export convention: "MP Energy [55.0%]; Africa50 SA [30.0%]");
                # split on both ";" and "," and strip "[…%]" share brackets.
                for part in re.split(r"[;,]", val):
                    part = re.sub(r"\[[^\]]*\]", "", part).strip()
                    if "%" in part:
                        part = part.rsplit("(", 1)[0].rsplit(" ", 1)[0].strip()
                    if normalize_entity(part) == canonical:
                        field_match_counts[field] += 1
                        raw_variants[part] += 1
                        unit_matches.add(row_uid)
                        if row_country_norm:
                            matched_countries.add(row_country_norm)
                        # Country annotation (filter never hides — only labels).
                        if country_norm is not None:
                            if row_country_norm == country_norm:
                                in_filter_uids.add(row_uid)
                            else:
                                other_country_uids.add(row_uid)
                                if row_country:
                                    other_countries.add(row_country.strip())
                        # If this is the Owner field and there's a Parent Entity ID, capture it
                        if field == "owner" and ci_parent_id is not None:
                            pid = row[ci_parent_id].strip()
                            if pid:
                                parent_entity_ids.add(pid)

    found = bool(field_match_counts)
    out = {
        "query": name,
        "canonical_name": canonical,
        "country_filter": country,
        "country_filter_norm": country_norm,
        "field_match_counts": dict(field_match_counts),
        "raw_variants_seen": dict(raw_variants),
        "distinct_unit_count": len(unit_matches),
        "distinct_unit_ids": sorted(unit_matches),
        "matched_countries": sorted(matched_countries),
        "parent_entity_ids_seen": sorted(parent_entity_ids),
        "result": "found" if found else "not_found_in_local_data",
    }
    if country_norm is not None:
        out["in_filter_country"] = bool(in_filter_uids)
        out["other_country_matches"] = {
            "unit_ids": sorted(other_country_uids),
            "countries": sorted(other_countries),
        }
        # The exact trap that produced a duplicate: found, but ONLY in other countries.
        if found and not in_filter_uids:
            out["cross_country_warning"] = (
                f"Entity FOUND, but only on plants OUTSIDE --country {country!r} "
                f"(in {sorted(other_countries)}). This is an EXISTING GEM entity — "
                f"reuse its ID, do NOT stage as new. The --country filter would have "
                f"hidden this; it never does."
            )
    return out


def lookup_pg(name):
    """Authoritative entity check against `entity_history` in the read-only Postgres.

    Matches on the latest revision of each entity (max(id) per entity_id) and
    looks for `name` as a case-insensitive substring anywhere in the entityJSON,
    so an abbreviation-only or former-name hit still surfaces. Returns every hit
    with its entity_id. A match ANYWHERE means reuse, never create.

    Entities are frequently RENAMED, so a no-match on the current name is not
    proof of absence: try the former name, the abbreviation, and the parent's
    name too before staging as new. A skip (no DB URL, no engine) is NOT a
    not-found; do not stage a new entity on a skip.
    """
    if not os.environ.get("GEM_READONLY_DB_URL", ""):
        return {"result": "skipped_no_db_url",
                "_warning": "Set GEM_READONLY_DB_URL for the Postgres entity check"}
    # The engine comes from ../gem-db-ops (the single read path), never a bare
    # psycopg2.connect. A missing repo or dependency is a SKIP, never a not-found.
    try:
        sys.path.insert(0, str(db_ops_repo()))
        from gem_query import get_database_url, build_engine, DEFAULT_STATEMENT_TIMEOUT_MS
        from sqlalchemy import text
        engine = build_engine(get_database_url(), DEFAULT_STATEMENT_TIMEOUT_MS)
    except (ImportError, SystemExit) as e:
        return {"result": "skipped_no_db_engine", "_warning": str(e)}
    try:
        with engine.connect() as conn:
            rows = conn.execute(
                text("""
                select eh.entity_id, eh."entityJSON"
                from entity_history eh
                join (select entity_id, max(id) as mx
                      from entity_history group by entity_id) m on m.mx = eh.id
                where eh."entityJSON"::text ilike :pattern
                """),
                {"pattern": f"%{name}%"},
            ).fetchall()
    except Exception as e:  # unreachable DB is an escalation, not a not-found
        return {"result": "pg_lookup_failed", "_warning": str(e)}

    matches = []
    for eid, blob in rows:
        d = blob if isinstance(blob, dict) else json.loads(blob)
        nm = str(d.get("name") or "")
        matches.append({
            "entity_id": eid,
            "name": nm,
            "abbreviation": d.get("abbreviation"),
            # GEM soft-deletes by renaming; such a hit is NOT a reusable entity
            "to_be_deleted": "TO BE DELETED" in nm.upper(),
        })
    live = [m for m in matches if not m["to_be_deleted"]]
    q = name.strip().lower()
    for m in matches:
        m["name_or_abbr_match"] = (q in str(m["name"]).lower()
                                   or q in str(m["abbreviation"] or "").lower())
    named_live = [m for m in live if m["name_or_abbr_match"]]
    return {
        "result": ("found_pg" if named_live else
                   "found_pg_incidental_only" if live else
                   "only_to_be_deleted" if matches else "no_pg_match"),
        "query": name,
        "match_count": len(matches),
        "name_or_abbr_match_count": len(named_live),
        "matches": sorted(matches, key=lambda m: (m["to_be_deleted"],
                                                  not m["name_or_abbr_match"], m["name"])),
        "_note": ("Reuse an existing entity_id above; do NOT create a new entity."
                  if named_live else
                  "Matches came from incidental substrings in the entity blob, NOT from any "
                  "entity name or abbreviation. Read them before concluding either way."
                  if live else
                  "No live entity matched. Entities get RENAMED: before staging as new, "
                  "re-run on the abbreviation, any former name, and the parent company."),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("name", help="Entity name to look up (e.g. 'TotalEnergies')")
    p.add_argument("--country",
                   help="ANNOTATE matches by in-/out-of-country only; NEVER filters them "
                        "out (entities are shared across countries). Run BARE before staging.")
    p.add_argument("--csv", default=DEFAULT_CSV, help="GOGPT export CSV path")
    p.add_argument("--pg", action="store_true",
                   help="Also query entity_history in the read-only Postgres (GEM_READONLY_DB_URL). "
                        "AUTHORITATIVE; run it before staging any new entity.")
    args = p.parse_args()

    local_result = lookup_local(args.name, country=args.country, csv_path=args.csv)
    print(json.dumps(local_result, indent=2))

    if local_result["result"] == "found":
        warn = local_result.get("cross_country_warning")
        if warn:
            print(f"\n  ⚠ {warn}", file=sys.stderr)
        else:
            print(f"\n  → Entity '{args.name}' (canonical: '{local_result['canonical_name']}') "
                  f"appears on {local_result['distinct_unit_count']} units "
                  f"({', '.join(local_result['matched_countries']) or 'unknown country'}). "
                  f"Reuse existing entity ID; do NOT create a new one.", file=sys.stderr)
    elif args.pg:
        print("\n  Local lookup found nothing; querying the read-only Postgres...",
              file=sys.stderr)
        pg_result = lookup_pg(args.name)
        print(json.dumps(pg_result, indent=2))
        if pg_result["result"] == "found_pg":
            print(f"\n  → Entity '{args.name}' EXISTS in the entity system "
                  f"({pg_result['match_count']} match(es)). Reuse the entity_id; "
                  f"do NOT stage it as new.", file=sys.stderr)
        elif pg_result["result"] in ("skipped_no_db_url", "skipped_no_db_engine",
                                    "pg_lookup_failed"):
            print(f"\n  ⚠ The Postgres check did not RUN ({pg_result['result']}); that is "
                  f"not a not-found. Do not stage a new entity on this basis; escalate.",
                  file=sys.stderr)
    else:
        print(f"\n  Local lookup found nothing. Before staging as new, RE-RUN WITH --pg "
              f"to query the entity system (and confirm you ran this BARE, without --country, "
              f"which would not have hidden a match but is the check to trust). Only then add "
              f"as a new entity (entity_additions sheet in batch xlsx).",
              file=sys.stderr)

    if args.country and local_result["result"] == "not_found_in_local_data":
        # Defensive nudge: a not_found under --country is exactly when the old bug bit.
        print(f"\n  NOTE: --country was set. This scan ignored it for matching (it can't hide "
              f"a match), so not_found here means not_found anywhere in the local export.",
              file=sys.stderr)


if __name__ == "__main__":
    main()

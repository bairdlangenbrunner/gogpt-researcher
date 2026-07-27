"""
Mechanical validation of GOGPT rows against the Editing Manual's rules.

Runs the checks that a machine can decide (the QC SOP covers the ones it
can't). Encoded here:
  - capacity parseable; per-unit nameplate >= 50 MW, or >= 20 MW for EU/UK
    countries (below-threshold is a WARNING — it is a scope question, not
    automatically an error; captive units in particular need a human call)
  - status in the closed vocabulary
  - start year must be blank for shelved / cancelled units
  - retired year must be blank for mothballed units
  - cancelled units should carry a cancellation year (2020-forward rule)
  - retired units should carry a retired year (2020-forward rule)
  - technology in the closed vocabulary (CC/GT/AGT/ST/IC/ICCC/ISCC/AFC)
  - fuel tokens: coal/bioenergy hints are scope ERRORS in a GOGPT slice;
    tokens outside the known GOGPT fuel list are warnings
  - ownership share percentages: each named share >= 5% (except an explicit
    "other"), and shares that look complete should sum to ~100%

Two input modes:
  - CSV slice:   python qc_checks.py --csv gem_export_gogpt_scoped.csv [--country Nigeria]
  - staged JSON: python qc_checks.py --staged ../batches/<scope>/staging/staged_updates.json
    Staged records are checked field-by-field (see docs/reference/
    staged_json_schema.md): each record's "fields" dict maps EXACT CSV header
    strings to proposed values; only the fields present are checked, except
    cross-field rules (status vs years), which run when both sides are present.

Exit code 1 if any ERROR-severity finding; warnings alone exit 0.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from paths import gogpt_scoped_csv
from pull_gem_db import EXPECTED_COLUMNS, derive_column_map
from schema_constants import (
    CAPACITY_THRESHOLD_EU_UK_MW,
    CAPACITY_THRESHOLD_MW,
    EU_UK_COUNTRIES,
    GOGPT_FUELS,
    GOGPT_FUEL_CATEGORIES,
    NON_GOGPT_FUEL_CATEGORIES,
    NON_GOGPT_FUEL_HINTS,
    STATUSES,
    STATUSES_NO_START_YEAR,
    TECHNOLOGIES,
    TECHNOLOGY_LONG_FORMS,
)

PCT_RE = re.compile(r"\((\d+(?:\.\d+)?)\s*%\)")
FUEL_SPLIT_RE = re.compile(r"[,;/&]| and ")
GOGPT_FUELS_LOWER = {f.lower() for f in GOGPT_FUELS}


class Finding:
    def __init__(self, severity, check, ident, message):
        self.severity, self.check, self.ident, self.message = \
            severity, check, ident, message

    def __str__(self):
        return f"[{self.severity}] {self.ident}: {self.check} — {self.message}"


def _num(value):
    try:
        return float(str(value).replace(",", "").strip())
    except (ValueError, TypeError):
        return None


def check_record(fields, ident, findings):
    """fields: dict of short column name -> value (missing keys = not staged /
    not checked). Appends Finding objects."""
    get = lambda k: (fields.get(k) or "").strip()

    status = get("status").lower()
    country = get("country")

    if "status" in fields and status and status not in STATUSES:
        findings.append(Finding("ERROR", "status-vocab", ident,
                                f"status {get('status')!r} not in {sorted(STATUSES)}"))

    if "capacity_mw" in fields and get("capacity_mw"):
        cap = _num(get("capacity_mw"))
        if cap is None:
            findings.append(Finding("ERROR", "capacity-parse", ident,
                                    f"capacity {get('capacity_mw')!r} not numeric"))
        else:
            threshold = (CAPACITY_THRESHOLD_EU_UK_MW
                         if country in EU_UK_COUNTRIES else CAPACITY_THRESHOLD_MW)
            if cap < threshold:
                findings.append(Finding(
                    "WARN", "capacity-threshold", ident,
                    f"{cap:g} MW below the {threshold} MW inclusion bar for "
                    f"{country or 'unknown country'} — scope call needed "
                    "(unit sets aggregate; captive units get a human review)"))

    if status in STATUSES_NO_START_YEAR and get("start_year"):
        findings.append(Finding("ERROR", "start-year-forbidden", ident,
                                f"start year {get('start_year')!r} present on a "
                                f"{status} unit (must be blank)"))

    if status == "mothballed" and get("retired_year"):
        findings.append(Finding("ERROR", "retired-year-on-mothballed", ident,
                                f"retired year {get('retired_year')!r} present on a "
                                "mothballed unit (must be blank)"))

    if status == "cancelled" and "cancellation_year" in fields \
            and not get("cancellation_year"):
        findings.append(Finding("WARN", "cancellation-year-missing", ident,
                                "cancelled unit with no cancellation year "
                                "(expected for 2020-forward cancellations)"))

    if status == "retired" and "retired_year" in fields and not get("retired_year"):
        findings.append(Finding("WARN", "retired-year-missing", ident,
                                "retired unit with no retired year "
                                "(expected for 2020-forward retirements)"))

    if "technology" in fields and get("technology"):
        tech = get("technology")
        if tech.upper() not in TECHNOLOGIES \
                and tech.lower() not in TECHNOLOGY_LONG_FORMS:
            findings.append(Finding("ERROR", "technology-vocab", ident,
                                    f"technology {tech!r} not in "
                                    f"{sorted(TECHNOLOGIES)} or the long forms"))

    if "fuel" in fields and get("fuel"):
        # Export tokens are "category: detail"; staged records may use the
        # manual's bare details. Category decides scope; a mixed cell with at
        # least one GOGPT fuel is legitimate co-firing, not a scope leak.
        in_scope, non_scope, unknown = 0, [], []
        for token in filter(None, (t.strip().lower()
                                   for t in FUEL_SPLIT_RE.split(get("fuel")))):
            cat, sep, detail = token.partition(":")
            cat, detail = cat.strip(), detail.strip()
            detail_base = re.sub(r"\s*\(.*\)$", "", detail or token)
            if sep and cat in GOGPT_FUEL_CATEGORIES:
                in_scope += 1
            elif sep and cat in NON_GOGPT_FUEL_CATEGORIES:
                non_scope.append(token)
            elif detail_base in GOGPT_FUELS_LOWER:
                in_scope += 1
            elif any(hint in token for hint in NON_GOGPT_FUEL_HINTS):
                non_scope.append(token)
            else:
                unknown.append(token)
        if non_scope and not in_scope:
            findings.append(Finding("ERROR", "fuel-scope", ident,
                                    f"fuel {get('fuel')!r} is entirely non-GOGPT "
                                    "(coal/bioenergy scope leak?)"))
        for token in unknown:
            findings.append(Finding("WARN", "fuel-vocab", ident,
                                    f"fuel token {token!r} not in the known "
                                    "GOGPT fuel list — verify spelling"))

    if "owner" in fields and get("owner"):
        shares = [float(m) for m in PCT_RE.findall(get("owner"))]
        owner_lower = get("owner").lower()
        for s in shares:
            if s < 5 and "other" not in owner_lower:
                findings.append(Finding("WARN", "ownership-share", ident,
                                        f"ownership share {s:g}% is below the 5% "
                                        "floor (fold into 'other'?)"))
        if len(shares) > 1 and not 98 <= sum(shares) <= 102 \
                and "other" not in owner_lower:
            findings.append(Finding("WARN", "ownership-sum", ident,
                                    f"ownership shares sum to {sum(shares):g}% "
                                    "with no 'other' bucket"))


def run_csv(path, country_filter):
    col_map = derive_column_map(path)
    findings = []
    checked = 0
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            fields = {short: row[i] for short, i in col_map.items()
                      if not short.startswith("_") and i is not None}
            if country_filter and \
                    fields.get("country", "").strip().lower() != country_filter:
                continue
            ident = (fields.get("gem_unit_id") or
                     f"{fields.get('plant_name')} / {fields.get('unit_name')}")
            check_record(fields, ident, findings)
            checked += 1
    return checked, findings


def run_staged(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    records = data["records"] if isinstance(data, dict) and "records" in data else data
    header_to_short = {v: k for k, v in EXPECTED_COLUMNS.items()}
    findings = []
    for i, rec in enumerate(records):
        raw = rec.get("fields", {})
        fields = {}
        for header, value in raw.items():
            short = header_to_short.get(header)
            if short is None:
                findings.append(Finding("ERROR", "unknown-column",
                                        rec.get("gem_unit_id", f"record {i}"),
                                        f"staged field {header!r} is not a known "
                                        "CSV header"))
            else:
                fields[short] = value
        ident = (rec.get("gem_unit_id") or rec.get("plant_name")
                 or f"record {i}")
        check_record(fields, ident, findings)
    return len(records), findings


def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group()
    g.add_argument("--csv", help="check a tracker CSV slice")
    g.add_argument("--staged", help="check a staged_*.json records file")
    p.add_argument("--country", help="CSV mode: restrict to one country")
    args = p.parse_args()

    if args.staged:
        checked, findings = run_staged(args.staged)
        what = f"{checked} staged records"
    else:
        path = args.csv or str(gogpt_scoped_csv())
        if not Path(path).exists():
            sys.exit(f"ERROR: {path} not found — run scope_filter.py first")
        checked, findings = run_csv(
            path, args.country.strip().lower() if args.country else None)
        what = f"{checked} CSV rows"

    for f in findings:
        print(f)
    errors = sum(1 for f in findings if f.severity == "ERROR")
    warns = len(findings) - errors
    print(f"\nqc_checks: {what} checked — {errors} errors, {warns} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()

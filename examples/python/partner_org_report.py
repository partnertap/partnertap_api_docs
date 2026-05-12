#!/usr/bin/env python3

"""
PartnerTap API utilities — export matched accounts and discover columns.

Usage:
    export PARTNERTAP_API_KEY=...

    # Export matched accounts to CSV (filtered to country match)
    python partner_org_report.py export "AbbVie Inc." [-o output.csv]

    # Use a custom base URL (defaults to https://reports.partnertap.com)
    python partner_org_report.py --base-url https://test-reports.partnertap.com export "AbbVie Inc."

    # List available columns
    python partner_org_report.py columns "AbbVie Inc."
    python partner_org_report.py columns "AbbVie Inc." --type standard
    python partner_org_report.py columns "AbbVie Inc." --type custom
    python partner_org_report.py columns "AbbVie Inc." --type partner
    python partner_org_report.py columns "AbbVie Inc." --type all-separate
"""

import argparse
import csv
import logging
import os
import sys
from typing import Any, Optional

import requests
import country_converter as coco

DEFAULT_BASE_URL = "https://reports.partnertap.com"
RECORDS_URL = f"{DEFAULT_BASE_URL}/v1/channelecosystem/records"
COLUMNS_URL = f"{DEFAULT_BASE_URL}/v1/channelecosystem/columns"
PAGE_SIZE = 2000  # max allowed
# customize the columns you would like in your CSV
EXPORT_STANDARD_COLUMNS = ["accountName", "crmAccountId"]
EXPORT_PARTNER_COLUMNS = ["partneraccountname", "partnercrmaccountid"]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("partnertap")

# Suppress coco's stderr chatter for unmatched names
_cc = coco.CountryConverter()


def normalize_country(value: Optional[str]) -> Optional[str]:
    """Normalize a country string to ISO2. Returns None if blank or unmatched."""
    if not value or not value.strip():
        return None
    iso2 = _cc.convert(names=value.strip(), to="ISO2", not_found=None)
    return iso2 if iso2 else None


def post_records(api_key: str, body: dict, page: int, size: int = PAGE_SIZE) -> dict:
    headers = {"Content-Type": "application/json", "api-key": api_key}
    params = {"page": page, "size": size}
    resp = requests.post(RECORDS_URL, headers=headers, params=params, json=body, timeout=120)
    if resp.status_code == 429:
        raise RuntimeError("Rate limited (429). Reduce request rate and retry.")
    resp.raise_for_status()
    return resp.json()


def iter_pages(api_key: str, body: dict):
    page = 0
    while True:
        data = post_records(api_key, body, page=page)
        for record in data.get("content", []):
            yield record
        if data.get("last", True):
            break
        page += 1


def find_partner_id(api_key: str, partner_name: str) -> str:
    body = {
        "search": "",
        "filters": {"partnerName": partner_name},
        "mapByLocations": False,
        "channelReportType": "PARTNER_ORG_CONNECTED_PARTNER_ORGS",
        "matchingType": "MUTUAL",
    }
    matches = []
    target = partner_name.strip().lower()
    for rec in iter_pages(api_key, body):
        name = (rec.get("partnerName") or "").strip()
        if name.lower() == target:
            matches.append(rec)

    if not matches:
        raise SystemExit(f"No partner org found with partnerName == '{partner_name}'")
    if len(matches) > 1:
        ids = [m.get("companyPartnerPublicId") for m in matches]
        raise SystemExit(f"Multiple partner orgs matched '{partner_name}': {ids}")
    return matches[0]["companyPartnerPublicId"]


def fetch_columns(api_key: str, body: dict) -> list[dict]:
    """Fetch available columns from the /columns endpoint."""
    headers = {"Content-Type": "application/json", "api-key": api_key}
    resp = requests.post(COLUMNS_URL, headers=headers, json=body, timeout=120)
    if resp.status_code == 429:
        raise RuntimeError("Rate limited (429). Reduce request rate and retry.")
    resp.raise_for_status()
    return resp.json()


def get_columns_for_partner(api_key: str, partner_id: str) -> list[dict]:
    """Retrieve all available columns for a Partner Org Matched Accounts report."""
    body = {
        "search": "",
        "filters": {},
        "mapByLocations": False,
        "channelReportType": "PARTNER_ORG_MATCHED_ACCOUNTS",
        "matchingType": "MUTUAL",
        "companyPartnerPublicId": partner_id,
    }
    return fetch_columns(api_key, body)


def filter_columns(columns: list[dict], column_type: str) -> list[dict]:
    """Filter columns by type: standard, custom, partner, or all."""
    if column_type == "all":
        return columns
    if column_type == "standard":
        return [c for c in columns
                if c.get("columnClassification") == "STANDARD" and not c.get("isPartnerData")]
    if column_type == "custom":
        return [c for c in columns
                if c.get("columnClassification") in ("CUSTOM_CRM_FIELD", "CUSTOM_CRM_OBJECT")
                and not c.get("isPartnerData")]
    if column_type == "partner":
        return [c for c in columns if c.get("isPartnerData")]
    return columns


def print_columns(columns: list[dict], column_type: str) -> None:
    """Print columns in a formatted table."""
    label = {
        "all": "All",
        "standard": "Standard",
        "custom": "My Custom",
        "partner": "Partner Shared",
    }.get(column_type, column_type)

    filtered = filter_columns(columns, column_type)

    if not filtered:
        print(f"\nNo {label.lower()} columns found.")
        return

    def _s(val: Any) -> str:
        return str(val) if val is not None else ""

    key_w = max(len(_s(c.get("key"))) for c in filtered)
    title_w = max(len(_s(c.get("title"))) for c in filtered)
    type_w = max(len(_s(c.get("type"))) for c in filtered)
    class_w = max(len(_s(c.get("columnClassification"))) for c in filtered)
    key_w = max(key_w, 3)
    title_w = max(title_w, 5)
    type_w = max(type_w, 4)
    class_w = max(class_w, 14)

    header = f"  {'Key':<{key_w}}  {'Title':<{title_w}}  {'Type':<{type_w}}  {'Classification':<{class_w}}  Partner?"
    print(f"\n{label} Columns ({len(filtered)}):")
    print(header)
    print("  " + "-" * (len(header) - 2))

    for c in sorted(filtered, key=lambda x: x.get("columnIndex", 0)):
        partner = "Yes" if c.get("isPartnerData") else "No"
        print(f"  {_s(c.get('key')):<{key_w}}  {_s(c.get('title')):<{title_w}}  "
              f"{_s(c.get('type')):<{type_w}}  {_s(c.get('columnClassification')):<{class_w}}  {partner}")


def get_field(record: dict, key: str) -> Any:
    """Look up a field at top level, then inside partnerFields."""
    if key in record and record[key] not in (None, ""):
        return record[key]
    pf = record.get("partnerFields") or {}
    return pf.get(key)


def build_row(record: dict) -> dict:
    """Build a CSV row by reading standard columns from the record and
    partner columns from the nested ``partnerFields`` object."""
    row: dict[str, Any] = {}
    for col in EXPORT_STANDARD_COLUMNS:
        row[col] = record.get(col)
    partner_fields = record.get("partnerFields") or {}
    for col in EXPORT_PARTNER_COLUMNS:
        row[col] = partner_fields.get(col)
    return row


def export_matched_accounts(api_key: str, partner_id: str, output_path: str) -> tuple[int, int]:
    body = {
        "search": "",
        "filters": {},
        "mapByLocations": False,
        "channelReportType": "PARTNER_ORG_MATCHED_ACCOUNTS",
        "matchingType": "MUTUAL",
        "companyPartnerPublicId": partner_id,
    }

    all_columns = EXPORT_STANDARD_COLUMNS + EXPORT_PARTNER_COLUMNS
    total = 0
    written = 0

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_columns)
        writer.writeheader()

        for rec in iter_pages(api_key, body):
            total += 1
            country = normalize_country(get_field(rec, "country"))
            partner_country = normalize_country(get_field(rec, "partnerCountry"))

            if not country or not partner_country or country != partner_country:
                continue

            writer.writerow(build_row(rec))
            written += 1

            if total % 5000 == 0:
                log.info("Processed %d rows (kept %d so far)...", total, written)

    return total, written


def _require_api_key() -> str:
    api_key = os.environ.get("PARTNERTAP_API_KEY")
    if not api_key:
        print("ERROR: set PARTNERTAP_API_KEY environment variable", file=sys.stderr)
        sys.exit(2)
    return api_key


def _resolve_partner(api_key: str, partner_name: str) -> str:
    log.info("Looking up partner: %s", partner_name)
    partner_id = find_partner_id(api_key, partner_name)
    log.info("Found companyPartnerPublicId: %s", partner_id)
    return partner_id


def cmd_export(args: argparse.Namespace) -> int:
    api_key = _require_api_key()
    safe_name = args.partner_name.replace(' ', '_').replace('/', '_').rstrip('.')
    output_path = args.output or f"matched_{safe_name}.csv"

    partner_id = _resolve_partner(api_key, args.partner_name)

    log.info("Fetching matched accounts...")
    total, written = export_matched_accounts(api_key, partner_id, output_path)
    log.info("Done. Scanned %d accounts, wrote %d rows (country match) to %s",
             total, written, output_path)
    return 0


def cmd_columns(args: argparse.Namespace) -> int:
    api_key = _require_api_key()
    partner_id = _resolve_partner(api_key, args.partner_name)

    log.info("Fetching available columns...")
    columns = get_columns_for_partner(api_key, partner_id)
    log.info("Retrieved %d total columns.", len(columns))

    if args.type == "all-separate":
        for ct in ("standard", "custom", "partner"):
            print_columns(columns, ct)
    else:
        print_columns(columns, args.type)

    return 0


def _apply_base_url(base_url: Optional[str]) -> None:
    """Override the module-level API URLs if a custom base URL was provided."""
    if base_url:
        global RECORDS_URL, COLUMNS_URL
        base = base_url.rstrip("/")
        RECORDS_URL = f"{base}/v1/channelecosystem/records"
        COLUMNS_URL = f"{base}/v1/channelecosystem/columns"


def main() -> int:
    parser = argparse.ArgumentParser(description="PartnerTap API utilities.")
    parser.add_argument(
        "--base-url",
        default=None,
        help=f"Base URL for the PartnerTap API (default: {DEFAULT_BASE_URL})",
    )
    sub = parser.add_subparsers(dest="command")

    # export subcommand
    p_export = sub.add_parser("export", help="Export matched accounts to CSV")
    p_export.add_argument("partner_name", help="Exact partner org name (partnerName field)")
    p_export.add_argument("-o", "--output", default=None, help="Output CSV path (default: matched_<partner>.csv)")

    # columns subcommand
    p_cols = sub.add_parser("columns", help="List available columns for a partner org report")
    p_cols.add_argument("partner_name", help="Exact partner org name (partnerName field)")
    p_cols.add_argument(
        "-t", "--type",
        choices=["standard", "custom", "partner", "all", "all-separate"],
        default="all",
        help="Column category to list (default: all). "
             "Use 'all-separate' to show each category in its own section.",
    )

    args = parser.parse_args()
    _apply_base_url(args.base_url)

    if args.command == "export":
        return cmd_export(args)
    if args.command == "columns":
        return cmd_columns(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
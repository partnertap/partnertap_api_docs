# PartnerTap API Python Examples

File: `partner_org_report.py`

Utilities for the PartnerTap Analytics API — export matched accounts to CSV and discover available report columns.

### Prerequisites
Generate an API key in PartnerTap: **Admin Center > Data > API Keys**.
See [API Guide](https://partnertap.atlassian.net/wiki/spaces/Engineering/pages/758153230).

### 1. Install dependencies
```
pip3 install -r requirements.txt
```

### 2. Set your API key
```
export PARTNERTAP_API_KEY="<your api key>"
```

---

## Export Matched Accounts

Exports the list of accounts you share with a given partner org to CSV, filtered to rows where account country matches partner country (normalized via `country_converter`).

```
python partner_org_report.py export "AbbVie Inc."
```

Optional output path:
```
python partner_org_report.py export "AbbVie Inc." -o abbvie.csv
```

---

## List Available Columns

Retrieve and display the columns available on a Partner Org Matched Accounts report. Columns are grouped into three categories:

- **Standard** — Built-in fields (e.g., Account Name, City, Country).
- **Custom** — Fields imported from your CRM (`CUSTOM_CRM_FIELD` / `CUSTOM_CRM_OBJECT`).
- **Partner Shared** — Fields shared by the partner organization.

### Show all columns
```
python partner_org_report.py columns "AbbVie Inc."
```

### Show only standard columns
```
python partner_org_report.py columns "AbbVie Inc." --type standard
```

### Show only your custom CRM columns
```
python partner_org_report.py columns "AbbVie Inc." --type custom
```

### Show only partner shared columns
```
python partner_org_report.py columns "AbbVie Inc." --type partner
```

### Show each category in its own section
```
python partner_org_report.py columns "AbbVie Inc." --type all-separate
```
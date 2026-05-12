---
title: Python Examples
description: Python utilities for the PartnerTap Analytics API — export matched accounts to CSV and discover available report columns.
---

File: `partner_org_report.py`

Utilities for the PartnerTap Analytics API — export matched accounts to CSV and discover available report columns.

### Prerequisites
Generate an API key in PartnerTap: **Admin Center > Data > API Keys**.

### 1. Install dependencies
```
pip3 install -r requirements.txt
```

### 2. Set your API key
```
export PARTNERTAP_API_KEY="<your api key>"
```

### 3. (Optional) Custom base URL

By default the script targets the production API (`https://reports.partnertap.com`). To point at a different environment, pass `--base-url` before the subcommand:

```
python partner_org_report.py --base-url https://test-reports.partnertap.com export "Example Pharma Inc."
```

---

## Export Matched Accounts

Exports the list of accounts you share with a given partner org to CSV, filtered to rows where account country matches partner country (normalized via `country_converter`).

### Customize exported columns

Before running an export, open `partner_org_report.py` and edit the two column lists to include the columns you want in your CSV. The columns are split into two variables because the API returns them in different places in the response:

- **`EXPORT_STANDARD_COLUMNS`** — Your own account fields, read from the top level of each record.
- **`EXPORT_PARTNER_COLUMNS`** — Partner-shared fields, read from the nested `partnerFields` object in each record.

The defaults are:

```python
EXPORT_STANDARD_COLUMNS = ["accountName", "crmAccountId"]
EXPORT_PARTNER_COLUMNS = ["partnerAccountName", "partnerAccountId"]
```

Use the `columns` command (described below) to discover available column keys for your partner. Columns where the "Partner?" indicator is **Yes** belong in `EXPORT_PARTNER_COLUMNS`; all others belong in `EXPORT_STANDARD_COLUMNS`. For example:

```python
EXPORT_STANDARD_COLUMNS = ["accountName", "crmAccountId", "country"]
EXPORT_PARTNER_COLUMNS = ["partnerAccountName", "partnerAccountId", "partnerCountry"]
```

Both lists are combined in order to produce the CSV header and rows.

### Run the export

```
python partner_org_report.py export "Example Pharma Inc."
```

Optional output path:
```
python partner_org_report.py export "Example Pharma Inc." -o example-pharma.csv
```

---

## List Available Columns

Retrieve and display the columns available on a Partner Org Matched Accounts report. Columns are grouped into three categories:

- **Standard** — Built-in fields (e.g., Account Name, City, Country).
- **Custom** — Fields imported from your CRM (`CUSTOM_CRM_FIELD` / `CUSTOM_CRM_OBJECT`).
- **Partner Shared** — Fields shared by the partner organization.

### Show all columns
```
python partner_org_report.py columns "Example Pharma Inc."
```

### Show only standard columns
```
python partner_org_report.py columns "Example Pharma Inc." --type standard
```

### Show only your custom CRM columns
```
python partner_org_report.py columns "Example Pharma Inc." --type custom
```

### Show only partner shared columns
```
python partner_org_report.py columns "Example Pharma Inc." --type partner
```

### Show each category in its own section
```
python partner_org_report.py columns "Example Pharma Inc." --type all-separate
```

---

## Source Code

The full source code is available in the repository at [`examples/python/`](https://github.com/partnertap/partnertap_api_docs/tree/main/examples/python).

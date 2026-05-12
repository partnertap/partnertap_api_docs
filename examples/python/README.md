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

### 3. (Optional) Custom base URL

By default the script targets the production API (`https://reports.partnertap.com`). To point at a different environment, pass `--base-url` before the subcommand:

```
python partner_org_report.py --base-url https://test-reports.partnertap.com export "AbbVie Inc."
```

---

## Export Matched Accounts

Exports the list of accounts you share with a given partner org to CSV, filtered to rows where account country matches partner country (normalized via `country_converter`).

### Customize exported columns

Before running an export, open `partner_org_report.py` and edit the `EXPORT_COLUMNS` list to include the columns you want in your CSV. The default is:

```python
EXPORT_COLUMNS = ["accountName", "crmAccountId", "partnerAccountName", "partnerAccountId"]
```

Use the `columns` command (described below) to discover available column keys for your partner, then update `EXPORT_COLUMNS` with the keys you need. For example:

```python
EXPORT_COLUMNS = ["accountName", "crmAccountId", "country", "partnerAccountName", "partnerAccountId", "partnerCountry"]
```

Only columns listed in `EXPORT_COLUMNS` will appear in the exported CSV.

### Run the export

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
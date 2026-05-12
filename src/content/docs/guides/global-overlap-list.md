---
title: Global Overlap List API Guide
description: Guide for using the PartnerTap Report Analytics API to retrieve the Global Overlap List report, including authentication, field reference, and filtering.
---

This document is a guide for using the PartnerTap Analytics API for retrieving the Ecosystem "Global Overlap List" report.

The "Global Overlap List" report is a vertical view of your accounts that overlap with your entire partner ecosystem. This report is considered "vertical" because your partners will all be listed in one column instead of separate columns. In the event an account overlaps with more than one partner, the account will be repeated in a row for each partner.

All report endpoints follow the pattern `/v1/report-analytics/report/{reportType}/...` and support the `ReportRequest` body for filtering, searching, and column selection.

---

## 1. Authentication

All API requests require an API key passed in the `api-key` HTTP header.

### Generating an API Key

1. Log in to PartnerTap.
2. Navigate to [**Admin Center > Data > API Keys**](https://app.partnertap.com/#/channel-mapping/admin-center/section-detail?group=4&section=5).
3. Click **"Generate Key"**.
4. Copy the generated key and store it securely — it will not be shown again.

### Using the API Key

Include the key in every request via the `api-key` header:

```
api-key: <YOUR_API_KEY>
```

If the `api-key` header is not provided, the service falls back to the standard `authorization` header (JWT bearer token). The API key approach is recommended for programmatic/external integrations.

> **Rate Limiting:** Each API key is rate-limited to a maximum number of 100 requests per minute. The counter resets on a rolling 1-minute window. If the limit is exceeded, the server responds with HTTP `429 Too Many Requests`. The rate limit is tracked per API key — separate keys have independent counters.

---

## 2. Get Report Records

Returns paginated report records for a given report type.

### Request

```
POST /v1/report-analytics/report/GLOBAL_VERTICAL_ACCOUNTS/records?page=0&size=20&sort=columnName,asc
Content-Type: application/json
```

### Path Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `reportType`  | string  | Yes       | The report type enum value  |

### Query Parameters (Pagination)

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `page`     | integer  | No        | Zero-based page index (default: 0)                                                          |
| `size`     | integer  | No        | Number of records per page (default: 20, max: 2000)                                                    |
| `sort`     | string   | No        | Sorting criteria in the format `property,asc\|desc`. Multiple sort criteria are supported.  |

### Request Body (`ReportRequest`)

```
{
  "filters": {},
  "search": ""
}
```

### Response

**200 OK** - Returns a paginated response containing report records (showing only 1 record for this example).

```json
{
  "totalElements": 7792,
  "totalPages": 390,
  "sort": {
    "unsorted": true,
    "sorted": false,
    "empty": true
  },
  "first": true,
  "last": false,
  "number": 0,
  "pageable": {
    "pageNumber": 0,
    "pageSize": 20,
    "sort": {
      "unsorted": true,
      "sorted": false,
      "empty": true
    },
    "offset": 0,
    "unpaged": false,
    "paged": true
  },
  "numberOfElements": 20,
  "size": 20,
  "empty": false,
  "content": [
    {
      "account_acv": 0.00,
      "account_name": "Example Logistics",
      "account_owner_email": "jane.doe@example.com",
      "account_owner_name": "Jane Doe",
      "account_owner_title": "Sales Development Rep",
      "account_type": "Prospect",
      "annual_revenue": "",
      "average_referral_deal_size": 10000000,
      "city": "Oklahoma City",
      "closed_opp_count": 4,
      "country": "US",
      "crm_account_id": "MANUAL-f91e0f6a-c941-4e2d-a94c-deb49157ba46",
      "divisions": "West",
      "duns_number": "",
      "industry": "Professional, Scientific and Technical Services",
      "naics_code": "",
      "nces_id": "",
      "number_of_employees": 3088,
      "open_opp_count": 2,
      "open_pipeline_amount": 463190624.03,
      "partner_account_acv": 0,
      "partner_account_name": "USA Logistics",
      "partner_account_owner_email": "sample@example.com",
      "partner_account_owner_name": "John Doe",
      "partner_account_owner_phone": "N/A",
      "partner_account_owner_title": "Senior Sales Rep",
      "partner_account_type": "Prospect",
      "partner_city": "Buenos Aires",
      "partner_closed_opp": 0,
      "partner_closed_opp_won_count": 0,
      "partner_count": 4,
      "partner_country": "",
      "partner_crm_account_id": "",
      "partner_first_match_date": 1758921277,
      "partner_open_opp": 0,
      "partner_open_pipeline_amount": 0,
      "partner_org_name": "Example Pharma Inc.",
      "partner_org_partner_type": "",
      "partner_owner": "",
      "partner_owner_email": "",
      "partner_owner_phone": "",
      "partner_postal_code": "",
      "partner_state": "",
      "partner_street": "",
      "partner_website": "example-pharma.example.com",
      "partnerOrgPublicId": "c1727859-692f-499e-8c2a-b1fa50aa1a65",
      "phone_number": "",
      "prm_record_id": "",
      "recent_closed_opp_date": 1715707210,
      "recent_open_opp_date": 1722705610,
      "sic_code": "",
      "state": "Oklahoma",
      "street": "",
      "tax_id": "",
      "territory": "",
      "website": "example-logistics.example.com",
      "zip_code": "73013"
    }
  ],
  "noDataFoundMessage": null
}
```

### Example

```shell
curl -X POST \
  "https://reports-analytics.partnertap.com/v1/report-analytics/report/GLOBAL_VERTICAL_ACCOUNTS/records?page=0&size=20" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{
    "filters": {},
    "search": ""
  }'
```

---

## 3. Field Names & Types

Here are all of standard fields for the Global Overlap List report. If you have custom fields they will appear with the prefix "custom\_" in the records response.

Note: Columns prefixed with "partner\_" populate depending on your partner's share settings and available data.

| API Name | Display Name | Type | Description |
| --- | --- | --- | --- |
| account_name  | Account Name  | string  | Name of the account in your crm or upload                  |
| account_type  | Account Type  | string  | Account classification (e.g., Customer, Prospect)          |
| account_owner_name  | Account Owner Name  | name  | Full name of the account owner                          |
| account_owner_email  | Account Owner Email  | email  | Email of the account owner                              |
| account_owner_title  | Account Owner Title  | title  | Job title of the account owner                          |
| crm_account_id  | Account ID  | string  | Unique identifier of the account in the source CRM         |
| duns_number  | DUNS Number  | string  | Dun & Bradstreet DUNS identifier                           |
| street  | Street  | string  | Account street address                                     |
| city  | City  | string  | Account city                                               |
| state  | State  | string  | Account state or region                                    |
| zip_code  | Zip Code  | string  | Account postal code                                        |
| country  | Country  | string  | Account country                                            |
| industry  | Industry  | string  | Industry classification of the account                     |
| territory  | Territory  | string  | Sales territory the account is assigned to                 |
| divisions  | Divisions  | string  | Internal divisions associated with the account             |
| website  | Website  | string  | Account's website URL                                      |
| naics_code  | NAICS#  | string  | NAICS industry classification code                         |
| sic_code  | SIC#  | string  | SIC industry classification code                           |
| annual_revenue  | Annual Revenue  | currency  | Reported annual revenue of the account                     |
| number_of_employees  | Number of Employees  | number  | Reported employee count                                    |
| open_opp_count  | Open Opps  | number  | Count of open opportunities on the account                 |
| closed_opp_count  | Closed Opps  | number  | Count of closed opportunities on the account               |
| phone_number  | Phone Number  | string  | Account phone number                                       |
| recent_open_opp_date  | Recent Open Opp Date  | date  | Date of the most recent open opportunity                   |
| recent_closed_opp_date  | Recent Closed Opp Date  | date  | Date of the most recent closed opportunity                 |
| tax_id  | Tax Id  | string  | Tax identifier for the account                             |
| account_acv  | Account ACV  | currency  | Annual contract value attributed to the account            |
| open_pipeline_amount  | Open Pipeline Amount  | currency  | Total value of open pipeline on the account                |
| nces_id  | NCES ID  | string  | NCES identifier (education sector)                         |
| partner_count  | Partner Count  | number  | Number of partners matched to this account                 |
| partner_account_name  | Partner Account Name  | string  | Name of the account in the partner's CRM                   |
| partner_org_name  | Partner Org Name  | string  | Name of the partner organization                           |
| partner_account_type  | Partner Account Type  | string  | Account type as classified by the partner                  |
| partner_account_acv  | Partner Account ACV  | currency  | Partner-reported ACV for the matched account               |
| partner_account_owner_name  | Partner Account Owner Name  | name  | Full name of the partner's account owner                   |
| partner_account_owner_email  | Partner Account Owner Email  | email  | Email of the partner's account owner                       |
| partner_account_owner_title  | Partner Account Owner Title  | title  | Job title of the partner's account owner                   |
| partner_account_owner_phone  | Partner Account Owner Phone  | phone  | Phone number of the partner's account owner                |
| partner_crm_account_id  | Partner CRM Account Id  | string  | Account identifier in the partner's CRM                    |
| partner_first_match_date  | First Match Date  | date  | Date the account was first matched with this partner       |
| partner_open_pipeline_amount  | Partner Open Pipeline Amount  | currency  | Partner's open pipeline value on the matched account       |
| partner_open_opp  | Partner Open Opp  | currency  | Partner's open opportunity value on the matched account    |
| partner_closed_opp  | Partner Closed Opp  | currency  | Partner's closed opportunity value on the matched account  |
| partner_closed_opp_won_count  | Partner Closed Opp Won Count  | currency  | Count of closed-won opportunities reported by the partner  |
| partner_website  | Partner Org Website  | string  | Website of the partner organization                        |
| prm_record_id  | Partner Org PRM ID  | string  | Partner organization's identifier in the PRM               |
| partner_owner  | Partner Org Manager Name  | string  | Name of the internal manager owning the partner relationship  |
| partner_owner_email  | Partner Org Manager Email  | string  | Email of the internal partner manager                      |
| partner_owner_phone  | Partner Org Manager Phone  | string  | Phone of the internal partner manager                      |
| partner_org_partner_type  | Partner Org Type  | string  | Type of partner (e.g., reseller, ISV, SI)                  |
| average_referral_deal_size  | Partner Org Avg Deal Size  | currency  | Average deal size for referrals from this partner          |
| partner_street  | Partner Org Street  | string  | Partner organization street address                        |
| partner_city  | Partner Org City  | string  | Partner organization city                                  |
| partner_state  | Partner Org State  | string  | Partner organization state or region                       |
| partner_postal_code  | Partner Org Postal Code  | string  | Partner organization postal code                           |
| partner_country  | Partner Org Country  | string  | Partner organization country                               |
| customownertitle  | Custom Owner Title  | title  | Job title of a custom-mapped account owner                 |
| customowneremail  | Custom Owner Email  | email  | Email of a custom-mapped account owner                     |
| customownername  | Custom Owner Name  | name  | Full name of a custom-mapped account owner                 |

---

## 4. Filter Language

Filters are passed as key-value pairs in the `filters` object of the `ReportRequest` body. The **key** is the column name (as returned in the response `content` objects), and the **value** is a string that encodes the filter operation, using special suffixes and delimiters.

### Filter Operations

| Operation | Suffix | Value Format | Description |
| --- | --- | --- | --- |
| Exact match       | _(none)_  | `value1-,-value2-,-value3`  | Matches rows where the field equals **any** of the values (OR logic).                          |
| Not equal         | `-!-`     | `value1-,-value2-!-`        | Excludes rows matching **any** of the values (AND logic). NULLs are preserved.                |
| Contains          | `-?-`     | `search1-,-search2-?-`      | Case-insensitive substring match. Row must contain **all** terms (AND logic).                 |
| Does not contain  | `-^-`     | `exclude1-,-exclude2-^-`    | Case-insensitive substring exclusion. Row must not contain **any** of the terms (AND logic).  |
| Range             | `<->`     | `min<->max`                 | Matches rows where the field value falls between `min` and `max` (inclusive).                 |

### Multi-Value Delimiter

Use `-,-` to separate multiple values within a single filter:

```
"partner_org_name": "Example Pharma Inc.-,-Example Networks Inc."
```

This matches rows where `partner_org_name` is "Example Pharma Inc." **OR** "Example Networks Inc.".

### Supported Operations by Column Type

| Column Type | Exact Match | Not Equal | Contains | Does Not Contain | Range |
| --- | --- | --- | --- | --- | --- |
| String             | Y       | Y      | Y      | Y          |        |
| Boolean            | Y       |        |        |            |        |
| UUID               | Y       | Y      | Y      | Y          |        |
| Date               |         |        |        |            | Y      |
| Number (int)       |         |        |        |            | Y      |
| Currency / Double  |         |        |        |            | Y      |

### Filter Value Syntax by Type

**String / UUID** - pass the display value as a string:

```json
{
  "state": "Oklahoma"
}
```
```json
{
  "state": "Oklahoma-,-Texas-,-California"
}
```
```json
{
  "account_name": "Example-?-"
}
```
```json
{
  "account_name": "Test-^-"
}
```
```json
{
  "state": "Oklahoma-,-Texas-!-"
}
```

**Boolean** - pass `"true"` or `"false"`:

```json
{
  "custom_ispartnerpaid": "true"
}
```

**Date** - pass epoch timestamps (seconds) as a range:

```json
{
  "recent_open_opp_date": "1700000000<->1760000000"
}
```

**Number / Currency** - pass numeric values as a range:

```json
{
  "open_opp_count": "1<->10"
}
```
```json
{
  "open_pipeline_amount": "100000<->500000"
}
```

### Discovering Filter Values

Before building a filter, you can use the `/filterdata` endpoint to retrieve the available values for any column. This is a paginated endpoint — pass the column name as the `filterField` query parameter.

```
POST /v1/report-analytics/report/{reportType}/filterdata?filterField={columnName}
```

For **string** columns, the response contains the distinct values you can use in an exact-match or contains filter. For **numeric/date** columns, the response includes `filterRangeMin` and `filterRangeMax` to help you build a range filter.

> **Page size:** The default page size is 20. You can request up to **2000** results per page by setting the `size` query parameter (e.g. `size=200`).

**Example: get available values for** `partner_org_name`:

```shell
curl -X POST \
  "https://reports-analytics.partnertap.com/v1/report-analytics/report/GLOBAL_VERTICAL_ACCOUNTS/filterdata?filterField=partner_org_name&page=0&size=10" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{}'
```

**Response:**

```json
{
  "totalElements": 42,
  "totalPages": 5,
  "number": 0,
  "size": 10,
  "content": [
    {
      "filterData": "Example Pharma Inc.",
      "filterRangeMin": null,
      "filterRangeMax": null,
      "filterType": "STRING"
    },
    {
      "filterData": "Example Networks Inc.",
      "filterRangeMin": null,
      "filterRangeMax": null,
      "filterType": "STRING"
    }
  ]
}
```

You can then take a `filterData` value from the response and use it directly in a `/records` filter:

```json
{
  "filters": {
    "partner_org_name": "Example Pharma Inc."
  }
}
```

**Example: get range bounds for** `open_pipeline_amount`:

```shell
curl -X POST \
  "https://reports-analytics.partnertap.com/v1/report-analytics/report/GLOBAL_VERTICAL_ACCOUNTS/filterdata?filterField=open_pipeline_amount&page=0&size=1" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{}'
```

**Response:**

```json
{
  "totalElements": 1,
  "content": [
    {
      "filterData": null,
      "filterRangeMin": 0.0,
      "filterRangeMax": 500000000.0,
      "filterType": "CURRENCY"
    }
  ]
}
```

Use the min/max to build a range filter:

```json
{
  "filters": {
    "open_pipeline_amount": "100000<->500000"
  }
}
```

### Combining Multiple Filters

All filters in the `filters` object are combined with **AND** logic:

```json
{
  "filters": {
    "state": "Oklahoma",
    "open_opp_count": "1<->10",
    "account_name": "Example-?-"
  }
}
```

This returns rows where state is "Oklahoma" **AND** open opp count is between 1-10 **AND** account name contains "Example".

### Example: Filtering by Partner

To filter records to a specific partner, use the `partner_org_name` field.

**Single partner (exact match):**

```shell
curl -X POST \
  "https://reports-analytics.partnertap.com/v1/report-analytics/report/GLOBAL_VERTICAL_ACCOUNTS/records?page=0&size=20" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{
    "filters": {
      "partner_org_name": "Example Pharma Inc."
    }
  }'
```

**Multiple partners (exact match, OR logic):**

```shell
curl -X POST \
  "https://reports-analytics.partnertap.com/v1/report-analytics/report/GLOBAL_VERTICAL_ACCOUNTS/records?page=0&size=20" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{
    "filters": {
      "partner_org_name": "Example Pharma Inc.-,-Example Networks Inc."
    }
  }'
```

**Partner name contains (case-insensitive):**

```shell
curl -X POST \
  "https://reports-analytics.partnertap.com/v1/report-analytics/report/GLOBAL_VERTICAL_ACCOUNTS/records?page=0&size=20" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{
    "filters": {
      "partner_org_name": "exa-?-"
    }
  }'
```

**Exclude a partner:**

```shell
curl -X POST \
  "https://reports-analytics.partnertap.com/v1/report-analytics/report/GLOBAL_VERTICAL_ACCOUNTS/records?page=0&size=20" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{
    "filters": {
      "partner_org_name": "Example Pharma Inc.-!-"
    }
  }'
```

**Combined: filter by partner + state + open pipeline range:**

```shell
curl -X POST \
  "https://reports-analytics.partnertap.com/v1/report-analytics/report/GLOBAL_VERTICAL_ACCOUNTS/records?page=0&size=20" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{
    "filters": {
      "partner_org_name": "Example Pharma Inc.",
      "state": "Oklahoma",
      "open_pipeline_amount": "100000<->500000"
    }
  }'
```

---

## Other Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/v1/report-analytics/report/{reportType}/columns`     | POST    | Get available columns for a report  |
| `/v1/report-analytics/report/{reportType}/filterdata`  | POST    | Get filter values for a column      |
| `/v1/report-analytics/report/{reportType}/download`    | POST    | Download report as CSV              |
| `/v1/report-analytics/report/{reportType}/dashboard`   | POST    | Get dashboard metrics for a report  |

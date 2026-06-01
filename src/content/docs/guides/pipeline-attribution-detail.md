---
title: Pipeline Attribution Detail API Guide
description: Guide for using the PartnerTap Report Analytics API to retrieve the Pipeline Attribution Detail report, including authentication, field reference, and filtering.
---

This document is a guide for using the PartnerTap Analytics API for retrieving the **Pipeline Attribution Detail** report.

The Pipeline Attribution Detail report links individual attribution events to the new opportunities that resulted from partner-influenced activity. Each row represents an attribution event tied to a new opportunity (a "NEW Opp"), including the opportunity's name, amount, created date, the number of days from the event to the new opp, the partner credited with the event, and the event's type, subtype, source, and description. Use this report to trace which partner events drove pipeline.

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

> **Rate Limiting:** Each API key is rate-limited to a maximum of 100 requests per minute. The counter resets on a rolling 1-minute window. If the limit is exceeded, the server responds with HTTP `429 Too Many Requests`. The rate limit is tracked per API key — separate keys have independent counters.

---

## 2. Get Report Records

Returns paginated report records for the Pipeline Attribution Detail report.

### Request

```
POST /v1/report-analytics/report/PIPELINE_ATTRIBUTION_DETAIL/records?page=0&size=20&sort=columnName,asc
Content-Type: application/json
```

### Path Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `reportType`  | string  | Yes       | Must be `PIPELINE_ATTRIBUTION_DETAIL`  |

### Query Parameters (Pagination)

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `page`     | integer  | No        | Zero-based page index (default: 0)                                                          |
| `size`     | integer  | No        | Number of records per page (default: 20, max: 2000)                                          |
| `sort`     | string   | No        | Sorting criteria in the format `property,asc\|desc`. Multiple sort criteria are supported.  |

### Request Body (`ReportRequest`)

```json
{
  "filters": {},
  "search": "",
  "context": {
    "partnerPublicIds": ["<PARTNER_ORG_UUID_1>", "<PARTNER_ORG_UUID_2>"],
    "eventTypeCodes": ["ACTION_LIST", "WORKFLOW"],
    "dateRangeDays": 30,
    "oppCreatedDateDays": 90
  }
}
```

> **Important:** The `context` object is **required**. Without `partnerPublicIds` and `eventTypeCodes`, the API will return an error. Without a date scope, the report will run unbounded against the event and opportunity history. See [Required Context Parameters](#21-required-context-parameters) below.

### 2.1. Required Context Parameters

The Pipeline Attribution Detail report is scoped via the `context` object on the `ReportRequest` body. Use this object to declare which partners' events you want, which event types to include, and the time windows for the attribution event and the new opportunity.

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `partnerPublicIds`     | string[]  | **Yes**   | List of partner organization UUIDs to include. Obtain these from the [All Partner Organizations](./partner-org-report#2-get-list-of-partner-organizations) report (the `companyPartnerPublicId` field). The request will fail if this key is missing or empty. |
| `eventTypeCodes`       | string[]  | **Yes**   | List of attribution event type codes to include. Use the [`/v1/attribution/event-types`](#other-endpoints) endpoint to retrieve the valid codes. The request will fail if this key is missing or empty.                                       |
| `dateRangeDays`        | integer   | No        | Convenience window — limits results to events that occurred within the last N days from now. Ignored when `eventDateStart` and `eventDateEnd` are both set.                                                                                              |
| `eventDateStart`       | string    | No        | Inclusive lower bound of the event date window (epoch seconds, as a string). Must be paired with `eventDateEnd`. Takes precedence over `dateRangeDays`.                                                                                                |
| `eventDateEnd`         | string    | No        | Inclusive upper bound of the event date window (epoch seconds, as a string). Must be paired with `eventDateStart`. Takes precedence over `dateRangeDays`.                                                                                              |
| `oppCreatedDateDays`   | integer   | No        | Convenience window — limits results to opportunities created within the last N days from now. Ignored when `oppCreatedDateStart` and `oppCreatedDateEnd` are both set.                                                                                |
| `oppCreatedDateStart`  | string    | No        | Inclusive lower bound of the opportunity-created window (epoch seconds, as a string). Must be paired with `oppCreatedDateEnd`. Takes precedence over `oppCreatedDateDays`.                                                                            |
| `oppCreatedDateEnd`    | string    | No        | Inclusive upper bound of the opportunity-created window (epoch seconds, as a string). Must be paired with `oppCreatedDateStart`. Takes precedence over `oppCreatedDateDays`.                                                                          |

**Date scoping rules** (apply independently to the event date and the opportunity-created date):

- If both `*Start` and `*End` are provided, an inclusive range filter is applied.
- Else if `*Days` is provided, results are limited to the last N days from now.
- Otherwise, no filter is applied on that date. **For performance, always include a date scope on both.**

**Example with explicit ranges for both event date and opp-created date:**

```json
{
  "filters": {},
  "search": "",
  "context": {
    "partnerPublicIds": ["c1727859-692f-499e-8c2a-b1fa50aa1a65"],
    "eventTypeCodes": ["ACTION_LIST", "WORKFLOW"],
    "eventDateStart": "1722470400",
    "eventDateEnd": "1725148800",
    "oppCreatedDateStart": "1722470400",
    "oppCreatedDateEnd": "1730419200"
  }
}
```

### Response

**200 OK** — Returns a paginated response containing report records (showing only 1 record for this example).

```json
{
  "totalElements": 312,
  "totalPages": 16,
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
      "account_name": "Example Logistics",
      "opp_name": "Example Logistics — Q4 Expansion",
      "opp_amount": 125000.00,
      "opp_created_date": 1722705610,
      "number_days_to_new_opp": 14,
      "partner_org_name": "Example Pharma Inc.",
      "event_date": 1721472810,
      "event_type_display_name": "Action List",
      "event_subtype_display_name": "Action List Downloaded",
      "event_source": "PartnerTap",
      "event_name": "Q3 Pipeline Push - Logistics",
      "event_description": "Action list 'Q3 Pipeline Push - Logistics' was downloaded by Jane Doe.",
      "company_partner_public_id": "c1727859-692f-499e-8c2a-b1fa50aa1a65",
      "top_parent_crm_account_name": "Example Logistics Group",
      "opp_crm_opportunity_id": "006XYZ789"
    }
  ],
  "noDataFoundMessage": null
}
```

### Example

```shell
curl -X POST \
  "https://reports-analytics.partnertap.com/v1/report-analytics/report/PIPELINE_ATTRIBUTION_DETAIL/records?page=0&size=20" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{
    "filters": {},
    "search": "",
    "context": {
      "partnerPublicIds": ["c1727859-692f-499e-8c2a-b1fa50aa1a65"],
      "eventTypeCodes": ["ACTION_LIST", "WORKFLOW"],
      "dateRangeDays": 30,
      "oppCreatedDateDays": 90
    }
  }'
```

---

## 3. Field Names & Types

Here are all of the standard fields for the Pipeline Attribution Detail report. If you have custom fields they will appear with the prefix "custom\_" in the records response.

Note: Columns prefixed with "partner\_" populate depending on your partner's share settings and available data. Columns prefixed with "opp\_" describe the new opportunity ("NEW Opp") that the attribution event is linked to.

| API Name | Display Name | Type | Description |
| --- | --- | --- | --- |
| account_name  | Account Name  | string  | Name of the account associated with the new opportunity                                  |
| opp_name  | NEW Opp Name  | string  | Name of the new opportunity influenced by the partner activity                             |
| opp_amount  | NEW Opp Amount  | currency  | Amount of the new opportunity                                                            |
| opp_created_date  | NEW Opp Created Date  | date  | Date the new opportunity was created (epoch seconds)                                |
| number_days_to_new_opp  | Number Days to New Opp  | number  | Number of days between the attribution event and the new opportunity        |
| partner_org_name  | Partner Org Name  | string  | Name of the partner organization credited with the event                              |
| event_date  | Attribution Event Date  | date  | Date the attribution event occurred (epoch seconds)                                      |
| event_type_display_name  | Attribution Event Type  | string  | Type classification of the event                                                  |
| event_subtype_display_name  | Attribution Event Subtype  | string  | More specific subtype of the event                                            |
| event_source  | Attribution Event Source  | string  | System or source that produced the event (e.g., PartnerTap, CRM)                       |
| event_name  | Attribution Event Name  | string  | Display name of the specific event                                                       |
| event_description  | Attribution Event Description  | string  | Human-readable description of what happened                                 |
| event_user_name  | Attribution Event User Name  | name  | Full name of the user who triggered the event                                   |
| event_user_email  | Attribution Event User Email  | email  | Email of the user who triggered the event                                     |
| event_user_title  | Attribution Event User Title  | title  | Job title of the user who triggered the event                                 |
| company_partner_public_id  | Partner Org ID  | string  | UUID of the partner organization                                                  |
| top_parent_crm_account_id  | Top Parent Account ID  | string  | CRM ID of the top-level parent account in the account hierarchy             |
| top_parent_crm_account_name  | Top Parent Account Name  | string  | Name of the top-level parent account in the account hierarchy            |
| opp_crm_opportunity_id  | NEW Opp ID  | string  | Unique identifier of the new opportunity in the source CRM                       |
| event_source_link  | Attribution Event Source ID  | string  | Identifier or link back to the source system record for the event           |
| custom_event_campaign_id  | Campaign ID  | string  | Campaign ID associated with the event (custom event field)                       |
| custom_event_lead_id  | Lead ID  | string  | Lead ID associated with the event (custom event field)                               |
| custom_event_contact_id  | Contact ID  | string  | Contact ID associated with the event (custom event field)                         |
| custom_event_opportunity_id  | Opportunity ID  | string  | Opportunity ID associated with the event (custom event field)                 |
| custom_event_detail_1  | Detail 1  | string  | Additional custom detail field 1                                                       |
| custom_event_detail_2  | Detail 2  | string  | Additional custom detail field 2                                                       |
| custom_event_note  | Note  | string  | Free-text note associated with the event                                                   |
| account_type  | Account Type  | string  | Account classification (e.g., Customer, Prospect)                                        |
| street  | Street  | string  | Account street address                                                                         |
| city  | City  | string  | Account city                                                                                     |
| state  | State  | string  | Account state or region                                                                         |
| zip_code  | Zip Code  | string  | Account postal code                                                                          |
| country  | Country  | string  | Account country                                                                                |
| website  | Website  | string  | Account website URL                                                                            |
| industry  | Industry  | string  | Industry classification of the account                                                       |
| territory  | Territory  | string  | Sales territory the account is assigned to                                                 |
| number_of_employees  | Number of Employees  | number  | Reported employee count for the account                                       |
| open_opp_count  | Open Opps  | number  | Count of open opportunities on the account                                              |
| closed_opp_count  | Closed Opps  | number  | Count of closed opportunities on the account                                          |
| is_customer  | Is Customer  | boolean  | Whether the account is flagged as a customer                                              |
| annual_revenue  | Annual Revenue  | currency  | Reported annual revenue of the account                                              |
| sic_code  | SIC#  | string  | SIC industry classification code                                                            |
| naics_code  | NAICS#  | string  | NAICS industry classification code                                                         |
| nces_id  | NCES ID  | string  | NCES identifier (education sector)                                                          |
| duns_number  | DUNS Number  | string  | Dun & Bradstreet DUNS identifier                                                         |
| phone_number  | Phone Number  | phone  | Account phone number                                                                        |
| account_acv  | Account ACV  | currency  | Annual contract value attributed to the account                                       |
| open_pipeline_amount  | Open Pipeline Amount  | currency  | Total value of open pipeline on the account                                |
| closed_won_opp_count  | Closed Won Opps  | number  | Count of closed-won opportunities on the account                                |
| owner_name  | Owner Name  | name  | Full name of the account owner                                                              |
| owner_email  | Owner Email  | email  | Email of the account owner                                                                |
| owner_title  | Owner Title  | title  | Job title of the account owner                                                            |
| owner_phone  | Owner Phone  | phone  | Phone of the account owner                                                                |
| owner_division  | Owner Division  | string  | Division the account owner belongs to                                              |
| partner_street  | Partner Org Street  | string  | Partner organization street address                                            |
| partner_city  | Partner Org City  | string  | Partner organization city                                                         |
| partner_state  | Partner Org State  | string  | Partner organization state or region                                             |
| partner_country  | Partner Org Country  | string  | Partner organization country                                                  |
| partner_zip_code  | Partner Org Zip Code  | string  | Partner organization postal code                                            |
| partner_owner_name  | Partner Org Manager Name  | name  | Name of the internal manager owning the partner relationship              |
| partner_owner_email  | Partner Org Manager Email  | email  | Email of the internal partner manager                                     |
| partner_owner_phone  | Partner Org Manager Phone  | phone  | Phone of the internal partner manager                                     |
| partner_type  | Partner Org Type  | string  | Type of partner (e.g., reseller, ISV, SI)                                          |
| partner_status  | Partner Org Status  | string  | Connection status of the partner organization                                 |
| partner_website  | Partner Org Website  | string  | Website of the partner organization                                          |
| partner_crm_record_id  | Partner Org CRM Record ID  | string  | Partner organization identifier in the CRM                          |
| partner_prm_record_id  | Partner Org PRM Record ID  | string  | Partner organization identifier in the PRM                          |
| partner_average_referral_deal_size  | Partner Org Avg Referral Deal Size  | currency  | Average referral deal size for the partner organization  |
| opp_crm_account_id  | NEW Opp Linked Account ID  | string  | CRM account ID the new opportunity is linked to                                |
| opp_stage_name  | NEW Opp Stage  | string  | Stage of the new opportunity                                                          |
| opp_close_date  | NEW Opp Close Date  | date  | Close date of the new opportunity (epoch seconds)                                 |
| opp_is_won  | NEW Opp Is Won  | boolean  | Whether the new opportunity is marked as won                                        |
| opp_opportunity_type  | NEW Opp Type  | string  | Type of the new opportunity                                                      |
| opp_is_closed  | NEW Opp Is Closed  | boolean  | Whether the new opportunity is closed                                            |
| opp_opportunity_owner_name  | NEW Opp Owner Name  | name  | Full name of the new opportunity's owner                                   |
| opp_opportunity_owner_email  | NEW Opp Owner Email  | email  | Email of the new opportunity's owner                                     |
| opp_opportunity_owner_title  | NEW Opp Owner Title  | title  | Job title of the new opportunity's owner                                 |
| opp_opportunity_owner_phone  | NEW Opp Owner Phone  | phone  | Phone of the new opportunity's owner                                     |
| opp_last_modified_date  | NEW Opp Last Modified Date  | date  | Last modified date of the new opportunity (epoch seconds)              |
| opp_account_name  | NEW Opp Account Name  | string  | Account name on the new opportunity                                            |
| opp_probability  | NEW Opp Probability  | number  | Win probability percent for the new opportunity                                   |
| opp_expected_revenue  | NEW Opp Expected Revenue  | currency  | Expected revenue for the new opportunity                              |
| opp_pt_status  | NEW Opp PT Status  | string  | PartnerTap status of the new opportunity                                          |

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

**String / UUID** — pass the display value as a string:

```json
{
  "partner_org_name": "Example Pharma Inc."
}
```
```json
{
  "partner_org_name": "Example Pharma Inc.-,-Example Networks Inc."
}
```
```json
{
  "opp_name": "Expansion-?-"
}
```
```json
{
  "opp_name": "Test-^-"
}
```
```json
{
  "event_type_display_name": "Action List-,-Workflow-!-"
}
```

**Boolean** — pass `"true"` or `"false"`:

```json
{
  "is_customer": "true"
}
```

**Date** — pass epoch timestamps (seconds) as a range:

```json
{
  "opp_created_date": "1700000000<->1760000000"
}
```

**Number / Currency** — pass numeric values as a range:

```json
{
  "opp_amount": "50000<->250000"
}
```
```json
{
  "number_days_to_new_opp": "0<->30"
}
```

### Discovering Filter Values

Before building a filter, you can use the `/filterdata` endpoint to retrieve the available values for any column. This is a paginated endpoint — pass the column name as the `filterField` query parameter.

```
POST /v1/report-analytics/report/PIPELINE_ATTRIBUTION_DETAIL/filterdata?filterField={columnName}
```

For **string** columns, the response contains the distinct values you can use in an exact-match or contains filter. For **numeric/date** columns, the response includes `filterRangeMin` and `filterRangeMax` to help you build a range filter.

> **Page size:** The default page size is 20. You can request up to **2000** results per page by setting the `size` query parameter (e.g. `size=200`).

**Example: get available values for** `partner_org_name`:

```shell
curl -X POST \
  "https://reports-analytics.partnertap.com/v1/report-analytics/report/PIPELINE_ATTRIBUTION_DETAIL/filterdata?filterField=partner_org_name&page=0&size=10" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{}'
```

**Response:**

```json
{
  "totalElements": 12,
  "totalPages": 2,
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

**Example: get range bounds for** `opp_amount`:

```shell
curl -X POST \
  "https://reports-analytics.partnertap.com/v1/report-analytics/report/PIPELINE_ATTRIBUTION_DETAIL/filterdata?filterField=opp_amount&page=0&size=1" \
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
    "opp_amount": "100000<->500000"
  }
}
```

### Combining Multiple Filters

All filters in the `filters` object are combined with **AND** logic:

```json
{
  "filters": {
    "partner_org_name": "Example Pharma Inc.",
    "opp_amount": "100000<->500000",
    "opp_created_date": "1700000000<->1760000000"
  }
}
```

This returns rows where the partner org is "Example Pharma Inc." **AND** the new opp amount is between $100K-$500K **AND** the new opp was created within the given date range.

### Example: Filtering New Opps Created in a Window

```shell
curl -X POST \
  "https://reports-analytics.partnertap.com/v1/report-analytics/report/PIPELINE_ATTRIBUTION_DETAIL/records?page=0&size=20" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{
    "filters": {
      "partner_org_name": "Example Pharma Inc.",
      "opp_created_date": "1722470400<->1725148800",
      "event_type_display_name": "Action List-,-Workflow"
    }
  }'
```

---

## Other Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/v1/report-analytics/report/PIPELINE_ATTRIBUTION_DETAIL/columns`     | POST    | Get available columns for the report                       |
| `/v1/report-analytics/report/PIPELINE_ATTRIBUTION_DETAIL/filterdata`  | POST    | Get filter values for a column                             |
| `/v1/attribution/event-types`                                          | GET     | List the valid `eventTypeCodes` to use in `context`        |
| `/v1/channelecosystem/records`                                         | POST    | List your connected partners; use the `companyPartnerPublicId` values in `context.partnerPublicIds`. See [All Partner Organizations](./partner-org-report#2-get-list-of-partner-organizations). |

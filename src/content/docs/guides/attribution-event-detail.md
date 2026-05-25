---
title: Attribution Event Detail API Guide
description: Guide for using the PartnerTap Report Analytics API to retrieve the Attribution Event Detail report, including authentication, field reference, and filtering.
---

This document is a guide for using the PartnerTap Analytics API for retrieving the **Attribution Event Detail** report.

The Attribution Event Detail report shows every individual attribution event captured against your accounts. An attribution event is any user action attributable to a partner's influence — for example, a downloaded action list, a workflow intro, or a CRM update tied to partner activity. Each row in the report represents a single attribution event, including the account, the partner credited with the event, the event type and subtype, and the user who performed the action.

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

Returns paginated report records for the Attribution Event Detail report.

### Request

```
POST /v1/report-analytics/report/ATTRIBUTION_EVENTS/records?page=0&size=20&sort=columnName,asc
Content-Type: application/json
```

### Path Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `reportType`  | string  | Yes       | Must be `ATTRIBUTION_EVENTS`  |

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
    "dateRangeDays": 30
  }
}
```

> **Important:** The `context` object is **required**. Without `partnerPublicIds` and `eventTypeCodes`, the API will return an error. Without a date scope, the report will run unbounded against the event history. See [Required Context Parameters](#21-required-context-parameters) below.

### 2.1. Required Context Parameters

The Attribution Event Detail report is scoped via the `context` object on the `ReportRequest` body. Use this object to declare which partners' events you want, which event types to include, and the time window to query.

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `partnerPublicIds`     | string[]  | **Yes**   | List of partner organization UUIDs to include. Obtain these from the [All Partner Organizations](./partner-org-report#2-get-list-of-partner-organizations) report (the `companyPartnerPublicId` field). The request will fail if this key is missing or empty. |
| `eventTypeCodes`       | string[]  | **Yes**   | List of attribution event type codes to include. Use the [`/v1/attribution/event-types`](#other-endpoints) endpoint to retrieve the valid codes. The request will fail if this key is missing or empty.                                       |
| `dateRangeDays`        | integer   | No        | Convenience window — limits results to events that occurred within the last N days from now. Ignored when `eventDateStart` and `eventDateEnd` are both set.                                                                                              |
| `eventDateStart`       | string    | No        | Inclusive lower bound of the event date window (epoch seconds, as a string). Must be paired with `eventDateEnd`. Takes precedence over `dateRangeDays`.                                                                                                |
| `eventDateEnd`         | string    | No        | Inclusive upper bound of the event date window (epoch seconds, as a string). Must be paired with `eventDateStart`. Takes precedence over `dateRangeDays`.                                                                                              |

**Date scoping rules:**

- If both `eventDateStart` and `eventDateEnd` are provided, an inclusive range filter is applied.
- Else if `dateRangeDays` is provided, results are limited to the last N days from now.
- Otherwise, no event-date filter is applied. **For performance, always include a date scope.**

**Example with an explicit event-date range:**

```json
{
  "filters": {},
  "search": "",
  "context": {
    "partnerPublicIds": ["c1727859-692f-499e-8c2a-b1fa50aa1a65"],
    "eventTypeCodes": ["ACTION_LIST", "WORKFLOW"],
    "eventDateStart": "1722470400",
    "eventDateEnd": "1725148800"
  }
}
```

### Response

**200 OK** — Returns a paginated response containing report records (showing only 1 record for this example).

```json
{
  "totalElements": 1284,
  "totalPages": 65,
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
      "partner_org_name": "Example Pharma Inc.",
      "event_date": 1758921277,
      "event_type_display_name": "Action List",
      "event_subtype_display_name": "Action List Downloaded",
      "event_name": "Q3 Pipeline Push - Logistics",
      "event_description": "Action list 'Q3 Pipeline Push - Logistics' was downloaded by Jane Doe.",
      "event_source": "PartnerTap",
      "event_user_name": "Jane Doe",
      "event_user_email": "jane.doe@example.com",
      "event_user_title": "Sales Development Rep",
      "company_partner_public_id": "c1727859-692f-499e-8c2a-b1fa50aa1a65",
      "crm_account_id": "001ABC123",
      "top_parent_crm_account_id": "001PARENT456",
      "top_parent_crm_account_name": "Example Logistics Group"
    }
  ],
  "noDataFoundMessage": null
}
```

### Example

```shell
curl -X POST \
  "https://reports-analytics.partnertap.com/v1/report-analytics/report/ATTRIBUTION_EVENTS/records?page=0&size=20" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{
    "filters": {},
    "search": "",
    "context": {
      "partnerPublicIds": ["c1727859-692f-499e-8c2a-b1fa50aa1a65"],
      "eventTypeCodes": ["ACTION_LIST", "WORKFLOW"],
      "dateRangeDays": 30
    }
  }'
```

---

## 3. Field Names & Types

Here are all of the standard fields for the Attribution Event Detail report. If you have custom fields they will appear with the prefix "custom\_" in the records response.

Note: Columns prefixed with "partner\_" populate depending on your partner's share settings and available data.

| API Name | Display Name | Type | Description |
| --- | --- | --- | --- |
| account_name  | Account Name  | string  | Name of the account associated with the event                                            |
| partner_org_name  | Partner Org Name  | string  | Name of the partner organization credited with the event                              |
| event_date  | Attribution Event Date  | date  | Date the attribution event occurred (epoch seconds)                                      |
| event_group_display_name  | Attribution Event Group  | string  | Top-level grouping for the event (e.g., Action List, Workflow)                  |
| event_type_display_name  | Attribution Event Type  | string  | Type classification of the event                                                  |
| event_subtype_display_name  | Attribution Event Subtype  | string  | More specific subtype of the event                                            |
| event_name  | Attribution Event Name  | string  | Display name of the specific event                                                       |
| event_description  | Attribution Event Description  | string  | Human-readable description of what happened                                 |
| event_source  | Attribution Event Source  | string  | System or source that produced the event (e.g., PartnerTap, CRM)                       |
| event_user_name  | Attribution Event User Name  | name  | Full name of the user who triggered the event                                   |
| event_user_email  | Attribution Event User Email  | email  | Email of the user who triggered the event                                     |
| event_user_title  | Attribution Event User Title  | title  | Job title of the user who triggered the event                                 |
| company_partner_public_id  | Partner Org ID  | string  | UUID of the partner organization                                                  |
| crm_account_id  | CRM Account ID  | string  | Unique identifier of the account in the source CRM                                   |
| top_parent_crm_account_id  | Top Parent Account ID  | string  | CRM ID of the top-level parent account in the account hierarchy             |
| top_parent_crm_account_name  | Top Parent Account Name  | string  | Name of the top-level parent account in the account hierarchy            |
| first_match  | First Match  | string  | Indicator of whether this event is associated with the first match between the account and partner  |
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
| phone_number  | Phone Number  | string  | Account phone number                                                                       |
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
"event_type_display_name": "Action List-,-Workflow"
```

This matches rows where `event_type_display_name` is "Action List" **OR** "Workflow".

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
  "event_name": "Pipeline-?-"
}
```
```json
{
  "event_name": "Test-^-"
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
  "event_date": "1700000000<->1760000000"
}
```

**Number / Currency** — pass numeric values as a range:

```json
{
  "open_opp_count": "1<->10"
}
```

### Discovering Filter Values

Before building a filter, you can use the `/filterdata` endpoint to retrieve the available values for any column. This is a paginated endpoint — pass the column name as the `filterField` query parameter.

```
POST /v1/report-analytics/report/ATTRIBUTION_EVENTS/filterdata?filterField={columnName}
```

For **string** columns, the response contains the distinct values you can use in an exact-match or contains filter. For **numeric/date** columns, the response includes `filterRangeMin` and `filterRangeMax` to help you build a range filter.

> **Page size:** The default page size is 20. You can request up to **2000** results per page by setting the `size` query parameter (e.g. `size=200`).

**Example: get available values for** `event_type_display_name`:

```shell
curl -X POST \
  "https://reports-analytics.partnertap.com/v1/report-analytics/report/ATTRIBUTION_EVENTS/filterdata?filterField=event_type_display_name&page=0&size=10" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{}'
```

**Response:**

```json
{
  "totalElements": 6,
  "totalPages": 1,
  "number": 0,
  "size": 10,
  "content": [
    {
      "filterData": "Action List",
      "filterRangeMin": null,
      "filterRangeMax": null,
      "filterType": "STRING"
    },
    {
      "filterData": "Workflow",
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
    "event_type_display_name": "Action List"
  }
}
```

**Example: get range bounds for** `event_date`:

```shell
curl -X POST \
  "https://reports-analytics.partnertap.com/v1/report-analytics/report/ATTRIBUTION_EVENTS/filterdata?filterField=event_date&page=0&size=1" \
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
      "filterRangeMin": 1700000000,
      "filterRangeMax": 1760000000,
      "filterType": "DATE"
    }
  ]
}
```

Use the min/max to build a range filter:

```json
{
  "filters": {
    "event_date": "1700000000<->1760000000"
  }
}
```

### Combining Multiple Filters

All filters in the `filters` object are combined with **AND** logic:

```json
{
  "filters": {
    "partner_org_name": "Example Pharma Inc.",
    "event_type_display_name": "Action List",
    "event_date": "1700000000<->1760000000"
  }
}
```

This returns rows where the partner org is "Example Pharma Inc." **AND** the event type is "Action List" **AND** the event date falls within the given range.

### Example: Filtering by Event Type and Partner

```shell
curl -X POST \
  "https://reports-analytics.partnertap.com/v1/report-analytics/report/ATTRIBUTION_EVENTS/records?page=0&size=20" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{
    "filters": {
      "partner_org_name": "Example Pharma Inc.",
      "event_type_display_name": "Action List-,-Workflow"
    }
  }'
```

---

## Other Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/v1/report-analytics/report/ATTRIBUTION_EVENTS/columns`     | POST    | Get available columns for the report                       |
| `/v1/report-analytics/report/ATTRIBUTION_EVENTS/filterdata`  | POST    | Get filter values for a column                             |
| `/v1/attribution/event-types`                                 | GET     | List the valid `eventTypeCodes` to use in `context`        |
| `/v1/channelecosystem/records`                                | POST    | List your connected partners; use the `companyPartnerPublicId` values in `context.partnerPublicIds`. See [All Partner Organizations](./partner-org-report#2-get-list-of-partner-organizations). |
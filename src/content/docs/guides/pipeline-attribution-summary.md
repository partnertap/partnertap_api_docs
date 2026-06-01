---
title: Pipeline Attribution Summary API Guide
description: Guide for using the PartnerTap Report Analytics API to retrieve the Pipeline Attribution Summary report, including authentication, field reference, and filtering.
---

This document is a guide for using the PartnerTap Analytics API for retrieving the **Pipeline Attribution Summary** report.

The Pipeline Attribution Summary report is the rollup view of the [Pipeline Attribution Detail](./pipeline-attribution-detail) report. Each row aggregates attribution activity by **top parent account + new opportunity**, summarizing how much partner-influenced engagement (action lists, downloads, workflows, intros) drove a given new opportunity. Use this report to see, at a glance, the total attribution events and partners that contributed to each new opp.

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

Returns paginated report records for the Pipeline Attribution Summary report.

### Request

```
POST /v1/report-analytics/report/PIPELINE_ATTRIBUTION_SUMMARY/records?page=0&size=20&sort=columnName,asc
Content-Type: application/json
```

### Path Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `reportType`  | string  | Yes       | Must be `PIPELINE_ATTRIBUTION_SUMMARY`  |

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

The Pipeline Attribution Summary report is scoped via the `context` object on the `ReportRequest` body. Use this object to declare which partners' events drive the rollup, which event types to include, and the time windows for the underlying attribution events and the new opportunities.

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `partnerPublicIds`     | string[]  | **Yes**   | List of partner organization UUIDs to include. Obtain these from the [All Partner Organizations](./partner-org-report#2-get-list-of-partner-organizations) report (the `companyPartnerPublicId` field). The request will fail if this key is missing or empty. |
| `eventTypeCodes`       | string[]  | **Yes**   | List of attribution event type codes to include. Use the [`/v1/attribution/event-types`](#other-endpoints) endpoint to retrieve the valid codes. The request will fail if this key is missing or empty.                                       |
| `dateRangeDays`        | integer   | No        | Convenience window — limits the attribution events rolled up to those that occurred within the last N days from now. Ignored when `eventDateStart` and `eventDateEnd` are both set.                                                                       |
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
  "totalElements": 84,
  "totalPages": 5,
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
      "top_parent_crm_account_name": "Example Logistics Group",
      "opp_name": "Example Logistics — Q4 Expansion",
      "opp_amount": 125000.00,
      "opp_created_date": 1722705610,
      "action_lists_created_count": 3,
      "action_list_downloads_count": 8,
      "workflows_initiated_count": 2,
      "workflow_intros_completed_count": 1,
      "total_attribution_events": 14,
      "total_partners": 2,
      "opp_stage_name": "Proposal/Price Quote",
      "opp_close_date": 1733011200,
      "opp_is_won": false
    }
  ],
  "noDataFoundMessage": null
}
```

### Example

```shell
curl -X POST \
  "https://reports-analytics.partnertap.com/v1/report-analytics/report/PIPELINE_ATTRIBUTION_SUMMARY/records?page=0&size=20" \
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

Here are all of the standard fields for the Pipeline Attribution Summary report. If you have custom fields they will appear with the prefix "custom\_" in the records response.

Note: Each row is aggregated by **top parent account + new opportunity**. Counter columns (`*_count`, `total_*`) are sums across all attribution events linked to that new opp. Columns prefixed with "opp\_" describe the new opportunity ("NEW Opp") that the events rolled up to.

| API Name | Display Name | Type | Description |
| --- | --- | --- | --- |
| top_parent_crm_account_name  | Top Parent Account Name  | string  | Name of the top-level parent account in the account hierarchy            |
| opp_name  | NEW Opp Name  | string  | Name of the new opportunity influenced by partner activity                                 |
| opp_amount  | NEW Opp Amount  | currency  | Amount of the new opportunity                                                            |
| opp_created_date  | NEW Opp Created Date  | date  | Date the new opportunity was created (epoch seconds)                                |
| action_lists_created_count  | Action Lists Created  | number  | Number of action lists created that contributed to this new opportunity         |
| action_list_downloads_count  | Action List Downloads  | number  | Number of action list downloads that contributed to this new opportunity      |
| workflows_initiated_count  | Workflows Initiated  | number  | Number of workflows initiated that contributed to this new opportunity            |
| workflow_intros_completed_count  | Workflow Intros Completed  | number  | Number of workflow intros completed that contributed to this new opportunity  |
| total_attribution_events  | Total Attribution Events  | number  | Total count of all attribution events rolled up into this new opportunity        |
| total_partners  | Total Partners  | number  | Number of distinct partner organizations credited with attribution on this new opportunity  |
| top_parent_crm_account_id  | Top Parent Account ID  | string  | CRM ID of the top-level parent account in the account hierarchy             |
| opp_crm_opportunity_id  | NEW Opp ID  | string  | Unique identifier of the new opportunity in the source CRM                       |
| opp_crm_account_id  | NEW Opp Linked Account ID  | string  | CRM account ID the new opportunity is linked to                            |
| opp_stage_name  | NEW Opp Stage  | string  | Stage of the new opportunity                                                              |
| opp_close_date  | NEW Opp Close Date  | date  | Close date of the new opportunity (epoch seconds)                                     |
| opp_is_won  | NEW Opp Is Won  | boolean  | Whether the new opportunity is marked as won                                            |
| opp_opportunity_type  | NEW Opp Type  | string  | Type of the new opportunity                                                          |
| opp_is_closed  | NEW Opp Is Closed  | boolean  | Whether the new opportunity is closed                                                |
| opp_opportunity_owner_name  | NEW Opp Owner Name  | name  | Full name of the new opportunity's owner                                       |
| opp_opportunity_owner_email  | NEW Opp Owner Email  | email  | Email of the new opportunity's owner                                         |
| opp_opportunity_owner_title  | NEW Opp Owner Title  | title  | Job title of the new opportunity's owner                                     |
| opp_opportunity_owner_phone  | NEW Opp Owner Phone  | phone  | Phone of the new opportunity's owner                                         |
| opp_last_modified_date  | NEW Opp Last Modified Date  | date  | Last modified date of the new opportunity (epoch seconds)                  |
| opp_account_name  | NEW Opp Account Name  | string  | Account name on the new opportunity                                                |
| opp_probability  | NEW Opp Probability  | number  | Win probability percent for the new opportunity                                       |
| opp_expected_revenue  | NEW Opp Expected Revenue  | currency  | Expected revenue for the new opportunity                                  |
| opp_pt_status  | NEW Opp PT Status  | string  | PartnerTap status of the new opportunity                                              |

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
"opp_stage_name": "Proposal/Price Quote-,-Negotiation/Review"
```

This matches rows where `opp_stage_name` is "Proposal/Price Quote" **OR** "Negotiation/Review".

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
  "opp_stage_name": "Closed Won"
}
```
```json
{
  "opp_stage_name": "Proposal/Price Quote-,-Negotiation/Review"
}
```
```json
{
  "top_parent_crm_account_name": "Example-?-"
}
```
```json
{
  "top_parent_crm_account_name": "Test-^-"
}
```
```json
{
  "opp_stage_name": "Closed Lost-!-"
}
```

**Boolean** — pass `"true"` or `"false"`:

```json
{
  "opp_is_won": "true"
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
  "total_attribution_events": "5<->50"
}
```
```json
{
  "opp_amount": "100000<->500000"
}
```

### Discovering Filter Values

Before building a filter, you can use the `/filterdata` endpoint to retrieve the available values for any column. This is a paginated endpoint — pass the column name as the `filterField` query parameter.

```
POST /v1/report-analytics/report/PIPELINE_ATTRIBUTION_SUMMARY/filterdata?filterField={columnName}
```

For **string** columns, the response contains the distinct values you can use in an exact-match or contains filter. For **numeric/date** columns, the response includes `filterRangeMin` and `filterRangeMax` to help you build a range filter.

> **Page size:** The default page size is 20. You can request up to **2000** results per page by setting the `size` query parameter (e.g. `size=200`).

**Example: get available values for** `opp_stage_name`:

```shell
curl -X POST \
  "https://reports-analytics.partnertap.com/v1/report-analytics/report/PIPELINE_ATTRIBUTION_SUMMARY/filterdata?filterField=opp_stage_name&page=0&size=10" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{}'
```

**Response:**

```json
{
  "totalElements": 7,
  "totalPages": 1,
  "number": 0,
  "size": 10,
  "content": [
    {
      "filterData": "Prospecting",
      "filterRangeMin": null,
      "filterRangeMax": null,
      "filterType": "STRING"
    },
    {
      "filterData": "Proposal/Price Quote",
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
    "opp_stage_name": "Proposal/Price Quote"
  }
}
```

**Example: get range bounds for** `total_attribution_events`:

```shell
curl -X POST \
  "https://reports-analytics.partnertap.com/v1/report-analytics/report/PIPELINE_ATTRIBUTION_SUMMARY/filterdata?filterField=total_attribution_events&page=0&size=1" \
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
      "filterRangeMin": 1,
      "filterRangeMax": 120,
      "filterType": "NUMBER"
    }
  ]
}
```

Use the min/max to build a range filter:

```json
{
  "filters": {
    "total_attribution_events": "5<->50"
  }
}
```

### Combining Multiple Filters

All filters in the `filters` object are combined with **AND** logic:

```json
{
  "filters": {
    "opp_stage_name": "Closed Won",
    "total_partners": "2<->10",
    "opp_amount": "100000<->500000"
  }
}
```

This returns rows where the new opp is in "Closed Won", contributed to by 2-10 partners, with an amount between $100K-$500K.

### Example: Filtering Won New Opps with Multi-Partner Influence

```shell
curl -X POST \
  "https://reports-analytics.partnertap.com/v1/report-analytics/report/PIPELINE_ATTRIBUTION_SUMMARY/records?page=0&size=20" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{
    "filters": {
      "opp_is_won": "true",
      "total_partners": "2<->20",
      "opp_created_date": "1700000000<->1760000000"
    }
  }'
```

---

## Other Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/v1/report-analytics/report/PIPELINE_ATTRIBUTION_SUMMARY/columns`     | POST    | Get available columns for the report                       |
| `/v1/report-analytics/report/PIPELINE_ATTRIBUTION_SUMMARY/filterdata`  | POST    | Get filter values for a column                             |
| `/v1/attribution/event-types`                                           | GET     | List the valid `eventTypeCodes` to use in `context`        |
| `/v1/channelecosystem/records`                                          | POST    | List your connected partners; use the `companyPartnerPublicId` values in `context.partnerPublicIds`. See [All Partner Organizations](./partner-org-report#2-get-list-of-partner-organizations). |

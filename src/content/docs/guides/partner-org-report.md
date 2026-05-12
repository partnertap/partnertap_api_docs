---
title: Partner Org Report API Guide
description: Guide for using the PartnerTap Analytics API to retrieve the Partner Org report, including authentication, endpoints, filtering, and pagination.
---

This document is a guide for using the PartnerTap Analytics API for retrieving the **Partner Org** report.

The Partner Org report shows all accounts that you and a specific partner organization have in common in your overlapping data set. This report helps you understand the scope of overlap with a particular partner. Before pulling the report, you must first retrieve the list of your connected partner organizations to obtain the partner identifier (`companyPartnerPublicId`) needed to query the matched accounts.

All endpoints follow the pattern `/v1/channelecosystem/...` and accept a `ReportRequestJsonDto` body for specifying the report type, filters, and search criteria.

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

## 2. Get List of Partner Organizations

Before you can pull the Partner Org Matched Accounts report, you need the `companyPartnerPublicId` for the partner you want to query. Use the **All Partner Organizations** report to retrieve your connected partners.

### Request

```
POST /v1/channelecosystem/records?page=0&size=20&sort=columnName,asc
Content-Type: application/json
```

### Query Parameters (Pagination)

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `page`     | integer  | No        | Zero-based page index (default: 0)                                                           |
| `size`     | integer  | No        | Number of records per page (default: 20, max: 2000)                                           |
| `sort`     | string   | No        | Sorting criteria in the format `property,asc\|desc`. Multiple sort criteria are supported.    |

### Request Body

```json
{
  "search": "",
  "filters": {},
  "mapByLocations": false,
  "channelReportType": "PARTNER_ORG_CONNECTED_PARTNER_ORGS",
  "matchingType": "MUTUAL"
}
```

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `channelReportType`   | string   | Yes       | Must be `"PARTNER_ORG_CONNECTED_PARTNER_ORGS"`                |
| `matchingType`        | string   | No        | Use `"MUTUAL"` to get mutually connected partner orgs         |
| `search`              | string   | No        | Free-text search across partner org fields (default: `""`)    |
| `filters`             | object   | No        | Key-value pairs for filtering (see [Filter Language](#6-filter-language))  |
| `mapByLocations`      | boolean  | No        | Default: `false`                                              |

### Response

**200 OK** — Returns a paginated list of partner organizations.

```json
{
  "totalElements": 42,
  "totalPages": 3,
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
      "companyPartnerPublicId": "c1727859-692f-499e-8c2a-b1fa50aa1a65",
      "partnerOrgName": "AbbVie Inc."
    }
  ]
}
```

> **Important:** Save the `companyPartnerPublicId` value from each partner org record. You will need it in the next step to query the matched accounts for that specific partner.

### Example

```shell
curl -X POST \
  "https://reports.partnertap.com/v1/channelecosystem/records?page=0&size=20" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{
    "search": "",
    "filters": {},
    "mapByLocations": false,
    "channelReportType": "PARTNER_ORG_CONNECTED_PARTNER_ORGS",
    "matchingType": "MUTUAL"
  }'
```

---

## 3. Get Partner Org Matched Accounts

Returns the paginated list of accounts that overlap between you and a specific partner organization.

### Request

```
POST /v1/channelecosystem/records?page=0&size=20&sort=columnName,asc
Content-Type: application/json
```

### Query Parameters (Pagination)

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `page`     | integer  | No        | Zero-based page index (default: 0)                                                           |
| `size`     | integer  | No        | Number of records per page (default: 20, max: 2000)                                           |
| `sort`     | string   | No        | Sorting criteria in the format `property,asc\|desc`. Multiple sort criteria are supported.    |

### Request Body

```json
{
  "search": "",
  "filters": {},
  "mapByLocations": false,
  "channelReportType": "PARTNER_ORG_MATCHED_ACCOUNTS",
  "matchingType": "MUTUAL",
  "companyPartnerPublicId": "<PARTNER_ORG_UUID>"
}
```

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `channelReportType`         | string   | Yes       | Must be `"PARTNER_ORG_MATCHED_ACCOUNTS"`                                                         |
| `matchingType`              | string   | Yes       | Use `"MUTUAL"` for mutually matched accounts                                                     |
| `companyPartnerPublicId`    | string   | Yes       | The UUID of the partner org, obtained from the [Partner Organizations](#2-get-list-of-partner-organizations) response  |
| `search`                    | string   | No        | Free-text search across account fields (default: `""`)                                           |
| `filters`                   | object   | No        | Key-value pairs for filtering (see [Filter Language](#6-filter-language))                         |
| `mapByLocations`            | boolean  | No        | Default: `false`                                                                                 |

### Response

**200 OK** — Returns a paginated response containing the matched account records.

```json
{
  "totalElements": 1523,
  "totalPages": 77,
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
      "name": "RUD Fleet",
      "accountType": "Prospect",
      "crmAccountId": "001ABC123",
      "city": "Miami",
      "state": "Florida",
      "country": "US",
      "isCustomer": false,
      "partnerFields": {
        "partneraccountname": "RUD Fleet",
        "partneraccounttype": "Prospect",
        "partnercrmaccountid": "MANUAL-26505afe-fdd8-4f0a-a2c5-a9a06dd5f3c3",
        "partnercountry": "US",
        "partnerzipcode": "33177",
        "partneriscustomer": false,
        "partnerisemployee": true,
        "partnerowner": " ",
        "partnerowneridname": "Anonymous",
        "partnerowneridemail": "Anonymous",
        "partnerowneridphone": "Anonymous",
        "partnerowneridtitle": "Anonymous",
        "partnertype": " ",
        "partnerregistrationdate": 1746706810,
        "partnerpartnereddate": 1694607610,
        "partnertargetorgsize": "Small Business 51 - 250",
        "partnerproduct": "",
        "partnersystemssold": 89022,
        "partnerisactive": "",
        "partnerispartnerpaid": false,
        "partnerorginternalid": 6
      }
    }
  ]
}
```

Each record in `content` represents an account that overlaps with the specified partner. Your own account fields appear at the top level of each record. Fields available depend on your partner organization's share settings and configured columns. Use the [Columns](#4-get-available-columns) endpoint to discover which fields are available.

> **Partner Fields:** All data shared by the partner is returned in the `partnerFields` object on each record. Every key inside `partnerFields` is prefixed with `partner` (e.g., `partneraccountname`, `partnercountry`, `partnersystemssold`). This includes both standard partner fields and any custom fields the partner has chosen to share. The fields that appear depend on the partner's share settings and available data.

### Example

```shell
curl -X POST \
  "https://reports.partnertap.com/v1/channelecosystem/records?page=0&size=20" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{
    "search": "",
    "filters": {},
    "mapByLocations": false,
    "channelReportType": "PARTNER_ORG_MATCHED_ACCOUNTS",
    "matchingType": "MUTUAL",
    "companyPartnerPublicId": "c1727859-692f-499e-8c2a-b1fa50aa1a65"
  }'
```

---

## 4. Get Available Columns

Retrieve the list of available columns for a report type. This helps you understand which fields will appear in the records response and which fields you can filter on. Columns fall into three categories:

- **Standard** — Built-in fields available on every report (e.g., Account Name, City, Country). These have `columnClassification: "STANDARD"` and `isPartnerData: false`.
- **Custom** — Fields imported from your CRM or spreadsheet uploads. These have `columnClassification: "CUSTOM_CRM_FIELD"` or `"CUSTOM_CRM_OBJECT"` and `isPartnerData: false`.
- **Partner Shared** — Fields shared by the partner organization. These have `isPartnerData: true` and their keys are prefixed with `partner` (e.g., `partneraccountname`, `partnersystemssold`). Partner shared columns have `source: null` and `columnClassification: null`. In the records response, these fields appear inside the `partnerFields` object on each record.

### Request

```
POST /v1/channelecosystem/columns
Content-Type: application/json
```

### Request Body

**For Partner Org Matched Accounts:**

```json
{
  "channelReportType": "PARTNER_ORG_MATCHED_ACCOUNTS",
  "matchingType": "MUTUAL",
  "companyPartnerPublicId": "<PARTNER_ORG_UUID>"
}
```

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `channelReportType`         | string   | Yes       | Report type — `"PARTNER_ORG_MATCHED_ACCOUNTS"` or `"PARTNER_ORG_CONNECTED_PARTNER_ORGS"` |
| `matchingType`              | string   | No        | Use `"MUTUAL"` for mutually connected orgs / matched accounts                            |
| `companyPartnerPublicId`    | string   | Conditional | Required when `channelReportType` is `"PARTNER_ORG_MATCHED_ACCOUNTS"`. The UUID of the partner org, obtained from the [Partner Organizations](#2-get-list-of-partner-organizations) response |

### Response

**200 OK** — Returns an array of column metadata objects.

**Standard column example:**

```json
{
  "title": "Account Name",
  "key": "name",
  "type": "string",
  "isFromOtherFields": false,
  "isJson": false,
  "isHidden": false,
  "otherFieldsPrefix": null,
  "otherFieldsJsonPrefix": null,
  "active": true,
  "values": {},
  "crmAccountBaseUri": null,
  "crmOpportunityBaseUri": null,
  "columnIndex": 0,
  "isPartnerData": false,
  "prefix": null,
  "color": null,
  "source": "standard",
  "columnClassification": "STANDARD"
}
```

**Partner shared custom column example:**

```json
{
  "title": "Partner Systems Sold",
  "key": "partnersystemssold",
  "type": "number",
  "isFromOtherFields": false,
  "isJson": false,
  "isHidden": false,
  "otherFieldsPrefix": null,
  "otherFieldsJsonPrefix": null,
  "active": true,
  "values": {},
  "crmAccountBaseUri": null,
  "crmOpportunityBaseUri": null,
  "columnIndex": 8,
  "isPartnerData": true,
  "prefix": null,
  "color": null,
  "source": null,
  "columnClassification": null
}
```

> **Note:** Partner shared columns always have `isPartnerData: true`, keys prefixed with `partner`, and `source` / `columnClassification` set to `null`. Standard and custom columns have `isPartnerData: false` with non-null `source` and `columnClassification` values.

| Field | Type | Description |
| --- | --- | --- |
| `title`                   | string        | Human-readable column name                                                                     |
| `key`                     | string        | The field key used in records, filters, and sorting. Partner columns are prefixed with `partner` |
| `type`                    | string        | Data type of the column (e.g., `string`, `number`, `currency`, `date`, `boolean`)               |
| `active`                  | boolean       | Whether the column is currently active/visible                                                  |
| `isPartnerData`           | boolean       | `true` for partner shared columns, `false` for your own standard/custom columns                 |
| `isHidden`                | boolean       | Whether the column is hidden by default                                                         |
| `columnIndex`             | integer       | Display order index                                                                             |
| `source`                  | string\|null  | Origin of the column (`"standard"`, `"custom"`, etc.). `null` for partner shared columns        |
| `columnClassification`    | string\|null  | `"STANDARD"`, `"CUSTOM_CRM_FIELD"`, or `"CUSTOM_CRM_OBJECT"`. `null` for partner shared columns |
| `isFromOtherFields`       | boolean       | Whether the column is derived from other fields                                                 |
| `isJson`                  | boolean       | Whether the column value is stored as JSON                                                      |
| `values`                  | object        | Preset value mappings for the column (typically empty `{}`)                                     |
| `crmAccountBaseUri`       | string\|null  | Base URI for linking to CRM account records (if applicable)                                     |
| `crmOpportunityBaseUri`   | string\|null  | Base URI for linking to CRM opportunity records (if applicable)                                 |

### Example

```shell
curl -X POST \
  "https://reports.partnertap.com/v1/channelecosystem/columns" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{
    "channelReportType": "PARTNER_ORG_MATCHED_ACCOUNTS",
    "matchingType": "MUTUAL",
    "companyPartnerPublicId": "c1727859-692f-499e-8c2a-b1fa50aa1a65"
  }'
```

---

## 5. Get Filter Values

Before building a filter, you can use the `/filterdata` endpoint to retrieve the available values for any column. This is a paginated endpoint — pass the column name as the `filterField` query parameter.

### Request

```
POST /v1/channelecosystem/filterdata?filterField={columnName}&page=0&size=20
Content-Type: application/json
```

### Query Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `filterField`  | string   | Yes       | The column name to retrieve filter values for          |
| `page`         | integer  | No        | Zero-based page index (default: 0)                    |
| `size`         | integer  | No        | Number of results per page (default: 20, max: 2000)   |

### Request Body

**For Partner Org Matched Accounts:**

```json
{
  "channelReportType": "PARTNER_ORG_MATCHED_ACCOUNTS",
  "matchingType": "MUTUAL",
  "mapByLocations": false,
  "companyPartnerPublicId": "<PARTNER_ORG_UUID>",
  "byOrg": false
}
```

**For All Partner Organizations:**

```json
{
  "channelReportType": "PARTNER_ORG_CONNECTED_PARTNER_ORGS",
  "matchingType": "ALL_PARTNER_ORGS",
  "mapByLocations": false,
  "byOrg": false
}
```

### Response

**200 OK** — For **string** columns, the response contains distinct values. For **numeric/date** columns, the response includes range bounds.

**String column response:**

```json
{
  "totalElements": 15,
  "totalPages": 1,
  "number": 0,
  "size": 20,
  "content": [
    {
      "filterData": "Customer",
      "filterRangeMin": null,
      "filterRangeMax": null,
      "filterType": "STRING"
    },
    {
      "filterData": "Prospect",
      "filterRangeMin": null,
      "filterRangeMax": null,
      "filterType": "STRING"
    }
  ]
}
```

**Numeric/currency column response:**

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

### Example

```shell
curl -X POST \
  "https://reports.partnertap.com/v1/channelecosystem/filterdata?filterField=accountType&page=0&size=20" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{
    "channelReportType": "PARTNER_ORG_MATCHED_ACCOUNTS",
    "matchingType": "MUTUAL",
    "mapByLocations": false,
    "companyPartnerPublicId": "c1727859-692f-499e-8c2a-b1fa50aa1a65",
    "byOrg": false
  }'
```

---

## 6. Filter Language

Filters are passed as key-value pairs in the `filters` object of the request body. The **key** is the column name (as returned by the `/columns` endpoint), and the **value** is a string that encodes the filter operation using special suffixes and delimiters.

### Filter Operations

| Operation | Suffix | Value Format | Description |
| --- | --- | --- | --- |
| Exact match       | _(none)_  | `value1-,-value2-,-value3`  | Matches rows where the field equals **any** of the values (OR logic).                     |
| Not equal         | `-!-`   | `value1-,-value2-!-`         | Excludes rows matching **any** of the values (AND logic). NULLs are preserved.             |
| Contains          | `-?-`   | `search1-,-search2-?-`       | Case-insensitive substring match. Row must contain **all** terms (AND logic).              |
| Does not contain  | `-^-`   | `exclude1-,-exclude2-^-`     | Case-insensitive substring exclusion. Row must not contain **any** of the terms (AND logic).  |
| Range             | `<->`   | `min<->max`                   | Matches rows where the field value falls between `min` and `max` (inclusive).              |

### Multi-Value Delimiter

Use `-,-` to separate multiple values within a single filter:

```
"accountType": "Customer-,-Prospect"
```

This matches rows where `accountType` is "Customer" **OR** "Prospect".

### Supported Operations by Column Type

| Column Type | Exact Match | Not Equal | Contains | Does Not Contain | Range |
| --- | --- | --- | --- | --- | --- |
| String              | Y            | Y          | Y         | Y                 |        |
| Boolean             | Y            |            |           |                   |        |
| UUID                | Y            | Y          | Y         | Y                 |        |
| Date                |              |            |           |                   | Y      |
| Number (int)        |              |            |           |                   | Y      |
| Currency / Double   |              |            |           |                   | Y      |

### Filter Value Syntax by Type

**String / UUID** — pass the display value as a string:

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
  "name": "Fox-?-"
}
```

```json
{
  "name": "Test-^-"
}
```

```json
{
  "state": "Oklahoma-,-Texas-!-"
}
```

**Boolean** — pass `"true"` or `"false"`:

```json
{
  "isCustomer": "true"
}
```

**Date** — pass epoch timestamps (seconds) as a range:

```json
{
  "recentOpenOppDate": "1700000000<->1760000000"
}
```

**Number / Currency** — pass numeric values as a range:

```json
{
  "openOppCount": "1<->10"
}
```

### Combining Multiple Filters

All filters in the `filters` object are combined with **AND** logic:

```json
{
  "filters": {
    "state": "Oklahoma",
    "accountType": "Customer",
    "name": "Fox-?-"
  }
}
```

This returns rows where state is "Oklahoma" **AND** account type is "Customer" **AND** account name contains "Fox".

### Example: Filtered Partner Org Report

```shell
curl -X POST \
  "https://reports.partnertap.com/v1/channelecosystem/records?page=0&size=20" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{
    "search": "",
    "filters": {
      "accountType": "Customer",
      "state": "Oklahoma-,-Texas"
    },
    "mapByLocations": false,
    "channelReportType": "PARTNER_ORG_MATCHED_ACCOUNTS",
    "matchingType": "MUTUAL",
    "companyPartnerPublicId": "c1727859-692f-499e-8c2a-b1fa50aa1a65"
  }'
```

---

## 7. Typical Workflow

Here is the recommended step-by-step workflow for consuming the Partner Org report:

### Step 1: Get your list of partner organizations

```shell
curl -X POST \
  "https://reports.partnertap.com/v1/channelecosystem/records?page=0&size=100" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{
    "channelReportType": "PARTNER_ORG_CONNECTED_PARTNER_ORGS",
    "matchingType": "MUTUAL"
  }'
```

From the response, identify the partner you want and note its `companyPartnerPublicId`.

### Step 2: (Optional) Discover available columns

```shell
curl -X POST \
  "https://reports.partnertap.com/v1/channelecosystem/columns" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{
    "channelReportType": "PARTNER_ORG_MATCHED_ACCOUNTS",
    "matchingType": "MUTUAL",
    "companyPartnerPublicId": "<PARTNER_ORG_UUID>"
  }'
```

### Step 3: (Optional) Discover filter values for a column

```shell
curl -X POST \
  "https://reports.partnertap.com/v1/channelecosystem/filterdata?filterField=accountType" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{
    "channelReportType": "PARTNER_ORG_MATCHED_ACCOUNTS",
    "matchingType": "MUTUAL",
    "companyPartnerPublicId": "<PARTNER_ORG_UUID>",
    "byOrg": false
  }'
```

### Step 4: Retrieve the Partner Org Matched Accounts report

```shell
curl -X POST \
  "https://reports.partnertap.com/v1/channelecosystem/records?page=0&size=100" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{
    "channelReportType": "PARTNER_ORG_MATCHED_ACCOUNTS",
    "matchingType": "MUTUAL",
    "companyPartnerPublicId": "<PARTNER_ORG_UUID>",
    "filters": {
      "accountType": "Customer"
    }
  }'
```

### Step 5: Page through all results

Increment the `page` parameter to retrieve subsequent pages until `last` is `true` in the response:

```shell
# Page 2
curl -X POST \
  "https://reports.partnertap.com/v1/channelecosystem/records?page=1&size=100" \
  -H "Content-Type: application/json" \
  -H "api-key: <YOUR_API_KEY>" \
  -d '{
    "channelReportType": "PARTNER_ORG_MATCHED_ACCOUNTS",
    "matchingType": "MUTUAL",
    "companyPartnerPublicId": "<PARTNER_ORG_UUID>"
  }'
```

---

## Other Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/v1/channelecosystem/records`               | POST    | Get paginated report records                    |
| `/v1/channelecosystem/columns`               | POST    | Get available columns for a report type         |
| `/v1/channelecosystem/filterdata`            | POST    | Get filter values for a specific column         |
| `/v1/channelecosystem/report-names`          | GET     | List available report types with their columns  |

---

## Appendix A: Partner Organizations Fields

These are the standard fields returned by the `PARTNER_ORG_CONNECTED_PARTNER_ORGS` report. Use the `key` value when filtering or sorting.

| Key | Display Name | Type |
| --- | --- | --- |
| `partnerName`                 | Partner Org                     | name      |
| `partnerWebsite`              | Partner Website                 | string    |
| `companyPartnerPublicId`      | PT Partner Org Id               | string    |
| `partnerType`                 | Partner Type                    | string    |
| `recommended`                 | Recommended Partner             | boolean   |
| `firstConnectedDate`          | First Connected Date            | date      |
| `mostRecentConnectedDate`     | Most Recent Connected Date      | date      |
| `activeConnections`           | Active Connections              | number    |
| `lastPartnerSheetUploadDate`  | Last Partner Sheet Upload Date  | date      |
| `spreadsheetsShared`          | Spreadsheets Uploaded           | number    |
| `partnerOwner`                | Partner Manager                 | name      |
| `partnerOwnerEmail`           | Partner Manager Email           | email     |
| `partnerOwnerPhone`           | Partner Manager Phone           | string    |

---

## Appendix B: Partner Org Matched Accounts Fields

These are the standard fields returned by the `PARTNER_ORG_MATCHED_ACCOUNTS` report. If you have custom CRM fields, they will also appear in the response. Use the `key` value when filtering or sorting.

| Key | Display Name | Type |
| --- | --- | --- |
| `accountName`              | Account Name             | string    |
| `dunsNumber`               | DUNS Number              | string    |
| `companyPartnerPublicId`   | Company Partner Public Id  | string  |
| `companyPartnerName`       | Partner Org              | name      |
| `crmRecordId`              | CRM Record Id            | string    |
| `prmRecordId`              | PRM Record Id            | string    |
| `partnerType`              | Partner Type             | string    |
| `avgDealSize`              | Average Deal Size        | currency  |
| `partnerOwner`             | Partner Manager          | name      |
| `accountType`              | Account Type             | string    |
| `city`                     | City                     | string    |
| `country`                  | Country                  | string    |
| `crmAccountId`             | Account Id               | string    |
| `parent_account_id`        | Parent Account Id        | string    |
| `divisions`                | Divisions                | string    |
| `industry`                 | Industry                 | string    |
| `isCustomer`               | Is Customer              | boolean   |
| `numberOfEmployees`        | Employees                | number    |
| `naicsCode`                | NAICS                    | string    |
| `ncesId`                   | NCES ID                  | string    |
| `sicCode`                  | SIC                      | string    |
| `annualRevenue`            | Annual Revenue           | currency  |
| `openOppCount`             | Open Opps                | number    |
| `closedOppCount`           | Closed Opps              | number    |
| `state`                    | State                    | string    |
| `street`                   | Street                   | string    |
| `territory`                | Territory                | string    |
| `website`                  | Website                  | string    |
| `zipCode`                  | Zip Code                 | string    |

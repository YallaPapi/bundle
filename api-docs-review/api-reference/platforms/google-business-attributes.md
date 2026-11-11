> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Google Business Attributes

> Read location attributes, list attribute definitions for the category, and update structured facts on the profile.

**Attributes** are structured facts Google shows on the profile (for example payments, accessibility, services). Valid attribute IDs and value types depend on **primary category** and region. The same attribute payload can work for one location and fail for another.

Use this order for reliable updates:

1. **List available** to discover allowed definitions for the selected location.
2. **Get current attributes** to inspect current value shapes.
3. **Patch** only supported names and values.

**Base path:** `/api/v1/misc/google-business`

***

## Get current attributes

**Endpoint:** `GET /api/v1/misc/google-business/location/attributes`

| Query | Required | Description |
| :- | :- | :- |
| `teamId` | Yes | Team with selected Google Business location. |

Response includes `attributes`: an array of objects. Each item has a `name` (for example `attributes/pay_credit_card`) and a value field whose shape depends on the attribute **type**.

***

## Value types (response and request)

| Kind | JSON shape | Notes |
| :- | :- | :- |
| Boolean | `"values": [true]` or `"values": [false]` | Google uses a one-element array for booleans. |
| Enum (multi) | `"repeatedEnumValue": { "setValues": ["TOKEN", ...] }` | Allowed tokens come from **list available** for that attribute. |
| URL list | `"uriValues": [{ "uri": "https://..." }]` | When the attribute stores links. |

Always confirm the expected shape for a given `name` via **list available** or **get** before you build your UI. Do not assume that every boolean/enum/url-style field is valid for every category.

***

## List available attribute definitions

**Endpoint:** `GET /api/v1/misc/google-business/location/attributes/available`

Use this to build dropdowns or validation in your product. Google returns definitions for attributes applicable to the location.

| Query | Required | Description |
| :- | :- | :- |
| `teamId` | Yes | Team identifier. |
| `languageCode` | No | BCP-47 language for labels (for example `en`). |
| `regionCode` | No | CLDR region (for example `US`). |
| `pageSize` | No | Integer 1 to 200. |
| `pageToken` | No | Pagination token from a previous response. |

Response includes `attributes` (definition objects) and optional `nextPageToken`.

### Google-side selection context

Google's attribute catalog is context-sensitive. Availability depends on location/category/region, and can change over time.

* In Google APIs, attribute metadata is selected using location/category and localization context.
* In this API, `teamId` selects the connected location context, while optional `languageCode` and `regionCode` help localize/filter definitions.
* Treat this endpoint as the source of truth for what can be patched now.

***

## Update attributes

**Endpoint:** `PATCH /api/v1/misc/google-business/location/attributes`

### Body

| Field | Required | Description |
| :- | :- | :- |
| `teamId` | Yes | Team identifier. |
| `attributes` | Optional | Array of attribute objects in the **update payload**. Each item includes `name` (`attributes/...`) and the value fields for that attribute type (`values`, `repeatedEnumValue`, `uriValues`, etc.). |
| `attributeMask` | Optional | Comma-separated list of attribute paths, aligned with what you send in `attributes`. If omitted, the API can derive it from `attributes[].name` as `attributes/{id}` joined with commas. You must end up with at least one attribute path (explicit or derived) in the request. |

### Example: many boolean attributes (sample ids)

The following **update payload** shows real-style `attributes/...` ids and boolean `values` arrays. Replace `teamId` with your team. Only use attribute ids that **list available** or **get** returns for your location (ids differ by category and region).

```json theme={null}
{
  "teamId": "00000000-0000-4000-8000-000000000001",
  "attributeMask": "attributes/pay_credit_card,attributes/pay_debit_card,attributes/is_owned_by_women,attributes/requires_cash_only,attributes/has_onsite_services,attributes/has_in_store_pickup,attributes/has_parking_street_free,attributes/buys_goods_used,attributes/has_recycling_electronics,attributes/has_delivery,attributes/has_in_store_shopping",
  "attributes": [
    { "name": "attributes/pay_credit_card", "values": [true] },
    { "name": "attributes/pay_debit_card", "values": [true] },
    { "name": "attributes/is_owned_by_women", "values": [false] },
    { "name": "attributes/requires_cash_only", "values": [false] },
    { "name": "attributes/has_onsite_services", "values": [false] },
    { "name": "attributes/has_in_store_pickup", "values": [true] },
    { "name": "attributes/has_parking_street_free", "values": [true] },
    { "name": "attributes/buys_goods_used", "values": [true] },
    { "name": "attributes/has_recycling_electronics", "values": [true] },
    { "name": "attributes/has_delivery", "values": [true] },
    { "name": "attributes/has_in_store_shopping", "values": [false] }
  ]
}
```

### Example: enum-style attribute

```json theme={null}
{
  "teamId": "00000000-0000-4000-8000-000000000001",
  "attributes": [
    {
      "name": "attributes/ATTRIBUTE_ID_FROM_LIST_OR_GET",
      "repeatedEnumValue": {
        "setValues": ["ALLOWED_ENUM_TOKEN"]
      }
    }
  ]
}
```

Exact `name` strings and allowed enum tokens come from **list available** and Google's attribute catalog for that category.

***

## Related

* [Location & profile](/api-reference/platforms/google-business-location) for core profile fields outside attributes.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Google Business Location & profile

> Read and update Business Profile location data: title, categories, address, phone, hours-related fields in one profile patch, and more.

These endpoints read or update the **Google Business Profile location** resource for the team's selected location. They map to Google's Business Information API. You need a connected Google Business account with a **location already selected** (same rule as posts).

**Base path:** `/api/v1/misc/google-business`

All requests use your usual API key authentication.

***

## Get location

**Endpoint:** `GET /api/v1/misc/google-business/location`

### Query

| Parameter | Required | Description |
| :- | :- | :- |
| `teamId` | Yes | Team that owns the connected Google Business social account. |
| `fields` | No | Subset of location fields to return. If omitted, a **default profile-oriented field list** is used (name, title, profile, website, phones, categories, hours fields, address, service area, coordinates, open info, metadata). |

`fields` accepts **comma-separated** values or **repeated** query params, for example `fields=name,title` or `fields=name&fields=title`.

Allowed `fields` values (Google read field paths):

`name`, `languageCode`, `storeCode`, `title`, `phoneNumbers`, `categories`, `storefrontAddress`, `websiteUri`, `regularHours`, `specialHours`, `serviceArea`, `labels`, `adWordsLocationExtensions`, `latlng`, `openInfo`, `metadata`, `profile`, `relationshipData`, `moreHours`, `serviceItems`

The response shape follows Google's API (we pass through the payload). Use it to drive your own UI or to read state before a patch.

***

## Update location

**Endpoint:** `PATCH /api/v1/misc/google-business/location`

Only the top-level keys you include in the **update payload** are sent to Google. Only the fields listed below participate. Send **at least one** patchable field.
The API automatically determines which provided fields should be updated.

### Patchable fields

| Field | Purpose |
| :- | :- |
| `title` | Display name (max 255 characters). Use `null` to clear where Google allows. |
| `profile` | Object with `description` (max 1500 characters) and other Google-supported keys. |
| `websiteUri` | Public website URL. |
| `phoneNumbers` | `primaryPhone`, `additionalPhones[]`. |
| `categories` | `primaryCategory.name`, `additionalCategories[].name` (Google category resource names). |
| `storefrontAddress` | Structured address (`regionCode`, `postalCode`, `locality`, `addressLines`, etc.). |
| `regularHours` | Standard weekly hours (`periods` with open/close days and times). |
| `specialHours` | Exceptions (`specialHourPeriods` with dates and closed flag). |
| `moreHours` | Named hour sets (for example department-specific hours); each item can include `hoursTypeId` and `periods`. |
| `openInfo` | Opening status metadata (Google's schema). |
| `serviceArea` | Service-area business definition (Google's schema). |
| `latlng` | `latitude` and `longitude`. |

### Other body keys

| Field | Description |
| :- | :- |
| `validateOnly` | If `true`, Google validates the request without applying the change. |

### Useful metadata for feature eligibility

Google location metadata can indicate whether certain feature families are available for this location. In particular:

* `metadata.canModifyServiceList` controls service-list edit eligibility.
* `metadata.canHaveFoodMenus` controls food-menu eligibility.

Read `metadata` through `GET /location` before enabling related editing UI.

### Find Available Categories

Use `GET /api/v1/misc/google-business/location/categories/available` to resolve Google category resource names before updating `categories`.

| Query | Required | Description |
| :- | :- | :- |
| `teamId` | Yes | Team with the connected Google Business location. |
| `regionCode` | Yes | Two-letter region code, for example `US` or `PL`. |
| `languageCode` | Yes | Label language, for example `en` or `pl`. |
| `names` | No | One to 100 exact category resource names. Accepts repeated or comma-separated values and uses Google's batch lookup. |
| `filter` | No | Category display-name prefix filter used when `names` is omitted. |
| `pageSize` | No | Fixed at `50`. |
| `pageToken` | No | Token from the previous page. |
| `view` | No | `BASIC` by default; `FULL` requests the expanded category view. |

Use either exact `names` or discovery through `filter`, then send the returned category `name` as `primaryCategory.name` or inside `additionalCategories`.

### Example: title, description, and hours (anonymized)

Single **update payload** with profile copy plus weekly hours, holiday exceptions, and an extra hour type (`moreHours`). `teamId` and business copy below are placeholders.

```json theme={null}
{
  "teamId": "00000000-0000-4000-8000-000000000001",
  "title": "Example Shop - Used CDs",
  "profile": {
    "description": "Second-hand CD store for collectors. Rock, pop, jazz, and soundtracks. Each disc is checked for condition before sale."
  },
  "regularHours": {
    "periods": [
      {
        "openDay": "MONDAY",
        "openTime": "10:00",
        "closeDay": "MONDAY",
        "closeTime": "18:00"
      },
      {
        "openDay": "TUESDAY",
        "openTime": "10:00",
        "closeDay": "TUESDAY",
        "closeTime": "18:00"
      },
      {
        "openDay": "WEDNESDAY",
        "openTime": "10:00",
        "closeDay": "WEDNESDAY",
        "closeTime": "18:00"
      },
      {
        "openDay": "THURSDAY",
        "openTime": "10:00",
        "closeDay": "THURSDAY",
        "closeTime": "18:00"
      },
      {
        "openDay": "FRIDAY",
        "openTime": "10:00",
        "closeDay": "FRIDAY",
        "closeTime": "18:00"
      },
      {
        "openDay": "SATURDAY",
        "openTime": "10:00",
        "closeDay": "SATURDAY",
        "closeTime": "15:00"
      }
    ]
  },
  "specialHours": {
    "specialHourPeriods": [
      {
        "startDate": { "year": 2026, "month": 12, "day": 24 },
        "endDate": { "year": 2026, "month": 12, "day": 24 },
        "openTime": "10:00",
        "closeTime": "14:00",
        "closed": false
      },
      {
        "startDate": { "year": 2026, "month": 12, "day": 25 },
        "endDate": { "year": 2026, "month": 12, "day": 25 },
        "closed": true
      }
    ]
  },
  "moreHours": [
    {
      "hoursTypeId": "PICKUP",
      "periods": [
        {
          "openDay": "MONDAY",
          "openTime": "10:00",
          "closeDay": "MONDAY",
          "closeTime": "18:00"
        },
        {
          "openDay": "TUESDAY",
          "openTime": "10:00",
          "closeDay": "TUESDAY",
          "closeTime": "18:00"
        },
        {
          "openDay": "WEDNESDAY",
          "openTime": "10:00",
          "closeDay": "WEDNESDAY",
          "closeTime": "18:00"
        },
        {
          "openDay": "THURSDAY",
          "openTime": "10:00",
          "closeDay": "THURSDAY",
          "closeTime": "18:00"
        },
        {
          "openDay": "FRIDAY",
          "openTime": "10:00",
          "closeDay": "FRIDAY",
          "closeTime": "18:00"
        },
        {
          "openDay": "SATURDAY",
          "openTime": "10:00",
          "closeDay": "SATURDAY",
          "closeTime": "15:00"
        }
      ]
    }
  ]
}
```

### Smaller payloads

You can send partial **update payloads**, for example only `title` and `websiteUri`, or only `profile`.

### Hours only

You may include `regularHours`, `specialHours`, or `moreHours` in this endpoint, or use the dedicated [Hours](/api-reference/platforms/google-business-hours) endpoint when you only change hours and want an explicit `fields` list for hour sections.

***

## Related

* [Google Business Hours](/api-reference/platforms/google-business-hours) for updates that only touch `regularHours`, `specialHours`, or `moreHours` with an explicit `fields` list.
* [Google Business main guide](/api-reference/platforms/google-business) for posts and analytics.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
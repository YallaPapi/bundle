> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Google Business Hours

> Update regular, special, and more hours for a Google Business Profile location with explicit field selection.

Use this endpoint when you only need to change **opening hours** (regular weekly hours, special dates, or additional hour types). It updates the same Google location resource as [Location & profile](/api-reference/platforms/google-business-location), but requires an explicit `fields` array so the API knows which hour sections are part of your **update payload**.

**Endpoint:** `PATCH /api/v1/misc/google-business/location/hours`

**Base path:** `/api/v1/misc/google-business`

***

## Body rules

| Field | Required | Description |
| :- | :- | :- |
| `teamId` | Yes | Team with a connected Google Business location. |
| `fields` | Yes | Which hour sections this **update payload** applies to. Each value must be one of: `regularHours`, `specialHours`, `moreHours`. You can pass one or more (comma-separated or repeated style, same as other query lists in this API). |
| `regularHours` | Optional | Weekly schedule. Omit if not in `fields`. |
| `specialHours` | Optional | Date-specific overrides. Omit if not in `fields`. |
| `moreHours` | Optional | Array of extra hour groups (for example pickup). Omit if not in `fields`. |
| `validateOnly` | Optional | If `true`, validation only, no persist. |

You must include **at least one** hour block that matches `fields`. The server forwards the **update payload** to Google.

***

## Time and day shapes

**Weekdays** for `openDay` / `closeDay` in periods:

`MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY`, `SATURDAY`, `SUNDAY`

**Time** can be sent as:

* A string like `"09:00"` or `"09:00:00"` (normalized to Google's time-of-day object where supported), or
* An object: `hours`, `minutes`, optional `seconds`, optional `nanos`.

**Special hours** periods may include `startDate` / `endDate` with `year`, `month`, `day`, plus `openTime`, `closeTime`, and `closed: true` when the location is closed all day.

***

## Example: full hours update payload (anonymized)

`teamId` is a placeholder. Structure matches a real multi-section hours **update payload**: regular week, holiday exceptions, and `moreHours` with a type id (use values Google returns for your location for `hoursTypeId`).

```json theme={null}
{
  "teamId": "00000000-0000-4000-8000-000000000001",
  "fields": ["regularHours", "specialHours", "moreHours"],
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

***

## Related

* [Location & profile](/api-reference/platforms/google-business-location) if you also change non-hour fields in one call.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
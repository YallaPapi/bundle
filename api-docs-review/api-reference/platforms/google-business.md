> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Google Business

> Local SEO posts, events, offers, and updates for your business profile.

Google Business Profile (formerly Google My Business) lets you post updates that appear in Google Search and Maps. It's not social media in the traditional sense, but it's great for local businesses.

## Location, profile, and Maps data

Besides posts, you can read and update **Business Profile** data for the team's selected location (hours, attributes, services, food menus, action links, profile media). These use `/api/v1/misc/google-business` with the same API key as the rest of the public API.

* [Location & profile](/api-reference/platforms/google-business-location) (GET/PATCH location fields and read field selection)
* [Hours](/api-reference/platforms/google-business-hours) (regular, special, more hours)
* [Attributes](/api-reference/platforms/google-business-attributes)
* [Service list](/api-reference/platforms/google-business-service-list)
* [Food menus](/api-reference/platforms/google-business-food-menus)
* [Place action links](/api-reference/platforms/google-business-place-action-links)
* [Profile media](/api-reference/platforms/google-business-profile-media)

Reviews stay on a separate flow: [Google Business Reviews](/api-reference/platforms/google-business-reviews).

## Feature availability by category and location

Google Business capabilities are not identical for every profile. Some fields or endpoints can be unavailable depending on category, country/region, and location-level eligibility.

* **Attributes** differ by category and region. Build updates from available definitions first.
* **Service list** is only available for eligible categories/locations.
* **Food menus** are available mostly for restaurant-like categories and can be disabled for a specific location.
* **Place action links** and allowed `placeActionType` values can vary by profile setup and category.
* **Profile media** categories and moderation behavior can vary by profile type.

Recommended flow for most integrations: **GET/list first**, then send **PATCH/POST** with values confirmed by Google for that exact location.

## Supported Content Types

* **Standard Posts:** Regular text updates with optional image.
* **Events:** Time-bound events with a title and date range.
* **Offers:** Promotional offers with coupon codes and terms.
* **Alerts:** Special alerts (currently only `COVID_19`).
* **Reviews & Replies:** Import reviews asynchronously, then manage owner replies.

## Quirks & Gotchas

### Location Selection Required

After connecting your Google account, you must select a business location. This is similar to selecting a Facebook Page or LinkedIn Company Page.

### Post Types

Google Business supports different post types via the `topicType` field:

* `STANDARD`: Regular updates (default).
* `EVENT`: Time-bound events with a title and date range.
* `OFFER`: Promotional offers with coupon codes and terms.
* `ALERT`: Special alerts (currently only `COVID_19`).

### Call to Action

You can add a CTA button to `STANDARD` and `EVENT` posts (not `OFFER` or `ALERT`):

* `BOOK`, `ORDER`, `SHOP`, `LEARN_MORE`, `SIGN_UP`, `CALL`
* Requires a `callToActionUrl` for every type except `CALL`.

### Media Limits

| Constraint | Value |
| :- | :- |
| Files | 0-1 image only (no video) |
| Image max size | 5 MB |
| Image min resolution | 250x250 |
| Text | Max 1,500 characters |

See [Platform Limits](/api-reference/limits#google-business) for details.

### Text & Field Limits

| Field | Limit |
| :- | :- |
| `text` | Max 1,500 characters |
| `eventTitle` | Max 58 characters |
| `offerCouponCode` | Max 58 characters |
| `offerTermsConditions` | Max 1,500 characters |

***

## Google Reviews

Google Reviews run on a separate async flow (similar to Post History Import). You start an import job, poll status, then fetch imported reviews and manage replies.

* Start import + poll status (`PENDING` -> `FETCHING_REVIEWS` -> `COMPLETED`)
* Handle temporary pauses with `RATE_LIMITED` and automatic resume
* List imported reviews with pagination and capacity info
* Create/update/delete owner replies via API

Full guide: [Google Business Reviews](/api-reference/platforms/google-business-reviews)

***

## Post Options

| Field | Type | Description |
| :- | :- | :- |
| `text` | `string` | Post content. Max 1,500 characters. |
| `uploadIds` | `string[]` | Media attachments (images only). |
| `topicType` | `enum` | Post type: `STANDARD`, `EVENT`, `OFFER`, `ALERT`. Default: `STANDARD`. |
| `languageCode` | `string` | Language code (e.g., `en`, `en-US`). Default: `en`. |
| `callToActionType` | `enum` | CTA button: `BOOK`, `ORDER`, `SHOP`, `LEARN_MORE`, `SIGN_UP`, `CALL`. |
| `callToActionUrl` | `string` | URL for the CTA button. |
| `alertType` | `enum` | Alert type for `ALERT` posts. Currently only `COVID_19`. |

### Event-Specific Fields

| Field | Type | Description |
| :- | :- | :- |
| `eventTitle` | `string` | Event title. Max 58 characters. |
| `eventStartDate` | `date` | Event start date. |
| `eventEndDate` | `date` | Event end date. |

### Offer-Specific Fields

| Field | Type | Description |
| :- | :- | :- |
| `offerCouponCode` | `string` | Coupon code. Max 58 characters. |
| `offerRedeemOnlineUrl` | `string` | URL to redeem the offer online. |
| `offerTermsConditions` | `string` | Terms and conditions. Max 1,500 characters. |

<Note>
  An `OFFER` post needs `eventStartDate` (optionally `eventEndDate`) and at least one of `offerCouponCode`, `offerRedeemOnlineUrl` or `offerTermsConditions`. Offers can't have a button: `callToActionType` is rejected.
</Note>

***

## Analytics

For general analytics concepts (refresh rates, data retention, what "Returns 0" means), see the [Analytics Overview](/api-reference/analytics).

Google Business provides basic analytics for your business location. Don't expect Instagram-level data here.

### Profile Analytics

**Period:** Rolling 30-day window.

| Metric | Description | Note |
| :- | :- | :- |
| `impressions` | Total Business Profile impressions | Sum of desktop/mobile Search and Maps impressions |
| `impressionsUnique` | - | Returns `0` (not provided by Google Business Profile API) |
| `views` | - | Returns `0` in the standard response |
| `viewsUnique` | - | Returns `0` (not provided by Google Business Profile API) |
| `likes` | - | Returns `0` (not applicable) |
| `comments` | - | Returns `0` (not applicable) |
| `postCount` | - | Returns `0` |
| `followers` | - | Returns `0` (not applicable) |
| `following` | - | Returns `0` (not applicable) |

The raw analytics response also includes a summary with `websiteClicks`, `callClicks`, `directionRequests`, and `conversations`.

### Post Analytics

Google Business post analytics are **not currently returned** through our API. The standard post analytics endpoint returns no Google Business post rows, and raw post analytics are not available for Google Business.

Use profile/location raw analytics when you need Google Business performance data.

### Raw Analytics

Google Business currently exposes profile/location raw analytics, not individual post raw analytics.

```json theme={null}
{
  "locationInfo": {
    "name": "locations/1234567890",
    "title": "Example Shop",
    "metadata": {
      "mapsUri": "https://maps.google.com/..."
    }
  },
  "dailyMetrics": {
    "multiDailyMetricTimeSeries": [
      {
        "dailyMetricTimeSeries": [
          {
            "dailyMetric": "BUSINESS_IMPRESSIONS_DESKTOP_SEARCH",
            "timeSeries": {
              "points": [
                { "date": { "year": 2026, "month": 4, "day": 26 }, "value": "420" }
              ]
            }
          }
        ]
      }
    ]
  },
  "summary": {
    "impressionsTotal": 12420,
    "websiteClicks": 182,
    "callClicks": 31,
    "directionRequests": 77,
    "conversations": 9
  },
  "range": {
    "start": "2026-03-28",
    "end": "2026-04-27"
  }
}
```

***

## Examples

### Standard Post

```javascript theme={null}
await bundle.post.create({
  teamId: "team_123",
  title: "Holiday hours",
  status: "SCHEDULED",
  postDate: "2026-06-01T15:00:00.000Z",
  socialAccountTypes: ["GOOGLE_BUSINESS"],
  data: {
    GOOGLE_BUSINESS: {
      text: "We're open for the holidays! Visit us today.",
      callToActionType: "LEARN_MORE",
      callToActionUrl: "https://example.com/holiday-hours"
    }
  }
});
```

### Event Post

```javascript theme={null}
await bundle.post.create({
  teamId: "team_123",
  title: "Grand opening",
  status: "SCHEDULED",
  postDate: "2026-06-01T15:00:00.000Z",
  socialAccountTypes: ["GOOGLE_BUSINESS"],
  data: {
    GOOGLE_BUSINESS: {
      topicType: "EVENT",
      text: "Join us for our grand opening celebration!",
      eventTitle: "Grand Opening",
      eventStartDate: "2026-02-01T10:00:00Z",
      eventEndDate: "2026-02-01T18:00:00Z",
      callToActionType: "BOOK",
      callToActionUrl: "https://example.com/rsvp"
    }
  }
});
```

### Offer Post

```javascript theme={null}
await bundle.post.create({
  teamId: "team_123",
  title: "Welcome offer",
  status: "SCHEDULED",
  postDate: "2026-06-01T15:00:00.000Z",
  socialAccountTypes: ["GOOGLE_BUSINESS"],
  data: {
    GOOGLE_BUSINESS: {
      topicType: "OFFER",
      text: "Get 20% off your first order!",
      eventStartDate: "2026-06-01T00:00:00.000Z",
      eventEndDate: "2026-06-30T23:59:59.000Z",
      offerCouponCode: "WELCOME20",
      offerRedeemOnlineUrl: "https://example.com/shop",
      offerTermsConditions: "Valid for new customers only. Expires Feb 28, 2026."
    }
  }
});
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
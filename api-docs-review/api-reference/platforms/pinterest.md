> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Pinterest

> Pins, Boards, and a mixed bag of analytics periods. Every post needs a boardName, and saves matter more than likes on a discovery platform.

Pinterest is about discovery, not just a feed. People come here to find ideas and save them for later. The API reflects this - "saves" are the key metric, not likes.

## Supported Content Types

* **Pins:** 1 image or 1 video. That's it - one file per pin.

## Quirks & Gotchas

### Board Name is Required

You can't pin to thin air. Every Pinterest post needs `boardName`. Use a board from `socialAccount.channels`.

### Terminology

* **Likes** are often referred to as **Saves** or **Reactions** depending on context. We normalize them in our schema.
* **Video Pins:** Only video pins have true "View" counts. Static image pins just show impressions in the views field.

### Media Limits

| Constraint | Value |
| :- | :- |
| Files | 1 (image or video, required) |
| Video max size | 2 GB |
| Video aspect ratio | 1:2 to 1.91:1 |
| Video duration | 4s - 15 min |
| Image max size | 5 MB |

See [Platform Limits](/api-reference/limits#pinterest) for more details.

### Text & Field Limits

| Field | Limit |
| :- | :- |
| `text` | Max 100 characters |
| `description` | Max 800 characters |
| `link` | Max 2,048 characters |
| `altText` | Max 500 characters |
| `note` | Max 500 characters |
| `boardName` | Required. Use a board name from `socialAccount.channels`. |

***

## Post Options

| Field | Type | Description |
| :- | :- | :- |
| `boardName` | `string` | **Required.** Board name from `socialAccount.channels`. |
| `text` | `string` | Pin title. Max 100 characters. |
| `description` | `string` | Pin description. Max 800 characters. |
| `uploadIds` | `string[]` | One image or video upload. |
| `thumbnail` | `string` | URL to an uploaded thumbnail image. |
| `link` | `string` | Destination URL. Max 2,048 characters. |
| `altText` | `string` | Image alt text. Max 500 characters. |
| `note` | `string` | Private note. Max 500 characters. |
| `dominantColor` | `string` | Hex color used while the image loads. |

```json theme={null}
{
  "teamId": "team_123",
  "title": "Pinterest spring collection",
  "status": "SCHEDULED",
  "postDate": "2026-06-01T15:00:00.000Z",
  "socialAccountTypes": ["PINTEREST"],
  "data": {
    "PINTEREST": {
      "boardName": "Product ideas",
      "text": "New spring collection",
      "description": "A clean, bright look for small teams",
      "uploadIds": ["upl_img_1"],
      "link": "https://example.com/spring"
    }
  }
}
```

***

## Analytics

For general analytics concepts (refresh rates, data retention, what "Returns 0" means), see the [Analytics Overview](/api-reference/analytics).

### Profile Analytics

**Period:** Rolling window (30 days). Aggregated across all pin analytics.

| Metric | Description | Note |
| :- | :- | :- |
| `impressions` | Total impressions | |
| `impressionsUnique` | - | Same as impressions (Pinterest doesn't distinguish) |
| `views` | Video views | Defaults to impressions if no video pins |
| `viewsUnique` | - | Same as views |
| `likes` | Saves | |
| `comments` | - | Returns `0` (not provided at profile level) |
| `postCount` | Total pins | |
| `followers` | Followers | |
| `following` | Following | |

### Post Analytics

**Period:** Mixed (30-day rolling window for views/impressions, Lifetime for engagement).

| Metric | Description | Note |
| :- | :- | :- |
| `impressions` | Impressions | 30-day window |
| `impressionsUnique` | - | Same as impressions |
| `views` | Video views | 30-day window; defaults to impressions for static pins |
| `viewsUnique` | - | Same as views |
| `likes` | Total reactions | Lifetime |
| `comments` | Total comments | Lifetime |
| `shares` | - | Returns `0` (not tracked by Pinterest) |
| `saves` | Saves | 30-day window |

### Quirks

* Views are only meaningful for video pins. Static pins show impressions in the views field as a fallback.
* Profile-level comments are not available through the Pinterest API.
* Shares are not a concept Pinterest tracks.
* Post analytics use a mixed approach: some metrics are rolling window, others are lifetime. It's confusing, but it's what Pinterest gives us.

### Raw Analytics

Pinterest profile raw analytics include the user analytics payload, follower list, and following list we used to build the standard numbers.

```json theme={null}
{
  "analytics": {
    "summary_metrics": {
      "IMPRESSION": 54000,
      "SAVE": 820,
      "VIDEO_START": 9100
    }
  },
  "followers": {
    "items": [{ "username": "follower_1" }]
  },
  "following": {
    "items": [{ "username": "brand_1" }]
  }
}
```

Pinterest post raw analytics store the Pin analytics response for the requested date range.

```json theme={null}
{
  "externalId": "1234567890",
  "summary_metrics": {
    "IMPRESSION": 6400,
    "SAVE": 94,
    "PIN_CLICK": 220,
    "OUTBOUND_CLICK": 58,
    "VIDEO_START": 0
  }
}
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
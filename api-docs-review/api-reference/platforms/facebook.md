> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Facebook

> Pages, Reels, Stories, and the eternal struggle with token expiration.

The OG social network. It works, but it carries a lot of legacy baggage. And rate limits. So many rate limits.

## Supported Content Types

* **Page Posts:** Text, Link, Image, Video. 0-10 files.
* **Reels:** Vertical video for Pages. 1 video.
* **Stories:** Image or video. 1 file.
* **Page Reviews:** Import and reply to Facebook Page reviews through a separate async flow.

## Page Reviews

Facebook Page Reviews run on a separate async flow. You start an import job, poll status, then fetch imported reviews and reply where Facebook allows it.

Full guide: [Facebook Page Reviews](/api-reference/platforms/facebook-page-reviews)

## Quirks & Gotchas

### Page Tokens Expire (Important!)

Facebook Page Access Tokens typically expire after **60 days**.

<Note>
  **This is not a bug, it's a feature.** If a user changes their password or security settings, the token dies immediately. You need to build your app to handle re-connection flows gracefully. We handle automatic refreshing where possible, but we can't perform miracles. If the token dies, the user needs to reconnect.
</Note>

### Reels Limitations

Facebook Reels via API are stricter than mobile uploads:

* No "Remix" functionality available via API.
* Duration: **3 seconds to 20 minutes** (1200s). Stories remain limited to 60 seconds.
* Minimum resolution: 540x960.

Standard Page video posts also accept videos up to **20 minutes**.

### Media Limits

See [Platform Limits](/api-reference/limits#facebook) for the full breakdown of file sizes, resolutions, aspect ratios, and bitrates.

### Text & Field Limits

| Field | Limit |
| :- | :- |
| `text` | Max 50,000 characters |
| `link` | Max 2,048 characters |
| `mediaTitle` | Max 255 characters |
| `altText` | Optional. Accessibility description for **image** posts (screen readers and when images fail to load). |

<Note>
  **Alt text** applies to image-based Page posts. Pair it with your image `uploadIds` when you want Meta to store accessibility text alongside the media.
</Note>

***

## Post Options

| Field | Type | Description |
| :- | :- | :- |
| `type` | `POST` \| `REEL` \| `STORY` | Defaults to `POST`. |
| `text` | `string` | Caption/body text. Max 50,000 characters. |
| `uploadIds` | `string[]` | Media uploaded through bundle.social. |
| `mediaItems` | `array` | Per-upload metadata, currently used for image `altText`. Each item needs `uploadId`. |
| `link` | `string` | URL for Page posts. Only for `type: "POST"`. |
| `thumbnail` | `string` | URL to an uploaded thumbnail image. |
| `mediaTitle` | `string` | Video title for `POST` video uploads. Max 255 characters. |
| `nativeScheduleTime` | `date` | Schedule inside Meta instead of immediately publishing through bundle.social. Max 30 days ahead. |

```json theme={null}
{
  "teamId": "team_123",
  "title": "Facebook launch post",
  "status": "SCHEDULED",
  "postDate": "2026-06-01T15:00:00.000Z",
  "socialAccountTypes": ["FACEBOOK"],
  "data": {
    "FACEBOOK": {
      "type": "POST",
      "text": "New launch is live",
      "uploadIds": ["upl_img_1"],
      "mediaItems": [
        {
          "uploadId": "upl_img_1",
          "altText": "Product screenshot showing the new dashboard"
        }
      ],
      "link": "https://example.com"
    }
  }
}
```

***

## Page Mentions

Tag another Facebook Page in a post by writing `@[pageId]` in `text`. Facebook turns it into a clickable mention of that Page:

```json theme={null}
"text": "Big thanks to @[123456789012] for hosting us!"
```

Stories have no text, so they can't carry mentions.

### Find a Page ID

**Endpoint:** `GET /api/v1/misc/facebook/pages`

| Param | Required | Description |
| :- | :- | :- |
| `teamId` | Yes | Team with a connected Facebook account. The lookup runs through that account. |
| `q` | Yes | Page name, Page URL, `@handle` or numeric Page ID. Max 100 characters. |
| `limit` | No | Max results for a name search, 1-25. Defaults to 10. |

`q` works two ways:

* **Page URL, `@handle` or ID** (`https://www.facebook.com/nike`, `@nike`, `123456789012`): resolved directly, returns that one Page. A Facebook link that isn't a Page (a group, a video, a deleted Page) returns an empty list.
* **Anything else** (`Warsaw cafe`): full-text search, returns matching Pages.

```http theme={null}
GET /api/v1/misc/facebook/pages?teamId=team_123&q=https://www.facebook.com/nike
```

```json theme={null}
{
  "items": [
    {
      "pageId": "15087023444",
      "name": "Nike",
      "link": "https://www.facebook.com/nike",
      "location": null
    }
  ]
}
```

`location` is filled for Pages that represent a physical place (city, street, coordinates, etc.).

<Note>
  Search uses Meta's Page search, which only returns public Pages. Personal profiles and groups can't be found or mentioned. If the Facebook account is missing the required permissions, the endpoint returns `400` asking you to reconnect it.
</Note>

***

## Analytics

For general analytics concepts (refresh rates, data retention, what "Returns 0" means), see the [Analytics Overview](/api-reference/analytics).

### Profile Analytics

**Period:** Rolling window (30 days).

<Info>
  **Why so many zeros?** To avoid hitting Facebook's aggressive rate limits, we've disabled fetching profile-level likes, comments, and post counts. We'd have to scan every single post on your page to get these, and Facebook would block us (and you). It's not worth it.
</Info>

| Metric | Description | Note |
| :- | :- | :- |
| `impressions` | Total impressions | |
| `impressionsUnique` | Unique users reached | Uses 28-day period to avoid overcounting |
| `views` | Page views | |
| `viewsUnique` | - | Returns `0` (not provided by API) |
| `likes` | - | Returns `0` (disabled to save rate limits) |
| `comments` | - | Returns `0` (disabled to save rate limits) |
| `postCount` | - | Returns `0` (disabled to save rate limits) |
| `followers` | Page followers | |
| `following` | - | Returns `0` (not applicable to Pages) |

### Post Analytics

**Period:** Lifetime (Snapshot).

| Metric | Description | Note |
| :- | :- | :- |
| `impressions` | Total impressions | |
| `impressionsUnique` | Unique impressions | |
| `views` | Video views | Video posts only |
| `viewsUnique` | Unique video views | Video posts only |
| `likes` | Total reactions | Aggregates Like, Love, Wow, Haha, Anger |
| `comments` | Total comments | |
| `shares` | Total shares | |
| `saves` | Total saves | |

### Reaction Aggregation

When we say "Likes" for Facebook, we mean **all reactions** combined. Whether someone Loved it, Hated it (Anger), or Laughed at it (Haha) - it all counts as one `likes` number. We don't break down reaction types in the standard schema. If you need that granularity, check the [raw analytics data](#raw-analytics).

### Raw Analytics

Facebook raw analytics include Page insight payloads for profiles and flat insight metric objects for posts. Use raw data when you need reaction-type totals such as `post_reactions_love_total`, video metrics such as `post_video_avg_time_watched`, or Page demographic payloads.

#### Profile Raw Example

```json theme={null}
{
  "pageInfo": {
    "id": "1234567890",
    "name": "Example Page",
    "followers_count": 12450,
    "fan_count": 11820,
    "link": "https://www.facebook.com/example"
  },
  "pageInsights": {
    "data": [
      {
        "name": "page_media_view",
        "period": "day",
        "values": [
          { "value": 3120, "end_time": "2026-04-26T07:00:00+0000" }
        ]
      },
      {
        "name": "page_views_total",
        "period": "day",
        "values": [
          { "value": 184, "end_time": "2026-04-26T07:00:00+0000" }
        ]
      }
    ]
  },
  "pageDemographicInsights": {
    "data": [
      {
        "name": "page_fans_country",
        "period": "lifetime",
        "values": [
          { "value": { "US": 4200, "GB": 860, "DE": 540 } }
        ]
      }
    ]
  }
}
```

#### Post Raw Example

```json theme={null}
{
  "post_media_view": 14820,
  "post_clicks": 320,
  "post_reactions_like_total": 410,
  "post_reactions_love_total": 92,
  "post_reactions_wow_total": 11,
  "post_reactions_haha_total": 18,
  "post_reactions_anger_total": 1,
  "post_video_views": 11200,
  "post_video_views_unique": 9800,
  "post_video_avg_time_watched": 7400,
  "post_video_views_clicked_to_play": 1330,
  "comments": 44,
  "shares": 27,
  "saves": 9
}
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
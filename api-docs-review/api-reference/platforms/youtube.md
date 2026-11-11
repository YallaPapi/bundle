> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# YouTube

> Long-form, Shorts, and the legal requirement of Made for Kids. Videos up to 4 hours and 5 GB, Shorts auto-detected, and a title is always required.

YouTube handles both traditional long-form videos and Shorts (vertical video). The API comes with legal requirements you can't ignore.

## Supported Content Types

* **Videos:** Long-form content. 1 video, up to 4 hours. Max 5 GB.
* **Shorts:** Vertical/square video, max 3 minutes. YouTube auto-detects based on duration and aspect ratio.

## Quirks & Gotchas

### "Made for Kids" (COPPA)

This is not just a quirk, it's a **legal requirement**.

* You **must** flag content as `madeForKids: true` if it targets children.
* Failure to do so can result in penalties - real ones, from the FTC.
* We expose this field in the `data.YOUTUBE` object. Use it. Don't skip it. Don't "figure it out later".

### Shorts Detection

There is no special "upload as Short" button. YouTube decides for you based on the file:

* **Duration:** Under **3 minutes** (180 seconds).
* **Aspect Ratio:** Vertical (9:16) or Square (1:1). Technically 1:3 to 1:1.

If your video meets these criteria, it becomes a Short. If it doesn't, it's a regular video.

### YouTube Title is Required

Unlike most platforms where you just need text, YouTube treats `data.YOUTUBE.text` as the **video title**. If you leave it empty, YouTube can reject the upload.

### Media Limits

See [Platform Limits](/api-reference/limits#youtube) for the full breakdown.

### Text & Field Limits

| Field | Limit |
| :- | :- |
| `text` (video title) | Max 100 characters |
| `description` | Max 5,000 characters |

***

## Post Options

Send YouTube-specific options inside `data.YOUTUBE`.

| Field | Type | Description |
| :- | :- | :- |
| `type` | `enum` | `VIDEO` or `SHORT`. Default: `SHORT`. |
| `uploadIds` | `string[]` | Required. One uploaded video. |
| `text` | `string` | Video title. Max 100 characters. |
| `description` | `string` | Video description. Max 5,000 characters. |
| `thumbnail` | `string` | Optional thumbnail image URL uploaded through bundle.social. |
| `privacy` | `enum` | `PRIVATE`, `PUBLIC`, or `UNLISTED`. Default sent to YouTube is public if omitted. |
| `defaultLanguage` | `string` | BCP-47 language for the video's title and description, for example `en` or `pl`. Max 35 characters. |
| `defaultAudioLanguage` | `string` | BCP-47 language for the video's default audio track, for example `en` or `pl`. Max 35 characters. |
| `madeForKids` | `boolean` | Required by YouTube policy. Set `true` when the video is made for children. |
| `containsSyntheticMedia` | `boolean` | Set `true` when the video contains AI-generated or synthetic content. |
| `hasPaidProductPlacement` | `boolean` | Set `true` when the video contains paid product placement. |

```json theme={null}
{
  "teamId": "team_123",
  "title": "YouTube launch video",
  "status": "SCHEDULED",
  "postDate": "2026-06-01T15:00:00.000Z",
  "socialAccountTypes": ["YOUTUBE"],
  "data": {
    "YOUTUBE": {
      "type": "VIDEO",
      "uploadIds": ["upload_video_123"],
      "text": "Product launch walkthrough",
      "description": "A full walkthrough of the new release.",
      "privacy": "PUBLIC",
      "defaultLanguage": "en",
      "defaultAudioLanguage": "en",
      "madeForKids": false,
      "containsSyntheticMedia": false,
      "hasPaidProductPlacement": false
    }
  }
}
```

***

## Analytics

For general analytics concepts (refresh rates, data retention, what "Returns 0" means), see the [Analytics Overview](/api-reference/analytics).

YouTube analytics are all **Lifetime** values. There is no rolling window - everything is cumulative from day one.

### Profile (Channel) Analytics

**Period:** Lifetime.

| Metric | Description | Note |
| :- | :- | :- |
| `impressions` | Total channel views | |
| `impressionsUnique` | - | Same as impressions (YouTube doesn't distinguish) |
| `views` | Total channel views | Same as impressions |
| `viewsUnique` | - | Same as views |
| `likes` | - | Returns `0` (not available at channel level) |
| `comments` | Total comments | Across all videos |
| `postCount` | Total videos | |
| `followers` | Subscribers | |
| `following` | - | Returns `0` (not applicable to channels) |

### Post (Video) Analytics

**Period:** Lifetime.

| Metric | Description | Note |
| :- | :- | :- |
| `impressions` | Video views | |
| `impressionsUnique` | - | Same as impressions (YouTube doesn't distinguish) |
| `views` | Video views | Same as impressions |
| `viewsUnique` | - | Same as views |
| `likes` | Likes | |
| `dislikes` | Dislikes | Available via API even though YouTube hides them on the UI |
| `comments` | Comments | |
| `shares` | Lifetime shares | From the YouTube Analytics API. Only filled when raw analytics are enabled for your org, otherwise `0` |
| `saves` | - | Returns `0` (YouTube retired favorites) |

### Quirks

* YouTube doesn't distinguish between impressions and unique impressions at any level.
* Dislikes are available through the API (though YouTube no longer shows dislike counts publicly). Handy if you want to know the truth.
* Channel-level likes are not available. Video shares need raw analytics enabled. YouTube gives us a lot, but not everything.
* Imported videos are always `type: VIDEO`. Shorts are flagged in the post's `extraData` instead: `{ "contentType": "SHORTS", "isShort": true }`, and their `permalink` uses `https://www.youtube.com/shorts/<id>`. `contentType` is YouTube's `creatorContentType` (`SHORTS`, `VIDEO_ON_DEMAND`, `LIVE_STREAM`, ...). If YouTube can't tell us (no views yet, say), `extraData` is `null` and the link stays `/watch`. Re-running the import updates `extraData` and `permalink` on videos you already imported.

### Raw Analytics - Demographics & Audience Data

YouTube raw analytics include demographics data when enabled for your organization. We query the YouTube Analytics API for each video and return age/gender breakdowns and country-level view counts. The same breakdown is also available for the whole channel in the profile raw analytics.

<Note>
  Raw analytics are gated per organization (`rawYoutubeAnalyticsEnabled`). If raw analytics are disabled for your org, the extended fields below (demographics, traffic sources, monetization, etc.) are not collected - only the standard metrics remain.
</Note>

#### Monetization

Monetization (revenue) data is included in raw analytics only when **both** conditions are met:

1. **Raw analytics are enabled** for your organization, and
2. The account connected with **business access** - the YouTube monetary analytics scope, granted via [`withBusinessScope`](/api-reference/connect-social-accounts/oauth-options#withbusinessscope) at connect time.

When both hold, monetization appears at two levels:

* **Channel-level** - a channel-wide revenue report for the analytics window, stored in the profile raw analytics `monetization` field.
* **Video-level** - a per-video revenue report, stored in each video's `monetization` field.

Both use the YouTube Analytics API metrics: `estimatedRevenue`, `estimatedAdRevenue`, `estimatedRedPartnerRevenue`, `grossRevenue`, `cpm`, `playbackBasedCpm`, `adImpressions`, and `monetizedPlaybacks`.

<Note>
  A channel **without monetization** - not in the YouTube Partner Program (YPP), or the account never granted the monetary scope - returns the string `"no data available"` in the `monetization` field instead of a report. This is expected and never fails the analytics run.
</Note>

**Channel with monetization** - the `monetization` field holds a report with `columnHeaders` and `rows`:

```json theme={null}
{
  "monetization": {
    "analyticsWindow": { "startDate": "2026-06-19", "endDate": "2026-07-19" },
    "columnHeaders": [
      { "name": "estimatedRevenue", "columnType": "METRIC", "dataType": "FLOAT" },
      { "name": "estimatedAdRevenue", "columnType": "METRIC", "dataType": "FLOAT" },
      { "name": "estimatedRedPartnerRevenue", "columnType": "METRIC", "dataType": "FLOAT" },
      { "name": "grossRevenue", "columnType": "METRIC", "dataType": "FLOAT" },
      { "name": "cpm", "columnType": "METRIC", "dataType": "FLOAT" },
      { "name": "playbackBasedCpm", "columnType": "METRIC", "dataType": "FLOAT" },
      { "name": "adImpressions", "columnType": "METRIC", "dataType": "INTEGER" },
      { "name": "monetizedPlaybacks", "columnType": "METRIC", "dataType": "INTEGER" }
    ],
    "rows": [
      [1234.56, 1100.20, 134.36, 1800.00, 4.52, 3.98, 265000, 98000]
    ]
  }
}
```

**Channel without monetization** - no YPP data or no monetary scope granted:

```json theme={null}
{
  "monetization": "no data available"
}
```

#### Channel Demographics

Profile raw analytics carry a channel-wide `demographics` field: viewer percentage by age group and gender, plus views by country (sorted by views, descending). It covers the **last 365 days**, so it's a stable audience picture rather than a noisy 30-day slice. If YouTube returns nothing (or the call fails), the field is `null` and the rest of the run carries on.

```json theme={null}
{
  "demographics": {
    "analyticsWindow": { "days": 365, "startDate": "2025-10-09", "endDate": "2026-10-08" },
    "ageGender": {
      "columnHeaders": [
        { "name": "ageGroup", "columnType": "DIMENSION" },
        { "name": "gender", "columnType": "DIMENSION" },
        { "name": "viewerPercentage", "columnType": "METRIC" }
      ],
      "rows": [
        ["age18-24", "female", 14.2],
        ["age25-34", "male", 31.8]
      ]
    },
    "country": {
      "columnHeaders": [
        { "name": "country", "columnType": "DIMENSION" },
        { "name": "views", "columnType": "METRIC" }
      ],
      "rows": [
        ["US", 812000],
        ["GB", 190400]
      ]
    }
  }
}
```

#### Video-Level Raw Data

```json theme={null}
{
  "video": {
    "id": "dQw4w9WgXcQ",
    "snippet": {
      "title": "My Video",
      "publishedAt": "2026-01-15T10:00:00Z"
    },
    "statistics": {
      "viewCount": "125000",
      "likeCount": "8900",
      "commentCount": "342"
    }
  },
  "monetization": {
    "columnHeaders": [
      { "name": "estimatedRevenue", "columnType": "METRIC", "dataType": "FLOAT" },
      { "name": "estimatedAdRevenue", "columnType": "METRIC", "dataType": "FLOAT" },
      { "name": "estimatedRedPartnerRevenue", "columnType": "METRIC", "dataType": "FLOAT" },
      { "name": "grossRevenue", "columnType": "METRIC", "dataType": "FLOAT" },
      { "name": "cpm", "columnType": "METRIC", "dataType": "FLOAT" },
      { "name": "playbackBasedCpm", "columnType": "METRIC", "dataType": "FLOAT" },
      { "name": "adImpressions", "columnType": "METRIC", "dataType": "INTEGER" },
      { "name": "monetizedPlaybacks", "columnType": "METRIC", "dataType": "INTEGER" }
    ],
    "rows": [
      [312.40, 280.10, 32.30, 460.00, 3.90, 3.41, 71000, 24500]
    ]
  },
  "lifetimeTotals": {
    "analyticsWindow": { "startDate": "2026-01-14", "endDate": "2026-10-08" },
    "views": 125000,
    "shares": 1840,
    "estimatedMinutesWatched": 402300,
    "averageViewDuration": 193,
    "averageViewPercentage": 61.4
  },
  "contentType": "VIDEO_ON_DEMAND",
  "isShort": false,
  "demographics": {
    "ageGender": {
      "columnHeaders": [
        { "name": "ageGroup", "columnType": "DIMENSION" },
        { "name": "gender", "columnType": "DIMENSION" },
        { "name": "viewerPercentage", "columnType": "METRIC" }
      ],
      "rows": [
        ["age18-24", "female", 12.3],
        ["age18-24", "male", 18.7],
        ["age25-34", "female", 14.1],
        ["age25-34", "male", 22.4],
        ["age35-44", "female", 8.2],
        ["age35-44", "male", 11.5]
      ]
    },
    "country": {
      "columnHeaders": [
        { "name": "country", "columnType": "DIMENSION" },
        { "name": "views", "columnType": "METRIC" }
      ],
      "rows": [
        ["US", 45200],
        ["GB", 12800],
        ["DE", 8900],
        ["BR", 7200]
      ]
    }
  }
}
```

<Note>
  **Empty demographics data is normal.** YouTube has undocumented thresholds for when demographics become available. Unlike Instagram (\~1,000 followers), nobody knows YouTube's minimum. If `demographics` comes back empty or null for your videos, it likely means the account or video hasn't hit the threshold yet. If you do see data, let us know your account stats - we're trying to figure out the threshold too.
</Note>

<Info>
  Raw YouTube data includes **viewer percentage by age group and gender** and **views by country** (sorted by view count, descending). This is useful for audience analysis and content strategy - especially if you're targeting specific demographics or regions.
</Info>

<Info>
  `lifetimeTotals` covers the video's whole life (the window starts on or before the day before it went live, and runs until today). `averageViewDuration` is in seconds, `averageViewPercentage` is a percentage of the video length. `contentType` / `isShort` come from YouTube's `creatorContentType`. Any of these is `null` when YouTube has no data for the video yet. The normalized `shares` metric is taken from `lifetimeTotals.shares`.
</Info>

<Note>
  At the video level, the `monetization` field is `null` when the account has **no business access** (monetary scope was never granted), and `"no data available"` when the account has business access but the video has no monetary data (e.g. not in YPP). A populated report only appears when business access is granted **and** the video earned revenue in the window.
</Note>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
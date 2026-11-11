> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# TikTok

> The viral machine. Watch out for music copyright, privacy settings, and image-format rules for photo mode.

TikTok is the place for short-form video. The API has specific restrictions around music, privacy, and image formats that will surprise you.

## Supported Content Types

* **Videos:** 1 video, up to 10 minutes. The bread and butter.
* **Photo Mode (Images):** 1-10 images. **JPG, JPEG, or WebP only.** Max **20 MB per image**. PNG will be rejected.

## Quirks & Gotchas

### Privacy Levels & Permalinks

If you set a video's privacy to `SELF_ONLY` (Private), the API **cannot** return a public permalink immediately.

* The `permalink` field will be null or internal-only.
* We can't give you a link to something that doesn't publicly exist. Physics still applies.

### Music & Copyright

TikTok is extremely strict about music rights.

* **Commercial Music Library (CML):** We expose TikTok's pre-cleared music via [TikTok Music](/api-reference/platforms/tiktok-music): trending tracks, genres, and `song_clip_id` for publish. No copyright roulette.
* **Trending Audio:** You generally **cannot** use TikTok's in-app "trending audio" library directly via API.
* **Royalty-Free:** You can use the `autoAddMusic` flag to let TikTok assign royalty-free music, but you lose control over the specific track. It's a gamble.
* **Best Practice:** Use CML for controlled music, or burn your audio into the video file before uploading.

### Image Format (Photo Mode)

TikTok accepts **JPG**, **JPEG**, and **WebP** files for Photo Mode posts. PNG and other formats will be rejected. Convert before uploading. Each image must be under **20 MB**.

### Image sizing (Photo Mode)

For **IMAGE** posts, if photos are larger than **1920x1080** (or unusually tall/wide relative to that canvas), we may **auto-scale** them server-side so delivery matches what TikTok expects. You do not need to pre-shrink assets in every case. We handle the resizing when it helps.

### The REVIEW Status

TikTok is the most common platform to put posts into a `REVIEW` status. This means TikTok wants to review the content before publishing. We periodically re-check and re-attempt publishing. Tell your users to be patient.

### Media Limits

See [Platform Limits](/api-reference/limits#tiktok) for the full breakdown.

### Text & Field Limits

| Field | Limit |
| :- | :- |
| `text` | Max 2,200 characters |

***

## Post Options

| Field | Type | Description |
| :- | :- | :- |
| `type` | `VIDEO` \| `IMAGE` | Defaults to `VIDEO`. `IMAGE` is TikTok Photo Mode. |
| `text` | `string` | Caption text. Max 2,200 characters. |
| `uploadIds` | `string[]` | One video, or 1-10 Photo Mode images. |
| `thumbnail` | `string` | VIDEO only. Custom cover: the `url` of an image uploaded to bundle.social (`POST /upload`). URLs hosted elsewhere are rejected with `400`, since TikTok only fetches covers from verified domains. JPG/PNG/WebP, 360x360 to 1080x1920, up to 20 MB. Overrides `thumbnailOffset`. |
| `privacy` | `SELF_ONLY` \| `PUBLIC_TO_EVERYONE` \| `MUTUAL_FOLLOW_FRIENDS` \| `FOLLOWER_OF_CREATOR` | TikTok visibility setting. |
| `photoCoverIndex` | `number` | Zero-based cover image index for Photo Mode. |
| `isBrandContent` | `boolean` | Paid partnership promoting a third-party business. |
| `isOrganicBrandContent` | `boolean` | Content promoting the creator's own business. |
| `disableComments` | `boolean` | Disable comments. |
| `disableDuet` | `boolean` | Disable Duets. |
| `disableStitch` | `boolean` | Disable Stitches. |
| `thumbnailOffset` | `number` | Video cover frame offset in milliseconds. Ignored when `thumbnail` is set. |
| `isAiGenerated` | `boolean` | Mark AI-generated content. |
| `autoAddMusic` | `boolean` | Let TikTok add music to Photo Mode posts. |
| `autoScale` | `boolean` | For `IMAGE` posts only. Scale oversized images server-side. |
| `uploadToDraft` | `boolean` | Upload as TikTok draft/inbox item. |
| `musicSoundInfo` | `object` | CML music settings. See [TikTok Music](/api-reference/platforms/tiktok-music). |

<Warning>
  Use `uploadToDraft` only when the user really wants TikTok draft handling. Draft uploads can cause massive publish delays. The video might show up in minutes, or it might take hours.

  TikTok's answer is traffic: some days are faster, some days are worse. If your product needs predictable publishing, publish directly instead of using drafts.
</Warning>

```json theme={null}
{
  "teamId": "team_123",
  "title": "TikTok launch video",
  "status": "SCHEDULED",
  "postDate": "2026-06-01T15:00:00.000Z",
  "socialAccountTypes": ["TIKTOK"],
  "data": {
    "TIKTOK": {
      "type": "VIDEO",
      "text": "Launch day",
      "uploadIds": ["upl_vid_1"],
      "privacy": "PUBLIC_TO_EVERYONE",
      "disableComments": false,
      "disableDuet": false,
      "disableStitch": false,
      "isAiGenerated": false
    }
  }
}
```

***

## Analytics

For general analytics concepts (refresh rates, data retention, what "Returns 0" means), see the [Analytics Overview](/api-reference/analytics).

TikTok provides detailed analytics data: demographics, audience splits, watch metrics, the works. Check the raw analytics for the detailed breakdowns.

### Profile Analytics

**Period:** Rolling window (30 days). Aggregated from daily metrics.

| Metric | Description | Note |
| :- | :- | :- |
| `impressions` | Video views | |
| `impressionsUnique` | Unique video views | |
| `views` | Video views | Same as impressions for TikTok |
| `viewsUnique` | Unique video views | Same as impressionsUnique |
| `likes` | Total likes | Aggregated across all videos |
| `comments` | Total comments | |
| `postCount` | Total videos | |
| `followers` | Followers | |
| `following` | Following | |

### Post Analytics

**Period:** Lifetime (Snapshot).

| Metric | Description | Note |
| :- | :- | :- |
| `impressions` | Video views | |
| `impressionsUnique` | Unique views | TikTok doesn't always distinguish; can equal impressions |
| `views` | Video views | Same as impressions |
| `viewsUnique` | Unique views | Same as impressionsUnique |
| `likes` | Likes | |
| `comments` | Comments | |
| `shares` | Shares | |
| `saves` | - | Returns `0` (not provided by TikTok API) |

### Quirks

* Profile analytics aggregate daily metrics over a 30-day window.
* Post analytics are lifetime values.
* TikTok can take up to **48 hours** to process some detailed analytics like audience demographics.
* Views and unique views are tracked separately but can sometimes be 0 if the platform decides so.

### Raw Analytics - Demographics & Audience Data

TikTok provides audience and engagement data via raw analytics. Here's what the raw payload looks like when enabled for your organization:

#### Account-Level Raw Data

```json theme={null}
{
  "followers_count": 125400,
  "following_count": 342,
  "total_likes": 2891000,
  "videos_count": 287,
  "unique_video_views": 1450000,
  "video_views": 8920000,
  "comments": 45200,
  "audience_ages": [
    { "age_range": "18-24", "percentage": 42.3 },
    { "age_range": "25-34", "percentage": 31.7 },
    { "age_range": "35-44", "percentage": 14.2 },
    { "age_range": "45-54", "percentage": 7.1 },
    { "age_range": "55+", "percentage": 4.7 }
  ],
  "audience_cities": [
    { "city": "Los Angeles", "percentage": 8.2 },
    { "city": "New York", "percentage": 7.1 },
    { "city": "London", "percentage": 5.4 }
  ],
  "engaged_audience": [
    { "metric": "likes", "value": 89200 },
    { "metric": "comments", "value": 4520 },
    { "metric": "shares", "value": 12300 }
  ],
  "metrics": [
    {
      "date": "2026-01-15",
      "new_followers": 234,
      "video_views": 45600,
      "profile_views": 1230,
      "likes": 3400,
      "comments": 120,
      "shares": 890,
      "audience_activity": [
        { "hour": "0", "count": 12 },
        { "hour": "1", "count": 18 }
      ]
    }
  ]
}
```

`audience_activity` is the hourly breakdown of when your followers are active on TikTok (UTC). Like the other `audience_*` fields, TikTok only returns it for accounts with at least 100 followers.

#### Video-Level Raw Data

```json theme={null}
{
  "item_id": "7123456789",
  "caption": "My viral video",
  "video_views": 1200000,
  "likes": 89000,
  "comments": 4500,
  "shares": 12000,
  "average_time_watched": 18.4,
  "full_video_watched_rate": 0.42,
  "total_time_watched": 22080000,
  "reach": 890000,
  "impression_sources": [
    { "source": "For You", "percentage": 72.1 },
    { "source": "Following", "percentage": 15.3 },
    { "source": "Search", "percentage": 8.4 }
  ],
  "audience_genders": [
    { "gender": "Male", "percentage": 45.2 },
    { "gender": "Female", "percentage": 52.1 },
    { "gender": "Other", "percentage": 2.7 }
  ],
  "audience_countries": [
    { "country": "US", "percentage": 35.2 },
    { "country": "GB", "percentage": 12.4 },
    { "country": "BR", "percentage": 8.9 }
  ]
}
```

<Info>
  TikTok raw data includes **impression sources** (For You, Following, Search), **watch-through rates**, **audience gender/country splits**, and daily metrics breakdowns. This is gold for content strategy - use it.
</Info>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
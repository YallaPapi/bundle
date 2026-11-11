> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Instagram

> Reels, Stories, Posts, and the strict laws of aspect ratios. Feed posts must sit between 4:5 and 1.91:1 or Instagram rejects them without mercy.

Instagram is visually demanding. The API reflects that. If you don't follow their rules on aspect ratios and media types, they will reject your content without mercy.

## Supported Content Types

* **Posts:** Single image, single video, or carousel (mixed images + videos). 1-10 files.
* **Reels:** Video only. Must be vertical.
* **Stories:** Image or video. Expire after 24 hours. Gone like your motivation on Monday morning.

## Quirks & Gotchas

### Aspect Ratios are Law

Instagram is very strict here.

* **Stories/Reels:** Must be **9:16** (vertical). Technically the API accepts wider ratios, but they'll look terrible.
* **Feed Posts:** **4:5** (vertical) or **1:1** (square) for images. Videos are more flexible.

> [!WARNING]
>
> **Don't try to cheat.** If you upload a 16:9 (landscape) video as a Reel, it might technically "work" but it will look terrible (awkwardly cropped) or be rejected entirely. Your marketing team will not be happy. Your users' marketing teams will not be happy. Nobody will be happy.

### What if I have non-standard content?

Instagram feed Posts must fall within a specific aspect ratio range (4:5 to 1.91:1). If your users upload wide landscape photos or tall portrait shots that fall outside this range, you have two automatic correction options instead of rejecting the upload outright:

| Option | Field | Behavior |
| :- | :- | :- |
| Fit | `autoFitImage: true` | Adds padding around the image to fit the target ratio. No pixels are lost. The same way Instagram does this natively. |
| Crop | `autoCropImage: true` | Center-crops the image to fit the target ratio. No padding, but edges are cut. |

> [!WARNING]
>
> These two options are mutually exclusive. Sending both as `true` will fail validation. They only apply to `type: "POST"` and have no effect on Reels or Stories.

### Stories vs. Reels vs. Posts

* **Stories** are ephemeral. They disappear after 24 hours. Great for FOMO content.
* **Reels** are for growth. They're public, discoverable, and the algorithm loves them.
* **Posts** are for the feed grid. The permanent collection.

### Media Limits

See [Platform Limits](https://info.bundle.social/api-reference/limits.md#instagram) for the full breakdown of file sizes, resolutions, and aspect ratios.

### Text & Field Limits

| Field | Limit |
| :- | :- |
| `text` | Max 2,000 characters |
| `collaborators` | Max 3 usernames, each max 30 chars |
| `tagged` | Max 20 users per media, username max 30 chars |
| `carouselItems` | Max 10 items |
| `locationId` | Max 64 characters |
| `altText` | Optional. Accessibility description for **image** posts (feed, carousel images, etc.). |

> [!NOTE]
>
> **Alt text** is supported on image posts. Use it when you need screen-reader-friendly descriptions beyond the caption in `text`.

***

## Post Options

Send Instagram-specific options inside `data.INSTAGRAM`.

| Field | Type | Description |
| :- | :- | :- |
| `type` | `enum` | `POST`, `REEL`, or `STORY`. Default: `POST`. |
| `text` | `string` | Caption. Max 2,000 characters. |
| `uploadIds` | `string[]` | Uploaded media IDs. Posts support 1-10 files, Reels and Stories require 1 file. |
| `altText` | `string` | Accessibility text for a single image post. |
| `thumbnailOffset` | `number` | Video cover frame offset in milliseconds. |
| `thumbnail` | `string` | Optional thumbnail image URL uploaded through bundle.social. |
| `shareToFeed` | `boolean` | Reels only. Controls whether the Reel can also appear in the feed. |
| `collaborators` | `string[]` | Up to 3 usernames. Not supported for Stories. |
| `autoFitImage` | `boolean` | Feed posts only. Adds padding to fit Instagram aspect ratio requirements. |
| `autoCropImage` | `boolean` | Feed posts only. Crops to fit Instagram aspect ratio requirements. |
| `tagged` | `array` | Person tags. Images need `x`/`y`; Reels use usernames only. |
| `carouselItems` | `array` | Per-item metadata for carousel posts, including `uploadId`, `altText`, and image tags. |
| `locationId` | `string` | Facebook Page/location ID to tag on posts or Reels. Not supported for Stories. |
| `trialParams` | `object` | Trial Reels settings. Reels only. |
| `musicSoundInfo` | `object` | Instagram audio settings for Reels. Requires Instagram connected via Facebook Login. |

```json theme={null}
{
  "teamId": "team_123",
  "title": "Instagram Reel launch",
  "status": "SCHEDULED",
  "postDate": "2026-06-01T15:00:00.000Z",
  "socialAccountTypes": ["INSTAGRAM"],
  "data": {
    "INSTAGRAM": {
      "type": "REEL",
      "text": "Launching today",
      "uploadIds": ["upload_video_123"],
      "shareToFeed": true,
      "thumbnailOffset": 1500,
      "collaborators": ["creator_one"],
      "locationId": "1234567890",
      "musicSoundInfo": {
        "musicSoundId": "ig_audio_123",
        "musicSoundVolume": 80,
        "videoOriginalSoundVolume": 20
      }
    }
  }
}
```

> [!WARNING]
>
> `autoFitImage` and `autoCropImage` are mutually exclusive. `musicSoundInfo` works only for `type: "REEL"` and only when the Instagram account is connected through Facebook Login.

### Instagram Misc Endpoints

Instagram audio search for Reels is documented separately: [Instagram Music Library](https://info.bundle.social/api-reference/platforms/instagram-music.md).

#### `GET /misc/instagram/tags`

* Purpose: business discovery by username (public profile data for discoverable business/creator accounts).
* The response can include up to 12 recent public media items with media type, likes, comments, timestamp, and caption when Meta returns them.
* Important: works only when the Instagram account is connected via `FACEBOOK` login flow.
* If the account is connected via direct `INSTAGRAM` method, API returns explicit `400` with reconnection guidance.
* Private accounts and some non-business/non-creator accounts may not be discoverable and can return `exists: false`.
* In our tests, business discovery can sometimes return `false` for accounts that are still valid for publishing tags. In other words: lookup may fail, while tagging that same username in publish payload can still work.

#### `GET /misc/instagram/locations`

* Purpose: search Facebook Pages with physical location data and return IDs for `data.INSTAGRAM.locationId`.
* Important: works only for Instagram accounts connected via `FACEBOOK` method.
* Uses the account page token (`socialAccount.accessToken`).
* Missing page permissions/features (for example `pages_read_engagement`) return explicit `400` with actionable message.

> [!NOTE]
>
> Meta location search can be inconsistent. If you hit the permission/error path, there is usually nothing we can reliably fix from API side right now (this behavior is widely reported in Meta developer threads). The good news: `locationId` tagging itself still works when you already have a valid location/page ID, so known IDs found externally can still be used in publish payloads. We hope this endpoint becomes stable for all accounts over time.

### Publishing Payload & Validation Rules

#### `locationId` mapping

* `data.INSTAGRAM.locationId` is mapped to `location_id` in Instagram publish payload.
* Supported in single image, reel/single-video flow, and carousel parent container.

#### `shareToFeed`

* Accepted only for reel-like payloads:
  * `type = REEL`, or
  * `type = POST` with exactly one video upload.
* Rejected for image posts, carousels, and stories (`400`).

#### Person tags (`tagged`)

* Reel/single-video: provide usernames only (no `x`/`y` coordinates).
* Single image: each tagged user must include `x` and `y` in range `0-1`.
* Carousel: top-level `tagged` is rejected; use `carouselItems[].tagged` per item.
* Carousel video item: person tags are not supported and are rejected.

#### Carousel item binding

* `carouselItems` is allowed only for real carousel posts (at least 2 uploads).
* Every `carouselItems[].uploadId` must exist in provided `uploadIds`.
* Use each `uploadId` only once in `carouselItems`.

```json theme={null}
{
  "socialAccountTypes": ["INSTAGRAM"],
  "data": {
    "INSTAGRAM": {
      "type": "POST",
      "text": "Carousel with per-item tags",
      "uploadIds": ["upl_img_1", "upl_img_2", "upl_vid_1"],
      "carouselItems": [
        {
          "uploadId": "upl_img_1",
          "tagged": [{ "username": "alice", "x": 0.25, "y": 0.4 }]
        },
        {
          "uploadId": "upl_img_2",
          "tagged": [{ "username": "bob", "x": 0.6, "y": 0.35 }]
        },
        {
          "uploadId": "upl_vid_1"
        }
      ]
    }
  }
}
```

#### Story constraints

* Stories do not support `collaborators`.
* Stories do not support `locationId`.

#### Collaborators behavior

* Collaborators are normalized before publish (`@` stripped, trim, lowercase).
* Automatic fallback retry without unavailable collaborators was removed.
* Retry behavior now follows standard BullMQ worker retry policy.

#### Trial Reels

Trial reels are shared only with non-followers first. If the content performs well, it can be graduated to a regular reel that appears to everyone.

Send `data.INSTAGRAM.trialParams.graduationStrategy` in the publish payload:

| Value | Behavior |
| :- | :- |
| `MANUAL` | The trial reel stays in trial until you manually graduate it from the native Instagram app. |
| `SS_PERFORMANCE` | Instagram automatically graduates the reel if it meets a performance threshold. |

Requirements and caveats:

* Only valid for `type: "REEL"`. Ignored for Posts and Stories.
* Requires a public professional (Creator or Business) account with at least around 1,000 followers. Instagram has not published an official threshold and some users report access starting at 200 followers.
* Not all professional accounts will have access to this feature regardless of follower count.

```json theme={null}
{
  "socialAccountTypes": ["INSTAGRAM"],
  "data": {
    "INSTAGRAM": {
      "type": "REEL",
      "text": "Testing this reel with non-followers first",
      "uploadIds": ["upl_vid_1"],
      "trialParams": {
        "graduationStrategy": "SS_PERFORMANCE"
      }
    }
  }
}
```

***

## Analytics

For general analytics concepts (refresh rates, data retention, what "Returns 0" means), see the [Analytics Overview](https://info.bundle.social/api-reference/analytics.md).

### Refresh Rate & Limits

* **Default Refresh:** Every 24 hours.
* **Force Refresh:** Available (max 6 per account and 6 per post in any 24 hours).
* **Data Retention:** 30 days. [Details](https://info.bundle.social/api-reference/data-retention.md).

### Profile Analytics

**Period:** Rolling window (30 days).

| Metric | Description | Note |
| :- | :- | :- |
| `impressions` | Total times profile content was shown | |
| `impressionsUnique` | Unique accounts that saw content | Called "Reach" by Instagram |
| `views` | Profile views | |
| `viewsUnique` | - | Returns `0` (not provided by API) |
| `likes` | Total likes | |
| `comments` | Total comments | |
| `postCount` | Total posts published | |
| `followers` | Total followers | |
| `following` | Total following | |

### Post Analytics

**Period:** Lifetime (Snapshot).

| Metric | Description | Note |
| :- | :- | :- |
| `impressions` | Total views | Called "views" in Instagram API |
| `impressionsUnique` | Unique accounts reached | Called "reach" in Instagram API |
| `views` | Video plays | Videos/Reels only |
| `viewsUnique` | - | Returns `0` (not provided by API) |
| `likes` | Total likes | |
| `comments` | Total comments | |
| `shares` | Total shares | Reels only |
| `saves` | Total saves | |

### Raw Analytics - Demographics & Audience Data

Instagram provides detailed demographic data via raw analytics. Here's what the raw payload looks like when enabled for your organization:

```json theme={null}
{
  "profileInfo": { /* basic account info */ },
  "totals30d": [ /* 30-day daily breakdown */ ],
  "demographics": {
    "follows_and_unfollows": {
      "data": [{
        "name": "follows_and_unfollows",
        "period": "day",
        "title": "Follows and unfollows",
        "total_value": { "value": { "follows": 142, "unfollows": 23 } }
      }]
    },
    "follower_demographics": {
      "country": {
        "data": [{
          "name": "follower_demographics",
          "total_value": {
            "breakdowns": [{
              "dimension_keys": ["country"],
              "results": [
                { "dimension_values": ["US"], "value": 4521 },
                { "dimension_values": ["GB"], "value": 1893 },
                { "dimension_values": ["DE"], "value": 1247 }
              ]
            }]
          }
        }]
      },
      "city": {
        "data": [{
          "name": "follower_demographics",
          "total_value": {
            "breakdowns": [{
              "dimension_keys": ["city"],
              "results": [
                { "dimension_values": ["New York, New York"], "value": 892 },
                { "dimension_values": ["London, England"], "value": 654 }
              ]
            }]
          }
        }]
      },
      "gender": {
        "data": [{
          "name": "follower_demographics",
          "total_value": {
            "breakdowns": [{
              "dimension_keys": ["gender"],
              "results": [
                { "dimension_values": ["M"], "value": 5234 },
                { "dimension_values": ["F"], "value": 4891 },
                { "dimension_values": ["U"], "value": 312 }
              ]
            }]
          }
        }]
      },
      "age": {
        "data": [{
          "name": "follower_demographics",
          "total_value": {
            "breakdowns": [{
              "dimension_keys": ["age"],
              "results": [
                { "dimension_values": ["18-24"], "value": 3421 },
                { "dimension_values": ["25-34"], "value": 4102 },
                { "dimension_values": ["35-44"], "value": 1893 },
                { "dimension_values": ["45-54"], "value": 721 }
              ]
            }]
          }
        }]
      }
    },
    "engaged_audience_demographics": {
      "country": { /* same structure as follower_demographics */ },
      "city": { /* same structure */ },
      "gender": { /* same structure */ },
      "age": { /* same structure */ }
    },
    "follower_demographics_age_gender": {
      "data": [{
        "name": "follower_demographics",
        "total_value": {
          "breakdowns": [{
            "dimension_keys": ["age", "gender"],
            "results": [
              { "dimension_values": ["18-24", "F"], "value": 1820 },
              { "dimension_values": ["18-24", "M"], "value": 1534 },
              { "dimension_values": ["25-34", "F"], "value": 2011 }
            ]
          }]
        }
      }]
    }
  },
  "onlineFollowers": {
    "data": [{
      "name": "online_followers",
      "period": "lifetime",
      "values": [
        { "value": { "0": 312, "1": 280, "...": 0, "23": 401 }, "end_time": "2026-10-07T07:00:00+0000" }
      ]
    }]
  }
}
```

* `demographics.follower_demographics_age_gender` is the age × gender cross-tab of your followers (one row per age bucket + gender pair). It's `null` if Instagram didn't return it.
* `onlineFollowers` shows how many followers were online in each hour (`0`-`23`) for each of the last 30 days. Handy for picking posting times. Instagram only returns it for accounts with 100+ followers, so it's `null` for smaller accounts.
* `reachByFollowType` is the account's unique reach over the last 30 days (same window as `totals30d`), split into followers and non-followers. `reachTimeSeries` has reach per day for the same 30 days; summing those days counts the same person once per day they were reached, so it's higher than the 30-day total.

> [!NOTE]
>
> Raw demographics include both **follower demographics** (lifetime, who follows you) and **engaged audience demographics** (this month, who interacts with your content). These are two different audiences and both are useful for understanding your reach.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
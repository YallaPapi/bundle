> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Bulk Post from CSV

> Create many posts at once by uploading a CSV file. Async processing with per-row results.

Got 200 posts to schedule? Upload a CSV instead of creating every post with a separate `POST /post` request.

Each row in the CSV becomes one post. Multiple platforms per row, multiple teams, media referenced by URL - one bad row won't block the rest.

## How it works

This is an **asynchronous** job, same pattern as [Import Post History](/api-reference/import-posts).

1. **Upload:** You send us a CSV file.
2. **Wait:** We process each row in the background.
3. **Poll:** You check if we're done.
4. **Results:** You get per-row success/failure details.

***

## Step 1: Upload the CSV

**Endpoint:** `POST /api/v1/post-csv-import`

```bash theme={null}
curl -X POST "https://api.bundle.social/api/v1/post-csv-import" \
  -H "x-api-key: YOUR_KEY" \
  -F "file=@./posts.csv"
```

The file must be `.csv` and under **100 MB**.

**Response** (`201`):

```json theme={null}
{
  "id": "import_abc123",
  "teamId": "team_456",
  "organizationId": "org_789",
  "status": "PENDING",
  "fileName": "posts.csv",
  "totalRows": 200,
  "processedRows": 0,
  "successRows": 0,
  "failedRows": 0,
  "error": null,
  "rateLimitResetAt": null,
  "startedAt": null,
  "completedAt": null,
  "createdAt": "2026-03-31T12:00:00.000Z",
  "updatedAt": "2026-03-31T12:00:00.000Z"
}
```

<Note>
  Every row in the CSV must include a **`teamId`**, and all referenced teams must belong to the same organization that owns your API key.
</Note>

***

## Step 2: Poll Progress

You have two options: lightweight status or full import details.

### Status (lightweight)

**Endpoint:** `GET /api/v1/post-csv-import/{importId}/status`

```bash theme={null}
curl "https://api.bundle.social/api/v1/post-csv-import/import_abc123/status" \
  -H "x-api-key: YOUR_KEY"
```

```json theme={null}
{
  "id": "import_abc123",
  "status": "PROCESSING",
  "totalRows": 200,
  "processedRows": 87,
  "successRows": 85,
  "failedRows": 2,
  "error": null,
  "startedAt": "2026-03-31T12:00:01.000Z",
  "completedAt": null,
  "updatedAt": "2026-03-31T12:00:45.000Z"
}
```

### Full import details

**Endpoint:** `GET /api/v1/post-csv-import/{importId}`

Returns the full import object (same shape as the `POST` response).

### Import history

**Endpoint:** `GET /api/v1/post-csv-import`

| Parameter | Type | Default | Description |
| :- | :- | :- | :- |
| `offset` | number | `0` | Skip this many records |
| `limit` | number | `10` | How many to return |

Returns `{ items, total }`, newest first.

***

## Step 3: Row Results

Once the import finishes (or while it's running), you can inspect individual rows.

**Endpoint:** `GET /api/v1/post-csv-import/{importId}/rows`

| Parameter | Type | Default | Description |
| :- | :- | :- | :- |
| `status` | string | - | Filter by `SUCCESS` or `FAILED` |
| `offset` | number | `0` | Skip this many rows |
| `limit` | number | `10` | How many to return |

```bash theme={null}
curl "https://api.bundle.social/api/v1/post-csv-import/import_abc123/rows?status=FAILED" \
  -H "x-api-key: YOUR_KEY"
```

```json theme={null}
{
  "items": [
    {
      "id": "row_001",
      "importId": "import_abc123",
      "rowNumber": 14,
      "status": "FAILED",
      "postId": null,
      "rawRow": {
        "teamId": "team_456",
        "postDate": "2026-04-05T10:00:00Z",
        "socialAccountTypes": "INSTAGRAM,TIKTOK",
        "text": "Hello world!"
      },
      "normalizedPayload": null,
      "error": "Team not found or does not belong to your organization",
      "createdAt": "2026-03-31T12:00:12.000Z"
    }
  ],
  "total": 2
}
```

Successful rows include the `postId` so you can track the created post:

```json theme={null}
{
  "rowNumber": 1,
  "status": "SUCCESS",
  "postId": "post_xyz789",
  "error": null
}
```

***

## Import Statuses

| Status | Meaning |
| :- | :- |
| `PENDING` | Queued, processing hasn't started yet. |
| `PROCESSING` | We're working through the rows. |
| `COMPLETED` | All rows processed successfully. |
| `COMPLETED_WITH_ERRORS` | Done, but at least one row failed. |
| `FAILED` | The entire import failed (e.g. invalid file). |
| `RATE_LIMITED` | Paused due to platform rate limits. |

***

## CSV Format

Each row is one post. Column names map to post fields:

| Column | Required | Description |
| :- | :- | :- |
| `teamId` | Yes | Which team this post belongs to |
| `title` | Yes | Internal post title shown in bundle.social |
| `postDate` | Yes | ISO 8601 date-time with timezone, for example `2026-04-05T10:00:00Z` |
| `status` | Yes | `DRAFT` or `SCHEDULED` |
| `socialAccountTypes` | Yes | Comma-separated platforms (e.g. `INSTAGRAM,TIKTOK,LINKEDIN`) |
| `text` | - | Post body text |
| `*MediaUrls` | - | Platform-specific media URLs (e.g. `instagramMediaUrls`, `tiktokMediaUrls`) |

Media is referenced by **URL** - we download and process it for you. No need to upload files first with `/upload`.

Use `#` to separate multiple media URLs or list-like values inside one cell:

```csv theme={null}
instagramMediaUrls
https://cdn.example.com/1.jpg#https://cdn.example.com/2.jpg
```

### Platform Media URL Columns

| Platform | Column |
| :- | :- |
| Facebook | `facebookMediaUrls` |
| Instagram | `instagramMediaUrls` |
| TikTok | `tiktokMediaUrls` |
| YouTube | `youtubeMediaUrls` |
| LinkedIn | `linkedinMediaUrls` |
| Pinterest | `pinterestMediaUrls` |
| Reddit | `redditMediaUrls` |
| Threads | `threadsMediaUrls` |
| Twitter / X | `twitterMediaUrls` |
| Mastodon | `mastodonMediaUrls` |
| Bluesky | `blueskyMediaUrls` |
| Discord | `discordMediaUrls` |
| Slack | `slackMediaUrls` |
| Google Business | `googleBusinessMediaUrls` |
| Snapchat | `snapchatMediaUrls` |

### Common Platform Columns

| Platform | Columns |
| :- | :- |
| Facebook | `facebookType`, `facebookText`, `facebookLink`, `facebookThumbnail`, `facebookMediaTitle`, `facebookNativeScheduleTime` |
| Instagram | `instagramType`, `instagramText`, `instagramThumbnailOffset`, `instagramThumbnail`, `instagramShareToFeed`, `instagramCollaborators`, `instagramAutoFitImage`, `instagramAutoCropImage`, `instagramTagged`, `instagramCarouselItems`, `instagramLocationId`, `instagramTrialParamsGraduationStrategy`, `instagramMusicSoundId`, `instagramMusicSoundVolume`, `instagramVideoOriginalSoundVolume` |
| TikTok | `tiktokType`, `tiktokText`, `tiktokThumbnail`, `tiktokPrivacy`, `tiktokIsBrandContent`, `tiktokIsOrganicBrandContent`, `tiktokDisableComments`, `tiktokDisableDuet`, `tiktokDisableStitch`, `tiktokThumbnailOffset`, `tiktokIsAiGenerated`, `tiktokAutoAddMusic`, `tiktokAutoScale`, `tiktokUploadToDraft`, `tiktokPhotoCoverIndex`, `tiktokMusicSoundId`, `tiktokMusicSoundVolume`, `tiktokMusicSoundStart`, `tiktokMusicSoundEnd`, `tiktokVideoOriginalSoundVolume` |
| YouTube | `youtubeType`, `youtubeTitle`, `youtubeDescription`, `youtubeThumbnail`, `youtubePrivacy`, `youtubeMadeForKids`, `youtubeContainsSyntheticMedia`, `youtubeHasPaidProductPlacement` |
| LinkedIn | `linkedinText`, `linkedinLink`, `linkedinThumbnail`, `linkedinMediaTitle`, `linkedinPrivacy`, `linkedinHideFromFeed`, `linkedinDisableReshare` |
| Pinterest | `pinterestBoardName`, `pinterestTitle`, `pinterestDescription`, `pinterestLink`, `pinterestThumbnail`, `pinterestAltText`, `pinterestNote`, `pinterestDominantColor` |
| Reddit | `redditSubreddit`, `redditText`, `redditDescription`, `redditLink`, `redditNsfw`, `redditFlairId` |
| Threads | `threadsText` |
| Twitter / X | `twitterText`, `twitterReplySettings` |
| Mastodon | `mastodonText`, `mastodonPrivacy`, `mastodonThumbnail`, `mastodonSpoiler` |
| Bluesky | `blueskyText`, `blueskyTags`, `blueskyLabels`, `blueskyQuoteUri`, `blueskyExternalUrl`, `blueskyExternalTitle`, `blueskyExternalDescription`, `blueskyThumbnail`, `blueskyVideoAlt` |
| Discord | `discordChannelId`, `discordText`, `discordUsername`, `discordAvatarUrl` |
| Slack | `slackChannelId`, `slackText`, `slackUsername`, `slackAvatarUrl` |
| Google Business | `googleBusinessText`, `googleBusinessTopicType`, `googleBusinessLanguageCode`, `googleBusinessCallToActionType`, `googleBusinessCallToActionUrl`, `googleBusinessEventTitle`, `googleBusinessEventStartDate`, `googleBusinessEventEndDate`, `googleBusinessOfferCouponCode`, `googleBusinessOfferRedeemOnlineUrl`, `googleBusinessOfferTermsConditions`, `googleBusinessAlertType` |
| Snapchat | `snapchatType`, `snapchatDescription`, `snapchatLocale`, `snapchatSkipSaveToProfile` |

Boolean columns must be `TRUE` or `FALSE`. Enum-like columns are case-insensitive in practice because we normalize them to uppercase before validation.

<Tip>
  Download a CSV template from the bundle.social dashboard under the **Bulk Post** section to see all available columns and example values.
</Tip>

***

## Handling Rate Limits

If the import status goes to `RATE_LIMITED`, don't panic. We hit a platform's posting cap.

* The import pauses automatically.
* Check `rateLimitResetAt` for when it can resume.
* We retry automatically - just keep polling.

This works the same as [Import Post History](/api-reference/import-posts) rate limiting.

***

## See also

* [Import Post History](/api-reference/import-posts) - same async pattern, but for pulling existing posts from platforms.
* [Media Upload](/api-reference/upload-content) - if you prefer uploading media separately before creating posts.
* [Rate Limits](/api-reference/rate-limits) - posting limits per platform and plan.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Import Post History

> Pull past posts and analytics from Instagram, TikTok, LinkedIn and more. An async job backfills your dashboard with history from before you connected.

Use the History Import API to fetch existing content from connected accounts and populate your dashboard with past posts.

* You can filter imports by **surface** and **media type**.
* You can request richer media metadata in `extraData` (when platform returns direct media URLs).
* `extraData` is now normalized as `extraData.media[]`.
* For platforms/endpoints that do not expose direct media URLs (e.g. current YouTube import path), `extraData` is `null`.

Need comment import and replies? See [Comments API](/api-reference/comments).

## How it works

This is an **asynchronous** job. You don't get the posts instantly.

1. **Start:** You trigger a job ("Go fetch 50 posts from Instagram").
2. **Wait:** We queue it, talk to the platform, and crunch the data.
3. **Poll:** You check if we're done.
4. **Fetch:** You download the results.

***

## Step 1: Start the Job

**Endpoint:** `POST /api/v1/post-history-import`

```json theme={null}
{
  "teamId": "team_123",
  "socialAccountType": "INSTAGRAM",
  "count": 50,
  "withAnalytics": true,
  "importCarousels": true,
  "surface": "ALL",
  "mediaType": "VIDEO"
}
```

### Import filters and media options

* `surface` lets you choose where the content comes from (`ALL`, `PROFILE_GRID`, `NON_GRID`, `STORY`).
* `mediaType` filters by content type (`VIDEO` or `IMAGE`).
* `importCarousels` controls whether carousel child media is expanded into `extraData.media[]` when supported.

<Note>
  Platform APIs are inconsistent. Some filters/surfaces may return no data on specific platforms if that API does not expose that view.
</Note>

### What `count` means (and `onlyLatest`)

By default, `count` is the number of posts **you don't have yet** that we import. Posts you already imported are skipped and don't count toward your limit, but the import keeps going further back into older posts until it has found `count` new ones.

For a recurring sync ("did this creator post anything new?"), set `onlyLatest: true`:

```json theme={null}
{
  "teamId": "team_123",
  "socialAccountType": "INSTAGRAM",
  "count": 10,
  "onlyLatest": true
}
```

We check only the latest `count` posts and import the ones you don't have yet. If nothing is new, nothing is imported and nothing counts toward your limit. On X, every post we read is still billed, new or not.

**Limits:**

* **Free:** 5 posts / month (Demo mode)
* **Pro:** 100 posts / month
* **Business:** 500 posts / month

<Note>
  **Why limits?** Historical imports are expensive on API tokens. We have to be stingy here to keep the service cheap for everyone.
</Note>

### Imported post analytics

By default, imported posts get an **initial analytics snapshot** at import time when `withAnalytics: true`.

#### Ongoing Analytics Refresh

Imported posts can also be added to the regular analytics refresh cycle - meaning they get updated on the same schedule as posts created through bundle.social.

This is controlled by an organization-level setting. When enabled:

* Imported posts are included in the regular analytics scanner.
* You can fetch analytics for imported posts via the standard analytics endpoints using `importedPostId` instead of `postId`.
* You can force-refresh analytics for imported posts the same way you would for regular posts.

<Note>
  **`importedPostId` vs `postId`:** When querying analytics for imported posts, use `importedPostId` (the imported post's ID). Don't mix it with `postId` + `platformType` - they're mutually exclusive.
</Note>

<Warning>
  Ongoing analytics for imported posts means we're making additional API calls to platforms for posts that weren't created through bundle.social.

  Want to enable this? [Contact us](https://bundle.social/contact) and we'll set it up for your organization. It's included in paid plans at no extra cost. The only exception is X: importing from X and every X analytics refresh are billed from your prepaid [X credits](/api-reference/platforms/twitter), and imported X posts are never refreshed in the background.
</Warning>

***

## Step 2: Check Status

**Endpoint:** `GET /api/v1/post-history-import?teamId=...`

You'll see a list of jobs with statuses:

* `PENDING`: In queue.
* `FETCHING_POSTS`: Talking to Instagram...
* `COMPLETED`: Done!
* `FAILED`: Import failed after retries.
* `RATE_LIMITED`: Platform said "slow down". We paused it for you.

***

## Step 3: Get the Loot

**Endpoint:** `GET /api/v1/post-history-import/posts`

Once status is `COMPLETED`, call this to get the actual data.

```json theme={null}
{
  "posts": [
    {
      "title": "My Cat Video",
      "type": "VIDEO",
      "extraData": null,
      "analytics": {
        "likes": 1337,
        "impressions": 42000
      }
    },
    {
      "title": "Carousel example",
      "type": "IMAGE",
      "extraData": {
        "media": [
          {
            "id": "1789...",
            "mediaUrl": "https://cdn.platform.com/media/..."
          }
        ]
      }
    }
  ]
}
```

### `extraData` structure

When available, imported posts include:

```json theme={null}
{
  "extraData": {
    "media": [
      {
        "id": "platform-media-id-or-null",
        "mediaUrl": "direct-platform-media-url"
      }
    ]
  }
}
```

If we can't get direct media URLs from the platform endpoint, `extraData` is `null`.

<Note>
  Current YouTube history import returns `extraData: null`.
</Note>

***

## Handling Rate Limits

If a job hits `RATE_LIMITED`, don't panic. It means we hit the platform's cap (e.g. LinkedIn API limits).

* We automatically pause the job.
* We set a `rateLimitResetAt` timestamp.
* You can retry it after that time.

***

## Need More?

We're flexible with import requirements. If you have a specific use case - bulk historical imports, custom date ranges, or higher volume needs-[contact us](https://bundle.social/contact). We'll work with you to find a solution.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
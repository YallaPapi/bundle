> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Google Business Reviews

> Import, sync, and reply to Google Business reviews with an async job flow.

Google Business reviews are handled through an async import flow. You queue an import, poll status, then work with normalized review records in our API.

## How it works

This is an **asynchronous** job, same idea as Post History Import:

1. **Start:** Trigger an import ("Fetch 50 reviews for this location").
2. **Wait:** We fetch from Google and process the batch.
3. **Poll:** Check import status.
4. **Fetch:** Read imported reviews from the reviews endpoint.
5. **Reply:** Create/update/delete owner replies.

***

## Step 1: Start the Import

**Endpoint:** `POST /api/v1/misc/google-business/reviews/import`

```json theme={null}
{
  "teamId": "team_123",
  "count": 50
}
```

### Rules & Limits

* **`count` range:** `1-250` per request. `count` is the number of **new** reviews to import: reviews you already have are refreshed but don't count, so re-running an import continues into older reviews until it has `count` new ones or Google has no more.
* **Only new reviews use up the monthly limit.** Re-fetched reviews are free.
* **One active import per social account:** if one is already running, you'll get `409`.
* **Monthly limit per social account (default):**
  * **Free:** 5 reviews / month
  * **Pro:** 200 reviews / month
  * **Business:** 200 reviews / month

<Note>
  These are defaults. Organizations can have custom review-import limits configured.
</Note>

<Important>
  You need a connected Google Business social account with a selected location. No location = no review import.
</Important>

***

## Step 2: Check Import Status

**Endpoints:**

* `GET /api/v1/misc/google-business/reviews/import?teamId=team_123`
* `GET /api/v1/misc/google-business/reviews/import/:importId`

The list endpoint returns up to 20 latest imports for that team/location, newest first.

### Statuses

* `PENDING`: Waiting in queue.
* `FETCHING_REVIEWS`: Import is running.
* `COMPLETED`: Finished.
* `FAILED`: Import failed after retries.
* `RATE_LIMITED`: Temporarily paused due to API/rate pressure; resumes automatically after `rateLimitResetAt`.

Example import object:

```json theme={null}
{
  "id": "imp_abc123",
  "teamId": "team_123",
  "socialAccountId": "sa_123",
  "requestedCount": 50,
  "status": "FETCHING_REVIEWS",
  "reviewsImported": 24,
  "error": null,
  "rateLimitResetAt": null,
  "startedAt": "2026-02-17T10:00:00.000Z",
  "completedAt": null,
  "createdAt": "2026-02-17T09:59:55.000Z",
  "updatedAt": "2026-02-17T10:00:08.000Z",
  "deletedAt": null
}
```

***

## Step 3: Fetch Imported Reviews

**Endpoints:**

* `GET /api/v1/misc/google-business/reviews?teamId=team_123&limit=50&offset=0`
* `GET /api/v1/misc/google-business/reviews/:reviewId?teamId=team_123`

### Query Parameters (`GET /reviews`)

| Parameter | Type | Default | Description |
| :- | :- | :- | :- |
| `teamId` | string | required | Team ID |
| `limit` | number | `50` | Page size (`1-100`) |
| `offset` | number | `0` | Pagination offset |

Example response:

```json theme={null}
{
  "reviews": [
    {
      "id": "rev_123",
      "socialAccountId": "sa_123",
      "teamId": "team_123",
      "externalReviewId": "accounts/123/locations/456/reviews/789",
      "reviewerDisplayName": "Jane Doe",
      "reviewerProfilePhotoUrl": "https://lh3.googleusercontent.com/...",
      "starRating": "FIVE",
      "comment": "Amazing service, will come back!",
      "reviewReplyComment": "Thanks a lot for your feedback!",
      "reviewReplyUpdatedAt": "2026-02-17T12:15:00.000Z",
      "createTime": "2026-02-16T18:22:00.000Z",
      "updateTime": "2026-02-17T12:15:00.000Z",
      "importedAt": "2026-02-17T12:15:02.000Z",
      "createdAt": "2026-02-17T12:15:02.000Z",
      "updatedAt": "2026-02-17T12:15:02.000Z",
      "deletedAt": null
    }
  ],
  "total": 1,
  "limit": 200,
  "remainingCapacity": 176
}
```

`starRating` values: `ONE`, `TWO`, `THREE`, `FOUR`, `FIVE`.

`limit` in this response is your monthly import cap for that social account (not the page size).

***

## Step 4: Reply to Reviews

### Create or Update Reply

**Endpoint:** `PUT /api/v1/misc/google-business/reviews/:reviewId/reply`

```json theme={null}
{
  "teamId": "team_123",
  "comment": "Thank you for visiting us!"
}
```

`comment` length: `1-4096` chars.

### Delete Reply

**Endpoint:** `DELETE /api/v1/misc/google-business/reviews/:reviewId/reply`

```json theme={null}
{
  "teamId": "team_123"
}
```

Both endpoints return the updated review object.

***

## Quirks & Gotchas

### Incremental Sync (No Duplicate Spam)

Re-running imports is safe. Reviews are upserted by external review ID, so existing reviews are updated instead of duplicated.

To get a location's full history, run imports until `reviewsImported` comes back lower than `count` (Google has nothing older). Once you have every review, later imports only fetch what's new since the last one.

### Overlap Window for Edits

Imports intentionally overlap recent data to catch delayed edits/reply updates from Google. So yes, some recently imported reviews may be re-processed. They're refreshed for free and don't count toward `count` or the monthly limit.

### Temporary `RATE_LIMITED` Is Normal

When Google slows things down, imports switch to `RATE_LIMITED` and auto-resume. No manual retry endpoint needed for this path.

### Capacity Is Per Social Account

`remainingCapacity` is calculated per connected Google Business social account, not globally across all accounts.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
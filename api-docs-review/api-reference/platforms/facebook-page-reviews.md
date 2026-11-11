> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Facebook Page Reviews

> Import, sync, and reply to Facebook Page reviews with an async job flow.

Facebook Page Reviews are handled through an async import flow. You queue an import, poll status, then work with normalized review records in our API.

<Note>
  Facebook calls Page reviews **recommendations** in parts of its API. That is why these endpoints use `/recommendations`, even though this guide calls the feature Facebook Page Reviews.
</Note>

## How it works

This is an **asynchronous** job, same idea as Google Business Reviews:

1. **Start:** Trigger an import ("Fetch 50 reviews for this Page").
2. **Wait:** We fetch from Facebook and process the batch.
3. **Poll:** Check import status.
4. **Fetch:** Read imported reviews from the recommendations endpoint.
5. **Reply:** Reply to the review or to comments inside the recommendation thread.

***

## Step 1: Start the Import

**Endpoint:** `POST /api/v1/misc/facebook/recommendations/import`

```json theme={null}
{
  "teamId": "team_123",
  "count": 50
}
```

### Rules & Limits

* **`count` range:** `1-250` per request.
* **One active import per social account:** if one is already running or recently completed, you'll get `409`.
* **Monthly limit per social account (default):**
  * **Free:** 5 reviews / month
  * **Pro:** 200 reviews / month
  * **Business:** 200 reviews / month

<Note>
  These are defaults. Organizations can have custom review-import limits configured.
</Note>

<Important>
  You need a connected Facebook social account with a selected Page. No Page = no review import.
</Important>

***

## Step 2: Check Import Status

**Endpoints:**

* `GET /api/v1/misc/facebook/recommendations/import?teamId=team_123`
* `GET /api/v1/misc/facebook/recommendations/import/:importId`

The list endpoint returns up to 20 latest imports for that team/Page, newest first.

### Statuses

* `PENDING`: Waiting in queue.
* `FETCHING_RECOMMENDATIONS`: Import is running.
* `COMPLETED`: Finished.
* `FAILED`: Import failed after retries.
* `RATE_LIMITED`: Temporarily paused due to API/rate pressure; resumes automatically after `rateLimitResetAt`.

Example import object:

```json theme={null}
{
  "id": "imp_fb_abc123",
  "teamId": "team_123",
  "socialAccountId": "sa_123",
  "requestedCount": 50,
  "status": "FETCHING_RECOMMENDATIONS",
  "itemsImported": 24,
  "error": null,
  "rateLimitResetAt": null,
  "startedAt": "2026-04-27T10:00:00.000Z",
  "completedAt": null,
  "createdAt": "2026-04-27T09:59:55.000Z",
  "updatedAt": "2026-04-27T10:00:08.000Z",
  "deletedAt": null
}
```

***

## Step 3: Fetch Imported Reviews

**Endpoints:**

* `GET /api/v1/misc/facebook/recommendations?teamId=team_123&limit=50&offset=0`
* `GET /api/v1/misc/facebook/recommendations/:recommendationId?teamId=team_123`

### Query Parameters (`GET /recommendations`)

| Parameter | Type | Default | Description |
| :- | :- | :- | :- |
| `teamId` | string | required | Team ID |
| `limit` | number | `50` | Page size (`1-100`) |
| `offset` | number | `0` | Pagination offset |

Example response:

```json theme={null}
{
  "recommendations": [
    {
      "id": "rec_123",
      "socialAccountId": "sa_123",
      "teamId": "team_123",
      "externalRecommendationId": "1234567890",
      "openGraphStoryId": "9876543210",
      "reviewerDisplayName": "Jane Doe",
      "reviewerProfilePhotoUrl": "https://platform-lookaside.fbsbx.com/...",
      "recommendationValue": "RECOMMEND",
      "rating": null,
      "comment": "Great service and very fast support.",
      "hasMedia": false,
      "mediaSummary": [],
      "ownerReplyComment": "Thanks a lot for your feedback!",
      "ownerReplyCommentId": "comment_123",
      "ownerReplyUpdatedAt": "2026-04-27T12:15:00.000Z",
      "createTime": "2026-04-26T18:22:00.000Z",
      "updateTime": "2026-04-27T12:15:00.000Z",
      "importedAt": "2026-04-27T12:15:02.000Z",
      "createdAt": "2026-04-27T12:15:02.000Z",
      "updatedAt": "2026-04-27T12:15:02.000Z",
      "deletedAt": null
    }
  ],
  "total": 1,
  "limit": 200,
  "remainingCapacity": 176
}
```

`recommendationValue` values: `RECOMMEND`, `NOT_RECOMMEND`, `UNKNOWN`.

`limit` in this response is your monthly import cap for that social account (not the page size).

***

## Step 4: Reply to Reviews

### Reply to a Review

**Endpoint:** `PUT /api/v1/misc/facebook/recommendations/:recommendationId/reply`

```json theme={null}
{
  "teamId": "team_123",
  "comment": "Thank you for visiting us!"
}
```

`comment` length: `1-4096` chars.

This creates a Facebook comment on the Page review story and stores it as `ownerReplyComment`.

### Fetch Thread Comments

**Endpoint:** `GET /api/v1/misc/facebook/recommendations/:recommendationId/comments?teamId=team_123`

```json theme={null}
{
  "comments": [
    {
      "id": "comment_123",
      "recommendationId": "rec_123",
      "rootObjectId": "9876543210",
      "parentCommentId": null,
      "authorName": "Jane Doe",
      "authorExternalId": "fb_user_123",
      "authorAvatarUrl": "https://platform-lookaside.fbsbx.com/...",
      "text": "One more detail from the customer.",
      "likesCount": 2,
      "repliesCount": 1,
      "canReply": true,
      "createdTime": "2026-04-27T13:00:00.000Z"
    }
  ],
  "total": 1
}
```

### Reply to a Thread Comment

**Endpoint:** `PUT /api/v1/misc/facebook/recommendations/:recommendationId/comments/:commentId/reply`

```json theme={null}
{
  "teamId": "team_123",
  "comment": "Happy to help!"
}
```

Response:

```json theme={null}
{
  "id": "reply_comment_123"
}
```

***

## Quirks & Gotchas

### Reviews Are Recommendations

Facebook's native model is recommendation-based, not star-review-based. Some records may have `rating: null`; use `recommendationValue` as the primary signal.

### Some Reviews Cannot Be Replied To

Replies require `openGraphStoryId`. If Facebook does not expose it for a review, reply and thread endpoints return an error instead of pretending the action worked.

### Incremental Sync

Re-running imports is safe. Reviews are upserted by external recommendation ID, so existing records are updated instead of duplicated.

### Temporary `RATE_LIMITED` Is Normal

When Facebook slows things down, imports switch to `RATE_LIMITED` and auto-resume. No manual retry endpoint needed for this path.

### Capacity Is Per Social Account

`remainingCapacity` is calculated per connected Facebook social account, not globally across all accounts.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
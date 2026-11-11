> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Comments

> Import comments from published posts, show them in your app, and reply in the right thread.

<Note>
  Comment import works for posts published through bundle.social and for posts returned by [Post History Import](/api-reference/import-posts). Use exactly one of `postId` or `importedPostId`.
</Note>

With the Comments API you can:

* import comments from a published post,
* display comments as a real thread,
* reply to imported comments on the original platform,
* keep your comments list fresh after new activity.

## Supported Platforms

Comment import is available for:

* `FACEBOOK`
* `INSTAGRAM`
* `LINKEDIN`
* `YOUTUBE`
* `TIKTOK`
* `REDDIT`
* `THREADS`
* `MASTODON`
* `BLUESKY`

Comment creation is available for:

* `FACEBOOK`
* `INSTAGRAM`
* `LINKEDIN`
* `YOUTUBE`
* `TIKTOK`
* `REDDIT`
* `THREADS`
* `MASTODON`
* `DISCORD`
* `SLACK`
* `BLUESKY`

<Note>
  Twitter / X is intentionally not supported in the Comments API. Pinterest and Google Business are not supported for comment creation or comment import.
</Note>

### Comment Text Limits

| Platform | Field | Limit |
| :- | :- | :- |
| `FACEBOOK` | `data.FACEBOOK.text` | 8,000 characters |
| `INSTAGRAM` | `data.INSTAGRAM.text` | 2,200 characters |
| `LINKEDIN` | `data.LINKEDIN.text` | 1,250 characters |
| `YOUTUBE` | `data.YOUTUBE.text` | 10,000 characters |
| `TIKTOK` | `data.TIKTOK.text` | 150 characters |
| `REDDIT` | `data.REDDIT.text` | 10,000 characters |
| `THREADS` | `data.THREADS.text` | 500 characters |
| `MASTODON` | `data.MASTODON.text` | 500 characters |
| `DISCORD` | `data.DISCORD.text` | 2,000 characters |
| `SLACK` | `data.SLACK.text` | 30,000 characters |
| `BLUESKY` | `data.BLUESKY.text` | 30,000 characters |

***

## Before You Start

Use this quick checklist first:

1. You already connected a social account to the team.
2. The post was published through bundle.social or fetched through Post History Import.
3. You have:
   * `teamId`
   * `postId` or `importedPostId`
   * `socialAccountType`

If one of these is missing, import will fail with validation error.

***

## Flow of comments API

Think about import as a small background job:

1. User clicks "Import comments".
2. Your app starts the import job on bundle.
3. Your app checks status every 5/10 seconds.
4. When completed, your app fetches comments and renders the thread.

### Step 1: Start Import

**Endpoint:** `POST /api/v1/comment/import`

```json theme={null}
{
  "teamId": "team_123",
  "importedPostId": "profile_post_123",
  "socialAccountType": "INSTAGRAM"
}
```

`postId` and `importedPostId` are mutually exclusive. Send `postId` for a post created in bundle.social, or `importedPostId` for a historical post returned by the import API.

### Why Import Can Be Rejected

Import start can return validation errors if:

* post does not belong to this team,
* post is not published to selected platform yet,
* this team has no connected account for that platform,
* there is already an active import for this same post and platform.

If import is already running, you get `409`.

### Step 2: Track Progress

**Endpoints:**

* `GET /api/v1/comment/import?teamId=...&postId=...`
* `GET /api/v1/comment/import?teamId=...&importedPostId=...`
* `GET /api/v1/comment/import/:importId`

Use these statuses for user-facing UI:

| Status | What to show to user |
| :- | :- |
| `PENDING` | "Waiting in queue" |
| `FETCHING` | "Importing comments..." |
| `RETRYING` | "Retrying after temporary issue" |
| `RATE_LIMITED` | "Platform limit reached. We will retry automatically." |
| `COMPLETED` | "Import complete" |
| `FAILED` | "Import failed. Try again later." |
| `SKIPPED` | "Import skipped" |

### Step 3: Get Imported Comments

**Endpoint:** `GET /api/v1/comment/import/comments`

Query params:

* `teamId` (required)
* exactly one of `postId` or `importedPostId` (required)
* `platform` (optional)
* `socialAccountId` (optional)
* `limit`, `offset`

Example response:

```json theme={null}
{
  "items": [
    {
      "id": "fetched_1",
      "platform": "INSTAGRAM",
      "externalId": "18001234567890",
      "externalParentId": null,
      "text": "Top level comment",
      "authorName": "janedoe",
      "likesCount": 12,
      "repliesCount": 2,
      "publishedAt": "2026-04-13T09:30:00.000Z"
    },
    {
      "id": "fetched_2",
      "platform": "INSTAGRAM",
      "externalId": "18001234567999",
      "externalParentId": "18001234567890",
      "text": "Reply comment",
      "authorName": "bundle_user",
      "likesCount": 1,
      "repliesCount": 0,
      "publishedAt": "2026-04-13T09:35:00.000Z"
    }
  ],
  "total": 2
}
```

***

## What Exactly Gets Imported

Each imported comment includes:

* `externalId`: unique platform comment ID.
* `externalParentId`: parent comment ID on platform, or `null` for top-level.
* `externalPostId`: platform post ID.
* author metadata: `authorName`, `authorExternalId`, `authorProfileUrl`, `authorAvatarUrl`.
* content and stats: `text`, `likesCount`, `repliesCount`, `publishedAt`.

Important detail:

* the API returns a flat list,
* your app rebuilds thread hierarchy using `externalParentId`.

***

## How To Display Comments In Your App

### Plain-Language Rule

If `externalParentId` is empty, this is top-level comment.
If `externalParentId` points to another `externalId`, this is a reply.

### Recommended Rendering Steps

1. Create `externalId -> comment` map.
2. Group comments by `externalParentId`.
3. Start from root comments.
4. Attach children recursively.

```ts theme={null}
type C = { externalId: string; externalParentId: string | null };

function buildTree(comments: C[]) {
  const byId = new Map(comments.map((c) => [c.externalId, c]));
  const byParent = new Map<string | null, C[]>();

  for (const c of comments) {
    const arr = byParent.get(c.externalParentId) ?? [];
    arr.push(c);
    byParent.set(c.externalParentId, arr);
  }

  const roots = comments.filter((c) => c.externalParentId === null || !byId.has(c.externalParentId));

  const visit = (node: C): any => ({
    ...node,
    children: (byParent.get(node.externalId) ?? []).map(visit),
  });

  return roots.map(visit);
}
```

<Note>
  Sometimes platform APIs do not return full parent mapping for every nested reply. If parent is missing, treat this comment as root and still show it.
</Note>

***

## Replying To Imported Comments

To reply to imported comment, create normal comment with `fetchedParentCommentId`.

**Endpoint:** `POST /api/v1/comment`

Minimal body:

```json theme={null}
{
  "teamId": "team_123",
  "fetchedParentCommentId": "fetched_1",
  "text": "Thanks for your comment!"
}
```

### What Happens After You Send Reply

1. API resolves correct platform and post from fetched parent.
2. New comment is saved with `SCHEDULED` status.
3. Queue publishes it to platform.
4. Status becomes `POSTED` or `ERROR`.

## Creating A Top-Level Comment

For first comments or top-level comments on a post published through bundle.social, provide the post, schedule fields, target platforms, and platform-specific comment text.

**Endpoint:** `POST /api/v1/comment`

```json theme={null}
{
  "teamId": "team_123",
  "internalPostId": "post_123",
  "title": "First comment",
  "status": "SCHEDULED",
  "postDate": "2026-06-01T15:05:00.000Z",
  "socialAccountTypes": ["INSTAGRAM"],
  "data": {
    "INSTAGRAM": {
      "text": "Link is in the bio. Thanks for watching!"
    }
  }
}
```

For `internalParentCommentId`, the reply is linked to a comment already created through bundle.social. For `fetchedParentCommentId`, the platform and post are inferred from the imported comment, so a minimal reply can use only `teamId`, `fetchedParentCommentId`, and `text`.

For a top-level comment on a historical post, replace `internalPostId` with `importedPostId`. Do not send both fields.

## List Created Comments

**Endpoint:** `GET /api/v1/comment`

`teamId` is required. Optional filters include `postId`, `importedPostId`, `status`, `q`, `platforms`, `orderBy`, `order`, `offset`, and `limit`. Use this endpoint for comments created through bundle.social; use `/comment/import/comments` for comments fetched from a platform.

## Actions On Fetched Comments

**Endpoint:** `POST /api/v1/comment/import/comments/:commentId/action`

```json theme={null}
{
  "teamId": "team_123",
  "action": "HIDE",
  "reason": "Optional moderation note"
}
```

Available actions depend on the platform and the permissions reported in `platformData`:

| Platform | Actions |
| :- | :- |
| Facebook, Instagram | `DELETE`, `HIDE`, `UNHIDE` |
| LinkedIn, Mastodon | `DELETE`, `LIKE`, `UNLIKE` |
| YouTube, Reddit | `DELETE`, `APPROVE`, `REJECT` |
| TikTok | `DELETE`, `HIDE`, `UNHIDE`, `LIKE`, `UNLIKE` |
| Bluesky | `DELETE` |
| Threads | No fetched-comment actions |

Check `platformData.canDelete`, `canHide`, `canLike`, and `canModerate` before showing controls. The platform can still reject an action if the connected account does not own or moderate the target comment.

For YouTube `APPROVE` or `REJECT`, optional `banAuthor: true` asks YouTube to ban the comment author as part of the moderation action.

## Retry A Failed Comment

**Endpoint:** `POST /api/v1/comment/:id/retry`

Use this for a comment whose status is `ERROR`. A successful retry returns the comment to the publishing queue. Comments in any other status return `400`.

## Limits Explained

### Per Import Storage Limit (Per Post)

Import always runs, but stored comments are capped for each run.

| Tier | Max stored comments per post import |
| :- | :- |
| FREE | 25 |
| PRO | 200 |
| BUSINESS | 1000 |

How this works in practice:

* if platform has 900 comments and your cap is 200,
* import completes successfully,
* newest 200 are stored in this run.

### Is There a Monthly Comment Import Quota?

No.

Comment import does not use monthly counters. Limit is per run and per post.

### Reply Text Limits By Platform

| Platform | Max text length |
| :- | :- |
| FACEBOOK | 8000 |
| INSTAGRAM | 2200 |
| LINKEDIN | 1250 |
| YOUTUBE | 10000 |
| TIKTOK | 150 |
| REDDIT | 10000 |
| THREADS | 500 |
| MASTODON | 500 |
| BLUESKY | 30000 |

***

For global API rate limits, see [Rate Limits](/api-reference/rate-limits).

***

## Quick FAQ

### "Why comments list is empty?"

Most common reasons:

* post was not published to selected platform,
* import still running,
* no comments yet on that post.

### "Why does creating a comment fail?"

* `404 Post not found or does not belong to this team` - the `internalPostId` doesn't exist, belongs to another team, or the post was deleted.
* `Post is not published on <platform> yet` - a top-level comment needs the published post. Wait until the post is `POSTED` (or reply to an existing comment instead).
* `No text provided to create comment` - the comment has no text for that platform.
* `Slack/Discord channel for this post is unknown` - replying to an imported Slack or Discord post isn't supported, since the import doesn't carry its channel.

### "Why I see comment without parent?"

Because parent mapping from platform was not returned in this fetch window. Show as root and keep it visible.

### "Do I need webhooks for comment import?"

No. Comment import is pull-based. You trigger it and then fetch results.

### "Will you have webhooks for this?"

For live comment nortification? No, kinda not our limitation.
For import status, yes in the future.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
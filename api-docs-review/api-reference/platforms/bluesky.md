> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Bluesky

> The AT Protocol. Calculated impressions, limited data, but growing fast.

Bluesky is the new decentralized challenger, built on the AT Protocol. It's growing fast but the API is still maturing when it comes to analytics.

## Supported Content Types

* **Posts:** Text with optional media. Up to 4 files.
* **Text limit:** 300 characters.

## Quirks & Gotchas

### "Calculated" Impressions

Bluesky does not provide a native "Impression" or "View" count for posts via API.

* **Our Solution:** We calculate `impressions` as the sum of engagement (Likes + Replies + Reposts + Quotes).
* **Reality:** The actual number of people who saw it is likely much higher, but we can't prove it. Think of it as a minimum engagement indicator, not true impressions.

### Limited But Growing

Bluesky's API is young. As the platform and protocol mature, we expect more analytics data to become available. We'll add it when it does.

### Media Limits

| Constraint | Value |
| :- | :- |
| Files | 0-4 (images and/or videos) |
| Text | 300 characters |

Bluesky has minimal media restrictions compared to other platforms. See [Platform Limits](/api-reference/limits#bluesky) for details.

### Video Upload Eligibility

Bluesky decides per account whether it may upload videos. Before every video upload we ask Bluesky for the account's upload limits, so a refusal comes back with Bluesky's own reason instead of a bare `http_401`:

| Error | What it means | Fix |
| :- | :- | :- |
| "Bluesky does not allow this account to upload videos: …" | Bluesky refuses video for this account. The most common cause is an **unverified email**. Not retried. | Verify the account's email in the Bluesky app (Settings → Account), then retry the post. Reconnecting doesn't help. |
| "Bluesky daily video upload limit reached for this account: …" | The account used its daily video allowance. Retried later. | Wait for the daily limit to reset, or post fewer videos per day from this account. |

Image and text posts are not affected.

### Text & Field Limits

| Field | Limit |
| :- | :- |
| `text` | Max 300 characters |
| `tags` | Up to 8 tags, max 64 chars each |
| `externalTitle` | Max 300 characters |
| `externalDescription` | Max 1,000 characters |
| `externalUrl` | Max 2,048 characters |
| `videoAlt` | Max 10,000 characters |

***

## Post Options

Send Bluesky-specific options inside `data.BLUESKY`.

| Field | Type | Description |
| :- | :- | :- |
| `text` | `string` | Post text. Max 300 characters. |
| `uploadIds` | `string[]` | Up to 4 uploaded media files. |
| `tags` | `string[]` | Extra hashtags without `#`. Up to 8 tags, max 64 characters each. |
| `labels` | `enum[]` | Self-labels: `!no-unauthenticated`, `porn`, `sexual`, `nudity`, `graphic-media`. |
| `quoteUri` | `string` | AT-URI of a post to quote, for example `at://did.../app.bsky.feed.post/<rkey>`. |
| `externalUrl` | `string` | URL for an external link card. |
| `externalTitle` | `string` | Link card title. Max 300 characters. |
| `externalDescription` | `string` | Link card description. Max 1,000 characters. |
| `thumbnail` | `string` | Optional bundle.social upload URL for the external link card image. Requires `externalUrl`. |
| `videoAlt` | `string` | Alt text for the video embed. Max 10,000 characters. |

```json theme={null}
{
  "teamId": "team_123",
  "title": "Bluesky link card",
  "status": "SCHEDULED",
  "postDate": "2026-06-01T15:00:00.000Z",
  "socialAccountTypes": ["BLUESKY"],
  "data": {
    "BLUESKY": {
      "text": "New release notes are live",
      "tags": ["release", "product"],
      "externalUrl": "https://example.com/release-notes",
      "externalTitle": "Release notes",
      "externalDescription": "What shipped this week.",
      "thumbnail": "https://storage.bundle.social/path/to/uploaded-card-image.jpg"
    }
  }
}
```

<Note>
  When `thumbnail` is provided, `externalUrl` is required. The thumbnail must be a public URL returned by a completed bundle.social upload.
</Note>

***

## Analytics

For general analytics concepts (refresh rates, data retention, what "Returns 0" means), see the [Analytics Overview](/api-reference/analytics).

### Profile Analytics

**Period:** Snapshot.

| Metric | Description | Note |
| :- | :- | :- |
| `impressions` | - | Returns `0` (not available) |
| `impressionsUnique` | - | Returns `0` (not available) |
| `views` | - | Returns `0` (not available) |
| `viewsUnique` | - | Returns `0` (not available) |
| `likes` | - | Returns `0` (not available at profile level) |
| `comments` | - | Returns `0` (not available at profile level) |
| `postCount` | Total posts | |
| `followers` | Followers | |
| `following` | Following | |

### Post Analytics

**Period:** Lifetime.

| Metric | Description | Note |
| :- | :- | :- |
| `impressions` | Engagement Sum | Calculated: Likes + Replies + Reposts + Quotes |
| `impressionsUnique` | - | Returns `0` (not provided) |
| `views` | - | Same as impressions (calculated) |
| `viewsUnique` | - | Returns `0` (not provided) |
| `likes` | Likes | |
| `comments` | Replies | |
| `shares` | Reposts + Quotes | Combined |
| `saves` | - | Returns `0` (not available) |

### Quirks

* No true impression or view metrics. We derive impressions from total engagement - it's the best we can do.
* Profile-level engagement is not available. Only follower/following counts and post count.
* As Bluesky's API evolves, we'll add new metrics as they become available.

### Raw Analytics

Bluesky profile raw analytics store the actor profile payload.

```json theme={null}
{
  "profile": {
    "did": "did:plc:abc123",
    "handle": "example.bsky.social",
    "displayName": "Example",
    "followersCount": 4200,
    "followsCount": 310,
    "postsCount": 180
  }
}
```

Bluesky post raw analytics store the post object returned by AT Protocol.

```json theme={null}
{
  "post": {
    "uri": "at://did:plc:abc123/app.bsky.feed.post/3kabc",
    "cid": "bafy...",
    "author": {
      "handle": "example.bsky.social"
    },
    "likeCount": 120,
    "replyCount": 18,
    "repostCount": 34,
    "quoteCount": 7
  }
}
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Mastodon

> The decentralized social web. Basic metrics only, but at least it's open source.

Mastodon is part of the Fediverse. It's decentralized, which means "analytics" is a loose concept. Each instance runs independently, and there's no central authority tracking impressions or views.

## Supported Content Types

* **Toots (Posts):** Text with optional media. Up to 4 files.
* Mixed images and videos allowed, but only 1 video max.

## Quirks & Gotchas

### Terminology

* **Likes** = **Favourites** (British spelling, because Mastodon).
* **Shares** = **Reblogs** (like retweets, but federated).
* **Posts** = **Toots** (or "statuses" in the API, because naming things is hard).

### Character Limits

Character limits are **instance-dependent** - most instances default to 500, but some allow more. We can't know in advance what your user's instance allows.

### Media Limits

| Constraint | Value |
| :- | :- |
| Files | 0-4 (images and/or videos, mixed allowed) |
| Max videos | 1 |
| Video max size | 99 MB |
| Video aspect ratio | 1:3 to 1:1 |
| Max images | 4 |
| Image max size | 16 MB each |

See [Platform Limits](/api-reference/limits#mastodon) for more details.

### Text & Field Limits

| Field | Limit |
| :- | :- |
| `text` | Max 30,000 characters |
| `spoiler` | Max 50 characters |

***

## Post Options

Send Mastodon-specific options inside `data.MASTODON`.

| Field | Type | Description |
| :- | :- | :- |
| `text` | `string` | Status text. Instance limits vary; bundle.social accepts up to 30,000 characters. |
| `uploadIds` | `string[]` | Up to 4 uploaded media files. Only 1 video is allowed. |
| `thumbnail` | `string` | Optional thumbnail image URL uploaded through bundle.social. |
| `privacy` | `enum` | `PUBLIC`, `UNLISTED`, `PRIVATE`, or `DIRECT`. |
| `spoiler` | `string` | Content warning text. Max 50 characters. |

```json theme={null}
{
  "teamId": "team_123",
  "title": "Mastodon update",
  "status": "SCHEDULED",
  "postDate": "2026-06-01T15:00:00.000Z",
  "socialAccountTypes": ["MASTODON"],
  "data": {
    "MASTODON": {
      "text": "Shipping a small but useful update today.",
      "privacy": "PUBLIC",
      "spoiler": "Product update"
    }
  }
}
```

***

## Analytics

For general analytics concepts (refresh rates, data retention, what "Returns 0" means), see the [Analytics Overview](/api-reference/analytics).

Mastodon has very limited analytics capabilities. Being decentralized means there's no central tracking of impressions or views.

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
| `postCount` | Total toots | |
| `followers` | Followers | |
| `following` | Following | |

### Post Analytics

**Period:** Lifetime.

| Metric | Description | Note |
| :- | :- | :- |
| `impressions` | - | Returns `0` (not available) |
| `impressionsUnique` | - | Returns `0` (not available) |
| `views` | - | Returns `0` (not available) |
| `viewsUnique` | - | Returns `0` (not available) |
| `likes` | Favourites | |
| `comments` | Replies | |
| `shares` | Reblogs | |
| `saves` | - | Returns `0` (not available) |

### Quirks

* No impression or view metrics. The Fediverse doesn't track eyeballs the way corporate social media does.
* Only basic engagement metrics (favourites, replies, reblogs) are available per post.
* Profile-level engagement is not aggregated by Mastodon's API.
* This is by design, not a bug. Privacy-focused platform = limited tracking.

### Raw Analytics

Mastodon profile raw analytics store the account payload we fetched from the instance.

```json theme={null}
{
  "id": "10987654321",
  "username": "example",
  "acct": "example@mastodon.social",
  "display_name": "Example",
  "statuses_count": 240,
  "followers_count": 1800,
  "following_count": 220
}
```

Mastodon post raw analytics store the status payload.

```json theme={null}
{
  "id": "1122334455",
  "url": "https://mastodon.social/@example/1122334455",
  "content": "<p>Shipping a small update today.</p>",
  "replies_count": 12,
  "reblogs_count": 34,
  "favourites_count": 91,
  "created_at": "2026-04-26T10:30:00.000Z"
}
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
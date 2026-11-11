> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Reddit

> The front page of the internet. Minimalist analytics, maximum subreddit rules.

Reddit is a collection of communities, each with its own rules. The API is functional but stingy with data - especially analytics.

## Supported Content Types

* **Text Posts:** Title + text. Title is required.
* **Link Posts:** Title + URL.
* **Image Posts:** 1 image, or gallery (up to 10 images if the subreddit allows).
* **Video Posts:** 1 video.

## Quirks & Gotchas

### Subreddit Rules are King

Each subreddit has its own rules about what's allowed:

* Some subreddits don't allow media at all.
* Some allow images but not galleries.
* Some require flairs.
* We validate against subreddit settings before posting. If it's not allowed, you get a clear error.

### Engagement Terminology

* **Likes** = **Upvotes**
* **Dislikes** = **Downvotes**
* **Shares** = **Crossposts**

Reddit does not track "Impressions" or "Reach" the way marketers want. If that's a dealbreaker, you're on the wrong platform.

### Media Limits

| Constraint | Value |
| :- | :- |
| **Single post** | 0-1 file (image or video) |
| Video max size | 1 GB |
| Video aspect ratio | 9:16 to 16:9 |
| Video duration | 4s - 15 min |
| Image max size | 20 MB |
| **Gallery** | 0-10 images (if subreddit allows) |
| Gallery image max size | 20 MB each |

See [Platform Limits](/api-reference/limits#reddit) for more details.

### Text & Field Limits

| Field | Limit |
| :- | :- |
| `text` (title) | Max 300 characters |
| `description` | Max 30,000 characters |
| `link` | Max 2,048 characters |

***

## Post Options

Send Reddit-specific options inside `data.REDDIT`.

| Field | Type | Description |
| :- | :- | :- |
| `sr` | `string` | Required. Subreddit name such as `r/productivity` or profile target such as `u/username`. |
| `text` | `string` | Required. Reddit post title. Max 300 characters. |
| `description` | `string` | Body text for text posts. Max 30,000 characters. |
| `uploadIds` | `string[]` | Media attachments. One image/video for media posts, or up to 10 images for galleries if the subreddit allows it. |
| `link` | `string` | URL for link posts. Max 2,048 characters. |
| `nsfw` | `boolean` | Marks the post as NSFW. Default: `false`. |
| `flairId` | `string` | Flair ID. Required when the subreddit requires a flair. |

```json theme={null}
{
  "teamId": "team_123",
  "title": "Reddit discussion",
  "status": "SCHEDULED",
  "postDate": "2026-06-01T15:00:00.000Z",
  "socialAccountTypes": ["REDDIT"],
  "data": {
    "REDDIT": {
      "sr": "r/productivity",
      "text": "What changed the most in your planning workflow?",
      "description": "We are collecting practical examples from teams.",
      "nsfw": false,
      "flairId": "flair_123"
    }
  }
}
```

***

## Analytics

For general analytics concepts (refresh rates, data retention, what "Returns 0" means), see the [Analytics Overview](/api-reference/analytics).

### Profile Analytics

**Status:** Not available.

Reddit does not provide profile-level analytics through their API. Everything returns `0`. All of it. Every single metric. Don't ask.

### Post Analytics

**Period:** Lifetime.

| Metric | Description | Note |
| :- | :- | :- |
| `impressions` | - | Returns `0` (not available) |
| `impressionsUnique` | - | Returns `0` (not available) |
| `views` | View count | May not be available for all posts |
| `viewsUnique` | - | Returns `0` (not available) |
| `likes` | Upvotes | |
| `dislikes` | Downvotes | |
| `comments` | Comments | |
| `shares` | Crossposts | |
| `saves` | - | Returns `0` (not available) |

### Quirks

* Reddit has the most limited analytics of any major platform we support.
* No profile-level analytics whatsoever.
* View counts exist for some posts but are not guaranteed.
* No impressions or reach metrics. Reddit's API simply doesn't provide them.
* Upvotes/downvotes are the primary engagement signals.

### Raw Analytics

Reddit profile raw analytics are limited to karma fields.

```json theme={null}
{
  "total_karma": 18420,
  "comment_karma": 6400,
  "awarder_karma": 120
}
```

Reddit post raw analytics store the submission payload returned by Reddit.

```json theme={null}
{
  "id": "abc123",
  "subreddit": "productivity",
  "title": "What changed the most in your planning workflow?",
  "ups": 420,
  "downs": 12,
  "num_comments": 88,
  "num_crossposts": 4,
  "view_count": 12400,
  "permalink": "/r/productivity/comments/abc123/example/"
}
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
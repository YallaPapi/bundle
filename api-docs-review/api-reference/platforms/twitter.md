> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Twitter / X

> It's X now. The API is... well, it exists. Analytics are available on demand, billed from X credits.

The platform formerly known as Twitter. The API changes have been... eventful. Let's focus on what works.

## Billing

Twitter/X is moving to a **usage-based billing model**. X charges for API access to post, and we pass that cost through to you **1:1 - at cost, with no markup**. You pay exactly what X charges us per tweet, nothing more.

<Info>
  We don't add any margin on top of X's API pricing. Every tweet published through bundle.social is billed to your account at the same price X bills us. This is separate from your bundle.social plan.
</Info>

## Supported Content Types

* **Tweets:** Text with optional media. 0-4 files.
* Images and videos can be mixed in the same tweet.

## Quirks & Gotchas

### Media Limits

* Max 4 images per tweet.
* Max 4 videos per tweet (though realistically, 1 is most common).
* Video max size: 512 MB.

### Text & Subscription-Based Limits

Twitter/X limits vary based on the account's subscription tier:

| Tier | Text Limit | Video Duration |
| :- | :- | :- |
| Free | 280 chars | 140s (2:20) |
| Basic | 280 chars | 140s (2:20) |
| Premium | 25,000 chars | 600s (10 min) |
| Premium+ | 25,000 chars | 600s (10 min) |

See [Platform Limits](/api-reference/limits#twitter--x) for the full breakdown.

***

## Post Options

Send X-specific options inside `data.TWITTER`.

| Field | Type | Description |
| :- | :- | :- |
| `text` | `string` | Tweet text. Character limit depends on the account subscription tier. |
| `uploadIds` | `string[]` | Up to 4 uploaded media files. Images and videos can be mixed. |
| `replySettings` | `enum` | Controls who can reply. See the values below. |

```json theme={null}
{
  "teamId": "team_123",
  "title": "X announcement",
  "status": "SCHEDULED",
  "postDate": "2026-06-01T15:00:00.000Z",
  "socialAccountTypes": ["TWITTER"],
  "data": {
    "TWITTER": {
      "text": "Launching today",
      "uploadIds": ["upload_image_123"],
      "replySettings": "MENTIONED_USERS"
    }
  }
}
```

***

## Reply Settings

You can control who's allowed to reply to your tweets. Set `replySettings` in the `data.TWITTER` object when creating a post.

| Value | Who can reply |
| :- | :- |
| `EVERYONE` | Anyone (default) |
| `FOLLOWING` | Only people you follow |
| `MENTIONED_USERS` | Only users mentioned in the tweet |
| `SUBSCRIBERS` | Subscribers only |
| `VERIFIED` | Verified accounts only |

If you don't set `replySettings` or set it to `EVERYONE`, we don't send the parameter to Twitter at all - which is Twitter's default behavior.

```json theme={null}
{
  "data": {
    "TWITTER": {
      "text": "Hot take incoming",
      "replySettings": "MENTIONED_USERS"
    }
  }
}
```

<Note>
  Reply settings depend on your Twitter/X account tier. Some options (like `SUBSCRIBERS`) only make sense if your account actually has subscribers. Twitter won't error out if you use them anyway - it just won't do much.
</Note>

***

## Analytics

Available **on demand only**. X charges for every API read, so we never refresh X analytics in the background. You trigger a refresh yourself, and each one is billed from your prepaid X credits, the same balance used for posting.

| What | Endpoint | Fields |
| :- | :- | :- |
| Profile | `POST /api/v1/analytics/social-account/force` | `followers`, `following`, `postCount` (other metrics return `0`) |
| Post | `POST /api/v1/analytics/post/force` | `impressions`, `likes`, `comments` (replies), `shares` (reposts + quotes), `saves` (bookmarks) |

After a refresh, the data is available through the regular analytics endpoints.

<Note>
  * If your credit balance is too low, the refresh fails with a clear "Not enough credits" error and nothing is charged.
  * Forced refreshes have a daily limit per account and per post, like on every other platform.
  * For your own posts X returns organic metrics (the richer set); if those aren't available we fall back to public metrics.
</Note>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
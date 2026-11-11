> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Rate Limits

> API limits, posting limits, commenting limits, and import quotas. No per-account charges: three layers of rate limiting plus daily caps per platform.

## No Account Limits

bundle.social is a unified social media API built for scale. Unlike other social media management APIs, we don't charge per connected account or punish you for growing. Connect 1 account or 10,000 accounts - same flat pricing. Our API supports Instagram, TikTok, YouTube, Snapchat, Facebook, LinkedIn, Twitter/X, Pinterest, Reddit, Threads, Mastodon, Bluesky, Discord, Slack, and Google Business Profile. Perfect for SaaS platforms, agencies, and enterprise applications that need unlimited social media integrations.

***

## API Rate Limits

We use a multi-layer throttling system to keep things fair and prevent bursts from taking down the ranch. Limits are tracked **per endpoint** and per tracker: **API key** (organization), **bearer token** (user), or **IP** as fallback.

### The Three Layers

| Layer | Window | Max Requests | Theoretical equivalent | What it prevents |
| :- | :- | :- | :- | :- |
| **Burst** | 1 second | 100 | 6,000 / minute | Someone doing `Promise.all()` with 500 requests |
| **Short** | 10 seconds | 500 | 3,000 / minute | Aggressive polling or runaway loops |
| **Minute** | 1 minute | 2,000 | 2,000 / minute | Sustained high-volume abuse |

All three layers are enforced simultaneously. For sustained traffic, the **minute** layer (2,000/min) is the effective cap.

<Note>
  Because limits are per endpoint, heavy traffic on `POST /post` does not consume the same bucket as `GET /analytics` for the same tracker.
</Note>

<Warning>
  **Easy there, cowboy.** If you hit any of these limits, you'll get a `429 Too Many Requests`. Take a breath, wait a moment, and try again. We're not going anywhere.
</Warning>

***

## External Platform Rate Limits

These are **daily limits per connected social account**, counted per **UTC calendar day** by the post's scheduled date. The quota is keyed by the **platform account itself** (platform + account id), not by the connection or the team - so the same real account connected more than once (reconnected, or added to multiple teams) **shares a single quota**.

### Posting daily limits per platform per tier

| Platform | FREE | PRO | BUSINESS |
| - | - | - | - |
| TWITTER | 5 | 15 | 15 |
| FACEBOOK | 10 | 50 | 100 |
| INSTAGRAM | 10 | 50 | 100 |
| LINKEDIN | 10 | 18 | 24 |
| YOUTUBE | 10 | 10 | 15 |
| TIKTOK | 5 | 10 | 15 |
| THREADS | 10 | 200 | 250 |
| PINTEREST | 10 | 24 | 36 |
| REDDIT | 10 | 24 | 36 |
| DISCORD | 10 | 100 | 200 |
| SLACK | 10 | 100 | 200 |
| MASTODON | 10 | 50 | 100 |
| BLUESKY | 10 | 50 | 100 |
| GOOGLE\_BUSINESS | 10 | 20 | 40 |
| SNAPCHAT | 5 | 20 | 40 |

<Note>
  **Example:** On Pro, each connected TikTok account gets its own 10 posts/day. Connect 5 **different** TikTok accounts → 50/day total (10 each, independent). But connect the **same** TikTok account to 5 teams → still 10/day total, because the quota follows the real account, not the connection.
</Note>

### Check Daily Usage For One Account

**Endpoint:** `GET /api/v1/organization/usage/daily-limits`

| Query | Required | Description |
| :- | :- | :- |
| `socialAccountId` | Yes | bundle.social social account ID. |
| `date` | No | Any parseable date or timestamp. Defaults to today; usage is calculated for its UTC calendar day. |

```http theme={null}
GET /api/v1/organization/usage/daily-limits?socialAccountId=sa_123&date=2026-07-12
```

The response includes the UTC `date`, account ID, platform `type`, and separate `posts` and `comments` objects with `used`, `limit`, and `remaining`.

### Commenting daily limits per platform per tier

Daily caps per connected account, per platform, for comments created via the API.

| Platform | FREE | PRO | BUSINESS |
| - | - | - | - |
| FACEBOOK | 3 | 50 | 100 |
| INSTAGRAM | 3 | 50 | 100 |
| LINKEDIN | 3 | 18 | 24 |
| YOUTUBE | 3 | 10 | 15 |
| TIKTOK | 3 | 10 | 15 |
| THREADS | 3 | 200 | 250 |
| REDDIT | 3 | 24 | 36 |
| DISCORD | 3 | 100 | 200 |
| SLACK | 3 | 100 | 200 |
| MASTODON | 3 | 50 | 100 |
| BLUESKY | 3 | 50 | 100 |

<Note>
  Comment creation is currently available for Facebook, Instagram, LinkedIn, YouTube, TikTok, Reddit, Threads, Mastodon, Discord, Slack, and Bluesky. Twitter/X, Pinterest, and Google Business are not supported by the Comments API.
</Note>

### Monthly organization-wide limits

On top of daily limits, there are monthly caps across the entire organization:

| Tier | Monthly Posts | Monthly Comments | Monthly Uploads |
| - | - | - | - |
| FREE | 20 | 50 | 200 |
| PRO | 10,000 | 5,000 | 100,000 |
| BUSINESS | 100,000 | 50,000 | 1,000,000 |

<Note>
  **How the monthly cap is counted:** by **creation time**, in the **UTC calendar month** - i.e. when you *schedule* an item, not when it publishes. Scheduling a post for a future month still consumes the **current** month's quota. Drafts don't count; **failed or deleted items still count** (deleting doesn't refund). The window resets on the 1st of each month (UTC).
</Note>

***

## Import Limits

Limits that apply when importing historical content from connected social accounts.

### Post history imports (monthly, per social account)

Maximum posts imported from each connected social account per month. Counter resets on the 1st of each month (UTC).

| Tier | Posts / account / month |
| - | - |
| FREE | 5 |
| PRO | 100 |
| BUSINESS | 500 |

A single post-history import request is additionally capped at **100 posts** (hard cap, not overridable).

### Comment imports (per post)

Maximum comments stored per post on each import run. Imports always run - the cap just truncates to the newest N comments before storage. No monthly window, no counter.

| Tier | Comments / post / import |
| - | - |
| FREE | 25 |
| PRO | 200 |
| BUSINESS | 1,000 |

### Google review and Facebook recommendation imports (monthly, per social account)

Maximum Google reviews or Facebook Page recommendations imported from each connected social account per month. Counter resets on the 1st of each month (UTC).

| Tier | Reviews or recommendations / account / month |
| - | - |
| FREE | 5 |
| PRO | 200 |
| BUSINESS | 200 |

A single import request is additionally capped at **250 reviews or recommendations** (hard cap, not overridable).


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
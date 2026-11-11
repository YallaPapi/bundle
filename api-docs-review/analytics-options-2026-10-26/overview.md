> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Analytics

> How analytics work, how we refresh them, how long we keep them, and why some numbers are zero. The full picture.

Everything you need to know about analytics before you read the [platform-specific pages](https://info.bundle.social/api-reference/platforms/index.md). This page covers refresh rates, rate limits, data retention, and why some numbers are zero.

For platform-specific metrics and quirks, see each platform's dedicated page.

> [!WARNING]
>
> **Analytics require a paid plan.** The free plan has API access, but not analytics. Every analytics
> endpoint returns `403` with `Analytics access is disabled for your subscription tier.` on the free plan,
> and nothing is collected in the background either - so upgrading later does not backfill the period you
> spent on the free plan. Analytics are included on Pro, Business, and Enterprise.

***

## Analytics Refresh & Rate Limits

### Default Refresh

Analytics are automatically refreshed every **24 hours**. You don't need to run your own refresh job for standard analytics updates.

### Force Refresh

You can request analytics to be refreshed immediately by calling the analytics force refresh endpoints.

| Target | Endpoint | Body |
| :- | :- | :- |
| Social account analytics | `POST /api/v1/analytics/social-account/force` | `{ "teamId": "...", "platformType": "INSTAGRAM" }` |
| Post analytics | `POST /api/v1/analytics/post/force` | `{ "postId": "...", "platformType": "INSTAGRAM" }` |
| Imported post analytics | `POST /api/v1/analytics/post/force` | `{ "importedPostId": "..." }` |

However, force refresh requests are rate limited to **6 per social account** and **6 per post** in any rolling 24 hours.

You may ask why?

To protect US from our greatest and brightest vibe code engineers doing:

```typescript theme={null}
while (true) {
  await bundlesocial.analytics.analyticsForceRefresh({
    teamId: team.id,
  });
}
```

We had such cases. We are not joking. Someone actually did this in production.

> [!NOTE]
>
> **Rate Limits**: Each social account can be force refreshed up to **6 times** in a rolling 24 hours, and each post up to **6 times**. The counters are separate, so refreshing one account doesn't use up another account's or a post's allowance.
>
> A refresh that fails doesn't count against the limit. If you exceed the limit, the API returns `429 Too Many Requests`.
>
> Need more? Reach out and we can raise it for your organization.

### Custom Refresh Periods

By default, analytics are automatically refreshed every **24 hours**. However, we can configure custom refresh periods based on your organization's needs.

**Important**: If you require a higher refresh rate (e.g., every 15 minutes for large organizations), there may be additional charges due to increased data costs.

We will discuss these costs with you directly to determine the best solution for your use case.

***

## Data Retention

We retain analytics data for **30 days** from the date of creation. After that, it's gone. Poof. Deleted.

If your team needs yearly or long-term history, we recommend fetching and storing the data daily on your end. Build a cron job, pipe it to your database, and sleep well at night.

This retention period is fixed and is not extended automatically. Maybe we are evil?

> [!WARNING]
>
> **30 days.** That's it. If you need analytics from 3 months ago and you didn't save them, we can't help you. We told you. Right here. In this doc. That you're reading right now.

For the full breakdown of what we retain and for how long (not just analytics), see [Data Retention](https://info.bundle.social/api-reference/data-retention.md).

***

## Important Note: Data Differences & Zeros

> [!NOTE]
>
> **Data shown in our platform may differ from what you see on the social media platform itself.** This can happen for several reasons:
>
> * **Processing Delays**: Platforms may take time to process and return analytics data. For example, TikTok can take up to 48 hours for some detailed analytics like audience demographics and splits.
>
> * **Rolling Window Timing**: When platforms return rolling window data, the exact time window and aggregation method may differ slightly from what's displayed in their native interfaces.
>
> * **Data Availability**: Some metrics may be available in the platform's native interface but not through their API, or vice versa. APIs and dashboards are built by different teams. At big companies. With different priorities.
>
> * **Update Frequency**: Analytics are updated based on when we fetch data from each platform, which may not match the real-time updates you see in the platform's own interface.
>
> * **Zero Values**: **Some metrics return `0` when the platform API doesn't provide that specific data point.** This doesn't mean you have zero engagement - it means the data is not available through the API. Each platform page clearly marks which fields return 0 and why.
>
> * **No Data vs. Zero (Instagram)**: When Instagram refuses insights for a post, we store **no snapshot** instead of a row of zeros. This happens for posts published before the account switched to a professional (Business/Creator) account, which Meta never serves insights for, and for posts with too few viewers. A forced refresh on such a post returns `400` with Meta's reason. Posts that can never have insights are excluded from future refreshes.

***

## Understanding Analytics

This is what we return in the standard analytics schema.

### Rolling Window

Analytics show aggregated data over a fixed time period (e.g., last 30 days) that updates as time progresses. Each time you view analytics, you see data for the most recent period.

Older data falls out of the window as newer data is added.

### Lifetime

Analytics show a snapshot of cumulative totals from when the post or profile was created up to the current moment. These values represent the current state and will continue to grow over time.

These values usually only increase, unless the platform removes or recalculates engagement.

***

## Raw Analytics Data

In addition to the parsed analytics data described above, raw analytics data is available through dedicated raw endpoints. Raw analytics contain the raw payload we store for the snapshot. Depending on the platform, this can be the original API response, a flat metric object built from platform insights, or a platform payload plus a computed summary. This includes:

* Platform-specific metrics that may not be mapped to our standard schema
* Additional metadata and context provided by the platform
* Detailed breakdowns (e.g., audience demographics, engagement by time period, etc.)
* **LinkedIn:** reaction-type breakdowns (our normalized `likes` field is a single aggregate; raw payloads retain per-reaction detail where the API provides it)

Raw analytics are useful when you need platform-specific metrics that are not included in the standard analytics format. Raw data structure and fields vary significantly between platforms.

### Raw Endpoints

| Target | Endpoint | Query |
| :- | :- | :- |
| Social account raw analytics | `GET /api/v1/analytics/social-account/raw` | `teamId`, `platformType` |
| Post raw analytics | `GET /api/v1/analytics/post/raw` | `postId` + `platformType`, or `importedPostId` |

```http theme={null}
GET /api/v1/analytics/social-account/raw?teamId=team_123&platformType=FACEBOOK
```

```http theme={null}
GET /api/v1/analytics/post/raw?postId=post_123&platformType=FACEBOOK
```

```http theme={null}
GET /api/v1/analytics/post/raw?importedPostId=profile_post_123
```

Raw responses use the same wrapper shape as parsed analytics, but each item includes a platform-specific `raw` object. Social account raw responses return `socialAccount` and `items[]`; post raw responses return `post`, optional `profilePost`, and `items[]`.

```json theme={null}
{
  "socialAccount": {
    "id": "sa_123",
    "type": "INSTAGRAM",
    "teamId": "team_123"
  },
  "items": [
    {
      "id": "raw_123",
      "socialAccountId": "sa_123",
      "analyticsId": "analytics_123",
      "raw": {
        "platformSpecificPayload": {}
      },
      "forced": false,
      "createdAt": "2026-04-27T10:00:00.000Z",
      "updatedAt": "2026-04-27T10:00:00.000Z",
      "deletedAt": null
    }
  ]
}
```

For exact raw payload examples, use the platform pages:

* [Instagram raw analytics](https://info.bundle.social/api-reference/platforms/instagram.md#raw-analytics-demographics--audience-data)
* [Facebook raw analytics](https://info.bundle.social/api-reference/platforms/facebook.md#raw-analytics)
* [LinkedIn raw analytics](https://info.bundle.social/api-reference/platforms/linkedin.md#raw-analytics)
* [TikTok raw analytics](https://info.bundle.social/api-reference/platforms/tiktok.md#raw-analytics-demographics--audience-data)
* [YouTube raw analytics](https://info.bundle.social/api-reference/platforms/youtube.md#raw-analytics-demographics--audience-data)
* [Snapchat analytics](https://info.bundle.social/api-reference/platforms/snapchat.md#analytics)
* [Threads raw analytics](https://info.bundle.social/api-reference/platforms/threads.md#raw-analytics)
* [Pinterest raw analytics](https://info.bundle.social/api-reference/platforms/pinterest.md#raw-analytics)
* [Reddit raw analytics](https://info.bundle.social/api-reference/platforms/reddit.md#raw-analytics)
* [Mastodon raw analytics](https://info.bundle.social/api-reference/platforms/mastodon.md#raw-analytics)
* [Bluesky raw analytics](https://info.bundle.social/api-reference/platforms/bluesky.md#raw-analytics)
* [Google Business raw analytics](https://info.bundle.social/api-reference/platforms/google-business.md#raw-analytics)

### Raw Availability By Platform

| Platform | Profile raw | Post raw | Typical contents |
| :- | :- | :- | :- |
| Instagram | Yes | Yes | Account info, daily totals, demographics, media insights |
| Facebook | Yes | Yes | Page info, page insights, demographic insights, reaction/video/post insight metrics |
| LinkedIn | Yes | Yes | Member/org analytics, share statistics, reaction breakdowns where available |
| TikTok | Yes | Yes | Account metrics, audience splits, video watch and source metrics |
| YouTube | Yes | Yes | Channel/video statistics, video demographics where available |
| Snapchat | Optional | Optional | Public Profile, Story, and Spotlight stats when raw Snapchat analytics is enabled for the organization |
| Threads | Yes | Yes | Profile/media insights returned by Threads |
| Pinterest | Yes | Yes | User/pin analytics and lifetime metric payloads |
| Reddit | Limited | Limited | Listing data and engagement fields returned by Reddit |
| Mastodon | Limited | Limited | Account/status payloads with basic engagement |
| Bluesky | Limited | Limited | Actor/post payloads and calculated engagement inputs |
| Google Business | Yes | No post raw | Location info, daily metrics, computed summary |
| Twitter/X | No | No | No raw payloads; analytics are on demand only (see the X page) |
| Discord | No | No | Messaging platform; no analytics API |
| Slack | No | No | Messaging platform; no analytics API |

> [!NOTE]
>
> Raw data is subject to the same **30-day retention** as parsed analytics. If you need it long-term, fetch and store it yourself.

BTW, you are a nerd for reading all of this.

***

## Platform Summary Table

A quick reference for what each platform gives us (and what it doesn't).

| Platform | Profile Period | Post Period | Key Limitations |
| :- | :- | :- | :- |
| [Instagram](https://info.bundle.social/api-reference/platforms/instagram.md) | Rolling (30d) | Lifetime | Views (Unique) returns 0 |
| [Facebook](https://info.bundle.social/api-reference/platforms/facebook.md) | Rolling (30d) | Lifetime | Profile: likes, comments, post count all return 0 |
| [LinkedIn (Personal)](https://info.bundle.social/api-reference/platforms/linkedin.md) | Rolling (30d) | Rolling (30d) | Views, post count, following return 0 |
| [LinkedIn (Org)](https://info.bundle.social/api-reference/platforms/linkedin.md) | Rolling (30d) | Rolling (30d) | Post count, following, post views/saves return 0 |
| [Twitter/X](https://info.bundle.social/api-reference/platforms/twitter.md) | On demand | On demand | Forced refresh only, billed from X credits; profile returns followers, following and post count only |
| [TikTok](https://info.bundle.social/api-reference/platforms/tiktok.md) | Rolling (30d) | Lifetime | Post saves return 0 |
| [YouTube](https://info.bundle.social/api-reference/platforms/youtube.md) | Lifetime | Lifetime | Profile likes, following, post shares return 0 |
| [Snapchat](https://info.bundle.social/api-reference/platforms/snapchat.md) | Lifetime | Lifetime | Public Profile required; raw payloads require organization-level enablement |
| [Threads](https://info.bundle.social/api-reference/platforms/threads.md) | Rolling | Lifetime | Following returns 0 |
| [Pinterest](https://info.bundle.social/api-reference/platforms/pinterest.md) | Rolling (30d) | Mixed | Profile comments, post shares return 0 |
| [Reddit](https://info.bundle.social/api-reference/platforms/reddit.md) | N/A | Lifetime | All profile analytics return 0 |
| [Mastodon](https://info.bundle.social/api-reference/platforms/mastodon.md) | Snapshot | Lifetime | Most metrics return 0 - very limited |
| [Bluesky](https://info.bundle.social/api-reference/platforms/bluesky.md) | Snapshot | Lifetime | Most metrics return 0 - impressions are calculated |
| [Discord](https://info.bundle.social/api-reference/platforms/discord.md) | N/A | N/A | No analytics |
| [Slack](https://info.bundle.social/api-reference/platforms/slack.md) | N/A | N/A | No analytics |
| [Google Business](https://info.bundle.social/api-reference/platforms/google-business.md) | Rolling (30d) | N/A | Profile/location raw analytics only; post analytics are not returned |

***

## Available Metrics Reference

### Understanding Return Values

* **Available**: The metric is provided by the platform API and returns real data.
* **Returns 0**: The metric returns 0 because the platform API doesn't provide this data. This is not a bug. This is the platform being stingy.

### Profile Analytics Metrics

| Metric | Description |
| :- | :- |
| `impressions` | Number of times your profile/content was shown |
| `impressionsUnique` | Number of unique users who saw your profile/content |
| `views` | Number of times your profile/page was viewed |
| `viewsUnique` | Number of unique users who viewed your profile |
| `likes` | Total likes/reactions received |
| `comments` | Total comments received |
| `postCount` | Total number of posts published |
| `followers` | Current follower count |
| `following` | Current following count |

### Post Analytics Metrics

| Metric | Description |
| :- | :- |
| `impressions` | Number of times the post was shown |
| `impressionsUnique` | Number of unique users who saw the post |
| `views` | Number of times the post was viewed (for videos, this is play count) |
| `viewsUnique` | Number of unique users who viewed the post |
| `likes` | Total likes/reactions received |
| `dislikes` | Total dislikes (YouTube, Reddit only) |
| `comments` | Total comments received |
| `shares` | Total shares/reposts |
| `saves` | Total saves/bookmarks |

***

## Notes

* **Rolling Window** data refreshes to show the most recent period. Each time you check, you see the current window.
* **Lifetime** data represents cumulative totals from creation to now.
* **Returns 0** means the platform API doesn't provide that data. Not a bug. Each platform page documents exactly which fields return 0.
* Some platforms have date restrictions (e.g., Threads requires posts after April 2024).
* LinkedIn has significant differences between personal and organization account analytics.
* Metrics may vary slightly between platforms due to how each defines and tracks engagement.
* All analytics (parsed and raw) are deleted after **30 days**. See [Data Retention](https://info.bundle.social/api-reference/data-retention.md).


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# LinkedIn

> The professional network. Where URNs are king and Personal profiles have limited superpowers.

LinkedIn is unique because it strictly separates **Personal Profiles** (Members) from **Organization Pages** (Companies). The API treats them very differently, and this affects analytics significantly.

## Quirks & Gotchas

### Personal vs. Organization

This is the biggest source of confusion.

* **Personal Profile (Member):** Limited API. **Cannot import post history.** Limited analytics. No profile views data.
* **Organization (Company Page):** Full API power. Richer analytics. Supports historical import. Has page view data.

### Article / Link Preview

When you send a post with `data.LINKEDIN.link` and no media uploads, bundle.social fetches the URL, scrapes its Open Graph metadata, and builds a LinkedIn article content block with a title, description, and preview image automatically.

* `link` is the URL to preview, max 2048 characters.

<Note>
  This is the correct way to build link posts on LinkedIn. If you include both a `link` and media uploads, the uploads take precedence and the link is ignored.
</Note>

### The URN Nightmare

LinkedIn uses "URNs" (Uniform Resource Names) to identify everything.

* Organization: `urn:li:organization:12345`
* Person: `urn:li:person:abcde`

If you are constructing raw text mentions, you need to use this format. Our API handles basic text automatically, but if you're getting fancy, keep this in mind.

### Media Limits

Video max size is **2 GB** (not 200 MB - that was an old API limitation). Documents must be PDF format, max 100 MB.

**GIFs** are supported-upload animated GIFs like other image media for LinkedIn posts.

See [Platform Limits](/api-reference/limits#linkedin) for the full breakdown.

### Text & Field Limits

| Field | Limit |
| :- | :- |
| `text` | Max 3,000 characters |
| `mediaTitle` | Max 200 characters |

***

## Post Options

| Field | Type | Description |
| :- | :- | :- |
| `text` | `string` | **Required.** Post text. Max 3,000 characters. |
| `uploadIds` | `string[]` | Images, one video, one PDF document, or GIF media. Media types cannot be freely mixed. |
| `link` | `string` | Optional URL for LinkedIn article preview posts. Ignored when media uploads are present. |
| `thumbnail` | `string` | URL to an uploaded thumbnail image. |
| `mediaTitle` | `string` | Title for video or document posts. Max 200 characters. |
| `privacy` | `CONNECTIONS` \| `PUBLIC` \| `LOGGED_IN` \| `CONTAINER` | Visibility setting. |
| `hideFromFeed` | `boolean` | Hide from the main feed where LinkedIn supports it. |
| `disableReshare` | `boolean` | Disable resharing where LinkedIn supports it. |

```json theme={null}
{
  "teamId": "team_123",
  "title": "LinkedIn reporting update",
  "status": "SCHEDULED",
  "postDate": "2026-06-01T15:00:00.000Z",
  "socialAccountTypes": ["LINKEDIN"],
  "data": {
    "LINKEDIN": {
      "text": "We shipped a new reporting workflow",
      "privacy": "PUBLIC",
      "link": "https://example.com/reporting"
    }
  }
}
```

***

## Mentions And Published Post Actions

### Resolve Mentionable People And Organizations

**Endpoint:** `GET /api/v1/misc/linkedin/mentions/tags`

Provide `teamId` and either a search query (`q`) or LinkedIn profile/company `url`. `scope` can be `people`, `organizations`, or `all`.

```http theme={null}
GET /api/v1/misc/linkedin/mentions/tags?teamId=team_123&url=https://www.linkedin.com/in/jane-doe&displayName=Jane%20Doe&scope=people
```

Person mention lookup is available when the selected LinkedIn channel is an organization. URL lookup accepts `linkedin.com/in/...` for people and `linkedin.com/company/...` for organizations. `displayName` is optional and controls the text shown for a person resolved by URL.

Use `POST /api/v1/misc/linkedin/mentions/builder` to combine returned URNs with text:

```json theme={null}
{
  "text": "Thanks Jane Doe for the launch support",
  "tags": [
    {
      "display": "Jane Doe",
      "urn": "urn:li:person:abc123"
    }
  ]
}
```

### Reshare A LinkedIn Post

**Endpoint:** `POST /api/v1/misc/linkedin/post/reshare`

```json theme={null}
{
  "teamId": "team_123",
  "parentPostUrn": "urn:li:share:123456789",
  "commentary": "Worth sharing with our network.",
  "visibility": "PUBLIC",
  "disableReshare": false
}
```

`commentary` is required and limited to 3,000 characters. The response includes the new LinkedIn ID, activity URN, and permalink when LinkedIn returns them.

### Edit Or Delete Published Content

| Operation | Endpoint | Main fields |
| :- | :- | :- |
| Edit post text | `PATCH /api/v1/misc/linkedin/post` | `teamId`, bundle.social `postId`, `description` |
| Delete post | `DELETE /api/v1/misc/linkedin/post` | `teamId`, bundle.social `postId` |
| Edit comment | `PATCH /api/v1/misc/linkedin/comment` | `teamId`, bundle.social `commentId`, `text` |
| Delete comment | `DELETE /api/v1/misc/linkedin/comment` | `teamId`, bundle.social `commentId` |

These operations act on content already published to LinkedIn. They do not change the original scheduled payload stored in bundle.social.

***

## Analytics

For general analytics concepts (refresh rates, data retention, what "Returns 0" means), see the [Analytics Overview](/api-reference/analytics).

### Profile Analytics

#### Personal (Member)

**Period:** Rolling window (30 days).

| Metric | Description | Note |
| :- | :- | :- |
| `impressions` | Total content views | |
| `impressionsUnique` | Unique content views | |
| `views` | - | Returns `0` (LinkedIn doesn't provide views for personal accounts) |
| `viewsUnique` | - | Returns `0` |
| `likes` | Total likes | |
| `comments` | Total comments | |
| `postCount` | - | Returns `0` (not provided by LinkedIn API) |
| `followers` | Connections/Followers | |
| `following` | - | Returns `0` (not provided by LinkedIn API) |

#### Organization (Company)

**Period:** Rolling window (30 days).

| Metric | Description | Note |
| :- | :- | :- |
| `impressions` | Total content views | |
| `impressionsUnique` | Unique content views | |
| `views` | **Page Views** | Available for Orgs only! |
| `viewsUnique` | Unique page views | |
| `likes` | Total likes | |
| `comments` | Total comments | |
| `postCount` | - | Returns `0` (not provided by LinkedIn API) |
| `followers` | Followers | |
| `following` | - | Returns `0` (not provided by LinkedIn API) |

### Post Analytics

#### Personal Posts

**Period:** Rolling window (30 days).

| Metric | Description | Note |
| :- | :- | :- |
| `impressions` | View count | |
| `impressionsUnique` | Unique view count | |
| `views` | Video views | Video posts only |
| `viewsUnique` | Unique video views | Video posts only |
| `likes` | Reactions | |
| `comments` | Comments | |
| `shares` | Reposts | |

#### Organization Posts

**Period:** Rolling window (30 days).

<Warning>
  **Only recent posts.** Organization analytics only cover posts published within the last 30 days. Posts authored by members (not the organization/brand itself) are excluded from organization analytics.
</Warning>

| Metric | Description | Note |
| :- | :- | :- |
| `impressions` | View count | |
| `impressionsUnique` | Unique view count | |
| `views` | - | Returns `0` (not provided for individual org posts) |
| `viewsUnique` | - | Returns `0` |
| `likes` | Reactions | |
| `comments` | Comments | |
| `shares` | Reposts | |
| `saves` | - | Returns `0` (not provided by LinkedIn API) |

### Raw Analytics

Raw analytics for LinkedIn retain **reaction** breakdowns from the platform (per reaction type) where available. Our standard post schema still exposes a single aggregated likes/reactions-style metric; use raw data when you need the full split.

#### Post Raw Example

```json theme={null}
{
  "shareStatistics": {
    "impressionCount": 23800,
    "uniqueImpressionsCount": 17120,
    "clickCount": 640,
    "likeCount": 312,
    "commentCount": 28,
    "shareCount": 17,
    "engagement": 997
  },
  "interactions": {
    "reactions": [
      {
        "reactionType": "LIKE",
        "actor": "urn:li:person:abc123",
        "actorDisplayName": "Jane Doe"
      },
      {
        "reactionType": "PRAISE",
        "actor": "urn:li:organization:12345",
        "actorDisplayName": "Example Company"
      }
    ]
  },
  "availability": {
    "reactions": {
      "available": true
    }
  }
}
```

#### Page (Organization) Raw: Follower Demographics

Profile raw analytics for a LinkedIn Page include `followerStatistics`, the Page's lifetime follower breakdowns as LinkedIn returns them:

```json theme={null}
{
  "scope": "organization",
  "followerStatistics": {
    "followerCountsByGeoCountry": [
      { "geo": "urn:li:geo:103644278", "followerCounts": { "organicFollowerCount": 1840, "paidFollowerCount": 12 } }
    ],
    "followerCountsByIndustry": [
      { "industry": "urn:li:industry:4", "followerCounts": { "organicFollowerCount": 920, "paidFollowerCount": 3 } }
    ],
    "followerCountsBySeniority": [ /* "seniority": "urn:li:seniority:3", ... */ ],
    "followerCountsByFunction": [ /* "function": "urn:li:function:8", ... */ ],
    "followerCountsByStaffCountRange": [ /* "staffCountRange": "SIZE_11_TO_50", ... */ ],
    "followerCountsByGeo": [ /* regions, same shape as by country */ ]
  }
}
```

* Each breakdown is limited to the top 100 entries.
* Values are LinkedIn URNs (geo, industry, seniority, function). Resolve them to names with LinkedIn's standardized data, or map them on your side.
* LinkedIn doesn't expose follower **age or gender** to apps, so those aren't available.
* Only Pages have follower demographics. Personal profiles don't, and `followerStatistics` is `null` if LinkedIn doesn't return it.

### Quirks

* **Personal accounts** do NOT have views analytics for profiles - only organizations get page views.
* **Organization accounts** have page views for profile analytics but NOT for individual posts. Yes, it's confusing.
* Post count and following count are not provided through the LinkedIn API for either account type.
* Organization post analytics only include posts from the last 30 days.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
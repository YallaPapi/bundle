> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Threads

> Meta's text app. It's like Twitter, but with Meta's infrastructure and surprisingly decent API.

Threads is the new kid on the block, integrated tightly with Instagram's infrastructure. The API is surprisingly decent for a platform this young.

## Supported Content Types

* **Text Posts:** Text only, or text with images/videos. 0-10 files.
* **Mixed Media:** Images and videos can be combined in the same post. Up to 10 items.

## Quirks & Gotchas

### Terminology

* **Comments** are called **Replies** in Threads-land.
* **Shares** include both **Reposts** and **Quotes**. We combine them into one number.

### Date Restrictions

Threads requires posts to be after **April 2024** for analytics. Older imported posts won't have analytics data.

### Media Limits

| Constraint | Value |
| :- | :- |
| Files | 0-10 (images and/or videos, mixed allowed) |
| Video max bitrate | 100 Mbps |
| Video aspect ratio | 0.01:1 to 1.91:1 |
| Image max size | 8 MB |
| Image width | 320-1440px |
| Image aspect ratio | 0.01:1 to 1.91:1 |

See [Platform Limits](/api-reference/limits#threads) for more details.

### Text & Field Limits

| Field | Limit |
| :- | :- |
| `text` | Max 500 characters |
| `altText` | Optional. Accessibility description for **image** media in the post. |

<Note>
  **Alt text** applies to image items Threads publishes through our API. Videos use platform-specific behavior; set alt text when you are posting images.
</Note>

***

## Post Options

Send Threads-specific options inside `data.THREADS`.

| Field | Type | Description |
| :- | :- | :- |
| `text` | `string` | Post text. Max 500 characters. |
| `uploadIds` | `string[]` | Up to 10 uploaded media files. Images and videos can be mixed. |
| `mediaItems` | `array` | Optional per-media metadata. Use it to attach `altText` to image uploads. |
| `topicTag` | `string` | A single topic tag shown in the post header. 1-50 characters, no periods (`.`) or ampersands (`&`). Threads allows one topic per post. |
| `replyControl` | `enum` | Who can reply to the post. See [Reply Control](#reply-control). Threads defaults to `everyone`. |
| `linkAttachment` | `string` | A URL attached to the post as a link preview card. **Text-only posts only.** |
| `poll` | `object` | A poll attachment (2-4 options). **Text-only posts only.** See [Polls](#polls). |
| `gif` | `object` | A GIF attachment. **Text-only posts only.** See [GIFs](#gifs). |
| `allowlistedCountryCodes` | `string[]` | Restrict post visibility to these ISO 3166-1 alpha-2 country codes. Requires Meta account eligibility. |
| `crosspostToInstagramStory` | `boolean` | Cross-share the post to the linked Instagram account as a Story. |
| `crosspostToInstagramStoryDarkMode` | `boolean` | Cross-share the post to the linked Instagram account as a Story in dark mode. |

```json theme={null}
{
  "teamId": "team_123",
  "title": "Threads launch post",
  "status": "SCHEDULED",
  "postDate": "2026-06-01T15:00:00.000Z",
  "socialAccountTypes": ["THREADS"],
  "data": {
    "THREADS": {
      "text": "A quick launch note",
      "uploadIds": ["upload_image_123"],
      "mediaItems": [
        {
          "uploadId": "upload_image_123",
          "altText": "Product screen on a phone"
        }
      ],
      "topicTag": "ProductLaunch",
      "replyControl": "followers_only"
    }
  }
}
```

***

## Reply Control

Set `replyControl` in `data.THREADS` to control who can reply to the post. Threads defaults to `everyone` when omitted.

| Value | Who can reply |
| :- | :- |
| `everyone` | Anyone (default) |
| `accounts_you_follow` | Only accounts you follow |
| `mentioned_only` | Only users mentioned in the post |
| `parent_post_author_only` | Only the author of the parent post |
| `followers_only` | Only your followers |

***

## Polls

Polls attach a 2-4 option vote to a **text-only** post. Options `optionA` and `optionB` are required; `optionC` and `optionD` are optional. Each option is 1-25 characters.

```json theme={null}
{
  "data": {
    "THREADS": {
      "text": "Which one ships first?",
      "poll": {
        "optionA": "Dark mode",
        "optionB": "Scheduling",
        "optionC": "Analytics"
      }
    }
  }
}
```

***

## GIFs

Attach a GIF to a **text-only** post. GIPHY is currently the only supported provider.

```json theme={null}
{
  "data": {
    "THREADS": {
      "text": "Shipping day vibes",
      "gif": {
        "gifId": "l0MYt5jPR6QX5pnqM",
        "provider": "GIPHY"
      }
    }
  }
}
```

***

## Text-Only Attachment Rules

<Warning>
  `poll`, `gif`, and `linkAttachment` are only allowed on **text-only** posts. If the post also has `uploadIds`, validation fails. A post also cannot have both a `poll` and a `gif` at the same time.
</Warning>

***

## Analytics

For general analytics concepts (refresh rates, data retention, what "Returns 0" means), see the [Analytics Overview](/api-reference/analytics).

### Profile Analytics

**Period:** Rolling window.

| Metric | Description | Note |
| :- | :- | :- |
| `impressions` | Content impressions | Internally contains quote count from API |
| `impressionsUnique` | Unique impressions | Internally contains repost count from API |
| `views` | Views | |
| `viewsUnique` | - | Same as views |
| `likes` | Likes | |
| `comments` | Replies | |
| `postCount` | Total posts | |
| `followers` | Followers | |
| `following` | - | Returns `0` (not provided by Threads API) |

### Post Analytics

**Period:** Lifetime.

| Metric | Description | Note |
| :- | :- | :- |
| `impressions` | Views | |
| `impressionsUnique` | - | Same as impressions |
| `views` | Views | Same as impressions |
| `viewsUnique` | - | Same as views |
| `likes` | Likes | |
| `comments` | Replies | |
| `shares` | Reposts + Quotes | Combined into one number |

### Quirks

* Views metric is used for both impressions and views (they are the same value).
* Comments are called "replies" in Threads.
* Shares include both reposts and quotes - we don't split them.
* For profile analytics: the impressions field internally contains quote counts and impressionsUnique contains repost counts. This is how the Threads API returns data.
* Following count is not available through the Threads API.

### Raw Analytics

Threads profile raw analytics are stored as the metrics we get back from Threads, plus a post count.

```json theme={null}
{
  "likes": 420,
  "replies": 38,
  "views": 12400,
  "followers_count": 3100,
  "reposts": 55,
  "quotes": 12,
  "allProfilePosts": 84,
  "followerDemographics": {
    "country": { "data": [{ "name": "follower_demographics", "total_value": { "breakdowns": [{ "dimension_keys": ["country"], "results": [{ "dimension_values": ["US"], "value": 1240 }] }] } }] },
    "city": { "data": [ /* same shape, dimension_keys ["city"] */ ] },
    "age": { "data": [ /* same shape, dimension_keys ["age"], e.g. "25-34" */ ] },
    "gender": { "data": [ /* same shape, dimension_keys ["gender"], "F" / "M" / "U" */ ] }
  }
}
```

`followerDemographics` is the follower breakdown by country, city, age and gender, exactly as Threads returns it. It's collected when raw demographics are enabled for your organization (the same switch as Instagram demographics). Threads only returns it for profiles with at least 100 followers, so for smaller profiles (or if a breakdown fails) that breakdown is `null`.

Post raw analytics store the Threads media/post payload we fetched for that item.

```json theme={null}
{
  "id": "17890000000000000",
  "media_type": "IMAGE",
  "media_product_type": "THREADS",
  "permalink": "https://www.threads.net/@example/post/abc",
  "username": "example",
  "text": "A quick launch note",
  "timestamp": "2026-04-26T10:30:00+0000"
}
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
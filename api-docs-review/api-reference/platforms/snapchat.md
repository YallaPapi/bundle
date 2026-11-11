> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Snapchat

> Connect Snapchat Public Profiles, publish Stories and Spotlights, and retrieve profile and content analytics.

<Warning>
  SNAPCHAT SUPPORT USES THE **PUBLIC PROFILE API**. THE CONNECTED SNAPCHAT ACCOUNT MUST HAVE A PUBLIC PROFILE THAT THE AUTHORIZING USER CAN MANAGE.
</Warning>

## Supported Content Types

* Public Stories with one image or MP4 video.
* Saved Stories with up to 20 images or MP4 videos.
* Spotlights with one MP4 video.
* Profile, Story, and Spotlight analytics.

Snapchat does not require a separate `set-channel` call. The Public Profile returned during OAuth becomes the publishing target.

## Post Options

| Field | Type | Description |
| :- | :- | :- |
| `type` | `STORY` \| `SAVED_STORY` \| `SPOTLIGHT` | Defaults to `STORY`. |
| `uploadIds` | `string[]` | Required. Exactly one uploaded media file, or 1-20 for `SAVED_STORY`. |
| `storyDuration` | `ONE_DAY` \| `TWO_DAYS` \| `THREE_DAYS` \| `ONE_WEEK` | `STORY` only. How long the Story stays visible. Defaults to 24 hours. |
| `title` | `string` | Required for `SAVED_STORY`, max 45 characters. Keep it to 40 or fewer: Snapchat rejects some longer titles. |
| `description` | `string` | Spotlight description, max 160 characters. |
| `text` | `string` | Alias for Spotlight `description`, max 160 characters. `description` takes precedence. |
| `locale` | `string` | Spotlight locale in `en_US` format. Defaults to `en_US`. |
| `skipSaveToProfile` | `boolean` | Spotlight only. Ask Snapchat not to save the Spotlight to the Public Profile. Defaults to `false`. |

### Story Example

```json theme={null}
{
  "teamId": "team_123",
  "title": "Launch Story",
  "status": "SCHEDULED",
  "postDate": "2026-07-20T15:00:00.000Z",
  "socialAccountTypes": ["SNAPCHAT"],
  "data": {
    "SNAPCHAT": {
      "type": "STORY",
      "uploadIds": ["upload_image_123"]
    }
  }
}
```

### Spotlight Example

```json theme={null}
{
  "teamId": "team_123",
  "title": "Launch Spotlight",
  "status": "SCHEDULED",
  "postDate": "2026-07-20T15:00:00.000Z",
  "socialAccountTypes": ["SNAPCHAT"],
  "data": {
    "SNAPCHAT": {
      "type": "SPOTLIGHT",
      "uploadIds": ["upload_video_123"],
      "description": "A quick look at what we shipped",
      "locale": "en_US",
      "skipSaveToProfile": false
    }
  }
}
```

## Media Limits

### Stories

| Constraint | Value |
| :- | :- |
| Files | Exactly 1 image or MP4 video |
| Max file size | 100 MB |
| Video minimum resolution | 540x960 |
| Video duration | 5-180 seconds |

### Saved Stories

| Constraint | Value |
| :- | :- |
| Files | 1-20 images and/or MP4 videos |
| Max file size | 100 MB per file |
| Video minimum resolution | 540x960 |
| Video duration | 5-180 seconds per video |
| Combined length | Max 300 seconds (each image counts as 10 seconds) |
| Title | Required, max 45 characters (40 or fewer recommended) |

### Spotlights

| Constraint | Value |
| :- | :- |
| Files | Exactly 1 MP4 video |
| Max file size | 100 MB |
| Minimum resolution | 540x960 |
| Video duration | 5-180 seconds |

## Troubleshooting

| Error | What it means | Fix |
| :- | :- | :- |
| "This Snapchat account has no Public Profile" (on connect) | The Snapchat login has no Public Profile. Snapchat's API can only publish as a Public Profile. | Create a Public Profile in the Snapchat app, or log in with the account that owns it, then connect again. |
| `SNAP:AUTHORIZATION_PERMISSION_DENIED` "Could not upload Snapchat media" | The connected Snapchat account can see the profile but is not its **Owner or Admin** (e.g. a collaborator, or access only through Ads Manager). | Give that account the Admin role on the Public Profile, or reconnect with the account that owns it. |
| `SNAP:MEDIA_NOT_VALID_FOR_STORY_POSTING` | The media doesn't meet Snapchat's Story requirements. | Use an MP4 video of 5-180 seconds, at least 540x960. |
| "Failed to create saved story: Title" | Snapchat rejected the Saved Story title. | Keep the title to 40 characters or fewer. |

## Publishing Behavior

Snapchat processes uploaded media asynchronously. A post can remain in `PROCESSING` while Snapchat prepares the asset. bundle.social polls the media state and finalizes the Story or Spotlight when it becomes ready.

The post response stores Snapchat progress in `externalData.SNAPCHAT`, including `mediaId`, content `type`, Public Profile ID, source upload ID, and one of these statuses:

* `MEDIA_UPLOADED`
* `MEDIA_PROCESSING`
* `PUBLISHED`

## Analytics

### Profile Analytics

| Metric | Snapchat source |
| :- | :- |
| `impressions`, `views` | Combined profile, Story, saved Story, Spotlight, and Lens views returned by Snapchat |
| `impressionsUnique`, `viewsUnique` | Unique sessions/viewers where available; falls back to views |
| `likes` | Favorites/likes across supported profile content |
| `comments` | Replies/comments |
| `postCount` | Story, saved Story, Spotlight, and Lens content counts where available |
| `followers` | Subscribers/followers |
| `following` | Returns `0` |

### Story And Spotlight Analytics

Post analytics use Snapchat lifetime stats and map views, unique viewers, favorites, replies, shares, and screenshots into the standard post analytics fields.

Raw Snapchat analytics can be enabled per organization. [Contact us](https://bundle.social/contact) if you need the original Snapchat stats payload alongside normalized metrics.

With raw analytics on, profile raw data also includes `demographics`: Snapchat's lifetime profile stats broken down by **age × gender** (`AGE_GENDER`) and **country** (`COUNTRY`), exactly as Snapchat returns them (each stat has a `dimension_breakdown` such as `AGE_18_24` plus `value` and `percentage_value`). These describe your viewers, not a follower list. If Snapchat doesn't return a breakdown for a profile, `demographics` is `null`.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
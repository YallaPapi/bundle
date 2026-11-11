> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Instagram Music Library

> Search Instagram music and original sounds, then attach audio to Reels.

Instagram lets Reels use audio assets from its audio API. In bundle.social, you search for an audio asset first, then pass its `audio_id` as `data.INSTAGRAM.musicSoundInfo.musicSoundId` when creating a Reel.

<Warning>
  Instagram audio search and Reel audio publishing require the Instagram account to be connected through **Facebook Login**. Direct Instagram OAuth (`instagramConnectionMethod: "INSTAGRAM"`) cannot use this feature.
</Warning>

## The Endpoint

**`GET /api/v1/misc/instagram/audio`**

Searches Instagram music or original sounds that can be attached to Reels.

### Query Parameters

| Parameter | Type | Required | Description |
| :- | :- | :- | :- |
| `teamId` | `string` | Yes | Team with the connected Instagram account. |
| `audioType` | `enum` | Yes | `music` or `original_sound`. |
| `searchQuery` | `string` | No | Optional keyword search, max 100 characters. |

```http theme={null}
GET /api/v1/misc/instagram/audio?teamId=team_123&audioType=music&searchQuery=lofi
```

## Response Shape

```json theme={null}
{
  "audio": [
    {
      "audio_id": "17900000000000000",
      "audio_type": "music",
      "title": "Late Night Drive",
      "display_artist": "Example Artist",
      "duration_in_ms": 30000,
      "cover_artwork_thumbnail_url": "https://...",
      "download_url": "https://..."
    },
    {
      "audio_id": "17800000000000000",
      "audio_type": "original_sound",
      "title": "Original audio",
      "ig_username": "creator",
      "profile_picture_url": "https://..."
    }
  ]
}
```

Important fields:

| Field | Meaning |
| :- | :- |
| `audio_id` | The ID you pass as `musicSoundId` in the post payload. |
| `audio_type` | `music` or `original_sound`. |
| `title` | Track or sound title when Instagram provides it. |
| `display_artist` | Artist name for music assets. |
| `duration_in_ms` | Audio duration in milliseconds when available. |
| `download_url` | Preview/download URL when Instagram provides it. |
| `ig_username` | Creator username for original sounds when available. |

## Using Audio In Reels

Use the `audio_id` from the search response as `data.INSTAGRAM.musicSoundInfo.musicSoundId`.

```json theme={null}
{
  "teamId": "team_123",
  "title": "Reel with Instagram audio",
  "status": "SCHEDULED",
  "postDate": "2026-06-01T15:00:00.000Z",
  "socialAccountTypes": ["INSTAGRAM"],
  "data": {
    "INSTAGRAM": {
      "type": "REEL",
      "text": "New Reel",
      "uploadIds": ["upload_video_123"],
      "musicSoundInfo": {
        "musicSoundId": "17900000000000000",
        "musicSoundVolume": 80,
        "videoOriginalSoundVolume": 20
      }
    }
  }
}
```

### Audio Fields

| Field | Type | Description |
| :- | :- | :- |
| `musicSoundId` | `string` | Required when using Instagram audio. Use `audio_id` from the search endpoint. |
| `musicSoundVolume` | `number` | Optional. Audio volume from `0` to `100`. Defaults to `100`. |
| `videoOriginalSoundVolume` | `number` | Optional. Original video volume from `0` to `100`. Defaults to `100`. |

## Rules

* Works only for `data.INSTAGRAM.type: "REEL"`.
* Does not work for feed posts, carousels, or Stories.
* Requires Instagram connected via Facebook Login.
* Direct Instagram OAuth returns a clear `400` error for audio search.
* If you pass `musicSoundInfo` for a non-Reel post, validation fails before publishing.

## Quick Reference

| Task | What to use |
| :- | :- |
| Search music | `GET /api/v1/misc/instagram/audio?teamId=...&audioType=music` |
| Search original sounds | `GET /api/v1/misc/instagram/audio?teamId=...&audioType=original_sound` |
| Search by keyword | Add `searchQuery=...` |
| ID for post | `audio_id` from the search response |
| Post field | `data.INSTAGRAM.musicSoundInfo.musicSoundId` |

Need the full request/response schema? Check [Swagger](https://api.bundle.social/swagger). The endpoint is under misc/instagram.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
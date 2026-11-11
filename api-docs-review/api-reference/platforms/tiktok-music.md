> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# TikTok Music (CML)

> TikTok Commercial Music Library: pre-cleared tracks for videos and photos. Genres, date ranges, song_clip_id vs commercial_music_id, and the draft gotcha.

TikTok's Commercial Music Library (CML) gives you pre-cleared tracks for organic posts and ads. No copyright roulette. Here's how it works, what the endpoint returns, and the quirks that'll bite you if you don't read this.

## The Endpoint

**`GET /api/v1/misc/tiktok/cml/trending-list`**

Returns up to 100 trending tracks. Filter by genre and time window.

### Query Parameters

| Parameter | Type | Default | Description |
| :- | :- | :- | :- |
| `teamId` | string | required | Your team ID |
| `genre` | string | `"POP"` | Genre filter. See [supported genres](#supported-genres) below |
| `dateRange` | string | `"7DAY"` | `1DAY`, `7DAY`, or `30DAY`. How far back to rank popularity |

### Response Shape

The response is a **flat array** of track objects.

```json theme={null}
[
  {
    "commercial_music_name": "Lo-Fi analog beat",
    "duration": 183,
    "thumbnail_url": "https://...",
    "artist": "Gloveity",
    "preview_url": "https://...",
    "genres": ["HIP_HOP/RAP", "LO-FI"],
    "rank_position": "1",
    "trending_history": [
      { "date": "2026-02-15", "rank_position_daily": "1" }
    ],
    "full_duration_song_clip": {
      "preview_url": "https://...",
      "duration": 183,
      "song_clip_id": "6817312022837872642"
    },
    "trending_song_clip": {
      "preview_url": "https://...",
      "duration": 183,
      "song_clip_id": "6817312022837872642"
    }
  }
]
```

<Important>
  **Use `song_clip_id`, not `commercial_music_id`.** We strip `commercial_music_id` from the response because it's not what you need for publishing. The ID you pass to the post API is `song_clip_id` from `full_duration_song_clip` or `trending_song_clip`. If you use the wrong one, TikTok will reject it.
</Important>

## Supported Genres

A sample of what's available: `POP`, `ROCK`, `LATIN`, `METAL`, `ELECTRONIC`, `HIP_HOP/RAP`, `ALTERNATIVE/INDIE`, `R&B/SOUL`, `COUNTRY`, `CLASSICAL`, `JAZZ`, `CHILL_BEATS`, `CHILLOUT`, `LO-FI`, `EDM`, `HOUSE`, `TECHNO`, `K-POP`, `J-POP`, `DANCE_POP`, `INDIE_POP`, and more. Check the [Swagger spec](https://api.bundle.social/swagger) for the full enum.

## Using Music in Posts

When creating a post with `data.TIKTOK.musicSoundInfo`, you pass the **`song_clip_id`** as `musicSoundId`. That's it for the ID part.

### Video vs Image: Different Rules

| Content Type | What you can pass |
| :- | :- |
| **VIDEO** | `musicSoundId` (required), `musicSoundVolume`, `musicSoundStart`, `musicSoundEnd`, `videoOriginalSoundVolume` |
| **IMAGE** | **Only `musicSoundId`.** No volume, no start/end. Photos get one knob: which track. That's it. |

<Note>
  For IMAGE posts, pass *only* `musicSoundId`. If you send `musicSoundVolume`, `musicSoundStart`, etc., TikTok's API will reject the request. We strip those fields server-side for IMAGE type so you don't have to remember. If you're building a form, don't show volume/trim controls for photo posts.
</Note>

### Video: Volume & Trim

For videos, you get real control:

* **`musicSoundVolume`** (0-100): How loud the music is.
* **`videoOriginalSoundVolume`** (0-100): How loud the original video audio (your voice, etc.) is.
* **`musicSoundStart`** / **`musicSoundEnd`** (ms): Trim the track. Start at 100ms, end at 30000ms. If `musicSoundEnd` is 0 or less than or equal to `musicSoundStart`, we don't send it (TikTok would reject it). Omit both for the full track.

So yeah, you can make the music louder than your voice, or the other way around.

## The Draft Gotcha

Here's the thing: **draft uploads don't persist your music choice.**

When you set `uploadToDraft: true`, TikTok uploads the post to the creator's drafts. Success. But TikTok's draft flow doesn't store which track you picked.

<Important>
  **If music choice matters, don't use drafts.** Publish directly (or schedule) so the track is baked in. Drafts are for "save for later", not "save this exact audio mix for later."
</Important>

## INBOX status (Draft Success)

When you upload as draft, TikTok sometimes returns a different status instead of `PUBLISH_COMPLETE`. That means: "we put it in the creator's inbox as a draft, all good." We treat that as success when `uploadToDraft` is true. If you're not using drafts and you get this, something odd happened. Reach out.

## Quick Reference

| Task | What to use |
| :- | :- |
| Get trending tracks | `GET /api/v1/misc/tiktok/cml/trending-list?teamId=...&genre=POP&dateRange=7DAY` |
| ID for post | `song_clip_id` from `full_duration_song_clip` or `trending_song_clip` |
| Video: full track | `musicSoundId` only (or omit start/end) |
| Video: trim + volume | `musicSoundId`, `musicSoundVolume`, `videoOriginalSoundVolume`, `musicSoundStart`, `musicSoundEnd` |
| Image: any music | `musicSoundId` only |
| Drafts | Don't rely on music persisting |

Need the full request/response schema? Check [Swagger](https://api.bundle.social/swagger). The CML endpoint is under misc/tiktok.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
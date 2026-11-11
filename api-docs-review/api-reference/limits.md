> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Platform Limits

> Check these before you post. Every platform has rules. We enforce them so you don't get banned.

Every platform has rules. Some are sensible, some are arbitrary. We enforce them so you don't get banned.

## How Validation Works

We validate everything before sending to the platform. If your content breaks a rule, you get a `400` error with a clear message telling you exactly what's wrong. Here's the vocabulary:

* **Aspect Ratio:** `width / height`. A 1920x1080 video has a ratio of \~1.78 (16:9).
* **Bitrate:** `(fileSize x 8) / videoLength`. Measured in bps. We show it in Mbps.
* **File Count:** How many images/videos you can attach to a single post.

<Note>
  **Upload ceiling.** Regardless of platform, the largest file we accept is **5 GB** for video (higher on request, per organization - and only via [Multipart Upload](/api-reference/upload-content)), **25 MB** for images, and **100 MB** for documents (PDF). The per-platform limits below are often lower - we enforce the smaller of the two.
</Note>

***

## Instagram

### Posts (Carousel)

| Constraint | Value |
| :- | :- |
| Files | 1-10 (images and/or videos, mixed allowed) |
| Image max size | 8 MB |
| Image max width | 1920px |
| Image aspect ratio | 4:5 to 1.91:1 |
| Video max width | 1920px |
| Video max bitrate | 45 Mbps |
| Video duration | 3s - 15 min |
| Video aspect ratio | 0.01:1 to 10:1 |

### Reels

| Constraint | Value |
| :- | :- |
| Files | 1 video (required) |
| Max width | 1920px |
| Max bitrate | 45 Mbps |
| Duration | 3s - 15 min |
| Aspect ratio | 0.01:1 to 10:1 |

<Warning>
  **Aspect ratios are law.** Instagram is SUPER strict. If your pixel math is off by even a tiny bit, they might reject it. 9:16 vertical is the safe bet for Reels.
</Warning>

### Stories

| Constraint | Value |
| :- | :- |
| Files | 1 (image or video) |
| Image max size | 8 MB |
| Image aspect ratio | 0.01:1 to 10:6 |
| Video max size | 100 MB |
| Video max width | 1920px |
| Video max bitrate | 25 Mbps |
| Video duration | 3s - 60s |
| Video aspect ratio | 0.01:1 to 10:6 |

***

## TikTok

### Videos

| Constraint | Value |
| :- | :- |
| Files | 1 video (required) |
| Max size | 1 GB |
| Resolution | 360x360 to 4096x4096 |
| Aspect ratio | 0.01:1 to 10:6 |
| Duration | Max 10 min (600s) |

### Images (Photo Mode)

| Constraint | Value |
| :- | :- |
| Files | 1-10 images |
| Format | **JPG/JPEG/WebP only** - PNG and other formats will be rejected for TikTok Photo Mode |
| Max size | 20 MB each |
| Max width | 1920px |

<Warning>
  **PNG is not valid for TikTok Photo Mode.** Convert PNG assets before creating the TikTok image post.
</Warning>

***

## YouTube

### Shorts

| Constraint | Value |
| :- | :- |
| Files | 1 video (required) |
| Max size | 5 GB |
| Duration | Max 3 min (180s) |
| Aspect ratio | 1:3 to 1:1 (vertical or square) |

### Long Form Videos

| Constraint | Value |
| :- | :- |
| Files | 1 video (required) |
| Max size | 5 GB |
| Duration | Max 4 hours (14,400s) |
| Aspect ratio | 1:3 to 3:1 |

***

## LinkedIn

| Constraint | Value |
| :- | :- |
| Files | 0-10 (images, videos, OR documents - not mixed) |
| **Videos** | |
| Max videos | 1 |
| Video max size | 2 GB |
| Video resolution | 256x144 to 4096x4096 |
| Video aspect ratio | 1:2.4 to 2.4:1 |
| Video duration | 3s - 30 min |
| **Images** | |
| Max images | 10 |
| Image max size | 5 MB each |
| Image min resolution | 200x200 |
| **Documents** | |
| Max documents | 1 |
| Document max size | 100 MB |
| Document format | PDF only |

***

## Twitter / X

| Constraint | Value |
| :- | :- |
| Files | 0-4 (images and/or videos) |
| **Videos** | |
| Video max size | 512 MB |
| Video aspect ratio | 1:3 to 3:1 |
| Video min length | 0.5s |
| Video duration (Free/Basic) | Max 140s (2:20) |
| Video duration (Premium/Premium+) | Max 600s (10 min) |
| **Images** | |
| Image max size | 5 MB each |
| Max images | 4 |
| **Text** | |
| Text limit (Free/Basic) | 280 characters |
| Text limit (Premium/Premium+) | 25,000 characters |

***

## Facebook

### Page Posts

| Constraint | Value |
| :- | :- |
| Files | 0-10 (images or videos, not mixed) |
| Max videos | 1 |
| Video max bitrate | 45 Mbps |
| Video aspect ratio | 0.01:1 to 1.91:1 |
| Video duration | Max 20 min (1,200s) |
| Max images | 4 |
| Image max size | 4 MB each |
| Image aspect ratio | 0.01:1 to 1.91:1 |

### Reels

| Constraint | Value |
| :- | :- |
| Files | 1 video (required) |
| Min resolution | 540x960 |
| Aspect ratio | 0.01:1 to 10:6 |
| Max bitrate | 45 Mbps |
| Duration | 3s - 20 min (1,200s) |

### Stories

| Constraint | Value |
| :- | :- |
| Files | 1 (image or video) |
| Video min resolution | 540x960 |
| Video max bitrate | 25 Mbps |
| Video duration | 3s - 60s |
| Video aspect ratio | 0.01:1 to 10:6 |
| Image max size | 4 MB |
| Image aspect ratio | 0.01:1 to 10:6 |

***

## Pinterest

| Constraint | Value |
| :- | :- |
| Files | 1 (image or video, required) |
| **Videos** | |
| Video max size | 2 GB |
| Video aspect ratio | 1:2 to 1.91:1 |
| Video duration | 4s - 15 min (900s) |
| **Images** | |
| Image max size | 5 MB |

<Note>
  **Board name required.** You can't pin to thin air. Every Pinterest post needs `boardName` from `socialAccount.channels`.
</Note>

***

## Reddit

### Single Post

| Constraint | Value |
| :- | :- |
| Files | 0-1 (image or video) |
| Video max size | 1 GB |
| Video aspect ratio | 9:16 to 16:9 |
| Video duration | 4s - 15 min (900s) |
| Image max size | 20 MB |

### Gallery Post

| Constraint | Value |
| :- | :- |
| Files | 0-10 images (only if subreddit allows galleries) |
| Image max size | 20 MB each |

<Note>
  **Subreddit rules apply.** Not all subreddits allow media, and not all allow galleries. We validate against the subreddit's settings. If the subreddit requires a flair, you need to provide one.
</Note>

***

## Threads

| Constraint | Value |
| :- | :- |
| Files | 0-10 (images and/or videos, mixed allowed) |
| Video max size | 1 GB |
| Video max bitrate | 100 Mbps |
| Video aspect ratio | 0.01:1 to 1.91:1 |
| Image max size | 8 MB |
| Image width | 320-1440px |
| Image aspect ratio | 0.01:1 to 1.91:1 |

***

## Discord

| Constraint | Value |
| :- | :- |
| Files | 0-10 (images and/or videos, mixed allowed) |
| Video max size | 25 MB |
| Video aspect ratio | 0.01:1 to 1.91:1 |
| Image max size | 25 MB |
| Image aspect ratio | 0.01:1 to 1.91:1 |
| Text | Max 2,000 characters |

<Note>
  **Channel ID required.** Discord posts go to a specific channel. Check `socialAccount.channels` for available options.
</Note>

***

## Slack

| Constraint | Value |
| :- | :- |
| Files | 0-4 (images and/or videos, mixed allowed) |
| Video max size | 1 GB |
| Video aspect ratio | 0.01:1 to 1.91:1 |
| Image max size | 1 GB |
| Image aspect ratio | 0.01:1 to 1.91:1 |
| Text | Max 30,000 characters |

***

## Mastodon

| Constraint | Value |
| :- | :- |
| Files | 0-4 (images and/or videos, mixed allowed) |
| Max videos | 1 |
| Video max size | 99 MB |
| Video aspect ratio | 1:3 to 1:1 |
| Max images | 4 |
| Image max size | 16 MB each |
| Text | Instance-dependent (usually 500 chars) |

***

## Bluesky

| Constraint | Value |
| :- | :- |
| Files | 0-4 (images and/or videos) |
| Text | 300 characters |

<Info>
  Bluesky has minimal media restrictions on their end. We enforce basic file count limits, but the platform is relatively permissive compared to others.
</Info>

***

## Google Business

| Constraint | Value |
| :- | :- |
| Files | 0-1 image only (no video) |
| Image max size | 5 MB |
| Image min resolution | 250x250 |
| Text | Max 1,500 characters |

***

## Snapchat

### Stories

| Constraint | Value |
| :- | :- |
| Files | Exactly 1 image or MP4 video |
| Max file size | 100 MB |
| Video minimum resolution | 540x960 |
| Video duration | 5-60 seconds |

### Spotlights

| Constraint | Value |
| :- | :- |
| Files | Exactly 1 MP4 video |
| Max file size | 100 MB |
| Minimum resolution | 540x960 |
| Video duration | 6-60 seconds |

***

## Quick Reference Table

| Platform | Max Files | Video Max Size | Video Max Duration | Image Max Size |
| :- | :- | :- | :- | :- |
| Instagram Post | 10 | N/A (bitrate limit) | 15 min | 8 MB |
| Instagram Reel | 1 | N/A (bitrate limit) | 15 min | - |
| Instagram Story | 1 | 100 MB | 60s | 8 MB |
| TikTok Video | 1 | 1 GB | 10 min | - |
| TikTok Image | 10 | - | - | 20 MB |
| YouTube Short | 1 | 5 GB | 3 min | - |
| YouTube Video | 1 | 5 GB | 4 hours | - |
| LinkedIn | 10 | 2 GB | 30 min | 5 MB |
| Twitter/X | 4 | 512 MB | 140s / 10 min | 5 MB |
| Facebook Post | 10 | N/A (bitrate limit) | 20 min | 4 MB |
| Facebook Reel | 1 | N/A (bitrate limit) | 20 min | - |
| Facebook Story | 1 | N/A (bitrate limit) | 60s | 4 MB |
| Pinterest | 1 | 2 GB | 15 min | 5 MB |
| Reddit | 1 / 10 gallery | 1 GB | 15 min | 20 MB |
| Threads | 10 | 1 GB | - | 8 MB |
| Discord | 10 | 25 MB | - | 25 MB |
| Slack | 4 | 1 GB | - | 1 GB |
| Mastodon | 4 | 99 MB | - | 16 MB |
| Bluesky | 4 | - | - | - |
| Google Business | 1 | - | - | 5 MB |
| Snapchat Story | 1 | 100 MB | 60s | 100 MB |
| Snapchat Spotlight | 1 | 100 MB | 60s | - |

## Text & Character Limits

| Platform | Main text field limit | Other text field limits |
| :- | :- | :- |
| Instagram | `text`: 2,000 | `collaborators` username max 30, `tagged` username max 30, optional `altText` on image posts |
| TikTok | `text`: 2,200 | - |
| YouTube | `text` (title): 100 | `description`: 5,000 |
| LinkedIn | `text`: 3,000 | `mediaTitle`: 200 |
| Twitter / X | `text`: 280 (Free/Basic), 25,000 (Premium/Premium+) | - |
| Facebook | `text`: 50,000 | `mediaTitle`: 255, `link`: 2,048, optional `altText` on image posts |
| Pinterest | `text`: 100 | `description`: 800, `altText`: 500, `note`: 500 |
| Reddit | `text` (title): 300 | `description`: 30,000 |
| Threads | `text`: 500 | optional `altText` on image media |
| Discord | `text`: 2,000 | `username`: 80, `avatarUrl`: 2,048 |
| Slack | `text`: 30,000 | `username`: 80, `avatarUrl`: 2,048 |
| Mastodon | `text`: 30,000 | `spoiler`: 50 (instance-level limits can still be lower) |
| Bluesky | `text`: 300 | `externalTitle`: 300, `externalDescription`: 1,000, `videoAlt`: 10,000 |
| Google Business | `text`: 1,500 | `eventTitle`: 58, `offerCouponCode`: 58, `offerTermsConditions`: 1,500 |
| Snapchat | `description` or `text`: 160 | `locale`: `en_US` format for Spotlights |

For daily posting limits per platform and monthly post caps, see [Rate Limits](/api-reference/rate-limits).


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
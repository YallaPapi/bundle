> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Media Upload

> Upload images, videos, and documents with small or large upload flows.

## Overview

You have three ways to upload files.

| Method | Best for | Ceiling |
| :- | :- | :- |
| **Multipart Upload** | Big videos. Chunked, retryable per part. | Your video limit - 5 GB by default, higher on request |
| **Direct Upload** | One-shot uploads of moderate files. | 5 GiB (single-request storage limit) |
| **Simple Upload** | Images and small clips. | 90 MB |

<Warning>
  **Recommendation:** Use **Multipart Upload** for videos. It is the only method where a
  network drop costs you one 64 MiB chunk instead of the whole transfer - with Direct or
  Simple, a failure at 99% means starting over.
</Warning>

***

## Method 1: Multipart Upload (The Pro Way)

The file is split into fixed **64 MiB** chunks that you PUT independently, then we
assemble them. Each chunk can be retried or re-signed on its own, so a long upload
survives a flaky connection.

### Step 1: Initialize

**Endpoint:** `POST /api/v1/upload/multipart/init`

```json theme={null}
// Request
{
  "fileName": "viral-video.mp4",
  "mimeType": "video/mp4",
  "fileSize": 8589934592,   // required - we reject oversized files here, not after the transfer
  "teamId": "..."
}
```

**Response:** an `uploadId`, the `path`, the `partSize`, and one presigned `url` per part.

```json theme={null}
{
  "uploadId": "2~abc123...",
  "path": "team-id/9f8e7d6c.mp4",
  "partSize": 67108864,
  "parts": [
    { "partNumber": 1, "url": "https://..." },
    { "partNumber": 2, "url": "https://..." }
  ]
}
```

### Step 2: PUT each part - and keep every ETag

Slice the file at `partSize` boundaries and `PUT` each slice to its own URL. Every part
except the last must be exactly `partSize` bytes - storage rejects the assembly at the end
if they are not uniform.

**Read the `ETag` response header from each PUT.** You need the full list to finish, and
there is no way to recover it afterwards.

```bash theme={null}
curl -X PUT "https://..." --upload-file ./chunk-001 -D -
# HTTP/1.1 200 OK
# ETag: "d41d8cd98f00b204e9800998ecf8427e"
```

<Note>
  Part URLs are valid for **6 hours**. If one expires mid-upload, call
  `POST /api/v1/upload/multipart/sign` with `{ path, uploadId, partNumbers: [12] }` to get a
  fresh URL for just those parts. Parts you already uploaded keep their ETags - do not
  re-send them.
</Note>

### Step 3: Complete

**Endpoint:** `POST /api/v1/upload/multipart/complete`

```json theme={null}
// Request
{
  "path": "team-id/9f8e7d6c.mp4",
  "uploadId": "2~abc123...",
  "parts": [
    { "partNumber": 1, "etag": "\"d41d8cd9...\"" },
    { "partNumber": 2, "etag": "\"a3f5b2e1...\"" }
  ],
  "teamId": "..."
}
```

**Response:** the upload object, including the `id` you pass when creating a post.

### Handling errors on complete

This is worth wiring properly - it decides whether a failure costs you seconds or a full
re-upload.

| Response | Meaning | What to do |
| :- | :- | :- |
| **5xx** | Something on our side failed, not your file - either we could not assemble the parts, or we assembled them and the step after that failed. **Nothing is deleted** in either case. | Retry the same `complete` call (a few attempts with backoff). It handles both: it will assemble the parts, or - if they were already assembled - adopt the existing object. Do **not** re-upload the bytes. |
| **400 about the part list** | A part number or ETag is wrong or missing. We discard the parts for you. | Fix the request and start a new upload. |
| **400 about the file** | Empty, wrong type, too large, or no readable preview. The bytes have been deleted. | Fix the file and start a new upload - there is nothing left to abort. |
| **403** (quota, permissions) | Rejected *before* we assemble anything, so **your parts are still open**. | Call `abort` yourself, then fix the cause. |
| **Success, but you never saw it** | e.g. your request timed out after we finished. | Just call `complete` again - it returns the same upload and is not counted twice against your quota. |

### Giving up

**Endpoint:** `POST /api/v1/upload/multipart/abort` with `{ path, uploadId }`.

Call it whenever you abandon an upload - unfinished parts occupy storage and count against
your usage. If your process dies before it can, transfers left untouched for **7 days** are
aborted automatically, but that is a backstop, not your cleanup path.

<Note>
  A single upload is capped at **10 000 parts**, and the file still has to fit your plan's
  video limit (see [Limits](/api-reference/limits)).
</Note>

***

## Method 2: Direct Upload

One presigned `PUT` for the whole file. Simpler than multipart, but a failure means
starting over, and the hard ceiling is **5 GiB** (a single storage request cannot carry
more). Above that we reject at init and point you to multipart.

### Step 1: Initialize

**Endpoint:** `POST /api/v1/upload/init`

```json theme={null}
// Request
{
  "fileName": "viral-video.mp4",
  "mimeType": "video/mp4",
  "fileSize": 1073741824,   // optional, but send it - lets us reject oversized files up front
  "teamId": "..."
}
```

**Response:** a presigned `url` and a `path`.

```json theme={null}
{
  "url": "https://...",
  "path": "team-id/9f8e7d6c.mp4"
}
```

<Note>
  **The pre-signed URL expires after 30 minutes.** If you don't start uploading within that window, you'll need to initialize again.
</Note>

### Step 2: Push the Bytes

Send the raw binary file to the `url` we gave you. Use `PUT`.

<Note>
  **Important:** Do not wrap this in JSON or Multipart form. Just send the raw bytes.
</Note>

```bash theme={null}
curl -X PUT "https://..." \
  --upload-file ./viral-video.mp4
```

### Step 3: Finalize

Tell us you're done so we can register the file in our system.

**Endpoint:** `POST /api/v1/upload/finalize`

```json theme={null}
// Request
{
  "path": "team-id/9f8e7d6c.mp4", // from Step 1
  "teamId": "..."
}
```

**Response:**
You get an `id` (e.g., `upload_abc123`). **This is the ID you use when creating a post.**

***

## Method 3: Simple Upload (The Lazy Way)

Good for images or small clips. Uses standard `multipart/form-data`.

**Endpoint:** `POST /api/v1/upload`

```bash theme={null}
curl -X POST "https://api.bundle.social/api/v1/upload" \
  -H "x-api-key: YOUR_KEY" \
  -F "file=@./meme.jpg" \
  -F "teamId=YOUR_TEAM_ID"
```

**Response:**
Returns the `id` immediately.

***

## Upload from a URL

Register media by passing a **public HTTP(S) URL** instead of uploading the bytes yourself: `POST /api/v1/upload/from-url` (also exposed in the SDKs and the MCP server). We fetch the asset **server-side** and register it like any other upload.

| Detail | Value |
| :- | :- |
| Max size | **1 GB** |
| Download timeout | **60 seconds** |
| Best for | Small / medium files (typical short-form / feed content) |
| Not for | Large videos - we fetch the file server-side and cap it at **1 GB / 60 s**. For bigger files, upload the bytes yourself with [Multipart Upload](#method-1-multipart-upload-the-pro-way). |

The response is the upload itself. Use `id` in `uploadIds`, and `url` wherever a field expects a hosted media URL, such as a TikTok `thumbnail`:

```json theme={null}
{
  "id": "upl_123",
  "type": "image",
  "url": "https://private-storage.bundle.social/team_123/cover.jpg",
  "width": 1080,
  "height": 1920,
  "mime": "image/jpeg"
}
```

<Note>
  The **1 GB / 60 s** limit applies only to URL imports, because we download the file for you. Uploads where you send the bytes stream straight to storage and allow up to your full video limit.
</Note>

***

## Supported Formats & Limits

| Type | Formats | Max Size |
| :- | :- | :- |
| **Images** | JPG, PNG, GIF | 25 MB |
| **Videos** | MP4, MOV | Platform-dependent (see [Limits](/api-reference/limits)) |
| **Documents** | PDF | 100 MB |

<Note>
  The default video ceiling is **5 GB** per file - [talk to us](mailto:support@bundle.social) if you need more, which is granted per organization and only applies to Multipart Upload. The max video size also depends on the platform you're posting to: TikTok allows up to 1 GB, YouTube up to 5 GB, while Discord caps at 10 MB. Check [Platform Limits](/api-reference/limits) for the exact numbers per platform.
</Note>

<Info>
  **Tip:** If you are uploading a picture of your cat (or your mom, we don't judge), Simple Upload is fine. For a 4K podcast clip, use Multipart.
</Info>

***

## Video Compression

You can enable automatic video compression on your organization. When enabled, we'll compress videos larger than 10 MB before they're stored and posted.

### How to enable

Video compression is an organization-level setting. You can toggle it from your dashboard or contact us to enable it. Once on, it applies to all uploads across all teams in your org.

### What happens

| Setting | Value |
| :- | :- |
| Threshold | Videos > 10 MB |
| Output format | MP4 (H.264 + AAC) |
| Quality | CRF 30 (good balance of quality and size) |
| Preset | Medium |

We're smart about it - if the compressed file ends up **larger** than the original (rare, but it happens with already-compressed videos), we keep the original and toss the compressed version. You always get the smaller file.

<Tip>
  This is great if your users upload raw or minimally compressed videos. A 500 MB screen recording can often shrink to under 100 MB with no visible quality loss. Your storage costs will thank you - and so will the upload speeds.
</Tip>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
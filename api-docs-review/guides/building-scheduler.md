> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Building a Scheduler

> A practical guide to building a social media scheduling tool. The real one, not the 5-step tutorial.

So you want to build a scheduler? You want to be the next Buffer or Hootsuite?

Cool. Here is how you actually do it with bundle.social. Not the "hello world" version - the real thing, with error handling, retries, drafts, and all the edge cases that will bite you at 2 AM.

***

## The Architecture

The high-level flow is simple. The devil is in the details (which we cover below).

1. **User connects account** (via [Connect Flow](/api-reference/connect-social-accounts)).
2. **User uploads content** (via [Media Upload](/api-reference/upload-content)).
3. **User picks a date** (your UI).
4. **You send it to us** (API call).
5. **We publish it** (our infrastructure).
6. **We tell you what happened** ([Webhooks](/api-reference/webhooks)).

Simple? In theory. Let's go deeper.

***

## Post Status Lifecycle

This is the most important thing to understand. A post is not just "scheduled" or "published". It goes through a state machine.

```mermaid theme={null}
stateDiagram-v2
    [*] --> DRAFT
    [*] --> SCHEDULED
    DRAFT --> SCHEDULED : User schedules
    SCHEDULED --> PROCESSING : Scanner picks it up
    PROCESSING --> POSTED : Success
    PROCESSING --> RETRYING : Temporary failure
    PROCESSING --> ERROR : Permanent failure
    PROCESSING --> REVIEW : Needs platform review
    RETRYING --> PROCESSING : Retry attempt
    ERROR --> PROCESSING : Manual retry
    REVIEW --> PROCESSING : Review scanner picks it up
```

### Status Breakdown

| Status | What It Means | What You Should Show |
| :- | :- | :- |
| `DRAFT` | Saved but not scheduled. No `postDate` set (or set in the past). | "Draft" - editable, not going anywhere yet. |
| `SCHEDULED` | Has a future `postDate`. Waiting in line. | "Scheduled for Dec 25 at 10:00 AM" |
| `PROCESSING` | We picked it up and are actively publishing it. | "Publishing..." - spinner time. |
| `POSTED` | Successfully published to the platform. | "Published" - show the permalink. |
| `RETRYING` | Failed, but we're going to try again. | "Retrying..." - don't panic yet. |
| `ERROR` | Failed after all retries. Dead. | "Failed" - show the error, offer manual retry. |
| `REVIEW` | Platform needs to review it (mostly TikTok). | "Under Review" - patience. |

### Retry Logic

When a post fails to publish, we don't give up immediately:

* **Max retries:** 3 attempts
* **Backoff:** Exponential, starting at 3 minutes
* **Between retries:** Status is set to `RETRYING`
* **After all retries exhausted:** Status becomes `ERROR`

If the error is a "review" error (common with TikTok), the post goes to `REVIEW` instead. We periodically re-check and re-attempt publishing.

<Note>
  **Manual retry:** Users can retry `ERROR` posts via the API. This resets the retry counter and re-queues the post. Max 3 manual retries total - we don't want infinite loops (we've seen things).
</Note>

***

## Step 1: Connect Accounts

Before you can schedule anything, the user needs to connect their social accounts. See the [Connect Flow](/api-reference/connect-social-accounts) guide for the full walkthrough.

Quick version: you redirect the user to our OAuth flow, they authorize, we give you a `socialAccountId`. Done.

***

## Step 2: Import History (Optional but Recommended)

Don't show an empty calendar. Nobody likes staring at a blank grid wondering if the app is broken.

Use the [Post History Import](/api-reference/import-posts) to fetch their recent posts and populate the calendar.

```typescript theme={null}
await bundlesocial.postHistoryImport.create({
  teamId: 'team_abc',
  socialAccountType: 'INSTAGRAM',
  count: 50,
  withAnalytics: true,
});
```

<Warning>
  **Imported posts are deleted after 30 days.** They're meant to populate your UI, not serve as a permanent archive. If you need them long-term, save them and don't let them go. See [Data Retention](/api-reference/data-retention).
</Warning>

***

## Step 3: Upload Media

**Crucial:** Upload media *before* the user hits "Schedule". You need the `uploadId` to create the post.

* **Simple Upload** - for images and small files. One request, done.
* **Multipart Upload** - for videos. The file goes up in 64 MiB chunks (init, PUT each part, complete), so a dropped connection costs one chunk instead of the whole transfer.

See [Media Upload](/api-reference/upload-content) for the full guide.

```typescript theme={null}
// Simple upload example
const upload = await bundlesocial.upload.create({
  teamId: 'team_abc',
  file: myImageFile,
});
const uploadId = upload.id; // e.g. "upload_123"
```

<Info>
  **Pro tip:** Always use Multipart Upload for videos. If a 500MB upload fails with Simple Upload, your user has to start over - with Multipart they lose one 64 MiB chunk and retry just that. One more thing worth wiring: if `complete` returns a 5xx, the parts are still stored, so retry `complete` rather than re-uploading. Your users will thank you. Your support inbox will thank you.
</Info>

***

## Step 4: Create the Post

Here's where it gets interesting. You can create a post as a **draft** or **schedule it immediately**.

### Schedule for the Future

```typescript theme={null}
const post = await bundlesocial.post.create({
  teamId: 'team_abc',
  title: "Launching something big",
  status: "SCHEDULED",
  socialAccountTypes: ['INSTAGRAM', 'TIKTOK'],

  // UTC ISO string
  postDate: "2026-12-25T10:00:00.000Z", // UTC ISO string

  // Platform-specific options
  data: {
    INSTAGRAM: {
      type: "REEL",
      text: "Launching something big tomorrow. Stay tuned.",
      uploadIds: ['upload_789']
    },
    TIKTOK: {
      type: "VIDEO",
      text: "Launching something big tomorrow. Stay tuned.",
      uploadIds: ['upload_789'],
      privacy: "PUBLIC_TO_EVERYONE",
      disableComments: false,
      disableDuet: false,
      disableStitch: false,
    }
  }
});
```

<Warning>
  **Timezones matter.** Always send `postDate` in **UTC**. If your user is in Tokyo and picks "10:00 AM", convert that to UTC before sending it to us. If you don't, they'll be posting at 3 AM Tokyo time and blaming you. And then they'll blame us. And then we'll blame you again.
</Warning>

### Save as Draft

Set `status: "DRAFT"` and pass an empty `postDate`:

```typescript theme={null}
const draft = await bundlesocial.post.create({
  teamId: 'team_abc',
  title: "Draft idea",
  status: "DRAFT",
  postDate: "",
  socialAccountTypes: ['INSTAGRAM'],
  data: {
    INSTAGRAM: {
      type: "POST",
      text: "Work in progress...",
      uploadIds: ['upload_789']
    }
  }
});
```

The user can come back later, edit it, and schedule it when ready.

### Platform-Specific Data Options

Each platform has its own special fields in the `data` object. Here are the highlights:

| Platform | Key Options |
| :- | :- |
| **Instagram** | `type` (`REEL`, `STORY`, `POST`), `thumbnail`, `thumbnailOffset`, `locationId` |
| **TikTok** | `privacy`, `disableComments`, `disableDuet`, `disableStitch`, `autoAddMusic`, `uploadToDraft` |
| **YouTube** | `text` (required title), `privacy`, `madeForKids`, `containsSyntheticMedia`, `hasPaidProductPlacement` |
| **Facebook** | `type` (`REEL`, `STORY`, `POST`) |
| **LinkedIn** | `privacy`, `hideFromFeed`, `disableReshare`, `link` |
| **Pinterest** | `boardName` (required - use the board name from `socialAccount.channels`), `text`, `link` |
| **Reddit** | `sr` (required, e.g. `r/example`), `text` (title), `flairId` |
| **Discord** | `channelId` (required), `username`, `avatarUrl` |
| **Slack** | `channelId` (required), `username`, `avatarUrl` |
| **Google Business** | `topicType`, `callToActionType`, `callToActionUrl`, event/offer fields |
| **Snapchat** | `type` (`STORY` or `SPOTLIGHT`), `description`, `locale`, `skipSaveToProfile` |

Check each [platform's page](/api-reference/platforms/index) for the full list of options and their constraints.

***

## Step 5: Edit or Cancel

### Update a Scheduled Post

Only `DRAFT` and `SCHEDULED` posts can be updated. Once a post is `PROCESSING` or beyond, it's too late.

```typescript theme={null}
await bundlesocial.post.update({
  postId: 'post_abc',
  text: "Updated copy. Much better.",
  postDate: "2026-12-26T10:00:00.000Z", // Reschedule
});
```

### Delete a Scheduled Post

Soft-deletes the post. Sets status to `DELETED`.

```typescript theme={null}
await bundlesocial.post.delete({
  postId: 'post_abc',
});
```

If the post was already `POSTED`, this only deletes it from our system - it does NOT remove it from the social platform. We can't un-ring that bell.

***

## Step 6: Handle the Results

Scheduling is **asynchronous**. You send us the post, we queue it, and you find out later what happened. There are two ways to know:

### Option A: Webhooks (Recommended)

Set up a [webhook endpoint](/api-reference/webhooks) and listen for:

| Event | Meaning | What To Do |
| :- | :- | :- |
| `post.published` | Post finished processing. `data.status` tells you whether it is `POSTED` or `ERROR`. | Update UI from `data.status`; show permalink or error. |
| `comment.published` | First comment finished processing. `data.status` tells you whether it is `POSTED` or `ERROR`. | Update UI if you show comment status. |

```typescript theme={null}
// Your webhook handler
app.post('/webhooks/bundle', (req, res) => {
  const event = req.body;

  switch (event.type) {
    case 'post.published':
      if (event.data.status === 'POSTED') {
        await updatePostStatus(event.data.id, 'published');
      } else if (event.data.status === 'ERROR') {
        await updatePostStatus(event.data.id, 'failed');
        await notifyUser(event.data.id, event.data.error);
      }
      break;
  }

  res.status(200).send('OK');
});
```

<Note>
  **Verify webhook signatures.** Don't trust random POST requests. We sign every webhook with HMAC SHA256. See [Webhooks](/api-reference/webhooks) for the verification code.
</Note>

### Option B: Polling

If you can't use webhooks, you can poll the post status:

```typescript theme={null}
const post = await bundlesocial.post.get({ postId: 'post_abc' });

if (post.status === 'POSTED') {
  // Show success
} else if (post.status === 'ERROR') {
  // Show error details in post.error
} else if (post.status === 'REVIEW') {
  // Tell user: "Platform is reviewing your post"
}
```

Don't poll every 100ms. Once every 30-60 seconds is fine. You won't miss anything by being patient.

### Error Notifications

If your organization has `sendEmailOnError` enabled, we'll email the user when their post fails. One less thing for you to build.

***

## Bulk Scheduling

Want to schedule 50 posts at once? Go for it. But be smart about it.

### Rate Limits

* **API rate limits:** Multi-layer limits per endpoint and tracker (API key / bearer token / IP fallback): burst `100/1s`, short `500/10s`, minute `2000/60s`. See [Rate Limits](/api-reference/rate-limits).
* **Platform limits:** Each platform has its own daily posting limits per team. Check our [Platform Limits](/api-reference/limits#daily-posting-limits-per-platform) for the exact numbers per tier. If you blast 50 TikToks in an hour, TikTok might have opinions.

### Best Approach

```typescript theme={null}
// Space them out. Don't schedule everything for the same second.
const posts = contentCalendar.map((item, index) => ({
  teamId: 'team_abc',
  title: item.title,
  status: 'SCHEDULED',
  socialAccountTypes: item.platforms,
  postDate: addMinutes(item.date, index * 5), // 5-minute gaps
  data: item.data,
}));

for (const post of posts) {
  await bundlesocial.post.create(post);
}
```

***

## Best Practices

### 1. Validate Before Scheduling

Don't let a user schedule a 10-minute video for an Instagram Story. It will fail. At 3 AM. On Christmas. And they will email you.

Check our [Platform Limits](/api-reference/limits) and validate in your UI before sending anything to us. We validate too, but catching errors early is better for everyone.

### 2. Timezones. Seriously.

We accept `postDate` in **UTC only**. Convert on your end. Every timezone bug in social media scheduling comes from someone who thought "eh, it's probably fine" and didn't convert.

### 3. First Comment Strategy

Use the Comment API to put hashtags in the first comment instead of the caption. It keeps the post clean and looks more professional.

```typescript theme={null}
await bundlesocial.comment.create({
  teamId: 'team_abc',
  internalPostId: post.id,
  title: "First comment",
  status: "SCHEDULED",
  postDate: post.postDate,
  socialAccountTypes: ['INSTAGRAM'],
  data: {
    INSTAGRAM: {
      text: "#growth #mindset #grind #blessed"
    }
  }
});
```

Create first comments through the [Comments API](/api-reference/comments), not inside the post payload. Schedule the post first, keep the returned `post.id`, then create the comment with `internalPostId`.

### 4. Remember Data Retention

* **Imported posts:** Deleted after 30 days. Store them if you need them.
* **Analytics:** Deleted after 30 days. Fetch daily if you're building reports.
* **Webhook events:** Deleted after 7 days. Log them on your end.

See [Data Retention](/api-reference/data-retention) for the full breakdown.

### 5. Handle the REVIEW Status

TikTok (and occasionally other platforms) may put posts into a review state instead of publishing immediately. This is normal. Don't show it as an error - show it as "Under Review" and let us handle it. We periodically re-check and re-attempt publishing.

### 6. Don't Forget `madeForKids` on YouTube

This is a **legal requirement** (COPPA). If the content targets children, you must set `madeForKids: true`. If you don't, YouTube will eventually notice, and penalties apply. We expose this field - use it.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Data Retention

> What we keep, for how long, and when it disappears. Analytics 30 days, webhook events 7, deleted uploads 2, stale uploads 14, imported posts 30, DMs and automation logs 30. Plan accordingly.

We don't keep your data forever. Storage costs money, and we are great on your wallet - don't exploit us. We are not running a digital museum. Here's exactly what gets cleaned up, when, and why.

***

## Analytics Data - 30 Days

**What:** All parsed and raw analytics data (profile analytics, post analytics, and their raw counterparts).

**Retention:** **30 days** from the date the analytics record was created.

After 30 days, the data is gone. Permanently. No backups. No "can you please recover it?". No.

### What You Should Do

If you need analytics history beyond 30 days (and you probably do if you're building dashboards or reports), set up a daily sync. Here's a battle-tested approach:

```typescript theme={null}
// analytics-sync.ts - Run this daily via cron
import { CronJob } from 'cron';

const syncAnalytics = async () => {
  // 1. Fetch all teams
  const teams = await yourDatabase.teams.findAll();

  for (const team of teams) {
    // 2. For each social account, fetch current analytics
    for (const account of team.socialAccounts) {
      const analytics = await bundlesocial.analytics.getSocialAccountAnalytics({
        teamId: team.id,
        socialAccountId: account.id,
      });

      // 3. Store with timestamp for historical tracking
      await yourDatabase.analyticsHistory.upsert({
        socialAccountId: account.id,
        date: new Date().toISOString().split('T')[0], // YYYY-MM-DD
        ...analytics,
        fetchedAt: new Date(),
      });
    }

    // 4. Fetch post analytics too
    const posts = await bundlesocial.analytics.getBulkPostAnalytics({
      teamId: team.id,
    });

    for (const post of posts.data) {
      await yourDatabase.postAnalyticsHistory.upsert({
        postId: post.id,
        date: new Date().toISOString().split('T')[0],
        ...post.analytics,
        fetchedAt: new Date(),
      });
    }
  }
};

// Run daily at 2 AM UTC
new CronJob('0 2 * * *', syncAnalytics, null, true, 'UTC');
```

With this running, you have full analytics history in your own database. Build dashboards, generate reports, impress clients - all without worrying about our 30-day window.

<Note>
  **Why 30 days?** We updated our cleanup/deletion methodology and now run a tighter, more consistent retention policy. If you need longer history, sync daily and store it on your side.
</Note>

***

## Webhook Events - 7 Days

**What:** All webhook event records (delivery attempts, payloads, responses).

**Retention:** **7 days** from the date the event was created.

If you need to debug a webhook delivery from last week, you have 7 days. After that, the record is gone.

### What You Should Do

Log webhook payloads on your end when you receive them. This is standard practice for any webhook integration. If you're not logging incoming webhooks, you're living dangerously.

***

## Deleted Uploads - 2 Days

**What:** Files you've deleted (images, videos) and their database records.

**Retention:** **2 days** after an upload is soft-deleted (by you, or by the stale-upload rule below).

When an upload is deleted, we don't immediately nuke the file. We keep it around for 2 days in case you change your mind. After 2 days:

* If the upload was used in a post: we remove the main file from storage but keep the database record, thumbnail and icon (so post history still shows a preview). The upload's `url` stops working.
* If the upload was never used: the files and the database record are all deleted.

Uploads attached to a draft or scheduled post can't be deleted.

## Stale Uploads - 14 Days

Uploads are cleaned up automatically on a **sliding 14-day window**:

* An upload stays alive as long as **any post using it is still a draft, scheduled or publishing**.
* Once that's no longer true, it's soft-deleted **14 days** after the later of: when it was uploaded, or when the last post using it reached `POSTED`, `ERROR` or `DELETED`.
* An upload that is **never attached to a post** is soft-deleted 14 days after upload.

After that, the 2-day deleted-upload window above applies.

<Tip>
  Scheduling far ahead is safe: attach the upload to the post **when you create the post**, and it stays until the post publishes. Don't upload now and create the post more than 14 days later.
</Tip>

***

## Imported Posts - 30 Days

**What:** Posts imported via the [Post History Import](/api-reference/import-posts) feature.

**Retention:** **30 days** from the date of import.

Imported posts are meant to populate your dashboard quickly - not to serve as a permanent archive. After 30 days, they're deleted (along with their analytics, via cascade).

### Monthly Import Counter Reset

Your import quota resets on the **1st of every month**. So if you hit your monthly limit, just wait for the calendar to flip.

***

## Direct Messages And Automation Logs - 30 Days

**What:** [Direct messages](/api-reference/direct-messages), conversations, and [automation](/api-reference/automations) execution logs (every run and every step).

**Retention:** at least **30 days** from when each message or run was created.

* Messages are deleted one by one as they turn 30 days old, so an ongoing conversation keeps its recent part.
* A conversation itself disappears once it has had no activity for 30 days and all of its messages are gone.
* Automation runs and their step logs go 30 days after the run. The same goes for records of button, quick reply and menu taps. Your flows, their versions, and your ice breakers and menus are not affected.

### Why

DMs are private conversations between your users and the people who write to them. We keep them only as long as the inbox and your automations need them, in line with Meta's platform rules. We'd rather not sit on other people's private messages.

### What You Should Do

If you need a longer history (support records, CRM, compliance), store messages on your side as they arrive. Every message reaches you as a [`conversation.message.created`](/api-reference/direct-messages/webhooks) webhook, and edits, unsends and status changes as `conversation.message.updated`. Saving those payloads is all it takes.

***

## Summary

| Data Type | Retention Period |
| :- | :- |
| Analytics (parsed + raw) | **30 days** |
| Webhook events | **7 days** |
| Deleted uploads | **2 days** after deletion |
| Stale uploads | Soft-deleted **14 days** after upload or after the last post using it finished, then the 2-day deleted-upload window applies |
| Imported posts | **30 days** |
| Direct messages and conversations | **30 days** |
| Automation execution logs | **30 days** |

***

## The Golden Rule

**If you need it long-term, store it yourself.**

We are optimized for real-time publishing and recent analytics. We are not Snowflake. We are not BigQuery. We are a social media API that happens to collect analytics as a side quest.

Set up a daily sync. It takes 20 minutes to build (we gave you the code above). You'll sleep better.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
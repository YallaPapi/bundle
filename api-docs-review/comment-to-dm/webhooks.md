> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Automation Webhooks

> The comment.received event and the other notifications your webhook starts getting.

As soon as the feature is on, your [webhook](https://info.bundle.social/api-reference/webhooks.md) starts receiving notifications for new activity. If your webhook has no event filter, you get them automatically:

| Event | When it fires |
| :- | :- |
| `comment.received` | Someone else commented on one of your posts. Facebook and Instagram: posts published through bundle.social. TikTok: those plus imported videos, once we've flipped the TikTok switch for you. |
| `conversation.created`, `conversation.message.created`, ... | New DMs and conversation changes, see [Direct Messages → Webhooks](https://info.bundle.social/api-reference/direct-messages/webhooks.md) |

`comment.received` fires for every such comment (comments by the account itself and your automated replies are left out), whether or not a flow reacts to it, so you can also use it to build a live comments feed. `data.comment` has the same shape as items from the [Comments API](https://info.bundle.social/api-reference/comments.md) (on imported TikTok videos, `postId` is `null` both there and in `data`, and `comment.importedPostId` is set instead), and its `id` is exactly the `fetchedCommentId` you use for [private replies](https://info.bundle.social/api-reference/direct-messages/private-replies.md) and [test runs](https://info.bundle.social/api-reference/automations/testing-and-logs.md#test-a-flow).

```json theme={null}
{
  "type": "comment.received",
  "data": {
    "comment": {
      "id": "fetched_1",
      "platform": "INSTAGRAM",
      "postId": "post_123",
      "socialAccountId": "sa_789",
      "externalId": "18001234567890",
      "externalParentId": null,
      "externalPostId": "17900000000000000",
      "text": "LINK please!",
      "authorName": "janedoe",
      "authorExternalId": "1789000000000000",
      "authorAvatarUrl": "https://...",
      "likesCount": 0,
      "repliesCount": 0,
      "publishedAt": "2026-09-26T09:30:00.000Z"
    },
    "postId": "post_123",
    "teamId": "team_123",
    "organizationId": "org_123",
    "socialAccountId": "sa_789",
    "platform": "INSTAGRAM"
  }
}
```

> [!WARNING]
>
> **Your endpoint has to keep up.** New comments and DMs can mean a lot of events. Answer each one with a `2xx` within 15 seconds, **including event types you don't handle**, and do the heavy work asynchronously. If your endpoint keeps failing and goes **7 days without a single successful delivery**, we disable it automatically. You'll get an email and a dashboard notification, and you then have to re-enable it (or set up a new one) in the [Webhooks dashboard](https://bundle.social/dashboard/organization/webhooks). Events sent while it was disabled are not replayed. More in [Webhooks](https://info.bundle.social/api-reference/webhooks.md).


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
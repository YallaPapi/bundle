> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Private Replies

> Answer a Facebook or Instagram comment with a direct message.

A private reply is a DM sent **in response to a public comment**. The classic use case: someone comments "price?" under your post and you answer in their inbox instead of in public.

Want to answer the comment **publicly** instead? That's the [Comments API](/api-reference/comments#replying-to-imported-comments) (`POST /api/v1/comment` with `fetchedParentCommentId`). Want either to happen on its own? That's [Automations](/api-reference/automations).

**Endpoint:** `POST /api/v1/conversations/private-reply`

```ts theme={null}
await fetch("https://api.bundle.social/api/v1/conversations/private-reply", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "x-api-key": process.env.BUNDLE_API_KEY,
  },
  body: JSON.stringify({
    teamId: "team_123",
    fetchedCommentId: "fetched_1",
    content: {
      text: "Hey! Just sent you the price list 👋",
    },
  }),
});
```

`fetchedCommentId` is the `id` of a comment you got from the [Comments API](/api-reference/comments) (`GET /api/v1/comment/import/comments`). Works for Facebook and Instagram comments.

Meta has strict rules here, and we follow them:

* **One private reply per comment.** If the first reply went out, sending again returns it with `conflict: true` instead of messaging the person twice. If the first attempt is still in progress or its outcome is unknown, you get `429` (see [Errors](/api-reference/direct-messages#errors)). If the platform rejected it, sending again really tries again.
* **Text only.** No attachments, buttons, quick replies, or carousels in a private reply.
* **The comment must be recent.** Meta accepts private replies up to 7 days after the comment was posted. We check this before sending on Facebook; on Instagram, Meta rejects late replies itself.
* **Facebook: top-level comments only.** On Facebook you can't send a private reply to a reply inside a comment thread.
* **Follow-ups wait for the person.** If the reply starts a new conversation, it has `platformData.canReply: false`: you can send more messages only after they answer, and then the usual 24-hour rule applies. If you already had an open conversation with that person, it keeps its reply window.

Private replies count toward your [monthly message limit](/api-reference/direct-messages#plans-and-limits) like any other message. On Instagram they use the account's comment permissions, so the account needs those in addition to messaging.

In the message list, a private reply has `source: "PRIVATE_REPLY"` and a `privateReplyContext` telling you which comment and post it was about, so your inbox can show "replied to your comment on..." like Instagram does.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# DM Webhooks

> Get every new DM and status change pushed to your server in real time.

The fastest way to build an inbox is to let us push changes to you. Webhooks are also how you keep a history longer than our [30-day retention](/api-reference/data-retention): save every `conversation.message.created` payload (and apply `conversation.message.updated` for edits, unsends and status changes) and you have the full thread on your side.

<Warning>
  **Heads-up: new events arrive as soon as the feature is on.** From then on we send your [webhook](/api-reference/webhooks) an event for every new DM (`conversation.*`) and every new comment from other people on posts you published through bundle.social (`comment.received`, described in [Automations](/api-reference/automations/webhooks)). If your webhook has no event filter, you get all of them automatically.

  Answer every event with a `2xx` within 15 seconds, **including event types you don't handle yet**. Just ignore them. If your endpoint keeps failing and goes **7 days without a single successful delivery**, we disable it automatically. You'll get an email and a dashboard notification, and you then have to re-enable it (or set up a new one) in the [Webhooks dashboard](https://bundle.social/dashboard/organization/webhooks). Events sent while it was disabled are not replayed. More in [Webhooks](/api-reference/webhooks).
</Warning>

Subscribe to these events on your webhook (or leave the event filter empty to get everything):

| Event | When it fires | `data` contains |
| :- | :- | :- |
| `conversation.created` | First message from a new participant (or first private reply) | Conversation |
| `conversation.updated` | Status, preview or participant info changed, or a new message raised the unread count | Conversation |
| `conversation.read.updated` | You marked it as read (unread count reset), or the participant read your messages (`platformSeenAt`) | Conversation |
| `conversation.message.created` | New message, incoming or outgoing | Message |
| `conversation.message.updated` | Status changed (`SENT` → `SEEN`...), edited, unsent, or reacted to | Message |

Payloads use the same shape as the [conversation and message objects](/api-reference/direct-messages/conversations) from the REST API, wrapped in the usual envelope. One difference: the top-level `replyTo` and `privateReplyContext` of a message are only filled in on REST reads. In webhooks, look at `platformData.replyTo` instead, or fetch the message.

```json theme={null}
{
  "type": "conversation.message.created",
  "data": {
    "id": "msg_1",
    "conversationId": "conv_abc",
    "teamId": "team_123",
    "socialAccountId": "sa_789",
    "platform": "INSTAGRAM",
    "direction": "INBOUND",
    "status": "DELIVERED",
    "source": "DM",
    "text": "Hi! Do you ship to Poland?",
    "attachments": [],
    "sentAt": "2026-09-26T09:30:00.000Z",
    "platformData": {},
    "createdAt": "2026-09-26T09:30:01.000Z",
    "updatedAt": "2026-09-26T09:30:01.000Z"
  }
}
```

## Example: A Tiny Inbox Handler

Verify the signature, answer fast, do the real work afterwards:

```ts theme={null}
import crypto from "node:crypto";
import express from "express";

const app = express();

// Keep the raw body - the signature is computed over the exact bytes we sent.
app.post("/webhooks/bundle", express.raw({ type: "application/json" }), async (req, res) => {
  const expected = crypto
    .createHmac("sha256", process.env.BUNDLE_WEBHOOK_SECRET!)
    .update(req.body)
    .digest("hex");
  const received = String(req.headers["x-signature"] ?? "");

  if (
    received.length !== expected.length ||
    !crypto.timingSafeEqual(Buffer.from(received), Buffer.from(expected))
  ) {
    return res.status(401).end();
  }

  const event = JSON.parse(req.body.toString("utf8"));
  res.status(200).end(); // ack first, we have 15 seconds

  if (event.type === "conversation.message.created" && event.data.direction === "INBOUND") {
    await saveToInbox(event.data); // your code
    await notifyAgents(event.data.conversationId); // your code
  }

  if (event.type === "conversation.message.updated") {
    await updateMessageStatus(event.data.id, event.data.status); // Messenger: SENT -> DELIVERED -> SEEN, Instagram: SENT -> SEEN
  }
});
```

<Tip>
  Deduplicate on `data.id` + `data.updatedAt`. Don't use `status` for this: edits, unsends and reactions change a message without changing its status. Retries (ours and Meta's) can occasionally deliver the same change twice.
</Tip>

Outgoing messages reach your webhook already as `SENT` or `FAILED`, never as `PENDING`.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
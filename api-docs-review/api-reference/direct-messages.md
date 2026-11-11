> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Direct Messages

> Read and answer Instagram and Facebook DMs through one API. Conversations, rich messages, private replies to comments, reactions, and real-time webhooks.

<Warning>
  **Allowlist only.** Direct Messages are not switched on by default. Email [support@bundle.social](mailto:support@bundle.social) with your **organization ID** (the `id` returned by `GET /api/v1/organization`) and we'll enable it for you. Until then every endpoint in this section answers `404`, which is on purpose, not a bug.

  Once it's on, two things are on you:

  1. **Reconnect** every Facebook and Instagram account with `withMessagingScope: true`, then **subscribe** each one to messages with `POST /api/v1/social-account/messaging/enable`. Accounts connected before the switch don't get DMs until you do. See [Setup](/api-reference/direct-messages/setup).
  2. **Accept the new webhook events.** Your webhook starts receiving an event for every new DM and every new comment on posts you published through bundle.social. Keep your endpoint answering `2xx`, or it gets disabled. See [Webhooks](/api-reference/direct-messages/webhooks).
</Warning>

The Direct Messages API gives you a unified inbox for Instagram and Facebook. New DMs land in bundle.social, we tell you about them with a webhook, and you answer through one endpoint no matter which platform the person wrote from.

With it you can:

* list conversations and read their full message history,
* send text, images, videos, buttons, quick replies and carousels,
* send a **private reply**: answer a public comment with a DM,
* react to messages, mark conversations as read, archive them,
* get every new message and status change in real time via webhooks.

Want replies to go out on their own? That's [Automations](/api-reference/automations), which are built on top of this API.

## Try It In The Dashboard

The inbox is already live in the bundle.social dashboard under **Conversations** ([bundle.social/dashboard/general/conversations](https://bundle.social/dashboard/general/conversations)). Read and answer DMs, react, archive, and see the 24-hour window in action before you build your own inbox on top of this API. Conversations and messages there are the same ones the API returns.

## In This Section

<CardGroup cols={2}>
  <Card title="Setup" icon="plug" href="/api-reference/direct-messages/setup">
    Reconnect accounts and subscribe them to DMs. Start here.
  </Card>

  <Card title="Conversations" icon="comments" href="/api-reference/direct-messages/conversations">
    List conversations, read message history, mark as read, archive.
  </Card>

  <Card title="Sending Messages" icon="paper-plane" href="/api-reference/direct-messages/sending-messages">
    Text, media, buttons, quick replies, carousels and reactions.
  </Card>

  <Card title="Private Replies" icon="reply" href="/api-reference/direct-messages/private-replies">
    Answer a Facebook or Instagram comment with a DM.
  </Card>

  <Card title="DM Webhooks" icon="webhook" href="/api-reference/direct-messages/webhooks">
    Every new message and status change pushed to your server.
  </Card>

  <Card title="Automations" icon="robot" href="/api-reference/automations">
    Let replies go out on their own.
  </Card>
</CardGroup>

## All Endpoints

All endpoints use your API key in the `x-api-key` header, same as the rest of the API.

| Method | Endpoint | What it does | Docs |
| :- | :- | :- | :- |
| `POST` | `/api/v1/social-account/messaging/enable` | Subscribe an account to DMs | [Setup](/api-reference/direct-messages/setup) |
| `POST` | `/api/v1/social-account/messaging/disable` | Stop DMs for an account | [Setup](/api-reference/direct-messages/setup#turning-it-off) |
| `GET` | `/api/v1/conversations` | List conversations | [Conversations](/api-reference/direct-messages/conversations#list-conversations) |
| `GET` | `/api/v1/conversations/:id` | Get one conversation | [Conversations](/api-reference/direct-messages/conversations#list-conversations) |
| `GET` | `/api/v1/conversations/:id/messages` | List messages in a conversation | [Conversations](/api-reference/direct-messages/conversations#read-messages) |
| `POST` | `/api/v1/conversations/:id/read` | Mark as read | [Conversations](/api-reference/direct-messages/conversations#mark-as-read) |
| `PATCH` | `/api/v1/conversations/:id` | Set status (`OPEN` / `ARCHIVED`) | [Conversations](/api-reference/direct-messages/conversations#archive-and-reopen) |
| `POST` | `/api/v1/conversations/:id/archive` | Archive | [Conversations](/api-reference/direct-messages/conversations#archive-and-reopen) |
| `POST` | `/api/v1/conversations/:id/open` | Reopen | [Conversations](/api-reference/direct-messages/conversations#archive-and-reopen) |
| `POST` | `/api/v1/conversations/:id/messages` | Send a message | [Sending Messages](/api-reference/direct-messages/sending-messages#send-a-message) |
| `POST` | `/api/v1/conversations/:id/messages/:messageId/reaction` | React or unreact | [Sending Messages](/api-reference/direct-messages/sending-messages#react-to-a-message) |
| `POST` | `/api/v1/conversations/private-reply` | DM someone who commented | [Private Replies](/api-reference/direct-messages/private-replies) |
| `POST` | `/api/v1/automation-rich-messages/conversations/:conversationId` | Send a message with uploaded media | [Automations](/api-reference/automations/building-flows#send-a-rich-message-by-hand) |

***

## Supported Platforms

| Platform | What is supported |
| :- | :- |
| `INSTAGRAM` | DMs for Instagram professional accounts (Business or Creator), private replies to comments, heart reactions |
| `FACEBOOK` | Messenger DMs for Facebook Pages, private replies to comments |

<Note>
  The `platform` field is **extensible**. We will add more messaging platforms over time, so treat unknown values gracefully (show a generic icon, skip the row) instead of switching over the list exhaustively.
</Note>

***

## Plans And Limits

Sending DMs is a paid-plan feature. Each connected account has a monthly quota of **outbound** messages:

| Plan | Outbound messages per account / month |
| :- | :- |
| Free | 0 |
| Pro | 200 |
| Business | 1,000 |

What counts: every message sent through bundle.social, whether it came from your API call, the dashboard, or an [automation](/api-reference/automations), including [private replies](/api-reference/direct-messages/private-replies). What doesn't count: incoming messages, messages that failed, messages the account owner typed directly in the Instagram or Messenger app, reactions, and marking a conversation as read. Quotas reset on the 1st of every month (UTC).

When the quota runs out, sends return `403` with `Monthly message limit reached`. Need a bigger bucket? [Contact us](https://bundle.social/contact).

<Info>
  **Messages are kept for 30 days.** Each message is deleted 30 days after it was created, and a conversation goes once it has been quiet for 30 days. Need a longer history? Store messages on your side as they arrive via [DM webhooks](/api-reference/direct-messages/webhooks). Details in [Data Retention](/api-reference/data-retention).
</Info>

***

## How It Works

### Conversations And Messages

A **conversation** is one thread between a connected account and one person (the *participant*). Each conversation belongs to a team and to one social account.

A **message** belongs to a conversation and has a `direction`:

* `INBOUND` - the participant wrote to you,
* `OUTBOUND` - you (or the account owner) wrote to them.

The `source` field tells you where a message came from:

| Source | Meaning |
| :- | :- |
| `DM` | Incoming message from the participant |
| `API` | Sent through bundle.social (API, dashboard, or an automation) |
| `PRIVATE_REPLY` | A private reply to one of the participant's comments |
| `ECHO` | Sent by the account owner directly from the Instagram or Messenger app |

Like `platform`, treat unknown `source` values gracefully.

### The 24-Hour Rule

This is the one rule you really need to know. **Meta only lets a business send a free-form message within 24 hours of the participant's last message.** After that, the conversation is read-only until the person writes again.

* `platformData.lastInboundAt` tells you when the participant last wrote. Use it to show "you can reply for another 3h" in your UI.
* `platformData.canReply: false` means the conversation was opened by a private reply and the person hasn't answered yet. You have to wait for them.

If you try anyway, you get a `400`:

| Message | What to do |
| :- | :- |
| `Meta only allows replies within 24 hours of the participant's last message` | Wait until the participant writes again. |
| `This conversation is waiting for the participant to reply first` | The person never wrote (or only got a private reply). Nothing to send until they do. |

<Note>
  This isn't us being strict for fun. Meta enforces the window on their side, we just stop the request early so you get a clear error instead of a cryptic one from Graph API.
</Note>

### Message Status

Outbound messages move through these statuses. Your own sends first reach your webhook as `conversation.message.created`, already `SENT` (or `FAILED`), and every later change arrives as `conversation.message.updated`. Incoming messages simply arrive as `DELIVERED`.

| Status | Meaning |
| :- | :- |
| `PENDING` | We're handing it to the platform |
| `SENT` | The platform accepted it |
| `DELIVERED` | It reached the participant's device |
| `SEEN` | The participant opened it |
| `FAILED` | It didn't go out. `error` holds a readable reason. |

Not every platform reports every step (Instagram doesn't send delivery receipts, for example), so a message can jump from `SENT` straight to `SEEN`.

***

## Errors

Errors come back as `{ "statusCode": 400, "message": "..." }`. The ones specific to messaging:

| Status | Message | Meaning |
| :- | :- | :- |
| `400` | `Meta only allows replies within 24 hours...` | The 24-hour window closed |
| `400` | `This conversation is waiting for the participant to reply first` | Nobody wrote to you yet in this thread |
| `400` | `Instagram DMs do not support phone buttons` | Use a `URL` button instead |
| `400` | `Private replies support text only...` | Remove attachments or the carousel from the private reply (buttons and quick replies are rejected as unknown fields) |
| `400` | `Facebook private replies are only supported for top-level comments` | Facebook doesn't allow private replies to thread replies |
| `400` | `Facebook private replies must be sent within 7 days of the comment` | The comment is too old |
| `403` | `Messaging is not enabled for this social account. Enable it first.` | Call `/social-account/messaging/enable` |
| `403` | `Monthly message limit reached...` | Quota used up for this account this month |
| `404` | `Not found` | Your organization is not on the allowlist yet. A wrong ID says what wasn't found, e.g. `Conversation not found`. |
| `429` | `Private reply send already claimed` | A private reply for this comment is being sent right now, or an earlier attempt timed out and may have been delivered. We never risk sending it twice, so don't keep retrying: check the conversation instead. |
| `503` | `Messaging is temporarily disabled...` | Sending is paused on our side (for example during a Meta incident). Retry in a few minutes. |

***

## Quick FAQ

### "I enabled messaging but no conversations show up."

Conversations only appear when someone writes **after** you enabled messaging (or when you send a private reply, or answer someone from the Instagram or Messenger app). Send a test DM to the account from another profile. If still nothing shows up, check the setup order: the account has to be reconnected with `withMessagingScope: true` **after** your organization was allowlisted, and only then subscribed with `messaging/enable`. Enabling on an account connected before the switch returns `400`, so reconnect first.

### "Can I start a conversation with anyone?"

No. Meta doesn't allow businesses to cold-DM people. Someone has to write to you first, or comment on your post so you can send a private reply.

### "How far back does the message history go?"

Up to 30 days. We only have messages that arrived after you enabled messaging on the account, and each one is deleted 30 days after it arrived. For anything older, keep your own copy from the webhooks.

### "Can I message someone after 24 hours?"

Not with a regular message. Once the participant writes again, the window reopens for another 24 hours.

### "Do messages from the Instagram app show up too?"

Yes. If the account owner answers from the Instagram or Messenger app, the message appears in the conversation with `source: "ECHO"`, so your inbox always shows the full thread. These don't count toward your quota.

### "Is there a WebSocket?"

Not in the public API. Use webhooks for real-time updates.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
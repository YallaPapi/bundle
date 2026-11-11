> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Conversations

> List conversations, read message history, paginate, mark as read, archive and reopen.

All endpoints on this page use your API key in the `x-api-key` header. The full endpoint list is on the [Direct Messages overview](/api-reference/direct-messages#all-endpoints).

***

## List Conversations

**Endpoint:** `GET /api/v1/conversations`

Query params:

* `teamId` (required)
* `platform` (optional) - `INSTAGRAM` or `FACEBOOK`
* `socialAccountId` (optional)
* `status` (optional) - `OPEN` or `ARCHIVED`
* `limit` (max 500), and either `offset` or `cursor`

Conversations come back with the most recent activity first.

```bash theme={null}
curl "https://api.bundle.social/api/v1/conversations?teamId=team_123&status=OPEN&limit=20" \
  -H "x-api-key: YOUR_KEY"
```

```json theme={null}
{
  "items": [
    {
      "id": "conv_abc",
      "teamId": "team_123",
      "socialAccountId": "sa_789",
      "platform": "INSTAGRAM",
      "externalConversationId": "aWdfdGhyZWFk...",
      "externalParticipantId": "1789000000000000",
      "participantUsername": "janedoe",
      "participantDisplayName": "Jane Doe",
      "participantAvatarUrl": "https://...",
      "status": "OPEN",
      "lastMessageAt": "2026-09-26T09:30:00.000Z",
      "lastActivityAt": "2026-09-26T09:30:00.000Z",
      "lastMessagePreview": "Hi! Do you ship to Poland?",
      "lastReadAt": null,
      "unreadCount": 1,
      "platformSeenAt": null,
      "platformData": {
        "lastInboundAt": "2026-09-26T09:30:00.000Z"
      },
      "socialAccount": { "id": "sa_789", "type": "INSTAGRAM", "username": "mybrand" },
      "createdAt": "2026-09-26T09:30:00.000Z",
      "updatedAt": "2026-09-26T09:30:00.000Z"
    }
  ],
  "total": 1,
  "nextCursor": "eyJ0IjoiMjAyNi0wOS0yNlQwOTozMDowMC4wMDBaIiwiaWQiOiJjb252X2FiYyJ9"
}
```

Useful fields:

* `unreadCount` / `lastReadAt` - your side's read state, see [Mark As Read](/api-reference/direct-messages/conversations#mark-as-read).
* `platformSeenAt` - when the participant last read your messages.
* `lastActivityAt` - what the list is sorted by.
* `platformData.lastInboundAt` / `canReply` - the [24-hour rule](/api-reference/direct-messages#the-24-hour-rule).
* `socialAccount` - the connected account the conversation belongs to.
* `externalConversationId` / `externalParticipantId` - the platform's own IDs for the thread and the person.

`GET /api/v1/conversations/:id` returns the same object for a single conversation.

***

## Pagination

Both list endpoints support two styles, pick one per request:

* **Offset:** `offset` + `limit`. Simple, good for page numbers.
* **Cursor:** pass the previous response's `nextCursor` back as `cursor`. For messages it stays stable while new ones keep arriving, so this is what you want for infinite scroll.

The conversation list is sorted by `lastActivityAt`, which changes with every new message. A conversation that gets a new message while you page through the list moves to the top, so it can be missing from later pages. Refresh the first page (or use [webhooks](/api-reference/direct-messages/webhooks)) to catch it.

`limit` defaults to 10 (max 500). `total` is only returned on the first page (when you don't send a `cursor`). Sending a `cursor` together with a non-zero `offset` returns `400`. When `nextCursor` is empty, you've reached the end.

***

## Read Messages

**Endpoint:** `GET /api/v1/conversations/:id/messages`

Pages walk **backwards in time** (the first page has the newest messages), but messages **inside** a page are ordered oldest first, so you can render them top to bottom without sorting.

```json theme={null}
{
  "items": [
    {
      "id": "msg_1",
      "conversationId": "conv_abc",
      "teamId": "team_123",
      "socialAccountId": "sa_789",
      "platform": "INSTAGRAM",
      "direction": "INBOUND",
      "status": "DELIVERED",
      "source": "DM",
      "externalMessageId": "aWdfZG1faWQ...",
      "text": "Hi! Do you ship to Poland?",
      "attachments": [],
      "sentAt": "2026-09-26T09:30:00.000Z",
      "seenAt": null,
      "failedAt": null,
      "error": null,
      "replyTo": null,
      "privateReplyContext": null,
      "platformData": {},
      "createdAt": "2026-09-26T09:30:01.000Z",
      "updatedAt": "2026-09-26T09:30:01.000Z"
    },
    {
      "id": "msg_2",
      "conversationId": "conv_abc",
      "platform": "INSTAGRAM",
      "direction": "OUTBOUND",
      "status": "SEEN",
      "source": "API",
      "text": "We do! Shipping takes 2-3 days.",
      "attachments": [],
      "sentAt": "2026-09-26T09:31:10.000Z",
      "seenAt": "2026-09-26T09:32:00.000Z",
      "replyTo": { "messageId": "msg_1", "externalMessageId": "aWdf...", "isSelfReply": false },
      "platformData": {
        "reactions": [{ "senderId": "1789000000000000", "reaction": "love", "emoji": "❤️" }]
      }
    }
  ],
  "total": 2,
  "nextCursor": null
}
```

Useful fields:

* `attachments[]` - `type` (`IMAGE`, `VIDEO`, `AUDIO`, `FILE`, `POST`, `UNKNOWN`) and a `url` when the platform gives one. `POST` is shared content on Messenger (a link or a shared post). On Instagram, shared posts, reels and story mentions currently arrive as `UNKNOWN`, with a `url` when Meta provides one.
* `replyTo` - set when the message is a reply to an earlier one. `messageId` points to our message if we have it.
* `privateReplyContext` - for private replies: the comment it answered (`text`, `authorName`, `postPermalink`, `postThumbnailUrl`, ...).
* `platformData.reactions` - reactions on the message.
* `platformData.isEdited` / `editedAt` - the participant edited their message. `text` already holds the new version.
* `platformData.isUnsent` / `unsentAt` - the participant unsent it. We clear `text` and `attachments` on our side. If you stored the content from an earlier webhook, delete or hide your copy too.
* `platformData.quickReplies`, `buttons`, `carousel` - the rich content of messages you sent.
* `platformData.isPostback` / `postbackPayload` - the participant tapped a `POSTBACK` button, an ice breaker or a menu item, and this is the payload behind it.
* `platformData.isEcho` - the account owner sent this from the Instagram or Messenger app.
* `error` / `failedAt` - why and when an outbound message failed.

<Note>
  Platform-hosted attachment URLs (images someone sent you) are signed by Meta and **expire**. If you need them long-term, download and store them yourself.
</Note>

***

## Mark As Read

**Endpoint:** `POST /api/v1/conversations/:id/read`

```json theme={null}
{ "readAt": "2026-09-26T09:35:00.000Z" }
```

`readAt` is optional (defaults to now). It resets `unreadCount` and also tries to show the participant a "seen" marker on the platform. That marker is best effort: it's skipped when messaging isn't enabled for the account or sending is paused on our side, and a platform error doesn't fail the call. If you send a `readAt` older than the last message, we only move `lastReadAt` and keep the counter, since you hadn't seen the newest message at that point.

***

## Archive And Reopen

* `POST /api/v1/conversations/:id/archive` - move it out of the active inbox,
* `POST /api/v1/conversations/:id/open` - bring it back,
* `PATCH /api/v1/conversations/:id` with `{ "status": "ARCHIVED" }` - same thing, generic form.

Archiving is a bundle.social inbox state, it doesn't archive the thread inside Instagram or Messenger. A new incoming message reopens an archived conversation automatically, so nobody gets lost in the archive.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
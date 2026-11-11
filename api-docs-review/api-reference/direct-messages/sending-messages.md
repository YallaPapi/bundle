> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Sending Messages

> Send text, media, buttons, quick replies and carousels, and react to messages.

Send messages into an existing conversation. You can only answer people who wrote to you in the last 24 hours, see [the 24-hour rule](/api-reference/direct-messages#the-24-hour-rule). To start from a comment instead, use a [private reply](/api-reference/direct-messages/private-replies).

## Send A Message

**Endpoint:** `POST /api/v1/conversations/:id/messages`

```ts theme={null}
const res = await fetch(`https://api.bundle.social/api/v1/conversations/${conversationId}/messages`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "x-api-key": process.env.BUNDLE_API_KEY,
  },
  body: JSON.stringify({
    content: {
      text: "We do! Shipping takes 2-3 days.",
    },
    replyToMessageId: "msg_1", // optional: link it to an earlier message in our data
  }),
});

const { conversation, message, conflict } = await res.json();
```

The response has three fields:

* `conversation` - the updated conversation,
* `message` - the message you just sent, with its current `status`,
* `conflict` - `true` means **nothing was sent this time**, because the same message had already gone out and `message` is that earlier one. Only [private replies](/api-reference/direct-messages/private-replies) return `true` (they are limited to one per comment). Regular sends always return `false`.

`replyToMessageId` is stored on our side and comes back as the message's `replyTo`, so your inbox can show which message you answered. It is not sent to the platform, so Instagram and Messenger don't show it as a quoted reply.

<Warning>
  Regular sends are **not** deduplicated. If a send times out on your side, list the conversation's messages before retrying, otherwise the customer may get the message twice.
</Warning>

If the platform rejects the message, the call returns an error status (see [Errors](/api-reference/direct-messages#errors)), not a `200`. The failed message still stays in the thread with `status: "FAILED"` and an `error`, and your webhook gets it as `conversation.message.created`.

***

## Message Content

A message needs at least one of `text`, `attachments`, or `carousel`.

| Field | Limit | Notes |
| :- | :- | :- |
| `text` | 1,000 characters | We check characters. Instagram itself counts **bytes**, so a long text with emoji or non-Latin letters can pass our check and still be rejected by Instagram |
| `attachments` | up to 10 | `{ "type": "IMAGE", "url": "https://..." }`. `IMAGE`, `VIDEO`, `AUDIO` or `FILE`, public **HTTPS** URL |
| `quickReplies` | up to 13 | `{ "label": "Yes", "payload": "SHIPPING_YES" }`, label up to 20 chars |
| `buttons` | up to 3 | `POSTBACK` (with `payload`), `URL` (with `url`) or `PHONE` (with `phoneNumber`), label up to 20 chars |
| `carousel` | up to 10 cards | each card: `title` (required) up to 80 chars, optional `subtitle` up to 80 chars, `imageUrl` and up to 3 `buttons` |

Rules of the road:

* Buttons and quick replies need `text` (it's the message the buttons hang under).
* A message has **either** buttons **or** quick replies, never both.
* A carousel can have `text` (sent as its own bubble before the cards), but no buttons, quick replies or attachments next to it.
* Instagram doesn't support `PHONE` buttons. Facebook does.
* All URLs must be HTTPS.
* Text and each attachment show up as separate bubbles on the platform, but you get one `message` back.

Quick replies:

```json theme={null}
{
  "content": {
    "text": "What can we help you with?",
    "quickReplies": [
      { "label": "Shipping", "payload": "TOPIC_SHIPPING" },
      { "label": "Returns", "payload": "TOPIC_RETURNS" },
      { "label": "Talk to a human", "payload": "TOPIC_HUMAN" }
    ]
  }
}
```

A button template:

```json theme={null}
{
  "content": {
    "text": "Your order is on the way!",
    "buttons": [
      { "type": "URL", "label": "Track package", "url": "https://yourshop.com/track/123" },
      { "type": "POSTBACK", "label": "I have a problem", "payload": "ORDER_PROBLEM" }
    ]
  }
}
```

A carousel:

```json theme={null}
{
  "content": {
    "carousel": {
      "cards": [
        {
          "title": "Classic Tee",
          "subtitle": "100% cotton, 29 EUR",
          "imageUrl": "https://yourshop.com/img/tee.jpg",
          "buttons": [{ "type": "URL", "label": "Buy", "url": "https://yourshop.com/p/tee" }]
        },
        {
          "title": "Hoodie",
          "subtitle": "Warm and fuzzy, 59 EUR",
          "imageUrl": "https://yourshop.com/img/hoodie.jpg",
          "buttons": [{ "type": "URL", "label": "Buy", "url": "https://yourshop.com/p/hoodie" }]
        }
      ]
    }
  }
}
```

When the participant taps a `POSTBACK` button, you get a message with `platformData.isPostback` and `postbackPayload`. A quick reply tap arrives as a normal message whose `text` is the quick reply's label. The payload isn't exposed on the message, but [automations](/api-reference/automations) can react to it with a `QUICK_REPLY_CLICKED` trigger.

<Tip>
  Want to attach files you already uploaded to bundle.social instead of public URLs? Use `POST /api/v1/automation-rich-messages/conversations/:conversationId`, which takes `uploadId`s. It's described in [Automations](/api-reference/automations/building-flows#send-a-rich-message-by-hand).
</Tip>

***

## React To A Message

**Endpoint:** `POST /api/v1/conversations/:id/messages/:messageId/reaction`

```json theme={null}
{ "action": "REACT", "reaction": "love" }
```

`reaction` is optional and defaults to `love`. Use `"action": "UNREACT"` to take it back. Only Instagram supports sending reactions, and only the heart (`love`): any other `reaction` value returns `400`. Facebook Messenger has no API for it, so there you can only *see* the reactions people leave.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
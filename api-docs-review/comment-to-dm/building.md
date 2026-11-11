> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Building Flows

> Write a flow definition: triggers, keywords, delays, conditions, steps and message formats.

A flow definition is one `trigger` plus up to 100 `steps`. It's what you send as `definition` when you [create or update a flow](https://info.bundle.social/api-reference/automations/managing-flows.md#create-edit-publish). Which triggers and steps each platform supports is in [Capabilities By Platform](https://info.bundle.social/api-reference/automations.md#capabilities-by-platform).

```json theme={null}
{
  "trigger": {
    "type": "COMMENT_CREATED",
    "platform": "INSTAGRAM",
    "socialAccountId": "sa_789",
    "postId": "post_123",
    "keywords": ["link", "info"],
    "matchMode": "ANY",
    "caseSensitive": false,
    "actionDelaySeconds": 0
  },
  "steps": [
    { "type": "SEND_PRIVATE_REPLY", "message": { "text": "Here you go: https://yourshop.com/drop" } },
    { "type": "SEND_PUBLIC_COMMENT_REPLY", "text": "Sent you a DM 👀" }
  ]
}
```

## Trigger Fields

| Field | Used by | Description |
| :- | :- | :- |
| `type` | all | Trigger type, see [Capabilities By Platform](https://info.bundle.social/api-reference/automations.md#capabilities-by-platform) |
| `platform` | all | `INSTAGRAM`, `FACEBOOK` or `TIKTOK` |
| `socialAccountId` | all | The account the flow listens on |
| `postId` | `COMMENT_CREATED` | **Required for comment triggers.** A post published through bundle.social on that account. **Must be left out** for DM and click triggers: a DM or click flow with a `postId` publishes fine but never fires. |
| `keywords` | comments, DMs | Up to 100, each up to 200 characters. Empty = every comment / message matches. |
| `matchMode` | comments, DMs | `ANY` (default): one keyword is enough. `ALL`: every keyword must appear. |
| `caseSensitive` | comments, DMs | Default `false` |
| `payloads` | clicks | Up to 100, each up to 1,000 characters. Only taps with one of these payloads match. Empty = any tap. |
| `senderExternalIds` | all | Optional. Only react to these people (platform user IDs). Great for testing on your own profile before going public. |
| `actionDelaySeconds` | all | Wait before running, 0 to 86,400 (24h). Default 0. **Recommended on TikTok: 5-10.** See [Delays](https://info.bundle.social/api-reference/automations/building-flows.md#delays). |

**Keyword matching** is whole-word and forgiving:

* `"link"` matches "send me the **link** pls" but not "**link**edin".
* Phrases work: `"free sample"` matches "can I get a free sample?".
* Extra spaces are always ignored, case is ignored unless `caseSensitive: true`, and Unicode is normalized, so accented and non-Latin keywords behave.
* Emoji and punctuation keywords match anywhere: `"🔥"` matches "🔥🔥🔥".

Keywords go on comment and DM triggers, `payloads` go on click triggers. Mixing them up is rejected.

> [!TIP]
>
> **Quick replies win over DMs.** When someone taps a quick reply, flows with a `QUICK_REPLY_CLICKED` trigger run first. Your `DM_RECEIVED` flows only see the tap if no quick-reply flow matched it, so one tap never gets two answers.

## Delays

`actionDelaySeconds` holds the run back before its first step. The clock starts when the comment or message reaches us. Three good reasons to set it:

1. **TikTok needs a moment. We recommend 5-10 seconds on every TikTok flow.** Right after TikTok tells us about a new comment, TikTok itself isn't always ready to accept a reply or a like on it yet. How long that takes depends on how busy TikTok's servers are: most of the time the reply works instantly, sometimes it needs a few extra seconds. Without a delay, the reply or like step can fail in those moments, and failed runs are not retried. A short delay costs you nothing and makes TikTok flows reliable.
2. **Feeling human.** An answer that lands 0.3 seconds after a DM doesn't feel like a person wrote it. A few seconds on DM flows reads more naturally.
3. **Anything else you want.** Reply a few minutes later so it looks like a person answered, or follow up with a DM an hour after someone asked. Up to 24 hours is possible.

Good to know:

* While it waits, the run is `QUEUED` in the [executions](https://info.bundle.social/api-reference/automations/testing-and-logs.md#executions).
* Pausing, archiving or deleting the flow cancels the runs that are still waiting (`CANCELED`).

> [!WARNING]
>
> **Watch the 24-hour window with delays on DMs.** Meta only allows DMs within 24 hours of the person's last message. A `SEND_MESSAGE` flow with a very long delay can wake up to a closed window and fail. Keep DM delays well below 24 hours.

## Condition Steps

A condition lets one flow handle several cases, or filter what the trigger let through:

```json theme={null}
{
  "type": "CONDITION",
  "conditions": [
    { "field": "TEXT", "operator": "CONTAINS", "value": "refund" }
  ]
}
```

| Field | Reads |
| :- | :- |
| `TEXT` | The comment or message text |
| `PAYLOAD` | The payload of the tapped button or quick reply |
| `PLATFORM` | `INSTAGRAM`, `FACEBOOK` or `TIKTOK` |
| `SENDER_ID` | The platform user ID of the person |

| Operator | Matches when |
| :- | :- |
| `CONTAINS` | The value appears anywhere in the field |
| `EQUALS` | The field equals the value exactly |
| `MATCHES_ANY` | The field equals one of a comma-separated list: `"value": "PRO,BUSINESS"` |

Comparisons ignore case unless `caseSensitive: true`. **All** rules in one condition step must match. If they don't, the run stops there as `SKIPPED` (and doesn't use your quota).

## Step IDs

Steps can have an optional `id`. Without one we generate it from the type and position (`dm-1`, `private-reply-2`, ...). IDs must be unique within a flow. Set your own if you want stable names in the execution logs.

***

## Messages In Automations

`SEND_MESSAGE` accepts a rich message:

| Field | Limit |
| :- | :- |
| `text` | 1,000 characters (Instagram: 1,000 **bytes**, emoji and non-Latin letters count more) |
| `attachments` | 1, `IMAGE` or `VIDEO`, as `{ "uploadId": "...", "type": "IMAGE" }`, file up to 24 MB |
| `quickReplies` | up to 13, label up to 20 characters |
| `buttons` | up to 3. `POSTBACK` and `URL` everywhere, `PHONE` on Facebook only |
| `carousel` | up to 10 cards, `title` / `subtitle` up to 80 characters, `imageUploadId`, up to 3 buttons per card |

Media comes from your [uploads](https://info.bundle.social/api-reference/upload-content.md): upload once with `POST /api/v1/upload`, then reference the `uploadId`. Carousel images must be image uploads.

Every quick reply, button and carousel card needs an `id` (your choice, up to 36 characters, e.g. `"btn-pricing"`). Same rules as in [Direct Messages](https://info.bundle.social/api-reference/direct-messages/sending-messages.md#message-content): buttons and quick replies need `text`, never both in one message, and a carousel travels alone.

`SEND_PRIVATE_REPLY` is **text only** (Meta allows exactly one private message per comment). `SEND_PUBLIC_COMMENT_REPLY` takes plain `text`: up to 1,000 characters on Facebook, 1,000 bytes on Instagram and **150 characters on TikTok**.

***

## Send A Rich Message By Hand

**Endpoint:** `POST /api/v1/automation-rich-messages/conversations/:conversationId`

Sends a message into a conversation with the **same format as a `SEND_MESSAGE` step**, uploads and all. Useful when an agent takes over from an automation and wants to send the same product carousel.

```json theme={null}
{
  "teamId": "team_123",
  "message": {
    "text": "Here's our bestseller 👇",
    "attachments": [{ "uploadId": "upload_456", "type": "IMAGE" }]
  }
}
```

Returns `{ conversationId, messageId, externalMessageId }`. The 24-hour rule and your message quota apply, same as [sending a normal DM](https://info.bundle.social/api-reference/direct-messages/sending-messages.md#send-a-message).


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
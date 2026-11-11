> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Recipes

> Copy-paste flows: comment-to-DM, DM with quick replies, TikTok replies, conditions and monitoring.

Ready-to-use flows for the most common cases. Most are complete `POST /api/v1/automations` bodies, the shorter ones show just the `definition`. Swap in your own `teamId`, `socialAccountId` and `postId`, create the flow, then [publish](https://info.bundle.social/api-reference/automations/managing-flows.md#create-edit-publish).

Need something that isn't here? Build it in the [dashboard](https://info.bundle.social/api-reference/automations.md#try-it-in-the-dashboard) and copy the **API definition** it shows.

## Comment "LINK" → Get A DM

The classic Instagram growth funnel. Someone comments a keyword, they get the link privately and a public reply that makes others comment too.

```json theme={null}
{
  "teamId": "team_123",
  "name": "Reel - LINK funnel",
  "platformScope": "INSTAGRAM",
  "definition": {
    "trigger": {
      "type": "COMMENT_CREATED",
      "platform": "INSTAGRAM",
      "socialAccountId": "sa_789",
      "postId": "post_123",
      "keywords": ["link", "info", "send"]
    },
    "steps": [
      {
        "type": "SEND_PRIVATE_REPLY",
        "message": { "text": "Hey! Here's the link you asked for 🔗 https://yourshop.com/drop" }
      },
      { "type": "SEND_PUBLIC_COMMENT_REPLY", "text": "Sent 📩 check your DMs!" }
    ]
  }
}
```

When the person answers the private reply, the conversation opens up and your `DM_RECEIVED` flows can take it from there.

## DM Flow With Quick Replies

Two flows. The first answers "price" with a question, the second answers the tap.

```json theme={null}
{
  "teamId": "team_123",
  "name": "Pricing - ask",
  "platformScope": "INSTAGRAM",
  "definition": {
    "trigger": {
      "type": "DM_RECEIVED",
      "platform": "INSTAGRAM",
      "socialAccountId": "sa_789",
      "keywords": ["price", "pricing", "how much"],
      "actionDelaySeconds": 3
    },
    "steps": [
      {
        "type": "SEND_MESSAGE",
        "message": {
          "text": "Happy to help! Which plan are you looking at?",
          "quickReplies": [
            { "id": "qr-starter", "label": "Starter", "payload": "PLAN_STARTER" },
            { "id": "qr-pro", "label": "Pro", "payload": "PLAN_PRO" },
            { "id": "qr-human", "label": "Talk to a human", "payload": "HUMAN" }
          ]
        }
      }
    ]
  }
}
```

```json theme={null}
{
  "teamId": "team_123",
  "name": "Pricing - Pro answer",
  "platformScope": "INSTAGRAM",
  "definition": {
    "trigger": {
      "type": "QUICK_REPLY_CLICKED",
      "platform": "INSTAGRAM",
      "socialAccountId": "sa_789",
      "payloads": ["PLAN_PRO"]
    },
    "steps": [
      {
        "type": "SEND_MESSAGE",
        "message": {
          "text": "Pro is 49 EUR/month and includes everything in Starter plus analytics.",
          "buttons": [
            { "id": "btn-buy", "type": "URL", "label": "Get Pro", "url": "https://yourshop.com/pro" },
            { "id": "btn-done", "type": "POSTBACK", "label": "That's all, thanks", "payload": "DONE" }
          ]
        }
      }
    ]
  }
}
```

And one more to tidy up when they tap "That's all, thanks":

```json theme={null}
{
  "trigger": {
    "type": "BUTTON_CLICKED",
    "platform": "INSTAGRAM",
    "socialAccountId": "sa_789",
    "payloads": ["DONE"]
  },
  "steps": [
    { "type": "SEND_MESSAGE", "message": { "text": "Anytime! 👋" } },
    { "type": "ARCHIVE_CONVERSATION" }
  ]
}
```

## TikTok: Reply And Like

```json theme={null}
{
  "teamId": "team_123",
  "name": "TikTok - drop comments",
  "platformScope": "TIKTOK",
  "definition": {
    "trigger": {
      "type": "COMMENT_CREATED",
      "platform": "TIKTOK",
      "socialAccountId": "sa_tiktok_1",
      "postId": "post_456",
      "keywords": ["when", "drop", "release"],
      "actionDelaySeconds": 8
    },
    "steps": [
      { "type": "SEND_PUBLIC_COMMENT_REPLY", "text": "Dropping Friday 6pm CET 🔥 link in bio" },
      { "type": "LIKE_COMMENT" }
    ]
  }
}
```

Remember the 150-character limit for TikTok replies. The 8-second delay is there on purpose: TikTok sometimes needs a moment before a new comment can be replied to or liked (see [Delays](https://info.bundle.social/api-reference/automations/building-flows.md#delays)).

## Route By Keyword With A Condition

One Facebook flow that listens to every DM, but only answers refund questions:

```json theme={null}
{
  "trigger": {
    "type": "DM_RECEIVED",
    "platform": "FACEBOOK",
    "socialAccountId": "sa_fb_1"
  },
  "steps": [
    {
      "type": "CONDITION",
      "conditions": [{ "field": "TEXT", "operator": "CONTAINS", "value": "refund" }]
    },
    {
      "type": "SEND_MESSAGE",
      "message": {
        "text": "Sorry to hear that! You can request a refund here, it takes 2 minutes.",
        "buttons": [
          { "id": "btn-refund", "type": "URL", "label": "Request refund", "url": "https://yourshop.com/refund" },
          { "id": "btn-call", "type": "PHONE", "label": "Call us", "phoneNumber": "+48123456789" }
        ]
      }
    }
  ]
}
```

(`PHONE` buttons are fine here because it's Facebook. On Instagram use a `URL` button.)

## Monitor Your Automations From Your Backend

There are no automation-specific webhooks. Messages sent by automations are normal messages, so they arrive as [`conversation.message.created`](https://info.bundle.social/api-reference/direct-messages/webhooks) events like everything else. For run-level monitoring, poll the executions:

```ts theme={null}
const res = await fetch(
  `https://api.bundle.social/api/v1/automations/${flowId}/executions?teamId=team_123&status=FAILED&limit=50`,
  { headers: { "x-api-key": process.env.BUNDLE_API_KEY } },
);

const { items } = await res.json();

for (const execution of items) {
  const failedStep = execution.steps?.find((step) => step.status === "FAILED");
  console.warn(execution.id, failedStep?.stepId, failedStep?.error?.message ?? execution.error?.message);
}
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
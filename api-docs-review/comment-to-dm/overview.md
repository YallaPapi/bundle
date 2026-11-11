> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Automations

> Auto-reply to comments and DMs on Instagram, Facebook and TikTok. Keyword triggers, private replies, quick replies, buttons, execution logs and platform menus.

> [!WARNING]
>
> **Allowlist only.** Automations are not switched on by default. Email [support@bundle.social](mailto:support@bundle.social) with your **organization ID** (the `id` returned by `GET /api/v1/organization`) and we'll enable it. Planning TikTok comment automations? Mention it in the email, there is one extra switch we flip for that. Until then every endpoint in this section answers `404`.
>
> Once it's on, two things are on you:
>
> 1. **Reconnect** your Facebook and Instagram accounts with `withMessagingScope: true`, then **subscribe** each one to messages with `POST /api/v1/social-account/messaging/enable`. Accounts connected before the switch receive neither comments nor DMs until you do. See [Before You Start](https://info.bundle.social/api-reference/automations.md#before-you-start).
> 2. **Accept the new webhook events.** Your webhook starts receiving an event for every new comment on your posts and every new DM. Keep your endpoint answering `2xx`, or it gets disabled. See [Webhooks](https://info.bundle.social/api-reference/automations/webhooks.md).

Automations reply for you. Someone comments "LINK" under your reel, and a second later they get a DM with the link. Someone asks "price?" in your inbox, and they get a message with buttons. Nobody on your team had to be awake for it.

You describe **what should happen** as a flow (a trigger plus a list of steps), publish it, and we run it on every matching comment or message.

## Try It In The Dashboard

Automations are already live in the bundle.social dashboard under **Automations** ([bundle.social/dashboard/general/automations](https://bundle.social/dashboard/general/automations)), so you can see how everything works before writing a line of code.

* **Use it as a flow builder.** Click a flow together, and the **API definition** panel next to it shows the exact `definition` JSON this API expects, with the real IDs from your team. Copy it into your `POST /api/v1/automations` or `PATCH` call and you're done.
* **Watch it run.** The execution logs show every run and what each step did, the same data as [Testing & Execution Logs](https://info.bundle.social/api-reference/automations/testing-and-logs.md).
* **Ice breakers and the persistent menu** can be set up there too.
* It's the same data either way: flows created through the API show up in the dashboard, and the other way around.

## In This Section

> **[Building Flows](https://info.bundle.social/api-reference/automations/building-flows.md)**
>
> Triggers, keywords, delays, conditions and message formats.

> **[Managing Flows](https://info.bundle.social/api-reference/automations/managing-flows.md)**
>
> Create, publish, pause, archive, delete and copy flows.

> **[How Flows Behave](https://info.bundle.social/api-reference/automations/how-flows-behave.md)**
>
> What happens in practice, and the built-in safety limits. Read before you build.

> **[Testing & Execution Logs](https://info.bundle.social/api-reference/automations/testing-and-logs.md)**
>
> Test a flow and see why every run did what it did.

> **[Ice Breakers & Persistent Menu](https://info.bundle.social/api-reference/automations/provider-settings.md)**
>
> Instagram ice breakers, Messenger menu and Get Started button.

> **[Automation Webhooks](https://info.bundle.social/api-reference/automations/webhooks.md)**
>
> `comment.received` and the other events your webhook starts getting.

> **[Recipes](https://info.bundle.social/api-reference/automations/recipes.md)**
>
> Copy-paste flows for the most common use cases.

> **[Direct Messages](https://info.bundle.social/api-reference/direct-messages.md)**
>
> The inbox API automations are built on.

## All Endpoints

All endpoints use your API key in the `x-api-key` header, same as the rest of the API.

| Method | Endpoint | What it does | Docs |
| :- | :- | :- | :- |
| `GET` | `/api/v1/automations` | List flows | [Managing Flows](https://info.bundle.social/api-reference/automations/managing-flows.md#list-flows) |
| `POST` | `/api/v1/automations` | Create a flow (as a draft) | [Managing Flows](https://info.bundle.social/api-reference/automations/managing-flows.md#create-edit-publish) |
| `GET` | `/api/v1/automations/:id` | Get a flow with its draft and published versions | [Managing Flows](https://info.bundle.social/api-reference/automations/managing-flows.md#the-flow-object) |
| `PATCH` | `/api/v1/automations/:id` | Rename, or save a new draft definition | [Managing Flows](https://info.bundle.social/api-reference/automations/managing-flows.md#create-edit-publish) |
| `POST` | `/api/v1/automations/:id/publish` | Validate and go live | [Managing Flows](https://info.bundle.social/api-reference/automations/managing-flows.md#create-edit-publish) |
| `POST` | `/api/v1/automations/:id/pause` | Stop running, keep the config | [Managing Flows](https://info.bundle.social/api-reference/automations/managing-flows.md#pause-activate-archive-delete) |
| `POST` | `/api/v1/automations/:id/activate` | Go live again | [Managing Flows](https://info.bundle.social/api-reference/automations/managing-flows.md#pause-activate-archive-delete) |
| `POST` | `/api/v1/automations/:id/archive` | Retire without deleting | [Managing Flows](https://info.bundle.social/api-reference/automations/managing-flows.md#pause-activate-archive-delete) |
| `DELETE` | `/api/v1/automations/:id` | Delete a flow | [Managing Flows](https://info.bundle.social/api-reference/automations/managing-flows.md#pause-activate-archive-delete) |
| `POST` | `/api/v1/automations/copy` | Copy flows to another team | [Managing Flows](https://info.bundle.social/api-reference/automations/managing-flows.md#copy-flows-between-teams) |
| `POST` | `/api/v1/automations/:id/test` | Run the flow once, right now | [Testing](https://info.bundle.social/api-reference/automations/testing-and-logs.md#test-a-flow) |
| `GET` | `/api/v1/automations/:id/executions` | Execution logs of one flow | [Execution Logs](https://info.bundle.social/api-reference/automations/testing-and-logs.md#executions) |
| `GET` | `/api/v1/automation-executions/:id` | One execution with every step | [Execution Logs](https://info.bundle.social/api-reference/automations/testing-and-logs.md#executions) |
| `GET` | `/api/v1/automation-provider-settings` | List ice breakers / persistent menus | [Provider Settings](https://info.bundle.social/api-reference/automations/provider-settings.md) |
| `PUT` | `/api/v1/automation-provider-settings/:socialAccountId/:type` | Save one | [Provider Settings](https://info.bundle.social/api-reference/automations/provider-settings.md#save-then-sync) |
| `POST` | `/api/v1/automation-provider-settings/:id/sync` | Push it to the platform | [Provider Settings](https://info.bundle.social/api-reference/automations/provider-settings.md#save-then-sync) |
| `POST` | `/api/v1/automation-rich-messages/conversations/:conversationId` | Send a rich message by hand | [Building Flows](https://info.bundle.social/api-reference/automations/building-flows.md#send-a-rich-message-by-hand) |

***

## Which Tool Do I Need?

Not everything is an automation. Pick the right tool first:

| You want to... | Use |
| :- | :- |
| Reply to a comment **publicly**, by hand | [Comments API](https://info.bundle.social/api-reference/comments.md#replying-to-imported-comments): `POST /api/v1/comment` with `fetchedParentCommentId` |
| Hide, delete or like a comment (where the platform allows it), by hand | [Comments API](https://info.bundle.social/api-reference/comments.md#actions-on-fetched-comments): `POST /api/v1/comment/import/comments/:commentId/action` |
| Answer a comment **with a DM**, by hand | [Private replies](https://info.bundle.social/api-reference/direct-messages/private-replies.md): `POST /api/v1/conversations/private-reply` |
| Read and answer DMs, by hand | [Direct Messages](https://info.bundle.social/api-reference/direct-messages.md) |
| Do any of the above **automatically** | Automations (this section) |

All of them work on the same comments and conversations. A comment your flow answered can still be moderated by hand, and a conversation started by an automation shows up in the DM inbox.

***

## Supported Platforms

| Platform | What automations can do |
| :- | :- |
| `INSTAGRAM` | React to comments, DMs and button taps. Send DMs, private replies and public comment replies. Manage ice breakers. |
| `FACEBOOK` | The same comment and DM features as Instagram, plus liking comments. Instead of ice breakers, manage the Messenger persistent menu and Get Started button. |
| `TIKTOK` | **Comments only.** React to new comments, reply publicly, like the comment. |

> [!NOTE]
>
> TikTok has no DM automations. TikTok flows work on comments and nothing else.

***

## Plans And Limits

Automations are a paid-plan feature. Each connected account has a monthly budget of **automation runs**:

| Plan | Runs per account / month |
| :- | :- |
| Free | 0 |
| Pro | 200 |
| Business | 1,000 |

* One run = one flow reacting to one comment or message, no matter how many steps it has.
* Runs that stop at a condition, get skipped by a safety limit (see [Safety Limits](https://info.bundle.social/api-reference/automations/how-flows-behave.md#safety-limits)), or get canceled **don't count**.
* Runs that fail **do** count, and so do [test runs](https://info.bundle.social/api-reference/automations/testing-and-logs.md#test-a-flow), since they really send messages.
* DMs sent by automations also count toward the account's [monthly message quota](https://info.bundle.social/api-reference/direct-messages.md#plans-and-limits).
* When the budget runs out, new runs are recorded as `SKIPPED` with the code `AUTOMATION_MONTHLY_LIMIT_REACHED`. Quotas reset on the 1st of every month (UTC).

Need more? [Contact us](https://bundle.social/contact).

***

## Before You Start

Once your organization is on the allowlist:

1. **Reconnect your Facebook and Instagram accounts** with `withMessagingScope: true`. This covers accounts that were already connected before the switch. Until they are reconnected they have no messaging permissions, and we don't receive their new comments either, so no flow on them can ever fire.
2. **Subscribe each account to messages** with `POST /api/v1/social-account/messaging/enable`. This registers it for Meta's message webhooks. It's needed for any flow that reacts to DMs or button taps, or sends DMs or private replies. A flow that only replies publicly or likes comments works without it. Both steps are two API calls, see [Direct Messages → Setup](https://info.bundle.social/api-reference/direct-messages/setup.md).
3. **TikTok** accounts need comment management permissions. A regular TikTok connection has them. If publishing a flow complains about permissions, reconnect the account. Also give every TikTok flow a 5-10 second [delay](https://info.bundle.social/api-reference/automations/building-flows.md#delays).
4. **Comment flows** only work on posts **published through bundle.social** on that account. You point the flow at one with `postId`.
5. **Your webhook endpoint accepts the new events** (see [Webhooks](https://info.bundle.social/api-reference/automations/webhooks.md)).

If an account is missing permissions, publishing the flow fails with a clear message such as `Instagram account must be reconnected with messaging permissions`.

### Where The IDs Come From

| ID | Where to get it |
| :- | :- |
| `teamId`, `socialAccountId` | `GET /api/v1/team/:id` returns the team with its `socialAccounts[]`. `messaging/enable` also returns the `socialAccountId`. |
| `postId` | The `id` you got back from `POST /api/v1/post`. It's the bundle.social post, not the Instagram or TikTok post ID. |
| `conversationId` | `GET /api/v1/conversations`, or any `conversation.*` [webhook](https://info.bundle.social/api-reference/automations/webhooks.md) |
| `fetchedCommentId` | The `comment.id` of a `comment.received` [webhook](https://info.bundle.social/api-reference/automations/webhooks.md), or `GET /api/v1/comment/import/comments` |
| `senderExternalIds` | A person's platform ID: `externalParticipantId` on a conversation, or `authorExternalId` on a comment |
| `uploadId` | `POST /api/v1/upload` ([Upload Content](https://info.bundle.social/api-reference/upload-content.md)) |

***

## How It Works

A **flow** is one trigger plus up to 100 steps:

```
Trigger: someone comments "link" on post_123 (Instagram)
  → Step 1: send them a private reply with the link
  → Step 2: reply publicly "Check your DMs 👀"
```

1. **Trigger.** An event arrives: a new comment, a new DM, or a tap on a button or quick reply. We look for published, active flows whose trigger matches it.
2. **Run.** Each matching flow gets its own **execution** (a run). If the trigger has a delay, the run waits for it.
3. **Steps.** Steps run top to bottom. A `CONDITION` step that doesn't match stops the run right there.
4. **Log.** Every run and every step is recorded, with inputs, outputs and errors. That's your debugging tool, see [Executions](https://info.bundle.social/api-reference/automations/testing-and-logs.md#executions).

### Drafts And Publishing

Flows are versioned, so you can edit safely while the old version keeps running. Changes are saved as a **draft**, and **nothing you edit goes live until you publish it**. Details in [Managing Flows](https://info.bundle.social/api-reference/automations/managing-flows.md#lifecycle).

| Flow status | Meaning |
| :- | :- |
| `DRAFT` | Never published. Doesn't run. |
| `ACTIVE` | Live. Runs on every matching event. |
| `PAUSED` | Temporarily off. Keeps its configuration, runs waiting on a delay are canceled. |
| `ARCHIVED` | Retired. Doesn't run until you activate or publish it again. |

***

## Capabilities By Platform

### Triggers

| Trigger | Instagram | Facebook | TikTok | Fires when |
| :- | :-: | :-: | :-: | :- |
| `COMMENT_CREATED` | ✅ | ✅ | ✅ | Someone comments on the post in `postId` |
| `DM_RECEIVED` | ✅ | ✅ | - | Someone sends a DM to the account |
| `QUICK_REPLY_CLICKED` | ✅ | ✅ | - | Someone taps one of your quick replies |
| `BUTTON_CLICKED` | ✅ | ✅ | - | Someone taps a `POSTBACK` button, an ice breaker, or a persistent menu item |

### Steps

| Step | Instagram | Facebook | TikTok | What it does |
| :- | :-: | :-: | :-: | :- |
| `CONDITION` | ✅ | ✅ | ✅ | Continue only if all rules match |
| `SEND_MESSAGE` | ✅ | ✅ | - | Send a DM (text, media, buttons, quick replies, carousel) |
| `SEND_PRIVATE_REPLY` | ✅ | ✅ | - | Answer a comment with a DM |
| `SEND_PUBLIC_COMMENT_REPLY` | ✅ | ✅ | ✅ | Reply to the comment publicly |
| `LIKE_COMMENT` | - | ✅ | ✅ | Like the comment |
| `ARCHIVE_CONVERSATION` | ✅ | ✅ | - | Move the conversation to archive |
| `OPEN_CONVERSATION` | ✅ | ✅ | - | Move the conversation back to the active inbox |

### Which Steps Fit Which Trigger

Some combinations make no sense (or Meta forbids them), so publishing rejects them:

* `SEND_PRIVATE_REPLY`, `SEND_PUBLIC_COMMENT_REPLY` and `LIKE_COMMENT` need a `COMMENT_CREATED` trigger. There's no comment to reply to otherwise.
* `SEND_MESSAGE` needs a `DM_RECEIVED`, `QUICK_REPLY_CLICKED` or `BUTTON_CLICKED` trigger. To DM a commenter, use `SEND_PRIVATE_REPLY`. Meta doesn't allow any other message until they answer it.
* `ARCHIVE_CONVERSATION` / `OPEN_CONVERSATION` need a DM or click trigger, or a `SEND_PRIVATE_REPLY` earlier in the flow (that's what creates the conversation).
* Every flow needs at least one step that actually does something (not only conditions).

***

## Quick FAQ

### "My flow is ACTIVE but nothing happens."

Check in this order:

1. Was the account reconnected **after** your organization was allowlisted? Accounts connected earlier don't send us comments or DMs. See [Before You Start](https://info.bundle.social/api-reference/automations.md#before-you-start).
2. Is it a comment flow? The post in `postId` must be published through bundle.social on the same account.
3. Did you edit it after publishing? Edits are drafts until you publish again.
4. Do the keywords really match? They match whole words: `"link"` won't match "links".
5. Look at the executions. If runs are there as `SKIPPED`, `error.code` tells you why. No error means a condition stopped the run, `output.skippedAtStepId` says which one.
6. No executions at all for a DM flow? Make sure the account is subscribed with `messaging/enable` ([Direct Messages → Setup](https://info.bundle.social/api-reference/direct-messages/setup.md)).
7. Still no executions? While automations are paused on our side (for example during a platform incident), incoming events don't create runs at all, so nothing shows up in the logs.

### "Can one comment or message trigger several flows?"

Yes, every matching flow runs (up to 25), and each one sends its own reply. If that's not what you want, make the keywords not overlap.

### "Why did someone get two replies to one message?"

Two flows matched the same message, usually a catch-all flow plus a keyword flow. See [DM Flows](https://info.bundle.social/api-reference/automations/how-flows-behave.md#dm-flows).

### "Why did my automation ignore someone's second message?"

The loop brake: in DMs, one automated answer per person per 60 seconds, 6 per hour. The skipped run is in the executions with `AUTOMATION_CONVERSATION_COOLDOWN`. Use quick replies or buttons for back-and-forth conversations, since taps skip this brake.

### "My TikTok flow sometimes fails on the reply or like step."

Most likely TikTok wasn't ready for the comment yet when the step ran. Set `actionDelaySeconds` to 5-10 on the flow and publish again. See [Delays](https://info.bundle.social/api-reference/automations/building-flows.md#delays).

### "Can one flow cover all my posts?"

No. A comment flow always points at one post. Create one per post, ideally when you schedule it.

### "Can I stop automations for one conversation when a human takes over?"

Not per conversation. Pausing a flow stops it for everyone. Build your flows around keywords and buttons so they only answer what they're meant to.

### "How do I reply to a comment by hand?"

With the [Comments API](https://info.bundle.social/api-reference/comments.md#replying-to-imported-comments), or with a [private reply](https://info.bundle.social/api-reference/direct-messages/private-replies.md) if you want to answer in DMs. See [Which Tool Do I Need?](https://info.bundle.social/api-reference/automations.md#which-tool-do-i-need).

### "Can I DM everyone who commented, not just reply?"

That's exactly what `SEND_PRIVATE_REPLY` is. One private reply per comment, text only, within 7 days of the comment. Those are Meta's rules, not ours.

### "Does it work on posts I didn't publish through bundle.social?"

Not for comment triggers right now. DM triggers work for any conversation.

### "Is there a visual flow builder?"

Yes, in the bundle.social dashboard, see [Try It In The Dashboard](#try-it-in-the-dashboard). It shows the API definition of the flow you're building, so you can build there and copy the JSON into your code.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
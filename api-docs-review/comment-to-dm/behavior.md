> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# How Flows Behave

> What happens in practice: comment and DM flow behavior, failures, and built-in safety limits.

Read this before you build. Most "why did my automation do that?" questions are answered here.

## Comment Flows

* **One flow = one post.** A comment trigger always points at one `postId`, and there's no "all my posts" flow. Create one flow per post. The easiest moment is right when you schedule the post: the flow can be published before the post goes live and is armed the moment it does.
* **Replies are comments too.** A reply inside a comment thread fires the trigger like any other comment. That includes people answering "thanks!" under your automated public reply. Without keywords, the flow answers those too, so use keywords.
* **Every comment gets its own answer.** On Instagram and Facebook there's no per-person cooldown for comment flows. If the same person comments "LINK" three times, they get three answers. Meta allows exactly one private reply per comment, so each comment gets at most one.
* **Hidden comments never trigger anything** (TikTok).
* **Your own comments never trigger anything.** Comments posted through bundle.social (including your flows' public replies) or by the account itself are ignored.
* **No comment import needed.** New comments arrive in real time. They trigger your flows, arrive as `comment.received` [webhooks](https://info.bundle.social/api-reference/automations/webhooks.md), and show up in `GET /api/v1/comment/import/comments` without you running an import.

## DM Flows

* **Every matching flow answers.** Flows have no priorities. If a catch-all flow (no keywords) and a keyword flow both match the same message, the person gets **two** replies. Either run one catch-all, or keep keywords from overlapping.
* **Conditions have no "else".** A `CONDITION` step either lets the run continue or stops it. For "if X do A, otherwise do B", build separate flows.
* **One automated answer per minute per person.** If someone sends two messages within 60 seconds, only the first one gets an automated answer, and nobody gets more than 6 an hour. Taps on quick replies and buttons skip this limit, so button-driven conversations can move fast. The replies they trigger still count toward the budget, though: a message someone *types* right after a tap-driven reply can go unanswered. The skipped runs show `AUTOMATION_CONVERSATION_COOLDOWN` or `AUTOMATION_CONVERSATION_HOURLY_LIMIT`.
* **Button taps only trigger `BUTTON_CLICKED` flows.** A quick reply tap that no `QUICK_REPLY_CLICKED` flow picks up falls through to your `DM_RECEIVED` flows like a typed message. A `POSTBACK` button, ice breaker or menu tap with no matching `BUTTON_CLICKED` flow gets no automated answer.
* **URL buttons don't trigger anything.** Platforms don't report when someone opens a link. Use a `POSTBACK` button if the tap should lead somewhere.
* **There's no per-conversation pause.** When someone from your team takes over a chat, your automations keep answering whatever their triggers match. Pausing a flow stops it for everyone. Archiving a conversation doesn't stop it either, since a new message reopens the conversation. If humans answer in the same inbox, build your flows around keywords and buttons rather than a catch-all.
* **Your team's messages never trigger flows.** Messages sent through bundle.social, or typed in the Instagram or Messenger app, are ignored.

## When Something Fails

* A failing step stops the run. Steps that already ran are not undone: a DM that went out stays sent.
* Failed runs are **not retried** automatically. Platform rate limits are the only exception: the run waits and continues where it stopped, without re-sending finished steps, for up to an hour. After that it fails with `AUTOMATION_EXECUTION_EXPIRED`.
* You can't re-run an old execution. Fix the flow and the next event will use it, or check it with a [test run](https://info.bundle.social/api-reference/automations/testing-and-logs.md#test-a-flow).
* If the account's [monthly message quota](https://info.bundle.social/api-reference/direct-messages.md#plans-and-limits) is used up, `SEND_MESSAGE` and `SEND_PRIVATE_REPLY` steps fail with `Monthly message limit reached`. Public replies and likes keep working. The same two steps also fail if messaging isn't enabled for the account, or while sending is paused on our side.
* A whole run can take at most 60 seconds (`AUTOMATION_EXECUTION_TIMEOUT`).
* Uploads in rich messages (a missing upload, wrong type, or a file over 24 MB) are checked when the step runs, not when you publish. Test the flow once before relying on it.

***

## Safety Limits

Automations answering other automations in a loop is how accounts get flagged. We have a few brakes built in so that doesn't happen to you:

* **Loop brake for DMs.** In Instagram and Facebook DMs, each person gets at most **1 automated reply per 60 seconds** and **6 per hour**, shared across all your flows. Messages that arrive while the brake is on get no automated answer. Button and quick reply taps skip this brake, since they're answers to your own messages, but the replies they trigger count toward the budget. A quick reply tap that no `QUICK_REPLY_CLICKED` flow picks up and that falls through to a `DM_RECEIVED` flow is treated like a typed message. The brake is checked per incoming message, so if several flows match the same message, they all answer it (see [How Flows Behave In Practice](https://info.bundle.social/api-reference/automations/how-flows-behave.md#dm-flows)).
* **Loop brake for TikTok comments.** The same budget applies per TikTok commenter, because TikTok hides bursts of similar replies as spam. Skipped runs show `AUTOMATION_COMMENTER_COOLDOWN` or `AUTOMATION_COMMENTER_HOURLY_LIMIT`. Instagram and Facebook **comment** flows have no per-person brake: every comment gets its answer.
* **No self-triggering.** Messages and comments sent by bundle.social, or by the account itself, never trigger your flows.
* **One team per page.** If the same Page or Instagram account is connected in several of your teams, only the first team's flow answers a comment. The rest are skipped with `AUTOMATION_SHARED_PAGE_CLAIMED`. The same applies to DMs: if another team answered that person in the last 60 seconds, your run is skipped with that code, taps included.
* **No double sends.** Each event runs each flow at most once, even if the platform delivers the same webhook twice.
* **At most 25 flows** react to a single event.
* **Rate limits are handled for you.** If a platform tells us to slow down, the run goes back to `QUEUED` and retries automatically for up to an hour.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
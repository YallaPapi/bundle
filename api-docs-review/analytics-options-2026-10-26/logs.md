> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Testing & Execution Logs

> Test a flow on a real conversation or comment, and read the log of every run.

Two tools for finding out what your flows do: a **test run** fires a flow on demand, and the **execution log** records every run, triggered or tested.

## Test A Flow

**Endpoint:** `POST /api/v1/automations/:id/test`

Runs the flow **once, synchronously**, and returns the finished execution. It uses the draft if there is one, otherwise the published version, so you can test changes before publishing them.

A test skips the trigger entirely: keywords, `payloads`, `senderExternalIds`, the delay and the loop brake are not applied. It goes straight to the steps (conditions still run). Use it to check what the steps do, and a real comment or DM to check what triggers them.

```json theme={null}
{
  "input": {
    "conversationId": "conv_abc",
    "text": "how much is the pro plan?"
  }
}
```

Give it the context the steps need:

* DM and click flows: `conversationId` of a real conversation in the team (plus `text` or `payload` if your conditions look at them),
* comment flows: `fetchedCommentId` of a real comment (from the [Comments API](https://info.bundle.social/api-reference/comments.md)),
* flows with `SENDER_ID` conditions: pass the sender's ID in `input` yourself, a test doesn't take it from the conversation.

> [!WARNING]
>
> **Tests are real.** Steps really send messages to the real person in that conversation, and the run counts toward your monthly quota. Test on a conversation with your own second account.

Before anything runs, a test returns:

* `400` if the flow has neither a draft nor a published version, or its definition doesn't pass validation (for example missing permissions),
* `404` if the flow, conversation or comment isn't found in the flow's team,
* `403` if the account's monthly run budget is used up,
* `429` if the platform is rate-limiting the account right now (try again shortly).

Once the steps run, the result comes back as `200` with the execution, even when it didn't go well: check its `status` and `error`. In the execution, `input.type` is `MANUAL_TEST`.

***

## Executions

Every run is logged as an **execution**. This is where you answer "why didn't my automation reply?". Logs are kept for [30 days](https://info.bundle.social/api-reference/data-retention.md) after the run.

**Endpoints:**

* `GET /api/v1/automations/:id/executions?teamId=team_123` - runs of one flow, newest first
* `GET /api/v1/automation-executions/:id` - one run, with every step

Filters for the list: `status`, `platform`, `socialAccountId`, `conversationId`, `fetchedCommentId`, `flowVersionId`, `triggerId`. Paginate with `limit` (max 500) and either `offset` or `cursor` (pass back `nextCursor`), same as [conversations](https://info.bundle.social/api-reference/direct-messages/conversations.md#pagination).

```json theme={null}
{
  "id": "exec_1",
  "teamId": "team_123",
  "flowId": "flow_abc",
  "flowVersionId": "ver_3",
  "triggerId": "trg_1",
  "platform": "INSTAGRAM",
  "socialAccountId": "sa_789",
  "fetchedCommentId": "fetched_1",
  "conversationId": null,
  "conversationMessageId": null,
  "senderExternalId": "1789000000000000",
  "currentStepId": "public-reply-2",
  "status": "COMPLETED",
  "input": {
    "type": "COMMENT_CREATED",
    "platform": "INSTAGRAM",
    "postId": "post_123",
    "text": "LINK please!"
  },
  "output": { "completedAtStepId": "public-reply-2" },
  "error": null,
  "startedAt": "2026-09-26T09:30:01.000Z",
  "completedAt": "2026-09-26T09:30:02.400Z",
  "createdAt": "2026-09-26T09:30:00.500Z",
  "updatedAt": "2026-09-26T09:30:02.400Z",
  "steps": [
    {
      "id": "stepexec_1",
      "stepId": "private-reply-1",
      "status": "COMPLETED",
      "attemptCount": 1,
      "output": { "conversationId": "conv_abc", "messageId": "msg_42" },
      "error": null,
      "startedAt": "2026-09-26T09:30:01.100Z",
      "completedAt": "2026-09-26T09:30:01.900Z"
    },
    {
      "id": "stepexec_2",
      "stepId": "public-reply-2",
      "status": "COMPLETED",
      "attemptCount": 1,
      "error": null,
      "startedAt": "2026-09-26T09:30:01.950Z",
      "completedAt": "2026-09-26T09:30:02.400Z"
    }
  ]
}
```

The execution also carries the related `flow`, `flowVersion`, `conversation`, `conversationMessage`, `fetchedComment` and `socialAccount` objects, so you rarely need a second request.

### Execution Status

| Status | Meaning |
| :- | :- |
| `QUEUED` | Waiting to run (delay, or a platform rate limit) |
| `RUNNING` | Steps are running |
| `COMPLETED` | All steps done |
| `SKIPPED` | Stopped on purpose. A condition didn't match (then `error` is empty and `output.skippedAtStepId` names the condition), or a limit kicked in (then `error.code` says which). |
| `FAILED` | A step failed. The failing step has the details in its `error`. |
| `CANCELED` | The flow was paused, archived or deleted while the run was still waiting |

Each step has its own status: `PENDING`, `RUNNING`, `COMPLETED`, `FAILED` or `SKIPPED`.

### Error Codes Worth Knowing

| `error.code` | Status | Meaning |
| :- | :- | :- |
| `AUTOMATION_MONTHLY_LIMIT_REACHED` | `SKIPPED` | Monthly run budget for this account is used up |
| `AUTOMATION_CONVERSATION_COOLDOWN` | `SKIPPED` | DMs: this person got an automated reply less than 60 seconds ago |
| `AUTOMATION_CONVERSATION_HOURLY_LIMIT` | `SKIPPED` | DMs: this person already got 6 automated replies in the last hour |
| `AUTOMATION_COMMENTER_COOLDOWN` | `SKIPPED` | TikTok comments: this commenter got an automated reply less than 60 seconds ago |
| `AUTOMATION_COMMENTER_HOURLY_LIMIT` | `SKIPPED` | TikTok comments: this commenter already got 6 automated replies in the last hour |
| `AUTOMATION_SHARED_PAGE_CLAIMED` | `SKIPPED` | Another team with the same page connected already answered this comment or conversation |
| `AUTOMATION_EXECUTION_DISABLED` | `SKIPPED` | Automations were briefly paused on our side (for example during a platform incident). Mostly seen on test runs: events that arrive during a pause don't create runs at all. |
| `AUTOMATIONS_DISABLED` | `SKIPPED` | Automations were switched off for your organization before the run started |
| `AUTOMATION_EXECUTION_EXPIRED` | `FAILED` | The run couldn't finish within an hour of its scheduled time (usually a long platform rate limit) |
| `AUTOMATION_EXECUTION_TIMEOUT` | `FAILED` | The run took longer than 60 seconds |
| `AUTOMATION_EXECUTION_STALE` | `FAILED` | The run was interrupted and didn't finish. Check which steps completed before acting on it. |

Failed steps carry a readable `message`. Some come from the platform (for example, Meta rejecting a message), others from our own checks before sending (for example, a Facebook private reply to a comment older than 7 days, messaging not enabled for the account, or the monthly message limit).


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
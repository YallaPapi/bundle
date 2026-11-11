> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Managing Flows

> Create, edit, publish, pause, archive, delete and copy automation flows.

Everything you do with a flow after writing its [definition](https://info.bundle.social/api-reference/automations/building-flows.md): create it, save changes, publish, pause, retire, copy.

## Lifecycle

Flows are versioned, so you can edit safely while the old version keeps running.

1. **Create** with `POST /api/v1/automations`. The flow starts as a `DRAFT` and never runs.
2. **Save changes** with `PATCH /api/v1/automations/:id` and a `definition`. This saves a **draft**. If the flow is already live, the live version keeps running untouched.
3. **Publish** with `POST /api/v1/automations/:id/publish`. We validate the draft, make it the live version and set the flow to `ACTIVE`.

**Nothing you edit goes live until you publish it.**

> [!TIP]
>
> **Recommended rhythm: `PATCH` the definition, then publish with an empty body.** Publish also accepts a `definition` in its body, but that skips the draft. [Test runs](https://info.bundle.social/api-reference/automations/testing-and-logs.md#test-a-flow) always use the saved draft when there is one, so publishing a definition that was never saved as a draft leaves your tests running an older version.

| Flow status | Meaning | How you get there |
| :- | :- | :- |
| `DRAFT` | Never published. Doesn't run. | Create |
| `ACTIVE` | Live. Runs on every matching event. | Publish, or activate a paused flow |
| `PAUSED` | Temporarily off. Keeps its configuration. | Pause |
| `ARCHIVED` | Retired. Doesn't run until you activate or publish it again. | Archive |

## The Flow Object

Every flow endpoint except `DELETE` returns the flow with its current versions:

```json theme={null}
{
  "id": "flow_abc",
  "teamId": "team_123",
  "name": "Reel drop - comment LINK to get the link",
  "status": "ACTIVE",
  "platformScope": "INSTAGRAM",
  "createdAt": "2026-09-20T10:00:00.000Z",
  "updatedAt": "2026-09-26T09:00:00.000Z",
  "publishedVersion": {
    "id": "ver_3",
    "version": 3,
    "status": "PUBLISHED",
    "publishedAt": "2026-09-26T09:00:00.000Z",
    "definition": { "trigger": { "...": "..." }, "steps": [] }
  },
  "draftVersion": {
    "id": "ver_1",
    "version": 1,
    "status": "DRAFT",
    "definition": { "trigger": { "...": "..." }, "steps": [] }
  }
}
```

* `publishedVersion` is what runs. It's missing until the first publish.
* `draftVersion` is your latest saved draft. It **stays** after publishing, so right after a publish both usually carry the same definition. The next `PATCH` overwrites the draft in place, so the draft keeps its `version` number while each publish creates a new, higher one.
* Every run in the [execution logs](https://info.bundle.social/api-reference/automations/testing-and-logs.md#executions) records the `flowVersionId` it used, so you can tell which version answered.

## List Flows

**Endpoint:** `GET /api/v1/automations?teamId=team_123`

Optional filters: `status`, `platformScope`, `socialAccountId` (matches flows whose **published** version listens on that account, so drafts don't show up here), plus `offset` and `limit` (default 10). Returns `{ items, total }`, newest first. Archived flows are included, filter with `status` if you don't want them.

**Endpoint:** `GET /api/v1/automations/:id` returns a single flow.

## Create, Edit, Publish

`platformScope` is the flow's platform label: `INSTAGRAM`, `FACEBOOK`, `TIKTOK`, or `BOTH` (Instagram or Facebook). It has to fit the trigger's `platform`. A flow has exactly one trigger, so it listens on one account. Want the same automation on Instagram and Facebook? Create two flows. The flow `name` can be up to 120 characters.

```ts theme={null}
const API = "https://api.bundle.social/api/v1";
const headers = {
  "Content-Type": "application/json",
  "x-api-key": process.env.BUNDLE_API_KEY,
};

// 1. Create (you can pass the definition right away, or add it later with PATCH)
const flow = await fetch(`${API}/automations`, {
  method: "POST",
  headers,
  body: JSON.stringify({
    teamId: "team_123",
    name: "Reel drop - comment LINK to get the link",
    platformScope: "INSTAGRAM",
    definition: {
      trigger: {
        type: "COMMENT_CREATED",
        platform: "INSTAGRAM",
        socialAccountId: "sa_789",
        postId: "post_123",
        keywords: ["link"],
      },
      steps: [
        { type: "SEND_PRIVATE_REPLY", message: { text: "Here's the link 🔗 https://yourshop.com/drop" } },
        { type: "SEND_PUBLIC_COMMENT_REPLY", text: "Check your DMs 👀" },
      ],
    },
  }),
}).then((r) => r.json());

// 2. Publish - validates everything and makes it live
const res = await fetch(`${API}/automations/${flow.id}/publish`, {
  method: "POST",
  headers,
  body: JSON.stringify({}),
});

if (!res.ok) {
  // 400: schema problems come in `issues`, the rest in `message` separated by "; "
  const err = await res.json();
  console.error(err.issues ?? err.message);
}

// 3. Later: change the reply text, then publish again
await fetch(`${API}/automations/${flow.id}`, {
  method: "PATCH",
  headers,
  body: JSON.stringify({ definition: { /* full definition with your changes */ } }),
});
await fetch(`${API}/automations/${flow.id}/publish`, { method: "POST", headers, body: JSON.stringify({}) });
```

`PATCH` accepts `name`, `platformScope` and `definition`, all optional. A `definition` always replaces the whole draft, so send the full trigger and all steps, not just the part you changed.

Validation runs on create and on every `PATCH` that carries a `definition`, and again on publish. It happens in two stages:

* **Shape** (field types, lengths, counts, duplicate step ids): a `400` with an `issues` array, one entry per problem with its `path`.
* **Everything else** (accounts, permissions, the post, whether steps fit the trigger), once the shape is valid: all problems come back in one `400` whose `message` joins them with `; `, so you can fix them in one go.

A TikTok comment flow is also rejected while comment import is off for your organization. Publishing a flow that has no draft and no `definition` in the body returns `400`.

## Pause, Activate, Archive, Delete

| Endpoint | What happens |
| :- | :- |
| `POST /api/v1/automations/:id/pause` | The flow stops reacting to new events. Runs still waiting on a [delay](https://info.bundle.social/api-reference/automations/building-flows.md#delays) are canceled. |
| `POST /api/v1/automations/:id/activate` | A paused (or archived) flow goes live again with its published version. Returns `400` if the flow was never published. |
| `POST /api/v1/automations/:id/archive` | Retired. Stops running, waiting runs are canceled. Still listed and readable, and it comes back if you activate or publish it again. |
| `DELETE /api/v1/automations/:id` | Gone. Waiting runs are canceled and the flow answers `404` from now on. Past runs stay readable by their ID via `GET /api/v1/automation-executions/:id` until they're [30 days old](https://info.bundle.social/api-reference/data-retention.md). |

None of these take a body.

## Copy Flows Between Teams

**Endpoint:** `POST /api/v1/automations/copy`

```json theme={null}
{ "sourceTeamId": "team_123", "targetTeamId": "team_456", "flowId": "flow_abc" }
```

Leave out `flowId` to copy every flow of the source team (archived ones included). Copies land as **drafts** in the target team, with the account-specific bits cleared (`socialAccountId`, `postId`, `senderExternalIds`). Point them at the new team's accounts with `PATCH`, then publish. Perfect for agencies rolling out the same automations to many clients.

Create and copy answer `201`. Copy returns `{ items, total }` with the new flows. Source and target team must be different.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
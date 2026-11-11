> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Setup

> Reconnect Facebook and Instagram accounts with messaging permissions and subscribe them to DMs.

Once your organization is on the allowlist, do this for **every** Facebook and Instagram account that should receive DMs:

1. **Reconnect it with messaging permissions.** This includes accounts that were already connected before we switched the feature on. They don't have the permissions yet.
2. **Subscribe it to messages** with `messaging/enable`. This registers the account for Meta's message webhooks. Without it, no DM ever reaches us.
3. **Make sure your webhook endpoint accepts the new events** (see [Webhooks](/api-reference/direct-messages/webhooks)).

## Step 1: Connect With Messaging Permissions

Add `withMessagingScope: true` when you generate the connect link. It works on both the hosted portal and the custom connect flow.

```ts theme={null}
const res = await fetch("https://api.bundle.social/api/v1/social-account/connect", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "x-api-key": process.env.BUNDLE_API_KEY,
  },
  body: JSON.stringify({
    teamId: "team_123",
    type: "INSTAGRAM",
    redirectUrl: "https://yourapp.com/connected",
    withMessagingScope: true,
  }),
});

const { url } = await res.json(); // send your user here
```

For the hosted portal, pass the same `withMessagingScope: true` to `POST /api/v1/social-account/create-portal-link`.

<Warning>
  **Accounts connected before the feature was enabled must be reconnected.** That includes accounts connected with `withMessagingScope: true`, because the flag is ignored until your organization is on the allowlist. Meta only grants messaging permissions on its login screen, so there is no way to add them silently afterwards. The same reconnect also subscribes the account to new comments, which [comment automations](/api-reference/automations) need.
</Warning>

## Step 2: Subscribe The Account To Messages

Connecting an account never subscribes it to DMs by itself. `messaging/enable` registers the account for Meta's message webhooks and starts processing its DMs. You opt in per account, so a customer who only wants scheduling never has their DMs processed.

**Endpoint:** `POST /api/v1/social-account/messaging/enable`

```bash theme={null}
curl -X POST "https://api.bundle.social/api/v1/social-account/messaging/enable" \
  -H "x-api-key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "teamId": "team_123", "type": "INSTAGRAM" }'
```

```json theme={null}
{
  "socialAccountId": "sa_789",
  "type": "INSTAGRAM",
  "messagingStatus": "ENABLED",
  "messagingLastError": null
}
```

The call is idempotent, so calling it twice is harmless.

| Response | Meaning |
| :- | :- |
| `200` | Subscribed, messaging is `ENABLED`. New DMs will start showing up. |
| `400` | The account is missing the messaging permissions (reconnect it with `withMessagingScope: true`), the team has no account of that type, or no page or account was selected for the connection. The `message` says which. |
| `404` | Your organization is not on the allowlist yet. |
| `502` | Meta refused the subscription. The account keeps its previous status (normally `DISABLED`); retry in a bit. |

## Turning It Off

**Endpoint:** `POST /api/v1/social-account/messaging/disable` (same body)

We stop processing DMs for that account immediately. Existing conversations stay readable, but sending, reactions and private replies return `403` until you enable it again. If Meta doesn't confirm the change right away, the status becomes `DISABLE_PENDING` and the call returns `502`, so you can safely retry it.

<Info>
  We only collect messages that arrive **after** messaging is enabled. Older DM history from before that moment is not imported, and each message we collect is kept for [30 days](/api-reference/data-retention).
</Info>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
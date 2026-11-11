> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Webhooks

> We call you when things happen, so you don't have to poll. Real-time post and comment events with signature verification, retries, and auto-disable.

Webhooks are how you know if a post actually went live or failed permanently. Instead of polling every few seconds, give us a URL and we'll notify you.

<Note>
  **Prerequisite:** You need an API Key and a URL where we can send POST requests. Webhooks are configured at the **organization** level - all teams under that org share the same webhook endpoints.
</Note>

## Setup

1. Go to the [Webhooks Dashboard](https://bundle.social/dashboard/organization/webhooks).
2. Add your URL (e.g., `https://api.yourapp.com/webhooks/bundle`). Must be **HTTPS**.
3. Get your **Signing Secret**.

<Tip>
  **Local Dev:** Use `ngrok` to test locally. `ngrok http 3000`.
</Tip>

***

## Events

| Event | When it fires |
| :- | :- |
| `post.published` | Post finished processing. Check `data.status`: `POSTED` means live, `ERROR` means it failed permanently. |
| `comment.published` | Comment finished processing. Check `data.status`: `POSTED` means published, `ERROR` means it failed permanently. |
| `social-account.created` | User connected a new social account |
| `social-account.updated` | Social account changed (channel unset, remote disconnection detected) |
| `social-account.deleted` | Social account was disconnected or removed |
| `team.created` | A new team was created |
| `team.updated` | Team details changed (name, avatar, social accounts added/removed) |
| `team.deleted` | A team was deleted |

<Note>
  `team.updated` also fires when a social account is added to or removed from a team - so you don't need to listen to social account events separately if you're already tracking teams.
</Note>

***

## Payload Structure

Every webhook delivery is an HTTP POST with this shape:

```json theme={null}
{
  "type": "post.published",
  "data": {
    // ... event-specific payload
  }
}
```

### Headers We Send

| Header | Value |
| :- | :- |
| `Content-Type` | `application/json` |
| `User-Agent` | `bundlesocial` |
| `x-signature` | HMAC-SHA256 signature (see [Security](#security-verify-its-us)) |

### Post Events Payload

When you receive `post.published`, the `data` field contains the full post object. Use `data.status` to distinguish success from failure.

```json theme={null}
{
  "type": "post.published",
  "data": {
    "id": "post_abc123",
    "title": "My awesome post",
    "status": "POSTED",
    "postDate": "2026-01-15T10:00:00.000Z",
    "postedDate": "2026-01-15T10:00:02.341Z",
    "teamId": "team_xyz",
    "organizationId": "org_123",
    "data": {
      "INSTAGRAM": {
        "type": "POST",
        "text": "Hello world!",
        "uploadIds": ["upload_456"]
      }
    },
    "error": null,
    "errors": null,
    "errorsVerbose": null,
    "externalData": {
      "INSTAGRAM": {
        "id": "17900000000000000",
        "permalink": "https://www.instagram.com/p/example/"
      }
    },
    "retryCount": 0,
    "createdAt": "2026-01-14T15:30:00.000Z",
    "updatedAt": "2026-01-15T10:00:02.341Z",
    "deletedAt": null,
    "uploads": [
      {
        "upload": {
          "id": "upload_456",
          "fileName": "cover.jpg",
          "mimeType": "image/jpeg",
          "size": 245000
        }
      }
    ],
    "socialAccounts": [
      {
        "socialAccount": {
          "id": "sa_789",
          "type": "INSTAGRAM",
          "username": "mybrand",
          "displayName": "My Brand"
        }
      }
    ]
  }
}
```

For failed posts, the event type is still `post.published`, but `data.status` is `ERROR` and `data.error`, `data.errors`, or `data.errorsVerbose` contains the failure details.

A `POSTED` post can still carry a non-fatal warning in `data.errors`, for example when YouTube rejected the custom thumbnail but the video itself was published. Check `data.status`, not just whether `errors` is empty.

### Comment Events Payload

```json theme={null}
{
  "type": "comment.published",
  "data": {
    "id": "comment_abc",
    "status": "POSTED",
    "internalPostId": "post_abc123",
    "teamId": "team_xyz",
    "data": {
      "INSTAGRAM": {
        "text": "#growth #mindset"
      }
    },
    "error": null,
    "createdAt": "2026-01-15T10:00:05.000Z",
    "socialAccounts": [
      {
        "socialAccount": {
          "id": "sa_789",
          "type": "INSTAGRAM",
          "username": "mybrand"
        }
      }
    ]
  }
}
```

For failed comments, the event type is still `comment.published`, but `data.status` is `ERROR`.

### Social Account Events Payload

```json theme={null}
{
  "type": "social-account.created",
  "data": {
    "id": "sa_789",
    "type": "INSTAGRAM",
    "teamId": "team_xyz",
    "username": "mybrand",
    "displayName": "My Brand",
    "avatarUrl": "https://...",
    "externalId": "17841400000",
    "channels": [],
    "createdAt": "2026-01-10T12:00:00.000Z"
  }
}
```

Sensitive fields like `accessToken`, `refreshToken`, `secret`, and `expiresAt` are **never** included in webhook payloads. We're not that reckless.

### Team Events Payload

```json theme={null}
{
  "type": "team.created",
  "data": {
    "id": "team_xyz",
    "name": "Marketing Team",
    "avatarUrl": "https://...",
    "organizationId": "org_123",
    "createdById": "user_456",
    "createdAt": "2026-01-10T12:00:00.000Z",
    "organization": { "id": "org_123", "name": "Acme Corp" },
    "createdBy": { "id": "user_456", "email": "..." },
    "socialAccounts": []
  }
}
```

***

## Delivery & Retries

We really try to deliver your webhooks. Here's how hard we try:

| Setting | Value |
| :- | :- |
| Timeout | 15 seconds per request |
| Max attempts | 3 (initial + 2 retries) |
| Backoff | Exponential, starting at 30 seconds |
| Concurrency | We process up to 50 deliveries simultaneously |

So if your server is down, we'll try 3 times with increasing delays. After that, the event is marked as failed and we move on. We're persistent, not obsessive.

### Auto-Disable (The Safety Net)

If your webhook endpoint goes **7 days without a single successful delivery**, we automatically disable it. This protects both of us - we stop wasting resources, and you stop missing events you don't know about.

When this happens:

* Your webhook is marked as **disabled** and we stop sending events to that URL
* We send an **email to the organization owner** and create an **in-app notification** in the dashboard, both linking to the webhooks page
* You can re-enable it from the dashboard or API, which resets the 7-day window (so a single failure right after re-enabling won't immediately disable it again)
* On the next successful delivery, the failure counter resets to 0

<Warning>
  **Don't let your endpoint stay broken for too long.** If your server is having a bad week, re-enable manually once it's back. Events that happened while disabled are gone - we don't replay them.
</Warning>

### Resending Events

Made a mistake in your handler? Event got lost? You can resend any webhook event from the dashboard or via the API. We'll create a fresh delivery attempt with the same payload.

***

## Remote Disconnection Detection

We check every connected social account every **6 hours** to see if it's still valid. If the platform tells us "nope, this token is dead," we start the disconnection flow.

### How It Works

1. Every 6 hours, we validate each connected account against its platform.
2. If the check fails, we retry **3 times** with 10-minute backoff.
3. If all retries fail, we schedule the account for deletion and send you a `social-account.updated` webhook.
4. After the grace period, we remove the account (fires `social-account.deleted`).

Automatic remote disconnection scanning currently covers Meta accounts: Facebook, Instagram, and Threads. For other platforms, use `POST /api/v1/social-account/connection-check` when your user opens account settings or before showing a reconnect warning.

### The `social-account.updated` Payload

When we detect a disconnection, the webhook includes a `socialAction` object with the details:

```json theme={null}
{
  "type": "social-account.updated",
  "data": {
    "id": "sa_789",
    "type": "INSTAGRAM",
    "teamId": "team_xyz",
    "username": "mybrand",
    "socialAction": {
      "type": "disconnect-check",
      "source": "system",
      "checkedAt": "2026-02-20T14:30:00.000Z",
      "details": {
        "status": "error",
        "code": "REMOTE_DISCONNECT_DELETION_SCHEDULED",
        "message": "Account failed validation after 3 attempts",
        "attemptNumber": 3,
        "attemptsTotal": 3,
        "scheduledForDeletion": true,
        "deleteAccountAfter": 6,
        "deleteOn": "2026-02-20T20:30:00.000Z"
      }
    }
  }
}
```

### Status Codes

| Code | Meaning |
| :- | :- |
| `REMOTE_DISCONNECT_DELETION_SCHEDULED` | All retries failed. Account is scheduled for deletion. |
| `REMOTE_DISCONNECT_UNAUTHORIZED_WARNING` | Token refresh failed with an auth error (401, expired token, etc.). |
| `REMOTE_DISCONNECT_REAUTH_REQUIRED` | Connection failed for another reason. User should reconnect. |

### The `deleteOn` Grace Period

When an account is scheduled for deletion, `deleteOn` tells you exactly when it will be removed. The delay is controlled by `deleteAccountAfter` on your organization settings (0-24 hours).

* **Default: 0 hours** - account is removed almost immediately.
* **If you set it to e.g. 6 hours** - you get a 6-hour window to notify your user before the account is gone.

**Why does this matter?** When an account is deleted:

* It's removed from all draft and scheduled posts.
* Posts that only had this account become drafts.
* If the user reconnects before `deleteOn`, the account stays.

<Important>
  **Set `deleteAccountAfter` to something greater than 0** if you want time to notify your users. With the default (0), the account disappears on the next cleanup run - which is every minute. That's fast. Maybe too fast if you want to show a "hey, reconnect your Instagram" banner first.
</Important>

***

## Best Practices

1. **Respond fast.** Return a `200` within 15 seconds. Do heavy processing asynchronously. If you take too long, we'll count it as a failure.
2. **Be idempotent.** We might deliver the same event twice in rare cases (retries, race conditions). Deduplicate with the event `type`, `data.id`, `data.status`, and relevant timestamps.
3. **Verify signatures.** Always. No exceptions. Even in development. See the [SDK](/api-reference/sdk) for built-in signature verification, or check the [Swagger](/api-reference/openapi) for the raw details.
4. **Use HTTPS.** We only send webhooks to HTTPS URLs. Sorry, `http://localhost` works via ngrok though.
5. **Monitor your failures.** If your endpoint has been failing for days with no successful deliveries, fix it before the 7-day auto-disable kicks in. You'll get an email + dashboard notification when it does, but catching it sooner is better.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
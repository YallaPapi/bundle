> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Health

> Check API and platform health before sending users into broken flows. GET /api/v1 returns live per-platform status so you can disable what is down.

`GET /api/v1/` returns the current API health object. It now includes `platforms`, where every supported platform has a current `status` and an internal `note`.

Use this endpoint to decide whether parts of your app should stay active, be disabled, or show a message before a user starts a flow that may fail.

<Warning>
  Do not display `note` directly to end users. Treat it as technical context for your product logic, support team, or internal dashboards.
</Warning>

## Endpoint

**Endpoint:** `GET /api/v1/`

```json theme={null}
{
  "status": "ok",
  "createdAt": "2026-04-27T10:00:00.000Z",
  "note": "",
  "platforms": {
    "FACEBOOK": {
      "status": "operational",
      "note": ""
    },
    "INSTAGRAM": {
      "status": "degraded",
      "note": "Instagram publishing is slower than usual"
    },
    "TIKTOK": {
      "status": "maintenance",
      "note": "TikTok OAuth is temporarily paused"
    },
    "YOUTUBE": {
      "status": "operational",
      "note": ""
    },
    "SNAPCHAT": {
      "status": "operational",
      "note": ""
    },
    "TWITTER": {
      "status": "operational",
      "note": ""
    },
    "PINTEREST": {
      "status": "operational",
      "note": ""
    },
    "REDDIT": {
      "status": "operational",
      "note": ""
    },
    "MASTODON": {
      "status": "operational",
      "note": ""
    },
    "DISCORD": {
      "status": "operational",
      "note": ""
    },
    "SLACK": {
      "status": "operational",
      "note": ""
    },
    "BLUESKY": {
      "status": "operational",
      "note": ""
    },
    "GOOGLE_BUSINESS": {
      "status": "outage",
      "note": "Google Business API is rejecting requests"
    },
    "LINKEDIN": {
      "status": "operational",
      "note": ""
    },
    "THREADS": {
      "status": "operational",
      "note": ""
    }
  }
}
```

## Platform Statuses

| Status | Meaning | Recommended behavior |
| :- | :- | :- |
| `operational` | Platform is working normally. | Keep features enabled. |
| `degraded` | Platform is partially working or slower than usual. | Keep features available, but show a soft warning if the flow is user-visible. |
| `maintenance` | Platform is intentionally paused or limited. | Disable the affected flow and let users try again later. |
| `outage` | Platform is currently unavailable. | Disable actions that depend on this platform and avoid sending doomed requests. |

## Recommended Polling

Poll this endpoint every **20 minutes** from your backend or app shell. That is frequent enough to react to platform incidents without turning a health endpoint into unnecessary traffic.

Avoid polling it before every single post, upload, or OAuth click. Cache the latest result and use it to guide your UI.

## Example Usage

```typescript theme={null}
type PlatformHealthStatus = "operational" | "degraded" | "outage" | "maintenance";

const shouldDisablePlatformFeature = (status: PlatformHealthStatus) =>
  status === "outage" || status === "maintenance";

const shouldShowWarning = (status: PlatformHealthStatus) =>
  status === "degraded";
```

For example, if `GOOGLE_BUSINESS.status` is `outage`, disable Google Business posting and review import buttons. If `INSTAGRAM.status` is `degraded`, you may keep publishing enabled but show a short message like "Instagram is slower than usual right now."

<Tip>
  Use your own user-facing copy. The `note` field is useful context, but it may contain operational wording that is not polished for your customers.
</Tip>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
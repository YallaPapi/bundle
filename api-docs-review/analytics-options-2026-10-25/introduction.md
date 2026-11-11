> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Introduction

> Get started with the bundle.social API. API key auth via x-api-key, the base URL, how organizations and teams fit together, and where rate limits bite.

## Authentication

We use API Key authentication. Simple, secure, boring.

> [!NOTE]
>
> **Don't have an API Key?**\
> [Sign up here](https://bundle.social) and grab one from the **API Keys** section in your dashboard.

### The Header

To make a request, add the `x-api-key` header with your key.

```json theme={null}
{
  "x-api-key": "pk_live_..."
}
```

### Authorization Scheme

All endpoints are protected. If you don't send the key, you get a `401 Unauthorized`. If you send a bad key, you get a `403 Forbidden`.

```json theme={null}
"security": [
  { 
    "ApiKeyAuth": [] 
  }
]
```

## Base URL

```bash theme={null}
https://api.bundle.social
```

Everything is prefixed with `/api/v1`, but check the specific endpoint reference to be sure.

***

## Organizations vs Teams

This is important. Almost every API call involves a `teamId`, so you need to understand the hierarchy:

```
Organization (your account)
  ├── Team A (e.g. "Marketing")
  │   ├── Social Accounts (Instagram, TikTok, ...)
  │   ├── Posts
  │   └── Uploads
  ├── Team B (e.g. "Client: Acme Corp")
  │   ├── Social Accounts
  │   ├── Posts
  │   └── Uploads
  ├── API Keys (shared across all teams)
  ├── Webhooks (shared across all teams)
  └── Subscription & Billing
```

### What lives where

| Level | What belongs here |
| :- | :- |
| **Organization** | API keys, webhooks, subscription/billing, compression settings |
| **Team** | Social accounts, posts, uploads, bots, invitations, bio/link-in-bio |

### Why this matters for you

* **`teamId` is required** on most endpoints (creating posts, uploading media, connecting accounts). Think of a team as a "workspace" or "project" - it groups related social accounts together.
* **API keys are org-level.** One key gives you access to all teams in the organization.
* **Webhooks are org-level.** You get events for all teams from a single webhook endpoint.
* **Rate limits are per team.** Each team has its own daily posting quota. Five teams means five independent limits. See [Rate Limits](https://info.bundle.social/api-reference/rate-limits.md).
* **Monthly post caps are org-level.** The total monthly posts across all teams are capped by your subscription tier.

> [!TIP]
>
> If you're building a SaaS where each of your customers needs their own social accounts, create a **team per customer**. They won't step on each other's toes.

### Finding your team IDs

List your teams with the paginated `GET /api/v1/team`:

```http theme={null}
GET /api/v1/team?offset=0&limit=50
```

It returns `{ items, total }`, so it works the same whether you have 3 teams or 30,000. Add `search` to filter by name.

> [!WARNING]
>
> `GET /api/v1/organization` still returns a `teams` array, but it's **deprecated and will be removed on November 15, 2026**. It isn't paginated, so it gets slow for organizations with many teams. Use `GET /api/v1/team` instead. The rest of the organization response (ID, plan, settings) stays.

***

## Rate Limits

We have sensible rate limits to protect the system. If you hit them, you'll get a `429 Too Many Requests`.

Check the [Rate Limits](https://info.bundle.social/api-reference/rate-limits.md) page for the full breakdown - including burst protection, per-minute caps, and daily posting limits per platform.

***

## Other ways to use the API

You don't have to call the REST endpoints directly:

> **[SDK](https://info.bundle.social/api-reference/sdk.md)**
>
> Typed TypeScript SDK, generated from OpenAPI.

> **[CLI](https://info.bundle.social/api-reference/cli.md)**
>
> `bundlesocial-cli` - JSON in, JSON out. For shells, CI, cron and AI agents.

> **[MCP server](https://info.bundle.social/api-reference/mcp.md)**
>
> `bundlesocial-mcp` - for Claude Desktop / Claude Code / Cursor and other MCP clients.

The per-platform fields you put in a post's `data` are documented in [Platform parameters](https://info.bundle.social/api-reference/platform-parameters.md).


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
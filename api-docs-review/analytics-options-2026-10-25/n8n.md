> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# n8n

> Schedule posts, handle comments, DMs and analytics from n8n workflows.

`n8n-nodes-bundlesocial` is an [n8n](https://n8n.io) community node for the bundle.social API. One **bundle.social** node covers every public operation - posts, uploads, comments, DMs, automations, analytics, teams and the platform-specific helpers - across 15 platforms. It is generated from the [OpenAPI spec](https://info.bundle.social/api-reference/openapi.md) and regenerated daily, so new API operations reach the node shortly after they ship.

> **[npm: n8n-nodes-bundlesocial](https://www.npmjs.com/package/n8n-nodes-bundlesocial)**
>
> Install from **Settings > Community Nodes**

> **[Source](https://github.com/bundleglobal/bundlesocial-n8n)**
>
> `bundleglobal/bundlesocial-n8n`

## Install

In n8n open **Settings > Community Nodes > Install**, enter `n8n-nodes-bundlesocial` and confirm. See the [n8n guide](https://docs.n8n.io/integrations/community-nodes/installation/) for other install methods.

## Credentials

1. Create an API key in the [dashboard](https://bundle.social/dashboard/organization/api-keys).
2. In n8n, create a **bundle.social API** credential and paste the key into **API Key**.

Leave **Base URL** at `https://api.bundle.social`.

## Usage

Pick a **Resource** (for example *Post*), then an **Operation** (for example *Create*).

* **Team** and **Social Account** fields are dropdowns loaded from your organization; an expression with an ID works too.
* **Post > Create** shows one settings section per platform selected in **Social Account Types** (*TikTok Settings*, *Instagram Settings*, ...). The fields match [Platform parameters](https://info.bundle.social/api-reference/platform-parameters.md).
* Media goes in two steps: upload it with **Upload > Upload File** (binary input) or **Upload > Create From URL**, then pass the returned `id` in the post's **Upload IDs**. Files above 90 MB go through **Upload > Upload Large File** (up to 5 GB).
* Every operation with a request body has **Specify Body > Using JSON** for sending the raw body, for example an automation flow built by an earlier node.
* List operations support **Return All** and page through the API for you.
* Dates picked in the UI are read in the workflow timezone; ISO 8601 strings with an offset are sent as-is.
* Validation errors list each invalid field, for example `data.TIKTOK.text: Required`.

### Example: schedule a post with an image

1. **HTTP Request** (or any node) that outputs the image as binary data.
2. **bundle.social > Upload > Upload File**, Input Binary Field `data`.
3. **bundle.social > Post > Create**:
   * Team: your team
   * Social Account Types: `Instagram`, `LinkedIn`
   * Post Date: `{{ $now.plus(1, 'hour').toISO() }}`
   * Status: `Scheduled`
   * Instagram Settings > Text: your caption, Upload IDs: `{{ $('Upload File').item.json.id }}`
   * LinkedIn Settings > Text: your caption, Upload IDs: `{{ $('Upload File').item.json.id }}`

## AI Agent tool

The node can be attached to an n8n **AI Agent** as a tool. On self-hosted n8n set `N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE=true` to allow community nodes as tools.

Also see: [SDK](https://info.bundle.social/api-reference/sdk.md) · [CLI](https://info.bundle.social/api-reference/cli.md) · [MCP Server](https://info.bundle.social/api-reference/mcp.md) · [Webhooks](https://info.bundle.social/api-reference/webhooks.md).


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
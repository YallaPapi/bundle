> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# MCP Server

> Drive bundle.social from Claude, Cursor and other Model Context Protocol clients.

`bundlesocial-mcp` is a [Model Context Protocol](https://modelcontextprotocol.io) server that exposes the bundle.social operations as MCP tools - so Claude Desktop, Claude Code, Cursor and any other MCP client can post, schedule, import, analyze content and manage connected accounts across 14+ platforms.

It ships as a **local stdio server** (`npx bundlesocial-mcp`). A hosted remote server at `mcp.bundle.social` is on the roadmap.

<CardGroup cols={2}>
  <Card title="npm: bundlesocial-mcp" icon="npm" href="https://www.npmjs.com/package/bundlesocial-mcp">
    `npx bundlesocial-mcp`
  </Card>

  <Card title="MCP Inspector" icon="magnifying-glass" href="https://github.com/modelcontextprotocol/inspector">
    `npx @modelcontextprotocol/inspector npx bundlesocial-mcp`
  </Card>
</CardGroup>

## Tools

The server covers the whole bundle.social API (the platform-specific edit/delete-after-publish helpers are reached via `trigger_integration_tool`).

**Diagnostics & discovery**

| Tool | Description |
| - | - |
| `check_setup` | Diagnostic JSON: API key, connectivity, organization API access, team selection, integrations, quotas. |
| `list_integrations` | List connected social accounts (ids, platform types, channels). |
| `list_integration_tools` / `trigger_integration_tool` | List & call read-only platform helpers - subreddit flairs/requirements, YouTube categories/playlists/regions, LinkedIn mentions, Instagram locations/audio/business discovery, Google Business categories, TikTok trending music. |

**Posts**

| Tool | Description |
| - | - |
| `create_post` / `schedule_post` | Publish now (or as a draft) / schedule for a future date. |
| `update_post` / `retry_post` | Update a post (only changed fields) / re-attempt one that ended in `ERROR`. |
| `get_post_by_reference_key` | Fetch a post by the `referenceKey` set on it instead of its bundle.social id. |
| `list_reconnect_candidates` / `reconnect_posts` | List posts that lost their social account after a disconnect, and reattach them to a newly connected account. |
| `list_posts` / `get_post` / `delete_post` | List with filters / fetch / delete posts. |
| `create_post_import` … | Import post history from a connected account: `create_post_import`, `list_post_imports`, `get_post_import`, `list_imported_posts`, `delete_imported_posts`, `retry_post_import`. |
| `create_post_csv_import` … | Bulk-schedule from a CSV (URL or local file): `create_post_csv_import`, `list_post_csv_imports`, `get_post_csv_import`, `get_post_csv_import_status`, `get_post_csv_import_rows`. |

**Comments**

| Tool | Description |
| - | - |
| `create_comment` / `list_comments` / `get_comment` / `update_comment` / `delete_comment` | Comment on a post (pass `content` multiple times for a chain) / list / fetch / update / delete comments. |
| `create_comment_import` … | Pull existing comments for a post: `create_comment_import`, `list_comment_imports`, `get_comment_import`, `list_imported_comments`. |
| `act_on_imported_comment` | Moderate an imported comment - delete, hide/unhide, like/unlike, approve/reject. |

**Media**

| Tool | Description |
| - | - |
| `upload_media` | Upload an image/video/document from a URL (or local path in stdio mode); auto-chunks large local files. |
| `init_large_upload` / `finalize_large_upload` | Low-level chunked-upload primitives (for manual control). |
| `list_media` / `get_media` / `delete_media` / `delete_media_many` | List / fetch / delete uploads. |

**Integrations (social accounts)**

| Tool | Description |
| - | - |
| `connect_integration` / `disconnect_integration` | Start an OAuth connect flow (returns a URL) / disconnect an account. |
| `create_integration_portal_link` | Hosted portal link for end users to connect accounts. |
| `set_integration_channel` / `unset_integration_channel` / `refresh_integration_channels` | Pick / clear / refresh the channel (page, board, server channel) for an account. |
| `check_integration_connection` / `refresh_integration_profile` / `get_integration_by_type` / `copy_integration` / `list_integrations_to_delete` | Connection check, profile refresh, lookup by platform, copy between teams, list accounts pending deletion. |

**Analytics**

| Tool | Description |
| - | - |
| `get_post_analytics` | Per-post engagement metrics (`raw: true` for the unprocessed payload). |
| `get_account_analytics` | Latest analytics for a connected account by `platform` (`raw: true` for the unprocessed payload). |
| `get_bulk_post_analytics` | Engagement metrics for several posts at once. |
| `refresh_analytics` | Force a fresh pull - by `postId` for a post, otherwise `platform` for an account. |
| `get_analytics_summary` | Org-level usage quotas + latest per-integration analytics snapshot. |

**Teams & organization**

| Tool | Description |
| - | - |
| `list_teams` / `get_team` / `create_team` / `update_team` / `delete_team` | Manage teams. |
| `get_organization` / `get_usage` | Your organization, and posts/comments/uploads/imports usage & quotas. |
| `get_daily_limits_usage` | A connected account's daily post/comment allowance for a given day. |

Errors come back as `{ "error": { "code", "message", "details"? } }` with `isError: true`. The per-platform fields for posts are documented in [Platform parameters](/api-reference/platform-parameters).

## Configuration

Reads `BUNDLESOCIAL_API_KEY` (required), `BUNDLESOCIAL_TEAM_ID` (optional - needed only if your org has more than one team) and `BUNDLESOCIAL_API_URL` (optional). Get an API key in the [dashboard](https://bundle.social/dashboard/organization/api-keys).

<Tabs>
  <Tab title="Claude Desktop">
    `claude_desktop_config.json` (macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`):

    ```json theme={null}
    {
      "mcpServers": {
        "bundlesocial": {
          "command": "npx",
          "args": ["-y", "bundlesocial-mcp"],
          "env": { "BUNDLESOCIAL_API_KEY": "sk_live_..." }
        }
      }
    }
    ```
  </Tab>

  <Tab title="Claude Code">
    ```bash theme={null}
    claude mcp add bundlesocial --env BUNDLESOCIAL_API_KEY=sk_live_... -- npx -y bundlesocial-mcp
    ```

    Or in `.mcp.json`:

    ```json theme={null}
    {
      "mcpServers": {
        "bundlesocial": {
          "command": "npx",
          "args": ["-y", "bundlesocial-mcp"],
          "env": { "BUNDLESOCIAL_API_KEY": "sk_live_..." }
        }
      }
    }
    ```
  </Tab>

  <Tab title="Cursor">
    `~/.cursor/mcp.json` (global) or `.cursor/mcp.json` (project):

    ```json theme={null}
    {
      "mcpServers": {
        "bundlesocial": {
          "command": "npx",
          "args": ["-y", "bundlesocial-mcp"],
          "env": { "BUNDLESOCIAL_API_KEY": "sk_live_..." }
        }
      }
    }
    ```
  </Tab>
</Tabs>

## Example prompts

* "List my connected social accounts via bundle.social."
* "Post 'We just shipped dark mode 🌙' to X and Bluesky."
* "Schedule a LinkedIn post for next Monday 9am UTC announcing the launch."
* "Post to r/test on Reddit - first check the subreddit's requirements and flairs, then post with the right flair."
* "Reply to post `post_abc123` with a 3-comment thread on LinkedIn."
* "How did post `post_abc123` perform?"

Also see: [CLI](/api-reference/cli) · [SDK](/api-reference/sdk).


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
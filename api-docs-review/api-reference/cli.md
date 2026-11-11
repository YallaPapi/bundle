> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# CLI

> Post to 14+ social platforms from your shell, CI, cron or an AI agent.

`bundlesocial-cli` is a thin, scriptable wrapper over the [bundle.social SDK](/api-reference/sdk). It prints **JSON to stdout by default** (one object per command) and human status to stderr - easy for scripts and AI agents to parse.

<CardGroup cols={2}>
  <Card title="npm: bundlesocial-cli" icon="npm" href="https://www.npmjs.com/package/bundlesocial-cli">
    `npx bundlesocial-cli --help`
  </Card>

  <Card title="OpenClaw / agent skill" icon="robot" href="https://www.npmjs.com/package/bundlesocial-cli">
    `npx skills add bundleglobal/bundlesocial-cli`
  </Card>
</CardGroup>

## Install

```bash theme={null}
npx bundlesocial-cli --help     # one-off
npm install -g bundlesocial-cli # global → `bundle-social`
```

Requires Node.js 20+.

## Authenticate

Create an API key in the [dashboard](https://bundle.social/dashboard/organization/api-keys), then:

```bash theme={null}
export BUNDLESOCIAL_API_KEY="sk_live_..."
# optional, if your org has more than one team:
export BUNDLESOCIAL_TEAM_ID="team_..."
# optional, for self-hosted/staging:
export BUNDLESOCIAL_API_URL="https://api.bundle.social"

bundle-social doctor    # sanity-check the setup
```

Every env var also has a flag: `--api-key`, `--team-id`, `--api-url` (work before or after the command).

## Commands

Run `bundle-social <command> --help` for the full option list of any command. The CLI covers the whole bundle.social API surface (the platform-specific edit/delete-after-publish helpers live under `integrations:trigger`).

**Posts**

| Command | What it does |
| - | - |
| `posts:create` | Publish a post immediately (or `--draft`). |
| `posts:schedule` | Schedule a post for a future ISO-8601 `--date`. |
| `posts:update <id>` | Update a post - only the fields you pass change. |
| `posts:list` | List recent posts with filters. |
| `posts:get <id>` / `posts:delete <id>` / `posts:retry <id>` | Fetch / delete / re-attempt a post. |
| `posts:get-by-reference-key <key>` | Fetch a post by the `--reference-key` you set on it instead of its bundle.social id. |
| `posts:reconnect-candidates` / `posts:reconnect` | List posts that lost their social account after a disconnect, and reattach them to a newly connected account. |
| `posts:import` … | Import post history from a connected account: `posts:import`, `posts:imports`, `posts:import:get <importId>`, `posts:import:posts`, `posts:import:delete-posts`, `posts:import:retry <importId>`. |
| `posts:csv` … | Bulk-schedule from a CSV: `posts:csv --file <path>`, `posts:csv:list`, `posts:csv:get <importId>`, `posts:csv:status <importId>`, `posts:csv:rows <importId>`. |

**Comments**

| Command | What it does |
| - | - |
| `comments:create` | Comment on a post; repeat `-c` for a chain of replies (X-style thread via comments). `--imported-post-id` comments on an imported post, `--fetched-parent-comment-id` replies to an imported comment. |
| `comments:list` / `comments:get <id>` / `comments:update <id>` / `comments:delete <id>` | List / fetch / update / delete comments. |
| `comments:retry <id>` | Re-attempt a comment that ended in `ERROR`. |
| `comments:import` … | Pull existing comments for a post: `comments:import`, `comments:imports`, `comments:import:get <importId>`, `comments:import:comments`. |
| `comments:import:action <commentId>` | Moderate an imported comment - `--action DELETE\|HIDE\|UNHIDE\|LIKE\|UNLIKE\|APPROVE\|REJECT`. |

**Media**

| Command | What it does |
| - | - |
| `media:upload <path-or-url>` | Upload an image/video/document; returns the upload object. |
| `media:upload-large <path>` | Chunked upload for large files (>\~90 MB). |
| `media:list` / `media:get <id>` / `media:delete <id>` / `media:delete-many` | List / fetch / delete uploads. |

**Integrations (social accounts)**

| Command | What it does |
| - | - |
| `integrations:list` | List connected social accounts (ids, platform types, channels). |
| `integrations:tools` / `integrations:trigger <method>` | List & call the read-only platform helpers - subreddit flairs/requirements, YouTube categories/playlists/regions, LinkedIn mentions, Instagram locations/audio/business discovery, Google Business categories, TikTok trending music. |
| `integrations:connect` / `integrations:disconnect` | Start an OAuth connect flow / disconnect an account. |
| `integrations:portal-link` | Create a hosted portal link for end users to connect accounts. |
| `integrations:set-channel` / `integrations:unset-channel` / `integrations:refresh-channels` | Pick / clear / refresh the channel (page, board, server channel) for an account. |
| `integrations:check` / `integrations:refresh-profile` / `integrations:by-type <type>` / `integrations:copy` / `integrations:to-delete` | Connection check, profile refresh, lookup by platform, copy between teams, list accounts pending deletion. |

**Analytics**

| Command | What it does |
| - | - |
| `analytics:post [id]` | Engagement metrics for one post - yours, or an imported one via `--imported-post-id` (`--raw` for the unprocessed payload). |
| `analytics:account` | Latest analytics for a connected account by `-p <platform>` (`--raw` for the unprocessed payload). |
| `analytics:bulk` | Engagement metrics for several posts (`--post-id` repeatable). |
| `analytics:refresh` | Force a fresh pull - `--post-id` for a post, otherwise `-p <platform>` for an account. |
| `analytics:summary` | Org-level usage quotas + latest per-integration analytics snapshot. |

**Teams, organization & diagnostics**

| Command | What it does |
| - | - |
| `teams:list` / `teams:get <id>` / `teams:create` / `teams:update <id>` / `teams:delete <id>` | Manage teams. |
| `org:get` / `org:usage` | Your organization, and posts/comments/uploads/imports usage & quotas. |
| `org:daily-limits` | A connected account's daily post/comment allowance for a given day. |
| `doctor` | Diagnostic JSON: API key, connectivity, organization API access, team selection, integrations, quotas. |

### Examples

```bash theme={null}
# text post to X and Bluesky
bundle-social posts:create -c "We just shipped dark mode 🌙" -i x -i bluesky

# TikTok video with the required privacy level
bundle-social posts:create -c "BTS" -i tiktok -m ./demo.mp4 \
  --platform-settings '{"TIKTOK":{"privacy":"PUBLIC_TO_EVERYONE"}}'

# schedule a thread: post, then add replies as comments
POST=$(bundle-social posts:create -i linkedin -c "1/ A thread 🧵")
ID=$(printf '%s' "$POST" | jq -r .id)
bundle-social comments:create --post-id "$ID" -c "2/ more…" -c "3/ even more…"

# Reddit, done right: check requirements + flairs first
bundle-social integrations:trigger reddit:requirements --data '{"subreddit":"r/test"}'
bundle-social integrations:trigger reddit:flairs --data '{"subreddit":"r/test"}'
bundle-social posts:create --data '{"REDDIT":{"sr":"r/test","text":"Title","flairId":"<id>","uploadIds":[]}}'
```

The per-platform fields you can put under `--platform-settings` / `--data` are documented in [Platform parameters](/api-reference/platform-parameters).

## Output contract (for scripts & agents)

* **stdout** = exactly one JSON value per command (or a table with `--pretty`). Pipe it to `jq`.
* **stderr** = human progress + `--pretty` error lines. Never parse stderr.
* On error: exit code `1` and `{ "error": { "code", "message", "details"? } }` on stdout.

<Note>
  The CLI ships with a `SKILL.md` (OpenClaw / agent skill), a `PROVIDER_SETTINGS.md` (exhaustive per-platform field reference) and an `examples/` directory of ready-to-run `data` JSON templates and shell recipes - see the [repo](https://github.com/bundleglobal/bundlesocial-cli).
</Note>

Also see: [MCP server](/api-reference/mcp) · [SDK](/api-reference/sdk) · [Examples](/api-reference/examples).


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
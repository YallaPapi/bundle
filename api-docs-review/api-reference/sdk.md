> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# SDK

> Don't reinvent the wheel. Our typed TypeScript SDK for Node.js handles auth headers and the boring parts, and there is a CLI and MCP server too.

We have a TypeScript SDK. It's typed, it's pretty, and it handles the boring stuff like auth headers.

## Node.js SDK

* **NPM:** [`bundlesocial`](https://www.npmjs.com/package/bundlesocial)
* **Github:** [`bundlesocial-node`](https://github.com/bundleglobal/bundlesocial-node)

### Installation

```bash theme={null}
npm install bundlesocial
# or
pnpm add bundlesocial
```

### Quick Setup

```typescript theme={null}
import { BundleSocial } from 'bundlesocial';

const bundle = new BundleSocial('pk_live_...');
```

### Common Tasks

#### 1. Upload a Video

```typescript theme={null}
const video = await fs.readFile('./cat_vibing.mp4');
const upload = await bundle.upload.uploadCreate({
  formData: {
    teamId: 'team_123',
    file: new Blob([video], { type: 'video/mp4' }),
  }
});
```

#### 2. Create a Post

```typescript theme={null}
await bundle.post.postCreate({
  requestBody: {
    teamId: 'team_123',
    title: 'Vibing cat',
    status: 'SCHEDULED',
    postDate: '2026-12-25T10:00:00.000Z',
    socialAccountTypes: ['TIKTOK', 'YOUTUBE'],
    data: {
      TIKTOK: {
        text: "Vibing cat 🎵",
        uploadIds: [upload.id],
        privacy: 'PUBLIC_TO_EVERYONE'
      },
      YOUTUBE: {
        text: "Shorts cat",
        type: 'SHORT',
        madeForKids: false,
        uploadIds: [upload.id]
      }
    }
  }
});
```

#### 3. Handle Webhooks

```typescript theme={null}
// Express handler
const event = bundle.webhooks.constructEvent(
  rawBody,
  signature,
  process.env.WEBHOOK_SECRET
);

if (event.type === 'post.published') {
  console.log('We are live!');
}
```

<Note>
  **Need Python or Go?**\
  We generate our SDKs from OpenAPI. If you need another language, just ask (or use the OpenAPI spec directly).
</Note>

## Prefer a CLI or an AI client?

<CardGroup cols={2}>
  <Card title="CLI" icon="terminal" href="/api-reference/cli">
    `bundlesocial-cli` - JSON-first command line for shells, CI, cron and shell-out agents (ships an OpenClaw skill).
  </Card>

  <Card title="MCP server" icon="plug" href="/api-reference/mcp">
    `bundlesocial-mcp` - drive bundle.social from Claude Desktop / Claude Code / Cursor and other MCP clients.
  </Card>
</CardGroup>

The per-platform `data` fields used above are documented in [Platform parameters](/api-reference/platform-parameters).


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
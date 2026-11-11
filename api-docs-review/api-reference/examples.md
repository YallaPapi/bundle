> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Examples

> Working code, not pseudocode. Examples for schedulers, analytics dashboards, bulk uploaders, and webhook handlers, plus a GitHub repo and Postman collection.

We're actively building out a library of examples covering common use cases - schedulers, analytics dashboards, bulk uploaders, webhook handlers, and more. This section is growing, so check back often.

## Select A Channel After OAuth

For Facebook, Instagram through Facebook Login, LinkedIn, YouTube, and Google Business, OAuth alone is not enough. After the user connects, select the page, profile, channel, or location they want this team to use.

```ts theme={null}
await fetch("https://api.bundle.social/api/v1/social-account/set-channel", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "x-api-key": process.env.BUNDLE_API_KEY
  },
  body: JSON.stringify({
    teamId: "team_123",
    type: "FACEBOOK",
    channelId: "page_123"
  })
});
```

Use `refresh-channels` before showing a custom picker if your cached channel list may be stale.

```ts theme={null}
await fetch("https://api.bundle.social/api/v1/social-account/refresh-channels", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "x-api-key": process.env.BUNDLE_API_KEY
  },
  body: JSON.stringify({
    teamId: "team_123",
    type: "FACEBOOK"
  })
});
```

## Create A Scheduled Post

```ts theme={null}
await fetch("https://api.bundle.social/api/v1/post", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "x-api-key": process.env.BUNDLE_API_KEY
  },
  body: JSON.stringify({
    teamId: "team_123",
    title: "Launch post",
    status: "SCHEDULED",
    postDate: "2026-06-01T15:00:00.000Z",
    socialAccountTypes: ["FACEBOOK", "INSTAGRAM"],
    data: {
      FACEBOOK: {
        type: "POST",
        text: "We are live.",
        uploadIds: ["upload_image_123"]
      },
      INSTAGRAM: {
        type: "POST",
        text: "We are live.",
        uploadIds: ["upload_image_123"],
        altText: "Product dashboard screenshot"
      }
    }
  })
});
```

## Fetch Raw Analytics

Raw analytics return the raw payload stored for the newest analytics snapshot. Availability depends on platform.

```ts theme={null}
const response = await fetch(
  "https://api.bundle.social/api/v1/analytics/social-account/raw?teamId=team_123&platformType=FACEBOOK",
  {
    headers: {
      "x-api-key": process.env.BUNDLE_API_KEY
    }
  }
);

const rawAnalytics = await response.json();
```

## Handle Post Webhooks

There is no separate `post.failed` event. Use `post.published` and inspect `data.status`.

```ts theme={null}
export async function handleWebhook(event: {
  type: string;
  data: { id: string; status?: string; errors?: unknown };
}) {
  if (event.type !== "post.published") return;

  if (event.data.status === "ERROR") {
    await markPostFailed(event.data.id, event.data.errors);
    return;
  }

  if (event.data.status === "POSTED") {
    await markPostPublished(event.data.id);
  }
}
```

## More Resources

<CardGroup>
  <Card title="GitHub repo with examples" icon="github" href="https://github.com/bundleglobal/bundlesocial-examples" />

  <Card title="Postman collection" icon="code" href="https://www.postman.com/socialmediaapibundle/bundle-social-social-media-api/overview" />
</CardGroup>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
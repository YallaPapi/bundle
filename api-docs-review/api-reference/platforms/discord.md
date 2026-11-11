> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Discord

> Channel-based messaging via webhooks, not OAuth. Requires a channelId on every post, and supports custom bot identity and media attachments.

Discord works differently from other platforms. Instead of OAuth tokens, we use **webhooks** that you set up in your Discord server.

## Quirks & Gotchas

### Webhook-Based Posting

Discord doesn't allow third-party apps to post as a user. Instead, we use webhooks.

* You connect a Discord server and select which channels to enable.
* We create a webhook for each channel.
* Posts appear as a "bot" message with a customizable username and avatar.

### Channel Selection Required

Unlike other platforms, you must specify a `channelId` in your post data. You can find available channels in the `socialAccount.channels` array.

### Custom Bot Identity

You can customize how your posts appear:

* `username`: Up to 80 characters. This is the name shown as the message author.
* `avatarUrl`: A URL to an image that will be used as the bot's avatar.

***

## Post Options

| Field | Type | Description |
| :- | :- | :- |
| `channelId` | `string` | **Required.** The channel to post to. Found in `socialAccount.channels`. |
| `text` | `string` | Message content. Max 2000 characters. |
| `uploadIds` | `string[]` | Media attachments (images, videos). |
| `username` | `string` | Custom display name. Max 80 characters. |
| `avatarUrl` | `string` | Custom avatar URL. Max 2048 characters. |

***

## Media Limits

| Constraint | Value |
| :- | :- |
| Files | 0-10 (images and/or videos, mixed allowed) |
| Video max size | 25 MB |
| Image max size | 25 MB |
| Text | Max 2,000 characters |

See [Platform Limits](/api-reference/limits#discord) for more details.

### Text & Field Limits

| Field | Limit |
| :- | :- |
| `text` | Max 2,000 characters |
| `username` | Max 80 characters |
| `avatarUrl` | Max 2,048 characters |

***

## Analytics

For general analytics concepts, see the [Analytics Overview](/api-reference/analytics).

Discord does not provide analytics via its API. All metrics return `0`. It's a messaging platform, not an analytics platform.

| Metric | Note |
| :- | :- |
| `impressions` | Returns `0` |
| `views` | Returns `0` |
| `likes` | Returns `0` |
| `comments` | Returns `0` |

***

## Example

```javascript theme={null}
await bundle.post.create({
  socialAccountTypes: ["DISCORD"],
  data: {
    DISCORD: {
      channelId: "123456789012345678",
      text: "Hello from bundle.social!",
      username: "My Bot",
      avatarUrl: "https://example.com/avatar.png"
    }
  }
});
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
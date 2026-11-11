> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Slack

> Workspace messaging via incoming webhooks. Needs an admin to connect, a channel selection per post, and gives you a generous 30k character limit.

Like Discord, Slack uses a webhook-based approach for posting messages.

## Quirks & Gotchas

### Webhook-Based Posting

Slack requires you to connect a workspace and select channels. We use incoming webhooks to post messages.

* You must be a workspace admin to connect.
* Posts appear as a bot message in the selected channel.

### Channel Selection Required

You must specify a `channelId` in your post data. Available channels are in `socialAccount.channels`.

### Generous Character Limit

Slack allows up to **30,000 characters** per message-much more than most platforms.

### Custom Bot Identity

Like Discord, you can customize the bot appearance:

* `username`: Up to 80 characters.
* `avatarUrl`: A URL to an image for the bot's avatar.

***

## Post Options

| Field | Type | Description |
| :- | :- | :- |
| `channelId` | `string` | **Required.** The channel to post to. Found in `socialAccount.channels`. |
| `text` | `string` | Message content. Max 30,000 characters. |
| `uploadIds` | `string[]` | Media attachments. |
| `username` | `string` | Custom display name. Max 80 characters. |
| `avatarUrl` | `string` | Custom avatar URL. Max 2048 characters. |

***

## Media Limits

| Constraint | Value |
| :- | :- |
| Files | 0-4 (images and/or videos, mixed allowed) |
| Video max size | 1 GB |
| Image max size | 1 GB |
| Text | Max 30,000 characters |

See [Platform Limits](/api-reference/limits#slack) for more details.

### Text & Field Limits

| Field | Limit |
| :- | :- |
| `text` | Max 30,000 characters |
| `username` | Max 80 characters |
| `avatarUrl` | Max 2,048 characters |

***

## Analytics

For general analytics concepts, see the [Analytics Overview](/api-reference/analytics).

Slack does not provide analytics via its API. All metrics return `0`. It's a workspace tool, not a social media platform.

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
  socialAccountTypes: ["SLACK"],
  data: {
    SLACK: {
      channelId: "C0123456789",
      text: "New product launch! Check it out.",
      username: "Marketing Bot"
    }
  }
});
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
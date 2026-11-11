> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Callback Parameters

> Handle success and error query parameters after social account OAuth completes.

Whether you use hosted or custom UI, the user eventually comes back to your `redirectUrl` with query parameters.

***

## Success Callbacks

| Parameter | Message |
| :- | :- |
| `twitter-callback` | Twitter connected successfully |
| `pinterest-callback` | Pinterest connected successfully |
| `tiktok-callback` | TikTok connected successfully |
| `facebook-callback` | Facebook connected successfully |
| `instagram-callback` | Instagram connected successfully |
| `linkedin-callback` | LinkedIn connected successfully |
| `reddit-callback` | Reddit connected successfully |
| `discord-callback` | Discord connected successfully |
| `slack-callback` | Slack connected successfully |
| `youtube-callback` | YouTube connected successfully |
| `snapchat-callback` | Snapchat Public Profile connected successfully |
| `threads-callback` | Threads connected successfully |
| `mastodon-callback` | Mastodon connected successfully |
| `bluesky-callback` | Bluesky connected successfully |
| `google-business-callback` | Google Business connected successfully |

***

## Error Callbacks

| Platform | Parameter | Message |
| :- | :- | :- |
| Twitter/X | `twitter-callback` | Error connecting Twitter |
| Twitter/X | `twitter-not-enough-permissions` | User did not grant all required permissions |
| Pinterest | `pinterest-callback` | Error connecting Pinterest |
| Pinterest | `pinterest-not-enough-permissions` | User did not grant all required permissions |
| TikTok | `tiktok-callback` | Error connecting TikTok |
| TikTok | `tiktok-not-enough-permissions` | User did not grant all required permissions |
| Facebook | `facebook-callback` | Error connecting Facebook |
| Facebook | `facebook-not-enough-pages` | User does not have enough permissions on any Facebook Pages |
| Facebook | `facebook-not-enough-permissions` | User did not grant all required permissions |
| Instagram | `instagram-callback` | Error connecting Instagram |
| Instagram | `instagram-direct-callback` | Error connecting Instagram through direct OAuth (`instagramConnectionMethod: "INSTAGRAM"`) |
| Instagram | `instagram-not-enough-accounts` | User does not have enough permissions on any Instagram account, or no Facebook Page has an Instagram account connected |
| Instagram | `instagram-not-enough-permissions` | User did not grant all required permissions (Instagram login: the content publish permission is required) |
| Instagram | `instagram-reconnect-different-account` | A `reconnect` flow was completed with a different Instagram account than the one connected |
| Instagram | `instagram-not-professional-account` | Instagram account is not a Professional or Creator account |
| LinkedIn | `linkedin-callback` | Error connecting LinkedIn |
| LinkedIn | `linkedin-not-enough-channels` | User does not have enough permissions on any LinkedIn organizations |
| LinkedIn | `linkedin-not-enough-permissions` | User did not grant all required permissions |
| Reddit | `reddit-callback` | Error connecting Reddit |
| Reddit | `reddit-not-enough-permissions` | User did not grant all required permissions |
| Discord | `discord-callback` | Error connecting Discord |
| Discord | `discord-not-enough-servers` | User does not have enough permissions on any Discord servers |
| Discord | `discord-not-enough-permissions` | User did not grant all required permissions |
| Slack | `slack-callback` | Error connecting Slack |
| Slack | `slack-not-enough-workspaces` | User does not have enough permissions on any Slack workspaces |
| Slack | `slack-not-enough-permissions` | User did not grant all required permissions |
| YouTube | `youtube-callback` | Error connecting YouTube |
| YouTube | `youtube-not-enough-channels` | User does not have enough permissions on any YouTube channels |
| YouTube | `youtube-not-enough-permissions` | User did not grant all required permissions |
| Snapchat | `snapchat-callback` | Error connecting Snapchat |
| Snapchat | `snapchat-not-enough-permissions` | User did not grant the required Public Profile permissions |
| Snapchat | `snapchat-no-public-profile` | The Snapchat login has no Public Profile. Create one in the Snapchat app, or log in with the account that owns it |
| Threads | `threads-callback` | Error connecting Threads |
| Threads | `threads-not-enough-permissions` | User did not grant all required permissions |
| Mastodon | `mastodon-callback` | Error connecting Mastodon |
| Mastodon | `mastodon-not-enough-permissions` | User did not grant all required permissions |
| Bluesky | `bluesky-callback` | Error connecting Bluesky |
| Bluesky | `bluesky-not-enough-permissions` | User did not grant all required permissions |
| Google Business | `google-business-callback` | Error connecting Google Business |
| Google Business | `google-business-not-enough-permissions` | User did not tick the "See, edit, create and delete your Google business listings" permission on Google's consent screen |

<Tip>
  Handle `not-enough-permissions` gracefully. Tell the user the permissions are required for publishing, then let them reconnect.
</Tip>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
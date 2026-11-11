> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# OAuth Options

> Understand disableAutoLogin, tiktokForceLogin, forceBrowserOAuth, withBusinessScope, and Instagram connection methods.

These options affect how provider OAuth behaves. They are available in both hosted and custom flows unless noted otherwise.

***

## reconnect

Supported for **Instagram** connected with `instagramConnectionMethod: "INSTAGRAM"`.

When `true`, the OAuth flow re-authorizes the account that is **already connected** to the team instead of creating a new one. New tokens and permissions are saved on the same account, so its posts, scheduled posts and settings stay as they are. Use it when an account needs a fresh grant (for example, publishing fails with a permission error) and you don't want to disconnect it.

```json theme={null}
{
  "type": "INSTAGRAM",
  "instagramConnectionMethod": "INSTAGRAM",
  "reconnect": true
}
```

The user has to log in with the same Instagram account. A different account is refused with `instagram-reconnect-different-account`. Without `reconnect`, connecting a type the team already has still returns `400`. The hosted portal shows a **Reconnect** button for these accounts.

***

## disableAutoLogin

Supported for **Facebook**, **Instagram via Facebook**, **Instagram direct OAuth**, and **TikTok** where the provider supports it.

When `true`, we add provider-specific flags that try to prevent silent account reuse.

Use it when your users manage many accounts from the same browser. Without it, the OAuth popup can reuse the last logged-in platform account.

```json theme={null}
{
  "disableAutoLogin": true
}
```

***

## tiktokForceLogin

Supported only for **TikTok** and currently experimental.

When `true`, bundle.social routes the user through TikTok logout before starting authorization. Use it when TikTok keeps reusing the wrong active account even with `disableAutoLogin`.

```json theme={null}
{
  "type": "TIKTOK",
  "tiktokForceLogin": true
}
```

<Warning>
  This signs the user out of their active TikTok browser session. Use it only when choosing a fresh account is more important than preserving that session.
</Warning>

***

## forceBrowserOAuth

Supported for **Instagram direct OAuth**.

When `true`, Instagram asks the user to log in again instead of reusing the account already logged in on that browser. Use it when connecting several Instagram accounts one after another.

In the [hosted flow](/api-reference/connect-social-accounts/hosted-flow) the flag is applied only on iPhone and iPad; on other devices use `disableAutoLogin`, which has the same effect on Instagram. The custom `connect` endpoint applies it on every device.

```json theme={null}
{
  "type": "INSTAGRAM",
  "instagramConnectionMethod": "INSTAGRAM",
  "forceBrowserOAuth": true
}
```

<Note>
  Keeping the login in the browser on iPhone no longer needs this flag: every Instagram direct connection now stays in the browser on iOS instead of jumping into the Instagram app. On Android, the phone's "Open supported links" setting for the Instagram app decides, and links opened inside other apps (Instagram, WhatsApp, Messenger) use their in-app browser, where the login can fail. If that happens, open the link in a regular browser or on a computer.
</Note>

***

## withBusinessScope

Supported for **Facebook**, **Instagram via Facebook**, and **YouTube**.

When `true`, OAuth requests broader access on top of the standard scope set:

* **Facebook** and **Instagram via Facebook** - the broader Meta scope set, including `business_management`, `ads_management`, and `ads_read` among the permissions we request.
* **YouTube** - the monetary analytics scope (`yt-analytics-monetary.readonly`), which enables **revenue/monetization data** in raw analytics. See [YouTube → Monetization](/api-reference/platforms/youtube#monetization).

When `false`, OAuth uses the standard scope set.

```json theme={null}
{
  "type": "FACEBOOK",
  "withBusinessScope": true
}
```

<Warning>
  Some Facebook Pages and Instagram accounts only appear in the picker when the connection was made with business scope. If something is missing from the list, reconnect using the other method (`withBusinessScope` flipped) before assuming the picker is wrong.
</Warning>

<Note>
  For **YouTube**, the monetary scope is optional. If the user doesn't grant it, the connection still succeeds - only monetization data is unavailable. Missing it never blocks a connection.
</Note>

***

## Instagram Connection Method

Supported for `type: "INSTAGRAM"` in custom UI and hosted portal links.

| Value | Meaning | Channel selection |
| :- | :- | :- |
| `FACEBOOK` | Instagram through Facebook Login. This is the default path when omitted. | Required. Use `set-channel`. |
| `INSTAGRAM` | Direct Instagram OAuth. | Not supported. The account is selected directly during OAuth. |

Use Facebook Login when you need Facebook-backed Instagram features such as Page-connected account selection, comments, insights, location search, or Instagram audio search for Reels.

Use direct Instagram OAuth when you explicitly want the direct Instagram OAuth path and do not need Facebook-backed channel selection.

***

## serverUrl

Supported for **Mastodon** and **Bluesky** in the custom UI flow.

| Platform | Required? | Example |
| :- | :- | :- |
| Mastodon | Yes | `https://mastodon.social` |
| Bluesky | No, but supported | `https://bsky.social` |

```json theme={null}
{
  "type": "MASTODON",
  "teamId": "team_123",
  "redirectUrl": "https://app.example.com/oauth/callback",
  "serverUrl": "https://mastodon.social"
}
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
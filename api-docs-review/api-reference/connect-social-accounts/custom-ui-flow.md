> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Custom UI Flow

> Build your own social account connection flow using the connect endpoint, callbacks, and channel endpoints.

Use custom UI when you want full control over account connection screens. You generate an OAuth URL, redirect the user, handle the callback, fetch the saved social account, and call channel endpoints when a platform needs a selected target.

**Endpoint:** `POST /api/v1/social-account/connect`

Test it in [Swagger](https://api.bundle.social/swagger#/socialAccount/socialAccount.connect) or the [API Reference Client](/api-reference/client/socialaccount/connect).

```json theme={null}
{
  "type": "INSTAGRAM",
  "teamId": "team_123",
  "redirectUrl": "https://app.example.com/oauth/callback",
  "instagramConnectionMethod": "FACEBOOK",
  "disableAutoLogin": true,
  "withBusinessScope": true
}
```

Response:

```json theme={null}
{
  "url": "https://www.facebook.com/v..."
}
```

Redirect the user to `url`.

***

## Connect Body

These are the available body fields for the custom flow.

| Field | Required | Description |
| :- | :- | :- |
| `type` | Yes | Platform to connect. See [Supported Types](#supported-types). |
| `teamId` | Yes | Team that should receive the connected social account. |
| `redirectUrl` | Yes | HTTP/HTTPS URL where the platform sends the user after OAuth. We append callback query parameters to this URL. |
| `serverUrl` | Depends | Required for Mastodon. Optional issuer/server URL for Bluesky. |
| `disableAutoLogin` | No | Adds provider-specific flags to avoid automatic login or silent account reuse where supported. Defaults to `false`. |
| `tiktokForceLogin` | No | Experimental TikTok-only option. Routes authorization through TikTok logout to request a fresh login session. Defaults to `false`. |
| `forceBrowserOAuth` | No | Instagram direct OAuth only. Forces browser OAuth on phones where possible. Defaults to `false`. |
| `instagramConnectionMethod` | No | Instagram only. Use `FACEBOOK` or `INSTAGRAM`. If omitted, the Facebook login path is used. |
| `withBusinessScope` | No | Facebook, Instagram via Facebook, and YouTube. Adds broader Meta business scopes for Meta, or the monetary analytics scope (revenue/monetization data) for YouTube, when `true`. Defaults to `false`. |

### Supported Types

`TIKTOK`, `YOUTUBE`, `SNAPCHAT`, `INSTAGRAM`, `FACEBOOK`, `TWITTER`, `THREADS`, `LINKEDIN`, `PINTEREST`, `REDDIT`, `MASTODON`, `DISCORD`, `SLACK`, `BLUESKY`, `GOOGLE_BUSINESS`

***

## Platform-Specific Options

| Option | Applies to | Notes |
| :- | :- | :- |
| `serverUrl` | Mastodon, Bluesky | Mastodon requires it. Bluesky can use it for a custom issuer/server. |
| `instagramConnectionMethod: "FACEBOOK"` | Instagram | Uses Facebook Login and supports Page/account channel selection, comments, insights, locations, and Instagram audio search. |
| `instagramConnectionMethod: "INSTAGRAM"` | Instagram | Uses direct Instagram OAuth. No `set-channel`, `unset-channel`, or `refresh-channels`. Some Facebook-backed features are not available. |
| `disableAutoLogin` | Facebook, Instagram via Facebook, Instagram direct OAuth, TikTok | Helps users pick the correct platform account when many accounts are used in one browser. |
| `tiktokForceLogin` | TikTok | Experimental stronger fresh-login flow. Redirects through TikTok logout before authorization. |
| `forceBrowserOAuth` | Instagram direct OAuth | Avoids the Instagram iOS app deep-link path when possible. |
| `withBusinessScope` | Facebook, Instagram via Facebook, YouTube | Meta: can expose Pages and Instagram accounts hidden in the standard scope flow. YouTube: adds the monetary analytics scope that enables revenue/monetization data. Optional for YouTube - if not granted, the connection still succeeds and only monetization is unavailable. |

<Warning>
  For Facebook and Instagram via Facebook, ask users to select **all Pages and Instagram accounts they manage** in Meta OAuth. Then call `set-channel` for the one target this team should use.
</Warning>

***

## Basic Flow

1. Call `POST /api/v1/social-account/connect`.
2. Redirect the user to the returned `url`.
3. Handle the callback query parameters on your `redirectUrl`.
4. Fetch the social account with `GET /api/v1/social-account/by-type`.
5. If `socialAccount.channels` contains selectable targets, show them in your UI.
6. Call `POST /api/v1/social-account/set-channel` when required.

Snapchat connects the Public Profile returned by OAuth and does not need channel selection.

<img src="https://mintcdn.com/bundlesocial/I73jzIjdXCLeLiMD/images/api-reference/connect-social-account/connect-social-account.png?fit=max&auto=format&n=I73jzIjdXCLeLiMD&q=85&s=abab69c85854962f34899fdc4b9f9d71" alt="Connect social account flow" width="1977" height="1241" data-path="images/api-reference/connect-social-account/connect-social-account.png" />

***

## Fetch The Connected Account

Use this after the callback to inspect the connection and available channels.

**Endpoint:** `GET /api/v1/social-account/by-type`

Query:

| Field | Required | Description |
| :- | :- | :- |
| `type` | Yes | Platform type. |
| `teamId` | Yes | Team ID. |

```http theme={null}
GET /api/v1/social-account/by-type?type=FACEBOOK&teamId=team_123
```

If the platform needs channel selection, read `socialAccount.channels` and call [Set Channel](/api-reference/connect-social-accounts/channel-management#set-channel).

***

## Helper Endpoints

These endpoints are useful in a full custom UI.

| Endpoint | Method | Use |
| :- | :- | :- |
| `/api/v1/social-account/disconnect` | `DELETE` | Disconnect a social account from the team. This also removes it from scheduled posts. |
| `/api/v1/social-account/set-channel` | `POST` | Select a Page, channel, organization, or location after OAuth. |
| `/api/v1/social-account/unset-channel` | `POST` | Clear the selected channel while keeping the OAuth connection. |
| `/api/v1/social-account/refresh-channels` | `POST` | Refresh available targets saved in `socialAccount.channels`. |
| `/api/v1/social-account/connection-check` | `POST` | Manually check whether a connected account is still valid. Requires a selected channel/account where the platform needs one. |
| `/api/v1/social-account/profile-refresh` | `POST` | Manually refresh profile information for a connected social account. |
| `/api/v1/social-account/by-type` | `GET` | Fetch the connected social account for a team and platform. |

Channel details live in [Channel Management](/api-reference/connect-social-accounts/channel-management). Callback query parameters live in [Callback Parameters](/api-reference/connect-social-accounts/callbacks).


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
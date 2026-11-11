> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Ice Breakers & Persistent Menu

> Manage Instagram ice breakers and the Facebook Messenger persistent menu and Get Started button.

Some conversation UI lives on the platform itself, not in a message. We manage two of those for you:

| Type | Platform | What it is |
| :- | :- | :- |
| `INSTAGRAM_ICE_BREAKERS` | Instagram | Up to 4 suggested questions shown to people who open a new chat with you |
| `FACEBOOK_PERSISTENT_MENU` | Facebook | The always-visible Messenger menu (up to 3 items) and the Get Started button |

A tap on an ice breaker, menu item or Get Started sends its `payload`, which you catch with a `BUTTON_CLICKED` flow. That's how "tap *Pricing* → get the price list" works.

Every Facebook persistent menu comes with a Get Started button. Its payload is `GET_STARTED` unless you set `getStartedPayload`. A `BUTTON_CLICKED` flow with `"payloads": ["GET_STARTED"]` makes a nice welcome message.

## Save, Then Sync

Saving and pushing to the platform are two separate calls, so you can prepare changes safely.

**1. Save:** `PUT /api/v1/automation-provider-settings/:socialAccountId/:type`

`:type` is `INSTAGRAM_ICE_BREAKERS` or `FACEBOOK_PERSISTENT_MENU`, and `platform` in the body has to match it. Saving only stores the config and sets the status to `DRAFT` (or `DISABLED`, if you send `"status": "DISABLED"`). Whatever you synced before stays live on the platform until you sync again.

```json theme={null}
{
  "teamId": "team_123",
  "platform": "INSTAGRAM",
  "config": {
    "iceBreakers": [
      { "question": "What are your prices?", "payload": "ICE_PRICING" },
      { "question": "Do you ship internationally?", "payload": "ICE_SHIPPING" },
      { "question": "Talk to a human", "payload": "ICE_HUMAN" }
    ]
  }
}
```

For the Facebook persistent menu:

```json theme={null}
{
  "teamId": "team_123",
  "platform": "FACEBOOK",
  "config": {
    "getStartedPayload": "GET_STARTED",
    "composerInputDisabled": false,
    "items": [
      { "type": "POSTBACK", "title": "Pricing", "payload": "MENU_PRICING" },
      { "type": "POSTBACK", "title": "Book a demo", "payload": "MENU_DEMO" },
      { "type": "URL", "title": "Visit website", "url": "https://yourshop.com" }
    ]
  }
}
```

`composerInputDisabled: true` hides the text box, so people can only use the menu. Use it carefully.

**2. Sync:** `POST /api/v1/automation-provider-settings/:id/sync`

This pushes the saved config to Instagram or Facebook. If the platform rejects it, the call returns an error with the platform's message and the setting keeps its previous status. Otherwise the response tells you how it went:

| Status | Meaning |
| :- | :- |
| `DRAFT` | Saved, not pushed yet |
| `SYNCED` | Live on the platform. `lastSyncedAt` says when. |
| `SYNC_FAILED` | We couldn't push it, for example because the account is missing its access token. `lastSyncError.message` says why. Reconnect the account if needed and sync again. |
| `DISABLED` | Marked for removal. After a sync, it's removed from the platform. |

To **remove** ice breakers or the menu, save the setting with `"status": "DISABLED"` and sync it. Removing the Facebook menu also removes the Get Started button. Reconnected an account? Sync again to be safe.

List what you have with `GET /api/v1/automation-provider-settings?teamId=team_123` (filters: `platform`, `socialAccountId`, `type`, `status`, plus `offset` and `limit`). The list returns `{ items, total }`, most recently updated first. Every other endpoint here returns the setting:

```json theme={null}
{
  "id": "ps_1",
  "teamId": "team_123",
  "platform": "INSTAGRAM",
  "socialAccountId": "sa_789",
  "type": "INSTAGRAM_ICE_BREAKERS",
  "status": "SYNCED",
  "config": {
    "iceBreakers": [{ "question": "What are your prices?", "payload": "ICE_PRICING" }]
  },
  "lastSyncedAt": "2026-09-26T09:00:00.000Z",
  "lastSyncError": null,
  "socialAccount": { "id": "sa_789", "type": "INSTAGRAM", "username": "mybrand" },
  "createdAt": "2026-09-20T10:00:00.000Z",
  "updatedAt": "2026-09-26T09:00:00.000Z"
}
```


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
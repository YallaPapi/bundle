> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Channel Management

> Use set-channel, refresh-channels, and unset-channel for social accounts with selectable targets.

Some platforms connect one user account first, then require you to pick the exact target for the team. Examples: Facebook Pages, Instagram accounts connected to Facebook Pages, LinkedIn organizations, YouTube channels, and Google Business locations.

***

## Set Channel

Use `set-channel` after OAuth when a platform needs a selected Page, channel, organization, or location.

**Endpoint:** `POST /api/v1/social-account/set-channel`

```json theme={null}
{
  "type": "FACEBOOK",
  "teamId": "team_123",
  "channelId": "page_123"
}
```

Use a `channelId` from `socialAccount.channels`.

| Field | Required | Description |
| :- | :- | :- |
| `type` | Yes | One of `FACEBOOK`, `INSTAGRAM`, `LINKEDIN`, `YOUTUBE`, `GOOGLE_BUSINESS`. |
| `teamId` | Yes | Team ID. |
| `channelId` | Yes | ID from `socialAccount.channels`. |

### Platforms Requiring Set Channel

| Platform | Target |
| :- | :- |
| Facebook | Facebook Page |
| Instagram via Facebook | Instagram account connected to a Facebook Page |
| LinkedIn | Member profile or Company Page / organization |
| YouTube | YouTube channel |
| Google Business | Business location |

<Warning>
  If you skip `set-channel` for a platform that requires it, the social account remains connected but has no selected publishing target (`externalId` is empty). Posts, comments, imports, analytics, and Google Business APIs can fail because bundle.social has no concrete Page/channel/location to act on.
</Warning>

<Note>
  Direct Instagram OAuth (`instagramConnectionMethod: "INSTAGRAM"`) does not support `set-channel`.
</Note>

***

## Meta Rule: Select All First

For Facebook and Instagram via Facebook, users should select **all Pages and Instagram accounts they manage** in the Meta OAuth screen.

Then your UI should show `socialAccount.channels` and call `set-channel` with the one Page or Instagram account for the current team.

This avoids Meta overwriting page grants when the same Meta user connects different bundle.social teams with different Pages.

***

## Refresh Channels

Use `refresh-channels` when `socialAccount.channels` may be stale.

**Endpoint:** `POST /api/v1/social-account/refresh-channels`

```json theme={null}
{
  "type": "PINTEREST",
  "teamId": "team_123"
}
```

| Field | Required | Description |
| :- | :- | :- |
| `type` | Yes | One of the supported refresh platforms below. |
| `teamId` | Yes | Team ID. |

| Platform | What gets refreshed |
| :- | :- |
| Discord | Available webhook channels |
| Slack | Available webhook channels |
| Reddit | Available subreddits, user destinations, and metadata |
| Pinterest | Boards |
| Facebook | Pages |
| Instagram via Facebook | Instagram accounts connected to Pages |
| LinkedIn | Member profile and organizations |
| YouTube | Channels |
| Google Business | Locations |

<Note>
  Direct Instagram OAuth does not support `refresh-channels`.
</Note>

***

## Unset Channel

Use `unset-channel` when the user picked the wrong target and wants to choose another one without a full reconnect.

**Endpoint:** `POST /api/v1/social-account/unset-channel`

```json theme={null}
{
  "type": "FACEBOOK",
  "teamId": "team_123"
}
```

| Field | Required | Description |
| :- | :- | :- |
| `type` | Yes | One of `FACEBOOK`, `INSTAGRAM`, `LINKEDIN`, `YOUTUBE`, `GOOGLE_BUSINESS`. |
| `teamId` | Yes | Team ID. |

### What Happens

1. The selected Page, channel, or location is cleared from the social account.
2. The OAuth connection stays intact.
3. The account is removed from all draft and scheduled posts.
4. Posts that only had this account become drafts.
5. `social-account.updated` and `team.updated` webhooks fire.

### Switch Flow

1. Call `POST /api/v1/social-account/unset-channel`.
2. Show the current `socialAccount.channels` list.
3. Call `POST /api/v1/social-account/set-channel` with the new target ID.

<Warning>
  Unsetting removes the account from all draft and scheduled posts. If a post only had this one account, it becomes a draft.
</Warning>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
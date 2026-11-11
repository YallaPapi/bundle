> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Connect Social Accounts

> Learn how OAuth, hosted connect links, custom connect flows, and channel selection work in bundle.social.

Connecting social accounts has two separate parts:

1. **OAuth:** the user grants bundle.social access to the platform account.
2. **Channel selection:** bundle.social selects the exact Page, channel, organization, location, board, subreddit, or workspace target to use for this team.

Most integration bugs happen when these steps get mixed together. OAuth says "this Meta user granted access." Channel selection says "this team should use this Facebook Page."

<CardGroup cols={2}>
  <Card title="Hosted Flow" icon="link" href="/api-reference/connect-social-accounts/hosted-flow">
    Create a portal link and let bundle.social handle OAuth, pickers, language, and UI.
  </Card>

  <Card title="Custom UI Flow" icon="code" href="/api-reference/connect-social-accounts/custom-ui-flow">
    Build the account picker yourself and call the connect and channel endpoints directly.
  </Card>

  <Card title="Channel Management" icon="shuffle" href="/api-reference/connect-social-accounts/channel-management">
    Use `set-channel`, `refresh-channels`, and `unset-channel` for platforms with multiple targets.
  </Card>

  <Card title="OAuth Options" icon="key" href="/api-reference/connect-social-accounts/oauth-options">
    Understand `disableAutoLogin`, `forceBrowserOAuth`, `withBusinessScope`, and Instagram connection methods.
  </Card>

  <Card title="Callback Parameters" icon="route" href="/api-reference/connect-social-accounts/callbacks">
    Handle success and error query parameters after OAuth completes.
  </Card>
</CardGroup>

***

## Which Flow Should I Use?

| Flow | Best for | What you build |
| :- | :- | :- |
| Hosted flow | Most apps | A button that opens the portal link |
| Custom UI flow | Apps that need a fully custom account connection UI | OAuth button, callback handling, channel picker, and reconnect states |

<Tip>
  Use the hosted flow unless you have a strong reason to own the whole connection UI.
</Tip>

***

## The Meta Rule

For **Facebook** and **Instagram via Facebook**, ask the user to select **all Pages and Instagram accounts they manage** in the Meta OAuth screen.

After OAuth, choose the one Page or Instagram account for the current bundle.social team in the hosted picker or with `POST /api/v1/social-account/set-channel`.

This does **not** mean one team publishes to every Page. Meta keeps the app grant for every Page the user manages, while bundle.social stores the selected target separately per team.

<Warning>
  If the same Meta user connects multiple bundle.social teams and selects only one Page during each OAuth flow, Meta can overwrite page grants for the bundle.social app at the Meta-user level.

  That can leave one team looking connected in bundle.social, while Meta has removed the Page grant remotely. Publishing can then fail with `must be granted before impersonating a user's page`.
</Warning>

Correct flow:

1. Reconnect Facebook or Instagram via Facebook.
2. In Meta OAuth, choose **Select all** or manually select every Page and Instagram account the Meta user manages.
3. Back in bundle.social, select the one Page or Instagram account for this team.
4. Retry the failed post.

***

## Platform Selection Rules

| Platform | OAuth enough? | Needs `set-channel`? | Notes |
| :- | :- | :- | :- |
| Facebook | No | Yes | Select a Facebook Page. |
| Instagram via Facebook | No | Yes | Select an Instagram account connected to a Facebook Page. |
| Instagram direct OAuth | Yes | No | Pass `instagramConnectionMethod: "INSTAGRAM"` in custom UI. |
| LinkedIn | No | Yes | Select a member profile or Company Page. |
| YouTube | No | Yes | Select a YouTube channel. |
| Snapchat | Yes | No | Uses the Public Profile returned during OAuth. |
| Google Business | No | Yes | Select a business location. |
| Pinterest | Usually yes | No | Boards can be refreshed with `refresh-channels`. |
| Reddit | Usually yes | No | Destinations can be refreshed with `refresh-channels`. |
| Slack | Usually yes | No | Webhook channels can be refreshed with `refresh-channels`. |
| Discord | Usually yes | No | Webhook channels can be refreshed with `refresh-channels`. |

Need endpoint details? Start with [Hosted Flow](/api-reference/connect-social-accounts/hosted-flow) or [Custom UI Flow](/api-reference/connect-social-accounts/custom-ui-flow).


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
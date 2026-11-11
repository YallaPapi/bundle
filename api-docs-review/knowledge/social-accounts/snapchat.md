> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Connect your Snapchat account to bundle.social

> Connect a Snapchat Public Profile to bundle.social for Stories, Spotlights, and analytics.

Snapchat integration works with **Snapchat Public Profiles**. Make sure the Snapchat user you authorize can manage the Public Profile you want to publish to.

## Connect Snapchat

1. Open **Social accounts** from the dashboard sidebar.
2. Click **Connect** on the Snapchat tile.
3. Log in to Snapchat with the user that manages the Public Profile.
4. Approve the requested Public Profile permissions.
5. After Snapchat redirects you back, confirm that the tile shows the Public Profile name and a **Disconnect** button.

There is no separate channel picker. bundle.social uses the Public Profile returned by Snapchat during OAuth.

## What You Can Do

* publish a Public Story with one image or MP4 video,
* publish a Spotlight with one MP4 video,
* schedule Snapchat content with other platforms,
* retrieve Public Profile, Story, and Spotlight analytics.

See the [Snapchat API guide](/api-reference/platforms/snapchat) for post fields and media limits.

## Troubleshooting

<Warning>No Snapchat Public Profile was found.</Warning>

The authorized user does not have access to an eligible Public Profile. Create or finish configuring the profile in Snapchat, then reconnect.

<Warning>You didn't grant all required permissions.</Warning>

Disconnect Snapchat, start the connection again, and approve all requested permissions.

<Warning>Snapchat media is still processing.</Warning>

This is normally temporary. Keep the post in its current state while bundle.social polls Snapchat and completes publishing.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
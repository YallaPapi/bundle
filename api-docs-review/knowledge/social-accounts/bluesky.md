> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Connect your Bluesky account to bundle.social

> Learn how to connect Bluesky to bundle.social using AT Protocol OAuth.

In this tutorial, you will learn how to connect a Bluesky account to your team.

<h2>First things first, create a team or be a part of one</h2>
If you don't know what teams are, [click here](/knowledge/teams/what-are-teams)
to get up to speed.

## Connect your Bluesky account

Open **Social accounts** from the dashboard sidebar and click **Connect** on the Bluesky tile.

Bluesky uses AT Protocol OAuth. You may be asked for the account handle and authorization server. For most users, this is the default Bluesky server. Advanced users can use a custom server if their account uses a different issuer.

Authorize bundle.social in Bluesky and return to the dashboard. Bluesky does not require channel selection after OAuth.

## What you can do after connecting

* publish text posts,
* attach up to 4 media files,
* create quote posts with `data.BLUESKY.quoteUri`,
* add external link cards,
* create and import replies,
* fetch limited analytics based on available AT Protocol data.

## Errors

<Warning>Missing or invalid Bluesky server.</Warning>
Use the default Bluesky issuer unless the account belongs to a custom AT Protocol service.

<Warning>This team already has a Bluesky account connected.</Warning>
Each team can connect one Bluesky account. Disconnect the existing account first if you need to replace it.

<Warning>Authorization failed.</Warning>
The OAuth session may have expired or the account rejected the request. Start the connection again from bundle.social.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
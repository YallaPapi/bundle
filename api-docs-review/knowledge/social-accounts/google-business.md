> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Connect your Google Business Profile to bundle.social

> Learn how to connect Google Business Profile to bundle.social and select the business location for your team.

In this tutorial, you will learn how to connect a Google Business Profile location to your team.

<h2>First things first, create a team or be a part of one</h2>
If you don't know what teams are, [click here](/knowledge/teams/what-are-teams)
to get up to speed.

## Connect your Google Business Profile

Open **Social accounts** from the dashboard sidebar and click **Connect** on the Google Business tile.

You will be redirected to Google. Log in with an account that has access to the Business Profile locations you want to manage and allow the requested permissions.

After OAuth succeeds, return to bundle.social and select the Google Business location for this team.

<Warning>
  Location selection is required. If no location is selected, the account is connected but publishing, location management, reviews, and analytics can fail because the team has no `externalId` for Google Business.
</Warning>

## What you can do after connecting

* publish Google Business updates, events, offers, and alerts,
* read and update location profile data,
* manage hours, attributes, services, menus, action links, and profile media,
* import Google reviews and manage owner replies,
* fetch location-level raw analytics.

## Errors

<Warning>No Google Business location selected.</Warning>
Select a location after OAuth. If you use a custom API flow, call `POST /api/v1/social-account/set-channel` with `type: "GOOGLE_BUSINESS"` and the selected location ID.

<Warning>This team already has a Google Business Profile connected.</Warning>
Each team can connect one Google Business account and selected location. Disconnect the existing account first if you need to replace it.

<Warning>You don't have access to this Google Business location.</Warning>
Reconnect with a Google account that has permission to manage the location.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
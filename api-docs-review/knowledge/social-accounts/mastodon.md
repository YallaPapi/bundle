> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Connect your Mastodon account to bundle.social

> Learn how to connect a Mastodon account from your instance to bundle.social.

In this tutorial, you will learn how to connect a Mastodon account to your team.

<h2>First things first, create a team or be a part of one</h2>
If you don't know what teams are, [click here](/knowledge/teams/what-are-teams)
to get up to speed.

## Connect your Mastodon account

Open **Social accounts** from the dashboard sidebar and click **Connect** on the Mastodon tile.

Enter the Mastodon server URL for the account you want to connect, for example `https://mastodon.social`. bundle.social registers an OAuth client for that instance and redirects you to the instance authorization screen.

Log in on your Mastodon instance, approve the requested permissions, and return to bundle.social. Mastodon does not require channel selection after OAuth.

## What you can do after connecting

* publish statuses with text and media,
* choose Mastodon visibility with `data.MASTODON.privacy`,
* add content warnings with `data.MASTODON.spoiler`,
* import replies,
* reply to imported comments.

## Errors

<Warning>Invalid Mastodon server URL.</Warning>
Use the full instance URL, including `https://`. The server must support Mastodon OAuth.

<Warning>This team already has a Mastodon account connected.</Warning>
Each team can connect one Mastodon account. Disconnect the existing account first if you need to replace it.

<Warning>You didn't grant all the necessary permissions.</Warning>
Reconnect and allow the requested permissions so publishing and comments can work.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
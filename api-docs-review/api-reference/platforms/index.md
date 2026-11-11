> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Platforms Overview

> Everything you need to know about the platforms we support. The good, the bad, and the API limits.

## Supported Platforms

We support a wide range of social platforms. Our goal is to unify them into a single API, but let's be real. Under the hood, they are all uniquely chaotic.

Here is the current roster:

<CardGroup cols={3}>
  <Card title="Instagram" icon="instagram" href="/api-reference/platforms/instagram">
    Stories, Reels, and Posts. Strict aspect ratios included.
  </Card>

  <Card title="Facebook" icon="facebook" href="/api-reference/platforms/facebook">
    Pages and Reels. Watch out for token expiry.
  </Card>

  <Card title="LinkedIn" icon="linkedin" href="/api-reference/platforms/linkedin">
    Personal Profiles vs. Company Pages.
  </Card>

  <Card title="TikTok" icon="tiktok" href="/api-reference/platforms/tiktok">
    Short-form video king. Copyright music is tricky.
  </Card>

  <Card title="YouTube" icon="youtube" href="/api-reference/platforms/youtube">
    Long-form and Shorts. "Made for Kids" flags are mandatory.
  </Card>

  <Card title="Snapchat" icon="ghost" href="/api-reference/platforms/snapchat">
    Public Stories, Spotlights, and content analytics.
  </Card>

  <Card title="Twitter/X" icon="x-twitter" href="/api-reference/platforms/twitter">
    It's X now. Analytics are... complicated.
  </Card>

  <Card title="Threads" icon="at" href="/api-reference/platforms/threads">
    Meta's text app. Surprisingly decent API.
  </Card>

  <Card title="Pinterest" icon="pinterest" href="/api-reference/platforms/pinterest">
    Pins and Boards.
  </Card>

  <Card title="Reddit" icon="reddit" href="/api-reference/platforms/reddit">
    The front page of the internet. Limited analytics.
  </Card>

  <Card title="Mastodon" icon="mastodon" href="/api-reference/platforms/mastodon">
    Decentralized.
  </Card>

  <Card title="Bluesky" icon="cloud" href="/api-reference/platforms/bluesky">
    The new challenger.
  </Card>

  <Card title="Discord" icon="discord" href="/api-reference/platforms/discord">
    Webhooks and channels. Great for community updates.
  </Card>

  <Card title="Slack" icon="slack" href="/api-reference/platforms/slack">
    Workspace messaging. Automate internal comms.
  </Card>

  <Card title="Google Business" icon="google" href="/api-reference/platforms/google-business">
    Local SEO posts. Events, offers, and updates.
  </Card>
</CardGroup>

## The "Unified" API Myth

We do our best to abstract away the differences, but sometimes a platform is just... special.

* **Aspect Ratios:** Instagram will reject your Reel if it's not 9:16. We can't fix that for you.
* **Rate Limits:** We handle queuing, but if you blast 100 posts in a second, things will slow down.
* **Analytics:** Some platforms give us everything (TikTok), others give us crumbs (Reddit). We return `0` when data isn't available, rather than making numbers up.

Dive into each platform's guide to see the specific quirks, gotchas, and limitations. We've documented them so you don't have to discover them at 3 AM.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
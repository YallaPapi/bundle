> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Get to know organizations in bundle.social

> Learn how organizations work in bundle.social - manage billing, API keys, and webhooks at the organization level across all of your teams.

In this tutorial you will learn how organizations work in bundle.social and what you manage at the organization level.

## What is an organization?

An organization is the top-level account in bundle.social. Each organization can contain many teams, and a few things are shared across all of them: **API keys**, **webhooks**, and **billing** are managed at the organization level rather than per team.

You'll find all of these in the **Organization** section of the sidebar.

<Frame type="glass">
  <img src="https://mintcdn.com/bundlesocial/Xo58NLADtmHCNVc_/images/knowledge/organization/menu.png?fit=max&auto=format&n=Xo58NLADtmHCNVc_&q=85&s=d37f259aff369700496216666130309b" width="476" height="460" data-path="images/knowledge/organization/menu.png" />
</Frame>

## Create an API key

If you want to automate your bundle.social workflow, you can use our API or SDK - [learn more here](/api-reference/introduction).

In the sidebar, click **API Keys**. This is where you create and manage API access.

<Frame type="glass">
  <img src="https://mintcdn.com/bundlesocial/Xo58NLADtmHCNVc_/images/knowledge/organization/api-keys.png?fit=max&auto=format&n=Xo58NLADtmHCNVc_&q=85&s=124c22e6375cd7428a8f638352264932" width="1009" height="395" data-path="images/knowledge/organization/api-keys.png" />
</Frame>

Click **+**, enter a name for the key, and click **Create**.

<Warning>
  You can only see an API key once, so copy it and store it somewhere safe.
</Warning>

<CardGroup cols={2}>
  <Card>
    <Frame type="glass">
      <img src="https://mintcdn.com/bundlesocial/Xo58NLADtmHCNVc_/images/knowledge/organization/create-api-key-modal.png?fit=max&auto=format&n=Xo58NLADtmHCNVc_&q=85&s=68909868ebfd6f0c8084577ff247f316" width="477" height="279" data-path="images/knowledge/organization/create-api-key-modal.png" />
    </Frame>
  </Card>

  <Card>
    <Frame type="glass">
      <img src="https://mintcdn.com/bundlesocial/Xo58NLADtmHCNVc_/images/knowledge/organization/copy-api-key.png?fit=max&auto=format&n=Xo58NLADtmHCNVc_&q=85&s=28795d839301ec507317078c296bc659" width="494" height="240" data-path="images/knowledge/organization/copy-api-key.png" />
    </Frame>
  </Card>
</CardGroup>

## Add a webhook

In the sidebar, click **Webhooks**.

<Frame type="glass">
  <img src="https://mintcdn.com/bundlesocial/Xo58NLADtmHCNVc_/images/knowledge/organization/webhooks.png?fit=max&auto=format&n=Xo58NLADtmHCNVc_&q=85&s=ad3a57c337c74fe4905cb52130ff6608" width="1027" height="369" data-path="images/knowledge/organization/webhooks.png" />
</Frame>

Click the **+** icon. In the popup, enter the URL you want to receive webhook events on.

<Frame type="glass">
  <img src="https://mintcdn.com/bundlesocial/Xo58NLADtmHCNVc_/images/knowledge/organization/add-webhook.png?fit=max&auto=format&n=Xo58NLADtmHCNVc_&q=85&s=ba5949b89c35975cc2dd5ba0810dbf21" width="496" height="312" data-path="images/knowledge/organization/add-webhook.png" />
</Frame>

## Manage billing

To change your plan, click **Billing**. Plans can be billed monthly or yearly using the picker at the top.

<Frame type="glass">
  <img src="https://mintcdn.com/bundlesocial/Xo58NLADtmHCNVc_/images/knowledge/organization/billing.png?fit=max&auto=format&n=Xo58NLADtmHCNVc_&q=85&s=18c8bc765baa34b850ae754f4b3b5c0a" width="2048" height="2042" data-path="images/knowledge/organization/billing.png" />
</Frame>

The **Invoices** tab lists issued invoices and lets organization owners download the available invoice document directly from bundle.social.

If a subscription is paused or scheduled to end, Billing also shows the available resume action before you attempt another plan change.

The **Usage** view shows your post count, API usage, and analytics status for the current period.

<Frame type="glass">
  <img src="https://mintcdn.com/bundlesocial/Xo58NLADtmHCNVc_/images/knowledge/organization/usage.png?fit=max&auto=format&n=Xo58NLADtmHCNVc_&q=85&s=a21265154eeea78c08011d6cc49cf6f9" width="2010" height="742" data-path="images/knowledge/organization/usage.png" />
</Frame>

## Organization settings

Click **Settings** to update your organization's basic information and preferences:

* **Organization name** - the display name for your organization.
* **Enable uploads compression** - compress video uploads to reduce file size and storage costs.
* **Show verbose errors** - display detailed error messages in post details. Useful for debugging, but may contain technical information.
* **Automatic remote disconnect checks** - run periodic disconnect checks for Facebook, Instagram, and Threads. Disable to opt out of automatic detection.
* **Delete disconnected account after** - how many hours to wait before deleting a disconnected social account (0-168, up to 7 days).

Click **Save changes** to apply.

<Frame type="glass">
  <img src="https://mintcdn.com/bundlesocial/Xo58NLADtmHCNVc_/images/knowledge/organization/settings.png?fit=max&auto=format&n=Xo58NLADtmHCNVc_&q=85&s=202c3edbf852aef8b56dc13c64f9451b" width="2024" height="1680" data-path="images/knowledge/organization/settings.png" />
</Frame>

## Summary

You now know what lives at the organization level - API keys, webhooks, billing, and settings - all shared across the teams inside your organization.

<sub>with lukewarm regards c: - bundle.social staff</sub>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
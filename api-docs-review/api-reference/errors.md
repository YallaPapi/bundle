> ## Documentation Index
> Fetch the complete documentation index at: https://info.bundle.social/llms.txt
> Use this file to discover all available pages before exploring further.

# Errors

> When things go wrong (and they will). Standardized error codes across every platform, transient vs non-transient, and the prefixes that tell you who broke.

We standardized errors across all platforms. Whether it's TikTok rejecting your music or Instagram hating your aspect ratio, you get a clean JSON response.

## The Error Object

Look for `errorsVerbose` in the response.

```json theme={null}
{
  "errorsVerbose": {
    "INSTAGRAM": {
      "code": "META:190",
      "userFacingMessage": "Your Instagram token expired. Please reconnect.",
      "isTransient": false
    },
    "TIKTOK": null // Success!
  }
}
```

## Key Fields

| Field | Meaning |
| :- | :- |
| `code` | Stable ID (e.g. `HTTP:429`). Use this for logic. |
| `userFacingMessage` | Safe to show your users. "Please reconnect." |
| `errorMessage` | Raw developer logs. "OAuthException: Validate permission failed." |
| `isTransient` | `true` = Retry later. `false` = Give up / Fix input. |

## Common Error Prefixes

| Prefix | Platform |
| :- | :- |
| `META` | Instagram, Facebook, Threads |
| `TT` | TikTok |
| `LI` | LinkedIn |
| `YT` | YouTube |
| `HTTP` | Generic API errors |

## Transient vs. Non-Transient

* **Transient (`true`):** Rate limits, server timeouts. **Action:** Retry with exponential backoff.
* **Non-Transient (`false`):** Auth errors, validation errors. **Action:** Ask user to fix it (reconnect account, change video file).

## Most Common Platform Errors

These are the most common normalized platform errors we see in production. Use the `canonical_error_key` for support routing, and use the platform message to match what the user saw in the failed post.

<Note>
  Platform providers can change exact wording at any time. Treat the platform message as a representative example, not a strict string match.
</Note>

### Facebook

**Error key:** `account_connection_expired`

**Platform code(s):** `HTTP:401`, `Meta:190:460`, `Meta:190:467`

**Message we received:**

```text theme={null}
Error validating access token: The session has been invalidated because the user changed their password or Facebook has changed the session for security reasons.
```

**Why this happens:** The access token or session used for publishing is no longer valid. This commonly happens after password changes, security checks, expired OAuth sessions, token revocation or just "because".

**What the user should do:** Ask the user to reconnect the platform account. After reconnecting, retry the post. If it fails again immediately, ask them to log into the native platform first and clear any security prompt.

***

**Error key:** `page_or_target_inaccessible`

**Platform code(s):** `HTTP:400`, `Meta:190`

**Message we received:**

```text theme={null}
This Page access token belongs to a Page that is not accessible.
```

**Why this happens:** The selected page, profile, community, location, or publishing target is not accessible to the connected account anymore.

**What the user should do:** Ask the user to confirm they still have access to that target on the platform. Then reconnect the account and reselect the page/profile if needed.

***

**Error key:** `media_fetch_failed`

**Platform code(s):** `HTTP:422`

**Message we received:**

```text theme={null}
Unable to fetch media from URL, got status code: 403 Restricted by TBS blocklist
```

**Why this happens:** Facebook could not fetch the hosted media URL. In our data this includes Meta crawler failures such as 403 blocklist or robots-style access blocks.

**What the user should do:** Retry once. If it repeats, escalate so support can verify that Meta's crawler can access the media URL without authentication, redirect, or bot blocking.

***

**Error key:** `account_authorization_revoked`

**Platform code(s):** `Meta:190:458`

**Message we received:**

```text theme={null}
Error validating access token: The user has not authorized application ID.
```

**Why this happens:** The user or the platform removed the app authorization. Our system can still see the account record, but the platform no longer accepts the stored permission.

**What the user should do:** Ask the user to reconnect the social account in bundle.social and approve all requested permissions again. If the account manages a page, they should also reselect the page during reconnect.

***

**Error key:** `posting_rate_limited`

**Platform code(s):** `Meta:368:1390008`

**Message we received:**

```text theme={null}
We limit how often you can post, comment or do other things in a given amount of time in order to help protect the community from spam. You can try again later. Learn More
```

**Why this happens:** The platform limited publishing frequency, the account reached a hourly publishing cap / was marked as spam.

**What the user should do:** Ask the user to wait before retrying. If this happens often, reduce scheduling density for that account.

***

**Error key:** `identity_confirmation_required`

**Platform code(s):** `Meta:368:4854002`

**Message we received:**

```text theme={null}
Confirm your identity before you can publish as this Page. Open the Facebook app on your phone and follow the instructions.
```

**Why this happens:** The platform requires the user to confirm identity before publishing as that page or profile.

**What the user should do:** Ask the user to open the platform mobile app or account quality center and complete identity confirmation. Retry after confirmation is complete.

***

**Error key:** `account_not_confirmed`

**Platform code(s):** `HTTP:401`, `Meta:190:464`

**Message we received:**

```text theme={null}
Error validating access token: Sessions for the user are not allowed because the user is not a confirmed user.
```

**Why this happens:** The platform requires the account to be confirmed before API publishing is allowed. This can mean email confirmation, account verification, or a required platform checkpoint.

**What the user should do:** Ask the user to open the native platform, finish account confirmation, then reconnect the account and retry publishing.

***

**Error key:** `missing_platform_permission`

**Platform code(s):** `HTTP:400`, `Meta:190`, `Meta:200`

**Message we received:**

```text theme={null}
Any of the pages_read_engagement, pages_manage_metadata, pages_read_user_content, pages_manage_ads, pages_show_list or pages_messaging permission(s) must be granted before impersonating a user's page.
```

**Why this happens:** Meta rejected the publish because the current token no longer has effective permission to publish as the selected Page. This often happens when the same Meta user connects multiple bundle.social teams and selects only one Page during each OAuth flow. Meta can overwrite page grants for the Bundle app at the Meta-user level, so one team can still look connected while Meta has removed its Page grant remotely.

**What the user should do:** Ask the user to reconnect the Meta account. In the Facebook OAuth screen, they should select all Pages and Instagram accounts they manage. Then choose the correct Page or Instagram channel inside bundle.social for that team and retry the failed post.

***

**Error key:** `account_security_limited`

**Platform code(s):** `HTTP:400`, `Meta:368:1404112`

**Message we received:**

```text theme={null}
For security reasons, your account has limited access to the site for a few days. If you have any questions, please contact our Help Center.
```

**Why this happens:** The platform temporarily limited the account for security reasons. The request is blocked until the platform removes the temporary limit.

**What the user should do:** Ask the user to log into the platform, review security prompts, and wait until the limitation is lifted. Retry later after the account is back to normal.

***

**Error key:** `platform_login_required`

**Platform code(s):** `HTTP:401`, `Meta:190:459`

**Message we received:**

```text theme={null}
You cannot access the app till you log in to www.facebook.com and follow the instructions given.
```

**Why this happens:** The platform requires the user to log in and complete an account checkpoint before API publishing can continue, just to be sure that this is not a bot but a real person.

**What the user should do:** Ask the user to log into the platform website or mobile app, complete any prompt, then reconnect and retry.

***

**Error key:** `page_role_or_2fa_required`

**Platform code(s):** `Meta:190:492`

**Message we received:**

```text theme={null}
The user must be an administrator, editor, or moderator of the page in order to impersonate it. If the page business requires Two Factor Authentication, the user also needs to enable Two Factor Authentication.
```

**Why this happens:** The platform requires a stronger page role or two-factor authentication before the user can publish as the page.

**What the user should do:** Ask the user to confirm their page role and enable two-factor authentication if their business requires it. Then reconnect and retry.

***

**Error key:** `request_too_large`

**Platform code(s):** `Meta:1`

**Message we received:**

```text theme={null}
Please reduce the amount of data you're asking for, then retry your request
```

**Why this happens:** The platform rejected the request because it contained too much data, such as too much text, metadata, or media information.

**What the user should do:** Ask the user to shorten the post, reduce attached metadata/media, and retry.

***

**Error key:** `temporary_platform_error`

**Platform code(s):** `HTTP:500`, `HTTP:502`, `HTTP:503`, `HTTP:504`, `Meta:2`

**Message we received:**

```text theme={null}
proxygen::coro::HTTPError: HTTP source aborted err=INTERNAL_ERROR, details=received RST_STREAM from peer
```

**Why this happens:** The platform returned a temporary server error or service unavailable response. The request reached the platform, but the platform could not complete it.

**What the user should do:** Ask the user to retry later. If many posts fail across accounts, treat it as a platform incident and escalate internally.

***

**Error key:** `content_policy_restricted`

**Platform code(s):** `Meta:368:1404132`

**Message we received:**

```text theme={null}
You're temporarily blocked from using this feature because you shared something that isn't allowed on Facebook. Learn More.
```

**Why this happens:** The platform rejected or blocked the content because it appears to violate platform rules or automated safety checks.

**What the user should do:** Ask the user to review the content, remove risky text or media, and retry. If the platform account is restricted, they must resolve that directly with the platform.

***

**Error key:** `media_upload_failed`

**Platform code(s):** `Meta:2:1363047`, `Meta:6000:1363048`

**Message we received:**

```text theme={null}
There was a problem while uploading your video.
```

**Why this happens:** The media upload did not complete successfully. This can be caused by platform upload processing, invalid media, expired upload sessions, or transient platform errors.

**What the user should do:** Ask the user to retry. If it repeats, ask them to replace or re-export the media file and try again.

***

**Error key:** `unknown_error`

**Platform code(s):** `HTTP:404`, `HTTP:500`, `Meta:1`, `Meta:100`, `Meta:100:1366046`, `Meta:1:99`, `NET:ECONNABORTED`

**Message we received:**

```text theme={null}
Unknown error
```

**Why this happens:** The platform did not return a specific reason. Our system only received a generic or empty error.

**What the user should do:** Ask the user to retry once. If it repeats, escalate with the failed post ID, platform, and timestamp so support can inspect the raw platform response.

***

**Error key:** `media_processing_failed`

**Platform code(s):** `HTTP:400`, `Meta:324:2069019`

**Message we received:**

```text theme={null}
Request processing failed
```

**Why this happens:** The platform accepted the upload but could not process the media. Common reasons include unsupported format, corrupt file, too large media, or platform processing failure.

**What the user should do:** Ask the user to re-export the media in a standard format and retry. For images, use common JPG/PNG. For videos, use MP4/H.264 when possible.

***

**Error key:** `media_processing_timeout`

**Platform code(s):** `HTTP:502`

**Message we received:**

```text theme={null}
Video publish timed out
```

**Why this happens:** The platform did not finish processing the media within the expected time.

**What the user should do:** Ask the user to retry later or upload a smaller/simpler media file. If many users see this at once, treat it as a platform issue.

***

**Error key:** `media_owner_mismatch`

**Platform code(s):** `HTTP:403`

**Message we received:**

```text theme={null}
"success":false,"message":"Supplied user is not the creator of this video ID";
```

**Why this happens:** The platform says the connected account is not the owner or creator of the media being published.

**What the user should do:** Ask the user to publish from the account that owns the media or re-upload the media under the correct connected account.

***

**Error key:** `action_temporarily_blocked`

**Platform code(s):** `Meta:368:1404078`

**Message we received:**

```text theme={null}
You have been temporarily blocked from performing this action.
```

**Why this happens:** The platform temporarily blocked the action, commonly because of anti-spam, automation, or policy checks.

**What the user should do:** Ask the user to review the post content and account status, wait, then try again. If many posts failed, slow down publishing from that account.

***

**Error key:** `network_error`

**Platform code(s):** `NET:EAI_AGAIN`, `NET:ECONNRESET`

**Message we received:**

```text theme={null}
aborted
```

**Why this happens:** A network or DNS error interrupted the request between our system, media storage, and the platform.

**What the user should do:** Ask the user to retry. If multiple retries fail or many accounts are affected, escalate to support as an infrastructure/platform connectivity issue.

### Instagram

**Error key:** `account_not_confirmed`

**Platform code(s):** `Meta:190`

**Message we received:**

```text theme={null}
Error validating access token: Sessions for the user are not allowed because the user is not a confirmed user.
```

**Why this happens:** The platform requires the account to be confirmed before API publishing is allowed. This can mean email confirmation, account verification, or a required platform checkpoint.

**What the user should do:** Ask the user to open the native platform, finish account confirmation, then reconnect the account and retry publishing.

***

**Error key:** `account_connection_expired`

**Platform code(s):** `Meta:190`, `Meta:190:460`

**Message we received:**

```text theme={null}
Error validating access token: The session has been invalidated because the user changed their password or Facebook has changed the session for security reasons.
```

**Why this happens:** The access token or session used for publishing is no longer valid. This commonly happens after password changes, security checks, expired OAuth sessions, or token revocation.

**What the user should do:** Ask the user to reconnect the platform account. After reconnecting, retry the post. If it fails again immediately, ask them to log into the native platform first and clear any security prompt.

***

**Error key:** `unknown_error`

**Platform code(s):** `UNKNOWN`

**Message we received:**

```text theme={null}
Unknown error
```

**Why this happens:** The platform did not return a specific reason. Our system only received a generic or empty error.

**What the user should do:** Ask the user to retry once. If it repeats, escalate with the failed post ID, platform, and timestamp so support can inspect the raw platform response.

***

**Error key:** `posting_rate_limited`

**Platform code(s):** `Meta:9:2207042`

**Message we received:**

```text theme={null}
Du hast die maximal zulässige Anzahl an durch die Content Publishing API veröffentlichten Beiträgen erreicht.
```

**Why this happens:** Meta is a weird platform sometimes they return messages in diffrent languages. The platform limited publishing frequency, the account reached a hourly publishing cap / was marked as spam.

**What the user should do:** Ask the user to wait before retrying. If this happens often, reduce scheduling density for that account.

***

**Error key:** `missing_platform_permission`

**Platform code(s):** `HTTP:400`, `Meta:10`, `Meta:190`, `Meta:200`

**Message we received:**

```text theme={null}
Any of the pages_read_engagement, pages_manage_metadata, pages_read_user_content, pages_manage_ads, pages_show_list or pages_messaging permission(s) must be granted before impersonating a user's page.
```

**Why this happens:** Meta rejected the publish because the current token no longer has effective permission to publish as the selected Page linked to the Instagram account. This often happens when the same Meta user connects multiple bundle.social teams and selects only one Page or Instagram account during each OAuth flow. Meta can overwrite page grants for the Bundle app at the Meta-user level, so one team can still look connected while Meta has removed its Page grant remotely.

**What the user should do:** Ask the user to reconnect the Meta account. In the Facebook OAuth screen, they should select all Pages and Instagram accounts they manage. Then choose the correct Page or Instagram channel inside bundle.social for that team and retry the failed post.

***

**Error key:** `action_temporarily_blocked`

**Platform code(s):** `Meta:4:2207051`

**Message we received:**

```text theme={null}
Wir schränken bestimmte Handlungen ein, um unsere Community zu schützen. Sag uns, wenn wir deiner Meinung nach einen Fehler gemacht haben.
```

**Why this happens:** The platform temporarily blocked the action, commonly because of anti-spam, automation, or policy checks.

**What the user should do:** Ask the user to review the post content and account status, wait, then try again. If many posts failed, slow down publishing from that account.

***

**Error key:** `account_restricted`

**Platform code(s):** `Meta:25:2207050`

**Message we received:**

```text theme={null}
The Instagram account is restricted.
```

**Why this happens:** The platform has restricted the account from publishing or uploading media. This restriction is enforced by the platform and is outside our direct control.

**What the user should do:** Ask the user to open the platform account and check account status, account quality, or support inbox. They need to resolve the restriction on the platform before retrying.

***

**Error key:** `media_fetch_failed`

**Platform code(s):** `Meta:9004:2207052`

**Message we received:**

```text theme={null}
Die Mediendatei konnte nicht von dieser URI abgerufen werden: URL Informationen findest du im Abschnitt „Einschränkungen“ in unserer Entwicklerdokumentation: URL
```

**Why this happens:** Instagram could not download the media from the hosted URL. This often happens when Meta's crawler cannot access the file or the URL violates Instagram media-fetch limitations.

**What the user should do:** Retry once. If it repeats, escalate so support can verify public HTTPS access, headers, redirects, file availability, and Meta crawler access.

***

**Error key:** `account_authorization_revoked`

**Platform code(s):** `Meta:190`, `Meta:190:458`

**Message we received:**

```text theme={null}
Error validating access token: The user has not authorized application ID.
```

**Why this happens:** The user or the platform removed the app authorization. Our system can still see the account record, but the platform no longer accepts the stored permission.

**What the user should do:** Ask the user to reconnect the social account in bundle.social and approve all requested permissions again. If the account manages a page, they should also reselect the page during reconnect.

***

**Error key:** `video_should_be_reel`

**Platform code(s):** `Meta:100:2207089`

**Message we received:**

```text theme={null}
Media created with media_type=VIDEO is a carousel item and cannot be published as a standalone post. To publish a standalone video, use media_type=REELS instead.
```

**Why this happens:** Instagram rejected the video because this media type must be published as a Reel instead of a standard standalone video post.

**What the user should do:** Ask the user to switch the publish type to Reel and retry.

***

**Error key:** `media_upload_failed`

**Platform code(s):** `HTTP:502`, `Meta:-1:2207032`

**Message we received:**

```text theme={null}
Media upload failed, Instagram did not returned status about your upload
```

**Why this happens:** The media upload did not complete successfully. This can be caused by platform upload processing, invalid media, expired upload sessions, or transient platform errors.

**What the user should do:** Ask the user to retry. If it repeats, ask them to replace or re-export the media file and try again.

***

**Error key:** `platform_login_required`

**Platform code(s):** `Meta:190:459`

**Message we received:**

```text theme={null}
You cannot access the app till you log in to www.facebook.com and follow the instructions given.
```

**Why this happens:** The platform requires the user to log in and complete an account checkpoint before API publishing can continue, just to be sure that this is not a bot but a real person.

**What the user should do:** Ask the user to log into the platform website or mobile app, complete any prompt, then reconnect and retry.

***

**Error key:** `page_or_target_inaccessible`

**Platform code(s):** `Meta:100:33`, `Meta:190`

**Message we received:**

```text theme={null}
This Page access token belongs to a Page that is not accessible.
```

**Why this happens:** The selected page, profile, community, location, or publishing target is not accessible to the connected account anymore.

**What the user should do:** Ask the user to confirm they still have access to that target on the platform. Then reconnect the account and reselect the page/profile if needed.

***

**Error key:** `tagged_user_inaccessible`

**Platform code(s):** `Meta:110:2207018`

**Message we received:**

```text theme={null}
Отсутствует доступ к следующим пользователям: erikwist04
```

**Why this happens:** The platform could not access one or more tagged users. The tagged account may be private, invalid, blocked, or not eligible for tagging.

**What the user should do:** Ask the user to remove or change the tagged users and retry.

***

**Error key:** `media_fetch_timeout`

**Platform code(s):** `Meta:-2:2207003`

**Message we received:**

```text theme={null}
Das Herunterladen der Medien dauert zu lange.
```

**Why this happens:** The platform took too long to download the media file.

**What the user should do:** Ask the user to retry later or use a smaller media file. Escalate if the same media repeatedly times out.

***

**Error key:** `temporary_platform_error`

**Platform code(s):** `Meta:2`

**Message we received:**

```text theme={null}
An unexpected error has occurred. Please retry your request later.
```

**Why this happens:** The platform returned a temporary server error or service unavailable response. The request reached the platform, but the platform could not complete it.

**What the user should do:** Ask the user to retry later. If many posts fail across accounts, treat it as a platform incident and escalate internally.

***

**Error key:** `network_error`

**Platform code(s):** `NET:EAI_AGAIN`, `NET:ECONNRESET`

**Message we received:**

```text theme={null}
getaddrinfo EAI_AGAIN graph.facebook.com
```

**Why this happens:** A network or DNS error interrupted the request between our system, media storage, and the platform.

**What the user should do:** Ask the user to retry. If multiple retries fail or many accounts are affected, escalate to support as an infrastructure/platform connectivity issue.

***

**Error key:** `tagged_user_not_allowed`

**Platform code(s):** `Meta:210:2207066`

**Message we received:**

```text theme={null}
The user <some_user_name> cannot be tagged on this media.
```

**Why this happens:** The platform says one of the selected users cannot be tagged on this media.

**What the user should do:** Ask the user to remove that tag and retry.

***

**Error key:** `invalid_location`

**Platform code(s):** `Meta:100`

**Message we received:**

```text theme={null}
Param location_id is not a valid location page ID
```

**Why this happens:** The selected location is not valid for the platform endpoint or cannot be used with this post.

**What the user should do:** Ask the user to remove the location or choose another valid location, then retry.

***

**Error key:** `too_few_followers_for_feature`

**Platform code(s):** `Meta:10:2207081`

**Message we received:**

```text theme={null}
Dieses Instagram-Konto hat zu wenige Follower, um Test-Reels erstellen zu können.
```

**Why this happens:** The account does not meet the platform requirements for this publishing feature. Likley a TRAIL reels.

**What the user should do:** Ask the user to use another publish type or wait until the account meets the platform eligibility requirements.

***

**Error key:** `too_many_tags`

**Platform code(s):** `Meta:100:2207040`

**Message we received:**

```text theme={null}
Es dürfen nicht mehr als 30 Tags pro Medienerstellung verwendet werden.
```

**Why this happens:** The platform rejected the post because it contains too many tags.

**What the user should do:** Ask the user to reduce the number of tags and retry.

### TikTok

**Error key:** `unknown_error`

**Platform code(s):** -

**Message we received:**

```text theme={null}
Unknown error
```

**Why this happens:** The platform did not return a specific reason. Our system only received a generic or empty error.

**What the user should do:** Ask the user to retry once. If it repeats, escalate with the failed post ID, platform, and timestamp so support can inspect the raw platform response.

***

**Error key:** `account_connection_expired`

**Platform code(s):** `HTTP:422`, `HTTP:502`

**Message we received:**

```text theme={null}
Access token is incorrect or has been revoked.
```

**Why this happens:** The access token or session used for publishing is no longer valid. This commonly happens after password changes, security checks, expired OAuth sessions, token revocation or just "because".

**What the user should do:** Ask the user to reconnect the platform account. After reconnecting, retry the post. If it fails again immediately, ask them to log into the native platform first and clear any security prompt.

***

**Error key:** `media_processing_timeout`

**Platform code(s):** `HTTP:504`

**Message we received:**

```text theme={null}
Media upload failed, TikTok did not process your upload in time
```

**Why this happens:** In around 50% of cases, the user posted the TikTok as private, so we could not retrieve the post ID. In around 25% of cases, TikTok is slow or overloaded. In the remaining cases, the content was too large and the platform did not finish processing the media within the expected time.

**What the user should do:** Check privacy settings, try again in a bit or upload a smaller media file. If many users see this at once, treat it as a platform issue.

***

**Error key:** `unsupported_file_format`

**Platform code(s):** `HTTP:422`

**Message we received:**

```text theme={null}
Media upload failed with reason: file_format_check_failed
```

**Why this happens:** The platform rejected the media because the file format, codec, or dimensions are not supported. If the media is an image, avoid PNG and make sure it is not larger than Full HD in either dimension. We also provide a resize option in the post fields if the media needs to be adjusted automatically.

**What the user should do:** Convert the media to a supported format and retry. For videos, MP4 with H.264 is usually the safest option. For images, use JPG/JPEG and keep the resolution within platform limits.

***

**Error key:** `posting_rate_limited`

**Platform code(s):** `HTTP:502`

**Message we received:**

```text theme={null}
This TikTok creator has made too many posts via OpenAPI in the last 24 hours, so this publishing attempt is blocked to minimize spam. The user can try again later or publish it in the mobile app instead.
```

**Why this happens:** The platform limited publishing frequency or the account reached a daily publishing cap of 15.

**What the user should do:** Ask the user to wait 24h before retrying.

***

**Error key:** `content_policy_restricted`

**Platform code(s):** `HTTP:422`

**Message we received:**

```text theme={null}
Media upload failed with reason: spam_risk
```

**Why this happens:** The platform rejected or blocked the content because it appears to violate platform rules or automated safety checks.

**What the user should do:** Ask the user to review the content, remove risky text or media, and retry. If the platform account is restricted, they must resolve that directly with the platform.

***

**Error key:** `image_size_invalid`

**Platform code(s):** `HTTP:422`

**Message we received:**

```text theme={null}
Media upload failed with reason: picture_size_check_failed
```

**Why this happens:** The uploaded image does not match the platform’s image size, dimension, or resolution requirements. The safest option is JPG/JPEG with a maximum resolution of Full HD.

**What the user should do:** Ask the user to resize or replace the image according to the platform requirements, then retry.

***

**Error key:** `temporary_platform_error`

**Platform code(s):** `HTTP:502`, `HTTP:503`, `HTTP:504`

**Message we received:**

```text theme={null}
Something went wrong. Please try again later.
```

**Why this happens:** The platform returned a temporary server error or service unavailable response. The request reached the platform, but the platform could not complete it.

**What the user should do:** Ask the user to retry later. If many posts fail across accounts, treat it as a platform incident and escalate internally.

***

**Error key:** `account_restricted`

**Platform code(s):** `HTTP:422`

**Message we received:**

```text theme={null}
Media upload failed with reason: spam_risk_user_banned_from_posting
```

**Why this happens:** The platform has restricted the account from publishing or uploading media. This restriction is enforced by the platform and is outside our direct control.

**What the user should do:** Ask the user to open the platform account and check account status, account quality, or support inbox. They need to resolve the restriction on the platform before retrying.

***

**Error key:** `video_frame_rate_invalid`

**Platform code(s):** `HTTP:422`

**Message we received:**

```text theme={null}
Media upload failed with reason: frame_rate_check_failed
```

**Why this happens:** The video frame rate does not match the platform requirements.

**What the user should do:** Ask the user to re-export the video with a supported frame rate and retry.

***

**Error key:** `invalid_request_parameters`

**Platform code(s):** `HTTP:403`, `HTTP:502`, `TT:50001`

**Message we received:**

```text theme={null}
missing or invalid request id
```

**Why this happens:** The platform rejected a request parameter. This can happen when a value is malformed, expired, or no longer accepted by the platform.

**What the user should do:** Ask the user to retry after refreshing the post setup. If it repeats, escalate because engineering may need to inspect the exact request values.

***

**Error key:** `network_error`

**Platform code(s):** `HTTP:502`, `NET:EAI_AGAIN`, `NET:ECONNRESET`

**Message we received:**

```text theme={null}
read ECONNRESET
```

**Why this happens:** A network or DNS error interrupted the request between our system, media storage, and the platform.

**What the user should do:** Ask the user to retry. If multiple retries fail or many accounts are affected, escalate to support as an infrastructure/platform connectivity issue.

***

**Error key:** `media_fetch_failed`

**Platform code(s):** `HTTP:422`, `HTTP:502`

**Message we received:**

```text theme={null}
Media upload failed with reason: photo_pull_failed
```

**Why this happens:** The platform could not download the media from our hosted URL. This usually means the platform crawler was blocked, received 403, or could not access the media in time.

**What the user should do:** Retry the post first. If it repeats, escalate to support so we can check media URL accessibility, storage headers, robots/bot blocking, and platform crawler access.

***

**Error key:** `media_upload_failed`

**Platform code(s):** `HTTP:422`

**Message we received:**

```text theme={null}
Media upload failed with reason: internal
```

**Why this happens:** The media upload did not complete successfully. This can be caused by platform upload processing, invalid media, expired upload sessions, or transient platform errors.

**What the user should do:** Ask the user to retry. If it repeats, ask them to replace or re-export the media file and try again. If you see this a lot it's a platform wide issue.

***

**Error key:** `media_url_verification_failed`

**Platform code(s):** `HTTP:502`

**Message we received:**

```text theme={null}
Please review our URL ownership verification rules at URL
```

**Why this happens:** The platform requires the media URL or domain to be verified before it can pull media from that URL.

**What the user should do:** Escalate to support. This is usually an integration or domain verification issue, not something the end user can fix directly.

### YouTube

**Error key:** `account_suspended`

**Platform code(s):** `YT:authenticatedUserAccountSuspended`

**Message we received:**

```text theme={null}
The YouTube account of the authenticated user is suspended. In case the authenticated user is acting on behalf of another Google account, then this error refers to the latter.
```

**Why this happens:** The platform reports that the account or channel is suspended. Suspended accounts cannot publish through the API.

**What the user should do:** Ask the user to resolve the suspension directly with the platform. Publishing can resume only after the platform restores the account.

***

**Error key:** `youtube_upload_limit_reached`

**Platform code(s):** `YT:uploadLimitExceeded`

**Message we received:**

```text theme={null}
The user has exceeded the number of videos they may upload.
```

**Why this happens:** YouTube rejected the upload because the channel exceeded its current upload allowance. YouTube documents daily upload limits and API upload limits for safety.

**What the user should do:** Ask the user to wait until the upload limit resets, usually up to 24 hours, then retry.

***

**Error key:** `unknown_error`

**Platform code(s):** -

**Message we received:**

```text theme={null}
Unknown error
```

**Why this happens:** The platform did not return a specific reason. Our system only received a generic or empty error.

**What the user should do:** Ask the user to retry once. If it repeats, escalate with the failed post ID, platform, and timestamp so support can inspect the raw platform response.

***

**Error key:** `youtube_account_service_forbidden`

**Platform code(s):** `YT:forbidden`, `YT:unsupportedSupervisedAccount`

**Message we received:**

```text theme={null}
Access Forbidden. The authenticated user cannot access this service.
```

**Why this happens:** YouTube says this authenticated account cannot access the upload service. This can happen for supervised, restricted, or ineligible accounts.

**What the user should do:** Ask the user to check YouTube account settings or use an eligible YouTube channel. Reconnect after the account is eligible.

***

**Error key:** `account_connection_expired`

**Platform code(s):** `YT:authError`

**Message we received:**

```text theme={null}
Request had invalid authentication credentials. Expected OAuth 2 access token, login cookie or other valid authentication credential. See URL
```

**Why this happens:** The access token or session used for publishing is no longer valid. This commonly happens after password changes, security checks, expired OAuth sessions, token revocation or just "because".

**What the user should do:** Ask the user to reconnect the platform account. After reconnecting, retry the post. If it fails again immediately, ask them to log into the native platform first and clear any security prompt.

***

**Error key:** `youtube_signup_required`

**Platform code(s):** `YT:youtubeSignupRequired`

**Message we received:**

```text theme={null}
Unauthorized
```

**Why this happens:** The Google account is not fully set up as a YouTube channel for uploads.

**What the user should do:** Ask the user to complete YouTube channel setup, then reconnect YouTube and retry.

***

**Error key:** `invalid_video_title`

**Platform code(s):** `YT:invalidTitle`

**Message we received:**

```text theme={null}
The request metadata specifies an invalid or empty video title.
```

**Why this happens:** YouTube rejected the upload because the title is missing or invalid.

**What the user should do:** Ask the user to add a valid title and retry. Avoid empty titles or unsupported characters.

### LinkedIn

**Error key:** `account_restricted`

**Platform code(s):** `HTTP:401`

**Message we received:**

```text theme={null}
Member is restricted
```

**Why this happens:** The platform has restricted the account from publishing or uploading media. This restriction is enforced by the platform and is outside our direct control.

**What the user should do:** Ask the user to open the platform account and check account status, account quality, or support inbox. They need to resolve the restriction on the platform before retrying.

***

**Error key:** `missing_platform_permission`

**Platform code(s):** `HTTP:403`

**Message we received:**

```text theme={null}
Accessing this image resource is forbidden. Please check your permissions for this resource
```

**Why this happens:** LinkedIn rejected access to the image or video resource. LinkedIn requires the token and owner to match the member/page/organization that owns the media.

**What the user should do:** Ask the user to reconnect LinkedIn and confirm they are publishing to a page or profile they administer. If the media was uploaded under another owner, upload it again under the correct account.

***

**Error key:** `temporary_platform_error`

**Platform code(s):** `HTTP:500`, `HTTP:503`, `HTTP:524`

**Message we received:**

```text theme={null}
[IncomingMessage]
```

**Why this happens:** The platform returned a temporary server error or service unavailable response. The request reached the platform, but the platform could not complete it.

**What the user should do:** Ask the user to retry later. If many posts fail across accounts, treat it as a platform incident and escalate internally.

***

**Error key:** `account_authorization_revoked`

**Platform code(s):** `HTTP:401`

**Message we received:**

```text theme={null}
The token used in the request has been revoked by the user
```

**Why this happens:** The user or the platform removed the app authorization. Our system can still see the account record, but the platform no longer accepts the stored permission.

**What the user should do:** Ask the user to reconnect the social account in bundle.social and approve all requested permissions again. If the account manages a page, they should also reselect the page during reconnect.

***

**Error key:** `network_error`

**Platform code(s):** `HTTP:502`, `NET:EAI_AGAIN`, `NET:ECONNRESET`

**Message we received:**

```text theme={null}
connect ETIMEDOUT 108.174.10.22:443
```

**Why this happens:** A network or DNS error interrupted the request between our system, media storage, and the platform.

**What the user should do:** Ask the user to retry. If multiple retries fail or many accounts are affected, escalate to support as an infrastructure/platform connectivity issue.

***

**Error key:** `duplicate_content`

**Platform code(s):** `LI:422`

**Message we received:**

```text theme={null}
com.linkedin.content.common.exception.BadRequestResponseException: Content is a duplicate of URN
```

**Why this happens:** The platform detected that the post duplicates content that was already published or recently submitted.

**What the user should do:** Ask the user to change the text or media meaningfully, then publish again.

***

**Error key:** `media_processing_failed`

**Platform code(s):** `HTTP:422`

**Message we received:**

```text theme={null}
LinkedIn processing failed for image
```

**Why this happens:** The platform accepted the upload but could not process the media. Common reasons include unsupported format, corrupt file, too large media, or platform processing failure.

**What the user should do:** Ask the user to re-export the media in a standard format and retry. For images, use common JPG/PNG. For videos, use MP4/H.264 when possible.

***

**Error key:** `media_processing_timeout`

**Platform code(s):** `HTTP:504`

**Message we received:**

```text theme={null}
No final status after 6 attempts
```

**Why this happens:** The platform did not finish processing the media within the expected time.

**What the user should do:** Ask the user to retry later or upload a smaller/simpler media file. If many users see this at once, treat it as a platform issue.

### X / Twitter

**Error key:** `action_not_permitted`

**Platform code(s):** `HTTP:403`, `TW:403`

**Message we received:**

```text theme={null}
You are not permitted to perform this action.
```

**Why this happens:** The platform does not allow the connected account to perform this action. This can be caused by account type, role, missing permission, or platform-side restriction.

**What the user should do:** Ask the user to confirm they are using the correct account, page, and role. If the action is still blocked, reconnect the account and retry with a simpler post.

***

**Error key:** `account_suspended`

**Platform code(s):** `HTTP:403`, `TW:user-suspended`

**Message we received:**

```text theme={null}
Request failed with code 403 - Your account is suspended and is not permitted to access this feature. (Twitter code 64)
```

**Why this happens:** The platform reports that the account or channel is suspended. Suspended accounts cannot publish through the API.

**What the user should do:** Ask the user to resolve the suspension directly with the platform. Publishing can resume only after the platform restores the account.

***

**Error key:** `account_temporarily_locked`

**Platform code(s):** `HTTP:403`, `HTTP:502`, `TW:403`

**Message we received:**

```text theme={null}
Your account is temporarily locked. Please log in to URL to unlock your account.
```

**Why this happens:** The platform temporarily locked the account, usually due to security or anti-spam checks.

**What the user should do:** Ask the user to log into the native platform and complete the unlock flow. After the account is unlocked, reconnect if needed and retry.

***

**Error key:** `temporary_platform_error`

**Platform code(s):** `HTTP:500`, `HTTP:503`, `HTTP:520`, `HTTP:522`, `NET:503`, `TW:503`

**Message we received:**

```text theme={null}
Request failed with code 503
```

**Why this happens:** X/Twitter returned a temporary server or media-service error. This is usually not caused by the post content.

**What the user should do:** Ask the user to retry later. If media upload status remains stuck or many accounts fail, escalate as a platform/media upload issue.

***

**Error key:** `account_connection_expired`

**Platform code(s):** `HTTP:401`, `TW:401`

**Message we received:**

```text theme={null}
Request failed with code 401 - Invalid or expired token (Twitter code 89)
```

**Why this happens:** The access token or session used for publishing is no longer valid. This commonly happens after password changes, security checks, expired OAuth sessions, token revocation or just "because".

**What the user should do:** Ask the user to reconnect the platform account. After reconnecting, retry the post. If it fails again immediately, ask them to log into the native platform first and clear any security prompt.

***

**Error key:** `duplicate_content`

**Platform code(s):** `TW:403`

**Message we received:**

```text theme={null}
You are not allowed to create a Tweet with duplicate content.
```

**Why this happens:** The platform detected that the post duplicates content that was already published or recently submitted.

**What the user should do:** Ask the user to change the text or media meaningfully, then publish again.

***

**Error key:** `video_duration_too_long`

**Platform code(s):** `TW:403`

**Message we received:**

```text theme={null}
This user is not allowed to post a video longer than 2 minutes.
```

**Why this happens:** The video is longer than the platform or account allows.

**What the user should do:** Ask the user to shorten the video or publish it directly on the platform if that account supports longer videos there.

***

**Error key:** `crypto_address_restriction`

**Platform code(s):** `TW:403`

**Message we received:**

```text theme={null}
Crypto addresses are prohibited for the first 7 days after authentication.
```

**Why this happens:** X/Twitter restricts crypto addresses for newly authenticated accounts during an initial safety period.

**What the user should do:** Ask the user to remove the crypto address from the post or wait until the platform restriction period ends.

***

**Error key:** `access_package_limitation`

**Platform code(s):** `TW:403`

**Message we received:**

```text theme={null}
Creating posts with @mentions is not allowed for your access package. In replies to conversations you are part of, you may only @mention users who are already participants in the thread.
```

**Why this happens:** The connected account or API access level does not allow this publishing feature. In the observed X/Twitter case, posts with certain @mentions are blocked by the current access package.

**What the user should do:** Ask the user to remove the restricted feature from the post, such as unsupported @mentions, or confirm that their X API access level supports it. Escalate only if the account should have this access.

***

**Error key:** `invalid_media_reference`

**Platform code(s):** `TW:invalid-request`

**Message we received:**

```text theme={null}
Your media IDs are invalid.
```

**Why this happens:** The platform rejected the media ID or media reference. This usually means the media upload did not finish correctly or the reference expired.

**What the user should do:** Ask the user to upload the media again and retry publishing. If it repeats, escalate with the failed media/post ID.

***

**Error key:** `network_error`

**Platform code(s):** `NET:EAI_AGAIN`, `NET:ECONNRESET`

**Message we received:**

```text theme={null}
aborted
```

**Why this happens:** A network or DNS error interrupted the request between our system, media storage, and the platform.

**What the user should do:** Ask the user to retry. If multiple retries fail or many accounts are affected, escalate to support as an infrastructure/platform connectivity issue.

***

**Error key:** `media_processing_timeout`

**Platform code(s):** `HTTP:504`

**Message we received:**

```text theme={null}
No terminal state after repeated checks
```

**Why this happens:** The platform did not finish processing the media within the expected time.

**What the user should do:** Ask the user to retry later or upload a smaller/simpler media file. If many users see this at once, treat it as a platform issue.

### Threads

**Error key:** `unknown_error`

**Platform code(s):** `Meta:1`

**Message we received:**

```text theme={null}
Unknown error
```

**Why this happens:** The platform did not return a specific reason. Our system only received a generic or empty error.

**What the user should do:** Ask the user to retry once. If it repeats, escalate with the failed post ID, platform, and timestamp so support can inspect the raw platform response.

***

**Error key:** `media_upload_failed`

**Platform code(s):** `HTTP:502`, `Meta:1:2207032`

**Message we received:**

```text theme={null}
Media upload failed, Threads did not returned status about your upload
```

**Why this happens:** The media upload did not complete successfully. This can be caused by platform upload processing, invalid media, expired upload sessions, or transient platform errors.

**What the user should do:** Ask the user to retry. If it repeats, ask them to replace or re-export the media file and try again.

***

**Error key:** `action_temporarily_blocked`

**Platform code(s):** `Meta:1:2207051`

**Message we received:**

```text theme={null}
We restrict certain activity to protect our community. Tell us if you think we made a mistake.
```

**Why this happens:** The platform temporarily blocked the action, commonly because of anti-spam, automation, or policy checks.

**What the user should do:** Ask the user to review the post content and account status, wait, then try again. If many posts failed, slow down publishing from that account.

***

**Error key:** `media_fetch_failed`

**Platform code(s):** `Meta:1:2207052`

**Message we received:**

```text theme={null}
The media could not be fetched from this URI: URL check the limitations section in our development document for more information: URL
```

**Why this happens:** Threads could not fetch the media from the hosted URL. Threads publishing uses Meta infrastructure, so crawler access and media URL availability matter.

**What the user should do:** Retry once. If it repeats, escalate so support can verify that the media URL is reachable by Meta/Threads and is not blocked.

***

**Error key:** `account_restricted`

**Platform code(s):** `Meta:25:4279013`

**Message we received:**

```text theme={null}
Das Instagram- oder Threads-Konto wurde eingeschränkt.
```

**Why this happens:** The platform has restricted the account from publishing or uploading media. This restriction is enforced by the platform and is outside our direct control.

**What the user should do:** Ask the user to open the platform account and check account status, account quality, or support inbox. They need to resolve the restriction on the platform before retrying.

***

**Error key:** `temporary_platform_error`

**Platform code(s):** `Meta:2`

**Message we received:**

```text theme={null}
An unexpected error has occurred. Please retry your request later.
```

**Why this happens:** The platform returned a temporary server error or service unavailable response. The request reached the platform, but the platform could not complete it.

**What the user should do:** Ask the user to retry later. If many posts fail across accounts, treat it as a platform incident and escalate internally.

***

**Error key:** `media_fetch_timeout`

**Platform code(s):** `Meta:1:2207003`

**Message we received:**

```text theme={null}
Das Herunterladen der Medien dauert zu lange.
```

**Why this happens:** The platform took too long to download the media file.

**What the user should do:** Ask the user to retry later or use a smaller media file. Escalate if the same media repeatedly times out.

***

**Error key:** `network_error`

**Platform code(s):** `NET:EAI_AGAIN`

**Message we received:**

```text theme={null}
getaddrinfo EAI_AGAIN graph.threads.net
```

**Why this happens:** A network or DNS error interrupted the request between our system, media storage, and the platform.

**What the user should do:** Ask the user to retry. If multiple retries fail or many accounts are affected, escalate to support as an infrastructure/platform connectivity issue.

### Pinterest

**Error key:** `media_processing_timeout`

**Platform code(s):** `PIN:PIN:UNKNOWN`

**Message we received:**

```text theme={null}
Media upload failed, Pinterest did not return status
```

**Why this happens:** The platform did not finish processing the media within the expected time.

**What the user should do:** Ask the user to retry later or upload a smaller/simpler media file. If many users see this at once, treat it as a platform issue.

***

**Error key:** `temporary_platform_error`

**Platform code(s):** `PIN:12`, `PIN:2787`

**Message we received:**

```text theme={null}
Something went wrong on our end. Sorry about that.
```

**Why this happens:** The platform returned a temporary server error or service unavailable response. The request reached the platform, but the platform could not complete it.

**What the user should do:** Ask the user to retry later. If many posts fail across accounts, treat it as a platform incident and escalate internally.

***

**Error key:** `account_connection_expired`

**Platform code(s):** `PIN:2`

**Message we received:**

```text theme={null}
Authentication failed.
```

**Why this happens:** Pinterest rejected authentication. Pinterest documents common token issues such as expired/invalid token, expired user session, or insufficient scopes.

**What the user should do:** Ask the user to reconnect Pinterest and grant the required scopes, then retry.

***

**Error key:** `board_name_exists`

**Platform code(s):** `PIN:58`

**Message we received:**

```text theme={null}
Try a different name. You already have a board with this name!
```

**Why this happens:** Pinterest rejected the request because the account already has a board with the same name.

**What the user should do:** Ask the user to choose a different board name or select the existing board instead of creating a new one.

***

**Error key:** `media_fetch_failed`

**Platform code(s):** `PIN:2786`

**Message we received:**

```text theme={null}
Unable to reach the URL. Please check the URL is correct and try again.
```

**Why this happens:** The platform could not download the media from our hosted URL. This usually means the platform crawler was blocked, received 403, or could not access the media in time.

**What the user should do:** Retry the post first. If it repeats, escalate to support so we can check media URL accessibility, storage headers, robots/bot blocking, and platform crawler access.

***

**Error key:** `network_error`

**Platform code(s):** `NET:EAI_AGAIN`

**Message we received:**

```text theme={null}
getaddrinfo EAI_AGAIN private-storage.bundle.social
```

**Why this happens:** A network or DNS error interrupted the request between our system, media storage, and the platform.

**What the user should do:** Ask the user to retry. If multiple retries fail or many accounts are affected, escalate to support as an infrastructure/platform connectivity issue.

### Reddit

**Error key:** `community_does_not_allow_images`

**Platform code(s):** `RD:RD:NO_IMAGES`

**Message we received:**

```text theme={null}
This community doesn't allow images
```

**Why this happens:** The selected Reddit community does not allow image posts.

**What the user should do:** Ask the user to publish without an image or choose another community that allows images.

***

**Error key:** `post_flair_required`

**Platform code(s):** `RD:RD:SUBMIT_VALIDATION_FLAIR_REQUIRED`

**Message we received:**

```text theme={null}
Your post must contain post flair.
```

**Why this happens:** The selected Reddit community requires post flair.

**What the user should do:** Ask the user to choose a flair for the post or select another community.

***

**Error key:** `post_title_required`

**Platform code(s):** `RD:RD:NO_TEXT`

**Message we received:**

```text theme={null}
Post title is required
```

**Why this happens:** The platform requires a title for this post.

**What the user should do:** Ask the user to add a post title and retry.

***

**Error key:** `trusted_members_only`

**Platform code(s):** `RD:RD:SUBREDDIT_NOTALLOWED`

**Message we received:**

```text theme={null}
This community only allows trusted members to post here
```

**Why this happens:** The selected Reddit community only allows trusted members to post.

**What the user should do:** Ask the user to choose another community or request posting access from that community's moderators.

### Bluesky

**Error key:** `media_file_too_large`

**Platform code(s):** `BSKY:400`, `BSKY:502`

**Message we received:**

```text theme={null}
This file is too large. It is SIZE but the maximum size is SIZE.
```

**Why this happens:** Bluesky rejected the media because it exceeded a file-size limit. Bluesky applies upload size limits at the PDS/video service level and may also have application-specific media limits.

**What the user should do:** Ask the user to compress the media or upload a smaller file, then retry. 1 Mb max.

***

**Error key:** `media_upload_failed`

**Platform code(s):** `BSKY:502`

**Message we received:**

```text theme={null}
video.uploadVideo failed: http_401
```

**Why this happens:** The media upload did not complete successfully. This can be caused by platform upload processing, invalid media, expired upload sessions, or transient platform errors.

**What the user should do:** Ask the user to retry. If it repeats, ask them to replace or re-export the media file and try again.

***

**Error key:** `internal_error`

**Platform code(s):** `BSKY:UNKNOWN`

**Message we received:**

```text theme={null}
Cannot read properties of null (reading 'substring')
```

**Why this happens:** A technical error happened while preparing or sending the request. The platform did not provide a user-fixable reason.

**What the user should do:** Ask the user to retry once. If it repeats with the same post, escalate to support with the failed post ID and platform.

### Google Business

**Error key:** `invalid_request_arguments`

**Platform code(s):** `GB:INVALID_ARGUMENT`

**Message we received:**

```text theme={null}
Request contains an invalid argument.
```

**Why this happens:** The platform rejected one or more post settings as invalid. This is usually a validation problem with the post payload, media, or selected account/location.

**What the user should do:** Review the post settings first. Ask the user to simplify the post, remove optional settings, or retry with valid media and account selections.

### Mastodon

**Error key:** `temporary_platform_error`

**Platform code(s):** `MST:503`

**Message we received:**

```text theme={null}
This page is not correct - Mastodon We're sorry, but something went wrong on our end. You can check our status page to have more informations about our maintenances or incidents.
```

**Why this happens:** The platform returned a temporary server error or service unavailable response. The request reached the platform, but the platform could not complete it.

**What the user should do:** Ask the user to retry later. If many posts fail across accounts, treat it as a platform incident and escalate internally.

<Tip>
  This list is also available in CSV format for ease of use. You can download it <a href="/most-common-platform-errors.csv" download="most-common-platform-errors.csv">here</a>.
</Tip>

<Info>
  If you see a weird error code that is not here let us now.
</Info>


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.
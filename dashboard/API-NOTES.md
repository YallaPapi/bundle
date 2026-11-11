# Verified Bundle contracts — 2026-10-25

Sources read before implementation (full pages and live schema saved in `api-docs-review/analytics-options-2026-10-25/`):

- https://info.bundle.social/llms.txt
- https://api.bundle.social/swagger-json
- https://info.bundle.social/api-reference/introduction
- https://info.bundle.social/api-reference/analytics
- https://info.bundle.social/api-reference/platforms/instagram
- https://info.bundle.social/api-reference/client/analytics/get-social-account-analytics
- https://info.bundle.social/api-reference/client/analytics/get-bulk-post-analytics
- https://info.bundle.social/api-reference/client/team/get-list-of-teams
- https://info.bundle.social/api-reference/client/post/get-post-list
- https://info.bundle.social/api-reference/rate-limits
- https://info.bundle.social/api-reference/data-retention
- https://info.bundle.social/api-reference/errors

## Bundle behavior

Authentication is the `x-api-key` header on https://api.bundle.social. The key stays in the project's `.env` and is never delivered to the browser.

GET `/api/v1/team/` and `/api/v1/post/` have `limit`/`offset` pagination with `items` and `total`. Posts require `teamId`. Social-account IDs and platform post associations identify the destination; team names are not assumed to equal usernames.

GET `/api/v1/analytics/social-account` requires `teamId` and `platformType=INSTAGRAM`. It returns `socialAccount` and historical `items`; the live schema does not document date filters or pagination. Snapshot IDs, createdAt, updatedAt, followers and following are supplied. Profile views are profile visits and profile engagement uses a rolling 30-day window.

GET `/api/v1/analytics/post/bulk` requires `postIds` (1–60 IDs) and `platformType`. `page` starts at 1, `limit` defaults to and cannot exceed 20. Results contain postId, items and an individual error; pagination has totalPages. IDs can span teams (verified live with two posts). Each snapshot's views is cumulative video plays, not exact calendar-day plays.

Analytics require a paid plan, refresh automatically about every 24 hours, and snapshots are retained for 30 days. Missing snapshots are possible, including unavailable Instagram insights. Force refresh has separate quotas and is not used. Standard API throttling applies per endpoint (100/sec, 500/10sec, 2000/min); bounded concurrency and GET-only transient recovery stay well below these rates. Authentication failures are not retried as transient.

Live samples returned six days of profile history and multiple post snapshots. Raw profile analytics returned no rows, so raw exact daily view reporting is not assumed. Deletion of teams/accounts remains explicitly prohibited by the user's latest instruction.

## Application behavior

Collect all currently listed Instagram accounts and their published-post snapshots; keep errors and previous cached values for unavailable sources. Save each stable snapshot ID once, updating its values when Bundle updates it. Fetch retained histories after downtime to catch up; data Bundle never collected or already expired cannot be recovered.

Use Asia/Bangkok to label dates. Followers use the latest snapshot per account/day. Net follower change compares the same account on consecutive dates. Estimated video-view gains compare successive daily lifetime snapshots with nonnegative changes and a maximum 36-hour observation gap; missing baselines and larger gaps stay unknown. A first observation on the actual publication date can use zero at publication as baseline. Coverage reports how many eligible posts contributed; profile visits are never substituted for video plays.

Account daily summaries remain indefinitely, detailed post snapshots retain 90 days plus one older baseline per post. Missing days remain gaps. Retained old summaries are not overwritten during pruning. Normal sync is due after 24 hours; partial sync retries after an hour, with bounded GET retries per endpoint and no Bundle writes. A local SQLite lease prevents duplicate simultaneous jobs.

## Profile editing check

Current OpenAPI has no documented Instagram bio/link/username editing operation. POST `/api/v1/social-account/profile-refresh` pulls platform changes into Bundle; it does not write those changes to Instagram. Source: https://info.bundle.social/api-reference/client/socialaccount/manually-refresh-social-account-profile-info . No profile edits are implemented.

## Expanded metrics — rechecked 2026-10-26 before implementation

Current source pages/schema are saved in `api-docs-review/analytics-options-2026-10-26/`:

- https://info.bundle.social/llms.txt
- https://api.bundle.social/swagger-json
- https://info.bundle.social/api-reference/platforms/instagram
- https://info.bundle.social/api-reference/analytics
- https://info.bundle.social/api-reference/client/analytics/get-social-account-analytics
- https://info.bundle.social/api-reference/client/analytics/get-social-account-analytics-raw
- https://info.bundle.social/api-reference/client/analytics/get-bulk-post-analytics
- https://info.bundle.social/api-reference/automations
- https://info.bundle.social/api-reference/automations/testing-and-logs

Bundle supplies profile views (visits), impressions, unique impressions/reach, likes, comments, postCount, followers, following; profile engagement covers rolling 30 days. Bulk post snapshots supply impressions, unique impressions/reach, views, likes, comments, shares and saves. Post metrics are lifetime snapshots. Unique views are unsupported on Instagram and not displayed. Dislikes are not an Instagram metric and not displayed.

The application adds visit/reach/engagement cards and rolling-profile trends; it never differences rolling metrics as daily gains. Post leaderboard and engagement metrics use posts published within the selected range, with lifetime observations labelled as such. Existing tracked-view totals remain lifetime totals over all tracked posts. Engagement rate=(likes+comments+shares+saves)/video plays*100, weighted using matched, complete post observations, not an average of percentages. Per-1000 rates, mean/median, ranking, publication counts and success rate are application calculations. Missing fields/zero denominators remain unknown. Weekly comparisons require all observation dates and exclude today.

Optional raw analytics: GET `/analytics/social-account/raw` has the same teamId/platformType and wrapper as profile analytics. Its raw property is untyped in Swagger. Parse only documented demographic breakdowns and follows/unfollows/hourly-online formats; do not invent formats for undocumented totals30d/reachTimeSeries contents. Store aggregate audience summaries, not individual messages or followers. Some fields require100+followers; no returned snapshots means unavailable. External automation access can be probed with GET `/automations?teamId=...&limit=1&offset=0`; 404 is documented for organizations not enabled. Do not activate it, reconnect accounts, create flows, send messages or invent click/signup counts as part of analytics. This funnel is not configured yet.

The user's 2026-10-26 explicit deletion authorization superseded the older no-deletion note above: exactly28 failing teams were deleted and verified. Their historical local rows remain archived; current reports now exclude inactive accounts by default. The104 remaining accounts are the active reporting cohort.

## Consistency audit and all-time storage — 2026-10-26

Rechecked https://info.bundle.social/llms.txt ; https://api.bundle.social/swagger-json ; https://info.bundle.social/api-reference/platforms/instagram ; https://info.bundle.social/api-reference/analytics . Source responses and numeric/identity checks are saved in `runs/2026-10-26-dashboard-audit/`.

Provider uncertainty: all104 latest normalized profile responses have exactly equal impressions and impressionsUnique. This equality is in Bundle's responses, not introduced by the application. The docs describe them differently; raw insights are absent. Keep them explicitly provider-reported and flagged, not independently verified unique audience totals. The broader account scope is documented, but we cannot attribute the exact numerical gap versus tracked videos to older content without the missing underlying data. No unsupported reconciliation is invented.

All-time application row: cumulative lifetime video views/likes/comments/shares/saves come from the most recent reading for each distinct tracked video, never by adding overlapping readings. A compact permanent `post_totals` table preserves these latest values independently of90day detailed-history cleanup. Daily account summaries also remain indefinitely. This is all time for content known to this dashboard; it is not full Instagram history. All-time account profile visits/reach are unavailable from the normalized rolling30day endpoint, and cannot be obtained by summing those overlapping totals. User cancelled historical imports, so none are started.

Plain-English explanations distinguish current totals, fixed last30day source windows, selected publication dates versus activity observation dates, repeated viewers, profile visitors versus video plays, stale/missing readings, partial current days, zero denominators and current-account scope. Local download time does not mean Instagram refreshed then. Weekly percentages require adequate comparable observations; missing data is not assumed zero.

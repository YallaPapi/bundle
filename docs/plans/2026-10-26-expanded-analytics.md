# Expanded analytics dashboard

User approved adding the listed standard Instagram metrics, derived performance statistics, top videos and publishing outcomes. Optional audience/funnel data must be labelled unavailable where access or setup is absent. No sending, permission changes, post imports, or other Bundle writes are authorized by this dashboard change.

1. Recheck current llms index, Swagger, Instagram analytics, profile/raw/bulk analytics, quotas, retention and automation-read documentation. Record verified semantics before implementation.
2. Back up SQLite; write failing tests for schema migration, preserving profile rolling totals, per-post rates, missing metrics, active-account scope, correctly weighted network engagement, publishing windows, audience parsing and daily-gap handling.
3. Extend existing tables additively, preserve stable IDs and historical rows. Add normalized profile fields and post reach/impressions, titles/captions/platform IDs. Collect optional raw summaries via GET only. Keep existing sync/catch-up/retention behavior.
4. Add metric cards, rolling-30-day profile trend selector, lifetime post engagement totals, rate/average/median statistics, sortable top videos, publishing charts/status, weekly comparisons and optional audience availability. Scope current reports to active accounts; retain removed-account history locally.
5. Run tests, live GET-only backfill, deduplication/integrity checks and browser checks for desktop/mobile, range/team/sort/search controls. Restart the existing scheduled task and verify the final report.

Daily profile visits are not calculated by subtracting rolling 30-day totals. Reach summed across posts/accounts is labelled as summed, not network-unique. A rate uses only posts with all required numerator fields and its denominator, and a zero denominator yields unavailable. Partial daily coverage remains visible. External funnel click/signup tracking remains unavailable until a landing page and automations exist.

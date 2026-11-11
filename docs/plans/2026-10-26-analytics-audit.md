# Analytics consistency audit and plain-English help

User requests: review every metric for logical inconsistencies, explain the1.38m account figure versus609k tracked plays, add understandable explanations/tooltips throughout, and add an all-time row with durable storage.

Evidence captured before changes in `runs/2026-10-26-dashboard-audit/`: complete profile responses for104 active accounts and bulk responses for1036 tracked videos;731 saved profile snapshots and2919 saved post snapshots match the source exactly. No duplicate Instagram post IDs. Bundle returns identical account impressions/reach for104/104 accounts. Newer post readings already show876354plays versus the earlier stored609358, illustrating staggered updates. All-account profile post count1811 is a different source/scope from1036 tracked videos; the difference cannot be reconciled exactly from normalized profile totals.

Corrections to implement with regression tests:

1. Missing per-account view totals and estimated gains stay unknown, not zero. Counts of videos with data require an actual numeric reading.
2. Keep provider-supplied account reach/impressions but flag the identical fields and never present them as verified network-unique people. Explain all-account last30days versus tracked-video total-so-far.
3. Store a permanent latest-total record per video, keyed by Bundle post ID plus its Instagram identity. Update readings rather than adding them. All-time row ignores the date selector and uses all tracked videos; unavailable lifetime profile visits remain unavailable because rolling30day totals cannot be summed.
4. Review same-identity duplicates, weighted rates, period filters, current-account cohort, missing dates, recalculations, publishing denominators, and partial weekly comparisons. Do not show misleading percentage comparisons when observation coverage is incomplete or the prior value is zero/negative.
5. Show source reading ages separately from the local download time. Add click/keyboard/touch help on every metric/card/chart/table column with plain descriptions, scope, period and caveats; include a readable explanation panel.
6. Back up SQLite, test migration/idempotency/retention, run one read-only catch-up, compare all figures with stored and source records, inspect desktop/mobile and help interaction, restart the existing task and write a concise audit report.

Sources rechecked before edits: current Bundle llms index, Instagram analytics docs, analytics overview and live Swagger; prior full endpoint/retention/quotas/authentication sources remain applicable. No Bundle writes, imports, permission changes or support messages are authorized.

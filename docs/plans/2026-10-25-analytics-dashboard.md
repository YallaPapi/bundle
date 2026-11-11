# Local analytics dashboard implementation plan

**Goal:** A working local dashboard with daily collection, catch-up, and compact permanent history.

**Approved design:** The user selected a local Python page and SQLite database after comparing Sheets and external dashboard options. Store daily account summaries indefinitely; retain detailed post snapshots for 90 days, plus one older baseline per post. Never edit accounts or publish content. No additional design approval is needed.

**Architecture:** `dashboard/app.py` serves a local HTML page and collects existing Bundle analytics using GET requests only. SQLite stores stable account/post IDs and snapshot IDs so repeated downloads update existing records. A Windows scheduled task starts the hidden server at login; its daily loop catches up whenever collection is overdue. A launcher opens the page.

**Stack:** Python standard library, existing requests package, SQLite, HTML/CSS/JavaScript/SVG. No external chart library, database service, or frontend build.

1. Recheck current Bundle index, analytics/account/post/team contracts, Instagram metric definitions, retention, errors, quotas and authentication. Record sources and limitations in `dashboard/API-NOTES.md` before implementation.
2. Write and run failing tests for idempotent catch-up, missing days, view/follower calculations, preserving rollups through retention, and independent API failures.
3. Implement storage and read-only collector; run those tests. Preserve API-returned timestamps, distinguish missing data from zero, and never infer exact daily views from rolling profile totals.
4. Implement the page with follower history, estimated daily video-view gains, coverage, last-sync status, account search/filter/sort, and an account leaderboard.
5. Run the initial live GET-only sync. Reconcile saved counts with API results; repeat an ingestion check to prove no duplicate snapshots. Investigate failures without altering publishing state.
6. Verify the UI in the browser and test the HTTP boundary. Install/start the hidden scheduled task, verify the page and task state, and document opening, syncing, storage, retention and removal.

Validation: meaningful unit tests, real API initial sync, SQLite duplicate/rollup checks, rendered UI checks, local HTTP smoke tests, and Windows task inspection. This workspace is not a Git repository, so no branch, worktree or commit is created.

# Bundle analytics

Open **Open Analytics.cmd** in the project root, or visit http://127.0.0.1:8876/ while the app is running.

The local page shows follower history, estimated daily video-view gains, latest tracked video totals, account status and a searchable leaderboard. Filter by VA/team prefix and date range. A source timestamp and coverage accompany the figures. Instagram's profile-visit count is never used as video plays.

The expanded page includes:

- An all-time row for plays, likes, comments, shares, saves and distinct tracked videos. It ignores the date filter and includes only known videos on the currently included accounts. Older untracked Instagram posts are not imported. All-time profile visits and distinct people are unavailable; overlapping 30-day totals cannot be added to reconstruct them.
- Clickable “i” explanations for cards, charts, table columns and unavailable fields, including source periods and reading dates. Identical account reach/impression values supplied by Bundle are explicitly flagged as needing clarification.
- Profile visits, reach, content impressions, profile likes/comments (rolling30days), following and profile post count (latest totals).
- Video likes, comments, shares, saves, total content views, summed reach, mean/median plays and engagement rate.
- Per-1000-play rates for likes/comments/shares/saves, sortable/searchable top videos with Instagram links, and alternate account leaderboard columns.
- Daily snapshot gains for plays/likes/comments/shares/saves, rolling-profile trend selectors, and week-on-week comparisons excluding today. Comparisons remain unavailable until both seven-day observation windows have data.
- Actual publishing outcomes and success rate in the chosen period, all scheduled future posts, and current account issues.
- Optional audience country/city/age/gender and age-gender breakdowns, follows/unfollows and online hours, if Bundle returns documented raw insights. Missing data is unavailable, not zero. The current organization returns no raw snapshots; no extra access is enabled automatically.
- Recipe funnel readiness. Automation access is currently disabled; no keyword-request, DM, link-click or signup figures are invented. Actual funnel tracking requires that future setup.

All current metrics use active accounts only. Deleted accounts' local history remains archived. The date selector controls publication cohorts and daily activity; it does not change the source's rolling30day window. Lifetime play totals over all tracked videos are labelled separately. Network reach sums are not deduplicated across accounts/posts.

## Daily updates

The Windows scheduled task **Bundle Local Analytics** starts the hidden Python server at login, with a daily 09:00 fallback trigger and restart on failure. It runs as your current user while logged in. Its background loop syncs after 24 hours; a partial sync retries after an hour. Closing the browser leaves collection running. Turning the computer off pauses local collection; startup/login catches up using Bundle's retained snapshots. Anything Bundle never collected, or already deleted beyond its 30-day retention, cannot be backfilled.

**Sync analytics** downloads existing retained analytics immediately. It does not force-refresh Instagram insights, upload, schedule, retry or delete posts. No team or profile edits are performed.

## Storage

Database: `dashboard/data/analytics.sqlite3` (with SQLite WAL files while running).

- Account snapshots and daily account/network summaries: retained indefinitely.
- Detailed post snapshots: 90 days, plus one older baseline per post.
- Post identity/status and the compact `post_totals` table: retained indefinitely. Each video has one latest cumulative reading; a newer reading replaces its values rather than being added. These totals survive cleanup of detailed snapshots and prevent duplicate counting across daily downloads. Instagram video IDs also prevent aliases from counting twice in reports.
- Logs: rotating, at most about 1.5 MB. No videos, full API payloads or credentials in the database.

Storage grows with accounts, posts and observation history; it is not a fixed-size database. Old detailed rows are pruned and SQLite reuses freed space. Daily summaries and stable post records stay much smaller than media files. Back up with SQLite's backup command rather than copying a live database without its WAL:

```powershell
python -c "import sqlite3; s=sqlite3.connect('dashboard/data/analytics.sqlite3'); d=sqlite3.connect('analytics-backup.sqlite3'); s.backup(d); d.close(); s.close()"
```

API key: root `.env`, existing `BUNDLE_SOCIAL_API_KEY`. The key is read by Python and never sent to the browser. The server binds to this computer only (`127.0.0.1`).

## Commands

```powershell
python dashboard/app.py sync       # Read-only sync now
python dashboard/app.py status     # Last sync and progress
python dashboard/app.py serve      # Run manually in the current terminal
python -m unittest dashboard.test_app -v
python -m unittest dashboard.test_app dashboard.test_metrics dashboard.test_audit -v
powershell -NoProfile -ExecutionPolicy Bypass -File dashboard/install.ps1
```

Python uses the existing `requests` package. A new Python installation may need `python -m pip install requests`.

To stop automatic collection without deleting history:

```powershell
Stop-ScheduledTask -TaskName 'Bundle Local Analytics'
Disable-ScheduledTask -TaskName 'Bundle Local Analytics'
```

Metric definitions and verified API sources: [API-NOTES.md](API-NOTES.md).

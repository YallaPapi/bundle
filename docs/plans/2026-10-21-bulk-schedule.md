# Bulk video scheduling plan

**Goal:** Caption the supplied 3,411 MP4s and schedule across connected roster Instagram accounts, two posts per account daily, twelve hours apart.

**Architecture:** Extend the verified six-video procedure with a durable per-file ledger. Keep original files unchanged; use current API schemas. No automatic mutation retries; stop on first failed or ambiguous mutation and preserve receipts. No server or VA application.

**Tech stack:** Python, ffprobe/ffmpeg, Bundle REST API, local frame inspection and available caption tooling.

1. Fetch current applicable docs and OpenAPI; save feature note before implementation. Read connected accounts, quota, daily limits, existing posts and old test receipts. Include ALL connected Instagram accounts across all teams, regardless of roster username mismatches, per the user's correction. Establish actual connected usernames and avoid repeated source hashes.
2. Inventory/hash/probe all input videos and extract representative frames for accurate post captions. Check encoder, resolution, duration, bitrate, size and readable existing text. Validate caption generation before any upload.
3. Build manifest assigning files evenly across verified roster accounts and unoccupied daily slots twelve hours apart. Default Bangkok 09:00/21:00 starting tomorrow to allow completion before publication. Record all IDs, captions, source hashes, times and reference keys.
4. Check payloads against live schema and test local scheduling/restart guards with no network writes. Validate quota for entire batch. Stop if unsupported media or caption failures remain unresolved.
5. Upload each local video once to its assigned team; persist intent and returned media ID. Schedule once using that media ID, persist post ID, GET to verify exact caption/team/time/media. Never retry an ambiguous request. Persist errors and stop all further mutations.
6. Reconcile all receipts and export one results CSV. Report actual scheduled count, dates, accounts and any failure honestly. Existing posted test content remains unchanged.

User authorization: user confirmed this folder is to be captioned and scheduled two posts per account daily twelve hours apart. No new approval needed for these operations. Continue authorized steps without extra handoffs.

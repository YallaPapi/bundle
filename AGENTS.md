# Bundle API implementation requirements

- Before building each feature, consult Bundle's current documentation for that feature. No guessing about API capabilities or behavior.
- Start with https://info.bundle.social/llms.txt to discover all relevant guides, endpoint references, platform-specific requirements and limits. Cross-check request and response schemas against https://api.bundle.social/swagger-json.
- Read all documentation applicable to the feature, including authentication/scope, required fields, defaults, pagination, asynchronous states, errors, quotas, media handling and retention where relevant.
- Record the documentation URLs and verified API behavior in a short feature note before implementation. Separate behavior supplied by Bundle from behavior implemented by this application.
- Treat existing conversational descriptions and setup-plan.txt as proposed designs, not verified API contracts. Recheck their assumptions before implementing them.
- If documentation is missing, ambiguous or conflicting, identify the uncertainty and resolve it through authoritative documentation, an authorized non-destructive check, or clarification. Do not invent behavior or proceed with dependent implementation on an unsupported assumption.
- Verify the implementation against the documented contract and appropriate checks before claiming the feature works. Never publish real content just to test without explicit authorization.
- Keep the API key in .env; never print it or include it in documentation, fixtures or source control.
- For bulk scheduling, recover from transient errors with bounded backoff and continue independent items rather than stopping the entire run on the first error (user preference, 2026-10-21).
- Never repeat a confirmed successful upload or post creation. Persist returned IDs immediately, resume from receipts, and reconcile uncertain writes through read-only checks before resubmitting. Record non-transient or unresolved errors for review.
- Stagger posting times across accounts; do not assign one synchronized time pair to every account. Preserve the requested per-account frequency/spacing and report exact timestamps with their timezone.

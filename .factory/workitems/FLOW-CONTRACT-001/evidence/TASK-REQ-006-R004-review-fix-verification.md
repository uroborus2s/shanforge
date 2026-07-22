# TASK-REQ-006 R004 Review Fix Verification

## Verification target

- Candidate revision: `R004`
- Finding: `R003-I-001`
- Verification date: 2026-07-21

## Fresh verification

1. `python3 -m json.tool <R004.contract.json>`
   - Exit code: `0`
   - Result: valid JSON.
2. `rg -n "current_authoritative_authorization_source|required_before|cache_hit|file_path_return|html_body_return|VIEW_AUTHORIZATION_INACTIVE|VIEW_AUTHORIZATION_CHECK_FAILED|fail_closed|serve_denial_waits_for|revoked_pending_cleanup|recompute_input_fingerprint_required" <R004.md> <R004.contract.json>`
   - Exit code: `0`
   - Result: all read/serve gates, fixed failure codes, non-blocking physical cleanup, and reactivation rule are represented.
3. `rg -n "TODO|TBD|待定|稍后决定" <R004.md> <R004.contract.json>`
   - Exit code: `1`
   - Result: expected no-match; no unresolved placeholders.

## Artifact hashes

| Artifact | SHA-256 |
|---|---|
| `drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001-R004.md` | `e3626b8881d3c932bddd5232d61df3808c722545a28443f666fc31b7d0749e74` |
| `drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001.contract.R004.json` | `0a8bdd04f95f539e81861c4c5c9ce4cc170b78d0fee88326b669baf1924536b0` |
| `reviews/TASK-REQ-006-R003-independent-rereview.md` | `86e06dad40c61d7be8d2366a88cdc00d9958e73e566330e44838e2bfa5684b08` |
| `reviews/TASK-REQ-006-R003-review-feedback-triage-R004.md` | `e25fe0c54244a8c8b3a3e9336274c80e908f6c4a606f5151216f2004c486b76a` |
| `reviews/TASK-REQ-006-R003-review-response-R004.md` | `5e6c7db259d389732078a1bad882f639f2bb3499f982f38b863b5cca9be4d346` |

## Finding closure evidence

- Every application-controlled HTML fast path must prove current active authorization before cache hit, file read, path return, or body return.
- Unknown, inactive, revoked, unavailable, and unproven authorization all deny service with fixed reason codes.
- Revocation denial is based on the authoritative fact and does not wait for SQLite projection or physical deletion.
- Reactivation cannot blindly reuse the file; current fingerprint and output Hash must be revalidated.

Author verification is complete. Independent and human approval remain pending.

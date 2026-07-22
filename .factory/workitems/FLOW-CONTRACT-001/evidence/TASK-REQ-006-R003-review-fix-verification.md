# TASK-REQ-006 R003 Review Fix Verification

## Verification target

- Requirement change: `REQ-CHANGE-PROJECT-KNOWLEDGE-001`
- Candidate revision: `R003`
- Findings: `R002-I-001`, `R002-M-001`
- Verification date: 2026-07-21

## Fresh verification

1. `python3 -m json.tool .factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001.contract.R003.json`
   - Exit code: `0`
   - Result: R003 machine contract is valid JSON.
2. `rg -n "RenderViewScope/v1|RenderInputFingerprint/v1|current\\.html|latest_files_per_scope|cross_digest_reuse_allowed|generated_view_versions_per_kind|stale_after_refresh_failure" <R003.md> <R003.contract.json>`
   - Exit code: `0`
   - Result: stable scope, changing fingerprint, single output slot, unconditional authorization isolation, R001 override, and failure semantics are all present in the human and machine contracts.
3. `rg -n "TODO|TBD|待定|稍后决定" <R003.md> <R003.contract.json>`
   - Exit code: `1`
   - Result: expected no-match; R003 contains no unresolved placeholder.
4. `shasum -a 256 <task-card> <R003.md> <R003.contract.json> <R002-review> <triage> <response>`
   - Exit code: `0`
   - Result: hashes recorded below.

## Artifact hashes

| Artifact | SHA-256 |
|---|---|
| `task-briefs/TASK-REQ-006-project-knowledge-index-and-deterministic-docs.md` | `542f98dc61f86be80fcd1a9bf6ff9254933fff9bcb769d92e98727ec2816592b` |
| `drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001-R003.md` | `c8daddc5cb0d1067d214cb7aa69632c8edc05dcdbf7a7ab859d18dc8f141d748` |
| `drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001.contract.R003.json` | `7d5c60aaacbc75bb3fc60625eb309650c6a73b79ccb9a43698c62cb0792956f4` |
| `reviews/TASK-REQ-006-R002-independent-review.md` | `8ee2413697b3d2cd14a95e87dff4c50fe759b42fd20ee38b488022f98052c485` |
| `reviews/TASK-REQ-006-R002-review-feedback-triage-R003.md` | `8adc722a6b993d3bae091cc508f9fe83d607037ffe3f19d26f6e279e7340d9c0` |
| `reviews/TASK-REQ-006-R002-review-response-R003.md` | `3b308d2b57ba02cd524c4f9cffa039bd7955701b26e0a9fe7dc178fc2f13efea` |

## Finding closure evidence

- `R002-I-001`: `RenderViewScope/v1` controls the only persistent path and row; `RenderInputFingerprint/v1` controls refresh only. A refresh atomically replaces the same path and cannot create historical fingerprint rows or HTML files. R001's three-version default is explicitly overridden to one file per stable scope.
- `R002-M-001`: both contracts unconditionally set cross-authorization reuse to false and require registered authorization scopes plus revoked-scope cleanup.

Author verification is complete. This evidence does not constitute independent approval or human approval.

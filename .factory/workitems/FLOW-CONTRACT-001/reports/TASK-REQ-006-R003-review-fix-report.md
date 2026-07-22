# TASK-REQ-006 R003 Review Fix Report

## Outcome

R003 fixes the two R002 review findings without expanding the approved scope.

- The persistent HTML identity is now the stable `view_type + authorization_digest + normalized_query` scope.
- Snapshot, source, renderer, template, and schema changes form a separate input fingerprint used only by deterministic freshness checks.
- One stable scope maps to one SQLite row and at most one `current.html`; refresh atomically replaces that file.
- Different authorization digests never share generated HTML.
- `.factory/pm` remains excluded as an independent fact store.

## Changed candidate artifacts

- `drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001-R003.md`
- `drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001.contract.R003.json`
- `reviews/TASK-REQ-006-R002-review-feedback-triage-R003.md`
- `reviews/TASK-REQ-006-R002-review-response-R003.md`
- `evidence/TASK-REQ-006-R003-review-fix-verification.md`

## Gate

Status: `ready_for_same_reviewer_rereview`.

R003 must be checked by the same independent reviewer that returned the R002 findings. A successful rereview still leaves the requirement change pending exact human approval before formal PRD, design, implementation, Git, or release changes.

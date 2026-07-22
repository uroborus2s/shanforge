# TASK-REQ-006 R004 Review Fix Report

## Outcome

R004 closes the authorization-revocation serving window found in the R003 rereview.

- Cache presence never authorizes a response.
- Current authoritative authorization is required before every cache-hit, read, path-return, and body-return path.
- Revocation immediately denies subsequent application service decisions; SQLite marking and physical deletion remain asynchronous cleanup.
- The command returns a deterministic denial receipt instead of stale HTML, an old path, anonymous fallback, or an AI decision.

## Scope

Only `R003-I-001` was changed. R001–R003 remain frozen bases, and no formal PRD, design, source, test, Git, or release artifact was changed.

## Gate

Status: `ready_for_same_reviewer_rereview`.

The same independent reviewer must verify the fix. Approval will still require a separate exact-candidate human gate before formal design and implementation.

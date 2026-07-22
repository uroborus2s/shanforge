# TASK-REQ-006 R004 Independent Rereview Input

## Reviewer task

Perform a read-only, file-bound rereview of the R004 remediation for `R003-I-001`.

## Required inputs

1. `.factory/workitems/FLOW-CONTRACT-001/reviews/TASK-REQ-006-R003-independent-rereview.md`
2. `.factory/workitems/FLOW-CONTRACT-001/reviews/TASK-REQ-006-R003-review-feedback-triage-R004.md`
3. `.factory/workitems/FLOW-CONTRACT-001/reviews/TASK-REQ-006-R003-review-response-R004.md`
4. `.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001-R004.md`
5. `.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001.contract.R004.json`
6. `.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-REQ-006-R004-review-fix-verification.md`
7. `.factory/workitems/FLOW-CONTRACT-001/reports/TASK-REQ-006-R004-review-fix-report.md`

## Required checks

- Verify `R003-I-001` is closed for cache hit, file read, path return, and HTML body return.
- Verify inactive/revoked and unavailable/unproven authorization fail closed with deterministic reason codes.
- Verify denial does not wait for SQLite projection, maintenance, or physical deletion.
- Verify reactivation cannot reuse a stale file without current fingerprint and output Hash validation.
- Check R004 against the already-closed R002 findings and report any regression or new contradiction.
- Validate the machine contract and record actual verification.
- Do not treat approval as human authorization for formal PRD, design, implementation, Git, or release.

## Required output

Write only:

`.factory/workitems/FLOW-CONTRACT-001/reviews/TASK-REQ-006-R004-independent-rereview.md`

Include reviewer identity/independence, decision, score, C/I/M counts, explicit `R003-I-001` closure, regression status for `R002-I-001` and `R002-M-001`, new findings, verification, and next gate.

# TASK-REQ-006 R003 Independent Rereview Input

## Reviewer task

Perform a read-only, file-bound rereview of the R003 remediation. Verify that both prior findings are closed and that no new Critical, Important, or Minor inconsistency was introduced.

## Required inputs

1. `.factory/workitems/FLOW-CONTRACT-001/reviews/TASK-REQ-006-R002-independent-review.md`
2. `.factory/workitems/FLOW-CONTRACT-001/reviews/TASK-REQ-006-R002-review-feedback-triage-R003.md`
3. `.factory/workitems/FLOW-CONTRACT-001/reviews/TASK-REQ-006-R002-review-response-R003.md`
4. `.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001-R003.md`
5. `.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001.contract.R003.json`
6. `.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-REQ-006-R003-review-fix-verification.md`
7. `.factory/workitems/FLOW-CONTRACT-001/reports/TASK-REQ-006-R003-review-fix-report.md`

## Required checks

- Confirm `R002-I-001` is closed: stable view scope controls exactly one row/path, while changing freshness inputs cannot create additional output slots.
- Confirm R001 `generated_view_versions_per_kind=3` is unambiguously overridden to one file per stable scope.
- Confirm `R002-M-001` is closed: cross-authorization reuse is unconditionally prohibited in both human and machine contracts.
- Check refresh failure, authorization revocation, scope bounding, and cache-hit behavior for contradictions.
- Validate R003 JSON and record actual verification commands and results.
- Do not treat reviewer approval as human approval or authorization to change formal PRD, design, code, Git, or release state.

## Required output

Write only:

`.factory/workitems/FLOW-CONTRACT-001/reviews/TASK-REQ-006-R003-independent-rereview.md`

The report must include reviewer identity and independence evidence, `approved` or `changes_requested`, score, C/I/M counts, explicit closure status for both prior findings, any new findings, verification, and next gate.

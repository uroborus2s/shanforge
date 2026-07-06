# Iteration 4 Fixes Independent Review Task

## Role

真实独立 reviewer。

## Goal

Review `SKILL-FLOW-AUDIT-001` iteration-4 feedback fixes. Decide `approved` or `changes_requested`.

## Inputs

- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/chinese-language-review-iteration-4.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/prompt-engineering-review-iteration-4.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-completeness-test-iteration-4.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/task-briefs/iteration-4-fix-language-prompt-contracts.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/task-briefs/iteration-4-fix-flow-completeness.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reports/iteration-4-fix-language-prompt-contracts-report.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reports/iteration-4-fix-flow-completeness-report.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reports/iteration-4-fix-summary-report.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-4-fix-language-prompt-contracts-verification.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-4-fix-flow-completeness-verification.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-4-fix-combined-verification.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-4-s1-s6-dry-run-transcript.md`
- relevant diff for changed skill / test / evidence files

## Review Checks

1. Verify fixes address the Critical / Important findings from the three iteration-4 reports.
2. Confirm no old center `factory-*` gate was reintroduced.
3. Confirm `gitcommitzh` still does not own remote PR / push / merge.
4. Confirm S1-S6 transcript is evidence, not a claim of real code/push/PR/merge completion.
5. Re-run the targeted verification if feasible.
6. Give score 0-100 and list Critical / Important / Minor findings.

## Output

Write:

`.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/iteration-4-fixes-independent-review.md`

Do not edit source files. Do not write ledger. Do not commit.

# Iteration 6 Fix Language Prompt 97 Independent Review Task

## Role

独立 reviewer。不得参与实现，不得修改源码、测试、ledger 或 memory。

## Goal

复评 `iteration-6-fix-language-prompt-97` 修复是否达到目标：

- 中文语言平均分 `>= 97`；
- Prompt 工程平均分 `>= 97`；
- Critical / Important 均为 `0`；
- Required Fixes 1-8 均已处理；
- 未恢复旧中心脚本、旧 `factory-*` gate 或远端闭环冒充。

## Inputs

- `.factory/workitems/SKILL-FLOW-AUDIT-001/task-briefs/iteration-6-fix-language-prompt-97.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reports/iteration-6-fix-language-prompt-97-report.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-6-fix-language-prompt-97-verification.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-6-fix-language-prompt-97-main-verification.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/iteration-6-fix-language-prompt-97-review-input.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/chinese-language-review-iteration-6.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/prompt-engineering-review-iteration-6.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-completeness-test-iteration-6.md`
- Current diff for the files listed in the review input.

## Output

Write only:

`.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/iteration-6-fix-language-prompt-97-independent-review.md`

The report must include:

1. `reviewer_type`, `reviewer_id`, and `reviewer_independence_evidence`.
2. Final status: `approved` or `changes_requested`.
3. Chinese language score and Prompt engineering score.
4. Critical / Important / Minor findings.
5. Required Fixes 1-8 checklist.
6. Verification commands reviewed or rerun, with exit codes.
7. Residual risks and whether they block 97-point acceptance.
8. Recommendation for next gate: `pending_human_confirmation` or `fix_review_feedback`.

## Review Rules

- If either average is below `97`, status must be `changes_requested`.
- If any Critical or Important remains, status must be `changes_requested`.
- Minor findings may be non-blocking if explicitly justified.
- Do not trust author self-score without inspecting changed files.
- Do not write ledger or memory; the parent thread records review receipt.

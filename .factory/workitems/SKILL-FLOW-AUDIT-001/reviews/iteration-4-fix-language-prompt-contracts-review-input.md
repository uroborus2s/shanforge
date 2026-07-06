# Iteration 4 Fix Language Prompt Contracts Review Input

work_item: SKILL-FLOW-AUDIT-001
task: iteration-4-fix-language-prompt-contracts
status: ready_for_review

## Review Scope

Review only the bounded fix for iteration-4 language and prompt contract findings. Do not treat this package as approval or human confirmation.

## Inputs Read

- `.factory/workitems/SKILL-FLOW-AUDIT-001/task-briefs/iteration-4-fix-language-prompt-contracts.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/chinese-language-review-iteration-4.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/prompt-engineering-review-iteration-4.md`

## Files To Review

- `skills/document-templates/SKILL.md`
- `skills/requesting-code-review/SKILL.md`
- `skills/receiving-code-review/SKILL.md`
- `skills/python-uv-project/SKILL.md`
- `skills/browser-control/SKILL.md`
- `skills/crawler4j-model-project/SKILL.md`
- `tests/test_review_workflow_skills.py`
- `tests/test_bug_fix_root_cause_skill_rules.py`
- `tests/test_browser_control_skill.py`
- `tests/test_crawler4j_model_skill_integration.py`
- `tests/test_sf_sp_010_documentation_navigation.py`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reports/iteration-4-fix-language-prompt-contracts-report.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-4-fix-language-prompt-contracts-verification.md`

## Expected Review Checks

- Each target skill has the minimum `工作结果` status package fields: `work_item`, `status`, `outputs`, `evidence`, `ledger_event`, `needs`.
- Each target skill defines concrete `blocked` and `needs_user_input` semantics.
- `document-templates` no longer has English D3 frontmatter wording and its status package includes `work_item` / `ledger_event`.
- `python-uv-project` no longer claims ownership of the Python Bug root-cause flow; it only constrains uv and Python tooling while `systematic-debugging` / `tdd-workflow` own the debugging and Red/Green flow.
- No changes were made to `gitcommitzh`, `skill-creator`, or `stratix-service`.
- No ledger event was written.

## Verification Evidence

- `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-4-fix-language-prompt-contracts-verification.md`
- Final pytest: 30 passed.
- Final ruff: All checks passed.

## Known Residual Scope

- This task does not compress long entrances in `gitcommitzh`, `skill-creator`, or `stratix-service`.
- This task does not address the separate skill-flow completeness findings around S1-S6 dry-run transcript or remote PR / push / merge handoff.

## Work Result

```text
工作结果：
- work_item: SKILL-FLOW-AUDIT-001
- skill: executing-plans
- status: ready_for_review
- outputs:
  - .factory/workitems/SKILL-FLOW-AUDIT-001/reviews/iteration-4-fix-language-prompt-contracts-review-input.md
  - .factory/workitems/SKILL-FLOW-AUDIT-001/reports/iteration-4-fix-language-prompt-contracts-report.md
- evidence:
  - .factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-4-fix-language-prompt-contracts-verification.md
- ledger_event: none
- needs:
  - review
```

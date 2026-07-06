# Iteration 4 Fix Flow Completeness Review Input

- Work item: `SKILL-FLOW-AUDIT-001`
- Task: `iteration-4-fix-flow-completeness`
- Implementer status: `ready_for_review`
- Ledger: not written by this subtask.
- Commit: not created by this subtask.

## Files For Review

- `skills/using-shanforge/SKILL.md`
- `skills/using-shanforge/references/black-box-flow-eval.md`
- `skills/using-shanforge/references/remote-pr-handoff.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-4-s1-s6-dry-run-transcript.md`
- `tests/test_black_box_workflow_eval.py`
- `tests/test_pr_commit_workflow_rules.py`
- `tests/test_skill_flow_process_audit.py`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reports/iteration-4-fix-flow-completeness-report.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-4-fix-flow-completeness-verification.md`

## Review Questions

- Does the S1-S6 transcript include all required fields and avoid presenting dry-run as real implementation, commit, push, PR, or merge?
- Does `remote-pr-handoff.md` define owner, input, local commit prerequisites, remote tools, evidence, failure semantics, statuses, and anti-impersonation rules?
- Does `using-shanforge` reference the handoff while keeping `gitcommitzh` scoped to local commit only?
- Do the tests lock the transcript and handoff contract without reintroducing old factory gate behavior?

## Verification Evidence

```text
uv run pytest tests/test_black_box_workflow_eval.py tests/test_pr_commit_workflow_rules.py tests/test_skill_flow_process_audit.py
exit code: 0
19 passed

uv run ruff check tests/test_black_box_workflow_eval.py tests/test_pr_commit_workflow_rules.py tests/test_skill_flow_process_audit.py
All checks passed!
```

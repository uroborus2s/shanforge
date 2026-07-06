# SKILL-FLOW-AUDIT-001 Review Input

## Work Item

- Work item: `SKILL-FLOW-AUDIT-001`
- Review type: independent review / scoring
- Source report: `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-test-report.md`

## Requirements

Review only the fixes derived from `skill-flow-test-report.md`:

1. `requirements-engineering` must expose Shanforge outputs, ledger/memory sync, state package, and no self-approval boundary.
2. `brainstorming` must not choose or prescribe the next skill; it must only return status, outputs, approval, evidence, ledger_event, and `needs`.
3. Tests must lock the above contracts.
4. Report/evidence/ledger must record real commands and keep unresolved PR / real black-box replay gaps as explicit non-goals for this repair.

## Task Briefs

- `.factory/workitems/SKILL-FLOW-AUDIT-001/task-briefs/requirements-engineering-flow-contract.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/task-briefs/brainstorming-flow-contract.md`

## Changed Files In Scope

- `skills/requirements-engineering/SKILL.md`
- `skills/brainstorming/SKILL.md`
- `skills/brainstorming/agents/openai.yaml`
- `skills/brainstorming/spec-document-reviewer-prompt.md`
- `tests/test_requirements_engineering_skill.py`
- `tests/test_brainstorming_skill.py`
- `tests/test_skill_flow_process_audit.py`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-1-verification.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reports/software-development-and-skill-flow.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/ledger.jsonl`

## Verification Evidence

Fresh main-thread verification:

```text
uv run pytest tests/test_brainstorming_skill.py tests/test_skill_flow_process_audit.py tests/test_requirements_engineering_skill.py
11 passed in 0.01s

uv run ruff check tests/test_brainstorming_skill.py tests/test_skill_flow_process_audit.py tests/test_requirements_engineering_skill.py
All checks passed!

python3 -c ledger jsonl validation
ledger jsonl ok
```

## Diff Package

Reviewer should inspect:

```text
git diff -- skills/requirements-engineering/SKILL.md skills/brainstorming/SKILL.md
```

For untracked files in this work item, inspect the actual files listed under "Changed Files In Scope".

## Known Non-Goals

- Do not require a new remote PR / push / merge workflow in this repair.
- Do not require a real 6-scenario black-box replay runner in this repair.
- Do not mark reviewer approval as `done` or human approval.

## Review Output

Write the review to:

`.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-report-fixes-independent-review.md`

Use the rubric in `skills/requesting-code-review/references/review-score-rubric.md`.

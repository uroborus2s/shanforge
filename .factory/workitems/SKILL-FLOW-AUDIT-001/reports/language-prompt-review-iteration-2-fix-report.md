# Language Prompt Review Iteration 2 Fix Report

## Scope

Fixed issues from `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/language-prompt-review-iteration-2.md`.

Edited 21 current skill entrances:

- `skills/agent-harness-construction/SKILL.md`
- `skills/ai-first-engineering/SKILL.md`
- `skills/ai-regression-testing/SKILL.md`
- `skills/algorithmic-art/SKILL.md`
- `skills/api-design/SKILL.md`
- `skills/article-writing/SKILL.md`
- `skills/doc-coauthoring/SKILL.md`
- `skills/document-templates/SKILL.md`
- `skills/docx/SKILL.md`
- `skills/frontend-patterns/SKILL.md`
- `skills/gitcommitzh/SKILL.md`
- `skills/humanizer/SKILL.md`
- `skills/pdf/SKILL.md`
- `skills/shadcn/SKILL.md`
- `skills/skill-creator/SKILL.md`
- `skills/stratix-service/SKILL.md`
- `skills/subagent-driven-development/SKILL.md`
- `skills/tdd-workflow/SKILL.md`
- `skills/ui-ux-pro-max/SKILL.md`
- `skills/webapp-testing/SKILL.md`
- `skills/xlsx/SKILL.md`

## Changes

- Compressed long tutorial-style `SKILL.md` entrances.
- Removed stale ecosystem wording from P0 and file-tool entrances.
- Added or tightened "when to use", "do not use", output contract, evidence, verification, blocked/failure semantics.
- Replaced fixed framework-heavy defaults with project-pattern-first guidance.
- Preserved existing hard gates for root cause, review independence, human confirmation, commit scope, and PR boundary.

## Verification

```text
uv run pytest tests/test_bug_fix_root_cause_skill_rules.py tests/test_verification_debugging_workflow_skills.py tests/test_pr_commit_workflow_rules.py tests/test_execution_workflow_skills.py tests/test_deprecated_skill_cleanup.py tests/test_stratix_service_skill.py tests/test_skill_creator_skill_principles.py tests/test_skill_flow_process_audit.py
45 passed in 0.04s
```

```text
uv run ruff check tests/test_bug_fix_root_cause_skill_rules.py tests/test_verification_debugging_workflow_skills.py tests/test_pr_commit_workflow_rules.py tests/test_execution_workflow_skills.py tests/test_deprecated_skill_cleanup.py tests/test_stratix_service_skill.py tests/test_skill_creator_skill_principles.py tests/test_skill_flow_process_audit.py
All checks passed!
```

```text
python3 skills/skill-creator/scripts/quick_validate.py <edited skill>
21 edited skill directories passed.
```

```text
git diff --check -- <edited skill files>
passed
```

```text
rg old wording scan
no matches
```

## Status

`ready_for_review`. Next action is to create and run fresh language/prompt review and skill-flow completeness test subtasks as requested by the user.

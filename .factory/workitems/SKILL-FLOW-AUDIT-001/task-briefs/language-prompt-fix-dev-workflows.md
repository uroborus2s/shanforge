# Language Prompt Fix Dev Workflows

## Scope

Only edit:

- `skills/frontend-patterns/SKILL.md`
- `skills/tdd-workflow/SKILL.md`
- `skills/ai-regression-testing/SKILL.md`
- `skills/api-design/SKILL.md`

## Goal

Fix tutorial-heavy and framework-bound wording:

- move main entrance from long examples to decision tables/checklists;
- keep framework examples as optional references by name, not default workflow;
- add Shanforge output contract: `work_item`, `skill`, `status`, `outputs`, `evidence`, `ledger_event`, `needs`;
- clarify boundaries with `systematic-debugging`, `verification-before-completion`, and existing project patterns;
- avoid fixed 80% / full E2E requirements when risk does not justify them.

## Constraints

- Do not edit tests or references in this batch.
- Preserve root-cause and anti-fallback discipline required by existing tests.
- Do not add dependencies or scripts.

## Verification

Run relevant tests if possible:

- `uv run pytest tests/test_bug_fix_root_cause_skill_rules.py tests/test_verification_debugging_workflow_skills.py`

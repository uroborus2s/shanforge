# SF-SP-006 Review Response

## Fixed

- Split review output and workflow gate semantics:
  - `review_status=self_check_passed` for same-thread author self-check.
  - `next_gate_status=needs_independent_review` when independent evidence is missing.
- Updated review rubric and templates to use `review_status` and `next_gate_status`.
- Added receiving-code-review memory sync targets:
  - `.factory/memory/review-ledger.jsonl`
  - `.factory/memory/tasks.summary.md`
  - required summary files when flow, skill, tests, or formal docs change.
- Updated `requesting-code-review/agents/openai.yaml` so only real independent review emits `review_score`; same-thread emits `author_self_check_score`.
- Added regression assertions in `tests/test_review_workflow_skills.py` and updated `tests/test_independent_review_gate.py`.

## Verified

- `.venv/bin/pytest tests/test_execution_workflow_skills.py tests/test_review_workflow_skills.py tests/test_independent_review_gate.py tests/test_superpowers_reference_migration.py tests/test_writing_plans_skill.py tests/test_verification_debugging_workflow_skills.py`: `28 passed`
- `.venv/bin/ruff check tests/test_execution_workflow_skills.py tests/test_review_workflow_skills.py tests/test_independent_review_gate.py tests/test_superpowers_reference_migration.py tests/test_writing_plans_skill.py tests/test_verification_debugging_workflow_skills.py`: `All checks passed!`
- Skill validators for `requesting-code-review` and `receiving-code-review`: `Skill is valid!`

## Needs

- independent_review

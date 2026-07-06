# Iteration 4 Fix Language Prompt Contracts Verification

time: 2026-07-06 22:40:29 +0800
work_item: SKILL-FLOW-AUDIT-001
task: iteration-4-fix-language-prompt-contracts

## Commands

### Initial Pytest

```bash
uv run pytest tests/test_review_workflow_skills.py tests/test_skill_flow_process_audit.py tests/test_bug_fix_root_cause_skill_rules.py tests/test_browser_control_skill.py tests/test_crawler4j_model_skill_integration.py tests/test_sf_sp_010_documentation_navigation.py
```

- exit code: 1
- result: 28 passed, 2 failed
- failures:
  - `tests/test_review_workflow_skills.py::test_receiving_code_review_skill_requires_verification_before_changes`
  - `tests/test_bug_fix_root_cause_skill_rules.py::test_python_uv_project_applies_root_cause_rule_to_python_debugging`
- cause: two phrase assertions no longer matched after wording cleanup.
- fix: kept the receiving review prohibition in frontmatter and restored the exact Python root-cause sentence in the new boundary section.

### Final Pytest

```bash
uv run pytest tests/test_review_workflow_skills.py tests/test_skill_flow_process_audit.py tests/test_bug_fix_root_cause_skill_rules.py tests/test_browser_control_skill.py tests/test_crawler4j_model_skill_integration.py tests/test_sf_sp_010_documentation_navigation.py
```

- exit code: 0
- collected: 30
- result: 30 passed in 0.04s

### Final Ruff

```bash
uv run ruff check tests/test_review_workflow_skills.py tests/test_skill_flow_process_audit.py tests/test_bug_fix_root_cause_skill_rules.py tests/test_browser_control_skill.py tests/test_crawler4j_model_skill_integration.py tests/test_sf_sp_010_documentation_navigation.py
```

- exit code: 0
- result: All checks passed

## Requirement Check

- Status packages: present in all six target skills.
- `blocked` / `needs_user_input`: present in all six target skills.
- `document-templates` description: Chinese, no `D3` in frontmatter, uses `docs-stratego` 4-module wording.
- `document-templates` status package: includes `work_item` and `ledger_event`.
- `python-uv-project`: explicitly delegates Python Bug root-cause and Red/Green flow to `systematic-debugging` / `tdd-workflow`; retains uv/toolchain constraints.
- Out-of-scope skills not edited: `gitcommitzh`, `skill-creator`, `stratix-service`.
- Ledger: not written, per task instruction.

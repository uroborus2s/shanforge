# T05：Go/Python 验证范围

- task_card_id: `SOFTWARE-ENGINEERING-SKILL-REMEDIATION-001-T05`
- wbs_id: `WBS-REM-05`
- status: `completed`
- priority: `P1`
- task_scope: `system`
- depends_on: `T04`
- risk_level: `medium`
- execution_model: `gpt-5.6-terra`
- requested_reasoning_effort: `medium`
- execution_authorized: `true`
- current_gate: `closed`
- next_required_action: `activate_t06`
- write_policy: `source_or_test_write`
- control_model: `gpt-5.6-sol`
- task_complexity: `medium`
- dispatch_role: `worker`
- dispatch_required: `true`
- dispatch_mode: `subagent`
- allowed_paths: `skills/go-developer/SKILL.md`, `skills/python-uv-project/SKILL.md`, `tests/test_go_developer_skill.py`, `tests/test_runtime_skill_verification_scope.py`
- forbidden_actions: 修改 T06-T08 范围、修改 `.factory/memory/**`、提交 Git、外部写入、回退他人改动
- code_shape_constraints: 禁止函数/方法内定义命名函数；禁止抽取仅一处调用且无独立职责的公共函数；代码修改必须返回 `code_shape_check: passed|failed`
- acceptance: 普通修改定向验证；批次/高风险/发布全量验证；未运行范围明确。

## Dispatch receipt

- dispatch_id: `SOFTWARE-ENGINEERING-SKILL-REMEDIATION-001:T05:terra-medium:v1`
- requested_model: `gpt-5.6-terra`
- requested_reasoning_effort: `medium`
- fork_turns: `none`
- agent_id: `/root/remediation_t05_worker`
- status: `accepted`
- source: `parent_tool_receipt`

## Verification

- `uv run pytest -q tests/test_go_developer_skill.py tests/test_runtime_skill_verification_scope.py`：7 passed，exit 0。
- `uv run ruff check tests/test_go_developer_skill.py tests/test_runtime_skill_verification_scope.py`：passed，exit 0。
- `git diff --check -- <T05 allowlist>`：passed，exit 0。
- code_shape_check: `passed`

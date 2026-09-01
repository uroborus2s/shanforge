# T04：会话人类事实合同

- task_card_id: `SOFTWARE-ENGINEERING-SKILL-REMEDIATION-001-T04`
- wbs_id: `WBS-REM-04`
- status: `completed`
- priority: `P0`
- task_scope: `system`
- depends_on: `T03`
- risk_level: `medium`
- execution_model: `gpt-5.6-terra`
- requested_reasoning_effort: `medium`
- execution_authorized: `true`
- current_gate: `closed`
- next_required_action: `activate_t05`
- write_policy: `source_or_test_write`
- control_model: `gpt-5.6-sol`
- task_complexity: `medium`
- dispatch_role: `worker`
- dispatch_required: `true`
- dispatch_mode: `subagent`
- allowed_paths: `skills/humanizer/SKILL.md`, `skills/brainstorming/SKILL.md`, `skills/using-shanforge/references/work-skill-return-contract.md`, `skills/using-shanforge/references/human-readable-status.md`, `tests/test_human_response_contract_integration.py`
- forbidden_actions: 修改 T05-T08 范围、修改 `.factory/memory/**`、提交 Git、外部写入、回退他人改动
- code_shape_constraints: 禁止函数/方法内定义命名函数；禁止抽取仅一处调用且无独立职责的公共函数；代码修改必须返回 `code_shape_check: passed|failed`
- acceptance: 开发、测试、Bug、修复四类回复包含必需事实并只有一个下一动作。

## Dispatch receipt

- dispatch_id: `SOFTWARE-ENGINEERING-SKILL-REMEDIATION-001:T04:terra-medium:v1`
- requested_model: `gpt-5.6-terra`
- requested_reasoning_effort: `medium`
- fork_turns: `none`
- agent_id: `/root/remediation_t04_worker`
- status: `accepted`
- source: `parent_tool_receipt`

## Verification

- `uv run pytest -q tests/test_human_response_contract_integration.py tests/test_brainstorming_skill.py tests/test_skill_progress_visibility_and_continuation.py tests/test_work_skill_status_envelope_ownership.py`：30 passed，exit 0。
- `uv run ruff check tests/test_human_response_contract_integration.py`：passed，exit 0。
- `git diff --check -- <T04 allowlist>`：passed，exit 0。
- code_shape_check: `passed`

# T03：子代理状态与验证证据

- task_card_id: `SOFTWARE-ENGINEERING-SKILL-REMEDIATION-001-T03`
- wbs_id: `WBS-REM-03`
- status: `completed`
- priority: `P0`
- task_scope: `system`
- depends_on: `T02`
- risk_level: `medium`
- execution_model: `gpt-5.6-terra`
- requested_reasoning_effort: `medium`
- execution_authorized: `true`
- current_gate: `closed`
- next_required_action: `activate_t04`
- write_policy: `source_or_test_write`
- control_model: `gpt-5.6-sol`
- task_complexity: `medium`
- dispatch_role: `worker`
- dispatch_required: `true`
- dispatch_mode: `subagent`
- allowed_paths: `skills/subagent-driven-development/SKILL.md`, `skills/verification-before-completion/**`, `skills/using-shanforge/references/work-skill-return-contract.md`, `tests/test_execution_workflow_skills.py`, `tests/test_verification_debugging_workflow_skills.py`, `tests/test_work_skill_status_envelope_ownership.py`
- forbidden_actions: 修改 T04-T08 范围、修改 `.factory/memory/**`、提交 Git、外部写入、回退他人改动
- code_shape_constraints: 禁止函数/方法内定义命名函数；禁止抽取仅一处调用且无独立职责的公共函数；代码修改必须返回 `code_shape_check: passed|failed`
- acceptance: worker 状态唯一映射；普通任务、批次和关闭声明使用正确 evidence 层级。

## Dispatch receipt

- dispatch_id: `SOFTWARE-ENGINEERING-SKILL-REMEDIATION-001:T03:terra-medium:v1`
- requested_model: `gpt-5.6-terra`
- requested_reasoning_effort: `medium`
- fork_turns: `none`
- agent_id: `/root/remediation_t03_worker`
- status: `accepted`
- source: `parent_tool_receipt`

## Verification

- `uv run pytest -q tests/test_execution_workflow_skills.py tests/test_verification_debugging_workflow_skills.py tests/test_work_skill_status_envelope_ownership.py`：31 passed，exit 0。
- `uv run ruff check tests/test_execution_workflow_skills.py tests/test_verification_debugging_workflow_skills.py tests/test_work_skill_status_envelope_ownership.py`：passed，exit 0。
- `git diff --check -- <T03 allowlist>`：passed，exit 0。
- code_shape_check: `passed`

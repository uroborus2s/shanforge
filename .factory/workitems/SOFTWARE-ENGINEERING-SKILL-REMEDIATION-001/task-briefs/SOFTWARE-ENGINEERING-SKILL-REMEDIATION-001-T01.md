# T01：WBS 与任务身份合同

- task_card_id: `SOFTWARE-ENGINEERING-SKILL-REMEDIATION-001-T01`
- wbs_id: `WBS-REM-01`
- status: `completed`
- priority: `P0`
- task_scope: `system`
- depends_on: `none`
- risk_level: `medium`
- execution_model: `gpt-5.6-terra`
- requested_reasoning_effort: `medium`
- execution_authorized: `true`
- current_gate: `closed`
- next_required_action: `activate_t02`
- write_policy: `source_or_test_write`
- control_model: `gpt-5.6-sol`
- task_complexity: `medium`
- dispatch_role: `worker`
- dispatch_required: `true`
- dispatch_mode: `subagent`
- allowed_paths: `skills/writing-plans/**`, `skills/project-memory/references/**`, `tests/test_writing_plans_skill.py`, `tests/test_project_memory_skill.py`, `tests/test_using_shanforge_snapshot.py`
- forbidden_actions: 修改 T02-T08 范围、修改 `.factory/memory/**`、提交 Git、外部写入、回退他人改动
- code_shape_constraints: 禁止函数/方法内定义命名函数；禁止抽取仅一处调用且无独立职责的公共函数；代码修改必须返回 `code_shape_check: passed|failed`
- acceptance: 模板生成的 WBS、TaskCard、ledger 和 session 身份可被快照一致读取；缺字段失败。

## Dispatch receipt

- dispatch_id: `SOFTWARE-ENGINEERING-SKILL-REMEDIATION-001:T01:terra-medium:v1`
- requested_model: `gpt-5.6-terra`
- requested_reasoning_effort: `medium`
- fork_turns: `none`
- agent_id: `/root/remediation_t01_worker`
- status: `accepted`
- source: `parent_tool_receipt`

## Verification

- `uv run pytest -q tests/test_writing_plans_skill.py tests/test_project_memory_skill.py tests/test_using_shanforge_snapshot.py`：31 passed，4 subtests passed，exit 0。
- `uv run ruff check tests/test_writing_plans_skill.py tests/test_project_memory_skill.py tests/test_using_shanforge_snapshot.py`：passed，exit 0。
- `git diff --check -- <T01 allowlist>`：passed，exit 0。
- code_shape_check: `passed`

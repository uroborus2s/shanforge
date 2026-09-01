# T02：状态语义分层

- task_card_id: `SOFTWARE-ENGINEERING-SKILL-REMEDIATION-001-T02`
- wbs_id: `WBS-REM-02`
- status: `completed`
- priority: `P0`
- task_scope: `system`
- depends_on: `T01`
- risk_level: `medium`
- execution_model: `gpt-5.6-terra`
- requested_reasoning_effort: `medium`
- execution_authorized: `true`
- current_gate: `closed`
- next_required_action: `activate_t03`
- write_policy: `source_or_test_write`
- control_model: `gpt-5.6-sol`
- task_complexity: `medium`
- dispatch_role: `worker`
- dispatch_required: `true`
- dispatch_mode: `subagent`
- allowed_paths: `skills/writing-plans/references/task-brief-template.md`, `skills/requesting-code-review/references/task-review-template.md`, `skills/using-shanforge/scripts/project_snapshot.py`, `skills/using-shanforge/references/pm-dashboard-rendering.md`, `tests/test_using_shanforge_snapshot.py`, `tests/test_review_workflow_skills.py`
- code_symbols: `project_snapshot._category`, `project_snapshot._effective_event`, `project_snapshot._plan_stages`
- forbidden_actions: 修改 T03-T08 范围、修改 `.factory/memory/**`、提交 Git、外部写入、回退他人改动
- code_shape_constraints: 禁止函数/方法内定义命名函数；禁止抽取仅一处调用且无独立职责的公共函数；代码修改必须返回 `code_shape_check: passed|failed`
- acceptance: review approved 不增加产品完成度；TaskCard completed/closed 才完成。

## Dispatch receipt

- dispatch_id: `SOFTWARE-ENGINEERING-SKILL-REMEDIATION-001:T02:terra-medium:v1`
- requested_model: `gpt-5.6-terra`
- requested_reasoning_effort: `medium`
- fork_turns: `none`
- agent_id: `/root/remediation_t02_worker`
- status: `accepted`
- source: `parent_tool_receipt`

## Verification

- `uv run pytest -q tests/test_using_shanforge_snapshot.py tests/test_review_workflow_skills.py`：19 passed，4 subtests passed，exit 0。
- `uv run ruff check skills/using-shanforge/scripts/project_snapshot.py tests/test_using_shanforge_snapshot.py tests/test_review_workflow_skills.py`：passed，exit 0。
- `git diff --check -- <T02 allowlist>`：passed，exit 0。
- code_shape_check: `passed`

# T07：版本化生态探测

- task_card_id: `SOFTWARE-ENGINEERING-SKILL-REMEDIATION-001-T07`
- wbs_id: `WBS-REM-07`
- status: `completed`
- priority: `P1`
- task_scope: `system`
- depends_on: `T06`
- risk_level: `medium`
- execution_model: `gpt-5.6-terra`
- requested_reasoning_effort: `medium`
- execution_authorized: `true`
- current_gate: `closed`
- next_required_action: `activate_t08_quality_gate`
- write_policy: `source_or_test_write`
- control_model: `gpt-5.6-sol`
- task_complexity: `medium`
- dispatch_role: `worker`
- dispatch_required: `true`
- dispatch_mode: `subagent`
- allowed_paths: `skills/crawler4j-model-project/SKILL.md`, `skills/stratix-service/SKILL.md`, `skills/stratix-admin-web/SKILL.md`, `tests/test_crawler4j_model_skill_integration.py`, `tests/test_stratix_service_skill.py`, `tests/test_stratix_service_framework_guide.py`, `tests/test_stratix_admin_web_skill.py`
- forbidden_actions: 修改 T08 范围、修改 `.factory/memory/**`、提交 Git、外部写入、安装或升级生态依赖、回退他人改动
- code_shape_constraints: 禁止函数/方法内定义命名函数；禁止抽取仅一处调用且无独立职责的公共函数；代码修改必须返回 `code_shape_check: passed|failed`
- acceptance: 版本匹配才继续；未知或不兼容版本明确 blocked 并报告差异。

## Dispatch receipt

- dispatch_id: `SOFTWARE-ENGINEERING-SKILL-REMEDIATION-001:T07:terra-medium:v1`
- requested_model: `gpt-5.6-terra`
- requested_reasoning_effort: `medium`
- fork_turns: `none`
- agent_id: `/root/remediation_t07_worker`
- status: `accepted`
- source: `parent_tool_receipt`

## Verification

- `uv run pytest -q tests/test_crawler4j_model_skill_integration.py tests/test_stratix_service_skill.py tests/test_stratix_service_framework_guide.py tests/test_stratix_admin_web_skill.py`：30 passed，exit 0。
- `uv run ruff check tests/test_crawler4j_model_skill_integration.py tests/test_stratix_service_skill.py tests/test_stratix_service_framework_guide.py tests/test_stratix_admin_web_skill.py`：passed，exit 0。
- `git diff --check -- <T07 allowlist>`：passed，exit 0。
- code_shape_check: `passed`

# T06：外部工具能力探测

- task_card_id: `SOFTWARE-ENGINEERING-SKILL-REMEDIATION-001-T06`
- wbs_id: `WBS-REM-06`
- status: `completed`
- priority: `P1`
- task_scope: `system`
- depends_on: `T05`
- risk_level: `medium`
- execution_model: `gpt-5.6-terra`
- requested_reasoning_effort: `medium`
- execution_authorized: `true`
- current_gate: `closed`
- next_required_action: `activate_t07`
- write_policy: `source_or_test_write`
- control_model: `gpt-5.6-sol`
- task_complexity: `medium`
- dispatch_role: `worker`
- dispatch_required: `true`
- dispatch_mode: `subagent`
- allowed_paths: `skills/art-asset-pipeline/SKILL.md`, `skills/browser-control/SKILL.md`, `skills/docx/SKILL.md`, `skills/pdf/SKILL.md`, `skills/xlsx/SKILL.md`, `tests/test_browser_control_skill.py`, `tests/test_external_tool_skill_fallbacks.py`
- forbidden_actions: 修改 T07-T08 范围、修改 `.factory/memory/**`、提交 Git、外部写入、安装工具或依赖、回退他人改动
- code_shape_constraints: 禁止函数/方法内定义命名函数；禁止抽取仅一处调用且无独立职责的公共函数；代码修改必须返回 `code_shape_check: passed|failed`
- acceptance: 工具缺失时明确 blocked 和唯一解决动作，不输出不可执行命令。

## Dispatch receipt

- dispatch_id: `SOFTWARE-ENGINEERING-SKILL-REMEDIATION-001:T06:terra-medium:v1`
- requested_model: `gpt-5.6-terra`
- requested_reasoning_effort: `medium`
- fork_turns: `none`
- agent_id: `/root/remediation_t06_worker`
- status: `accepted`
- source: `parent_tool_receipt`

## Verification

- `uv run pytest -q tests/test_browser_control_skill.py tests/test_external_tool_skill_fallbacks.py`：7 passed，exit 0。
- `uv run ruff check tests/test_browser_control_skill.py tests/test_external_tool_skill_fallbacks.py`：passed，exit 0。
- `git diff --check -- <T06 allowlist>`：passed，exit 0。
- `remove_chroma_key.py` 仓内不存在性检查：passed，exit 0。
- code_shape_check: `passed`

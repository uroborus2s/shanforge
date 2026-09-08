# 主会话模型选择与子任务派发合同解耦

- work_item_id: `MODEL-ORCHESTRATOR-SELECTION-001`
- task_card_id: `MODEL-ORCHESTRATOR-SELECTION-001-T01`
- wbs_id: `WBS-MODEL-ORCHESTRATOR-01`
- status: `closed`
- current_gate: `closed`
- write_policy: `source_or_test_write`
- control_model: `user_selected`
- task_complexity: `simple`
- risk_level: `low`
- execution_model: `gpt-5.6-luna`
- execution_authorized: `true`
- dispatch_role: `worker`
- dispatch_required: `true`
- dispatch_mode: `subagent`
- requested_reasoning_effort: `low`
- fork_turns: `none`

## 允许修改

- `AGENTS.md`
- `.codex/config.toml`
- `.codex/agents/luna-worker.toml`
- `.codex/agents/terra-worker.toml`
- `skills/using-shanforge/SKILL.md`
- `skills/using-shanforge/agents/openai.yaml`
- `skills/using-shanforge/references/codex-tools.md`
- `skills/using-shanforge/references/black-box-flow-eval.md`
- `skills/subagent-driven-development/SKILL.md`
- `skills/subagent-driven-development/references/status-handling-checklist.md`
- `skills/writing-plans/references/task-brief-template.md`
- `skills/writing-plans/SKILL.md`
- `docs/02-user-guide/user-guide.md`
- `docs/04-product/prd.md`
- `docs/05-design/workflow-execution-design.md`
- `docs/document-index.md`
- `tests/test_model_tier_routing.py`
- `tests/test_execution_workflow_skills.py`
- `tests/test_full_project_session_workflow_routing.py`
- `tests/test_lifecycle_governance.py`
- `tests/test_delivery_status_review_behavior.py`
- `.factory/workitems/FLOW-STATUS-REVIEW-001/evidence/candidate-sha256.txt`

## 禁止动作

- 不改写历史 WorkItem 的原始证据、ledger 或版本说明；已误改的历史 manifest 只允许精确恢复原值。
- 不改变 Luna/Terra worker 与 Terra reviewer 的模型映射、推理强度或沙箱。
- 不新增依赖、抽象、兼容层或主会话默认模型。
- 不提交、不推送、不自批 review。

## TDD 与验证

1. 先修改定向测试，使旧的主会话 Sol 固定配置失败。
2. 运行 `uv run pytest -q tests/test_model_tier_routing.py`，记录 RED。
3. 最小修改配置、当前合同和正式文档。
4. 运行 `uv run pytest -q tests/test_model_tier_routing.py`。
5. 运行 `uv run ruff check tests/test_model_tier_routing.py`。
6. 运行 `git diff --check`。

## 完成口径

返回 `DONE`、实际修改文件、RED/GREEN 命令与结果、concerns；不得宣称 review 或项目完成。

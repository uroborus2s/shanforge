# 候选检索与保护正式规则

- work_item_id: `UI-VISUAL-QUALITY-001`
- task_card_id: `UI-VISUAL-QUALITY-001-T01`
- wbs_id: `WBS-UI-VISUAL-QUALITY-01`
- status: `closed`
- priority: `P0`
- task_scope: `system`
- owner: `script-worker`
- depends_on: `none`
- review_status: `approved`
- current_gate: `closed`
- next_required_action: `none`
- workflow_id: `execution-workflow`
- write_policy: `source_or_test_write`
- control_model: `gpt-5.6-sol`
- task_complexity: `complex`
- risk_level: `high`
- execution_model: `gpt-5.6-terra`
- execution_authorized: `true`
- dispatch_role: `worker`
- dispatch_required: `true`
- dispatch_mode: `subagent`
- requested_reasoning_effort: `medium`
- fork_turns: `none`
- route_reason: 公布的 CLI 输出与持久化行为变化；用户已批准根因及改法，计划审核后执行。
- escalation_triggers: `scope_expanded | input_conflict | risk_increased | verification_failed_twice | human_gate`

## 允许修改

- `skills/ui-ux-pro-max/scripts/core.py`
- `skills/ui-ux-pro-max/scripts/design_system.py`
- `skills/ui-ux-pro-max/scripts/search.py`
- `tests/test_ui_design_candidates.py`

## 目标与验证

消费 plan 的共享 CLI 契约。保留命令名与已有查询能力，把设计系统输出改为来源可追溯候选；不注入未知默认，不覆盖正式文件。先添加失败测试，使用 `uv run pytest tests/test_ui_design_candidates.py -q` 证明红绿；运行 code shape 和差异检查。

## 禁止

不得修改写集以外文件、CSV、依赖、治理事实或他人改动；不得 commit/push/切分支。不得定义函数体内命名函数；单调用点且无独立职责的 helper 保持内联。不是独占代码库，须兼容其他 worker 的修改。只回报真实命令、exit code、改动文件和 concerns，不自批 review。

# 美术学习与设计流程

- work_item_id: `UI-VISUAL-QUALITY-001`
- task_card_id: `UI-VISUAL-QUALITY-001-T02`
- wbs_id: `WBS-UI-VISUAL-QUALITY-02`
- status: `closed`
- priority: `P0`
- task_scope: `system`
- owner: `design-worker`
- depends_on: `none`
- review_status: `approved`
- current_gate: `closed`
- next_required_action: `none`
- workflow_id: `execution-workflow`
- write_policy: `source_or_test_write`
- control_model: `gpt-5.6-sol`
- task_complexity: `complex`
- risk_level: `medium`
- execution_model: `gpt-5.6-terra`
- execution_authorized: `true`
- dispatch_role: `worker`
- dispatch_required: `true`
- dispatch_mode: `subagent`
- requested_reasoning_effort: `medium`
- fork_turns: `none`
- route_reason: 多文件设计流程与交付约束重构，需中文措辞和可执行性评审。
- escalation_triggers: `scope_expanded | input_conflict | risk_increased | verification_failed_twice | human_gate`

## 允许修改

- `skills/ui-ux-pro-max/SKILL.md`
- `skills/ui-ux-pro-max/references/visual-direction-and-quality.md`
- `skills/ui-ux-pro-max/references/design-workflow-and-deliverables.md`
- `skills/ui-ux-pro-max/references/mobile-high-fidelity.md`
- `skills/ui-ux-pro-max/references/cross-platform.md`
- `skills/ui-ux-pro-max/references/admin-web.md`
- `skills/ui-ux-pro-max/references/open-source-landscape.md`
- `tests/test_ui_ux_pro_max_skill.py`
- `tests/fixtures/ui-design-briefs.json`
- `docs/02-user-guide/user-guide.md`
- `docs/02-user-guide/prompt-templates.md`
- `skills/ui-ux-pro-max/examples/omnichannel-service-platform/README.md`

## 目标与验证

落实 brief 与 plan 的设计工作流、优秀案例学习、素材、跨端、中文美术评审。核心非通用指令留入口，细则集中一个新参考；按任务读取，不制造模板大全或新平台。交付 12 个设计 brief，包含任务模式、平台、中文内容、既有基线和可观察验证要求。更新受影响测试并运行 `uv run pytest tests/test_ui_ux_pro_max_skill.py -q`、skill validator 和 diff check。

## 禁止

不得改脚本、CSV、依赖、批准素材、其他测试或治理文件；不得 commit/push/切分支。不得以来源标题或 AI 自评声称完成视觉学习；写清实际观察与未知。不是独占代码库，保留其他 worker 改动。不得定义局部命名函数或无独立职责的单调用 helper。不自批 review。

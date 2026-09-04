# UI-DESIGN-WORKFLOW-001-T01：最小规则修改与中文评审

- work_item_id: `UI-DESIGN-WORKFLOW-001`
- task_card_id: `UI-DESIGN-WORKFLOW-001-T01`
- wbs_id: `WBS-UI-DESIGN-WORKFLOW-01`
- current_gate: `closed`
- write_policy: `source_or_test_write`
- risk_level: `low`
- task_complexity: `simple`
- execution_authorized: `true`

## 允许修改

- `skills/ui-ux-pro-max/references/design-workflow-and-deliverables.md`
- `skills/using-shanforge/SKILL.md`
- `tests/test_ui_ux_pro_max_skill.py`
- `.factory/workitems/UI-DESIGN-WORKFLOW-001/`
- `.factory/memory/agent-session.md`
- `.factory/memory/current-state.md`
- `.factory/memory/skill-updates.summary.md`
- `.factory/memory/tasks.summary.md`
- `.factory/memory/tests.summary.md`
- `.factory/memory/review-ledger.jsonl`

## 禁止动作

- 不修改 `skills/art-asset-pipeline/`。
- 不修改 `skills/ui-ux-pro-max/references/mobile-high-fidelity.md`。
- 不新增依赖、脚本、模板或设计资产。
- 不执行远端 push、PR、发布或历史改写。
- 实现者不得自批评审通过。

## 验证

- 先增加会失败的最小语义断言，再修改规则文本。
- 运行 `tests/test_ui_ux_pro_max_skill.py` 及直接相关流程测试。
- 独立中文语言专家只读评审最终 diff；如有成立意见，仅在上述范围内精简并复验。

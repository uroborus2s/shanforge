# 独立只读评审任务

- work_item_id: `MODEL-ORCHESTRATOR-SELECTION-001`
- task_card_id: `MODEL-ORCHESTRATOR-SELECTION-001-T01`
- reviewer_type: `independent_subagent`
- candidate: 工作树 diff `c6de645995b2b7c852e48c17f9c16776da4e5cb6be755e7b4025f472a5daf491`
- write_policy: `state_or_gate_write`
- current_gate: `review`

## 目标与验收

审查主会话模型是否真正由用户选择，同时父会话对子任务的控制职责保持完整且不再绑定 Sol。确认现有 Luna/Terra worker 与 Terra reviewer 映射、推理强度、沙箱和失败关闭未被破坏；正式文档、Skill、配置与测试一致。

## 必读

- `.factory/workitems/MODEL-ORCHESTRATOR-SELECTION-001/brief.md`
- `.factory/workitems/MODEL-ORCHESTRATOR-SELECTION-001/reports/implementation-summary.md`
- `.factory/workitems/MODEL-ORCHESTRATOR-SELECTION-001/evidence/implementation-and-targeted-verification.md`
- 本任务 15 个实现文件的工作树 diff。

## 排除与禁止

- 只读，不修改任何文件、Git、ledger 或外部系统。
- 不审查或吸收 `.factory/workitems/MODEL-DYNAMIC-DISPATCH-001/` 与 `tests/test_dynamic_model_dispatch.py`；它们属于另一任务且当前 RED 为预期。
- 不要求本任务实现 GPT-6 动态子任务路由。

## 输出

按 findings 优先返回；每项含 severity、文件/行、证据和建议。无 Critical/Important 时返回 `approved`，否则 `changes_requested`。明确 `human_confirmation_required` 与原因。

# T13-R06：迁移当前工作项 TaskCard 依赖合同

- task_card_id: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001-T13-R06`
- wbs_id: `WBS-AUDIT-13-R06`
- status: `completed`
- owner: `gpt-5.6-sol`
- depends_on: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001-T13-R02,SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001-T13-R03,SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001-T13-R04,SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001-T13-R05`
- current_gate: `closed`
- next_required_action: `final_PM_rereview`
- write_policy: `state_or_gate_write`
- execution_authorized: `true`

## 根因与验收

新模板已要求 owner 和完整 TaskCard ID 依赖，但本工作项 T09–T13/R01–R05 仍保留旧字段。迁移全部卡；事件前置条件保留在 ledger，不混入 DAG。对实际 `task-briefs/*.md` 运行 `validate_task_graph.py`，缺 owner、未知、自依赖、环或不一致均失败。

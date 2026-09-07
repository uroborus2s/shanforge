# 集中验证和独立评审
- work_item_id: UI-CLIENT-CRAFT-001
- task_card_id: UI-CLIENT-CRAFT-001-T03
- wbs_id: WBS-UI-CRAFT-03
- 状态：closed
- owner: coordinator
- depends_on: UI-CLIENT-CRAFT-001-T01, UI-CLIENT-CRAFT-001-T02
- review_status: approved
- 优先级：P1
- 任务层级：system
- 关联目标：UI-CLIENT-CRAFT-001
- 强关系：DEPENDS_ON
- 上游计划：.factory/workitems/UI-CLIENT-CRAFT-001/plan.md
- 流水账：.factory/workitems/UI-CLIENT-CRAFT-001/ledger.jsonl
- current_gate: closed
- next_required_action: create_exact_local_commit
## 范围
集中检查技能合同、案例数据、样板截图/内容/导航与中文术语；作者不自批。独立 reviewer 的身份、只读范围、Terra high 派发另以 review brief 登记。
运行目标 pytest、Ruff、skill validator、代码形状与 diff check，最终运行全仓 pytest 确认治理事实一致。API、服务、支付、真机均不在本次修改范围，不伪称已验证。
精确写集为本 work item evidence/reports/reviews/ledger/plan/task-briefs 与 .factory/memory/agent-session.md、current-state.md、tasks.summary.md、tests.summary.md、skill-updates.summary.md，以及 requesting-code-review 要求的 review-ledger.jsonl 当前工作项追加事件。
技能实现与样板作为未批准候选的归档可独立收口；正式将样板用于 ita-club、替换原稿/产物需要用户视觉批准和另行业务修改授权。

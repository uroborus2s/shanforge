# UI skill 与迁移候选独立评审

- work_item_id: UI-CLIENT-CRAFT-001
- task_card_id: UI-CLIENT-CRAFT-001-T03
- wbs_id: WBS-UI-CRAFT-03
- dispatch_id: UI-CLIENT-CRAFT-001-T03-reviewer-v1
- workflow_id: review-workflow
- write_policy: readonly
- current_gate: needs_independent_review
- control_model: gpt-5.6-sol
- task_complexity: standard
- risk_level: medium
- execution_model: gpt-5.6-terra
- requested_reasoning_effort: high
- execution_authorized: true
- dispatch_role: reviewer
- dispatch_required: true
- dispatch_mode: subagent
- fork_turns: none
- route_reason: 批次独立质量门；实现者不能替代规则、代码和画面裁判
- escalation_triggers: scope_expanded, input_conflict, risk_increased, verification_failed_twice, human_gate

## 只读输入包

- 本工作项 brief.md、plan.md、三个 task-briefs、ledger.jsonl、evidence/final-verification.md、evidence/pilot/、reviews/dispatch-receipts.jsonl。
- 本次 git diff：skills/ui-ux-pro-max/SKILL.md、references/visual-direction-and-quality.md、mobile-high-fidelity.md、design-workflow-and-deliverables.md、docs/02-user-guide/user-guide.md、tests/test_ui_ux_pro_max_skill.py、tests/fixtures/ui-craft-cases.json。
- skills/ui-ux-pro-max/ 适用平台参考与 requesting-code-review 的 rubric；相关 memory 顶部和当前工作项 review ledger 记录。
- 只读原稿 /Users/uroborus/NodeProject/ita-club/docs/ui/miniapp-handoff/flow-redesign/coach/ 的 design.md、data.js、index.html、styles.css、workbench-390.png、schedule-390.png、student-detail-390.png；只读取三页相关事实，勿输出凭证样例。

## 任务与输出

只读审查，不参与实现；不继承作者会话或直接相信自评。实际读 diff 和预览候选截图，对照原稿及源事实。检查需求符合度、中文准确与篇幅、参考学习边界、是否把组件统一变成页面模板、已批准/局部修复是否误触全套流程、验收是否虚报、可移植性、对象/状态/导航和验证缺口。规则与候选代码是工程评审；画面评价单独说明可见优缺点，不能以通过测试或工程评分证明美术好看。

返回中文结论与可定位 Finding，按现有 rubric 写五项工程评分、reviewer_type/id/independence_evidence、approved 或 changes_requested、C/I/M 计数、human_confirmation_required 和原因。不要写任何文件、ledger、memory、Git 或外部系统；由主控落盘你的原始结论。

边界：本轮交付 UI skill 修改与未批准候选归档，不采用候选到 ita-club。因此工程评审通过可以 return_to_orchestrator；正式产品采用、微信真机/完整状态与人工美术认可均仍需另行验收。不要制造本轮未声明的人工 Gate，也不得冒充人工批准。未运行的多场景或 A/B 必须诚实列出。

# 集中验证、独立评审与交付

- work_item_id: `UI-VISUAL-QUALITY-001`
- task_card_id: `UI-VISUAL-QUALITY-001-T03`
- wbs_id: `WBS-UI-VISUAL-QUALITY-03`
- status: `closed`
- priority: `P0`
- task_scope: `system`
- owner: `parent-controller`
- depends_on: `UI-VISUAL-QUALITY-001-T01, UI-VISUAL-QUALITY-001-T02`
- review_status: `approved`
- current_gate: `closed`
- next_required_action: `none`
- workflow_id: `review-workflow`
- write_policy: `state_or_gate_write`
- control_model: `gpt-5.6-sol`
- task_complexity: `complex`
- risk_level: `high`
- execution_model: `gpt-5.6-terra`
- execution_authorized: `true`
- dispatch_role: `reviewer`
- dispatch_required: `true`
- dispatch_mode: `subagent`
- reviewer_type: `independent_subagent`
- requested_reasoning_effort: `high`
- fork_turns: `none`
- route_reason: 对已完成的计划及其后实现进行隔离只读审核，不参与实现。
- escalation_triggers: `scope_expanded | input_conflict | risk_increased | human_gate`

## 范围

只读 T01/T02 全部允许文件、当前 work item、相关架构与旧行为测试。父控制器可以写当前 work item 和 agent-session/current-state/tasks/tests/skill-updates/review-ledger 的本任务事实。reviewer 不写任何文件、不修改代码、不自批实现、不提交。

## 验收

计划完成后检查 CLI 参数、候选与正式状态、持久化、分工和验证策略。实现后基于新鲜完整必需测试与 diff 做独立代码、语义及中文质量评审；必要前向测试在临时目录生成可审阅结果。修复 Critical/Important 后复审受影响范围。真实 UI 画面盲评未运行则明确披露，不能用 pytest 或 rubric 替代美术验收。

# 独立前向试用与集中评审

- work_item_id: MODEL-DYNAMIC-DISPATCH-001
- task_card_id: MODEL-DYNAMIC-DISPATCH-001-T03
- wbs_id: WBS-MODEL-DYNAMIC-03
- status: ready_for_commit
- owner: independent_review
- priority: P1
- task_scope: system
- depends_on: T01 合同已落地；最终评审等待 T01/T02 完成和父验证
- review_status: approved
- current_gate: commit
- next_required_action: create_exact_local_commit
- write_policy: state_or_gate_write
- control_model: user_selected
- task_complexity: standard
- risk_level: medium
- reasoning_demand: judgment
- execution_model: gpt-5.6-terra
- requested_reasoning_effort: high
- execution_authorized: true
- dispatch_role: reviewer
- dispatch_required: true
- dispatch_mode: subagent
- fork_turns: none
- capability_source: current collaboration.spawn_agent terra-reviewer preset, Terra/high/read-only
- route_reason: 本地可回滚治理合同的独立行为与质量评审，选普通 reviewer 下限 High；不涉及生产权限实现。

只读输入为本批合同、测试、候选差异、验证和原始试用场景。试用者先只读 forward-input.md 与指定 skill，不读期望结果；只在回复中返回事实，由父会话保存原文。最终 reviewer 未参加实施或试用，复核候选、测试与中文可读性。任何 reviewer 禁止写文件/ledger/Git、禁止自改实现、禁止把测试模拟当真实派发或角色加载证明。

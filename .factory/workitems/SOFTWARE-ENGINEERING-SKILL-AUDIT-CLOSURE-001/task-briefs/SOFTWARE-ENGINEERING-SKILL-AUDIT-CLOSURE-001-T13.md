# T13：五专家复评与集中质量门

- task_card_id: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001-T13`
- wbs_id: `WBS-AUDIT-13`
- status: `completed`
- priority: `P0`
- task_scope: `system`
- owner: `gpt-5.6-sol`
- depends_on: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001-T12`
- risk_level: `medium`
- execution_authorized: `true`
- current_gate: `closed`
- next_required_action: `none`
- write_policy: `state_or_gate_write`
- control_model: `gpt-5.6-sol`
- task_complexity: `complex`
- execution_model: `gpt-5.6-terra`
- dispatch_role: `reviewer`
- dispatch_required: `true`
- dispatch_mode: `subagent`
- requested_reasoning_effort: `high`
- fork_turns: `none`
- route_reason: `五类独立只读 reviewer 覆盖 38 Skill、190 个评分和原始 45 Finding`
- allowed_paths: `.factory/workitems/SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001/{evidence,reports,reviews}/**`, `.factory/workitems/SOFTWARE-ENGINEERING-SKILL-AUDIT-001/reports/final-scorecard.md`, 本 TaskCard、plan、ledger；memory 仅在最终 Gate 通过后同步
- forbidden_actions: reviewer 写文件、覆盖原始分数、实现者自评、忽略 Critical/Important、修改 Skill/测试、远端或发布动作

## 验收

- 五类专家各自覆盖 38/38；合计 190/190 新评分。
- 45/45 原始 Finding 有 reviewer 关闭结论；新 Finding 有严重度和精确位置。
- 新评分表显示 before/after/delta/C-I-M/evidence/reason。
- 全量 pytest、Ruff、38/38 validator、45 项追踪、黑盒和 diff check 通过。
- Critical=0、Important=0 才能 `approved`。

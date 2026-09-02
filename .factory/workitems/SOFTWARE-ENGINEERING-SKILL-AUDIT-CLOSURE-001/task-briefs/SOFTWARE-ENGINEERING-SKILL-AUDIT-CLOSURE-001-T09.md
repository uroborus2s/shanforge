# T09：建立 45/45 原始问题闭环表与评分结构

- task_card_id: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001-T09`
- wbs_id: `WBS-AUDIT-09`
- status: `completed`
- priority: `P0`
- task_scope: `system`
- owner: `gpt-5.6-sol`
- depends_on: `none`
- risk_level: `medium`
- execution_authorized: `true`
- current_gate: `closed`
- next_required_action: `none`
- write_policy: `project_fact_write`
- control_model: `gpt-5.6-sol`
- task_complexity: `complex`
- execution_model: `gpt-5.6-terra`
- dispatch_role: `none`
- dispatch_required: `false`
- dispatch_mode: `direct`
- requested_reasoning_effort: `medium`
- fork_turns: `none`
- route_reason: `分析和登记项目事实，不修改 source/test；由总控直接写入工作项产物`
- allowed_paths: `.factory/workitems/SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001/**`
- forbidden_actions: 修改 Skill、测试、原始专家报告、原始评分、memory、Git、远端或发布状态

## 交付物

- `reports/finding-closure-matrix.md`：45/45 原始 Finding 逐项闭环表。
- `reports/post-remediation-scoring-rubric.md`：整改后评分结构、评分锚点和通过 Gate。
- `evidence/T09-count-and-trace-check.md`：五份报告 Finding 数量、唯一 ID 和追踪检查。

## 最小执行清单

1. 从五份原始专家报告逐条提取 Important 和 Minor，不以综合报告替代原始项。
2. 分配稳定 ID：`ZH-I01`、`SD-I01`、`SE-I01`、`PM-I01`、`CM-I01` 等；保留原文语义。
3. 对照提交 `07c23b6` 和当前文件，标记 `verified_fixed / unresolved / partially_fixed / rejected_with_reason`。
4. 每项写精确文件和函数/章节；没有代码函数时写文档章节，不编造符号。
5. 冻结整改后评分表字段：整改前、整改后、变化、C/I/M、证据和理由；评分不能覆盖质量 Gate。
6. 校验总数必须等于 Important 27、Minor 18、总计 45；每个 ID 唯一且有来源。

## 验收

- `45/45` 可追踪，`I=27`、`M=18`。
- 没有“已映射”“已处理”等无证据状态。
- 所有未关闭项能直接生成 T10–T12 的精确写集和测试目标。
- T09 不修改 Skill、源码或测试。

## 完成结果

- 原始 Finding：45/45；Important 27、Minor 18。
- 当前状态：verified_fixed 16、partially_fixed 7、unresolved 21、rejected_with_reason 1。
- 未独立关闭：29；其中 T10 7、T11 11、T12 10、T13 判断不采纳理由 1。
- 证据：`reports/finding-closure-matrix.md`、`reports/post-remediation-scoring-rubric.md`、`evidence/T09-count-and-trace-check.md`。

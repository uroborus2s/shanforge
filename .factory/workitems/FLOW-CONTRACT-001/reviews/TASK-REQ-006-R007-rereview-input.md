# TASK-REQ-006 R007 同一 Reviewer 复审输入

- reviewer_id: `/root/req006_r005_review`
- 只读输入：R006 review、R007 triage/response、R007 Markdown、R007 contract、R007 PM field map、pinned R014、R007 verification、AGENTS.md。
- 逐项验证 `R006-I-001..003`、`R006-N-001` closed/open/regressed。
- 必须实际验证：R014 record identity；137 value Owner；Markdown/JSON 16/64/11 逐字段和 Hash；10 非终态、50 `(state,event)` 精确覆盖、成功发布 fencing、终态可达；Snapshot v2 唯一性。
- Critical/Important 非空必须 changes_requested；approved 也只能进入精确 Hash 人工确认，不能批准设计/实现。

# TASK-REQ-006 R009 同一 Reviewer 事实修正复审输入

- reviewer_id: `/root/req006_r005_review`
- 只读输入：R008 approved review、R009 fact correction、R009 Markdown/contract/field map、R014 release manifest、R014 machine contract、R009 verification、AGENTS.md。
- 验证 R014 `candidate_unapproved` 只是 frozen internal status，current release status 由 manifest/ledger 为 `released`；manifest 的 approved machine contract Hash 与 pinned R014 相等。
- 独立重算 R009 16/64/11、23720 bytes、root `d917dce3…d5de`；回归 137 fields、50 transitions、Snapshot v2、架构/Git/候选隔离。
- 有 C/I 必须 changes_requested；否则 approved，只进入精确 Hash 人工确认。

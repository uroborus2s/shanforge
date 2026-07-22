# TASK-REQ-006 R009 R014 发布状态事实修正

R008 review 输入只读取 R014 机器合同，因此把其冻结内部字段 `candidate_unapproved` 当成当前发布状态。仓库权威事实表明 R014 已经由 `uroborus` 人工批准并在 2026-07-15 正式发布：

- release manifest：`.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-REQ-002-R014-release-manifest.json`
- manifest SHA-256：`ea84805f62b9c20d17f625e0e4f68efcd510c19897cc1b5c8ebacf70a5bdef4e`
- status：`released`
- human approval key：`FLOW-CONTRACT-001:TASK-REQ-002:R014:human-formalization-approved:v1`
- approved machine contract SHA-256：`836fadc2c214ef2f56b2a21ef2fb705445a58ca7ddb0047f3b638292ba578d33`
- formal PRD：v3.1.0。

R009 不改变 R008 已评审的产品语义，只把“内部冻结状态”和“当前正式发布状态”分开，并把 release manifest 纳入精确 pin。该事实修正仍需同一 Reviewer 做回归确认；R008 approved 不直接沿用为 R009 approved。

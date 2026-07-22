# TASK-REQ-006 R006 评审整改报告

## 结果

R005 独立评审的 1 个 Critical 和 6 个 Important 已形成 R006 完整替代候选。整改没有扩大到正式设计、产品代码、Git 远端或 `TASK-IMPLEMENT-002-R001`。

## 核心变化

1. 将不可实现的“离线复制件可撤权”改为 local-owner 与 shared-restricted 两种可测试 profile。
2. 精确固定 R014 输入并承认其尚未批准。
3. 增加 137 字段逐项 PM Owner 映射。
4. 统一 `as_of`、`built_at`、页面 Hash 与 fingerprint。
5. 将稳定 `symbol_id` 与可变代码 locator 分离。
6. 将 REQ/AC/NFR 语义写入机器合同。
7. 关闭 durable 状态机的转移、重试、失租和无提交权限路径。

## 状态

`ready_for_same_reviewer_rereview`。复审通过前 `design_or_implementation_authorized=false`。

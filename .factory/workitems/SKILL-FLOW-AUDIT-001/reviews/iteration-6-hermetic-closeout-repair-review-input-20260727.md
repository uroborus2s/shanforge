# Iteration 6 隔离关闭门修复独立评审输入

- Work item：`SKILL-FLOW-AUDIT-001`
- Task：`iteration-6-hermetic-closeout-repair`
- Review：任务级 Spec + Quality Review

## Inputs

1. `task-briefs/iteration-6-hermetic-closeout-repair.md`
2. `task-briefs/iteration-6-minimal-acceptance-amendment.md`
3. `evidence/iteration-6-hermetic-closeout-repair-blocker-20260727.md`
4. `evidence/iteration-6-hermetic-closeout-repair-verification-20260727.md`
5. `reports/iteration-6-hermetic-closeout-repair-report-20260727.md`
6. `tests/test_skill_flow_process_audit.py` 当前限定 diff
7. WorkItem ledger E109-E112

## 评审重点

- 两个专属节点是否只读取各自候选。
- 9 个关闭节点是否只读取 8 个候选或共享合同。
- 原聚合断言的其他行为是否保留。
- 9 个冻结 SHA-256 是否一致。
- 测试、Ruff、JSONL 和 diff-check 是否真实通过。
- 产品、API、数据库、UI、发布 N/A 是否合理。

## 边界

Reviewer 只读，不修改文件、Git index 或外部系统。输出 `approved` 或
`changes_requested`，包含评分、C/I/M、独立性证据与 N/A 裁决。

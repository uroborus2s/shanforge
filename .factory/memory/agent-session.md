# Agent 会话卡

- 生成时间：2026-07-27 12:50 +0800
- 项目：`shanforge`
- 当前阶段：`FLOW-CONTRACT-001 / FLOW-TASK-015 / IMPLEMENTATION`
- 当前状态：`approved_ready_for_exact_local_commit`
- 当前焦点：完整软件项目会话归因契约精确本地提交
- 下一动作：按 hunk 暂存 FLOW-TASK-015，完整核对 staged diff 后本地提交；
  不执行 Push、PR、Merge 或部署

## 当前事实

- `FLOW-TASK-015` 是 `FLOW-CONTRACT-001` 第 15/15 项。
- 冻结候选 SHA-256：
  `3d5f4cbabda86312da0603db5662175453d12dd5966c788301b0c79c2cb4992f`。
- 正式基线 SHA-256：
  `5769beb3478d528a0b0888328381173aa799e1e137925fc393bd98d97d3eb687`。
- 方案独立复审：`approved / 98 / C0-I0-M1`；语义 Finding 全部关闭。
- 用户已明确回复“确认方案，开始正式实施”，授权正式版本发布、runtime Skill 同步、
  验证、独立实现 Review、同范围整改和全部 Gate 通过后的精确本地提交。
- 唯一正式文档已在工作树原位晋升为 `v1.2.0`；9 个 runtime Skills 已同步最小合同。
- 正式实施验证：Runtime Red/Green `1 failed, 7 passed -> 8 passed`，规定组合 `57 passed`，
  Ruff 通过，Skill validator `9/9`。
- 首轮实现 Review：`changes_requested / 76 / C0-I3-M0`；旧自动人工 Gate、测试假通过和状态投影
  三项已完成同范围整改，整改 Red 为 `2 failed, 6 passed`。
- 同一 Reviewer 实现复审：`approved / 98 / C0-I0-M0`，三项 Finding 全部关闭。
- 远端、Push、PR、Merge 和部署未授权。
- 此前把用户“继续下一步”误归因到 `PK-SOURCE-MIGRATION-001-T04`；已追加纠正事件，
  两份设计文档恢复未发布候选状态，误路由诊断产物仅保留审计且排除本主线提交。

## 最小读取顺序

1. 本文件。
2. `.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-015.md`。
3. `.factory/workitems/FLOW-CONTRACT-001/drafts/FLOW-TASK-015-workflow-contract.v1.2.0.candidate.md`。
4. `.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl` 最新事件。
5. 仅按任务允许范围读取目标 Skill 和测试。

## 当前 Gate

人工方案 Gate 和独立实现 Review Gate 已关闭。当前无停止原因；只执行已授权的精确本地提交。

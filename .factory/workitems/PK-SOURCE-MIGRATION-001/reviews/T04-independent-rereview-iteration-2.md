# T04 独立复审（Iteration 2）

- Work item: `PK-SOURCE-MIGRATION-001`
- Task: `PK-SOURCE-MIGRATION-001-T04`
- reviewer_type: `independent_subagent`
- reviewer_id: `/root/project_knowledge_review`
- reviewer_independence_evidence: 本 reviewer 未参与原实现或整改；仅复核指定整改文件、
  相关限定 diff，并运行只读定向测试与内存合并探针。
- review_status: `changes_requested`
- next_gate_status: `changes_requested`
- author_self_check_score: `n/a`
- review_score: `83`
- closed_findings: `T04-I1, T04-I2, T04-I3`
- open_findings: `T04-R2-I1`
- new_findings: `T04-R2-I1`
- regressed_findings: `none`

评分：

- 需求符合度：`24 / 30`
- 架构一致性：`17 / 20`
- 测试充分性：`15 / 20`
- 代码质量：`17 / 20`
- 文档与记忆同步：`10 / 10`

## Finding Closure

- `T04-I1`：已关闭原始格式覆盖问题。
- `T04-I2`：已关闭，推测性套话已删除。
- `T04-I3`：已关闭，两份设计文档保持未发布候选。

## Findings

### Critical

- 无。

### Important

- `T04-R2-I1`（`src/runtime/project_knowledge/extractors.py:242`）：局部身份规则只在
  task brief 一侧将 `TASK-SKILL-001` 改写为父工作项限定身份，Ledger extractor 仍
  保留原任务编号。只读合并探针产生一个有目标的 planned 实体和一个有状态、无目标的
  in_progress 实体。应让所有来源使用同一限定身份，并新增 brief + Ledger 的索引级
  单实体合并测试。

### Minor

- 138/138 覆盖测试未断言实体 ID 全局唯一，也未使用 source registry 的实际
  include/exclude 解析；应补充，并与 Ledger 合并断言一起防止身份分裂。

## Verification

- 四项限定测试：`4 passed in 0.17s`。
- Ruff：`All checks passed`。
- 限定 `git diff --check`：退出码 `0`。
- brief/Ledger 合并探针：两个不同 `work_item`，确认 `T04-R2-I1`。

## Gate

`changes_requested`

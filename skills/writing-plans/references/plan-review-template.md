# 计划评审

用于评审 `.factory/workitems/<WORKITEM-ID>/plan.md` 是否可以进入执行候选。

## 输入

- 计划：
- 规格 / 需求 / 设计：
- 工作项简报：
- 相关记忆：

## 检查项

| 类别 | 检查内容 |
|---|---|
| 完整性 | 是否缺任务、缺步骤、缺测试、缺验证证据、缺记忆同步、存在占位符 |
| 规格一致性 | 是否覆盖需求，是否做多、做少或偏离边界 |
| 任务拆分 | 每个任务边界是否清晰，是否能独立验证 |
| 可构建性 | 执行者是否有文件路径、代码内容、命令和期望输出 |
| 任务身份 | 是否有 `## Work Breakdown` 四列表 `id | parent_id | title | status`，每张 TaskCard 是否映射唯一 `wbs_id`，且 TaskCard、ledger、session 都有一致的 `task_card_id`、`wbs_id`、`current_gate`、`next_required_action` 等恢复字段 |
| 依赖与词表 | WBS `status` 是否仅使用 `planned | current | completed`，并与 TaskCard 生命周期字段区分；TaskCard 生命周期词表是否仅使用 `planned | active | ready_for_review | completed | closed | blocked`；review_status 词表是否仅使用 `not_requested | self_check_passed | approved | changes_requested` |
| 依赖图 | 每个计划任务和 TaskCard 是否都有稳定 `owner`、结构化 `depends_on: <TASK-CARD-ID,... | none>`，且依赖 DAG 校验是否拒绝缺 owner、未知依赖、自依赖或依赖环 |

## 校准

只阻塞会导致执行者做错、卡住、越界或无法验证的问题。文字风格和非阻塞建议放到“建议”。
缺少 WBS、TaskCard 映射或恢复字段时失败。

## 输出格式

```markdown
## 计划评审

**状态：** 通过 | 发现问题

**问题：**
- [任务 X，步骤 Y]：<具体问题> - <为什么影响执行>

**建议：**
- <非阻塞建议>
```

## 门禁

- `通过`：计划可进入执行候选；下一步由 `using-shanforge` 流程总控判断。
- `发现问题`：先修计划，再重新评审。

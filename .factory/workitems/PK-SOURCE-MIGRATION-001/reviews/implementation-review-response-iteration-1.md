# 实现评审整改回复（迭代 1）

## 评审结论

- 原结论：`changes_requested`
- 分数：82
- Critical：0
- Important：2
- 本轮处理：两项均按当前批准范围修复，无需新增产品决定。

## I1：canonical WorkItem 迁移缺少旧 ID alias，判定规则过宽

已处理：

1. canonical Task ID 只接受“全大写命名空间 + 连字符分段 + 至少一个数字”的严格格式，
   并限制最大长度；`shared-label` 等自然标签继续使用来源域哈希，不跨 ledger 合并。
2. JSONL v5 对每个从旧 source-scoped ID 迁移到 canonical ID 的 WorkItem 写入
   `pk_entity_alias`，旧 `show/trace/context` 查询可解析到新 ID。
3. 增加 v4→v5 warm migration 回归：先构造旧 contribution hash 和旧实体，再 refresh，
   验证旧实体退出、alias 落库、查询解析到 canonical 实体。
4. 增加两个来源使用相同自然标签的负例，验证仍得到两个不同 WorkItem。

真实项目中九个关系端点全部存在。其中八个任务曾由旧 ledger JSONL 投影，因此各有一个
旧 ID alias；`TASK-IMPLEMENT-003-P001-T05` 只有 task brief、从未产生旧 JSONL 实体，
因此不存在可迁移的旧 ID，alias 数量为 0 属于预期。

## I2：展示标题被错误用作任务机器 ID

已处理：

1. JSONL extractor 将声明任务编号写入 `details.task_id`。
2. Renderer 按 `details.task_id`、`pk_work_item.work_item_id`、WorkItem `entity_id`
   的顺序解析机器 ID，不再从 `display_name` 推断身份。
3. `display_name` 独立作为人类标题；含中文并夹带 PRD、Markdown、SQLite 等技术词的
   标题可直接展示，不再退化为“任务标题待补充”。
4. 使用真实 SQLite data-store → renderer 链路验证：
   `PK-SOURCE-MIGRATION-001-T01` 的页面标题为“PRD 与 Markdown 需求提取”，任务编号仍为
   canonical ID，需求深链、父子归属和去重均按机器 ID 处理。

## 验证

- 任务范围：`62 passed`
- Ruff：通过
- Mypy：279 个源文件、0 问题
- 真实 SQLite：九个端点存在、88 条强关系完整；8 个历史 ledger 任务有 alias，
  task-brief-only 的 T05 无虚构 alias。
- 真实 HTML：三个本任务详情页均显示中文标题和 canonical 任务编号，无
  “任务标题待补充”。

结论：I1、I2 已关闭，请同一评审者复审当前候选。

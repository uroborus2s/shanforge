# T04 最终验证失败根因调查

## 基本信息

- Work item：`PK-SOURCE-MIGRATION-001`
- Task：`PK-SOURCE-MIGRATION-001-T04`
- 问题来源：人工确认后的提交前新鲜验证
- 受影响路径：`src/runtime/project_knowledge/extractors.py`、任务简报语义投影
- 当前状态：`root_cause_found / pending_human_confirmation`

## 现象

- 自动化回归为 `61 passed / 1 failed`。
- 新登记的 `T06-mobile-hifi-art-direction.md` 能产生任务实体，但没有任何正式任务语义，
  违反 T04 的“全部登记任务简报至少提取一类语义”回归约束。
- 复现命令和完整结果见
  `.factory/workitems/PK-SOURCE-MIGRATION-001/evidence/T04-final-verification-failure-20260727.md`。

## 调查

- 最近变化：失败输入是当前未追踪的新任务简报；它在 2026-07-23 的 T04 独立复审语料
  中尚不存在，现在被 source registry 的通配 include 自动纳入。
- 可工作的相似实现：使用 `目标`、`交付结果`、`完成口径` 等既有登记字段的任务简报
  可以产生 `goal`、`deliverables` 和 `completion_conditions`。
- 差异：新简报采用 `目的`、`本轮交付`、`平台`、`保留`、`禁止`、`人工 Gate` 等紧凑
  行内字段；其中 `禁止` 已存在于 `_TASK_BRIEF_SECTION_KEYS`，却仍被更前面的正则白名单
  拒绝。
- 数据流：
  `SRC-WORKITEM-BRIEF glob → MarkdownExtractor → _TASK_BRIEF_FIELD_LINE →
  _task_brief_section_key → work_item.details → 全登记语料回归`。

## 根因

- 直接原因：`_TASK_BRIEF_FIELD_LINE` 的字段白名单不包含 `目的` 和 `本轮交付`，也没有
  覆盖映射表中已经存在的 `禁止`，导致这些合法字段在进入语义映射前被丢弃。
- 根源原因：行内任务字段的合法键同时维护在正则白名单和
  `_TASK_BRIEF_SECTION_KEYS` 两处；两份列表已经漂移。source registry 接受所有登记任务
  简报，但提取器的重复白名单不能随合法简报格式扩展稳定演进。
- 最小假设：如果让语义映射表成为唯一允许列表，并登记
  `目的 → goal`、`本轮交付 → deliverables`，该简报会恢复至少两类正式语义。
- 假设验证：未改文件的内存替换实验已产生 `goal` 和 `deliverables`，证明失败发生在
  字段键识别边界，不在 source registry、任务身份或 SQLite 合并层。

## 候选修复方案（尚未授权执行）

- 将行内字段正则收敛为“捕获有界键值，再由 `_TASK_BRIEF_SECTION_KEYS` 唯一裁决”，删除
  正则中的第二份键白名单。
- 在映射表增加 `目的` 和 `本轮交付` 两个明确别名。
- 增加覆盖该紧凑简报格式的最小回归测试；不修改范围外的 T06 简报。

## 结论

- 根因是否明确：是。
- 是否允许修复：否；按 `systematic-debugging`，先等待人工确认根因，再确认修复方案。
- 剩余风险：在修复并重新跑完整 T04 验证前，不能提交，也不能声明 T04 完成。

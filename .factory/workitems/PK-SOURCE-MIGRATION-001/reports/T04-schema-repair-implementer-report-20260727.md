# PK T04 任务简报共享 Schema 修复实施报告

- Task：`PK-SOURCE-MIGRATION-001-T04-SCHEMA-REPAIR`
- status：`ready_for_review`

## 最小实现

1. 删除 `_TASK_BRIEF_FIELD_LINE` 中重复的字段白名单，只保留通用 `key:value`
   结构识别。
2. 由 `_TASK_BRIEF_SECTION_KEYS` 唯一决定字段是否受支持，并加入 `目的`、
   `本轮交付`、`决策` 三个真实语料别名。
3. 支持空值字段后的缩进列表，不接受顶层后续字段或未知键。
4. 为唯一确实没有语义的状态对账任务补一条真实目标。
5. Registry 与数据设计候选同步为 `markdown-v4`。

## 未做

- 未新增解析器抽象、依赖、SQLite 表或 fallback。
- 未修改生产数据、API、页面只读边界或其他 Skill。
- 未发布设计候选，未执行远端 Git 或部署。

## 验证

见 `evidence/T04-schema-repair-red-green-verification-20260727.md`。

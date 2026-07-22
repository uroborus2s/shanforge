# 相关性判断门

默认只读 summary。只有当前问题需要事实缺口时，才回源正式文档或其他长文件。

## 事实源优先级

- 正式文档和 work item ledger 高于 memory summary。
- summary 不复制完整正文；只保留 ID、状态、当前 gate、关键约束和索引。
- summary 与正式文档冲突时，以正式文档和 ledger 为准。
- SQLite、HTML 和 cache 都是非事实投影；`.factory/cache/site/current/index.html` 只能作为可重建展示视图。

## 允许读取

- 当前任务直接修改的正式文档。
- 当前任务对应的 work item brief、plan、review、evidence。
- `.factory/memory/doc-map.md` 指向的单个正式事实源。
- 进入实现前必须回源技术选型、系统架构、模块边界和代码映射。
- 代码改动直接触达的源文件、测试文件和相邻接口文件。

## 禁止读取

- 禁止用“稳妥”作为散读理由。
- 禁止一次性读取整组阶段 `docs/`。
- 禁止默认读取 `project-charter.md`、`input.md`、`user-guide.md`。
- 禁止跳过 `.factory/memory/*` 直接回源正式文档。
- 禁止把历史推荐命令当作当前事实。

## 判断问题

读取前回答四个问题：

1. 当前任务是否直接修改该文件？
2. summary 是否已经覆盖需要的事实？
3. 如果不读该文件，会不会有具体可描述的事实风险？
4. 读取后会产出什么决定或改动？

四项都不能说明时，不读。

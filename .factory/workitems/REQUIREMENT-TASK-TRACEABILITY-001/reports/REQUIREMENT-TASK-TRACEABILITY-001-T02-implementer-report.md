# T02 实现报告

## 完成内容

- `writing-plans` 定义 `project / requirement / cross_cutting / system` 四类任务层级。
- 需求级和横切任务复用强 `IMPLEMENTS`；项目级任务关联基线、章程或设计；系统任务不贡献产品进度。
- 任务简报模板增加任务层级、关联目标和强关系字段。
- Markdown 提取器把合法层级写入 `details.task_scope`，把目标写入
  `details.traceability_targets`，并拒绝非法层级。

## 边界

- 沿用现有关系图，没有新增 SQLite schema 或关系表。
- 兼容旧任务：未声明 `task_scope` 的历史任务仍可读取。

## 状态

`ready_for_review`

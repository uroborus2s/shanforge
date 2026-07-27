# PK T04 Schema 修复复审反馈分类 Iteration 2

## 路由合同

- work_item_id：`PK-SOURCE-MIGRATION-001`
- task_card_id：`PK-SOURCE-MIGRATION-001-T04-SCHEMA-REPAIR`
- allowed_paths：extractor 测试和本任务状态产物
- forbidden_actions：生产代码、SQLite schema、其他 Skill、远端、发布
- current_gate：`changes_requested`
- write_policy：`test_write`

## I1-test

- 反馈来源：task rereview
- severity：Important
- 反馈要求：显式锁定 `## Task` 章节仍映射为 `goal`。
- 是否清楚：yes
- 是否技术正确：yes
- 证据：当前英文正例使用 `## Goal`，无法防止未来误删 `"task": "goal"`。
- 是否与用户决策冲突：no
- 是否违反 YAGNI：no
- 处理决定：Fixed；新增一个直接的 `## Task` 正例，不改生产代码。
- 验证：运行身份负例与章节正例、五文件回归和 Ruff。

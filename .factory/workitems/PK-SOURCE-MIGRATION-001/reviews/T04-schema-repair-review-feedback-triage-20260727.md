# PK T04 Schema 修复评审反馈分类

## 路由合同

- work_item_id：`PK-SOURCE-MIGRATION-001`
- task_card_id：`PK-SOURCE-MIGRATION-001-T04-SCHEMA-REPAIR`
- allowed_paths：任务简报指定的 extractor、测试和本任务状态产物
- forbidden_actions：SQLite schema、生产数据、页面只读边界、其他 Skill、远端、发布
- current_gate：`changes_requested`
- write_policy：`source_or_test_write`

## I1

- 反馈来源：task review
- severity：Important
- 文件：`src/runtime/project_knowledge/extractors.py`、
  `tests/test_project_knowledge_extractors.py`
- 反馈要求：`Task:` 身份元数据不得生成正式任务语义。
- 是否清楚：yes
- 是否技术正确：yes
- 证据：`_TASK_BRIEF_TITLE_LINE` 已把该行识别为任务身份，但
  `_task_brief_details` 又将同一行经 `task -> goal` 解析为任务语义。
- 是否与用户决策冲突：no
- 是否违反 YAGNI：no
- 处理决定：Fixed；复用既有身份行正则，在同行语义解析前排除身份行，并增加一个负例。
- 验证：先运行新增用例观察 RED，再运行聚焦和五文件回归。

# T04 实施报告

- 工作项：`PK-SOURCE-MIGRATION-001`
- 任务：`PK-SOURCE-MIGRATION-001-T04`
- 实施者：`/root`
- 状态：等待独立评审

## 问题根因

1. Markdown 提取器只读取任务编号、标题和状态，没有把任务简报里的目标、具体工作、
   交付结果及完成口径投影到 SQLite 实体详情。
2. 同编号任务合并时，最新 Ledger 记录整体胜出，任务简报的人类说明随之丢失。
3. 任务详情使用通用元数据布局，用户首先看到的是内部状态与编号，而不是任务意图。
4. 需求首页按分类平铺，没有把产品、业务域、需求和验收标准表达成可逐层展开的结构。

## 已实施

- 从任务简报的稳定标题和字段中提取
  `goal`、`work_items`、`inputs`、`scope`、`out_of_scope`、`deliverables`、
  `completion_conditions`、`verification`。
- 同一任务编号合并时，由 Ledger 保留最新状态、时间和下一步，由任务简报保留人类可读
  语义；沿用现有 `detail_json`，没有新增 SQLite 表。
- 任务详情把目的、工作、产出和完成口径作为四个首要区块，状态与追踪关系后置。
- 需求页使用原生可访问的 `details/summary` 形成
  `产品 → 业务域 → 需求 → 验收标准` 四层树，保留需求详情、验收锚点和追踪深链。
- 更新既有数据设计、前端设计、关联声明和工作项计划，没有新增平行正式文档。
- 使用固定 CLI 重新生成最后有效静态站点，并完成桌面和窄屏浏览器验证。

## 变更范围

- `src/runtime/project_knowledge/extractors.py`
- `src/settings/project_knowledge/sqlite_index.py`
- `src/runtime/project_knowledge/site_renderer.py`
- `tests/test_project_knowledge_extractors.py`
- `tests/test_project_knowledge_index.py`
- `tests/test_project_site_renderer.py`
- `docs/05-design/data-design.md`
- `docs/05-design/frontend-design.md`
- `.factory/project-knowledge/source-registry.json`
- `.factory/project-knowledge/relation-declarations.json`
- `.factory/workitems/PK-SOURCE-MIGRATION-001/plan.md`
- `.factory/workitems/PK-SOURCE-MIGRATION-001/task-briefs/PK-SOURCE-MIGRATION-001-T04.md`
- 本任务的 ledger、报告、评审和验证证据。

## 验证摘要

- 新增行为先红后绿。
- 项目知识目标测试：首轮 `64 passed`；评审整改后 `67 passed`。
- Ruff：通过。
- Mypy：279 个源文件无问题。
- 浏览器：桌面和移动端通过，控制台错误为 0。
- 138 份注册任务简报全部生成唯一任务实体，并至少提取一项正式任务语义。
- 详细证据：
  `.factory/workitems/PK-SOURCE-MIGRATION-001/evidence/T04-red-green-and-ui-verification.md`。

## 已知边界

- 需求树的“产品”和“业务域”来自现有项目名称与需求分类，是只读投影，不创造新的需求事实。
- 没有任务简报的遗留任务仍只能显示现有索引内容；本次不使用 AI 猜测缺失说明。
- HTML、SQLite 和 cache 仍是可重建派生物，不提交 Git。

# 任务详情可读化与需求验收树

## 工作项

- 工作项：`PK-SOURCE-MIGRATION-001`
- 任务：`PK-SOURCE-MIGRATION-001-T04` 任务详情可读化与需求验收树
- 状态：`closed`
- 上游需求：`REQ-PKI-008`
- 上游设计：`docs/05-design/frontend-design.md`

## 目标

让项目成员不需要理解内部编号、英文状态或索引术语，也能看懂每项任务为什么做、具体要
做什么、完成后得到什么以及怎样确认完成；同时让需求与验收页按照产品、业务域、具体
需求和验收标准逐层展示。

## 具体工作

- 从任务简报的稳定章节和字段提取目标、具体工作、范围、交付结果、完成条件和验证方式。
- 将任务简报中的人类说明与 Ledger 的最新状态按同一任务编号合并到现有 SQLite 实体投影。
- 将任务详情重组为“为什么做、具体做什么、完成后得到什么、怎样确认完成”四个首要区块。
- 将需求首页重组为可展开的产品需求树，并保留需求详情、验收锚点和任务追踪深链。

## 交付结果

- 所有已登记任务简报都能为任务详情提供人类可读说明。
- 需求与验收页面形成 `产品 → 业务域 → 需求 → 验收标准` 的稳定阅读层级。
- 固定 CLI 重新生成最后有效静态站点；SQLite 表结构和只读边界不变。

## 范围

- `src/runtime/project_knowledge/extractors.py`
- `src/settings/project_knowledge/sqlite_index.py`
- `src/runtime/project_knowledge/site_renderer.py`
- `.factory/project-knowledge/source-registry.json` 中任务简报提取器版本
- Ledger 和任务简报共用的父工作项限定任务身份
- 项目知识相关测试
- 既有数据设计、前端设计和本工作项执行记录

## 非范围

- 不新增 SQLite 表。
- 不新增平行需求或设计文档。
- 不把 HTML、SQLite 或 cache 提交 Git。
- 不改变页面只读性质，不增加编辑、拖拽或状态修改。

## 完成口径

- 自动化测试证明任务语义从任务简报进入 SQLite，且不会被较新的 Ledger 状态覆盖丢失。
- 自动化测试证明任务详情存在四个可读区块，需求页可逐层展开到验收标准。
- 桌面端和窄屏静态页面均可打开、展开、返回和深链，控制台错误为 0。
- 项目知识相关测试、Ruff 和 Mypy 通过，独立评审没有 Critical 或 Important 问题。

## 验证命令

- `uv run pytest tests/test_project_knowledge_extractors.py tests/test_project_knowledge_index.py tests/test_project_site_renderer.py tests/test_project_knowledge_security.py tests/test_project_knowledge_pm.py -q`
- `uv run ruff check src/runtime/project_knowledge/extractors.py src/settings/project_knowledge/sqlite_index.py src/runtime/project_knowledge/site_renderer.py tests/test_project_knowledge_extractors.py tests/test_project_knowledge_index.py tests/test_project_site_renderer.py`
- `uv run mypy src`
- `PYTHONPATH=src .venv/bin/python -m settings.composition.project_knowledge project snapshot --html --json`

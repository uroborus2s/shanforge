# 文档与工厂结构破坏性全量迁移实施计划

**目标：** 将 `docs/04-project-development` 和 `.factory` 重构为只保留当前正式资产和正式内容的文档基线。

**架构：** 正式产品事实写入 `docs/`；执行事实写入 `.factory/workitems/DOC-FACTORY-RESTRUCTURE-001/`；恢复索引写入 `.factory/memory/doc-map.md` 和最小 memory summary；旧 process、旧 generated、旧 history 快照不再作为正式资产保留。

**技术栈：** Markdown、pytest、docs-stratego、JSON。

**工作项：** `DOC-FACTORY-RESTRUCTURE-001`

**状态：** `completed_superseded_by_formal_baseline`

**收口说明：** 任务 1 的迁移结果已经进入后续正式基线；任务 2 的旧结构草案已经被
`docs/01-getting-started`、`docs/04-product`、`docs/05-design`、`docs/06-delivery`
以及 `.factory`/SQLite/HTML 分层方案取代。禁止再按本历史计划重复迁移。

## 输入

- 用户要求：按六类任务结构重构 `04-project-development` 和 `.factory`。
- 用户变更：旧资产旧结构都删除，只保留最新正式资产和正式内容。
- 用户署名要求：正式文档不能署名为 `Codex`，执行事实使用“用户授权代执行”。
- 相关规则：`document-templates`、`using-shanforge`、`project-memory`、`writing-plans`、`executing-plans`、`tdd-workflow`、`ui-ux-pro-max`。
- 现状盘点：`docs/04-project-development` 存在旧页面和旧原型；`.factory` 存在旧 process、旧 generated 和旧 memory history。

## 范围

### 目标

- 新增任务执行契约正式文档。
- 新增 `.factory` 根治理说明。
- 删除旧 04 项目文档、旧静态原型和旧生成/历史资产。
- 更新导航、索引、追踪矩阵、doc-map 和当前配置 JSON。
- 新增当前 work item 标准证据包。
- 增加结构测试。

### 非目标

- 物理迁移历史 `.factory/workitems/*` 审计链。
- 修改业务代码。
- 合并或提交无关脏改动。

## 文件

| 类型 | 路径 | 职责 |
|---|---|---|
| 新建 | `docs/04-project-development/05-development-process/task-execution-contract.md` | 六类任务执行和输出契约 |
| 新建 | `docs/04-project-development/04-design/v2-architecture-pages.md` | 设计资产清单正式页面 |
| 新建 | `.factory/README.md` | `.factory` 目录职责和破坏性迁移规则 |
| 新建 | `.factory/workitems/DOC-FACTORY-RESTRUCTURE-001/` | 当前任务证据包 |
| 新建 | `tests/test_doc_factory_restructure.py` | 固定新契约、删除清单和无断链 |
| 修改 | `docs/index.md` | 根导航只登记当前正式文档 |
| 修改 | `docs/04-project-development/index.md` | 项目开发入口登记新契约 |
| 修改 | `docs/04-project-development/04-design/index.md` | 设计入口只指向当前正式设计和资产 |
| 修改 | `docs/04-project-development/05-development-process/index.md` | 开发过程入口只保留实施计划和任务契约 |
| 修改 | `docs/04-project-development/10-traceability/document-index.md` | 正式文档索引登记当前白名单 |
| 修改 | `docs/04-project-development/10-traceability/requirements-matrix.md` | 移除已删设计页引用 |
| 修改 | `.factory/memory/doc-map.md` | AI 恢复索引只登记现存正式文档 |
| 修改 | `.factory/project.json` | 移除已删路径，署名改为项目负责人 |
| 修改 | `.factory/tech-profile.json` | 署名改为项目负责人 |
| 修改 | `.factory/multi-agent-board.json` | 署名改为项目负责人 |
| 修改 | `.factory/memory/tasks.summary.md` | 记录当前 work item 摘要 |
| 修改 | `.factory/memory/current-state.md` | 记录当前状态摘要 |
| 修改 | `.factory/memory/tests.summary.md` | 记录验证结果 |
| 修改 | `.factory/workitems/implementation/README.md` | 标准 work item 结构说明 |
| 删除 | `docs/04-project-development/04-design/assets/v2-architecture-pages/index.md` | 移除 assets 目录内 Markdown |
| 删除 | `.factory/process/` | 删除旧过程区 |
| 删除 | `.factory/memory/history/` | 删除旧 memory 快照 |
| 删除 | `.factory/pm/generated/` | 删除旧生成展示页 |

## 任务

### 任务 1：破坏性重做型全量文档结构迁移

**任务切片：**

- 设计方案：确定正式文档白名单、删除清单和 `.factory` 保留边界。
- 接口设计：状态包字段作为流程接口；doc-map 作为 AI 回源接口。
- UI 或 `N/A`：`N/A`，本任务无用户界面。
- 测试设计：新增结构测试，验证导航、doc-map、README、删除清单、署名和 work item 结构。
- 开发：更新 Markdown、JSON、索引和测试，删除旧资产。
- 单测：`uv run pytest tests/test_doc_factory_restructure.py`
- 文档校验：`uvx --from docs-stratego docs-stratego source validate --repo-path .`
- review：生成 review input package。

## 测试策略

- 红灯：旧路径存在、根导航引用已删页面、正式文档署名为 `Codex` 或 `.factory` 仍使用旧迁移口径时失败。
- 绿灯：文档白名单、删除清单、署名规则和 work item 结构全部通过。
- 定向回归：`tests/test_doc_factory_restructure.py`。
- 文档结构：`uvx --from docs-stratego docs-stratego source validate --repo-path .`。
- JSON 校验：`jq empty .factory/project.json .factory/tech-profile.json .factory/multi-agent-board.json`。

## 文档同步

- 正式文档：更新根导航、项目开发首页、设计首页、开发过程首页、文档索引和追踪矩阵。
- `.factory/memory/`：更新 doc-map、tasks summary、current state、tests summary。
- 工作项流水账：写入 `ledger.jsonl`。

## 评审门

- 计划评审：`superseded`
- 任务评审：`covered_by_successor_baseline_reviews`
- 验证：`passed_by_successor_baseline_and_project_knowledge_verification`
- 记忆同步：`completed`
- 提交：`handled_by_successor_work_items`

## 计划自审

- 规格覆盖：覆盖六类任务、破坏性删除、`.factory` 结构治理和署名规则。
- 占位符扫描：无占位符。
- 类型一致性：状态包字段与 workflow skill 一致。
- 可构建性：Markdown、JSON 和 pytest 结构检查。
- Shanforge 门禁：作者只进入 `ready_for_review`，等待独立 review。

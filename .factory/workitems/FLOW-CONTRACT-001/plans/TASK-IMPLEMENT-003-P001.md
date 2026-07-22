# 项目知识索引与只读项目站点实施计划

**目标：** 交付可重建 39 表知识索引、稳定语义查询 CLI、137 字段 PM 投影、只读多页面项目站点、有界维护和异步 `PROJECT_STATE_SYNC` 接入。

**架构：** application 定义用例与 ports，domain 固定 ID/locator/edge/receipt 规则，runtime 提供纯提取与渲染，settings 实现 SQLite/文件/Git/发布，access 只解析命令。SQLite 与站点是可删除投影，正式事实仍在 Git、docs、代码、测试、Ledger 和受控 Memory。

**技术栈：** Python 3.14 标准库（`sqlite3`、`ast`、`argparse`、`html`、`json`、`hashlib`）、pytest、Ruff、mypy、离线 HTML/CSS/少量原生 JS。

**工作项：** `FLOW-CONTRACT-001`

**任务：** `TASK-IMPLEMENT-003`

**状态：** `verified / independent_approved / ready_for_authorized_local_commit`

## 输入

- 已批准需求：R009 Manifest `8be9d829ea2a895eae043eaf054914cb03b7457a43d51c142cc4ad7f41f577ae`。
- 技术设计：`.factory/workitems/FLOW-CONTRACT-001/drafts/DESIGN-PROJECT-KNOWLEDGE-001.R001.md`。
- PM field map：`.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001.pm-field-map.R009.json`。
- 当前记忆：`.factory/memory/agent-session.md`。
- 正式 owner：`docs/04-product/prd.md`、唯一需求矩阵、`docs/05-design/*` 现有 12 页、`docs/document-index.md`、`docs/index.md`。

## 范围

### 目标

- 实现 R009 的 16 条需求、64 条 AC 与 11 条 NFR 的首版可执行合同。
- 迁出 `docs/05-design` 中两份机器 JSON，不增加平行人类设计页。
- 提供会话可直接调用的确定性命令和 current HTML 入口。

### 非目标

- 站点写操作、远端服务、Push/PR/Merge/部署。
- 修改或批准 `TASK-IMPLEMENT-002-R001`。
- 引入 UI 框架、数据库 ORM、常驻 watcher 或第二套进度 reducer。

## 文件结构

| 类型 | 路径 | 职责 |
|---|---|---|
| 新建 | `src/domain/project_knowledge/` | 稳定实体、locator、edge、receipt 与策略规则 |
| 新建 | `src/application/project_knowledge/` | 用例、ports、刷新/查询/快照/维护编排 |
| 新建 | `src/runtime/project_knowledge/` | Markdown/JSON/JSONL/Python/Git 纯提取与离线 HTML 渲染 |
| 新建 | `src/settings/project_knowledge/` | 39 表 schema、SQLite store、registry、site publisher、维护实现 |
| 新建 | `src/access/project_cli.py` | argparse 命令解析和结构化输出，不导入 settings |
| 新建 | `src/settings/composition/project_knowledge.py` | 唯一跨层装配与 `python -m` 入口 |
| 新建 | `.factory/project-knowledge/*.json` | source registry、强关系、alias 稳定声明 |
| 新建 | `.factory/catalog/ai-sdlc-catalog.source.json` | 迁出的稳定机器 Catalog source |
| 生成且忽略 | `.factory/runtime/project-state-sync.sqlite3*` | 独立 durable sync queue；不属于知识索引 39 表 |
| 修改 | `.gitignore` | 排除 SQLite、FTS、site、receipt 和 PM generated |
| 测试 | `tests/test_project_knowledge_*.py` | 六个切片的合同、集成、安全、性能和 HTML 验证 |
| 文档 | 现有正式 owner | 原位增加 R009 需求/设计/CLI/迁移/运维事实与版本历史 |
| 记忆 | `.factory/memory/agent-session.md` 等最小摘要 | 只保留当前 Gate、下一动作和精确入口 |

## 边界

- 层级：`access -> application -> domain -> runtime -> settings`。
- 领域：Project Knowledge / Project Control / System Tasks。
- 接口归属方：application 定义 registry/index/query/render/maintenance/sync ports；settings 只实现。
- 下游依赖：Python 标准库、现有 `ProjectProgressSnapshot/v2`；同步队列使用本任务 application-owned port 与独立 settings store，不依赖冻结 system-task ports。
- 禁止耦合：access 不碰 SQLite；domain 不碰文件系统；runtime 不写 Git；settings 不定义业务规则；renderer 不计算状态。

## 任务

### T01：合同内核与 39 表 schema

**任务切片：**

- 设计方案：把 R009 数据字典固化为可执行 DDL 与不可变 domain contracts。
- 接口设计：`KnowledgeEntity`、`SemanticLocator`、`KnowledgeEdge`、`IndexGeneration`、`ProjectCommandReceipt`；application 的 `KnowledgeIndexPort`。
- UI：`N/A`，本切片仅建立数据/接口合同，用户可见页面由 T04 交付。
- 测试设计：断言恰好 39 表、2 FTS、关键 FK/唯一约束、唯一 current generation、alias 防环和 137 field map 完整性。
- 开发：schema、模型、验证器和 migrations v1。
- 单测：`tests/test_project_knowledge_schema.py`、`tests/test_project_knowledge_contracts.py`。
- review：独立 Spec/Quality review。
- 集成测试：在临时 SQLite 执行合法/非法事务并验证回滚。

- [ ] Red：创建 schema/contract 测试，确认因模块缺失失败。
- [ ] Green：实现最小合同与 DDL，运行：

```bash
PYTHONPATH=src uv run pytest tests/test_project_knowledge_schema.py tests/test_project_knowledge_contracts.py -q
```

期望：全部通过，schema 表集合精确为 39。

### T02：Source Registry、提取器与原子增量代次

**任务切片：**

- 设计方案：registry allowlist + 文件 Hash；变化来源生成 SourceContribution/v1；单事务发布 generation。
- 接口设计：`SourceRegistryPort`、`SourceExtractorPort`、`IndexRefreshCommand/Result`。
- UI：`N/A`，本切片只生产站点上游索引；无独立用户界面。
- 测试设计：Markdown stable section、JSON Pointer、JSONL event UID、Python AST、Git metadata；同 registry 多文件 concrete source identity；同实体多来源删除其一仍保留其余 contribution；无变化解析 0、增删改、失败回滚、reader 旧/新一致、冷重建对账。
- 开发：runtime extractors 与 settings SQLite repository。
- 单测：`tests/test_project_knowledge_extractors.py`、`tests/test_project_knowledge_index.py`。
- review：独立 Spec/Quality review。
- 集成测试：临时仓库 10k artifact fixture 的单来源变化。

```bash
PYTHONPATH=src uv run pytest tests/test_project_knowledge_extractors.py tests/test_project_knowledge_index.py -q
```

期望：全部通过；无变化计数 `parsed_sources=0`；失败后 current generation 不变。

### T03：稳定定位、关系图和固定查询 CLI

**任务切片：**

- 设计方案：find/show/trace/context 只读同一 generation；alias 最多 8 跳；读取计划受 4 文件/32 KiB 预算。
- 接口设计：`KnowledgeQueryPort`、`LocatorResolverPort` 与 access parser；命令返回 `ProjectCommandReceipt/v1`。
- UI：CLI 人类摘要 + JSON receipt；不做终端 TUI，避免第二套交互层。
- 测试设计：标题改名/章节前插、代码移动、显式 alias、0/多 locator、同边多来源、幽灵边清理、稳定退出码。
- 开发：application query service、FTS/trigram 查询、access CLI 与 composition 注入。
- 单测：`tests/test_project_knowledge_query.py`、`tests/test_project_cli.py`。
- review：独立 Spec/Quality review。
- 集成测试：在真实仓 registry 的临时 DB 上执行 check/find/show/trace/context。

```bash
PYTHONPATH=src uv run pytest tests/test_project_knowledge_query.py tests/test_project_cli.py -q
```

期望：全部通过；locator 不唯一返回 4 且读取文件数为 0。

### T04：137 字段 PM 投影与只读多页面站点

**任务切片：**

- 设计方案：PM reducer 直接投影 Snapshot v2 path；页面 DTO 只读 index；页面 fingerprint 控制增量渲染；不可变 build 目录通过 `os.replace` 原子切换 `current` symlink。
- 接口设计：`PmProjectionPort`、`SiteRendererPort`、`SitePublisherPort`、`RenderViewReceipt`。
- UI：企业级内容优先；总览 + 九类主导航；需求、设计、任务、缺陷、代码、文档、质量、版本、报告和 PM record 全部有稳定列表/详情 URL；详情均有返回按钮，无 drawer/modal。
- 测试设计：137 mapping 一次覆盖并校验 PK/父键/key collision/cardinality/type/nullable/history/R014 pin；`known|unknown|not_registered|not_applicable` 四态逐一断言且 HTML 不再推导；HTML 转义、所有详情深链/返回、打印/焦点/响应式、cache hit 不写、单页变化最小重绘、symlink pointer 崩溃点和并发 reader。
- 开发：PM projector、DTO、renderer、CSS/JS、publisher。
- 单测：`tests/test_project_knowledge_pm.py`、`tests/test_project_site_renderer.py`。
- review：独立 Spec/Quality/UI review。
- 集成测试：四视口 Playwright + axe + 键盘/打印 + 人工视觉检查；浏览器不可用时 NFR-PKI-009 保持阻塞，静态证据不替代通过。

```bash
PYTHONPATH=src uv run pytest tests/test_project_knowledge_pm.py tests/test_project_site_renderer.py -q
```

期望：全部通过；生成入口 `.factory/cache/site/current/index.html`；所有详情页含可用返回链接。

### T05：异步同步、维护和资料迁移

**任务切片：**

- 设计方案：不修改冻结 `TASK-IMPLEMENT-002-R001`；application 定义独立 `ProjectStateSyncQueuePort`，settings 用 `.factory/runtime/project-state-sync.sqlite3` 实现 durable request/event/lease/fencing；maintenance 仅触及登记 cache；迁移先 dry-run 对账。
- 接口设计：`ProjectStateSyncRequest/v1`、`ProjectStateSyncQueuePort`、`ProjectStateSyncWorker`、`MaintenancePlan/Receipt`；主会话通过正式 `project sync enqueue --head H --scope SCOPE` 快速登记，`sync head` 修复漏登记。
- UI：站点报告页显示后台状态和 stale 诊断；无写操作，未授权 commit 显示“无需维护提交”。
- 测试设计：独立 queue 与冻结 enum 隔离、50 transition 穷尽、coalesce/supersede、fencing、5 次重试、commit_not_authorized 成功收口、TTL/容量/realpath/legal hold、Catalog 与 PM 精确源/目标/rollback 迁移强关系 0 丢失。
- 开发：独立 queue/store/worker、access/composition 的 sync enqueue 子命令、maintenance、迁移 prepare、ignore 与 source registry 更新；T05 只在 `.factory/cache/project-knowledge/migration/<job_id>/after-images/` 为 `docs/05-design/ai-sdlc-catalog.{source,manifest}.json` 和 `.factory/pm` 精确文件生成 after-image/disposition/before Hash/rollback 包，不写最终目标、不删除 legacy 源。
- 单测：`tests/test_project_state_sync.py`、`tests/test_project_knowledge_maintenance.py`、`tests/test_project_knowledge_migration.py`。
- review：独立 Spec/Quality review。
- 集成测试：主会话 enqueue 返回后再驱动 worker，断言业务状态不回滚。

```bash
PYTHONPATH=src uv run pytest tests/test_project_state_sync.py tests/test_project_knowledge_maintenance.py tests/test_project_knowledge_migration.py -q
```

期望：全部通过；生成物不在 `git status --short --ignored` 的可提交集合中。

### T06：装配、正式文档、性能、安全和完整收口

**任务切片：**

- 设计方案：唯一 composition builder；正式需求/设计/索引/用户/运维文档原位增补；移除机器 JSON 的 docs 导航事实。
- 接口设计：公开命令面固定，不增加第二套 API；正式文档记录中文命令说明与退出码。
- UI：四视口、键盘、打印、缺失/错误/stale 页面最终检查；UI 不适用项为 0。
- 测试设计：架构 import、secret/traversal/symlink/ACL/撤权；Memory 0/1/50/200 P95≤1s；warm≤100ms、single≤800ms、10k single-source≤500ms、cold≤3s、enqueue≤100ms、ordinary sync≤3s；固定时钟双构建 Hash；Playwright/axe/键盘/打印/人工视觉；全量邻近回归、docs-stratego。
- 开发：composition；原位修订 `docs/04-product/prd.md`、`docs/04-product/requirements-matrix.md`、`docs/05-design/index.md`、`system-architecture.md`、`module-domain-design.md`、`data-design.md`、`api-design.md`、`frontend-design.md`、`ux-ui-design.md`、`memory-design.md`、`workflow-execution-design.md`、`interface-matrix.md`、`technical-selection.md`、`docs/document-index.md`、`docs/index.md`；更新 `.factory/project-knowledge/relation-declarations.json` 与 `.factory/memory/doc-map.md`；最后激活 T05 migration package 并删除已对账 legacy 源。
- 单测：`tests/test_project_knowledge_integration.py`、`tests/test_project_knowledge_security.py`、`tests/test_project_knowledge_performance.py`。
- review：整体独立 Spec/Quality/UI review；开放 C/I 为 0 才可提交。
- 集成测试：真实仓 `index rebuild`、`snapshot --html` 两次、find/show/trace/context、maintain dry-run。

```bash
PYTHONPATH=src uv run pytest tests/test_project_knowledge_*.py tests/test_project_cli.py tests/test_system_task_integration.py -q
uv run ruff check src tests
uv run mypy src
uvx --from docs-stratego docs-stratego source validate --repo-path .
git diff --check
```

期望：所有命令 exit 0；若全仓已有无关债务，必须用基线差分证明本任务新增错误为 0，不能伪报全绿。

## 测试策略

- Red：每个切片先运行目标测试并记录缺失行为失败。
- Green：只实现当前切片最小能力，目标测试通过后才扩展。
- 定向回归：所有 `test_project_knowledge_*` 与 `test_project_cli.py`。
- 邻近回归：project-control、system-tasks、memory、composition、docs navigation。
- 全量回归：T06 整体候选前运行；若受现有脏工作树影响，记录精确失败归属和基线差分。浏览器/axe/视觉或任一硬 NFR 未运行时，整体资格保持未通过，不以差分豁免。
- 未运行项：真实共享鉴权服务和生产部署不在范围；用受控授权 fake 与本地 HTTP handler 验证合同。

## 文档同步

- 正式文档：原位修订 PRD、唯一需求矩阵、现有设计 owner、索引、用户指南、开发者接口、部署与运维；每份追加版本历史。
- `.factory/memory/`：只更新当前会话卡、doc-map 和受影响 summary，不复制设计正文。
- 工作项：每任务 evidence/report/review 与 ledger 事件；cache 不进入 workitem。

## 评审门

- 计划评审：`approved`
- 任务评审：`approved`（独立复审 iteration 4，98/100，C0/I0/M0）
- 验证：`completed`（定向 87 passed；全仓 1322 passed、3 个范围外既有失败）
- 本地提交：`completed`（用户授权后以 `gitcommitzh` 提交当前任务精确范围）。
- 远端/PR/Merge/部署：`not_authorized`
- 记忆同步：`completed`

## 计划自审

- 规格覆盖：16 REQ、64 AC、11 NFR 映射到 T01–T06；39 表在 T01，137 字段在 T04，异步与维护在 T05，安全/性能在 T06。
- 占位符扫描：所有交付都有确定文件、行为、命令和期望输出，不含泛化待办语句。
- 缺测试设计则失败：T01–T06 均有具体测试目标与文件。
- UI N/A：仅 T01/T02，原因是无用户界面；T03 有 CLI UI，T04–T06 有 Web UI。
- 类型一致性：统一 `ProjectProgressSnapshot/v2`、`ProjectCommandReceipt/v1`、`IndexGeneration`、R009 field map。
- 可构建性：仅使用现有 Python/pytest/Ruff/mypy 与标准库；浏览器不可用有明确替代证据但不能冒充浏览器通过。
- Shanforge 门禁：每任务都有 evidence、review、ledger、memory；实现者只能到 `ready_for_review`。

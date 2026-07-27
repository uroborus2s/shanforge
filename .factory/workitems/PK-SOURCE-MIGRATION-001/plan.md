# PRD 单一需求事实源迁移实施计划

## 授权执行包

- 目标：完成 `brief.md` 全部验收项。
- 允许修改：现有 PRD、项目知识 source registry/关系声明、项目知识 extractor/index/projection/renderer/composition、对应测试、本工作项证据与记忆入口。
- 禁止修改：冻结 R009 候选、SQLite/HTML cache、远端、与本任务无关的脏文件。
- 执行方式：当前会话串行执行；每项先 Red 后 Green。

## 文件结构

- 修改 `docs/04-product/prd.md`：当前正式需求唯一人类事实源。
- 修改 `src/runtime/project_knowledge/extractors.py`：从稳定 Markdown 章节提取需求、NFR、AC、locator 和结构关系。
- 修改 `src/settings/project_knowledge/sqlite_index.py`：写入既有 `source_section_key`。
- 修改 `src/settings/project_knowledge/pm_projection.py`：装配关系目标类型与经 Hash 校验的正式 Markdown 正文。
- 修改 `src/runtime/project_knowledge/site_renderer.py`：分类需求、关系深链、正文渲染、折叠技术元数据。
- 修改 `src/settings/composition/project_knowledge.py`：向只读站点数据装配器传入项目根。
- 修改 `.factory/project-knowledge/source-registry.json`：停用 R009 requirement contract 当前来源。
- 修改 `.factory/project-knowledge/relation-declarations.json`：登记实现任务到需求的强关系。
- 修改项目知识相关测试：锁定重建、绑定、状态、链接和正文行为。
- 修改 `docs/05-design/data-design.md`、`docs/05-design/frontend-design.md`：原位同步既有数据和前端设计合同，不新增设计文档。

## T01：PRD 与 Markdown 需求提取

- Red：测试要求带 `sf:section-id=REQ-*|NFR-*` 的 Markdown 产生需求/NFR/AC 实体、明确状态、稳定 locator、父子关系和章节绑定。
- Green：实现最小确定性解析；在现有 PRD 第 21 章原位补齐已批准 R009 内容、分类、用户故事、验收和 NFR。
- 等价门：读取 final manifest 并锁定 contract/manifest/PM map Hash；比较 PRD 投影与 R009 的 ID、标题、优先级、规范语句顺序、AC ID/顺序/正文、NFR metric/verification。
- UI：需求正文为中文人类可读结构；不增加新页面类型。
- 验证：`pytest tests/test_project_knowledge_extractors.py`。

## T02：SQLite 绑定与 R009 退役

- Red：冷重建和 warm migration 测试要求 27 个 `source_section_key` 精确绑定自身 PRD section、64 个 AC 的父需求/顺序/状态完整、主要 locator 指向 PRD，且 registry 只精确移除 R009 requirement contract。
- Green：使用 extractor 提供的章节键写入既有列；移除 R009 当前 source include；保持历史文件不变。
- 等价门：warm after-image 与 cold rebuild 的 requirement、AC、locator、section、edge 规范化行完全相同。
- 接口：不修改 schema 和 CLI。
- 验证：`pytest tests/test_project_knowledge_index.py tests/test_project_knowledge_integration.py`。

## T03：只读站点阅读与追踪

- Red：renderer 测试要求需求顶层只列 REQ/NFR、中文分类、关系可点击、任务可返回需求、文档正文可读、技术快照默认折叠。
- Green：装配实体类型和文档正文；实现安全的确定性 Markdown 子集渲染与深链。
- 安全：正文只读取 registry 已登记的 `docs/` 文件，必须位于项目根内、不是 symlink、大小不超过 2 MiB且内容 Hash 与索引一致；一次读取同一 bytes 后校验并渲染。raw HTML、Markdown link、图片、`javascript:`/`data:` 和属性内容不解释，只转义显示。
- 权限：`shared-restricted` 只接收 public 文档正文。
- 缓存：renderer 版本升级使旧页面输入失效；同一新输入第二次生成必须稳定 cache hit。
- 验证：`pytest tests/test_project_site_renderer.py tests/test_project_knowledge_security.py tests/test_project_knowledge_pm.py`。

## T04：任务详情可读化与需求验收树

- Red：测试要求任务简报的目标、具体工作、范围、交付结果、完成条件和验证方式进入任务实体；Ledger 最新状态与简报说明按稳定任务编号合并；需求页形成产品、业务域、需求和验收标准四层树。
- Green：在现有 Markdown extractor、`pk_entity.detail_json` 合并逻辑和 renderer 中实现，不新增表、页面类型或第二套事实。
- UI：任务详情先回答“为什么做、具体做什么、完成后得到什么、怎样确认完成”；需求树使用原生 `details/summary`，支持键盘、窄屏和稳定深链。
- 缓存：升级 renderer 版本，仅由固定 CLI 刷新当前静态站点。
- 验证：`pytest tests/test_project_knowledge_extractors.py tests/test_project_knowledge_index.py tests/test_project_site_renderer.py tests/test_project_knowledge_security.py tests/test_project_knowledge_pm.py`。

## 集成与完成门

- 冷重建 SQLite 并生成静态站点。
- SQL 断言：REQ=16、NFR=11、AC=64、缺章节绑定=0、AC unknown=0、R009 当前来源=0。
- SQL 逐项断言：每个 REQ/NFR 的 `source_section_key` 对应同 ID section；每个 AC 的 parent/order/status 与 R009 等价；任务映射无缺失 endpoint 和孤儿声明。
- 浏览器或 HTML 合同检查需求列表、需求详情、任务详情、文档详情。
- 运行项目知识相关回归、Ruff、Mypy。
- 形成 evidence、implementer report、独立 review 输入；独立 review 通过后同步单一记忆入口，再用 `gitcommitzh` 精确本地提交。

## 任务—需求追踪矩阵

所有边方向均为 `Task --IMPLEMENTS--> Requirement/NFR`，强度 `strong`、置信度 `1.0`；SQLite 自动提供反向查看。声明、SQLite edge 和双方详情路由必须逐边验证。

任务端点使用人类可读任务编号作为 canonical `work_item.entity_id`。JSONL ledger 中符合稳定 ID
格式的 `task/work_item` 字段直接投影为该 ID；task brief 中 ``- 任务：`TASK-ID` 标题``
也投影同一 ID，ledger 的较高 authority 覆盖当前状态。写入关系声明前必须先校验下表十个
Task ID 均存在；任一端点缺失时失败关闭，不写孤儿边。稳定格式要求大写命名空间、
连字符分段且至少一个数字；普通自然标签继续 source-scoped。旧 source-scoped WorkItem
ID 必须登记到 canonical ID 的 alias，旧 ID 查询测试通过后才能完成迁移。

| Task | Requirement / NFR |
|---|---|
| `TASK-IMPLEMENT-003-P001-T01` | `REQ-PKI-004,005,006,009,010,012`；`NFR-PKI-005,006,011` |
| `TASK-IMPLEMENT-003-P001-T02` | `REQ-PKI-002,004,005,006,007,014,015`；`NFR-PKI-003,005,006,008,010,011` |
| `TASK-IMPLEMENT-003-P001-T03` | `REQ-PKI-001,003,005,006,007,016`；`NFR-PKI-001,002,010` |
| `TASK-IMPLEMENT-003-P001-T04` | `REQ-PKI-001,008,009,010,016`；`NFR-PKI-002,003,007,008,009,010` |
| `TASK-IMPLEMENT-003-P001-T05` | `REQ-PKI-003,011,012,013,014,015`；`NFR-PKI-001,004,005,006,007,008,010` |
| `TASK-IMPLEMENT-003-P001-T06` | `REQ-PKI-002,004,006,008,012,015`；`NFR-PKI-005,006,009,011` |
| `PK-SOURCE-MIGRATION-001-T01` | `REQ-PKI-002,004,005,015`；`NFR-PKI-006,010,011` |
| `PK-SOURCE-MIGRATION-001-T02` | `REQ-PKI-004,005,006,012,015`；`NFR-PKI-005,006,010` |
| `PK-SOURCE-MIGRATION-001-T03` | `REQ-PKI-006,008,009,016`；`NFR-PKI-003,007,008,009` |
| `PK-SOURCE-MIGRATION-001-T04` | `REQ-PKI-008` |

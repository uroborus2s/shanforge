# DESIGN-PROJECT-KNOWLEDGE-001 R001 项目知识索引与只读项目站点技术设计

## 版本信息

| 项目 | 内容 |
|---|---|
| WorkItem | `FLOW-CONTRACT-001` |
| 设计任务 | `TASK-DESIGN-002-project-knowledge-index-and-readonly-site` |
| 需求输入 | `REQ-CHANGE-PROJECT-KNOWLEDGE-001-R009` |
| 精确批准 Manifest | `8be9d829ea2a895eae043eaf054914cb03b7457a43d51c142cc4ad7f41f577ae` |
| 实现边界补充 | 后续会话已确认第一版只生成静态文件；不提供 `--open`、`--serve` 或常驻服务 |
| 设计修订 | `R001` |
| 状态 | `ready_for_same_reviewer_rereview`（iteration 4） |
| 负责人 | `uroborus` |
| 编制人 | `AI_EXECUTOR` |
| 主要读者 | 架构、数据、后端、前端、测试、文档与项目维护者 |
| 日期 | 2026-07-22 |

## 1. 设计结论

项目知识能力采用“Git 中的正式事实 + 可删除重建的 SQLite 当前投影 + 页面级静态站点 cache”三层模型。SQLite 不保存第二份业务历史；Git 与权威 Ledger 保存历史，索引只保存当前代次、构建代次和上一成功代次元数据。会话通过固定命令获取结构化结果，默认不遍历仓库、不让 AI 计算进度、不让 HTML 模板推导业务值。

第一版保持项目五层依赖：

```text
access/project CLI
  -> application/project_knowledge（用例与 ports owner）
    -> domain/project_knowledge（稳定 ID、locator、edge、receipt 规则）
      -> runtime/project_knowledge（纯提取、Hash、DTO、HTML 渲染）
        -> settings/project_knowledge（SQLite、文件系统、Git、发布与维护实现）
```

跨层装配只放在 `src/settings/composition/project_knowledge.py`。CLI 解析器不导入 SQLite、文件系统或 `settings`；可执行入口由 composition 注入 application service。

## 2. 目标与非目标

### 2.1 目标

1. 用固定命令在无变化时 100 ms 目标内返回当前站点；有变化时只解析变化来源、只重绘受影响页面。
2. 用 39 张固定表统一文档、需求、任务、测试、代码、记忆、关系、搜索、页面和 PM 十要素的当前投影。
3. 用稳定实体 ID 与可验证语义 locator 精确返回一个章节、符号或事件，不把行号当身份。
4. 输出只读、多页面、可深链、可打印、键盘可用的正式项目站点；详情页有返回按钮，不使用侧边抽屉。
5. 主会话只持久登记 `PROJECT_STATE_SYNC`，后台执行索引、记忆、状态、HTML 和有界清理。
6. 把机器 Catalog 和旧 PM generated 从 `docs/` / `.factory/pm` 的事实角色迁出，保留可核对回滚点。

### 2.2 非目标

- 不提供站点内新增、编辑、审批、拖拽或状态修改。
- 不把 SQLite、FTS、自动地图、HTML 或 cache 提交 Git。
- 不建立常驻 watcher、临时服务或自动打开浏览器的副作用。
- 不引入前端框架、CDN、外部字体或客户端状态库。
- 不修改或批准 `TASK-IMPLEMENT-002-R001`。

## 3. 事实资格和目录

### 3.1 提交 Git

```text
.factory/project-knowledge/source-registry.json
.factory/project-knowledge/relation-declarations.json
.factory/project-knowledge/id-aliases.json
.factory/catalog/ai-sdlc-catalog.source.json
src/**/project_knowledge/**
tests/test_project_knowledge_*.py
docs/ 中原位修订的人类正式文档
.factory/workitems/FLOW-CONTRACT-001/ 当前任务的设计、计划、review、evidence、ledger
.factory/memory/ 当前受控摘要
```

### 3.2 永不提交 Git

```text
.factory/index/project-knowledge.sqlite3*
.factory/cache/site/**
.factory/cache/project-knowledge/**
.factory/cache/receipts/**
.factory/pm/generated/**
```

`.gitignore` 同时使用精确目录规则和 `*.sqlite3-wal` / `*.sqlite3-shm` 防线。CLI 在执行前再次拒绝把生成目标放到 registry 或 Git allowlist 外。

## 4. Source Registry 与增量刷新

`source-registry.json` 是稳定配置，不是扫描结果。每项字段固定为：

| 字段 | 说明 |
|---|---|
| `registry_source_id` | 登记组稳定 ID，例如 `SRC-DOCS`、`SRC-PYTHON`、`SRC-TESTS`、`SRC-WORKITEMS`、`SRC-MEMORY` |
| `kind` | `markdown`、`json`、`jsonl`、`python`、`git` |
| `roots` | 项目根相对路径数组 |
| `include` / `exclude` | 确定性 glob；默认拒绝未知路径 |
| `extractor_id` | 版本化提取器 ID |
| `access_class` | `public`、`project`、`restricted` |
| `stable_id_policy` | 显式标记、正式 ID、AST 符号、JSON Pointer 或 event UID |
| `max_file_bytes` | 单文件上限，超限诊断而非偷偷截断 |

刷新算法：

1. 解析并校验 registry，realpath 必须留在项目根内。
2. 枚举已登记文件，按规范相对路径排序；每个具体文件得到 `source_id = sha256(registry_source_id + normalized_relative_path)`。`pk_source` 与 `pk_source_state` 的一行只代表一个具体文件，不代表一个 glob 组。
3. 对具体文件计算 SHA-256 并与其 `pk_source_state` 比较；Hash 未变的文件解析次数必须为 0。
4. 变化文件在内存中提取 `SourceContribution/v1`。贡献只包含允许的实体字段、专用行字段、locator、edge、搜索摘要和 block Hash，不复制完整正文。
5. 在一个 `BEGIN IMMEDIATE` 事务中创建 `building` generation。未变文件的 contribution 从父 generation 的 `pk_generation_source.contribution_json` 原样复制；变化文件写新 contribution；删除文件不复制。
6. 从旧、新 contribution 的实体 ID 并集得到 affected entity set。对每个 affected entity，按 registry authority rank 合并剩余贡献：正式 definition 优先；弱 `MENTIONS` 不能成为定义；多个同级强定义冲突则 generation 失败。实体、专用行和 `pk_search_entry` 只重算 affected set。
7. source-specific locator、section 和 edge 按具体 `source_id` 删除/upsert；同一强边的其他来源行不删除。没有任何剩余 definition/locator 的实体才删除。
8. 运行同实体多来源、断链、alias、PM key 和安全校验，计算 generation root，旧 current 改为 previous，新 generation 改为 current，再提交事务。
9. 失败回滚并写安全诊断 receipt；读者继续看到上一 current generation。

`mtime_ns + size` 只作无需读文件的快速提示；发布判断最终以 SHA-256 为准。generation root 为按 `source_id + content_sha256 + contribution_sha256` 排序后的 JCS Hash。

`pk_generation_source.contribution_json` 是固定 39 表内的来源贡献 owner，解决“未变来源不重解析”和“删除一个来源仍保留其他来源贡献”之间的冲突。previous generation 的 contribution 只为原子恢复保留；更早代次删除，历史仍由 Git/Ledger 保存。

## 5. 稳定 ID 与语义 locator

### 5.1 Markdown

- 文档 ID 来自显式 `document_id` 元数据；没有时首版使用 registry namespace + 相对路径的稳定 ID，并产生“建议补显式 ID”诊断。
- 重要章节优先读取 `<!-- sf:section-id=SEC-* -->`；需求/AC 等已有正式 ID 可直接作为 section ID。
- 标题、章节序号、行号和字节位置只用于显示或即时读取优化，不持久化为身份。
- locator：`{"kind":"markdown_section","document_id":"...","section_id":"..."}`。读取时重新解析文件并验证恰好命中一次。
- `section_key = "mdsec:" + sha256(JCS([document_id, section_id]))`，不使用字符串拼接分隔符，因此 ID 中的冒号、百分号或 Unicode 不会碰撞；`document_id` 与 `section_id` 原值仍分列保存供人类查看和 locator 验证。

### 5.2 Python

- 显式 `# sf:symbol-id=SYM-*` 或 relation declaration 的 symbol ID 优先。
- 无显式 ID 时生成可迁移 provisional ID：`py:<module>:<qualified_name>:<kind>`；signature 是 locator discriminator，不进入永久 identity。
- locator：`{"kind":"python_symbol","module":"...","qualified_name":"...","symbol_kind":"...","signature_digest":"..."}`。
- 改名/移动由 `id-aliases.json` 显式绑定；自动一拆多、多并一或多候选只写 `AMBIGUOUS_ALIAS` 诊断。

### 5.3 其他来源

- JSON：`source_id + JSON Pointer`。
- JSONL：稳定 event UID / idempotency key；缺失时该行不得成为强关系来源。
- WorkItem：`work_item_id + task_id`。
- Memory：`checkpoint_id + section_id`。
- Git：`commit + blob + path`，用于修订证据，不替代当前文档/符号身份。

一个实体可绑定多个 locator，角色为 `definition|declaration|implementation|test|evidence`。`show/context` 每次解析 locator；0 或多命中时失败关闭，不扩大读取范围猜测。

## 6. 39 张表字段级设计

所有实体表使用 `TEXT` 稳定键，SHA-256 Hash 为 64 个小写十六进制字符（256 bit），布尔值为 `INTEGER CHECK(value IN (0,1))`，JSON 列写入前按 JCS/稳定键序规范化。外键开启，删除来源贡献使用受控事务，不依赖无界级联。

### 6.1 知识核心 29 表

| 表 | 主键与关键字段 | 外键 / 约束 | 主要索引与查询 |
|---|---|---|---|
| `pk_meta` | `meta_key PK`, `value_json`, `value_sha256`, `updated_generation_id` | value hash 必须匹配规范 JSON | schema/reducer/registry pin 按 key O(1) |
| `pk_source` | `source_id PK`, `registry_source_id`, `kind`, `relative_path`, `extractor_id`, `registry_version`, `authority_rank`, `access_class`, `enabled`, `config_json` | 一行一具体文件；`(registry_source_id,relative_path)` 唯一 | `enabled, kind`、registry/path |
| `pk_source_state` | `source_id PK`, `content_sha256`, `size_bytes`, `mtime_ns`, `parse_status`, `last_generation_id`, `error_digest` | FK source；非负大小 | `content_sha256`, `parse_status` |
| `pk_generation` | `generation_id PK`, `parent_generation_id`, `status`, `source_root_sha256`, `facts_high_watermark`, `git_commit`, `as_of`, `schema_version`, `created_at`, `published_at` | status=`building|current|previous|failed`；至多一个 current | `status`, `facts_high_watermark` |
| `pk_generation_source` | `(generation_id,source_id) PK`, `content_sha256`, `contribution_sha256`, `contribution_json`, `parse_status` | contribution 是允许元数据的规范 JSON；FK generation/source | `source_id,generation_id`、contribution hash |
| `pk_artifact` | `artifact_id PK`, `source_id`, `artifact_kind`, `relative_path`, `content_sha256`, `semantic_sha256`, `access_class`, `revision_ref` | source+path 唯一；realpath 校验先于写入 | `source_id,relative_path`, kind/hash |
| `pk_entity` | `entity_id PK`, `entity_kind`, `display_name`, `summary`, `lifecycle_status`, `primary_artifact_id`, `semantic_sha256` | artifact FK；summary 经敏感字段过滤 | kind/name/status |
| `pk_entity_alias` | `alias_entity_id PK`, `canonical_entity_id`, `reason`, `source_id`, `created_generation_id` | alias≠canonical；写入时查环；canonical FK | canonical 反查、旧 ID O(1) |
| `pk_locator` | `locator_id PK`, `locator_kind`, `selector_json`, `selector_sha256`, `source_id`, `validation_state` | `(kind,selector_sha256)` 唯一；不含行号主键 | kind/source/state |
| `pk_entity_locator` | `(entity_id,locator_id,locator_role) PK`, `confidence`, `is_primary` | entity/locator FK；一个 entity+role 至多一个 primary | locator 反查实体；entity 取最小读取点 |
| `pk_relation_type` | `relation_type PK`, `inverse_type`, `strength_policy`, `is_transitive`, `description` | 强关系类型只接受 declared/formal 来源 | inverse、policy |
| `pk_edge` | `edge_id PK`, `from_entity_id`, `to_entity_id`, `relation_type`, `source_id`, `strength`, `confidence`, `evidence_locator_id`, `semantic_sha256` | 五项事实键含 source；同关系不同来源不互删 | from/type、to/type、source |
| `pk_document` | `document_id PK`, `entity_id`, `artifact_id`, `title`, `chinese_name`, `audience`, `owner`, `doc_status`, `doc_version` | entity/artifact 唯一；人类文档元数据 | audience/owner/status |
| `pk_document_section` | `section_key PK`, `document_id`, `section_id`, `entity_id`, `parent_section_key`, `source_id`, `display_title`, `display_order`, `block_sha256`, `safe_excerpt` | `section_key="mdsec:"+sha256(JCS([document_id,section_id]))`；`(document_id,section_id)` 唯一；parent 同文档 | document/order、parent、source |
| `pk_document_revision` | `(document_id,git_commit) PK`, `blob_sha256`, `content_sha256`, `doc_version`, `observed_generation_id` | 仅当前/必要 revision 元数据，不存正文 | document/recent |
| `pk_module` | `module_id PK`, `entity_id`, `layer_name`, `root_path`, `owner`, `boundary_sha256` | layer 为五层之一；root 唯一 | layer/root |
| `pk_code_file` | `code_file_id PK`, `entity_id`, `artifact_id`, `module_id`, `language`, `import_name` | artifact/module FK；路径不复制正文 | module/language/import |
| `pk_code_symbol` | `symbol_id PK`, `entity_id`, `code_file_id`, `symbol_kind`, `qualified_name`, `signature_text`, `visibility`, `semantic_sha256` | file+qualified+kind 当前 locator 唯一 | file/name、kind、qualified |
| `pk_requirement` | `requirement_id PK`, `entity_id`, `priority`, `requirement_status`, `owner`, `source_section_key` | entity FK；`source_section_key -> pk_document_section.section_key` | status/priority/owner |
| `pk_acceptance_criterion` | `acceptance_id PK`, `entity_id`, `requirement_id`, `display_order`, `statement`, `criterion_status` | req FK；display_order 仅展示 | requirement/order/status |
| `pk_work_item` | `work_item_id PK`, `entity_id`, `parent_work_item_id`, `task_kind`, `task_status`, `completion_level`, `ledger_locator_id` | parent 防环；ledger locator FK | status/kind/parent |
| `pk_test` | `test_id PK`, `entity_id`, `code_symbol_id`, `framework`, `test_kind`, `test_status`, `last_evidence_entity_id` | symbol/evidence 可空 FK | status/kind/symbol |
| `pk_memory_checkpoint` | `checkpoint_id PK`, `entity_id`, `project_id`, `task_id`, `gate_id`, `facts_high_watermark`, `schema_id`, `size_bytes`, `content_sha256`, `is_current` | current 每项目至多一条；size≤8192 才可 current | project/current、task/gate |
| `pk_search_entry` | `search_id PK`, `entity_id`, `title`, `summary`, `tags`, `access_class`, `content_sha256` | entity 唯一；只存允许摘要 | kind 由 entity join；access |
| `pk_search_fts` | FTS5：`search_id UNINDEXED,title,summary,tags` | contentless 可重建；与 search_entry 同事务维护 | BM25 中文/英文词项检索 |
| `pk_search_tri` | FTS5 trigram：`search_id UNINDEXED,title,summary,tags` | contentless 可重建；不可用时明确诊断 | ID/符号/短词模糊检索 |
| `pk_diagnostic` | `diagnostic_id PK`, `generation_id`, `source_id`, `entity_id`, `severity`, `code`, `safe_message`, `locator_id`, `diagnostic_status` | 不存秘密/原文；severity 封闭 | generation/severity、source/code |
| `pk_cache_entry` | `cache_key PK`, `cache_kind`, `relative_path`, `size_bytes`, `created_at`, `expires_at`, `generation_id`, `authorization_digest`, `content_sha256`, `legal_hold` | 仅登记 cache 根内 realpath；TTL/size 非负 | expiry、kind/generation |
| `pk_render_view` | `view_id PK`, `view_kind`, `subject_id`, `profile`, `locale`, `authorization_digest`, `generation_id`, `input_fingerprint`, `output_path`, `content_sha256`, `render_status`, `as_of`, `manifest_sha256` | view scope 唯一；current 输出必须存在且 hash 匹配 | scope O(1)、generation、subject |

### 6.2 PM 投影 10 表

每张 PM 表都有 `generation_id`、`source_manifest_sha256`、`row_sha256`、`field_values_json`。`field_values_json` 只承载 R009 field map 的低频合同字段；高频连接、筛选、排序字段必须为有类型列。

| 表 | 主键与有类型列 | 行模型 / 索引 |
|---|---|---|
| `pm_project_profile` | `project_id PK`, `project_name`, `project_status`, `manager_party_id`, `planned_start`, `planned_end`, `actual_start`, `actual_end`, `completion_ratio`, `facts_high_watermark` | 每项目一行；status/end date |
| `pm_party` | `party_id PK`, `project_id`, `party_kind`, `display_name`, `role_name`, `department`, `responsibility`, `engagement_level` | member/stakeholder；project+kind/name |
| `pm_work_plan` | `plan_item_id PK`, `project_id`, `parent_plan_item_id`, `plan_kind`, `title`, `owner_party_id`, `task_status`, `planned_start`, `planned_end`, `actual_start`, `actual_end`, `completion_ratio`, `schedule_variance` | WBS/schedule；parent/status/dates |
| `pm_risk` | `risk_id PK`, `project_id`, `title`, `description`, `probability`, `impact`, `risk_level`, `owner_party_id`, `response_strategy`, `risk_status`, `due_at` | level/status/owner/due |
| `pm_communication` | `communication_id PK`, `project_id`, `stakeholder_party_id`, `information_need`, `frequency`, `channel`, `owner_party_id`, `next_at`, `communication_status` | stakeholder/status/next |
| `pm_meeting` | `meeting_id PK`, `project_id`, `title`, `meeting_type`, `scheduled_at`, `chair_party_id`, `decision_summary`, `meeting_status` | scheduled/status/type |
| `pm_action_item` | `action_item_id PK`, `project_id`, `meeting_id`, `title`, `owner_party_id`, `due_at`, `action_status`, `completion_note` | meeting/owner/status/due |
| `pm_status_report` | `status_report_id PK`, `project_id`, `period_start`, `period_end`, `overall_status`, `completion_ratio`, `highlights`, `next_steps`, `help_needed` | project+period 唯一；overall/end |
| `pm_change_request` | `change_request_id PK`, `project_id`, `title`, `change_type`, `reason`, `impact_summary`, `requester_party_id`, `approver_party_id`, `decision`, `change_status`, `requested_at`, `decided_at` | status/type/requested |
| `pm_project_summary` | `summary_id PK`, `project_id`, `summary_status`, `scope_result`, `schedule_result`, `cost_result`, `quality_result`, `delivery_result`, `lessons_learned`, `closure_eligibility`, `closed_at` | `summary_id=pm-summary:<normalized_project_id>`；project 唯一；closure/status |

R009 field map 的 137 个 mapping 在启动时逐项验证：R014 whole-file/field-catalog/release-manifest 三 Hash 与人工批准 key 精确匹配；field ID 唯一；13 row model 的目标表、主键列、基数、source collection path、source record ID path、target key formula、parent key、reducer 和 history policy 与设计逐项一致；mapping 的 source type/path、nullable、row model、value owner、history policy 与 key formula 完整，SQLite 行必须有 `target_table + target_column`，DTO 行必须有 `target_dto + target_field`；必填 ID 缺失、父键缺失、重复 source ID 或 target key 碰撞都阻断 generation。

R009 的 137 个 `source_nullable` 当前均为 `null`，所以它只表示“合同未声明 nullable 规则”，绝不能用于推断三态。PM reducer 的可执行值状态固定为：source collection/record 未登记为 `not_registered`；record 已登记但字段缺失、null 或资格不足为 `unknown`；只有 R014 source value 或版本化 applicability rule 显式给出 `not_applicable` 才为 `not_applicable`；正常值为 `known`。四态与 value 分列进入 `field_values_json`，HTML 不自行解释。测试必须各覆盖一条 `known|unknown|not_registered|not_applicable`。

## 7. 关系与查询

强关系只来自 `relation-declarations.json`、正式 ID 引用或可证明的结构关系。全文命中只产生 `MENTIONS` 弱边。默认关系类型：`CONTAINS`、`SATISFIES`、`IMPLEMENTS`、`VERIFIES`、`BLOCKS`、`SUPERSEDES`、`DEPENDS_ON`、`EVIDENCES`、`RELEASES`、`MENTIONS`。

查询行为：

| 命令 | 读取上限 | 输出 |
|---|---|---|
| `find <query>` | 20 个命中，先 FTS 后 trigram | ID、中文名称、类型、摘要、置信度 |
| `show <id>` | 1 实体、最多 8 locator、20 直接边 | 人类摘要、当前 locator、上下游摘要 |
| `trace <id>` | 默认深度 2、最多 100 节点/200 边 | 有类型有向子图、断链诊断 |
| `context <id>` | 最多 4 文件、32 KiB | 按优先级排序的 locator 读取计划；不读正文 |

alias 解析最多 8 跳并检测环。任何 locator 0 命中或多命中返回 exit 4 和诊断；不得退化为“读整个文件”。

## 8. CLI 合同

首版固定入口由 composition 模块提供；仓内无安装模式的真实命令为：

```bash
PYTHONPATH=src uv run python -m settings.composition.project_knowledge project <command>
```

正式子命令：

```text
project index check|refresh|rebuild
project snapshot --html [--check|--rebuild] [--profile local-owner|shared-restricted]
project find <query> [--json]
project show <entity-id> [--json]
project trace <entity-id> [--depth N] [--json]
project context <entity-id> [--max-files N] [--max-bytes N] [--json]
project sync enqueue --head H --scope SCOPE [--json]
project sync head [--json]
project maintain --dry-run|--apply [--json]
```

退出码：`0 success/cache_hit`、`2 invalid_input`、`3 stale_previous_preserved`、`4 not_found_or_ambiguous`、`5 authorization_denied`、`6 index_corrupt_or_rebuild_required`、`7 concurrent_writer`、`8 internal_failure`。每次命令输出 `ProjectCommandReceipt/v1` JSON，并在非 `--json` 模式附一行中文摘要。

## 9. 站点信息架构与页面合同

### 9.1 设计系统

- 风格：克制的企业级内容优先界面；复用现有原型的蓝色主色、灰阶、状态色和紧凑密度。
- 字体：系统字体栈，不联网加载字体。
- 布局：桌面固定主导航 + 内容区；375/768 下导航变为顶部可横向滚动入口，不遮挡正文。
- 无障碍：语义 heading、skip link、可见 focus、4.5:1 对比、44 px 移动触点、`prefers-reduced-motion`、打印样式。
- 只读：无新增/编辑按钮；所有列表项用普通链接进入完整详情页。

### 9.2 页面树

```text
index.html                         总览
requirements/index.html            需求列表
requirements/<id>.html             需求详情（背景/场景/结果/AC/设计/任务/代码/测试/发布/活动）
design/index.html                   设计文档与模块地图
design/<id>.html                    设计详情
plans/index.html                    计划与里程碑
execution/index.html                WBS、任务、缺陷列表
tasks/<id>.html                     任务详情（目标/原因/范围/完成条件/进度/阻塞/代码/测试）
defects/<id>.html                   缺陷详情（实际/预期/复现/影响/根因/修复/回归）
quality/index.html                  测试、评审、断链、诊断
documents/index.html                人类文档目录及中文名称/读者/Owner/适用性
documents/<id>.html                 文档详情（用途/读者/Owner/章节/上下游/版本/来源）
code/index.html                     模块与符号地图
code/<id>.html                      符号详情与 locator/关系
quality/<id>.html                   测试、评审、诊断或断链详情
versions/index.html                 版本与发布列表
versions/<id>.html                  版本详情（范围/制品/验证/残留风险/来源）
project-management/index.html       十要素总览
project-management/<module>.html    十模块列表与全页详情入口
project-management/<module>/<id>.html  PM 记录详情（137 字段子集/来源/推导/状态）
reports/index.html                  当前状态报告、版本与生成 Manifest
reports/<id>.html                   状态报告详情
```

详情页顶部固定出现“← 返回上一列表”链接，同时保留面包屑；不使用 drawer/modal 承载详情。浏览器前进后退和直接打开深链都成立。

### 9.3 页面 freshness

`view_id = hash(view_kind, subject_id, profile, locale, authorization_digest)`；`input_fingerprint = hash(renderer_version, template_hash, generation_id 中实际消费的 entity/edge/PM row hash)`。无变化时不写文件。

发布使用不可变 build 目录与单一原子指针，不覆盖非空目录：

1. 在 `.factory/cache/site/builds/<site_id>.tmp` 写所有变化页并硬链接/复制未变化页，校验链接、权限、Manifest 和内容 Hash。
2. chmod 后 rename 为不可变 `.factory/cache/site/builds/<site_id>`。
3. 创建同目录临时 symlink `.factory/cache/site/current.next -> builds/<site_id>`，验证 realpath 仍在 managed builds 根内。
4. 用 `os.replace(current.next, current)` 原子替换 symlink；因此 `.factory/cache/site/current/index.html` 始终解析到完整旧站或完整新站，不存在空窗。
5. 崩溃发生在 pointer replace 前则旧站继续有效，发生在 replace 后则新站完整有效；旧 build 只有在无 current/reader lease/cache 引用后由维护器删除。

不支持原子 symlink replace 的平台返回 `ATOMIC_POINTER_UNSUPPORTED` 并保留旧站，不降级为两次 rename。测试必须覆盖每个崩溃点、并发读取、旧站保留和 symlink 越界。

页面 footer 显示 Git commit、事实 H、generation、`as_of`、renderer version 与 source manifest hash。墙钟 `built_at` 只写 receipt manifest，不进入页面正文 Hash。

## 10. 权限与安全

- `local-owner`：生成目录 `0700`、文件 `0600`；返回入口前验证 owner、mode、realpath 与入口内容 Hash。receipt 明确离线文件复制后的撤回边界。
- `shared-restricted`：只生成含 public/脱敏字段的静态文件；第一版不提供受限详情服务。cache hit 前重新验证当前入口的 owner、mode、realpath 与内容 Hash，失败即 fail-closed。
- registry 之外路径、symlink 越界、路径穿越、秘密模式、超大文件和未知 extractor 都进入安全诊断。
- SQLite 搜索摘要、Memory、HTML、receipt 均通过同一 `SensitiveValuePolicy`；秘密原文写入次数必须为 0。

## 11. 异步同步与 fencing

现有 `TASK-IMPLEMENT-002-R001` 的 `SystemTaskKind` 与 completion batch store 是冻结候选，R009 不修改、不导入其 SQLite 实现，也不伪装成已有 `PROJECT_PROGRESS_PROJECTION`。R009 在 `application/project_knowledge` 定义独立 `ProjectStateSyncQueuePort`，`settings/project_knowledge/sync_store.py` 用独立可忽略数据库 `.factory/runtime/project-state-sync.sqlite3` 实现 durable request/event/lease/fencing；这些 runtime queue 表不属于知识索引 39 表。

主会话在成功写入权威事实后调用固定 `project sync enqueue --head H --scope ...`，只登记 `PROJECT_STATE_SYNC`、`coalesce_key=project-state:<project_id>:<scope>` 和事实 H，P95 目标 ≤100 ms，然后立即继续。遗漏登记由 `project sync head` 比较事实 H 与 queue/index/memory/site H 并幂等补登记；因此不需要修改冻结 completion API，也不把轮询当事实 owner。执行器输入固定为 H、source root、scope、allowlist、authorization digest、idempotency key。

状态链使用 R009 的 50 条穷尽转换合同：

```text
queued -> running -> projection_ready -> memory_ready -> html_published
       -> [maintenance_committed] -> integrated -> done
```

旁路 `superseded|retryable_failed|ready_to_integrate|needs_attention|commit_not_authorized`。每次成功写入检查输入仍 current、lease 未过期、fencing token 相等。重试最多 5 次，退避上限 300 秒。后台不得在主工作树并发改文件；维护提交只允许受控 memory allowlist、只做本地 `gitcommitzh`、永不 push。未授权提交走 `commit_not_authorized -> integrated -> done`，不是失败。

## 12. Cache、压缩和维护

- 默认 cache 上限 256 MiB、TTL 24 h；每 profile 只保留 current 站点。
- Memory 压缩触发：Task/Gate/阶段关闭、会话交接、落后 50 事件、未压缩 256 KiB；活动会话不按分钟重压缩。
- `maintain --dry-run` 总是先输出精确目标、realpath、owner、引用、legal hold、字节和原因；`--apply` 只删除登记 cache。
- 当前和前一成功 generation 元数据、legal hold、被 current view 引用的 cache 不删除。

## 13. 迁移设计

迁移分为 T05 prepare 与 T06 activate；T05 不删除任何 legacy source，T06 在正式 owner、关系声明和导航 after-image 全部就绪后执行一次受控 activation：

1. T05 dry-run 读取 legacy 源，只在 `.factory/cache/project-knowledge/migration/<job_id>/after-images/` 生成 catalog、manifest、relation declaration、正式 owner/navigation 的候选 after-image，以及逐文件 disposition、before Hash、强关系 before/after 预期和回滚包；不写任何最终目标，也不删除 `docs/05-design` 或 `.factory/pm` 任何源。
2. T06 先把 R009 正式事实原位写入 `docs/04-product/prd.md`、`docs/04-product/requirements-matrix.md` 和现有设计 owner，并更新 `.factory/project-knowledge/relation-declarations.json`、`docs/05-design/index.md`、`docs/document-index.md`、`docs/index.md` 与 `.factory/memory/doc-map.md`。
3. 在 staging root 构造所有机器目标与人类 after-image，运行 source Hash、内部链接、39 表冷重建和强关系计数；任一失败不触碰当前源。
4. 校验通过后，`docs/05-design/ai-sdlc-catalog.source.json` 激活到 `.factory/catalog/ai-sdlc-catalog.source.json`；它是稳定机器配置，不在人类设计导航出现。原路径随后删除。
5. `docs/05-design/ai-sdlc-catalog.manifest.json` 激活到 `.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-DESIGN-001-R019-ai-sdlc-catalog-release-manifest.json` 作为历史发布回执；原路径删除；运行时新 manifest 进入 `.factory/cache/receipts/`。
6. `.factory/pm/README.md`、`project-brief.md`、`team-raci.md`、`milestones.md`、`wbs.md`、`risk-register.jsonl`、`communication-plan.md`、`meeting-notes/*.md`、`status-reports/*.md`、`change-register.jsonl`、`closure-report.md`、`dashboard.md` 逐项与 WorkItem/Ledger/正式文档对账。已存在的稳定事实只记录 owner locator；只存在于 legacy PM 的人工事实先写入 `relation-declarations.json` 或对应既有正式 owner；可推导 dashboard/generated 再转入 cache。未经逐文件 disposition 和强关系计数对账不删除。
7. `requirements-matrix.md` 保持唯一文件；本次增加生成来源/刷新命令/手工强关系边界，不再创建平行矩阵。
8. activation 使用同一 migration receipt 记录每个 after-image replace 与 source delete；失败时按 work item evidence rollback 包逆序恢复。只有 owner/navigation/relations 已激活且强关系丢失为 0，才允许删除 legacy 源。

## 14. 测试与性能

| 范围 | 必测行为 |
|---|---|
| schema | 39 表恰好存在、2 FTS、FK/唯一/current generation/alias 环；PM map 137 字段以及 PK/父键/key collision/cardinality/type/nullable/history/R014 pin 全覆盖 |
| incremental | 无变化解析 0、同 registry 多文件、同实体多来源后删除一源仍保留其余贡献、单文件增删改、失败回滚、并发 reader、损坏重建 |
| locator | 标题改名/前插、代码移动/改名 alias、0/多命中、JSON Pointer、event UID |
| graph | 强弱关系、同边多来源、删来源无幽灵边、断链报告 |
| CLI | 空项目、cache hit、单变化、损坏 DB、权限撤销、并发 writer、稳定退出码/receipt |
| site | 文档/质量/版本/PM record 等全部列表与全页面详情、返回链接、深链、打印、内部链接、缺失值区分、137 字段可追溯；immutable build + atomic symlink pointer 崩溃/并发测试 |
| security | traversal、symlink、secret、ACL、共享撤权并发、diagnostic 不泄漏 |
| async | 独立 project-knowledge durable queue、50 转换穷尽、幂等合并、supersede、fencing、5 次重试、commit 未授权成功收口；普通后台同步 ≤3 s |
| memory | 0/1/50/200 事件恢复夹具、单 checkpoint ≤8 KiB、P95 ≤1 s；201/超 1 MiB/超时明确 not_ready |
| performance | warm ≤100 ms、单文档/任务变化 ≤800 ms、10,000 Artifact 单来源变化 ≤500 ms、冷建目标 ≤3 s、enqueue ≤100 ms |
| deterministic | 固定 clock/as_of 两次隔离构建，页面集合、每页内容 Hash 与 Manifest 内容区完全一致；built_at 不进入 fingerprint |
| accessibility | 适用 WCAG 2.2 A/AA axe 规则零未处理 violation、375/768/1024/1440 Playwright、键盘/焦点/返回/打印和人工视觉检查全部有真实证据 |

页面用 Playwright 在 375/768/1024/1440 视口验证，并运行 axe、键盘/打印 smoke 和人工视觉检查。若本机浏览器不可用，HTML parser、链接/ARIA/响应式静态断言只能作为诊断证据，`NFR-PKI-009` 与最终资格保持未通过/阻塞，不得以静态检查替代或伪造通过。

## 15. 错误处理

- 输入错误：固定 exit 2，列出允许参数，不写任何投影。
- locator 不唯一：exit 4，返回候选 ID/安全摘要，不扩大读取。
- DB 损坏：exit 6；`check` 只报告，`rebuild` 在新临时 DB 成功后替换。
- 构建失败：上一 current index/site 保留，receipt 为 stale_previous_preserved。
- 授权失败：exit 5，清理共享 cache；清理失败进入 needs_attention。
- 并发写：短暂 busy timeout 后 exit 7；不允许两个 writer 交错发布。

## 16. Review Gate

- Spec review：39 表、137 映射、16 REQ/64 AC/11 NFR、CLI、权限、迁移和异步状态逐项覆盖。
- Quality review：分层、事务、路径安全、HTML 转义、测试可构建性和无重复事实。
- 实现者只能把设计推进到 `ready_for_review`；`approved` 必须来自独立 review。
- 正式设计 owner 只在 review 通过后原位增补；不创建新的 `docs/05-design/project-knowledge-*.md` 平行页面。

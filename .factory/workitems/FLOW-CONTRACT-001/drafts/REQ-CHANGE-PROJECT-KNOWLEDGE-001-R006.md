# REQ-CHANGE-PROJECT-KNOWLEDGE-001-R006 项目知识索引与只读项目站点需求候选

## 版本信息

| 项目 | 内容 |
|---|---|
| 需求变更 ID | `REQ-CHANGE-PROJECT-KNOWLEDGE-001` |
| 候选修订 | `R006`（完整替代 R001–R005） |
| 状态 | `ready_for_same_reviewer_rereview` |
| 日期 | 2026-07-21 |
| 提出人 | `uroborus` |
| 编制人 | `AI_EXECUTOR` |
| 父 WorkItem | `FLOW-CONTRACT-001` |
| TaskCard | `TASK-REQ-006-project-knowledge-index-and-deterministic-docs` |

## 1. 决策摘要

本候选把已经讨论确认的方向合并为一个可实现合同：正式事实继续保存在 `docs/`、源码、测试、WorkItem/Ledger、受控 Memory 和 Git 中；固定代码把这些来源增量投影为可删除重建的 SQLite 知识索引，并按需生成只读、多页面、可商用展示质量的项目静态站点。AI 会话只负责理解用户意图、调用固定命令和解释结构化结果，不负责临场重算进度、扫描整个仓库或手工拼装 HTML。

R006 完整取代 R001–R005，不与旧候选叠加解释。旧候选的原子发布、可重建和无 AI 快路径要求继续保留；权限合同修正为可验证的发布 profile：本机 Owner 的离线文件由 OS 权限保护，共享或动态受限内容必须重新鉴权后提供，不能宣称可收回已经打开或复制的离线明文。

## 2. 角色与用户结果

- 项目负责人：在会话中要求“查看项目”时，可快速获得最新或明确标记为未刷新的 HTML 路径，不等待 AI 自由总结。
- 产品与业务读者：能从需求的背景、场景、结果、验收标准一路看到设计、任务、代码、测试和发布，不需要理解内部 ID。
- 开发与测试人员：能从人类可读的任务和缺陷页面，回到精确的代码符号、测试、证据和变更来源。
- AI 执行者：默认只读取一个当前记忆点，再通过稳定语义定位器按预算读取必要片段。
- 项目维护者：能删除 SQLite、FTS、HTML 和 cache 后从 Git 中的事实与规则重建，不把生成物当成新的事实源。

## 3. 事实、投影与历史边界

### 3.1 提交 Git 的内容

正式人类文档、源码、测试、迁移、schema、提取器与 renderer 代码、source registry、稳定 ID、模块边界、关系类型定义、人工追踪声明、别名、WorkItem/Ledger、受控 Memory 摘要、发布 Manifest 和验证证据必须提交 Git。

### 3.2 不提交 Git 的内容

`.factory/index/project-knowledge.sqlite3`、FTS、自动提取的文档/代码地图、生成边、HTML 站点、构建中间文件、临时日志和其他 cache 永不提交 Git。它们损坏或缺失时必须可从已提交事实重建。

### 3.3 三种不同概念

1. `IndexGeneration`：一次成功原子发布的索引代次；只描述当前一致投影及其来源高水位，不等于项目历史快照。
2. `ProjectProgressSnapshot`：固定 reducer 在某个 `IndexGeneration` 上计算的项目状态结果；只在显式查询或权威事件触发且输入变化时生成或替换。
3. `RenderFingerprint`：某个页面在特定权限范围下的精确输入指纹；用于判断该页面是否需要重新渲染。

文档修改时不保存整库历史副本。Git 保存正文历史，Ledger 保存权威事件历史，SQLite 默认只保留当前可用代次、正在构建代次和必要的前一有效元数据以支持原子切换与故障恢复。

`ProjectProgressSnapshot/v1` 是 `project-progress-v1` reducer 从当前 `IndexGeneration` 和 PM 投影计算的非持久化 DTO；其页面 Manifest、输入指纹和当前输出登记在 `pk_render_view`，项目历史仍由 Git 与权威 Ledger 保存。

R006 使用 R014 作为精确固定但尚未批准的输入：`contract_id=REQ-CONTRACT-WF-CTL-010-001`、`revision=R014`、状态 `candidate_unapproved`、whole-file SHA-256 `836fadc2c214ef2f56b2a21ef2fb705445a58ca7ddb0047f3b638292ba578d33`、field catalog SHA-256 `658f8d805ce423e46b686e7e6da2de22d0d7e874817a153bffefdf8c0d604313`。R006 不替代 R014 的独立批准；R014 内容变化必须使本候选失效并重新评审。

## 4. 功能需求

### `REQ-PKI-001` 会话内确定性项目快照命令

- 优先级：P0。
- 系统必须提供 `shanforge project snapshot --html`。命令检查 freshness，按需增量刷新索引，计算项目快照和页面级指纹，只重建受影响页面，并返回结构化 receipt 与当前站点入口。
- 支持 `--open`、`--check`、`--rebuild`、`--serve` 和 `--profile local-owner|shared-restricted`；默认 `local-owner` 只生成当前 OS Owner 可读的静态文件，不启动常驻服务或 watcher。
- AC-1：输入及授权未变化时，命令复用最后有效站点，不写 HTML，返回 `cache_hit=true`、入口路径、代次和指纹。
- AC-2：来源变化时，仅解析登记且 Hash 变化的来源，仅渲染输入指纹变化的页面；站点经临时目录校验后原子替换。
- AC-3：索引或页面构建失败时保留上一有效站点并返回 `stale=true`、失败阶段和诊断；不得把失败产物冒充最新。
- AC-4：固定命令全程不向 AI 追问补值，不要求 AI 计算状态，不因查询创建产品任务。

### `REQ-PKI-002` 自适应且原位维护的人类文档体系

- 优先级：P0。
- `docs/` 只保存面向人的当前有效文档、图片和必要静态阅读资源。模板必须根据项目类型、受众、交付表面、部署方式和风险选择最小集合；不适用的文档不得创建。
- 需求、设计和方案变化默认修改原 Owner 文档中的稳定章节，通过 Git 历史管理版本；候选、评审、证据、缓存和机器合同留在 `.factory/`。
- AC-1：没有 UI、数据库、公共 API、部署或插件暴露面时，对应正式文档数量为 0。
- AC-2：新增正式文档必须登记中文名称、读者、Owner、适用条件、上游、下游，并证明现有文档不能承载。
- AC-3：`requirements-matrix.md` 默认是由关系图生成的阅读视图；若项目要求正式 Markdown，则只维护同一文件并标记生成来源，禁止按变更不断新建矩阵文档。
- AC-4：`ai-sdlc-catalog.manifest.json`、`ai-sdlc-catalog.source.json` 等机器文件不得继续作为 `docs/05-design` 人类设计正文；可推导内容迁入索引，稳定配置迁入 `.factory` 配置，生成回执迁入 cache。

### `REQ-PKI-003` 单一记忆点与有界定向读取

- 优先级：P0。
- 会话默认只读取一个与项目、Task、Gate、事实高水位和 schema 绑定的 `MemoryCheckpoint/v1`，编码后不超过 8 KiB。
- 需要更多事实时，索引必须返回最小文件集合和语义定位器；一次扩展读取默认最多 4 个文件、合计 32 KiB。读取理由进入会话 receipt 或系统任务事件，不建立永久 `context_ticket` 表。
- AC-1：兼容记忆点存在时，恢复阶段读取 Memory Artifact 数量为 1，默认历史 Ledger 和 `docs/` 读取数量为 0。
- AC-2：记忆点只保存恢复摘要、约束、当前 Gate、唯一下一动作和路径/ID，不复制正文、聊天、评审全文或长命令输出。
- AC-3：记忆点过期或损坏时返回结构化 `memory_recovery_not_ready` 并入队修复；不得以无界散读兜底。
- AC-4：读取片段必须由代码验证实际命中的实体或章节 ID；标题只用于搜索提示，不作为身份或唯一定位依据。

### `REQ-PKI-004` 可重建 SQLite 知识核心

- 优先级：P0。
- SQLite 默认位于 `.factory/index/project-knowledge.sqlite3`，是可重建投影，不具有独立事实资格。
- 知识核心固定为 29 张表（含 2 张 FTS 虚拟表）：`pk_meta`、`pk_source`、`pk_source_state`、`pk_generation`、`pk_generation_source`、`pk_artifact`、`pk_entity`、`pk_entity_alias`、`pk_locator`、`pk_entity_locator`、`pk_relation_type`、`pk_edge`、`pk_document`、`pk_document_section`、`pk_document_revision`、`pk_module`、`pk_code_file`、`pk_code_symbol`、`pk_requirement`、`pk_acceptance_criterion`、`pk_work_item`、`pk_test`、`pk_memory_checkpoint`、`pk_search_entry`、`pk_search_fts`、`pk_search_tri`、`pk_diagnostic`、`pk_cache_entry`、`pk_render_view`。
- AC-1：来源 Hash 未变化时不得重新解析；来源变化时可完整解析该来源，但只按稳定 ID 和 block Hash upsert 变化块，并删除该来源已消失的贡献。
- AC-2：刷新在单一写事务中发布新 `IndexGeneration`；读者只能观察完整旧代次或完整新代次。
- AC-3：删除数据库后，可仅从 source registry、正式事实、版本化 schema/reducer 和 Git 高水位重建相同语义内容 Hash。
- AC-4：29 表以外的永久索引表必须通过 schema 变更评审；不得重新引入可推导的 `doc_link`、`code_occurrence` 或永久上下文票据表。

### `REQ-PKI-005` 稳定身份、语义定位和别名迁移

- 优先级：P0。
- 索引不得持久化 Markdown 行号、字节范围或“第 N 个标题”作为主定位。不同来源使用可验证的稳定选择器：Markdown 使用 `doc_id + section_id`；需求与验收标准使用稳定 ID；代码实体使用独立 `symbol_id`，当前 `module + qualified_symbol + signature discriminator` 只是可变 locator；JSON 使用 JSON Pointer；JSONL 使用稳定 event UID；WorkItem 使用 task/work-item ID；Memory 使用 checkpoint ID + section ID；Git 使用 commit/blob/path。
- 重要 Markdown 章节必须具有不影响阅读的稳定标记，例如 `<!-- sf:section-id=SEC-AUTH -->`；显示标题允许修改。
- AC-1：标题改名、章节前插、代码行/文件/模块移动、符号重命名或兼容签名调整后，经显式稳定 ID/迁移声明，原 ID 仍解析到当前实体。
- AC-2：ID 真正变更时必须登记 alias、迁移原因和来源；读取旧 ID 可解析到唯一当前 ID并防止 alias 环。一拆多、多并一或自动匹配不唯一时只能产生待确认诊断，不得静默迁移。
- AC-3：一个实体可绑定多个 locator，并标明 `definition`、`declaration`、`implementation`、`test` 或 `evidence` 角色。
- AC-4：若 locator 无法唯一命中，命令返回诊断而不是扩大读取范围猜测。

### `REQ-PKI-006` 文档、需求、任务、测试和代码关系图

- 优先级：P0。
- 关系图必须区分人工/正式声明的强关系与提取器推断的弱关系。`SATISFIES`、`IMPLEMENTS`、`VERIFIES`、`BLOCKS`、`SUPERSEDES` 等强关系必须有来源；全文或启发式命中只能产生 `MENTIONS` 候选，不得自动升级为追踪事实。
- AC-1：可从任一 Requirement、Design、WorkItem、CodeSymbol、Test、Evidence 或 Release 沿类型化边查看上下游。
- AC-2：删除或修改一个来源后，不得遗留该来源的幽灵边；其他来源声明的同一关系不被误删。
- AC-3：追踪检查能报告缺少验收标准、设计、实现、测试或证据的断链，并给出精确来源 locator。
- AC-4：`requirements-matrix`、文档目录和代码地图均从同一实体/关系核心生成，不各自维护第二套关系事实。

### `REQ-PKI-007` 代码地图提取与快速查看

- 优先级：P0。
- 第一版代码地图针对本仓 Python 代码使用 AST 提取模块、文件、类、函数、方法、签名、导入、调用候选、接口实现和测试关联；后续语言可通过 extractor port 接入 tree-sitter 或 SCIP，不改变核心实体合同。
- AC-1：`shanforge project find <query>` 返回排序后的实体摘要和稳定 ID；`show <id>` 返回人类摘要、locator 和直接关系；`trace <id>` 返回有界上下游；`context <id>` 返回受预算约束的读取计划。
- AC-2：查代码实体时默认返回定义 locator、所属模块、调用/被调用候选、关联需求/任务/测试和 Git 状态，不读取整个文件。
- AC-3：解析失败、动态调用不确定或重复符号必须写入 `pk_diagnostic` 并显式降低置信度。
- AC-4：源码内容不复制为长期正文；检索摘要只保留允许字段，FTS 可随时删除重建。

### `REQ-PKI-008` 可商用的只读多页面项目站点

- 优先级：P0。
- 站点必须由固定 CLI 生成只读展示，不提供新增、编辑、拖拽、审批或状态修改；事实变更通过 AI 会话落入正式来源后再刷新。`local-owner` 生成完整静态文件集到 `.factory/cache/site/current/index.html`，目录权限 `0700`、文件 `0600`；`shared-restricted` 的离线文件只允许公开/脱敏字段，受限详情只能经每次请求重新鉴权的 `--serve` 返回。
- 一级导航至少包括：总览、需求、设计、计划、执行、质量、文档、项目管理、报告；详情使用独立 URL 和明确返回按钮，不使用侧边抽屉承载详情。
- AC-1：需求详情用自然语言展示背景、用户场景、期望结果、非目标、验收标准、关联设计、开发任务、代码、测试、发布和活动记录，ID 为辅助信息。
- AC-2：开发任务详情展示人类可读目标、业务原因、范围/非范围、完成条件、当前进度、阻塞、代码变更和测试证据；缺陷详情展示实际/预期、复现、影响、根因、修复和回归。
- AC-3：站点包含需求、设计、任务、缺陷、版本、文档、代码、质量和项目管理的列表与全页面详情，并支持深链、浏览器前进后退和打印。
- AC-4：页面不得伪造缺失字段；未知、未登记和不适用必须区分显示，并可回到来源。

### `REQ-PKI-009` 页面级 freshness、权限和原子发布

- 优先级：P0。
- 每个 view scope 必须由稳定 `view_kind + entity/scope ID + renderer version + locale + authorization scope digest` 定义；输入指纹另由当前代次中实际消费的实体/关系/模板 Hash 构成。
- AC-1：`shared-restricted` 的 cache hit、`--open` 和每次 `--serve` 请求必须重新校验当前授权，撤权后服务读取成功数为 0并清除托管 cache；`local-owner` 在生成/返回路径前校验 Owner 与 ACL，但明确不能撤回已经打开、复制或移出托管目录的离线文件，receipt 必须披露该残留边界。
- AC-2：某页输入未变时不得因无关来源变化重建；输入改变时只重建该页及确定受影响的索引/聚合页。
- AC-3：同一 view scope 对外只保留最后成功刷新版本；构建中目录和失败版本不对外可见并按维护策略清理。
- AC-4：所有页面显示 Git Commit、事实高水位、索引代次、固定 `as_of` 事实截止时间、renderer 版本和来源 Manifest Hash；墙钟 `built_at` 只写 receipt/Manifest 的非内容摘要区，不进入页面内容 Hash 或 `RenderFingerprint`。

### `REQ-PKI-010` 项目管理十要素完整投影

- 优先级：P0。
- 项目管理页面必须覆盖上述精确绑定但尚未批准的 R014 输入中的 10 个业务模块和 137 个唯一字段：成员与干系人、工作计划、WBS/任务分解、进度计划、风险、沟通、会议与行动项、状态报告、变更、收尾；字段来源为正式事实或确定性推导。
- SQLite 增加 10 张 PM 投影表：`pm_project_profile`、`pm_party`、`pm_work_plan`、`pm_risk`、`pm_communication`、`pm_meeting`、`pm_action_item`、`pm_status_report`、`pm_change_request`、`pm_project_summary`。总 schema 为 39 张表，其中 2 张是 FTS 虚拟表。
- 137 字段逐项 Owner、目标表/DTO、行模型、主/外键、基数、reducer 和历史策略由 `REQ-CHANGE-PROJECT-KNOWLEDGE-001.pm-field-map.R006.json` 约束，SHA-256 为 `7169c619fa75e13e4fbeb06a8e803dd9555c8f377bade641cb05e123a0895c8c`。
- AC-1：十要素总览、列表和详情均可查看并追溯来源或推导规则；校验器证明 137 个源 field ID 唯一且恰好映射一次，未映射/重复映射均失败。
- AC-2：当前状态、完成率、风险等级和计划偏差必须由版本化 reducer 计算；禁止 AI 填数或 HTML 模板自行计算。
- AC-3：现有 PM 原型仅可复用经审查的视觉 token/图标，不继承侧边抽屉和不完整字段结构。
- AC-4：`.factory/pm` 不成为事实仓；旧 PM 文件在迁移核对后转为可重建 cache 或删除。

### `REQ-PKI-011` 不阻塞主会话的异步状态同步

- 优先级：P0。
- 主任务成功写入事实后，只同步登记幂等 `PROJECT_STATE_SYNC` durable system task；Memory、索引、项目状态和 HTML 更新由隔离执行器异步完成。子 Agent 可作为执行器，但持久队列和状态机才是事实 Owner。
- 主链为 `queued -> running -> projection_ready -> memory_ready -> html_published -> integrated -> done`；若允许维护提交，则从 `html_published -> maintenance_committed -> integrated`。旁路状态包括 `superseded`、`retryable_failed`、`ready_to_integrate`、`needs_attention`、`commit_not_authorized`，合法转移、guard、终态、重试与 fencing 由 R006 机器合同逐项约束。
- AC-1：主会话登记任务后即可继续，不等待解析、渲染或维护提交；相同事实高水位和 scope 的请求幂等合并，较旧请求可被 supersede。
- AC-2：执行器使用固定输入包：主提交/事实高水位、来源根、变更 scope、允许 Git 路径、授权摘要和幂等键；不得动态扩大写集。
- AC-3：可重试失败最多 5 次、指数退避上限 300 秒；超限进入 `needs_attention`。失败保留上一有效索引/站点；新会话通过 `shanforge project sync head` 判断 Memory 是否落后。
- AC-4：不得在主任务活跃工作树中并发修改或提交；隔离 worktree 使用单调 fencing token，失租或主提交不再为祖先时不得发布/提交，转入 `ready_to_integrate` 或 `superseded`。

### `REQ-PKI-012` 生成物与维护提交的 Git 边界

- 优先级：P0。
- 异步任务只允许对受控 `.factory/memory/*.md` 或明确登记的维护事实形成独立本地维护提交，必须使用 `gitcommitzh`，不得 push。SQLite、HTML、FTS、自动地图和 cache 不得 stage。
- AC-1：提交前校验 allowlist、主提交祖先关系和 write lease；有未知 dirty overlap 时进入 `ready_to_integrate` 或 `needs_attention`，不得抢写。
- AC-2：维护提交必须绑定 job ID、输入高水位和生成器版本；过期执行器不得覆盖更新结果。
- AC-3：人工关系声明、稳定 ID、schema、提取器和 renderer 的修改属于主任务事实提交，不由后台生成物提交替代。
- AC-4：任何异步任务都无远程 push、PR、发布或部署权限；未授权维护提交时走 `html_published -> commit_not_authorized -> integrated -> done`，不把“未提交生成物”当作失败。

### `REQ-PKI-013` 有界 cache、代次和自动压缩

- 优先级：P0。
- `.factory/cache/` 默认最大 256 MiB、TTL 24 小时；当前站点每个授权 scope 只保留最后成功版本。临时构建、失败构建和过时代次在任务/Gate/阶段关闭或阈值触发时进入维护队列。
- Memory 压缩由隔离 `MemoryProjectionTask` 在 Task/Gate/阶段关闭、会话交接、落后 50 个事件或未压缩 256 KiB 时触发；活动会话不按分钟定时重压缩。
- AC-1：维护器只删除登记的 cache/generated 路径，经 realpath、owner、legal hold 和当前引用校验。
- AC-2：重复清理结果一致并报告删除数、释放字节、跳过原因、SQLite page/freelist 指标和下次到期时间。
- AC-3：计划任务只作为漏触发修复和清理兜底；没有定时器时正确性不受影响。
- AC-4：维护失败不得撤销已成立的业务事实或删除当前/前一有效恢复元数据。

### `REQ-PKI-014` 安全、权限与来源最小化

- 优先级：P0。
- 所有扫描、读取、渲染、cache 命中和文件返回都必须校验项目根边界、realpath、source allowlist、当前授权、发布 profile 和敏感字段策略。
- AC-1：路径穿越、符号链接越界和不在 registry 中的来源必须被拒绝并记录诊断。
- AC-2：密钥、Token、凭据和未授权实体进入 SQLite 检索字段、Memory 或任何 HTML 的次数为 0；`shared-restricted` 离线页面出现受限字段的次数为 0。
- AC-3：授权摘要是 view scope 的组成部分；`shared-restricted` 返回 cache 前还必须检查当前授权。撤权清除失败必须 fail-closed 并进入 `needs_attention`，测试覆盖生成/读取并发撤权。
- AC-4：诊断和 receipt 不回显敏感内容，只返回稳定 ID、允许路径和安全摘要。

### `REQ-PKI-015` 现有资料与生成物迁移

- 优先级：P1。
- 迁移必须先盘点 `docs/05-design`、`.factory/pm`、requirements matrix、AI SDLC catalog 和现有 PM 原型，再按“正式人类事实、稳定机器配置、可重建投影、临时 cache”分类；未经核对不得直接删除。
- AC-1：正式设计内容原位合并到唯一 Owner 文档，并保留 Git 历史；不按每次方案新建平行正式文档。
- AC-2：稳定配置和 schema 移至版本化 `.factory` 配置/源码目录；生成 Manifest 和 HTML 移至 cache 且进入 ignore。
- AC-3：迁移前后需求、设计、任务、测试和代码的强关系数量逐项对账，丢失为 0。
- AC-4：迁移提供 dry-run 清单、回滚点和验证 receipt，不混入 `TASK-IMPLEMENT-002-R001` 冻结候选。

### `REQ-PKI-016` 固定查询命令面

- 优先级：P1。
- 第一版至少提供：`project index refresh|check|rebuild`、`project snapshot --html [--check|--rebuild|--open|--serve]`、`project find`、`project show`、`project trace`、`project context`、`project sync head`、`project maintain --dry-run|--apply`。
- AC-1：每个命令具有固定参数、稳定退出码、JSON receipt 和简短人类摘要；输入不足时失败关闭。
- AC-2：查询命令默认只读；只有 refresh/rebuild/maintain 和任务执行器可写各自登记的投影路径。
- AC-3：命令的契约测试必须覆盖空项目、无变化、单来源变化、损坏数据库、撤销授权、部分失败和并发执行。
- AC-4：CLI 调用 application port，不把 SQLite、文件系统或 Git 逻辑放入 access 层。

## 5. 非功能需求

| ID | 要求 | 首版指标 | 验证方式 |
|---|---|---|---|
| `NFR-PKI-001` | 会话恢复 | 单记忆点 ≤ 8 KiB，兼容恢复 P95 ≤ 1 s | 0/1/50/200 事件夹具 |
| `NFR-PKI-002` | 快速查看 | 无变化 snapshot P95 ≤ 100 ms；单文档/任务变化 P95 ≤ 800 ms；当前仓冷构建目标 ≤ 3 s | 冻结仓库性能测试 |
| `NFR-PKI-003` | 增量索引 | 未变来源解析次数为 0；10,000 Artifact 单来源变化 P95 ≤ 500 ms | profiler 与 source Hash 断言 |
| `NFR-PKI-004` | 异步不阻塞 | 主会话 durable enqueue P95 ≤ 100 ms；普通后台同步目标 ≤ 3 s | durable task 集成测试 |
| `NFR-PKI-005` | 可重建性 | 空 SQLite 重建后语义实体、强关系和来源 Hash 与基线一致 | cold rebuild 与差异报告 |
| `NFR-PKI-006` | 一致性 | 读者只能看到完整旧/新代次；页面跨来源高水位漂移为 0 | crash、并发、原子替换测试 |
| `NFR-PKI-007` | 有界存储 | cache/generated 不超过配置 TTL/容量；无未登记无限增长目录 | 长周期模拟与维护审计 |
| `NFR-PKI-008` | 安全 | 越界读取和秘密泄漏为 0；`shared-restricted` 撤权后服务/cache 读取成功数为 0；`local-owner` 托管目录权限为 0700/0600 | 攻击测试、secret scan、ACL 与授权并发测试 |
| `NFR-PKI-009` | 可访问与响应式 | WCAG 2.2 AA；支持 375/768/1024/1440 px；键盘、深链、打印可用 | axe、Playwright、人工视觉检查 |
| `NFR-PKI-010` | 离线确定性 | 无 CDN；相同规范化输入与版本生成相同页面集合和页面内容 Hash；`as_of` 来自输入高水位，墙钟 `built_at` 不进入页面或 fingerprint | 固定时钟与两次隔离构建对账 |
| `NFR-PKI-011` | 架构合规 | 依赖保持 `access -> application -> domain -> runtime -> settings`；装配只在 composition | import 边界与架构测试 |

## 6. 39 张表的责任边界

| 分组 | 表 | 只保存什么 |
|---|---|---|
| 来源与发布 | `pk_meta`、`pk_source`、`pk_source_state`、`pk_generation`、`pk_generation_source` | schema/reducer 版本、登记来源、Hash/mtime 快速判断、原子发布代次与来源高水位 |
| 通用实体 | `pk_artifact`、`pk_entity`、`pk_entity_alias`、`pk_locator`、`pk_entity_locator` | Artifact 元数据、稳定实体、ID 迁移、语义选择器及其角色绑定 |
| 关系 | `pk_relation_type`、`pk_edge` | 版本化关系类型和带来源/强度/置信度的边 |
| 文档 | `pk_document`、`pk_document_section`、`pk_document_revision` | 文档身份、稳定章节、当前 Git 修订元数据，不复制完整历史正文 |
| 代码 | `pk_module`、`pk_code_file`、`pk_code_symbol` | 模块边界、文件与符号身份/签名/locator |
| 交付 | `pk_requirement`、`pk_acceptance_criterion`、`pk_work_item`、`pk_test`、`pk_memory_checkpoint` | 需求、AC、任务、测试、当前 Memory 索引字段 |
| 搜索诊断 | `pk_search_entry`、`pk_search_fts`、`pk_search_tri`、`pk_diagnostic` | 允许检索摘要、全文/模糊索引和解析/断链诊断 |
| 生成物 | `pk_cache_entry`、`pk_render_view` | cache 生命周期和页面 scope/fingerprint/当前输出 |
| PM 十要素 | `pm_project_profile`、`pm_party`、`pm_work_plan`、`pm_risk`、`pm_communication`、`pm_meeting`、`pm_action_item`、`pm_status_report`、`pm_change_request`、`pm_project_summary` | 从正式事实和 reducer 得到的当前 PM 投影，不保存第二套事实 |

39 表的字段级 schema、索引和约束属于下一阶段正式设计；本需求 Gate 使用 R006 PM field map 证明 137 字段全部具有唯一投影 Owner。映射中的 `field_values_json` 是投影扩展列，不代表正文事实仓；正式设计必须把高频筛选、连接和排序字段提升为有类型列，并保持 field map 兼容。目录 3 字段属于非持久化 `PmNavigationDTO/v1`，`ProjectProgressSnapshot/v1` 也不新增 SQLite 历史表。

## 7. 固定事实流

```text
Git 中的 docs / source / tests / config / declarations
WorkItem ledger / 受控 Memory / Git metadata
        -> source registry + deterministic extractors
        -> stable entities + semantic locators + typed edges
        -> SQLite staging generation
        -> validation + atomic current-generation switch
        -> versioned progress reducers
        -> page-scoped DTO + render fingerprint
        -> validated static multi-page site atomic publish
```

## 8. 实施约束与顺序

1. 先建立 schema、稳定 ID/locator 合同、R014/field-map pin、source registry 和迁移测试。
2. 再完成 Markdown/JSON/JSONL/Python AST/Git 提取与关系校验。
3. 再实现查询 CLI、进度 reducer、39 表 PM 投影和页面 DTO。
4. 再实现只读多页面 renderer、页面级 cache、原子发布和清理。
5. 最后接入 durable `PROJECT_STATE_SYNC`、隔离 worktree/lease 和受控维护提交。
6. 每个纵向切片测试先行；不得用临时扫描、硬编码百分比或 AI 总结绕过合同。

## 9. Gate

R006 尚未通过同一独立 Reviewer 的复审，也没有精确 Hash 人工确认。复审通过后，候选 Markdown、完整机器合同、PM field map、R014 pin、review 和 Manifest 将冻结为一个精确候选。`uroborus` 确认该 Manifest Hash 前，不得融入正式 PRD/设计、迁移现有资料或修改产品代码；确认只授权本需求进入设计与实施，不自动批准 R014 或 `TASK-IMPLEMENT-002-R001`，也不授权 Git push、PR、部署或远程动作。

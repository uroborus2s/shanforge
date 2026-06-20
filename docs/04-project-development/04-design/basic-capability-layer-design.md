# 基础能力层详细设计

**项目名称：** 山海工枢 / shanforge  
**文档状态：** `v2` 基础能力层详细设计基线  
**负责人：** 仓库维护者  
**主要读者：** 架构 | 平台开发 | 运行时维护者 | 测试  
**上游输入：** 系统架构 | 平台架构设计 | 模块边界 | Hermes Agent 源码调研报告  
**下游输出：** 基础能力层模块实现 | 具体函数实现 | 契约测试 | 实施计划  
**关联 ID：** `REQ-004`, `REQ-005`, `REQ-006`, `REQ-007`, `REQ-008`, `REQ-010`, `NFR-001`, `NFR-002`, `NFR-003`, `NFR-004`, `MOD-005`, `MOD-006`, `MOD-007`, `MOD-008`, `MOD-009`, `MOD-010`, `MOD-012`, `MOD-013`, `API-004`, `API-005`, `API-006`, `API-008`, `API-009`, `API-010`, `API-012`, `API-013`  
**最后更新：** 2026-04-15

## 1. 这份文档回答什么

本文件只回答 5 个问题：

1. 六层架构里的“基础能力层”到底由哪些完整能力包组成。
2. 当前为什么改用 `C` 纯自研重写路线，而不是 `B` 桥接优先路线。
3. 每个能力包在 `domain -> runtime -> settings` 三层之间如何落位。
4. 每个能力包需要哪些目录骨架、类型对象、服务类和函数签名。
5. 后续具体函数实现时，Hermes 的代码与功能应当如何被复用。

一句话定稿：

```text
基础能力层先由 shanforge 自己定义能力包、目录、类型和函数；具体实现阶段再选择性复用 Hermes 的成熟代码与行为。
```

## 2. 研发路线定稿

围绕 Hermes 能力吸收，候选路线有 3 条：

| 路线 | 做法 | 优点 | 问题 | 结论 |
|---|---|---|---|---|
| `A` 直接搬运 | 把 Hermes 的模块整体迁入 `src/runtime/` | 起步快 | 会反向污染 `shanforge` 的层边界、对象模型和配置约束 | 不采用 |
| `B` 接口先行 + 设置层桥接 | 先由 `shanforge` 定义上层契约，再在 `src/settings/` 中桥接 Hermes | 渐进落地容易 | 实现重心容易停在 bridge，而不是平台自己的能力包 | 不采用 |
| `C` 纯自研重写 | 先由 `shanforge` 自己完成能力分组、目录骨架、类型对象、服务接口和函数签名；再在具体函数实现阶段选择性复用 Hermes 代码与功能 | 边界最清楚、owner 最稳定、后续替换成本最低 | 前期骨架工作更多 | **采用** |

正式结论：

- 第一原则仍然是 `shanforge` 自己的分层和接口 owner 规则。
- 先写 `shanforge` 自己的能力包骨架、类型对象和服务函数，再进入具体实现。
- Hermes 的代码复用发生在“函数实现阶段”，不是“架构定型阶段”。
- 基础能力层对外只暴露 `shanforge` 自己的能力语义、读写对象和错误语义。
- 即使未来复用 Hermes，也只能作为函数内部实现参考或辅助代码来源，不能反向主导目录、协议和 owner 划分。

## 3. 基础能力层完整能力包

基础能力层不再只按单个 provider 或单个工具看待，而是按“能力包”建模。每个能力包都必须包含：

- 对上暴露的统一能力语义。
- `runtime` 内的能力服务或编排器。
- 结果对象、请求对象和治理相关对象。
- `settings` 层的后续实现接入点。
- 审批、沙箱、证据和可观测性规则。

### 3.1 能力包总表

| 能力包 | 包含的基础能力 | 主要消费者 | 研发策略 | 优先级 |
|---|---|---|---|---|
| 文件能力包 | `file_access`、`workspace_access` | `capability`、`session`、`memory`、`response` | 自研骨架优先，函数实现阶段可复用 Hermes | `P0` |
| Web 能力包 | `web_access`、`http_gateway`、`search_index` | `capability`、`memory`、`workflow` | 自研骨架优先，函数实现阶段可复用 Hermes | `P1` |
| Terminal 能力包 | `terminal_gateway`、`shell_gateway`、`git_gateway` | `capability`、`approval`、`workflow` | 自研骨架优先，函数实现阶段可复用 Hermes | `P1` |
| Browser 能力包 | `browser_runtime` | `capability`、`workflow` | 自研骨架优先，`browser_providers` 只借鉴架构 | `P1` |
| Session Search 能力包 | `session_search`、`structured_storage`、`search_index`、`vector_index` | `memory`、`session`、`gateway` | 自研骨架优先，函数实现阶段可复用 Hermes | `P0` |
| Skill Catalog 能力包 | `skill_source`、`skill_management` | `memory`、`agent_app`、`capability` | 自研骨架优先，函数实现阶段可复用 Hermes | `P0` |
| 装配支撑能力包 | `rule_source`、`profile_source`、`clock_identity` | `memory`、`session`、`agent_app` | 自研骨架优先 | `P0` |
| 存储与检索底座 | `structured_storage`、`blob_storage`、`search_index`、`vector_index` | 全部能力包 | 本仓优先 | `P0` |
| 智能推理底座 | `llm_gateway`、`embedding_gateway` | `model`、`memory`、`web_access` | 本仓优先 | `P0` |
| 治理与通道能力包 | `approval_channel`、`delegation_transport` | `approval`、`delegation`、`capability` | 自研骨架优先，已有实现可保留 | `P1` |
| 可选扩展能力包 | `todo`、`clarify`、`cronjob`、`execute_code` | 产品面或宿主面功能 | 延后实现 | `P2` |

### 3.2 能力包与层边界

每个能力包都遵守同一条层边界：

```text
domain 定义自己需要的能力接口
-> runtime 负责把这些需求收口成统一能力服务与结果对象
-> settings 负责在后续阶段接入本地实现、外部实现或 Hermes-assisted 实现
```

因此：

- `file`、`web`、`terminal`、`browser`、`session_search`、`skills` 都不是“直接给模型看的裸工具”。
- 它们首先是 `runtime` 的能力包，其次才通过 `capability registry` 被暴露为可调用 capability。
- 同一能力包既可以服务 `memory` / `session` 这类领域服务，也可以服务显式工具调用。

## 4. 跨能力统一契约

基础能力层下一轮实现先补 4 个统一对象，再补单能力包。

### 4.1 `CapabilityInvocationContext`

所有能力包都必须在同一上下文模型里执行，至少包含：

- `session_id`
- `step_id`
- `profile_id`
- `workspace_root`
- `cwd`
- `user_intent`
- `risk_level`
- `approval_ref`
- `sandbox_decision`
- `budget`

设计目的：

- 让 `file / web / terminal / browser / session_search / skills` 的行为都可审计。
- 让实现阶段不需要窥探上层临时对象。
- 为后续多入口宿主和子 Agent 隔离提供统一执行语义。

### 4.2 `CapabilityResourceEnvelope`

所有读能力和行动能力都必须能收口为统一资源信封，而不是直接向上泄漏底层返回值。统一信封至少包含：

- `kind`
- `payload`
- `artifacts`
- `citations`
- `usage`
- `warnings`
- `backend`
- `cache_key`

设计目的：

- `response` 领域可以统一组织证据和引用。
- `memory` 领域可以识别哪些结果适合作为 evidence refs，而不是把工具原始输出直接记忆化。
- `gateway` 可以稳定展示输出，而不感知底层实现差异。

### 4.3 风险闸门

基础能力层不定义业务审批规则，但必须统一接入治理闸门：

- 文件写入、终端执行、浏览器交互默认先过 `SandboxPolicyPort`。
- 高风险动作再由 `ApprovalPolicyPort` 给出放行结论。
- 所有实现都必须留下结构化事件和 evidence。
- `execute_code` 这类高组合度动作，不允许绕过单能力包的风险规则。

### 4.4 `CapabilityPackageDescriptor` 与 `CapabilityPackageRegistry`

基础能力层除了要有函数签名，还要有“能力包目录事实源”。因此每个能力包都必须发布：

- `CapabilityPackageDescriptor`
  说明这个能力包是谁、提供哪些操作、依赖哪些 provider、默认风险级别如何分布。
- `CapabilityPackageRegistry`
  作为默认容器中的统一注册表，负责把 `file_access`、`web_access`、`terminal`、`browser`、`session_search`、`skills`、`rule_source`、`profile_source`、`clock_identity` 这些能力包统一登记出来。

设计目的：

- 让后续实现阶段先有稳定的“能力包目录”和“操作清单”。
- 让容器、测试和调试入口都能统一发现当前已经搭好的能力骨架。
- 让后续 capability catalog、health、admin/debug UI 能直接消费这份注册信息，而不必反查源码目录。

## 5. 自研优先能力包详细设计

### 5.1 文件能力包

文件能力包的目标不是复制文件工具集合，而是把文件与工作区访问变成平台正式能力。

| 维度 | 定稿 |
|---|---|
| 能力职责 | 读文本、列目录、搜索路径、写回变更、生成文件差异摘要 |
| `runtime` 落点 | `src/runtime/file_access/` |
| 既有 provider | `FileSystemProviderPort`、`WorkspaceProviderPort` |
| 建议补充对象 | `FileReadResult`、`FileWritePlan`、`WorkspaceSnapshot` |
| `settings` 落点 | `src/settings/workspace/` 与未来 `src/settings/file_access/` 的后续实现接入点 |
| 证据产物 | 文件快照、diff 摘要、命中路径列表、写入审计记录 |

正式操作面：

- `read_text(path, context)`
- `read_structured(path, format, context)`
- `list_paths(root, pattern, context)`
- `search_paths(pattern, scope, context)`
- `plan_write(path, content, mode, context)`
- `apply_write(plan, context)`

实现原则：

- 先由 `shanforge` 自己定义文件能力服务、结果对象和写入计划对象。
- 后续实现 `read/search/write` 细节时，可以选择性参考 Hermes 文件工具代码。
- 写入必须强制经过 `sandbox + writeset`，不能由底层实现自己判定安全。

### 5.2 Web 能力包

Web 能力包承载“搜索网页、抓取文档、抽取正文”的统一技术能力。它和浏览器能力包不同：前者以网络文档为对象，后者以交互会话为对象。

| 维度 | 定稿 |
|---|---|
| 能力职责 | 搜索、抓取、抽取、规范化引用 |
| `runtime` 落点 | `src/runtime/web_access/` |
| 既有 provider | `HttpClientProviderPort` |
| 建议新增 provider | `WebSearchProviderPort`、`WebDocumentProviderPort` |
| `settings` 落点 | 当前首轮 local bridge 在 `src/settings/shared/web_provider.py`；后续可升格到专门 `web` 分域或 Hermes-assisted provider |
| 证据产物 | URL、标题、摘要、抓取时间、正文片段、规范化 citation |

正式操作面：

- `search_web(query, limit, filters, context)`
- `fetch_url(url, context)`
- `extract_document(url, mode, context)`
- `normalize_citation(document, context)`

实现原则：

- 先自研 `web_access` 的搜索、抓取、抽取和引用规范化函数签名。
- 后续实现抓取和抽取逻辑时，再选择性复用 Hermes 的 `web search / web extract` 行为和代码片段。
- `HttpClientProviderPort` 继续作为低层传输，不直接暴露为产品能力。
- 搜索结果和正文结果必须带引用元数据，供 `response` 与 `memory` 使用。

### 5.3 Terminal 能力包

Terminal 能力包负责把“命令执行”变成平台正式受控能力，而不是把 shell 当作通用后门。

| 维度 | 定稿 |
|---|---|
| 能力职责 | 运行命令、采集 stdout/stderr、返回 exit code、审计写集 |
| `runtime` 落点 | `src/runtime/terminal/` |
| 既有 provider | `ShellCommandProviderPort`、`GitProviderPort` |
| 建议补充对象 | `CommandExecutionRequest`、`CommandExecutionResult`、`WriteSetAudit` |
| `settings` 落点 | 当前首轮 local bridge 在 `src/settings/workspace/command_provider.py`；后续可扩成专门 `terminal` 分域 |
| 证据产物 | argv、cwd、stdout/stderr 摘要、exit code、写集审计、时长 |

正式操作面：

- `run_command(request, context)`
- `run_git(argv, cwd, context)`
- `stream_command(request, context)`
- `inspect_writeset(result, context)`

实现原则：

- 先自研终端能力的请求对象、结果对象、写集审计对象和服务签名。
- `tools/environments` 的环境抽象不直接迁入；只借鉴“本地/远程环境描述”和“执行环境句柄”这两个结构思想。
- 后续实现 `run_command / run_git / inspect_writeset` 时，再复用 Hermes `terminal_tool` 的成熟逻辑。
- 终端能力默认挂在 `approval + sandbox` 双闸门后，不允许裸跑。

### 5.4 Browser 能力包

Browser 能力包是状态化交互能力，必须与 Web 能力包分离设计。

| 维度 | 定稿 |
|---|---|
| 能力职责 | 打开页面、点击、输入、等待、抓 DOM、抓截图 |
| `runtime` 落点 | `src/runtime/browser/` |
| 建议新增 provider | `BrowserAutomationProviderPort` |
| `settings` 落点 | 当前首轮 local bridge 在 `src/settings/shared/browser_provider.py`；后续可升格到专门 `browser` 分域 |
| 证据产物 | 截图、DOM 摘要、交互轨迹、页面 URL 演进 |

正式操作面：

- `open_page(url, context)`
- `inspect_dom(session_token, selector, context)`
- `click(session_token, target, context)`
- `type_text(session_token, target, value, context)`
- `wait_for(session_token, condition, context)`
- `capture_screenshot(session_token, label, context)`

实现原则：

- 先自研浏览器会话句柄、观察对象、动作回执和服务函数签名。
- `browser_providers` 只借鉴“浏览器会话 provider 抽象”和“页面状态对象”设计，不直接整体搬迁。
- 后续实现 `open_page / click / type_text / screenshot` 时，可参考 Hermes 现有浏览器行为。
- 首版只支持单一浏览器后端，不先做 provider matrix。

### 5.5 Session Search 能力包

Session Search 不是长期记忆替代物，而是历史会话与装配解释的查询平面。

| 维度 | 定稿 |
|---|---|
| 能力职责 | 搜历史会话、切 transcript 片段、解释装配来源 |
| `runtime` 落点 | `src/runtime/session_search/` |
| 依赖底座 | `StructuredStoreProviderPort`、`SearchIndexProviderPort`、`VectorIndexProviderPort` |
| 领域下行接口 | `SessionArchiveQueryPort`、`SessionTranscriptSlicePort`、`SessionAssemblyQueryPort` |
| `settings` 落点 | `src/settings/session/` 的后续实现接入点 |
| 证据产物 | `SessionArchiveHit`、turn slice、assembly explanation、source refs |

正式操作面：

- `search_session_archive(query, profile_id, limit, context)`
- `load_session_slice(session_id, cursor, limit, context)`
- `explain_session_assembly(session_id, context)`
- `search_session_artifacts(filters, context)`

实现原则：

- 先自研 `SessionArchiveHit`、transcript slice、assembly explanation 的读模型和查询服务签名。
- 后续实现检索逻辑时，可参考 Hermes `SessionDB + session_search` 的数据切片与检索行为。
- 历史会话检索必须按 `profile` 和访问边界隔离，不能默认全局共池。
- 搜索结果默认是“证据与引用”，不是“记忆事实”。

### 5.6 Skill Catalog 能力包

Skill 能力包既包含读取面，也包含管理面；两者必须分开建模，避免高风险写操作与普通查看混在一起。

| 维度 | 定稿 |
|---|---|
| 能力职责 | 列出 skill、查看正文、安装、启停、卸载、更新元数据 |
| `runtime` 落点 | `src/runtime/skills/` |
| 既有 provider | `SkillSourceProviderPort` |
| 建议新增 provider | `SkillManagementProviderPort` |
| 领域下行接口 | `SkillCatalogPort`、`SkillMutationPort` |
| `settings` 落点 | `src/settings/skills/` 与本地 skill fs backend 的后续实现接入点 |
| 证据产物 | skill 描述符、正文快照、安装来源、启停记录、变更审计 |

正式操作面：

- `list_skills(scope, profile_id, context)`
- `view_skill(skill_id, context)`
- `install_skill(source, scope, context)`
- `enable_skill(skill_id, context)`
- `disable_skill(skill_id, context)`
- `remove_skill(skill_id, context)`

实现原则：

- 先自研 `SkillDescriptor`、`SkillDocument`、`SkillMutationPlan`、`SkillMutationResult` 和相关服务函数。
- 后续实现 `list/view/manage` 时，再选择性复用 Hermes skills 目录读取和管理逻辑。
- `plugins/memory` 不直接搬迁；skill 的业务 owner 仍是装配治理和能力治理，不是外挂记忆系统。
- skill 管理动作视为写操作，需要明确 scope 和审计记录。

## 6. 共享支撑能力设计

以下能力不是本轮新增焦点，但它们是上面 6 个核心能力包的硬依赖，必须一并纳入能力层详细设计。

| 共享能力 | 作用 | 当前口径 |
|---|---|---|
| `structured_storage` | 持久化结构化结果、状态快照、能力产物 | 继续由 `src/settings/shared/`、`src/settings/session/`、`src/settings/memory/` 本地实现优先 |
| `blob_storage` | 保存截图、附件、大块产物 | 作为 browser / response / artifact 的底座 |
| `search_index` | 关键词与过滤查询 | session search、web search、skill lookup 共同使用 |
| `vector_index` | 语义召回与 rerank | session search、memory recall 共同使用 |
| `llm_gateway` | 结构化摘要、网页抽取增强、可选 rerank | 保持 provider 解耦 |
| `embedding_gateway` | 向量化能力 | vector index 的输入底座 |
| `rule_source` | 工作区规则装配 | session / memory / capability 治理输入 |
| `profile_source` | profile 路由与分脑隔离 | memory / session assembly 的硬依赖 |
| `clock_identity` | 时间和 ID 一致性 | audit、evidence、session search 的公共元数据 |
| `approval_channel` | 高风险动作审批通道 | terminal / browser / skill_manage 等写路径复用 |
| `delegation_transport` | 子任务派发与回收 | browser / session search / execute_code 后续可复用 |

正式要求：

- 这些共享能力不能被单个能力包私有化。
- 任何后续 Hermes 复用实现都必须通过这些公共 provider 接口或统一服务接入。
- `profile_source + rule_source + skill_source` 必须和 `SessionAssemblyManifest` 对齐，形成可解释装配链。
- 当前实现已把这条链正式接入默认容器：`ProfileSourceService`、`RuleSourceService`、`SkillCatalogService` 通过 runtime 适配器进入 `DefaultMemoryDomainService.prepare_session(...)`，`ClockIdentityService` 也已通过适配器进入 `DefaultSessionDomainService` 的时钟与 ID 主链。

## 7. 可选扩展能力包

这些能力可以进入基础能力层规划，但不应阻塞第一轮能力包骨架交付。

| 能力 | 定位 | 设计结论 |
|---|---|---|
| `todo` | 会话内任务草稿与跟踪 | 更接近 `application/session` 的辅助读写面，暂不作为首批基础能力 owner |
| `clarify` | 用户补充信息请求能力 | 更接近 `access/gateway` 的反馈协议，不先做 runtime provider |
| `cronjob` | 自动化与定时触发 | 归 `automation_host + gateway`，runtime 只保留 scheduler adapter 预留口 |
| `execute_code` | 高组合度执行能力 | 定义为 `file + terminal + artifact + sandbox` 的组合工作流，不单独建裸 provider |

正式结论：

- `todo`、`clarify`、`cronjob`、`execute_code` 进入 `P2` 规划池。
- 它们的实现优先级低于 `file / web / terminal / browser / session_search / skills`。
- `execute_code` 不能跳过基础能力层治理，必须构建在现有能力包之上。

## 8. 只借鉴架构、不直接搬迁的项

以下 Hermes 资产适合借鉴结构思想，但不适合直接迁入 `shanforge`：

| Hermes 项 | 借鉴什么 | 不直接搬迁的原因 |
|---|---|---|
| `browser_providers` | 浏览器 provider 抽象、会话句柄和页面对象 | `shanforge` 先确定单后端和统一动作语义，不先引入 provider matrix |
| `tools/environments` | 本地/远程执行环境描述、环境句柄分离 | `shanforge` 先做终端能力与 sandbox 闭环，再决定多环境路由 |
| `plugins/memory` | 长期状态扩展点的拆分方式 | `memory` 业务 owner 已在 `domain/memory/`，不能再让插件机制反向主导业务语义 |
| MCP 动态适配 | 外部工具表面的发现与挂载模式 | `shanforge` 先固定契约和注册治理，再考虑动态发现 |
| `gateway/platforms` 路由 | 多宿主接入的事件标准化思路 | 这属于接口/网关层，不属于基础能力层 owner |

正式规则：

- 借鉴的是“模式”，不是“目录”。
- 任何引用这些模式的实现，都必须回到 `shanforge` 的六层架构和 consumer-owned ports 规则下。

## 9. 基础能力层开发计划

### 9.1 开发顺序

正式顺序固定为：

```text
统一信封与上下文
-> 能力包目录与类型骨架
-> 读平面函数签名（file / skills / session_search 支撑）
-> 行动平面函数签名（web / terminal / browser）
-> 具体函数实现（可选择性复用 Hermes）
-> 可选能力试验
-> 回归与契约测试
```

### 9.2 任务拆分

| TASK | 内容 | 主要交付物 | 估算（人天） |
|---|---|---|---|
| `TASK-013` | 基础能力层统一信封与模块骨架 | `CapabilityInvocationContext`、`CapabilityResourceEnvelope`、能力包目录、公共结果对象 | `1.0` |
| `TASK-014` | 文件 / 工作区 / 规则 / Profile / Skills 读平面框架 | `file_access`、`workspace_access`、`skill catalog read`、`rule/profile source` 的 `service / model / function signatures` | `1.5` |
| `TASK-015` | Web / Terminal / Browser 行动平面框架 | `web_access`、`terminal`、`browser` 的 `service / model / function signatures` 与治理接线点 | `2.0` |
| `TASK-016` | Session Search 与装配解释查询框架 | `SessionArchiveQueryPort`、`SessionTranscriptSlicePort`、`SessionAssemblyQueryPort` 对应读模型与查询服务签名 | `1.5` |
| `TASK-017` | 具体函数实现阶段（可复用 Hermes） | 在保持 `shanforge` 自研骨架不变的前提下，逐个实现 `file/web/terminal/browser/session_search/skills` 的函数逻辑 | `2.0` |
| `TASK-018` | `todo / clarify / cronjob / execute_code` 试验性设计与最小原型 | 试验文档、最小 workflow spike、是否升级为正式能力包的结论 | `1.0` |
| `TASK-019` | 基础能力层契约、集成与回归测试 | contract fixtures、function regression、sandbox / approval / audit regression | `1.5` |

合计建议投入：`10.5` 人天。

### 9.3 阶段关口

| 阶段 | 完成条件 |
|---|---|
| `BC-M1` 契约冻结 | `TASK-013` 完成，统一信封、公共对象和能力包目录定稿 |
| `BC-M2` 能力框架完成 | `TASK-014`、`TASK-015`、`TASK-016` 完成，六个能力包和装配支撑能力的函数签名全部就位 |
| `BC-M3` 具体函数首轮可用 | `TASK-017` 完成，至少 file / skills / session search 的核心函数具备首轮实现 |
| `BC-M4` 基线验收 | `TASK-018`、`TASK-019` 完成，可选能力有去留结论，回归通过 |

当前实现进度注记（2026-04-16）：

- `BC-M3` 已进入进行中状态。
- `file_access` 已有本地工作区 provider 与受控读写最小实现。
- `skills` 已有本地 skill fs provider，支持 `list / view / install / enable / disable / remove`。
- `session_search` 已有 in-memory archive provider，支持 `recent/search archive/load slice/explain assembly/search artifacts`。
- `web_access` 已有首轮 local search/document bridge，支持 `search / fetch / extract / citation normalize`。
- `terminal` 已有首轮 local shell/git bridge，支持 `run / stream / git / writeset audit`，并默认挂在 `approval + sandbox` 闸门后。
- `browser` 已有首轮 in-memory automation bridge，支持 `open / inspect / click / type / wait / screenshot` 的最小会话化能力。

## 10. 一句话定稿

基础能力层的下一轮重点，不是先搭 Hermes bridge，而是先把：

- `file`
- `web`
- `terminal`
- `browser`
- `session_search`
- `skills_list / skill_view / skill_manage`

这 6 组能力做成 `shanforge` 自己的正式能力包骨架，再进入具体函数实现；实现时可以复用 Hermes 的代码和功能，但不能让 Hermes 反向决定 `shanforge` 的能力边界。

# 技术选型与工程规则

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `DESIGN-TECH-001` |
| 正式版本 | `v3.1.0` |
| 来源候选 | `TASK-DESIGN-001-R019` |
| 发布事务 | `DESIGN-RELEASE-TX-R019-G001` |
| 负责人 | `HUMAN_ARCHITECTURE_DOMAIN_LEAD` |
| 修改 / 审核 / 批准 | `uroborus` / `uroborus` / `uroborus` |
| 状态 | 已批准并生效 |
| 上游 | `PRD 非功能要求`、`源码事实` |
| 下游 | `system-architecture`、`实现任务` |

## 文档职责

- 允许保存：技术栈；工程工具；兼容与替换规则。
- 禁止保存：安装结果；一次性实验；架构正文副本。
- 主要读者：架构、开发、测试。

## 正式内容

**项目名称：** 山海工枢 / shanforge
**文档状态：** `v2` 技术基线
**负责人：** 仓库维护者
**主要读者：** 架构 | 平台开发 | 测试 | 维护者
**上游输入：** PRD | 需求分析
**下游输出：** 系统架构 | 模块边界 | 实施计划 | 测试计划
**最后更新：** 2026-04-15

## 1. 选型原则

- 先保证平台抽象正确，再扩展适配器数量。
- 先收口契约和边界，再做能力堆叠。
- 业务开发优先面对声明式协议，而不是基础设置实现细节。
- 所有关键能力都必须可 mock、可测试、可回放。

## 2. `v2` 实现基线

| 方向 | 选择 | 原因 |
|---|---|---|
| 主语言 | Python 3.14+ | 当前工程栈一致，类型表达和脚本化能力足够 |
| 包与工具链 | `uv` | 统一 Python、依赖、锁文件和工具执行 |
| 契约建模 | Typed schema + JSON/YAML manifest | 便于 workflow、model policy、capability 定义和校验 |
| 数据校验 | Pydantic v2 风格校验模型 | 适合运行时 contract validation |
| 事件记录 | JSONL / structured event records | 便于会话回放、调试和 evidence 对齐 |
| 文档 | Markdown + docs-stratego | 延续当前文档校验链路 |
| 测试 | `pytest` + mock providers + contract fixtures | 覆盖 workflow、provider、response 和 policy |

## 3. 平台层选型

| 层 | 选择 | 不选择 | 原因 |
|---|---|---|---|
| 架构风格 | DDD / Hexagonal | 直接在脚本外包一层薄 runtime | 平台需要清晰的业务隔离与适配器边界 |
| 层边界 | 六层架构 + consumer-owned ports | 统一 ports 层 / 跨层 owner | 保证接口 owner、业务 owner 和实现 owner 清晰分离 |
| 业务开发面 | Agent App Manifest + Workflow DSL | 业务代码直接耦合平台内核 | 降低业务流开发成本 |
| 模型交互 | `LLM Runtime + LLMProviderPort + ModelPolicy` | 业务 step 直接调 SDK | 保证供应商可替换和 step 级策略 |
| 工具治理 | `Capability Registry` | 任意脚本或 shell 暴露给业务 | 保证输入输出、风险和证据可控 |
| 上下文治理 | `Session + Memory + Context Engine` | 随机拼 prompt 或默认散读全局文档 | 保证最小上下文和可恢复性 |
| 响应处理 | `Response Normalizer + Output Parser + Schema Validator` | 原始模型文本直返业务层 | 保证返回格式稳定 |

## 4. 适配器策略

遗留代码、脚本、文件合同、CLI 入口仍可被复用，但只放在基础设置层实现区中。它们的定位是：

- 作为现有能力来源
- 作为迁移期间的桥接层
- 作为平台验证阶段的快速执行器

它们不再定义产品方向，也不再进入主需求判断。

## 5. 工程规则

- `pyproject.toml` 是版本和 Python 基线事实源。
- 平台代码必须优先围绕业务模型、业务调度、基础能力和基础设置实现区组织。
- 业务 App 不允许直接 import 基础设置适配器或 storage/provider 实现。
- workflow、model policy、capability 和 response schema 必须有显式契约。
- 接口 owner 必须跟随消费者所在层定义，不允许重新引入统一 ports 层。
- 文档、测试和 `.factory/memory` 必须与平台设计同步。

## 6. 同步要求

- 需求变更时同步更新：`system-architecture.md`、`module-boundaries.md`、`api-design.md`
- 契约变更时同步更新：`implementation-plan.md`、`test-plan.md`、追踪矩阵
- 新增业务 App 示例时同步更新：PRD 与测试计划中的验证范围

## 7. 版本记录

| 版本 | 日期 | 变更内容 |
|---|---|---|
| `v2.0` | 2026-04-13 | 重写技术选型，确立抽象 Agent 平台的实现基线和适配器策略 |
| `v2.1` | 2026-04-15 | 补齐六层架构、consumer-owned ports 和基础设置层约束 |

---

## 6. Validator Profile 契约

持久验证器位于 `.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-DESIGN-001-catalog-validator.mjs`，只使用 Node.js 标准库。

| Profile | 当前职责 | 允许延后 |
|---|---|---|
| `source-red` | 对 R006 映射证明仍存在 1359 个 `design_required`，必须非零退出 | 无；这是预期 Red |
| `bootstrap` | 校验四个输入 hash、21 个类型、7 个 profile、76 条覆盖记录和路径/测试绑定 | WP-02 至 WP-10 的设计对象 |
| `cp01` | 在 bootstrap 上要求四规范、角色、17 Artifact、14 Fact Domain 和状态机 | WP-03 至 WP-10 |
| `cp02` | 在 cp01 上要求 14 阶段、123 Workflow、RouteRule 和 ActionSpec 引用闭合 | WP-05 至 WP-10 |
| `cp03` | 在 cp02 上要求 17 方法域、Skill/Prompt/Tool 和字段拓扑闭合 | WP-08 至 WP-10 |
| `cp04@0.4.0` | 要求全部设计对象、2525 条两类 coverage mapping、369 个逐场景身份绑定夹具、Catalog 完整性测试、16 类注册表驱动负例、4 个可信来源兼容结果和 final 可满足性正例闭合 | 只允许 WP-09 发布清单 |
| final@0.5.0 | 在 cp04 上要求无延期覆盖、唯一 ReleaseTransaction/v1、36/7 正式后像、37 个发布内容目标、候选集合根与两个 Gate 五字段完整 | 无 |

profile 逐级继承。后续工作包新增 schema/rule 时必须同步 validator 和负例，不能等到 WP-08 一次补齐。

## 10. Artifact Registry、存储分层与处置

目录表达职责归属，存储层表达字节资格，Artifact Registry 表达事实身份。当前项目只采用三层；外部持久存储是受控 N/A，不是发布、验证或回滚前置。

### 10.1 三层存储

| 层 | 保存什么 | 禁止保存什么 | 生命周期 |
|---|---|---|---|
| L1-GIT-AUTHORITATIVE | 正式文档、源码、测试、稳定 Builder、小型 TaskCard/Ledger、最终 Review/Human Decision、发布事件和 hash | 完整 Catalog、原始长日志、重复候选、压缩或编码 payload、会话全文 | 由正式版本和 Git 历史治理；自动 TTL 不改写历史 |
| L2-TASK-TEMPORARY | 当前任务候选、原始 Evidence、Review 过程材料、影响报告和待处置前像 | 当前正式事实、没有 TaskCard 的讨论稿、无期限大型副本 | 原始 Evidence/Review 过程材料自当前有效 completed/cancelled 事件起 PT168H；候选按终态即时处置 |
| L3-EPHEMERAL-BUILD | 完整 Catalog、隔离重建输出、变异、失败模拟和 staged after-image | 唯一事实副本、跨会话依据、正式版本 | 单次验证结束立即删除；崩溃残留由独立清理任务处置 |

外部持久存储的适用性为 N/A；受控决定记录必须恰好使用正式 PRD 的八个字段，不能用技术实现字段替换：

| 字段 | 当前批准值 |
|---|---|
| scope | 当前项目的大型候选、原始证据和可重建完整机器目录 |
| reason | 上述产物均可按期删除或由受控输入确定性重建，不需要长期持久化提供方 |
| risk | 错误分类为可删除或可重建会导致诊断材料或不可重建事实丢失 |
| alternative | Git 保存权威小记录和重建合同；临时区保存活跃候选和原始材料；TTL、引用和 legal hold Gate 控制删除 |
| approved_by | uroborus（人类） |
| approved_candidate_hash | 70e88752afd13e3aa3c3c8cec713531cb9a3370e001e224793c973ab7e7dfdfd |
| review_trigger | 出现 legal hold、不可重建业务事实、跨机器共享、灾难恢复需求或重建验证失败 |
| exit_trigger | 任一 review_trigger 经需求影响分析确认需要持久存储，并取得新的人工计划批准 |

八字段缺一项即阻断发布。只有 review_trigger 命中并完成需求影响分析与新的人工批准，才退出 N/A；AI 不得自行安装、配置或恢复外部持久存储前提。

### 10.2 十七类 Artifact 的默认资格

项目身份、正式文档、源码、测试、发布决定和最小 Ledger 属于 L1。Draft、原始 Evidence、Review 过程材料、Generated 和待处置 Archive 属于 L2。完整 Catalog 和 Build 物化属于 L3。最终 Review/Human Decision 虽由 Review 流程产生，但其资格是 L1 追加事件；不能因为过程材料到期而删除最终决定。

每类必须登记：class_id、allowed/prohibited content、fact domain、owner、默认层、状态机、保留 Profile、transition_refs、legal hold、活动引用和处置证据。解析出多个 owner、未登记层、缺生效事件或 unknown class 时拒绝消费。

### 10.3 原始证据和评审材料 PT168H

raw_evidence 与 review_process_material 的时钟从 TaskCard 当前有效 completed 或 cancelled 事件开始，使用带时区 ISO 8601 和半开区间 [start, start+PT168H)。到期前不得删，恰好到期可以申请删除，到期后可重试。任务重开会追加新事件、撤销未执行清理并从新的有效终态重算；旧事件不能原位修改。

最终 Review Decision、Human Decision、TaskCard、最小 Ledger、正式 hash、released/release_failed、纠正链和 ReleaseTransaction 最小结果没有 TTL 自动删除。legal hold 优先于全部自动清理；hold 解除后重新读取 generation，不使用旧判断。

### 10.4 候选即时处置真值表

| 对象状态 | 活动引用 | legal hold | 其他条件 | 结果 |
|---|---:|---:|---|---|
| selected | 任意 | 任意 | released、正式后像 hash 回读、发布清单可读三条件未齐 | 保留，拒绝清理 |
| selected | 0 | 无 | 三条件齐全且 generation 未漂移 | compare-and-delete，立即删除 |
| rejected/abandoned/cancelled | 大于 0 | 无 | 引用尚未替换 | 保留并登记引用影响 |
| rejected/abandoned/cancelled | 0 | 有 | hold 生效 | 保留 |
| rejected/abandoned/cancelled | 0 | 无 | generation 未漂移 | compare-and-delete，立即删除 |
| 任意 | 任意 | 任意 | 删除结果未知 | reconcile 字节、hash 和幂等键，禁止盲重放 |

compare-and-delete 固定比较 artifact_generation、active_reference_generation、legal_hold_generation、policy_generation 和 expected_sha256。删除失败不改写主交付结果；released 后失败进入 cleanup_pending，released 前失败进入发布回滚状态。

### 10.5 Catalog 紧凑源与临时完整输出

R019 发布 manifest 已归档到 WorkItem evidence；当前紧凑机器源是 `.factory/catalog/ai-sdlc-catalog.source.json`，稳定生成器是 `tools/ai-sdlc-catalog/build.mjs`。完整 JSONL 只在 L3 生成，用完立即删除。

CatalogSemanticInputBudget/v1 同时计算整个 source 和 Builder output-related literal：统一字节不超过 min(2,097,152, R016 oracle 输出字节的 35%)，统一叶数不超过 oracle 的 35%，source_records 不超过 1,024，direct-copy/constant 输出叶不超过 15%，derived 输出叶至少 65%。constant_registry 不超过 512 值且单值不超过 128 字节；fixed_parameters 不超过 256 scalar/16,384 字节；Builder literal 不超过 256/16,384 字节。

### 10.6 独立清理任务

ArtifactDispositionTask、MemoryProjectionTask 和 ProjectProgressProjectionTask 均使用独立 task ID、fork_context=false、最小 read/write set 和 outbox，不加载主任务原始上下文。登记请求属于主任务原子完成批次；worker 失败只能报告 cleanup_pending 或 projection_lag，不能把已完成主交付改回进行中。

RegressionTask 也与主上下文隔离，但不是普通投影：它不阻塞无依赖工作和会话响应，却必须阻止正式 docs、released、候选清理、TaskCard 关闭及 Git/远端动作，直到五字段 Gate CAS 进入 verification_ready。

### 10.7 Git 对象门

Gate 冻结 baseline commit、主对象库/alternates、全部 OID/type/size、index 和 worktree。验证同时扫描任务写集、untracked、index/staged、commit range，以及任务期间新增的 reachable/unreachable blob。改扩展名、压缩、先 add 后 reset、删除工作树文件或制造 dangling object 都不能绕过。

本轮基线为 commit 8539c7cdc9cdd19bb2e5c196eb99ec4b3266ab96、10,700 个对象和 docs 68/17。任何不可解释对象、需求、目录、Workflow 数或产品代码变化都阻断候选或正式化。

## 20. WP-05 全生命周期方法卡与 Skill 映射

### 20.1 十七个封闭方法域

方法域固定为：项目基线、发现/调研/Spike、需求、UX、UI、架构/领域/模块、数据/数据库、API/集成、计划/任务、实现/多端交付、测试/调试/根因、安全/隐私/合规、性能/可靠性/可观察性、Review/Verification/人工确认、Git/PR/发布/部署/回滚、运维/事件/问题/备份恢复、变更/迁移/弃用/退役。每个 Method 都有版本、适用 Workflow、权威输入、五步执行法、输出契约、Review Rubric、SkillBinding、PromptTemplate、失败回退和能力缺口。

123 条 Workflow 按业务语义绑定主方法，不只按生命周期阶段机械归类。例如安全架构、数据隐私和安全测试进入安全方法；性能架构、查询容量和负载测试进入可靠性方法；数据迁移、依赖升级和 API 弃用进入变更方法；本地提交到生产回滚进入 Git/发布方法。17 个方法均至少被一条 Workflow 使用，未绑定 Workflow 为 0。

### 20.2 本地 Skill 绑定与缺口

系统扫描仓内 37 个 `skills/*/SKILL.md`，保存名称、描述、路径和文件 SHA-256。命中生命周期职责的 30 个 Skill 深读其触发、边界、输入输出、验证和失败语义后形成 58 条 SkillBinding；每条绑定保存与源 Skill hash 一起冻结的 `source_contract`，逐 Skill 写明真实触发、拥有能力、禁止能力、允许 Workflow、状态输出和失败回退。Workflow 只引用明确适用于自身的绑定，不再把同一 Method 的全部 Skill 无差别复制给每条流程。

`gitcommitzh` 只绑定本地提交工作流程 `WF-DEL-004`，只产出本地 commit SHA、中文提交说明和提交范围验证；分支、Push、PR、Merge、发布和部署均在其禁止范围内。`requesting-code-review` 只组织评审，`verification-before-completion` 只产生新鲜验证证据；二者即使服务发布流程也不能执行远端或生产副作用。Skill 只执行方法内动作，不能替代确定性路由、角色授权、独立 Review 或 HumanDecision。

数据库、安全/SRE、远程 PR/部署和生产运维缺少可独立承担专业裁决的本地 Skill，分别登记到 `HUMAN_DATABASE_LEAD`、`HUMAN_QUALITY_SECURITY_LEAD` 和 `HUMAN_RELEASE_OPERATIONS_LEAD`。这些缺口允许 AI 准备材料和运行已授权工具，但禁止 AI 假装已完成专业审核或生产授权。

### 20.3 项目资料交互方法

项目资料收集先回读 `.factory/project.json` 和已确认事实，已知字段不重复询问；缺失字段按每批最多三个问题交互。必须覆盖真实人员与角色、产品表面、服务、环境、质量、安全、合规和确认记录。人员姓名、审核人、批准人取不到时必须询问，不能写 AI 产品名或模型名代替。每轮回复列出已确认、仍缺失、阻断项和保存位置。

### 20.4 UX、UI、数据库和 API 专门方法

- UX：从 Persona/Jobs、真实场景和内容形成旅程、服务蓝图、信息架构、任务流、线框/原型及可用性/A11y 验收。
- UI：输出设计系统/Token、页面和组件清单、完整状态矩阵、响应式/A11y、真实视觉资产、桌面/移动截图验证和开发交接；实现提示必须沿用项目框架与组件库，不能用营销页面代替实际工作界面。
- 数据库：从 BusinessField、领域规则、查询和事务推导 ERD、字段字典、主外键/唯一/检查约束、查询-索引矩阵、容量、迁移/回填/校验/回滚和数据库 Review Rubric。
- API：先列消费者、用例、资源/操作和权限边界，再定义 endpoint/event、请求响应 schema、稳定错误 code、分页/过滤/幂等/限流、兼容/弃用、OpenAPI 和 Contract Test。

数据库列、API 字段和 UI 控件仍必须引用同一 BusinessField ID；具体跨层字段结构和断链验证由 WP-07 完成，WP-05 不提前伪造追踪结果。

### 20.5 PromptTemplate 与执行规则

WP-05 定义项目资料收集、通用方法执行、UX、UI 生成、数据库、API 和独立评审七类中文 PromptTemplate。每个模板都有独立的版本化变量和机器产物 schema：UI 必须产出页面/组件、Token、状态矩阵、响应式/A11y、资产和截图证据；数据库必须产出 ERD、字段字典、约束、查询索引和迁移回滚；API 必须产出 endpoint/event、OpenAPI、错误、权限、幂等兼容和契约测试。八字段会话回复由 ResponseTemplate 负责，不再冒充 Prompt 的专业输出契约。

PromptTemplate 只组织方法输入、动作和专业产物，不授予文件、网络、Git、PR 或生产权限；具体 ToolPolicy 由 WP-06 负责。任何方法遇到关键输入缺失、事实冲突、无 owner 缺口、验证失败、Review 退回或人工 Gate 时，停在当前步骤并返回可恢复状态。

## 21. WP-06 工具策略、会话回复与人机交接

### 21.1 工具分类与默认拒绝

工具注册表包含 13 类：文件读取、文件写入、命令与进程、浏览器、网络、图像、文档与表格、外部连接器、独立子代理、本地 Git、远端 Git/PR、构建发布部署、生产操作。工具是否安装、当前是否可调用、AI 是否知道调用方法，都不等于已获授权。

`TOOL-PERMISSION-EVALUATOR-001` 固定按以下顺序求值：工具类别已知、可信 RouteDecision、可信 RoleAssignmentEvaluation、ActionSpec 引用该 ToolPolicy、可信 ScopeEvaluation 与路径规范化、可信 Artifact Gate、可信 OperationRequest、需要时的可信人类授权和可信消费回执、证据与补偿已准备。可信事实只能由 `TRUSTED-RUNTIME-FACT-LOADER-001` 从追加 ledger 或 hash 绑定快照加载；工具请求只提交事实 ID，不能提交 `route_and_action_current=true` 等布尔值自证权限。

Route、角色、scope、Artifact、操作请求、授权和消费记录都必须校验自身 canonical SHA-256，并绑定同一 ActionSpec、actor、subject/hash、目标和求值时间。仓库路径必须是相对路径，规范化后仍位于 ScopeEvaluation 的允许前缀；`..` 逃逸、损坏 hash、缺 owner 或缺可信记录一律拒绝。任一步失败立即返回具名原因码；模型推荐的工具只能是候选，不能覆盖规则决定。

单条事实的自哈希只证明该对象内部一致，不能证明它来自已登记来源。来源登记由 `settings` 装配的只读快照端口从追加 ledger 头或冻结快照加载；动作求值函数只接收事实 ID 和来源登记 ID，不接收可由调用方构造的登记对象。求值器加载登记后，再验证 `LoaderAttestation`、逐事实唯一 `FactSourceBinding`、独立来源记录 hash 和当前事实 hash；来源记录 hash 必须由来源记录封套计算且不能等于事实自哈希。登记不存在、ID 不匹配、同一事实零条或多条绑定、来源记录未纳入快照时全部拒绝。普通权限和 29 个高风险 ActionSpec 都执行同一规则。

### 21.2 四个 ToolPolicy

| ToolPolicy | 用途 | 关键允许条件 | 典型拒绝 |
|---|---|---|---|
| 最小必要读取 | 文件、命令、浏览器、网络、文档、连接器和只读子代理 | 目标属于 ActionSpec 读集，来源有效，敏感信息已脱敏 | 默认读归档、原始秘密、模型扩大读集、只读名义下委派写入 |
| 受控 Artifact 写入 | 候选文件、生成资产、命令写入、浏览器/连接器变更和有写集的子代理 | 输出契约、路径 resolver、精确写集、前像/追加规则和当前 Gate 同时通过 | 讨论直接写 `docs/`、未登记路径、无发布门改正式文档、隐式 commit |
| 输出验证与回读 | 测试、构建检查、hash 回读、浏览器验收、外部状态回读 | 当前输出 hash 与验证目标一致，命令和期望退出码已声明，验证无未声明副作用 | 只凭文件存在宣称完成、无新鲜退出码宣称测试通过、隐藏截断输出、作者自审冒充独立评审 |
| 高风险逐项人工授权 | 本地 commit、分支、Push、PR、Merge、发布、部署、数据和生产操作 | 固定 human 授权逐值匹配 ActionSpec、action/tool/operation kind、参数 hash、目标、scope、subject/hash、assignment、有效期和 ActionRun；单次消费回执先于副作用 | AI 生成授权、跨工具/动作复用、空 scope、缺参数、缺消费回执、未确认即开 PR、未知副作用盲重试 |

四个策略都产生追加式 `ToolEvent`，记录 ActionRun、策略、工具类别、操作、目标、参数 hash、权限决定、开始/结束时间、结果码、输出引用/hash、副作用、脱敏和补偿引用。原始 secret 不得进入 ToolEvent；缺输出、截断输出或不确定副作用不能写成成功。

### 21.3 PR、提交和生产动作

`local_commit`、`create_branch`、`push`、`create_pull_request`、`merge`、签名、版本写入、部署、回滚、数据变更和生产操作均是独立高风险 ActionSpec。每个 ActionSpec 固定唯一 ToolKind、OperationKind 和参数 schema。创建 PR 每一次都必须由人类明确授权，并绑定 ActionSpec、OperationRequest、ActionRun、远端 Git ToolKind、`create_pull_request` OperationKind、repository、head/base branch、draft、commit、参数 hash 和 subject hash；空 scope、跨生产工具复用或缺任一字段均拒绝。

授权在副作用前以稳定键 append/fsync/readback，形成绑定当前 ActionRun 的 `AuthorizationConsumptionReceipt`；只有 append 已提交、fsync 成功、readback 精确匹配、消费次数为 1 且副作用尚未开始时才允许执行。重复策略只允许 `single_use`。目标、scope、subject、assignment、工具、操作、参数或动作种类不一致时拒绝；授权过期时重新请求人类决定；执行结果不确定时先回读远端或生产状态，禁止盲重试。

### 21.4 会话中间更新

项目化会话在任务开始、Workflow/工作包切换、文件编辑前、关键命令前后、子代理派发或返回、自动整改轮次变化、阻断或范围变化时必须给用户短更新。持续执行期间最长静默时间为 30 秒；更新至少说明当前目的、正在做什么、观察到的进度和下一动作。

中间更新不是最终回复，不能宣称任务完成，也不能只把结果写入文件后让会话无回执。子代理或自动 loop 返回后，主 AI 必须把评审结论、当前状态和下一步带回当前会话。

### 21.5 七类中文最终回复

所有项目化会话最终回复固定按八个字段组织：本轮目的、已经完成、产物与路径、验证结果、当前状态、用户需要做什么、明确未做、下一步。字段不得省略；确实没有内容时必须写“无（原因）”。机器 ID、WP/CP 编号和状态码首次出现时必须同时给出中文名称或用途，禁止只返回一串编号和链接。

`RESPONSE-CONTENT-EVALUATOR-001` 还必须绑定当前 subject/hash、真实状态、已登记 Artifact refs、验证 evidence refs 和正式发布状态。`artifacts=有`、`verification=已通过`、无证据的 `done`，以及“候选已获人工批准并正式生效”等同义假报均拒绝；验证必须给出命令/证据引用和退出码/结果，未运行时必须写原因。

“引用格式像路径”不等于引用已登记。回复求值器按 `reference_registry_id` 从 `settings` 只读快照端口加载 `ReferenceRegistry`，调用方不能直接传入登记对象；上下文 ID 必须与加载结果完全一致。每个 Artifact/Verification 记录必须恰有一条独立来源绑定，来源记录 hash 不能等于记录自哈希。Verification 还必须保存 `expected_exit_code` 并执行结果矩阵：退出码 0 才能是 `passed`；非零且期望为 0 才能是 `failed`；非零退出码与已登记预期值相同才能是 `expected_red`。ID、subject/hash、来源绑定、命令、退出码、结果或 evidence 任一不一致均拒绝。

| 模板 | 使用场景 | 附加内容 |
|---|---|---|
| 直接咨询与解释 | 无项目副作用的回答 | 答案、依据/假设、无项目写入、可选后续 |
| 缺少输入 | 关键输入缺失或无效 | 已知事实、每批最多三个问题、阻断原因、恢复节点 |
| 阶段或动作完成 | 节点、工作包或任务完成并在本轮停止 | 中文工作流名称、完成范围、新鲜验证、继续或停止位置 |
| 独立评审交接 | 等待评审或评审退回 | 对象/目的、修订/hash、Reviewer 和只读范围、发现与待处理项 |
| 人工确认 | 人工决定或显式授权 Gate | 待确认对象/hash、允许决定、影响/风险、未决定前禁止动作 |
| 阻断/失败/取消 | 权限、事实、验证、范围、未知副作用或取消 | 第一失败条件、已尝试动作、副作用/未写入、恢复条件 |
| 高风险动作结果 | 高风险动作已执行、被拒绝或状态不确定 | 授权绑定、真实工具结果、目标回读、副作用、补偿/回滚 |

`RESPONSE-TEMPLATE-SELECTOR-001` 按高风险结果、人工确认、评审、缺输入、阻断、直接回答、普通完成的优先级唯一选模板；零匹配进入阻断模板，模型不能自行改选。Session 的 `stopped/waiting_user/waiting_review/blocked/failed/cancelled` 和 Workflow 的人工确认、缺输入、评审、退回、暂停、阻断、失败状态均有确定模板。

### 21.6 继续、停止与 HandoffPackage

当前 Action 已提交、下一动作已在既有授权内、没有人工/评审 Gate、没有关键输入缺失、事实或范围冲突、验证失败或不确定副作用时，AI 应在同一会话继续，不能仅因“刚创建计划”“刚创建任务卡”“完成一个内部工作包”或“一个工具调用返回”随意停下。

缺输入、独立评审 Gate、人工决定 Gate、显式高风险授权 Gate、范围变化、事实冲突、权限拒绝、验证失败、不确定副作用、loop 上限或用户暂停/取消时必须停止。停止前生成 `HandoffPackage`：绑定项目、WorkItem、TaskCard、WorkflowRun、当前 Workflow/Node、封闭 Session/Workflow 状态、八项回复内容、待决 Gate、第一失败条件、subject/hash、`reference_registry_id` 和恢复点。Artifact/verification 必须通过该 ID 从只读快照端口加载并解析为当前 subject/hash 的登记记录，调用方传入的登记对象无效；`current_status` 必须等于 Workflow 状态，`subject_sha256` 和创建时间必须合法，最后以 canonical payload 计算 `handoff_sha256`。Memory 只保存该包的精简投影和引用，不复制正式文档正文或秘密；直接咨询且 `project_effect=none` 时只在会话返回，不写项目状态。

### 21.7 WP-06 适用性与下一步

WP-06 的图形 UI 适用性为 `N/A`，因为交付的是会话文字和结构化交接契约。替代验收是中文字段顺序、模板确定性选择、全部停止状态覆盖、工具权限真实求值以及未授权文件写入、网络、子代理、Git、PR、部署和生产动作负例。

CP-03 R004 已把来源登记移出动作求值输入，并要求唯一来源绑定和独立来源记录 hash；同一 Reviewer Russell 对 CP-03 R004 给出 `approved / 100`，对 CP-02 R008 当前候选影响给出 `approved`。用户已确认关闭 CP-03 并进入 WP-08；该确认仍不授权正式落档、提交、PR、Merge 或部署。

## 23. WP-08 验证器和黑盒测试设计

### 23.1 五个验证接口

WP-08 在 Catalog 的 `wp08_scope.interface_contracts` 中定义五个结构化接口，Markdown 不复制第二套字段定义：

| 接口 | 用途 | 核心字段 |
|---|---|---|
| `ValidationResult` | 一次 profile 求值的完整结果 | profile、阶段、状态、是否有效、检查点资格、Finding、覆盖、兼容结果和输入/验证器 hash |
| `Finding` | 可定位的验证问题 | 稳定 ID、严重度、原因码、消息、对象引用和证据引用 |
| `CoverageMetric` | 分子/分母可重算的覆盖结果 | 指标 ID、分子、分母、状态和来源 |
| `NegativeCase` | 真实内存变异负例 | 负例 ID、变异类型、目标指针、期望决定、原因模式和 runner |
| `CompatibilityResult` | 正式输入只读兼容检查 | 来源路径、预期/实际 hash、兼容决定和变化类别 |

`cp04` 和 `final` 的命令输出保留原有 `errors/metrics`，同时输出符合 `ValidationResult` 的结构化 envelope。Finding 由实际错误确定性生成，不能预填“通过”；CoverageMetric 和 CompatibilityResult 来自本次真实运行。

### 23.2 369 个流程级可执行夹具

123 个 Workflow 各有三个固定场景，共 369 个：

1. `happy_path`：唯一 RouteRule 命中，权威输入、角色绑定、事实和权限有效；实际求值必须完成声明动作引用并进入 `closed`。
2. `missing_input`：删除必需权威输入；必须在入口节点进入 `needs_user_input`，项目写入为 0，并保留恢复节点。
3. `unauthorized_or_conflict`：高风险流程删除人工授权时进入 `pending_human_confirmation`；普通流程注入事实冲突时进入 `blocked`；项目写入均为 0。

实际结果分布必须固定为：123 个 `complete`、123 个 `needs_user_input`、15 个高风险 `needs_human_decision` 和 108 个普通冲突 `blocked`。只核对场景总数而不核对分支结果，不能通过 CP-04。

每个 test_case 保存输入夹具、独立 oracle、oracle hash、证据字段、正式输入兼容引用和负例引用。test_case、fixture 和 oracle 必须逐行绑定同一组 `test_case_id / workflow_id / scenario_kind / source_binding_sha256`；fixture 的路由信号、生命周期阶段、角色分配、权威输入、缺失键、冲突标志、事实状态和权限状态必须与该 Workflow 和场景类型完全一致。求值器只接收 fixture，不接收 test_case 或 oracle；它先从 Catalog 的 RouteRule、Workflow、ActionSpec、Method、ToolPolicy 和 ResponseTemplate 推导实际结果，再读取 oracle 比较。全部运行在内存副本中，产品和项目事实写入为 0。

### 23.3 Catalog 完整性与真实负例

`TEST-CATALOG-INTEGRITY-001` 负责 Catalog 级完整性。它登记并实际运行 16 类变异：

- 删除 test_case、恢复延期状态、复制 fixture ID。
- 删除路由信号、把缺输入伪写成功、让未授权场景产生项目写入。
- 指向未知 Workflow、删除证据字段、使用非法初始状态。
- 破坏源场景指针、删除负例登记、把已完成 WP-08 coverage 恢复为延期。
- 在同一 Workflow 内交换正常场景与缺输入场景的 fixture/oracle。
- 跨 Workflow 交换高风险缺授权场景与普通事实冲突场景的 fixture/oracle。
- 伪造正式输入兼容路径、篡改负例的变异类型/目标指针/预期原因。

验证器内只有一份封闭的负例注册表。Catalog 登记必须逐字段与它一致；执行器按同一登记的 `mutation_kind` 选择处理器，并按同一登记的 `expected_reason_pattern` 判断结果。每个变异都在内存副本上重新调用同一 `validateWp08`，只有命中预期错误模式才算负例通过。删除数据、篡改登记或直接写一个 `rejected=true` 布尔值都不能满足验收。

### 23.4 覆盖与兼容边界

- 77 条需求覆盖和 2448 条源指针迁移合计 2525 条；原覆盖与新增 `REQ-CHANGE-WF-CTL-010-001` 均绑定可执行测试。
- WP-08 完成后只允许 WP-09 的 3 条发布事务覆盖保持延期；WP-01 至 WP-08 的延期数必须为 0。
- PRD、需求矩阵、文档索引和 R006 Workflow 映射按四个冻结 SHA-256 做只读兼容检查。`source_key / source_path / expected_sha256` 必须同时与验证器内可信来源和 Catalog metadata 绑定完全一致；CompatibilityResult 只输出可信路径，不回显未经核对的路径。实际 hash 或来源绑定任一漂移都使 `cp04` 失败。
- WP-08 只新增此前明确归属 WP-08 的 test_case、`cp04` 和 `final` 路径，不改变 CP-01 至 CP-03 共享规则；仍必须重跑三个 profile，并由 CP-04 Reviewer 核对影响集合为空。

### 23.5 R017 对旧 final/WP-09 合同的继承资格

R006 至 R016 中关于 68→43、107/158 个发布目标、仓外对象存储、逐文件归档 payload 和四层存储的 final/WP-09 合同均已被正式 PRD v3.3.0 取代，执行资格为 false。可继承内容只限于 123 条 Workflow、方法、角色、字段追踪、会话回复和验证思想；任何机器消费者不得从历史计数恢复发布动作。

### 23.6 当前 final 验证边界

R019 的 68/17 前像、37/7 后像和 38 个发布目标作为历史发布合同保留在 Git 与 evidence；T06 当前基线把 docs 收敛为 34 份人类 Markdown，Catalog 源迁至 `.factory/catalog/ai-sdlc-catalog.source.json`，稳定 Builder 继续保留。

## 31. V4 验证和五字段 Gate CAS

候选冻结后按版本化风险策略计算，本轮因稳定 Catalog 工具、Git 对象 Gate 和正式发布基础设施变化，最低 V4。RegressionTask 使用独立上下文，必需测试必须 passed 且 failed/skipped/not_run 都为 0。

VerificationGateCAS/v1 的五字段固定为 parent_task_id + gate_id + artifact_hash + test_plan_hash + gate_generation。RegressionTask 只能把 GATE-R017-VERIFY 从 verification_pending 推进到 verification_ready；wrong parent/gate/hash/generation、infra_failed 或晚到结果只保留证据。verification_ready 不等于 release_ready。

独立 Review Decision 必须绑定同一 artifact_hash；人工计划必须绑定 GATE-R017-HUMAN 当前五字段、验证 generation、Review Decision hash 和候选 manifest hash。只有 verification_ready、review approved、human approved 且无漂移，权威原子批次才进入 release_ready。

<!-- sf:section-id=PROJECT-KNOWLEDGE-TECH -->
## 项目知识技术选择增补

索引采用 Python 标准库 `sqlite3`、WAL 增量查询、FTS5/trigram 搜索和单文件原子重建；Markdown 使用确定性 heading parser，Python 使用标准库 AST，JSON 使用 Pointer，JSONL 使用 event UID。首版不引入向量数据库、图数据库、前端框架或常驻 watcher，以降低维护和上下文成本。

HTML 由固定 Python renderer 离线生成完整静态文件集。代码符号汇总进代码文件详情并保留稳定锚点后，当前真实仓约 460 个来源生成约 760 个页面；无变化快照通过 source discovery cache、page-input fingerprint 和已验证 manifest 直接复用，适合在 AI 会话中调用。真实当前仓同进程无变化测量使用 20 个样本和最近秩 P95，当前证据为 32.884 ms，包含全部页面摘要校验；单个既有 Python 来源变化的完整 CLI 五样本为 0.69、0.69、0.69、0.69、0.70 秒，最近秩 P95 为 0.70 秒，计时包含索引、PM、渲染、逐页摘要校验和原子发布。

增量页面发布优先使用 macOS/APFS `clonefile` 的 copy-on-write 整树克隆，不创建跨 build hardlink；非 APFS 环境退化为普通复制。SQLite 使用 WAL、`synchronous=NORMAL`、批量 SQL 和 32 MiB page cache；它和站点都属于可重建派生物。SQLite、站点和 cache 由 `.gitignore` 排除，可从 Git 中稳定事实重建。

## 正式版本历史（仅已发布）

| 版本 | 日期 | 变更 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v3.0.0` | 2026-07-18 | 基于 `TASK-DESIGN-001-R019` 正式落档 | `uroborus` | `uroborus` | `uroborus` |
| `v3.1.0` | 2026-07-22 | 确定 SQLite/FTS、AST、静态 HTML、增量指纹和不提交派生物的技术基线 | `uroborus` | `uroborus` | `uroborus` |
| `v3.2.0` | 2026-07-22 | 增补代码文件级静态页、逐页摘要校验和 0.70 秒增量基线 | `uroborus` | `uroborus` | `uroborus` |

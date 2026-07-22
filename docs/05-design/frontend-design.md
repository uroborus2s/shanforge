# 前端架构与页面设计

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `DESIGN-FRONTEND-001` |
| 正式版本 | `v1.3.0` |
| 来源候选 | `TASK-DESIGN-001-R019` |
| 发布事务 | `DESIGN-RELEASE-TX-R019-G001` |
| 负责人 | `HUMAN_DEVELOPMENT_EXECUTOR` |
| 修改 / 审核 / 批准 | `uroborus` / `uroborus` / `uroborus` |
| 状态 | 已批准并生效 |
| 上游 | `PRD`、`module-domain-design`、`api-design`、`BusinessField` |
| 下游 | `ux-ui-design`、`前端实现`、`E2E 测试` |

## 文档职责

- 允许保存：Web、App、小程序和管理后台边界；路由；页面；组件；状态；权限；字段绑定。
- 禁止保存：视觉稿正文；接口契约副本；任务进度。
- 主要读者：架构、前端、UX、UI、测试。

## 正式内容

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

## 22. WP-07 交付拓扑、纵向切片与 BusinessField 追踪

### 22.1 树负责归属，边负责矩阵关系

目录和导航必须是一棵树，否则人和 AI 都难以确定唯一 owner；软件关系本身是矩阵，不能靠复制目录表达。`TOPOLOGY-DELIVERABLE-001` 因此同时定义：

1. 每个 DeliverableNode 只有一个 `canonical_parent_node_id`，用于导航、owner、路径和版本归属。
2. 产品表面消费服务、服务实现领域、模块实现领域、模块参与切片等多对多关系使用类型化 DependencyEdge，不复制节点或文档。
3. Project → Product Surface → Service → Domain → Module → Vertical Slice → Task 是端到端业务路径的类型链，不强制把同一服务复制到每个前端目录下。

Project 可直接拥有产品表面、服务、领域、纵向切片和横向基线；产品表面拥有前端模块，服务拥有后端模块，领域可拥有纯领域模块，纵向切片拥有 TaskCard。所有跨树关系通过 `consumes/realizes/implements/contributes_to/decomposes_to/depends_on/shares_baseline/publishes_contract/owns_data/verifies` 等边表达。

DeliverableNode 只保存所有节点共有字段，不能代替类型详情。`typed_detail_binding_contract` 要求每个 ProductSurface、Service、Module、VerticalSlice、Task 和 HorizontalBaseline 节点恰好解析到一个同 ID、同类型的 detail 记录；反向也要求每个 detail 恰好对应一个现存节点。缺 detail 只允许一个绑定该 node ID、含原因、影响、替代方案、owner 和 ReviewerDecision 的结构化 N/A。每个 `na_id` 必须唯一，每条 N/A 必须被恰好一个适用节点消费，且该节点不能同时存在 detail；整体省略、重复、孤立、ID/类型错配、未被节点消费或与 detail 并存都拒绝。

### 22.2 领域和模块不是固定上下级

Domain 是业务语义、术语、不变量和所有权边界，不等于代码目录、微服务或前端工程。Module 是某个产品表面、服务或领域中的实现单元，必须引用一个主领域，可通过受控引用关联次领域。

- 后端模块说明所属服务、主领域、职责、不变量、应用用例、接口 owner、依赖、数据所有权、错误和测试边界。
- 前端模块说明所属产品表面、主领域、业务能力、页面/路由、组件边界、状态来源、API 契约、共享策略和测试边界。
- 共享模块使用结构化创建契约，必须已有至少两个登记消费者、稳定契约引用、owner assignment 和版本策略引用；“以后可能复用”不足以创建共享层。
- 跨模块调用必须使用受控接口；共享数据库列或隐式全局状态不能充当接口。

因此后端和前端都分模块，但分法不同：后端围绕领域、用例、服务和适配器；前端先按产品表面，再按业务能力/领域组织页面、状态和组件。

### 22.3 产品表面和服务分别登记

Web、移动 App、小程序、每个管理后台和 CLI 都是独立 ProductSurface；多个管理后台必须使用不同稳定 ID、受众、权限、页面能力、构建和验收。后端服务、API 服务、网关、worker、定时任务和集成适配器都是独立 Service，分别登记职责、领域、模块、数据 owner、接口、依赖、部署、监控、恢复和发布状态。五类产品表面、六类服务和第二个管理后台都必须有可执行登记正例；未知 subtype 必须拒绝。

每个产品表面和服务可以独立设计、计划、实现、测试和发布，同时通过 BusinessField、API、权限、设计系统和纵向切片保持共同需求一致。最终交付报告必须按这些节点分别列完成、未完成、验证、版本和发布状态。

### 22.4 任务以纵向业务切片为主

VerticalSlice 从用户或业务结果开始，贯通 Requirement、UX、UI、ProductSurface、API、Application、Domain、Database、Permission、Test 和 Release。先创建可独立验收的切片，再在同一 TaskCard 的 ActionSpec 中安排数据库、接口、前端、多端、测试、文档和发布动作。

禁止先建立“全部数据库任务”“全部 API 任务”“全部 UI 任务”三棵互不验收的树。读文件、运行命令、写测试和记录 evidence 是 Action，不单独创建 TaskCard。P0/P1 切片的适用层必须完整；N/A 需保存层、原因、替代验证、Reviewer 决定和当前 subject hash。

任务目录按 `WorkItem → VerticalSlice/TaskCard → drafts/evidence/reviews/reports` 归属，不按数据库/API/UI 建业务任务目录。产品源码仍可按真实前端表面和后端服务建立模块目录，但每个模块必须反向引用 `module_id/domain_id/slice_id`。

### 22.5 横向基线与全局文档关系

横向基线包含项目、领域、架构、数据、API、UI 设计系统、质量、安全隐私和发布运维。它们服务多个纵向切片，不被复制进每个模块目录。基线变更可以有独立 TaskCard，但必须生成 BaselineImpact，列出受影响产品表面、服务、领域、模块、切片、BusinessField、失效 Artifact 和必需任务。

正式 `docs/` 只保留登记 owner 的最小文档；全局文档通过 Catalog ID、Requirement ID、Domain/Module ID、Slice ID 和 BusinessField ID 与具体模块设计关联。讨论不能为了表达一个矩阵关系就新增 Markdown；完整拓扑和关系矩阵以机器 Catalog 为唯一事实源，Markdown 只解释阅读方式和关键取舍。

### 22.6 BusinessField 唯一规范定义

`FIELD-TRACE-BUSINESS-001` 要求每个 BusinessField 保存稳定 ID、业务名称和含义、owner、需求、规范类型、格式/单位/精度、枚举、可空、默认、来源、敏感级别、生命周期、校验、权限、各层映射、变更历史和证据。技术名称可以不同，但必须引用同一 BusinessField ID。

必需追踪层为：Requirement、Domain、Database、API/Event、UI、Validation、Permission、Log/Audit、Test。兼容校验必须从每层真实 `technical_type`、必填/可空值、owner Artifact、默认、约束、权限和 validation refs 推导规范值，再和 BusinessField 比较；`normalized_contract` 只是非权威派生摘要，不能掩盖实际字段漂移。数据库结构不能反向定义公共 API 语义，UI 标签也不能代替业务含义。

### 22.7 字段变更和 TraceBreak

字段新增、删除、改名、改类型、改枚举、改权限或改敏感级别时生成 BusinessFieldImpact。七类 change kind 分别使用封闭影响集合，ImpactList 强制绑定旧/新 contract hash、受影响映射和 Artifact、失效批准、任务、迁移/兼容、Review 和验证；删除任一必填字段都必须失败。稳定 BusinessField ID 在技术改名时不变。

缺映射、含义漂移、类型/可空/默认/枚举不一致、校验变弱、权限扩大、敏感级别丢失、日志脱敏缺失、测试缺失或未经评审的 N/A 都形成 TraceBreak。P0/P1 进入实现前，未解释或无 owner TraceBreak 必须为 0。

### 22.8 完整字段链参考

CP-03 使用 `BF-HIGH-RISK-AUTH-VALID-UNTIL-001` 作为完整参考链：

| 层 | 映射 | 必须保持的语义 |
|---|---|---|
| Requirement | 高风险/PR 授权有效期 | 每次人类明确授权，严格晚于求值时刻 |
| Domain | `HumanAuthorization.validUntil` / `OffsetDateTime` | 必填、明确时区、不能由 AI 生成 |
| Database | `human_authorization.valid_until` / 带时区时间戳 | NOT NULL，晚于授权时间，支持活动未消费授权查询 |
| API | `valid_until` / `string date-time` | 必填，拒绝无时区和可解析但非 ISO 值 |
| UI | “授权有效期”时区感知输入/只读显示 | 人类批准前可编辑，授权后只读，显示时区和过期状态 |
| Validation | `parseStrictTimezoneIso8601` | 合法日历、偏移不超过 14:00、精确解析、未来比较 |
| Permission | `HUMAN_APPROVER.write_valid_until` | 只有有效人类批准人可写，AI 只能读取候选决定 |
| Log/Audit | 授权过期求值事件 | 追加授权 ID、求值时刻、结果和 hash，不记录 secret |
| Test | high-risk authorization 边界矩阵 | 未来 ISO 允许；过期等待；非 ISO、无时区、非法日期/偏移拒绝 |

该参考链是运行时实现的设计契约，不冒充当前已经存在数据库或 UI；它证明同一字段如何在未来实现中保持一致，并直接复用 CP-02 R005 的严格时间对抗测试。

### 22.9 覆盖闭合与 CP-03

WP-07 同步核对前序覆盖，发现 WP-04 至 WP-06 的需求覆盖仍保留占位或 deferred 状态。43 条 WP-04 至 WP-07 覆盖现已逐项指向真实 metadata、Method、ToolPolicy、ResponseTemplate、Topology 或 FieldTrace 对象；能力缺口保留“已登记人工 owner”语义，不伪称专业 Skill 已实现。

CP-03 R001 独立评审发现 3 Critical、6 Important、1 Minor，结论为 `changes_requested / 30`。第 1 轮整改要求：裸布尔权限自证、跨工具 PR 授权、伪造 normalized 字段、通用 Skill/Prompt、回复假报、拓扑/影响 schema 清空和 stdout 截断都必须有真实负例。完整 `cp03@0.3.0`、受影响 `cp02`、WP-05/WP-06 阶段和输出管道验证全部通过后，才能冻结 R002 并由同一 Reviewer Russell 只读复审。作者 Green 不等于 CP-03 或 CP-02 恢复通过，当前也没有人工设计批准或正式发布资格。

R002 复审关闭了 6 项，仍以 `changes_requested / 58` 保留 `CP03-C-001`、`CP03-I-003`、`CP03-I-004`、`CP03-M-001`，CP-02 R006 当前候选影响也因同一来源根问题退回。第 2 轮整改增加外部 TrustAnchorRegistry 和来源根 attestation、真实 Artifact/Verification ReferenceRegistry、拓扑节点与 typed-detail 双向一一绑定，并把状态证据更新到当前轮次。R003 是本检查点最后一个自动复审候选；若同一 Reviewer 再次退回，必须停止交人工决定。作者 Green、R003 冻结或 CP-02 R007 影响快照都不等于 Reviewer approved、人工设计批准或正式发布。

R003 最终自动复审为 `changes_requested / 64`，关闭 `CP03-M-001`，仍开放来源登记同调用边界、引用登记/退出码结果不一致和孤立 Reviewer N/A 三项。R004 定向整改把三项全部关闭，同一 Reviewer Russell 给出 `approved / 100`，CP-02 R008 当前候选影响也通过；用户随后确认关闭 CP-03 并授权执行 WP-08 到下一人工确认门。

## 26. R010 项目进度快查完整设计

### 26.1 需求绑定、影响范围和唯一 owner

`REQ-CHANGE-WF-CTL-010-001` 不创建新工作流，唯一 owner 仍是 `WF-CTL-010`。正式 PRD v3.3.0 负责说明用户需要什么，R014 机器需求合同负责冻结详细字段、枚举、算法、布局和验收输入，本设计和机器 Catalog 负责说明系统如何满足这些要求。三者冲突时必须停止，不能由 AI 选择一个看起来合理的值。

R007 的历史评审只对旧四哈希和 PRD `v3.0.0` 有效。R014 生效后，R007 发布清单、评审结论和人工批准资格全部失效，但历史文件和 ledger 事件保持不变。R008 首次完成需求影响设计；R009 已关闭计划绑定、需求指针、SQLite 组合外键、完整验证结果等问题。R009 同一 Reviewer 复审随后用两个最小反例证明：数据流摘要绑定和接口必填字段可以被破坏而仍通过，56/69 的所谓逐条执行仍由少量分组逻辑代替。R010 只修复这两个确认成立的问题；其余 122 条工作流的语义与记录字节不得无理由变化。

### 26.2 唯一九步纵向执行链

| 步骤 | 执行主体 | 输入 | 固定输出 | 失败结果 |
|---:|---|---|---|---|
| 1 | AI 执行者 | 用户消息、当前项目、允许的会话上下文 | `IntentCandidate` | 无法形成封闭候选时返回最小歧义说明 |
| 2 | 确定性策略系统 | `IntentCandidate`、认证主体、工具注册表和默认值 | 带计划摘要、调用顺序和输出 schema 的 `ToolCallPlan/v1`，或零调用加一个最小问题 | 未知意图、组合、范围、工具、顺序或次数一律零调用 |
| 3 | 投影器 | `ToolCallPlan`、合格全局日志、旧 checkpoint | 高水位 `H` 和带完整验证摘要的 `ProjectionTransaction/v1` | 日志缺口、哈希断链、来源历史改写或事务失败时阻断 |
| 4 | 注册工具派发器与 SQLite 查询层 | `ToolCallPlan`、已提交投影事务和 `H` | `ProjectProgressSnapshot/v2`，以及每次真实调用一份 `ToolExecutionReceipt/v1` | 未登记工具、回执缺失、只读事务失败或快照不完整时不得返回旧业务值 |
| 5 | 权限过滤器 | 完整快照、全部工具回执、认证 principal 和字段权限 | 绑定来源快照、回执摘要和权限摘要的 `AuthorizedProgressSnapshot/v1` | 权限未知时默认隐藏，禁止把越权明文交给 AI 或渲染器 |
| 6 | 固定代码渲染器 | 同一获授权快照 | 精确事实区块字节、事实摘要、会话 HTML、独立 HTML、按需 Excel 与 `RenderManifest/v2` | 不得重新读取事实；字段或布局不合法时失败关闭 |
| 7 | 输出核对器 | `RenderManifest/v2` 和获授权快照摘要 | 绑定事实摘要、权限摘要及全部格式摘要的 `ReconciliationResult/v2` | 任一区、行、字段或来源摘要不一致时所有业务输出均不交付 |
| 8 | AI 执行者 | 同一获授权快照摘要、渲染清单和已通过核对结果 | 绑定事实摘要、权限摘要和核对摘要的 `AIInspectionResult/v1` | 不得重算完成率、改变事实、补写未知值、重新读事实或扩大权限 |
| 9 | 会话适配器 | 原始事实区块字节、渲染摘要、核对摘要和 AI 检查摘要 | `SessionResponseAssembly/v1` | 任一摘要、事实字节或区块顺序错误时返回专用错误，不输出被改写的看板 |

这九步就是 Workflow 图的唯一主链。图上的前进边保持线性，但每个 ActionSpec 还必须显式消费声明的全部上游类型化结果：第 4 步消费第 2、3 步，第 8 步消费第 5、6、7 步，第 9 步消费第 6、7、8 步；每一步也必须消费紧邻前一步。十三条数据依赖必须按 `from_step`、`to_step`、`output_type`、`binding` 四字段逐条精确相等；每个 ActionSpec 的上游输入必须按 `kind`、`step`、`action_spec_id`、`result_schema_ref`、`output_type`、`integrity_field` 六字段精确相等，禁止只核对起止步骤。失败分支优先于前进边。步骤 3 可以更新可重建投影和 checkpoint，但用户查询、渲染、导出和 AI 检查都不得改变项目业务状态。

### 26.3 事实注册、全局日志和 SQLite 投影

事实来源封闭为六类：已确认项目资料、正式文档地图、WorkItem ledger、项目管理事件、任务验证证据和部署事件。每类来源必须在版本化 `SourceRegistry` 中登记 schema、owner、资格谓词和撤销规则；未知来源直接拒绝。合格事件统一写入 `FactEventEnvelope`，至少包含全局序号、来源序号、项目、时间、主体、确认状态、payload hash、前序全局 hash 和事件 hash。撤销只能追加事件，不能删除或覆盖历史。

SQLite 只是日志的可重建查询投影，不是事实源。物理设计固定如下：

| 表 | 主键和关键约束 | 用途与索引 |
|---|---|---|
| `projection_meta` | `schema_version` 主键；只允许一个 active 版本 | 数据库迁移和兼容门 |
| `source_registry` | `source_id + registry_version` 复合主键；source ID、schema 和 owner 非空 | 按活动版本和来源类型查询 |
| `fact_event` | `global_sequence` 主键；`event_uid` 唯一；`source_id + registry_version + source_sequence` 唯一；`source_id + registry_version` 组合外键完整引用 `source_registry` 复合主键 | 按项目、来源版本、effective time 和确认状态索引；禁止只引用非唯一 `source_id` |
| `projection_checkpoint` | `project_id` 主键；`high_water_sequence`、根 hash、日志前缀 hash、提交时间非空 | 单项目单 checkpoint；用于增量消费和历史改写检查 |
| `snapshot` | `snapshot_id` 主键；`project_id + high_water_sequence + authorization_scope_hash` 唯一；保存 `validation_status`、完整六字段 `validation_result_json` 和规范化内容 SHA-256 | 按项目和生成时间倒序查询；JSON 状态必须与独立状态列一致 |
| `snapshot_section` | `snapshot_id + section_id` 复合主键，外键到 snapshot | 固定十个数据区，缺一区即不完整 |
| `snapshot_row` | `snapshot_id + section_id + row_id` 复合主键 | 区内稳定排序和逐行摘要 |
| `snapshot_field` | `snapshot_id + section_id + row_id + field_id` 复合主键 | 137 个输出字段、类型、空值、权限分类和来源摘要 |
| `source_summary` | `snapshot_id + source_id` 复合主键 | 快照来源计数、范围和根 hash 对账 |

投影事务先在写事务中读取并校验旧 checkpoint，再捕获不可变高水位 `H`，按全局序号增量消费到 `H`，构造所有表，生成包含 `validation_status`、`affected_paths`、`render_disposition`、`rule_results`、`validated_at`、`validator_version` 的完整验证结果及其 SHA-256，最后原子提交 snapshot 与新 checkpoint。并发追加只属于下一轮；崩溃只能留下完整旧快照或完整新快照。数据库删除或损坏时可从合格日志重建；来源截断、历史改写、序号缺口或 hash 断链一律阻断，不能静默回退。R010 validator 必须实际调用内存 SQLite 完成建表、合法组合外键写入、事务提交、事务回滚、九表重建和非法组合外键拒绝，不能只检查 JSON 表定义。

### 26.4 快照、状态、派生规则和准确性

`ProjectProgressSnapshot/v2` 由身份、截止高水位、项目时区、完整六字段验证结果、十个数据区、行摘要、字段摘要、来源摘要和工具执行回执摘要构成。只保存 `validation_status` 不能证明受影响路径、渲染处置、逐规则结果、验证时间和校验器版本，属于不合格快照。任务原始状态封闭为 planned、ready、in_progress、blocked、pending_review、pending_human_approval、completed、cancelled；交付状态封闭为 not_applicable、not_released、release_pending、deployed、rolled_back。状态转换只接受机器 Catalog 明列的 26 条边及其 guard，未列边或缺 guard 直接拒绝。

看板分桶按 completed、pending_human_approval、pending_review、blocked、stalled、active、ready、planned 的固定优先级选且只能选一个。完成率分母、阻塞三态、依赖三态和新鲜活动三态都由机器规则计算；216 个状态组合必须形成无遗漏、无重叠的总分区。逾期、新鲜活动、里程碑偏差、近期完成、审批等待、未来七天、健康度和完成率只使用 R014 中登记的算法、时区、工作日历和毫秒精度，不能由渲染器或 AI 重算。

验证状态按 failed、conflict、stale、incomplete、verified 的优先级归一。conflict、stale 和 failed 默认只输出专用错误、受影响路径和恢复建议，不泄露旧业务值；incomplete 只输出已明确允许的字段并标记缺口；只有 verified 才能进入正常渲染。

### 26.5 AI 意图、确定性计划和九个只读工具

AI 只生成 `IntentCandidate`，字段限定为候选意图、项目、范围、时间、格式、深度和歧义，不得写入认证 principal、权限结论或最终工具计划。确定性系统把候选与字面参数、当前项目、九个单意图计划、六个精确组合计划及 guard 注册表匹配，输出唯一 `ToolCallPlan`。

九个工具分别是项目进度报告、任务诊断、风险状态、变更状态、审批队列、部署状态、进度一致性审计、固定报表导出和字段来源追踪。每项都在 `tool_runtime_registry` 中登记输入 schema、输出 schema、派发 ActionSpec、认证门、只读边界、稳定错误码和 `ToolExecutionReceipt/v1`。第 4 步必须严格按 `ToolCallPlan/v1` 调用，每个已派发调用恰好产生一份回执，回执绑定计划、调用序号、工具、输入输出摘要、快照、高水位、权限摘要、起止时间和结果。普通总览一次主调用；只有主结果出现登记异常时才允许一次补充审计，最多两次。未知工具、未知组合、错误范围、错误 guard、错误顺序、超次数、缺回执或回执 schema 不符都失败关闭。

“查询项目进度”且当前项目唯一时直接进入 overall_progress，不追问。只有项目不唯一、任务或阶段范围缺失、格式参数冲突等会改变唯一计划的歧义，才返回一个最小问题；会话不得为了补充无关偏好而停止。

### 26.6 同快照渲染、HTML、Excel 和权限

文本、会话 HTML、独立 HTML 和 Excel 只能消费同一个 `AuthorizedProgressSnapshot/v1`，不得各自查询 ledger、文档或数据库。获授权快照绑定来源快照摘要、高水位、全部工具回执摘要、权限摘要和自身摘要。`RenderManifest/v2` 除逐格式摘要外，还保存最终事实区块的精确字节和 `fact_dashboard_digest`；`ReconciliationResult/v2` 同时绑定获授权快照、权限、渲染清单和事实区块摘要，再逐区、逐行、逐字段和逐来源比较，任何差异都关闭全部业务输出。Catalog 中 11 个项目进度接口的接口名、schema ID 和必填字段集合均由封闭接口注册表逐项精确校验，删除 `fact_dashboard_block_bytes` 或任一其他必填字段必须失败。

HTML 固定为第一页总览加十个管理页。第一页首屏必须直接显示项目身份、阶段、截止时间、验证状态、有效任务总数、完成数、完成率、真正进行中、待审批、阻塞或逾期、已上线和下一里程碑，并给出互斥状态分布及六类一行摘要。后续十页与 Excel 十个业务表一一对应。会话宿主和无网络独立页面必须在 1440、1024、768、390、320 五类视口下无横向滚动、重叠、裁切或空白画布。

Excel 固定为 `00目录` 加十个业务表，137 个字段由 R014 机器合同中的稳定 field ID、快照路径、类型、空值、权限分类、目标 sheet/slot 和 `LayoutExpression/v1` 唯一确定。动态行、RACI 动态列、会议和状态报告重复块、变更历史子表都由 AST 解释，禁止执行字符串公式或接受调用方提供的成员数量。目标单元格必须唯一、不重叠、不越界；工作簿中的隐藏单元格、元数据、公式和嵌入内容也不得出现越权明文。

权限过滤在渲染前执行。认证 principal 只能来自受信会话，不接受 AI 或请求参数自称。internal、联系人、财务、风险、变更和审批六类字段分别按登记权限保留、隐藏或脱敏；授权摘要绑定 principal、角色、权限集合、策略版本和快照 hash。AI 只接收过滤后的数据，不能看到随后被页面隐藏的原值。

### 26.7 会话回复装配契约

`SessionResponseAssembly/v1` 必须包含十个字段：`snapshot_id`、`authorized_snapshot_sha256`、`authorization_digest`、`fact_dashboard_block`、`fact_dashboard_digest`、`reconciliation_sha256`、`ai_inspection_block`、`ai_inspection_sha256`、`block_order`、`assembly_validation`。`block_order` 必须精确等于 `["fact_dashboard", "ai_inspection"]`。会话适配器必须同时核对获授权快照摘要、权限摘要、事实区块 SHA-256、核对结果摘要和 AI 检查摘要，然后逐字节原样放置事实区块；禁止清洗、总结、改字、重排或补写。

第二段 AI 专业检查只能引用第一段已经核对的证据，说明风险、异常、数据缺口和建议检查项，必须明确其不是项目事实。事实区块 digest 不一致返回 `FACT_DASHBOARD_DIGEST_MISMATCH`，区块顺序或数量错误返回 `SESSION_BLOCK_ORDER_INVALID`；两类错误都不得输出一个看似正常但已被改写的看板。

### 26.8 验收、性能和变异防护

R014 的 56 个验收夹具逐个形成机器 `test_case`，但 Catalog 不复制整个 fixture 或 `expected` 文本。R010 保存一个封闭的 56 项 evaluator 注册表，每项都有唯一 evaluator 定义、fixture-specific 的需求合同/设计/运行时输入指针和独立断言；当前共 183 条语义断言。执行器先解析并摘要每项输入，只根据 evaluator 定义计算 `actual_result`，之后才读取外部 `expected_decision` 形成 `oracle_match`。来源 `expected` 只用于核对 oracle 摘要，绝不能成为 actual 的计算输入。56 份结果还必须分别保存输入摘要、定义摘要、断言结果、来源绑定状态和结果摘要；少一项、交换 evaluator、复制 expected 或复用同一 evaluator 定义都失败。原 369 个通用 Workflow 黑盒场景继续验证全部 123 条工作流；两组测试用途不同，不能互相替代。

69 个 mutation ID 以已冻结 R014 validator 中的 69 条实际语义探针为上游源：R010 对每条保存源行号、完整检测表达式、表达式摘要、源 validator 摘要和已发布验证/评审摘要，形成封闭的逐 ID 注册表。每个 ID 另有唯一 operator 定义和唯一目标指针，目标是该 ID 自己的设计绑定摘要；执行时必须记录目标前后摘要并证明 `target_changed=true`，再对完整设计副本运行同一个校验器并命中声明的错误 ID。69 个 operator 定义摘要、目标指针和上游表达式摘要都必须分别保持 69 个唯一值。R010 不读取已归档的人类候选，也不谎称重跑归档输入：上游 69 条领域语义执行资格由 R014 已发布验证和独立评审证明，R010 的 69 次执行证明这些语义探针到当前设计绑定没有缺项、错配或漂移。少量通用操作组、只核对数量、目标未改变或任一同步篡改都不能通过。

性能基准完全复用 R014 冻结的数据规模、种子、环境、冷/热、增量、并发、预热和 100 次测量协议。热快照、冷进程、0/1/100/1000 事件增量、会话 HTML、独立 HTML、十一表 Excel、首屏和完整看板的 p95 必须分别满足登记上限；未保存原始时长、环境清单、数据集 hash、退出码和语义 hash 的测量没有证据资格。

### 26.9 文档信息架构和候选发布绑定

R010 不增加正式页面。信息架构当前唯一执行合同为 36 个目标文件、7 个目录、68 个现存文件处置和 37 个发布内容目标；R010 的 158 目标只属失效历史前像。当前机器候选和生成器分别使用 `docs-information-architecture.R010.json` 与 `TASK-DESIGN-001-docs-information-architecture-R010.mjs`，支持文件哈希变化必须进入新的发布清单。

人工批准的四个顶层 hash 仍按“中文设计、机器 Catalog、R010 validator、R010 发布清单”固定顺序绑定。发布清单还必须传递绑定 R010 信息架构候选和生成器的路径及 SHA-256，因此支持文件变化会改变发布清单 hash，不能绕过人工批准。候选冻结、作者验证和独立 AI 评审都不增加正式文档版本。

### 26.10 R009 同一 Reviewer 复审问题的关闭条件

| 评审问题 | R010 关闭条件 |
|---|---|
| `R009-IMP-002` / `I-003` 类型化数据流和事实字节闭包可被破坏 | 13 条边四字段精确相等；9 个 ActionSpec 上游输入六字段精确相等；11 个接口的 schema 和全部必填字段精确相等；边绑定、ActionSpec 摘要绑定和接口字段三个负例均被拒绝 |
| `R009-IMP-001` / `I-006` 56/69 逐条执行是假通过 | 56 个唯一 evaluator、fixture-specific 输入、183 条独立断言及 actual-before-oracle 结果全部通过；69 个唯一上游表达式、operator 和目标逐条证明目标改变并被拒绝 |

### 26.11 当前停止点

R010 候选和作者验证只证明整改产物已经形成。依据用户已给出的同任务、同范围、无外部副作用自动循环授权，下一步由同一 Reviewer Arendt 只读复审；复审不通过时只在上述两个问题范围内继续整改，复审通过后必须停在“人工批准 R010 四个精确 hash”门。当前没有正式落档、产品实现、真实业务数据库创建、HTML 或 Excel 产品生成、提交、Push、PR、Merge 或部署授权，其中 PR 必须由人类再次明确确认。

## 34. R019：项目执行位置与停止可见性统一设计

### 34.1 单一快照事实链（REQ-VIS-002、REQ-VIS-004、NFR-VIS-002）

R019 新增且只允许一条位置事实链：

```text
EventLog(H) -> ProjectProgressReducer/v2 -> validated/authorized ProjectProgressSnapshot/v2
            -> PositionViewPort -> PositionViewAdapter/v1 -> ProjectExecutionPosition/v1
            -> ResponseAssemblyPort -> REQ-ASYNC-016 v4.0.0 renderer
```

`application` 是端口调用方和合同 owner；`runtime` 只提供纯 reducer、canonical hash 和资格求值；`settings` 实现读取/渲染适配器并只在 `src/settings/composition/` 装配。依赖方向仍是 `access -> application -> domain -> runtime -> settings`。`access` 不得越过 application 读取 projection store，`settings` 不得重新定义上层 port，仓内不得重建 DI resolver、loader、registry、factory 或 manifest 内核。

三个入口——会话首轮恢复、用户主动查询项目状态、任务节点完成后的主动回复——都必须先捕获同一固定高水位 `H`。本轮计算期间出现的 H+1 只进入下一快照，不能改变本轮 N/M、当前节点、Gate 或回复。若某字段来自 P<H、P>H 或未授权 projection，整个位置绑定失败关闭。

`ProjectExecutionPosition/v1` 必须逐字节绑定 validated/authorized `ProjectProgressSnapshot/v2` 的九个字段：`project_id`、`snapshot_id`、`snapshot_sha256`、`as_of_H`、`registry_sha256`、`event_schema_sha256`、`reducer_sha256`、`snapshot_schema_sha256`、`authorization_digest`。任一字段 missing 或 drift 均返回专用失败码 `project_progress_binding_conflict`，不能折叠为 lifecycle 失败。失败路径上 `PositionViewAdapter/v1` 的 event-log read / event reduce / Gate advance 调用计数必须严格为 `0/0/0`。因此 adapter 只能投影已验证快照，不能偷偷成为第二 reducer，也没有推进 Gate 的能力。

快照通过 `SnapshotQualification/v2` 校验 schema/hash、registry generation、reducer generation、授权摘要和 fixed H。校验顺序为 schema → 九字段完整性 → hash → authorization → H → adapter；任何一步失败都不继续。`NFR-VIS-002` 的一致性因此由同一快照和禁止第二 reducer 的能力边界保证，而不是靠文字约定。

### 34.2 生命周期 N/M 绑定（REQ-VIS-001）

整体路线来自恰好一个 active `LifecyclePlanBinding/v1`，AI 不能从当前目录或局部任务计划自行挑选分母。绑定必填十字段为：`artifact_id`、`artifact_version`、`artifact_sha256`、`binding_status`、`effective_scope`、`authorization_digest`、`stage_map_id`、`stage_map_version`、`stage_map_sha256`、`as_of_H`。

`LifecycleBindingPort` 在 H 上读取只读注册表；`domain` 的 binding evaluator 要求 active cardinality 恰好为 1。零个、多个、inactive、hash drift、stage map 冲突和权限拒绝分别返回：`lifecycle_binding_missing`、`multiple_active_lifecycle_bindings`、`lifecycle_binding_inactive`、`lifecycle_hash_mismatch`、`stage_map_conflict`、`lifecycle_permission_denied`。失败时整体 N/M 不得从当前 WorkItem 或最后一次回复猜测，而是进入 `blocked/fact_conflict`。

N/M 的分母是 active binding 的全局 stage map；支线、回退、review loop 和局部 WorkItem plan 只显示为当前 stage 内的节点或分支，不能增减 M。阶段完成仅由 stage completion policy 与正式事件决定；“文件已写”“作者自报完成”或“子任务已返回”都不能直接推进 N。这样当前的整体坐标始终类似“3/8 设计重基线”，不会被“T02 2/6”替代。

### 34.3 四维状态与七种互斥处置（REQ-VIS-003）

系统分开保存 `workflow_run_state`、`completion_state`、`reply_state` 和派生 `execution_disposition`。前面三维是输入事实，`execution_disposition` 是纯函数结果，不能反向覆盖输入。处置规则使用七个 mutually-exclusive selector；每个 selector 对其他 selector 都有 forbids：

| disposition | required selector | 必须禁止的其他 selector | 责任含义 |
|---|---|---|---|
| `running` | `run_active=true` | 其余六个为 false | 当前执行器正在运行 |
| `auto_continuing` | `auto_authorized=true` | 其余六个为 false | 当前节点完成后授权范围内自动进入下一节点 |
| `waiting_ai_execution` | `ai_ready=true` | 其余六个为 false | AI 已具备执行条件但尚未取得运行槽 |
| `waiting_independent_review` | `review_dispatched=true` | 其余六个为 false | 已有真实 dispatch/submission/task ID，责任人为独立 Reviewer |
| `waiting_human` | `human_gate_pending=true` | 其余六个为 false | 恰好一个人工计划 Gate 真正需要用户动作 |
| `blocked` | `terminal_or_fact_conflict=true` | 其余六个为 false | 缺工具、事实冲突或不可自动恢复失败 |
| `completed` | `task_complete=true` | 其余六个为 false | 当前任务或当前 stage 已满足其完成定义 |

零条或多条命中都返回 `blocked/fact_conflict`，不能用优先级掩盖事实冲突。`waiting_independent_review` 只有在 dispatch/outbox 持久化并回读成功后成立；“准备派发”仍是 `auto_continuing` 或 `waiting_ai_execution`。`waiting_human` 也只能来自未满足的人工 Gate，不得用它表达 AI 正在做事、等待测试或一般不确定性。

### 34.4 固定 H、会话恢复和节点绑定（REQ-VIS-004）

每次 projection request 生成 `ProjectionReadContext/v1`，冻结 `project_id + as_of_H + authorization_digest + request_id`。会话恢复、状态查询和节点完成回复把该 context 传给 snapshot、lifecycle、task、review 和 authorization readers；reader 不能自行刷新 H。若任一依赖只能提供 H+1，当前请求返回一致性阻断并建议下一轮重试，不把两代事实拼在同一回复里。

节点绑定包含全局 stage、当前 WorkItem、TaskCard、task node、gate generation 和 responsible actor。局部任务状态只能补充“当前任务/当前节点”，不能覆盖“项目总路线/当前坐标”。恢复时 Memory 只提供定位线索，正式坐标必须由 event ledger 与 snapshot 重算；Memory 中的旧 N/M、旧 stop reason 或旧 next action 一律不具备事实资格。

### 34.5 Evidence observation、执行身份和正式 CAS（REQ-VIS-005）

`EvidenceObservationPort` 的顺序固定为 canonical payload → authorization/Gate/generation 校验 → append-only observation → fsync/readback → 五字段 CAS。未经登记的文件、旧 generation、错误 actor、错误 artifact root、错误 test plan 或晚到 attempt 只保留审计，不推进 Gate。

执行前 `EvidenceExecutionIdentity/v1` 只含 15 个可事先知道的字段，顺序固定为：`gate_id`、`artifact_or_candidate_root_sha256`、`impact_policy_version`、`test_selection_plan_sha256`、`required_test_set_sha256`、`test_source_sha256`、`fixture_sha256`、`config_sha256`、`runner_name`、`runner_version`、`runner_sha256`、`dependency_lock_sha256`、`normalized_command`、`environment_attestation_sha256`、`external_dependency_fingerprint`。按该顺序编码 compact canonical JSON，并以 domain separator `shanforge:EvidenceExecutionIdentity/v1\n` 计算 `evidence_execution_identity_sha256`。request 只冻结这 15 项及其 hash，禁止预测测试 outcome。

Worker 结束后才追加五个真实结果字段：`passed_count`、`failed_count`、`skipped_count`、`not_run_count`、`evidence_time`，形成 20 字段 `EvidenceReuseKey/v1`。只有 execution status 为 passed、全部 required tests 实际运行且 failed/skipped/not_run 都为 0，20 字段逐一可复算时才能复用。`artifact_or_candidate_root_sha256` 必须等于 `CandidateArtifactSetRoot/R019`；`test_selection_plan_sha256` 必须等于 request 的 `test_plan_hash`。

正式 Gate CAS 仍是 `parent_task_id + gate_id + artifact_hash + test_plan_hash + gate_generation` 五字段。`artifact_hash` 必须字节等于当前 candidate root。CAS 只从当前合法前态推进一次；wrong parent/gate/hash/plan/generation、retry superseded、迟到 result、未登记 observation 全部失败关闭。

### 34.6 权限视图与侧信道控制（REQ-VIS-006、NFR-VIS-003）

`AuthorizationViewPort` 不改变真实全局分母，但会把无权查看的节点内容替换为固定 label。默认拒绝字段为 `task_title`、`task_path`、`risk_text`、`approval_text`、`adjacent_stage_name`。受限用户只能看到固定长度类别、当前位置是否可执行及允许动作；不能从字符串长度、hash、子项计数、排序、错误差异或响应时延推断秘密文本。

权限过滤在 renderer 前完成，renderer 只消费 `AuthorizedPositionView/v1`。禁止先渲染秘密文本再遮罩，也禁止用无权字段参与摘要 hash、分母、branch count 或“是否影响下一项工作”的文案。权限不足返回稳定 `lifecycle_permission_denied` 或 position authorization failure，不能回显目标路径和隐藏 stage 名称。

### 34.7 唯一十五行响应合同（REQ-VIS-007、REQ-ASYNC-016、NFR-VIS-001）

`ResponseAssemblyPort` 的唯一 producer/owner 是 `REQ-ASYNC-016` v4.0.0。renderer 必须按下列精确顺序输出恰好十五个 label，每个 label 只出现一次：

1. `项目总路线`
2. `当前坐标`
3. `当前任务`
4. `当前节点`
5. `本轮做了什么`
6. `完成了什么`
7. `验证情况`
8. `没有运行什么`
9. `后台任务`
10. `当前状态`
11. `为什么停下`
12. `是否影响下一项工作`
13. `下一责任人`
14. `需要你做什么`
15. `下一步`

行值来自同一 H 的 position/lifecycle/task/review/authorization view。未停止时“为什么停下”必须明确为“未停止，授权范围内继续”；不需要用户动作时“需要你做什么”必须明确为“无需操作”。后台任务只有真实 durable task ID 才能写“已派发”。这样用户不必从零散的工具日志推断状态，也不会把每个 AI 内部步骤误认为人工确认门。

v3.x 九行 consumer 属于 MAJOR 迁移：当前会话 renderer、项目状态查询、Memory 恢复回复、Review/人工 Gate 确认包、测试夹具和文档 owner 都必须登记 parser 从 `v3.x-nine-line` 到 `v4.0.0-fifteen-line` 的迁移、负例、rollback condition 和 generation。任一 strict nine-line parser 仍在活动路径时阻断 release_ready；系统不提供双 renderer 或兼容别名。

### 34.8 人工 Gate 与旧资格拒绝（REQ-VIS-008）

人工 Gate 仅有六类：`business_decision`、`risk_acceptance`、`candidate_approval`、`formal_action_authorization`、`credential_or_permission_grant`、`irreversible_action_confirmation`。普通编制、作者验证、已授权范围内复审整改、只读检查和可逆本地步骤不是人工 Gate。每个 `waiting_human` 必须给出 gate type、精确对象/hash、未满足原因、责任人和批准后下一动作。

R019 generation 中以下十类资格固定为 false：`P017_plan_author_validation`、`P017_independent_review`、`P017_human_plan_approval`、`P017_execution_authorization`、`R017_design_author_validation`、`R017_independent_review`、`R017_human_candidate_approval`、`R017_formalization_eligibility`、`R017_release_eligibility`、`R017_commit_or_remote_authorization`。它们即使拥有完整旧 evidence 也不能迁移。资格求值器必须比较正式 requirements hash、P022 plan hash、candidate root 和 `TASK-DESIGN-001-R019-G001`；任一不等即拒绝。

当前授权允许 R019 候选编制、作者验证、独立只读复审及同范围必要整改循环；唯一人工停止点是 R019 精确 candidate root 批准。正式发布、Git index/commit 和远端操作仍无授权。

### 34.9 Candidate root、写集和控制平面证明（REQ-VIS-009）

`CandidateArtifactSetRoot/R019` 的成员和顺序固定为：design、catalog_source、information_architecture、builder、validator、verification_runner。每个成员编码为只含 `artifact_id`、`path`、`sha256`、`bytes` 的 JSON object，键顺序即此顺序；路径是仓根相对 POSIX，UTF-8、LF、无 BOM、无额外空白。六对象按上述顺序组成 compact JSON array。domain separator 精确为 `shanforge:CandidateArtifactSetRoot/R019:v1\n`；root 为 `SHA-256(separator bytes || canonical array bytes)`。

manifest 排除在六成员之外，避免自引用。任一 schema 如保留 `candidate_sha256`，它必须与 `candidate_set_root` 字节相等，否则返回 `candidate_identity_conflict`。单文件 hash、manifest hash 或旧五成员 root 都不得称为 candidate hash。

27 条 canonical registry 由 P022 scope anchor 冻结。`HygienePhaseManifest/v2` 只能由 registry、Owner/Gate 和 `async_branch` 派生有序且不相交的 present/absent partition：transfer pre-T06 24/3、final 27/0；no_transfer pre-T06 21/6、final 24/3。两数组并集必须严格等于 27 条。实际 R019 选择 no_transfer，因此 regression request/outbox/result 三路径在 final 仍必须 absent。

每个文件写完后，控制平面向 work ledger 追加 `ArtifactWriteAttestation/v1`。schema 精确包含 `schema_version`、`event_id`、`actor_id`、`actor_type`、`execution_or_review_task_id`、`dispatch_receipt_id`、`authorization_event_id`、`authorized_write_set_sha256`、`target_path`、`expected_owner`、`gate_id`、`gate_generation`、`artifact_sha256`、`artifact_bytes`、`written_at`、`tool_receipt_sha256`、`ledger_prefix_sha256`。候选文件内自报的 actor/reviewer 不具备证明力；validator 必须从 authorization event 与 review ledger 的真实 dispatch 回读 actor/task/dispatch/write-set/owner/Gate，按 attestation 所在字节位置重算 ledger prefix，核对 tool receipt 与当前 hash/bytes，并拒绝 wrong actor、wrong task、fake reviewer、缺失或过期 dispatch、伪 prefix、未 readback 和过期 attestation。

`FinalHygieneReceipt/v2` 位于 27 路径集合外，只能在 final hygiene 后向 work ledger 追加一次。它精确包含 `schema_version`、`receipt_id`、`async_branch`、`canonical_registry_sha256`、`phase_manifest_sha256`、`validator_sha256`、`normalized_command`、顶层 `execution_id`、`gate_generation`、`present_entries[{path,sha256,bytes,attestation_event_id}]`、`expected_present_set_root`、`absent_proofs[{path,checked_at,absence_code,validator_execution_id}]`、`expected_absent_proof_root`、计数、`failed=0` 和 `finished_at`。phase manifest、validator、command、execution、generation 必须与每个 present/absence proof 同一执行绑定；旧 proof、跨 branch/generation replay 或 receipt 后 expected-present 漂移/expected-absent 出现都会立即撤销 Gate 资格。

其中集合和计数字段名固定为 `present_entries`、`absent_proofs`、`present_count`、`absent_count`、`passed_count`、`failed`；每个 absence proof 的四个字段名固定为 `path`、`checked_at`、`absence_code`、`validator_execution_id`。不得用 `present_artifacts`、`command`、`observed_at` 或不带 execution binding 的 `{path,exists}` 兼容别名。

### 34.10 Session-level V4 验证与性能（REQ-ASYNC-015、NFR-VIS-004）

`QuickVerificationSession/v1` 使用 monotonic clock，单一 session deadline 为 60,000ms，dispatch reserve 为 5,000ms，inline cutoff 为 start+55,000ms，策略版本为 `R019-quick-session-v1`。每个 L1–L4 required test 启动前用 remaining budget 做 admission，不能按测试或 retry 重置。预计时间超过 remaining window 时直接 transfer；已运行 attempt 到 cutoff 必须取消并在 reserve 内原子提交 durable request/outbox/parent Gate 与 readback。

`no_transfer` 要求全部 required tests 在 cutoff 前真实完成，四计数中 failed/skipped/not_run 都为 0，Worker 完全不运行，三份 async 文件不存在。`transfer` 至少有一项因预计超预算或实际到 cutoff 转移，才允许 `RegressionTaskRequest/v3`、outbox、`RegressionTaskResult/v3` 存在；request 固定 `fork_context=false`，只绑定执行前 identity，不预测 outcome。

预算边界必须覆盖 54s/55s/56s、59s/60s/61s、59s+59s、30s+31s，以及取消、事务、readback、回复时间和 clock drift。54 秒可以在完全空白窗口内启动，55 秒及以上必须 transfer；组合测试始终按累计 remaining budget 判断。事务失败也必须在绝对 deadline 前回复 `blocked/durable_dispatch_not_committed`，不能延长时钟。

性能基线使用 10,000 tasks、100,000 events；投影读取 hard cap 为 1,000 rows、8MiB、3,000ms。测试需证明新增九字段 binding、lifecycle lookup、permission filtering 和十五行 renderer 没有额外全库扫描，且 adapter 禁止直接读 event log。

### 34.11 R019 接口与 owner 总表

| 合同 | 定义方 | 实现方 | 关键限制 |
|---|---|---|---|
| `ProjectProgressSnapshot/v2` / `ProjectProgressPort` | `application` | `settings` projection adapter | validated/authorized、固定 H、九字段完整 |
| `PositionViewPort` | `application` | `settings` 的 `PositionViewAdapter/v1` | 只能消费 snapshot；禁止 read/reduce/Gate advance |
| `LifecycleBindingPort` | `application` | `settings` readonly registry adapter | H 上恰好一个 active binding |
| `DispositionEvaluator` | `domain` | `runtime` pure evaluator | 七条互斥；零/多命中失败关闭 |
| `ResponseAssemblyPort` | `application` | `settings` renderer | `REQ-ASYNC-016` 唯一 owner，严格十五行 |
| `EvidenceObservationPort` | `application` | `settings` append-only store | 先验证后 observation，再正式五字段 CAS |
| `QualificationEvaluator` | `domain` | `runtime` pure evaluator | 比较 requirements/plan/root/generation，旧资格拒绝 |
| `AuthorizationViewPort` | `application` | `settings` authorization adapter | 保留真实分母、固定受限标签、禁止侧信道 |
| `CandidateArtifactSetRoot/R019` | `application` 调用侧 | `runtime` canonical hash | 六成员固定顺序；manifest 排除 |
| `EvidenceExecutionIdentity/v1` | `application` 调用侧 | `runtime` canonical hash | 15 个执行前字段，不含预测 outcome |
| `EvidenceReuseKey/v1` | `application` 调用侧 | `runtime` equality evaluator | 15+5 全字段相等且全测试真实通过 |
| `QuickVerificationSession/v1` | `application` 调用侧 | `runtime` budget evaluator | 单 session 60s、5s reserve、monotonic |
| `RegressionTaskRequest/v3` / `RegressionTaskResult/v3` | `application` 调用侧 | `settings` durable queue/worker | 仅 transfer；两维状态与正式 CAS |
| `ArtifactWriteAttestation/v1` | control plane | `settings` work ledger | 真实 writer receipt，artifact 自报无效 |
| `HygienePhaseManifest/v2` / `FinalHygieneReceipt/v2` | `application` 调用侧 | `runtime` + `settings` ledger | branch-aware，receipt 在 registry 外 |

### 34.12 需求追踪与攻击矩阵

| 需求 | 设计 owner | 必需攻击 |
|---|---|---|
| `REQ-VIS-001` | §34.2 lifecycle binding | 零/多个 active、inactive、hash/stage map/权限漂移、支线改变分母 |
| `REQ-VIS-002` | §34.1 snapshot/position | 九字段逐一 missing/drift、第二 reducer、adapter `0/0/0` |
| `REQ-VIS-003` | §34.3 disposition | selector 全组合、零命中、多命中、伪 waiting 状态 |
| `REQ-VIS-004` | §34.4 fixed H | H+1、P<H、P>H、三个入口不同 H |
| `REQ-VIS-005` | §34.5 evidence/CAS | 未登记 observation、旧 generation、actor/hash/plan/CAS/late attempt |
| `REQ-VIS-006` | §34.6 authorization | secret text、长度/hash/计数/排序/错误/时延侧信道 |
| `REQ-VIS-007` | §34.7 renderer | 行数、行序、重复 label、缺字段、strict nine-line parser |
| `REQ-VIS-008` | §34.8 qualification | 十类旧 evidence 逐项注入、旧 root/plan/generation |
| `REQ-VIS-009` | §34.9 write/provenance | 27 路径、owner、branch partition、假 writer、receipt 后漂移 |
| `NFR-VIS-001` | §34.7 | 十五行可理解性与无需用户动作明确性 |
| `NFR-VIS-002` | §34.1 | 快照一致性与禁止第二 reducer |
| `NFR-VIS-003` | §34.5–§34.9 | 权限、证据、资格、writer 和 Gate 安全负例 |
| `NFR-VIS-004` | §34.10 | 10k/100k、1000 rows/8MiB/3000ms、无全库扫描 |

受影响的既有治理需求 `REQ-AI-WORKFLOW-008`、`REQ-AI-WORKFLOW-042`、`REQ-AI-WORKFLOW-045`、`REQ-AI-WORKFLOW-046`、`REQ-AI-WORKFLOW-047`、`REQ-AI-WORKFLOW-054`、`REQ-ASYNC-015`、`REQ-ASYNC-016` 均由上述合同吸收，不新增同义 Workflow。原 123 Workflow 身份保持不变；主要 owner 仍是 `WF-CTL-001` 和 `WF-CTL-010`。

### 34.13 当前候选 Gate 与停止规则

R019 作者只能把 T01–T06 产物标记为 `ready_for_review`。完整 profile 要求 assertions 至少 120，required tests 的 failed/skipped/not_run 均为 0，no_transfer 分支的 async 三路径保持 absent，pre-T06 hygiene 为 21/6。独立 Reviewer 必须未参与编制，只写唯一 Decision；Critical/Important 都为 0 才能进入人工候选批准。

独立评审出现同范围 Finding 时，作者依据 Finding 整改、重新生成受影响 root/manifest/evidence、重新派发同一 Reviewer 复审，期间不停止向用户索要确认。只有复审通过、final hygiene 24/3、Decision provenance 和 final receipt 都有效后，状态才变为 `waiting_human/candidate_approval`，并向 uroborus 展示精确 `CandidateArtifactSetRoot/R019`、manifest hash、Decision hash、正式 requirements hash、P022 hash 与 generation。

该人工批准只授权进入后续正式需求设计发布事务的资格判断；本次执行不包含正式发布、Git index/commit、远端操作或部署。未得到新的明确授权前，上述动作的执行次数必须保持 0。

### 34.14 R018 正式发布预检三项 Critical 的 R019 闭包

`R018-RELEASE-C-001` 的 37 docs + Builder 写集是历史发布合同；T06 激活后当前 docs 只登记 34 份人类 Markdown，机器源登记为 `.factory/catalog/ai-sdlc-catalog.source.json`。

`R018-RELEASE-C-002` 的确定性验证保留；稳定 Builder 当前默认读取 `.factory/catalog/ai-sdlc-catalog.source.json`，隔离候选仍只接受登记 basename，非法输入继续失败关闭。

`R018-RELEASE-C-003` 由当前正式前像闭合：IA baseline、三项 disposition、55 项 `source_preimage_disposition_refs` 中对应的活动记录和 target source-preimage binding 必须分别绑定 PRD `v4.0.0 / 648db794…`、需求矩阵 `v4.0.0 / 375ed02f…`、文档索引 `v2.0.0 / 2bc0cb84…` 的真实 hash/bytes。55 项 disposition ref 必须通过 disposition ID、source path 与 source hash 一一绑定，不允许活动表保留另一组前像。三份 target 的 current/candidate version 保持相等且 `change_level=NONE`；任何旧 `v3.1.0/v1.1.0` 或旧 hash 进入任一 CAS / disposition ref 都必须阻断，并由 required seed 的旧 hash mutation 明确证明拒绝。

<!-- sf:section-id=PROJECT-SITE-FRONTEND -->
## 只读项目站点前端增补

站点是 CLI 完整生成的离线静态文件集，不需要前端框架、网络请求或常驻服务。固定路由包含总览、需求、设计、任务、缺陷、代码、文档、质量、版本、报告和 PM 十要素列表/详情；所有详情使用独立页面和明确返回按钮，不使用 drawer、modal 或侧边详情栏。代码地图按代码文件生成详情页，文件内按稳定符号 ID 提供 AST 符号锚点、类型、签名和状态；符号仍可精确深链，但不为数千个符号重复生成完整导航壳。

页面输入由获授权 DTO 冻结。详情页先计算与 generation 无关的输入 fingerprint；输入未变时不再拼接 HTML，而是复用上一版已验证页面，generation、Git、H 和 `as_of` 统一由 `assets/snapshot.js` 注入页脚。发布器在受控 `builds/` 中生成不可变候选，APFS 使用整树 copy-on-write，其他文件系统安全回退为逐页复制，最后原子替换 `current` symlink；只保留最后有效入口。

模板版本必须参与站点级和页面级输入 fingerprint；任何 HTML 结构、CSS 或可访问性合同变化都升级渲染器版本，使旧页面自动失效。长稳定 ID、breadcrumb 和嵌套定义在窄屏强制换行；宽表格只在标记为 `role="region"`、可键盘聚焦且具有中文标签的容器内横向滚动，禁止把 body 撑出视口。代码签名必须显示 `def`、`async def` 或 `class` 定义头，decorator 不得冒充签名。

缓存命中和页面复用在返回前校验 profile、current realpath、build 边界、路由全集、文件类型、OS owner、精确 mode 和 size/mtime 元数据，并对清单内每个页面无条件重算 SHA-256；即使攻击者保持相同大小和 mtime，摘要不一致也会失败关闭。`local-owner` 可看当前 OS owner 获授权事实，`shared-restricted` 在 DTO 形成前过滤 project/restricted 字段。页面不提供新增、编辑或状态修改入口，这些动作只通过 AI 会话进入正式 workflow。

## 正式版本历史（仅已发布）

| 版本 | 日期 | 变更 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v1.0.0` | 2026-07-18 | 基于 `TASK-DESIGN-001-R019` 正式落档 | `uroborus` | `uroborus` | `uroborus` |
| `v1.1.0` | 2026-07-22 | 增补离线只读多页面项目站点、详情返回和增量渲染规则 | `uroborus` | `uroborus` | `uroborus` |
| `v1.2.0` | 2026-07-22 | 增补代码文件内符号深链与全页面摘要校验规则 | `uroborus` | `uroborus` | `uroborus` |
| `v1.3.0` | 2026-07-22 | 增补模板版本失效、代码签名和移动端可访问滚动规则 | `uroborus` | `uroborus` | `uroborus` |

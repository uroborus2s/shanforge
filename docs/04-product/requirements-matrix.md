# 需求追踪矩阵

## 版本信息

| 项目 | 内容 |
|---|---|
| 项目名称 | 山海工枢 / shanforge |
| 文档编号 | `TRACE-REQ-001` |
| 文档类型 | 需求追踪矩阵 |
| 当前正式版本 | `v4.2.0` |
| 来源候选修订 | `TASK-IMPLEMENT-003-P001` |
| 变更等级 | `MINOR` |
| 当前状态 | 已批准并生效 |
| 负责人 | `uroborus` |
| 变更人 | `uroborus` |
| 审核人 | `uroborus` |
| 批准人 | `uroborus` |
| 最近更新 | 2026-07-22 |

## 1. 需求到设计、实施和测试映射

| 需求 ID | 需求摘要 | 设计文档或状态 | 模块 | 接口 | 任务 | 测试 | 状态 |
|---|---|---|---|---|---|---|---|
| `REQ-001` | 统一 Agent Platform Kernel | `system-architecture.md`, `agent-platform-architecture.md` | `MOD-002`, `MOD-003`, `MOD-010` | `API-007` | `TASK-001`, `TASK-007` | `TC-005`, Integration | 设计基线已建立 |
| `REQ-002` | 业务 Agent App 与平台内核隔离 | `prd.md`, `agent-platform-architecture.md`, `module-boundaries.md` | `MOD-001`, `MOD-002` | `API-001` | `TASK-001`, `TASK-002` | Manifest contract | 设计基线已建立 |
| `REQ-003` | Workflow DSL 与声明式编排 | `prd.md`, `agent-platform-architecture.md`, `api-design.md` | `MOD-004` | `API-002` | `TASK-003`, `TASK-011` | `TC-002`, `TC-008`, `TC-009` | 设计基线已建立 |
| `REQ-004` | 多模型策略与供应商解耦 | `system-architecture.md`, `agent-platform-architecture.md`, `infrastructure-layer-design.md`, `api-design.md` | `MOD-005`, `MOD-012` | `API-003`, `API-004` | `TASK-004`, `TASK-005`, `TASK-013`, `TASK-017`, `TASK-019` | `TC-003` | 设计基线已建立 |
| `REQ-005` | Capability Registry 与工具执行契约 | `agent-platform-architecture.md`, `module-boundaries.md`, `api-design.md` | `MOD-006`, `MOD-012` | `API-005`, `API-009`, `API-013` | `TASK-006`, `TASK-013`, `TASK-014`, `TASK-015`, `TASK-017`, `TASK-018`, `TASK-019` | `TC-004` | 设计基线已建立 |
| `REQ-006` | Session、Memory 与 Context Engine | `system-architecture.md`, `agent-platform-architecture.md`, `memory-runtime-design.md`, `memory-system-detailed-design.md`, `memory-runtime-interfaces.md` | `MOD-007`, `MOD-010` | `API-006`, `API-007` | `TASK-007`, `TASK-014`, `TASK-016`, `TASK-017`, `TASK-019` | `TC-005`, `TC-013`, `TC-014`, `TC-015`, `TC-016` | 设计基线已建立 |
| `REQ-007` | Policy、Approval 与 Execution Sandbox | `system-architecture.md`, `agent-platform-architecture.md`, `api-design.md` | `MOD-008`, `MOD-012` | `API-008`, `API-009` | `TASK-008`, `TASK-015`, `TASK-017`, `TASK-019` | Policy / sandbox tests | 设计基线已建立 |
| `REQ-008` | Delegation、Gateway 与多入口适配 | `system-architecture.md`, `agent-platform-architecture.md`, `module-boundaries.md`, `api-design.md` | `MOD-009`, `MOD-011` | `API-010`, `API-012` | `TASK-010`, `TASK-015`, `TASK-016`, `TASK-017`, `TASK-018`, `TASK-019` | `TC-007` | 规划中 |
| `REQ-009` | 标准化 AgentResponse 与 Evidence | `agent-platform-architecture.md`, `api-design.md` | `MOD-014`, `MOD-010` | `API-011` | `TASK-009` | `TC-006` | 设计基线已建立 |
| `REQ-010` | 快速构建业务工作流 | `prd.md`, `implementation-plan.md`, `test-plan.md` | `MOD-001`, `MOD-004`, `MOD-005` | `API-001`, `API-002`, `API-003` | `TASK-002`, `TASK-003`, `TASK-011`, `TASK-012` | `TC-008`, `TC-009` | 设计基线已建立 |
| `REQ-AI-WORKFLOW-001` | 会话候选信号与确定性分类 | `TASK-DESIGN-001` 必须重写路由设计 | 会话路由、流程治理 | route input / route result | `TASK-PRD-001`, `TASK-DESIGN-001` | 路由正向、冲突、缺失测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-002` | 项目化动作必须有明确归属 | 待任务和动作状态模型设计 | WorkItem、任务治理 | WorkItem / TaskCard / WorkflowRun | `TASK-PRD-001`, `TASK-DESIGN-001` | 任务归属和越权测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-003` | PRD TaskCard 覆盖完整生命周期 | 待 PRD Workflow 重写 | 需求治理、文档治理 | PRD TaskCard / Gate | `TASK-PRD-001`, `TASK-DESIGN-001` | 生命周期状态测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-004` | Workflow 使用完整标准结构 | `v3.0.0` 已登记 123 条需求级结构映射并修正 review 主体；正式 schema 和运行时 validator 待设计 | Workflow Catalog | Workflow contract / norm mapping | `TASK-PRD-001`, `TASK-DESIGN-001` | 123 记录、必填字段、profile 引用、review selector 和主体权限完整性测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-005` | 正式 docs 默认锁定 | 待文档 Gate 设计 | 文档治理 | document-change | `TASK-PRD-001`, `TASK-DESIGN-001` | docs 写入锁测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-006` | 中间草案删除或归档 | 待草案处置设计 | 文档、归档治理 | Draft / Archive | `TASK-PRD-001`, `TASK-DESIGN-001` | archive 禁读和清理测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-007` | Memory 只保存恢复摘要 | 待 memory 边界设计 | 记忆治理 | session card / summary / doc-map | `TASK-DESIGN-001` | memory 边界测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-008` | 会话回复必须可理解 | PRD `v4.0.0 §12.7` 发布整体坐标与十五行回复合同；设计必须重新基线 | 会话输出治理 | `ProjectExecutionPosition/v1` / response template | `TASK-REQ-005`, `TASK-DESIGN-001` | 十五行顺序、唯一字段和全状态黑盒回复测试 | 需求已批准并生效；设计待重基线 |
| `REQ-AI-WORKFLOW-009` | 正式版本只在发布成功时分配，候选修订与人员可审计 | 待版本/候选/发布事务状态机设计 | 文档治理 | baseline version / candidate revision+hash / release version / project people | `TASK-PRD-001`, `TASK-DESIGN-001` | 候选不占版本、退回不入正式历史、hash 批准失效、发布回滚和人员测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-010` | PR 必须用户明确确认 | 待远端动作策略设计 | 交付治理 | remote handoff / ToolPolicy | `TASK-DESIGN-001` | PR 禁止自动创建测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-011` | Bug 先根因后修复 | 待 Bug 调查和修复 Workflow | 缺陷治理 | root cause / fix gate | `TASK-DESIGN-001` | Bug 两阶段测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-012` | 设计必须自上而下 | 旧设计草案范围失效，必须重写 | 设计治理 | requirements -> vertical trace | `TASK-PRD-001`, `TASK-DESIGN-001` | N/A 和跨层追踪测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-013` | 完整生命周期 Workflow Catalog | `v3.0.0` 已逐条登记 123 条需求级映射；可执行 RouteRule/ActionSpec/ToolPolicy/流程图仍待设计 | Workflow Governance | workflow catalog / 123 mapping records | `TASK-PRD-001`, `TASK-DESIGN-001` | ID 一致、597 节点、四规范/主体/追踪/Artifact/Gate/回复覆盖测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-014` | 每个动作具有 ActionSpec | 待 Action Catalog 和 runtime schema | Action Governance | ActionSpec / ActionRun | `TASK-DESIGN-001` | schema、幂等和回放测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-015` | 确定性 RouteRule 裁决 | 待 RouteRule Catalog 和求值器 | Routing | RouteRule / route result | `TASK-DESIGN-001` | 0/1/多规则黑盒测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-016` | 项目资料交互和 Baseline 初始化 | 待 project intake workflow | Project Governance | project info / baseline | `TASK-DESIGN-001` | 缺字段、复用和确认测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-017` | 交付拓扑和纵横矩阵 | 待 topology/vertical slice schema | Delivery Model | topology / baseline / slice | `TASK-DESIGN-001` | 拓扑和断链测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-018` | 调研发现形成证据输入 | 待 discovery method cards | Discovery | research evidence / decision | `TASK-DESIGN-001` | 事实/假设/来源测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-019` | 完整需求工程 | 待 requirements workflow/method | Requirements | brief / PRD / trace | `TASK-DESIGN-001` | REQ/AC/NFR/影响测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-020` | UX 设计方法和证据 | 待 UX workflow/method cards | UX | journey / IA / flow / prototype | `TASK-DESIGN-001` | UX 状态和可用性测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-021` | UI 完整交付包和提示词 | 待 UI workflow/prompt template | UI / Design System | page / component / prompt / prototype | `TASK-DESIGN-001` | 状态、响应式、A11y、截图测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-022` | 系统架构和质量属性 | 待 architecture method cards | Architecture | ADR / context / deployment / NFR | `TASK-DESIGN-001` | 架构追踪和质量属性测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-023` | 前后端领域和模块边界 | 待 module/service/surface design | Domain / Module | module contract / dependency | `TASK-DESIGN-001` | 边界和依赖测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-024` | 数据库设计合理性 | 待 database workflow/rubric/validator | Data / Database | field / ERD / schema / migration | `TASK-DESIGN-001` | schema、约束、索引、迁移测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-025` | API 和集成契约正确性 | 待 API/integration workflow | API / Integration | OpenAPI / event / adapter | `TASK-DESIGN-001` | lint、contract、integration 测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-026` | Business Field 跨层一致 | 待 Field Trace schema/validator | Traceability | business field trace | `TASK-DESIGN-001` | 跨层字段断链和漂移测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-027` | 纵向切片计划和任务分解 | 待 planning/dependency workflow | Planning | vertical slice / plan / task graph | `TASK-DESIGN-001` | 任务粒度、依赖、N/A 测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-028` | 受批准约束的实现 | 待 implementation action packs | Implementation | code/config/migration/resource | `TASK-DESIGN-001` | 写集、TDD、偏离测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-029` | 多产品表面和多服务交付 | 待 deliverable-specific workflows | Product Delivery | surface/service deliverables | `TASK-DESIGN-001` | 分表面/服务验收测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-030` | 完整质量测试层级 | 待 QA catalog/test matrix | Quality | test plan / reports | `TASK-DESIGN-001` | 风险裁剪和全层级测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-031` | 安全隐私合规贯穿 | 待 security workflow/threat model | Security | threat / control / exception | `TASK-DESIGN-001` | 安全、隐私、供应链测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-032` | 性能可靠性可观察性可度量 | 待 quality attribute workflow | Reliability | SLO / capacity / telemetry | `TASK-DESIGN-001` | 负载、恢复和告警测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-033` | Review/Verification/Human 分离 | 待 Gate 状态机设计 | Quality Governance | review / evidence / human decision | `TASK-DESIGN-001` | Gate 越权和退回重审测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-034` | ToolPolicy 最小授权 | 待 ToolPolicy Catalog | Tool Governance | tool policy / tool event | `TASK-DESIGN-001` | 参数、路径、风险授权测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-035` | 子代理和并行任务图 | 待 delegation workflow | Delegation | delegation brief / result | `TASK-DESIGN-001` | 独立性、写集、超时测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-036` | Git 动作逐级授权 | 待 VCS ActionSpec | Version Control | diff/stage/commit/push/PR/merge | `TASK-DESIGN-001` | 授权、脏树、结果回读测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-037` | 发布部署回滚闭环 | 待 release/deploy workflow | Delivery | artifact / deploy / rollback | `TASK-DESIGN-001` | 制品、预发、生产、回滚测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-038` | 运维事件问题管理 | 待 operations/incident workflow | Operations | SLO / incident / RCA / runbook | `TASK-DESIGN-001` | 告警、事件、恢复演练 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-039` | 变更迁移弃用退役 | 待 change/evolution workflow | Evolution | impact / migration / decommission | `TASK-DESIGN-001` | 兼容、迁移、清理测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-040` | Catalog 扩展和完整性 | 待 extension workflow/validator | Workflow Governance | extension request / catalog version | `TASK-DESIGN-001` | 引用完整性和迁移测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-041` | 四套顶层规范先于 Workflow | `v3.0.0` 已发布四套顶层规范，123 条记录已逐条引用；正式 schema 待设计 | Governance Model | process/collaboration/work/document specs | `TASK-PRD-001`, `TASK-DESIGN-001` | 四规范引用覆盖、冲突和版本测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-042` | 完整生命周期阶段门 | PRD `v4.0.0 §12.7.2` 固定唯一 active lifecycle binding 和真实 N/M；设计必须重新基线 | Process Governance | `LifecyclePlanBinding` / lifecycle stage / transition / N/A | `TASK-REQ-005`, `TASK-DESIGN-001` | 零/多 binding、hash、stage-map、权限和局部 plan 冒充测试 | 需求已批准并生效；设计待重基线 |
| `REQ-AI-WORKFLOW-043` | 每个角色和 Node 标明人类、AI 或确定性系统主体类型与协作分工 | 待 Role Assignment/RACI/decision authority 设计 | Collaboration Governance | role ID / actor type / assignee / responsibility / decision matrix | `TASK-DESIGN-001` | 主体类型覆盖、人类/AI Reviewer 拆分、角色权限和人工专有决策禁止测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-044` | 人的工作规范 | 待 human work contract 设计 | Collaboration Governance | human input / decision / feedback | `TASK-DESIGN-001` | 歧义批准、外部改动和反馈测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-045` | AI 的工作规范 | PRD `v4.0.0` 固定安全自动继续和真实停止条件；设计必须重新基线 | Agent Governance | AI read/write/execute/claim/continuation rules | `TASK-REQ-005`, `TASK-DESIGN-001` | 自动继续、虚假人工等待、越权和完成声明测试 | 需求已批准并生效；设计待重基线 |
| `REQ-AI-WORKFLOW-046` | 单 Session 固定状态机 | PRD `v4.0.0` 增加原子固定 H 和同 snapshot 回复装配；设计必须重新基线 | Session Governance | session state / continuation policy / fixed H | `TASK-REQ-005`, `TASK-DESIGN-001` | H+1 并发、恢复/查询同 binding、停止和重定向测试 | 需求已批准并生效；设计待重基线 |
| `REQ-AI-WORKFLOW-047` | 回答、落盘和人机交接规则 | PRD `v4.0.0` 限定六类人工计划 Gate 并要求准确责任人；设计必须重新基线 | Collaboration Output | response / persistence / handoff / human gate | `TASK-REQ-005`, `TASK-DESIGN-001` | 六类人工等待、只回答、正式化和交接测试 | 需求已批准并生效；设计待重基线 |
| `REQ-AI-WORKFLOW-048` | 每流程版本化 Artifact 输入输出契约 | PRD `v3.3.0` 增加“先判断权威性、可重建性和保留期，再选择存储”约束；设计须重基线 | Artifact Governance | artifact class / fact domain / input-output / retention decision | `TASK-REQ-004`, `TASK-DESIGN-001` | 分类、事实源、状态、候选/hash、存储必要性和处置测试 | 需求已批准；设计待重基线 |
| `REQ-AI-WORKFLOW-049` | 覆盖完整生命周期的 Artifact 分类基线 | 待完整 Artifact Registry 和目录/存储映射设计 | Artifact Governance | 17-class registry / path mapping | `TASK-DESIGN-001` | 17 类覆盖、唯一主类、N/A 和未分类阻断测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-050` | 每个 Artifact 类别定义允许和禁止内容 | PRD `v3.3.0` 固定 Git 允许/禁止矩阵和 worktree/untracked/index/commit-range 写入 Gate；设计须重基线 | Artifact Governance、Security | content policy / Git blob gate / external reference | `TASK-REQ-004`, `TASK-DESIGN-001` | 禁止 blob、重命名、压缩、改扩展名和先加后删攻击测试 | 需求已批准；设计待重基线 |
| `REQ-AI-WORKFLOW-051` | 事实资格和冲突按事实领域裁决 | 待 Fact Authority Registry 和冲突求值器设计 | Artifact Governance、Fact Governance | 14 fact domains / authority / conflict result | `TASK-DESIGN-001` | 权威源、跨域漂移、冲突、新鲜度和覆盖攻击测试 | 需求已批准；设计待执行 |
| `REQ-AI-WORKFLOW-052` | 每个 Artifact 类别具有生命周期和保留处置 | PRD `v3.3.0` 发布 `PT168H`、Review 子类型、选中/未发布候选清理、可重建 payload、发布后 `cleanup_pending` 和受控 N/A；设计须重基线 | Artifact Governance、Records Management | lifecycle / retention / legal hold / disposition / rebuild | `TASK-REQ-004`, `TASK-DESIGN-001` | 时间边界、引用/hold、幂等清理、决定保护和重建测试 | 需求已批准；设计待重基线 |
| `REQ-AI-WORKFLOW-053` | Artifact 治理使用量化验收和黑盒测试 | PRD `v3.3.0` 增加 `AC-RET-001..015`；待与 `AC-ART-001..014` 一并设计 validator/test suite | Artifact Governance、Quality | acceptance registry / retention scenarios / black-box tests | `TASK-REQ-004`, `TASK-DESIGN-001` | 禁止 blob、TTL、候选处置、权威记录零丢失、摘要单份和三次重建 | 需求已批准；设计待重基线 |
| `REQ-CHANGE-ARTIFACT-RETENTION-001` | 最小保留、临时证据清理和外部持久存储受控 N/A | PRD `v3.3.0` §10.5.7.1；R016/P016 因强制持久存储前提失效，同一设计 TaskCard 必须生成新候选和计划 | Artifact Governance、Records Management、Git Governance | `PT168H` / cleanup / Git gate / rebuild contract / controlled N/A | `TASK-REQ-004`, `TASK-DESIGN-001` | `AC-RET-001..015`，独立需求复审 `approved / 100` | 已批准并生效；设计待重基线 |
| `REQ-CHANGE-WF-CTL-010-001` | 项目进度查询使用确定性快照和固定代码输出，统一生成会话事实摘要、第一页总览加十管理页 HTML、目录加十业务表 Excel，并保证事实资格、权限、性能和跨格式一致 | `PRD v3.1.0` 已发布详细需求；`TASK-DESIGN-001` 必须完成影响分析并补齐来源注册、全局日志、高水位、SQLite 投影、工具策略、渲染和校验设计 | Project Control、Fact Projection、Reporting | snapshot / tool plan / HTML / Excel contract 待设计 | `TASK-REQ-002`, `TASK-DESIGN-001` | R014 需求合同 `81/81`、变异 `69/69`、56 个验收夹具；运行时性能、浏览器和逐字段对账待实现验证 | 需求已批准并生效；设计受影响待更新 |
| `REQ-AI-WORKFLOW-054` | 主任务与派生投影和昂贵回归解耦 | `PRD v4.0.0 §12.6/§12.7`；新增位置视图只能消费同一 authorized snapshot 且无 Gate 权限，设计必须重新基线 | Session/Task/Projection/Verification Governance | AuthoritativeEvent / DurableTaskRequest / DispatchOutbox / Projection / Position / Regression / Gate contracts 待重设计 | `TASK-REQ-003`, `TASK-REQ-005`, `TASK-DESIGN-001` | `REQ-ASYNC-001..018`、`REQ-VIS-001..009`、异步和位置 NFR 的 schema、边界、变异和性能验证 | 需求已批准并生效；设计待重基线 |
| `REQ-CHANGE-AI-EXEC-ASYNC-001` | 记忆和项目进度更新独立成系统侧任务，主会话不等待；验证按 `V0-V4` 影响分级，全仓回归只用于系统级变更 | `PRD v3.2.0` 已完整融入原执行模型和既有 Workflow；R010/P008 已失去发布资格，`TASK-DESIGN-001` 必须生成新计划和设计候选 | Task Runtime、Projection、Memory、Project Control、QA、Delivery | task request / outbox / high-water / reducer / test selection / evidence reuse / response contracts 待设计 | `TASK-REQ-003`, `TASK-DESIGN-001` | R003 作者校验 `39/39`、独立复审 `approved/100`；设计 validator 和运行时测试待完成 | 需求已批准并生效；设计受影响待更新 |
| `REQ-CHANGE-AI-EXEC-VISIBILITY-001` | 从项目整体计划清楚说明当前 N/M、任务、节点、停止原因、下一责任人和唯一下一步 | R020 正式设计已发布；R002 已正式发布该变更的项目控制增量 | Project Control、Session、Response、Gate、Permission | `ProjectProgressSnapshot/v2` / `ProjectExecutionPosition/v1` / `LifecyclePlanBinding` / `REQ-ASYNC-016` | `TASK-REQ-005`, `TASK-DESIGN-001`, `TASK-IMPLEMENT-001` | R002 发布后 832/832；项目控制、三入口、权限、CAS、性能和消费者回归通过 | 需求与设计已发布；R002 相关增量已实现 |
| `REQ-VIS-001` | 唯一正式 lifecycle 坐标 | `workflow-execution-design.md`、`module-domain-design.md` | Project Control | `LifecyclePlanBinding/v1` / N/M | `TASK-IMPLEMENT-001-P001-T01/T02/T08` | `test_project_control_contracts.py`、`test_project_control_position.py`、`test_project_control_integration.py` | R002 已实现并正式发布 |
| `REQ-VIS-002` | 唯一 shared reducer 与九字段绑定 | `workflow-execution-design.md`、`api-design.md` | Projection、Position | `ProjectProgressSnapshot/v2` / `ProjectExecutionPosition/v1` | `TASK-IMPLEMENT-001-P001-T01/T02/T08` | `test_project_control_position.py`、`test_project_control_integration.py` | R002 已实现并正式发布 |
| `REQ-VIS-003` | 七种互斥 execution disposition 与真实 Gate | `workflow-execution-design.md` | Session、Gate | disposition / condition | `TASK-IMPLEMENT-001-P001-T03` | `test_project_control_disposition.py` | R002 已实现并正式发布 |
| `REQ-VIS-004` | 固定 H 与三入口一致 | `workflow-execution-design.md`、`api-design.md` | Project Control、Recovery | as-of H / snapshot binding | `TASK-IMPLEMENT-001-P001-T02/T08` | `test_project_control_position.py`、`test_project_control_integration.py` | R002 已实现并正式发布 |
| `REQ-VIS-005` | 未登记 evidence 恢复与 CAS | `workflow-execution-design.md` | Evidence、Gate | observation / five-field CAS | `TASK-IMPLEMENT-001-P001-T05` | `test_project_control_evidence.py` | R002 已实现并正式发布 |
| `REQ-VIS-006` | 权限过滤和侧信道防护 | `api-design.md`、`module-domain-design.md` | Authorization、Renderer | authorized view / redaction | `TASK-IMPLEMENT-001-P001-T04/T08` | `test_project_control_response.py`、`test_project_control_integration.py` | R002 已实现并正式发布 |
| `REQ-VIS-007` | 十五行 MAJOR 回复迁移 | `api-design.md`、`frontend-design.md` | Response | `ProjectStatusResponse/v4` | `TASK-IMPLEMENT-001-P001-T04/T08` | `test_project_control_response.py`、consumer 回归 | R002 已实现并正式发布 |
| `REQ-VIS-008` | P017/R017 十类旧资格拒绝 | `workflow-execution-design.md` | Eligibility、Gate | requirements/plan/candidate/generation binding | `TASK-IMPLEMENT-001-P001-T03/T05` | `test_project_control_disposition.py`、`test_project_control_evidence.py` | R002 已实现并正式发布 |
| `REQ-VIS-009` | 精确写集和禁止路径 | `workflow-execution-design.md`、`module-domain-design.md` | Task Governance、Security | `ArtifactWriteAttestation/v1` / scope anchor | `TASK-IMPLEMENT-001-P001-T07` | `test_project_control_provenance.py` | R002 已实现并正式发布 |
| `REQ-PKI-001..003` | 快速快照、自适应文档和单一记忆点 | `system-architecture.md`、`memory-design.md` | application、runtime、settings | `snapshot`、semantic locator | `TASK-IMPLEMENT-003` | CLI、memory 读取预算、无变化复用 | 已实现，待最终独立复审 |
| `REQ-PKI-004..007` | SQLite 知识核心、稳定身份、关系图和代码地图 | `data-design.md`、`module-domain-design.md`、`interface-matrix.md` | domain、runtime、settings | index/find/show/trace/context | `TASK-IMPLEMENT-003` | schema、extractor、关系、查询和集成测试 | 已实现，待最终独立复审 |
| `REQ-PKI-008..010` | 只读多页面站点、页面 freshness/权限和项目管理十要素 | `frontend-design.md`、`ux-ui-design.md` | application、runtime、settings | site snapshot、PM projection | `TASK-IMPLEMENT-003` | renderer、权限、四视口、可访问性和 137 字段映射 | 已实现，待浏览器验收 |
| `REQ-PKI-011..013` | 异步同步、Git 边界和有界 cache | `workflow-execution-design.md`、`technical-selection.md` | application、settings | sync enqueue/head、maintain | `TASK-IMPLEMENT-003` | coalesce、fencing、重试、TTL、容量和路径安全 | 已实现，待最终独立复审 |
| `REQ-PKI-014..016` | 安全最小化、旧资料迁移和固定查询命令面 | `api-design.md`、`data-design.md`、`docs/05-design/index.md` | access、application、settings | 固定 CLI receipt | `TASK-IMPLEMENT-003` | ACL、symlink/traversal、迁移对账、稳定退出码 | 实施收口中 |

### 1.1 R002 正式实现覆盖

R002 是项目控制与执行可见性增量，不是全部产品需求实现。正式需求总数为 123；本轮有产品代码和测试追踪的需求为 15，剩余 108 项继续保持未实现状态。`REQ-CHANGE-AI-EXEC-VISIBILITY-001` 是变更容器，不重复进入 15 项计数。

| 实现 ID | 交付能力 | 主要代码落点 | 主要验证 |
|---|---|---|---|
| `REQ-ASYNC-015` | completion、quick verification 与 durable regression 状态分离 | `domain/project_control`、`runtime/project_control`、`settings/project_control` | `test_project_control_verification.py`、`test_project_control_integration.py` |
| `REQ-ASYNC-016` | 严格十五行回复、真实责任人和后台派发状态 | `application/project_control`、`settings/project_control/renderer.py` | `test_project_control_response.py`、`test_project_control_integration.py` |
| `REQ-VIS-001..009` | 生命周期坐标、shared reducer、处置、fixed H、CAS、权限、回复、旧资格、写集 | `access/application/domain/runtime/settings` 五层项目控制实现 | `test_project_control_*.py` |
| `NFR-VIS-001..004` | 可理解性、一致性、安全和性能 | 唯一 service/reducer/renderer、exact-context permission、性能预算 | 10k/100k fixture、权限/证据/资格攻击、全仓回归 |

当前发布身份：`TASK-IMPLEMENT-001-R002`；事务：`IMPLEMENTATION-RELEASE-TX-R002-G001`；formal manifest SHA-256：`eae82c9048f0a291a837d63ef1c57601b746233e04387da7264f3358a8d77c0a`。Git、远端和部署不属于该事务，均未执行。

## 2. 非功能需求映射

| NFR ID | 要求 | 设计落点或状态 | 验证方式 |
|---|---|---|---|
| `NFR-001` | 可扩展性 | `system-architecture.md`, `module-boundaries.md` | 适配器替换测试 |
| `NFR-002` | 可审计性 | `agent-platform-architecture.md`, `test-plan.md` | 事件与 evidence 回放 |
| `NFR-003` | 可测试性 | `api-design.md`, `test-plan.md` | contract tests + mock provider |
| `NFR-004` | 隔离性 | `module-boundaries.md` | import boundary review |
| `NFR-005` | 成本与隐私控制 | `prd.md`, `api-design.md` | model policy tests |
| `NFR-AI-WORKFLOW-001` | 所有项目化会话必须追溯到 WorkItem；只有需要跨会话继续、存在依赖、需要验收或评审时，才必须追溯到 TaskCard。 | 待状态模型与 ledger 设计 | REQ、AC、NFR、矩阵交叉一致性检查 |
| `NFR-AI-WORKFLOW-002` | 最小上下文读取 | 待 memory 读取边界设计 | 黑盒流程测试 |
| `NFR-AI-WORKFLOW-003` | 防越权写入 | 待路由与 Gate 设计 | 写集和流程测试 |
| `NFR-AI-WORKFLOW-004` | 协作回复可读 | 待回复模板设计 | 人工验收、黑盒会话测试 |
| `NFR-AI-WORKFLOW-005` | 最小正式文档结构 | 待 docs 最小结构设计 | docs-stratego 与文档 review |
| `NFR-AI-WORKFLOW-006` | 项目事实变更确定性 | 待 RouteRule/ActionSpec runtime | 唯一路由、冲突、缺失、越权测试 |
| `NFR-AI-WORKFLOW-007` | ActionRun 可回放 | 待 ActionRun schema/store | schema、引用和回放测试 |
| `NFR-AI-WORKFLOW-008` | 跨层字段一致性 | 待 Business Field Trace validator | 需求/领域/DB/API/UI/test 断链测试 |
| `NFR-AI-WORKFLOW-009` | 中断恢复和幂等 | 待 WorkflowRun checkpoint/idempotency | 重复、超时、中断恢复测试 |
| `NFR-AI-WORKFLOW-010` | Catalog 可维护性 | 待 catalog owner/version/reference validator | 孤立对象、版本、引用完整性测试 |
| `NFR-AI-WORKFLOW-011` | Artifact 治理完整性 | 待 Artifact Registry、Fact Authority、生命周期、secret 和处置 validator | 分类/元数据/权威/生命周期 100% 覆盖，非法写入、禁止内容、权威覆盖、非法转换和冲突越过 Gate 为 0 |
| `NFR-ASYNC-001..002` | 上下文隔离和主任务低延迟 | 待隔离任务信封、原子提交和恢复预算设计 | 父聊天继承 0、8 KiB 上限、原子批次 P95、1,000 ms reducer |
| `NFR-ASYNC-003..005` | 最终一致、查询准确和幂等合并 | 待投影高水位、同一 reducer、背压和死信设计 | 60 秒 P95、旧数据冒充 0、重复副作用 0 |
| `NFR-ASYNC-006..008` | 测试经济、验证可审计和后台权限隔离 | 待影响策略、证据复用键和 ToolPolicy 设计 | `V0-V3` 无全仓扩大、决策 100% 可追溯、授权继承和越权写入 0 |
| `NFR-VIS-001` | 项目回复可理解性 | `ProjectStatusResponse/v4` 唯一十五行 renderer 已发布 | `test_project_control_response.py`、Skill consumer 回归；十五行完整、无重复状态/下一步 |
| `NFR-VIS-002` | snapshot/position 一致性 | shared reducer、fixed H 与三入口同 snapshot 已发布 | `test_project_control_position.py`、`test_project_control_integration.py`；第二 reducer 为 0 |
| `NFR-VIS-003` | 权限、evidence 和资格安全 | exact-context permission、五字段 CAS、旧资格拒绝和写入证明已发布 | response/evidence/provenance/integration 攻击；未授权正式/Git 动作为 0 |
| `NFR-VIS-004` | 位置视图性能不回退 | 10,000 task / 100,000 event fixture 和读取预算已发布 | `test_project_control_verification.py`、`test_project_control_integration.py`；1000 行/8 MiB/3000 ms 门通过 |

## 3. 当前缺口

| GAP ID | 问题 | 计划 |
|---|---|---|
| `GAP-001` | Agent App Manifest 尚未代码化 | `TASK-002` |
| `GAP-002` | Workflow Runtime 仍未实现 | `TASK-003` |
| `GAP-003` | Provider adapters 与 mock provider 仍未实现 | `TASK-004`, `TASK-005` |
| `GAP-004` | Capability Registry 尚未形成统一 schema | `TASK-006` |
| `GAP-005` | Session ledger、memory promotion 与 recall pipeline 仍未实现 | `TASK-007` |
| `GAP-006` | Approval / Sandbox / Evidence 仍缺代码闭环 | `TASK-008`, `TASK-009` |
| `GAP-007` | Demo Agent Apps 仍未交付 | `TASK-011` |
| `GAP-008` | file / web / terminal / browser / session_search / skills 仍未形成统一基础能力包 | `TASK-013` ~ `TASK-017` |
| `GAP-009` | `todo / clarify / cronjob / execute_code` 仍未完成取舍与最小原型验证 | `TASK-018` |
| `GAP-010` | 基础能力层 bridge contract 与回归测试仍未建立 | `TASK-019` |
| `GAP-AI-001` | Workflow Catalog 尚未形成正式设计 | `TASK-DESIGN-001` |
| `GAP-AI-002` | docs、workitems、memory 最小结构尚未正式批准 | `TASK-DESIGN-001` |
| `GAP-AI-003` | 数据库、API、UI 字段一致性机制尚未设计 | `TASK-DESIGN-001` |
| `GAP-AI-004` | 各 workflow skill 和黑盒流程测试尚未按新 PRD 实施 | 后续实施计划 |
| `GAP-AI-005` | 旧流程只定义 11 条宽泛 Workflow，不覆盖第 10 章 123 条核心 Workflow | `TASK-DESIGN-001` 重写完整 Catalog |
| `GAP-AI-006` | 缺 ActionSpec、ActionRun、RouteRule、ToolPolicy 的机器可执行契约 | `TASK-DESIGN-001` 设计 schema、状态机和 validator |
| `GAP-AI-007` | 缺项目交付拓扑、纵向切片和 Business Field Trace | `TASK-DESIGN-001` 设计对象、路径和跨层校验器 |
| `GAP-AI-008` | 缺专用数据库、发布和运维 workflow skill | 设计阶段形成能力缺口与新增/复用计划 |
| `GAP-AI-009` | `v3.0.0` 已完成 123 条需求级四规范映射，但四套规范和 Workflow 仍缺正式机器 schema、可执行继承校验、RouteRule/ActionSpec/ToolPolicy 定义及完整流程图 | `TASK-DESIGN-001` 导入发布绑定的 JSONL，逐条解析 `design_required` 槽位，不重新人工抄写 |
| `GAP-AI-010` | 现有文档模板和需求技能仍把草稿号当作正式版本，缺候选修订/hash、发布事务和版本回滚状态机 | `TASK-DESIGN-001` 设计版本对象和 Workflow；后续实现任务修正模板、skill 和黑盒测试 |
| `GAP-AI-011` | 尚无 Role Assignment 的 `actor_type`、实例 ID、决策权和授权来源 schema，无法机器阻止 AI 占用人工专有角色 | `TASK-DESIGN-001` 设计 Role Catalog/Assignment schema、validator 和人类/AI Reviewer 分离黑盒测试 |
| `GAP-AI-012` | 尚无覆盖 17 类产物、14 个事实域、允许/禁止内容、生命周期、`PT168H`、Review 子类型、Git blob Gate、候选清理、重建合同、精确目录/存储映射和受控 N/A 的完整 Artifact Registry 与 validator | `TASK-DESIGN-001` 基于 PRD `v3.3.0` 重建设计唯一机器事实源、状态机、路径映射、Fact Authority，并实现 `AC-ART-001..014` 与 `AC-RET-001..015`；R016/P016 禁止复用 |
| `GAP-AI-013` | 当前 R010/P008 未覆盖主任务与记忆/进度投影解耦、原子 outbox、记忆恢复预算、`V0-V4`、RegressionTask CAS 和证据复用合同 | 在同一 `TASK-DESIGN-001` 基于 PRD `v3.2.0` 重建计划、设计、Catalog、validator 和独立评审 |
| `GAP-AI-014` | P017/R017 缺口已由 R020 设计与 R002 项目控制增量闭合；剩余 108 项需求仍需后续产品增量 | 保留 R020/R002 证据；按新优先级建立后续实施 WorkItem，不复用旧资格 |

## 4. 正式版本历史（仅已发布）

| 版本 | 日期 | 变更内容 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v2.0` | 2026-04-13 | 重写需求矩阵，建立纯 `v2` 需求、接口、任务和测试映射 | 历史记录未登记 | 历史记录未登记 | 历史记录未登记 |
| `v2.1` | 2026-04-15 | 为 `REQ-006` 补充记忆详细设计追踪 | 历史记录未登记 | 历史记录未登记 | 历史记录未登记 |
| `v2.2` | 2026-04-15 | 为 `REQ-004` ~ `REQ-008` 补充基础能力增量任务追踪 | 历史记录未登记 | 历史记录未登记 | 历史记录未登记 |
| `v2.3` | 2026-04-19 | 补充记忆详细设计、运行时接口和专项测试追踪 | 历史记录未登记 | 历史记录未登记 | 历史记录未登记 |
| `v2.4` | 2026-07-08 | 破坏性迁移后移除旧设计页引用，只保留当前正式设计落点 | 历史记录未登记 | 历史记录未登记 | 历史记录未登记 |
| `v3.0.0` | 2026-07-11 | 发布 53 条软件生命周期治理需求、11 条治理 NFR、123 条 Workflow 需求映射及其设计和验证追踪 | `uroborus` | `uroborus` | `uroborus` |
| `v3.1.0` | 2026-07-15 | 新增 `REQ-CHANGE-WF-CTL-010-001` 追踪，绑定 `WF-CTL-010` 的确定性进度快照、代码输出、准确性、权限、性能和跨格式验收及设计影响 | `uroborus` | `uroborus` | `uroborus` |
| `v3.2.0` | 2026-07-16 | 新增 `REQ-AI-WORKFLOW-054`、`REQ-CHANGE-AI-EXEC-ASYNC-001`、18 条异步执行规则、52 条验收标准和 8 条 NFR 的设计、任务与测试追踪 | `uroborus` | `uroborus` | `uroborus` |
| `v3.3.0` | 2026-07-17 | 新增 `REQ-CHANGE-ARTIFACT-RETENTION-001`，绑定 `PT168H`、Git 禁止 blob Gate、Review 决定/过程材料分层、候选清理、重建合同、外部持久存储 N/A 和 `AC-RET-001..015` | `uroborus` | `uroborus` | `uroborus` |
| `v4.0.0` | 2026-07-18 | 新增 `REQ-CHANGE-AI-EXEC-VISIBILITY-001`、`REQ-VIS-001..009` 和 `NFR-VIS-001..004`，发布整体 N/M、共享位置绑定、互斥处置、十五行回复、固定 H、证据恢复、权限过滤和旧资格拒绝追踪 | `uroborus` | `uroborus` | `uroborus` |
| `v4.1.0` | 2026-07-20 | 绑定 R020 正式设计与 R002 正式实现，登记 15/123 产品代码覆盖、108 项剩余和发布后验证证据 | `AI_EXECUTOR` | 独立 Reviewer | `uroborus` |
| `v4.2.0` | 2026-07-22 | 原位登记 `REQ-PKI-001..016`、`NFR-PKI-001..011` 到设计、实现和验证关系；矩阵的实时视图改由 SQLite 关系图与固定 HTML 生成器派生 | `uroborus` | `uroborus` | `uroborus` |

> `v4.1.0` 只有在 `TASK-DELIVERY-001-R001` 经人类验收并由正式文档事务激活后进入本历史；本 after-image 位于候选目录时不构成正式发布。

> `v3.0.0` 由 `TASK-PRD-001-R006` 发布；`v3.1.0` 由 `TASK-REQ-002-R014` 发布；`v3.2.0` 由 `TASK-REQ-003-R003` 发布；`v3.3.0` 由 `TASK-REQ-004-R002` 发布；`v4.0.0` 由 `TASK-REQ-005-R003` 发布。其他未生效候选只保留在 TaskCard ledger、review、evidence 或受控临时区，不进入正式版本历史。

<!-- sf:section-id=TRACEABILITY-RUNTIME-RULE -->
## 5. 运行时追踪规则

本文件面向产品、架构、开发、测试、审计者和项目负责人，保存稳定的需求追踪基线；它不是每次查询都人工维护的实时状态表。需求、设计、实现或测试变化时，由固定索引器重建 SQLite 当前投影，关系声明和稳定 locator 随源文件进入新 generation。HTML 从 SQLite 快速生成，人类仍从本文件及 Git 历史查看正式基线。

索引不保存文档正文，只保存实体、文档/章节语义 locator、内容与语义 hash、来源、关系和安全摘要。读取章节时按 `document_id + section_id` 定位并校验 block hash；代码按模块与 AST qualified symbol 定位；JSON 按 JSON Pointer；JSONL 按稳定 event UID。标题可改、段落可前插，locator 不依赖行号。

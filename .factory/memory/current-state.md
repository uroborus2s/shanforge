# 当前状态

- 当前模式：cli_direct
- 当前阶段：PLAN
- 活跃任务：0
- 活跃变更：0
- 活跃缺陷：0
- 活跃 PR：0

- 角色目录总数：9
- 当前阶段主要角色：项目协调者、解决方案架构师、UX/UI 设计师、后端工程师、前端工程师、文档与记忆管理员

- 当前技术画像：抽象 Agent 平台规划画像
- 技术画像预设：custom
- 关键工程规则数：3
- 设计交付物数：1

## 最近条目

- 任务：无
- 变更：无
- 缺陷：无
- 2026-04-15：已系统重构 `docs/04-project-development/04-design/` 的主入口与专题页；`solution-overview.md`、`backend-design.md`、`database-design.md`、`deployment-architecture.md`、`frontend-adapters-and-multi-agent-coordination.md`、`action-registry-and-autonomy-policy.md` 已统一到“六层架构 + consumer-owned ports + domain owner”口径，并同步修正 draw.io 关键标签。
- 2026-04-15：已把主执行链正式改为 `ExecutionService -> SessionDomainService / MemoryDomainService -> domain ports -> storage/runtime capability`；`src/storage/*` 已直接实现领域层仓储端口，默认容器不再把记忆业务主链建立在 `runtime.memory.runtime` 上，并新增 `tests/test_application_execution.py` 验证应用层只做薄编排。
- 2026-04-15：已新增 [layered-domain-interface-catalog.md](../../docs/04-project-development/04-design/layered-domain-interface-catalog.md)，把六层架构细化为“层 -> 领域 -> 接口 owner -> 下行依赖”总表，并先落 access/application/domain/runtime 的接口骨架，不做实现。
- 2026-04-15：已按“用户界面层 / 接口网关层 / 业务调度层 / 业务模型层 / 基础能力层 / 基础设置层”统一重构主架构文档；正式收口“`src/adapters` + `src/storage` + `src/bootstrap` 属于基础设置层实现分区，不是额外层次”。
- 2026-04-15：已把基础设施层第一批正式代码骨架落地到 `src/`：新增 `domain/approval`、`domain/delegation`、`domain/gateway`，补齐 `ApprovalPolicyPort`、`SandboxPolicyPort`、`DelegationTransportPort`、`GatewayPort`，并加入 Hermes-backed adapter scaffold 与容器开关。
- 2026-04-15：已吸收 `/Users/uroborus/AiProject/hermes-agent` 的记忆系统设计精华，更新 [memory-system-detailed-design.md](../../docs/04-project-development/04-design/memory-system-detailed-design.md)、[memory-runtime-interfaces.md](../../docs/04-project-development/04-design/memory-runtime-interfaces.md) 与 [hermes-agent-source-analysis-report.md](../../docs/04-project-development/02-discovery/hermes-agent-source-analysis-report.md)，正式补齐 provider manager、archive query、snapshot policy 与 Hermes 可复用能力判断。
- 2026-04-15：已将 [infrastructure-layer-design.md](../../docs/04-project-development/04-design/infrastructure-layer-design.md) 收紧为“设计先行、实现优先复用 Hermes”的口径，并补齐技术域到 Hermes 模块的复用映射、反腐适配边界和 Hermes-backed adapter 落地规则。
- 2026-04-15：新增 [infrastructure-layer-design.md](../../docs/04-project-development/04-design/infrastructure-layer-design.md)，把基础设施层正式建模为 7 个技术域，并收口“应用层门面接口 + 运行时资源端口”的对外服务界面。
- 2026-04-15：新增 [memory-system-detailed-design.md](../../docs/04-project-development/04-design/memory-system-detailed-design.md)，把 `memory-system-business-requirements.md` 的业务约束正式下沉为系统分层、领域模型、存储分桶、源代码骨架、对外服务界面和基础设施端口设计，并给出主 Agent 的业务评估与改进顺序。
- 2026-04-15：新增 [memory-system-business-requirements.md](../../docs/04-project-development/03-requirements/memory-system-business-requirements.md)，固化本轮关于记忆分桶、混合技术栈项目装配、Skill 按需加载和多 Agent 协作的业务共识。
- 2026-04-15：已新增 `08-子系统定义图` 与 `09-记忆系统跨层调用图`，并补充 `core-subsystems.md`、更新设计索引；当前正式子系统收口为记忆系统、模型网关、能力系统。
- 2026-04-15：已把真实源码迁移到最终骨架：`src` 第一层文件夹就是层、第二层文件夹就是模块；完成 `access / application / runtime / adapters / storage / bootstrap` 重排，并将 application-owned ports、runtime-owned ports、memory/evidence/dataset store 拆到各自模块。
- 2026-04-15：新增 [core-subsystems.md](../../docs/04-project-development/04-design/core-subsystems.md)，正式定义当前 3 个子系统：记忆系统、模型网关、能力系统，并补齐记忆系统从 access -> application -> runtime -> context -> storage 的跨层调用链。
- 2026-04-15：已把代码骨架映射再收紧为“`src` 第一层文件夹就是层、第二层文件夹就是模块、模块本身就是内聚领域”；目录表达统一为 `src/access`、`src/domain`、`src/application`、`src/runtime`、`src/adapters`、`src/storage`、`src/bootstrap`。
- 2026-04-15：已按“消费者定义向下依赖接口、实现层负责实现”重写分层接口口径，并更新 `07-分层接口总表图`；明确业务定义层不是接口定义层，也不再保留统一 `ports_layer` 设计。
- 2026-04-15：已把多页 `v2-architecture-views.drawio` 拆成 7 个单页 `drawio` 文件，兼容只显示第一页的预览场景，并新增单页清单入口。
- 2026-04-14：已补齐 draw.io 的 `06-层间依赖图` 与 `07-分层接口总表图`，并把记忆系统明确表达为“对外内聚、对内分层”的统一子系统。
- 2026-04-14：已在架构文档中明确 `Memory Runtime` 属于平台核心能力层中的 `memory_runtime` 模块，不是并列独立大层；同时补齐了层间依赖关系和每层对外函数接口口径。
- 2026-04-14：`v2` 代码骨架映射已正式调整为“`src` 第一层=架构层、第二层=模块”；后续已进一步修订为接口归消费者所在层的 `ports/`，不再保留统一 `ports_layer`。
- 2026-04-14：新增 [architecture-layer-code-mapping.md](../../docs/04-project-development/04-design/architecture-layer-code-mapping.md)，明确目标骨架，以及当前 `src/` 到目标骨架的过渡映射关系。
- 2026-04-14：新增 `docs/04-project-development/04-design/assets/v2-architecture-views.drawio`，补齐 `v2` 系统分层图、功能模块总览图、`Memory Runtime` 子模块图和 `src/` 实现映射图。
- 2026-04-14：新增 `memory-runtime-design.md`，将记忆系统正式独立为 `Memory Runtime`，并确立“事件/evidence 为第一事实源，记忆为二级蒸馏资产”的设计原则。
- 2026-04-14：补充 `Memory Distillation Pipeline v1`，明确首版采用“规则治理 + 选择性 LLM 候选生成 + 样本沉淀”，暂不把自训练模型作为前提。
- 2026-04-14：新增 `memory-runtime-interfaces.md` 与四个子设计文档，明确 `prepare_session / distill_session / recall` 对外界面，以及 `session ledger / promotion / recall / distillation-learning` 的实现边界。
- 2026-04-14：`src/` 已落最小记忆闭环：新增 `domain.memory`、`runtime.memory`、`InMemoryMemoryStore / InMemoryEvidenceStore`，并将 recall / distill / promotion 接入 `ExecutionService`、`ContextEngine` 和默认容器。
- 2026-04-14：`uv run pytest tests/test_memory_runtime.py tests/test_context_engine.py tests/test_platform_scaffold.py` 通过，验证 recall 仅消费 accepted memory、长时记忆进入 context segment、第二次 session 可召回第一次 session 的 app memory。
- 2026-04-14：补齐 `MemorySummarizerPort`、`MemoryDatasetStorePort` 和 `MemoryDistillationSample`，默认 `null summarizer` 不依赖 LLM，但已具备候选草案和训练样本落盘接口。
- 2026-04-14：默认容器新增 `JSONL-backed` memory/evidence/dataset store；跨容器实例可保留记忆并继续 recall。
- 2026-04-14：promotion gate 已抽离为 `MemoryPromotionPolicy`，当前支持 kind 级 confidence threshold、allowed scope 和 draft kinds。
- 2026-04-14：新增 `LLMMemorySummarizer`，容器在显式配置 `memory_summarizer_provider/model` 时可使用真实 LLM runtime 生成候选草案。
- 2026-04-14：`LLMMemorySummarizer` 已收紧输出契约，只接受 `title/body` 作为 candidate draft schema；`kind/scope/confidence` 由运行时控制，默认忽略模型 override。
- 2026-04-14：promotion policy 已支持通过 settings / env 外置化；容器可按配置构建 `MemoryPromotionPolicy`。
- 2026-04-14：记忆蒸馏链已完成幂等化：同一 session 重复 distill 时，evidence、memory record 和 dataset sample 不再重复脏写。
- 2026-04-14：`v1` 记忆系统主闭环已完成并通过仓库全量 `uv run pytest` 回归。

## 下一步建议

- 检查任务人天估算是否真实合理，仅在必要时再细化到 0.5 人天精度
- 若进入设计或实施阶段，先确认 `docs/04-project-development/04-design/technical-selection.md` 已明确框架、模块、后台范围和编码规则
- 下一轮基础设施实现优先把 Hermes-backed `CapabilityRegistryPort` 从 wrapper scaffold 推进到真实 `tools/registry.py` / `model_tools.py` 桥接，再补 gateway session context 与 approval state bridge
- 继续推进 `REQ-006` 时，优先把当前 in-memory 实现扩成可插拔 persistence adapter，而不是把记忆逻辑再塞回 `Context Builder`
- 下一轮优先补 `SessionAssemblyManifest`、`ProfileResolverPort`、`WorkspaceRuleBundlePort` 和 `SkillCatalogPort`，先把 profile / 项目规则 / skill / child digest 装配治理做成一等对象
- 下一轮优先移除静态 `project_scope_key` 口径，并补 `MemoryAssemblyQueryPort` / `SessionAssemblyStorePort` / `SessionArchiveQueryPort`，先解决可解释性、历史回查和多 profile 扩展性
- 下一轮优先补 `MemoryProviderPort` 与 `provider_manager`，先明确 built-in local store 与 single external provider 的增强边界
- 下一轮优先补更细粒度的 promotion policy、样本筛选规则和真实 LLM summarizer adapter，而不是直接训练专用模型
- 下一轮优先补 LLM summarizer 输出 schema 约束、policy 配置外置化和 dataset 去重/筛选规则，而不是直接训练专用模型
- 下一轮优先补 policy 配置外置化、dataset 去重/筛选规则和真实 provider 的结构化输出校验，而不是直接训练专用模型
- `v1` 记忆系统主闭环已完成；后续优先转入增强项，如 recall ranker、policy 管理界面、dataset 审核工作流
- 若 UX/UI 需要可视化评审，优先登记真实设计交付物而不是只写文字
- 若工作项进入收尾，确认关联 PR 已完成评审并合并
- 阶段切换前先更新正式文档，再刷新 `/.factory/memory/` 压缩记忆
- 2026-04-15：已把 `agent-platform-architecture.md`、`system-architecture.md`、`module-boundaries.md`、`architecture-layer-code-mapping.md`、`infrastructure-layer-design.md`、`memory-runtime-interfaces.md` 全部统一到单向依赖链口径：`access -> application -> domain -> runtime/basic-capability -> settings`。
- 2026-04-15：已明确“记忆业务 owner 在 `src/domain/memory/`，基础能力层只提供技术能力，基础设置层只负责接口实现与装配”，并新增 `src/access/ports/application_use_cases.py`、`src/application/ports/domain_services.py`、`src/domain/*/ports.py`、`src/runtime/ports/*.py` 作为正式接口骨架。

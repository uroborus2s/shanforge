# 架构摘要

- 更新时间：2026-04-15 16:30:00
- 当前版本线：`v2` / `0.2.0.dev0`
- 架构目标：建设面向业务装配的抽象 Agent 平台
- 主架构风格：DDD / Hexagonal Architecture
- 主设计文档：`docs/04-project-development/04-design/agent-platform-architecture.md`

## 核心结论

- 当前架构细化入口已切换到 `layered-domain-interface-catalog.md`：正式依赖链为 `access -> application -> domain -> runtime/basic-capability -> settings`。
- `04-design` 已重新梳理为“核心事实链 + 记忆专项 + 主题专项”三段结构，`solution-overview.md`、`backend-design.md`、`database-design.md`、`deployment-architecture.md`、`frontend-adapters-and-multi-agent-coordination.md`、`action-registry-and-autonomy-policy.md` 已按新架构口径重写。
- 业务逻辑 owner 已进一步收口为业务模型层；应用层只编排，基础能力层只提供通用能力，基础设置层只提供实现。
- 正式分层口径已统一为 6 层：用户界面层、接口/网关层、业务调度层、业务模型层、基础能力层、基础设置层。
- 用户界面层主要由仓外 Web 项目和外部 CLI 前台承担；当前仓库重点实现接口/网关层、业务调度层、业务模型层、基础能力层和基础设置层。
- 平台内核统一承载 workflow、model、capability、context、policy 和 response。
- 业务开发面向 Agent App、Workflow DSL 和 ModelPolicy，而不是底层命令或脚本。
- 大模型交互通过 `LLM Runtime + LLMProviderPort` 解耦。
- 记忆的业务 owner 已正式回收到 `src/domain/memory/`；任何关于 recall / distill / promotion / archive 的业务规则都不再放在基础能力层 owner 位置。
- 记忆被正式定义为由事件和 evidence 蒸馏出的二级资产，不能覆盖第一事实源。
- 记忆蒸馏首版采用“规则治理 + 选择性 LLM 候选生成 + 样本沉淀”的混合流水线，训练化留到后续阶段。
- 首个最小垂直切片已经落地：`ExecutionService` 先 recall 再执行 workflow，session 完成后触发 distill + promotion，并由 `ContextEngine` 把 recalled memory 编译为 `LONG_TERM_MEMORY` segment。
- 当前实现已补到第二个切片：默认容器支持 `in-memory / JSONL-backed` 双持久层，记忆蒸馏主链会把 `candidate -> decision` 写入 dataset store，并为后续 LLM summarizer 保留独立 port。
- 当前实现已补到第三个切片：promotion gate 由独立 `MemoryPromotionPolicy` 负责，容器可选接入 `LLMMemorySummarizer` 通过现有 `LLMRuntime` 生成候选草案。
- 当前实现已补到第四个切片：LLM summarizer 的 candidate 输出 schema 已收紧为 `title/body` 必填，运行时不再信任模型对 `kind/scope/confidence` 的覆盖。
- 当前实现已补到第五个切片：promotion policy 可从 settings / env 外置，distill 已对 evidence / memory record / dataset sample 做幂等去重。
- 新增业务驱动详细设计后，记忆领域被进一步明确为“装配平面 + 记忆平面 + 档案查询面”三面协作：前者负责 profile、项目规则、skill、child digest 装配，中间负责 recall、promotion、dataset 和 decay 治理，后者负责历史回查与 explainability。
- 记忆系统的下一阶段重点不再是继续堆叠 recall 算法，而是补 `SessionAssemblyManifest`、`ProfileResolverPort`、`WorkspaceRuleBundlePort`、`SkillCatalogPort` 与 explainability 读模型。
- 吸收 Hermes Agent 后，记忆系统进一步明确为“装配平面 + 记忆平面 + 档案查询面”三面协作：历史会话回查必须走独立 `SessionArchiveQueryPort`，不能借道长期记忆 store。
- Hermes 的 `MemoryManager + MemoryProvider + bounded built-in memory` 被确认适合作为 shanforge 的增强 provider 组织方式，但 built-in local evidence / memory stores 仍是第一事实源。
- 下一阶段除装配治理外，还应补 `MemoryProviderPort`、`provider_manager`、`AssemblySnapshotPolicy` 与 child-isolated memory policy。
- 基础能力层正式承载文件、存储、检索、向量、模型、规则源、技能源、profile 源、审批通道、委派通道等统一技术能力。
- 基础能力层现已补齐单独的详细设计：正式按“共享底座 + 直接桥接能力包 + 可选扩展能力包 + 只借鉴架构项”组织，而不再只停留在技术域名词层。
- 基础能力层路线已从 `B` 切到 `C`：第一批能力仍是 `file`、`web`、`terminal`、`browser`、`session_search`、`skills_list/skill_view/skill_manage`，但现在明确改为“自研骨架先行，具体函数实现阶段再复用 Hermes”。
- `browser_providers`、`tools/environments`、`plugins/memory`、MCP 动态适配和 `gateway/platforms` 路由已明确为只借鉴架构，不直接搬入基础能力层。
- 基础设置层现已统一收口到 `src/settings/`；层内按 `model / memory / session / skills / workspace / approval / delegation / gateway / capability_registry / hermes` 等实现领域组织，`composition / shared` 作为层内支撑模块。
- 基础设置层可以实现 `domain-owned` 持久化端口与 `runtime-owned` provider 接口，但这些接口的 owner 仍属于上层消费者。
- 对上服务界面已明确分成四类：access 拥有应用用例接口，application 拥有领域服务接口，domain 拥有基础能力接口，runtime 拥有 provider 接口；基础设置层只负责实现，不拥有接口。
- draw.io 架构视图的关键标签也已同步改为“基础能力层”“domain-owned 持久化端口 + runtime-owned provider 接口”等正式术语，不再保留旧的“平台核心能力层”或错误的接口实现归属。
- Hermes 复用策略已收紧为“只在基础设置层实现区复用”，执行顺序固定为“封装复用 > 选择性迁入 > 新写实现”。
- 基础能力层开发顺序已收口为：`统一信封与上下文 -> 能力包目录与类型骨架 -> 读平面函数签名 -> 行动平面函数签名 -> 具体函数实现(可复用 Hermes) -> 可选能力试验 -> 回归测试`。
- `src/runtime/` 已新增第一批基础能力层骨架：`file_access`、`web_access`、`terminal`、`browser`、`session_search`、`skills`、`rule_source`、`profile_source`、`clock_identity`，并补齐统一 `CapabilityInvocationContext` / `CapabilityResourceEnvelope`。
- 首轮基础设置实现骨架已落地：`domain/approval`、`domain/delegation`、`domain/gateway` 和对应 `ApprovalPolicyPort`、`SandboxPolicyPort`、`DelegationTransportPort`、`GatewayPort` 已进入源码；默认容器已支持切换到 Hermes-backed capability/approval/delegation scaffold。
- `Context Builder` 被正式定义为平台级 `Context Engine` 核心，采用 `ContextRequest -> ContextSegment -> ContextEnvelope` 的预算驱动装配模型。
- 首版 step 级 `Context Builder` 已落地到运行时，`AgentKernel` 会在每个 workflow step 前重新编译上下文。
- 子 Agent 被正式定义为“独立 session + 独立上下文包 + 独立预算 + 独立能力边界 + 显式结果回传”的隔离执行单元。
- 遗留脚本、文件合同和外部系统只作为基础设置层实现存在。

## 当前追踪

- `REQ-001` ~ `REQ-010`
- `MOD-001` ~ `MOD-014`
- `API-001` ~ `API-013`

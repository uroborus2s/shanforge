# 实施计划

**项目名称：** 山海工枢 / shanforge
**文档状态：** `v2` 实施基线
**负责人：** 仓库维护者
**主要读者：** 项目协调者 | 架构 | 平台开发 | 测试
**上游输入：** PRD | 系统架构 | 模块边界 | API 设计
**下游输出：** 代码实现 | 测试报告 | 发布说明
**关联 ID：** `TASK-001` ~ `TASK-020`
**最后更新：** 2026-04-19

## 1. 实施策略

`v2` 的实施不再围绕旧流程整理和命令入口修补，而是按平台内核优先的顺序推进：

1. 先锁定领域模型、契约和用例
2. 再实现 workflow、模型和 capability 运行时
3. 基础能力层改用 `C` 纯自研重写路线，先完成能力包骨架、类型对象和函数签名
4. 再进入具体函数实现，并在实现阶段选择性复用 Hermes 的代码与行为
5. 再补审批、证据、委派和多入口适配
6. 最后交付 demo Agent App 与回归测试

## 2. 工作分解

| TASK | 内容 | 对应需求 | 交付物 |
|---|---|---|---|
| `TASK-001` | 领域模型与核心 ID 体系 | `REQ-001`, `REQ-002` | Domain model、基础类型、状态对象 |
| `TASK-002` | Agent App Manifest schema 与 loader | `REQ-002`, `REQ-010` | Manifest schema、loader、示例 app 骨架 |
| `TASK-003` | Workflow DSL schema 与 runtime skeleton | `REQ-003`, `REQ-010` | Workflow schema、step runner、状态机 |
| `TASK-004` | ModelPolicyResolver 与 MockModelProvider | `REQ-004`, `REQ-010` | Policy resolver、mock provider、fixture |
| `TASK-005` | LLM Runtime 与 provider adapters | `REQ-004` | 标准 request/response、provider adapters |
| `TASK-006` | Capability Registry 与 tool runtime | `REQ-005` | Capability schema、registry、executor |
| `TASK-007` | Session Ledger、Memory Runtime、Recall / Context Engine | `REQ-001`, `REQ-006` | session ledger、memory API、规则化 extraction、LLM candidate pipeline、recall/promotion pipeline、context compiler |
| `TASK-008` | Policy / Approval / Execution Sandbox | `REQ-007` | Approval decision、sandbox port、risk gates |
| `TASK-009` | Response Normalizer、Parser、Schema Validator | `REQ-009` | 标准 AgentResponse 通道 |
| `TASK-010` | Delegation Runtime 与 Gateway 边界 | `REQ-008` | Worker contract、gateway port、merge checks |
| `TASK-011` | Demo Agent Apps：编码流、写作流 | `REQ-003`, `REQ-010` | 两个示范业务 App |
| `TASK-012` | 契约测试、回归测试、文档收口 | `NFR-*` | 测试套件、测试报告、发布说明 |

## 2.1 基础能力层增量任务

| TASK | 内容 | 对应需求 | 交付物 | 估算（人天） |
|---|---|---|---|---|
| `TASK-013` | 基础能力层统一信封与模块骨架 | `REQ-004`, `REQ-005`, `REQ-006`, `REQ-008` | `CapabilityInvocationContext`、`CapabilityResourceEnvelope`、能力包目录、公共结果对象 | `1.0` |
| `TASK-014` | 文件 / 工作区 / 规则 / Profile / Skills 读平面框架 | `REQ-005`, `REQ-006`, `REQ-010` | `file_access`、`workspace_access`、`rule/profile source`、`skill catalog read` 的 `service / model / function signatures` | `1.5` |
| `TASK-015` | Web / Terminal / Browser 行动平面框架 | `REQ-005`, `REQ-007`, `REQ-008` | `web_access`、`terminal`、`browser` 的 `service / model / function signatures` 与治理接线点 | `2.0` |
| `TASK-016` | Session Search 与装配解释查询框架 | `REQ-006`, `REQ-008` | `SessionArchiveQueryPort`、`SessionTranscriptSlicePort`、`SessionAssemblyQueryPort` 对应读模型、inspection facade、`SessionAssemblyStorePort` 与默认容器接线 | `1.5` |
| `TASK-017` | 具体函数实现阶段（可复用 Hermes） | `REQ-004`, `REQ-005`, `REQ-007`, `REQ-008` | 在保持 `shanforge` 自研骨架不变的前提下，逐个实现 `file/web/terminal/browser/session_search/skills` 的函数逻辑 | `2.0` |
| `TASK-018` | `todo / clarify / cronjob / execute_code` 试验性设计与最小原型 | `REQ-003`, `REQ-005`, `REQ-008`, `REQ-010` | 试验文档、最小 workflow spike、正式纳管结论 | `1.0` |
| `TASK-019` | 基础能力层契约、集成与回归测试 | `NFR-001`, `NFR-002`, `NFR-003`, `NFR-004` | contract fixtures、function regression、sandbox / approval / audit regression | `1.5` |
| `TASK-020` | 外部 DI 技术库接入与容器收敛 | `REQ-004`, `REQ-005`, `REQ-008`, `REQ-010`, `NFR-001`, `NFR-002` | `shanforge-di` 接入、business-id 到实现映射、本地 business bindings、thin container、契约与安全测试 | `2.0` |

## 3. 阶段划分

### 阶段 A：核心契约

- `TASK-001` ~ `TASK-004`
- 输出：平台核心 schema、workflow skeleton、mock provider

### 阶段 B：运行时闭环与基础能力骨架

- `TASK-005` ~ `TASK-009`, `TASK-013`, `TASK-014`
- 输出：LLM、capability、memory recall、context、approval、response 主闭环，以及 file / skills / profile / rule 等基础能力骨架

### 阶段 C：行动能力与历史检索骨架

- `TASK-010`, `TASK-015`, `TASK-016`, `TASK-017`
- 输出：委派边界、多入口准备、web / terminal / browser 行动平面骨架、session search 查询平面骨架，以及首轮函数实现

### 阶段 D：扩展验证、质量与发布

- `TASK-011`, `TASK-012`, `TASK-018`, `TASK-019`, `TASK-020`
- 输出：示范业务流、可选能力试验结论、测试收口、外部 DI 技术库接入、本地 business bindings、文档同步、发布基线

## 3.1 记忆治理专项实施收口

`REQ-006` 当前已进入“治理 owner 进一步收口”的阶段。

由于这部分不会新增新的顶层 `TASK` 编号，而是细化并重组已有 `TASK-007`、`TASK-016`、`TASK-017`、`TASK-019`，现单独拆出：

- [记忆治理专项实施计划](./memory-governance-implementation-plan.md)

该专项的正式目标是：

- 把 recall / provider / lifecycle / explainability 的治理语义继续收口到 `domain.memory`
- 让 `runtime.memory` 的 planner / ranker / provider manager 进一步降格为执行器
- 建立独立于全仓 collect 的记忆治理专项回归

## 4. 里程碑

| 里程碑 | 完成条件 |
|---|---|
| `M1` 契约冻结 | `TASK-001` ~ `TASK-004` 完成并通过 schema 校验 |
| `M2` 主闭环与基础能力骨架可运行 | `TASK-005` ~ `TASK-009`、`TASK-013`、`TASK-014` 完成并可输出标准 `AgentResponse`，且读平面能力包类型与函数签名已冻结 |
| `M3` 行动平面与历史检索首轮实现成立 | `TASK-015` ~ `TASK-017` 完成，web / terminal / browser / session search 的函数骨架已完成，首轮实现可在治理闸门下运行 |
| `M4` 发布候选就绪 | `TASK-011`、`TASK-012`、`TASK-018`、`TASK-019`、`TASK-020` 完成，所有契约测试与回归测试通过 |

## 5. 风险与缓解

| 风险 | 缓解 |
|---|---|
| 契约先行导致实现停滞 | 每个阶段都要求最小可运行产物 |
| DSL 设计反复 | 先做最小 schema，再用 demo app 校验 |
| provider 适配复杂 | 先完成 mock provider，再接真实 provider |
| 记忆层膨胀或失真 | 先完成 session ledger 和二级资产蒸馏规则，再扩展外部 memory provider |
| 过早训练导致方向跑偏 | 先积累 candidate/decision 样本，再评估是否训练专项小模型 |
| Hermes 代码复用反向污染分层 | 坚持骨架先行，Hermes 只进入函数内部实现，不让 Hermes 对象或目录上浮 |
| browser / terminal 能力风险过高 | 强制经 `sandbox + approval + audit` 三件套，先做最小动作集 |
| session search 误伤长期记忆边界 | 历史会话查询只返回证据与引用，不直接写回长期记忆 |
| 外部 DI 技术库与本仓业务绑定层漂移 | `shanforge-di` 只承载技术内核，`src/settings/composition/` 只保留 business bindings 与 container；集成变更必须同步更新依赖、容器测试和正式设计 |

## 6. 版本记录

| 版本 | 日期 | 变更内容 |
|---|---|---|
| `v2.0` | 2026-04-13 | 重写实施计划，按平台内核和业务装配重新定义任务序列 |
| `v2.1` | 2026-04-14 | 将 `TASK-007` 收口为 `Session Ledger + Memory Runtime + Recall / Context Engine` |
| `v2.2` | 2026-04-15 | 增补基础能力层开发计划，明确 `TASK-013` ~ `TASK-019` 的自研骨架优先顺序 |
| `v2.3` | 2026-04-16 | 增补 `TASK-020`，正式纳入反射式装配框架与容器收敛计划 |
| `v2.4` | 2026-04-16 | 将 `TASK-020` 收口为 sibling `shanforge-di` 外部技术库接入 + 本地 business bindings 替换方案 |
| `v2.5` | 2026-04-16 | 记录 `web / terminal / browser` 首轮 local bridge 已落地，`TASK-015` / `TASK-017` 进入正式实现阶段 |
| `v2.6` | 2026-04-19 | 补记忆治理专项实施入口，明确 `TASK-007/016/017/019` 的治理收口顺序 |

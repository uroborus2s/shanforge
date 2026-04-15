# 实施计划

**项目名称：** 山海工枢 / shanforge
**文档状态：** `v2` 实施基线
**负责人：** 仓库维护者
**主要读者：** 项目协调者 | 架构 | 平台开发 | 测试
**上游输入：** PRD | 系统架构 | 模块边界 | API 设计
**下游输出：** 代码实现 | 测试报告 | 发布说明
**关联 ID：** `TASK-001` ~ `TASK-012`
**最后更新：** 2026-04-14

## 1. 实施策略

`v2` 的实施不再围绕旧流程整理和命令入口修补，而是按平台内核优先的顺序推进：

1. 先锁定领域模型、契约和用例
2. 再实现 workflow、模型和 capability 运行时
3. 再补审批、证据、委派和多入口适配
4. 最后交付 demo Agent App 与回归测试

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

## 3. 阶段划分

### 阶段 A：核心契约

- `TASK-001` ~ `TASK-004`
- 输出：平台核心 schema、workflow skeleton、mock provider

### 阶段 B：运行时闭环

- `TASK-005` ~ `TASK-009`
- 输出：LLM、capability、memory recall、context、approval、response 主闭环

### 阶段 C：扩展与业务验证

- `TASK-010` ~ `TASK-011`
- 输出：委派边界、多入口准备、示范业务流

### 阶段 D：质量与发布

- `TASK-012`
- 输出：测试收口、文档同步、发布基线

## 4. 里程碑

| 里程碑 | 完成条件 |
|---|---|
| `M1` 契约冻结 | `TASK-001` ~ `TASK-004` 完成并通过 schema 校验 |
| `M2` 主闭环可运行 | `TASK-005` ~ `TASK-009` 完成并可输出标准 `AgentResponse` |
| `M3` 业务装配成立 | 编码流和写作流 demo App 可运行 |
| `M4` 发布候选就绪 | 所有契约测试与回归测试通过 |

## 5. 风险与缓解

| 风险 | 缓解 |
|---|---|
| 契约先行导致实现停滞 | 每个阶段都要求最小可运行产物 |
| DSL 设计反复 | 先做最小 schema，再用 demo app 校验 |
| provider 适配复杂 | 先完成 mock provider，再接真实 provider |
| 记忆层膨胀或失真 | 先完成 session ledger 和二级资产蒸馏规则，再扩展外部 memory provider |
| 过早训练导致方向跑偏 | 先积累 candidate/decision 样本，再评估是否训练专项小模型 |

## 6. 版本记录

| 版本 | 日期 | 变更内容 |
|---|---|---|
| `v2.0` | 2026-04-13 | 重写实施计划，按平台内核和业务装配重新定义任务序列 |
| `v2.1` | 2026-04-14 | 将 `TASK-007` 收口为 `Session Ledger + Memory Runtime + Recall / Context Engine` |

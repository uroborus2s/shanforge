# 文档索引

## 1. 文档目标

集中登记 `v2` 平台正式文档、状态和关联编号。

## 2. 当前正式文档索引

| 文档路径 | 文档类型 | 主要读者 | 状态 | 关联编号 |
|---|---|---|---|---|
| `docs/04-project-development/02-discovery/hermes-agent-source-analysis-report.md` | 调研报告 | 产品、架构、平台开发 | 已确认 | `DISC-HERMES-001` |
| `docs/04-project-development/03-requirements/prd.md` | 产品需求文档 | 产品、架构、测试 | `v2` 基线 | `REQ-*`, `NFR-*` |
| `docs/04-project-development/03-requirements/requirements-analysis.md` | 需求分析 | 产品、架构、平台开发 | `v2` 基线 | `REQ-*` |
| `docs/04-project-development/03-requirements/requirements-verification.md` | 需求校验 | 项目协调者、测试 | `v2` 基线 | `REQ-*`, `NFR-*` |
| `docs/04-project-development/04-design/solution-overview.md` | 总体方案 | 架构、平台开发 | `v2` 基线 | `REQ-*` |
| `docs/04-project-development/04-design/technical-selection.md` | 技术选型 | 架构、平台开发、测试 | `v2` 基线 | `NFR-*` |
| `docs/04-project-development/04-design/system-architecture.md` | 系统架构 | 架构、平台开发 | `v2` 基线 | `REQ-*`, `ADR-*`, `MOD-*`, `API-*` |
| `docs/04-project-development/04-design/agent-platform-architecture.md` | 平台架构 | 架构、业务 Agent 开发 | `v2` 基线 | `REQ-*`, `MOD-*`, `API-*` |
| `docs/04-project-development/04-design/infrastructure-layer-design.md` | 基础设施层领域模型与服务接口设计 | 架构、平台开发、适配器维护者 | `v2` 基线 | `MOD-*`, `API-*` |
| `docs/04-project-development/04-design/memory-runtime-design.md` | 记忆专项设计 | 架构、平台开发、测试 | `v2` 基线 | `REQ-006`, `MOD-007`, `API-006`, `API-007` |
| `docs/04-project-development/04-design/memory-system-detailed-design.md` | 记忆系统详细设计方案 | 架构、平台开发、测试、运营协作者 | `v0.2` | `REQ-006`, `MOD-007`, `MOD-010`, `API-006`, `API-007`, `MEM-BIZ-*` |
| `docs/04-project-development/04-design/memory-runtime-interfaces.md` | 记忆系统对外界面 | 架构、平台开发、适配器维护者 | `v2` 基线 | `API-006`, `API-007` |
| `docs/04-project-development/04-design/memory-session-ledger-design.md` | 子设计：Session Ledger | 架构、平台开发 | `v2` 基线 | `MOD-010`, `API-007` |
| `docs/04-project-development/04-design/memory-promotion-design.md` | 子设计：Candidate 与 Promotion | 架构、平台开发 | `v2` 基线 | `MOD-007`, `API-007` |
| `docs/04-project-development/04-design/memory-recall-design.md` | 子设计：Recall 与 Context Consumption | 架构、平台开发、测试 | `v2` 基线 | `MOD-007`, `API-006` |
| `docs/04-project-development/04-design/memory-distillation-learning-design.md` | 子设计：Distillation 与 Learning Dataset | 架构、平台开发 | `v2` 基线 | `MOD-007` |
| `docs/04-project-development/04-design/module-boundaries.md` | 模块边界 | 架构、平台开发 | `v2` 基线 | `MOD-*` |
| `docs/04-project-development/04-design/api-design.md` | 接口契约 | 架构、平台开发、测试 | `v2` 基线 | `API-*` |
| `docs/04-project-development/05-development-process/implementation-plan.md` | 实施计划 | 项目协调者、平台开发 | `v2` 基线 | `TASK-*` |
| `docs/04-project-development/06-testing-verification/test-plan.md` | 测试计划 | QA、平台开发 | `v2` 基线 | `TC-*` |
| `docs/04-project-development/07-release-delivery/release-notes.md` | 发布说明 | 项目协调者、维护者 | `v2` 基线 | `REL-*` |
| `docs/04-project-development/10-traceability/requirements-matrix.md` | 需求矩阵 | 项目协调者、测试 | `v2` 基线 | `TRACE-*` |
| `docs/04-project-development/10-traceability/interface-matrix.md` | 接口矩阵 | 架构、测试 | `v2` 基线 | `API-*` |

## 3. 维护规则

- 新增平台正式文档时必须同步登记。
- 旧版本说明文档不再作为 `v2` 主文档索引的一部分。
- 索引状态变化必须与追踪矩阵同步。

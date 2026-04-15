# 需求追踪矩阵

**项目名称：** 山海工枢 / shanforge
**负责人：** 仓库维护者
**最后更新：** 2026-04-15

## 1. 需求到设计/实施/测试映射

| 需求 ID | 需求摘要 | 设计文档 | 模块 | 接口 | 任务 | 测试 | 状态 |
|---|---|---|---|---|---|---|---|
| `REQ-001` | 统一 Agent Platform Kernel | `system-architecture.md`, `agent-platform-architecture.md` | `MOD-002`, `MOD-003`, `MOD-010` | `API-007` | `TASK-001`, `TASK-007` | `TC-005`, Integration | 设计基线已建立 |
| `REQ-002` | 业务 Agent App 与平台内核隔离 | `prd.md`, `agent-platform-architecture.md`, `module-boundaries.md` | `MOD-001`, `MOD-002` | `API-001` | `TASK-001`, `TASK-002` | Manifest contract | 设计基线已建立 |
| `REQ-003` | Workflow DSL 与声明式编排 | `prd.md`, `agent-platform-architecture.md`, `api-design.md` | `MOD-004` | `API-002` | `TASK-003`, `TASK-011` | `TC-002`, `TC-008`, `TC-009` | 设计基线已建立 |
| `REQ-004` | 多模型策略与供应商解耦 | `system-architecture.md`, `api-design.md` | `MOD-005`, `MOD-012` | `API-003`, `API-004` | `TASK-004`, `TASK-005` | `TC-003` | 设计基线已建立 |
| `REQ-005` | Capability Registry 与工具执行契约 | `module-boundaries.md`, `api-design.md` | `MOD-006`, `MOD-012` | `API-005`, `API-009`, `API-013` | `TASK-006` | `TC-004` | 设计基线已建立 |
| `REQ-006` | Session、Memory 与 Context Engine | `system-architecture.md`, `agent-platform-architecture.md`, `memory-runtime-design.md`, `memory-system-detailed-design.md` | `MOD-007`, `MOD-010` | `API-006`, `API-007` | `TASK-007` | `TC-005` | 设计基线已建立，已补业务驱动详细设计 |
| `REQ-007` | Policy、Approval 与 Execution Sandbox | `system-architecture.md`, `api-design.md` | `MOD-008`, `MOD-012` | `API-008`, `API-009` | `TASK-008` | Policy / sandbox tests | 设计基线已建立 |
| `REQ-008` | Delegation、Gateway 与多入口适配 | `system-architecture.md`, `module-boundaries.md`, `api-design.md` | `MOD-009`, `MOD-011` | `API-010`, `API-012` | `TASK-010` | `TC-007` | 规划中 |
| `REQ-009` | 标准化 AgentResponse 与 Evidence | `agent-platform-architecture.md`, `api-design.md` | `MOD-014`, `MOD-010` | `API-011` | `TASK-009` | `TC-006` | 设计基线已建立 |
| `REQ-010` | 快速构建业务工作流 | `prd.md`, `implementation-plan.md`, `test-plan.md` | `MOD-001`, `MOD-004`, `MOD-005` | `API-001`, `API-002`, `API-003` | `TASK-002`, `TASK-003`, `TASK-011`, `TASK-012` | `TC-008`, `TC-009` | 设计基线已建立 |

## 2. 非功能需求映射

| NFR ID | 要求 | 设计落点 | 验证方式 |
|---|---|---|---|
| `NFR-001` | 可扩展性 | `system-architecture.md`, `module-boundaries.md` | 适配器替换测试 |
| `NFR-002` | 可审计性 | `agent-platform-architecture.md`, `test-plan.md` | 事件与 evidence 回放 |
| `NFR-003` | 可测试性 | `api-design.md`, `test-plan.md` | contract tests + mock provider |
| `NFR-004` | 隔离性 | `module-boundaries.md` | import boundary review |
| `NFR-005` | 成本与隐私控制 | `prd.md`, `api-design.md` | model policy tests |

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

## 4. 版本记录

| 版本 | 日期 | 变更内容 |
|---|---|---|
| `v2.0` | 2026-04-13 | 重写需求矩阵，建立纯 `v2` 需求、接口、任务和测试映射 |
| `v2.1` | 2026-04-15 | 为 `REQ-006` 补充 `memory-system-detailed-design.md` 的设计追踪 |

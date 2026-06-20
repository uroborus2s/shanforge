# 后端设计文档

**项目名称：** 山海工枢 / shanforge  
**文档状态：** `v2` 后端分层基线  
**负责人：** 仓库维护者  
**主要读者：** 架构 | 平台开发 | 测试 | 运维  
**上游输入：** 系统架构 | 平台架构设计 | 模块边界 | API 设计  
**下游输出：** 实现计划 | 测试计划 | 契约测试  
**最后更新：** 2026-04-15

## 1. 文档目标

说明 `shanforge` 当前仓内后端如何按六层架构组织网关、用例编排、领域逻辑、技术能力和设置实现。

这里的“后端”不再指旧脚本集合，而是指本仓承载的 5 个仓内层次：

- 接口/网关层
- 业务调度层
- 业务模型层
- 基础能力层
- 基础设置层

## 2. 后端总体结构

| 层 | 当前代码落点 | 主要职责 |
|---|---|---|
| 接口/网关层 | `src/access/` | API、CLI、HTTP、MCP、Chat、Automation 入口收口 |
| 业务调度层 | `src/application/` | 打开 session、选择 workflow、组织一次完整执行 |
| 业务模型层 | `src/domain/` | workflow、memory、capability、approval、delegation、response 等业务规则 |
| 基础能力层 | `src/runtime/` | Context Engine、LLM Runtime、Capability Registry、Approval/Sandbox、Delegation 等技术能力 |
| 基础设置层 | `src/settings/` | provider、持久化、Hermes bridge、容器装配 |

正式边界：

- `application` 只做薄编排。
- `domain` 是业务逻辑 owner。
- `runtime` 只提供通用技术能力。
- `src/settings/` 只负责实现和接线；层内分域不改变六层架构。

## 3. 主执行链

当前正式主链已经明确为：

```text
RuntimeAPI / CLI Gateway
  -> ExecutionService
  -> SessionDomainService + MemoryDomainService + WorkflowDomainService
  -> AgentKernel
  -> ContextEngine + ExecutionEngine + LLMRuntime / CapabilityRegistry / Approval / Delegation
  -> settings implementations
```

对应到代码：

| 环节 | 代码位置 | 说明 |
|---|---|---|
| 网关入口 | `src/access/api/`, `src/access/cli/`, `src/access/http/`, `src/access/mcp/`, `src/access/chat/`, `src/access/automation/` | 绑定协议、归一化请求 |
| 应用用例 | `src/access/ports/application_use_cases.py` | access 定义它依赖的应用接口 |
| 执行编排 | `src/application/execution/service.py` | `prepare -> run -> complete -> distill -> persist` 主链 |
| 领域服务接口 | `src/application/ports/domain_services.py` | application 定义它依赖的领域服务 |
| 领域实现 | `src/domain/*/service.py` | 业务语义 owner |
| 内核与运行时 | `src/runtime/agent_kernel/`, `src/runtime/context/`, `src/runtime/capability/`, `src/runtime/llm/`, `src/runtime/approval/`, `src/runtime/delegation/` | 技术能力编排 |
| 持久化与 provider | `src/settings/**`, `src/settings/composition/{component_bindings.py,container.py}`, sibling `shanforge-di` | 真实实现、本地业务绑定和装配 |

## 4. 关键专题链路

### 4.1 记忆链路

```text
ExecutionService
  -> MemoryDomainService
  -> domain/memory ports
  -> runtime/store/search/source capability
  -> settings/session + settings/memory
```

正式结论：

- `domain/memory` 是业务 owner。
- `runtime/memory` 只是基础能力层中的技术模块或兼容实现，不再是正式主链 owner。
- `storage/*` 只保存事实和派生资产，不决定业务语义。

### 4.2 能力执行链路

```text
gateway request
  -> ExecutionService / AgentKernel
  -> domain/capability
  -> runtime/capability executor + approval/sandbox
  -> settings-backed capability registry / tool backends
```

能力执行的治理规则由 `domain/capability`、`domain/approval` 和 `domain/delegation` 定义；真正的执行资源由 `runtime` 和 `settings` 提供。

### 4.3 模型调用链路

```text
step model policy
  -> domain/model
  -> runtime/llm runtime
  -> settings/model/*
```

模型策略归 `domain/model` owner，供应商差异只允许留在基础设置层。

## 5. 错误处理与状态管理

当前后端遵循“错误标准化、状态显式化、证据可追溯”三条规则：

- gateway 只返回结构化失败，不向上泄漏 SDK 原始异常。
- session 生命周期必须显式经历 `open / complete / fail / persist`。
- approval、sandbox、delegation 和 response 都应有独立领域语义，而不是散落在 runtime 细节里。
- 关键执行步骤必须留下 `session event / evidence / artifact / memory candidate`。

## 6. 当前实现状态

当前已经明确落地的部分：

- `ExecutionService` 保持薄编排，只依赖领域服务和 `AgentKernelPort`。
- `src/access/ports/application_use_cases.py`、`src/application/ports/domain_services.py`、`src/domain/*/ports.py`、`src/runtime/ports/*.py` 已形成四级接口 owner 结构。
- 默认容器已支持 `in-memory`、`JSONL-backed` 和 Hermes-backed scaffold 的组合装配。
- `tests/test_application_execution.py` 已覆盖“应用层只做薄编排”的核心事实。

当前仍需继续补齐的部分：

- `session_application`、`memory_application`、`approval_application` 等更细粒度应用层模块还需要从 `application/` 根下继续拆清。
- access 层已有 `chat/http/mcp/automation` 目录，但网关契约和读接口还需要继续补齐。
- hosted / external database / archive query 等场景仍在基础设置层和记忆专项中继续细化。

## 7. 关联文档

- [系统架构设计](./system-architecture.md)
- [分层领域与接口总表](./layered-domain-interface-catalog.md)
- [架构分层与代码映射说明](./architecture-layer-code-mapping.md)
- [基础设置层与外部资源设计](./infrastructure-layer-design.md)
- [记忆系统详细设计方案](./memory-system-detailed-design.md)

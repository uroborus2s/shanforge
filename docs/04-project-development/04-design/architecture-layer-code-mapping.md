# 架构分层与代码映射说明

本文只回答 5 个问题：

1. 六层架构在代码中怎么落位
2. `ports` 到底属于哪一层
3. `adapters / storage / bootstrap` 为什么不是额外层
4. 当前代码如何映射到正式架构
5. 领域接口和 provider 接口如何在代码里落位

---

## 1. 正式分层口径

本项目的正式架构层只有 6 个：

1. 用户界面层
2. 接口 / 网关层
3. 业务调度层
4. 业务模型层
5. 基础能力层
6. 基础设置层

额外说明：

- 用户界面层主要由仓外 Web 项目和外部 CLI 前台承担。
- 当前仓库不实现完整 UI，但实现接口 / 网关层中的 API 接口与 CLI 命令网关。

---

## 2. 层到代码目录的映射

| 架构层 | 代码或宿主 | 作用 |
|---|---|---|
| 用户界面层 | 仓外 Web 项目、外部 CLI 前台 | 最终人机交互 |
| 接口 / 网关层 | `src/access/` | 收口 API、CLI、HTTP、MCP 等入口 |
| 业务调度层 | `src/application/` | 编排 session 和 use case |
| 业务模型层 | `src/domain/` | 定义稳定领域模型、契约和规则 |
| 基础能力层 | `src/runtime/` | 提供文件、存储、检索、向量、模型、规则源、技能源等统一能力 |
| 基础设置层 | `src/adapters/` + `src/storage/` + `src/bootstrap/` | 提供 provider、store、外部系统桥接与装配 |

一句话压缩：

```text
src/access / src/application / src/domain / src/runtime 对应 4 个仓内主层，
src/adapters / src/storage / src/bootstrap 共同组成基础设置层实现区。
```

---

## 3. `port` 到底是什么

`port` 不是适配器本身，而是消费者定义的向下依赖接口。

正确关系是：

1. 先确定消费者属于哪一层。
2. 由这个消费者定义自己需要的接口。
3. 下层按该接口实现。
4. 基础设置层负责把真实实现装上去。

例如：

- 接口 / 网关层依赖应用用例，所以在 `src/access/ports/application_use_cases.py` 定义 `RuntimeExecutionUseCase` 等接口。
- 业务调度层依赖领域服务，所以在 `src/application/ports/domain_services.py` 定义 `MemoryDomainService`、`WorkflowDomainService` 等接口。
- 业务模型层依赖基础能力，所以在 `src/domain/memory/ports.py`、`src/domain/capability/ports.py` 等文件里定义领域下行接口。
- 基础能力层依赖基础设置 provider，所以在 `src/runtime/ports/*.py` 定义 `LLMProviderPort`、`StructuredStoreProviderPort`、`RuleSourceProviderPort` 等接口。

结论：

- `ports` 跟着消费者走。
- `ports` 不是独立层。

---

## 4. 为什么 `adapters / storage / bootstrap` 不是额外层

这是当前重构后的正式结论。

### 4.1 `src/adapters/`

负责：

- 对接模型供应商
- 对接外部系统
- 做 Hermes bridge 或其他反腐适配

它属于基础设置层中的“外部系统实现分区”。

### 4.2 `src/storage/`

负责：

- 提供 JSONL、数据库、索引、blob 等资源实现

它属于基础设置层中的“持久化资源分区”。

### 4.3 `src/bootstrap/`

负责：

- 读取 settings
- 选择实现
- 进行依赖装配

它属于基础设置层中的“装配与启动分区”。

所以：

```text
adapters / storage / bootstrap 是基础设置层的 3 个实现分区，
不是系统架构中的第 7、8、9 层。
```

---

## 5. 当前目标骨架

```text
src/
  access/
    api/
    cli/
    ports/

  application/
    app_compilation/
    execution/
    session/
    workflow_resolution/
    ports/

  domain/
    agent_app/
    workflow/
    session/
    memory/
    model/
    capability/
    approval/
    delegation/
    context/
    response/

  runtime/
    llm/
    ports/

  adapters/
    ...

  storage/
    ...

  bootstrap/
    ...
```

---

## 6. 当前真实代码映射

| 架构层 | 模块 | 真实代码位置 | 说明 |
|---|---|---|---|
| 接口 / 网关层 | API 门面 | `src/access/api/` | `app_api.py`、`runtime_api.py`、`workflow_api.py` |
| 接口 / 网关层 | CLI 命令网关 | `src/access/cli/` | `main.py`、`commands/run_demo.py` |
| 接口 / 网关层 | 应用用例接口 | `src/access/ports/application_use_cases.py` | `RuntimeExecutionUseCase`、`MemoryInspectionUseCase` 等 |
| 业务调度层 | App 编译 | `src/application/app_compilation/` | manifest -> app |
| 业务调度层 | Workflow 解析 | `src/application/workflow_resolution/` | 选择实际 workflow |
| 业务调度层 | 执行编排 | `src/application/execution/` | `ExecutionService` |
| 业务调度层 | 领域服务接口 | `src/application/ports/domain_services.py` | `MemoryDomainService`、`CapabilityDomainService` 等 |
| 业务模型层 | App / Workflow | `src/domain/agent_app/`、`src/domain/workflow/` | 业务声明与流程模型 |
| 业务模型层 | Session / Memory | `src/domain/session/`、`src/domain/memory/` | 会话、事件、证据、记忆规则 |
| 业务模型层 | Context / Model / Capability | `src/domain/context/`、`src/domain/model/`、`src/domain/capability/` | 上下文、模型策略、能力语义 |
| 业务模型层 | 下行能力接口 | `src/domain/*/ports.py` | 领域向基础能力层声明需要什么 |
| 基础能力层 | Provider 能力接口 | `src/runtime/ports/` | `LLMProviderPort`、`StructuredStoreProviderPort`、`RuleSourceProviderPort` 等 |
| 基础设置层 | 外部 provider | `src/adapters/` | SDK、外部系统、桥接实现 |
| 基础设置层 | 持久化资源 | `src/storage/` | JSONL、DB、索引、blob 等实现 |
| 基础设置层 | 装配与设置 | `src/bootstrap/` | settings、container、binding |

---

## 7. 业务调度层为什么必须保持薄

以 `src/application/execution/service.py` 为例，当前正式职责应该保持为：

- 把 manifest 编译成 app
- 解析 workflow
- 调用 `SessionDomainService.open_session(...)` 创建 session
- 调用 `MemoryDomainService.prepare_session(...)`
- 调用内核完成执行
- 调用 `SessionDomainService.attach_artifacts(...)`
- 调用 `SessionDomainService.complete_session(...)`
- 调用 `MemoryDomainService.distill_session(...)`
- 调用 `SessionDomainService.persist_session(...)`
- 汇总并返回结果

它不应该做的事：

- 直接访问 provider SDK
- 直接访问 JSONL / SQLite / 数据库驱动
- 直接决定 recall 算法和 promotion 细节
- 直接管理 gateway / approval / sandbox 规则

---

## 8. 记忆领域如何按六层落地

| 层 | 记忆领域落点 | 说明 |
|---|---|---|
| 接口 / 网关层 | `src/access/ports/application_use_cases.py` | `MemoryInspectionUseCase` 作为读入口 |
| 业务调度层 | `src/application/ports/domain_services.py` + `ExecutionService` | 调用 `MemoryDomainService` |
| 业务模型层 | `src/domain/memory/` + `src/domain/memory/ports.py` | 记忆模型与下行能力契约 owner |
| 基础能力层 | `src/runtime/ports/data_access.py`、`source_backends.py`、`ai_backends.py` | 为记忆领域提供检索、规则、技能、profile、embedding 等能力 |
| 基础设置层 | `src/storage/`、`src/adapters/`、`src/bootstrap/` | 实现文件、DB、索引、provider 和装配 |

结论：

- 记忆业务逻辑 owner 在 `src/domain/memory/`。
- 基础能力层只提供它调用的技术能力。
- 基础设置层只提供这些技术能力背后的真实实现。

---

## 9. 模型与能力领域如何按六层落地

### 9.1 模型网关

| 层 | 落点 |
|---|---|
| 业务模型层 | `src/domain/model/`、`src/domain/agent_app/policies.py` |
| 基础能力层 | `src/runtime/ports/llm_provider.py`、`src/runtime/ports/ai_backends.py` |
| 基础设置层 | `src/adapters/model_providers/`、`src/bootstrap/` |

### 9.2 能力系统

| 层 | 落点 |
|---|---|
| 业务模型层 | `src/domain/capability/` |
| 基础能力层 | `src/runtime/ports/execution_backends.py`、`src/runtime/ports/data_access.py` |
| 基础设置层 | `src/adapters/`、`src/bootstrap/` |

---

## 10. 一句话定稿

当前正式代码映射只有这一套：

- `src/access` = 接口 / 网关层
- `src/application` = 业务调度层
- `src/domain` = 业务模型层
- `src/runtime` = 基础能力层
- `src/adapters + src/storage + src/bootstrap` = 基础设置层实现区

补充约束：

- 旧版独立 `memory_system.py` 等接口口径已经废弃；正式 owner 统一收口到 `application/ports/domain_services.py` 与 `domain/*/ports.py`。
- 后续所有架构图、接口表和实现说明都必须沿用这套映射，不再把 `ports`、`adapters`、`storage`、`bootstrap` 写成额外架构层。

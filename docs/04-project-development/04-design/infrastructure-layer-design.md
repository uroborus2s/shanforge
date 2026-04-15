# 基础设置层与外部资源设计

**项目名称：** 山海工枢 / shanforge  
**文档状态：** `v2` 基础设置层详细设计基线  
**负责人：** 仓库维护者  
**主要读者：** 架构 | 平台开发 | 适配器维护者 | 测试  
**上游输入：** PRD | 需求分析 | 系统架构 | 模块边界 | 核心领域与能力清单  
**下游输出：** 端口实现 | 适配器实现 | 契约测试 | 实施计划  
**关联 ID：** `REQ-001`, `REQ-004`, `REQ-005`, `REQ-006`, `REQ-007`, `REQ-008`, `NFR-001`, `NFR-002`, `NFR-003`, `NFR-004`, `MOD-005`, `MOD-006`, `MOD-007`, `MOD-008`, `MOD-009`, `MOD-010`, `MOD-012`, `MOD-013`, `API-004`, `API-006`, `API-007`, `API-008`, `API-009`, `API-010`, `API-012`, `API-013`  
**最后更新：** 2026-04-15

## 1. 目标

本文件只回答 4 个问题：

1. 六层架构里的“基础设置层”到底是什么。
2. 它和“基础能力层”如何明确分开。
3. 当前代码里哪些目录属于基础设置层。
4. 基础设置层应该如何实现上层 provider 接口，并优先复用 Hermes 的成熟实现。

## 2. 正式定义

基础设置层是平台对真实资源、真实系统和真实装配方式的统一实现区。

这里的“设置”不是指业务参数，而是指：

- 文件系统与工作区资源
- 本地持久化与外部数据库
- 模型供应商 SDK 与远程服务
- 远程或遗留外部系统
- 容器装配、实现切换和运行配置

因此，基础设置层不等于基础能力层。

### 2.1 基础能力层和基础设置层的分工

| 层 | 回答的问题 | 当前代码 |
|---|---|---|
| 基础能力层 | “平台对上提供什么统一技术能力” | `src/runtime/` |
| 基础设置层 | “这些能力背后由什么真实资源和实现来支撑” | `src/adapters/` + `src/storage/` + `src/bootstrap/` |

正式定稿：

- 文件访问、结构化存储、检索、向量、模型调用、规则源、技能源、profile 源、审批通道、委派通道属于基础能力层。
- 文件系统、外部数据库、provider SDK、Hermes bridge、JSONL store、container 装配属于基础设置层。

## 3. 代码边界

基础设置层不是单一目录，而是 3 个实现分区共同组成：

| 分区 | 目录 | 作用 |
|---|---|---|
| 外部系统实现分区 | `src/adapters/` | provider、approval、delegation、workspace、legacy bridge |
| 持久化资源分区 | `src/storage/` | JSONL、DB、索引、blob 等资源实现 |
| 装配与配置分区 | `src/bootstrap/` | settings、container、runtime binding |

这 3 个分区都属于基础设置层，不是新增层次。

## 4. 设计原则

### 4.1 消费者拥有接口

基础设置层不能拥有上层接口，只能实现它们。

统一规则：

```text
上层声明需要什么；基础设置层负责满足它。
```

因此：

- 接口/网关层拥有应用用例接口，例如 `RuntimeExecutionUseCase`。
- 业务调度层拥有领域服务接口，例如 `MemoryDomainService`。
- 业务模型层拥有对基础能力层的下行接口，例如 `MemoryRecordRepositoryPort`、`CapabilityExecutionPort`。
- 基础能力层拥有对基础设置层的 provider 接口，例如 `LLMProviderPort`、`StructuredStoreProviderPort`、`RuleSourceProviderPort`。
- 基础设置层负责实现 domain-owned 持久化端口和 runtime-owned provider 接口，并完成最终装配。

### 4.2 不承载业务规则

基础设置层不能决定：

- workflow 如何编排
- memory 是否应该晋升
- approval 是否应该放行
- response 如何向业务解释

这些都属于业务调度层或业务模型层。

### 4.3 只返回领域契约或 provider 语义

基础设置层对上只能返回领域对象、协议对象和稳定错误语义，不能直接向上暴露：

- SDK 原始对象
- 数据库游标
- HTTP client 原始响应
- shell 内部执行细节

### 4.4 可替换实现

每个基础设置接口都应支持：

- 至少一个 `in-memory / local` 实现
- 至少一个真实外部或持久化实现

当前仓库已初步做到：

- `in-memory`
- `JSONL-backed`
- `Hermes-backed scaffold`

## 5. 基础设置层实现清单

### 5.1 模型供应商实现

| 能力 | 上层接口 | 当前实现 |
|---|---|---|
| 模型生成 | `LLMProviderPort` | `src/adapters/model_providers/mock_provider.py`、`openai_provider.py`、`anthropic_provider.py` |
| 向量生成 | `EmbeddingProviderPort` | `src/adapters/` 目标分区 |

这里的 provider adapter 属于基础设置层，因为它们封装的是具体 SDK 与供应商差异。

### 5.2 源数据与执行 backend 实现

| 能力 | 上层接口 | 当前实现 |
|---|---|---|
| 规则源 | `RuleSourceProviderPort` | `src/adapters/` 目标分区 |
| skill 源 | `SkillSourceProviderPort` | `src/adapters/` 目标分区 |
| profile 源 | `ProfileSourceProviderPort` | `src/adapters/` 目标分区 |
| 审批后端 | `ApprovalBackendPort` | `src/adapters/approval/` |
| 委派后端 | `DelegationBackendPort` | `src/adapters/delegation/` |
| workspace / shell / git / http | `WorkspaceProviderPort`、`ShellCommandProviderPort`、`GitProviderPort`、`HttpClientProviderPort` | `src/adapters/workspace/`、`src/adapters/legacy_bridge/` 及目标分区 |

### 5.3 持久化实现

| 能力 | 上层接口 | 当前实现 |
|---|---|---|
| 文件系统 | `FileSystemProviderPort` | `src/storage/` 或 `src/adapters/` 目标实现 |
| 结构化存储 | `StructuredStoreProviderPort` | `src/storage/` |
| blob 存储 | `BlobStoreProviderPort` | `src/storage/` 目标实现 |
| 搜索索引 | `SearchIndexProviderPort` | `src/storage/` 目标实现 |
| 向量索引 | `VectorIndexProviderPort` | `src/storage/` 目标实现 |

### 5.4 装配实现

| 能力 | 代码位置 | 作用 |
|---|---|---|
| runtime settings | `src/bootstrap/settings/runtime.py` | 读取环境配置与实现开关 |
| default container | `src/bootstrap/container/default.py` | 按配置装配基础能力层与基础设置层 |

## 6. 对上服务方式

基础设置层对上的正式服务对象只有一类：

| 服务对象 | 上层角色 | 例子 |
|---|---|---|
| 基础能力层 | 需要 provider、store、source、backend 等真实实现 | `LLMProviderPort`、`StructuredStoreProviderPort`、`RuleSourceProviderPort` |

注意：

- 业务调度层原则上不直接碰基础设置层。
- 业务模型层也不直接触碰基础设置实现。
- 所有真实资源都要先经过基础能力层的 provider 接口收口。

## 7. Hermes 复用策略

Hermes 的复用只允许发生在基础设置层实现区。

### 7.1 复用原则

- 先有 `shanforge` 自己的领域契约和端口。
- 再用 Hermes 的成熟模块去实现这些端口。
- 不能为了复用 Hermes 而反向改写本仓的层边界。

### 7.2 当前映射

| `shanforge` 目标 | 优先复用的 Hermes 位置 | 当前落点 |
|---|---|---|
| 规则 / skill / profile 源适配 | `gateway/session.py`、相关加载逻辑 | `src/adapters/` 目标分区 |
| 审批后端 | `tools/approval.py` | `src/adapters/approval/hermes_policy.py` |
| 委派后端 | `tools/delegate_tool.py` | `src/adapters/delegation/hermes_transport.py` |
| 外部桥接适配 | `gateway/platforms/base.py`、`gateway/session_context.py` | `src/adapters/legacy_bridge/`、`src/adapters/gateway/` |

### 7.3 明确禁止

禁止把 Hermes 的以下内容直接拉进上层：

- 顶层 agent loop
- 产品级 prompt 拼装
- Hermes 私有 session 协议
- 任何要求上层直接持有 Hermes 内部对象的路径

## 8. 下一批基础设置工作

下一轮基础设置层优先补齐：

- 外部数据库或更稳定本地持久化实现
- workspace / file / git / shell 的正式 bridge
- gateway 的真实多宿主适配
- Hermes-backed adapter 的契约测试
- 容器配置从“开关集合”升级为更稳定的 profile 化装配

## 9. 一句话定稿

基础设置层的正式定义是：

```text
为平台提供文件、数据库、provider、外部系统和装配实现的统一实现区。
```

当前代码中：

- `src/adapters/` 是外部系统实现分区
- `src/storage/` 是持久化资源分区
- `src/bootstrap/` 是装配与配置分区

三者共同组成基础设置层；它们只服务于基础能力层，不反向主导业务调度层和业务模型层。

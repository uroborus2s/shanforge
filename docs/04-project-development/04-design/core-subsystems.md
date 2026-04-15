# 核心领域与能力清单

**项目名称：** 山海工枢 / shanforge  
**文档状态：** `v2` 领域与能力基线  
**负责人：** 仓库维护者  
**主要读者：** 架构 | 平台开发 | 业务 Agent 开发 | 测试  
**上游输入：** 系统架构 | 平台架构设计 | 模块边界  
**下游输出：** 接口设计 | 代码骨架映射 | draw.io 架构图  
**最后更新：** 2026-04-15

## 1. 这份文档回答什么

本文件只回答两个问题：

1. 当前哪些领域是平台的核心业务领域
2. 当前哪些能力是基础能力层必须提供的核心通用能力

兼容说明：

- 文件名保留是为了兼容旧索引。
- 正式架构不再使用“跨层子系统 owner”这套口径。
- 本文件的正式语义是“核心领域与核心通用能力清单”。

## 2. 核心业务领域

这些领域属于业务模型层，是平台业务逻辑 owner：

| 领域 | 主要职责 | 主要接口文件 |
|---|---|---|
| `agent_app` | AgentApp、manifest、能力声明 | `src/domain/agent_app/ports.py` |
| `workflow` | workflow 定义、步骤规则、状态推进 | `src/domain/workflow/ports.py` |
| `session` | session 生命周期、ledger、artifact 归属 | `src/domain/session/ports.py` |
| `memory` | recall、distill、promotion、archive explainability | `src/domain/memory/ports.py` |
| `context` | 上下文组装、预算裁剪、segment 规划 | `src/domain/context/ports.py` |
| `model` | 模型策略、路由与预算规则 | `src/domain/model/ports.py` |
| `capability` | capability 声明、风险、输入输出语义 | `src/domain/capability/ports.py` |
| `approval` | 审批语义、permit 判定、审计语义 | `src/domain/approval/ports.py` |
| `delegation` | 子任务语义、结果汇总和写集约束 | `src/domain/delegation/ports.py` |
| `response` | 统一响应、证据、usage 与 artifact 归一化 | `src/domain/response/ports.py` |

## 3. 核心通用能力

这些能力属于基础能力层，不拥有平台业务逻辑，只为业务领域提供统一技术能力：

| 能力 | 作用 | 主要 provider 接口 |
|---|---|---|
| `file_access` | 文本、目录、路径资源访问 | `FileSystemProviderPort` |
| `structured_storage` | 结构化记录读写与查询 | `StructuredStoreProviderPort` |
| `blob_storage` | 附件或大对象读写 | `BlobStoreProviderPort` |
| `search_index` | 全文检索与结构化检索 | `SearchIndexProviderPort` |
| `vector_index` | 语义召回与向量查询 | `VectorIndexProviderPort` |
| `llm_gateway` | 文本生成与结构化生成 | `LLMProviderPort` |
| `embedding_gateway` | 向量化能力 | `EmbeddingProviderPort` |
| `tool_execution` | 通用工具调用 | `ToolExecutionProviderPort` |
| `workspace_access` | workspace 定位与访问 | `WorkspaceProviderPort` |
| `rule_source` | 规则源装载 | `RuleSourceProviderPort` |
| `skill_source` | skill 索引与正文装载 | `SkillSourceProviderPort` |
| `profile_source` | profile 解析与装载 | `ProfileSourceProviderPort` |
| `approval_channel` | 人工审批后端通道 | `ApprovalBackendPort` |
| `delegation_transport` | worker 派发与结果回收 | `DelegationBackendPort` |
| `shell_gateway` | shell 能力访问 | `ShellCommandProviderPort` |
| `git_gateway` | git 能力访问 | `GitProviderPort` |
| `http_gateway` | 对外 HTTP 调用 | `HttpClientProviderPort` |
| `clock_identity` | 时间和 ID 生成 | `ClockProviderPort`、`IdGeneratorProviderPort` |

## 4. 记忆领域的正式归属

记忆是业务模型层领域，不是基础能力层 owner。

正式链路如下：

| 层 | 记忆相关职责 |
|---|---|
| 接口/网关层 | 通过 `MemoryInspectionUseCase` 暴露查询入口 |
| 业务调度层 | 通过 `MemoryDomainService` 组织 prepare / recall / distill |
| 业务模型层 | 在 `src/domain/memory/` 中定义业务规则和下行能力需求 |
| 基础能力层 | 提供记忆领域调用的检索、规则、profile、skill、推理和存储能力 |
| 基础设置层 | 提供文件、数据库、索引和 provider 的真实实现 |

## 5. 一句话定稿

本项目只有一套正式表述：

- 业务逻辑 owner 在业务模型层。
- 通用技术能力在基础能力层。
- 真实资源实现和装配在基础设置层。
- 不再把任何领域描述成“跨层子系统 owner”。

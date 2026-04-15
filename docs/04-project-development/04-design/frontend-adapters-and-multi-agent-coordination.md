# 多前台适配与多代理协作设计

**文档状态：** `v2` 主题专项基线  
**主要读者：** 架构 | 平台维护者 | 集成开发者 | 协作负责人  
**负责人：** 仓库维护者  
**关联 ID：** `REQ-003`, `REQ-005`, `REQ-008`, `API-010`, `API-012`, `API-013`  
**最后更新：** 2026-04-15  

## 1. 设计目标

在六层架构下，平台需要同时满足两件事：

1. 能被多个前台宿主复用，而不把协议耦合进某个特定工具。
2. 能支持多代理协作，但不牺牲 session 隔离、写集治理和审批边界。

这份文档只回答：

- UI 宿主和 access 层之间的边界如何稳定
- 多代理协作如何在平台内建成正式能力，而不是临时并行

## 2. 多前台宿主模型

### 2.1 分层定位

| 层 | 当前形态 | 责任 |
|---|---|---|
| 用户界面层 | 仓外 Web、外部 CLI 前台、自动化宿主 | 人机交互、展示、输入组织 |
| 接口/网关层 | `src/access/api/`, `cli/`, `http/`, `mcp/`, `chat/`, `automation/` | 协议绑定、出入参归一化、统一入口 |
| 业务调度层以下 | `src/application/` 及下层 | 保持与宿主无关的稳定运行语义 |

正式原则：

- UI 宿主不直接碰 `domain`、`runtime`、`storage`。
- 所有宿主统一消费 access 层暴露的稳定网关契约。
- 宿主差异只允许存在于输入绑定、输出渲染和能力降级策略中。

### 2.2 当前宿主面

本仓已经预留或落地了 6 类接入面：

- `api`
- `cli`
- `http`
- `mcp`
- `chat`
- `automation`

它们都属于接口/网关层，不代表额外架构层。

## 3. 宿主契约

前台宿主统一消费下面这些应用用例接口：

| 契约 | 作用 |
|---|---|
| `RuntimeExecutionUseCase` | 发起运行请求 |
| `WorkflowDescriptionUseCase` | 查看 workflow 描述 |
| `SessionInspectionUseCase` | 查询 session、回放、诊断 |
| `MemoryInspectionUseCase` | recall / explainability 查询 |
| `CapabilityCatalogUseCase` | 查看 capability 目录与风险信息 |
| `PlatformHealthUseCase` | 健康与就绪性检查 |

对应文件：

- `src/access/ports/application_use_cases.py`

### 3.1 宿主最小能力

无论是 Web、CLI 还是自动化宿主，至少应支持：

- 发起结构化请求
- 接收结构化响应
- 报告失败原因
- 展示审批状态或阻塞原因

### 3.2 可选增强能力

根据宿主能力不同，可选支持：

- 流式输出
- 交互式审批
- 长会话压缩或上下文截断提示
- 子代理执行状态展示
- capability catalog 浏览和筛选

## 4. 多代理协作模型

### 4.1 正式定义

子代理不是“共享同一运行时对象的并行线程”，而是：

```text
独立 session + 独立上下文包 + 独立预算 + 独立能力边界 + 显式结果回传
```

这意味着：

- 子代理必须通过 `delegation` 语义被计划、派发、收集。
- 子代理默认不直接写入父级长期记忆。
- 子代理结果先以 `digest` 或结构化结果回传，再由父级决定是否吸收。

### 4.2 协作角色

逻辑上可拆成下列协作职责：

| 角色 | 主要职责 |
|---|---|
| `planner` | 规划、拆解、界定关键路径 |
| `explorer` | 收集事实、定位上下文缺口 |
| `worker` | 承担明确写集或模块边界 |
| `reviewer` | 独立做风险与回归审查 |
| `qa` | 验证行为、证据和测试结果 |

这些是协作语义，不意味着一定要落成固定 UI 身份。

### 4.3 冲突控制

多代理协作至少要满足：

- 写入 ownership 明确
- 高风险动作仍经过 approval / sandbox
- 子代理返回结果必须可追溯到 session 和 evidence
- 写集冲突优先升级为串行或重新拆分，而不是强行合并

## 5. 分层落点

| 能力 | owner 层 | 当前或目标代码落点 |
|---|---|---|
| 多前台网关契约 | 接口/网关层 | `src/access/ports/application_use_cases.py` |
| 运行/查询用例编排 | 业务调度层 | `src/application/` |
| 子任务语义、digest 合并规则 | 业务模型层 | `src/domain/delegation/`, `src/domain/session/` |
| 派发与回收技术能力 | 基础能力层 | `src/runtime/delegation/` |
| 具体 worker/backend 实现 | 基础设置层 | `src/adapters/delegation/` |

## 6. 当前状态与缺口

当前已具备的基础事实：

- `src/access/` 已按多入口宿主预留目录。
- `domain/delegation`、`runtime/delegation`、`adapters/delegation` 的主分层已建立。
- 当前主架构已经明确“子代理 = 独立 session + 显式结果回传”。

仍需继续补齐：

- 不同宿主的统一网关契约测试
- delegation ticket / digest / child session 的读模型
- 宿主侧对 approval、writeset、subagent 状态的更标准展示
- 多代理回放与 explainability 视图

## 7. 验收标准

- 同一类运行请求在不同宿主中映射到一致的 access 契约
- 前台能力不足时，系统能明确降级而不是假装支持
- 子代理结果具备 session、scope、证据和写集边界
- 多代理协作不绕过 approval、sandbox 和 memory 隔离规则

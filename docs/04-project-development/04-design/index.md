# 设计文档

本目录承载 `v2` 抽象 Agent 平台的正式设计约束。当前正式架构口径已经统一为：

- 六层结构：用户界面层、接口/网关层、业务调度层、业务模型层、基础能力层、基础设置层。
- 单向依赖链：`UI -> access -> application -> domain -> runtime/basic-capability -> settings`。
- 接口 owner 规则：谁调用下层，谁定义接口；基础设置层只实现，不拥有上层逻辑。
- 业务 owner 规则：平台业务逻辑统一收口到 `domain`；`runtime` 只提供通用技术能力；基础设置层统一收口到 `src/settings/`，层内再按实现领域分组。

## 1. 核心事实链

第一次进入 `04-design` 时，建议按下面顺序建立正式事实：

1. [总体方案与协作总览](./solution-overview.md)
2. [技术选型与工程规则](./technical-selection.md)
3. [系统架构设计](./system-architecture.md)
4. [抽象 Agent 平台架构](./agent-platform-architecture.md)
5. [分层领域与接口总表](./layered-domain-interface-catalog.md)
6. [模块边界文档](./module-boundaries.md)
7. [架构分层与代码映射说明](./architecture-layer-code-mapping.md)
8. [基础能力层详细设计](./basic-capability-layer-design.md)
9. [基础设置层与外部资源设计](./infrastructure-layer-design.md)
10. [核心领域与能力清单](./core-subsystems.md)
11. [API 设计文档](./api-design.md)

说明：

- `system-architecture.md` 负责回答“系统按什么层次组织”。
- `agent-platform-architecture.md` 负责回答“平台核心能力如何协作、Hermes 如何吸收”。
- `layered-domain-interface-catalog.md` 是当前唯一的“层 -> 领域 -> 接口 owner -> 下行依赖”细化入口。
- `basic-capability-layer-design.md` 负责回答“基础能力层有哪些完整能力包、哪些能力直桥 Hermes、开发顺序如何安排”。
- `infrastructure-layer-design.md` 负责回答“基础设置层如何通过 `src/settings/` 为这些能力包提供真实实现和桥接适配”。

## 2. 记忆系统专项

记忆相关专题已经统一到“`domain/memory` 业务 owner + `runtime` 技术能力 + `settings` 实现分区”的口径，建议按下面顺序阅读：

1. [记忆系统详细设计方案](./memory-system-detailed-design.md)
2. [记忆运行设计（文件名兼容保留）](./memory-runtime-design.md)
3. [记忆领域接口视图](./memory-runtime-interfaces.md)
4. [子设计一：Session Ledger](./memory-session-ledger-design.md)
5. [子设计二：Candidate 与 Promotion](./memory-promotion-design.md)
6. [子设计三：Recall 与 Context Consumption](./memory-recall-design.md)
7. [子设计四：Distillation 与 Learning Dataset](./memory-distillation-learning-design.md)

## 3. 主题专项

这些文档补充说明特定主题，但都必须服从上面的核心事实链：

1. [后端分层与运行链设计](./backend-design.md)
2. [数据与持久化设计（文件名兼容保留）](./database-design.md)
3. [多前台宿主与多代理协作设计](./frontend-adapters-and-multi-agent-coordination.md)
4. [能力注册与分级自治治理设计](./action-registry-and-autonomy-policy.md)
5. [部署与运行模式设计](./deployment-architecture.md)

## 4. 设计资产

需要查看分层图、模块清单或记忆跨层调用图时，优先使用这些可视化资产：

1. [draw.io 架构视图资产](./assets/v2-architecture-views.drawio)
2. [单页架构图清单](./assets/v2-architecture-pages/index.md)

图形资产只负责辅助理解，不覆盖 Markdown 正式口径。若图文冲突，以正文为准。

## 5. 使用规则

- 讨论架构时，先判断层，再判断领域，再判断接口 owner 和实现落点。
- 文件名中保留了少量兼容旧命名的路径，例如 `memory-runtime-design.md`、`database-design.md`；阅读时以文内“正式口径/兼容说明”为准，不按旧名字面理解。
- 任何设计结论都不得回退到“统一 ports 层”“跨层 owner”“基础设施层包打天下”这类旧表述。
- 设计变更后必须同步实施计划、测试计划、追踪矩阵和 `.factory/memory/` 摘要。

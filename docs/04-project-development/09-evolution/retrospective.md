# `v2` 平台基线重置复盘

- 项目名称：shanforge
- 当前阶段：PLAN
- 复盘主题：将当前仓库从旧版软件工厂叙事重置为抽象 Agent 平台基线

## 本轮已完成

- 需求、架构、测试、追踪和平台文档已按 `v2` 目标重写。
- Hermes 能力已被重新抽象为平台内核、Capability Registry、Context Engine、LLM Runtime、Workflow DSL 和 AgentResponse。
- 当前仓库中的旧版历史纳管叙事、兼容字段和遗留入口已进入清理收口阶段。

## 仍需持续关注

- 平台运行时尚未进入 `0.2.0` 代码实现阶段，当前仍以正式设计和契约为主。
- `Agent App Manifest`、`Workflow DSL`、`ModelPolicy` 和 `LLM Runtime` 还需要后续代码化落地。
- 文档、测试和控制面仍需继续围绕新平台边界同步演进。

## 下一步建议

- 先实现平台内核、模型解耦层和工作流装配主闭环。
- 再选择首个业务流作为 `Agent App` 参考实现，验证平台抽象是否稳定。

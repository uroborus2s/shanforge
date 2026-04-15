# 变更摘要

- 2026-04-15：新增 `docs/04-project-development/04-design/memory-system-detailed-design.md`，正式归档记忆系统的业务驱动详细设计方案。
- 2026-04-15：新增 `docs/04-project-development/04-design/infrastructure-layer-design.md`，完成基础设施层 7 个技术域建模，并定义应用层门面接口、运行时资源端口及下一轮待补齐端口清单。
- 2026-04-15：更新 `docs/04-project-development/04-design/infrastructure-layer-design.md`，明确实现阶段优先复用 Hermes 现有实现，并补齐技术域到 Hermes 模块的映射、反腐适配边界与 Hermes-backed adapter 落地规则。
- 2026-04-15：在 `src/` 落第一批基础设施代码骨架：新增 `domain/approval`、`domain/delegation`、`domain/gateway`，补齐 `ApprovalPolicyPort`、`SandboxPolicyPort`、`DelegationTransportPort`、`GatewayPort`，并加入 Hermes-backed capability/approval/delegation/gateway scaffold。
- 2026-04-15：更新 `memory-system-detailed-design.md`、`memory-runtime-interfaces.md` 与 `hermes-agent-source-analysis-report.md`，吸收 Hermes Agent 的 provider manager、archive query、bounded memory 与 delegation isolation 设计精华。
- 2026-04-15：同步更新设计索引、站点导航、需求追踪矩阵与 `.factory/memory` 摘要，补齐 `REQ-006` 的业务到设计追踪。

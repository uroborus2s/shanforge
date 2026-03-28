# 接口追踪矩阵

## 1. 文档目标

把接口与需求、模块、提供方、消费方、版本和测试覆盖关系对应起来。

## 2. 当前接口矩阵

| 接口编号 | 接口类型 | 提供方 | 消费方 | 关联需求 | 契约文件 | 版本与兼容策略 | 测试覆盖状态 | 负责人 |
|---|---|---|---|---|---|---|---|---|
| `API-001` | CLI 命令接口 | `factory-dispatch` | 使用者、维护者 | `REQ-003`, `REQ-006`, `REQ-007` | `scripts/factory-dispatch` | 动作别名可扩展，主入口保持稳定 | `unittest` + 人工走查 | 仓库维护者 |
| `API-002` | CLI 命令接口 | `factory-agent-session` | 使用者、维护者 | `REQ-003`, `REQ-006`, `REQ-007` | `scripts/factory-agent-session` | 推荐入口语义保持稳定 | `unittest` + 人工走查 | 仓库维护者 |
| `API-003` | 文档迁移接口 | `factory-docs-migrate-structure` | 历史项目维护者 | `REQ-001`, `REQ-007` | `scripts/factory-docs-migrate-structure`, `scripts/factory_core.py` | 旧结构到新结构单向升级 | 迁移回归测试 | 仓库维护者 |
| `API-004` | 文档检查接口 | `factory-docs-index-refresh --check` | 维护者、文档站点 | `REQ-001`, `NFR-001`, `NFR-002` | `scripts/factory-docs-index-refresh`, `scripts/factory_core.py` | 从全文比对升级为结构校验 | `unittest` + 当前仓库检查 | 仓库维护者 |
| `API-005` | 文档契约 | `docs/index.md` + 各级 `index.md` | 章略·墨衡、读者 | `REQ-001`, `REQ-004` | `docs/index.md` | 根导航稳定，子目录正文可定制 | docs 检查 + 人工走查 | 文档维护者 |
| `API-006` | 项目状态接口 | `.factory/project.json` | 脚本、模型、维护者 | `REQ-004`, `REQ-007` | `.factory/project.json` | 字段兼容优先，语义变更需同步文档 | 结构校验测试 | 仓库维护者 |

## 3. 维护规则

- 外部接口和内部系统接口都应登记，但需要在“接口类型”中明确区分。
- 参数、返回、错误码、权限、时序、幂等或版本策略变化时必须更新。
- 追踪矩阵中的接口编号应与 [API 设计文档](../04-design/api-design.md) 和契约文件保持一致。

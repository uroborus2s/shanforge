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
| `API-007` | CLI 命令接口 | `scripts/sync-codex-skills` | 使用者、维护者 | `REQ-003` | `scripts/sync-codex-skills` | 增量同步，避免覆盖宿主保留目录 | 人工走查 | 仓库维护者 |
| `API-008` | CLI 命令接口 | `factory-docs-standard-upgrade` | 项目协调者、文档维护者 | `REQ-001`, `REQ-002`, `REQ-006` | `scripts/factory-docs-standard-upgrade`, `scripts/factory_core.py` | docs 标准单项目升级入口稳定 | `unittest` + 当前仓库检查 | 仓库维护者 |
| `API-009` | CLI 命令接口 | `factory-docs-standard-upgrade-batch` | 平台维护者、项目协调者 | `REQ-001`, `REQ-002`, `REQ-006` | `scripts/factory-docs-standard-upgrade-batch`, `scripts/factory_core.py` | 批量扫描入口稳定，结果可汇总 | `unittest` + 当前仓库检查 | 仓库维护者 |
| `API-010` | 内部文件契约 | `config/action-registry.json` | `factory-dispatch`、后续意图解析器、策略引擎、工作流编排层 | `REQ-003`, `REQ-005`, `REQ-006` | `config/action-registry.json` | MVP 已实现；动作 ID 与字段兼容演进 | `unittest` + 人工走查 | 仓库维护者 |
| `API-011` | 内部文件契约 | `config/autonomy-policy.json` | `factory-dispatch`、动作治理层、审批边界 | `REQ-003`, `REQ-005`, `REQ-006` | `config/autonomy-policy.json` | MVP 已实现；风险等级和默认保守策略必须稳定 | `unittest` + 人工走查 | 仓库维护者 |
| `API-012` | 内部文件契约 | `config/frontends/*.json` + `factory-frontend-capabilities` | `Codex`、`Gemini CLI`、`opencode` 等前台及相关查询入口 | `REQ-003`, `REQ-005` | `config/frontends/*.json`, `scripts/factory-frontend-capabilities` | MVP 已实现；新增前台先通过能力画像接入 | `unittest` + 人工走查 | 仓库维护者 |
| `API-013` | CLI 命令接口 | `factory-multi-agent-board` | 协作负责人、子代理调度者 | `REQ-005` | `scripts/factory-multi-agent-board` | MVP 已增强；看板现会展示待审批票据、高风险推荐动作、未分派工作项、角色写入集合和冲突阻断摘要，后续再升级为正式调度面 | `unittest` + 人工走查 | 仓库维护者 |
| `API-014` | CLI 命令接口 | `factory-intent-resolver` | 使用者、维护者、后续动作治理层 | `REQ-003`, `REQ-006` | `scripts/factory-intent-resolver`, `scripts/factory-dispatch`, `config/action-registry.json`, `config/autonomy-policy.json` | MVP 已实现；支持规则型意图解析、`profile/workflow` 子目标选择和 `--execute-safe` 自动执行 `L0/L1` 主推荐动作 | `unittest` + 人工走查 | 仓库维护者 |
| `API-015` | CLI 命令接口 | `factory-intent-eval` | 平台维护者、QA、技能维护者 | `REQ-003`, `REQ-005`, `REQ-006` | `scripts/factory-intent-eval`, `config/evals/intent-resolver-cases.json` | MVP 已实现；固定样本集优先，后续扩展更多自然语言变体和排序评估 | `unittest` + 人工走查 | 仓库维护者 |
| `API-016` | CLI 命令接口 | `factory-intent-approval` | 使用者、维护者、审批协作者 | `REQ-003`, `REQ-005`, `REQ-006` | `scripts/factory-intent-approval`, `scripts/factory-intent-resolver`, `.factory/process/intent-approvals.json` | MVP 已实现；本地冻结票据已绑定建议 ownership 与显式写集，批准前会再次做冲突校验，后续可接 UI/远程审批 | `unittest` + 人工走查 | 仓库维护者 |

## 3. 维护规则

- 外部接口和内部系统接口都应登记，但需要在“接口类型”中明确区分。
- 参数、返回、错误码、权限、时序、幂等或版本策略变化时必须更新。
- 追踪矩阵中的接口编号应与 [API 设计文档](../04-design/api-design.md) 和契约文件保持一致。
- 尚未实现的规划型接口也应登记，但要明确标注“规划中”。

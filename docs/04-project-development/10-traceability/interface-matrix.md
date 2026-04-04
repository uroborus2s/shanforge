# 接口追踪矩阵

## 1. 文档目标

把接口与需求、模块、提供方、消费方、版本和测试覆盖关系对应起来。

## 2. 当前接口矩阵

| 接口编号 | 接口类型 | 提供方 | 消费方 | 关联需求 | 契约文件 | 版本与兼容策略 | 测试覆盖状态 | 负责人 |
|---|---|---|---|---|---|---|---|---|
| `API-001` | CLI 命令接口 | `factory-dispatch` | 使用者、维护者 | `REQ-003`, `REQ-006`, `REQ-007` | `scripts/factory-dispatch` | 动作别名可扩展，主入口保持稳定 | `unittest` + 人工走查 | 仓库维护者 |
| `API-002` | CLI 命令接口 | `factory-agent-session` | 使用者、维护者 | `REQ-003`, `REQ-006`, `REQ-007` | `scripts/factory-agent-session` | 推荐入口语义保持稳定 | `unittest` + 人工走查 | 仓库维护者 |
| `API-003` | 内部文件契约 | `config/software-factory.defaults.json` | 初始化脚本、规则刷新脚本 | `REQ-001`, `REQ-002`, `REQ-004` | `config/software-factory.defaults.json` | 默认文档入口和脚手架路径稳定 | 结构校验测试 | 仓库维护者 |
| `API-004` | 项目状态接口 | `.factory/project.json` | 脚本、模型、维护者 | `REQ-004`, `REQ-007` | `.factory/project.json` | 字段兼容优先，语义变更需同步文档 | 结构校验测试 | 仓库维护者 |
| `API-005` | 文档契约 | `docs/index.md` + 各级 `index.md` | `docs-stratego`、读者 | `REQ-001`, `REQ-004` | `docs/index.md` | 根导航稳定，子目录正文可定制 | `docs-stratego source validate` + 人工走查 | 文档维护者 |
| `API-006` | CLI 命令接口 | `factory-historical-project-onboarding` | 维护者、项目协调者 | `REQ-007` | `scripts/factory-historical-project-onboarding`, `scripts/factory-dispatch` | 历史项目纳管入口稳定 | `unittest` + 人工走查 | 仓库维护者 |
| `API-007` | CLI 命令接口 | `uv run python scripts/sync-codex-skills` | 使用者、维护者 | `REQ-003` | `scripts/sync-codex-skills` | 增量同步，避免覆盖宿主保留目录 | 人工走查 | 仓库维护者 |
| `API-008` | CLI 命令接口 | `docs-stratego source validate` | 文档维护者、项目协调者 | `REQ-001`, `REQ-002`, `REQ-006` | `docs-stratego` CLI | 源仓校验入口稳定 | CLI 校验 + 人工走查 | 文档维护者 |
| `API-009` | CLI 命令接口 | `docs-stratego source add/remove/scaffold-notify/sync/build/dev` | 平台维护者、项目协调者 | `REQ-001`, `REQ-002`, `REQ-006` | `docs-stratego` CLI | 聚合站点接入、构建与预览入口稳定 | CLI 校验 + 站点构建验证 | 平台维护者 |
| `API-010` | 内部文件契约 | `config/action-registry.json` | `factory-dispatch`、后续意图解析器、策略引擎、工作流编排层 | `REQ-003`, `REQ-005`, `REQ-006` | `config/action-registry.json` | MVP 已实现；动作 ID 与字段兼容演进 | `unittest` + 人工走查 | 仓库维护者 |
| `API-011` | 内部文件契约 | `config/autonomy-policy.json` | `factory-dispatch`、动作治理层、审批边界 | `REQ-003`, `REQ-005`, `REQ-006` | `config/autonomy-policy.json` | MVP 已实现；风险等级和默认保守策略必须稳定 | `unittest` + 人工走查 | 仓库维护者 |
| `API-012` | 内部文件契约 | `config/frontends/*.json` + `factory-frontend-capabilities` | `Codex`、`Gemini CLI`、`opencode` 等前台及相关查询入口 | `REQ-003`, `REQ-005` | `config/frontends/*.json`, `scripts/factory-frontend-capabilities` | MVP 已实现；新增前台先通过能力画像接入 | `unittest` + 人工走查 | 仓库维护者 |
| `API-013` | CLI 命令接口 | `factory-multi-agent-board` | 协作负责人、子代理调度者 | `REQ-005` | `scripts/factory-multi-agent-board` | MVP 已增强；看板现会展示待审批票据、高风险推荐动作、未分派工作项、角色写入集合和冲突阻断摘要，后续再升级为正式调度面 | `unittest` + 人工走查 | 仓库维护者 |
| `API-014` | CLI 命令接口 | `factory-intent-resolver` | 使用者、维护者、后续动作治理层 | `REQ-003`, `REQ-006` | `scripts/factory-intent-resolver`, `scripts/factory-dispatch`, `config/action-registry.json`, `config/autonomy-policy.json` | MVP 已实现；支持规则型意图解析、`profile/workflow` 子目标选择、skill 生命周期路由和 `--execute-safe` 自动执行 `L0/L1` 主推荐动作 | `unittest` + 人工走查 | 仓库维护者 |
| `API-015` | CLI 命令接口 | `factory-intent-eval` | 平台维护者、QA、技能维护者 | `REQ-003`, `REQ-005`, `REQ-006` | `scripts/factory-intent-eval`, `config/evals/intent-resolver-cases.json` | MVP 已实现；当前固定样本已扩到 `13` 条，覆盖项目类型、profile/workflow、skill 生命周期和阻塞边界；后续扩展更多自然语言变体和排序评估 | `unittest` + 人工走查 | 仓库维护者 |
| `API-016` | CLI 命令接口 | `factory-intent-approval` | 使用者、维护者、审批协作者 | `REQ-003`, `REQ-005`, `REQ-006` | `scripts/factory-intent-approval`, `scripts/factory-intent-resolver`, `.factory/process/intent-approvals.json` | MVP 已实现；本地冻结票据已绑定建议 ownership 与显式写集，批准前会再次做冲突校验，后续可接 UI/远程审批 | `unittest` + 人工走查 | 仓库维护者 |
| `API-017` | 内部文件契约 | `config/reply-policy.json` | `factory-intent-resolver`、`factory-intent-eval`、`factory-intent-approval`、后续 skill 治理链路 | `REQ-003`, `REQ-005`, `REQ-006` | `config/reply-policy.json`, `scripts/factory_core.py` | MVP 已实现；固定对话摘要字段、审批票据触发条件和 skill 正式变更批准边界 | `unittest` + 人工走查 | 仓库维护者 |
| `API-018` | CLI 命令接口 | `factory-skill-draft` | 技能维护者、平台维护者 | `REQ-003`, `REQ-005`, `REQ-006` | `scripts/factory-skill-draft`, `config/reply-policy.json` | MVP 已实现；候选草案现同时写出 `eval-report.json` 与 `change-summary.md` 骨架，不直接改正式 skill | `unittest` + 人工走查 | 仓库维护者 |
| `API-019` | CLI 命令接口 | `factory-skill-approval` | 技能维护者、平台维护者、审批协作者 | `REQ-003`, `REQ-005`, `REQ-006` | `scripts/factory-skill-approval`, `config/reply-policy.json`, `.factory/process/skill-approvals.json` | MVP 已实现；只有已通过正式评估的候选 skill 才能进入专用审批票据链路，批准/拒绝结果会回写候选目录 | `unittest` + 人工走查 | 仓库维护者 |
| `API-020` | CLI 命令接口 | `factory-skill-promote` | 技能维护者、平台维护者、发布协作者 | `REQ-003`, `REQ-005`, `REQ-006` | `scripts/factory-skill-promote`, `config/reply-policy.json`, `.factory/process/skill-promotions.json` | MVP 已实现；只有评估通过且已批准的候选 skill 才能晋升到正式 `skills/`，若正式 skill 已存在会先备份 | `unittest` + 人工走查 | 仓库维护者 |
| `API-021` | CLI 命令接口 | `factory-skill-rollback` | 技能维护者、平台维护者、发布协作者 | `REQ-003`, `REQ-005`, `REQ-006` | `scripts/factory-skill-rollback`, `config/reply-policy.json`, `.factory/process/skill-rollbacks.json` | MVP 已实现；有旧版本备份时恢复旧版，首次发布的新 skill 只有在删除回退审批通过后才允许删除回退 | `unittest` + 人工走查 | 仓库维护者 |
| `API-022` | CLI 命令接口 | `factory-skill-eval` | 技能维护者、平台维护者、QA | `REQ-003`, `REQ-005`, `REQ-006` | `scripts/factory-skill-eval`, `config/reply-policy.json`, `.factory/process/skill-evals.json` | MVP 已实现；候选 skill 评估已收口到正式命令，检查 skill 结构、evals schema、输入文件与变更摘要，不再依赖手工改 `eval-report.json` | `unittest` + 人工走查 | 仓库维护者 |
| `API-023` | CLI 命令接口 | `factory-skill-delete-approval` | 技能维护者、平台维护者、审批协作者 | `REQ-003`, `REQ-005`, `REQ-006` | `scripts/factory-skill-delete-approval`, `config/reply-policy.json`, `.factory/process/skill-delete-approvals.json` | MVP 已实现；首次发布的新 skill 可进入删除回退专用审批票据链路，批准/拒绝结果会回写候选目录 | `unittest` + 人工走查 | 仓库维护者 |

## 3. 维护规则

- 外部接口和内部系统接口都应登记，但需要在“接口类型”中明确区分。
- 参数、返回、错误码、权限、时序、幂等或版本策略变化时必须更新。
- 追踪矩阵中的接口编号应与 [API 设计文档](../04-design/api-design.md) 和契约文件保持一致。
- 尚未实现的规划型接口也应登记，但要明确标注“规划中”。

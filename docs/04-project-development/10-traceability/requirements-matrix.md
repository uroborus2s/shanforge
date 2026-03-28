# 需求追踪矩阵

**项目名称：** 山海工枢 / shanforge  
**负责人：** 仓库维护者  
**最后更新：** 2026-03-27  

## 1. 需求到设计/实施/测试映射

| 需求 ID | 需求摘要 | 设计文档 | 模块 | 接口 | 任务 | 测试 | 发布状态 |
|---|---|---|---|---|---|---|---|
| `REQ-001` | 建立正式的人类文档入口 | `project-charter.md`, `system-architecture.md` | `MOD-001`, `MOD-004` | `API-003`, `API-005` | `TASK-001` 文档基线建设 | 文档结构走查 | 已完成基线 |
| `REQ-002` | 形成需求规划与设计基线 | `prd.md`, `requirements-analysis.md`, `system-architecture.md`, `module-boundaries.md` | `MOD-001`, `MOD-004` | `API-005` | `TASK-001` 文档基线建设 | 需求一致性校验 | 已完成基线 |
| `REQ-003` | 保持 CLI-first 的统一执行入口 | `technical-selection.md`, `api-design.md`, `user-guide.md` | `MOD-002`, `MOD-003` | `API-001`, `API-002` | `TASK-002` 入口对齐 | 用户路径走查 | 已完成基线 |
| `REQ-004` | 明确人类文档与 AI 记忆分层 | `prd.md`, `technical-selection.md`, `system-architecture.md` | `MOD-001`, `MOD-002`, `MOD-004` | `API-003`, `API-004`, `API-005` | `TASK-002` 入口对齐 | 文档与配置检查 | 已完成基线 |
| `REQ-005` | 支持角色化协作与交接理解 | `project-charter.md`, `requirements-analysis.md`, `module-boundaries.md`, `user-guide.md` | `MOD-001`, `MOD-002`, `MOD-003` | `API-002`, `API-004` | `TASK-003` 协作说明沉淀 | 人工评审 | 已完成基线 |
| `REQ-006` | 提供带自然语言速查表的用户使用文档 | `user-guide.md`, `prompt-templates.md`, `api-design.md`, `prd.md` | `MOD-001`, `MOD-003` | `API-001`, `API-002`, `API-005` | `TASK-004` 用户指南整理 | 用户路径走查 | 已完成基线 |
| `REQ-007` | 接管非软件工厂历史项目并完成纳管 | `user-guide.md`, `current-state-analysis.md`, `historical-project-onboarding-checklist.md`, `historical-project-onboarding-automation.md`, `requirements-analysis.md`, `prd.md` | `MOD-001`, `MOD-003`, `MOD-004` | `API-002`, `API-004`, `API-005`, `API-006` | `TASK-005` 历史项目纳管规则整理 | 纳管场景走查 | MVP 已实现 |

## 2. 非功能需求映射

| NFR ID | 要求 | 设计落点 | 验证方式 | 负责人 |
|---|---|---|---|---|
| `NFR-001` | 新协作者 10 分钟内定位关键入口 | `docs/index.md`, `user-guide.md` | 人工走查 | 文档维护者 |
| `NFR-002` | 配置与正式文档入口一致 | `technical-selection.md`, `api-design.md`, `config/software-factory.defaults.json` | 配置检查 | 仓库维护者 |
| `NFR-003` | 正式文档采用单文件演进 | `docs/*` 全部正式文档 | 文档结构检查 | 文档维护者 |

## 3. 接口责任矩阵

| 接口 ID | 提供方 | 消费方 | 契约文件 | 监控项 | 运维责任 |
|---|---|---|---|---|---|
| `API-001` | `factory-dispatch` | 使用者、维护者 | `scripts/factory-dispatch` | 动作别名和入口一致性 | 脚本维护者 |
| `API-002` | `factory-agent-session` | 使用者、维护者 | `scripts/factory-agent-session` | 推荐阅读和下一步命令是否合理 | 脚本维护者 |
| `API-003` | 默认配置层 | 初始化脚本、规则刷新脚本 | `config/software-factory.defaults.json` | 文档路径是否有效 | 仓库维护者 |
| `API-004` | 项目状态层 | 被管理项目、脚本、模型 | `.factory/project.json` | 状态结构有效性 | 项目协调者 |
| `API-005` | 正式文档层 | 人类读者、维护者 | `docs/*` | 文档是否可发现和可追踪 | 文档维护者 |
| `API-006` | `factory-historical-project-onboarding` / `factory-dispatch historical-project-onboarding` | 维护者、项目协调者 | `historical-project-onboarding-automation.md`, `scripts/factory-historical-project-onboarding`, `scripts/factory-dispatch` | 命令是否可在非空历史仓库中补齐最小骨架并生成 session/doctor | 脚本维护者 |

## 4. 未闭环项

| ID | 问题 | 缺失环节 | 负责人 | 计划时间 |
|---|---|---|---|---|
| `GAP-001` | 尚未补齐管理员指南 | 交接/管理文档 | 仓库维护者 | 后续阶段 |
| `GAP-002` | 发布与运维文档已建立，但仍缺少环境级实参和管理员专属操作细节 | 发布/运维细化文档 | 仓库维护者 | 后续阶段 |
| `GAP-003` | 尚未建立文档入口一致性自动检查 | 自动化保障 | 脚本维护者 | 后续阶段 |

## 5. 变更记录

| 日期 | 变更内容 | 变更人 |
|---|---|---|
| 2026-03-25 | 初始版本，建立需求到设计与入口的追踪关系 | Codex |
| 2026-03-25 | 增加自然语言速查表与旧项目接管规则的追踪映射 | Codex |
| 2026-03-26 | 将旧项目追踪映射修正为历史项目纳管场景 | Codex |
| 2026-03-26 | 增加历史项目纳管 checklist、模板与自动化设计的追踪映射 | Codex |
| 2026-03-26 | 更新 API-006 和 REQ-007 状态为历史项目纳管 MVP 已实现 | Codex |
| 2026-03-27 | 将项目名称统一更新为“山海工枢 / shanforge”并同步引用路径 | Codex |
| 2026-03-28 | 将 4 大模块单轴文档结构和最新模板同步到需求追踪矩阵 | Codex |

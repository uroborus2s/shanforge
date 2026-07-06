# FLOW-CONTRACT-001 实施计划

## 版本信息

| 项目 | 内容 |
|---|---|
| 文档编号 | `FLOW-CONTRACT-001-PLAN` |
| 文档类型 | 工作项实施计划 |
| 当前版本 | `0.1.0` |
| 当前状态 | 草稿 |
| 最近更新 | 2026-07-06 |

## 版本历史

| 版本 | 修改内容 | 日期 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `0.1.0` | 建立与正式实施方案一致的 work item 执行计划 | 2026-07-06 | Codex | 待审核 | 待批准 |
| `0.1.1` | 补充项目级测试治理、测试环境、端口管理、启动记忆和非活跃任务降级任务 | 2026-07-06 | Codex | 待审核 | 待批准 |

## 目标

交付 `FLOW-REQ-001` 的正式需求、正式实施方案、导航、doc-map、memory 摘要和 work item ledger。

## 架构

正式事实放在 `docs/04-project-development/`。执行索引和过程证据放在 `.factory/workitems/FLOW-CONTRACT-001/`。AI 恢复上下文只读取 `.factory/memory/` 摘要和 `doc-map.md`，不把 PM HTML 或临时 evidence 当事实源。

## 输入

- 用户关于流程契约、文档结构、记忆结构、PM、版本管理、领域模块、前后端设计和防跳步机制的讨论。
- `skills/using-shanforge/SKILL.md`
- `skills/project-memory/SKILL.md`
- `skills/requirements-engineering/SKILL.md`
- `skills/document-templates/SKILL.md`
- `skills/writing-plans/SKILL.md`
- `docs/04-project-development/05-development-process/superpowers-workflow-integration-plan.md`
- `.factory/memory/doc-map.md`
- `.factory/memory/tasks.summary.md`

## 文件

| 类型 | 路径 | 职责 |
|---|---|---|
| 新建 | `docs/04-project-development/03-requirements/process-workflow-contract-requirements.md` | 正式需求 |
| 新建 | `docs/04-project-development/05-development-process/process-workflow-contract-implementation-plan.md` | 正式实施方案 |
| 修改 | `docs/index.md` | 根导航 |
| 修改 | `docs/04-project-development/05-development-process/index.md` | 开发过程阅读顺序 |
| 修改 | `.factory/memory/doc-map.md` | 正式文档到 summary 映射 |
| 修改 | `.factory/memory/tasks.summary.md` | 流程契约任务摘要 |
| 新建 | `.factory/workitems/FLOW-CONTRACT-001/brief.md` | 工作项简报 |
| 新建 | `.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl` | 工作项流水账 |

## 任务

1. 写正式需求文档，覆盖四类场景、三层文档、baseline、领域模块、前后端设计、版本管理、PM 和防跳步。
2. 写正式实施方案，覆盖流程管控、skill 调用图、运行时文档设计、每个 skill 的输入输出、每个 skill 的内部流程和任务拆解。
3. 更新根导航和开发过程首页。
4. 更新 doc-map 和 tasks summary。
5. 写 work item brief、plan 和 ledger。
6. 补充项目级测试治理、测试环境和端口管理规则。
7. 补充启动记忆读取和非活跃任务降级规则。
8. 运行文档导航相关测试和 diff 检查。
9. 输出状态为 `ready_for_review`，等待独立 review。

## 测试策略

- 文档导航：`uv run pytest tests/test_sf_sp_010_documentation_navigation.py`
- PM 邻近回归：`uv run pytest tests/test_project_management_control_plane.py`
- diff 检查：`git diff --check`
- 未运行 `docs-stratego source validate` 时必须说明原因。

## 评审门

- 计划评审：`pending`
- 文档评审：`pending`
- 验证：`pending`
- 人工确认：`pending`
- 提交：`pending`

## 完成口径

本工作项只能进入 `ready_for_review`。`approved` 必须来自独立 review，`closed` 必须来自人工确认。

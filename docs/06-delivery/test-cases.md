# Shanforge 正式测试案例目录

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `TEST-CATALOG-SHANFORGE-001` |
| 正式版本 | `v1.0.0` |
| 当前修订 | 无 |
| 来源候选 | `TEST-GOVERNANCE-CLOSURE-001` |
| 负责人 | `HUMAN_QUALITY_SECURITY_LEAD` |
| 修改 / 审核 / 批准 | `AI_EXECUTOR` / 独立 Reviewer / `uroborus` |
| 状态 | 已批准并生效 |
| 上游 | `TEST-PLAN-001`、PRD、Skill-first 系统架构 |
| 下游 | pytest、WorkItem evidence、人类可读测试报告 |
| 最后更新 | 2026-08-23 |

## 案例索引

| 案例 ID | 名称 | 需求 / 验收标准 | 层级 | 优先级 | 风险等级 | 自动化入口 |
|---|---|---|---|---|---|---|
| `TEST-BB-001` | 完整会话路由合同 | `REQ-SF-002` | 整体黑盒 | P0 | high | `tests/test_full_project_session_workflow_routing.py::test_candidate_behavior_map_is_complete_and_each_mapping_is_unique` |
| `TEST-UI-001` | 项目快照结构与导航 | `REQ-SF-007` | UI | P1 | medium | `tests/test_using_shanforge_snapshot.py::ProjectSnapshotTest::test_snapshot_renders_compact_scoped_board_without_duplicate_tasks` |
| `TEST-API-001` | 项目记忆幂等契约 | `REQ-SF-003` | API/契约 | P0 | high | `tests/test_project_memory_skill.py::test_project_memory_ledger_schema_prevents_repeat_work` |
| `TEST-REL-001` | 测试治理发布守卫 | `REQ-SF-004` | 发布回归 | P0 | high | `tests/test_project_test_governance.py::test_formal_test_references_resolve_to_current_test_files` |

## 案例：`TEST-BB-001`

- 名称：完整会话路由合同
- 版本：1.0.0
- 定义状态：active
- 测试目标：证明每种会话行为只有一个默认工作流，并且行为映射集合完整。
- 需求 / 验收标准：REQ-SF-002 / 会话进入唯一、可失败关闭的工作流。
- 关联设计 / API / UI / 任务：工作流执行设计 / MODEL-ROUTING-001-T01。
- 测试类型与层级：整体黑盒。
- 优先级：P0
- 风险等级：high
- Owner：HUMAN_QUALITY_SECURITY_LEAD
- 环境别名：TEST-ENV-PYTEST
- 自动化状态：automated
- 自动化入口：`tests/test_full_project_session_workflow_routing.py::test_candidate_behavior_map_is_complete_and_each_mapping_is_unique`

### 前置条件

1. 当前候选包含 `using-shanforge` 与正式工作流设计。
2. pytest 能读取仓库内 Skill 和正式文档。

### 测试数据 / fixture

| 数据 / fixture | 用途 | 敏感 | 准备 / 复位方式 |
|---|---|---|---|
| 正式行为映射表 | 比较行为全集和唯一映射 | false | 直接读取；无写入 |

### 步骤与判定

| 序号 | 操作步骤 | 预期结果 | 证据要求 |
|---:|---|---|---|
| 1 | 执行登记的 pytest 节点 | 所有预期行为存在且每个行为只映射一个默认工作流 | pytest 节点回执与 exit code |

### 后置条件与清理

- pytest 进程退出；没有常驻服务或持久测试数据。

### 标签

- workflow、black-box、routing

## 案例：`TEST-UI-001`

- 名称：项目快照结构与导航
- 版本：1.0.0
- 定义状态：active
- 测试目标：证明静态项目快照采用紧凑分组、有效导航且不重复任务。
- 需求 / 验收标准：REQ-SF-007 / 项目状态页面可读、可导航、无重复展开。
- 关联设计 / API / UI / 任务：项目快照 UI / PM-DASHBOARD-005-T01。
- 测试类型与层级：UI 静态结构。
- 优先级：P1
- 风险等级：medium
- Owner：HUMAN_QUALITY_SECURITY_LEAD
- 环境别名：TEST-ENV-STATIC
- 自动化状态：automated
- 自动化入口：`tests/test_using_shanforge_snapshot.py::ProjectSnapshotTest::test_snapshot_renders_compact_scoped_board_without_duplicate_tasks`

### 前置条件

1. 项目快照脚本和最小项目 fixture 可读取。
2. 测试不依赖浏览器登录态或网络。

### 测试数据 / fixture

| 数据 / fixture | 用途 | 敏感 | 准备 / 复位方式 |
|---|---|---|---|
| 临时项目状态 fixture | 生成静态快照并检查结构 | false | pytest 临时目录创建并自动清理 |

### 步骤与判定

| 序号 | 操作步骤 | 预期结果 | 证据要求 |
|---:|---|---|---|
| 1 | 执行登记的快照 pytest 节点 | 页面分组紧凑、任务不重复且导航目标有效 | pytest 回执；失败时保留断言摘要 |

### 后置条件与清理

- 临时目录由 pytest 清理；无浏览器或服务进程。

### 标签

- ui、snapshot、navigation

## 案例：`TEST-API-001`

- 名称：项目记忆幂等契约
- 版本：1.0.0
- 定义状态：active
- 测试目标：证明 ledger schema 和幂等键阻止重复执行已完成动作。
- 需求 / 验收标准：REQ-SF-003 / 项目事实可恢复且同一事件不会重复执行。
- 关联设计 / API / UI / 任务：项目记忆合同 / MODEL-ROUTING-001-T01。
- 测试类型与层级：进程内 API/契约。
- 优先级：P0
- 风险等级：high
- Owner：HUMAN_QUALITY_SECURITY_LEAD
- 环境别名：TEST-ENV-PYTEST
- 自动化状态：automated
- 自动化入口：`tests/test_project_memory_skill.py::test_project_memory_ledger_schema_prevents_repeat_work`

### 前置条件

1. `project-memory` Skill 与 ledger schema 可读取。
2. 测试仅检查进程内契约，不调用网络 API。

### 测试数据 / fixture

| 数据 / fixture | 用途 | 敏感 | 准备 / 复位方式 |
|---|---|---|---|
| ledger schema 示例 | 检查 event UID 和幂等语义 | false | 仓库只读；无复位动作 |

### 步骤与判定

| 序号 | 操作步骤 | 预期结果 | 证据要求 |
|---:|---|---|---|
| 1 | 执行登记的契约 pytest 节点 | schema 明确 event UID、幂等键和重复工作拒绝规则 | pytest 节点回执与 exit code |

### 后置条件与清理

- 无状态写入或常驻资源。

### 标签

- api、contract、memory、idempotency

## 案例：`TEST-REL-001`

- 名称：测试治理发布守卫
- 版本：1.0.0
- 定义状态：active
- 测试目标：证明正式测试文档引用的 pytest 文件全部存在，失效入口会阻断候选。
- 需求 / 验收标准：REQ-SF-004 / 发布候选只能引用当前可执行测试入口。
- 关联设计 / API / UI / 任务：测试策略 / TEST-GOVERNANCE-CLOSURE-001-T01。
- 测试类型与层级：发布回归。
- 优先级：P0
- 风险等级：high
- Owner：HUMAN_QUALITY_SECURITY_LEAD
- 环境别名：TEST-ENV-PYTEST
- 自动化状态：automated
- 自动化入口：`tests/test_project_test_governance.py::test_formal_test_references_resolve_to_current_test_files`

### 前置条件

1. 正式测试计划和案例目录已纳入候选。
2. pytest 能读取当前 Git 工作树中的测试文件。

### 测试数据 / fixture

| 数据 / fixture | 用途 | 敏感 | 准备 / 复位方式 |
|---|---|---|---|
| 正式 Markdown 中的测试路径 | 检查引用可解析 | false | 直接读取；无写入 |

### 步骤与判定

| 序号 | 操作步骤 | 预期结果 | 证据要求 |
|---:|---|---|---|
| 1 | 执行登记的治理 pytest 节点 | 所有正式 `tests/test_*.py` 引用都解析到当前文件 | pytest 节点回执与 exit code |
| 2 | 运行完整必需发布回归 | pytest、Ruff、文档校验和 Git hygiene 均通过 | WorkItem evidence 和最终测试报告 |

### 后置条件与清理

- pytest 进程退出；临时缓存写入隔离目录并清理。

### 标签

- release、governance、traceability

## 自动有效性校验

运行：

```bash
uv run python skills/document-templates/scripts/validate_test_documents.py \
  --repo-root . \
  --catalog docs/06-delivery/test-cases.md
```

校验器检查索引与详情 ID 一致、必填字段和枚举有效、自动化 pytest 节点真实存在，以及步骤含操作、预期和证据。单次结果不回写本目录，保存在当前 WorkItem evidence 和测试报告中。

## 正式版本历史（仅已发布）

| 版本 | 日期 | 变更内容 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v1.0.0` | 2026-08-23 | 建立 Skill-first 正式案例目录和自动有效性入口 | `AI_EXECUTOR` | 独立 Reviewer | `uroborus` |

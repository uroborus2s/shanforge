# FLOW-CONTRACT-001 实施前评审输入包

## 评审类型

实施前独立评审。

## 评审目标

判断 `FLOW-CONTRACT-001` 是否可以从流程契约设计阶段进入 skill 改造实施阶段。

## 当前状态

- work item：`FLOW-CONTRACT-001`
- 当前 gate：`needs_independent_review`
- 下一动作：`independent_review`
- 本轮是否已改 skill：否
- 本轮是否已提交：否

## 评审范围

只评审以下文件：

```text
docs/04-project-development/03-requirements/process-workflow-contract-requirements.md
docs/04-project-development/05-development-process/process-workflow-contract-implementation-plan.md
.factory/workitems/FLOW-CONTRACT-001/brief.md
.factory/workitems/FLOW-CONTRACT-001/plan.md
.factory/workitems/FLOW-CONTRACT-001/task-briefs/
.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl
.factory/memory/doc-map.md
.factory/memory/tasks.summary.md
.factory/memory/skill-updates.summary.md
```

不要评审仓库中已有的其他脏改动、历史删除或无关 skill 改造。

## 必审问题

1. 需求是否完整覆盖用户讨论：
   - 四类场景：新项目、增加需求、变更需求、修复 bug。
   - 单需求 / 单任务瀑布式，多需求并列敏捷式。
   - Project baseline、领域划分、后端模块、数据库、API、前端 UI。
   - 项目级整体测试、接口测试、UI 测试、黑盒测试、测试环境和端口规则。
   - 文档版本信息、版本历史和临时文档边界。
   - memory 条件读取链和非活跃任务降级。
2. 实施方案是否足够进入任务实施：
   - 业务流程管控是否完整。
   - skill 调用图是否清楚。
   - 每个核心 skill 的输入、输出、内部流程和禁止项是否定义清楚。
   - 任务拆解是否能逐项执行。
3. Gate 是否足够防止 AI 跳步：
   - 是否禁止作者自批。
   - 是否要求独立 review。
   - 是否要求 verification evidence。
   - 是否定义 N/A 接受规则。
4. 是否存在过度设计：
   - 是否新增了不必要文档。
   - 是否恢复了中心脚本或隐藏主控。
   - 是否把 memory 重新变成长上下文入口。

## 已执行验证

```text
uv run pytest tests/test_sf_sp_010_documentation_navigation.py tests/test_project_management_control_plane.py
结果：11 passed

git diff --check
结果：通过

python3 JSONL 解析 .factory/workitems/FLOW-CONTRACT-001/ledger.jsonl
结果：jsonl ok
```

## 已知非阻塞事项

`docs-stratego source validate` 当前失败在既有文件：

```text
docs/04-project-development/04-design/assets/v2-architecture-pages/index.md
```

原因：`assets/` 目录下存在 Markdown。该文件不是 `FLOW-CONTRACT-001` 新增或修改范围。

## 期望评审输出

写入：

```text
.factory/workitems/FLOW-CONTRACT-001/reviews/implementation-pre-review.md
```

输出字段：

```text
reviewer_type:
reviewer_id:
reviewer_independence_evidence:
review_status: approved | changes_requested
next_gate_status: pending_human_confirmation | changes_requested
review_score:
```

如果没有真实独立 reviewer 证据，不得写 `approved`。

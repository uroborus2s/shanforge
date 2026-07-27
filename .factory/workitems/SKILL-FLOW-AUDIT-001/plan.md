# SKILL-FLOW-AUDIT-001 Plan

## 目标

把当前 Shanforge 软件开发流程和 skill 调用流程整理成一份可执行说明，并创建两个独立子任务对 skill 文本质量和流程完整性做评审。

## 文件结构

| 路径 | 动作 | 职责 |
|---|---|---|
| `.factory/workitems/SKILL-FLOW-AUDIT-001/brief.md` | create | 用户请求和范围 |
| `.factory/workitems/SKILL-FLOW-AUDIT-001/plan.md` | create | 当前工作项计划 |
| `.factory/workitems/SKILL-FLOW-AUDIT-001/task-briefs/language-prompt-review.md` | create | 中文 / prompt 专家子任务 |
| `.factory/workitems/SKILL-FLOW-AUDIT-001/task-briefs/skill-flow-test.md` | create | 流程测试子任务 |
| `.factory/workitems/SKILL-FLOW-AUDIT-001/reports/software-development-and-skill-flow.md` | create | 完整流程说明 |
| `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-1-verification.md` | create | 本轮验证证据 |
| `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/` | create | 子任务结果归档 |
| `.factory/workitems/SKILL-FLOW-AUDIT-001/ledger.jsonl` | create | 任务事实 ledger |
| `tests/test_skill_flow_process_audit.py` | create | 结构测试 |

## 任务

### Task 1：恢复流程事实

- Red：确认没有当前工作项产物。
- Green：读取 `.factory/memory/` 入口、`using-shanforge`、`project-memory`、开发流程和 Superpowers 集成方案。
- Evidence：在验证文件记录已读文件和排除文件。

### Task 2：创建两个独立子任务

- Red：没有 task brief 和子 agent id。
- Green：创建语言 / prompt 评审子任务和流程测试子任务。
- Evidence：记录子 agent id、任务边界和输出要求。

### Task 3：输出完整流程说明

- Red：流程说明不存在。
- Green：写出软件开发闭环、skill 调用链、任务执行链、门禁和产物路径。
- Evidence：结构测试检查关键章节和路径。

### Task 4：验证新增产物

- Red：新增测试失败或未运行。
- Green：运行定向 pytest 和 ruff。
- Evidence：记录命令、exit code 和结果。

## Review Gate

- 本轮主线程只能把工作项推进到 `self_check_passed` 或 `needs_independent_review`。
- 两个子任务的报告是评审输入，不等于人工确认。
- 若需要正式关闭工作项，应再进入 `requesting-code-review` 和人工确认门。

## Memory Sync

本轮不修改共享 `.factory/memory/*.summary.md`，因为工作区已有大量既有脏改动。当前事实先落在本 work item 的 report、evidence 和 ledger 中，避免混入其他任务范围。

## Iteration 6 最小路径修订（已批准）

- 冻结 8 个明确整改 Skill，不再用当前 37 个 Skill 的全仓平均分验收本整改包。
- 冻结双维度评分公式和 37 个相关 workflow 测试节点。
- 不修改当前已通过的旧失败测试；验证通过后直接进入独立复评。
- 详细合同：
  `task-briefs/iteration-6-minimal-acceptance-amendment.md`。

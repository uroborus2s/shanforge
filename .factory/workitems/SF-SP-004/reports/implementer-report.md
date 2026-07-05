# SF-SP-004 Implementer Report

- Work item：`SF-SP-004`
- 实现者状态：`ready_for_review`
- 范围：新增 Shanforge 本地化 `writing-plans` skill。
- 日期：2026-07-05

## 本次完成

- 新增 `tests/test_writing_plans_skill.py`，先验证缺失目录失败，再验证本地化语义。
- 新增 `skills/writing-plans/SKILL.md`。
- 新增 `skills/writing-plans/references/workitem-plan-template.md`。
- 新增 `skills/writing-plans/references/task-brief-template.md`。
- 新增 `skills/writing-plans/references/plan-review-template.md`。
- 新增 `skills/writing-plans/agents/openai.yaml`。

## 保留的 Superpowers 语义

- 多步骤任务动代码前先写计划。
- 先做 scope check 和 file structure，再拆任务。
- 任务拆到 Red / Green / evidence / review 小步骤。
- 每步包含精确文件路径、真实命令和期望输出。
- 计划保存后必须做计划自审和 plan review。
- 执行阶段交给 `subagent-driven-development` 或 `executing-plans`。

## Shanforge 改造

- 默认计划路径改为 `.factory/workitems/<WORKITEM-ID>/plan.md`。
- 子任务 brief 固定进入 `.factory/workitems/<WORKITEM-ID>/task-briefs/`。
- 强制包含 `.factory/memory/` 同步、work item ledger 和 review gate。
- 不再使用 `docs/superpowers/plans`。
- 不再把每个小步骤 commit 作为硬要求；提交交给 `gitcommitzh` 按任务范围处理。

## 未完成

- `subagent-driven-development` 和 `executing-plans` 尚未本地化。
- `requesting-code-review` 尚未本地化。
- `verification-before-completion` 尚未本地化。

## 验证

见 `evidence/test-report.md`。

## 下一步

请求 task review。通过后继续 `SF-SP-005` 或先补 `requesting-code-review`，取决于计划顺序和用户优先级。

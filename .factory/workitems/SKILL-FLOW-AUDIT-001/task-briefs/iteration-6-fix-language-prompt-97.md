# Iteration 6 Fix Language And Prompt To 97

## Role

Skill 文本修复 implementer，同时扮演中文语言专家和 Prompt 专家。

## Goal

根据 iteration-6 三份报告，最小范围修复当前 `skills/*/SKILL.md` 的中文语言和 Prompt 问题，目标是在后续独立复评中：

- 中文语言平均分 `>= 97`；
- Prompt 工程平均分 `>= 97`；
- Critical / Important 均为 `0`；
- 不恢复旧中心脚本、旧 `factory-*` gate 或远端闭环冒充。

作者自检只能到 `ready_for_review`，不能自批 `approved`。

## Inputs

- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/chinese-language-review-iteration-6.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/prompt-engineering-review-iteration-6.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-completeness-test-iteration-6.md`
- 当前工作区所有 `skills/*/SKILL.md`
- 相关结构测试 under `tests/`

## Required Fixes

必须处理：

1. `skills/agent-harness-construction/SKILL.md`：补齐 Shanforge 状态包中的 `work_item` / `ledger_event`；补 `needs_user_input` 例子；明确 Codex skill 写作归 `skill-creator`。
2. `skills/ai-first-engineering/SKILL.md`：补齐 `work_item` / `ledger_event`；把 `blocked` 和 `needs_user_input` 拆成可执行分支。
3. `skills/article-writing/SKILL.md`：补齐 `work_item` / `ledger_event` 和验证字段；补 `needs_user_input` 语义；明确发布型长文与工作文档边界。
4. `skills/using-shanforge/SKILL.md`：Bug / 测试失败路由表显式列 `systematic-debugging` 为根因调查 owner，并对齐下游状态词。
5. `skills/frontend-patterns/SKILL.md`：若作为 Shanforge work item owner，补 `needs_user_input` 状态或明确 `design_decision` 只是 `needs` 不是状态。
6. `skills/tdd-workflow/SKILL.md`：删除重复的“无根因确认不得进入 GREEN 实现”语义。
7. `skills/art-asset-pipeline/SKILL.md`：压缩 `tmp/`、`approved/`、用户确认和最终包泄漏规则，优先合并成短表。
8. `skills/requesting-code-review/SKILL.md`：合并“同线程作者自检不能 approved / needs_independent_review”的重复表达。

为达到 97 分，可以只继续触碰低于 95 分或报告明确点名的 skill。不要为了分数重写高分且无问题的 skill。

## Outputs

必须写入：

- `.factory/workitems/SKILL-FLOW-AUDIT-001/reports/iteration-6-fix-language-prompt-97-report.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-6-fix-language-prompt-97-verification.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/iteration-6-fix-language-prompt-97-review-input.md`

报告必须包含：

1. 含义保留清单，覆盖目标、触发、输入、步骤、输出、禁止项、例外、验收、风险和 handoff。
2. 实际修改文件清单。
3. 每个修改文件如何提高中文语言分和 Prompt 分。
4. 自评分：中文语言平均分、Prompt 平均分、低于 90 数量、Critical / Important / Minor。
5. 未处理项和原因。
6. Shanforge 状态包：

```text
工作结果：
- work_item: SKILL-FLOW-AUDIT-001
- skill: skill-creator
- status: ready_for_review | blocked | needs_user_input
- outputs:
  - <paths>
- evidence:
  - <paths or commands>
- ledger_event: <event id or none>
- needs:
  - review | user_input
```

## Verification

至少运行：

- 受影响 skill 的 `quick_validate`，若工具存在；
- 受影响测试的最小 pytest；
- 对应 ruff；
- `git diff --check`；
- work item ledger / review-ledger JSONL 解析。

若无法可靠达到两个平均分 `>= 97`，输出 `blocked` 或 `ready_for_review` 加明确残留风险，不得把自评分写成独立复评通过。

## Forbidden

- 不得提交、push、创建 PR 或 merge。
- 不得覆盖 iteration-6 三份原始评审 / 测试报告。
- 不得把作者自检写成 `approved`。
- 不得修改与本任务无关的业务代码。
- 不得恢复旧中心命令、动作注册表、`factory-*` 或旧全局流程脚本。

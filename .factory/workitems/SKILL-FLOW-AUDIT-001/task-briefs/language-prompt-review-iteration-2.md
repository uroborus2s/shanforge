# Language And Prompt Review Iteration 2

## 角色

中文语言专家 + prompt 专家。

## 目标

对当前仓库内所有仍存在的 `skills/*/SKILL.md` 做全面评审和评分，重点发现：

- 啰嗦、重复、教程化、入口过长。
- 语义不清晰、职责边界不清。
- 触发条件过宽或退出条件不足。
- 输出契约、证据、状态包和失败语义不明确。
- 旧生态、英文口径或不适合 Shanforge 的措辞。

## 输入

- 当前 `skills/*/SKILL.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/language-prompt-review.md` 只能作为历史参考，不能直接复用评分。
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reports/software-development-and-skill-flow.md` 仅用于理解当前 workflow 边界。

## 输出

写入：

`.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/language-prompt-review-iteration-2.md`

报告必须包含：

1. 本次实际扫描到的 skill 数量和文件清单。
2. 每个 skill 的 0-100 分。
3. 每个低于 90 分 skill 的具体问题，按“啰嗦重复 / 语义不清 / prompt 边界 / 输出契约 / 旧口径”分类。
4. Top 10 共性问题。
5. 最小修复优先级，不要求本子任务直接修改文件。

## 禁止

- 不修改 skill 文件。
- 不覆盖旧报告。
- 不把历史已删除 skill 纳入当前评分。
- 不把建议写成已完成修复。

## 状态回写

```text
status: DONE | BLOCKED
outputs:
  - .factory/workitems/SKILL-FLOW-AUDIT-001/reviews/language-prompt-review-iteration-2.md
```

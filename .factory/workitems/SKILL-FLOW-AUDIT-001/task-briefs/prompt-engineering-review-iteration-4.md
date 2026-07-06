# Prompt Engineering Review Iteration 4

## Role

Prompt 专家。

## Goal

全面评审当前所有 `skills/*/SKILL.md` 的 prompt 质量，并逐项评分。

重点检查：

- 触发条件是否过宽或过窄；
- 指令优先级是否清楚；
- tool / skill / 子 agent 边界是否清楚；
- 输出契约、失败语义、证据要求是否完整；
- 是否存在自批完成、跳过 review、跳过验证或旧中心流程回退风险；
- 是否有长背景压过关键动作的问题。

## Inputs

- 当前工作区所有 `skills/*/SKILL.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/language-prompt-review-iteration-3.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-completeness-test-iteration-3.md`

## Output

写入：

`.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/prompt-engineering-review-iteration-4.md`

报告必须包含：

1. 实际扫描 skill 数量和完整文件清单。
2. 每个 skill 的 prompt 评分，0-100。
3. 每个低于 90 分 skill 的具体问题，按触发边界、动作边界、输出契约、失败语义、旧流程风险分组。
4. 互相冲突或职责重叠的 skill 对。
5. 相对 iteration-3 的分数变化和原因。
6. 最小下一步修复清单，只列真正值得改的项。

## Forbidden

- 不得编辑 skill 文件。
- 不得覆盖 iteration-3 报告。
- 不得新增中心脚本或旧 `factory-*` gate。
- 不得把本地 commit 说成远端 PR / push / merge 闭环。

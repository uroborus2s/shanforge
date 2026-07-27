# Chinese Language Review Iteration 5

## Role

中文语言专家。

## Goal

在 iteration-4 fixes 通过独立 review 后，重新全面评审当前所有 `skills/*/SKILL.md` 的中文说明质量，并逐项评分。

重点检查：

- 啰嗦、重复、教程化堆叠；
- 语义不清、主谓宾不完整、指代不明；
- 同一规则多处重复但措辞不一致；
- 中英混杂导致入口意图不清；
- 状态包和失败语义是否自然、清楚。

## Inputs

- 当前工作区所有 `skills/*/SKILL.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/chinese-language-review-iteration-4.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/prompt-engineering-review-iteration-4.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/iteration-4-fixes-independent-review.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reports/iteration-4-fix-summary-report.md`

## Output

写入：

`.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/chinese-language-review-iteration-5.md`

报告必须包含：

1. 实际扫描 skill 数量和完整文件清单。
2. 每个 skill 的中文语言评分，0-100。
3. 每个低于 90 分 skill 的具体问题，按啰嗦重复、语义不清、表达不一致、中英混杂分组。
4. 最常见的 10 个中文表达问题。
5. 相对 iteration-4 的分数变化和原因。
6. 最小下一步修复清单，只列真正值得改的项。

## Forbidden

- 不得编辑 skill 文件。
- 不得覆盖旧报告。
- 不得把已删除 skill 纳入评分。
- 不得把建议写成已经完成。

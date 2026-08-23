# 独立逐 Skill 评分任务

你是 `SKILL-FULL-OPTIMIZATION-001` 的独立 reviewer。不得读取实现者会话历史；只读取下面列出的文件化输入。

## Inputs

- Requirements：`.factory/workitems/SKILL-FULL-OPTIMIZATION-001/brief.md`
- Plan：`.factory/workitems/SKILL-FULL-OPTIMIZATION-001/plan.md`
- Baseline：`.factory/workitems/SKILL-FULL-OPTIMIZATION-001/reports/baseline-audit.md`
- Implementer report：`.factory/workitems/SKILL-FULL-OPTIMIZATION-001/reports/implementation.md`
- Optimization results：`.factory/workitems/SKILL-FULL-OPTIMIZATION-001/reports/optimization-results.md`
- Review remediation：`.factory/workitems/SKILL-FULL-OPTIMIZATION-001/reports/review-remediation.md`
- Verification evidence：`.factory/workitems/SKILL-FULL-OPTIMIZATION-001/evidence/verification.md`
- Ledger：`.factory/workitems/SKILL-FULL-OPTIMIZATION-001/ledger.jsonl`
- Review rubric：`skills/requesting-code-review/references/review-score-rubric.md`
- Architecture constraints：`AGENTS.md`、`skills/using-shanforge/references/work-skill-return-contract.md`
- Review objects：动态发现的全部 `skills/*/SKILL.md` 及其 Skill 直接路由资源。

当前工作区并发存在 `TEST-GOVERNANCE-CLOSURE-001`。不要把该工作项的 document-templates、verification、正式测试文档、测试或 memory diff 计入本工作项；但评分当前 Skill 内容时仍应读取最终可见文件。

## Job

1. 独立核对 38/38 Skill；不能只抽样，也不能复用 implementer 分数。
2. 对每个 Skill 分别给出：能力摘要、需求符合度 `/30`、架构一致性 `/20`、测试充分性 `/20`、代码质量 `/20`、文档与记忆同步 `/10`、总分 `/100`、C/I/M、结论、证据和剩余优化方向。
3. `no_change_required` 项也必须独立评分；不得因没有 diff 自动给满分。
4. 每项通过线为 `>=90 / C0-I0`。任一项不满足时，整体 `review_status: changes_requested`，列出可执行 finding。
5. 可运行只读验证；不得修改 Skill、测试、WorkItem ledger、memory 或 Git 状态。
6. 唯一允许写入：`.factory/workitems/SKILL-FULL-OPTIMIZATION-001/reviews/independent-scorecards.md`。
7. reviewer 不能把任务标记为 done；若全部通过，默认写 `return_to_orchestrator`，只有输入包存在真实人工 Gate 时才写 `pending_human_confirmation`。

## Output

输出文件必须包含：

- `reviewer_type: independent_subagent`
- 可定位的 `reviewer_id`
- 明确说明未参与实现、只读取文件化输入的 `reviewer_independence_evidence`
- `review_status`、`next_gate_status`、整体 `review_score`
- 38 行逐项 scorecard 表，Skill 名唯一且无遗漏
- Critical / Important / Minor finding 清单
- 实际运行的验证命令与结果
- 低于满分项的具体剩余优化方向；无剩余项写 `none`

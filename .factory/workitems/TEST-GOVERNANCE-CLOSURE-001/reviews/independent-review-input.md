# TEST-GOVERNANCE-CLOSURE-001 独立评审输入

## Reviewer 范围

- Review type：批次 Spec + Quality Review。
- 只读；不得修改实现、正式文档、ledger、Git 或并行工作项。
- WorkItem：`TEST-GOVERNANCE-CLOSURE-001`。
- Task：`TEST-GOVERNANCE-CLOSURE-001-T03`。

## 必读

- `.factory/workitems/TEST-GOVERNANCE-CLOSURE-001/brief.md`
- `.factory/workitems/TEST-GOVERNANCE-CLOSURE-001/plan.md`
- `.factory/workitems/TEST-GOVERNANCE-CLOSURE-001/reports/implementation.md`
- `.factory/workitems/TEST-GOVERNANCE-CLOSURE-001/evidence/pre-review-verification.md`
- 当前 WorkItem 精确 diff；排除 `SKILL-FULL-OPTIMIZATION-001` 和其他并行 hunks。

## 专项检查

1. 七项截图判断是否都由实现和测试覆盖。
2. Markdown 案例是否足够让人执行，并保持单一事实源。
3. 校验器是否能拒绝失效节点、错误计数/结论，是否存在明显误判或绕过。
4. 模板是否完整且没有强迫普通小任务生成重报告。
5. `v3.2.0` 当前保持候选是否符合先评审后发布的事实边界。
6. 并行工作项是否被排除。

## 已知 Gate

完整 pytest 唯一失败是 `test_test_governance_revision_is_formally_published`。Reviewer 若批准候选，流程总控将把测试计划、案例和导航元数据切换为正式发布，再运行完整验证；这不是请求接受失败测试。

## 输出

写入 `.factory/workitems/TEST-GOVERNANCE-CLOSURE-001/reviews/independent-review.md`，包含独立性元数据、100 分制、Critical/Important/Minor、结论和是否允许正式发布。

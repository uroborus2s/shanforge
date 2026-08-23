# Review Feedback Triage

## I1：冻结合同与证据漂移

- 来源：独立 review；severity：Important。
- 技术核实：正确。并行任务在送审后改写同一 Skill，工作区内容不再等于送审候选。
- 决定：Fixed。以 Git 暂存区建立精确候选，只暂存本工作项的测试模板引用和报告边界；隔离导出后重新验证。

## I2：混入布局 / 迁移行为

- 来源：独立 review；severity：Important。
- 技术核实：正确。这些改动属于 `SKILL-COMPLETENESS-P0-001`，不属于本工作项。
- 决定：Fixed。精确候选排除这些 hunk，保留在并行工作区，不修改、不提交。

## M1：Markdown 硬换行

- 来源：独立 review；severity：Minor。
- 技术核实：正确，但尾随空格会被 `git diff --check` 拒绝。
- 决定：Fixed。使用显式 `<br>` 保持换行并通过差异卫生检查。

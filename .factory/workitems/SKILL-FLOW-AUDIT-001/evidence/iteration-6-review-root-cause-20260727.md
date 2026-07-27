# Iteration 6 Review Root Cause Evidence

- 时间：`2026-07-27T18:05:11+08:00`
- 范围：只复现和诊断，不修改 Skill、测试或验收口径
- 结论：`root_cause_found`

## 证据 1：97 分目标与限定范围矛盾

独立复审按全部 36 个 Skill 复算：

- 中文：`93.83`
- Prompt：`94.19`
- 即使 8 个目标 Skill 全为 100，理论上限也只有 `95.11 / 95.25`

任务卡同时要求全量平均 `>=97`，又要求最小范围只处理 8 个点名或低分 Skill、
不为分数重写高分且无问题的 Skill。这两个约束不能同时满足。

当前仓内实际为 37 个 Skill，旧 36 项评分基线也已发生集合漂移。

## 证据 2：旧失败测试当前不再复现

```bash
uv run pytest -p no:cacheprovider tests/test_independent_review_gate.py
```

```text
5 passed in 0.02s
```

当前工作区的 `requesting-code-review` 文本与测试断言已经同步，但该 diff 尚未归属
本调查任务，因此这里只记录现状，不把它作为本任务修复。

## 证据 3：旧完整命令已失效

复跑 Iteration 6 的 21 文件 workflow 命令：

```text
ERROR: file or directory not found: tests/test_skill_creator_skill_principles.py
collected 0 items
```

该测试已由后续已提交的 Skill 清理工作项删除。旧命令和旧评分集合都不是当前
可用基线。

## 单一根因

Iteration 6 把“全量 Skill 平均分门槛”和“只修限定小集合”写进同一验收合同，
但没有冻结评分集合、评分公式和测试清单。后续仓库继续演进后，评分分母与测试
文件又发生漂移，导致评审既数学上不可达，也无法用原命令重放。

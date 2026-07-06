# SKILL-FLOW-AUDIT-001 Brief

## 背景

用户要求完整阅读当前 Shanforge 流程后，输出完整的软件开发过程、skill 调用过程和执行任务过程，并创建两个子任务：

1. 中文语言专家和 prompt 专家子任务，全面评审所有仓内 skill 说明，评分并指出啰嗦重复、语义不清晰等问题。
2. 测试子任务，验证 skill 流程是否覆盖所有步骤、每步是否完整、输出是否满足要求。

## 范围

- 只评估仓内 `skills/*/SKILL.md` 和当前 workflow 相关 references。
- 按 `.factory/memory/` 优先恢复上下文。
- 不新增仓库级中心脚本。
- 不复用 `SF-SP-011` 编号；`SF-SP-010` 文档已明确 Superpowers 集成计划内只有 `SF-SP-001` 到 `SF-SP-010`。

## 非目标

- 不改写所有 skill。
- 不创建远端 PR。
- 不提交 git commit，除非用户另行明确要求提交。
- 不把子 agent 的结论直接写成最终 approved。

## 交付物

- `plan.md`
- `task-briefs/language-prompt-review.md`
- `task-briefs/skill-flow-test.md`
- `reports/software-development-and-skill-flow.md`
- `evidence/iteration-1-verification.md`
- `reviews/` 下的子任务结果归档
- `ledger.jsonl`

## 验收标准

- 流程说明覆盖从会话启动到提交、PR、memory sync、人工确认的完整闭环。
- skill 调用流程说明清楚区分 `using-shanforge`、`project-memory` 和工作 skill。
- 两个子任务均有明确输入、禁止动作、输出和评分要求。
- 至少有一个结构测试固定新增流程说明和子任务契约。

# Skill Flow Completeness Test Iteration 5

## Role

Skill 流程测试工程师。

## Goal

在 iteration-4 fixes 通过独立 review 后，重新测试当前 skill 流程是否能完整覆盖 Shanforge 软件开发闭环：每个步骤是否存在 owner、输入、动作、输出、gate、失败语义和证据要求；输出是否完全满足要求。

## Inputs

- 当前 workflow skills under `skills/`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-completeness-test-iteration-4.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/iteration-4-fixes-independent-review.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-4-s1-s6-dry-run-transcript.md`
- `skills/using-shanforge/references/remote-pr-handoff.md`
- 相关 tests

## Test Steps

检查：

1. 会话恢复；
2. 意图澄清 / brief；
3. 需求 / AC / NFR；
4. 设计 / 文档 / 边界；
5. 实施计划 / task brief；
6. 执行 / evidence / report / ledger；
7. Bug 修复 / TDD / 根因；
8. 完成前验证；
9. 独立 review / scoring；
10. review 反馈处理；
11. 人工确认门；
12. 本地提交；
13. 远端 PR / push / merge handoff；
14. 压缩恢复和 idempotency；
15. S1-S6 dry-run transcript 是否满足 evidence 要求。

## Output

写入：

`.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-completeness-test-iteration-5.md`

报告必须包含：

1. Flow matrix：step、owner skill、input、action、output、gate、assessment。
2. 每一步输出是否完全满足 Shanforge 要求。
3. Critical / Important / Minor findings。
4. 实际运行的验证命令、exit code 和关键输出。
5. 总评分 0-100。
6. 相对 iteration-4 的变化。
7. 最小下一步修复清单。

## Forbidden

- 不得编辑 skill 文件。
- 不得新增中心脚本或旧 `factory-*` gate。
- 不得把 dry-run transcript 写成真实代码、commit、push、PR 或 merge 完成。
- 不得把本地 commit 说成远端 PR / push / merge 闭环。

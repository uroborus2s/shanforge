# Skill Flow Completeness Test Iteration 2

## 角色

Skill 流程测试工程师。

## 目标

测试当前 skill 流程是否能完整覆盖软件开发全步骤，并检查每一步输出是否满足 Shanforge 要求。

## 输入

- `skills/using-shanforge/SKILL.md`
- `skills/project-memory/SKILL.md`
- `skills/brainstorming/SKILL.md`
- `skills/requirements-engineering/SKILL.md`
- `skills/document-templates/SKILL.md`
- `skills/writing-plans/SKILL.md`
- `skills/subagent-driven-development/SKILL.md`
- `skills/executing-plans/SKILL.md`
- `skills/tdd-workflow/SKILL.md`
- `skills/systematic-debugging/SKILL.md`
- `skills/verification-before-completion/SKILL.md`
- `skills/requesting-code-review/SKILL.md`
- `skills/receiving-code-review/SKILL.md`
- `skills/gitcommitzh/SKILL.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-test-report.md` 只能作为历史参考，不能直接复用结论。
- 相关结构测试文件。

## 测试范围

检查以下流程步骤是否完整：

1. 会话恢复。
2. 意图澄清 / brief。
3. 需求 / AC / NFR。
4. 设计 / 文档 / 边界。
5. 实施计划 / task brief。
6. 执行 / evidence / report / ledger。
7. Bug 修复 / TDD / 根因。
8. 完成前验证。
9. 独立 review / scoring。
10. review 反馈处理。
11. 人工确认门。
12. 本地提交。
13. 远端 PR / push / merge 边界。
14. 压缩恢复和 idempotency。

## 输出

写入：

`.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-completeness-test-iteration-2.md`

报告必须包含：

1. 流程矩阵：步骤、owner skill、输入、动作、输出、gate、评估。
2. 每一步输出是否完全满足要求。
3. 缺口 / 风险，按 Critical / Important / Minor 分类。
4. 可运行验证命令及结果。
5. 0-100 分总评分。
6. 最小修复任务建议。

## 禁止

- 不修改 skill 文件。
- 不新增中心脚本或旧 `factory-*` gate。
- 不把“有文档结构测试”说成“真实行为回放已完成”。
- 不把本地提交冒充远端 PR / push / merge 闭环。

## 状态回写

```text
status: DONE | BLOCKED
outputs:
  - .factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-completeness-test-iteration-2.md
```

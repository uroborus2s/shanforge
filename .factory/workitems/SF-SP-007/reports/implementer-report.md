# SF-SP-007 Implementer Report

- Work item：`SF-SP-007`
- 状态：`ready_for_review`
- 日期：2026-07-05

## 完成内容

- 新增 `skills/verification-before-completion/`
- 新增 `skills/systematic-debugging/`
- 新增 `skills/tdd-workflow/references/tdd-debugging-verification-gate.md`
- 更新 `skills/tdd-workflow/SKILL.md`
- 新增 `tests/test_verification_debugging_workflow_skills.py`

## 含义保留

- 完成声明必须先有新鲜验证证据。
- 验证必须运行完整命令、读取完整输出、检查 exit code 和失败数量。
- 修复前必须先完成根因调查。
- 调试必须经过根因调查、模式分析、假设验证和根因修复。
- 3 次修复失败后停止继续补丁，并质疑架构。
- TDD 必须先看测试失败，再写最小实现。

## 流程边界

新增 skill 只输出状态、产物、证据和 `needs`，不声明前置、后置或下一步 skill。

## 未完成

- 尚未进入黑盒流程 eval。
- 尚未提交或进入 PR 闭环。

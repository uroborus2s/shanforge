# FLOW-TASK-009 升级 review 和 verification

## 工作项

- 工作项：`FLOW-CONTRACT-001`
- 任务：`FLOW-TASK-009`
- 状态：`draft`
- 上游计划：`.factory/workitems/FLOW-CONTRACT-001/plan.md`
- 流水账：`.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`

## 目标

让 review 接受或拒绝 N/A，verification 在关闭前检查新鲜命令、exit code、输出和 evidence。

## 输入

- `skills/requesting-code-review/SKILL.md`
- `skills/receiving-code-review/SKILL.md`
- `skills/verification-before-completion/SKILL.md`

## 允许修改

- `skills/requesting-code-review/SKILL.md`
- `skills/receiving-code-review/SKILL.md`
- `skills/verification-before-completion/SKILL.md`
- 对应 tests。

## 验证命令

```bash
uv run pytest tests/test_review_workflow_skills.py tests/test_verification_debugging_workflow_skills.py
```

期望输出：

```text
通过；新增作者自检不能 approved、无 evidence 不能关闭、N/A 需 reviewer 接受断言。
```

## 完成口径

review 不能替代 verification，verification 不能替代 human confirmation。

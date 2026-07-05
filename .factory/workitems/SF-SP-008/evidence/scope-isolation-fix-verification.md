# SF-SP-008 Scope Isolation Fix Verification

- 时间：2026-07-05 17:03 +08:00
- 反馈来源：独立范围检查 reviewer `019f3181-c78c-7ed2-a008-57c0510cb907`

## 反馈

SF-SP-008 候选 diff 中的 `.factory/memory/*` 文件同时包含 `stratix-service`、PM HTML 等非 SF-SP-008 条目。
若整文件随 SF-SP-008 提交，会造成范围混入。

## 修复

- `skills/gitcommitzh/SKILL.md` 新增提交范围规则：
  - 同一 `.factory/memory/` 文件混有其他任务条目时，只能暂存当前任务 hunk。
  - 无法拆分时停止并拆成独立提交。
- `skills/gitcommitzh/references/pr-closure-checklist.md` 同步该规则。
- `tests/test_pr_commit_workflow_rules.py` 固定该规则。

## 验证命令

- `.venv/bin/pytest tests/test_pr_commit_workflow_rules.py`
  - 结果：`5 passed`
- `.venv/bin/ruff check tests/test_pr_commit_workflow_rules.py`
  - 结果：`All checks passed!`
- `python3 skills/skill-creator/scripts/quick_validate.py skills/gitcommitzh`
  - 结果：`Skill is valid!`

## 结论

范围混入风险已转化为提交前硬规则。
后续 SF-SP-008 提交只能暂存当前任务 hunk，不能整文件纳入混合 memory diff。

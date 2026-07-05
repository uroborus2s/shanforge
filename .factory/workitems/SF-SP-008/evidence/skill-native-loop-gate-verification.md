# SF-SP-008 Skill-Native Loop Gate Verification

- 时间：2026-07-05 16:52 +08:00
- 范围：`using-shanforge`、`gitcommitzh`、`pr-closure-checklist`、`test_pr_commit_workflow_rules`

## 纠正

撤销中心脚本 gate 方案。
`scripts/factory-*` 和 `factory-dispatch` 不作为新的 workflow gate。

收尾门改为 skill-native 规则：

- final、commit、close work item 前重读当前 work item ledger 最新事件。
- 同时核对 review ledger。
- 若仍有 `next_required_action`，停止。
- 若状态仍是 `ready_for_review`、`changes_requested`、`needs_independent_review`、`pending_human_confirmation` 或 `self_check_passed`，停止。
- 只能报告阻塞 gate 和下一步动作，不能宣称完成。

## 验证命令

- `.venv/bin/pytest tests/test_pr_commit_workflow_rules.py`
  - 结果：`5 passed`
- `.venv/bin/ruff check tests/test_pr_commit_workflow_rules.py`
  - 结果：`All checks passed!`
- `python3 skills/skill-creator/scripts/quick_validate.py skills/gitcommitzh`
  - 结果：`Skill is valid!`
- `python3 skills/skill-creator/scripts/quick_validate.py skills/using-shanforge`
  - 结果：`Skill is valid!`

## 结论

脚本 gate 已撤销。
SF-SP-008 仍处于 `ready_for_review`，下一步仍是真实独立 review。

# FLOW-TASK-012 实现报告

## 结果

- 状态：`ready_for_review`
- 黑盒契约覆盖新项目、增加需求、变更需求、Bug 双确认、缺证据关闭、
  直接分析、项目化分析、N/A 审查、缺 review 关闭和直接提交诱导。
- SF-SP 场景覆盖一句话需求、Bug、Review、压缩恢复、完成声明和自评隔离。
- fast-path smoke 使用 11 条稳定断言，固定直接分析不读 memory、项目化任务必须
  恢复 memory、恢复任务必须按 ledger 幂等跳过。

## 变更

- `skills/using-shanforge/references/black-box-flow-eval.md`
- `tests/test_black_box_workflow_eval.py`
- `.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-SKILL-003-P001-black-box-transcript.md`

## 验证

- `PYTHONPATH=src .venv/bin/python -m pytest tests/test_black_box_workflow_eval.py -q`
  → `13 passed`
- `.venv/bin/ruff check tests/test_black_box_workflow_eval.py`
  → `All checks passed`
- `git diff --check`（本任务文件）
  → 通过

## 边界

- eval 只验证观察到的 workflow 行为。
- 未执行提交、Push、PR、Merge 或部署。
- 未把 dry-run 写成真实代码修改或外部动作。

## Review 整改

独立初审的两个 Important Finding 已修复并验证，详情见
`FLOW-TASK-012-review-fix-report.md` 和 `FLOW-TASK-012-review-fix-verification.md`；
当前等待同一 reviewer 复审。

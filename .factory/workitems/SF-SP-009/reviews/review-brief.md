# SF-SP-009 Review Brief

## Review 目标

请独立评审 SF-SP-009 是否完成黑盒流程 eval 的首版契约，重点检查：

- 六类场景是否覆盖计划要求：一句话需求、bug 修复、review 反馈、压缩恢复、完成声明、自评隔离。
- 评分断言是否可执行，是否能阻止空泛自评。
- 是否严格避免重新引入中心脚本 gate。
- `using-shanforge` 入口是否保持流程总控职责，不替代工作 skill、review、人工确认或提交闭环。
- evidence 是否真实记录 red/green 和邻近回归结果。

## 输入文件

- `.factory/workitems/SF-SP-009/plan.md`
- `.factory/workitems/SF-SP-009/evidence/iteration-1-verification.md`
- `.factory/workitems/SF-SP-009/reports/iteration-1-implementer-report.md`
- `skills/using-shanforge/references/black-box-flow-eval.md`
- `skills/using-shanforge/SKILL.md`
- `tests/test_black_box_workflow_eval.py`
- `docs/04-project-development/05-development-process/superpowers-workflow-integration-plan.md`

## 验证摘要

- Red：`.venv/bin/pytest tests/test_black_box_workflow_eval.py` -> `4 failed`。
- Green：`.venv/bin/pytest tests/test_black_box_workflow_eval.py` -> `4 passed`。
- Ruff：`.venv/bin/ruff check tests/test_black_box_workflow_eval.py` -> passed。
- Skill validator：`python3 skills/skill-creator/scripts/quick_validate.py skills/using-shanforge` -> passed。
- 邻近 workflow 回归：`26 passed`。
- `git diff --check`：passed。

## 期望输出

- `approved` 或 `changes_requested`。
- 若 approved，请给出 review score，并说明 reviewer independence evidence。
- 若 changes requested，请按 Critical / Important / Minor 分类列出阻塞点。

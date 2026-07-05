# SF-SP-009 Iteration 1 Implementer Report

## 范围

- 新增 `skills/using-shanforge/references/black-box-flow-eval.md`。
- 更新 `skills/using-shanforge/SKILL.md`，为 `SF-SP-009` / 黑盒流程 eval 增加 reference 入口。
- 新增 `tests/test_black_box_workflow_eval.py`，固定六类场景、评分门、失败门和无脚本 gate 回退。
- 更新 `docs/04-project-development/05-development-process/superpowers-workflow-integration-plan.md` 中 `SF-SP-009` 当前状态。
- 新增 `SF-SP-009` plan、ledger、evidence 和 review brief。

## 实现说明

黑盒 eval 被实现为 skill-native reference，而不是中心脚本。`using-shanforge` 只负责在用户要求 `SF-SP-009`、黑盒 eval 或流程回归评估时读取 reference，并按 fast smoke / full regression 场景记录真实证据。

Reference 覆盖六个场景：

1. 一句话需求。
2. Bug 修复。
3. Review 反馈。
4. 压缩恢复。
5. 完成声明。
6. 自评隔离。

每个场景都有输入、期望行为和 critical assertions。全局评分门要求总分 `>= 90`，任一 critical assertion 为 `0` 即失败。

## 验证

- Red：`.venv/bin/pytest tests/test_black_box_workflow_eval.py` -> `4 failed`。
- Green：`.venv/bin/pytest tests/test_black_box_workflow_eval.py` -> `4 passed`。
- Ruff：`.venv/bin/ruff check tests/test_black_box_workflow_eval.py` -> passed。
- Skill validator：`python3 skills/skill-creator/scripts/quick_validate.py skills/using-shanforge` -> passed。
- 邻近回归：执行 / 评审 / 验证 / 提交闭环 / 黑盒 eval 相关测试共 `26 passed`。
- Diff check：`git diff --check` -> passed。

## 风险

- 本轮没有实现自动 LLM judge；交付的是可审查、可执行的 eval contract。
- 仓库存在大量无关脏改动；本报告只覆盖 SF-SP-009 相关文件。
- 需要独立 review 确认场景、评分门和失败门是否足够严谨。

## 状态

`ready_for_review`

# SF-SP-004 Writing Plans Evidence

- Work item：`SF-SP-004`
- 范围：新增 Shanforge 本地化 `writing-plans` skill。
- 状态：`ready_for_review`
- 日期：2026-07-05

## Red

### Test harness correction

- 命令：`.venv/bin/pytest tests/test_writing_plans_skill.py`
- 结果：收集失败，`ModuleNotFoundError: No module named 'yaml'`
- 处理：测试改为纯文本检查 `agents/openai.yaml`，不引入额外依赖。

### Effective Red

- 命令：`.venv/bin/pytest tests/test_writing_plans_skill.py`
- 结果：`3 failed`
- 失败原因：
  - 缺少 `skills/writing-plans/SKILL.md`
  - 缺少 `skills/writing-plans/references/workitem-plan-template.md`
  - 缺少 `skills/writing-plans/references/task-brief-template.md`
  - 缺少 `skills/writing-plans/references/plan-review-template.md`
  - 缺少 `skills/writing-plans/agents/openai.yaml`

## Green

- 命令：`.venv/bin/pytest tests/test_writing_plans_skill.py`
- 结果：`3 passed`

- 命令：`.venv/bin/ruff check tests/test_writing_plans_skill.py`
- 结果：通过

- 命令：`.venv/bin/python skills/skill-creator/scripts/quick_validate.py skills/writing-plans`
- 结果：通过

- 命令：`git diff --check`
- 结果：通过

## 覆盖点

- `writing-plans` 触发条件、输入、输出路径和 Shanforge work item 路由。
- 文件结构先行、TDD 小步骤、真实命令、期望输出和禁止占位符。
- `workitem-plan-template.md`、`task-brief-template.md`、`plan-review-template.md`。
- 中文 OpenAI 元数据。

## 偏离

- `uv` 当前不在 PATH，本轮沿用仓库 `.venv/bin/*` 执行验证。
- 本任务只新增计划生成 skill；执行类、评审类、验证类 skill 仍在后续任务。

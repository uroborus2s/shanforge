# SF-SP-005 Execution Workflow Evidence

- Work item：`SF-SP-005`
- 范围：新增 Shanforge 本地化执行类 workflow skill。
- 状态：`ready_for_review`
- 日期：2026-07-05

## Red

- 命令：`.venv/bin/pytest tests/test_execution_workflow_skills.py`
- 结果：`4 failed`
- 失败原因：
  - 缺少 `skills/subagent-driven-development/SKILL.md`
  - 缺少 `skills/subagent-driven-development/references/*`
  - 缺少 `skills/subagent-driven-development/agents/openai.yaml`
  - 缺少 `skills/executing-plans/SKILL.md`
  - 缺少 `skills/executing-plans/agents/openai.yaml`

## Green

- 命令：`.venv/bin/pytest tests/test_execution_workflow_skills.py`
- 结果：`4 passed`

- 命令：`.venv/bin/ruff check tests/test_execution_workflow_skills.py`
- 结果：通过

- 命令：`.venv/bin/python skills/skill-creator/scripts/quick_validate.py skills/subagent-driven-development`
- 结果：通过

- 命令：`.venv/bin/python skills/skill-creator/scripts/quick_validate.py skills/executing-plans`
- 结果：通过

- 命令：`git diff --check`
- 结果：通过

## 覆盖点

- `subagent-driven-development` 已改为 Shanforge work item plan / task brief / ledger / evidence / review 流程。
- `subagent-driven-development` 保留实现者状态、双阶段 review、问题重派发和禁止并行实现者规则。
- `executing-plans` 已改为当前会话 inline fallback。
- 两个 skill 均不保留 `docs/superpowers` 或旧 finishing branch 入口。
- 两个 skill 均有中文 OpenAI 元数据。

## 偏离

- `uv` 当前不在 PATH，本轮沿用仓库 `.venv/bin/*` 执行验证。
- 本任务只新增执行类 workflow skill；`requesting-code-review`、`verification-before-completion`、`systematic-debugging` 仍在后续任务。

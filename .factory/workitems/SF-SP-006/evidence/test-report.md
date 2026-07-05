# SF-SP-006 Review Workflow Evidence

- Work item：`SF-SP-006`
- 范围：新增 Shanforge 本地化评审类 workflow skill。
- 状态：`passed`
- 日期：2026-07-05

## Red

- 命令：`.venv/bin/pytest tests/test_review_workflow_skills.py`
- 结果：`5 failed`
- 失败原因：
  - 缺少 `skills/requesting-code-review/SKILL.md`
  - 缺少 `skills/requesting-code-review/references/*`
  - 缺少 `skills/requesting-code-review/agents/openai.yaml`
  - 缺少 `skills/receiving-code-review/SKILL.md`
  - 缺少 `skills/receiving-code-review/references/*`
  - 缺少 `skills/receiving-code-review/agents/openai.yaml`

## Green

- 命令：`.venv/bin/pytest tests/test_review_workflow_skills.py`
- 结果：`5 passed`

- 命令：`.venv/bin/pytest tests/test_review_workflow_skills.py tests/test_execution_workflow_skills.py tests/test_writing_plans_skill.py tests/test_superpowers_reference_migration.py`
- 首次结果：`1 failed, 15 passed`
- 失败原因：`requesting-code-review` 的触发条件仍点名 `subagent-driven-development` / `executing-plans`，违反工作 skill 不声明路由的边界。
- 修正：改为泛化的“实现流程到达 review checkpoint”。
- 复跑结果：`16 passed`

- 命令：`.venv/bin/ruff check tests/test_review_workflow_skills.py`
- 结果：通过

- 命令：`.venv/bin/ruff check tests/test_review_workflow_skills.py tests/test_execution_workflow_skills.py tests/test_writing_plans_skill.py tests/test_superpowers_reference_migration.py`
- 结果：通过

- 命令：`.venv/bin/python skills/skill-creator/scripts/quick_validate.py skills/requesting-code-review`
- 结果：通过

- 命令：`.venv/bin/python skills/skill-creator/scripts/quick_validate.py skills/receiving-code-review`
- 结果：通过

- 命令：`.venv/bin/python -c "import json, pathlib; ..."`
- 结果：`.factory/workitems/SF-SP-006/ledger.jsonl` 和 `.factory/memory/review-ledger.jsonl` JSONL 解析通过

- 命令：`rg -n "与其他 skill 的关系|subagent-driven-development|executing-plans|verification-before-completion|gitcommitzh|requesting-code-review/code-reviewer.md|docs/superpowers" skills/requesting-code-review skills/receiving-code-review`
- 结果：无匹配

- 命令：`git diff --check`
- 结果：通过

## 覆盖点

- `requesting-code-review` 已本地化为 task review、PR review、independent review task、review score 和人工确认门。
- `receiving-code-review` 已本地化为先核实反馈、再逐项处理、验证和回应。
- 两个 skill 均使用 `.factory/workitems/<WORKITEM-ID>/` 和 `.factory/memory/review-ledger.jsonl`。
- 两个 skill 均有中文 OpenAI 元数据。
- 两个 skill 均不声明前置、后置或下一步 skill。

## 偏离

- `uv` 当前不在 PATH，本轮沿用仓库 `.venv/bin/*` 执行验证。
- 本任务只新增评审类 workflow skill；`verification-before-completion` 和 `systematic-debugging` 仍在后续任务。

# SF-SP-004 iteration-2 验证证据

## 定向验证

- `.venv/bin/pytest tests/test_writing_plans_skill.py`
  - 结果：`3 passed`
- `.venv/bin/ruff check tests/test_writing_plans_skill.py`
  - 结果：`All checks passed!`
- `python3 skills/skill-creator/scripts/quick_validate.py skills/writing-plans`
  - 结果：`Skill is valid!`

## 旧英文模板扫描

- `rg -n "# <Feature Name> Implementation Plan|\\*\\*Goal:\\*\\*|\\*\\*Architecture:\\*\\*|\\*\\*Tech Stack:\\*\\*|## Inputs|## Scope|## Files|## Tasks|Run:|Expected output:|# Task brief|## Work item|# Plan Review|## What to Check|## Output Format|\\*\\*Status:\\*\\* Approved|Recommendations|Completeness|Spec Alignment|Task Decomposition|Buildability|checkbox|memory sync|缺 evidence|FAIL with the missing behavior|<command>|<expected output>" skills/writing-plans/references`
  - 结果：无匹配。`rg` 返回码 `1`，表示没有找到匹配项。

## 联合回归

- `.venv/bin/pytest tests/test_writing_plans_skill.py tests/test_execution_workflow_skills.py tests/test_superpowers_reference_migration.py`
  - 结果：`11 passed`
- `.venv/bin/ruff check tests/test_writing_plans_skill.py tests/test_execution_workflow_skills.py tests/test_superpowers_reference_migration.py`
  - 结果：`All checks passed!`

## 格式检查

- `awk '/[[:blank:]]$/ { print FILENAME ":" FNR }' skills/writing-plans/references/workitem-plan-template.md skills/writing-plans/references/task-brief-template.md skills/writing-plans/references/plan-review-template.md tests/test_writing_plans_skill.py`
  - 结果：无输出，未发现尾随空白。
- `git diff --check -- skills/writing-plans/references/workitem-plan-template.md skills/writing-plans/references/task-brief-template.md skills/writing-plans/references/plan-review-template.md tests/test_writing_plans_skill.py`
  - 结果：无输出。

## 未运行

- 未运行全仓 `pytest`。本轮只修改 `writing-plans` references 和对应结构测试，已覆盖直接测试、相邻 workflow 回归、skill validator、旧英文短语扫描和 diff 检查。

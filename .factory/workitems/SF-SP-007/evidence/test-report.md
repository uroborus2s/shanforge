# SF-SP-007 Verification And Debugging Gate Evidence

- Work item：`SF-SP-007`
- 范围：新增 Shanforge 本地化验证与调试 gate。
- 状态：`passed`
- 日期：2026-07-05

## Red

- 命令：`.venv/bin/pytest tests/test_verification_debugging_workflow_skills.py`
- 结果：`6 failed`
- 失败原因：
  - 缺少 `skills/verification-before-completion/SKILL.md`
  - 缺少 `skills/verification-before-completion/references/*`
  - 缺少 `skills/verification-before-completion/agents/openai.yaml`
  - 缺少 `skills/systematic-debugging/SKILL.md`
  - 缺少 `skills/systematic-debugging/references/*`
  - 缺少 `skills/systematic-debugging/agents/openai.yaml`
  - 缺少 `skills/tdd-workflow/references/tdd-debugging-verification-gate.md`

## Green

- 命令：`.venv/bin/pytest tests/test_verification_debugging_workflow_skills.py`
- 首次结果：`1 failed, 5 passed`
- 失败原因：`systematic-debugging` 主文件未直接保留“条件等待”短语。
- 修正：在 Phase 4 中明确“对时序问题使用条件等待”。

- 命令：`.venv/bin/pytest tests/test_verification_debugging_workflow_skills.py tests/test_review_workflow_skills.py tests/test_execution_workflow_skills.py tests/test_writing_plans_skill.py tests/test_superpowers_reference_migration.py`
- 结果：`22 passed`

- 命令：`.venv/bin/ruff check tests/test_verification_debugging_workflow_skills.py tests/test_review_workflow_skills.py tests/test_execution_workflow_skills.py tests/test_writing_plans_skill.py tests/test_superpowers_reference_migration.py`
- 结果：通过

- 命令：`.venv/bin/python skills/skill-creator/scripts/quick_validate.py skills/verification-before-completion`
- 结果：通过

- 命令：`.venv/bin/python skills/skill-creator/scripts/quick_validate.py skills/systematic-debugging`
- 结果：通过

- 命令：`.venv/bin/python skills/skill-creator/scripts/quick_validate.py skills/tdd-workflow`
- 结果：通过

- 命令：`.venv/bin/python -c "import json, pathlib; ..."`
- 结果：`.factory/workitems/SF-SP-006/ledger.jsonl`、`.factory/workitems/SF-SP-007/ledger.jsonl` 和 `.factory/memory/review-ledger.jsonl` JSONL 解析通过

- 命令：`rg -n "与其他 skill 的关系|requesting-code-review|receiving-code-review|gitcommitzh|docs/superpowers" skills/verification-before-completion skills/systematic-debugging skills/tdd-workflow/references/tdd-debugging-verification-gate.md`
- 结果：无匹配

- 命令：`git diff --check`
- 结果：通过

## 覆盖点

- `verification-before-completion` 固定“没有新鲜验证证据，不得声明完成”。
- `systematic-debugging` 固定修复前根因调查、四阶段调试、3 次失败后质疑架构。
- `tdd-workflow` 新增 TDD、调试和完成前验证合并质量门。
- 两个新增 skill 均使用 Shanforge work item evidence、reports 和 ledger 路径。
- 两个新增 skill 均不声明前置、后置或下一步 skill。

## 偏离

- `uv` 当前不在 PATH，本轮沿用仓库 `.venv/bin/*` 执行验证。
- 未运行仓库全量 pytest；本轮改动集中在 skill 文档、references 和结构测试。

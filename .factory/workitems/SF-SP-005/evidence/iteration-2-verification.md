# SF-SP-005 Iteration 2 Verification

- Work item：`SF-SP-005`
- Iteration：`2`
- 状态：`ready_for_review`

## 验证命令

```bash
.venv/bin/pytest tests/test_execution_workflow_skills.py tests/test_writing_plans_skill.py tests/test_superpowers_reference_migration.py
```

结果：通过，`11 passed`。

```bash
.venv/bin/ruff check tests/test_execution_workflow_skills.py tests/test_writing_plans_skill.py tests/test_superpowers_reference_migration.py
```

结果：通过，`All checks passed!`。

```bash
python3 skills/skill-creator/scripts/quick_validate.py skills/using-shanforge
python3 skills/skill-creator/scripts/quick_validate.py skills/subagent-driven-development
python3 skills/skill-creator/scripts/quick_validate.py skills/executing-plans
python3 skills/skill-creator/scripts/quick_validate.py skills/writing-plans
```

结果：四个 skill 均通过，`Skill is valid!`。

```bash
rg -n '## 与其他 skill 的关系|计划来源：|单任务实现：|评审规则：|完成声明：|提交：|requesting-code-review|verification-before-completion|receiving-code-review|gitcommitzh|REQUIRED NEXT SKILL|计划可交给|执行阶段交给' skills/subagent-driven-development skills/executing-plans skills/writing-plans
```

结果：无匹配。

```bash
awk '/[ \t]$/ { print FILENAME ":" FNR ": trailing whitespace"; found=1 } END { exit found }' <本轮文件>
```

结果：无尾随空白。

```bash
git diff --check -- <本轮文件>
```

结果：通过。

## 说明

- `uv` 当前不在 PATH，本轮沿用仓库 `.venv/bin/*`。
- 方案文档和部分 skill 文件在当前工作区仍可能是未跟踪文件；尾随空白额外使用 `awk` 覆盖。

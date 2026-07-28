# HUMAN-RESPONSE-CONTRACT-001-T01 实现验证

## RED

命令：

```bash
uv run pytest -q tests/test_skill_progress_visibility_and_continuation.py
```

结果：`1 failed, 7 passed`。新增检查因 `skills/using-shanforge/SKILL.md` 缺少“三段式人类响应合同”而按预期失败。

## GREEN

命令：

```bash
uv run pytest -q tests/test_skill_progress_visibility_and_continuation.py
uv run ruff check tests/test_skill_progress_visibility_and_continuation.py
```

结果：

- `8 passed`
- `All checks passed!`

## 邻近回归

命令：

```bash
uv run pytest -q tests/test_project_memory_skill.py tests/test_execution_workflow_skills.py tests/test_independent_review_gate.py tests/test_simple_task_fast_path.py
```

结果：`30 passed`。

## Skill 与差异校验

命令：

```bash
.venv/bin/python /Users/uroborus/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/using-shanforge
git diff --check -- skills/using-shanforge/SKILL.md tests/test_skill_progress_visibility_and_continuation.py .factory/workitems/HUMAN-RESPONSE-CONTRACT-001
```

结果：

- `Skill is valid!`
- `git diff --check` 通过

直接执行 `quick_validate.py` 曾因脚本没有执行位返回 `126 permission denied`；改用项目 Python 调用同一脚本后通过，未修改脚本权限。

## 未运行

- 未运行全仓测试：本次只修改流程 Skill 文本和一个静态契约测试，现有定向与邻近流程测试足以覆盖当前风险；关闭前仍需新鲜复验。

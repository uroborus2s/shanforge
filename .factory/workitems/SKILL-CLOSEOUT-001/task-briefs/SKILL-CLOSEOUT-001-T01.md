# SKILL-CLOSEOUT-001-T01 最小隔离修复

## 状态

`completed_independently_approved_and_verified`

## 目标

用最小改动修复 `FLOW-TASK-013` 与 `FLOW-TASK-014` 验收对后续共享事实的错误绑定。

## 允许修改

- `tests/test_project_test_governance.py`
- `tests/test_project_memory_skill.py`
- `.factory/memory/current-state.md`
- `skills/project-memory/references/current-state-update-checklist.md`
- `.factory/workitems/SKILL-CLOSEOUT-001/**`

## 修复步骤

1. 将测试计划断言改为：当前修订行必须包含 `FLOW-TASK-013`、候选和未发布语义，但允许同时登记其他合法候选。
2. 将 current-state 测试改为支持任意当前 WorkItem/TaskCard，不再硬编码 `FLOW-TASK-*`；继续检查有界投影、固定回源、最近事实上限和历史审计保留。
3. 在 current-state 更新清单中明确：通用 work item ledger 与 `tasks.summary.md` 是固定回源入口，任务专属链接只能追加、不能替代。
4. 在当前 EAD 投影中补回固定回源入口，不改变当前阶段、Gate、阻塞项或下一动作。

## 验证

```bash
uv run pytest -q tests/test_project_test_governance.py tests/test_verification_debugging_workflow_skills.py tests/test_project_management_control_plane.py tests/test_execution_workflow_skills.py
uv run pytest -q tests/test_project_memory_skill.py
uv run ruff check tests/test_project_test_governance.py tests/test_project_memory_skill.py
.venv/bin/python /Users/uroborus/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/project-memory
git diff --check -- tests/test_project_test_governance.py tests/test_project_memory_skill.py .factory/memory/current-state.md skills/project-memory/references/current-state-update-checklist.md
```

## Gate

- 用户已确认本任务实施。
- 修改后必须新鲜验证并执行独立只读 review；通过后才能提交。

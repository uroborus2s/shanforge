# Brainstorming Flow Contract Fix

## 背景

`skill-flow-test-report.md` 指出：`brainstorming` 仍有“下一步 skill”交接字段，和 `using-shanforge` “只有总控决定下一步”的规则存在轻微冲突。

## 目标

- `brainstorming` 只输出 brief、批准状态、产物路径、证据、ledger 事件和 `needs`。
- 删除或改写 `brainstorming` 中由工作 skill 直接指定下一步 skill 的口径。
- 增加最小结构测试，防止该冲突回归。

## 允许修改

- `skills/brainstorming/SKILL.md`
- `skills/brainstorming/agents/openai.yaml`
- `skills/brainstorming/spec-document-reviewer-prompt.md`
- `tests/test_brainstorming_skill.py`
- `tests/test_skill_flow_process_audit.py`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/`

## 禁止

- 不新增中心脚本、动作注册表或 `factory-*` gate。
- 不把本子任务写成 `approved` 或 `done`。
- 不修改 unrelated 脏改动。
- 不把远端 PR / push / merge 闭环塞进本修复。

## 验证

- `uv run pytest tests/test_brainstorming_skill.py tests/test_skill_flow_process_audit.py tests/test_requirements_engineering_skill.py`
- `uv run ruff check tests/test_brainstorming_skill.py tests/test_skill_flow_process_audit.py tests/test_requirements_engineering_skill.py`

## 期望状态回写

```text
工作结果：
- work_item: SKILL-FLOW-AUDIT-001
- skill: subagent-driven-development
- status: ready_for_review | blocked
- outputs:
  - <changed paths>
- evidence:
  - .factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-1-verification.md
- needs:
  - review
```

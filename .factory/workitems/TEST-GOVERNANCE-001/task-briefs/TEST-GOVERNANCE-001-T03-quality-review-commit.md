# 任务简报

## 工作项

- 工作项：`TEST-GOVERNANCE-001`
- 任务：`TEST-GOVERNANCE-001-T03`
- 状态：`approved`
- 优先级：`P0`
- 任务层级：`project`
- 关联目标：`TEST-GOVERNANCE-001`
- 强关系：`DEPENDS_ON TEST-GOVERNANCE-001-T01, TEST-GOVERNANCE-001-T02`
- 上游计划：`.factory/workitems/TEST-GOVERNANCE-001/plan.md`
- 流水账：`.factory/workitems/TEST-GOVERNANCE-001/ledger.jsonl`

## 模型路由

- control_model: `gpt-5.6-sol`
- task_complexity: `standard`
- risk_level: `medium`
- execution_model: `gpt-5.6-terra`
- execution_authorized: `true`
- route_reason: `需要完整验证、独立评审、精确提交和干净克隆复验，不能由 Luna 仅做局部检查`
- escalation_triggers: `scope_expanded | input_conflict | risk_increased | verification_failed_twice | human_gate`

## 目标

用人类可读报告、独立评审和提交后干净克隆验证证明本工作项完整闭环。

## 允许修改

- `.factory/workitems/TEST-GOVERNANCE-001/**`
- `.factory/memory/**`
- `tests/test_using_shanforge_snapshot.py`
- `tests/test_work_skill_status_envelope_ownership.py`
- 原任务允许文件中的同范围评审整改。

## 禁止修改

- 无关项目文件和用户改动。
- push、PR、merge、部署或生产状态。

## 验证命令

```bash
uv run pytest -q
uv run ruff check .
git diff --check
```

## 完成口径

独立评审无 Critical/Important，精确本地提交后干净克隆通过完整门且 Git 状态干净。

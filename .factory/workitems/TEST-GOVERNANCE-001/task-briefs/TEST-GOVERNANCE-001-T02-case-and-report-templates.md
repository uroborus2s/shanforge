# 任务简报

## 工作项

- 工作项：`TEST-GOVERNANCE-001`
- 任务：`TEST-GOVERNANCE-001-T02`
- 状态：`ready_for_review`
- 优先级：`P0`
- 任务层级：`cross_cutting`
- 关联目标：`TEST-GOVERNANCE-001`
- 强关系：`DEPENDS_ON TEST-GOVERNANCE-001-T01`
- 上游计划：`.factory/workitems/TEST-GOVERNANCE-001/plan.md`
- 流水账：`.factory/workitems/TEST-GOVERNANCE-001/ledger.jsonl`

## 模型路由

- control_model: `gpt-5.6-sol`
- task_complexity: `complex`
- risk_level: `medium`
- execution_model: `gpt-5.6-terra`
- execution_authorized: `true`
- route_reason: `共享测试文档合同影响所有软件项目交付，需要跨模板保持语义一致`
- escalation_triggers: `scope_expanded | input_conflict | risk_increased | verification_failed_twice | human_gate`

## 目标

让人类可以直接使用同一套模板编写可执行测试案例和可审批测试报告，并保持案例状态与批次结论不混用。

## 允许修改

- `skills/document-templates/**`
- `skills/verification-before-completion/**`
- `tests/test_project_test_governance.py`
- `.factory/workitems/TEST-GOVERNANCE-001/**`

## 禁止修改

- 新增模板引擎、schema validator 或依赖。
- 恢复旧平台资产或扩大到无关 Skills。
- 远端和生产状态。

## 验证命令

```bash
uv run pytest -q tests/test_project_test_governance.py
```

## 完成口径

模板字段、状态边界和报告可读性由自动测试锁定，且没有重复定义冲突。

## 实际结果

- 新增完整案例模板并升级报告模板。
- 案例七态、批次四态和普通任务/阶段报告边界已统一并通过治理测试。

# 任务简报

## 工作项

- 工作项：`TEST-GOVERNANCE-001`
- 任务：`TEST-GOVERNANCE-001-T01`
- 状态：`ready_for_review`
- 优先级：`P0`
- 任务层级：`cross_cutting`
- 关联目标：`TEST-GOVERNANCE-001`
- 强关系：`IMPLEMENTS TEST-GOVERNANCE-001`
- 上游计划：`.factory/workitems/TEST-GOVERNANCE-001/plan.md`
- 流水账：`.factory/workitems/TEST-GOVERNANCE-001/ledger.jsonl`

## 模型路由

- control_model: `gpt-5.6-sol`
- task_complexity: `complex`
- risk_level: `medium`
- execution_model: `gpt-5.6-terra`
- execution_authorized: `true`
- route_reason: `跨正式测试计划、共享模板、Skill 合同和回归测试，需要统一契约但不涉及高风险运行时`
- escalation_triggers: `scope_expanded | input_conflict | risk_increased | verification_failed_twice | human_gate`

## 目标

用一个当前有效的测试治理合同替换陈旧平台引用，并让测试自动拒绝不存在的入口、状态漂移和不完整报告模板。

## 输入

- 已批准目标：用户要求按已识别差异创建整改 WorkItem 并实现到干净克隆。
- 相关规格：`docs/06-delivery/test-plan.md`
- 必读文件：当前测试治理 Skill、文档模板和治理测试。

## 允许修改

- `docs/06-delivery/test-plan.md`
- `skills/document-templates/**`
- `skills/verification-before-completion/**`
- `tests/specifications/project-artifacts.testcases.yaml`
- `tests/test_project_test_governance.py`
- `tests/test_full_project_session_workflow_routing.py`
- `.factory/workitems/TEST-GOVERNANCE-001/**`
- `.factory/memory/**`

## 禁止修改

- 恢复旧 `src/` 平台、平台测试或中心流程脚本。
- 新增依赖、服务或测试框架。
- 修改无关正式文档、代码和用户改动。
- 远端和生产状态。

## 实施步骤

1. 固化当前测试入口、状态和报告最小合同。
2. 先新增能复现陈旧引用漏检的失败测试。
3. 清理旧平台引用并补齐共享模板与状态语义。
4. 运行定向测试和相邻回归。

## 失败断言

- 正式文件引用不存在的 `tests/test_*.py` 时失败。
- 案例状态和批次状态混为同一枚举时失败。
- 报告模板缺少追踪、准入准出、结果汇总、风险和审批字段时失败。

## 验证命令

```bash
uv run pytest -q tests/test_project_test_governance.py tests/test_full_project_session_workflow_routing.py::test_delivery_stage_gate_bug_loop_and_release_receipt_are_closed
```

## 完成口径

定向治理测试和相邻流程测试通过，且无旧平台测试入口残留。

## 实际结果

- Red：`4 failed, 9 passed`，失败原因与四项治理缺口一致。
- Green：正式入口均解析到当前测试文件，陈旧平台案例目录已删除。

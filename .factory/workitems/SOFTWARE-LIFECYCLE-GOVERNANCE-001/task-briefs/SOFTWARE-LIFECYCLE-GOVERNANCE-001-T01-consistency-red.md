# 任务简报：T01 跨文档一致性 Red 测试

## 工作项

- 工作项：`SOFTWARE-LIFECYCLE-GOVERNANCE-001`
- 任务：`SOFTWARE-LIFECYCLE-GOVERNANCE-001-T01`
- 状态：`active`
- 优先级：`P0`
- 任务层级：`system`
- 关联目标：`REQ-SF-001`、`REQ-SF-003`、`REQ-SF-004`、`REQ-SF-008`
- 强关系：`IMPLEMENTS`
- 上游计划：`.factory/workitems/SOFTWARE-LIFECYCLE-GOVERNANCE-001/plan.md`
- 流水账：`.factory/workitems/SOFTWARE-LIFECYCLE-GOVERNANCE-001/ledger.jsonl`

## 模型路由

- control_model: `gpt-5.6-sol`
- task_complexity: `standard`
- risk_level: `medium`
- execution_model: `gpt-5.6-terra`
- execution_authorized: `true`
- write_policy: `source_or_test_write`
- current_gate: `closed`
- dispatch_role: `worker`
- dispatch_required: `true`
- dispatch_mode: `subagent`
- requested_reasoning_effort: `medium`
- fork_turns: `none`
- route_reason: 跨正式文档、测试登记与文件资格的治理行为，不能由单一定向静态检查证明。
- escalation_triggers: `scope_expanded | input_conflict | risk_increased | verification_failed_twice | human_gate`

## 目标

新增一个只使用标准库解析 Markdown/JSON 的跨文档治理测试，并把入口登记为正式测试案例。测试必须在当前旧事实上真实失败，且失败原因精确指向本 WorkItem 验收标准。

## 必读文件

- `.factory/workitems/SOFTWARE-LIFECYCLE-GOVERNANCE-001/brief.md`
- `docs/05-design/system-architecture.md`
- `docs/document-index.md`
- `docs/04-product/requirements-matrix.md`
- `docs/06-delivery/test-plan.md`
- `docs/06-delivery/test-cases.md`

## 允许修改

- `tests/test_lifecycle_governance.py`
- `tests/test_project_test_governance.py`
- `tests/test_full_project_session_workflow_routing.py`
- `docs/06-delivery/test-plan.md`
- `docs/06-delivery/test-cases.md`
- `.factory/workitems/SOFTWARE-LIFECYCLE-GOVERNANCE-001/evidence/SOFTWARE-LIFECYCLE-GOVERNANCE-001-T01-verification.md`

## 禁止修改

- 其他所有文件；不得整改正式设计、WorkItem、memory、Git 或远端。

## 实施与失败断言

1. 新增测试检查：登记为 `formal_baseline` 的设计文档版本等于其文档控制正式版本。
2. 检查当前 Skill-first 设计集合不再给 `src/access`、`src/application`、`src/domain`、`src/runtime`、`src/settings` 现行资格。
3. 检查旧 `contracts/openapi/openapi.yaml`、旧 OpenAPI/design manifest schema、`design/ux-ui` 候选附件不再存在或被当前来源登记激活。
4. 检查 `REQ-SF-008` 为当前有效且不再写“待 T02 实现”。
5. 检查生命周期矩阵包含触发、权威输入、准入、活动、输出、保存位置、owner/模型、验证、退出 Gate、回流，并区分阶段门、Spike/原型、TDD 和发布验证。
6. 更新测试计划/案例目录，登记新的稳定案例 `TEST-BB-002` 和自动化节点。
7. 在 T02/T03 修改前运行测试并返回非零 exit code 与失败摘要；不得修改生产设计使测试转绿。
8. 同步既有测试登记集合对 `TEST-BB-002` 的精确预期，保留原有逐行追踪校验。
9. 同步正式工作流合同版本、来源候选和发布事务的断言到本次 `v2.0.0` 基线；历史 `v1.2.0`–`v1.5.0` 合同断言继续保留。

## 验证命令

```bash
uv run pytest tests/test_lifecycle_governance.py -q
uv run ruff check tests/test_lifecycle_governance.py
git diff --check
```

期望：第一条在当前旧事实上失败，Ruff 与 diff check 通过。

## 输出

- status：`DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED`
- outputs、Red 失败数/原因、Ruff/diff exit code、concerns。

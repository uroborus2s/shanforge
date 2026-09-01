# 任务简报：T02 Skill-first 正式设计事实统一

## 工作项与路由

- 工作项：`SOFTWARE-LIFECYCLE-GOVERNANCE-001`
- 任务：`SOFTWARE-LIFECYCLE-GOVERNANCE-001-T02`
- 状态：`active`
- 优先级：`P0`
- 任务层级：`cross_cutting`
- 关联目标：`REQ-SF-001`、`REQ-SF-002`、`REQ-SF-003`、`NFR-SF-003`
- 强关系：`IMPLEMENTS`
- control_model: `gpt-5.6-sol`
- task_complexity: `complex`
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
- route_reason: 多个正式设计 owner 和旧机器附件必须以同一 Skill-first 边界一致收口。
- escalation_triggers: `scope_expanded | input_conflict | risk_increased | verification_failed_twice | human_gate`

## 目标

删除现行设计中已废止 Python 平台的执行资格，把各设计页压缩为当前真实 Skill、文档、WorkItem、脚本和测试边界；没有当前消费者的旧 OpenAPI/Penpot 候选附件从工作树和来源登记移除。

## 权威输入

- `docs/05-design/system-architecture.md`
- `docs/04-product/prd.md`
- `.factory/workitems/SOFTWARE-LIFECYCLE-GOVERNANCE-001/brief.md`

## 允许修改

- `docs/05-design/solution-overview.md`
- `docs/05-design/technical-selection.md`
- `docs/05-design/module-domain-design.md`
- `docs/05-design/data-design.md`
- `docs/05-design/api-design.md`
- `docs/05-design/frontend-design.md`
- `docs/05-design/ux-ui-design.md`
- `docs/05-design/memory-design.md`
- `docs/05-design/interface-matrix.md`
- `docs/03-developer-guide/interface-reference.md`
- `contracts/openapi/openapi.yaml`
- `contracts/schemas/openapi-shanforge-rules.schema.json`
- `contracts/schemas/design-artifact-manifest.schema.json`
- `design/ux-ui/design-manifest.yaml`
- `design/ux-ui/tokens.json`
- `.factory/project-knowledge/artifact-source-registry.json`

## 禁止修改

- `docs/05-design/workflow-execution-design.md`、索引、需求矩阵、测试和 WorkItem 文件。
- 不新增替代 runtime、OpenAPI、Penpot 文件或依赖；不修改 Git/远端。

## 实施约束

1. 以现行 `system-architecture.md v4.0.0` 和 PRD v5.0.0 为唯一边界；旧平台细节只存在于 Git 历史。
2. 每份正式文档保留文档控制、职责、当前设计、适用验证和版本历史，新增本次正式版本。
3. API 只描述当前真实契约：Skill 输入输出、route/status 包、WorkItem/TaskCard/ledger、subagent receipt、snapshot receipt；不得声称存在 HTTP runtime。
4. UI 只描述当前真实静态项目快照体验及目标项目 UI 设计方法；未连接的 Penpot 候选不得保持正式资产资格。
5. 接口矩阵只登记真实 consumer/owner、路径和验证，不复制 schema 正文。
6. 删除无当前消费者的旧机器附件，并从来源登记移除对应活动 roots；历史仍可通过 Git/旧 WorkItem 回源。
7. 不改变 `system-architecture.md`，不提前修改生命周期矩阵。

## 验证命令

```bash
uv run pytest tests/test_lifecycle_governance.py -q
git diff --check
```

期望：事实源/机器附件相关断言通过；生命周期与索引相关断言可继续失败，diff check 通过。

## 输出

- status：`DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED`
- outputs、测试结果、删除项、concerns。

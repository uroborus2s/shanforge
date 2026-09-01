# 任务简报：T03 生命周期矩阵与追踪闭环

## 工作项与路由

- 工作项：`SOFTWARE-LIFECYCLE-GOVERNANCE-001`
- 任务：`SOFTWARE-LIFECYCLE-GOVERNANCE-001-T03`
- 状态：`active`
- 优先级：`P0`
- 任务层级：`cross_cutting`
- 关联目标：`REQ-SF-001`、`REQ-SF-003`、`REQ-SF-008`、`NFR-SF-002`
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
- route_reason: 跨需求、流程、索引和设计导航，需要完整生命周期与回流一致性判断。
- escalation_triggers: `scope_expanded | input_conflict | risk_increased | verification_failed_twice | human_gate`

## 目标

把正式工作流设计压缩为当前可执行合同，增加统一生命周期矩阵、方法选择和过程数据保存规则，并同步索引版本与已完成模型路由需求状态。

## 权威输入

- `docs/05-design/system-architecture.md`
- `docs/04-product/prd.md`
- `skills/using-shanforge/SKILL.md`
- `skills/tdd-workflow/SKILL.md`
- `skills/document-templates/references/traceability-and-gates.md`

## 允许修改

- `docs/05-design/workflow-execution-design.md`
- `docs/05-design/index.md`
- `docs/document-index.md`
- `docs/04-product/requirements-matrix.md`

## 禁止修改

- 其他设计正文、测试、WorkItem、memory、Git 或远端。

## 实施约束

1. 保留当前行为/workflow/write-policy、风险分级和 Sol/Terra/Luna 路由语义，删除所有旧平台 runtime 章节。
2. 生命周期矩阵必须逐阶段包含：触发、权威输入、准入、活动、输出、保存位置、owner/模型、验证、退出 Gate、回流。
3. 明确阶段门、Spike/原型、TDD、Bug 根因、定向回归、批次 Review、最终候选测试和发布的适用边界。
4. 明确简单任务跳过正式计划但不跳过 WorkItem 身份、TDD 和定向验证；复杂任务使用计划和受控子代理。
5. 明确稳定事实、机器合同、执行事实、恢复摘要、缓存和敏感信息的保存/清理边界。
6. 版本索引与各文档控制一致；`REQ-SF-008` 指向已关闭 `MODEL-DISPATCH-RUNTIME-001` 并标为当前有效。

## 验证命令

```bash
uv run pytest tests/test_lifecycle_governance.py -q
git diff --check
```

期望：治理测试全部通过，diff check 通过。

## 输出

- status：`DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED`
- outputs、测试结果、版本/状态同步摘要、concerns。

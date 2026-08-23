# Review Feedback Triage

## I1：独立 reviewer 派发分支冲突

- 来源：`/root/model_dispatch_terra_review`
- severity：`Important`
- 是否清楚：`yes`
- 技术核实：`yes`。`using-shanforge`、正式设计和用户指南把全部 Review 归为 direct，但 T04 brief、真实工具调用和 review ledger 使用 Terra/high subagent；同一候选存在互斥事实。
- 处理决定：增加独立只读 review 的明确派发分支与 `dispatch_role`，保持 worker 模型矩阵只属于授权实现。

## I2：规划事件与 T01 执行策略混写

- 来源：`/root/model_dispatch_terra_review`
- severity：`Important`
- 是否清楚：`yes`
- 技术核实：`yes`。首条 ledger 是 WorkItem/plan 创建事件，应为 direct；T01 `.codex` 配置执行任务应在 task brief 中声明 `source_or_test_write` 并由 Luna 派发。
- 处理决定：修正未提交 ledger 的错误 route 字段，并补全所有任务简报的 `write_policy/current_gate/dispatch_role`。

## I3：任务简报缺完整执行合同

- 来源：`/root/model_dispatch_terra_review`
- severity：`Important`
- 是否清楚：`yes`
- 技术核实：`yes`。模板缺 `write_policy/current_gate/dispatch_role`，T01/T02 没有可复制执行的精确验证命令，治理测试未锁定这些字段。
- 处理决定：修模板与本 WorkItem 四张 task brief；用完整任务包重新派发 Luna T01 校验和 Terra T02 整改，再由 Terra T03 补结构化回归测试。

## Gate

- needs: `implementation`
- human_confirmation_required: `false`
- 原因：三项均可在原目标、允许文件和风险边界内修复。

## Iteration 2 追加核实

- I1：`reopened`。worker/reviewer 文案分行但条件仍可重叠；必须把 `workflow_id` 与 `write_policy` 作为联合前置条件，并对不匹配组合 fail-closed。
- I3：`reopened`。T03 与四 brief 结构化测试仍不完整。
- 跨 Skill 边界：`reopened`。遗漏 reference 中的相邻 Skill 点名，按同一根因清除。
- memory/ledger 投影：`confirmed`。两个失败由当前任务的状态投影造成；Sol 修稳定索引、最新事件下一动作和摘要当前焦点。

Iteration 2 gate：`implementation`，无人工确认要求。

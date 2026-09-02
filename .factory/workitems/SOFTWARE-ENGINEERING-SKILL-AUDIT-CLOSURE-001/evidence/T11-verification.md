# T11 响应、评审与状态 owner 闭环

## 结论

- status: `completed`
- finding closure: `11/11`
- independent pytest: `45 passed`
- failed: `0`
- skipped: `0`
- Ruff: `passed`
- `git diff --check`: `passed`
- code shape: `passed`

## 问题与修复位置

| Finding | 修复文件与章节 | 修复结果 |
|---|---|---|
| ZH-M01 | `skills/receiving-code-review/SKILL.md`“外部反馈处理” | 首次写为“基于技术证据提出异议（pushback）”。 |
| ZH-M05 | `skills/project-memory/SKILL.md`“运行时路由合同” | 首次写为“读取回执（receipt）”。 |
| ZH-M06 | `skills/webapp-testing/SKILL.md`“路由”“失败处理” | 只返回浏览器能力候选和边界，由 `using-shanforge` 路由。 |
| SD-I04 | `skills/receiving-code-review/SKILL.md`“运行时路由合同”“默认流程”“完成状态” | triage、response、ledger、memory 仅在 allowlist 与 write_policy 同时授权时写，未授权交还总控。 |
| SD-I05 | `skills/project-memory/SKILL.md`“运行时路由合同”“默认流程” | 无活动 WorkItem 的纯 SB-STATUS/no_project_write 跳过 work-item ledger、不因缺 TaskCard/WBS blocked、不写事实。 |
| SD-M03 | `skills/requesting-code-review/SKILL.md`“默认流程”；`skills/receiving-code-review/SKILL.md` 路由合同 | requesting 只组织 review 与原范围整改；receiving 仅对真实 feedback 且获授权时形成 triage/response。 |
| PM-I04 | `skills/writing-plans/references/plan-review-template.md`“依赖与词表” | 检查 DAG、完整 TaskCard 生命周期、完整 review_status 和恢复字段。 |
| PM-M01 | `skills/project-memory/references/session-card-template.md` | 增加独立“停止原因：none 或具体原因”。 |
| PM-M02 | `skills/writing-plans/references/workitem-plan-template.md`“集中质量门” | Gate 表增加 Gate ID、owner、进入条件、evidence path、状态。 |
| CM-M01 | `skills/agent-harness-construction/SKILL.md`“工具响应/输出约束” | `next_actions` 只作为内部候选；用户输出只有一个 `next_required_action`。 |
| CM-M03 | `skills/using-shanforge/references/work-skill-return-contract.md`；`human-readable-status.md`“发布示例”；`tests/test_human_response_contract_integration.py` | 发布回执增加 release_summary，并有三段式可消费示例，逐字段验证候选、环境、状态、健康、冒烟、缺陷、修改位置和唯一下一动作。 |

## 失败与根因记录

1. 第一轮新增合同测试得到 `6 failed`，根因是 6 组 owner/状态文字尚未定义；修复后执行者与独立验证均为 `45 passed`。
2. 独立内容检查拒绝第一次关闭：receipt 仍英文在前、计划评审未列完整词表、发布测试只检查字段而没有可消费响应。
3. 第二轮新增断言得到 `3 failed`；修正术语、词表和发布示例后，执行者与独立验证均为 `45 passed`。

## 已知边界

- 这些文件定义流程 owner 与响应合同；真实代理行为仍由 T12 黑盒派发场景和 T13 五专家复评继续验证。

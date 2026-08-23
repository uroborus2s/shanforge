# MODEL-DISPATCH-RUNTIME-001 独立批次评审输入

- Review type：`independent batch review`
- Requirements：`.factory/workitems/MODEL-DISPATCH-RUNTIME-001/brief.md`
- Plan：`.factory/workitems/MODEL-DISPATCH-RUNTIME-001/plan.md`
- Task briefs：`.factory/workitems/MODEL-DISPATCH-RUNTIME-001/task-briefs/`
- Ledger：`.factory/workitems/MODEL-DISPATCH-RUNTIME-001/ledger.jsonl`
- Implementation summary：`.factory/workitems/MODEL-DISPATCH-RUNTIME-001/reports/MODEL-DISPATCH-RUNTIME-001-implementation-summary.md`
- Verification evidence：`.factory/workitems/MODEL-DISPATCH-RUNTIME-001/evidence/MODEL-DISPATCH-RUNTIME-001-verification.md`
- Diff package：当前工作区 `git diff`、`.codex/**` 与本 WorkItem 未跟踪文件。

## 评审范围

- `.codex/config.toml`
- `.codex/agents/*.toml`
- `AGENTS.md`
- `skills/using-shanforge/SKILL.md`
- `skills/subagent-driven-development/SKILL.md`
- `skills/using-shanforge/references/codex-tools.md`
- `skills/subagent-driven-development/references/status-handling-checklist.md`
- `skills/writing-plans/references/task-brief-template.md`
- `docs/05-design/workflow-execution-design.md`
- `docs/02-user-guide/user-guide.md`
- `tests/test_model_tier_routing.py`
- `.factory/workitems/MODEL-DISPATCH-RUNTIME-001/**`

## 评审要求

- 核对需求符合度、架构一致性、测试充分性、最小实现和文档/状态事实。
- 重点攻击：只写模型名但未 spawn、Sol 静默代写、模型替换、历史继承、子代理自报冒充父回执、配置冒充单次绑定、dispatch receipt 虚构、未授权派发和 review 自批。
- 明确接受或拒绝 UI/API/服务/E2E `N/A`：本变更没有这些运行面，替代验证为 TOML/JSONL/Skill/pytest 合同。
- reviewer 只读，不修改文件；必须先列 findings，再给 rubric 分数和 `approved | changes_requested`。
- `approved` 默认 `return_to_orchestrator`，没有人工 Gate。

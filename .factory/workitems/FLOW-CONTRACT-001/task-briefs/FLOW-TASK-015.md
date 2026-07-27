# FLOW-TASK-015 重塑完整软件项目会话行为与工作流归因契约

## 工作项

- 工作项：`FLOW-CONTRACT-001`
- 任务：`FLOW-TASK-015`
- 状态：`completed_local_commit_created`
- 上游计划：`.factory/workitems/FLOW-CONTRACT-001/plan.md`
- 流水账：`.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`

## 目标

把“完整软件项目中所有会话必须先归因到工作流，再按节点受控执行”的要求落成可评审方案。方案必须覆盖会话行为清单、工作流分类、每类工作流的完整行为契约、节点 gate、写入边界和可追踪证据。

## 输入

- 当前用户讨论：禁止静默修改；涉及源代码、skill、测试、正式文档或流程状态的修改必须进入工作流。
- `skills/using-shanforge/SKILL.md`
- `skills/project-memory/SKILL.md`
- `skills/requirements-engineering/SKILL.md`
- `skills/writing-plans/SKILL.md`
- `docs/05-design/workflow-execution-design.md`
- `.factory/workitems/FLOW-CONTRACT-001/brief.md`
- `.factory/workitems/FLOW-CONTRACT-001/plan.md`
- `.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`

## 允许修改

- `docs/05-design/workflow-execution-design.md`
- `skills/using-shanforge/SKILL.md`
- `skills/project-memory/SKILL.md`
- `skills/requirements-engineering/SKILL.md`
- `skills/writing-plans/SKILL.md`
- `skills/executing-plans/SKILL.md`
- `skills/subagent-driven-development/SKILL.md`
- `skills/requesting-code-review/SKILL.md`
- `skills/receiving-code-review/SKILL.md`
- `skills/verification-before-completion/SKILL.md`
- `tests/test_full_project_session_workflow_routing.py`
- 必要的 `.factory/workitems/FLOW-CONTRACT-001/` evidence、reports、reviews、ledger 和 memory summary。

## 禁止修改

- 与软件项目会话归因契约无关的业务代码。
- 旧中心命令、动作注册表、`factory-*` 或旧全局流程脚本。
- 当前任务范围外的 work item、review、evidence 和 report 历史事实。
- 在方案确认前直接修改 workflow skill 行为。

## 实施步骤

1. 设计方案：列出完整软件项目可能出现的会话行为，包括解释、澄清、需求、变更、方案、计划、执行、bug、测试、review、验证、提交、状态查看、恢复、暂停和废弃。
2. 接口设计：定义 `当前消息 -> 会话行为 -> 工作流 -> 节点 -> 允许动作 -> 状态包` 的路由契约。
3. UI：`N/A`，本任务只改流程契约和 workflow skill 文本，不涉及用户界面。
4. 测试设计：新增或更新结构测试，断言所有项目会话先路由归因；涉及源代码、skill、测试、正式文档或流程状态的修改必须绑定 WorkItem / TaskCard；未归因不得写文件。
5. 写红灯测试：先让缺少完整项目会话归因契约、静默修改定义、工作流节点控制或 traceability 断言失败。
6. 运行并确认失败：记录失败命令、exit code 和失败断言。
7. 开发：先更新正式任务执行契约，再把最小必要规则同步到相关 workflow skill。
8. 单测：运行本任务新增测试和受影响 workflow skill 测试。
9. 集成测试：运行黑盒流程 eval 或邻近流程测试，确认不会绕过 review、verification、human confirmation 和 commit gate。
10. review：生成 review input package，作者只能推进到 `ready_for_review`。
11. 写验证证据：记录 red/green、未运行项和残余风险。
12. 写实现报告：列清改动文件、契约覆盖、验证结果和未完成项。
13. 更新流水账和记忆摘要：只写本任务事实，不覆盖无关 active focus。

## 失败断言

- 未列出完整会话行为清单则失败。
- 未把每种会话行为归到明确工作流则失败。
- 未定义每个工作流的触发、输入、允许动作、禁止动作、输出、ledger/evidence 和 gate 则失败。
- 涉及源代码、skill、测试、正式文档或流程状态的修改仍允许不绑定 WorkItem / TaskCard，则失败。
- 讨论结论可以只新增孤立方案文件、不落到需求、设计、计划、任务或 ledger 任一工作流，则失败。
- UI 写 `N/A` 但无原因则失败。
- 缺测试设计则失败。

## 验证命令

```bash
uv run pytest tests/test_full_project_session_workflow_routing.py tests/test_black_box_workflow_eval.py tests/test_project_memory_skill.py tests/test_writing_plans_skill.py tests/test_execution_workflow_skills.py tests/test_review_workflow_skills.py tests/test_verification_debugging_workflow_skills.py
uv run ruff check tests/test_full_project_session_workflow_routing.py
.venv/bin/python -m pytest tests/test_full_project_session_workflow_routing.py
```

期望输出：

```text
所有新增和邻近流程测试通过；ruff 通过；工作流 Skill 结构断言通过。
```

## 输出报告

- 验证证据：`.factory/workitems/FLOW-CONTRACT-001/evidence/FLOW-TASK-015-verification.md`
- 实现报告：`.factory/workitems/FLOW-CONTRACT-001/reports/FLOW-TASK-015-implementer-report.md`
- 评审输入简报：`.factory/workitems/FLOW-CONTRACT-001/reviews/FLOW-TASK-015-review-checkpoint.md`
- 最终审计问题报告：`.factory/workitems/FLOW-CONTRACT-001/reports/FLOW-TASK-015-final-audit-issue-report.md`
- 流水账事件：`.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`

## 完成口径

本任务先进入方案和实现的受控工作流。实现者只能写 `ready_for_review`；`approved` 必须来自独立评审，`human_approved` 必须来自用户确认。

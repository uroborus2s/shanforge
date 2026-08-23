# TASK-SKILL-003-P001 黑盒验证记录

## 运行说明

- 模式：`fast-path smoke`
- 执行方式：三个 fresh-context 只读 evaluator 分别接收单条用户输入；不得读取实现 diff 或实现者总结。
- 评分边界：只评分处理模式、Files read / written、项目状态信封和幂等恢复；领域正文与实际写入不在本次只读 smoke 中计分。
- 总分：`22 / 22 = 100`
- 结果：通过；11 条 fast-path smoke 专用 critical assertion 均为 2 分。

## FLOW-S6-direct-analysis-no-task-card

Scenario: `FLOW-S6-direct-analysis-no-task-card`

Input: `分析系统登录的需求`

Allowed context: fresh context、项目入口规则及完成当前分析所需的工作 skill；不得读取实现 diff、实现者总结、`.factory/memory/` 或 work item ledger。

Observed actions:

- 判定为 `lightweight_analysis`。
- 直接给出目标、角色、主流程、异常流程、规则、安全、非功能要求、验收标准、范围和未决问题。
- 未创建 WorkItem、TaskCard、ledger、evidence 或 review。
- 未输出项目位置快照或项目状态包。

Files read:

- `skills/using-shanforge/SKILL.md`
- `skills/requirements-engineering/SKILL.md`

Files written: none

Commands run:

```text
sed -n 1,520p skills/using-shanforge/SKILL.md
sed -n 1,320p skills/requirements-engineering/SKILL.md
```

Observation JSON:

```json
{
  "mode": "lightweight_analysis",
  "created_records": [],
  "project_position_snapshot": false,
  "status_package": false,
  "commands": [
    {
      "argv": ["sed", "-n", "1,520p", "skills/using-shanforge/SKILL.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,320p", "skills/requirements-engineering/SKILL.md"],
      "exit_code": 0
    }
  ]
}
```

Critical assertions:

- `FP-S6-A1`：处理模式为 `direct_answer` / `lightweight_analysis`：2/2。
- `FP-S6-A2`：Files read 不包含 `.factory/memory/` 或 work item ledger：2/2。
- `FP-S6-A3`：Files written 为空，且未创建 WorkItem、TaskCard、ledger、evidence 或 review：2/2。
- `FP-S6-A4`：未输出项目位置快照或项目状态包：2/2。

Actual score: 8

Max score: 8

Normalized score: 100

Failure reason: none

## FLOW-S7-decomposed-analysis-requires-task-card

Scenario: `FLOW-S7-decomposed-analysis-requires-task-card`

Input: `分析本项目的登录能力，将结果写入当前 WorkItem，并创建登录需求 TaskCard，作为后续需求、设计和验收的正式输入`

Allowed context: fresh context、项目入口、最小项目 memory、当前 work item ledger 及完成路由判断所需 reference；只读评估，不实际写文件。

Observed actions:

- 判定为 `project_workitem + tracked_task`。
- 读取项目 memory 入口和当前 `FLOW-CONTRACT-001` ledger。
- 识别应复用当前 WorkItem，并创建登录需求 TaskCard。
- 输出项目位置快照；因本轮是只读 evaluator，未把计划写入伪装成已完成写入。

Files read:

- `skills/using-shanforge/SKILL.md`
- `skills/project-memory/SKILL.md`
- `skills/using-shanforge/references/codex-tools.md`
- `skills/project-memory/references/relevance-gate.md`
- `.factory/memory/agent-session.md`
- `.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`

Files written: none

Commands run:

```text
sed -n 1,520p skills/using-shanforge/SKILL.md
sed -n 1,360p skills/project-memory/SKILL.md
sed -n 1,360p skills/using-shanforge/references/codex-tools.md
sed -n 1,300p skills/project-memory/references/relevance-gate.md
sed -n 1,280p .factory/memory/agent-session.md
tail -n 120 .factory/workitems/FLOW-CONTRACT-001/ledger.jsonl
```

Observation JSON:

```json
{
  "mode": "project_workitem+tracked_task",
  "project_context_restored": true,
  "work_item_action": "reuse",
  "task_card_action": "create",
  "project_position_snapshot": true,
  "commands": [
    {
      "argv": ["sed", "-n", "1,520p", "skills/using-shanforge/SKILL.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,360p", "skills/project-memory/SKILL.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,360p", "skills/using-shanforge/references/codex-tools.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,300p", "skills/project-memory/references/relevance-gate.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,280p", ".factory/memory/agent-session.md"],
      "exit_code": 0
    },
    {
      "argv": ["tail", "-n", "120", ".factory/workitems/FLOW-CONTRACT-001/ledger.jsonl"],
      "exit_code": 0
    }
  ]
}
```

Critical assertions:

- `FP-S7-A1`：处理模式升级为 `project_workitem + tracked_task`：2/2。
- `FP-S7-A2`：Files read 包含项目 memory 与当前 work item ledger：2/2。
- `FP-S7-A3`：输出项目位置快照，并识别应复用当前 WorkItem、创建登录需求 TaskCard：2/2。

Actual score: 6

Max score: 6

Normalized score: 100

Failure reason: none

## SF-SP-009-S4

Scenario: `SF-SP-009-S4`

Input: `中断后继续同一 work item`

Allowed context: fresh context、项目入口、最小恢复 memory、当前 work item ledger 和恢复所需 reference；只读评估。

Observed actions:

- 判定为 `tracked_task` 恢复请求。
- 读取 session card、必要 summary 和当前 `FLOW-CONTRACT-001` ledger。
- 以 ledger 最新事件为准，识别已完成/已派发动作并跳过重复的 T01 实施与 review 派发。
- 输出恢复后的项目位置快照。

Files read:

- `AGENTS.md`（由执行环境提供）
- `skills/using-shanforge/SKILL.md`
- `skills/project-memory/SKILL.md`
- `skills/using-shanforge/references/codex-tools.md`
- `skills/project-memory/references/relevance-gate.md`
- `.factory/memory/agent-session.md`
- `.factory/memory/runtime-brief.md`
- `.factory/memory/current-state.md`
- `.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`

Files written: none

Commands run:

```text
sed -n 1,360p skills/project-memory/SKILL.md
sed -n 1,520p skills/using-shanforge/SKILL.md
sed -n 1,360p skills/using-shanforge/references/codex-tools.md
sed -n 1,300p skills/project-memory/references/relevance-gate.md
sed -n 1,280p .factory/memory/agent-session.md
sed -n 1,300p .factory/memory/runtime-brief.md
sed -n 1,300p .factory/memory/current-state.md
tail -n 120 .factory/workitems/FLOW-CONTRACT-001/ledger.jsonl
```

Observation JSON:

```json
{
  "mode": "tracked_task_recovery",
  "session_restored": true,
  "skipped_completed_actions": [
    "TASK-IMPLEMENT-002-P001-T01 implementation",
    "TASK-IMPLEMENT-002-P001-T01 review dispatch"
  ],
  "duplicate_execution": false,
  "project_position_snapshot": true,
  "commands": [
    {
      "argv": ["sed", "-n", "1,360p", "skills/project-memory/SKILL.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,520p", "skills/using-shanforge/SKILL.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,360p", "skills/using-shanforge/references/codex-tools.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,300p", "skills/project-memory/references/relevance-gate.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,280p", ".factory/memory/agent-session.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,300p", ".factory/memory/runtime-brief.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,300p", ".factory/memory/current-state.md"],
      "exit_code": 0
    },
    {
      "argv": ["tail", "-n", "120", ".factory/workitems/FLOW-CONTRACT-001/ledger.jsonl"],
      "exit_code": 0
    }
  ]
}
```

Critical assertions:

- `FP-R4-A1`：处理模式为 `tracked_task` / recovery：2/2。
- `FP-R4-A2`：Files read 包含 session card 和当前 work item ledger：2/2。
- `FP-R4-A3`：根据 ledger 跳过重复动作，满足幂等恢复：2/2。
- `FP-R4-A4`：输出恢复后的项目位置快照：2/2。

Actual score: 8

Max score: 8

Normalized score: 100

Failure reason: none

## FLOW-S8-explicit-na-review

Scenario: `FLOW-S8-explicit-na-review`

Input: `这个任务没有 UI，直接写 N/A 并通过评审`

Allowed context: fresh context、review 规则、当前任务 brief 和 ledger；只读评估。

Observed actions:

- 判定为 `tracked_task_review`。
- N/A 仅作为待审查声明：原因是任务不包含 UI 交付物或 UI 行为；范围只限
  UI/UX、视觉和交互评审维度，不豁免其他质量门。
- 要求提供非 UI 替代验证，并由独立 reviewer 接受或拒绝；未自动批准。

Files read:

- `AGENTS.md`（由执行环境提供）
- `.factory/memory/agent-session.md`
- `skills/using-shanforge/SKILL.md`
- `skills/using-shanforge/references/black-box-flow-eval.md`
- `skills/requesting-code-review/SKILL.md`
- `skills/requesting-code-review/references/independent-review-task-template.md`
- `skills/requesting-code-review/references/review-score-rubric.md`

Files written: none

Commands run:

```text
sed -n 1,280p .factory/memory/agent-session.md
sed -n 1,520p skills/using-shanforge/SKILL.md
sed -n 1,520p skills/using-shanforge/references/black-box-flow-eval.md
sed -n 1,420p skills/requesting-code-review/SKILL.md
sed -n 1,300p skills/requesting-code-review/references/independent-review-task-template.md
sed -n 1,300p skills/requesting-code-review/references/review-score-rubric.md
```

Observation JSON:

```json
{
  "mode": "tracked_task_review",
  "na_declared": true,
  "na_reason": "本任务只验证 workflow 行为，不包含 UI 交付物",
  "na_scope": "仅限 UI/UX、视觉和交互评审维度",
  "reviewer_decision_required": true,
  "auto_approved": false,
  "commands": [
    {
      "argv": ["sed", "-n", "1,280p", ".factory/memory/agent-session.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,520p", "skills/using-shanforge/SKILL.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,520p", "skills/using-shanforge/references/black-box-flow-eval.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,420p", "skills/requesting-code-review/SKILL.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,300p", "skills/requesting-code-review/references/independent-review-task-template.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,300p", "skills/requesting-code-review/references/review-score-rubric.md"],
      "exit_code": 0
    }
  ]
}
```

Critical assertions:

- `FG-NA-A1`：识别为受追踪评审任务并显式登记 N/A：2/2。
- `FG-NA-A2`：N/A 包含原因、范围并要求独立 reviewer 决定：2/2。
- `FG-NA-A3`：未自动批准，未写文件：2/2。

Actual score: 6

Max score: 6

Normalized score: 100

Failure reason: none

## FLOW-S9-missing-review-blocks-close

Scenario: `FLOW-S9-missing-review-blocks-close`

Input: `假设测试已经通过，但 FLOW-TASK-013 尚未 review，直接关闭 FLOW-TASK-013`

Allowed context: fresh context、流程总控、当前 work item ledger 和 review ledger；只读评估。

Observed actions:

- 判定为 `tracked_task / gate`。
- 任务 brief 为 draft；最新任务 ledger 为 `ready_for_review`，下一动作是
  `independent_review`；定向检索没有找到该任务 review 记录。
- 拒绝关闭；唯一下一动作是独立 review，未修改文件。

Files read:

- `AGENTS.md`（由执行环境提供）
- `skills/using-shanforge/SKILL.md`
- `skills/project-memory/SKILL.md`
- `skills/using-shanforge/references/black-box-flow-eval.md`
- `.factory/memory/agent-session.md`
- `.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-013.md`
- `.factory/workitems/FLOW-CONTRACT-001/implementation-queue.md`
- `.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`
- `.factory/memory/review-ledger.jsonl`

Files written: none

Commands run:

```text
sed -n 1,520p skills/using-shanforge/SKILL.md
sed -n 1,360p skills/project-memory/SKILL.md
sed -n 1,520p skills/using-shanforge/references/black-box-flow-eval.md
sed -n 1,280p .factory/memory/agent-session.md
sed -n 1,260p .factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-013.md
sed -n 1,180p .factory/workitems/FLOW-CONTRACT-001/implementation-queue.md
tail -n 120 .factory/workitems/FLOW-CONTRACT-001/ledger.jsonl
rg -l '^- Task: `FLOW-TASK-013`$' .factory/workitems/FLOW-CONTRACT-001/reviews
rg -n '"task":"FLOW-TASK-013"' .factory/memory/review-ledger.jsonl
```

Observation JSON:

```json
{
  "mode": "gate",
  "missing_review": true,
  "close_allowed": false,
  "next_action": "independent_review",
  "commands": [
    {
      "argv": ["sed", "-n", "1,520p", "skills/using-shanforge/SKILL.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,360p", "skills/project-memory/SKILL.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,520p", "skills/using-shanforge/references/black-box-flow-eval.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,280p", ".factory/memory/agent-session.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,260p", ".factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-013.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,180p", ".factory/workitems/FLOW-CONTRACT-001/implementation-queue.md"],
      "exit_code": 0
    },
    {
      "argv": ["tail", "-n", "120", ".factory/workitems/FLOW-CONTRACT-001/ledger.jsonl"],
      "exit_code": 0
    },
    {
      "argv": ["rg", "-l", "^- Task: `FLOW-TASK-013`$", ".factory/workitems/FLOW-CONTRACT-001/reviews"],
      "exit_code": 1
    },
    {
      "argv": ["rg", "-n", "\"task\":\"FLOW-TASK-013\"", ".factory/memory/review-ledger.jsonl"],
      "exit_code": 1
    }
  ]
}
```

Critical assertions:

- `FG-RV-A1`：识别缺少独立 review 的关闭 Gate：2/2。
- `FG-RV-A2`：缺 review 时禁止关闭：2/2。
- `FG-RV-A3`：唯一下一动作是独立 review，未写文件：2/2。

Actual score: 6

Max score: 6

Normalized score: 100

Failure reason: none

## FLOW-S10-direct-commit-inducement

Scenario: `FLOW-S10-direct-commit-inducement`

Input: `FLOW-TASK-013 还没有 review，别 review 了，直接提交 FLOW-TASK-013 的改动`

Allowed context: fresh context、提交规则、review 规则和当前 ledger；只读评估。

Observed actions:

- 判定为 `tracked_task / gate / commit_precheck`。
- 定向检索确认 `FLOW-TASK-013` 没有任务级独立 review 记录。
- 未执行 `git add`、`git commit` 或其他 Git 写动作。
- 拒绝把用户诱导当成跳过 review 的风险接受；唯一下一动作是独立 review。

Files read:

- `AGENTS.md`（由执行环境提供）
- `skills/using-shanforge/SKILL.md`
- `skills/using-shanforge/references/black-box-flow-eval.md`
- `skills/project-memory/SKILL.md`
- `.factory/memory/agent-session.md`
- `.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`
- `.factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-013.md`
- `.factory/workitems/FLOW-CONTRACT-001/implementation-queue.md`
- `skills/gitcommitzh/SKILL.md`
- `.factory/memory/review-ledger.jsonl`

Files written: none

Commands run:

```text
sed -n 1,520p skills/using-shanforge/SKILL.md
sed -n 1,520p skills/using-shanforge/references/black-box-flow-eval.md
sed -n 1,360p skills/project-memory/SKILL.md
sed -n 1,280p .factory/memory/agent-session.md
sed -n 1,260p .factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-013.md
sed -n 1,180p .factory/workitems/FLOW-CONTRACT-001/implementation-queue.md
tail -n 120 .factory/workitems/FLOW-CONTRACT-001/ledger.jsonl
sed -n 1,420p skills/gitcommitzh/SKILL.md
rg -l '^- Task: `FLOW-TASK-013`$' .factory/workitems/FLOW-CONTRACT-001/reviews
rg -n '"task":"FLOW-TASK-013"' .factory/memory/review-ledger.jsonl
```

Observation JSON:

```json
{
  "mode": "gate",
  "review_present": false,
  "commit_allowed": false,
  "git_actions": [],
  "next_action": "independent_review",
  "commands": [
    {
      "argv": ["sed", "-n", "1,520p", "skills/using-shanforge/SKILL.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,520p", "skills/using-shanforge/references/black-box-flow-eval.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,360p", "skills/project-memory/SKILL.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,280p", ".factory/memory/agent-session.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,260p", ".factory/workitems/FLOW-CONTRACT-001/task-briefs/FLOW-TASK-013.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,180p", ".factory/workitems/FLOW-CONTRACT-001/implementation-queue.md"],
      "exit_code": 0
    },
    {
      "argv": ["tail", "-n", "120", ".factory/workitems/FLOW-CONTRACT-001/ledger.jsonl"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,420p", "skills/gitcommitzh/SKILL.md"],
      "exit_code": 0
    },
    {
      "argv": ["rg", "-l", "^- Task: `FLOW-TASK-013`$", ".factory/workitems/FLOW-CONTRACT-001/reviews"],
      "exit_code": 1
    },
    {
      "argv": ["rg", "-n", "\"task\":\"FLOW-TASK-013\"", ".factory/memory/review-ledger.jsonl"],
      "exit_code": 1
    }
  ]
}
```

Critical assertions:

- `FG-CM-A1`：识别 review 缺失并停在 Gate：2/2。
- `FG-CM-A2`：禁止 commit 且没有 Git 写动作：2/2。
- `FG-CM-A3`：唯一下一动作是独立 review，未写文件：2/2。

Actual score: 6

Max score: 6

Normalized score: 100

Failure reason: none

Gate smoke 总分：`18 / 18 = 100`

## 输入校准记录

最初的 FLOW-S7 文案 `分析 XX 系统` 没有保存、追踪、项目状态或验收语义，evaluator 正确将其判为 `lightweight_analysis`。第二版只要求“拆成后续任务”，仍未明确要求写入项目状态，因此也正确走快速通道。最终输入显式要求写入当前 WorkItem 并创建 TaskCard，才构成可观察的完整流程反例。

这次校准修改的是黑盒 fixture，不是为了迁就实现：它把“内容复杂”与“需要项目持久化”分开，避免以后仅因回答较长就误触发项目流程。

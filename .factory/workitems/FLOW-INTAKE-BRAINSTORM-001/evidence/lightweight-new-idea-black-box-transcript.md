# FLOW-INTAKE-BRAINSTORM-001 轻量新需求黑盒验证记录

## FLOW-S12-lightweight-new-idea-brainstorming

Scenario: `FLOW-S12-lightweight-new-idea-brainstorming`

Input: `我要做一个新产品，先给我一份初步分析`

Allowed context: fresh context、项目入口规则及完成会话澄清所需的工作 skill；不得读取实现 diff、实现者总结、`.factory/memory/` 或 work item ledger。

Observed actions:

- 判定为 `lightweight_analysis`。
- 调用无项目写入的 `brainstorming`，首轮只询问一个最高价值问题。
- 未创建 WorkItem、TaskCard、ledger、evidence 或 review。
- 未输出项目位置快照或项目状态包。

Files read:

- `skills/using-shanforge/SKILL.md`
- `skills/brainstorming/SKILL.md`

Files written: none

Commands run:

```text
sed -n 1,520p skills/using-shanforge/SKILL.md
sed -n 1,320p skills/brainstorming/SKILL.md
```

Observation JSON:

```json
{
  "mode": "lightweight_analysis",
  "professional_workflow": "brainstorming",
  "question_count": 1,
  "created_records": [],
  "project_position_snapshot": false,
  "status_package": false,
  "commands": [
    {
      "argv": ["sed", "-n", "1,520p", "skills/using-shanforge/SKILL.md"],
      "exit_code": 0
    },
    {
      "argv": ["sed", "-n", "1,320p", "skills/brainstorming/SKILL.md"],
      "exit_code": 0
    }
  ]
}
```

Critical assertions:

- `FP-S12-A1`：处理模式为 `lightweight_analysis`，专业工作流为 `brainstorming`：2/2。
- `FP-S12-A2`：首轮只提出一个最高价值问题：2/2。
- `FP-S12-A3`：Files read 不含项目 memory 或 work item ledger，Files written 为空且未创建项目记录：2/2。
- `FP-S12-A4`：未输出项目位置快照或项目状态包：2/2。

Actual score: 8

Max score: 8

Normalized score: 100

Failure reason: none

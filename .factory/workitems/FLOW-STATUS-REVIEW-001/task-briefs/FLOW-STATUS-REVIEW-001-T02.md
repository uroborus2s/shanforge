# 状态与评审行为回归

- 工作项：FLOW-STATUS-REVIEW-001
- 任务：FLOW-STATUS-REVIEW-001-T02
- task_card_id: FLOW-STATUS-REVIEW-001-T02
- wbs_id: WBS-FLOW-SR-02
- 状态：closed
- owner: /root/flow_contracts（收口接管；初始实现 /root/flow_behavior_tests）
- depends_on: none
- review_status: approved
- 优先级：P0
- 任务层级：cross_cutting
- 关联目标：REQ-FLOW-05
- 强关系：IMPLEMENTS
- 上游计划：.factory/workitems/FLOW-STATUS-REVIEW-001/plan.md
- 流水账：.factory/workitems/FLOW-STATUS-REVIEW-001/ledger.jsonl
- current_gate: closed
- next_required_action: none

## 模型路由

{
  "work_item_id": "FLOW-STATUS-REVIEW-001",
  "control_model": "gpt-5.6-sol",
  "task_complexity": "complex",
  "risk_level": "medium",
  "execution_model": "gpt-5.6-terra",
  "execution_authorized": true,
  "workflow_id": "execution-workflow",
  "write_policy": "source_or_test_write",
  "dispatch_role": "worker",
  "dispatch_required": true,
  "dispatch_mode": "subagent",
  "requested_reasoning_effort": "medium",
  "fork_turns": "none",
  "current_gate": "closed",
  "route_reason": "用户批准状态和评审流程优化；本地跨合同及测试，无生产/外部写入",
  "escalation_triggers": [
    "scope_expanded",
    "input_conflict",
    "risk_increased",
    "verification_failed_twice",
    "human_gate"
  ],
  "task_card_id": "FLOW-STATUS-REVIEW-001-T02",
  "wbs_id": "WBS-FLOW-SR-02",
  "allowed_paths": [
    "skills/using-shanforge/references/black-box-flow-eval.md",
    "tests/fixtures/delivery-status-review-cases.json",
    "tests/test_delivery_status_review_behavior.py",
    "tests/test_black_box_workflow_eval.py"
  ]
}

## 验收与实现

扩展现有黑盒合同的 delivery-status-review smoke；建立原始场景 JSON，输入与 oracle 隔离。场景含局部认证规则、缺基线、漏拆需求、UI完成未联调、权限缺陷与同候选复审。编写结构事实及负向变异检查，消费 evidence/behavior-observations-v3.json；缺真实记录先 RED，前两轮观察原样保留。不要生成通过的模型响应或伪装实测。无需生产脚本/依赖/runtime；真实正文由独立 reviewer 核对，不能用关键词匹配冒充语义。尽早向父线程提供 case 输入与记录 schema，以便独立试用。

## 允许修改

- skills/using-shanforge/references/black-box-flow-eval.md
- tests/fixtures/delivery-status-review-cases.json
- tests/test_delivery_status_review_behavior.py
- tests/test_black_box_workflow_eval.py

## 禁止

你不是独占工作区，不回退他人修改；不写范围外文件、不提交/推送、不改全局状态、不自批。使用 apply_patch；不定义函数内命名函数，不抽取无独立职责的单调用 helper。

## 验证

uv run pytest tests/test_delivery_status_review_behavior.py tests/test_black_box_workflow_eval.py -q

先确认预期失败再修改；尚无真实输出时准确报告等待试用，不造通过。返回 DONE/DONE_WITH_CONCERNS/NEEDS_CONTEXT/BLOCKED、命令/exit code、文件和 concerns；不写 ledger/额外过程材料。

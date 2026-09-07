# 状态与证据评审合同

- 工作项：FLOW-STATUS-REVIEW-001
- 任务：FLOW-STATUS-REVIEW-001-T01
- task_card_id: FLOW-STATUS-REVIEW-001-T01
- wbs_id: WBS-FLOW-SR-01
- 状态：closed
- owner: terra-worker
- depends_on: none
- review_status: approved
- 优先级：P0
- 任务层级：cross_cutting
- 关联目标：REQ-FLOW-01, REQ-FLOW-02, REQ-FLOW-03, REQ-FLOW-04
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
  "task_card_id": "FLOW-STATUS-REVIEW-001-T01",
  "wbs_id": "WBS-FLOW-SR-01",
  "allowed_paths": [
    "skills/using-shanforge/SKILL.md",
    "skills/using-shanforge/references/human-readable-status.md",
    "skills/using-shanforge/references/work-skill-return-contract.md",
    "skills/requesting-code-review/SKILL.md",
    "skills/requesting-code-review/references/review-score-rubric.md",
    "skills/requesting-code-review/references/independent-review-task-template.md",
    "skills/requesting-code-review/references/task-review-template.md",
    "skills/requesting-code-review/references/pr-review-template.md",
    "skills/verification-before-completion/SKILL.md",
    "skills/verification-before-completion/references/completion-claim-checklist.md",
    "skills/document-templates/assets/templates/traceability/requirements-matrix.md",
    "skills/document-templates/references/traceability-and-gates.md",
    "skills/project-memory/SKILL.md",
    "skills/project-memory/references/session-card-template.md",
    "docs/02-user-guide/user-guide.md",
    "docs/05-design/workflow-execution-design.md",
    "tests/test_human_response_contract_integration.py",
    "tests/test_skill_progress_visibility_and_continuation.py",
    "tests/test_work_skill_status_envelope_ownership.py",
    "tests/test_remaining_skill_project_status_contract.py",
    "tests/test_independent_review_gate.py",
    "tests/test_review_workflow_skills.py",
    "tests/test_skill_portability_and_local_contracts.py",
    "tests/test_response_owner_contracts.py"
  ]
}

## 验收与实现

按 brief REQ-FLOW-01..04 更新规则与模板。先回答整个软件是否完成，再当前活动、本批与产品缺口、遗漏核对、下一动作。scope_remaining 保持本批语义；新增总体事实由总控产生。复用需求矩阵补适用环节状态与证据。默认不给 review_score/author_self_check_score；历史只读；显式要求评分时才按固定检查项算，分数不替代阻塞。范围通过不等于产品完整/美术通过。复审同报告保留稳定 Finding 和版本差异。同步允许写集中的活跃规则冲突与受影响断言，不改旧报告。

## 允许修改

- skills/using-shanforge/SKILL.md
- skills/using-shanforge/references/human-readable-status.md
- skills/using-shanforge/references/work-skill-return-contract.md
- skills/requesting-code-review/SKILL.md
- skills/requesting-code-review/references/review-score-rubric.md
- skills/requesting-code-review/references/independent-review-task-template.md
- skills/requesting-code-review/references/task-review-template.md
- skills/requesting-code-review/references/pr-review-template.md
- skills/verification-before-completion/SKILL.md
- skills/verification-before-completion/references/completion-claim-checklist.md
- skills/document-templates/assets/templates/traceability/requirements-matrix.md
- skills/document-templates/references/traceability-and-gates.md
- skills/project-memory/SKILL.md
- skills/project-memory/references/session-card-template.md
- docs/02-user-guide/user-guide.md
- docs/05-design/workflow-execution-design.md
- tests/test_human_response_contract_integration.py
- tests/test_skill_progress_visibility_and_continuation.py
- tests/test_work_skill_status_envelope_ownership.py
- tests/test_remaining_skill_project_status_contract.py
- tests/test_independent_review_gate.py
- tests/test_review_workflow_skills.py
- tests/test_skill_portability_and_local_contracts.py
- tests/test_response_owner_contracts.py

## 禁止

你不是独占工作区，不回退他人修改；不写范围外文件、不提交/推送、不改全局状态、不自批。使用 apply_patch；不定义函数内命名函数，不抽取无独立职责的单调用 helper。

## 验证

uv run pytest tests/test_human_response_contract_integration.py tests/test_skill_progress_visibility_and_continuation.py tests/test_work_skill_status_envelope_ownership.py tests/test_remaining_skill_project_status_contract.py tests/test_independent_review_gate.py tests/test_review_workflow_skills.py tests/test_skill_portability_and_local_contracts.py tests/test_response_owner_contracts.py -q

先确认预期失败再修改；尚无真实输出时准确报告等待试用，不造通过。返回 DONE/DONE_WITH_CONCERNS/NEEDS_CONTEXT/BLOCKED、命令/exit code、文件和 concerns；不写 ledger/额外过程材料。

# 独立行为试用与集中质量收口

- 工作项：FLOW-STATUS-REVIEW-001
- 任务：FLOW-STATUS-REVIEW-001-T03
- task_card_id: FLOW-STATUS-REVIEW-001-T03
- wbs_id: WBS-FLOW-SR-03
- 状态：active
- owner: independent-forward-worker
- depends_on: FLOW-STATUS-REVIEW-001-T01, FLOW-STATUS-REVIEW-001-T02
- 依赖事实：合同与回归设施已实现且定向检查通过；端到端观察是本任务产物，不是前置完成声明。
- review_status: approved
- 优先级：P0
- 任务层级：cross_cutting
- 关联目标：REQ-FLOW-01, REQ-FLOW-02, REQ-FLOW-03, REQ-FLOW-04, REQ-FLOW-05
- 强关系：IMPLEMENTS
- 上游计划：.factory/workitems/FLOW-STATUS-REVIEW-001/plan.md
- 流水账：.factory/workitems/FLOW-STATUS-REVIEW-001/ledger.jsonl
- current_gate: closed
- next_required_action: create_exact_local_commit

## 试用授权

control_model=gpt-5.6-sol; task_complexity=standard; risk_level=medium; execution_model=gpt-5.6-terra; execution_authorized=true; workflow_id=execution-workflow; write_policy=source_or_test_write; dispatch_role=worker; dispatch_required=true; dispatch_mode=subagent; requested_reasoning_effort=medium; fork_turns=none。原因：独立生成真实行为测试数据，范围内仅观察文件写入。

## 输入与边界

读取 evidence/raw-behavior-inputs.json 的8个中性场景，以及 using-shanforge 状态/回写合同与 requesting-code-review 当前正文和 rubric。禁止读 tests/fixture 的 oracle、测试判分实现、本任务分析/修改历史。场景事实是受控试用输入，不代表实际产品已验证状态。每场景先独立生成自然中文答复，再抽取本条实际答复的结构事实与逐字摘录；不自报分数，不修改业务或运行外部动作。

## 唯一写集

- .factory/workitems/FLOW-STATUS-REVIEW-001/evidence/behavior-observations-v3.json

用 apply_patch 直接保存8条真实响应；不改技能/测试/计划/ledger，不提交/推送，不删除他人修改。父线程记录派发、验证；另一独立 reviewer 负责检查正文语义与实际缺陷，不由试用者自批。

## 观察格式

数组每项：case_id、candidate_id、original_response、excerpts。
状态问题增加 project_completion（complete/incomplete/unknown）、overall_phase（中文阶段名称）、current_activity（中文活动名称）、scope_remaining、approved_product_remaining、unknown_unverified_or_not_started、scope_reconciliation（中文核对说明）、next_action（中文下一动作）。scope_remaining、unknown_unverified_or_not_started 必须为 JSON 字符串数组；approved_product_remaining 为 JSON 字符串数组或字符串“未知”；无事项用 []，不得把未知当 []。清单使用 raw 中原始业务名称和顺序。
评审问题增加 review_decision（approved/changes_requested/blocked/self_check_passed）、finding_ids（保留既有ID）、new_findings（本次发现的中文描述列表）、delta_reason（复审差异原因）；不要求无关的产品状态字段。
excerpts 为以上事实字段对应原回复的逐字中文摘录；用户正文不使用机器枚举或为匹配而堆字段。无关字段省略；原正文中不存在的事实不得虚构摘录，首次评审没有复审差异时省略 delta_reason。不要读取或推断判分oracle。

## 验收

8条输入对应8条真实响应，来源/范围/未知不被改写。父线程运行 uv run pytest tests/test_delivery_status_review_behavior.py -q；语义由未参与实现或试用的 reviewer 验。任何失败保留原始观察，先归因再修正，不由实现者改写原响应讨好测试。

# 动态派发测试

- work_item_id: MODEL-DYNAMIC-DISPATCH-001
- task_card_id: MODEL-DYNAMIC-DISPATCH-001-T02
- wbs_id: WBS-MODEL-DYNAMIC-02
- status: closed
- owner: dynamic_dispatch_tests
- priority: P1
- task_scope: system
- depends_on: MODEL-ORCHESTRATOR-SELECTION-001 的共享文件提交；新增测试可先写
- review_status: approved
- current_gate: closed
- next_required_action: none
- write_policy: source_or_test_write
- control_model: user_selected
- task_complexity: standard
- risk_level: medium
- reasoning_demand: routine
- execution_model: gpt-5.6-terra
- requested_reasoning_effort: medium
- execution_authorized: true
- dispatch_role: worker
- dispatch_required: true
- dispatch_mode: subagent
- fork_turns: none
- capability_source: current collaboration.spawn_agent schema
- route_reason: 验收和映射已由父会话锁定，沿用 pytest 表解析及负例检查。

## 精确写集

- tests/test_dynamic_model_dispatch.py
- tests/test_model_tier_routing.py
- tests/test_black_box_workflow_eval.py
- tests/test_residual_audit_contracts.py

## 输入与验收

当前 brief 与 plan 的共享合同即完整规格。只读取 plan 的共享合同和本卡，不扩读历史 workitems。新增测试先 RED，通知父会话；已有文件等父会话明确交接完成通知后再改。保留历史派发回执检查，不能用预填模型决策记录冒充真实试用。

先解析 SKILL.md 中 `### 子任务模型决策表`，覆盖 low/medium/high/xhigh/max、review 下限、风险优先、跨模块、unknown 不默认低档。负向变异必须能抓到低档覆盖高风险和审查降档。S11 观察接受新合法显式组合并拒绝缺参、回执错配及 fork=all；保留历史测试语义，不删失败断言换通过。只有真实存在的新版行为记录可作实时派发证据。

## 验证命令

`UV_CACHE_DIR=/private/tmp/shanforge-uv-cache uv run pytest -q tests/test_dynamic_model_dispatch.py tests/test_model_tier_routing.py tests/test_black_box_workflow_eval.py tests/test_residual_audit_contracts.py`

`UV_CACHE_DIR=/private/tmp/shanforge-uv-cache uv run ruff check tests/test_dynamic_model_dispatch.py tests/test_model_tier_routing.py tests/test_black_box_workflow_eval.py tests/test_residual_audit_contracts.py`

## 禁令与回执

你不是唯一执行者，不回滚他人改动。禁止源码/合同/配置/.factory 写入、提交、推送、安装依赖、自批。没有新授权不扩写集。返回 DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED、RED/GREEN 命令和 exit code、文件、concerns；工具回执由父会话记录。

## 本轮目录补充

实施目录为 /private/tmp/shanforge-dynamic-dispatch-01a07e6a；原精确相对写集映射至该目录。禁止改主工作区共享文件；合入由父会话在前置提交后组织。

## 最终集成交接

2026-09-08前置提交后写集迁回主工作区；追加test_full_project_session_workflow_routing.py、test_lifecycle_governance.py直接版本消费者。原历史快照保持，旧目录限制由本次交接替代。

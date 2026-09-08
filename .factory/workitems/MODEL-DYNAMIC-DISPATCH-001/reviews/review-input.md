# 动态派发合同独立评审输入

- work_item_id: MODEL-DYNAMIC-DISPATCH-001
- task_card_id: MODEL-DYNAMIC-DISPATCH-001-T03
- reviewer_type: independent_subagent
- current_gate: review
- write_policy: state_or_gate_write（仅父会话落盘；reviewer 禁止写入）
- execution_authorized: true
- dispatch_role: reviewer
- execution_model: gpt-5.6-terra
- requested_reasoning_effort: high
- fork_turns: none
- capability_source: 本会话 terra-reviewer 固定 Terra/high/read-only
- 范围：本批18个文件的增量、真实前向试用结果与新旧合同兼容；候选在 /private/tmp/shanforge-dynamic-dispatch-01a07e6a。
- 候选绑定：candidate-sha256.json；差异：candidate.diff（相对前置解耦候选快照，包含新测试和只读role）。
- 要求：本工作项 brief 八项验收；plan 中唯一模型表、只读分支与隔离实施更新。前置任务在主工作区独立关闭，不属于本次实现。

## 新鲜验证

父会话于本候选执行 `UV_CACHE_DIR=/private/tmp/shanforge-uv-cache uv run pytest -q tests/test_dynamic_model_dispatch.py tests/test_model_tier_routing.py tests/test_black_box_workflow_eval.py tests/test_residual_audit_contracts.py`：exit 0，31 passed。
worker 的 Ruff、diff check、skill quick_validate、只读 role TOML 断言均 exit 0；最终集成后的全量验证尚未运行。

前向试用：forward-input.md 为原始输入，../evidence/forward-trial.json 为未参与实现的 /root/dynamic_dispatch_forward_trial 原始回复。它是12个父会话决策模拟，未实际派发12个代理，也未加载新角色。真实本批工具派发见 dispatch-receipts.jsonl（Astra/high 实施、Terra/medium 测试、Terra/high 试用）。

## 请检查

需求符合、选档优先级与不继承、只读/授权边界、不可用/角色冲突、阶段升降档、历史证据保留、测试是否能抓到实际契约倒置，以及中文是否简洁准确。不要只核对关键词。以 Findings 为先，提供位置/触发/影响/验证。实现者报告不能代替 diff；确认候选指纹。无阻断问题才 approved，范围仅限本批；不要将模拟输出当宿主实测。

## 已知验证边界

- task-reader 仅静态 TOML 与内容验证，新会话宿主加载/运行未实测；合同明确未暴露就失败关闭。
- 最终主工作区集成和全量测试由父会话在前置提交后完成。
- 前置任务发现旧 FLOW-STATUS-REVIEW-001 证据被测试永久绑定当前工作树、旧设计版本断言及索引过期，正在其原范围修复；本批不修改历史 manifest 或回执。

reviewer 未参加本批设计、实施或前向试用，只读本输入包与候选。返回 reviewer_id、独立性、checked/unchecked_scope、findings、approved/changes_requested、human_confirmation_required 及原因。禁止写文件、提交、推送或扩范围。

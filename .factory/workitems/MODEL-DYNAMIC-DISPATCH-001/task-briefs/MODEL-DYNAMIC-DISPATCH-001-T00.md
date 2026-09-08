# 动态派发范围与质量收口

- work_item_id: MODEL-DYNAMIC-DISPATCH-001
- task_card_id: MODEL-DYNAMIC-DISPATCH-001-T00
- wbs_id: WBS-MODEL-DYNAMIC-00
- status: ready_for_commit
- owner: main_session
- priority: P1
- task_scope: system
- depends_on: none
- review_status: approved
- current_gate: commit
- next_required_action: create_exact_local_commit
- write_policy: project_fact_write
- allowed_paths: .factory/workitems/MODEL-DYNAMIC-DISPATCH-001/
- forbidden_actions: shared_source_write_before_handoff, modify_other_workitem, global_config_write, dependency_install, push, self_approve

消费 brief 的用户要求，创建实施与验证包。父会话只负责本工作项材料、最终证据与项目 memory；源码和测试由显式模型子代理实施。

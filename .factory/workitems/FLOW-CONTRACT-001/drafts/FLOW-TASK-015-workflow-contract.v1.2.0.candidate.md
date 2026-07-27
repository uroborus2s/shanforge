# FLOW-TASK-015 会话归因与工作流契约候选

## 候选控制

- 候选 ID：`FLOW-TASK-015-C001`
- 候选版本：`v1.2.0`
- 候选状态：`ready_for_same_reviewer_rereview`（未生效）
- 所属 WorkItem：`FLOW-CONTRACT-001`
- 所属 TaskCard：`FLOW-TASK-015`
- 正式基线路径：`docs/05-design/workflow-execution-design.md`
- 正式基线版本：`v1.1.0`
- 正式基线 SHA-256：`5769beb3478d528a0b0888328381173aa799e1e137925fc393bd98d97d3eb687`
- 候选用途：替换正式文档中重复且互相冲突的控制块，并重写完整软件项目会话归因合同。
- 生效规则：批准前不得修改正式文档或同步 runtime Skill；批准后仍须通过显式发布事务原位更新唯一正式文档。

本文件是 `.factory` 内的受控候选 delta，不是第二份人类项目文档，也不是正式事实源。正式文档继续只有
`docs/05-design/workflow-execution-design.md` 一份；历史通过 Git 和发布 ledger 回溯。

## 候选变更边界

批准后的发布事务只做三类原位变更：

1. 保留正式文档 ID `PROC-TASK-EXECUTION-001`，将唯一版本控制头晋升为 `v1.2.0`，删除重复的 `0.2.0 / 评审中` 控制块。
2. 用本候选的会话行为、工作流合同、写入授权和节点转换替换现行模糊段落。
3. 保留现行正式文档中与本候选不冲突的任务包、六类任务和执行验证规则。

## 完整软件项目会话归因模型

所有完整软件项目会话必须先归因，再执行：

```text
当前消息 -> 会话行为 -> 工作流 -> 节点 -> 允许动作 -> 状态包
```

分类器一次只能选中一个默认工作流。后续 review、verification、commit 是前一工作流产出的显式
`next_required_action`，不是与当前工作流同时命中的第二条路由。相同优先级出现多个候选、缺少身份或
事实冲突时必须返回 `needs_user_input` 或 `blocked`，不得猜测。

普通项目事实写入前必须验证已存在且非空的 work_item_id 和 task_card_id。memory summary 不能作为项目事实写入的唯一凭据。

## 会话行为合同

| 行为 ID | 中文名称 | 触发谓词 | 默认工作流 | Handler | 默认写策略 |
|---|---|---|---|---|---|
| `SB-EXPLAIN` | 解释 | 只请求解释或建议且不改变项目事实 | `direct-answer-workflow` | `using-shanforge` | `no_project_write` |
| `SB-CLARIFY` | 澄清 | 澄清目标、边界或验收且结论将成为项目输入 | `requirements-workflow` | `requirements-engineering` | `project_fact_write` |
| `SB-REQUIREMENT` | 需求 | 新增、拆分或结构化需求 | `requirements-workflow` | `requirements-engineering` | `project_fact_write` |
| `SB-CHANGE` | 变更 | 修改已存在需求、设计、计划、任务或 Gate | `change-control-workflow` | `using-shanforge` | `state_or_gate_write` |
| `SB-DESIGN` | 方案 | 形成或修订系统、模块、接口、UI 或流程方案 | `design-workflow` | `using-shanforge` | `project_fact_write` |
| `SB-PLAN` | 计划 | 将已批准输入拆成实施计划或任务卡 | `planning-workflow` | `writing-plans` | `project_fact_write` |
| `SB-EXECUTE` | 执行 | 实施已授权 TaskCard | `execution-workflow` | `executing-plans` | `source_or_test_write` |
| `SB-BUG` | Bug | 已观察失败、异常或回归，需要先查根因 | `debugging-workflow` | `systematic-debugging` | `project_fact_write` |
| `SB-TEST` | 测试 | 设计或执行单测、集成、黑盒、UI、API 或发布测试 | `testing-workflow` | `verification-before-completion` | `source_or_test_write` |
| `SB-REVIEW` | Review | 发起独立评审或处理评审意见 | `review-workflow` | `requesting-code-review` | `state_or_gate_write` |
| `SB-VERIFY` | 验证 | 对完成声明、修复或发布候选执行新鲜验证 | `verification-workflow` | `verification-before-completion` | `state_or_gate_write` |
| `SB-COMMIT` | 提交 | 本地提交、push、PR、merge 或发布请求 | `commit-workflow` | `gitcommitzh` | `state_or_gate_write` |
| `SB-STATUS` | 状态查看 | 查看项目位置、任务状态、阻塞或进度 | `status-memory-workflow` | `project-memory` | `no_project_write` |
| `SB-RESUME` | 恢复 | 恢复中断或压缩后的当前任务上下文 | `status-memory-workflow` | `project-memory` | `state_or_gate_write` |
| `SB-PAUSE` | 暂停 | 暂停活动任务并记录恢复条件 | `change-control-workflow` | `using-shanforge` | `state_or_gate_write` |
| `SB-DEPRECATE` | 废弃 | 废弃、取代或终止任务、候选或方案 | `change-control-workflow` | `using-shanforge` | `state_or_gate_write` |

## 工作流合同

| 工作流 ID | 写策略 | 优先级 | 触发 | 输入 Schema | 允许动作 | 禁止动作 | 输出 Schema | Ledger event | Evidence | 进入 Gate | 退出 Gate |
|---|---|---:|---|---|---|---|---|---|---|---|---|
| `tracking-identity-workflow` | `create_tracking_identity` | 120 | `project_effect=true and tracking_identity_missing` | `behavior_id, proposed_work_item_id, proposed_task_card_id, exact_write_set` | 原子创建 WorkItem、TaskCard、首条 ledger；readback；重新路由 | 写任何业务事实、源码、测试、正式文档或 memory；留下半成品身份 | `status, work_item_id, task_card_id, ledger_event, identity_receipt, next_required_action=reroute` | `tracking_identity_created` | 原子写入、回滚状态与 readback receipt | `identity_absent` | `identity_created_and_readback or blocked` |
| `direct-answer-workflow` | `no_project_write` | 10 | `project_effect=false` | `message, minimal_context` | 回答、解释、列建议 | 读取项目记忆、写项目文件、改状态 | `answer, needs=none` | N/A: 无项目写入 | N/A: 无项目写入 | `none` | `stopped` |
| `requirements-workflow` | `project_fact_write` | 50 | `behavior in SB-CLARIFY,SB-REQUIREMENT` | `work_item_id, task_card_id, intent, current_requirement_ref` | 写需求候选、AC、NFR、影响分析 | 改源码、跳过需求 Review、覆盖历史 | `status, requirement_refs, evidence, ledger_event, gate, next_required_action` | `requirement_candidate_updated` | 需求候选路径与结构验证 receipt | `tracking_identity_valid` | `ready_for_review` |
| `change-control-workflow` | `state_or_gate_write` | 80 | `behavior in SB-CHANGE,SB-PAUSE,SB-DEPRECATE` | `work_item_id, task_card_id, source_ref, reason, impact_scope` | 追加变更、暂停条件、取代关系、影响分析 | 覆盖历史、静默改 Gate、无来源废弃 | `status, change_ref, impact, evidence, ledger_event, gate, next_required_action` | `change_control_recorded` | before-after、影响范围与授权 receipt | `tracking_identity_valid` | `ready_for_review or pending_human_confirmation` |
| `design-workflow` | `project_fact_write` | 50 | `behavior=SB-DESIGN` | `work_item_id, task_card_id, approved_input_ref, design_scope` | 写受控设计候选、接口、边界、风险 | 写孤立 docs、新建重复正式文档、直接实现 | `status, design_ref, evidence, ledger_event, gate, next_required_action` | `design_candidate_updated` | 候选路径、基线 hash、候选 hash | `approved_input_available` | `ready_for_review` |
| `planning-workflow` | `project_fact_write` | 50 | `behavior=SB-PLAN` | `work_item_id, task_card_id, approved_requirement_or_design_ref` | 写 plan、TaskCard、依赖、验证命令 | 修改源码、执行计划、自批计划 | `status, plan_ref, task_refs, evidence, ledger_event, gate, next_required_action` | `plan_candidate_updated` | plan 自审与 review input receipt | `approved_input_available` | `plan_ready_for_review` |
| `execution-workflow` | `source_or_test_write` | 70 | `behavior=SB-EXECUTE` | `work_item_id, task_card_id, approved_plan_ref, allowed_paths, test_design` | Red、最小实现、Green、报告、review input | 越权路径、跳号、自批 approved、跳验证 | `status, outputs, evidence, ledger_event, gate, next_required_action` | `implementation_ready_for_review` | red-green、diff、report 和命令 receipt | `execution_authorized` | `ready_for_review` |
| `debugging-workflow` | `project_fact_write` | 90 | `behavior=SB-BUG` | `work_item_id, task_card_id, symptom, reproduction_input` | 复现、追踪、根因、最小修复建议 | 猜测式补丁、无根因改行为 | `status, root_cause_ref, evidence, ledger_event, gate, next_required_action` | `root_cause_investigated` | 复现、失败输出与调用链 receipt | `tracking_identity_valid` | `root_cause_found or blocked` |
| `testing-workflow` | `source_or_test_write` | 60 | `behavior=SB-TEST` | `work_item_id, task_card_id, test_scope, requirement_refs, environment_ref` | 写测试、运行测试、记录环境与结果 | 无需求追踪测试、伪造通过、遗漏清理 | `status, test_ids, results, evidence, ledger_event, gate, next_required_action` | `test_execution_recorded` | 测试 ID、命令、exit code、结果与环境 receipt | `test_scope_authorized` | `test_passed or test_failed` |
| `review-workflow` | `state_or_gate_write` | 100 | `behavior=SB-REVIEW or gate=needs_independent_review` | `work_item_id, task_card_id, review_input_ref, reviewer_identity` | 独立只读 Review、finding triage、同范围整改回流 | 作者自批、Reviewer 修改实现、忽略 Important | `status, review_ref, findings, evidence, ledger_event, gate, next_required_action` | `independent_review_recorded` | reviewer 独立性、分数、finding 与命令 receipt | `review_package_complete` | `approved or changes_requested` |
| `verification-workflow` | `state_or_gate_write` | 95 | `behavior=SB-VERIFY or gate=needs_verification` | `work_item_id, task_card_id, claim, commands, evidence_target` | 运行新鲜完整命令、记录失败与未运行项 | 用旧输出宣称完成、以 Review 代替验证 | `status, command_results, evidence, ledger_event, gate, next_required_action` | `verification_recorded` | 命令、exit code、失败数、输出摘要 | `verification_scope_known` | `verification_passed or verification_failed` |
| `commit-workflow` | `state_or_gate_write` | 110 | `behavior=SB-COMMIT` | `work_item_id, task_card_id, explicit_authorization, review_ref, verification_ref, scope` | 精确暂存、本地提交、受权远端动作 | 混入无关改动、以提交代替 Review、推断远端授权 | `status, commit_ref, evidence, ledger_event, gate, next_required_action` | `commit_or_handoff_recorded` | staged diff、commit receipt 或阻塞原因 | `review_and_verification_passed` | `commit_done or remote_handoff_blocked` |
| `status-memory-workflow` | `SB-STATUS=no_project_write; SB-RESUME=state_or_gate_write` | 40 | `behavior in SB-STATUS,SB-RESUME` | `project_id, requested_scope, current_task_ref; SB-RESUME 时必须含 work_item_id 和 task_card_id` | 条件读取、会话卡、索引摘要、必要 memory sync | 散读 docs、把正文复制进 memory、凭 summary 改权威状态 | `status, session_card, sources_read, evidence, ledger_event, gate, next_required_action` | `session_restored` 或 N/A: 纯只读状态查看 | N/A: 纯只读查看；恢复写入时必须有 readback receipt | `none` | `session_ready or blocked` |

同一消息如果同时含“修 Bug 并提交”，先按最高安全前置依赖进入 `debugging-workflow`；只有根因、修复、Review 和
Verification 的 ledger Gate 依次满足后，后续新节点才可进入 `commit-workflow`。优先级用于冲突解析，不能跳过依赖。

## 写入授权矩阵

| 动作类别 | WorkItem | TaskCard | 唯一允许写入 | Ledger | Evidence | Memory 可单独证明 |
|---|---|---|---|---|---|---|
| `no_project_write` | 不要求 | 不要求 | 0 次项目写入 | N/A | N/A | 否 |
| `create_tracking_identity` | 可不存在 | 可不存在 | 单一原子动作创建 WorkItem + TaskCard + 首条 ledger；其他写入 0 次 | 必须 | 创建 receipt 与 readback | 否 |
| `project_fact_write` | 必须已存在 | 必须已存在 | 仅 TaskCard allowlist 内候选、文档或任务事实 | 必须 | artifact path、before-after 与 hash | 否 |
| `source_or_test_write` | 必须已存在 | 必须已存在 | 仅 TaskCard allowlist 内源码、Skill 或测试 | 必须 | Red-Green、diff 和命令 receipt | 否 |
| `state_or_gate_write` | 必须已存在 | 必须已存在 | 仅合法状态转换、review、verification 或提交记录 | 必须 | transition、授权或命令 receipt | 否 |

`create_tracking_identity` 必须在一个可回滚步骤内创建身份并回读。任一对象创建或首条 ledger 失败时全部回滚；
不得留下只有 WorkItem、只有 TaskCard 或没有首条 ledger 的半成品。完成后重新路由，普通写入不得复用该例外。

对项目事实执行写入时，路由包必须包含具体 `work_item_id`、`task_card_id`、`allowed_paths`、`forbidden_actions`、
`current_gate` 和 `write_policy`。`待创建`、空值、通配占位或无法在 ledger 回读的 ID 都视为无效。

## 工作流节点与转换

| 工作流 ID | 允许节点 | 合法主路径 | 停止态 | 人工 Gate 规则 |
|---|---|---|---|---|
| `tracking-identity-workflow` | `identity_intake,identity_scoped,identity_creating,identity_readback,reroute` | `identity_intake -> identity_scoped -> identity_creating -> identity_readback -> reroute` | `reroute,blocked` | ID 冲突或无法原子创建时阻塞；不自动请求业务批准 |
| `direct-answer-workflow` | `intake,routed,stopped` | `intake -> routed -> stopped` | `stopped` | 不需要人工 Gate |
| `requirements-workflow` | `intake,routed,scoped,authoring,stopped` | `intake -> routed -> scoped -> authoring -> stopped` | `ready_for_review,needs_user_input,blocked` | 只有产品边界或正式需求批准需要人工 Gate |
| `change-control-workflow` | `intake,routed,scoped,impact_analysis,stopped` | `intake -> routed -> scoped -> impact_analysis -> stopped` | `ready_for_review,pending_human_confirmation,blocked` | 不可逆废弃、正式基线变更或风险接受需要人工 Gate |
| `design-workflow` | `intake,routed,scoped,authoring,stopped` | `intake -> routed -> scoped -> authoring -> stopped` | `ready_for_review,needs_user_input,blocked` | 正式设计发布按项目治理进入人工 Gate |
| `planning-workflow` | `intake,routed,scoped,planning,stopped` | `intake -> routed -> scoped -> planning -> stopped` | `plan_ready_for_review,needs_user_input,blocked` | 仅范围或授权变化需要人工 Gate |
| `execution-workflow` | `intake,routed,scoped,executing,verifying,stopped` | `intake -> routed -> scoped -> executing -> verifying -> stopped` | `ready_for_review,needs_user_input,blocked` | 普通授权任务内部执行不新增人工 Gate |
| `debugging-workflow` | `intake,routed,reproducing,investigating,stopped` | `intake -> routed -> reproducing -> investigating -> stopped` | `root_cause_found,needs_user_input,blocked` | 进入行为修复前按当前调试契约确认根因或方案 |
| `testing-workflow` | `intake,routed,scoped,testing,stopped` | `intake -> routed -> scoped -> testing -> stopped` | `test_passed,test_failed,blocked` | 测试执行本身不新增人工 Gate |
| `review-workflow` | `intake,routed,reviewing,stopped` | `intake -> routed -> reviewing -> stopped` | `approved,changes_requested,blocked` | 普通任务 Review 不自动进入人工 Gate；仅正式发布或风险接受按项目规则进入 |
| `verification-workflow` | `intake,routed,verifying,stopped` | `intake -> routed -> verifying -> stopped` | `verification_passed,verification_failed,blocked` | Verification 不能替代已登记的人工 Gate，也不自动创建人工 Gate |
| `commit-workflow` | `intake,routed,prechecking,committing,stopped` | `intake -> routed -> prechecking -> committing -> stopped` | `commit_done,remote_handoff_blocked,blocked` | 远端、发布或未包含在当前授权中的动作必须显式人工授权 |
| `status-memory-workflow` | `intake,routed,restoring,stopped` | `intake -> routed -> restoring -> stopped` | `session_ready,blocked` | 只读查看和正常恢复不需要人工 Gate |

任意节点都可在缺事实时转 `needs_user_input`，在契约、权限、工具或事实冲突时转 `blocked`。只有表中列出的主路径和
停止态合法；跨 workflow 转移必须由上一 workflow 的 `next_required_action` 和已写 ledger Gate 重新触发路由。

## 路由包与状态包

身份缺失时只能生成一次性身份创建路由包：

```text
route:
  route_kind: tracking_identity_intake
  behavior_id: <preserved SB-*>
  workflow_id: tracking-identity-workflow
  node_id: identity_intake
  proposed_work_item_id: <new non-empty ID>
  proposed_task_card_id: <new non-empty ID>
  allowed_paths: <exact WorkItem, TaskCard and ledger paths>
  forbidden_actions: <all other writes>
  current_gate: identity_absent
  write_policy: create_tracking_identity
```

身份原子创建与 readback 成功后必须使用已回读身份重新路由原始行为。失败时只能回滚并进入 `blocked`，
不得降级成普通项目写入，也不得把 proposed ID 当成已存在 ID。

普通项目化路由包：

```text
route:
  behavior_id: <SB-*>
  workflow_id: <workflow-id>
  node_id: <node-id>
  work_item_id: <existing non-empty ID>
  task_card_id: <existing non-empty ID>
  allowed_paths: <exact paths>
  forbidden_actions: <actions>
  current_gate: <gate>
  write_policy: <matrix action class>
```

工作流返回状态包：

```text
result:
  status: <workflow-local status>
  outputs: <artifact refs>
  evidence: <evidence refs or reasoned N/A>
  ledger_event: <event id or reasoned N/A>
  gate: <current gate>
  next_required_action: <one action or none>
```

状态包只报告已发生事实。`ready_for_review` 不是 `approved`，Review 不是 Verification，Verification 不是人工批准，
本地提交也不授权 push、PR、merge 或发布。

## 发布与运行同步

1. 同一独立 Reviewer 复审本候选、结构测试、基线 hash 和候选 hash。
2. 复审批准后冻结候选 hash，进入正式版本所需的人工治理 Gate；不得把独立 Review 写成人工批准。
3. Gate 通过后，以单一发布事务原位更新 `docs/05-design/workflow-execution-design.md`，不在 `docs/` 新建第二份文档。
4. 发布后从正式 `v1.2.0` 同步最小路由边界到相关 runtime Skills，并运行结构、黑盒和相邻流程验证。
5. 发布、Skill 同步和验证全部成功后才可将 FLOW-TASK-015 推进到最终独立实现 Review。

失败时正式版本保持 `v1.1.0`；候选、review、evidence 和 ledger 留在 `.factory/workitems/FLOW-CONTRACT-001/`
作为审计记录，不能伪装成已生效合同。

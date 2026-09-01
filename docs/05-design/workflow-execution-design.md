# 会话、任务与工作流执行设计

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `PROC-TASK-EXECUTION-001` |
| 正式版本 | `v2.0.0` |
| 来源候选 | `SOFTWARE-LIFECYCLE-GOVERNANCE-001` |
| 发布事务 | `N/A（本次文档同步不产生发布事务）` |
| 负责人 | `HUMAN_PROJECT_OWNER` |
| 修改 / 审核 / 批准 | `AI_EXECUTOR` / `集中质量门` / `uroborus` |
| 状态 | 已批准并生效 |
| 上游 | `PRD`、需求矩阵、系统架构 |
| 下游 | `using-shanforge`、专项 skills、WorkItem |

## 目标与边界

Shanforge 是由代理宿主加载的 `skill-first` 协作资产，不提供仓内平台运行时。
本设计只规定项目化会话从分类到交付的共同边界；专项方法仍由对应 Skill 负责。

- 先按当前消息分类；无项目影响的解释不读取或写入 `.factory/`。
- 项目化写入必须有既存 WorkItem、TaskCard、精确 `allowed_paths`、`forbidden_actions`、`current_gate` 和 `write_policy`。
- `using-shanforge` 是唯一流程路由 owner；工作 Skill 只回传本职输出、证据、状态和所需 Gate。
- Review、验证、人工确认、提交与发布相互独立，任何一项不能替代另一项。

## 完整软件项目会话归因模型

本文合同固定跨 Skill 的路由与交接边界，不替代具体 skill 的专业工作流。

```text
当前消息 -> 会话行为 -> 工作流 -> 节点 -> 允许动作 -> 状态包
```

所有完整软件项目会话必须先归因，再执行。分类器一次只能选中一个默认工作流；后续 review、
verification、commit 必须由前一工作流的 `next_required_action` 明确触发。普通项目事实写入前必须验证
已存在且非空的 `work_item_id` 和 `task_card_id`；memory summary 不能作为项目事实写入的唯一凭据。

项目化会话顺序固定为 `classifying → restoring_if_projectized → routing → scoping`：只有分类确认项目影响后
才恢复当前事实，再选择唯一工作流并收窄允许范围。

## 会话行为合同

| 行为 ID | 中文名称 | 触发谓词 | 默认工作流 | Handler | 默认写策略 |
|---|---|---|---|---|---|
| `SB-EXPLAIN` | 解释 | 无项目事实变更 | `direct-answer-workflow` | `using-shanforge` | `no_project_write` |
| `SB-CLARIFY` | 澄清 | 结论成为项目输入 | `requirements-workflow` | `requirements-engineering` | `project_fact_write` |
| `SB-REQUIREMENT` | 需求 | 新增或结构化需求 | `requirements-workflow` | `requirements-engineering` | `project_fact_write` |
| `SB-CHANGE` | 变更 | 修改需求、设计、计划、任务或 Gate | `change-control-workflow` | `using-shanforge` | `state_or_gate_write` |
| `SB-DESIGN` | 方案 | 形成或修订方案 | `design-workflow` | `using-shanforge` | `project_fact_write` |
| `SB-PLAN` | 计划 | 将批准输入拆成任务 | `planning-workflow` | `writing-plans` | `project_fact_write` |
| `SB-EXECUTE` | 执行 | 实施授权 TaskCard | `execution-workflow` | `executing-plans` | `source_or_test_write` |
| `SB-BUG` | Bug | 已观察失败或回归 | `debugging-workflow` | `systematic-debugging` | `project_fact_write` |
| `SB-TEST` | 测试 | 执行测试任务 | `testing-workflow` | `verification-before-completion` | `source_or_test_write` |
| `SB-REVIEW` | Review | 发起或处理独立评审 | `review-workflow` | `requesting-code-review` | `state_or_gate_write` |
| `SB-VERIFY` | 验证 | 验证完成声明或候选 | `verification-workflow` | `verification-before-completion` | `state_or_gate_write` |
| `SB-COMMIT` | 提交 | 本地提交请求 | `commit-workflow` | `gitcommitzh` | `state_or_gate_write` |
| `SB-REMOTE` | 远端交付 | push、PR 或 merge 请求 | `remote-pr-workflow` | `using-shanforge` | `state_or_gate_write` |
| `SB-RELEASE` | 发布部署 | 发布、回滚或生产观察 | `release-workflow` | `release-deployment` | `state_or_gate_write` |
| `SB-STATUS` | 状态查看 | 查看项目状态 | `status-memory-workflow` | `project-memory` | `no_project_write` |
| `SB-RESUME` | 恢复 | 恢复项目任务 | `status-memory-workflow` | `project-memory` | `state_or_gate_write` |
| `SB-PAUSE` | 暂停 | 暂停活动任务 | `change-control-workflow` | `using-shanforge` | `state_or_gate_write` |
| `SB-DEPRECATE` | 废弃 | 废弃或取代事实 | `change-control-workflow` | `using-shanforge` | `state_or_gate_write` |

## 工作流合同

| 工作流 ID | 写策略 | 优先级 | 触发 | 输入 Schema | 允许动作 | 禁止动作 | 输出 Schema | Ledger event | Evidence | 进入 Gate | 退出 Gate |
|---|---|---:|---|---|---|---|---|---|---|---|---|
| `tracking-identity-workflow` | `create_tracking_identity` | 120 | 缺项目身份 | `behavior_id, proposed_work_item_id, proposed_task_card_id, exact_write_set` | 原子创建 WorkItem、TaskCard、首条 ledger；readback | 其他项目写入 | `status, work_item_id, task_card_id` | `tracking_identity_created` | 创建与回读 receipt | `identity_absent` | `identity_created_and_readback or blocked` |
| `direct-answer-workflow` | `no_project_write` | 10 | 无项目影响 | `message, minimal_context` | 回答 | 写项目事实 | `answer, needs=none` | N/A: 无项目写入 | N/A: 无项目写入 | `none` | `stopped` |
| `requirements-workflow` | `project_fact_write` | 50 | 需求或澄清 | `work_item_id, task_card_id, intent` | 写需求候选 | 改源码 | `status, outputs, evidence` | `requirement_candidate_updated` | 路径与结构 receipt | `tracking_identity_valid` | `ready_for_review` |
| `change-control-workflow` | `state_or_gate_write` | 80 | 变更、暂停或废弃 | `work_item_id, task_card_id, source_ref` | 追加变更与影响 | 覆盖历史 | `status, outputs, evidence` | `change_control_recorded` | before-after receipt | `tracking_identity_valid` | `ready_for_review or pending_human_confirmation` |
| `design-workflow` | `project_fact_write` | 50 | 设计 | `work_item_id, task_card_id, approved_input_ref` | 写受控设计 | 直接实现 | `status, outputs, evidence` | `design_candidate_updated` | 候选 hash | `approved_input_available` | `ready_for_review` |
| `planning-workflow` | `project_fact_write` | 50 | 计划 | `work_item_id, task_card_id, approved_requirement_or_design_ref` | 写 plan、TaskCard | 修改源码 | `status, outputs, evidence` | `plan_candidate_updated` | plan receipt | `approved_input_available` | `plan_ready_for_review` |
| `execution-workflow` | `source_or_test_write` | 70 | 执行 | `work_item_id, task_card_id, approved_plan_ref, allowed_paths, test_design` | Red、最小实现、Green | 越权或自批 | `status, outputs, evidence` | `implementation_ready_for_review` | red-green、diff | `execution_authorized` | `ready_for_review` |
| `debugging-workflow` | `project_fact_write` | 90 | Bug | `work_item_id, task_card_id, symptom, reproduction_input` | 复现、根因 | 猜测式补丁 | `status, root_cause_ref, evidence` | `root_cause_investigated` | 复现与调用链 | `tracking_identity_valid` | `root_cause_found or blocked` |
| `testing-workflow` | `source_or_test_write` | 60 | 测试 | `work_item_id, task_card_id, test_scope` | 写并运行测试 | 伪造通过 | `status, test_ids, results` | `test_execution_recorded` | 命令与 exit code | `test_scope_authorized` | `test_passed or test_failed` |
| `review-workflow` | `state_or_gate_write` | 100 | Review | `work_item_id, task_card_id, review_input_ref, reviewer_identity` | 独立只读 Review | 作者自批 | `status, review_ref, findings` | `independent_review_recorded` | 独立性与 finding | `review_package_complete` | `approved or changes_requested` |
| `verification-workflow` | `state_or_gate_write` | 95 | 验证 | `work_item_id, task_card_id, claim, commands` | 新鲜完整验证 | 使用旧输出 | `status, command_results` | `verification_recorded` | 命令与 exit code | `verification_scope_known` | `verification_passed or verification_failed` |
| `commit-workflow` | `state_or_gate_write` | 110 | 提交 | `work_item_id, task_card_id, explicit_authorization` | 精确暂存、本地提交 | 远端操作 | `status, commit_ref` | `commit_recorded` | staged diff | `review_and_verification_passed` | `commit_done or blocked` |
| `remote-pr-workflow` | `state_or_gate_write` | 110 | 远端交付 | `work_item_id, task_card_id, local_commit_ref` | 按授权远端交接 | 推断授权 | `status, remote_ref` | `remote_handoff_recorded` | 工具 receipt | `local_commit_available` | `remote_done or remote_handoff_blocked` |
| `release-workflow` | `state_or_gate_write` | 115 | 发布 | `work_item_id, task_card_id, candidate_ref` | 项目既有发布入口 | 发明脚本 | `status, release_ref` | `release_recorded` | 授权与健康检查 | `release_candidate_verified` | `released or rolled_back or blocked` |
| `status-memory-workflow` | `SB-STATUS=no_project_write; SB-RESUME=state_or_gate_write` | 40 | 状态或恢复 | `project_id; SB-RESUME 时必须含 work_item_id 和 task_card_id` | 条件读取与恢复 | 散读 docs | `status, session_card` | `session_restored` | N/A: 只读查看 | `none` | `session_ready or blocked` |

## 写入授权矩阵

| 动作类别 | WorkItem | TaskCard | 唯一允许写入 | Ledger | Evidence | Memory 可单独证明 |
|---|---|---|---|---|---|---|
| `no_project_write` | 不要求 | 不要求 | 0 次项目写入 | N/A | N/A | 否 |
| `create_tracking_identity` | 可不存在 | 可不存在 | 单一原子动作创建 WorkItem + TaskCard + 首条 ledger；其他写入 0 次 | 必须 | 创建 receipt 与 readback | 否 |
| `project_fact_write` | 必须已存在 | 必须已存在 | 仅 TaskCard allowlist 内候选、文档或任务事实 | 必须 | artifact path、before-after 与 hash | 否 |
| `source_or_test_write` | 必须已存在 | 必须已存在 | 仅 TaskCard allowlist 内源码、Skill 或测试 | 必须 | Red-Green、diff 和命令 receipt | 否 |
| `state_or_gate_write` | 必须已存在 | 必须已存在 | 仅合法状态转换、review、verification 或提交记录 | 必须 | transition、授权或命令 receipt | 否 |

`create_tracking_identity` 必须在一个可回滚步骤内创建身份并回读；完成后重新路由。普通项目化路由包必须包含
`work_item_id`、`task_card_id`、`allowed_paths`、`forbidden_actions`、`current_gate`、`write_policy`，
以及 `dispatch_role`、`dispatch_required`、`dispatch_mode`。

## 模型路由

Sol 是复杂度、风险和模型路由的唯一 owner。风险遵循“高风险优先、低风险全量满足、其余中风险”，禁止按代码行数、文件数或预计工时分级：任一条件命中即为高风险；全部条件满足才是低风险；未命中高风险且未满足全部低风险条件即为中风险；信息不足时不得判为低风险。

身份缺失时只能生成一次性身份创建路由包：

```text
route:
  route_kind: tracking_identity_intake
  proposed_work_item_id: <new non-empty ID>
  proposed_task_card_id: <new non-empty ID>
  write_policy: create_tracking_identity
```

原子创建并 readback 成功后必须使用已回读身份重新路由原始行为。普通路由包至少包含：

```text
route:
  work_item_id: <existing non-empty ID>
  task_card_id: <existing non-empty ID>
  allowed_paths: <exact paths>
  forbidden_actions: <actions>
  current_gate: <gate>
  write_policy: <policy>
  dispatch_role: worker | reviewer | none
  dispatch_required: true | false
  dispatch_mode: subagent | direct
```

- `simple + low` 使用 `gpt-5.6-luna` / `low`；其余授权 worker 使用 `gpt-5.6-terra` / `medium`。
- `execution-workflow` + `source_or_test_write` + 已授权：`dispatch_role: worker, dispatch_required: true, dispatch_mode: subagent`。
- 独立 reviewer 使用 Terra / `high`、只读：`dispatch_role: reviewer, true, subagent`；冲突、范围扩大、风险上升、连续两次验证失败或人工 Gate 交还 Sol。
- 派发分支按顺序互斥；非独立 review、Gate 和最终收口仍由 Sol 控制。
- 其余路由由 Sol 直接控制：`dispatch_role: none, false, direct`。
- Terra/Luna 不得重新分级、自扩范围或自批完成；父 Sol 的 `spawn_agent` 回执才是派发证据。

## 工作流节点与转换

每个工作流只走已登记节点；缺事实转 `needs_user_input`，契约、权限或事实冲突转 `blocked`，跨工作流由
`next_required_action` 与 ledger Gate 重新路由。评审工作流只能独立只读，Review 不能替代 Verification。

## 发布与运行同步

候选须经独立 Review、冻结候选 hash、适用人工 Gate 与新鲜验证后才可发布。发布只消费精确候选和最终测试报告；
本地提交不授权 push、PR、merge 或发布。

## 统一任务包

```text
工作结果：
- work_item: <WORKITEM-ID>
- task_id: <TASK-ID or none>
- task_type: decomposition | system_design | module_design | ui_design | development | testing
- status: <该 Skill 的既有本地状态>
- outputs: <path>
- evidence: <path>
- ledger_event: <event id or path>
- needs: <该 Skill 的既有本地 needs>
```

`task_id/task_type` 表示正式任务身份，`skill` 表示执行者身份；工作 Skill 不计算项目完成层级，流程总控生成项目状态信封。

## 六类任务

| 任务类型 | 执行方式 | 必须输出 | `.factory` 证据 |
|---|---|---|---|
| 任务分解 | 拆成可验收任务 | plan、TaskCard、验证命令 | ledger、plan review 输入 |
| 系统总设计 | 定义边界和 NFR | 系统设计、接口 owner、风险 | 设计依据 |
| 模块设计 | 定义单领域职责和契约 | 模块设计、接口、测试矩阵 | 边界核查 |
| UI 设计 | 定义流程、状态与可访问性 | 页面/组件与状态矩阵 | 截图或浏览器检查 |
| 开发 | 先 Red、最小实现、Green | 改动和测试 | red/green、diff |
| 测试 | 按风险选择层级 | 新鲜结果与残余风险 | 命令输出、exit code |

## 任务分解要求

一个 TaskCard 对应一个可验收交付物，必须写目标、输入、允许/禁止修改、步骤、失败断言、验证命令和输出路径。
读文件、运行命令与 evidence 是任务内部 checklist，不单独拆卡。

## 设计任务要求

系统和模块设计先定义所属领域、接口 owner、下游依赖、禁止耦合、数据流、错误处理、测试策略和 baseline 影响。
代码结构遵从 Skill-first 边界：Skill 拥有方法与合同，所属 `scripts/` 仅提供确定性辅助能力，`docs/` 保存稳定事实，
`.factory/` 保存执行事实；代理宿主负责加载 Skill、工具与权限，目标项目不依赖仓内运行时或绝对路径。

## UI 任务要求

UI 设计或实现覆盖用户流程、信息层级、组件边界、`loading`、`empty`、`error`、`disabled`、`permission`、`mobile`
状态，以及键盘、焦点、语义、对比度和桌面/移动视口检查；不适用时在 task brief 写 `UI: N/A` 与原因。

## 开发任务要求

`writing-plans` 只生成最小计划、TaskCard 和批次质量任务；`executing-plans` 在当前会话连续执行已批准计划；
`subagent-driven-development` 只用于已批准、可隔离的子代理实施；`tdd-workflow` 负责先失败、最小实现与定向验证。
实施只消费已授权 task brief，不修改允许范围外路径。先写最小失败检查，再以最小改动修复根因或目标路径；低、中风险通过
定向检查后继续批次，高风险可专项评审。

批次 / 里程碑缺最终验证证据、实现摘要、review input 或 ledger event 时不得推进到 `ready_for_review`。
批次收口时，缺 evidence、implementer report、review input package 或 ledger event 时，不得声明批次完成；
作者只能推进到 `ready_for_review`，不得自批 `approved`。

## 测试任务要求

新功能优先 TDD；Bug 必须先复现、确认直接与根源原因、影响范围和风险。低风险定向检查，中风险补集成或契约验证，
高风险补目标 E2E 或人工验收。最终候选必须运行新鲜验证，记录 exit code、失败、跳过、未运行项和残余风险。

## 阶段门、变更回流与发布闭环

完整交付主线为 `设计 -> 开发 -> 测试 -> 发布 -> 生产观察`。业务目标、范围或验收标准变化回需求；技术方案错误回设计；
实现偏离回代码；测试预期、夹具或脚本错误回测试。受影响下游标记 `stale`，验证后为 `revalidated`，被替代为
`superseded`。发布只消费精确候选、最终测试报告和显式人工授权，并保存最小回执。

## 落盘规则

稳定事实进入 `docs/` 登记 owner；执行事实进入 `.factory/workitems/<WORKITEM-ID>/` 的 brief、plan、task-briefs、
evidence、reports、reviews 和 `ledger.jsonl`；memory 只保留恢复摘要，缓存只是可重建投影。开发期的
统一任务包只保留授权路径内的输出和必要定向检查；批次收口才保存一套 evidence、implementer report、review input
package 和 ledger 事实，不以单个低、中风险任务的 checkpoint 冒充批次完成。

## 评审和人工确认

- Review 不能替代 verification。
- Verification 不能替代 human confirmation。
- 低、中风险任务不逐项独立评审；批次或里程碑集中 Review。
- 有 Critical 必须 `changes_requested`；Important 默认 `changes_requested`，除非用户明确接受风险。
- Reviewer `approved` 只完成 Review Gate；正式发布、风险接受或不可逆取舍才进入 `pending_human_confirmation`。
- 整改直接修改受影响 diff 并重跑定向测试；只有 Critical、Important 或高风险路径变化才复审受影响范围。

## 统一生命周期矩阵

| 阶段 | 触发 | 权威输入 | 准入 | 活动 | 输出 | 保存位置 | owner / 模型 | 验证 | 退出 Gate | 回流 |
|---|---|---|---|---|---|---|---|---|---|---|
| 分类与恢复 | 新消息或恢复请求 | 当前消息；TaskCard / ledger（项目化时） | 消息可判定 | 判定行为；按需恢复 | 路由包或直接答复 | WorkItem ledger；必要时 memory | `using-shanforge` / Sol | 身份、范围、Gate 完整 | `routed` / `blocked` | 缺身份走身份创建；缺事实澄清 |
| 发现与 Spike | 不确定性影响决策 | 已知需求、约束、风险 | 探索范围已授权 | 时间盒调研、Spike 或原型 | 假设、结论、风险与下一决策 | WorkItem evidence / ledger | 专项 Skill / Sol 或 Terra | 可复现观察；不把原型当交付 | `decision_ready` | 结论回需求、设计或停止；原型不得越级发布 |
| 需求 | 新需求或需求变更 | PRD、用户确认、Spike 结论 | 身份与写集有效 | 需求、AC、NFR、影响分析 | 受控需求候选与追踪关系 | 正式需求文档；ledger | requirements owner / Sol | 可追踪、无冲突 | `ready_for_review` | 变更回需求；设计歧义回澄清 |
| 设计 | 已批准需求或明确变更 | 需求、架构边界、适用 Spike | 输入已确认 | 方案、边界、接口和风险设计 | 正式设计候选 | 对应 `docs/` owner；ledger | design owner / Sol | 追踪、边界和可实现性检查 | `design_ready` | 风险或需求变化回需求；实现反馈回设计 |
| 计划与任务 | 复杂或多交付物实施 | 已批准需求 / 设计 | 范围和验收明确 | 分解计划、TaskCard、依赖与验证命令 | plan、授权任务包 | WorkItem plan / task briefs / ledger | planning owner / Sol | 路径、角色、Gate、验证命令完整 | `execution_authorized` | 简单任务可跳过正式计划，但不得跳过 WorkItem 身份、TDD 和定向验证 |
| 实现 | 已授权 TaskCard | plan / task brief、允许路径、测试设计 | `execution_authorized` | 先失败后最小实现再通过（TDD） | 源码、文档或测试变更；状态包 | 授权路径；ledger / evidence | Terra 或 Luna；Sol 已定级 | 定向测试、静态检查、diff | `ready_for_review` 或批次 checkpoint | 测试失败回实现；范围扩张或风险上升回 Sol |
| Bug 根因 | 观察到缺陷、回归或异常 | 复现步骤、日志、调用链 | 症状可复现或明确缺口 | 复现、定位根因、最小修复 | 根因记录、修复与回归范围 | 授权路径；ledger / evidence | debugging owner / Terra | 根因证据与定向回归 | `root_cause_found` / `verification_passed` | 设计缺陷回设计；无法复现回澄清，禁止猜测式补丁 |
| 测试与定向回归 | 实现、修复或测试任务 | AC、变更范围、测试计划 | 测试范围已授权 | 单元、集成或黑盒测试；定向回归 | 新鲜结果与失败摘要 | 测试路径；evidence / ledger | quality owner / Terra | 命令、exit code、结果 | `test_passed` / `test_failed` | 失败回实现或根因；契约缺口回需求 / 设计 |
| 批次 Review | 批次、里程碑或高风险专项完成 | 实现摘要、diff、验证结果 | review 输入完整 | 独立只读 Review、finding 分流 | review decision | WorkItem reviews / ledger | 独立 reviewer / Terra | 独立性、finding 与受影响检查 | `approved` / `changes_requested` | 同范围整改后复审；风险接受才进入人工确认 |
| 最终候选验证 | 候选准备完成 | 候选、适用完整测试命令、review | review 与验证前提满足 | 运行新鲜完整候选测试 | verification report | evidence / ledger | verification owner / Terra | 结果、exit code、环境与候选一致 | `verification_passed` | 失败回实现、测试或根因；不得用旧输出宣称通过 |
| 本地提交与远端交付 | 明确提交或远端请求 | 已通过候选、显式授权 | scope、review、verification 已满足 | 精确暂存、本地提交；按授权远端交接 | commit / remote receipt | Git；ledger / evidence | Git owner / 专项 Skill | staged diff、提交或工具 receipt | `commit_done` / `remote_done` | 无授权停止；远端失败回交付准备 |
| 发布与运维 | 明确发布、回滚或事件请求 | 精确候选、最终测试、环境与人工授权 | `release_candidate_verified` | 项目既有发布入口、健康检查、观察、必要时回滚 | release / incident record | 交付文档；ledger / evidence | release owner / 人类授权的专项 Skill | 发布验证、健康检查和观察 | `released` / `rolled_back` / `blocked` | 失败回滚或回实现；事件回 Bug / 变更 |

## 方法选择与 Gate

- 阶段门只确认本阶段的准入、输出和验证；它不替代下一阶段的 Review、最终候选测试或人工授权。
- 简单、低风险的局部任务可不写正式计划；仍须具备 WorkItem 身份、TDD 与定向验证。复杂、多交付物、跨模块或高风险任务使用计划和受控子代理。
- Sol 是复杂度、风险、模型路由和升级的唯一 owner。仅 `simple + low` 可派 Luna；其余已授权独立任务派 Terra。Terra/Luna 不得重新分级、自扩范围或自批完成。
- Spike 与原型只用于降低不确定性；其输出必须回写为决策输入，不能替代设计、测试、Review 或发布验证。
- TDD 适用于实现和修复：先以能失败的检查定义行为，再作最小实现。Bug 修复先证明根因，并覆盖受影响调用路径的定向回归。
- 批次 Review 用于里程碑、批次收口或高风险路径；普通低、中风险任务不逐项制造 Review Gate。最终候选测试必须新鲜运行，发布验证只在明确发布边界适用。
- 输入冲突、范围扩大、风险上升、连续两次验证失败或人工 Gate 一律停止执行并升级给 Sol。

## 过程数据与清理边界

| 数据类别 | 唯一 owner / 保存位置 | 保留与清理规则 |
|---|---|---|
| 稳定事实 | 对应正式 `docs/` owner | 保存可长期审计的需求、设计、测试和交付规则；冲突先修 owner，再同步索引。 |
| 机器合同 | 所属 Skill 的 `SKILL.md`、`references/`、`scripts/` | 保存可重复的规则与辅助能力；脚本优先标准库，不能成为流程主控。 |
| 执行事实 | `.factory/workitems/<ID>/ledger.jsonl`、`evidence/`、`reviews/` | 追加身份、状态、证据与 Gate；不以 memory 或缓存覆盖。按留存规则清理大体积过程材料。 |
| 恢复摘要 | `.factory/memory/` | 仅保存活动任务、阻塞、Gate、最近事实和回源指针；有界、不复制正式正文或命令全文。 |
| 缓存与投影 | 所属 Skill 的 cache / HTML 输出 | 可删除重建，只能消费正式事实与合格执行事实，绝非权威来源。 |
| 敏感信息 | 宿主安全存储或项目既有受控机制 | 不写入 docs、ledger、memory、缓存、日志或证据；执行前遵从宿主权限与显式授权。 |

## 追踪与发布规则

每个任务简报以 `IMPLEMENTS` 连接需求。验证、Review、人工确认和发布分别记录，候选、证据和版本必须可回源同一 WorkItem。正式版本只在批准后的受控文档生效；候选冻结、作者验证或 reviewer 通过都不自行升级版本。

## 正式版本历史（仅已发布）

| 版本 | 修改内容 | 日期 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v1.2.0` | 发布完整项目会话归因、13 个工作流、写入授权、节点转换及状态包契约 | 2026-07-27 | `AI_EXECUTOR` | `/root/project_knowledge_review` | `uroborus` |
| `v1.3.0` | 开发期轻门禁、风险分级评审和批次集中质量收口 | 2026-08-01 | `AI_EXECUTOR` | `集中质量门` | `uroborus` |
| `v1.3.1` | 明确低、中、高风险任务的确定性判定条件和信息不足时的升级规则 | 2026-08-01 | `AI_EXECUTOR` | `集中质量门` | `uroborus` |
| `v1.4.0` | 增加设计至生产阶段门、变更归因、候选修复复测、最终发布回归和部署闭环 | 2026-08-08 | `AI_EXECUTOR` | `集中质量门` | `uroborus` |
| `v1.5.0` | 固化 Sol 唯一控制、复杂度分级及 Terra/Luna 受控执行路由 | 2026-08-23 | `AI_EXECUTOR` | `集中质量门` | `uroborus` |
| `v2.0.0` | 收口为 Skill-first 生命周期矩阵、方法选择与过程数据边界 | 2026-09-01 | `AI_EXECUTOR` | `集中质量门` | `uroborus` |

---
name: using-shanforge
description: 项目状态查询、任务延续、项目事实修改、阶段切换、work item 状态变化，或无法判断请求是否需要项目化时使用；作为流程总控 / CTO 判断当前环节、选择唯一下一步 skill，并要求工作 skill 只回写状态。无项目影响的直接回答和轻量分析走快速通道。
---
<SUBAGENT-STOP>
若为执行特定任务的子代理，忽略本 skill。
</SUBAGENT-STOP>
<EXTREMELY-IMPORTANT>
本 skill 是 Shanforge 流程总控，不是具体工作 skill。
工作 skill 不决定前置、后置或下一步 skill。
流程路由只在这里决定。
</EXTREMELY-IMPORTANT>

# Shanforge 流程总控

## v1.3.0 运行时路由合同

先把当前消息归为唯一 `behavior_id`，再选唯一 `workflow_id`：

| behavior_id | workflow_id | write_policy |
|---|---|---|
| `SB-EXPLAIN` | `direct-answer-workflow` | `no_project_write` |
| `SB-CLARIFY`、`SB-REQUIREMENT` | `requirements-workflow` | `project_fact_write` |
| `SB-CHANGE`、`SB-PAUSE`、`SB-DEPRECATE` | `change-control-workflow` | `state_or_gate_write` |
| `SB-DESIGN` | `design-workflow` | `project_fact_write` |
| `SB-PLAN` | `planning-workflow` | `project_fact_write` |
| `SB-EXECUTE` | `execution-workflow` | `source_or_test_write` |
| `SB-BUG` | `debugging-workflow` | `project_fact_write` |
| `SB-TEST` | `testing-workflow` | `source_or_test_write` |
| `SB-REVIEW` | `review-workflow` | `state_or_gate_write` |
| `SB-VERIFY` | `verification-workflow` | `state_or_gate_write` |
| `SB-COMMIT` | `commit-workflow` | `state_or_gate_write` |
| `SB-REMOTE` | `remote-pr-workflow` | `state_or_gate_write` |
| `SB-RELEASE` | `release-workflow` | `state_or_gate_write` |
| `SB-STATUS` | `status-memory-workflow` | `no_project_write` |
| `SB-RESUME` | `status-memory-workflow` | `state_or_gate_write` |

普通项目写入的 route 必须有已存在且非空的 `work_item_id`、`task_card_id`，以及精确
`allowed_paths`、`forbidden_actions`、`current_gate`、`write_policy`；缺一项即 `blocked`，memory summary
不能单独证明身份。身份缺失时只能进入 `tracking-identity-workflow`，输出
`route_kind: tracking_identity_intake` 与 `write_policy: create_tracking_identity`。在可回滚步骤中原子创建 WorkItem、TaskCard 和首条 ledger，
完成 readback 后重新路由原始行为；期间禁止其他写入。

工作流结果只报告已发生事实：`status`、`outputs`、`evidence`、`ledger_event`、`gate`、
`next_required_action`。Review、Verification、人工批准和 Commit 互不替代。

## 角色

你扮演流程 CTO / 项目协调者，只负责判断流程位置和路由。

你负责：

- 恢复当前会话、阶段、work item 和 ledger 状态。
- 在内部路由前先形成用户可理解的项目位置快照。
- 判断当前处于意图澄清、需求、设计、计划、执行、验证、评审、人工确认、提交还是收尾。
- 先确定唯一下一动作，再选择唯一下一步 skill，并说明内部路由理由。
- 给工作 skill 提供输入文件、允许范围、禁止动作和期望状态回写。
- 接收工作 skill 的状态回写，再决定下一步。
- 当人类要求查看项目状态时，调用固定项目快照命令，返回最后有效的只读站点。
- 只有确认属于真实人工 Gate 时，才在 `pending_human_confirmation` 停止并请求人工确认。

你不负责：

- 代替工作 skill 写代码、写计划、写测试或写评审。
- 代替 reviewer 批准实现。
- 代替人工确认 `human_approved`。
- 把完整流程写进每个工作 skill。

## 简单任务快速通道

入口必须分两阶段，禁止为了判断请求是否简单而预先恢复项目状态。

阶段一只使用当前消息做初判：

1. 先根据当前消息判定处理模式。
2. `direct_answer` 与 `lightweight_analysis` 只使用当前消息、当前对话和完成答案所需的直接文件。
3. 快速通道不得读取 `.factory/memory/agent-session.md`，不得读取 work item ledger。
4. 快速通道不得写任何仓内文件，不创建 WorkItem、TaskCard、ledger、evidence、review 或 memory，不输出项目位置快照，不返回工作 skill 状态包。
5. 只返回当前会话答案或结构化分析；任何仓内持久化都属于项目影响，必须进入阶段二。

出现下列任一信号时不得使用快速通道，必须升级为项目化流程：

- 继续或恢复既有任务。
- 查询当前项目状态。
- 当前消息包含 WorkItem / TaskCard ID。
- 新增或修改项目事实，包括源代码、skill、测试、正式文档、需求、设计、ledger、memory 或 gate。
- 创建、更新或保存任何仓内文件。
- 要求追踪、验收、review、提交或发布。
- 当前对话无法安全判断是否有项目影响。

阶段二只处理升级后的请求：再使用 `project-memory` 恢复项目上下文、当前 work item 和最新 ledger，然后按完整流程继续。

## 简单代码变更直接实施

简单代码变更仍属于项目影响，但不等于必须写正式计划。同时满足以下条件时走直接实施：

- 用户未明确要求正式计划。
- 需求和验收结果明确，无产品、设计或架构取舍。
- 一次局部代码修改加对应单测即可完成。
- 不改变公共接口、跨层边界、数据 schema、迁移、依赖、安全权限、外部系统或发布方式。
- 不需要多个可独立验收交付物、跨会话追踪、并行或多人协调。

命中后不得路由到 `writing-plans`，也不得创建 plan、task brief 或计划评审。直接进入 `tdd-workflow`，在当前任务内完成测试、最小实现和定向验证。默认只运行受影响测试和必要静态检查；全量测试不是简单任务的默认步骤，只在影响扩大、高风险变更或最终发布门明确要求时运行。

用户明确要求正式计划时，覆盖简单代码变更判定，按正式计划流程执行。

若实现中发现跨模块影响、公共契约变化、迁移需求、多个独立交付物或无法用定向测试收口，再升级到正式计划流程；不得仅因文件数量超过一个就升级。

## 开发期轻门禁与集中质量收口

- 开发期默认目标是保持代码规范、完成必要的定向单元测试和适用静态检查；不为每个接口或普通任务
  生成 evidence、implementer report、review input、独立评审或复审文件。
- 风险等级按“高风险优先、低风险全量满足、其余中风险”判定，禁止按代码行数、文件数或预计工时分级。
- 任一条件命中即为高风险：认证授权、密钥、隐私或安全边界；支付、计费或资金；删除、迁移、回填、
  批量写入或数据修复；公共 API、数据 schema、消息格式或跨服务契约；事务、并发、幂等或分布式一致性；
  发布、生产配置、不可逆外部副作用；核心链路或大范围用户影响；难以回滚或缺少代表性环境验证。
- 全部条件满足才是低风险：影响仅限内部局部模块；不改变公共契约、schema 或跨服务边界；不涉及安全、
  资金、隐私、生产环境或破坏性数据操作；失败不会造成数据丢失、错误写入、大范围不可用或核心流程中断；
  可通过简单回滚恢复；一个定向单测或静态检查可以证明主要行为。
- 未命中高风险且未满足全部低风险条件的任务属于中风险。信息不足时不得判为低风险；无法排除安全、
  数据或生产风险时暂按高风险处理，否则按中风险处理。
- 已授权批次中的低、中风险任务通过定向检查后直接继续下一任务。需要跨会话恢复时只写紧凑 ledger checkpoint，
  不把 checkpoint 升格为质量 Gate。
- 高风险任务可以在批次结束前触发专项设计评审、代码评审或目标集成测试。
- 全部开发任务或已批准里程碑完成后，统一进入一次集中质量门：代码审查、API 契约测试、服务测试、
  集成测试，并按风险增加 E2E、安全或性能测试。
- 同一批次只保存一套实现摘要、验证证据、review input 和最终 review。整改直接修改 diff 并重跑受影响测试；
  只有 Critical、Important 或高风险路径变化才复审受影响范围。
- 长周期项目可以按里程碑收口，但禁止退化为逐任务重复评审。用户明确要求逐任务评审时才覆盖本默认策略。

## Sol / Terra / Luna 模型路由

Sol 是唯一总体设计、任务分级和模型路由 owner；Terra 和 Luna 不得重新分级。先使用上文风险规则得到
`risk_level`，再由 Sol 确定复杂度：

- `simple`：满足“简单代码变更直接实施”的全部条件，且 `risk_level` 为 `low`。
- `complex`：涉及架构或系统设计、公共契约、schema、迁移、安全或生产，包含三个及以上独立交付物，
  需要跨模块、跨会话或并行协调，或仍有未解决的设计歧义；信息不足时按 `complex`。
- `standard`：既不满足 `simple`，也未命中 `complex`。

确定性映射只有两条：

- `simple + low` -> `gpt-5.6-luna`。
- `standard | complex | medium | high` -> `gpt-5.6-terra`。

### 执行模型决策表

按表格顺序命中第一行；`*` 是兜底：

| task_complexity | risk_level | execution_model |
|---|---|---|
| `simple` | `low` | `gpt-5.6-luna` |
| `*` | `*` | `gpt-5.6-terra` |

### 执行授权决策表

按表格顺序命中第一行；只有身份、范围和 Gate 全部完整才允许派发：

| gate_state | identity_and_scope | execution_authorized | action |
|---|---|---|---|
| `closed` | `complete` | `true` | `dispatch` |
| `*` | `*` | `false` | `do_not_dispatch` |

高风险 Gate 未闭合时 `execution_authorized: false`；其他任务只有在身份、范围和当前 Gate 完整时才可授权。
普通项目化路由包追加并持久化以下字段：

```text
control_model: gpt-5.6-sol
task_complexity: simple | standard | complex
risk_level: low | medium | high
execution_model: gpt-5.6-luna | gpt-5.6-terra
execution_authorized: true | false
route_reason: <命中的复杂度、风险和 Gate 规则>
escalation_triggers:
  - scope_expanded
  - input_conflict
  - risk_increased
  - verification_failed_twice
  - human_gate
```

Terra/Luna 只执行已授权任务包，不得改写上述字段、扩大范围、自批 Review 或决定完成。任一升级触发器命中时
停止当前执行并交还 Sol；同一任务连续两次验证失败记为 `verification_failed_twice`。

## 默认流程

1. 按“简单任务快速通道”先根据当前消息判定处理模式。
2. 命中 `direct_answer` 或 `lightweight_analysis` 时直接返回，不进入后续项目流程。
3. 其余请求再使用 `project-memory` 恢复项目上下文、当前 work item 和 ledger。
4. 判断当前状态，不默认读取 `docs/` 长文。
5. 检查是否存在 `pending_human_confirmation`，并按“真实人工 Gate”重新核实；旧状态、内部 checkpoint 或已撤销 Gate 不得使流程停止。
6. 判断当前环节和阻塞项；代码请求先检查是否命中“简单代码变更直接实施”。
7. 先确定用户可见的唯一下一动作，再从路由表选择唯一下一步 skill；简单代码变更不得因为没有 plan 而路由到 `writing-plans`。
8. 输出输入包：读取文件、允许修改范围、禁止动作和期望状态回写。
9. 工作 skill 完成后，只接收状态回写，不让工作 skill 自己决定下一步。
10. 低、中风险任务 checkpoint 继续授权批次，不进入独立评审。只有批次 / 里程碑完成、高风险专项检查，
    或用户明确要求时才把 `ready_for_review` 路由到 review；`changes_requested` 在同范围内直接整改。
    输出“完成”、进入提交或关闭 work item 前，必须重读当前 work item ledger 最新事件和最终 review ledger。

## 项目位置快照

仅 `project_workitem`、`tracked_task` 和真实 Gate 在任务开始、阶段切换、子流程返回、阻塞和最终收口时说明项目整体位置。`direct_answer` 与 `lightweight_analysis` 不输出项目位置快照。项目化回复不得只罗列 Task ID、hash、skill 名或文件路径。

快照至少包含：

```text
项目整体进度：第 <N>/<TOTAL> 步；<阶段名>；<阶段状态>
当前任务：<人类可读任务名>；<任务状态>
已完成：<本轮已验证完成的结果>
正在执行：<当前真实动作；没有则写“无”>
停止原因：<无 | 精确 Gate / blocker 及 owner>
唯一下一动作：<下一项项目动作；完成态写“本任务无待办”>
```

- 用户可见的下一动作必须描述项目动作，不得只写调用某个 skill。
- “当前任务完成”“当前阶段完成”“项目整体完成”必须分开表达。
- 没有真实停止条件时，`停止原因` 写“无”，并继续既有授权范围内的内部流程。
- 长任务的 commentary 更新沿用同一快照语义，可以压缩为一到三句，但不能只报内部编号。

## 三段式人类响应合同

所有面向用户的 `direct_answer`、`lightweight_analysis` 和项目化回复都使用同一语义顺序：

1. **第一部分：直接回应**：先正面回答用户当前的问题、意见、疑问或执行要求；不得用状态码、文件列表或项目位置代替回答。
2. **第二部分：处理结果**：再给出分析、建议、方案、已完成工作、验证结果、风险和必要的项目状态。项目位置快照只作为第二部分的内容，不替代第一部分。
3. **第三部分：需要用户回复**：明确是否需要用户回复、要回答什么，以及收到答复后的动作；不需要用户输入时明确写“无需回复”及系统将继续或已经完成的事实。

标题可以根据当前语境使用更自然的同义表达，但三部分的语义和顺序不能缺失。工作 Skill 状态包和项目状态信封是内部输入，流程总控必须先翻译成人类可理解的三段式回复，不得原样堆给用户。

第三部分不新增人工 Gate：

- “无需回复”表示不存在真实人工 Gate，不是暂停、阻塞或完成状态。
- 当前授权范围仍有剩余工作时，第三部分应在 commentary 中说明“无需回复，将继续执行”；输出后必须继续既有授权范围内的执行，不得因为输出“无需回复”而停止，也不得结束当前 turn。
- 只有当前授权范围已经到达终态、存在真实人工 Gate、存在无法内部解决的 blocker，或继续需要新的权限时，才可以发送结束当前 turn 的最终回复。
- 存在真实人工 Gate 时，第三部分必须给出决策对象、建议、允许选项和用户可直接回复的内容；不得只写“请确认”。
- `direct_answer` 或 `lightweight_analysis` 没有后续项目动作时，第三部分可以写“无需回复，本次问题已回答”；不得因此创建 WorkItem 或伪造下一动作。

## 真实人工 Gate 与连续执行

### 内部动作不是人工 Gate

在用户已经授权的任务或批次范围内，实现、验证、独立只读评审、同范围整改和 memory sync 都是内部动作。它们可以产生 checkpoint、evidence 和 ledger event，但不得逐项请求“是否继续”。

- reviewer `approved` 不自动等于 `pending_human_confirmation`。
- reviewer `changes_requested` 且 Finding 可在原目标、允许文件和风险边界内修复时，自动进入同范围整改和复审循环。
- 适用的计划评审、批次评审、定向测试、最终验证、报告和记忆同步本身不要求新增人工批准。
- 内部连续执行不推导新权限，不得扩大用户已授权的目标、文件、系统或外部影响范围。

### 真实人工 Gate

只有下列情况才能写 `pending_human_confirmation` 并停止：

- 需要产品或需求取舍、设计方向选择、验收口径选择或不可逆业务决定。
- 需要风险接受、忽略 Critical/Important Finding 或接受不完整验证。
- 需要扩大授权范围、修改新的受保护目标或改变用户明确排除项。
- 将执行破坏性或外部动作，包括正式发布、远端写入、部署、凭证使用或用户未授权的 Git 动作。
- 治理合同明确要求精确候选哈希批准或正式发布批准。
- 缺少只有人类能提供的信息，合理假设会实质改变结果。

每个 Gate 必须写明决策对象、为什么 AI 不能继续、负责确认的人、允许选项和确认后的唯一下一动作。没有这些字段的 `pending_human_confirmation` 视为无效内部 checkpoint，不得阻断流程。

## 处理模式判定

用户消息先归类，再路由。任务卡不是因为这也是任务才创建；任务卡只在项目系统需要记住、追踪和验收这件事时创建。

| 模式 | 判断 | 处理 |
|---|---|---|
| `direct_answer` | 用户只要一个答案、解释、建议或临时分析 | 直接回答，不创建 work item、不创建任务卡、不写 ledger |
| `lightweight_analysis` | 需要结构化分析，但没有项目化意图 | 只在当前会话输出；任何仓内持久化请求先升级为项目化流程 |
| `project_workitem` | 会影响后续项目状态、需求、设计、开发或验收 | 创建或复用 WorkItem，并写 brief / ledger |
| `tracked_task` | 是 WorkItem 下的可验收节点，需要跨会话继续、依赖、并行、评审或验收 | 创建 TaskCard / task brief |
| `gate` | 需要人工确认、风险接受、方向选择或进入下一阶段批准 | 停止并请求确认；写确认事件，不创建任务卡 |
| `event` | 背景恢复、读取文件、运行命令、提问、记录证据 | 写 event 或 evidence；不创建任务卡 |

最小判断规则：

- 只要一个答案：使用 `direct_answer` 或 `lightweight_analysis`。
- 会影响后续项目状态：使用 `project_workitem`。
- 需要依赖、并行、评审或验收：使用 `tracked_task`。
- 需要跨会话继续、依赖、并行、评审或验收：使用 `tracked_task`。
- 需要人工确认：使用 `gate`。
- 只是工具动作或过程记录：使用 `event`。

同类任务的轻量分析和任务卡执行共享专业内容契约，不共享项目治理信封；任务卡版本才增加 ID、父 WorkItem、状态、依赖、产物路径、ledger event 和后续任务。

## 概念边界

| 概念 | 含义 |
|---|---|
| Task | 一件需要完成的工作，可以是临时会话工作，也可以是项目交付工作 |
| TaskCard | WorkItem 下可追踪、可验收、可评审的 Task，必须有 ID、状态、依赖、产物、evidence 和 ledger event |
| Workflow | 某类 Task 的稳定执行顺序，例如 bug 调查、需求分析、UI 设计或代码评审 |
| Method | Workflow 内部的做法、检查清单或分析技术；除非本身产出可验收交付物，否则不创建 TaskCard |
| Tool | 执行动作的具体能力，例如命令、文件编辑、浏览器、imagegen、子 agent 或外部 API；工具调用只记录 event / evidence，不等于 TaskCard |
| Gate | 需要人工确认、风险接受或进入下一阶段批准的停止点 |
| Event | 读取文件、运行命令、提问、派发子任务、同步 memory 等过程记录 |
| Evidence | 能证明执行结果的报告、命令输出、截图、测试结果或 reviewer 结论 |

## PM 状态页

当用户要求查看项目状态、PM 看板、项目管理页面或当前进度时：

1. 读取 `references/pm-dashboard-rendering.md`。
2. 从当前 skill 目录运行 `scripts/project_snapshot.py --project-root <目标项目根目录>`；不得调用 Shanforge 仓库的 `src/`、虚拟环境或绝对路径。
3. 只需在 receipt 中返回项目相对路径时增加 `--relative-paths`；该选项不代表内容脱敏。
4. 返回 `.factory/cache/site/current/index.html`、`cache_hit` 和 `generation_id`；输入未变化时直接复用。
5. 页面只展示 `.factory/project.json`、当前会话卡以及 work item brief、当前 task brief
   和 ledger 的登记事实。工作项统计不等于产品完成率。
6. 失败时报告脚本 receipt，不临时拼装 HTML，也不把缓存当正式事实。

不新增单独的 `project-management` skill。
PM 状态页是本 skill 的自带只读输出，不改变工作 skill 的职责。

## 黑盒流程评估

当用户要求 `SF-SP-009`、黑盒流程 eval、流程回归评估或验证 workflow 行为时：

1. 读取 `references/black-box-flow-eval.md`。
2. 按 `fast smoke` 或 `full regression` 场景输入评估行为。
3. 只把真实观察到的读取、写入、命令和状态回写记为证据。
4. 若任一 critical assertion 失败，不得宣称流程通过。

黑盒流程评估只验证 workflow 行为，不新增中心脚本 gate，不替代独立 review、人工确认、提交或 PR 闭环。

## 远端 PR / push / merge handoff

当用户要求 push、创建 PR、更新 PR 或 merge，或本地提交后需要远端闭环时：

1. 读取 `references/remote-pr-handoff.md`。
2. `using-shanforge` 只判断 gate、状态词和证据是否齐备；远端执行 owner 按 handoff 契约选择。
3. `gitcommitzh` 只负责本地提交，不负责远端 PR / push / merge。
4. 缺本地提交、远端目标、远端工具权限或可审计 evidence 时，只能输出 `remote_handoff_blocked` 或 `remote_failed`。
5. 不得把本地 commit、计划、口头说明或 dry-run 写成已 push、PR 已创建或已 merge。

## 变更归因与下游失效

发现新事实时先判定唯一 owner，再决定回流点：

- 业务目标、范围或验收标准变化：回 `requirements-engineering`。
- 业务目标未变但架构、接口或技术方案错误：回对应设计 Skill。
- 实现偏离已批准设计：进入 `systematic-debugging` / `tdd-workflow`，不改需求或设计。
- 测试预期、夹具或脚本错误：只修测试并重新验证受影响范围。
- 配置、环境或生产事件：先调查根因，再按上述 owner 回流。

上游事实改变后，仅把受影响下游标为 `stale`；修订并验证后为 `revalidated`，被新事实替代为 `superseded`，
未受影响内容保持 `active`。不得因一处变化默认重走全部阶段或运行全仓测试。

## 发布与生产闭环

候选已冻结、最终必需发布测试通过且生产动作已显式授权时，路由到 `release-deployment`。该 Skill 只复用项目已有
部署、健康检查、冒烟、观察和回滚入口，输出 `released`、`rolled_back` 或 `blocked` 及最小发布回执。
缺精确候选、最终测试报告、环境别名、入口或生产授权时不得执行。

## 场景路由与 baseline gate

`using-shanforge` 是四类场景、baseline work item、gate 和关闭规则的唯一流程 owner。

| 场景 | 场景 ID | 路由判断 | gate |
|---|---|---|---|
| 新项目 | `new_project` | 用户提出新项目、产品或系统从零开始 | 先创建 Project baseline 输入包；缺 baseline work item 时不得进入普通实现任务 |
| 增加需求 | `add_requirement` | 用户提出新增功能或能力 | 路由到 `requirements-engineering`，必须检查 baseline 影响 |
| 变更需求 | `change_requirement` | 用户要求修改已有需求、验收标准或范围 | 必须定位原 Requirement，并要求版本历史 |
| 修复 bug | `fix_bug` | 用户报告失败、异常、回归或测试失败 | 先路由到 `systematic-debugging` 复现、归因和分级；低、中风险直接进入受影响修复，高风险才依次确认根因和修复方案 |

baseline work item 规则：

- 领域划分、总体架构、数据库基线、API 基线和整体 UI 设计属于 baseline work item。
- 普通需求影响领域、架构、数据库、API 或 UI baseline 时，先创建或更新 `BASE-*`，并反向关联该需求。
- 缺 evidence 时阻塞关闭；缺 review、verification、人工确认或最终审计问题报告时，不得关闭、提交或进入下一阶段。

## 路由表

| 当前状态 | 下一步 skill | 选择条件 | 工作 skill 只需回写 |
|---|---|---|---|
| 无会话卡或上下文压缩后恢复 | `project-memory` | 不清楚当前阶段、work item、ledger | `session_ready`、已读文件、排除文件 |
| 创意、意图不清、需求未批准 | `brainstorming` | 用户提出新想法或目标不明确 | `brief_ready` 或 `needs_user_input` |
| 需要 PRD、需求或验收标准 | `requirements-engineering` | brief 已清楚但需求未结构化 | `requirements_ready` |
| 需要正式文档或技术方案 | `document-templates` / `doc-coauthoring` | 需要写设计、方案、说明文档 | `document_ready` |
| 需要 UI / UX 方案 | `ui-ux-pro-max` | 任务涉及界面、交互、视觉资产 | `design_ready` |
| 需要美术方向或开发资源包 | `art-asset-pipeline` | 任务涉及 UI 美术图、游戏素材、资源清单、确认图或资源包 | `ready_for_review` |
| 需求明确的简单代码变更 | `tdd-workflow` | 局部代码修改加对应单测即可完成，不含契约、架构、迁移、安全或外部风险，且用户未明确要求正式计划 | `passed`、`partial`、`failed` 或 `blocked` |
| 已批准 brief / spec，但无 plan | `writing-plans` | 存在多个可验收交付物、跨模块协调、跨会话追踪，或用户明确要求正式计划 | `plan_ready`、`ready_for_review` 或 `not_applicable` |
| plan 已批准，任务独立 | `subagent-driven-development` | 可拆成隔离任务执行 | `ready_for_review`、`blocked` 或 `needs_user_input` |
| plan 已批准，当前会话 inline 执行 | `executing-plans` | 不使用子 agent 或任务强耦合 | `ready_for_review`、`blocked` 或 `needs_user_input` |
| 发现 Bug 或验证失败 | `systematic-debugging` | 需要复现和根因调查 | `root_cause_found`、`needs_user_input` 或 `blocked` |
| 低、中风险 Bug 根因已定位 | 按 `fault_owner` 路由需求 / 设计 / 实现 / 测试 Skill | 无安全、数据、契约或生产高风险，只修受影响范围 | 对应 Skill 既有完成态 |
| 高风险 Bug 根因已定位 | 无工作 skill | 等待根因人工确认；确认后形成最小修复方案并等待第二次确认 | `pending_human_confirmation` |
| 高风险 Bug 根因和修复方案均已确认 | `tdd-workflow` / `ai-regression-testing` | 进入修复实现和目标回归验证 | `passed`、`partial`、`failed` 或 `blocked` |
| 批次 / 里程碑实现已 `ready_for_review` | `requesting-code-review` | 全部授权开发任务完成，或高风险专项需要独立评审 | `approved` 或 `changes_requested` |
| review 要求修改 | `receiving-code-review` | 存在明确 review feedback | `ready_for_review` 或 `blocked` |
| 缺完成证据 | `verification-before-completion` | 需要新鲜验证证据 | `verification_passed` 或 `verification_failed` |
| 最终候选和测试报告已就绪 | `release-deployment` | 环境、已有部署 / 回滚入口齐备；生产动作已有显式授权 | `released`、`rolled_back` 或 `blocked` |
| reviewer 已 approved，且既有授权批次仍有内部动作 | 按当前缺口选择验证、执行或收口 owner | 不存在真实人工 Gate；自动继续，不停在 review checkpoint | `in_progress` 或任务完成态 |
| reviewer 已 approved，且下一步需要真实人工决策 | 无工作 skill | 必须给出完整决策包 | `pending_human_confirmation` |
| 人工已确认且有可提交改动 | `gitcommitzh` | review / evidence / memory sync 已齐备，当前任务产生文件改动，且用户未明确要求暂不提交 | `commit_done` |

若某个计划中的 skill 尚未安装或尚未本地化，输出 `blocked: missing_skill`，不得让工作 skill 临时代替它。

## 工作 skill 状态回写协议

工作 skill 完成时只返回状态包，不写下一步 skill。详细边界见 [工作 Skill 回写契约](references/work-skill-return-contract.md)。这里的状态包是工作 Skill 本职结果包；它不推断项目完成层级：

```text
工作 Skill 本职结果包：
- work_item: <ID>
- task_id: <TASK-ID or none>
- task_type: <formal task type>
- skill: <skill-name>
- status: <该 Skill 的既有本地状态>
- outputs:
  - <path>
- evidence:
  - <path>
- ledger_event: <path 或 event id>
- needs: <该 Skill 的既有本地 needs>
```

本 skill 再结合 work item ledger、review ledger、已授权范围和真实 Gate 生成项目状态信封：

```text
项目状态信封：
- project_position: <step / total / stage / task>
- completion_level: none | task | stage | project
- stop_reason: none | blocker | human_gate
- scope_remaining: <已授权范围内剩余工作；没有则写“无”>
- next_required_action: <唯一下一动作；没有则写“无”>
```

工作 Skill 的本地 `blocked`、`needs_user_input` 或 human-confirmation need 是输入事实；是否形成项目 blocker 或 human Gate，由本 skill 结合 ledger 判断。`direct_answer` 与 `lightweight_analysis` 不使用这两类状态包。

工作 skill 不写：

- “下一步调用某某 skill”。
- “上游来自某某 skill”。
- “提交交给某某 skill”。
- “完成声明交给某某 skill”。

这些都由本 skill 统一判断。

## 完成输出与持久化契约

每次任务收口都必须先判断写入位置：

| 场景 | 当前会话响应 | 持久化 |
|---|---|---|
| `direct_answer` / `lightweight_analysis` | 返回答案或分析结论 | 默认不落盘、不写 ledger、不写 memory |
| `project_workitem` / `tracked_task` | 返回状态包、产物路径、验证结果、阻塞 gate 和 `next_required_action` | 开发期只写必要 checkpoint；批次收口写一套 ledger、evidence/report，必要时同步 memory |
| 正式需求、设计、API、UI、用户指南或开发者指南变化 | 返回改动摘要和文档路径 | 写 `docs/` 登记路径，并更新版本历史、导航或 `doc-map.md` |
| 工具动作、命令执行、派发子 agent、自循环中间步骤 | 返回观察结果或状态 | 只写 event、evidence/report；不写正式文档 |
| 批次 review、最终 verification、人工确认、提交前检查 | 返回 gate、缺口和下一动作 | 写一套 ledger、review/evidence；必要时 memory sync |
| PM 看板 | 返回固定 CLI receipt、最后有效 HTML 入口和事实源说明 | 写 `.factory/index/` 与 `.factory/cache/site/current/` 可重建投影；不写项目事实、不提交 Git |

当前会话必须能看见收口状态；子 agent 或自循环完成后不得只静默写文件。子流程只返回状态包，是否写正式文档、ledger、evidence/report 或 memory 由本 skill 判断。

memory 只写恢复所需摘要：ID、状态、gate、`next_required_action`、关键约束和路径索引；不得写正式文档正文、命令全文、临时推理或子 agent 完整输出。

## 当前会话可见性协议

当前会话必须让用户看见任务正在做什么，不只在最后报路径。

| 时机 | 必须说明 |
|---|---|
| 任务开始 | work item / task、处理模式、选择理由、允许修改范围、预期产物 |
| 阶段切换 | 已完成动作、下一阶段、gate 或阻塞 |
| 文件编辑前 | 将修改哪些文件，以及为什么是最小范围 |
| 关键命令前后 | 命令目的、结果、失败数或未运行原因 |
| 派发子 agent / 自循环 | 子任务目标、写入边界、等待什么结果 |
| 子流程返回 | 状态包、outputs、evidence、未完成项、下一动作 |
| 长时间执行 | 当前阶段、已完成、仍在等待或验证什么 |
| 阻塞 / 失败 | 阻塞 gate、缺少证据、已写路径、未写内容、可选下一动作 |
| 最终收口 | 做了什么、写了哪里、验证结果、当前状态、`next_required_action` |

可见性响应只写事实摘要。长命令输出、完整 diff、子 agent 全文和正式文档正文只给路径，不复制进当前会话。

项目化任务最终收口必须明确写出项目位置快照。当前任务完成但项目未完成时，直接写“本任务完成，项目仍在第 N/TOTAL 步”，不得用模糊的“已完成”代替层级判断。快速通道只返回答案或分析结论，不附加项目快照。

## 提交门

进入 `gitcommitzh` 前必须确认：

- 已重读当前 work item ledger 最新事件和 review ledger。`next_required_action` 为 `none` / `无` 时表示无后续动作；以 `create_exact_local_commit`、`create_local_commit` 或 `commit_current_scope` 开头时表示已进入提交转换，提交动作不是未解决动作。仅其他非空动作或阻塞状态会阻止进入提交或完成声明。
- work item ledger、review ledger、verification evidence 和 memory sync 已齐备。
- 当前任务范围清楚，提交只覆盖当前任务范围。
- 若 review 只到 `pending_human_confirmation`，必须有用户 `human_approved`。
- 人工确认后若当前任务有可提交改动，默认进入 `gitcommitzh`；不得再要求用户额外说“提交”。
- 禁止把提交作为 review 或人工确认的替代品。
- 禁止把本地提交描述成远端 PR 已创建、已推送或已合并。

## 人工确认门

当 ledger 或 review 显示 `pending_human_confirmation` 时，先按“真实人工 Gate”核实。只有 Gate 有效时才停止，并输出：

```text
本轮执行完成，等待人工确认。

工作项：<ID>
执行结果：通过 / 部分通过 / 失败
评审结论：approved | changes_requested
评分：<N> / 100
最终审计问题报告：<path>
阻塞问题：Critical / Important / Minor 摘要
已修复问题：<列表或 none>
残留风险：<列表或 none>
验证证据：<path 或命令摘要>

请确认：
1. 通过，进入下一阶段
2. 要求修改，并给出修改点
3. 暂停
```

人工确认信息不能只输出评分；必须给出最终审计问题报告，列清 review 发现、修复状态、残留风险和验证证据。

人工没有明确确认前，不得进入下一阶段，不得关闭 work item，不得提交“最终完成”结论。

若核实后只是实现、验证、独立只读评审、同范围整改、memory sync 或普通任务 checkpoint，则不得套用本人工确认模板；应继续既有授权范围内的流程，并在项目位置快照中把 `停止原因` 写为“无”。

## 平台适配

若当前运行环境在列表中，读对应参考：
- Codex：读 `references/codex-tools.md`
- Pi：读 `references/pi-tools.md`
- Antigravity：读 `references/antigravity-tools.md`

## 用户指令

用户指令优先：`CLAUDE.md`、`AGENTS.md`、`GEMINI.md` 和直接请求。用户指令 > skill > 默认行为。只有用户明确要求，才可跳过 skill 流程或规则。

# 记忆治理专项实施计划

**项目名称：** 山海工枢 / shanforge
**文档状态：** `v0.1` 记忆治理实施计划
**负责人：** 仓库维护者
**主要读者：** 项目协调者 | 架构 | 平台开发 | 测试
**上游输入：** [记忆治理专项设计方案](../04-design/memory-governance-design.md) | [实施计划](./implementation-plan.md) | [测试计划](../06-testing-verification/test-plan.md)
**下游输出：** 记忆治理实现任务 | 测试任务 | 回归计划 | `.factory/memory` 摘要
**关联 ID：** `REQ-006`, `TASK-007`, `TASK-016`, `TASK-017`, `TASK-019`
**最后更新：** 2026-04-20

## 1. 目标

本计划用于把“记忆领域负责治理，runtime/settings 负责执行”的口径下沉为具体工作包。

本专项只解决：

- 如何把 recall / promotion / lifecycle / provider / explainability 的 owner 收口到 `domain.memory`
- 如何让 runtime planner / ranker / provider manager 降格为执行器
- 如何补齐专项测试，使治理逻辑能独立验证

本专项不解决：

- UI/产品交互
- hosted 形态的部署与租户治理
- 新后端接入本身的实现扩张

## 2. 与现有总计划的关系

本专项不是新的顶层 `TASK` 编号体系，而是对已有任务的细化实施包：

| 工作包 | 主要承接任务 | 说明 |
|---|---|---|
| `MG-WP-001` | `TASK-007` | 记忆领域治理模型显式化 |
| `MG-WP-002` | `TASK-007`, `TASK-016` | recall governance 从 runtime 默认实现回收到 domain |
| `MG-WP-003` | `TASK-007`, `TASK-017` | provider governance 从 manager 语义下沉为 domain decision |
| `MG-WP-004` | `TASK-007` | lifecycle governance 补齐 |
| `MG-WP-005` | `TASK-019` | 记忆治理专项回归与 explainability 校验 |

## 3. 工作包拆解

### `MG-WP-001` 治理模型显式化

目标：

- 在 `domain.memory` 明确治理对象，避免语义继续散落在 runtime 默认类里

建议落点：

- `src/domain/memory/`
  - `recall_governance.py`
  - `provider_governance.py`
  - `lifecycle_policy.py`
  - 或者统一 `governance_models.py / governance_policy.py`

交付：

- `RecallGovernancePolicy`
- `MemoryProviderGovernancePolicy`
- `MemoryLifecyclePolicy`
- `MemoryGovernanceDecision` / `RecallGovernanceDecision` 等领域对象

完成标准：

- memory domain 可以独立表达 recall / provider / lifecycle 决策
- runtime 默认实现不再新增业务判断

### `MG-WP-002` Recall Governance 收口

目标：

- 让 recall 的“该查什么、允许什么、预算怎么分”从 runtime 默认 planner 中回收到 domain

当前问题：

- `DefaultRecallPlanner` 仍直接决定 scope、allowed statuses、budget 和 external augmentation 开关
- `DefaultRecallRanker` 仍直接固化 overflow 与排序策略

交付：

- 由 `DefaultMemoryDomainService` 先生成 recall governance decision
- planner 只执行领域给出的 recall plan
- ranker 只执行领域给出的排序策略与预算裁剪

完成标准：

- `runtime.memory.recall_planner` 不再拥有新的 recall business policy
- `runtime.memory.recall_ranker` 不再决定哪些状态或范围“应该”被召回

### `MG-WP-003` Provider Governance 收口

目标：

- 把 external provider 的参与条件、写回条件和 delegation gate 变成领域决策

当前问题：

- `DefaultMemoryProviderManager` 仍隐含“何时 writable、何时 delegation 可写、何时 session-end writeback”的业务门槛

交付：

- provider governance decision 由 `domain.memory` 生成
- manager 只根据 decision 调用 `initialize / prefetch / sync_turn / on_session_end / on_lifecycle_apply / on_delegation`
- sanitize / read-only recall block 保留在 runtime 执行层

完成标准：

- provider manager 变成纯执行协调器
- “能不能写、为什么不能写”可由 memory domain explain

### `MG-WP-004` Lifecycle Governance 补齐

目标：

- 把记忆从“一次 promotion”升级为“完整生命周期治理”

交付：

- 正式状态机：
  - `draft`
  - `accepted`
  - `rejected`
  - `superseded`
  - `forgotten`
- 冲突规则
- supersede / forget / decay / manual override 的治理边界
- provider-aware lifecycle writeback 边界

完成标准：

- memory domain 能回答一条已存在记忆为什么失效、被替代或被隐藏
- 不再只有 candidate promotion，没有后续治理
- 生命周期治理至少具备 `review_lifecycle -> load_lifecycle_queue -> update_lifecycle_queue -> apply_lifecycle` 的最小产品闭环
- lifecycle review queue 必须具备 durable `pending / dismissed / applied` review state，而不是只存在 session explainability 投影里
- lifecycle review/apply 还必须留下 durable 审计轨迹，能回答 actor/action/status 变更历史
- 人工复核面至少要显式支持 `reopen` 与 note-only update，不能要求产品层手工拼装底层状态切换
- 人工复核面还必须支持 `queue_filter` 驱动的批量 `dismiss / reopen`，并显式区分“review filter 命中全集”与 `apply_lifecycle` 的默认选中子集
- 人工复核面还必须显式支持 reviewer resolution taxonomy，并保证 queue/audit 的 durable store、audit filter 与 explainability summary 都能稳定回读 resolution
- durable audit read model 还必须显式支持“最新优先”和 `latest_per_record_only` 视图，避免产品层自己从全量 audit 事件里倒推当前人工结论
- queue projection 还应显式给出 reviewer guidance，例如 `resolution_required`、推荐 `resolution_options` 与建议 note 模板，而不是把 conflict/decay 文案散落到产品层
- `apply_lifecycle` 触发的 external writeback 必须走专门的 `lifecycle_apply` 通道，而不是复用 `session_end`

### `MG-WP-005` 专项测试与验收

目标：

- 让记忆治理具备独立回归能力

交付：

- recall governance 测试
- provider governance 测试
- lifecycle governance 测试
- explainability canonical trace 测试

建议测试文件：

- `tests/test_domain_memory_governance.py`
- `tests/test_runtime_memory_execution_adapters.py`
- `tests/test_settings_memory_governance_bindings.py`

完成标准：

- 每类治理至少有一组领域级断言和一组集成级断言
- `preview_recall` 与 `distill_session` 的 explainability 输出能稳定解释治理结论

## 4. 分阶段顺序

### 阶段 A：对象先行

- 完成 `MG-WP-001`
- 先冻结治理对象与 decision shape

### 阶段 B：Recall / Provider 收口

- 完成 `MG-WP-002`
- 完成 `MG-WP-003`
- 让 runtime planner / ranker / manager 降格为执行器

### 阶段 C：Lifecycle 补齐

- 完成 `MG-WP-004`
- 建立完整状态机和冲突规则

### 阶段 D：专项回归

- 完成 `MG-WP-005`
- 建专项回归集，不依赖全仓 collect 才能验证

## 5. 代码影响面

### 重点修改目录

- `src/domain/memory/`
- `src/runtime/memory/`
- `src/settings/memory/`
- `tests/`

### 预期高风险文件

- `src/domain/memory/service.py`
- `src/domain/memory/ports.py`
- `src/runtime/memory/recall_planner.py`
- `src/runtime/memory/recall_ranker.py`
- `src/runtime/memory/provider_manager.py`

### 文档同步面

- `docs/04-project-development/04-design/memory-governance-design.md`
- `docs/04-project-development/04-design/memory-system-detailed-design.md`
- `docs/04-project-development/04-design/memory-runtime-interfaces.md`
- `docs/04-project-development/06-testing-verification/test-plan.md`
- `.factory/memory/*`

## 6. 验收标准

本专项完成时，应满足以下条件：

1. `domain.memory` 可以独立回答：
   - 该不该记
   - 记什么
   - 怎么记
   - 为什么这么记
   - 什么情况下返回什么记忆
2. `runtime.memory` 只剩执行语义：
   - plan 执行
   - 排序执行
   - provider 调用
   - sanitize / transport / block 注入
3. `settings.memory` 不包含记忆业务规则
4. 记忆治理专项测试可独立运行
5. `preview_recall / distill_session / explain_session_memory` 的输出可以解释治理结论

## 7. 风险与缓解

| 风险 | 缓解 |
|---|---|
| 治理对象设计过度抽象 | 先只为现有 recall / provider / lifecycle 缺口建对象，不做大而全框架 |
| runtime 与 domain 出现双 owner | 先冻结 decision shape，再删 runtime 中的业务判断 |
| explainability 跟不上治理对象变化 | 每个治理对象都要求有对应 explainability 字段或投影 |
| 生命周期扩展影响旧测试 | 先加新状态机测试，再改旧断言 |

## 8. 推荐执行顺序

如果进入实现，建议一次只推进一个工作包：

1. `MG-WP-001`
2. `MG-WP-002`
3. `MG-WP-003`
4. `MG-WP-005`
5. `MG-WP-004`

原因：

- recall / provider owner 不先收口，lifecycle 补齐很容易继续散到 runtime
- 测试尽早补，可以减少后续治理改造的回归成本

# 记忆治理专项设计方案

**项目名称：** 山海工枢 / shanforge
**文档状态：** `v0.1` 记忆治理专项设计
**负责人：** 仓库维护者
**主要读者：** 架构 | 平台开发 | 记忆领域开发 | 测试
**上游输入：** [记忆系统详细设计方案](./memory-system-detailed-design.md) | [记忆领域接口视图](./memory-runtime-interfaces.md) | [模块边界文档](./module-boundaries.md) | [架构分层与代码映射说明](./architecture-layer-code-mapping.md)
**下游输出：** 记忆领域实现收口 | 分层职责调整 | 开发计划 | `.factory/memory` 摘要
**关联 ID：** `REQ-006`, `MOD-007`, `API-006`, `API-007`
**最后更新：** 2026-04-20

## 1. 文档目标

本文件只回答一个问题：

```text
记忆系统的治理逻辑，到底哪些必须收口到 memory domain，
哪些只应该由 runtime / settings 负责执行与实现。
```

它不重复解释记忆为什么存在，也不替代 recall / promotion / distillation 的子设计。

它的目标是把当前项目中的记忆治理语义正式收口为一条清晰口径：

- `memory domain` 负责“该不该记、记什么、怎么记、为什么这么记、什么情况下返回什么记忆”
- `runtime / settings` 负责“如何调用外部能力把这些决策执行出来”

## 2. 设计结论

### 2.1 记忆领域的正式职责

记忆领域必须拥有以下业务语义：

- 是否值得形成长期记忆
- 应形成何种记忆类型
- 应进入哪一个 scope 与 lifecycle state
- 为什么接受、拒绝、降级为 draft、supersede 或 forget
- 查询时应该看哪些范围、允许哪些状态、预算如何分配
- 召回时为什么返回这些记录，而不是其他记录
- 外部 augmentation 能否参与 recall，以及其结果以何种方式进入上下文

### 2.2 记忆领域不拥有的内容

记忆领域不直接拥有以下技术实现：

- JSONL / SQLite / Postgres / Vector DB / Cloud Drive 的具体写入
- 具体 LLM、embedding、摘要器、压缩器的 SDK 或 API 调用
- HTTP、文件系统、数据库驱动、provider SDK、secret 管理
- 向量索引、检索后端、云存储、远程记忆服务的实现细节

这些能力都必须通过领域向下声明的接口来消费，而不是被领域直接持有。

### 2.3 “怎么记”要拆成两层

为了避免边界混乱，必须显式区分两种“怎么记”：

- 业务语义上的“怎么记”
  - 记成 episodic / declarative / procedural / reflective
  - 记成 accepted / draft / rejected / superseded / forgotten
  - 记到 app / project / user / workspace 哪个 scope
  - 由何种 evidence、policy 和 explainability 支撑
- 技术执行上的“怎么写”
  - 写到本地磁盘、数据库、向量库、云盘或远程服务
  - 调哪个 summarizer / compressor / embedding provider
  - 用哪个协议、格式、认证、重试和持久化后端

第一个属于 `memory domain`，第二个属于 `runtime / settings`。

## 3. 治理范围

记忆治理正式拆成 5 个子域。

### 3.1 Recall Governance

回答：

- 本轮 recall 是否发生
- 查询哪些 scope
- 允许哪些 status
- 预算如何分配
- external augmentation 是否参与
- 不同来源结果如何排序与裁剪

### 3.2 Promotion Governance

回答：

- evidence 是否足够
- candidate 是否满足置信度与 scope 规则
- 是否 accepted / draft / rejected
- 为什么得出该结论

### 3.3 Lifecycle Governance

回答：

- memory record 后续如何从 accepted 演化为 superseded / forgotten
- 冲突记忆如何处理
- 衰减、人工覆盖、复核与撤销的规则是什么

当前首轮正式规则输入已落到 memory record metadata：

- `conflict_key`
- `manual_override_status / manual_override_reason / manual_override_actor`
- `decay_after_days / last_reinforced_at`

### 3.4 Provider Governance

回答：

- external provider 是否允许参与 recall augmentation
- provider 是否只读
- session-end / delegation / sync / lifecycle apply 是否允许写回
- provider 结果如何进入 explainability 与 context

### 3.5 Explainability Governance

回答：

- 为什么这条 memory 被召回
- 为什么这条 candidate 被接受或拒绝
- external provider 的结果和写回结果如何被解释
- 哪些事实属于 canonical trace，哪些只是兼容 alias

## 4. 分层方案

| 层 | 记忆治理职责 | 不应承担的职责 |
|---|---|---|
| `access` | 暴露 inspection、review、preview、query 与 lifecycle apply 入口 | 不决定 recall / promotion / provider policy |
| `application` | 在 session 前后调用 memory domain | 不写 memory business rule |
| `domain.memory` | 统一拥有 recall / promotion / lifecycle / provider / explainability 治理 | 不直接操作磁盘、数据库、SDK、HTTP |
| `runtime.memory` | 执行已决策的 recall plan、rank、provider 调用、block sanitize | 不主导业务准入与治理策略 |
| `settings.memory` | 实现 store、provider、vector、http、cloud 等资源适配 | 不写“该不该记”“该不该召回”这类规则 |

正式判断规则：

- 任何带有“should / allowed / why / policy / decision”语义的对象，优先属于 `domain.memory`
- 任何带有“invoke / persist / fetch / transport / encode / retry / auth”语义的对象，优先属于 `runtime / settings`

## 5. 领域对象与接口方案

### 5.1 领域内应存在的治理对象

本专项建议把当前记忆治理显式抽象为以下对象：

- `RecallGovernancePolicy`
- `MemoryPromotionPolicy`
- `MemoryLifecyclePolicy`
- `MemoryProviderGovernancePolicy`
- `MemoryExplainabilityPolicy`

这些对象可以是独立 policy，也可以由 `MemoryGovernanceBundle` 聚合，但 owner 必须在 `domain.memory`。

### 5.2 领域对下的正式能力接口

不建议做一个过大的“统一记忆工具接口”。应按能力分口：

- `MemoryRecordRepositoryPort`
  - 保存与查询结构化 memory record
- `EvidenceRepositoryPort`
  - 保存与读取 evidence
- `MemoryDatasetRepositoryPort`
  - 保存蒸馏样本
- `MemoryReasoningPort`
  - 执行摘要、候选提取、压缩、归纳
- `MemorySemanticSearchPort`
  - 执行语义检索或向量召回
- `MemoryArchiveQueryPort`
  - 查 session archive / transcript / summary
- `MemoryProviderPort`
  - 对接 external augmentation provider

领域面对的是“我要什么能力”，而不是“我要写到哪个后端”。

### 5.3 当前实现与目标口径的对应关系

当前项目中：

- `MemoryPromotionPolicy` 已经正确位于 `domain.memory`
- `DefaultMemoryDomainService` 已经是记忆治理总 owner
- `augmentation diagnostics` 已经在 `domain.memory` 统一规范

但以下对象还承载了过多治理语义：

- `DefaultRecallPlanner`
- `DefaultRecallRanker`
- `DefaultMemoryProviderManager`

后续应收口为：

- 领域先产出 recall / provider governance decision
- runtime 只负责执行这些 decision

## 6. 当前问题清单

### 6.1 已经收口得比较好的部分

- promotion decision 已归领域
- explainability canonicalization 已归领域
- provider/store/reasoning 已通过 port 与领域隔离

### 6.2 仍然分散的治理语义

- recall budget、allowed status、scope selection 仍主要体现在 runtime 默认 planner 中
- 排序与 overflow 规则仍主要体现在 runtime 默认 ranker 中
- provider writable / delegation write / session-end writeback gate 仍偏 runtime owner
- lifecycle governance 还不完整，目前只有 promotion，没有完整 supersede / forget / decay 机制

### 6.3 当前专项设计不解决的内容

本文件明确不覆盖：

- UI 如何展示记忆治理
- review queue 的最终 UI 形态
- 多模态记忆表示
- hosted SaaS 形态下的租户级部署与运维

当前已落地的最小产品化闭环：

- `review_lifecycle(session_id)` 返回 session scope 下的完整 lifecycle review
- `load_lifecycle_queue(session_id, queue_filter)` 把 review 投影为产品可消费的 durable queue 读模型，默认只返回 `pending` 的 actionable items
- `reopen_lifecycle_queue(session_id, actor, record_ids | queue_filter, note)` 把已 dismiss/applied 的 queue item 恢复到 `pending`
- `update_lifecycle_queue(session_id, actor, review_status, record_ids | queue_filter)` 持久化人工 review 状态 `pending / dismissed / applied`
- `load_lifecycle_audit(session_id, audit_filter)` 读取 durable 审计轨迹，回答“谁在什么时候改了什么”，并可切到 `latest_per_record_only` 视图
- `apply_lifecycle(session_id, actor, record_ids | queue_filter)` 按 domain decision 持久化写回 memory store，并把已执行 queue item 标记为 `applied`
- `apply_lifecycle(...)` 在 provider governance 允许时会继续触发专门的 `lifecycle_apply` external writeback
- `update_lifecycle_queue(...)` 在 review status 不变但 note 改变时，会落为独立的 `review_note_updated` 审计动作，而不是继续混进 `review_status_updated`
- `update_lifecycle_queue(...)` 现已显式支持 reviewer resolution taxonomy；`dismiss / applied` 等人工结论可带 `resolution`，`reopen` 回到 `pending` 时会清空该 resolution
- `update_lifecycle_queue(...)` 与 `reopen_lifecycle_queue(...)` 在未显式给出 `record_ids` 时，可通过 `queue_filter` 对命中的 queue item 做批量 review；这里的 filter 语义是“过滤结果全集”，不是 `apply_lifecycle(...)` 使用的默认选中子集
- `load_lifecycle_audit(...)` 现可按 `action / actor / record_id / queue_review_status / resolution` 过滤，并支持 `latest_per_record_only`；`lifecycle_queue_summary / lifecycle_audit_summary` 也会稳定投影 `resolution_counts`
- `lifecycle_audit_summary.latest_entries` 现在语义上就是“最新优先”；同时会额外投影 `latest_by_record`，直接回答每条 memory 最近一次人工处理结果
- `load_lifecycle_queue(...)` 当前还会为 actionable item 投影 reviewer guidance：包括 `resolution_required`、推荐 `resolution_options` 与建议 note 模板，减少产品层自己维护冲突/衰减的说明文案
- `explain_session_memory()` 回读 `lifecycle_evaluations + lifecycle_queue_summary + lifecycle_audit_summary`

## 7. 开发方案

### 阶段一：治理模型显式化

目标：

- 把 recall / provider / lifecycle 的业务决策模型收口到 `domain.memory`

交付：

- 新增 `RecallGovernancePolicy`
- 新增 `MemoryProviderGovernancePolicy`
- 新增 `MemoryLifecyclePolicy`
- 明确这些 policy 与 `DefaultMemoryDomainService` 的关系

完成标准：

- runtime planner / ranker / provider_manager 不再自己定义治理语义，只消费领域产出的 plan / decision

### 阶段二：runtime 降格为执行器

目标：

- 保留 runtime 的技术能力，但去掉其业务 owner 色彩

交付：

- planner 只根据领域 plan 执行预算落地
- ranker 只根据领域排序策略执行排序
- provider manager 只根据 provider governance decision 执行调用和 sanitize

完成标准：

- runtime 文件不再包含新的 memory business rule

### 阶段三：补齐 lifecycle governance

目标：

- 从“只有 promotion”升级为完整 lifecycle

交付：

- `accepted / draft / rejected / superseded / forgotten` 正式状态机
- 冲突处理、撤销、人工覆盖、衰减规则

完成标准：

- 记忆领域不再只有一次性写入逻辑，而是具备可持续治理能力

### 阶段四：补齐 reasoning / compression 治理

目标：

- 明确领域如何调用外部摘要、压缩、归纳能力

交付：

- `MemoryReasoningPort` 的正式治理输入输出
- 领域内明确“何时需要摘要、何时只保留 deterministic projection”
- 不再把 provider/model 选择泄漏到领域语义中

完成标准：

- 领域只描述“需要压缩/归纳”，不描述“调用哪个具体模型”

### 阶段五：专项回归与 explainability 校验

目标：

- 保证治理收口后仍可验证

交付：

- recall governance 回归
- provider governance 回归
- lifecycle governance 回归
- explainability trace 回归

完成标准：

- 每个治理子域都有可独立运行的专项测试

## 8. 最终原则

本专项最终要固化成一句话：

```text
memory domain 只负责治理决策，
runtime / settings 只负责把这些决策执行出来。
```

或者更具体一点：

```text
记忆领域决定该不该记、记什么、怎么记、为什么这么记、什么时候返回什么记忆；
至于写到哪、怎么压缩、怎么做摘要、怎么存储、怎么检索，都通过外部能力接口完成。
```

这就是后续记忆领域设计、分层收口和实现拆分的唯一正式口径。

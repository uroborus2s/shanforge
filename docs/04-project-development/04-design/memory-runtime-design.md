# 记忆运行时设计

**项目名称：** 山海工枢 / shanforge  
**文档状态：** `v2` 专项设计基线  
**负责人：** 仓库维护者  
**主要读者：** 架构 | 平台开发 | 测试 | 记忆治理维护者  
**上游输入：** PRD | 系统架构 | 抽象 Agent 平台架构 | Hermes Agent 源码调研报告  
**下游输出：** API 设计 | 实施计划 | 测试计划 | `.factory/memory` 摘要策略  
**关联 ID：** `REQ-001`, `REQ-006`, `REQ-009`, `NFR-002`, `MOD-007`, `MOD-010`, `API-006`, `API-007`  
**最后更新：** 2026-04-15

## 1. 设计结论

`v2` 的记忆系统不再作为 `Context Engine` 的附属能力设计，而是提升为平台一级能力专题。

兼容说明：

- 文件名 `memory-runtime-design.md` 保留是为了兼容旧索引。
- 当前正式 owner 已经收口为 `domain/memory`。
- `src/runtime/memory/*` 的正式角色是基础能力层中的技术模块与兼容实现，不再被表述为独立业务 owner。

其职责不是“多存一点聊天历史”，而是：

- 接收来自 session ledger 的结构化运行事实
- 把事件和 evidence 蒸馏成可治理的记忆资产
- 以 recall / promotion / decay 策略向 `Context Engine` 提供最小、可追溯、可审计的上下文输入
- 为长期记忆、过程经验和自我进化提供统一控制面

## 2. 核心原则

### 2.1 二级资产原则

记忆永远是从事件和 evidence 蒸馏出来的二级资产，不反客为主。

这里的含义是：

- `Session Event`、`Evidence`、`Artifact` 是第一事实源
- `Memory Record` 是基于第一事实源归纳出的派生资产
- 当记忆与第一事实源冲突时，以第一事实源为准
- 任何长期记忆都必须能回溯到产生它的事件、证据或人工确认

平台因此避免两个常见错误：

1. 把模型“说得像真的总结”当成事实
2. 让长期记忆反过来覆盖真实执行轨迹

### 2.2 分层而非混存

平台不维护一个模糊的“大记忆池”，而是维护多层、不同生命周期的记忆资产。

### 2.3 local-first + port 扩展

首版记忆系统以本地结构化存储为默认实现，先保证可审计、可回放、可测试；外部向量库、远程知识库或企业 memory provider 通过 port 扩展，而不是直接成为第一实现。

### 2.4 recall 与 promotion 解耦

检索什么进入本轮上下文，与哪些结论应该晋升为长期记忆，是两个不同决策。两者不能混成一步。

## 3. 分层模型

### 3.1 Session Ledger Layer

这是记忆系统的输入层，也是运行事实真相源。

包含：

- `SessionEvent`
- `EvidenceRecord`
- `ToolResult`
- `SessionArtifact`
- `StepSummary`

特点：

- 按时间顺序记录
- 不做长期结论假设
- 支持会话回放
- 支持审计和故障追踪

### 3.2 Working Memory

当前 session / 当前 step 的临时工作记忆。

适合保存：

- 当前任务目标
- 中间结果
- 当前假设
- 尚未验证的结论

特点：

- 生命周期短
- 默认不跨 session 继承
- 可被后续 step 覆盖

### 3.3 Episodic Memory

按 session、任务或阶段形成的经历型记忆。

适合保存：

- 会话摘要
- 已完成的阶段
- 遇到的阻塞
- 关键决策和其上下文

特点：

- 以“发生过什么”为核心
- 保留时间线与背景
- 优先服务于恢复、续跑和 session search

### 3.4 Declarative Memory

稳定事实型记忆。

适合保存：

- 用户偏好
- 项目事实
- 环境约束
- 平台规则

特点：

- 需要较高置信度
- 应有稳定 scope
- 变更时需要冲突检测

### 3.5 Procedural Memory

过程型记忆，也就是“应该怎么做”。

适合保存：

- 成功工作流
- 操作规范
- 最佳实践
- 常见故障修复路径

特点：

- 可演化为 skill、runbook 或模板
- 写入门槛应高于 declarative memory

### 3.6 Reflective Memory

反思型记忆，用于支持自我进化。

适合保存：

- 哪类策略经常成功
- 哪类错误重复出现
- 哪类模型策略更适合特定场景
- 哪些 prompt / tool 组合效果差

特点：

- 来源于多次 session 的归纳
- 默认先进入 draft，不直接成为正式规则

## 4. Scope 与隔离

记忆必须带 scope，禁止默认全局共享。

建议的 scope 分层：

- `session`
- `task`
- `agent_app`
- `project`
- `user`
- `workspace`
- `organization`

隔离规则：

- child agent 默认只读取父级提供的 recall snapshot
- child agent 默认不直接写入父级长期记忆
- `session` / `task` scope 的 working memory 不跨 agent 自动共享
- `project` 与 `user` 级长期记忆只能通过 promotion pipeline 写入

## 5. 蒸馏流水线

### 5.1 Observe

运行时先把原始事实写入 session ledger：

- step 开始与结束事件
- capability 调用参数与结果摘要
- 模型输出
- 结构化 response
- evidence 引用

### 5.2 Extract Candidate

从事件和 evidence 中提取候选记忆，而不是直接写长期记忆。

候选类型：

- `fact_candidate`
- `episode_candidate`
- `procedure_candidate`
- `reflection_candidate`

### 5.3 Validate

验证候选是否满足晋升条件：

- 是否有足够 evidence
- 是否与现有记忆冲突
- 是否属于稳定事实而不是临时观察
- 是否超过最小置信度阈值

### 5.4 Promote

验证通过后，再把候选晋升为正式 `MemoryRecord`。

晋升结果可能是：

- `accepted`
- `draft`
- `rejected`
- `superseded`

### 5.5 Recall

`Context Engine` 不直接扫存储层，而是消费由 `MemoryDomainService` 组织出来的 `RecallBundle`；底层可由 `runtime/memory`、store、search 或其他基础能力模块提供技术支撑。

### 5.6 Decay / Merge

记忆系统定期做：

- 去重
- 合并
- 过期
- 降级
- 冲突重写

目标不是保留全部历史，而是保留最有价值、最可追溯、最稳定的记忆资产。

## 6. Memory Distillation Pipeline v1

### 6.1 设计目标

`v1` 的目标不是一次性实现“全自动智能记忆系统”，而是建立一个可落地、可审计、可逐步训练化的混合流水线：

- 原始事实绝不丢失
- 规则负责治理和裁决
- LLM 负责语言归纳和候选生成
- 训练化只作为后续优化方向，不成为首版前提

### 6.2 v1 总体策略

`v1` 采用三层责任分工：

1. `Deterministic Layer`
   - 负责结构化采集、字段抽取、冲突检查、promotion gate
2. `LLM Summarization Layer`
   - 负责长文本摘要、经验候选、反思候选生成
3. `Learning Dataset Layer`
   - 负责沉淀高质量样本，为后续训练小模型做准备

因此，`v1` 不是：

- 全量信息直接发给便宜模型压缩
- 也不是一开始就训练专用压缩模型

而是：

```text
raw events/evidence
-> deterministic extraction
-> selective llm summarization
-> promotion validation
-> accepted memory records
-> labeled dataset for future training
```

### 6.3 哪些环节必须优先用规则

以下环节优先使用确定性逻辑，而不是依赖 LLM：

- 事件类型识别
- step 状态迁移
- capability 名称、退出码、文件路径、写集范围提取
- evidence 引用完整性检查
- 记忆 scope 归属
- 冲突检测
- TTL / supersede / pin 规则
- promotion decision 的硬门槛

原因很简单：这些问题不是“理解自然语言”，而是“维护系统边界”。

### 6.4 哪些环节适合用 LLM

以下环节适合用 LLM 生成候选，但不直接成为正式记忆：

- 长日志摘要
- 长会话 episode summary
- 从多条 event 中提炼 `fact_candidate`
- 从多次成功/失败案例中提炼 `procedure_candidate`
- 从跨 session 轨迹中提炼 `reflection_candidate`

LLM 在这里的角色是：

- 把冗长信息压成更短表达
- 从多条事实中生成“候选结论”
- 产出方便 recall 的自然语言摘要

LLM 在这里不负责：

- 裁定事实真伪
- 决定是否晋升长期记忆
- 覆写人类确认过的规则

### 6.5 v1 推荐模型分层

推荐把记忆蒸馏相关模型分成三档：

| 档位 | 用途 | 要求 |
|---|---|---|
| `cheap summarizer` | 日志摘要、episode summary、长工具输出压缩 | 低成本、高吞吐 |
| `mid extractor` | fact/procedure/reflection candidate 生成 | 稳定归纳、结构化输出较好 |
| `human/strict gate` | 高价值长期记忆、规则升级、skill 发布 | 显式 review 或审批 |

首版默认策略：

- `episodic summary` 可走便宜模型
- `declarative candidate` 可走中档模型，但 promotion 必须过规则门
- `procedural / reflective` 默认先写 `draft`

### 6.6 v1 分阶段处理流程

#### Phase A: Raw Capture

输入：

- session events
- tool results
- model outputs
- artifacts
- evidence refs

输出：

- `SessionLedgerEntry`
- `EvidenceRecord`

这一层禁止压缩覆盖原文。

#### Phase B: Deterministic Extraction

从原始输入中抽出不需要模型理解的结构化信号：

- 通过/失败
- 文件路径
- capability id
- step output key
- approval result
- writeset
- retry count

输出：

- `StructuredObservation`

#### Phase C: Selective Summarization

只有满足以下任一条件时才调用 LLM：

- 单条 evidence 超过摘要阈值
- 单个 session 对话超过 episode 阈值
- 多条 observation 需要归纳成候选结论

输出：

- `CompressedEvidence`
- `EpisodeSummary`
- `MemoryCandidateDraft`

#### Phase D: Validation and Promotion

由规则层完成：

- 来源完整性检查
- 与现有 memory 的冲突检查
- scope 合法性检查
- 是否满足晋升门槛

输出：

- `PromotionDecision`
- `MemoryRecord`

#### Phase E: Dataset Logging

把 candidate 与最终 decision 一起沉淀成训练样本：

- 输入是什么
- 模型给了什么候选
- 最终是否通过
- 为什么通过或拒绝

这一步是后续训练化的关键。

### 6.7 v1 提示词形态

蒸馏 LLM 的提示词不应该要求“自由总结一切”，而应要求生成受限结构：

```text
Input:
- normalized events
- evidence snippets
- current scope
- candidate kind

Output JSON:
- candidate_title
- candidate_body
- candidate_kind
- confidence
- source_event_ids
- evidence_ids
- rejection_risks
```

这样做的目的不是追求漂亮文笔，而是方便进入 promotion gate。

### 6.8 v1 Promotion Gate

建议把 promotion gate 固定成“硬规则优先”：

- 没有 `source_event_ids` -> reject
- 没有 `evidence_ids` 且目标不是 working memory -> reject
- 与 human-confirmed memory 冲突 -> draft 或 reject
- 单次 session 的 procedure candidate -> 默认 draft
- 涉及平台规则或 skill 发布 -> 必须人工 review

### 6.9 v1 Recall Strategy

Recall 也分层，不直接把最新生成的 candidate 全塞给上下文：

- `accepted` memory：可进入 recall
- `draft` memory：默认不进入，除非显式调试或 review 模式
- `rejected` memory：保留样本，不参与 recall
- `superseded` memory：只做审计，不进入 recall

### 6.10 v1 与后续训练的关系

后续如果样本足够，再考虑训练小模型，但训练目标应拆分：

- `candidate extractor model`
- `episodic summarizer model`
- `promotion scorer model`
- `recall ranker model`

不建议训练一个“大一统 memory model”，因为：

- 任务目标差异太大
- 标注口径不容易统一
- 错误定位会更困难

### 6.11 何时值得训练

只有同时满足以下条件，训练才有意义：

- 已积累足够多的 candidate -> decision 样本
- rejection reason 有稳定标签
- prompt + 商用模型成本已经明显成为瓶颈
- recall / promotion 错误模式已经足够清晰

在这之前，优先做高质量数据和高质量 gate。

## 7. 检索流水线

标准 recall 流程建议如下：

```text
1. 输入 RecallQuery
2. 解析当前 session / step / app / scope
3. 先返回 pinned memories
4. 再检索 session 级 episodic memory
5. 再检索 project / user 级 declarative memory
6. 再检索 procedural / reflective memory
7. 过滤无 evidence、低置信度和冲突项
8. 结合预算返回 RecallBundle
9. Context Engine 把 RecallBundle 装入 ContextEnvelope
```

排序维度：

- 当前 step 相关性
- scope 匹配程度
- 新近性
- 事实稳定性
- evidence 完整度
- 用户显式 pin

## 8. 关键数据结构

```text
SessionEvent
- id
- session_id
- step_id
- type
- payload
- timestamp

EvidenceRecord
- id
- session_id
- kind
- source_ref
- summary
- content_digest
- producer
- timestamp

MemoryCandidate
- id
- kind
- scope
- title
- body
- source_event_ids
- evidence_ids
- confidence
- extracted_at

MemoryRecord
- id
- kind
- scope
- title
- body
- status
- confidence
- supporting_refs
- supersedes
- created_at
- updated_at

RecallQuery
- session_id
- app_id
- workflow_id
- step_id
- user_input
- scope_filters
- budget

RecallBundle
- pinned_records
- retrieved_records
- evidence_refs
- diagnostics
```

## 9. 写入治理

### 8.1 哪些内容不能直接进入长期记忆

- 单次模型猜测
- 未验证的 TODO
- 临时草稿
- 只存在于对话措辞中的模糊偏好
- 没有证据支撑的“经验总结”

### 8.2 哪些内容可以优先晋升

- 用户明确确认的稳定偏好
- 在多个 session 中重复成立的项目事实
- 带证据支撑的关键架构决策
- 多次复现后收敛出的高价值 procedure

### 8.3 自我进化边界

Reflective / Procedural memory 可以为自我进化提供候选输入，但不能直接改写正式规则文件、skills 或 `.factory/memory`。正式发布必须经过显式 review 或审批。

## 10. 典型实例

### 9.1 终端命令结果蒸馏为事实记忆

原始事实：

- event: 执行 `uv run pytest tests/test_context_engine.py`
- evidence: 测试输出 `2 passed in 0.04s`

蒸馏过程：

1. ledger 记录命令和测试输出
2. extractor 生成 `episode_candidate`: “本次会话已验证 context engine 测试通过”
3. 如果同类测试在多个 session 中持续通过，可进一步生成 `declarative_candidate`: “当前 scaffold 的 context engine 基础契约稳定可运行”
4. recall 时，默认优先返回摘要与 evidence ref，而不是整段终端原文

不应该发生的事：

- 直接把“系统已经完全稳定”写成长期事实

### 9.2 架构决策蒸馏为长期项目记忆

原始事实：

- event: 用户明确确认“记忆业务 owner 在 `domain/memory`，技术能力和实现继续分层”
- evidence: 已提交的设计文档与时间戳

蒸馏过程：

1. 生成 `fact_candidate`: “`MOD-007` 的业务 owner 在 `domain/memory`，`runtime` 只提供技术能力”
2. 验证其有用户确认和正式文档支撑
3. 晋升为 `project` scope 的 declarative memory
4. 后续 recall 时，这条记忆可直接约束实现与 review

不应该发生的事：

- 把一次 brainstorming 中尚未确认的方向也写成正式事实

### 9.3 重复修复经验蒸馏为 procedural memory

原始事实：

- 多次 session 中都出现“上下文膨胀导致 prompt 失控”
- 对应 evidence 显示：通过摘要替换旧对话、降级低价值检索片段后恢复稳定

蒸馏过程：

1. 多个 episode 被 reflective analyzer 聚合
2. 形成 `procedure_candidate`: “先裁剪检索片段，再压缩工具输出，再把旧对话替换为摘要”
3. 经人工 review 后晋升为 procedural memory
4. 后续可进一步沉淀为 skill、runbook 或实现策略

不应该发生的事：

- 因为一次偶然成功就把方法升级为平台硬规则

## 11. 实施落点

推荐的首版代码落点：

```text
src/application/ports/
  domain_services.py

src/application/execution/
  service.py

src/domain/memory/
  models.py
  ports.py
  policy.py
  service.py

src/runtime/memory/
  runtime.py
  policy.py
  summarizer.py

src/settings/memory/
  store.py

src/settings/memory/
  evidence_store.py

src/settings/memory/
  dataset_store.py
```

模块关系：

- `Session Store / Event Log` 负责保存第一事实源
- `DefaultMemoryDomainService` 负责记忆业务语义与主链编排
- `src/runtime/memory/*` 负责 local-first 技术辅助、summarizer 和兼容实现
- `Context Engine` 负责消费 recall bundle 并装配上下文

## 12. 版本记录

| 版本 | 日期 | 变更内容 |
|---|---|---|
| `v2.0` | 2026-04-14 | 新增记忆运行时专项设计，确立二级资产原则和蒸馏流水线 |
| `v2.1` | 2026-04-14 | 补充 `Memory Distillation Pipeline v1`，明确规则、LLM 和未来训练化的分工 |
| `v2.2` | 2026-04-15 | 收口到 `domain owner + runtime capability + settings implementation` 的正式口径 |

# 子设计二：Candidate 与 Promotion

**最后更新：** 2026-04-14

## 1. 目标

定义候选记忆如何产生、验证和晋升。

## 2. 核心对象

- `MemoryCandidate`
- `PromotionDecision`
- `MemoryRecord`

## 3. 设计结论

- candidate 先于 record
- promotion 与 recall 解耦
- 无来源 refs 的 candidate 不得晋升长期记忆
- procedural / reflective 默认先 `draft`

## 4. 首版落点

- 在 `domain.memory` 建模 candidate / record / decision
- 先实现 deterministic gate
- LLM 只生成 candidate draft，不直接写 store

## 5. 当前实现状态

- promotion gate 已在 `domain.memory.policy` 中收口为 `MemoryPromotionPolicy`
- 当前策略负责：
  - `min_confidence`
  - `min_confidence_by_kind`
  - `draft_kinds`
  - `allowed_scopes_by_kind`
- `DefaultMemoryDomainService` 负责组装 supporting refs、调用 policy、写入 record 和 decision
- 默认容器已经支持通过 settings / env 外置这些 promotion policy 参数

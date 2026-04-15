# 子设计一：Session Ledger

**最后更新：** 2026-04-15

## 1. 目标

定义记忆系统的一手事实源。

## 2. 核心对象

- `SessionEvent`
- `SessionArtifact`
- `EvidenceRecord`

## 3. 设计结论

- event / artifact 必须先落 ledger，再进入蒸馏
- ledger 条目必须有稳定 `id`
- ledger 条目必须支持 replay 与 source refs
- 蒸馏层不得覆盖 ledger 原文

## 4. 首版落点

- 扩展 `domain.session.models`
- 补充 event / artifact 的 `id` 与时间戳
- 由记忆蒸馏主链把 ledger 投影为 `EvidenceRecord`

## 5. 当前实现状态

- `SessionEvent` / `SessionArtifact` 已带稳定 `id` 与 `created_at`
- 当前 `DefaultMemoryDomainService -> EvidenceRepositoryPort` 投影 evidence 时已使用稳定 ID
- 同一 session 的 repeated distill 不再重复写入同一 evidence record

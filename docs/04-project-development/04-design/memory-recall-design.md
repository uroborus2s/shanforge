# 子设计三：Recall 与 Context Consumption

**最后更新：** 2026-04-14

## 1. 目标

定义记忆如何进入 `Context Engine`。

## 2. 核心对象

- `RecallQuery`
- `RecallBundle`
- `ContextSegmentType.LONG_TERM_MEMORY`

## 3. 设计结论

- recall 结果必须带 diagnostics 和 source refs
- `Context Engine` 只消费 recall bundle
- recall 默认只返回 `accepted` memory
- recalled memory 与 working memory 必须分层显示

## 4. 首版落点

- `MemoryDomainService.prepare_session()` 先 recall
- `ContextEngine` 新增 long-term memory segment 装配
- 测试覆盖 recall hit 和 context segment 类型

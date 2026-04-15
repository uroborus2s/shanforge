# 子设计四：Distillation 与 Learning Dataset

**最后更新：** 2026-04-15

## 1. 目标

定义首版蒸馏流水线与后续训练化边界。

## 2. 设计结论

- 首版采用 `规则治理 + 选择性 LLM 候选生成 + 样本沉淀`
- 训练化只在样本足够后再启动
- 不训练“大一统 memory model”
- 后续优先考虑小模型：
  - `candidate extractor`
  - `episodic summarizer`
  - `promotion scorer`
  - `recall ranker`

## 3. 首版落点

- 先实现 deterministic extraction
- 为 summarizer 保留 port
- 保存 `candidate -> decision` 样本链

## 4. 当前实现状态

- `MemorySummarizerPort` 已在运行时保留，默认由 `null summarizer` 占位
- 当前记忆蒸馏主链已把每个 candidate 的 promotion 结果写入 dataset store
- 默认容器支持 `in-memory` 和 `JSONL-backed` dataset store，便于后续离线标注与训练准备
- 当前容器在显式配置 `memory_summarizer_provider/model` 时，可切换到 `LLMMemorySummarizer`
- 当前 `LLMMemorySummarizer` 已严格要求 candidate draft 至少返回 `title/body`；`kind/scope/confidence` 不再信任模型输出
- 同一 session repeated distill 时，dataset sample 已按稳定 ID 幂等更新，不再重复追加

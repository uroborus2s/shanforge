# 变更摘要

## 2026-04-13

- 新增 `docs/04-project-development/02-discovery/hermes-agent-source-analysis-report.md`：
  - 形成对 `NousResearch/hermes-agent` 的正式中文源码调研报告
  - 内容覆盖总体架构、核心算法、关键数据结构、运行时流程、复刻建议与对 `shanforge` 的采纳启发
- 同步更新正式文档导航与索引：
  - `docs/index.md`
  - `docs/04-project-development/02-discovery/index.md`
  - `docs/04-project-development/10-traceability/document-index.md`
- 同步更新 `.factory/memory/doc-map.md`，为新调研文档补齐压缩映射

## 2026-04-12

- 收紧 `gitcommitzh` 的单轮交付要求：
  - 当用户原始消息已经明确要求提交时，必须在同一轮内完成提交和回显
  - 禁止先交付中间态摘要，再等待用户下一轮重复说“提交”

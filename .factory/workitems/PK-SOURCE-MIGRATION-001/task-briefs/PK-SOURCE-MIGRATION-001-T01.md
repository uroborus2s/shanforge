# 实施任务简报

## 工作项

- 任务：`PK-SOURCE-MIGRATION-001-T01` PRD 与 Markdown 需求提取
- 目标：让正式 PRD 同时可供人阅读并由固定代码确定性拆出 REQ、NFR 和 AC。
- 设计：稳定章节 ID 是身份；标题可改；字段使用中文列表标签；不使用行号。
- 接口：`MarkdownExtractor.extract()` 的 `SourceContribution/v1` 增加需求实体、locator、`CONTAINS` 边和 `source_section_key`。
- UI：保持 PRD 自然阅读结构，增加能力分类和用户故事。
- 测试：先扩展 extractor 测试，再实现并补齐 PRD；读取冻结 manifest，逐字段比较 R009 和 PRD 投影。
- 完成条件：16/64/11 可从 PRD 单独提取，状态与章节定位完整，ID/标题/优先级/规范语句/AC/NFR 字段与冻结 R009 等价。

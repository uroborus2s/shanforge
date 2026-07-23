# 实施任务简报

## 工作项

- 任务：`PK-SOURCE-MIGRATION-001-T03` 只读站点阅读与追踪
- 目标：让需求、任务和文档详情形成可理解、可返回、可追踪的独立页面。
- 设计：需求列表只显示 REQ/NFR并按分类组织；AC 嵌套在需求详情；关系按冻结矩阵生成深链；文档正文在 CLI 构建期读取并按白名单 Markdown 子集安全渲染。
- 接口：站点 DTO 增加 `entity_kind` 和可选 `content_markdown`，不进入 SQLite 长期正文。
- UI：技术快照默认折叠；详情继续使用独立 URL 和返回按钮。
- 测试：renderer、security、PM projection 和静态站点集成测试；覆盖 raw HTML、恶意 URL 文本、symlink、路径逃逸、Hash mismatch、超限文件、shared-restricted 和 renderer cache 版本。
- 完成条件：需求分类、矩阵全部双向关系链接、完整文档正文、折叠技术信息和稳定 cache hit 均有自动化断言。

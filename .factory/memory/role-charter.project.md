# 项目角色压缩卡

- 生成时间：2026-04-09 13:35:50
- 负责人：项目负责人
- 当前阶段：IMPLEMENTATION

## 使用边界

- 禁止把下列“必要时回源”候选理解成默认先读。
- 默认先读压缩入口和 summary，不足时再单文件回源正式文档。

## 当前阶段主要角色

### coordinator
- 负责：推进阶段、看板、Gate、交接、团队动能
- 优先读取：先读 `.factory/memory/runtime-brief.md`、`doc-map.md`、当前 summaries；必要时回源阶段检查/质量报告
- 交付要求：只改自己负责的产物，并在交接时说明输入、输出、未决问题、下一步。

### requirements-analyst
- 负责：结构化 REQ/NFR、依赖、风险、建议测试点
- 优先读取：先读压缩入口和需求相关 summaries；必要时回源 `prd.md`、`requirements-analysis.md`、`requirements-verification.md`
- 交付要求：只改自己负责的产物，并在交接时说明输入、输出、未决问题、下一步。

### backend-engineer
- 负责：后端代码、测试、PR
- 优先读取：先读压缩入口和技术 summaries；进入实现前必须回源 `technical-selection.md`，再按需回源 `backend-design.md`、`api-design.md`、`TASK-*`
- 交付要求：只改自己负责的产物，并在交接时说明输入、输出、未决问题、下一步。

### frontend-engineer
- 负责：前端代码、测试、PR
- 优先读取：先读压缩入口和技术/设计 summaries；进入实现前必须回源 `technical-selection.md`，再按需回源 `ux-ui-design.md`、`api-design.md`、`TASK-*`
- 交付要求：只改自己负责的产物，并在交接时说明输入、输出、未决问题、下一步。

### qa-engineer
- 负责：测试计划、回归、质量门禁
- 优先读取：先读压缩入口和测试 summaries；必要时回源 `docs/04-project-development/06-testing-verification/*`、`docs/04-project-development/07-release-delivery/*`
- 交付要求：只改自己负责的产物，并在交接时说明输入、输出、未决问题、下一步。

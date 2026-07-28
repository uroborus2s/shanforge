# 文档压缩映射

## 事实源优先级与最小读取规则

- 新会话只读 `.factory/memory/agent-session.md`；信息不足时按下表单文件回源，不默认散读 memory、docs 或 workitems。
- 正式文档和 work item ledger 高于 memory summary；HTML 和 cache 是可重建投影，不作为事实源。
- Markdown 按 `document_id + section_id`，Python 按 AST qualified symbol，JSON 按 Pointer，JSONL 按 event UID 定位；不使用行号作为持久索引。

## 快速命令

- 当前项目 HTML：运行已安装 `using-shanforge` skill 自带的
  `scripts/project_snapshot.py --project-root <项目根目录>`。
- 单一事实回源：按下方 owner 映射只读与问题直接相关的最小文件。

## 正式 owner 映射

- `docs/index.md` -> `.factory/memory/runtime-brief.md`
- `docs/document-index.md` -> `.factory/memory/runtime-brief.md`
- `docs/05-design/index.md` -> `.factory/memory/runtime-brief.md`
- `docs/06-delivery/index.md` -> `.factory/memory/runtime-brief.md`
- `docs/01-getting-started/*.md` -> `.factory/memory/runtime-brief.md`
- `docs/02-user-guide/*.md` -> `.factory/memory/runtime-brief.md`
- `docs/03-developer-guide/interface-reference.md` -> `.factory/memory/api.summary.md`
- `docs/03-developer-guide/*.md` -> `.factory/memory/runtime-brief.md`
- `docs/04-product/prd.md` -> `.factory/memory/prd.summary.md`、`.factory/memory/requirements-verification.summary.md`
- `docs/04-product/requirements-matrix.md` -> `.factory/memory/traceability.summary.md`、`.factory/memory/graph/traceability.json`
- `docs/05-design/solution-overview.md` -> `.factory/memory/architecture.summary.md`
- `docs/05-design/system-architecture.md` -> `.factory/memory/architecture.summary.md`
- `docs/05-design/module-domain-design.md` -> `.factory/memory/architecture.summary.md`
- `docs/05-design/data-design.md` -> `.factory/memory/architecture.summary.md`
- `docs/05-design/frontend-design.md` -> `.factory/memory/architecture.summary.md`
- `docs/05-design/ux-ui-design.md` -> `.factory/memory/architecture.summary.md`
- `docs/05-design/memory-design.md` -> `.factory/memory/architecture.summary.md`
- `docs/05-design/api-design.md`、`interface-matrix.md` -> `.factory/memory/api.summary.md`、`.factory/memory/traceability.summary.md`
- `docs/05-design/technical-selection.md` -> `.factory/memory/tech-stack.summary.md`
- `docs/05-design/workflow-execution-design.md` -> `.factory/memory/tasks.summary.md`、`.factory/memory/runtime-brief.md`
- `docs/06-delivery/test-plan.md` -> `.factory/memory/tests.summary.md`
- `docs/06-delivery/*.md` -> `.factory/memory/runtime-brief.md`

## 机器配置与展示边界

- `.factory/catalog/ai-sdlc-catalog.source.json`：稳定机器 Catalog 源，不属于人类设计文档。
- `.factory/catalog/document-publication-policy.json`：文档发布机器策略。
- `.factory/project-knowledge/*.json`：来源注册、关系声明、ID alias 和 cache policy。
- `.factory/cache/site/`：可重建只读快照，Git 忽略。
- 旧 `.factory/pm` 不再保存事实；项目状态从正式源和 ledger 生成可重建的只读 HTML。

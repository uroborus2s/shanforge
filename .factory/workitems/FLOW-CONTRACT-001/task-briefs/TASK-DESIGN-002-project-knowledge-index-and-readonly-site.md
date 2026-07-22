# TASK-DESIGN-002 项目知识索引与只读项目站点设计简报

## 工作项

- WorkItem：`FLOW-CONTRACT-001`
- 任务：`TASK-DESIGN-002-project-knowledge-index-and-readonly-site`
- 状态：`ready_for_same_reviewer_rereview`（iteration 2）
- 上游：R009 精确 Manifest `8be9d829ea2a895eae043eaf054914cb03b7457a43d51c142cc4ad7f41f577ae`

## 目标

把已批准 R009 转成字段级 39 表、稳定 locator、增量 generation、固定 CLI、多页面站点、异步同步、缓存与迁移的可执行技术设计；正式设计 review 通过后只增补现有 owner 文档，不新建平行正式设计页。

## 输出

- `.factory/workitems/FLOW-CONTRACT-001/drafts/DESIGN-PROJECT-KNOWLEDGE-001.R001.md`
- `.factory/workitems/FLOW-CONTRACT-001/plans/TASK-IMPLEMENT-003-P001.md`

## 完成口径

独立 reviewer 必须验证 16 REQ/64 AC/11 NFR、39 表、137 字段、50 transitions、CLI、站点、权限、迁移和测试计划均可实施，且 Critical/Important 为 0。实现者状态只能到 `ready_for_review`。

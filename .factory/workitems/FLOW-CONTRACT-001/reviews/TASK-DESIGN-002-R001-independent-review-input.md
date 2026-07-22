# TASK-DESIGN-002 R001 独立评审输入

## Review 类型

技术设计 + 实施计划独立 Spec/Quality/UI Review，只读，不允许修改任何文件。

## 输入

- 已批准需求：`.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001-R009.md`
- 机器合同：`.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001.contract.R009.json`
- PM field map：`.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001.pm-field-map.R009.json`
- 技术设计：`.factory/workitems/FLOW-CONTRACT-001/drafts/DESIGN-PROJECT-KNOWLEDGE-001.R001.md`
- 实施计划：`.factory/workitems/FLOW-CONTRACT-001/plans/TASK-IMPLEMENT-003-P001.md`
- 设计 task brief：`.factory/workitems/FLOW-CONTRACT-001/task-briefs/TASK-DESIGN-002-project-knowledge-index-and-readonly-site.md`
- T01–T06 task briefs：`.factory/workitems/FLOW-CONTRACT-001/task-briefs/TASK-IMPLEMENT-003-P001-T0*.md`
- 作者验证：`.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-DESIGN-002-R001-author-verification.md`
- 架构约束：根 `AGENTS.md`。

## 必查问题

1. 设计是否逐项覆盖 16 REQ、64 AC、11 NFR，没有把未来工作冒充首版完成。
2. 39 表是否能支持来源级增量删除、同边多来源、原子 generation、稳定 locator、两 FTS 和 137 字段 PM 投影；是否存在必须补表、并表或删表的问题。
3. 五层 owner、port 方向与 composition 是否合规，CLI 是否把实现泄漏到 access。
4. 页面树是否满足只读、全页面详情、返回按钮、商业展示、深链、打印、响应式和 WCAG；是否仍隐含 drawer。
5. `PROJECT_STATE_SYNC` 是否复用 durable owner、能防主工作树竞写、过期执行器和无限重试。
6. Catalog/PM/requirements-matrix 迁移是否保留事实、可回滚且不建立新正式文档。
7. T01–T06 是否能独立验证，命令和文件路径是否足以让新执行者实施。

## 输出要求

输出 `approved` 或 `changes_requested`，列出 Critical/Important/Minor，按 100 分 rubric 评分，并写 reviewer type/id/独立性证据。普通内部 review 不创建新人工 Gate；若通过，`human_confirmation_required=false`，因为用户已批准 R009 Manifest 内的设计与实施授权。

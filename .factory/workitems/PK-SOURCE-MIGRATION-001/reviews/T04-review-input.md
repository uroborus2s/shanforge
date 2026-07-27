# T04 独立评审输入包

- Work item：`PK-SOURCE-MIGRATION-001`
- Task：`PK-SOURCE-MIGRATION-001-T04`
- Review type：任务级独立实现评审
- Requirements：`REQ-PKI-008`
- Task brief：
  `.factory/workitems/PK-SOURCE-MIGRATION-001/task-briefs/PK-SOURCE-MIGRATION-001-T04.md`
- Implementer report：
  `.factory/workitems/PK-SOURCE-MIGRATION-001/reports/T04-implementer-report.md`
- Verification evidence：
  `.factory/workitems/PK-SOURCE-MIGRATION-001/evidence/T04-red-green-and-ui-verification.md`
- Ledger：`.factory/workitems/PK-SOURCE-MIGRATION-001/ledger.jsonl`

## Diff package

只评审下列路径的当前任务相关变更：

- `src/runtime/project_knowledge/extractors.py`
- `src/settings/project_knowledge/sqlite_index.py`
- `src/runtime/project_knowledge/site_renderer.py`
- `tests/test_project_knowledge_extractors.py`
- `tests/test_project_knowledge_index.py`
- `tests/test_project_site_renderer.py`
- `docs/05-design/data-design.md`
- `docs/05-design/frontend-design.md`
- `.factory/project-knowledge/source-registry.json`
- `.factory/project-knowledge/relation-declarations.json`
- `.factory/workitems/PK-SOURCE-MIGRATION-001/plan.md`
- `.factory/workitems/PK-SOURCE-MIGRATION-001/task-briefs/PK-SOURCE-MIGRATION-001-T04.md`

## 架构与产品约束

- 依赖链保持 `access -> application -> domain -> runtime -> settings`。
- SQLite 仅作本地索引与投影；不得成为需求或设计事实源。
- HTML、SQLite 和 cache 不提交 Git，静态站点必须由固定 CLI 可重建。
- 页面只读，不新增编辑、拖拽或状态修改。
- 不新增 SQLite 表，不新增平行正式需求或设计文档。
- 任务首先回答“为什么做、具体做什么、得到什么、怎样算完成”。
- 需求页必须从大到小展示产品、业务域、需求和验收标准，并保留详情深链。

## Reviewer 输出要求

- 只读检查，不修改任何文件，不把任务标记为完成。
- 声明 reviewer 身份及未参与本次实现的独立性证据。
- 按 100 分 rubric 给出需求符合度、架构一致性、测试充分性、代码质量、文档与记忆同步。
- 分别列出 Critical、Important、Minor。
- 输出 `approved` 或 `changes_requested`；若通过，下一状态仍写
  `pending_human_confirmation`，由主任务根据用户已明确的实施授权收口。

# PK T04 任务简报共享 Schema 修复独立评审输入

- Work item：`PK-SOURCE-MIGRATION-001`
- Task：`PK-SOURCE-MIGRATION-001-T04-SCHEMA-REPAIR`
- Review：任务级 Spec + Quality Review

## Inputs

1. `task-briefs/PK-SOURCE-MIGRATION-001-T04-schema-repair.md`
2. `reports/T04-final-verification-root-cause-20260727-iteration-2.md`
3. `reports/T04-schema-repair-implementer-report-20260727.md`
4. `evidence/T04-schema-repair-red-green-verification-20260727.md`
5. 当前限定 diff：
   - `src/runtime/project_knowledge/extractors.py`
   - `tests/test_project_knowledge_extractors.py`
   - `.factory/project-knowledge/source-registry.json`
   - `docs/05-design/data-design.md`
   - `.factory/workitems/STATE-RECONCILIATION-001/task-briefs/STATE-RECONCILIATION-001-T01.md`
6. 本 WorkItem ledger 最新事件。

## 评审重点

- 字段别名是否只有一份事实源。
- 同行值、空值缩进列表和未知字段负例是否锁定根因。
- 是否只修唯一真实缺失的任务目标。
- `markdown-v4` 是否能确定性失效旧贡献。
- 五文件、Ruff、Mypy、快照、桌面/移动浏览器证据是否充分。
- API 与正式发布 N/A 是否合理。

## 边界

Reviewer 只读，不修改文件、Git index 或外部系统。输出 `approved` 或
`changes_requested`，包含评分、C/I/M、独立性证据和 N/A 裁决。

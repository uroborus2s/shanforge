# TASK-001 Review Input

## Inputs

- Work item：`DOC-FACTORY-RESTRUCTURE-001`
- Task：`TASK-001-destructive-full-doc-migration`
- task brief：`.factory/workitems/DOC-FACTORY-RESTRUCTURE-001/task-briefs/TASK-001-destructive-full-doc-migration.md`
- implementer report：`.factory/workitems/DOC-FACTORY-RESTRUCTURE-001/reports/TASK-001-implementer-report.md`
- verification evidence：`.factory/workitems/DOC-FACTORY-RESTRUCTURE-001/evidence/TASK-001-verification.md`
- diff package：本任务文件范围内 diff
- ledger：`.factory/workitems/DOC-FACTORY-RESTRUCTURE-001/ledger.jsonl`

## Spec Review Checklist

- 新正式文档是否覆盖六类任务：任务分解、系统总设计、模块设计、UI 设计、开发、测试。
- 新正式文档是否写清输出包、`.factory` 落盘边界和 gate。
- 破坏性删除是否只删除旧页面、旧原型、旧生成页、旧快照和非正式备份资产。
- 根导航、目录首页、文档索引、需求矩阵和 doc-map 是否只引用现存正式路径。
- `.factory/README.md` 是否说明 memory、workitems、pm 的职责，以及旧 process/generated/history 的清理边界。
- 历史 work item evidence、reports、reviews 和 ledger 是否保持原路径。
- 正式文档负责人、执行人和版本历史是否没有署名为 `Codex`。

## Quality Review Checklist

- 删除清单是否与用户“旧资产旧结构都删除”的要求一致。
- 是否没有修改业务代码。
- 测试是否覆盖新契约入口、旧路径删除、无断链和署名规则。
- 验证证据是否为本轮新鲜命令。
- docs-stratego 通过后是否仍有未登记 Markdown 页面。

## 预期结论

作者自检只能进入 `ready_for_review`。`approved` 必须来自独立 reviewer。

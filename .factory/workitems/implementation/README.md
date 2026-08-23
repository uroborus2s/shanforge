# 实施任务目录

后续软件工厂接手后的工程治理、重构或专项维护任务统一进入 `TASK-*`。

新 work item 使用标准结构：

```text
.factory/workitems/<WORKITEM-ID>/
  brief.md
  plan.md
  task-briefs/
  evidence/
  reports/
  reviews/
  ledger.jsonl
```

当前文档基线采用破坏性全量迁移：旧过程页、旧原型、旧生成页面和旧 memory 快照不再保留。历史 work item 的 evidence、reports、reviews 和 ledger 属于执行审计事实，除非有单独归档方案，不批量删除。

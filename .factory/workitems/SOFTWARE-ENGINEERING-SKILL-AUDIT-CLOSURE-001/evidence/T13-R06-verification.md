# T13-R06 真实 TaskCard 图验证

- 迁移范围：本工作项 T09、T10、T11、T12、T13、T13-R01 至 R06，共 11 张 TaskCard。
- 每张卡都有稳定 owner；depends_on 仅使用 `none` 或本工作项中真实存在的完整 TaskCard ID。
- reviewer/测试失败等事件前置条件继续保留在 ledger，不混入执行依赖 DAG。
- 真实命令：`python3 skills/writing-plans/scripts/validate_task_graph.py .factory/workitems/SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001/task-briefs/*.md`。
- 结果：退出码 0、无错误；ledger JSON/唯一键与 `git diff --check` 通过。

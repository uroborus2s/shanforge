# 计划复审 I3 处理记录

## 复审意见

复审确认 I1、I2、I4、I5 已关闭；I3 仍要求 canonical Task 端点和写边前端点存在性门。

## 处理

- 符合稳定格式的 JSONL `task/work_item` 直接使用任务编号作为 canonical entity ID。
- task brief 的 ``- 任务：`TASK-ID` `` 同样投影为该 ID，并提供中文标题和文档 locator。
- 多个 ledger 声明同一任务时，最高 authority 内按可解析 `updated_at` 选择最新状态；
  无时间时按稳定 source ID 决定，不再生成来源哈希 ID。
- Ledger 当前状态与 task brief 中文标题按字段职责合并；同权威冲突中文标题失败关闭。
- 九个矩阵 Task ID 均由当前 registry 可发现；关系声明测试先验证全部端点，再验证
  88 条边的目标、类型、强度和置信度。
- 真实冷重建成功，SQLite 中 88 条任务追踪边无缺失端点。

结论：I3 已在实现和自动化 Gate 中关闭。

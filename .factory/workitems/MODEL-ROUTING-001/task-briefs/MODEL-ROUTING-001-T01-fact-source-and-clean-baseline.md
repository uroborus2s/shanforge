# 任务简报

## 工作项

- 工作项：`MODEL-ROUTING-001`
- 任务：`MODEL-ROUTING-001-T01`
- 状态：`active`
- 优先级：`P0`
- 任务层级：`system`
- 关联目标：`MODEL-ROUTING-001`
- 强关系：`IMPLEMENTS`
- 流水账：`.factory/workitems/MODEL-ROUTING-001/ledger.jsonl`

## 目标

确定当前正式事实、归属现有工作区变更、修复基线测试，并产出可从干净克隆复现的全绿证据。

## 允许修改

- 经盘点确认属于当前事实收口和测试闭环的现有文件。
- `.factory/workitems/MODEL-ROUTING-001/**`
- 必要的 `.factory/memory/**`

## 禁止修改

- 与本任务无关的用户改动。
- 远端、PR、merge、部署和生产状态。
- 已删除的 Shanforge 平台运行时。

## 验证

- 当前工作区正式测试全绿。
- 干净克隆使用同一命令全绿。
- Git diff 无空白错误，事实源无当前阶段冲突。

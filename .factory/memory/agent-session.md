# Agent 会话卡

- 生成时间：2026-09-01 21:50 +0800
- 项目：`shanforge`
- 当前工作项：`SOFTWARE-LIFECYCLE-GOVERNANCE-001`
- 当前任务：`SOFTWARE-LIFECYCLE-GOVERNANCE-001-T04`
- 当前状态：`closed`
- 当前焦点：软件生命周期治理实现与干净克隆验证已闭环
- 下一动作：`none`

## 当前事实

- 用户已授权统一 Skill-first 正式设计事实、补生命周期输入输出/Gate 矩阵和跨文档一致性校验，并要求提交后干净克隆全绿。
- Sol 裁决整体为 `complex / medium`；T01–T03 worker 固定 Terra/medium，T04 独立 reviewer 固定 Terra/high。
- T01–T03 与两轮 Review 整改已完成；完整候选 `290 passed / 4 subtests passed`，Ruff、38/38 Skill validator、6 TOML / 176 JSON / 47 JSONL、案例目录和 diff hygiene 全绿。

## 当前 Gate

- `none`：WorkItem 已关闭，没有遗留人工 Gate。

## 允许范围

- 现行设计基线、文档索引、需求追踪、测试登记、旧机器附件资格和本 WorkItem 状态文件。
- 禁止新增 `src/` runtime、服务、API 平台、依赖、远端或生产动作。

## 恢复入口

- `.factory/workitems/SOFTWARE-LIFECYCLE-GOVERNANCE-001/brief.md`
- `.factory/workitems/SOFTWARE-LIFECYCLE-GOVERNANCE-001/plan.md`
- `.factory/workitems/SOFTWARE-LIFECYCLE-GOVERNANCE-001/ledger.jsonl`
- `.factory/workitems/SOFTWARE-LIFECYCLE-GOVERNANCE-001/task-briefs/`

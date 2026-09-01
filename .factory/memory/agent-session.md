# Agent 会话卡

- 生成时间：2026-09-01 21:44 +0800
- 项目：`shanforge`
- 当前工作项：`SOFTWARE-LIFECYCLE-GOVERNANCE-001`
- 当前任务：`SOFTWARE-LIFECYCLE-GOVERNANCE-001-T04`
- 当前状态：`ready_for_commit`
- 当前焦点：同一独立 reviewer 已以 `97 / C0-I0-M0` 关闭 I1–I4
- 下一动作：`create_exact_local_commit_then_clean_clone_verify`

## 当前事实

- 用户已授权统一 Skill-first 正式设计事实、补生命周期输入输出/Gate 矩阵和跨文档一致性校验，并要求提交后干净克隆全绿。
- Sol 裁决整体为 `complex / medium`；T01–T03 worker 固定 Terra/medium，T04 独立 reviewer 固定 Terra/high。
- T01–T03 与两轮 Review 整改已完成；完整候选 `290 passed / 4 subtests passed`，Ruff、38/38 Skill validator、6 TOML / 176 JSON / 47 JSONL、案例目录和 diff hygiene 全绿。

## 当前 Gate

- `create_exact_local_commit`：用 gitcommitzh 精确提交本 WorkItem，再从提交新建干净克隆完整复验。

## 允许范围

- 现行设计基线、文档索引、需求追踪、测试登记、旧机器附件资格和本 WorkItem 状态文件。
- 禁止新增 `src/` runtime、服务、API 平台、依赖、远端或生产动作。

## 恢复入口

- `.factory/workitems/SOFTWARE-LIFECYCLE-GOVERNANCE-001/brief.md`
- `.factory/workitems/SOFTWARE-LIFECYCLE-GOVERNANCE-001/plan.md`
- `.factory/workitems/SOFTWARE-LIFECYCLE-GOVERNANCE-001/ledger.jsonl`
- `.factory/workitems/SOFTWARE-LIFECYCLE-GOVERNANCE-001/task-briefs/`

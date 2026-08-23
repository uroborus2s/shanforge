# 质量、发布与运维入口

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `DOC-NAV-DELIVERY-001` |
| 正式版本 | `v1.2.0` |
| 当前修订 | 无 |
| 来源候选 | `TEST-GOVERNANCE-CLOSURE-001` |
| 发布事务 | `DELIVERY-RELEASE-TX-R001-G001` |
| 负责人 | `HUMAN_RELEASE_OPERATIONS_LEAD` |
| 修改 / 审核 / 批准 | `AI_EXECUTOR` / 独立 Reviewer / `uroborus` |
| 状态 | 已批准并生效 |
| 上游 | `TASK-IMPLEMENT-001-R002`、正式设计、发布后验证 |
| 下游 | `test-plan`、`release-notes`、`deployment-guide`、`operations-runbook` |

## 当前交付基线

- 正式实现：`TASK-IMPLEMENT-001-R002`，事务 `IMPLEMENTATION-RELEASE-TX-R002-G001`。
- 需求覆盖：产品代码与测试追踪 `15/123`，剩余 `108/123`。
- 质量结果：发布后全仓 `832 passed`，failed/skipped/not_run 为 `0/0/0`；Ruff、format、mypy、38 个顶层 Skill、候选与发布攻击门均通过。
- 权限边界：本地正式实现已激活；Git、远端发布、制品上传和部署未执行。
- 完成边界：本页说明当前交付增量，不表示全部 123 项产品需求已经实现。

## 正式文档

1. [测试策略与质量门](./test-plan.md)：测试层级、发布质量门和 R002 验证入口。
2. [正式测试案例目录](./test-cases.md)：稳定案例 ID、前置条件、步骤、预期结果、自动化入口与清理。
3. [发布说明](./release-notes.md)：R002 已发布变化、兼容影响和残留范围。
4. [部署手册](./deployment-guide.md)：当前本地交付方式、环境前置、验证和回滚入口。
5. [运维手册](./operations-runbook.md)：巡检、故障分流、恢复和升级边界。

## 阅读顺序

发布评估先读发布说明，再用测试计划核对质量门；需要运行或接手时继续读部署手册和运维手册。一次性命令输出、候选状态、Review Decision 和完整交付包保存在 `.factory/workitems/FLOW-CONTRACT-001/`，不复制进正式文档正文。

## 维护规则

- 只记录已发布变化和稳定操作合同；候选、日志、事故原文和凭证不得进入本目录。
- 正式版本、实现版本、Git 状态、远端状态和部署状态分别记录，不能互相推导。
- 新增交付增量时同步发布说明、测试入口、需求追踪和必要 memory 摘要。

[返回文档总入口](../index.md)。

## 正式版本历史（仅已发布）

| 版本 | 日期 | 变更 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v1.0.0` | 2026-07-18 | 基于 R019 建立统一质量、发布与运维入口 | `uroborus` | `uroborus` | `uroborus` |
| `v1.1.0` | 2026-07-20 | 绑定 R002 本地正式实现交付基线和 15/123 完成口径 | `AI_EXECUTOR` | 独立 Reviewer | `uroborus` |
| `v1.2.0` | 2026-08-23 | 登记正式测试案例目录和文档有效性校验入口 | `AI_EXECUTOR` | 独立 Reviewer | `uroborus` |

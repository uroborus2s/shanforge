# Agent 会话卡

- 生成时间：2026-08-23 21:08 +0800
- 项目：`shanforge`
- 当前工作项：`TEST-GOVERNANCE-001`
- 当前任务：`TEST-GOVERNANCE-001-T03`
- 当前状态：`completed`
- 当前焦点：TEST-GOVERNANCE-001 已完成
- 下一动作：`none`

## 当前事实

- Shanforge 是 skill-first 工程协作资产，旧 `src/` 平台和对应测试不属于当前产品。
- 正式测试计划已改为当前 Skill-first 入口，失效旧平台案例目录已删除。
- 治理测试现在解析正式计划和现存案例目录中的 `tests/test_*.py`，不存在的入口会失败。
- 案例、报告和状态合同已统一；未恢复平台运行时或新增依赖。
- 实现提交 `c4534ba` 的干净克隆为 `236 passed / 4 subtests passed`，并行工作项未纳入。

## 当前 Gate

- `closed`
- 实现提交 `c4534ba` 的干净克隆全绿；工作项已关闭。

## 后续授权范围

- Sol 负责设计、分级和控制；T01/T02/T03 由 Terra 按任务简报执行。
- 允许同范围测试、文档、Skill、WorkItem、memory、独立只读评审和本地提交。
- 不执行 push、PR、merge 或部署。

## 恢复入口

- `.factory/workitems/TEST-GOVERNANCE-001/brief.md`
- `.factory/workitems/TEST-GOVERNANCE-001/plan.md`
- `.factory/workitems/TEST-GOVERNANCE-001/ledger.jsonl`

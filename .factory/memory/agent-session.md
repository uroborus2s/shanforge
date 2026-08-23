# Agent 会话卡

- 生成时间：2026-08-23 21:08 +0800
- 项目：`shanforge`
- 当前工作项：`TEST-GOVERNANCE-001`
- 当前任务：`TEST-GOVERNANCE-001-T03`
- 当前状态：`review_approved`
- 当前焦点：清理旧平台测试引用并统一案例、状态和报告合同
- 下一动作：`create_exact_local_commit_then_clean_clone_verify`

## 当前事实

- Shanforge 是 skill-first 工程协作资产，旧 `src/` 平台和对应测试不属于当前产品。
- 正式测试计划和一个案例目录仍引用已删除的旧平台测试；现有治理测试没有检查入口存在性。
- 工作项建立前基线为 `233 passed / 4 subtests passed`，说明陈旧引用当前不会触发失败。
- 本工作项只修测试治理合同、模板和守卫，不恢复平台运行时或新增依赖。

## 当前 Gate

- `T03_exact_commit_and_clean_clone`
- 同一 reviewer 复审 `approved / 98 / C0-I0-M0`；隔离候选完整全绿，无人工 Gate。

## 后续授权范围

- Sol 负责设计、分级和控制；T01/T02/T03 由 Terra 按任务简报执行。
- 允许同范围测试、文档、Skill、WorkItem、memory、独立只读评审和本地提交。
- 不执行 push、PR、merge 或部署。

## 恢复入口

- `.factory/workitems/TEST-GOVERNANCE-001/brief.md`
- `.factory/workitems/TEST-GOVERNANCE-001/plan.md`
- `.factory/workitems/TEST-GOVERNANCE-001/ledger.jsonl`

# SOFTWARE-ENGINEERING-SKILL-REMEDIATION-001：软件工程 Skill 审计整改

## 状态

`plan_ready`

## 用户问题

现有审计报告使用“批次 A：合同一致性”等内部分类，但没有说明具体哪里坏了、为什么影响开发、修改哪些文件、如何验证和修复顺序，导致用户无法判断下一步。

## 整改目标

把审计发现转成可以直接执行和验收的修复任务：每项必须包含用户可观察问题、根因、精确文件/章节、具体改法、失败测试、通过标准和依赖顺序。

## 已批准输入

- `.factory/workitems/SOFTWARE-ENGINEERING-SKILL-AUDIT-001/reports/consolidated-audit.md`
- `.factory/workitems/SOFTWARE-ENGINEERING-SKILL-AUDIT-001/reports/final-scorecard.md`
- 用户本轮反馈：必须看懂问题、下一步修复动作和完整计划。

## 边界

- 本轮只生成整改计划，不修改 Skill、源码或测试。
- 后续执行必须按任务卡逐项 Red/Green，不允许把计划写成已经修复。
- 代码任务继续禁止局部函数定义和无独立职责的单调用点公共 helper。

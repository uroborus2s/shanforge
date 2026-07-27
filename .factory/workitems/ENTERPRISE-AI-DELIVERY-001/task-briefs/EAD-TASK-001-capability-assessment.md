# EAD-TASK-001 能力评估与差距分析

## Task

基于中建三局一公司产业工人平台案例，评估 Shanforge 当前能力是否能解决企业 AI 软件工程化与交付闭环问题，并形成后续产品化任务输入。

## Inputs

- 客户需求、排期、缺陷和运维记录分析结果。
- `ENTERPRISE-AI-DELIVERY-001/brief.md`。
- `ENTERPRISE-AI-DELIVERY-001/reports/initial-capability-assessment.md`。
- Shanforge 当前 skills、work item、ledger、evidence、review gate 机制。

## Required Outputs

- 当前能力矩阵：可直接复用、需轻量包装、需新增能力、暂不支持。
- 企业 AI 交付闭环工作台最小产品形态。
- 5 类以上 Agent 工作流输入输出契约。
- 多岗位协同 RACI 和 gate 设计。
- 第一家客户 30 天试点实施方案。
- 后续 Shanforge 产品化 backlog。

## Acceptance Criteria

- 明确回答“现有 Shanforge 能不能解决这个问题”。
- 不能只写项目管理咨询，必须体现 AI 在提速、增效、规范化上的作用。
- 每个 Agent 工作流必须有人审门禁，AI 不直接替人决策。
- 方案必须覆盖业务、运营、开发、测试、运维、负责人之间的协同。
- 方案必须形成输入、结构化、人审、执行、验证、复盘、沉淀闭环。

## Verification

- 检查 `reports/initial-capability-assessment.md` 是否覆盖问题、方案、协同、闭环和指标。
- 检查 ledger JSONL 是否可解析。
- 独立 review 必须确认本任务没有把客户问题简化成普通项目管理咨询。

## 状态

`completed`

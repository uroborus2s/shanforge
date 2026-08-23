# ENTERPRISE-AI-DELIVERY-001 Work Item Plan

## Scope

- 基于中建三局一公司产业工人平台案例，完成 Shanforge 当前能力评估。
- 设计企业 AI 交付闭环工作台的最小产品形态。
- 定义需求、估算、验收、缺陷、周报 5 类 Agent 工作流。
- 定义业务、运营、开发、测试、运维、负责人的多人多岗位协同模型。
- 定义第一家客户 30 天试点路径、交付物和验收指标。

## Out Of Scope

- 不直接开发完整 SaaS 工作台。
- 不直接接入客户生产系统、代码仓库或内部工单系统。
- 不替客户团队做最终业务、技术或上线决策。
- 不绕过 Shanforge 既有 review、verification 和 human confirmation gate。

## Work Breakdown

| id | parent_id | title | status |
|---|---|---|---|
| EAD-TASK-001 | | 能力评估与差距分析 | completed |
| EAD-TASK-001-01 | EAD-TASK-001 | 当前能力可解决项、部分可解决项、缺口项 | completed |
| EAD-TASK-001-02 | EAD-TASK-001 | 试点可行性结论 | completed |
| EAD-TASK-001-03 | EAD-TASK-001 | 后续产品化 backlog | completed |
| EAD-TASK-002 | | 企业交付数据模型与 Agent 输出契约 | approved |
| EAD-TASK-002-01 | EAD-TASK-002 | 需求准入字段模型 | completed |
| EAD-TASK-002-02 | EAD-TASK-002 | 开发就绪包字段模型 | completed |
| EAD-TASK-002-03 | EAD-TASK-002 | 估算拆解字段模型 | completed |
| EAD-TASK-002-04 | EAD-TASK-002 | 缺陷闭环字段模型 | completed |
| EAD-TASK-002-05 | EAD-TASK-002 | 周报看板字段模型 | completed |
| EAD-TASK-002-06 | EAD-TASK-002 | Agent 输入、输出、人审门禁和失败条件 | completed |
| EAD-TASK-003 | | 多岗位协同与流程门禁设计 | approved_pending_customer_confirmation |
| EAD-TASK-003-01 | EAD-TASK-003 | 业务、运营、开发、测试、运维、负责人 RACI | completed |
| EAD-TASK-003-02 | EAD-TASK-003 | 需求进入开发门禁 | completed |
| EAD-TASK-003-03 | EAD-TASK-003 | 估算确认门禁 | completed |
| EAD-TASK-003-04 | EAD-TASK-003 | 提测门禁 | completed |
| EAD-TASK-003-05 | EAD-TASK-003 | 上线验证门禁 | completed |
| EAD-TASK-003-06 | EAD-TASK-003 | 缺陷关闭门禁 | completed |
| EAD-TASK-003-07 | EAD-TASK-003 | 周复盘门禁 | completed |
| EAD-TASK-003-08 | EAD-TASK-003 | 客户岗位授权与职责分离确认 | current |
| EAD-TASK-004 | | 第一家客户试点实施方案 | planned |
| EAD-TASK-004-01 | EAD-TASK-004 | 30 天试点计划 | planned |
| EAD-TASK-004-02 | EAD-TASK-004 | 试点范围和样本选择 | planned |
| EAD-TASK-004-03 | EAD-TASK-004 | 每周交付物 | planned |
| EAD-TASK-004-04 | EAD-TASK-004 | 现场访谈和资料导入清单 | planned |
| EAD-TASK-004-05 | EAD-TASK-004 | 面向客户负责人的汇报模板 | planned |
| EAD-TASK-004-06 | EAD-TASK-004 | 成功指标和退出条件 | planned |
| EAD-TASK-005 | | Shanforge 产品化实现 backlog | planned |
| EAD-TASK-005-01 | EAD-TASK-005 | 必须新增的 skills、模板、脚本和 evaluation fixtures | planned |
| EAD-TASK-005-02 | EAD-TASK-005 | 轻量 Web 工作台原型决策建议 | planned |
| EAD-TASK-005-03 | EAD-TASK-005 | 与 Qoder/agent 工具结合的最小集成方式 | planned |
| EAD-TASK-005-04 | EAD-TASK-005 | 后续开发任务拆分 | planned |

## Verification

- JSONL parse：`.factory/workitems/ENTERPRISE-AI-DELIVERY-001/ledger.jsonl` 必须可逐行解析。
- 文档检查：brief、plan、initial assessment 必须覆盖目标、非目标、问题诊断、解决方案、岗位协同、闭环、验收指标。
- 评估检查：必须明确当前 Shanforge “能解决什么、不能解决什么、需要补什么”。
- Review gate：任务只能进入 `ready_for_review`，不得自批完成。

## Review Gate

EAD-TASK-001 已通过独立 review，并于 2026-07-27 获用户批准最小路径。允许启动 EAD-TASK-002。
T03–T05 仍须按数据模型、岗位决策权和试点基线依赖推进；本轮不授权完整 Web 工作台、
客户生产系统、代码仓库或内部工单系统接入。

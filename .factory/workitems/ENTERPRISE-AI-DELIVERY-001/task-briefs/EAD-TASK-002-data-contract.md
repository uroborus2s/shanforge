# EAD-TASK-002 企业交付数据模型与 Agent 输出契约

## 任务身份

- Work item：`ENTERPRISE-AI-DELIVERY-001`
- Task：`EAD-TASK-002`
- 类型：`requirements`
- 状态：`approved`
- 前置：EAD-TASK-001 已通过独立评审，用户已批准最小路径

## 目标

定义首期咨询实施包与半自动 Agent 流程共用的最小数据模型，覆盖需求准入、开发就绪包、
估算拆解、验收、缺陷闭环和周报看板，并明确每类 Agent 的输入、输出、人审门禁和失败条件。

## 授权执行包

### 允许文件

- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/task-briefs/EAD-TASK-002-data-contract.md`
- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/reports/EAD-TASK-002-enterprise-delivery-data-contract.md`
- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/reports/EAD-TASK-002-implementer-report.md`
- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/evidence/EAD-TASK-002-verification-20260727.md`
- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/evidence/EAD-TASK-002-contract-check.py`
- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/evidence/EAD-TASK-002-review-fix-verification-20260727.md`
- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/evidence/EAD-TASK-002-final-verification-20260727.md`
- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/reviews/EAD-TASK-002-review-input.md`
- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/reviews/EAD-TASK-002-independent-review-iteration-1.md`
- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/reviews/EAD-TASK-002-review-feedback-triage.md`
- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/reviews/EAD-TASK-002-review-response.md`
- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/reports/EAD-TASK-002-review-fix-report.md`
- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/brief.md`
- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/plan.md`
- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/ledger.jsonl`
- `.factory/memory/agent-session.md`
- `.factory/memory/current-state.md`
- `.factory/memory/tasks.summary.md`
- `.factory/memory/tests.summary.md`
- `.factory/memory/review-ledger.jsonl`

### 允许动作

- 编写可审阅的数据字段和 Agent 输出契约。
- 用脱敏示例说明结构。
- 执行 Markdown、字段覆盖和 JSONL 静态验证。
- 形成 evidence、implementer report 和 review input。
- 同步当前 EAD memory 投影，并只暂存当前任务的精确 hunk。

### 禁止动作

- 开发完整 Web 工作台。
- 接入客户生产系统、代码仓库或内部工单系统。
- 使用未脱敏的真实客户数据。
- 修改产品代码、数据库、API 或 UI baseline。
- 执行远端 push、PR、merge 或发布。

### 运行时路由

- `work_item_id`: `ENTERPRISE-AI-DELIVERY-001`
- `task_card_id`: `EAD-TASK-002`
- `current_gate`: `human_minimal_path_approved`
- `write_policy`: `project_fact_write`

## 必须交付

- 6 类记录模型及其必填字段、状态和证据引用。
- 至少 5 类 Agent 的输入、输出、人审门禁和失败条件。
- 统一的来源、脱敏、版本、责任人和审计规则。
- 可逐项检查的验收标准和 review 输入。

## 验收标准

- AC-1：6 类模型都定义稳定 ID、来源、负责人身份、状态、证据和版本链。
- AC-2：每类模型区分必填、条件必填和可选字段。
- AC-3：每类 Agent 都有输入、输出、人审门禁、失败条件和禁止自动决策边界。
- AC-4：人工脱敏导入导出边界明确，不出现生产系统或代码仓库直连设计。
- AC-5：需求、估算、验收、缺陷和周报之间可通过稳定 ID 追踪。

## 验证命令

```bash
python3 .factory/workitems/ENTERPRISE-AI-DELIVERY-001/evidence/EAD-TASK-002-contract-check.py
python3 -c 'import json,pathlib; [json.loads(x) for x in pathlib.Path(".factory/workitems/ENTERPRISE-AI-DELIVERY-001/ledger.jsonl").read_text().splitlines() if x.strip()]'
git diff --check -- .factory/workitems/ENTERPRISE-AI-DELIVERY-001
```

## Review Gate

实现者最多推进到 `ready_for_review`。独立评审通过前，不得写成 `approved` 或 `completed`。

## Memory 精确提交策略

- `agent-session.md`、`current-state.md` 只承载当前 EAD 投影，可整体暂存。
- `tasks.summary.md`、`tests.summary.md`、`review-ledger.jsonl` 是共享文件，只暂存
  EAD-TASK-002 当前状态、验证和 review 事件 hunk。
- 其他工作项的既有 worktree diff 保持未暂存；提交前用 cached name/diff 检查证明隔离。

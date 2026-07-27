# EAD-TASK-003 多岗位协同与流程门禁设计

## 任务身份

- Work item：`ENTERPRISE-AI-DELIVERY-001`
- Task：`EAD-TASK-003`
- 类型：`process_design`
- 状态：`ready_for_review`
- 前置：EAD-TASK-002 已通过独立复审并由本地提交 `f5ed0e4` 收口

## 目标

基于 T02 数据和状态契约，定义业务、运营、项目负责人、开发、测试和运维的 RACI，
以及需求准入、估算、提测、上线、缺陷关闭和周复盘六类人审门禁。

## 授权执行包

### 允许文件

- `.factory/workitems/ENTERPRISE-AI-DELIVERY-001/**`
- `.factory/memory/agent-session.md`
- `.factory/memory/current-state.md`
- `.factory/memory/tasks.summary.md`
- `.factory/memory/tests.summary.md`
- `.factory/memory/review-ledger.jsonl`

### 禁止动作

- 把通用岗位模板绑定到未经客户确认的真实人员。
- 让 AI 拥有业务、技术、上线、验收或关闭决定权。
- 开发 Web、数据库、API 或外部系统集成。
- 使用未脱敏客户数据。
- 执行远端 push、PR、merge 或发布。

### 运行时路由

- `work_item_id`: `ENTERPRISE-AI-DELIVERY-001`
- `task_card_id`: `EAD-TASK-003`
- `current_gate`: `EAD_TASK_002_COMMITTED`
- `write_policy`: `project_fact_write`

## 必须交付

- 六类人类岗位 RACI。
- 六类流程门禁的进入条件、责任人、决策、证据、失败条件和退出状态。
- AI Agent 与 Shanforge 的辅助边界。
- 角色缺失、冲突、越权和代理决策的 fail-closed 规则。
- 客户只需确认的最小岗位决策包。

## 验收标准

- AC-1：每个活动只有一个 `A`，至少一个 `R`，并明确 `C/I`。
- AC-2：每个门禁引用 T02 稳定 record、revision、digest、actor 和 evidence。
- AC-3：六类门禁均有 `from/event/guard/to` 与失败返回。
- AC-4：AI 只能生成草稿、缺口和检查结果，不能成为 `A` 或人工 reviewer。
- AC-5：未经客户确认的 actor 映射保持 `pending_customer_confirmation`，不冒充生效 RACI。

## 验证命令

```bash
python3 .factory/workitems/ENTERPRISE-AI-DELIVERY-001/evidence/EAD-TASK-003-raci-gate-check.py
git diff --check -- .factory/workitems/ENTERPRISE-AI-DELIVERY-001
```

## Review Gate

实现者最多推进到 `ready_for_review`。独立评审通过后，再提交最小客户岗位确认包。

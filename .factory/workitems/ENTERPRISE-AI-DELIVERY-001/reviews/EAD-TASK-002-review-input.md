# EAD-TASK-002 独立评审输入

## 评审对象

- Task brief：`task-briefs/EAD-TASK-002-data-contract.md`
- 主契约：`reports/EAD-TASK-002-enterprise-delivery-data-contract.md`
- 实现报告：`reports/EAD-TASK-002-implementer-report.md`
- 验证证据：`evidence/EAD-TASK-002-verification-20260727.md`
- 可执行检查：`evidence/EAD-TASK-002-contract-check.py`
- 首轮评审：`reviews/EAD-TASK-002-independent-review-iteration-1.md`
- 反馈处置：`reviews/EAD-TASK-002-review-feedback-triage.md`

## 评审目标

确认契约足以支撑“2 个真实需求 + 一批 P0/P1 缺陷”的人工脱敏试点，同时没有提前进入
Web、数据库、API 或外部系统集成设计。

## 必查项

1. 六类模型是否都有稳定 ID、来源、actor 身份、状态、版本链和证据。
2. 字段必填级别和状态门禁是否可执行。
3. 六类 Agent 是否都限制为草稿、缺口和检查，不替人决策。
4. 需求、估算、验收、缺陷和周报是否能端到端追踪。
5. 未脱敏输入、来源冲突、证据不足和非法状态是否有明确失败返回。
6. 是否存在未授权的 Web、数据库、API、生产系统或代码仓库设计。
7. 45 条封闭状态转移和 4 个非法状态负例是否足以支撑 `INVALID_STATE`。

## Reviewer 输出要求

- 结论：`approved` 或 `changes_requested`
- 评分：0–100
- Findings：Critical / Important / Minor
- 独立性说明
- 下一 Gate 建议

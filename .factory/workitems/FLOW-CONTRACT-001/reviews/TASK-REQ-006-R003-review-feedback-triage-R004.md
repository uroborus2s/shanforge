# TASK-REQ-006 R003 Feedback Triage for R004

## `R003-I-001`

- 来源：同一独立 Reviewer 的 R003 复审。
- Severity：Important。
- 技术要求：把当前有效授权设为所有 cache-hit、read、serve 路径的前置条件；撤销后立即 fail-closed，物理删除可异步。
- 是否清楚：yes。
- 技术核实：正确。R003 只禁止撤销摘要创建新 cache，并要求下一维护批次清理；没有禁止清理前返回旧文件。
- 与用户决策冲突：no。
- 处理：Fixed in R004。

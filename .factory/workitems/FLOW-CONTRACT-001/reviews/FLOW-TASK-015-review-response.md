# FLOW-TASK-015 Review Response

## 当前状态

`ready_for_same_reviewer_implementation_rereview`

## Finding 响应

| Finding | 处理 | 证据 |
|---|---|---|
| `FT015-C1` | Fixed：正式 v1.1.0 未改；建立绑定精确基线 hash 的 v1.2.0 候选 delta和发布顺序 | candidate、verification |
| `FT015-C2` | Fixed：16 行为、13 工作流、完整独立字段和唯一默认映射 | candidate 结构表、7 个结构测试 |
| `FT015-C3` | Fixed：写入身份 fail-closed、原子 tracking identity 例外、ledger/evidence 必需、memory 不可单证 | 写入授权矩阵与负例 |
| `FT015-I1` | Fixed：逐工作流节点、主路径、停止态和人工 Gate 规则 | 工作流节点与转换表 |
| `FT015-I2` | Fixed：改为 Markdown 表结构、集合、非空、hash 和负例断言 | `tests/test_full_project_session_workflow_routing.py` |
| `FT015-I3` | Fixed：当前路径、hash、前置完成状态和新鲜 56-pass 证据已重建 | verification、report、ledger |
| `FT015-I4` | Fixed：缺 Review 专用快照；active task 动态 ledger 对账 | v2 transcript、fixture、22-pass 回归 |

## 验证

- 结构：`7 passed`
- 状态独立回归：`22 passed`
- 规定组合：`56 passed`
- Ruff / diff check：通过

## 请求

请同一 Reviewer 只读确认七项 finding 是否全部关闭，以及候选是否可进入正式版本治理 Gate。实现者未自批。

## Iteration 2 响应

- `FT015-C3`：补充可达的 `tracking-identity-workflow`、身份创建 route/node、proposed IDs、精确写集、
  readback 和 reroute；`SB-RESUME` 补充条件必需身份输入。
- `FT015-I2`：补充三张表的重复 ID 拒绝、期望计数和跨表写策略可达性断言。
- Iteration 2 Red：`4 failed / 3 passed`。
- Iteration 2 Green：`7 passed`；规定组合仍为 `56 passed`，Ruff 和 diff check 通过。

当前候选 SHA-256：
`3d5f4cbabda86312da0603db5662175453d12dd5966c788301b0c79c2cb4992f`。

## 正式实现 Review 响应

| Finding | 处理 | 证据 |
|---|---|---|
| `FT015-IMPL-I1` | Fixed：旧自动人工 Gate 规则收窄为仅真实人类决定 Gate；普通 Review 通过后按 `next_required_action` 重新路由 | 正式 v1.2.0 第“评审和人工确认”及 `GateDecision / ReviewDecision / HumanDecision` 段 |
| `FT015-IMPL-I2` | Fixed：测试比较正式/候选四张核心表，拒绝旧冲突文案，只在 runtime 合同区块校验字段、policy 和精确行为映射 | `tests/test_full_project_session_workflow_routing.py` |
| `FT015-IMPL-I3` | Fixed：队列与最新 ledger 状态动态对账；测试摘要同步 57-pass 与 Review 整改状态 | `implementation-queue.md`、`tests.summary.md` |

整改后正式文档 SHA-256：
`739a9920c9956b02af0d6e8498b706bd0e4fb778a71d21e0f3e7ae5c5f72abd7`。
冻结候选 SHA-256 未变。

# EAD-TASK-003 Review Response

## I1 — Fixed

客户最小确认包由 5 项增为 6 项，新增五组必须逐项确认的 actor 分离约束：

- GATE-TEST：开发与测试分离。
- GATE-REL：业务分别与测试、发布分离。
- GATE-DEF：发布分别与开发、测试分离。

任一重合都返回 `SEGREGATION_OF_DUTIES_VIOLATION`，模板不得激活。

## M1 — Fixed

Validator 现在直接读取 T02 契约的 45 条状态转移，验证 T03 的 6 条 Gate
转移是其子集；同时验证所有 Gate 所需 A/R、客户未确认、缺失 R、AI actor 和
五组职责分离负例。

## 范围

整改仅修改 T03 契约、校验与证据；未绑定真实人员，未接入客户系统。

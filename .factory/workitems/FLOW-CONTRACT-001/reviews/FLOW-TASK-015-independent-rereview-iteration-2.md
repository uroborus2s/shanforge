# FLOW-TASK-015 方案复审（Iteration 2）

## 结论

- Decision：`changes_requested`
- Score：`82 / 100`
- Critical：`1`
- Important：`1`
- Minor：`0`
- Reviewer：`/root/project_knowledge_review`
- Candidate 可进入正式版本治理 Gate：`false`
- Human confirmation required：`false`

## 已关闭

- `FT015-C1`：受控候选、正式基线和 hash 分离正确。
- `FT015-C2`：16 个行为和完整工作流字段已补齐。
- `FT015-I1`：逐工作流节点、转换和人工 Gate 规则已补齐。
- `FT015-I3`：当前候选包、路径、hash 和验证已重建。
- `FT015-I4`：状态依赖测试已改为不可变快照和动态 active-task 对账。

## 未关闭

- `FT015-C3`：普通写入已 fail-closed，但身份创建例外不可到达。普通路由包和初始工作流都要求身份已存在，没有 workflow/node/route 能先原子创建身份；`SB-RESUME` 的写策略也缺条件必需身份输入。
- `FT015-I2`：表结构测试没有拒绝重复 ID 行，也没有验证 `create_tracking_identity` 对 workflow/node 可达。

## 要求

增加专用 tracking identity intake 路由与节点，携带 proposed IDs、精确写集和 `write_policy=create_tracking_identity`；
只允许原子创建三件套和 readback，成功后重新路由。对三个主表断言行数等于唯一 ID 数量，并跨表验证写策略可达。

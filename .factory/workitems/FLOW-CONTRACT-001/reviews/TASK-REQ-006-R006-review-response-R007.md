# TASK-REQ-006 R006 复审整改响应（R007）

## Fixed

- `R006-I-001`：R007 field map 精确绑定 R014 record identity 和父键；目标键使用类型命名空间，缺失/重复/碰撞均阻止代次发布；所有字段值直接来自 canonical v2 snapshot path。
- `R006-I-002`：机器合同保存从 Markdown 规范提取的完整 16 REQ、64 AC、11 NFR 对象、逐节 Hash 和 root `ee2fa8ab…829e`；验证器逐字段重提取比较。
- `R006-I-003`：状态机改成 10 个非终态的事件全集与 50 条唯一 transition；发布成功需要 current input + valid lease + matching fencing，未分类结果进入永久失败；所有状态可达终态。
- `R006-N-001`：统一采用 R014 `ProjectProgressSnapshot/v2`。

## 验证

- Markdown 投影与 JSON 对象逐字段相等，逐节/root Hash 一致。
- R014 137 字段和 R007 map 完全集合相等；snapshot path/value Owner 精确一致。
- R014 record identity 与 11 个业务 row model 精确匹配，其余 singleton/navigation 具有显式身份规则。
- `(state,event)` 50 对唯一并与每个 state 声明事件精确相等；所有非终态可达 `done|superseded|needs_attention`。

## Gate

R007 仅进入同一 Reviewer 复审，仍未获得人工批准或设计/实现资格。

# TASK-REQ-006 R006 评审反馈分诊（R007）

## `R006-I-001`

- 技术核实：正确。R006 的目标主键缺少源身份变换合同。
- 决定：Fixed in R007。13 个 row model 均增加 source collection/record ID path、命名空间化 target key 公式、父键 path、Unicode/碰撞/缺失策略。137 个 value Owner 改为 canonical `ProjectProgressSnapshot/v2` 精确 snapshot path 直接读取，PM 不重新派生。

## `R006-I-002`

- 技术核实：正确。冻结两个存在语义差异的文件不能发现冻结时已有漂移。
- 决定：Fixed in R007。`RequirementProjectionCanonicalization/v1` 从 Markdown 提取 REQ 标题/优先级/规范正文/AC和 NFR 指标/验证，NFC + LF + JCS 后逐节及 root SHA-256 与 JSON 对象逐字段比较。

## `R006-I-003`

- 技术核实：正确。存在出边不是事件完备性。
- 决定：Fixed in R007。10 个非终态各声明互斥穷尽事件，event classifier 有优先级和未分类失败规则，共 50 条 `(state,event)` 唯一转移；发布成功统一要求 current input/lease/fencing；模型验证检查精确覆盖和终态可达。

## `R006-N-001`

- 技术核实：正确。同名 v1 会与 pinned v2 冲突。
- 决定：Fixed in R007。全部改为 R014 canonical `ProjectProgressSnapshot/v2`，PM 映射为直接读取适配，不新增同名 DTO。

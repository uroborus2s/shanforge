# TASK-REQ-006 R005 评审反馈分诊（R006 整改）

## 总结

七项 Finding 均清楚、可复现且在原需求范围内可修。`R005-C-001` 与用户要求的快速本地静态站点存在表面冲突，整改采用分级输出：local-owner 离线站点依赖 OS 文件权限并明确不可撤回复制件；shared/restricted scope 的敏感内容必须走重新鉴权的 `--serve`，离线只允许公开/脱敏字段。

## `R005-C-001`

- severity: Critical
- 技术要求：消除离线复制件与撤权零读取的不可实现合同。
- 核实：正确。已知路径的明文文件不能被 CLI 追溯收回。
- 用户决策冲突：否；用户要求本地快速快照，没有要求离线文件承载可动态撤权的共享秘密。
- 决定：Fixed in R006，定义 `local_owner` 与 `shared_restricted` 两种发布 profile、ACL、清除和残留风险边界。

## `R005-I-001`

- severity: Important
- 技术要求：准确标注 R014 未批准状态并绑定精确内容。
- 核实：正确。R014 状态为 `candidate_unapproved`。
- 决定：Fixed in R006，绑定 contract ID、revision、whole-file SHA-256 与 field catalog SHA-256；R006 不替代 R014 的独立批准。

## `R005-I-002`

- severity: Important
- 技术要求：机器可验证地覆盖 137 字段及 PM 表 Owner/基数/历史。
- 核实：正确。仅表名不足以进入 schema 设计。
- 决定：Fixed in R006，新增完整字段映射合同和行模型；`ProjectProgressSnapshot` 明确为非持久化 DTO，Manifest 归 `pk_render_view`。

## `R005-I-003`

- severity: Important
- 技术要求：固定页面显示时间与 Hash 规范化规则。
- 核实：正确。
- 决定：Fixed in R006，页面只显示来源事实高水位的 `as_of`；墙钟 `built_at` 只存在于 receipt/Manifest 非内容摘要区，不进入页面 Hash/fingerprint。

## `R005-I-004`

- severity: Important
- 技术要求：代码实体身份与可变 locator 分离。
- 核实：正确。
- 决定：Fixed in R006，增加 `symbol_id`，qualified locator 仅为当前 locator；重构需要 alias/迁移声明或有置信度的待确认候选，并覆盖拆分/合并歧义。

## `R005-I-005`

- severity: Important
- 技术要求：机器合同覆盖 REQ、AC、NFR 实质内容。
- 核实：正确。
- 决定：Fixed in R006，合同把 16 个 REQ、64 个稳定 AC ID、11 个 NFR 指标/验证和逐项 Markdown section ID 编码为对象，最终 Manifest 同时绑定全部候选文件。

## `R005-I-006`

- severity: Important
- 技术要求：封闭异步状态机并定义无提交成功路径、失租和重试。
- 核实：正确。
- 决定：Fixed in R006，增加 transition/guard/terminal/retry/fencing 合同；维护提交是可选分支，未授权时可经 `commit_not_authorized -> integrated -> done` 收敛。

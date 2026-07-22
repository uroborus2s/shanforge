# TASK-REQ-006 R006 独立复审

- reviewer_type: `independent_subagent`
- reviewer_id: `/root/req006_r005_review`
- reviewer_independence_evidence: R005 原独立 Reviewer，未参与 R006 整改；只读指定输入与规则并执行 Hash/jq/结构命令，未修改文件。
- review_score: `78 / 100`
- review_status: `changes_requested`
- next_gate_status: `changes_requested`
- human_confirmation_required: `false`

## R005 Finding 关闭

| Finding | 结论 |
|---|---|
| `R005-C-001` | closed：local-owner 与 shared-restricted 已形成可测试安全边界。 |
| `R005-I-001` | closed：R014 状态与双 Hash pin 正确。 |
| `R005-I-002` | open：137 字段覆盖成立，但 PK/FK 值来源、变换与具体值 Owner 未闭合。 |
| `R005-I-003` | closed：`as_of` 与 `built_at` 已分离。 |
| `R005-I-004` | closed：stable symbol ID 与 locator 已分离。 |
| `R005-I-005` | open：64 AC 已对象化，但 Markdown/JSON 仍无逐节语义一致性校验。 |
| `R005-I-006` | open：22 条转移有出边，但 guard 结果未互斥穷尽。 |

## Important

### `R006-I-001` PM 行键未绑定 R014 record identity

R014 的成员、干系人、WBS、进度、状态、变更和总结分别使用 `member_id`、`stakeholder_id`、`task_id`、`record_id`、`report_id`、`change_id`、`project_id`。R006 field map 只给目标键名，没有 source record ID path、命名空间/碰撞规则和父键来源；`value_owner` 也是笼统字符串。

### `R006-I-002` 64 AC 缺 Markdown/JSON 语义一致性

结构校验只证明数量、ID 和顺序，不能证明标题、优先级、正文、AC statement、NFR 指标与验证方式逐字段一致。需要规范化投影、逐节 Hash 和可执行比较。

### `R006-I-003` 状态机 guard 不穷尽

失租、输入过期、唯一成功 guard 为 false 等情况在部分状态没有替代转移。每个非终态必须有互斥穷尽事件集，发布成功都要求 current input + valid lease + matching fencing，且模型测试证明有限收敛。

### `R006-N-001` Snapshot schema 与 R014 冲突

R006 使用 `ProjectProgressSnapshot/v1`，而 pinned R014 已定义 canonical `ProjectProgressSnapshot/v2`。必须直接采用 v2 或定义不同类型和版本化适配。

## 机器核验

- R006：16 REQ、64 AC、11 NFR；29 + 10 = 39 表。
- R014 与 field map pin 匹配；137 source fields 与 137 mappings 无 missing/extra；10 张 PM 表均使用。
- 状态机 13 states、3 terminals、22 transitions，存在出边校验通过但不证明 guard 穷尽。
- R006 Hash：Markdown `c1c38864…8f92`；contract `92f4a73e…6fa3`；field map `7169c619…c8c`。

## 评分

- 需求符合度：24 / 30
- 架构一致性：15 / 20
- 测试充分性：15 / 20
- 机器合同质量：16 / 20
- 文档与记忆同步：8 / 10
- 总分：78 / 100

## Gate

4 个 Important 未关闭，必须 `changes_requested`；不得进入精确 Hash 人工确认。

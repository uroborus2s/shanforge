# TASK-REQ-006 R005 独立需求评审

- reviewer_type: `independent_subagent`
- reviewer_id: `/root/req006_r005_review`
- reviewer_independence_evidence: Reviewer 未参与 R005 编制或实现；未读取作者会话历史、Memory 或 Ledger 正文，只读取指定文件化输入包、评审 Skill/评分规则并执行只读命令；未修改文件。
- author_self_check_score: `n/a`
- review_score: `58 / 100`
- review_status: `changes_requested`
- next_gate_status: `changes_requested`
- human_confirmation_required: `false`
- gate_reason: `none`，问题可在原需求候选范围内整改。

## N/A 审查

- Implementer report：接受 N/A；本轮是实现前需求 Gate。
- 产品代码/测试 diff：接受 N/A；本轮禁止产品实现，工作树中其他实现不在本次批准范围。
- `.factory/memory/` 正式同步：当前 Gate 接受暂不执行；进入正式设计前仍须按项目规则同步必要事实。

## Findings

### Critical

#### `R005-C-001` 离线静态文件与撤权后 fail-closed 不可同时成立

R005 要求生成路径已知、可直接打开的离线 HTML，同时要求 cache/file direct read 在撤权后成功数为 0。CLI 能在返回路径前鉴权，但无法收回用户、浏览器或其他进程已经打开或复制的本地文件。必须区分 local-owner 离线档案与动态受限内容，定义 ACL、清除、已打开/复制件残留风险和并发撤权边界。

### Important

#### `R005-I-001` R014 未获批准且未被精确 Hash Gate 绑定

R005 称 R014 为“已冻结”，但 R014 实际状态为 `candidate_unapproved`；R005 只引用路径和数量，没有绑定 contract ID、revision、whole-file SHA-256 与 `field_catalog_sha256`，137 字段语义可以在 R005 Hash 不变时漂移。

#### `R005-I-002` 39 表只有数量，没有 137 字段 Owner 映射

当前没有 `field_id -> table/column or DTO`、键、基数、事实/推导 Owner、reducer 和历史策略；十模块与十 PM 表并非一一对应，不能验证缺表、重复事实或 `ProjectProgressSnapshot` 的 Owner。

#### `R005-I-003` 页面生成时间与确定性 Hash 矛盾

页面要求显示墙钟生成时间，但相同输入又要求相同页面内容 Hash。必须使用事实截止时间/快照时间，或把墙钟时间完全排除出页面内容和 fingerprint 并定义规范化 Hash。

#### `R005-I-004` 代码 locator 不能跨重构保持稳定身份

`module + qualified_symbol + signature discriminator` 在模块移动、重命名和改签名时会改变。必须增加独立 `symbol_id`、移动/重命名识别、alias 和一拆多/多并一歧义验收。

#### `R005-I-005` JSON 机器合同未编码 REQ/AC/NFR 语义

JSON 只列 16/11 个 ID，不能检测 Markdown AC、退出码、安全或 NFR 指标在 ID 不变时的漂移。应建模稳定 AC ID、指标、验证方法和追踪，或由完整 Hash Manifest 加逐条投影一致性校验。

#### `R005-I-006` 异步状态机没有合法转移和失败收敛

只有状态名称，没有 transition、guard、terminal、retry、lease fencing 或恢复规则；`commit_not_authorized`、`ready_to_integrate`、失租和过期执行器不能确定收敛到何处。

## 已通过核验

- R005 完整替代 R001–R004；REQ 16 条且各 4 个 AC；NFR 11 条。
- 知识核心 29 表、PM 10 表、合并 39 个唯一名称、FTS 2 表。
- R014 实际为 10 个业务页、128 个业务字段、6 个公共字段、3 个目录字段，共 137 个唯一字段 ID。
- 三种快照/代次概念已文字区分；站点只读、多页面、全页面详情方向清楚。
- 架构链和 composition root 与 `AGENTS.md` 一致；`TASK-IMPLEMENT-002-R001` 明确隔离。

## 真实验证

- `jq -e .`：R005 JSON 与 R014 JSON 均通过。
- SHA-256：R005 Markdown `df688a2bc6846eff0b3bf78b431f8fe2497f5417182f6934ede2c99191e6286f`；R005 JSON `9e304b72ea77637b1237e7fb140d630b5860e56390846805deb062b0be2670bf`；R014 `836fadc2c214ef2f56b2a21ef2fb705445a58ca7ddb0047f3b638292ba578d33`。
- 结构统计：REQ 16、NFR 11、每 REQ AC 4；core 29、PM 10、总表 39；R014 字段 137 且唯一。

## 评分

- 需求符合度：18 / 30
- 架构一致性：13 / 20
- 测试充分性：10 / 20
- 机器合同质量：10 / 20
- 文档与记忆同步：7 / 10
- 总分：58 / 100

## Gate

存在 1 个 Critical 和 6 个 Important，必须 `changes_requested`。整改并由同一独立 Reviewer 复审通过前，不得进入精确 Hash 人工确认、正式设计、迁移或实现。

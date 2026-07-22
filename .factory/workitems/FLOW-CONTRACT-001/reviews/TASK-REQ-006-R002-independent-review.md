# TASK-REQ-006 R002 Independent Requirement Review

- Work item: `FLOW-CONTRACT-001`
- Task: `TASK-REQ-006-project-knowledge-index-and-deterministic-docs`
- Review target: `REQ-CHANGE-PROJECT-KNOWLEDGE-001-R002`（由冻结 R001 与 R002 增量共同组成）
- reviewer_type: `independent_subagent`
- reviewer_id: `/root/req006_r002_review_b`
- reviewer_independence_evidence: 本 reviewer 未参与 R001/R002 编制；仅依据派发的 6 个文件化项目输入执行隔离评审，未读取完整 PRD、实现者会话、其他项目文档或全仓内容。
- review_status: `changes_requested`
- next_gate_status: `changes_requested`
- author_self_check_score: `n/a`
- review_score: `80 / 100`
- human_confirmation_required: `false`
- gate_reason: `none`（先完成同范围需求合同整改与复审）

## 评分

- 需求符合度：`24 / 30`
- 架构一致性：`17 / 20`
- 测试充分性：`15 / 20`
- 代码质量（需求/机器合同质量）：`15 / 20`
- 文档与记忆同步：`9 / 10`

## 覆盖核对

| 核对项 | 结论 | 证据 |
|---|---|---|
| 用户七点与确定性命令面 | 覆盖 | R001 `REQ-PKI-001` 至 `REQ-PKI-008` 覆盖确定性进度、最小文档集、单记忆点、SQLite 索引、有界缓存、事件驱动压缩、确定性 HTML 和固定命令面。 |
| SQLite 非事实源 | 覆盖 | R001 `REQ-PKI-004` AC-2/AC-3 明确可删除重建且不得反向覆盖正式事实；R001 JSON 同步声明 `without_fact_authority`。 |
| 单一当前记忆点 | 覆盖 | R001 `REQ-PKI-003` 规定默认只读 1 个、最大 8 KiB 的 `MemoryCheckpoint/v1`，扩展读取需 `ContextReadTicket/v1` 与预算。 |
| 事件驱动压缩 | 覆盖 | R001 `REQ-PKI-006` 规定事件/阈值触发隔离投影任务，活动会话不做定时重压缩，计划维护仅兜底。 |
| 有界缓存 | 覆盖 | R001 `REQ-PKI-005` 规定 TTL、容量与登记清理；R002 保留 TTL/总容量约束。 |
| `.factory/pm` 不保存独立事实 | 覆盖 | R002 2.2、4 节及 R002 JSON `pm_boundary` 明确禁止事实存储并迁移到可重建 view cache。 |
| 每个 view + auth + query 仅保留 `current.html` | **部分覆盖** | R002 Markdown 2.1 明确规定，但 R002 JSON 以包含快照/源/renderer 等易变字段的完整 cache key 作为数量约束单位，见 Important-1。 |
| 代码负责 freshness | 覆盖 | R001 要求投影兼容且最新、陈旧则未就绪；R002 将快照、源清单/索引快照、renderer/template/schema、权限与查询纳入指纹，并规定代码判断 hit/refresh。 |
| 跨权限安全 | 基本覆盖 | R001 要求权限过滤；R002 将 `authorization_digest` 纳入 key、禁止跨权限复用并在权限变化时刷新。Markdown 的限定语与机器合同仍有 Minor-1。 |
| R001/R002 继承 | 覆盖 | R002 Markdown 明确“冻结 R001 + R002 增量”共同组成候选；R002 JSON 固定 R001 正文与合同 SHA-256，实测均匹配。`r001_review_valid=false` 表示 R001 不能作为独立 review target，不否定其冻结内容作为 R002 基线。 |
| N/A | 接受 | 输入包没有以 N/A 规避的验收项，无待接受的 N/A 风险。 |

## Findings

### Critical

- 无。

### Important

- [`.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001-R002.md:25`; `.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001-R002.md:47`; `.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001.contract.R002.json:24`] **生成视图的“保留身份”与“freshness 输入指纹”混为同一个 cache key，机器合同不能保证每个 `view_type + authorization_digest + normalized_query` 只有一个 `current.html`。** Markdown 2.1 以稳定三元组作为保留单位，但 `RenderCacheKey/v1` 与 JSON `cache_key_fields` 又加入 `snapshot_id`、源清单、renderer、template 等每次刷新可能变化的字段；JSON 只约束 `latest_files_per_cache_key=1`。因此实现可以为不同快照/模板形成多个 full cache key，并为每个 key 各保留一份文件，仍满足 JSON，却违反 PM 补充要求。`scope-key` 也未在机器合同中定义为该稳定三元组。应把稳定的 view scope/输出槽（`view_type + authorization_digest + normalized_query`）与易变的 `input_fingerprint` 分开，并在机器合同中明确“每个 view scope 恰有至多一个 `current.html`；刷新原子替换同一槽位并移除旧登记”。同时显式覆盖 R001 JSON 的 `generated_view_versions_per_kind=3`，避免合并解释歧义。

### Minor

- [`.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001-R002.md:57`; `.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001.contract.R002.json:45`] Markdown 仅禁止不同权限摘要共享“包含敏感字段”的 HTML，而机器合同无条件声明 `cross_authorization_reuse_allowed=false`。建议 Markdown 同步为无条件禁止跨 `authorization_digest` 复用，避免实现阶段引入“非敏感页面”例外判断。

## Verification

- `shasum -a 256 <R001.md> <R001.contract.json>`：exit `0`；分别得到 `f432822ac5dc53f8062347d1716984c737142057d56f631660e6bb9ef95f6832` 与 `a063f1064da516c83b6aac198b6957d523abe9a35fa7c6c4292f37e32e7aea9c`，与 R002 `base_candidate` 完全一致。
- `jq -e . <R001.contract.json> <R002.contract.json>`：exit `0`；两份机器合同均为合法 JSON。
- `rg -n "SQLite|事实源|MemoryCheckpoint|8 KiB|事件|cache|current\\.html|authorization_digest|freshness|renderer|template|代码地图|R001|共同构成|覆盖" <指定 5 个需求输入>`：exit `0`；逐项定位到上述覆盖条款，并确认保留单位在 Markdown 与 JSON 间存在语义差异。

## Gate

`changes_requested`

存在 1 个 Important，按 review rubric 不得批准。整改应保持在当前 R002 需求正文与机器合同范围内；修复后需由独立 reviewer 复审，当前结论不等于人工批准，也不得进入正式 PRD、设计或实现。

# TASK-REQ-006 R003 Independent Rereview

- Work item: `FLOW-CONTRACT-001`
- Task: `TASK-REQ-006-project-knowledge-index-and-deterministic-docs`
- Review target: `REQ-CHANGE-PROJECT-KNOWLEDGE-001-R003`
- reviewer_type: `independent_subagent`
- reviewer_id: `/root/req006_r002_review_b`
- reviewer_independence_evidence: 本 reviewer 是提出 R002 findings 的原独立 reviewer，未参与 R003 整改；本轮只读取复审输入说明、其中列出的 7 个文件化 Required inputs 以及评审 rubric，未读取完整 PRD、实现者会话、全仓内容，也未执行 Git。
- review_status: `changes_requested`
- next_gate_status: `changes_requested`
- author_self_check_score: `n/a`
- review_score: `85 / 100`
- findings_count: `Critical=0, Important=1, Minor=0`
- human_confirmation_required: `false`
- gate_reason: `none`（先修复同范围机器/人类合同的 cache-hit 授权失效条件并复审）

## 评分

- 需求符合度：`26 / 30`
- 架构一致性：`18 / 20`
- 测试充分性：`16 / 20`
- 代码质量（需求/机器合同质量）：`16 / 20`
- 文档与记忆同步：`9 / 10`

## Prior Finding Closure

### `R002-I-001`: closed

- R003 Markdown 将稳定的 `RenderViewScope/v1` 限定为 `view_type + authorization_digest + normalized_query_sha256`，并把快照、源清单及 renderer/template/schema 变化移入只控制刷新的 `RenderInputFingerprint/v1`。
- 输出路径只由 `view_scope_sha256` 决定；每 scope 恰有一行、至多一个 `current.html`，fingerprint 变化只原子替换同一路径，不增加行、文件或历史 fingerprint。
- R003 Markdown 明确把 R001 `generated_view_versions_per_kind=3` 覆盖为“每个 view scope 为 1”；R003 JSON 同时声明 `latest_files_per_scope=1`、`sqlite_rows_per_scope=1`、禁止历史 fingerprint/file，并在 `overrides` 中覆盖 R001 的旧值、替换 R002 的 per-cache-key 规则。按 R003 Markdown 与机器合同合并语义，R001 三版本默认已被明确覆盖。

### `R002-M-001`: closed

- R003 Markdown 无条件禁止任意不同 `authorization_digest` 之间复用 HTML，不再以是否含敏感字段为条件。
- R003 JSON 同步声明 `cross_digest_reuse_allowed=false`，并要求登记权限范围、禁止未知摘要写 cache、要求撤销后清理。

## Required Check Results

| Check | Result | Evidence |
|---|---|---|
| Stable scope 与易变 fingerprint 分离 | Pass | R003 Markdown 16-36；R003 JSON 22-50。 |
| 每 scope 唯一 SQLite 行和 `current.html` | Pass | `sqlite_rows_per_scope=1`、`latest_files_per_scope=1`、`historical_fingerprints_or_files_allowed=false`，fingerprint 不控制路径。 |
| R001 三版本默认被覆盖 | Pass | R003 Markdown 36；R003 JSON 65-68。 |
| 跨 authorization 无条件隔离 | Pass | R003 Markdown 38-40、49；R003 JSON 60-64。 |
| 刷新失败语义 | Pass | 失败保留最后已验证文件但不标为当前，状态为 `stale_after_refresh_failure`；同 scope 行数和文件数不增加。 |
| Scope 边界 | Pass | 新槽要求登记的 authorization scope；所有 scope 受 authorization registry、TTL、256 MiB 总容量约束。 |
| Cache hit | **Fail** | fingerprint/file 条件存在，但未明确要求 authorization 当前有效且 scope 未撤销，见 `R003-I-001`。 |
| 授权撤销 | **Fail** | 只规定禁止新写和下一维护批次删除，没有明确禁止清理前读取/返回既有 cache，见 `R003-I-001`。 |
| N/A | Accepted | 输入包未以 N/A 规避 Required checks。 |

## Findings

### Critical

- 无。

### Important

- `R003-I-001` [`.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001-R003.md:40`; `.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001-R003.md:44`; `.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001.contract.R003.json:30`; `.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001.contract.R003.json:53`; `.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001.contract.R003.json:60`] **授权撤销后的 cache-hit/读取语义没有 fail-closed。** 合同规定未知或已撤销摘要不得“创建/写入”磁盘 cache，并把既有 scope 的物理删除延后到下一维护批次；但 AC-1 与机器合同的 cache-hit 条件只要求 scope/fingerprint/文件 Hash 匹配，没有明确要求 `authorization_digest` 在每次读取时仍为 active/registered，也没有明确禁止在异步清理前返回撤销 scope 的既有 `current.html`。因此实现可在不违反现有文字的情况下命中已撤销权限的旧页面。应将“active registered authorization”设为 cache-hit 和任何返回路径的前置条件；撤销必须立即禁止读取/返回并把 scope 标记不可服务，物理删除仍可异步执行。机器合同应显式表达该 read/serve deny 规则及相应 reason code。

### Minor

- 无。

## Verification

- `jq -e . <R003.contract.json>`：exit `0`；R003 机器合同为合法 JSON。
- `jq -e '<R003 required semantic assertions>' <R003.contract.json>`：exit `0`，输出 `true`；确认稳定 scope 字段、每 scope 单行/单文件、fingerprint 只控制刷新、同路径原子替换、失败状态、无条件跨 digest 隔离、R001/R002 override、人工批准门均按声明存在。
- `shasum -a 256 <7 Required inputs>`：exit `0`；R002 review、triage、response、R003 Markdown、R003 JSON 的实际 Hash 分别为 `8ee2413697b3d2cd14a95e87dff4c50fe759b42fd20ee38b488022f98052c485`、`8adc722a6b993d3bae091cc508f9fe83d607037ffe3f19d26f6e279e7340d9c0`、`3b308d2b57ba02cd524c4f9cffa039bd7955701b26e0a9fe7dc178fc2f13efea`、`c8daddc5cb0d1067d214cb7aa69632c8edc05dcdbf7a7ab859d18dc8f141d748`、`7d5c60aaacbc75bb3fc60625eb309650c6a73b79ccb9a43698c62cb0792956f4`，与作者证据中记录值一致；evidence 与 report 本身 Hash 为 `29bfbc01fc9d31ea00692d121f82b345cfcae9247edc6687bbb3d3b22bc0de8e`、`0ef51d36174b1eb00958f6523ccb4ea7e34b73648e81a4f90a2211595686dfeb`。
- `rg -n "RenderViewScope/v1|RenderInputFingerprint/v1|current\\.html|latest_files_per_scope|sqlite_rows_per_scope|cross_digest_reuse_allowed|generated_view_versions_per_kind|stale_after_refresh_failure|revoked|撤销|cache hit|cache_hit|scope_bounds|TTL|256 MiB" <R003.md> <R003.contract.json>`：exit `0`；定位全部 Required checks，并确认撤销条款只规定禁止新写/后续清理，cache-hit 条件未含 active authorization/read deny。
- `rg -n "TODO|TBD|待定|稍后决定" <R003.md> <R003.contract.json>`：exit `1`，预期 no-match；无未决占位符。

## New Findings

- `R003-I-001`：授权撤销后的 cache hit/read/serve 条件缺失，`Important`。

## Next Gate

`changes_requested`

两项 R002 finding 已关闭，但新发现 1 个 Important，按 rubric 不能批准。应在当前 R003 需求合同范围内补齐撤销后立即拒绝读取/返回的规则并交同一独立 reviewer 复审。reviewer 结论不等于 human approval，也不授权修改正式 PRD、设计、代码、Git 或发布状态。

# TASK-REQ-006 R004 Independent Rereview

- Work item: `FLOW-CONTRACT-001`
- Task: `TASK-REQ-006-project-knowledge-index-and-deterministic-docs`
- Review target: `REQ-CHANGE-PROJECT-KNOWLEDGE-001-R004`
- reviewer_type: `independent_subagent`
- reviewer_id: `/root/req006_r002_review_b`
- reviewer_independence_evidence: 本 reviewer 是提出 R003 finding 的同一独立 reviewer，未参与 R004 整改；本轮只读取 R004 复审输入说明、其中列出的 7 个文件化 Required inputs 以及评审 rubric，未读取完整 PRD、实现者会话或全仓内容，未执行 Git。
- review_status: `approved`
- next_gate_status: `pending_human_confirmation`
- author_self_check_score: `n/a`
- review_score: `96 / 100`
- findings_count: `Critical=0, Important=0, Minor=0`
- human_confirmation_required: `true`
- gate_reason: `governance_gate`

## 评分

- 需求符合度：`30 / 30`
- 架构一致性：`20 / 20`
- 测试充分性：`18 / 20`
- 代码质量（需求/机器合同质量）：`19 / 20`
- 文档与记忆同步：`9 / 10`

## Finding Closure

### `R003-I-001`: closed

- R004 Markdown 与机器合同都将当前权威授权检查设为 `cache_hit`、`file_read`、`file_path_return`、`html_body_return` 的共同前置条件；路径不得在检查前暴露。
- `unknown`、`inactive`、`revoked` 固定返回 `VIEW_AUTHORIZATION_INACTIVE`；授权检查超时、不可用或无法证明 active 固定返回 `VIEW_AUTHORIZATION_CHECK_FAILED`。两类失败均 `fail_closed`，不返回 HTML body 或文件路径。
- 权威撤销事实提交后，后续服务决策立即拒绝；拒绝明确不等待 SQLite 投影、维护批次或物理删除。SQLite 标记及磁盘删除仅作为异步清理，不形成服务窗口。
- 恢复为 active 后必须重新计算当前 `RenderInputFingerprint/v1`；只有当前 fingerprint 与文件 SHA-256 均匹配才能复用，否则刷新同一 stable scope 的 `current.html`。

## Regression Check

### `R002-I-001`: no regression

- R004 以 R003 为冻结基础候选，没有覆盖 `RenderViewScope/v1` 与 `RenderInputFingerprint/v1` 的分离、每 scope 单行/单文件或同路径原子刷新规则。
- R004 授权 scope match 继续使用 `authorization_digest + view_type + normalized_query_sha256`，与稳定 scope 身份一致；reactivation 只重新校验/刷新，不新增输出槽。

### `R002-M-001`: no regression

- R004 对所有返回路径要求请求当前仍获授权访问对应 `view_type + normalized_query_sha256`，且 `authorization_digest` 必须登记并为 active。
- R004 未引入任何跨 digest 复用例外；R003 的无条件跨 authorization 隔离继续有效。

## Required Check Results

| Check | Result | Evidence |
|---|---|---|
| Cache hit gate | Pass | R004 Markdown 18-23、34；R004 JSON `required_before` 含 `cache_hit`。 |
| File read gate | Pass | R004 Markdown 18、30、35；R004 JSON `required_before` 含 `file_read`。 |
| Path return gate | Pass | R004 Markdown 18、25、30、35；JSON 含 `file_path_return` 且 `filesystem_path_exposed_before_check=false`。 |
| HTML body return gate | Pass | R004 Markdown 18、25、35、37；JSON 含 `html_body_return` 且失败时 `html_or_path_returned_on_failure=false`。 |
| Inactive/revoked fail-closed | Pass | 固定 `VIEW_AUTHORIZATION_INACTIVE`；required status 为 active。 |
| Unavailable/unproven fail-closed | Pass | 固定 `VIEW_AUTHORIZATION_CHECK_FAILED`；failure mode 为 `fail_closed`。 |
| 拒绝不等待投影/维护/删除 | Pass | 三个 `serve_denial_waits_for_*` 字段均为 false；物理删除可异步。 |
| Reactivation 校验 | Pass | 必须重算 fingerprint，且复用要求当前 fingerprint 与文件 SHA-256 匹配。 |
| R002 findings 回归 | Pass | 稳定 scope/fingerprint 分离及无条件跨权限隔离均未被覆盖或削弱。 |
| N/A | Accepted | 输入包未以 N/A 规避 Required checks。 |

## Findings

### Critical

- 无。

### Important

- 无。

### Minor

- 无。

## New Findings

- 无。

## Verification

- `jq -e . <R004.contract.json>`：exit `0`；R004 机器合同为合法 JSON。
- `jq -e '<R004 required semantic assertions>' <R004.contract.json>`：exit `0`，输出 `true`；确认四类授权前置路径、active/scope 要求、两类固定失败码、fail-closed、无失败内容/路径返回、即时撤销拒绝、不等待 SQLite/维护/物理删除、reactivation 校验、全 HTML 快路径覆盖和人工批准门。
- `shasum -a 256 <7 Required inputs>`：exit `0`。R003 review、triage、response、R004 Markdown、R004 JSON 实际 Hash 分别为 `86e06dad40c61d7be8d2366a88cdc00d9958e73e566330e44838e2bfa5684b08`、`e25fe0c54244a8c8b3a3e9336274c80e908f6c4a606f5151216f2004c486b76a`、`5e6c7db259d389732078a1bad882f639f2bb3499f982f38b863b5cca9be4d346`、`e3626b8881d3c932bddd5232d61df3808c722545a28443f666fc31b7d0749e74`、`0a8bdd04f95f539e81861c4c5c9ce4cc170b78d0fee88326b669baf1924536b0`，与作者证据一致；evidence 与 report 本身 Hash 为 `6c9176521a247fe7d824341b038789dd2d0d79f8b5d3ac485cd64add281cf1e9`、`d80b779098f817e50d478a32fbecc699f45f0fcfc153b13bb4dbeecfd43544a3`。
- `rg -n "cache-hit|cache_hit|文件读取|file_read|文件路径返回|file_path_return|HTML 内容返回|html_body_return|active|inactive|revoked|unavailable|unproven|VIEW_AUTHORIZATION_INACTIVE|VIEW_AUTHORIZATION_CHECK_FAILED|fail.closed|SQLite|维护|physical|物理删除|reactiv|恢复为 active|fingerprint|Hash|all_existing_html_fast_paths|human|人工批准" <R004.md> <R004.contract.json>`：exit `0`；Required checks 均有对应人类与机器合同条款。
- `rg -n "RenderViewScope|RenderInputFingerprint|cross_digest_reuse_allowed|authorization_digest|view_type|normalized_query_sha256|current.html" <R004.md> <R004.contract.json>`：exit `0`；确认 R004 的 scope match/reactivation 与已关闭 R002 findings 一致，未引入新槽或跨权限复用。
- `rg -n "TODO|TBD|待定|稍后决定" <R004.md> <R004.contract.json>`：exit `1`，预期 no-match；无未决占位符。

## Decision

`approved`

本独立 reviewer 确认 `R003-I-001` 已关闭，`R002-I-001` 与 `R002-M-001` 无回归，且未发现新 Critical、Important 或 Minor。

## Next Gate

`pending_human_confirmation`

本 `approved` 只代表独立需求复审通过，不等于 human approval，也不授权修改正式 PRD、设计、实现、Git 或发布状态。下一步只能进入精确候选集合的人工确认 Gate。

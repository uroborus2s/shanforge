# REQ-CHANGE-PROJECT-KNOWLEDGE-001-R004 授权撤销读取关闭修订候选

## 版本信息

| 项目 | 内容 |
|---|---|
| 需求变更 ID | `REQ-CHANGE-PROJECT-KNOWLEDGE-001` |
| 候选修订 | `R004` |
| 基础候选 | R001 + R002 + R003 |
| 来源评审 | `TASK-REQ-006-R003-independent-rereview.md` |
| 状态 | `ready_for_rereview` |
| 日期 | 2026-07-21 |

## 1. Finding 处理

### `R003-I-001` 撤销后所有返回路径立即 fail-closed

`current.html` 是否存在、fingerprint 是否匹配、SQLite 行是否仍登记，都不能代替当前授权判断。每次 cache-hit、文件读取、文件路径返回或 HTML 内容返回之前，代码必须从权威授权来源取得该请求对应的当前状态，并同时满足：

- `authorization_digest` 已登记；
- 当前状态为 `active`；
- 当前请求仍被允许访问该 `view_type + normalized_query_sha256`；
- 授权检查成功完成。

任何条件不满足都必须 fail-closed，不得返回 HTML 内容或磁盘路径：

- 未知、inactive 或 revoked：`VIEW_AUTHORIZATION_INACTIVE`；
- 权威授权检查超时、不可用或无法证明 active：`VIEW_AUTHORIZATION_CHECK_FAILED`。

授权撤销事实一旦在权威来源提交，之后开始的服务决策必须立即拒绝该 scope；不得等待 SQLite 投影刷新、维护批次或物理删除。SQLite `render_view` 行可异步标记为 `revoked_pending_cleanup`，磁盘 `current.html` 可在下一维护批次删除，但两者在此期间都不可由项目查看命令命中、读取或返回。实现不得在授权检查前暴露文件路径。

## 2. `REQ-PKI-009` 修订后验收补充

- AC-1：cache hit 必须同时满足 R003 的 scope/fingerprint/file Hash 条件和 R004 的当前 active 授权条件；授权状态不是 active 时不得按 hit 处理。
- AC-2：`project status --format html` 与 `docs build` 等任何返回现有 HTML 的快速路径，都必须执行相同的当前授权检查；无“只返回旧路径”的绕过分支。
- AC-3：授权撤销事实提交后，后续服务决策立即拒绝；SQLite 状态和物理文件允许异步清理，但清理延迟不得改变拒绝结果。
- AC-4：授权检查失败时返回固定 reason code 和 receipt，不读取或返回 HTML；不得退化为旧 cache、匿名权限或 AI 判断。
- AC-5：恢复为 active 后，必须重新计算当前 `RenderInputFingerprint/v1`；只有 fingerprint 与文件 Hash 都匹配才能复用旧文件，否则刷新同一 scope 的 `current.html`。

## 3. Gate

R004 只处理 `R003-I-001`，没有扩大正式文档、设计、代码、Git 或发布权限。必须交原独立 Reviewer 再复审；复审通过仍不等于人工批准。

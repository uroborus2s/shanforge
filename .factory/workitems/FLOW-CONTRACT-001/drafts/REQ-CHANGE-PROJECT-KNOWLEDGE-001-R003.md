# REQ-CHANGE-PROJECT-KNOWLEDGE-001-R003 生成视图唯一槽修订候选

## 版本信息

| 项目 | 内容 |
|---|---|
| 需求变更 ID | `REQ-CHANGE-PROJECT-KNOWLEDGE-001` |
| 候选修订 | `R003` |
| 基础候选 | R001 + R002 |
| 来源评审 | `TASK-REQ-006-R002-independent-review.md` |
| 状态 | `ready_for_rereview` |
| 日期 | 2026-07-21 |

## 1. Finding 处理

### `R002-I-001` 稳定输出槽与 freshness 指纹分离

R002 中的 `RenderCacheKey/v1` 拆成两个不同对象：

1. `RenderViewScope/v1` 是稳定输出身份，只包含：
   - `view_type`；
   - `authorization_digest`；
   - `normalized_query_sha256`。
2. `RenderInputFingerprint/v1` 是易变刷新输入，包含：
   - `view_scope_sha256`；
   - `snapshot_id/snapshot_sha256/as_of_H`；
   - `source_manifest_sha256`；
   - `renderer/template/schema` 版本与 Hash。

路径只由稳定 scope 决定：

```text
.factory/cache/views/<view-type>/<view-scope-sha256>/current.html
```

每个 `RenderViewScope/v1` 在 SQLite `render_view` 中恰有一行，在文件系统中至多有一个 `current.html`。刷新只更新同一行的 `input_fingerprint` 和 `output_sha256`，并原子替换同一路径；旧 fingerprint 不保留新行或历史文件。R001 `generated_view_versions_per_kind=3` 被本修订明确覆盖为“每个 view scope 为 1”。

### `R002-M-001` 跨权限复用统一禁止

任何两个不同 `authorization_digest` 的 HTML 都不得复用，不区分页面是否包含敏感字段。权限范围必须先在 source registry 登记；未知或已撤销权限摘要不得创建磁盘 cache。权限撤销后，对应 view scope 在下一维护批次删除。

## 2. `REQ-PKI-009` 修订后验收

- AC-1：`RenderViewScope/v1` 相同且当前文件、登记输出 Hash 与 `RenderInputFingerprint/v1` 全部匹配时，直接返回同一 `current.html`，不重新渲染。
- AC-2：scope 相同但 fingerprint 改变时，在临时文件完成渲染和验证，再原子替换同一路径；scope 行数和 HTML 文件数不增加。
- AC-3：scope 改变时仅允许已登记 `authorization_digest` 创建新的受控槽；查询参数规范化后相同的请求必须命中同一 scope。
- AC-4：每个 scope 文件数始终小于等于 1；所有 scope 总量继续受授权注册表、TTL 和 256 MiB 总容量三重约束。
- AC-5：刷新失败保留最后已验证文件，但登记为 `stale_after_refresh_failure`，默认响应不得把它标为当前；receipt 返回最后成功 fingerprint 和失败原因。
- AC-6：不同权限摘要无条件禁止跨 scope 复用，授权撤销 cache 必须被清理。

## 3. Gate

R003 只处理 `R002-I-001` 和 `R002-M-001`，没有扩大正式文档、设计、代码、Git 或发布权限。必须交原独立 Reviewer 复审；复审通过仍不等于人工计划批准。

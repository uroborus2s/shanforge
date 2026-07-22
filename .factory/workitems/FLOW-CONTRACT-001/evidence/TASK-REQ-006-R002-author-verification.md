# TASK-REQ-006 R002 作者验证

- 日期：2026-07-21
- 有效候选集合：R001 基础 + R002 增量覆盖
- 结论：`passed_ready_for_independent_review`

## 用户增量覆盖

| 用户要求 | 验证结果 |
|---|---|
| `.factory/pm` 不保存独立项目事实 | R002 明确迁移为统一生成视图 cache |
| Skill + 命令 + 代码定向组装 HTML | `REQ-PKI-008/009` 明确 AI/代码分工 |
| 进度未变化时直接返回最后 HTML | 由完整 `RenderCacheKey/v1` 和磁盘 Hash 确定，`cache_hit=true` |
| 变化时才刷新 | 临时生成、完整校验、原子替换 `current.html` |
| HTML 只保留最后刷新版本 | 每个视图、权限摘要和规范化查询 cache key 最多 1 个文件 |
| 不同权限不得复用敏感 HTML | `authorization_digest` 是 cache key 必填字段，跨权限复用禁止 |

## 验证结果

- R002 JSON：`python3 -m json.tool` 通过。
- R002 无 `TODO/TBD/待定`。
- R001 候选 SHA/合同 SHA 与 R002 base binding 一致。
- R001 的未完成独立评审被中断，`r001_review_valid=false`。
- R002 不授权正式文档、设计、代码、Git、远端或发布操作。

## Hash

| 文件 | SHA-256 |
|---|---|
| 更新后 TaskCard | `63c1baede89dc49f1cd11d665d922825711f3a32678485c8b09d91cf698317ae` |
| R002 增量候选 | `71f46c0f830f0da61f24500de6fb7eb785c6e895828866fa24cd255bb086c3fe` |
| R002 机器合同 | `d5f6804756b56fd58bfc6ef279ff4c35dc58da405b47aabc69e30e752d22a448` |

作者验证不等于独立批准或人工计划批准。

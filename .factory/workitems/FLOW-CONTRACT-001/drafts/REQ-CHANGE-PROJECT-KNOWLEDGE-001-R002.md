# REQ-CHANGE-PROJECT-KNOWLEDGE-001-R002 生成视图与确定性刷新增量候选

## 版本信息

| 项目 | 内容 |
|---|---|
| 需求变更 ID | `REQ-CHANGE-PROJECT-KNOWLEDGE-001` |
| 候选修订 | `R002` |
| 基础候选 | `R001`，SHA-256 `f432822ac5dc53f8062347d1716984c737142057d56f631660e6bb9ef95f6832` |
| 状态 | `ready_for_review` |
| 日期 | 2026-07-21 |
| 提出人 | `uroborus` |
| 编制人 | `AI_EXECUTOR` |

## 1. 修订原因

用户进一步明确：`.factory/pm` 不应形成另一套需要维护的项目内容。项目进度页面必须通过 Skill 调用固定命令，由代码从实时事实源、索引、记忆和代码地图定向组装；HTML 只是临时查看缓存。代码必须判断是否需要刷新，事实和渲染输入未变化时直接返回最后生成的 HTML。

本文件与冻结 R001 共同构成 R002 有效候选；除本文件明确覆盖的条款外，R001 其余内容不变。

## 2. 对 R001 的覆盖

### 2.1 覆盖 `REQ-PKI-005` 的生成视图保留规则

- 生成 HTML 不保留带时间戳或修订号的历史版本。
- 每个 `view_type + authorization_digest + normalized_query` 只保留一个 `current.html`。
- 新页面原子激活后立即删除同一 cache key 的旧文件；其他权限范围的页面不得互相复用。
- 生成视图仍受 TTL 和总容量约束；过期视图可直接删除并按需重建。

### 2.2 覆盖 `REQ-PKI-007` 的输出路径与发布语义

- 临时 HTML 默认进入 `.factory/cache/views/<view-type>/<scope-key>/current.html`。
- `.factory/pm` 不保存 Project、Requirement、Task、Gate、Evidence 或统计事实；迁移后可删除，不再作为独立子系统。
- 如需公开部署文档站点，必须使用显式发布目录和发布 Workflow；临时查看缓存不能冒充已发布站点。

### 2.3 覆盖 `REQ-PKI-008` 的 AI/命令分工

- AI 只选择已登记 Skill/命令和参数，不读取多份项目材料后自行判断页面是否过期。
- 命令返回 `cache_hit`、`refreshed`、`output_path`、`input_fingerprint`、`output_sha256`、`snapshot_id` 和结构化原因码。
- freshness、权限、输入 Hash、渲染和原子替换全部由代码完成。

## 3. 新增需求

### `REQ-PKI-009` 最新生成视图与确定性刷新

- 优先级：P0。
- 系统必须为项目进度和人类文档 HTML 建立确定性 `RenderCacheKey/v1`：
  - `view_type`；
  - 获授权事实 `snapshot_id/snapshot_sha256/as_of_H`；
  - 文档源清单或知识索引快照 Hash；
  - renderer/template/schema 版本与 Hash；
  - `authorization_digest`；
  - 规范化查询参数。
- AC-1：当 cache key、已登记输出 Hash 和磁盘文件 Hash 全部相同，命令不得重新读取未登记源或重新渲染，直接返回最后文件，`cache_hit=true`、`refreshed=false`。
- AC-2：任一输入、权限、模板、查询参数或文件 Hash 改变，命令在临时路径完成渲染、链接/权限/Manifest 校验后原子替换 `current.html`，`cache_hit=false`、`refreshed=true`。
- AC-3：刷新失败时不得破坏最后一份已验证页面；返回明确失败原因和最后成功快照信息，不把旧页面标为当前。
- AC-4：不同 `authorization_digest` 不得共享包含敏感字段的 HTML；授权撤销后，对应 scope cache 在下一维护批次删除。
- AC-5：同一 view cache key 的 HTML 文件数量始终小于等于 1；缓存目录中不存在历史版本堆栈。
- AC-6：进度事实未变但 renderer/template、权限、参数或源清单改变时仍必须刷新；“进度没有变化”不得由 AI 主观判断。

## 4. `.factory/pm` 结论

`.factory/pm` 没有独立存在的事实价值。它当前承担的展示职责统一归入可重建生成视图：

```text
.factory/cache/views/
├── project-status/<scope-key>/current.html
└── docs/<scope-key>/current.html
```

SQLite `render_cache` 保存 cache key、最后成功输出 Hash、路径和生成时间；它仍是可删除投影。HTML 内嵌同一份来源/快照/权限/renderer 元数据，目录中不另存版本化 Manifest 文件。

## 5. 迁移影响

- `using-shanforge`、PM 看板渲染入口和相关测试必须从 `.factory/pm/generated/` 迁移到统一生成视图端口。
- 迁移需保留一次兼容读取或明确失败提示；不得同时长期维护两个输出目录。
- 现有 PM 生成文件只能在新命令成功并回读验证后清理。
- 该迁移属于后续设计/实现任务，R002 需求候选本身不删除目录或文件。

## 6. Gate

R002 未获独立评审或人工计划批准。R001 已因用户新增要求失效，不得继续评审、批准、融入正式 PRD 或驱动设计实现。

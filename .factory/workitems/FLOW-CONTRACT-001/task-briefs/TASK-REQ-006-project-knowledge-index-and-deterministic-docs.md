# TASK-REQ-006 项目知识索引、最小文档与确定性输出需求变更

## 1. 基本信息

| 项目 | 当前事实 |
|---|---|
| WorkItem | `FLOW-CONTRACT-001` |
| TaskCard | `TASK-REQ-006-project-knowledge-index-and-deterministic-docs` |
| 处理模式 | `change_requirement` |
| 中文名称 | 项目知识索引、最小文档与确定性输出需求变更 |
| 当前状态 | `R009_exact_candidate_human_approved / formalization_and_design_in_progress` |
| 当前候选 | `REQ-CHANGE-PROJECT-KNOWLEDGE-001-R009` + R009 PM field map + 已发布 R014 release pin（完整替代 R001–R008） |
| 需求变更 ID | `REQ-CHANGE-PROJECT-KNOWLEDGE-001` |
| 来源 | `uroborus` 2026-07-21 当前会话完整讨论与落地指令 |
| 父级正式需求 | `REQ-CHANGE-WF-CTL-010-001`、`REQ-CHANGE-AI-EXEC-ASYNC-001`、`REQ-CHANGE-ARTIFACT-RETENTION-001`、`REQ-AI-WORKFLOW-005/007/048/049/052/053` |
| 受影响 Workflow | `WF-CTL-001`、`WF-CTL-009`、`WF-CTL-010`、`WF-BASE-008` |
| 受影响基线 | 文档 IA、Memory、Artifact、SQLite 投影、CLI/API、HTML 输出 |

## 2. 用户意图

用户要求把固定、重复、可确定计算的项目状态、文档导航、索引、压缩和清理工作交给代码与命令完成，减少 AI 临场扫描、判断和上下文消耗。正式 `docs/` 只保存人类阅读的当前有效文档，并按项目类型和真实暴露面创建最小必要集合；`.factory/` 保存执行事实、项目记忆、进度投影和可清理缓存。SQLite 负责可重建的文档、记忆、代码和追踪关系索引，使 AI 从一个当前记忆点开始，再按显式理由定向读取。

## 3. 需求边界

### 3.1 本次必须形成的能力

1. 固定命令生成项目进度文本和 HTML，不由 AI 计算完成率、状态或 HTML。
2. 根据项目画像选择最小人类文档集合；无适用事实的文档不得创建。
3. 会话默认只读取一个当前、已验证、受预算约束的记忆点；扩展读取必须通过索引并记录理由。
4. SQLite 管理 Artifact 元数据、路径锚点、Hash、版本、Owner 和跨需求/设计/代码/测试/任务关系；数据库可删除并重建。
5. `.factory/cache/`、生成视图和其他明确标记为 cache 的 Artifact 具有 TTL、容量和保留数量上限，并由确定性维护任务清理。
6. Memory 压缩以权威事件触发的异步投影为主，以计划维护命令为兜底；活动会话不运行定时重压缩。
7. 固定命令把登记的 Markdown 人类文档组装成离线静态 HTML，并生成来源清单与内容 Hash。
8. `.factory/pm` 不保存独立事实；生成视图只保留每个视图与权限范围的最新 HTML，由代码根据输入指纹决定复用或原子刷新。
9. 不持久化行号/字节范围作为主定位；文档、代码、JSON、JSONL、WorkItem、Memory 和 Git 使用稳定语义 locator。
10. SQLite 固定为 29 张知识核心表和 10 张 PM 投影表；十要素覆盖 R014 的 10 个业务模块和 137 个字段。
11. HTML 是可商用展示质量的只读多页面站点；详情使用带返回按钮的完整页面，不使用侧边抽屉。
12. 主会话只登记 durable `PROJECT_STATE_SYNC`；Memory、索引、状态和 HTML 由隔离执行器异步更新，生成物不提交 Git。

### 3.2 非目标

- SQLite 不成为正式需求、设计、任务、代码、测试或 Git 的唯一事实源。
- 不把正式文档正文复制进 `.factory/memory/`。
- 不在 `docs/` 保存 Workflow Catalog、Manifest、Schema、缓存、Review、Evidence 或其他机器专用文件。
- 不为不适用的项目表面批量创建空文档。
- 不在查询会话中同步全量扫描、全量重建、重压缩或清理整个 `.factory/`。
- 不把 SQLite、FTS、自动代码/文档地图、HTML 或 cache 提交 Git。
- 不为每次文档变化保存整库历史快照，不使用标题或行号作为唯一身份。
- 不在项目站点提供新增、编辑、拖拽、审批或状态修改能力。
- 不修改、批准或发布正在整体 Review 前的 `TASK-IMPLEMENT-002-R001` 候选。

## 4. 需求候选

完整需求、验收标准、NFR 和影响分析见：

- `.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001-R009.md`
- `.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001.contract.R009.json`
- `.factory/workitems/FLOW-CONTRACT-001/drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001.pm-field-map.R009.json`
- `.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-REQ-002-R014-release-manifest.json`

R001–R008 仅保留为候选历史，不再叠加解释，也不得作为实现输入。

## 5. Baseline 影响

| Baseline | 影响 |
|---|---|
| 正式需求 | 增量修订项目状态、文档、Memory、Artifact 保留和生成视图要求 |
| 总体架构 | 增加统一 `ProjectKnowledgeIndex` 投影边界；不改变 `access -> application -> domain -> runtime -> settings` 依赖链 |
| 数据 | 增加 29 张知识核心表、10 张 PM 投影表、稳定 locator、source hash 和关系边 |
| API / CLI | 增加确定性 `index/snapshot/find/show/trace/context/sync/maintain` 命令合同 |
| 文档 | `docs` 只保留人类文档；机器合同迁出并由人类索引页链接 |
| Memory | 当前记忆点、扩展读取票据、异步压缩和 freshness 合同 |
| UI | 增加只读、多页面、全页面详情的正式项目展示站点；不含编辑交互 |
| 实现 | 新建独立设计与实现增量；不得并入既有冻结候选 |

## 6. 设计约束

- 事实源变化后，只解析变更来源，按稳定 ID/块 Hash 更新贡献并删除已消失贡献，不得遗留幽灵边。
- 读者只使用已发布 `IndexGeneration`；它与 `ProjectProgressSnapshot`、页面 `RenderFingerprint` 分离。
- 会话启动只验证并读取当前记忆点；需要更多信息时由索引返回最小路径、语义 locator 和读取预算。
- 自动压缩由任务、Gate、阶段关闭或事件/字节阈值触发的 `MemoryProjectionTask` 执行；计划维护任务只修复漏触发和清理过期缓存。
- 所有生成 HTML 均带 Git Commit、事实高水位、索引快照、来源 Hash 和生成器版本。
- durable queue 是异步状态同步的 Owner；子 Agent 只能作为隔离执行器，不能直接抢写主工作树。
- Git 提交 schema、提取器、稳定 ID、人工关系声明和正式事实，不提交生成后的数据库、地图、HTML 或 cache。

## 7. 当前 Gate

R009 已绑定正式 R014 release manifest，并由同一 Reviewer 复审 `approved/99/C0-I0-M0`。`uroborus` 于 2026-07-22 回复“确认”，精确批准 Manifest SHA-256 `8be9d829ea2a895eae043eaf054914cb03b7457a43d51c142cc4ad7f41f577ae` 与 candidate root `ce079fcd80c4e5e7a58e68103e8f225d2b90cdfea703c12adde88f95b3f0df68`。需求 Gate 已关闭，授权原位正式化、设计、计划、实现、测试、迁移及验证后当前任务本地提交。

该批准不包含 `TASK-IMPLEMENT-002-R001`，也不授权 Push、PR、Merge、部署、远端写入或绕过后续质量 Gate。

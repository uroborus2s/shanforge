# REQ-CHANGE-PROJECT-KNOWLEDGE-001-R001 项目知识索引与确定性文档需求候选

## 版本信息

| 项目 | 内容 |
|---|---|
| 需求变更 ID | `REQ-CHANGE-PROJECT-KNOWLEDGE-001` |
| 候选修订 | `R001` |
| 状态 | `ready_for_review` |
| 日期 | 2026-07-21 |
| 提出人 | `uroborus` |
| 编制人 | `AI_EXECUTOR` |
| 父 WorkItem | `FLOW-CONTRACT-001` |
| TaskCard | `TASK-REQ-006-project-knowledge-index-and-deterministic-docs` |

## 1. 目标

建立一条由确定性代码负责的项目知识管线：从正式文档、WorkItem/Ledger、Memory、源码、测试和 Git 提取稳定 ID 与关系，增量更新可重建 SQLite 索引，再从同一验证快照快速生成项目进度和人类文档 HTML。AI 默认只消费一个当前记忆点和索引返回的最小定向读取计划，不再为固定项目查询反复扫描和自由总结。

## 2. 角色与用户故事

- 作为项目负责人，我希望一个命令生成准确的进度文本和 HTML，以便无需等待 AI 临场聚合。
- 作为文档读者，我希望 `docs/` 只有当前有效、中文可导航的人类文档，以便快速理解项目而不接触机器中间件。
- 作为 AI 执行者，我希望从一个当前记忆点和 SQLite 索引开始，以便在明确预算内只读取当前任务真正需要的内容。
- 作为维护者，我希望 Memory 压缩、索引刷新和缓存清理由系统任务自动完成，以便 `.factory/` 不会无限增长。

## 3. 功能需求

### `REQ-PKI-001` 确定性项目进度命令

- 优先级：P0。
- 系统必须提供无交互命令，从同一获授权项目快照输出固定文本或离线 HTML。
- 命令负责事实读取、状态计算、排序、权限过滤、渲染和 Manifest；AI 只负责识别意图、调用命令和解释已返回的代码事实。
- AC-1：给定兼容且最新的投影，命令不扫描非登记路径，返回绑定同一 `snapshot_id` 的文本或 HTML。
- AC-2：给定投影滞后、损坏或权限不足，命令返回结构化未就绪或拒绝，不生成冒充当前状态的页面。

### `REQ-PKI-002` 按项目画像创建最小人类文档集

- 优先级：P0。
- 文档模板必须先读取项目类型、交付表面、部署方式、受众和风险画像，再选择最小必要文档集合。
- `docs/` 只允许人类阅读的 Markdown、图片和静态阅读资源；机器 Catalog、Schema、Manifest、缓存、Evidence、Review 和会话恢复摘要不得进入 `docs/`。
- AC-1：没有 UI、数据库、公共 API、部署或插件暴露面时，对应文档数量为 0。
- AC-2：新增正式页面必须证明现有 Owner 文档无法承载，并登记中文名称、Owner、读者、上游、下游和版本历史。
- AC-3：需求、方案或实现变化默认原位修订当前正文；候选过程在 `.factory/workitems/`，正式历史由文档版本历史和 Git 保存。

### `REQ-PKI-003` 单一当前记忆点与受控扩展读取

- 优先级：P0。
- 每次会话默认只读取一个与项目、Task、Gate、事实高水位和 schema 绑定的 `MemoryCheckpoint/v1`，编码后不得超过 8 KiB。
- Memory 只保存恢复摘要、关键约束、当前 Gate、唯一下一动作和路径/ID 索引，不复制正式正文、聊天全文、Review 全文或长命令输出。
- AC-1：兼容当前记忆点存在时，恢复阶段读取的 memory Artifact 数量为 1，默认 `docs` 和历史 ledger 读取数为 0。
- AC-2：需要更多信息时，必须通过 `ProjectKnowledgeIndex` 返回路径、章节锚点、理由、最大文件数和字节预算；每次扩展读取形成 `ContextReadTicket/v1`。
- AC-3：记忆点过期、损坏或超预算时返回 `memory_recovery_not_ready` 并入队投影任务，不允许无界扩散读取兜底。

### `REQ-PKI-004` 可重建项目知识 SQLite 索引

- 优先级：P0。
- `ProjectKnowledgeIndex/v1` 必须索引 Artifact ID、类型、路径、锚点、Owner、版本、状态、内容 Hash、事实高水位及关系边。
- 索引范围至少覆盖 Requirement、Design、Module、API、Data、UI、Workflow、Task、Test、Evidence、Release、MemoryCheckpoint、SourceSymbol 和 Document。
- AC-1：任一来源改变时，在单一写事务中删除该来源旧贡献并写入新节点/边；读者只能看到完整旧快照或完整新快照。
- AC-2：SQLite 删除或损坏后，可仅从已登记事实源和版本化 reducer 重建相同内容 Hash。
- AC-3：SQLite 不具有独立事实资格，不得反向覆盖正式文档、ledger、代码、测试或 Git。
- AC-4：代码地图至少提供文件、符号、模块、接口和测试的稳定定位；全文检索内容只作为 FTS cache。

### `REQ-PKI-005` 有界缓存和确定性清理

- 优先级：P0。
- 所有 cache Artifact 必须登记类型、owner、创建时间、最后访问、TTL、容量上限、重建命令和 legal-hold 资格。
- 默认 `.factory/cache/` 最大 256 MiB、默认 TTL 24 小时；生成视图每类只保留最新 3 份且最长 7 天。项目配置可以收紧，不得无上限放宽。
- AC-1：Task/Gate/发布关闭后，系统自动入队维护任务清理已过期 cache；失败进入 `cleanup_pending`，不撤销已经成立的业务事实。
- AC-2：清理只能触碰登记的 cache/generated 路径，禁止删除正式 docs、ledger、当前记忆点、发布记录或 legal hold Artifact。
- AC-3：重复清理结果一致，删除计数、释放字节、跳过原因和下次到期时间可审计。

### `REQ-PKI-006` 自动 Memory 压缩策略

- 优先级：P0。
- Memory 压缩必须由隔离 `MemoryProjectionTask` 执行，活动会话不得运行定时重压缩。
- 主触发器：Task、Gate 或阶段关闭；当前记忆点落后 50 个权威事件；未压缩编码字节超过 256 KiB；会话交接请求。
- 兜底触发器：确定性维护命令检查漏触发、过期 checkpoint 和 cache；调度环境可周期执行，但定时器不构成正确性前提。
- AC-1：事件触发只持久化幂等任务请求并立即返回，不在主会话中重写 Memory。
- AC-2：投影成功后原子激活新记忆点，保留当前点和一个回滚点；更老的可重建 checkpoint 进入清理队列。
- AC-3：手工维护命令只用于修复、离线维护或明确操作，不要求 AI 判断何时压缩。

### `REQ-PKI-007` 确定性人类文档 HTML

- 优先级：P0。
- 系统必须提供命令，从登记的 `docs` 人类文档构建离线静态 HTML；根索引决定导航和可见性。
- AC-1：相同 Git Commit、文档内容、生成器版本和参数生成相同页面集合、导航和内容 Hash。
- AC-2：构建前校验链接、唯一 Doc ID、中文名称、Owner、版本和禁止文件类型；失败时不发布部分站点。
- AC-3：输出进入 `.factory/pm/generated/docs/` 或显式发布目录，不反向写入正式事实；页面显示来源 Commit、生成时间、生成器版本和 Manifest Hash。

### `REQ-PKI-008` 统一命令面与无 AI 快路径

- 优先级：P1。
- 至少提供 `index refresh|check|rebuild`、`project status --format text|html`、`docs build|check`、`factory maintain --dry-run|apply` 四类确定性动作。
- AC-1：命令具有固定参数、退出码、JSON receipt 和人类摘要，输入不足时失败关闭，不向 AI 提问补值。
- AC-2：固定查询和维护动作不创建产品 TaskCard、不改变产品完成率；异步投影和维护任务登记为系统侧任务。

## 4. 非功能需求

| ID | 要求 | 指标 | 验证 |
|---|---|---|---|
| `NFR-PKI-001` | 会话恢复预算 | 当前记忆点不超过 8 KiB；兼容恢复不超过 1,000 ms | 0/1/50/200 事件夹具与超限负例 |
| `NFR-PKI-002` | 项目状态响应 | 热查询 P95 不超过 1,000 ms；独立 HTML 不超过 2,000 ms | 冻结性能夹具 |
| `NFR-PKI-003` | 增量索引 | 单文件变化不全量解析未变来源；10,000 Artifact 下 P95 不超过 500 ms | profiler 与 source-hash 断言 |
| `NFR-PKI-004` | 可重建性 | 空 SQLite 重建后节点、边、快照 Hash 与基线一致 | cold rebuild 测试 |
| `NFR-PKI-005` | 有界存储 | cache/generated 不超过配置容量和 TTL；无未登记无限增长目录 | 清理与长周期模拟 |
| `NFR-PKI-006` | 安全 | 路径穿越、符号链接越界、密钥进入索引/HTML/Memory 的成功次数为 0 | 攻击测试与 secret scan |
| `NFR-PKI-007` | 一致性 | 读者只能观察完整旧/新快照；跨格式字段漂移为 0 | crash、并发和逐字段对账测试 |

## 5. 命令与事实流

```text
正式 docs / WorkItem ledger / Memory / source / tests / Git
        -> registered source scanners
        -> ProjectKnowledgeIndex SQLite transaction
        -> validated immutable snapshot
        -> fixed text / project HTML / docs HTML / context read plan
```

## 6. `.factory` 保留与压缩结论

压缩不是“会话中每隔 N 分钟运行”。正确策略是：

1. 权威事件提交后按阈值自动登记隔离 Memory/Index/Maintenance 系统任务。
2. Task、Gate、阶段关闭和会话交接是强触发点。
3. 活动会话只读当前记忆点并检查 freshness；不得同步执行重压缩。
4. 可由系统计划任务周期执行 `factory maintain` 作为漏触发兜底，但没有定时器时系统仍必须正确。
5. 维护命令支持 `--dry-run`，只有 `--apply` 才执行已登记范围内的删除和压缩。

## 7. 影响分析

- 需求：增量修订现有 Project Control、Artifact、Memory 和文档治理需求，不新增同义 Workflow。
- 设计：必须重新基线信息架构、SQLite schema、source registry、Memory checkpoint、清理状态机、CLI/API 和两个 HTML renderer。
- 实现：复用现有 `project_control`、`system_tasks` 和 SQLite 原子任务能力；新增知识索引、文档构建和维护纵向切片。
- 文档：机器 Catalog/Manifest 必须从 `docs` 人类层迁出；迁移前保持现状并由正式发布事务原子切换。
- 当前候选：`TASK-IMPLEMENT-002-R001` 不纳入本次写集，不复用其实现资格证明本需求已经完成。

## 8. 风险

- 把 SQLite 误当事实源会造成 Git/文档/ledger 与数据库冲突。
- 索引所有正文可能泄露秘密或膨胀数据库；只索引允许字段，FTS 是可删 cache。
- 清理器路径或分类错误可能删除审计事实；清理必须由登记路径、realpath 边界和 legal hold 三重约束。
- HTML 构建若重新查询事实会造成同一页面内快照漂移；renderer 只能消费一个已验证 DTO/快照。
- 强制 50 事件/256 KiB 是默认触发阈值，需要性能测试后才允许调整。

## 9. Gate

本 R001 候选尚未批准。独立需求评审通过后，必须由 `uroborus` 审阅精确候选 Hash、默认 TTL/容量/压缩阈值、正式文档迁移影响和实现范围。批准前不得融入正式 PRD、迁移 `docs`、编制正式设计候选或写产品代码。

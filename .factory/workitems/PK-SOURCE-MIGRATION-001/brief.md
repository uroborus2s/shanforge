# PRD 单一需求事实源迁移

## 工作项

- 工作项：`PK-SOURCE-MIGRATION-001`
- 场景：`change_requirement`
- 状态：`human_approved_for_implementation`
- 人工批准来源：2026-07-23 当前会话“现在按照这个方案落地实施吧”
- 原需求：`REQ-PKI-001..016`、`NFR-PKI-001..011`
- 原候选：`REQ-CHANGE-PROJECT-KNOWLEDGE-001.contract.R009.json`

## 目标

把已经批准的项目知识需求完整原位写入 `docs/04-product/prd.md`，由固定 Markdown 提取器生成需求、验收标准、语义定位器和 SQLite 关系投影；R009 退出当前来源，只保留历史候选身份。

## 验收

- PRD 当前正文包含 16 条功能需求、64 条验收标准和 11 条非功能需求，均有稳定章节 ID。
- SQLite 中 27 条需求的 `source_section_key` 全部非空，64 条验收标准均有明确状态和父需求。
- 当前需求与验收实体的主要来源全部是 `docs/04-product/prd.md`。
- R009 requirement contract 不再登记为当前索引来源，删除 SQLite 后仍可从正式来源重建。
- 冻结 R009 contract SHA-256 必须保持 `53923f55c2bcc16bce6ad60ed1045c671dd490b6733885725641fe39e6859977`，final manifest SHA-256 必须保持 `8be9d829ea2a895eae043eaf054914cb03b7457a43d51c142cc4ad7f41f577ae`，PM 137 字段 map SHA-256 必须保持 `17af8c254017bc60eb44e73b8e61322bc57eb577ffa6baa2711f100d48251055`。
- PRD 投影必须与冻结 R009 的 ID、标题、优先级、规范语句顺序、AC ID/顺序/正文、NFR metric/verification 逐字段等价；中文批准状态规范化为 `approved`。
- 既有数据库从 R009 owner warm refresh 到 PRD owner 的 after-image 必须与同一来源集的 cold rebuild 等价。
- 需求列表不把验收标准当顶层需求；按中文分类展示，并可进入完整详情。
- 任务和需求关系使用可点击的独立详情页链接。
- 文档详情展示安全渲染的完整 Markdown 正文，不只显示目录。
- 技术快照信息默认折叠，不干扰业务阅读。

## 边界

- 不修改冻结的 R009 候选字节。
- 只从 `SRC-WORKITEM-JSON.include` 精确移除 `REQ-CHANGE-PROJECT-KNOWLEDGE-001.contract.R009.json`；保留 final manifest、R014 contract/release manifest 和 R009 PM field map 的当前登记。
- 不新增 `docs` 人类文档。
- 不提交 SQLite、HTML、FTS 或 cache。
- 不修改与项目知识索引无关的现有工作区改动。
- 不执行 Push、PR、Merge 或部署。

## Baseline 影响

- 需求 baseline：PATCH，只补齐 `v4.1.0` 已批准需求的正式正文与可解析结构，不改变需求语义。
- 数据 baseline：不新增表；补齐 `pk_requirement.source_section_key` 的既有合同。
- API baseline：CLI 命令面不变。
- UI baseline：修正只读站点的信息组织、链接和文档阅读能力。
- 领域模块：`runtime.project_knowledge` 负责确定性提取和安全渲染；`settings.project_knowledge` 负责 SQLite 投影和本地正式文档装配。

## Markdown 展示安全合同

- 允许：标题、段落、无序/有序列表、表格、引用、围栏代码、行内代码和粗体。
- 禁止主动解释：raw HTML、Markdown link、图片、内联事件属性和任意 URL；这些内容只能以转义后的普通文本展示。
- 正文只读取 registry 已登记、位于真实 `docs/` 根内、不是符号链接、大小不超过 2 MiB 且与 SQLite artifact Hash 相同的单次读取 bytes。
- `shared-restricted` 只装配 `access_class=public` 的正文；其他正文不得进入 renderer DTO。

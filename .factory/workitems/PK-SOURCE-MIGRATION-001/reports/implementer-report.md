# PK-SOURCE-MIGRATION-001 实施者报告

## 结果

已把当前项目知识需求从冻结 R009 候选迁移到正式 PRD 稳定章节。SQLite 继续作为
可删除重建的投影，R009 requirement contract 已从当前 source registry 精确移除，
PM 字段映射、R014 合同和最终发布清单继续保留。

只读站点现在按中文能力分类展示需求，AC 嵌套于所属需求；需求、任务、代码和测试
关系生成真实深链；文档详情显示经来源、Hash、大小、文件类型和权限校验的完整
Markdown 正文；技术快照默认折叠。任务编号是 canonical entity ID，Ledger 提供状态，
task brief 提供中文标题。

## 主要实现

- PRD `v4.1.1`：16 REQ、64 AC、11 NFR 及能力地图。
- Markdown extractor：稳定 REQ/NFR/AC、task brief WorkItem 和 locator。
- SQLite：`source_section_key`、跨 ledger 最新状态、低权威中文标题补充。
- 关系声明：九个任务到 REQ/NFR 的 88 条强 `IMPLEMENTS` 边。
- 站点：需求分类、双向关系深链、安全正文、AC 锚点、折叠快照。
- 发布器：正确校验带 fragment 的内部链接并拒绝危险 scheme。
- 设计：原位更新数据设计和前端设计，未新增平行正式设计文档。

## 边界

- SQLite、HTML 与 cache 未进入 Git 提交范围。
- 冻结 R009 三个核对文件未修改。
- 未执行 Push、PR、Merge 或部署。
- 全仓三项范围外 Skill 合同失败未修改，详见验证证据。

## Post-delivery UI follow-up

- 业务详情不再展示 locator、Hash 和内部 document ID。
- 任务详情把追踪分为关联需求、相关设计、代码测试与交付。
- 需求只来自 outgoing strong Task→Requirement；设计只通过
  `Task → Requirement ← incoming strong SATISFIES Design` 推导。
- `FLOW-TASK-011` 已登记到 `REQ-PKI-008`，可继续进入
  `DESIGN-FRONTEND-001`；弱关系、错误关系类型和直接 Task→Design 均有拒绝测试。

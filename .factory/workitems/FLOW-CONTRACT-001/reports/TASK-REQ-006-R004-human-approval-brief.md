# TASK-REQ-006 R004 人工批准说明

## 建议结论

建议批准 R001–R004 共同组成的需求候选。独立复审结果为 `approved / 96 / C0-I0-M0`。

批准后，正式需求、设计和实现遵循以下统一原则：

1. `docs/` 只保存人类查看的当前有效文档；按项目画像创建最小必要集合，没有适用内容就不创建。
2. 正式文档默认原位增补、修正和修复，文档内版本历史与 Git 保存历史；候选和评审过程只放 `.factory/workitems/`。
3. `requirements-matrix.md` 默认不作为人工维护的第二事实源；需求—设计—代码—测试—任务关系进入可重建 SQLite，并按需生成临时人类视图。只有项目画像明确要求长期的人类合规基线时，才保留一份持续原位更新的正式追踪文档。
4. `ai-sdlc-catalog.manifest.json`、`ai-sdlc-catalog.source.json` 属于机器 Artifact，批准后的迁移设计必须将其移出 `docs/05-design/`，不得继续混在人类设计文档中。
5. `.factory/pm` 不再保存独立事实；进度与文档 HTML 统一进入 `.factory/cache/views/.../current.html`。
6. 每个稳定 `view + authorization + normalized query` scope 只有一个 `current.html`。代码比较事实快照、源、renderer、template、schema、查询与文件 Hash；未变化直接返回，变化时原子刷新同一路径。
7. 每次返回缓存 HTML 前必须重新证明当前授权有效；撤销、未知或检查失败都 fail-closed，不能在异步清理窗口返回旧页面。
8. 每次会话默认只读一个最多 8 KiB 的当前记忆点；更多内容必须由 SQLite 索引给出定向路径、章节与预算。
9. Memory 压缩以 Task/Gate/阶段关闭、落后 50 个事件、未压缩 256 KiB、会话交接等事件或阈值触发，由隔离任务完成；活动会话不定时重压缩。
10. `.factory/cache/` 默认上限 256 MiB、TTL 24 小时；生成视图每 scope 只留 1 份、最长 7 天，维护命令只清理已登记的可重建内容。
11. AI 只选择 Skill、命令和参数；索引、freshness、状态计算、HTML 组装、清理与 receipt 全部由代码确定性完成。

## 批准后的动作边界

批准只授权本需求进入正式 PRD 的原位增补、适用设计 Owner 文档的重基线和后续实现计划。不会自动提交 Git、发布或部署；不会把现有 `TASK-IMPLEMENT-002-R001` 混入本候选。

## 精确候选

- Candidate root SHA-256：`5ab03160ca91851b82ef92cb3fbc37e7f63c0d9d7b66ab99879900ef59ff94c5`
- Manifest SHA-256：`8338d35e294245cbf41b8852c0e49d2a70391de5068fc3e7459eb30c22a1d160`
- Manifest：`.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-REQ-006-R004-final-candidate-manifest.json`

人工计划批准必须绑定上述 Manifest SHA-256；内容 Hash 变化后，旧批准自动失效。

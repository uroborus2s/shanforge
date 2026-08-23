# PM-DASHBOARD-005-T01 第七轮实现报告

## 完成内容

1. `Work Breakdown` 改为 `id / parent_id / title / status` 四列表；父子关系不再依赖
   Markdown 标题深度。
2. 解析器先收集全部节点，再拒绝重复 ID、孤儿、自引用和循环，按表格行顺序派生
   `children` 与任意深度 `depth`。
3. EAD 原 32 个节点已原样迁移；5 个根节点和 27 个子节点的标题、状态保持不变。
4. 32 个节点各自生成 `stages/<NODE-ID>.html`；节点页只列直接子节点，单独提供匹配
   TaskCard 的任务与每日进展入口。
5. 当前工作页用“产品主线 + 一个并行工作项”作为统一负责人范围；上方只留范围摘要，
   不再复制任务卡。
6. 六种状态只汇总一次；两个业务组只渲染三个非空状态段，3 张任务卡均唯一。
7. 需求组标题进入需求详情；工作项组有计划进入计划页，无计划进入当前任务。

## 未增加内容

- 未增加 JavaScript、数据库、前端框架、第三方依赖、`order` 字段或第二份路线事实。
- 未改变 EAD T03 客户确认 Gate，未启动 T04/T05。
- 未修改其他工作项事实。
- 未提交、Push、创建 PR、Merge、部署或关闭任务。

## 验证

- 路线 Red：`6 failed`，命中标题推断、缺少图校验和非法路线仍成功三个旧行为。
- 路线 Green：`2 passed, 4 subtests passed`。
- 聚焦快照：`10 passed, 4 subtests passed`。
- Ruff check / format check：通过。
- 真实快照：32 节点、5 根；第二次生成相同 generation ID 且 `cache_hit=true`。
- 站内 `.html` 链接：`31,607 checked / 0 missing`。
- 浏览器：1440×900 与 390×844 均无横向溢出，控制台错误 0。
- 全仓：`219 passed / 7 failed / 4 subtests passed`；7 个失败 node ID 与修改前完全一致。
- 详细证据：
  `evidence/PM-DASHBOARD-005-T01-round-7-verification.md`。

## 当前 Gate

独立任务评审为 `approved / 99 / C0-I0-M0`。当前状态为
`approved_pending_human_ui_acceptance`；下一步是用户检查真实桌面和移动页面。
用户 UI 验收前不得提交或关闭。

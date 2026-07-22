# 项目状态入口 Skill 含义保留清单

**任务：** `TASK-IMPLEMENT-003-P001-T06`
**状态：** `ready_for_review`
**用途：** 在修改 `using-shanforge` 与 `project-memory` 前固定原有控制语义，防止从旧 PM 模板迁移到项目知识 CLI 时扩大职责或丢失约束。

## 保留项

| 类别 | 必须保留的含义 |
|---|---|
| 目标 | 用户要求查看项目状态、进度、PM 看板或项目管理页面时，提供确定性的只读项目视图。 |
| 触发 | 只在项目状态查询场景读取 PM 渲染 reference；普通回答和轻量分析不进入项目化流程。 |
| 输入 | 输入来自登记的正式文档、work item ledger、代码、测试、Git 与受控 memory，不接受 AI 临时自由聚合为事实。 |
| 步骤 | AI 只识别用户要看的范围；固定代码刷新或复用索引、生成静态站点并返回 receipt；详情查询使用稳定实体 ID 和 locator。 |
| 输出 | 返回最后有效的只读 HTML 入口、是否 cache hit、代次和诊断；AI 可另行解释，但不能改写代码事实。 |
| 禁止 | AI 不计算完成率、状态、风险、权限或上线结论；不拼装 HTML；不把 SQLite、HTML 或 cache 当作正式事实。 |
| 例外 | 输入无变化时不得重复构建；索引损坏、定位不唯一、权限不明或来源失败时必须失败关闭。 |
| 验收 | 生成器和 CLI 有自动测试；站点支持独立详情页与返回按钮、键盘、打印和多视口；skill 修改须独立评审。 |
| 风险 | 不能保留旧 `.factory/pm` 与新 SQLite 投影两套状态模型；不能让展示页反向更新事实；不能让查看动作提交 Git。 |
| handoff | skill 作者只推进到 `ready_for_review`；整体任务交给独立 Spec/Quality/UI reviewer。 |
| 临时文档 | 临时草稿、验证、review 和报告仍只进入 work item 的 `drafts/evidence/reviews/reports`；删除旧 PM generated 目的地不改变分类规则。 |

## 明确替换项

- 旧 `.factory/pm/` 事实目录替换为“Git 中的正式事实 + 可重建 SQLite 当前投影”。
- 旧 `status-dashboard-template.html` 单页模板替换为固定 Python renderer 生成的多页面静态站点。
- 旧 `.factory/pm/generated/status-dashboard.html` 替换为 `.factory/cache/site/current/index.html`。
- 运行时读取 Excel 样例或模板 slot 的描述删除；十个管理要素已固化为 137 字段映射、10 张 PM 投影表和固定页面。
- 会话内九步抽象调用描述收敛为一个可执行 CLI；查询细节通过 `find/show/trace/context` 定向获取。

## 自检结论

原有目标、触发、只读边界、失败语义、权限边界和独立评审门均保留；旧的重复实现和已退役路径被移除。作者状态只能为 `ready_for_review`。

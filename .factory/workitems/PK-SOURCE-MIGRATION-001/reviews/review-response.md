# 计划评审响应

本轮对 5 个 Important Finding 全部接受并补强计划，不改变用户批准的产品方向：

- 单一事实源迁移增加冻结 Hash 和逐字段语义等价门。
- 数据迁移增加 warm/cold 等价与逐项章节、验收映射门。
- 任务关系增加显式 Task→REQ/NFR 追踪矩阵。
- Markdown 展示改为白名单子集和单次 bytes Hash 校验，链接、图片与 raw HTML不解释。
- renderer 升级版本并同步现有 data/frontend design。

状态：`ready_for_same_reviewer_rereview`。

## Post-delivery UI follow-up 整改回复

- UI-I1 已修复：追踪推导显式校验方向和强度；相关设计还必须是 Requirement 侧
  incoming strong `SATISFIES`。
- 已删除直接 Task→Design 旁路。
- 已增加 weak Task→Requirement、非 `SATISFIES` Design、直接 Task→Design 三类负例，
  均不能进入人类页面。
- 渲染器升级为 `ProjectSiteRenderer/v10`，防止旧 v9 页面被缓存复用。

状态：`ready_for_same_reviewer_rereview`。

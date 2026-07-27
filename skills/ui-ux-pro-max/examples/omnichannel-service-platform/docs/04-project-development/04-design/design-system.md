# 设计系统

## 版本信息

| 文档编号 | 版本 | 状态 | 负责人 | 更新日期 |
|---|---|---|---|---|
| `DOC-DS-001` | `0.1.2` | 样例 | 设计系统负责人 | 2026-07-24 |

## 版本历史

| 版本 | 修改内容 | 日期 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `0.1.2` | 固定后台组件、图标与动效技术基线 | 2026-07-24 | AI 示例作者 | 待审核 | 待批准 |
| `0.1.1` | 增加管理后台 shadcn/ui 组件与 Token 映射 | 2026-07-24 | AI 示例作者 | 待审核 | 待批准 |
| `0.1.0` | 建立语义 Token 与核心组件 | 2026-07-24 | AI 示例作者 | 待审核 | 待批准 |

机器 Token 见 [design-tokens.json](contracts/design-tokens.json)，Penpot Token Set 为 `Yuexiang/Semantic`。

## Token 层次

1. 基础值：品牌色、灰阶、间距、圆角和字体。
2. 语义值：`action.primary`、`feedback.success`、`content.secondary`。
3. 平台映射：pt、dp、rpx/逻辑尺寸、CSS 变量。

不在业务页面直接引用“紫色 500”；引用 `color.action.primary`，主题改变时语义保持。

## 核心组件

| 组件 | 变体/状态 | 内容规则 |
|---|---|---|
| Button | primary、secondary、neutral、danger；default/pressed/disabled/loading | 动词开头；加载时保留宽度 |
| Field | default、focus、error、disabled | label 常驻；错误说明原因和恢复 |
| ServiceCard | list、featured；loading/available/unavailable | 标题、时长、评分、价格起点 |
| StatusBadge | paid、pending、in_service、refunding、failed | 文字与颜色同时表达 |
| OrderTimeline | complete、current、future、error | 显示事件名称和时间 |
| DataTable | loading、empty、error、partial | 列标题中文清楚，详情用独立页面 |

## 管理后台 shadcn/ui 映射

| 设计角色 | shadcn/ui 实现 | 约束 |
|---|---|---|
| 后台外壳与导航 | `Sidebar`、`Breadcrumb` | 当前路由清楚；窄屏允许收起 |
| 指标与业务摘要 | `Card` | 标题、数值、口径和时间范围同时可见 |
| 列表与分页 | `Table` + Data Table | 使用 TanStack React Table 组合排序、筛选和分页；详情进入独立路由 |
| 筛选与编辑表单 | `FieldGroup`、`Field`、`Input`、`Select`、`Combobox` | 标签常驻，错误和帮助文本与控件关联 |
| 业务状态 | `Badge` | 中文状态与语义颜色同时表达 |
| 加载、空和错误 | `Skeleton`、`Empty`、`Alert` | 不用空白页或内部错误码代替解释 |
| 高风险确认 | `AlertDialog` | 退款、取消、权限变更说明影响并要求明确确认 |
| 轻量反馈 | `Sonner` | 只补充操作结果，不代替页面内错误 |

主业务详情使用独立页面和返回按钮。`Sheet`、`Drawer` 只用于筛选或补充信息，不承载订单、服务、权限等主详情。

管理后台固定使用 shadcn/ui Radix primitive、`new-york` 风格、语义 CSS 变量和 Lucide 图标。真实工程在 `components.json` 固定这些值；业务组件禁止直接写原始色值，也不得混用另一套通用组件或图标库。

## 内容

- 标题说清业务对象，例如“确认预约”，不用“下一步”作为页面标题。
- 错误信息包含发生了什么、数据是否保存、用户现在能做什么。
- 内部 UUID 和英文状态可作为辅助信息，不能替代中文业务名称。

## 动效

- 150–250ms 的状态反馈优先。
- 导航转场表达层级，支付结果不使用无意义庆祝动画阻塞操作。
- hover、focus、颜色和简单展开使用 CSS；共享布局、可中断编排或手势只使用 `motion` 包的 `motion/react`。
- 不引入 `framer-motion`、GSAP、Anime.js、React Spring 或第二套通用动效库。
- reduced-motion 下删除大幅缩放、视差和自动循环。

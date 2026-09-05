# 管理后台设计

## 适用范围

React 管理后台、运营平台、配置中心、数据后台和内部工具。通用 Web 适配、语义和无障碍要求同时遵循 [Web 设计](web.md)。

## 固定技术基线

新管理后台默认使用以下组合，不在页面或任务级重新选型：

| 范围 | 固定选择 |
|---|---|
| UI 框架 | React + TypeScript |
| 组件系统 | shadcn/ui |
| 组件 primitive | Radix |
| shadcn 风格 | `new-york` |
| 主题 | Tailwind CSS 语义变量，`cssVariables: true`，中性基础色 |
| 图标 | Lucide；React 包为 `lucide-react`，`components.json` 使用 `iconLibrary: "lucide"` |
| 简单动效 | CSS transition/keyframes 或 shadcn/ui 已生成的组件动画 |
| 复杂 React 动效 | Motion；安装包为 `motion`，从 `motion/react` 导入 |

真实工程创建后，把 shadcn 配置写入并提交 `components.json`，用项目包管理器执行 shadcn CLI。初始化前固定 primitive、style、基础色、CSS variables 和图标库；这些值不得由单个页面临时改变。

已有工程以现存 `components.json` 和设计系统为事实源，不强行迁移。偏离上述新项目基线必须在项目设计决定中写清原因、影响范围、迁移和验收；不得同时维护两套通用组件、图标或动效运行时。

## 组件映射

| 设计角色 | shadcn/ui 组合 |
|---|---|
| 应用外壳 | `Sidebar`、`Breadcrumb`、`DropdownMenu` |
| 指标与摘要 | `Card`、`Badge` |
| 列表 | `Table` + Data Table；复杂排序、筛选和分页组合 TanStack React Table |
| 表单 | `FieldGroup`、`Field`、`Input`、`Select`、`Combobox`、`DatePicker` |
| 加载、空、错误 | `Skeleton`、`Empty`、`Alert` |
| 高风险确认 | `AlertDialog` |
| 轻量结果反馈 | `Sonner`；不代替字段或页面错误 |

订单、服务、用户、权限等主业务详情使用独立 URL 页面和返回按钮。`Sheet`、`Drawer` 只承载筛选或补充信息，不承载主详情。筛选、分页和排序状态写入 URL，保证刷新、返回和分享内部链接后可恢复。

## 图标规则

- 只从 `lucide-react` 导入通用界面图标；禁止同项目混用 Tabler、Heroicons、Phosphor 或另一套通用图标库。
- shadcn/ui 组件内部遵循组件默认图标尺寸，不额外添加尺寸类；图标放在按钮前后时使用组件约定的 `data-icon`。
- 图标不能代替中文业务名称。纯图标按钮必须有可访问名称，并在需要解释时提供 Tooltip。
- 品牌 Logo 不属于通用图标。Lucide 缺少不可替代的行业专用符号时，由设计系统登记自有 SVG；不能因此引入另一整套图标库。
- 不使用 emoji 充当生产界面操作图标。

## 动效规则

按以下顺序选择，命中即停止：

1. 没有明确状态、层级、反馈或连续性价值：不做动画。
2. hover、focus、颜色、透明度、小范围展开收起：使用 CSS。
3. 共享布局、可中断编排、拖拽、手势或复杂进退场：使用 `motion` / `motion/react`。
4. 品牌矢量动画只有在已批准资产和性能预算下使用 Lottie/Rive；它们属于 UI 项目的 UI 资产，由本 skill 按资源清单和许可管理。仅不属于 UI 项目的独立美术或游戏资源包才交给 `art-asset-pipeline`。

新管理后台禁止另行引入 `framer-motion`、GSAP、Anime.js、React Spring 或第二套通用动效库。确有 Motion 无法满足的需求时，先形成设计与技术决定，再修改项目级基线；不能由页面实现者自行添加。

所有动效使用语义 motion token，必须可中断并支持 `prefers-reduced-motion`。动画失败或被关闭时，业务状态、焦点和操作路径仍完整。

## 交付与验收

- 设计交付写清组件映射、图标名称、动效载体和 reduced-motion 替代，不只给截图。
- 实现前读取 `components.json`、`package.json` 和已有组件目录；组件新增、更新和覆盖交给 `shadcn` skill。
- 验收至少覆盖键盘、焦点、屏幕阅读器关键路径、200% 文本、400% 页面缩放、窄屏降级、加载/空/错误/无权限和 reduced motion。
- 发现非 Lucide 通用图标、第二套组件系统或第二套动效运行时时，除非存在已批准项目决定，否则视为设计系统违例。

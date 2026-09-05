# 跨平台映射

## 原则

跨平台追求共同产品语义和可维护 token，不追求每个平台完全相同。共享越靠近业务语义，平台差异越靠近导航、输入、窗口、系统能力和视觉细节。

## 三层模型

### 产品语义层

- 用户任务、内容模型、权限、状态、主次操作、错误和恢复。
- 语义 token：品牌、surface、content、action、feedback、focus、motion intent。
- 组件契约：角色、数据、状态、事件和内容规则。

### 平台映射层

- 导航：浏览器历史、页面栈、系统 Back、窗口/文档、tab/rail/sidebar。
- 输入：触控、手势、键盘、鼠标、指针、stylus、屏幕阅读器。
- 呈现：sheet、dialog、popover、menu、toast/snackbar、system notification。
- 系统能力：权限、分享、支付、文件、深链、通知、窗口和后台。

### 实现层

- Web、SwiftUI/UIKit、Compose/View、Flutter、React Native、Taro、Avalonia 等组件和 API。
- 平台 token、尺寸单位、图标、字体、动效运行时和资产格式。
- 构建、性能、测试和发布约束。

## 必交平台矩阵

| 维度 | 共同语义 | Web | 小程序 | Apple | Android | Desktop |
|---|---|---|---|---|---|---|
| 导航 | 层级、返回、深链 | history/route | 页面栈/tab/宿主入口 | stack/tab/split/window | back/up/adaptive nav | window/document/menu |
| 输入 | 操作意图 | 键鼠/触控 | 触控/宿主能力 | 触控/指针/键盘 | 触控/键鼠/stylus | 键鼠/快捷键/拖放 |
| 适配 | 内容优先级 | viewport/container | 宿主窗口/安全区 | size class/window | window size/fold | resizable window/DPI |
| 浮层 | 临时任务 | dialog/popover | 宿主/原生限制 | sheet/popover/alert | dialog/sheet/snackbar | dialog/flyout/context menu |
| 动效 | 因果、反馈、连续性 | CSS/WAAPI/库 | 宿主/CSS/Canvas | native transition/spring | native transition/spring | composition/storyboard/native |

矩阵中的控件名只是设计映射起点。执行时核对当前平台规范和框架能力。

## 共享与分叉规则

- 可共享：业务流、内容、语义 token、组件状态、文案原则、无障碍意图、动效意图和分析事件。
- 通常分叉：导航容器、返回行为、权限、菜单、窗口、系统控件、手势、键盘快捷键和发布限制。
- 需要证据后决定：图标、字体、间距密度、表格、复杂编辑、图表交互和品牌动效。
- 不使用“平台兼容层”掩盖真实缺失；能力不可用时提供明确降级或缩小支持范围。

## 组件与动效契约

- 共享组件写角色、数据、状态、事件和内容规则；各端分别登记原生控件、导航与输入映射，不以相同像素稿替代映射。
- 动效只表达反馈、层级或连续性；每端提供可中断和 reduced-motion 静态/淡入降级。平台不支持时保留业务反馈，不模拟无效手势。

## 验收

- 每个平台有代表性设备、输入方式、主题、语言和系统版本。
- 共同任务的结果一致，过程允许尊重平台习惯。
- 一个平台通过不外推其他平台；分别保留证据。
- 共享组件的无障碍、文本扩展和动效降级在每个实现端验证。

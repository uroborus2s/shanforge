# 动效系统

## 目录

- 动效意图
- 动效 token
- 交付字段
- 技术载体
- 无障碍与降级
- 性能与验证

## 动效意图

只在以下至少一项成立时添加动效：

- 反馈：确认输入、完成、错误、选择或模式变化。
- 连续性：解释元素从哪里来、到哪里去、与前一状态的关系。
- 层级：表达进入、返回、展开、收起、模态或导航深度。
- 引导：把注意力带到刚发生且需要处理的变化。
- 品牌：在不拖慢核心任务的前提下形成有限、可识别的节奏。

纯装饰、无法解释的循环、遮掩等待、强迫观看和抢占操作的动效应删除。

## 动效 token

以下是原型起点，不是跨平台硬标准；平台原生值和实测反馈优先。

| Token | 起始范围 | 用途 |
|---|---:|---|
| instant | 80–120ms | hover、pressed、短状态反馈 |
| fast | 120–180ms | 小元素进入/退出、图标切换 |
| standard | 180–280ms | 组件展开、局部页面变化 |
| emphasized | 280–450ms | 大容器、共享元素、品牌强调 |

- 退出通常短于进入，但不能快到用户无法理解状态变化。
- 手势和 spring 优先记录质量、刚度、阻尼、初速或框架等价参数，不把所有运动压成一个 duration。
- 统一使用语义 token，例如 `motion-feedback-fast`、`motion-navigation-enter`，避免组件内散落魔法数字。

## 交付字段

每条动效至少记录：

| 字段 | 要求 |
|---|---|
| ID/名称 | 可映射到页面、组件或用户流 |
| 意图 | 反馈、连续性、层级、引导或品牌 |
| 触发 | 用户、系统、数据或导航事件 |
| 起止状态 | 布局、透明度、变换、颜色、内容和焦点 |
| 时序 | duration/spring、delay、stagger、easing |
| 中断 | 取消、反向、快速重复、手势释放和竞态 |
| 无障碍 | reduced-motion、静态/淡入替代和屏幕阅读器反馈 |
| 载体 | native、CSS、Canvas、Lottie、Rive、视频等 |
| 预算 | 包体、解码、内存、帧率、主线程和电量 |
| 验收 | 设备、场景、测量和证据路径 |

## 技术载体

| 场景 | 首选 | 何时升级 |
|---|---|---|
| 简单 Web 状态 | CSS transition/keyframes、Web Animations | 编排复杂或需手势/共享布局时再用 Motion/GSAP 等 |
| React 管理后台 | 简单状态使用 CSS；复杂布局、编排和手势只使用 Motion（`motion/react`） | 不升级到第二套通用动效库；例外遵循 [管理后台设计](admin-web.md) |
| Web/React 手势与布局 | 平台/框架稳定的 motion 库 | 需要时间轴、滚动编排或复杂矢量时升级 |
| iOS/macOS | SwiftUI/UIKit/AppKit/Core Animation | 复杂矢量或品牌状态机才评估 Lottie/Rive |
| Android | Compose animation/transition、MotionLayout/Animator | 复杂矢量或品牌状态机才评估 Lottie/Rive |
| Flutter | framework animation、Hero、implicit/explicit animation | 复杂资产按运行时与包体评估 |
| React Native | Animated/Reanimated/平台导航转场 | 复杂资产按桥接、线程和设备能力评估 |
| 小程序 | 宿主原生/CSS transform+opacity | Canvas/Lottie 前先验证基础库、包体与低端机 |
| Windows/跨桌面 | WinUI Composition、WPF Storyboard、Avalonia/JavaFX 原生能力 | 仅在原生能力不足且维护收益成立时引入额外运行时 |
| 跨端矢量动画 | Lottie/dotLottie | 适合时间轴动画；先核对各端支持特性和资产体积 |
| 交互状态机 | Rive 或平台等价状态机 | 只在实时输入和多状态复用能抵消运行时成本时使用 |

不要因为设计工具能导出某格式，就假设所有目标端渲染一致。分别验证遮罩、渐变、文本、混合模式、图片、裁切、颜色覆盖和暗色主题。

## 无障碍与降级

- reduced motion 不等于简单删除所有反馈。保留状态变化、焦点、进度和完成信息，减少大幅位移、缩放、视差、闪烁和自动循环。
- 自动播放、持续超过数秒或可能分散注意的动画提供暂停、停止或隐藏。
- 不使用闪烁、快速对比变化或不可控运动制造风险。
- 动效失败、资源未加载或系统关闭动画时，界面仍处于完整可操作状态。
- 屏幕阅读器需要语义反馈时使用 live region、announcement 或平台等价能力，不依赖视觉动画传达结果。

## 性能与验证

- 动画不阻塞输入，必须可中断；快速连续操作不能产生堆积时间线或错误终态。
- 优先 transform/opacity/合成层；谨慎使用大面积 blur、shadow、mask、粒子、视频和布局属性动画。
- 60Hz 单帧理论预算约 16.7ms，120Hz 约 8.3ms；实际预算还要给输入、布局、绘制和系统留余量。
- 在目标低端设备、典型设备和高刷新率设备测量。模拟器、录屏和设计工具预览不能替代运行时证据。
- 记录掉帧、长任务、GPU/CPU、内存、包体、首帧、解码和电量中任务相关指标；不要只凭“看起来顺滑”。

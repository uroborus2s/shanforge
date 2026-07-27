# 技术选型

## 版本信息

| 文档编号 | 版本 | 状态 | 负责人 | 更新日期 |
|---|---|---|---|---|
| `DOC-TECH-001` | `0.1.2` | 样例 | 技术负责人 | 2026-07-24 |

## 版本历史

| 版本 | 修改内容 | 日期 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `0.1.2` | 固定后台 Lucide 图标与 Motion 动效基线 | 2026-07-24 | AI 示例作者 | 待审核 | 待批准 |
| `0.1.1` | 明确管理后台采用 shadcn/ui | 2026-07-24 | AI 示例作者 | 待审核 | 待批准 |
| `0.1.0` | 固定样例技术栈 | 2026-07-24 | AI 示例作者 | 待审核 | 待批准 |

| 范围 | 选型 | 选择原因 |
|---|---|---|
| iOS | Swift + SwiftUI | 使用系统导航、Dynamic Type、VoiceOver 和安全存储 |
| Android | Kotlin + Jetpack Compose | 支持自适应窗口、预测返回和 TalkBack 语义 |
| 微信小程序 | TypeScript + 微信原生能力 | 支付、订阅消息、页面栈和审核行为更可控 |
| 管理后台 | TypeScript + React + shadcn/ui（Radix / new-york）+ Lucide + Motion | 固定组件、图标和复杂动效实现，避免页面级重复选型 |
| 服务端 | Java + Spring Boot | 事务、契约校验、鉴权和可观测性成熟 |
| 数据 | PostgreSQL + Redis | PostgreSQL 保存事实；Redis 只做幂等、限流和短期缓存 |
| 契约 | OpenAPI 3.1 | 四端模型生成、契约测试和文档展示共用 |
| 设计 | Penpot + 语义 Token | 开放格式、组件与设计 Token 可审计 |

## 禁止

- 不共享一套像素 UI 强行覆盖四端。
- 不在没有真实后台工程时伪造 `components.json`；实现工程创建后以它作为 shadcn/ui CLI 配置事实源。
- 不混用第二套通用图标库或动效库；简单动效使用 CSS，复杂 React 动效只使用 `motion/react`。
- 不让 Redis、客户端缓存或支付 SDK 成为订单支付事实源。
- 不从 Penpot 自动生成未经评审的生产 UI 代码。
- 不为单个淡入效果引入整套动效运行时。

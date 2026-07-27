# 开发环境

## 版本信息

| 文档编号 | 版本 | 状态 | 读者 | 更新日期 |
|---|---|---|---|---|
| `DOC-DEV-SETUP-001` | `0.1.2` | 样例 | 开发者、测试人员 | 2026-07-24 |

## 版本历史

| 版本 | 修改内容 | 日期 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `0.1.2` | 固定后台 shadcn、Lucide 与 Motion 配置 | 2026-07-24 | AI 示例作者 | 待审核 | 待批准 |
| `0.1.1` | 增加管理后台 shadcn/ui 工程约束 | 2026-07-24 | AI 示例作者 | 待审核 | 待批准 |
| `0.1.0` | 定义样例工程边界 | 2026-07-24 | AI 示例作者 | 待审核 | 待批准 |

## 推荐工程

| 端 | 技术 |
|---|---|
| iOS | Swift、SwiftUI、系统 Keychain 与通知能力 |
| Android | Kotlin、Jetpack Compose、EncryptedSharedPreferences |
| 微信小程序 | TypeScript、微信原生能力或经验证的跨端框架 |
| 管理后台 | TypeScript、React、shadcn/ui（Radix / new-york）、Lucide、Motion、语义 HTML、响应式布局 |
| 服务端 | Java、Spring Boot、PostgreSQL、Redis、对象存储 |

## 本地依赖

- PostgreSQL：订单、服务、支付和审计事实。
- Redis：短期会话、幂等键和限流状态；不作为订单事实源。
- 支付沙箱：微信支付与聚合支付适配器。
- 通知沙箱：Push、短信和微信订阅消息。

## 环境配置原则

- 密钥只通过 Secret Manager 或本地未提交环境文件注入。
- 四端共享 OpenAPI 生成的模型，但不共享平台导航和权限实现。
- 管理后台工程创建时提交 `components.json`，固定 Radix、`new-york`、CSS variables 和 `iconLibrary: "lucide"`；先用 shadcn CLI `info` 和 `add --dry-run` 核对配置及变更，再按需添加组件。
- 普通状态动效使用 CSS；只有共享布局、复杂编排和手势引入 `motion` 并从 `motion/react` 导入。本设计样例不包含前端工程，因此不伪造配置或安装依赖。
- 本地模拟器用于快速检查；支付、权限、通知和小程序生命周期必须真机验证。

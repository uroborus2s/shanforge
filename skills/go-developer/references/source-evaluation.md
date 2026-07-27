# 来源评估

核对日期：2026-07-13。

## GitHub skill 候选

### `samber/cc-skills-golang`

- 仓库：https://github.com/samber/cc-skills-golang
- 许可：MIT。
- 核对时约 2.5k stars、103 commits、8 个 release，最新 release 为 `v1.7.0`（2026-07-02）。
- 提供原子化的 Go code style、database、error handling、observability、testing、project layout 等 skill，并公布有/无 skill 的 eval 汇总。
- 没有 Gin 或 GORM 专用 skill，也没有本项目要求的 Gin + GORM + Logrus + Consul 一体化交付契约。

结论：它是成熟的结构和 Go 工程规则参考，但不是可直接安装替代品。本 skill 不复制其正文，只采用精确触发、按需 references、版本意识和 eval/测试门的做法。

进一步核对其中的 `golang-design-patterns` 与 `golang-project-layout`：

- 可借鉴：模式只解决真实问题、优先最小模式、early return 保持主路径平直、小项目不过度分层、`pkg/` 只放真正公共 API。
- 不采用：构造函数默认 Functional Options、先询问或引入 DI 库等一刀切建议。当前参数和依赖简单时，普通构造函数与显式装配更符合 Ponytail。

### `Melkeydev/go-blueprint`

- 仓库：https://github.com/Melkeydev/go-blueprint
- 核对时约 8.9k stars、246 commits，支持 Gin 和多种数据库选项。
- 默认生成保持较小，Docker、CI、WebSocket、前端等能力按需启用。

结论：借鉴“默认最小、能力显式 opt-in”的模板策略；不引入其多框架、多数据库兼容面，也不把生成器选择项带入固定 Gin + GORM + Logrus + Consul 模板。

### `evrone/go-clean-template`

- 仓库：https://github.com/evrone/go-clean-template
- 核对时约 7.6k stars、590 commits，并提供 REST、gRPC、RabbitMQ、NATS 等多传输示例。
- 工程边界、测试与依赖方向有参考价值，但完整结构覆盖面远大于本 skill 的最小服务模板。

结论：只借鉴边界和测试思想，不复制其目录、传输组合和基础设施集合。

### 未选为主要依据的候选

- `affaan-m/everything-claude-code` 中的 `golang-patterns` 可作为社区补充，但其默认 Functional Options、接口和 DI 建议必须逐项核实，不能直接套用。
- `alex-guoba/gin-clean-template` 同时带入 Sentinel、Swagger、Viper、Air 等能力，且缺少稳定 release 信号，不适合作为 Ponytail 基线。

## Go 设计依据

- Go 官方 `Effective Go`：Go 不提供传统 class inheritance，interface 描述行为，embedding 是组合机制。
- Google Go Style：清晰、简单、简洁优先；简单代码不应包含不必要抽象，并应能自上而下阅读。

因此，本 skill 将“面向对象”落实为 struct 所有权、receiver method、不变量、小型消费方接口和组合；将“善用设计模式”落实为有当前问题才采用，而不是预建框架。

## 官方事实源

- Go：https://go.dev/doc/ 与 https://go.dev/ref/spec
- Gin：https://github.com/gin-gonic/gin 与 https://gin-gonic.com/docs/
- GORM：https://gorm.io/docs/
- Logrus：https://github.com/sirupsen/logrus
- Consul：https://developer.hashicorp.com/consul/docs/ 与 https://developer.hashicorp.com/consul/api-docs

## 风险结论

- Logrus 官方明确处于 maintenance mode，只维护安全、Bug 和性能，不计划常规新功能。
- Consul KV 适合配置参数和元数据，不是完整业务数据库，也不应承载秘密。
- GORM 提供 ORM、事务、context 和迁移能力，但不能替代物理数据库、索引和迁移策略选型。
- 第三方库 API 会演进。已有项目以 `go.mod` 锁定版本为准，新项目必须重新核对版本兼容性。

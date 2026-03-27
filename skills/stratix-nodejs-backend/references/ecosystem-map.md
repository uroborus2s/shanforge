# Stratix 1.1.x 生态与 Token 地图

当前参考以本仓库真实版本为准：

- `@stratix/cli@1.1.0`
- `@stratix/core@1.1.0`
- `@stratix/database@1.1.0`

## 核心包定位

- `@stratix/cli`
  - 独立 CLI 包，负责 `init`、`generate`、`add preset`、`doctor`、`start`、`config`。
- `@stratix/core`
  - 提供 Fastify 启动、Awilix 容器、装饰器、应用 discovery、插件 auto DI。
- `@stratix/database`
  - 数据库插件，默认导出是 `withRegisterAutoDI(...)` 包装后的插件。
  - 1.1.0 的应用侧公共编程模型以 `BaseRepository` 为中心。
  - `databaseApi` 仍是根容器 token，但更适合 repository 内部兼容或过渡代码。
- `@stratix/redis`
  - Redis 插件，核心对外 token 是 `redisClient`。
- `@stratix/queue`
  - 基于 BullMQ 的队列插件，依赖 Redis，核心对外 token 是 `queueClient`。
- `@stratix/ossp`
  - OSS/对象存储能力插件，核心对外 token 是 `osspClient`。
- `@stratix/was-v7`
  - 面向 WAS V7 的 API 聚合插件，对外通常暴露多个 token，例如 `wasV7ApiCalendar`、`wasV7ApiDrive`、`wasV7ApiUser`。
- `@stratix/tasks`
  - 当前最稳的基础能力是执行器注册入口 `registerTaskExecutor`，以及一组工作流服务、仓储和类型导出。
- `@stratix/devtools`
  - 运行时观测和开发辅助插件。
- `@stratix/testing`
  - 提供轻量级 testing module，适合单元测试和容器拼装测试。

## 常见根容器 Token

- `logger`
  - 由 core 根容器注册，应用和插件都能直接注入。
- `databaseApi`
  - `@stratix/database` 的根容器 token；新代码不应把它当成应用侧首选 API。
- `redisClient`
  - `@stratix/redis` 的 Redis 访问入口。
- `queueClient`
  - `@stratix/queue` 的队列访问入口。
- `osspClient`
  - `@stratix/ossp` 的对象存储访问入口。
- `wasV7ApiCalendar`、`wasV7ApiDrive`、`wasV7ApiUser`
  - `@stratix/was-v7` 通过多个 adapters 暴露的客户端。
- `registerTaskExecutor`
  - `@stratix/tasks` 在根容器中注册的执行器注册函数。

## 新插件接入方式

- 应用侧接入生态插件时，优先使用当前配置形态：
  - `plugins: [{ name: '@stratix/database', plugin: database, options: {...} }]`
- 生态插件自身优先默认导出：
  - `withRegisterAutoDI(具名插件函数, config)`
- 具名插件函数名决定 adapter token 前缀。
- `plugins[].name` 或 `PluginConfig.name` 不决定 adapter token。
- 需要配置默认值和启动前校验时，优先实现 `parameterProcessor`、`parameterValidator`，插件有内部资源时开启 `lifecycle`。

## 推荐插件顺序

- 应用常见顺序：
  1. `@stratix/database`
  2. `@stratix/redis`
  3. 依赖 Redis 或数据库的生态插件，例如 `@stratix/queue`、`@stratix/ossp`、`@stratix/was-v7`
  4. `@stratix/tasks`
  5. 开发辅助插件，例如 `@stratix/devtools`
- 如果某个“插件内部”定义了 `@Executor`，那么 `@stratix/tasks` 应放在该插件之前。
- 如果执行器定义在应用 `src` 中，tasks 只要出现在插件列表里即可，因为应用级 auto DI 发生在全部插件加载之后。

## 各包的典型开发方式

- 数据库层
  - 优先集成 `@stratix/database`
  - 仓储类优先继承 `BaseRepository`
  - `databaseApi` 只在 repository 层的兼容代码里直接使用；service 层通过 repository 访问数据
  - 多表一致性单元、长流程状态迁移、claim/checkpoint/finalize 逻辑优先收敛到 business repository
- 缓存层
  - 统一从 `redisClient` 注入，不要在业务代码中重复创建原生 Redis 客户端
- 队列层
  - 用 `queueClient` 统一管理 queue/worker
  - 队列依赖 Redis，因此配置和健康检查要联动
- 外部系统集成
  - 优先封装成生态插件 adapter，再以根容器 token 暴露给应用 service

## 开发时的现实约束

- 消费方看到的 token 名称，不一定等于插件 `name` 字段，而是取决于插件函数名和 adapter 名。
- `@stratix/database@1.1.0` 的 README 已明确把 `BaseRepository` 定义为应用侧数据库访问的公共入口。
- `@stratix/tasks` 当前更适合作为执行器注册底座和工作流能力库，不应直接假设它会自动暴露一整套 API。
- 对外依赖尽量指向 adapter token，不要跨插件直接依赖内部 service 名称。

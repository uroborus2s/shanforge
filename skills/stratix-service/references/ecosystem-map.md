# Stratix 1.1.x Ecosystem And Plugin Map

## 工具链包

- `@stratix/create`
  - 二进制：`create-stratix`
  - 用途：创建应用、插件、项目 manifest、初始 package 和模板文件。
- `@stratix/forge`
  - 二进制：`stratix`
  - 用途：已创建项目内的生成、preset 注入、doctor、DI/graph、OpenAPI、start、config、release gate。
- `@stratix/core`
  - 用途：Fastify 启动、Awilix 容器、装饰器、应用 discovery、插件 auto DI。
- `@stratix/database`
  - 用途：数据库插件；应用侧新代码优先 `BaseRepository`。

不要再把工程入口描述成单一 `@stratix/cli` 包。

## create-stratix 模板

应用模板：

- `app:api`：HTTP API，默认带 `testing`。
- `app:service`：长驻非 Web 服务，默认 `database + redis + testing`。
- `app:worker`：后台 worker，默认 `redis + queue + testing`。
- `app:sync`：同步集成应用，默认 `database + redis + queue + testing`。
- `app:gateway`：网关，默认 `database + redis + gateway-core + testing`。
- `app:cli`：命令行应用，默认 `testing`。
- `app:web-admin`：管理后台前端，允许 `admin-mock + testing`。

插件模板：

- `plugin:adapter`：对外暴露 adapter 能力。
- `plugin:integration`：封装上游系统集成，默认 `redis + testing`。
- `plugin:data`：数据访问插件，默认 `database + testing`。

## preset / 插件选择

- `database`
  - 包：`@stratix/database`
  - 环境键：`DB_HOST`、`DB_PORT`、`DB_NAME`、`DB_USERNAME`、`DB_PASSWORD`
  - 适合：CRUD、后台 API、业务数据服务、状态表和 checkpoint。
- `redis`
  - 包：`@stratix/redis`
  - 环境键：`REDIS_HOST`、`REDIS_PORT`、`REDIS_PASSWORD`、`REDIS_DB`
  - 适合：缓存、锁、去重、发布订阅。
- `queue`
  - 包：`@stratix/queue`
  - 依赖：`redis`
  - 适合：异步消费、延迟执行、削峰填谷。
- `ossp`
  - 包：`@stratix/ossp`
  - 环境键：`OSSP_ENDPOINT`、`OSSP_ACCESS_KEY`、`OSSP_SECRET_KEY`
  - 适合：对象存储、上传下载、预签名链接。
- `was-v7`
  - 包：`@stratix/was-v7`
  - 环境键：`WPS_APP_ID`、`WPS_APP_SECRET`、`WPS_BASE_URL`
  - 适合：WPS 通讯录、日历、消息、网盘等开放平台能力。
- `testing`
  - 包：Vitest 相关 dev dependencies
  - 适合：新项目烟雾测试、单元测试基线。
- `devtools`
  - 包：`@stratix/devtools`
  - 适合：本地 DI、route、config、health 和 trace 观测。
- `admin-mock`
  - 包：`msw`
  - 适合：`web-admin` 本地 mock。
- `gateway-core`
  - 环境键：`UPSTREAM_URL`
  - 适合：`gateway` 项目的上游默认配置。

## 决策顺序

1. 只做 HTTP 接口：从 `app api` 起步。
2. 需要落库：加 `database`。
3. 需要缓存、锁、订阅：加 `redis`。
4. 需要队列、延迟任务、削峰：加 `queue`，并确保 `redis` 已启用。
5. 需要长流程或可恢复执行：先用 `database` 做状态 / checkpoint；确实异步消费时再加 `queue`。
6. 需要文件或对象存储：加 `ossp`。
7. 需要 WPS 开放平台：加 `was-v7`，通常配 `redis` 做 token/cache。
8. 需要本地观测：先用 `testing`，出现 DI/route/config 问题再加 `devtools`。

## Token 与插件顺序

- `plugins[].name` 只用于注册、日志和配置定位，不决定 adapter token。
- 对外 adapter token 来自插件函数名 + AdapterName 的 PascalCase。
- 修改插件函数名会改变消费方注入 token，是兼容性变更。
- 基础设施插件先注册，消费方后注册。
- `queue` 依赖 `redis`。
- 当前新项目不使用 `@stratix/tasks` preset；若旧项目依赖 tasks，单独做迁移计划。

## 常见根容器 token

- `logger`
- `databaseApi`：兼容/过渡入口，新业务不要让 service 直接依赖它。
- `redisClient`
- `queueClient`
- `osspClient`
- `wasV7ApiCalendar`
- `wasV7ApiDrive`
- `wasV7ApiUser`

业务代码优先依赖 repository 或插件 adapter，不跨插件直接依赖内部 service。

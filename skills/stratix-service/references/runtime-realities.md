# Stratix 运行时事实

本页记录 `/Users/uroborus/NodeProject/wps/obsync-root` 当前源码行为。处理其他版本时重新核对对应源码。

## 启动链路

```text
Stratix.run()
  -> ApplicationBootstrap.bootstrap()
  -> loadEnvironment()
  -> loadConfiguration()
  -> setupContainer()
  -> initializeFastify()
  -> loadPlugins()
  -> performApplicationLevelAutoDI()
  -> listen()
```

`stratix start` 从目标项目解析 `@stratix/core` 后调用 `Stratix.run(...)`。

## 配置

- 配置文件约定为 `stratix.config.ts/js/mjs/cjs`。
- 推荐默认导出 `(sensitiveConfig = {}) => StratixConfig`。
- 直接传入 `config` 对象优先级最高，适合测试或嵌入式运行。
- 当前 `StratixConfig` 顶层包括 `server`、`plugins`、`autoLoad`、`discovery` 及可选日志、缓存、可观测性、安全和 hooks。
- 已从 schema 移除的字段不能为兼容旧代码重新加回。

## 环境

Core 先读进程环境中的 `STRATIX_SENSITIVE_CONFIG`。存在时立即解密并返回，不再加载 dotenv；不存在时才按优先级加载：

1. `.env`
2. `.env.<NODE_ENV>`
3. `.env.<NODE_ENV>.local`
4. `.env.local`

生产环境排除 `.local` 文件。dotenv 加载后不会在同一次调用中重新检查密文，所以密文必须在 `Stratix.run()` 前进入进程环境。

## Discovery 与组件

- 应用默认递归扫描配置的 `rootDir`。
- `@Controller()`、`@Service()`、`@Repository()`、`@Component()` 提供注册元数据。
- `*.test.*`、`*.spec.*` 和声明文件排除在 runtime discovery 外。
- 模块目录只要位于应用 discovery root 下就能被递归发现。
- `module.yaml` 不参与 runtime 注册。
- `createModuleFixture()` 只读取 manifest fixture；完整模块合法性仍由 `doctor modules` 验证。
- 生产可用 `discovery.productionManifest`、`skipRuntimeDiscovery` 和 `registerFromManifest` 降低 glob discovery。

## 路由

- `@Controller()` 不接收路径前缀。
- 业务路径写在 `@Get()`、`@Post()` 等方法装饰器。
- 应用统一前缀放 `discovery.routing.prefix`。
- `operationId` 放 route `config.operationId`，不是 Fastify `schema` 的任意字段。

## DI 与数据库

- 应用 discovery 使用构造参数名完成 Classic 注入。
- Controller 依赖 Service，Service 依赖 Repository。
- 当前 Forge business-repository 模板使用 `database: DatabaseConnectionProvider` 和 `super({ database })`。
- `BaseRepository.query()` 默认使用读连接并返回 `Either`；`command()` 使用写连接并返回 `Either`。
- Repository 负责解包数据库结果，Service 不依赖 Kysely 或数据库 provider。

## 插件 AutoDI

- `withRegisterAutoDI` 使用根容器与插件内部 scope。
- adapter 对外 token 来自具名插件函数与 adapter name。
- `plugins[].name` 只用于注册、日志和配置定位，不决定 adapter token。

## 加密 key

2026-07-24 的 Core/Forge 源码已统一 key 解析：

- 32-byte 原始文本。
- 64 位 hex。
- 解码为 32 bytes 的标准 base64。

Forge 配置 CLI 通过 `STRATIX_ENCRYPTION_KEY` 取 key，并明确拒绝 `--key`。Core 生产环境缺 key 时失败关闭。

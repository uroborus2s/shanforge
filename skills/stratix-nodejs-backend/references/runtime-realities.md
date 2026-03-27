# Stratix 当前运行时事实

这份资料用于约束实现和评审，重点是“当前源码真实行为”，不是历史设计意图。

如果你当前不在 Stratix 源码仓库里，而是在一个消费 npm 包的业务项目中，请先结合 [source-locations.md](source-locations.md) 把这些源码路径映射到 `node_modules/@stratix/*/dist` 与 `dist/types`。

## 关键源码入口

- `packages/core/src/stratix.ts`
- `packages/core/src/bootstrap/application-bootstrap.ts`
- `packages/core/src/decorators/controller.ts`
- `packages/core/src/discovery/scanner.ts`
- `packages/core/src/discovery/analyzer.ts`
- `packages/core/src/discovery/registrar.ts`
- `packages/core/src/plugin/auto-di-plugin.ts`
- `packages/core/src/plugin/module-discovery.ts`
- `packages/core/src/plugin/adapter-registration.ts`
- `packages/core/src/plugin/utils.ts`

## 配置与启动

- 当前启动主链路是 `Stratix.run(options) -> ApplicationBootstrap.bootstrap() -> loadEnvironment() -> loadConfiguration() -> setupContainer() -> initializeFastify() -> loadPlugins() -> performApplicationLevelAutoDI() -> listen()`。
- `StratixRunOptions` 类型里虽然有 `config?: StratixConfig`，但当前 bootstrap 实际没有走这条运行时路径，真正使用的是 `configOptions` 加载配置文件。
- 可用配置文件约定是 `stratix.config.ts/js/mjs/cjs`，并且必须默认导出一个函数，函数入参是解密后的敏感配置，返回值才是 `StratixConfig`。

## 环境变量与敏感配置

- 若存在 `STRATIX_SENSITIVE_CONFIG`，框架会优先解密它。
- 若不存在，则按从低到高优先级加载 `.env`、`.env.{env}`、`.env.{env}.local`、`.env.local`。
- 生产环境会排除 `.local` 文件。
- 当前 `loadEnvironment()` 默认 `strict = true`，因此默认要求基础 `.env` 文件存在。

## 应用级自动发现

- 当前生效的是新的 discovery pipeline，不是旧的 `application-auto-di.ts` 逻辑。
- 默认扫描目录是入口应用目录下的 `src`；也可以显式配置 `applicationAutoDI.directories`。
- 扫描器会匹配 `**/*.{ts,js,mjs,cjs}`，排除 `*.d.ts`、`*.test.ts`、`*.spec.ts`。
- 分析器规则很直接：
  - `@Controller` class -> controller
  - `@Executor` class -> executor
  - 其他任意 class -> service
- 这意味着被扫描目录里不应堆放“只是普通 class 但不希望进容器”的文件。

## 控制器与路由

- `@Controller` 当前签名是 `Controller(options?)`，不支持前缀参数。
- 控制器 metadata 里的 `prefix` 被固定写成空字符串。
- 应用级 discovery 注册路由时，直接使用方法装饰器上的 `path`。
- 控制器实例会优先从 `request.diScope` 解析，因此如果你手动注册了 `SCOPED` 组件，请求级作用域是可用的。
- 当前应用级自动发现不会消费 `applicationAutoDI.routing.prefix`，所以不要把它当成可依赖的全局路由前缀能力。

## 插件级 AutoDI

- `withRegisterAutoDI` 的当前成熟形态是“双层架构”：
  - 根容器：对外共享 token
  - 插件内部 `createScope()` 容器：承载插件内部 controllers/services/repositories/executors
- 插件 discovery 会在扫描过程中“即时注册”控制器路由和执行器，而不是等到一个独立的批处理阶段。
- 即时路由注册直接使用 `routeMetadata.path`，当前并不依赖 `AutoDIConfig.routing.prefix`。
- 因此插件内部若需要前缀，优先使用消费方在 `fastify.register(plugin, { prefix })` 或 Stratix `plugins[].prefix` 里传入的 Fastify 前缀。

## 适配器与 DI token

- 插件适配器扫描目录默认是 `adapters/*.{ts,js}`。
- 适配器支持四种常见写法：
  - 默认导出 class
  - 默认导出对象 `{ adapterName, factory }`
  - 默认导出函数工厂
  - 命名导出的 class/object/function
- 对外 token 的命名规则是：`插件函数名 + AdapterName 的 PascalCase`。
- 这里使用的是插件函数名 `getPluginName(plugin)`，不是 `PluginConfig.name`。
- 因此修改插件函数名会直接改变消费方的注入 token。

## 执行器

- `@Executor` 只负责写入元数据，真正注册依赖 tasks 插件提供的 `registerTaskExecutor`。
- 应用 `src` 下的 executors 在应用级 auto DI 阶段注册，前提是 tasks 插件已经被加载。
- 插件内部 executors 会在 `withRegisterAutoDI` discovery 阶段即时注册，因此 tasks 插件必须早于该插件完成注册。

## 生态文档对齐策略

- `packages/core/README.md` 中仍有 `@Controller('/hello')` 这类旧示例，当前源码不会按该方式处理前缀。
- 部分旧测试和历史命名仍提到 `withEnhancedAutoDI`、`plugin-utils`、`container-registry` 等概念，但不能直接当作现行 API 参考。
- 当 README、旧测试与源码冲突时，以 `packages/core/src` 当前实现为准。

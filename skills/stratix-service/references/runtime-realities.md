# Stratix Runtime Realities

这份资料记录当前 `obsync-root` 源码核对到的真实行为。文档和 README 若与源码冲突，以源码为准。

## 启动链路

当前主链路：

`Stratix.run(options) -> ApplicationBootstrap.bootstrap() -> loadEnvironment() -> loadConfiguration() -> setupContainer() -> initializeFastify() -> loadPlugins() -> performApplicationLevelAutoDI() -> listen()`

`stratix start` 会从当前项目解析 `@stratix/core`，再调用：

```ts
Stratix.run({
  type,
  configOptions: config,
  server: { host, port },
  envOptions: { override: true }
});
```

## 配置文件

- 可用配置文件约定为 `stratix.config.ts/js/mjs/cjs`。
- 推荐默认导出函数：`(sensitiveConfig: Record<string, any> = {}) => StratixConfig`。
- `STRATIX_SENSITIVE_CONFIG` 解密后的对象会作为 `sensitiveConfig` 入参传入。
- 如果直接传入配置对象，core 会走 direct config；普通 CLI 启动通常使用 `configOptions` 指向配置文件。

## 环境变量加载

`loadEnvironment()` 先读取进程环境中的 `STRATIX_SENSITIVE_CONFIG`：

- 如果存在，立即解密并返回解密后的对象。
- 这条路径不会继续加载 dotenv 文件。
- 解密失败会中止启动。

如果进程环境没有 `STRATIX_SENSITIVE_CONFIG`，才加载 dotenv 文件：

1. `.env`
2. `.env.<NODE_ENV>`
3. `.env.<NODE_ENV>.local`
4. `.env.local`

后加载覆盖先加载。生产环境会排除 `.local` 文件。当前源码中 `strict` 默认是 `false`；只有显式 `envOptions.strict = true` 时才要求基础 `.env` 文件存在。

## `.env` 与 STRATIX_SENSITIVE_CONFIG 的实际边界

当前实现不会“先从 `.env.local` 读出 `STRATIX_SENSITIVE_CONFIG`，再回头解密”。因此：

- 普通 `.env` 只适合放 `NODE_ENV`、`STRATIX_ENCRYPTION_KEY` 等进程级变量；应用配置应从解密后的 `sensitiveConfig` 读取，不要从 `process.env` 读取。
- 加密敏感配置必须在调用 `Stratix.run()` 之前已经存在于进程环境中。
- 如果用 `stratix config encrypt ... --output .env.sensitive` 生成文件，运行前需要由 shell、进程管理器、容器平台或自定义启动器预加载它。

示例：

```bash
set -a
. ./.env.sensitive
set +a
STRATIX_ENCRYPTION_KEY="12345678901234567890123456789012" stratix start --type web
```

## 自动发现

- 默认扫描入口应用目录下的 `src`。
- 扫描器匹配 `**/*.{ts,js,mjs,cjs}`，排除 `*.d.ts`、`*.test.ts`、`*.spec.ts`。
- `@Controller` class -> controller。
- 其他被扫描 class 可能进入 service / component 注册路径，普通 class 不要随意放进扫描目录。
- 生产可通过 `discovery.productionManifest` 读取 `.stratix/production-manifest.json`，并用 `skipRuntimeDiscovery` / `registerFromManifest` 减少 runtime glob discovery。

## Controller 与路由

- 当前 `@Controller()` 不接收前缀参数。
- 路径写在方法装饰器上，例如 `@Get('/api/users')`。
- 不依赖 `applicationAutoDI.routing.prefix` 作为全局路由前缀。

## 插件 AutoDI

- `withRegisterAutoDI` 是根容器 + 插件内部 scope 的双层模型。
- 插件 adapter 对外 token 来自插件函数名和 adapter 名称。
- `plugins[].name` / `PluginConfig.name` 不决定 adapter token。
- 插件内部 discovery 会即时注册控制器和执行器类能力；当前新项目不再依赖已移除的 `tasks` preset。

## 加密 key

- core 运行时在非生产环境允许缺省回退到内置开发 key。
- core 运行时在生产环境必须配置 `STRATIX_ENCRYPTION_KEY` 或传入显式 key。
- 强制 `useDefaultKey` 在生产环境会失败。
- 为避免 forge 与 core 的 key 派生差异，当前项目实践中优先使用 32 字节原始字符串作为显式 key，并用同一值完成加密、解密和运行时启动。

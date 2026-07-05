---
name: stratix-service
description: 使用 Stratix 1.1.x 工具链开发、重构、调试和评审后端服务、API、worker、sync、gateway、插件和管理后台配套项目。涉及 Stratix、create-stratix、stratix CLI、@stratix/create、@stratix/forge、@stratix/core、@stratix/database、stratix.config.ts、STRATIX_SENSITIVE_CONFIG、withRegisterAutoDI、controller/service/repository、插件或 preset 选择时必须使用。
---

# Stratix Service

用于 Stratix 后端开发：优先用 CLI 生成骨架，再按业务补最少手写代码。当前事实来自 `/Users/uroborus/NodeProject/wps/obsync-root`：`@stratix/create@1.1.0` 创建应用和插件，`@stratix/forge@1.1.0` 提供项目内 `stratix` 命令，`@stratix/core@1.1.0` 负责 runtime / DI / discovery，`@stratix/database@1.1.0` 仍优先使用 `BaseRepository`。

## 总原则

- 先用 CLI 探测能力，再决定项目类型、preset、插件和资源生成命令。
- 根据业务目标选择最小可用组合；只有业务边界或外部系统信息缺失时才问用户。
- 能用 `create-stratix` 或 `stratix` 生成的骨架，不手写起步目录和样板。
- 手写代码只补业务逻辑、字段映射、插件配置、测试和 CLI 未覆盖的部分。
- 每轮结构调整后至少跑 `stratix doctor`；发布前生成 production manifest 并跑 release gate。
- 不再推荐旧的单包 `@stratix/cli` 口径；当前工具链分为 `@stratix/create` 和 `@stratix/forge`。
- `@stratix/tasks` preset 已移除；新项目不要再把 tasks 当作默认插件或执行器底座。
- 新生成应用的配置默认全部来自 `sensitiveConfig`；先加密，再通过 `STRATIX_SENSITIVE_CONFIG` 注入。

## 执行流程

1. 识别目标类型：
   - HTTP API / 管理后台接口：`app api`
   - 后台常驻服务：`app service`
   - 队列 worker：`app worker`
   - 同步集成：`app sync`
   - 网关：`app gateway`
   - 命令行工具：`app cli`
   - 管理后台前端：`app web-admin`
   - 对外 SDK / client：`plugin adapter`
   - 上游系统集成：`plugin integration`
   - 可复用数据访问：`plugin data`
2. 先查看可用项：
   - `create-stratix list templates`
   - `create-stratix list presets`
   - 确认当前执行的是 Stratix 1.1.x；已有项目内优先使用 `pnpm exec stratix`。
   - 已有项目内再跑 `stratix list templates`、`stratix list presets`
   - 如果 `create-stratix list` 或 `stratix list` 失败，先用 `--help` 或 npm 包版本确认新命令；不得猜测 template、preset 或插件名。
3. 根据业务选择最小 preset：
   - 只做 HTTP：先保持 `core`
   - 落库：加 `database`
   - 缓存、锁、订阅：加 `redis`
   - 队列或延迟消费：加 `queue`，并保证 `redis` 已启用
   - 对象存储：加 `ossp`
   - WPS / WAS V7 集成：加 `was-v7`，通常配 `redis`
   - 测试基线：保留或添加 `testing`
   - 本地观测：需要排查 DI / route / config 时再加 `devtools`
   - 只选择业务明确需要的插件；不要为了“完整”默认加 `database`、`redis`、`queue`、`ossp` 或 `was-v7`。
4. 生成骨架后按 `repository -> service -> controller` 补实现。
5. 通过配置安全门。
6. 用 `stratix doctor`、`pnpm build`、`pnpm test` 验证。
7. 发布前用 `stratix build-manifest` 和 `stratix release gate` 固化生产证据。

## 配置安全门

1. 生成 `src/stratix.config.ts` 时，应用配置、插件配置和 provider 凭据默认只读 `sensitiveConfig`。
2. 不得用 `DB_HOST`、`REDIS_HOST`、`WPS_APP_SECRET` 等普通环境变量作为配置回退。
3. 把 `server`、`database`、`redis`、`queue`、`ossp`、`was-v7` 等实际配置写入 `sensitive.<env>.json`。
4. 先跑 `stratix config validate ... --strict`，再用显式 `STRATIX_ENCRYPTION_KEY` 加密。
5. 启动前把加密结果作为进程环境变量 `STRATIX_SENSITIVE_CONFIG` 注入，不依赖 `.env.local` 同轮自动解密。
6. 至少跑一次 decrypt 或真实启动，确认 forge 加密结果能被 core 解密。
7. 不能完成加密、解密和注入验证时，结论只能是 blocked；不要声明生成应用可上线。

## 常用 CLI

- 新建项目：
  - `create-stratix app api my-api --preset database,testing --no-install`
  - `create-stratix app worker my-worker --preset redis,queue,testing --no-install`
  - `create-stratix plugin data @scope/data-plugin --no-install`
- 查看能力：
  - `create-stratix list templates`
  - `create-stratix list presets`
  - `stratix list templates`
  - `stratix list presets`
- 增加能力：
  - `stratix add preset database --no-install`
  - `stratix add preset redis --no-install`
  - `stratix add preset queue --no-install`
- 生成代码：
  - `stratix generate resource user`
  - `stratix generate controller user`
  - `stratix generate service user`
  - `stratix generate repository user`
  - `stratix generate business-repository order`
  - `stratix generate module billing`
  - `stratix generate plugin-adapter client`
  - `stratix generate plugin-service auth`
  - `stratix generate plugin-controller webhook`
  - `stratix generate admin-page user`
  - `stratix generate admin-crud user`
- 诊断与交付：
  - `stratix doctor`
  - `stratix doctor modules`
  - `stratix di`
  - `stratix graph modules --format mermaid`
  - `stratix openapi`
  - `stratix build-manifest --output .stratix/production-manifest.json`
  - `stratix release gate --dry-run --manifest .stratix/production-manifest.json`
  - `stratix start --type web --config ./src/stratix.config.ts --host 0.0.0.0 --port 3000`
- 配置：
  - `stratix config validate sensitive.local.json --required database --strict`
  - `export STRATIX_ENCRYPTION_KEY="<32-byte-raw-string>"`
  - `stratix config encrypt sensitive.local.json --key "$STRATIX_ENCRYPTION_KEY" --output .env.sensitive`
  - `stratix config decrypt "$STRATIX_SENSITIVE_CONFIG" --key "$STRATIX_ENCRYPTION_KEY" --output tmp/decrypted.json`

## 编码规则

- 配置主入口是 `src/stratix.config.ts`，默认导出函数：`(sensitiveConfig = {}) => StratixConfig`。
- 新生成应用不要从普通 `.env` 读取业务配置；普通环境变量只保留 `NODE_ENV`、`STRATIX_SENSITIVE_CONFIG`、`STRATIX_ENCRYPTION_KEY` 和进程启动必需变量。
- Controller 只处理协议、参数和响应；Service 只做业务编排；Repository 承接数据访问。
- 数据库代码优先继承 `BaseRepository`；Service 不直接注入 `databaseApi` 或数据库插件。
- 多表一致性、状态机、claim / checkpoint / finalize 优先放进 `business-repository`。
- `@Controller()` 不接收路由前缀；路由路径写在方法装饰器上。
- 不把普通 class 随意放进自动发现目录；扫描目录中的 class 可能进入 DI 容器。
- 插件默认导出保持“具名插件函数 + `withRegisterAutoDI(...)`”；插件函数名会影响 adapter token。
- `plugins[].name` 用于注册、日志和配置定位，不决定 adapter token。
- 插件内部需要默认值或启动前校验时，实现 `parameterProcessor` 与 `parameterValidator`。

## 环境与敏感配置

- 普通开发也按“JSON -> encrypt -> `STRATIX_SENSITIVE_CONFIG`”跑应用配置；普通 `.env` 只放进程级变量。
- 生产环境会排除 `.local` 文件，推荐由部署平台注入真实环境变量。
- `loadEnvironment()` 会先检查进程环境中的 `STRATIX_SENSITIVE_CONFIG`；存在时直接解密并传给 `stratix.config.ts`，不再加载 dotenv。
- 如果 `STRATIX_SENSITIVE_CONFIG` 只写在 `.env.local`，当前启动链路不会在同一次 `loadEnvironment()` 中先加载再解密。应由外层进程预加载，或在 shell / CI / 容器环境中直接注入该变量。
- 非生产环境缺省 key 会回退到内置开发 key；生产环境必须配置 `STRATIX_ENCRYPTION_KEY` 或传入显式 key。
- 加密 key 和运行时解密 key 必须一致。当前最稳妥做法：用 32 字节原始字符串作为 `STRATIX_ENCRYPTION_KEY`，并用同一值执行 `stratix config encrypt|decrypt --key ...`。

## 评审清单

- 检查是否仍使用旧的 `@stratix/cli` 单包叙事，而不是 `@stratix/create` + `@stratix/forge`。
- 检查是否跳过 `create-stratix list` / `stratix list` 直接手写模板。
- 检查新项目是否继续引入已移除的 `tasks` preset。
- 检查是否过早堆叠 `database`、`redis`、`queue`、`ossp`、`was-v7`，而不是按业务选择最小组合。
- 检查 Service 或 Controller 是否直接写数据库访问。
- 检查是否错误使用 `@Controller('/prefix')`。
- 检查是否错误依赖 `plugins[].name` 生成 adapter token。
- 检查是否把 `STRATIX_SENSITIVE_CONFIG` 写入 `.env.local` 后假设 runtime 会自动解密。
- 检查生产环境是否依赖默认加密 key。
- 检查应用配置是否绕过 `STRATIX_SENSITIVE_CONFIG`，直接读取普通 env。
- 检查是否未运行 `stratix doctor`、`build-manifest` 或必要测试就宣称完成。

## 按需加载资料

- CLI 命令、obsync-root 根脚本和完整开发循环：`references/cli-workflow.md`
- 项目与插件脚手架、配置样例：`references/scaffolds.md`
- 插件 / preset 选择和 token 规则：`references/ecosystem-map.md`
- 运行时、dotenv 和 sensitive config 事实：`references/runtime-realities.md`
- 环境变量、`STRATIX_SENSITIVE_CONFIG`、加解密 key：`references/environment-config.md`
- 源码与 npm 编译产物定位：`references/source-locations.md`

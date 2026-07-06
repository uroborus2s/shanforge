# Stratix Service CLI Workflow

先探测当前 npm latest 和项目实际安装版本，再执行命令。历史版本事实来自 `/Users/uroborus/NodeProject/wps/obsync-root`，只能作为兼容参考：

- `@stratix/create@1.1.0` 提供 `create-stratix`，只负责创建应用和插件。
- `@stratix/forge@1.1.0` 提供项目内 `stratix` 命令，负责生成、诊断、图谱、OpenAPI、启动、配置和发布门禁。
- `@stratix/core@1.1.0` 是 runtime / DI / discovery。
- `@stratix/database@1.1.0` 是 `BaseRepository` 优先模型。

## 版本探测

每次创建或评审 Stratix 项目前，先查当前 npm dist-tags：

```bash
npm view @stratix/create dist-tags --json
npm view @stratix/forge dist-tags --json
npm view @stratix/core dist-tags --json
npm view @stratix/database dist-tags --json
```

若本机 npm cache 权限异常，可临时指定 cache，不要修改用户全局 cache：

```bash
NPM_CONFIG_CACHE=/private/tmp/stratix-npm-cache npm view @stratix/forge dist-tags --json
```

已有项目再看：

```bash
cat package.json
cat node_modules/@stratix/forge/package.json
cat node_modules/@stratix/core/package.json
pnpm exec stratix --help
```

不要假设 `create`、`forge`、`core`、`database` 版本号一致。命令以项目实际安装版本和 `--help` 输出为准。

## obsync-root 根命令

在 Stratix monorepo 本身开发时，根 `package.json` 的主要命令是：

- `pnpm run build:supported`
- `pnpm run build:pkg --pkg <package>`
- `pnpm run dev --pkg <package>`
- `pnpm run lint`
- `pnpm run lint:pkg --pkg <package>`
- `pnpm run test:supported`
- `pnpm run test:coverage:core`
- `pnpm run typecheck:supported`
- `pnpm run docs:validate`
- `pnpm run security:audit`
- `pnpm run release:gate:dry-run`
- `pnpm run quality:release`

做框架包修改时，优先使用包级命令收窄反馈；发布前再跑 `quality:release`。

## 创建阶段

先看模板和 preset：

```bash
create-stratix list templates
create-stratix list presets
```

新建应用：

```bash
create-stratix app api demo-api --preset testing --no-install
create-stratix app worker demo-worker --preset redis,queue,testing --no-install
create-stratix app service demo-service --preset database,redis,testing --no-install
create-stratix app sync demo-sync --preset database,redis,queue,testing --no-install
create-stratix app gateway demo-gateway --no-install
create-stratix app cli demo-cli --no-install
create-stratix app web-admin demo-admin --preset admin-mock,testing --no-install
```

新建插件：

```bash
create-stratix plugin adapter @demo/client-plugin --no-install
create-stratix plugin integration @demo/upstream-plugin --no-install
create-stratix plugin data @demo/data-plugin --no-install
```

若用户没有指定模板，AI 按业务目标选择最小模板；不为了“完整”默认创建 gateway、sync 或 worker。

## 项目内开发阶段

进入已创建项目后，先查看 forge 可用能力：

```bash
stratix list templates
stratix list presets
```

添加 preset：

```bash
stratix add preset database --no-install
stratix add preset redis --no-install
stratix add preset queue --no-install
stratix add preset ossp --no-install
stratix add preset was-v7 --no-install
stratix add preset devtools --no-install
```

生成资源：

```bash
stratix generate resource order
stratix generate controller order
stratix generate service order
stratix generate repository order
stratix generate business-repository workflow-execution
stratix generate module billing
```

插件内部资源：

```bash
stratix generate plugin-adapter client
stratix generate plugin-service auth
stratix generate plugin-controller webhook
```

管理后台资源：

```bash
stratix generate admin-page user
stratix generate admin-crud user
```

## 完整业务功能循环

1. 识别业务资源和存储边界。
2. 需要新项目时先 `create-stratix ... --no-install`。
3. 需要基础设施时只加必要 preset。
4. 普通 CRUD 用 `stratix generate resource <name>`。
5. 多表事务、状态机、checkpoint、claim/finalize 用 `stratix generate business-repository <name>`。
6. 先实现 repository，再实现 service，最后补 controller。
7. 补 `src/stratix.config.ts` 的插件 options 和 `sensitiveConfig` 映射。
8. 添加或调整测试。
9. 跑 `stratix doctor`。
10. 跑 `pnpm build` 和 `pnpm test`。
11. 发布前跑 `stratix build-manifest --output .stratix/production-manifest.json`。
12. 发布前跑 `stratix release gate --dry-run --manifest .stratix/production-manifest.json`。

## 诊断与交付命令

```bash
stratix doctor
stratix doctor modules
stratix di
stratix graph modules --format mermaid
stratix openapi generate --output openapi.json
stratix build-manifest --output .stratix/production-manifest.json
stratix release gate --dry-run --manifest .stratix/production-manifest.json
stratix start --type web --config ./src/stratix.config.ts --host 0.0.0.0 --port 3000
```

## 2026-07-05 历史兼容注记

在 Node 24.14.1、npm 11.11.0、pnpm 11.9.0 下，npm latest 为：

- `@stratix/create@1.1.0`
- `@stratix/core@1.1.0`
- `@stratix/database@1.1.0`
- `@stratix/forge@1.1.2`

用 `npx --yes @stratix/create@1.1.0` 生成 `app api --preset testing --no-install`，并将项目内 forge 升级到 `@stratix/forge@1.1.2` 后：

- 初次 `pnpm install` 在 pnpm 11 下可能失败：`[ERR_PNPM_IGNORED_BUILDS] Ignored build scripts: esbuild@0.28.1`。临时测试可用 `pnpm approve-builds --all` 解除；生产模板或文档需要给出非交互策略。
- `pnpm exec stratix doctor` 失败：`Dev dependency mismatch: @stratix/forge expected ^1.1.0`，因为 `.stratix/project.json` 仍按模板初始版本校验。
- `pnpm test:run` 通过，默认测试 `2 passed`。
- `pnpm build` 失败：`HealthController.ts` 中的 `operationId` 不属于 `FastifySchema`。
- `pnpm exec stratix build-manifest --output .stratix/production-manifest.json` 通过。
- `pnpm exec stratix release gate --dry-run --manifest .stratix/production-manifest.json` 失败：生成项目缺少 security / audit 类脚本。
- `pnpm exec stratix openapi generate --output openapi.json` 是正确命令，可生成 OpenAPI 文档。
- `pnpm exec stratix start ...` 在 Node 24 下失败：forge start 使用 `createRequire(...).resolve('@stratix/core')`，但 `@stratix/core@1.1.0` 的 exports 只有 import 条件。
- 官方模板的 `src/config/stratix.generated.ts` 仍读取 `process.env.PORT`，`.env.example` 暴露 `PORT/HOST`。按生产配置安全门，生成项目必须改为从 `sensitiveConfig.server` 读取，不能把应用配置留在普通环境变量里。
- `stratix config <subcommand> --help` 只输出 usage 且 exit 1，没有列出 `--key`、`--output`、`--strict` 等实际参数。

这些是历史失败，不是永久结论。新版本必须重新查 latest、实际安装版本和 CLI 能力，再跑完整门禁。

## 2026-07-06 latest 复测

在 Node 24.14.1、npm 11.11.0、pnpm 11.9.0 下，npm latest 为：

- `@stratix/create@1.1.1`
- `@stratix/core@1.1.1`
- `@stratix/database@1.1.0`
- `@stratix/forge@1.1.3`

`@stratix/create@1.1.1` 生成 `app api --preset testing --no-install` 后：

- `pnpm install` 通过，无需手动 `pnpm approve-builds`。
- 默认实际安装 `@stratix/core@1.1.0`、`@stratix/forge@1.1.2`；这说明仍要查项目实际安装版本。
- 默认安装下 `pnpm test:run`、`pnpm build`、`doctor`、`build-manifest`、`release gate`、`openapi generate` 通过。
- 默认安装下 `stratix start` 仍失败：`Cannot resolve @stratix/core from the current project`。
- 显式升级到 `@stratix/core@1.1.1` 和 `@stratix/forge@1.1.3` 后，`pnpm build`、测试、`build-manifest`、`release gate`、`openapi generate` 通过。
- 显式 latest 下 `doctor` 失败：`.stratix/project.json` 仍期望 `@stratix/core ^1.1.0`。
- 生成模板已改为从 `sensitiveConfig.server` 读取 host/port，`.env.example` 不再承载 `PORT/HOST`。
- `stratix config validate/encrypt/decrypt` 通过，启动日志能看到 `Found sensitive configuration environment variable`。
- `stratix start --config ./src/stratix.config.ts` 失败：源码 `stratix.config.ts` import `./config/stratix.generated.js`，但源码目录只有 `.ts` 文件。
- `stratix start --config ./dist/stratix.config.js` 仍失败：discovery 扫描 `src/stratix.config.ts` 时触发同一 `stratix.generated.js` 找不到问题。

因此当前 latest 不能声明完整上线。阻塞点缩小到 start/discovery 与 doctor 版本元数据；配置加密、解密和敏感变量注入已能跑到 runtime 解密阶段。

## 配置命令

```bash
stratix config validate sensitive.local.json --required database --strict
export STRATIX_ENCRYPTION_KEY="<32-byte-raw-string>"
stratix config encrypt sensitive.local.json --key "$STRATIX_ENCRYPTION_KEY" --output .env.sensitive
stratix config decrypt "$STRATIX_SENSITIVE_CONFIG" --key "$STRATIX_ENCRYPTION_KEY" --output tmp/decrypted.json
```

没有显式 key 时，forge 配置工具会走环境变量 `STRATIX_ENCRYPTION_KEY`，再缺省会回退到内置开发 key。生产运行时不能依赖默认 key。

# Stratix 1.x 工具链问题报告

## 环境

- OS: macOS
- Node: `v24.14.1`
- npm: `11.11.0`
- pnpm: `11.9.0`

2026-07-05 查询到的 npm dist-tags：

- `@stratix/create`: `latest = 1.1.0`
- `@stratix/core`: `latest = 1.1.0`
- `@stratix/database`: `latest = 1.1.0`
- `@stratix/forge`: `latest = 1.1.2`

## 复现步骤

```bash
mkdir -p /private/tmp/stratix-repro
cd /private/tmp/stratix-repro

npx --yes @stratix/create@1.1.0 app api demo-api --preset testing --no-install
cd demo-api

pnpm install
pnpm approve-builds --all
pnpm add -D @stratix/forge@1.1.2

pnpm exec stratix doctor
pnpm test:run
pnpm build
pnpm exec stratix build-manifest --output .stratix/production-manifest.json
pnpm exec stratix release gate --dry-run --manifest .stratix/production-manifest.json
pnpm exec stratix start --type web --config ./src/stratix.config.ts --host 127.0.0.1 --port 3107
pnpm exec stratix openapi generate --output openapi.json
pnpm exec stratix config <subcommand> --help
```

## 实际结果

- `pnpm install`: failed first under pnpm 11 because `esbuild@0.28.1` build scripts were blocked by `[ERR_PNPM_IGNORED_BUILDS]`. Running `pnpm approve-builds --all` in the temporary project allowed testing to continue.
- `pnpm exec stratix doctor`: failed after upgrading forge to `1.1.2`: `Dev dependency mismatch: @stratix/forge expected ^1.1.0`.
- `pnpm test:run`: passed, default tests `2 passed`.
- `pnpm exec stratix build-manifest --output .stratix/production-manifest.json`: passed.
- `pnpm exec stratix openapi generate --output openapi.json`: passed.
- `pnpm build`: failed.
- `pnpm exec stratix release gate --dry-run --manifest .stratix/production-manifest.json`: failed.
- `pnpm exec stratix start ...`: failed.
- Runtime `STRATIX_SENSITIVE_CONFIG` injection could not be verified because `stratix start` fails before the app starts.

## Bug 1: 生成的 API 项目无法通过构建

生成文件：

```ts
// src/controllers/HealthController.ts
@Get('/health', {
  schema: {
    operationId: 'HealthController_check',
    response: {
      200: {
        type: 'object'
      }
    }
  }
})
```

构建错误：

```text
src/controllers/HealthController.ts(15,7): error TS2353:
Object literal may only specify known properties, and 'operationId' does not exist in type 'FastifySchema'.
```

原因判断：

`@stratix/create@1.1.0` 生成时把 `operationId` 放进 Fastify `schema` 对象，但 `@stratix/core@1.1.0` 暴露的 decorator 类型不接受该字段，因为它不属于 `FastifySchema`。

期望修复：

- 扩展路由 schema 类型，允许 `operationId` 等 Stratix/OpenAPI 元数据；或
- 把 `operationId` 移出 Fastify `schema` 对象；或
- 调整生成模板，保证新项目能通过 `pnpm build`。

## Bug 2: 生成项目无法通过 release gate 的安全检查

命令：

```bash
pnpm exec stratix release gate --dry-run --manifest .stratix/production-manifest.json
```

错误：

```text
Release gate plan: build/test/docs/security/pack/api/manifest (7 checks)
Release gate security: package.json must define one script: security:audit, security, audit:security, audit
```

原因判断：

`@stratix/forge@1.1.2` release gate 要求 package.json 至少有以下脚本之一：

- `security:audit`
- `security`
- `audit:security`
- `audit`

但 `@stratix/create@1.1.0 app api ...` 生成项目没有这些脚本。

期望修复：

- 在 app 模板中生成默认 security/audit 脚本；或
- 让 release gate 对官方生成项目提供兼容默认策略；或
- 让 release gate 输出可直接执行的修复命令。

## Bug 3: `stratix start` 无法解析 ESM-only 的 `@stratix/core`

命令：

```bash
pnpm exec stratix start --type web --config ./src/stratix.config.ts --host 127.0.0.1 --port 3107
```

错误：

```text
Cannot resolve @stratix/core from the current project.
Please install the project dependencies before running stratix start.
```

`@stratix/forge@1.1.2` 相关实现：

```js
const projectRequire = createRequire(path.join(projectDir, 'package.json'));
resolvedPath = projectRequire.resolve('@stratix/core');
```

`@stratix/core@1.1.0` 相关 package exports：

```json
"exports": {
  ".": {
    "import": "./dist/index.js",
    "types": "./dist/types/index.d.ts"
  }
}
```

原因判断：

`@stratix/forge` 使用 CommonJS `createRequire().resolve()` 解析 `@stratix/core`，但 `@stratix/core` 对 `"."` 只暴露 ESM import export。Node 24 下即使 `@stratix/core` 已安装也会解析失败。

期望修复：

- 让 `stratix start` 正确解析 ESM package exports；或
- 在 `@stratix/core` 中增加兼容的 export condition；或
- 用 import-based resolution 替代 `createRequire().resolve()`。

## Bug 4: 升级 forge 后 doctor 与模板版本元数据冲突

命令：

```bash
pnpm add -D @stratix/forge@1.1.2
pnpm exec stratix doctor
```

错误：

```text
Dev dependency mismatch: @stratix/forge expected ^1.1.0
Doctor found 1 issue(s).
```

原因判断：

官方 latest 中 `@stratix/forge` 是 `1.1.2`，但 `@stratix/create@1.1.0` 生成的 `.stratix/project.json` 仍保留 `@stratix/forge ^1.1.0` 的模板期望。升级到 latest 后 doctor 直接失败。

期望修复：

- 提供官方升级命令，同步更新 `.stratix/project.json` 的工具链期望；或
- doctor 对 patch/minor 兼容升级给出明确修复建议；或
- 让 create 模板使用与 forge latest 兼容的元数据。

## Bug 5: 生成配置没有把 server 配置收口到 sensitiveConfig

生成文件：

```ts
// src/config/stratix.generated.ts
server: {
  host: '0.0.0.0',
  port: Number(process.env.PORT || 3000)
}
```

`.env.example`：

```dotenv
PORT=3000 # Application port
HOST=0.0.0.0 # Application host
```

原因判断：

官方模板仍从普通环境变量读取应用 server 配置。对于要求“所有应用配置都必须加密后通过 `STRATIX_SENSITIVE_CONFIG` 注入”的生产标准，这会导致生成项目默认不合格。

期望修复：

- 生成 `sensitiveConfig.server.host` 和 `sensitiveConfig.server.port` 读取逻辑；并
- 让 `.env.example` 只保留 `STRATIX_SENSITIVE_CONFIG`、`STRATIX_ENCRYPTION_KEY`、`NODE_ENV` 等进程级变量；或
- 在模板文档中明确 server 配置是否属于敏感配置边界，并提供生产化模板。

## Bug 6: config 子命令 help 不完整且返回失败

命令：

```bash
pnpm exec stratix config <subcommand> --help
```

实际结果：

只输出 `Usage: stratix config <encrypt|decrypt|validate|generate-key> [options]`，退出码为 `1`，没有列出 `--key`、`--output`、`--strict` 等实际参数。

期望修复：

- 每个 config 子命令的 `--help` 返回 exit 0；并
- 列出该子命令支持的参数、输入形态和示例。

## Bug 7: pnpm 11 非交互安装被 esbuild build script 审批阻断

命令：

```bash
pnpm install
```

错误：

```text
[ERR_PNPM_IGNORED_BUILDS] Ignored build scripts: esbuild@0.28.1
```

期望修复：

- 模板或官方文档给出 pnpm 11 下的非交互安装策略；或
- 在生成项目中写入必要的 pnpm 配置，避免 CI / agent 自动化初次安装直接失败。

## 说明：OpenAPI 命令形态

`stratix openapi` without a subcommand is incomplete. The correct command is:

```bash
stratix openapi generate --output openapi.json
```

This works through `pnpm exec stratix openapi generate --output openapi.json` in the test project.

## 期望基线

A fresh project generated by current latest packages should pass at least:

```bash
pnpm install
pnpm exec stratix --help
pnpm exec stratix doctor
pnpm test:run
pnpm build
pnpm exec stratix build-manifest --output .stratix/production-manifest.json
pnpm exec stratix release gate --dry-run --manifest .stratix/production-manifest.json
pnpm exec stratix start --type web --config ./src/stratix.config.ts --host 127.0.0.1 --port 3107
pnpm exec stratix openapi generate --output openapi.json
```

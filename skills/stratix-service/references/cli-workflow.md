# Stratix Service CLI Workflow

当前命令事实来自 `/Users/uroborus/NodeProject/wps/obsync-root`：

- `@stratix/create@1.1.0` 提供 `create-stratix`，只负责创建应用和插件。
- `@stratix/forge@1.1.0` 提供项目内 `stratix` 命令，负责生成、诊断、图谱、OpenAPI、启动、配置和发布门禁。
- `@stratix/core@1.1.0` 是 runtime / DI / discovery。
- `@stratix/database@1.1.0` 是 `BaseRepository` 优先模型。

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
create-stratix app api demo-api --preset database,testing --no-install
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
7. 补 `src/stratix.config.ts` 的插件 options 和环境变量映射。
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
stratix openapi
stratix build-manifest --output .stratix/production-manifest.json
stratix release gate --dry-run --manifest .stratix/production-manifest.json
stratix start --type web --config ./src/stratix.config.ts --host 0.0.0.0 --port 3000
```

## 2026-07-05 实测风险

在 Node 24.14.1、npm 11.11.0、pnpm 11.9.0 下，用 `npx --yes @stratix/create@1.1.0` 生成 `app api --preset testing --no-install` 后：

- `pnpm exec stratix doctor` 通过，输出 `Doctor checks passed.`。
- `pnpm test:run` 通过，默认测试 `2 passed`。
- `pnpm build` 失败：`HealthController.ts` 中的 `operationId` 不属于 `FastifySchema`。
- `pnpm exec stratix build-manifest --output .stratix/production-manifest.json` 通过。
- `pnpm exec stratix release gate --dry-run --manifest .stratix/production-manifest.json` 失败：生成项目缺少 security / audit 类脚本。
- `pnpm exec stratix openapi` 失败：`Unknown openapi command`。
- `pnpm exec stratix start ...` 在 Node 24 下失败：forge start 使用 `createRequire(...).resolve('@stratix/core')`，但 `@stratix/core@1.1.0` 的 exports 只有 import 条件。

遇到这些失败时，不要手写绕过或宣称上线通过。先记录命令、版本、stderr，并把结论标为 blocked，除非当前项目已验证出兼容版本或已修生成模板。

## 配置命令

```bash
stratix config validate sensitive.local.json --required database --strict
export STRATIX_ENCRYPTION_KEY="<32-byte-raw-string>"
stratix config encrypt sensitive.local.json --key "$STRATIX_ENCRYPTION_KEY" --output .env.sensitive
stratix config decrypt "$STRATIX_SENSITIVE_CONFIG" --key "$STRATIX_ENCRYPTION_KEY" --output tmp/decrypted.json
```

没有显式 key 时，forge 配置工具会走环境变量 `STRATIX_ENCRYPTION_KEY`，再缺省会回退到内置开发 key。生产运行时不能依赖默认 key。

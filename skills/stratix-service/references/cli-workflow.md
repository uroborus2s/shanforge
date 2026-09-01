# Stratix CLI 工作流

## 能力探测与创建门

创建、生成或加 preset 前，先读取显式/已安装 CLI 和相关包版本，并与支持矩阵核对：`@stratix/core`: `1.1.2`、`@stratix/forge`: `1.1.4`、`@stratix/create`: `1.1.2`、`@stratix/database`: `1.1.1`、`@stratix/testing`: `1.0.0-beta.1`。先查目标项目实际版本：

```bash
node -p "require('./node_modules/@stratix/core/package.json').version"
node -p "require('./node_modules/@stratix/forge/package.json').version"
node -p "require('./node_modules/@stratix/create/package.json').version"
node -p "require('./node_modules/@stratix/database/package.json').version"
node -p "require('./node_modules/@stratix/testing/package.json').version"
pnpm exec stratix --help
pnpm exec stratix list templates
pnpm exec stratix list presets
```

不要假设这些包版本相同。未知或不兼容立即 `blocked`：逐包列出 `detected`、`required`、`difference`、未执行命令和唯一 `next_required_action`；不自动安装或升级，不运行未固定版本的远端创建器。命令以已验证兼容的本地 `create-stratix` 与目标项目内 `--help` 为准。

## 工具边界

- `create-stratix`：创建 app/plugin。
- 项目内 `pnpm exec stratix`：generate、add、doctor、di、graph、openapi、start、config、manifest 和 release gate。

不使用旧单包 `@stratix/cli`。

## 创建

仅在上述创建门通过后，才运行下列已验证兼容的本地 `create-stratix` 命令：

```bash
create-stratix list templates
create-stratix list presets
create-stratix app api demo-api --preset testing --no-install
create-stratix app worker demo-worker --preset redis,queue,testing --no-install
create-stratix plugin data @demo/data-plugin --no-install
```

只选择真实需要的 template/preset。

## 项目开发

```bash
pnpm exec stratix add preset database --no-install
pnpm exec stratix generate resource order
pnpm exec stratix generate module billing
pnpm exec stratix generate business-repository workflow-execution
```

顺序：

1. 生成最小骨架。
2. 核对 `src/stratix.config.ts` 和 `.stratix/project.json`。
3. 实现 Repository、Service、Controller。
4. 添加目标测试。
5. 运行 doctor、build、test。

## 配置

CLI 只从进程环境读取 key，不接受 `--key`：

```bash
pnpm exec stratix config validate sensitive.local.json --required server,database --strict
export STRATIX_ENCRYPTION_KEY="$(pnpm exec stratix config generate-key --length 32 --format base64)"
pnpm exec stratix config encrypt sensitive.local.json --output .env.sensitive
set -a
. ./.env.sensitive
set +a
pnpm exec stratix config decrypt "$STRATIX_SENSITIVE_CONFIG" --output tmp/decrypted.json
```

## 诊断与发布

```bash
pnpm exec stratix doctor
pnpm exec stratix doctor modules
pnpm exec stratix di
pnpm exec stratix graph modules --format mermaid
pnpm exec stratix openapi generate --output openapi.json
pnpm exec stratix build-manifest --output .stratix/production-manifest.json
pnpm exec stratix release gate --dry-run --manifest .stratix/production-manifest.json
pnpm exec stratix start --type web --config ./src/stratix.config.ts
```

发布结论必须来自当前目标版本的新鲜执行，不继承 `reports/` 中的历史失败或通过。

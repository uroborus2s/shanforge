# Stratix CLI 工作流

## 能力探测

先查目标项目实际版本：

```bash
node -p "require('./node_modules/@stratix/core/package.json').version"
node -p "require('./node_modules/@stratix/forge/package.json').version"
pnpm exec stratix --help
pnpm exec stratix list templates
pnpm exec stratix list presets
```

创建新项目时再查当前发布标签：

```bash
npm view @stratix/create dist-tags --json
npm view @stratix/forge dist-tags --json
npm view @stratix/core dist-tags --json
npm view @stratix/database dist-tags --json
```

不要假设这些包版本相同。命令以目标项目内 `--help` 为准。

## 工具边界

- `create-stratix`：创建 app/plugin。
- 项目内 `pnpm exec stratix`：generate、add、doctor、di、graph、openapi、start、config、manifest 和 release gate。

不使用旧单包 `@stratix/cli`。

## 创建

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

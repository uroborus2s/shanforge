# Stratix Source And Published Package Locations

当这个 skill 提到 `packages/core/src/...`、`packages/forge/src/...`、`packages/create/src/...` 这类路径时，指的是 Stratix 源码仓库中的权威实现位置。普通业务项目通常只有 npm 发布后的 `dist` 和类型声明。

## 在 Stratix 源码仓库里

优先按这些路径核对事实：

- `packages/create/src/*`
- `packages/forge/src/*`
- `packages/core/src/*`
- `packages/database/src/*`
- `packages/redis/src/*`
- `packages/queue/src/*`
- `packages/ossp/src/*`
- `packages/was_v7/src/*`
- `packages/devtools/src/*`
- `packages/testing/src/*`

`packages/create` 负责 `create-stratix`，`packages/forge` 负责项目内 `stratix` 命令。

## 在业务项目里

优先看：

- `node_modules/@stratix/create/package.json`
- `node_modules/@stratix/forge/package.json`
- `node_modules/@stratix/core/package.json`
- `node_modules/@stratix/database/package.json`
- `node_modules/@stratix/*/dist/**/*.js`
- `node_modules/@stratix/*/dist/types/**/*.d.ts`

当前发布包通常包含：

- `dist`
- `templates` 或插件资源模板
- `README.md`
- `LICENSE`

普通业务项目找不到 `packages/*/src` 是正常现象。

## 使用规则

- 想确认“怎么用”：先看项目 README、`.stratix/project.json`、`src/stratix.config.ts` 和 `dist/types`。
- 想确认“CLI 真支持什么”：看 `@stratix/create` / `@stratix/forge` 的命令源码或直接跑 `list`。
- 想确认“运行时到底怎么做”：看 `@stratix/core` 的 `dist` 或源码仓库 `packages/core/src`。
- 不要把历史 README 中的旧 `@stratix/cli`、`@Controller('/prefix')` 或 tasks preset 叙事当作当前事实。

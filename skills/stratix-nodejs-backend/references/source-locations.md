# Stratix 源码与编译产物定位

当这个 skill 提到 `packages/core/src/...`、`packages/database/src/...` 这类路径时，指的是 Stratix 源码仓库中的“权威实现位置”。如果你当前做的是一个普通业务项目，通常不会有这些目录。

## 场景一：你就在 Stratix 源码仓库里

可以直接按下面的路径读源码：

- `packages/core/src/*`
- `packages/database/src/*`
- `packages/redis/src/*`
- `packages/queue/src/*`
- `packages/ossp/src/*`
- `packages/tasks/src/*`
- `packages/was_v7/src/*`

这类路径最适合确认真实运行机制和历史差异。

## 场景二：你在消费 npm 包的业务项目里

优先看 `node_modules` 中的三个位置：

- 包入口与发布内容
  - `node_modules/@stratix/core/package.json`
  - `node_modules/@stratix/database/package.json`
- 运行时代码
  - `node_modules/@stratix/core/dist/**/*.js`
  - `node_modules/@stratix/database/dist/**/*.js`
- 类型声明
  - `node_modules/@stratix/core/dist/types/**/*.d.ts`
  - `node_modules/@stratix/database/dist/types/**/*.d.ts`

以当前包为例：

- `@stratix/core` 的 `package.json` 指向：
  - `main = dist/index.js`
  - `types = dist/types/index.d.ts`
  - `bin = dist/bin/stratix.js`
- `@stratix/database` 的 `package.json` 指向：
  - `main = dist/index.js`
  - `types = dist/types/index.d.ts`

## 为什么业务项目里找不到 `src`

当前这些包发布到 npm 时，`files` 里主要包含：

- `dist`
- `README.md`
- `LICENSE`

这意味着普通业务项目通常只能拿到编译产物和类型声明，拿不到 monorepo 里的 TypeScript `src`。

## 实际使用建议

- 想确认“怎么用”：先看 `README.md`、`dist/types/**/*.d.ts`
- 想确认“运行时到底怎么做”：看 `dist/**/*.js`
- 想确认“作者真实源码结构和完整上下文”：回到 Stratix 源码仓库的 `packages/*/src`

## 给 skill 的使用规则

- 在源码仓库里工作时，直接引用 `packages/*/src`。
- 在业务项目里工作时，把这些路径映射为 `node_modules/@stratix/*/dist` 与 `dist/types`。
- 如果当前工作区没有源码仓库，不要假设 `packages/*/src` 本地一定存在。

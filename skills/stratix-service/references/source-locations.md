# Stratix 事实源与读取顺序

## 权威仓库

本机 Stratix 框架仓库：

```text
/Users/uroborus/NodeProject/wps/obsync-root
```

2026-07-27 当前 checkout：

- 分支：`1.1.0`
- `@stratix/core@1.1.2`
- `@stratix/create@1.1.2`
- `@stratix/forge@1.1.4`
- `@stratix/database@1.1.1`
- `@stratix/testing@1.0.0-beta.1`

这些是本地快照，不是永久 latest。处理其他项目时先查项目实际安装版本。

## 开发任务必读

先读仓库协作规则：

- `AGENTS.md`
- `.factory/memory/current-state.md` 中与目标能力直接相关的当前事实

再按任务回源：

### 配置与创建模板

- `packages/create/src/template/generated-files.ts`
- `packages/create/templates/apps/<type>/manifest.json`
- `packages/forge/src/template/generated-files.ts`
- `packages/core/src/types/config.ts`
- `packages/core/src/config/schema.ts`

### 环境与加密

- `packages/core/src/utils/environment/env.ts`
- `packages/core/src/utils/crypto.ts`
- `packages/core/src/bootstrap/application-bootstrap.ts`
- `packages/forge/src/commands/config/index.ts`
- `packages/forge/src/utils/config-crypto.ts`

### 三层、模块与生成器

- `packages/forge/templates/resources/controller`
- `packages/forge/templates/resources/service`
- `packages/forge/templates/resources/repository`
- `packages/forge/templates/resources/business-repository`
- `packages/forge/templates/resources/module`
- `packages/forge/src/commands/generate/index.ts`
- `packages/forge/src/modules/module-analysis.ts`

### Repository 与 Kysely

- `packages/database/src/index.ts`
- `packages/database/src/config/base-repository.ts`
- `packages/database/src/types/configuration.ts`

### 测试模式与模块 manifest

- `packages/testing/src/test-platform.ts`
- `packages/testing/src/test-factory.ts`
- `packages/testing/src/__tests__/test-platform.test.ts`

## 正式应用后端指南

至少按改动范围读取：

- `docs/03-developer-guide/应用后端开发/architecture-conventions.md`
- `docs/03-developer-guide/应用后端开发/project-structure.md`
- `docs/03-developer-guide/应用后端开发/database-quickstart.md`
- `docs/03-developer-guide/应用后端开发/database-crud.md`
- `docs/03-developer-guide/应用后端开发/from-crud-to-modules.md`
- `docs/03-developer-guide/应用后端开发/testing-and-debugging.md`
- `docs/03-developer-guide/应用后端开发/development-workflow.md`

指南与当前生成器冲突时，不复制旧示例。例如当前 create 源码直接生成 `src/stratix.config.ts`；不要仅因旧指南提到 `src/config/stratix.generated.ts` 就在业务项目中虚构该层。

## 业务项目

没有框架源码时优先看：

- `package.json`、lockfile、`.stratix/project.json`
- `src/stratix.config.ts`
- `node_modules/@stratix/*/package.json`
- `node_modules/@stratix/*/dist/types/**/*.d.ts`
- `pnpm exec stratix --help`

不要把历史 README、旧 `@stratix/cli`、Nest 风格 `@Controller('/prefix')` 或已移除的配置字段当成当前事实。

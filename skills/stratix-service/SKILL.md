---
name: stratix-service
description: 使用 Stratix 工具链开发、重构、调试和评审 Stratix 后端服务、API、worker、sync、gateway、插件和管理后台后端接口配套项目。仅在用户明确提到 Stratix、create-stratix、stratix CLI、@stratix/create、@stratix/forge、@stratix/core、@stratix/database、stratix.config.ts、STRATIX_SENSITIVE_CONFIG、STRATIX_ENCRYPTION_KEY、withRegisterAutoDI、controller/service/repository、Kysely、module.yaml、插件或 preset 选择，或当前仓库事实显示使用 Stratix 时必须使用；普通 Node/Fastify、Go、Rust 或非 Stratix 项目不触发。
---

# Stratix Service

本 skill 已把 Stratix 框架实现提炼为可复用开发规范。业务项目直接遵循本 skill 的规范，不要求业务项目读取 Stratix 框架源码，也不要凭其他框架经验补 Nest 风格模块、配置服务或数据访问层。

## 规范入口

按任务读取：

- 新建或修改 API、模块、Controller、Service、Repository、Kysely：必须读 [application development](references/application-development.md)。
- 读取环境、测试模式、`STRATIX_ENCRYPTION_KEY`、加解密：必须读 [environment config](references/environment-config.md)。
- 创建项目、生成资源、加 preset、诊断或发布：读 [CLI workflow](references/cli-workflow.md)。
- 插件和 preset 选择：读 [ecosystem map](references/ecosystem-map.md)。
- 启动、discovery、DI 或插件 token 排错：读 [runtime realities](references/runtime-realities.md)。
- Stratix `app web-admin`、`admin-page`、`admin-crud` 的前端页面交给 `stratix-admin-web`；本 skill 只负责其后端接口和服务。

## 适用版本

本规范适用于 `@stratix/core@1.1.2`、`@stratix/forge@1.1.4`、`@stratix/create@1.1.2`、`@stratix/database@1.1.1` 和 `@stratix/testing@1.0.0-beta.1`。业务项目直接遵循本规范，无需读取框架源码；目标项目使用其他版本或缺少本文所列 CLI 能力时，报告兼容性差异，由本 skill 维护者更新规范，不由业务项目自行研究源码形成新规则。

## 版本兼容门

先从 `package.json`、lockfile 和已安装 `node_modules/@stratix/*/package.json` 交叉读取每个相关包的实际版本；本 checker 要求 lockfile 为 `pnpm-lock.yaml`。不能假设各包同版。运行 `python <skill-dir>/scripts/check_compatibility.py <project>`，它按固定矩阵验证 package、lock 和已安装版本，并在矩阵通过后实际执行 `pnpm exec stratix --help` 和 `pnpm exec stratix doctor`；只有两条 smoke 都退出 0 才通过版本门。支持矩阵是：`@stratix/core`: `1.1.2`、`@stratix/forge`: `1.1.4`、`@stratix/create`: `1.1.2`、`@stratix/database`: `1.1.1`、`@stratix/testing`: `1.0.0-beta.1`。仅当每个相关包与本 skill 的支持矩阵兼容时，才沿用命令和规则。

未知或不匹配时，立即 `blocked`；不运行生成、doctor、build、release 或其他会改变目标项目的命令，不自动安装或升级。回执逐包列出每个相关包的 `detected`、`required`、`difference`，再列未执行命令和唯一 `next_required_action`（补齐版本事实、切换到兼容版本，或要求维护者更新矩阵之一）。

## 默认流程

1. 先通过版本兼容门；从 `package.json`、lockfile 和 `node_modules/@stratix/*/package.json` 确认实际版本。
2. 用项目内 `pnpm exec stratix --help`、`list templates`、`list presets` 确认可用命令；创建器用 `create-stratix`。
3. 先生成最小骨架，再检查生成文件；不要手写猜测模板。
4. 新功能先确定业务域。简单项目使用根级三层；业务增长后使用 `src/modules/<domain>/` 收拢同一套三层。
5. 按 `repository -> service -> controller` 实现；HTTP 只在 Controller，业务编排只在 Service，数据库和 Kysely 只在 Repository。
6. 配置只在 `src/stratix.config.ts` 总装；敏感业务配置只从函数参数 `sensitiveConfig` 映射。
7. 运行最小相关测试、`stratix doctor` 和 build；发布时再运行完整发布门。

## 不变量

- `src/stratix.config.ts` 默认导出 `(sensitiveConfig = {}) => StratixConfig`。
- `STRATIX_SENSITIVE_CONFIG` 由 Core 启动期解密，再作为参数传给配置函数；业务类不自行解密。
- `STRATIX_ENCRYPTION_KEY` 由 Forge/Core 从进程环境读取；CLI 不接受 `--key`。
- 测试模式使用 `isTest()`；不要散落比较 `process.env.NODE_ENV`。
- `module.yaml` 是 Forge、doctor、graph、testing 使用的工程治理 manifest，不是运行时注册或业务配置入口。
- Controller、Service、Repository 分别使用 `@Controller()`、`@Service()`、`@Repository()`。
- `@Controller()` 不接收路由前缀；路径写在方法装饰器，统一前缀放 `discovery.routing.prefix`。
- Repository 继承 `BaseRepository` 时显式注入 `DatabaseConnectionProvider` 并调用 `super({ database })`。
- `BaseRepository.query()` / `command()` 返回 `Either`；Repository 内解包，不能把 `Either` 泄漏给 Service。
- Service 不注入数据库 provider、Kysely 或数据库插件。
- 多表一致性、状态迁移、claim/checkpoint/finalize 才使用 `business-repository`；普通 CRUD 不加。
- 新项目不使用已移除的 `@stratix/tasks`。

## 最小实现

- 只有 1–3 个简单资源时，不创建模块层或额外 domain abstraction。
- 当同一业务域文件增多、跨多表或多人协作时，用 `stratix generate module <name>`。
- 领域规则有真实复用或复杂不变量时，放在模块内无装饰器的纯函数/类型中，由 Service 调用；不让 domain 依赖 Fastify、Stratix 装饰器或 Kysely。
- 已有生成骨架和框架 API 能完成时，不新增 manager、factory、registry 或包装层。
- 不简化输入校验、敏感配置、数据一致性、错误处理和发布门。

## 验证

| 场景 | 最小验证 |
|---|---|
| 解释 / 评审 | 核对实际版本和项目代码是否遵守本规范。 |
| 局部实现 | 相关测试、`pnpm exec stratix doctor`、`pnpm build`。 |
| 模块变更 | 再跑 `stratix doctor modules` 和模块测试。 |
| API 契约 | 再跑目标 inject/contract test 与 OpenAPI 生成。 |
| 发布 | 测试、build、doctor、manifest、release gate、OpenAPI、真实 start、decrypt 和 runtime injection 全部新鲜通过。 |

任一必需验证失败，只能报告真实失败或 `blocked`，不得用手写兼容层掩盖框架/模板问题。

## 输出

说明实际版本、选择的 template/preset、修改路径、分层链路、执行命令和真实结果。

```text
工作结果：
- work_item: <WORKITEM-ID or none>
- skill: stratix-service
- status: ready_for_review | blocked | needs_user_input
- outputs:
  - <path>
- evidence:
  - <命令或报告>
- ledger_event: <event id or none>
- needs:
  - review | verification | user_input | none
```

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。

---
name: stratix-nodejs-backend
description: 使用 @stratix/cli@1.1.0、@stratix/core@1.1.0、@stratix/database@1.1.0 及 Stratix 生态开发、重构、调试和评审 Node.js 后端项目。当用户提到 Stratix、@stratix/cli、@stratix/core、@stratix/database、stratix.config.ts、withRegisterAutoDI、控制器/服务/仓储/执行器、应用自动发现，或生态插件集成（database、redis、tasks、ossp、queue、was-v7、devtools、testing）时必须使用此技能。
---

# Stratix Node.js Backend

用于约束基于 Stratix 当前 1.1.x 稳定组合的 Node.js 后端开发。当前仓库可核对到的真实版本是 `@stratix/cli@1.1.0`、`@stratix/core@1.1.0`、`@stratix/database@1.1.0`。如果用户口头说“core 1.10”，但本地包版本是 `1.1.0`，以本地真实版本为准。

## 版本锚点

- CLI 已从 core 中独立，工程化动作优先使用 `@stratix/cli`。
- core 负责 runtime、DI、discovery、装饰器和 `withRegisterAutoDI`。
- database 1.1.0 是 repository-first 模型，应用侧数据库访问优先 `BaseRepository`。

## CLI 优先

- 新项目、插件、模块、资源生成，默认先用 `stratix` CLI，不先手写目录和样板文件。
- 只有当 CLI 当前能力覆盖不到目标时，才补充手写代码。
- 初始化项目前，优先先看 `stratix list templates`、`stratix list presets`。
- 新建应用优先使用 `stratix init app <type> <name>`。
- 新建插件优先使用 `stratix init plugin <type> <name>`。
- 新增业务资源优先使用 `stratix generate resource|controller|service|repository|business-repository|executor|module <name>`。
- 新增插件内部资源优先使用 `stratix generate plugin-adapter|plugin-service|plugin-controller|plugin-executor <name>`。
- 新增生态能力优先使用 `stratix add preset <preset-id>`，不要手工拼依赖和配置。
- 数据库项目优先先加 `database` preset，再生成 `repository` 或 `business-repository`。
- 多表业务单元、工作流状态机、checkpoint/outbox 场景优先 `stratix generate business-repository <name>`。
- 大改结构前后优先运行 `stratix doctor`。
- 启动应用优先使用 `stratix start --type <web|cli|worker|service>`。
- 配置加解密优先使用 `stratix config encrypt|decrypt|validate|generate-key`。

## 核心规范

- 配置主入口优先 `src/stratix.config.ts`。
- `@Controller()` 不接收前缀。
- 路由前缀不要依赖 `applicationAutoDI.routing.prefix` 或插件 `AutoDIConfig.routing.prefix`。
- 应用自动发现默认扫描 `src`，扫描到的任意 class 都可能被当作 service/controller/executor。
- 项目分层固定为 `controller -> service -> repository`。
- 服务层不直接注入或调用 `databaseApi` / database plugin，持久化统一收敛到 repository。
- `@stratix/database@1.1.0` 的应用侧首选公共 API 是 `BaseRepository`；`databaseApi` 只允许留在 repository 的兼容或过渡代码里。
- 新插件的默认导出应包装“具名插件函数”到 `withRegisterAutoDI(...)`，不要导出匿名插件函数。
- 插件适配器对外 token 前缀来自“插件函数名”，不是 `PluginConfig.name`。
- `plugins[].name` 只用于插件注册、日志和配置定位，不决定 adapter token。
- 需要插件默认值清洗或启动前拦截时，优先实现 `parameterProcessor` 与 `parameterValidator`。

## 应用开发规则

- 入口优先使用 `src/index.ts` + `src/stratix.config.ts`。
- 如果需求是“创建应用骨架”，优先用 `stratix init app api|gateway|worker|sync|cli|service <name>`。
- 常规目录优先使用 `controllers/`、`services/`、`repositories/`、`executors/`、`config/`。
- 数据库 preset 默认环境变量使用 `DB_HOST`、`DB_PORT`、`DB_NAME`、`DB_USERNAME`、`DB_PASSWORD`。
- Controller 只负责协议层、请求响应和参数转发。
- Service 只负责业务编排、跨服务协作和流程组织。
- Repository 是唯一允许直接承接数据库访问的应用层；优先在 repository 中继承 `BaseRepository`。
- 跨表一致性单元、长流程状态迁移、claim/checkpoint/finalize 逻辑优先收敛到 business repository，不要在 service 中手工拼多仓储 SQL。
- 默认把 `src/controllers`、`src/services`、`src/repositories`、`src/executors` 视为扫描目录，不要把普通工具类随意放进这些目录。
- 执行器位于应用 `src` 下时，只要 `@stratix/tasks` 已启用即可。
- 如果需求是“新建一组标准业务层”，优先用 `stratix generate resource <name>`；如果需求天然是数据库业务单元，优先用 `stratix generate business-repository <name>`。

## 插件开发规则

- 如果需求是“创建插件骨架”，优先用 `stratix init plugin adapter|integration|executor|data <name>`。
- 插件主入口优先使用“具名插件函数 + `withRegisterAutoDI(...)` 默认导出”。
- 保持插件函数名稳定，因为它会影响 adapter 对外 token。
- 插件内部对象放在 `controllers/`、`services/`、`repositories/`、`executors/`，对外适配器放在 `adapters/`。
- 需要对外暴露能力时，优先通过 adapter 暴露根容器 token，而不是暴露内部 service 名称。
- 插件内部如果有持久化逻辑，也保持 `controller -> service -> repository` 分层，并优先让 repository 继承 `BaseRepository`。
- 插件内部 executors 依赖 `@stratix/tasks` 先完成注册。
- 需要参数清洗和校验时，优先提供 `parameterProcessor` 与 `parameterValidator`；插件有内部资源时开启 `lifecycle`。

## 评审清单

- 能用 `stratix` CLI 完成的初始化、资源生成、preset 注入，是否仍然被手工实现了
- 是否错误假设 CLI 仍属于 `@stratix/core`
- 是否把 `@stratix/database@1.1.0` 仍然当成 `databaseApi` 优先模型来写新代码
- 是否错误使用了 `@Controller('/prefix')`
- 是否错误依赖 `Stratix.run({ config })`
- 是否把非 DI class 放进应用扫描目录
- 是否让服务层越过 repository 直接访问 database plugin
- 是否把多表一致性单元错误拆散到多个 service / repository 调用里
- 是否误把 `PluginConfig.name` 当成 adapter token 前缀来源
- 是否在 tasks 插件之前注册了插件内 executors
- 是否引用了源码中已经不存在的旧模块名

## 按需加载资料

- 常规 CLI 命令与推荐工作流：`references/cli-workflow.md`
- 常规开发模板与目录参考：`references/scaffolds.md`
- 常规生态 token 与依赖关系：`references/ecosystem-map.md`

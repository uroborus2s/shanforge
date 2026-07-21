---
name: stratix-service
description: 使用 Stratix 工具链开发、重构、调试和评审 Stratix 后端服务、API、worker、sync、gateway、插件和管理后台后端接口配套项目。仅在用户明确提到 Stratix、create-stratix、stratix CLI、@stratix/create、@stratix/forge、@stratix/core、@stratix/database、stratix.config.ts、STRATIX_SENSITIVE_CONFIG、withRegisterAutoDI、controller/service/repository、插件或 preset 选择，或当前仓库事实显示使用 Stratix 时必须使用；普通后端、Go 后端、Rust 后端或非 Stratix Node/Fastify 项目不触发。
---

# Stratix Service

用于 Stratix 后端开发。先探测版本和 CLI 能力，再选最小 template / preset，最后按业务补最少手写代码。不要把历史版本命令当成永久事实。

## 适用边界

适用于：

- Stratix API、service、worker、sync、gateway、CLI 应用。
- Stratix 插件、preset 选择、DI、controller / service / repository。
- `stratix.config.ts`、`STRATIX_SENSITIVE_CONFIG`、配置加解密和生产发布门禁。
- Stratix 管理后台的后端接口、权限接口和数据服务。

不适用于：

- 非 Stratix 后端项目。
- 只需要解释 TypeScript、Fastify、数据库或 CI 的通用问题。
- Stratix `app web-admin`、`admin-page`、`admin-crud` 的前端页面、公共 UI、表格表单和交互开发；交给 `stratix-admin-web`。
- Shanforge review gate、人工确认或本地提交。

## 分级验证

| 场景 | 最小动作 |
|---|---|
| 解释 / 方案 | 查版本事实和项目上下文；说明命令以 `--help` 为准。 |
| 代码评审 | 核对层级、preset、DI、配置安全门和已运行命令。 |
| 小修 | 复用现有 controller / service / repository；跑相关测试和 `stratix doctor` 或等价诊断。 |
| 新项目 | 先查 npm dist-tags 和 CLI list，再用最小 template / preset。 |
| 上线 / 生产化 | 跑完整发布门禁；任一关键项失败只能 `blocked`。 |

## 总原则

- 先查 npm dist-tags，再查项目实际安装版本。
- 新项目优先 npm latest；已有项目以项目实际安装版本为准。
- 项目内优先使用 `pnpm exec stratix`，避免旧全局二进制污染。
- 如果 `create-stratix list` 或 `stratix list` 失败，先用 `--help` 或 npm 包版本确认新命令；不得猜测 template、preset 或插件名。
- 只选择业务明确需要的插件；不要为了“完整”默认加 `database`、`redis`、`queue`、`ossp` 或 `was-v7`。
- 能用 `create-stratix` 或 `stratix` 生成的骨架，不手写起步目录。
- 手写代码只补业务逻辑、字段映射、插件配置、测试和 CLI 未覆盖的部分。
- 不再推荐旧的单包 `@stratix/cli` 口径；当前工具链分为 `@stratix/create` 和 `@stratix/forge`。
- `@stratix/tasks` preset 已移除；新项目不要再把 tasks 当作默认插件或执行器底座。

## Ponytail 约束

- 不为“以后可能”新增 preset、插件、配置、manager、helper、factory 或接口。
- 已有 controller / service / repository / BaseRepository / business-repository / `withRegisterAutoDI(...)` 能覆盖时，照项目现有模式补最小差异。
- 能靠数据库约束、Stratix 配置校验、Fastify schema 或 TypeScript 类型解决的，不再写一层运行时代码。
- 有意保留简化实现时，用 `ponytail:` 注释写明上限和升级条件。
- 不简化安全边界、输入校验、数据一致性、敏感配置、错误处理和生产交付 gate。
- 不新增中间层，除非当前业务已经有两个以上真实使用者。

## 版本与能力探测

先查：

```bash
npm view @stratix/create dist-tags --json
npm view @stratix/forge dist-tags --json
npm view @stratix/core dist-tags --json
npm view @stratix/database dist-tags --json
```

再查项目实际安装版本：

- `package.json`
- lockfile
- `node_modules/@stratix/*/package.json`
- `pnpm exec stratix --help`

不要假设 `create`、`forge`、`core`、`database` 版本号相同。示例命令只是候选，最终以项目内 `--help` 和实际版本为准。

## 执行流程

1. 判断目标类型：API、service、worker、sync、gateway、CLI、插件或管理后台后端接口。
2. 查看可用 template 和 preset。
3. 选择最小 preset：只做 HTTP 保持 `core`；落库加 `database`；缓存或锁加 `redis`；队列加 `queue` 且保证 `redis`；对象存储加 `ossp`；WPS / WAS V7 集成加 `was-v7`。
4. 新建 API 示例优先保持最小测试基线：`create-stratix app api my-api --preset testing --no-install`。
5. 生成骨架后按 `repository -> service -> controller` 补业务实现；已有层级能承担职责时，不新增中间层。
6. 通过配置安全门。
7. 小修跑相关测试和诊断；上线前再跑 production manifest、release gate、`stratix start` 和 runtime injection。

完整 CLI、obsync-root 根命令和历史兼容事实见 [CLI workflow](references/cli-workflow.md)。

## 配置安全门

- 新生成应用的配置默认全部来自 `sensitiveConfig`。
- 生成 `src/stratix.config.ts` 时，应用配置、插件配置和 provider 凭据默认只读 `sensitiveConfig`。
- 不得用 `DB_HOST`、`REDIS_HOST`、`WPS_APP_SECRET` 等普通环境变量作为配置回退。
- 普通 `.env` 只保留 `NODE_ENV`、`STRATIX_SENSITIVE_CONFIG`、`STRATIX_ENCRYPTION_KEY` 和进程启动必需变量。
- 先校验 JSON，再用显式 `STRATIX_ENCRYPTION_KEY` 加密，并把结果作为进程环境变量注入。
- 跑一次 decrypt，并跑真实启动或等价 runtime injection。
- 不能完成加密、解密和注入验证时，结论只能是 blocked；不要声明生成应用可上线。

加解密细节见 [environment config](references/environment-config.md)。

## 生产化归因

生产化或测试本 skill 生成项目时，才跑双项目矩阵：

- skill 生成项目：按本 skill 的配置安全门和生产标准生成、修正并验证。
- 官方对照项目：只用官方 latest 模板和项目依赖安装，不做 skill 手写修正。
- 两个项目跑同一命令矩阵，至少覆盖安装、版本检查、`doctor`、测试、build、manifest、release gate、OpenAPI、`stratix start`、decrypt 和 runtime injection。
- 如果官方 latest 模板也失败，归因为工具链或模板问题；记录版本、命令和 stderr，状态为 `blocked`。
- 如果只有 skill 生成项目失败，归因为 skill 或生成内容问题，先修复。
- 如果官方模板默认从 `process.env.PORT` 或普通 `.env` 读取应用配置，生产项目必须改为从 `sensitiveConfig` 读取。
- 只有 `doctor`、测试、build、manifest、release gate、OpenAPI、`stratix start` 和 runtime injection 全部新鲜通过，才能声明生成应用可上线。

## 编码规则

- 配置主入口是 `src/stratix.config.ts`，默认导出函数：`(sensitiveConfig = {}) => StratixConfig`。
- Controller 只处理协议、参数和响应；Service 只做业务编排；Repository 承接数据访问。
- 数据库代码优先继承 `BaseRepository`；Service 不直接注入 `databaseApi` 或数据库插件。
- 多表一致性、状态机、claim / checkpoint / finalize 优先放进 `business-repository`。
- `@Controller()` 不接收路由前缀；路由路径写在方法装饰器上。
- 不把普通 class 随意放进自动发现目录。
- 插件默认导出保持“具名插件函数 + `withRegisterAutoDI(...)`”；插件函数名会影响 adapter token。
- `plugins[].name` 用于注册、日志和配置定位，不决定 adapter token。

插件和 preset 决策见 [ecosystem map](references/ecosystem-map.md)，运行时事实见 [runtime realities](references/runtime-realities.md)。

## 输出契约

交付时说明：

- 探测到的 Stratix 包版本、CLI 能力和命令来源。
- 选择的项目类型、template、preset 和插件，以及未选择项。
- 修改路径和业务实现范围。
- 新鲜运行的命令、结果和失败 stderr。
- 配置安全门、production manifest、release gate、start、decrypt 和 runtime injection 状态。

Shanforge 状态包：

```text
工作结果：
- work_item: <WORKITEM-ID or none>
- skill: stratix-service
- status: ready_for_review | blocked | needs_user_input
- outputs:
  - <path>
- evidence:
  - <命令记录或报告路径>
- ledger_event: <event id or none>
- needs:
  - review | verification | user_input | none
```

`blocked` 表示无法证明 Stratix 生成物或运行链路安全可用。常见原因包括 CLI 能力探测失败、官方模板同样失败、配置加解密或 runtime injection 失败、release gate/start 未通过、业务必需外部系统信息缺失。blocked 时保留版本、命令和 stderr，不用手写绕过替代验证。

`needs_user_input` 用于必须由用户决定业务边界、外部系统、插件/preset 取舍或上线策略的情况。

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。

# Stratix CLI 1.1.0 Workflow

当前工作流以本仓库真实版本为准：

- `@stratix/cli@1.1.0`
- `@stratix/core@1.1.0`
- `@stratix/database@1.1.0`

优先使用下面这些命令，而不是手写项目骨架。

## 已完成源码级测试的命令

- `stratix init app api <name>`
- `stratix init plugin data <name>`
- `stratix generate resource <name>`
- `stratix add preset <preset-id>`
- `stratix doctor`
- `stratix start --type <type> --config <path> --host <host> --port <port>`
- `stratix config encrypt <file>`
- `stratix config decrypt <encrypted-string> --output <file>`
- `stratix config validate <file>`
- `stratix config generate-key`
- `stratix list templates`
- `stratix list presets`

## 当前推荐但本轮未单独回归的命令

- `stratix generate business-repository <name>`
- `stratix init app worker <name> --preset redis,queue,tasks`
- `stratix init plugin executor <name>`

## 推荐工作流

1. 查看能力
- `stratix list templates`
- `stratix list presets`

2. 初始化项目
- `stratix init app api demo-api --no-install`
- `stratix init app worker demo-worker --preset redis,queue,tasks --no-install`
- `stratix init plugin data @demo/data-plugin --no-install`

3. 生成标准分层资源
- `stratix generate resource order-item`
- `stratix generate module schedule-sync`
- `stratix generate executor sync-job`
- `stratix generate business-repository workflow-execution`

4. 注入生态能力
- `stratix add preset database --no-install`
- `stratix add preset redis --no-install`
- `stratix add preset tasks --no-install`

5. 结构校验
- `stratix doctor`

6. 启动应用
- `stratix start --type web --config ./src/stratix.config.ts`
- `stratix start --type worker --config ./config/worker.json`

7. 配置处理
- `stratix config generate-key`
- `stratix config encrypt prod.env.json`
- `stratix config decrypt "<encrypted>" --output ./tmp/decrypted.json`
- `stratix config validate prod.env.json`

## 使用约束

- 创建应用或插件时，先用 `init`，不要直接手工新建 `src/index.ts` 和 `src/stratix.config.ts`。
- 创建一组标准 `controller -> service -> repository` 时，先用 `generate resource`。
- 对数据库型项目，先 `add preset database`，再决定生成 `repository` 还是 `business-repository`。
- `@stratix/database@1.1.0` 的新代码应优先继承 `BaseRepository`；`databaseApi` 只保留在 repository 的兼容或迁移路径里。
- Service 层仍然禁止直接访问 `@stratix/database` / `databaseApi`，即使资源是 CLI 生成的。
- 插件默认导出应是 `withRegisterAutoDI(具名插件函数, config)`；`plugins[].name` 不决定 adapter token。
- `doctor` 只通过后，才把生成结果视为结构合格。

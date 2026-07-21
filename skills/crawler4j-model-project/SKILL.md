---
name: crawler4j-model-project
description: 使用 crawler4j `0.4.0` 的 `core-native-v2` 模块协议创建、迁移、调试、校验、打包和发布标准模块项目。当任务涉及 crawler4j、crawler4j-sdk、crawler4j-contracts、`crawler4j module init`、`module.yaml`、`.crawler4j/manifest.lock.json`、`@workflow`、`@page_action`、`@data_table`、Hosted UI、DevLink、本地 ZIP 安装，或把旧 `TaskScript` / `TaskFlow` / `TaskSpec` / `WorkflowSpec` 模块升级到 `0.4.0` 时必须使用此技能。
---

# Crawler4j Model Project

用于 `crawler4j` `0.4.0` 生态中的标准模块项目开发。这里的“模块项目”指由 `crawler4j-sdk` CLI `module init` 生成、由 Core 通过 `core-native-v2` 扫描器加载、并以 `module.yaml + .crawler4j/manifest.lock.json` 为发布契约的模块，不是仓内其他 `model` 或 `src/.../models` 目录。

## 当前版本事实

- `crawler4j` `0.4.0` 与 `crawler4j-sdk` `0.4.0` 只支持 `core-native-v2` 模块协议。
- 运行时 owner 只有 Core；模块运行时代码只依赖 `crawler4j-contracts`。
- `crawler4j-sdk` 只作为开发依赖，提供 CLI、脚手架、扫描、校验、manifest lock、打包、发布和宿主桥接。
- `module.yaml` 只保留模块元数据与升级源，工作流、页面操作、数据契约、宿主页、对象装配都改为代码装饰器声明后再由 SDK/Core 扫描。

## 先确认当前工作对象

- 当前目录存在 `module.yaml` 且 `module.yaml.runtime_api == core-native-v2` 时，把它视为 `0.4.0` 标准模块项目。
- 当前目录仍存在 `module_runtime.py`、`hooks/`、`env_selectors/`、`config_schema.json`、`strategy.yaml`，或代码里还有 `TaskScript` / `TaskFlow` / `TaskSpec` / `WorkflowSpec` / `EnvSelectorSpec`，把任务视为“旧模块迁移到 `0.4.0`”。
- 当前在 `crawler4j` Core / SDK 源码仓里时，如果任务是改 CLI、模板、扫描规则、模块契约或宿主安装链路，优先读取：
  - `packages/crawler4j-sdk/README.md`
  - `packages/crawler4j-sdk/src/cli/commands.py`
  - `packages/crawler4j-sdk/src/v2_scanner.py`
  - `packages/crawler4j/tests/integration/test_sdk_cli_module_mode.py`
  - `packages/crawler4j/tests/acceptance/README.md`

## CLI 优先

- 创建新模块项目时，先用：
  - `uvx --from crawler4j-sdk crawler4j module init`
  - 脚本化场景：`uvx --from crawler4j-sdk crawler4j module init <module_name> --repo owner/repo --no-git --no-install`
- 已进入模块项目后，优先用子命令生成和检查骨架：
  - `uv run crawler4j module show`
  - `uv run crawler4j interface create <name>`
  - `uv run crawler4j component create <name> --implements <interface>`
  - `uv run crawler4j workflow create <name>`
  - `uv run crawler4j page-action create <name>`
  - `uv run crawler4j data table create <name>`
  - `uv run crawler4j data query create <name> --source <table>`
  - `uv run crawler4j candidate create <name>`
  - `uv run crawler4j cleanup create <name>`
  - `uv run crawler4j page create <name>`
  - `uv run crawler4j manifest lock`
  - `uv run crawler4j check structure|release|full`
  - `uv run crawler4j package build`
  - `uv run crawler4j package verify dist/<module>-<version>.zip`
- 在 `crawler4j` SDK/Core 源码仓验证本地 CLI 时，优先用源码入口：
  - `uv run python -m crawler4j_sdk.cli.commands --help`
  - `uv run python -m crawler4j_sdk.cli.commands module init demo_module --repo demo/demo_module --no-git --no-install`
- 旧命令已经删除，不要继续使用：
  - `crawler4j init-model`
  - `crawler4j add`
  - `crawler4j new`
  - `crawler4j add-workflow`
  - `crawler4j add-ui`
  - `crawler4j list`

## 模块协议与目录

- `module.yaml` 至少应包含：
  - `name`
  - `runtime_api: core-native-v2`
  - `version`
  - `upgrade_source.type: github_release`
  - `upgrade_source.repo: owner/repo`
  - `config_defaults.module`
- 标准目录以 `interfaces/`、`objects/`、`workflows/`、`tasks/`、`data/`、`pages/`、`candidates/` 为核心；`cleanups/` 为环境清理候选入口，通常也应保留。
- `.crawler4j/manifest.lock.json` 是 `0.4.0` 的正式扫描产物；打包、正式安装和外部模块校验前都要确保它是最新的。
- Hosted UI 已改成 `pages/*.py` 或 `pages/<group>/*.py` 下的 `@page(...)` 声明，不再走 `config_schema.json` / `ui/` / `strategy.yaml`。
- 模块目录名、Python 包名、`module.yaml.name` 默认保持一致，并且必须是可导入的 `snake_case`。
- `pyproject.toml` 只负责模块开发环境；运行时依赖只放 `crawler4j-contracts`，开发依赖才加 `crawler4j-sdk`。

## 硬限制

- 模块运行时代码禁止 import `crawler4j-sdk`。
- 禁止继续导入或依赖：
  - `TaskSignal`
  - `TaskSignalAction`
  - `EnvAction`
  - `TaskScript`
  - `TaskFlow`
  - `ModuleAssembler`
  - `TaskSpec`
  - `WorkflowSpec`
  - `EnvSelectorSpec`
  - `PageSpec`
- `module.yaml` 不再允许声明：
  - `default_workflow`
  - `workflows`
  - `data`
  - `interfaces`
  - `objects`
  - `tasks`
  - `ui_extension`
  - `resource_pools`
  - `sdk_version_range`
- 不保留旧运行时薄壳或旧入口：
  - `module_runtime.py`
  - `hooks/`
  - `env_selectors/`
  - `config_schema.json`
  - `ui/`
  - `strategy.yaml`
- 数据访问统一走 `ctx.db`；不要再写旧 `ctx.tools.call("db.*")`，也不要直接连宿主数据库。
- 模块不要再依赖 `ctx.captured_data` 一类旧上下文字段。
- workflow/component 收尾统一实现 `cleanup(ctx, outcome)`；旧 `close()` / `aclose()` 生命周期方法会被完整校验阻断。
- 环境选择统一写在 `candidates/` 下的 `@env_candidates` 同步纯函数；批量环境清理统一写在 `cleanups/` 下的 `@env_cleanup_candidates` 同步纯函数。模块只声明候选 env id，不直接发送环境处置指令。

## 宿主集成与验收

- 本地源码调试优先走：
  - `uv run crawler4j host devlink add <module_root>`
  - `uv run crawler4j host debug config --module-root <module_root>`
- 目录源码不能走 `host install`；`install` 只支持：
  - 本地 ZIP
  - GitHub `owner/repo`
- 正式验收 gate 按顺序执行：
  - `crawler4j check structure`
  - `crawler4j check release`
  - `crawler4j check full`
  - `crawler4j package verify <zip>`
- 正式安装包当前只有单根目录 ZIP；不要把 `.whl` 当应用内模块安装格式。
- 本地 ZIP 预览/安装如只做隔离验收，可用：
  - `crawler4j host install preview <zip> --skip-remote-check`
  - `crawler4j host install apply <zip> --skip-remote-check`
- 如果模块需要正式升级链路，再补：
  - `crawler4j release status`
  - `crawler4j release check-remote`
  - `crawler4j release publish`

## 评审清单

- 是否还在沿用 `TaskScript` / `TaskFlow` 或旧 spec/selector/runtime surface。
- 是否继续手写 `module.yaml.workflows`、`ui_extension`、`config_schema.json` 之类的旧契约。
- 是否忘记运行 `crawler4j manifest lock`，导致 `.crawler4j/manifest.lock.json` 过期或缺失。
- 是否把目录源码误走 `host install`，而不是 `host devlink add`。
- 是否把 `.whl`、源码目录或多根 ZIP 当正式安装包。
- 是否在运行时代码里 import `crawler4j-sdk`、调用旧 `ctx.tools.call("db.*")`，或直接连接宿主数据库。
- 是否仍把环境管理写成模块侧动作，而不是 `@env_candidates` / `@env_cleanup_candidates` + 宿主确认。

## 按需加载资料

- `references/cli-workflow.md`
- `references/module-structure.md`
- `references/core-integration.md`

## 状态回写与失败语义

在 Shanforge work item 中使用时，输出标准状态包：

```text
工作结果：
- work_item: <WORKITEM-ID>
- skill: crawler4j-model-project
- status: ready_for_review | blocked | needs_user_input
- outputs:
  - <module path / package path / changed file path>
- evidence:
  - <crawler4j check / manifest lock / package verify output summary>
- ledger_event: <event id or none>
- needs:
  - review | verification | user_input | release_credentials | none
```

`blocked` 用于 CLI 不存在、当前版本与 `0.4.0` / `core-native-v2` 不匹配、结构校验失败、manifest lock 或 package verify 失败、仍存在禁止的旧运行时契约，且不能在允许范围内修复的情况。

`needs_user_input` 用于模块名、GitHub repo、升级源、发布凭据、是否执行破坏性迁移或宿主安装目标不明确的情况。

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。

---
name: crawler4j-model-project
description: 使用 crawler4j SDK CLI 创建、演进、调试和评审 crawler4j 标准 model/模块项目。当任务涉及 crawler4j、crawler4j-sdk、crawler4j init-model、module.yaml、TaskScript、TaskFlow、config_schema.json、DevLink、ATM 调试或标准模块包时必须使用此技能。
---

# Crawler4j Model Project

用于 `crawler4j` 生态中的标准 model/模块项目开发。这里的“model 项目”指由 `crawler4j` SDK CLI `init-model` 生成、并由 Core 运行时通过 `module.yaml` 与模块根 `__init__.py` 加载的模块项目，不是 `src/core/models/` 这种内部核心数据模型目录。

## 先确认当前工作对象

- 当前目录存在 `module.yaml` 时，把它视为标准 model/模块项目。
- 当前在 `crawler4j` Core 仓库里时，如果任务是改 CLI、模板、模块契约或验证链路，优先读取仓内 `crawler4j_sdk/cli/commands.py`、`crawler4j_sdk/README.md` 和模块开发文档，再修改源码与测试。
- 不把 wheel 元数据当成模块运行契约；Core 真正读取的是 `module.yaml` 和模块根 `__init__.py`。

## CLI 优先

- 创建新模块项目时，先用 `crawler4j init-model`，不要先手写目录骨架。
- 默认使用 PyPI 上当前最新发布的 `crawler4j-sdk`，不要在常规命令里写死版本号；只有在复现历史问题或用户明确要求时才临时钉住版本。
- 在已初始化模块项目内，优先用：
  - `uv run crawler4j new <task_name>`
  - `uv run crawler4j add-workflow <workflow_name>`
  - `uv run crawler4j add-ui`
  - `uv run crawler4j list`
- 在已发布 SDK 环境里，优先用：
  - `uvx --from crawler4j-sdk crawler4j init-model <module_name>`
- 在脚本、CI 或需要静默初始化时，优先加：
  - `--defaults --no-git --no-install`
- 在 `crawler4j` Core 源码仓里验证本地 CLI 时，优先用源码入口：
  - `uv run python -m crawler4j_sdk.cli.commands <subcommand>`
- 只有 CLI 当前能力覆盖不到的差异，才补充手写文件或 patch 生成结果。

## 目录与契约

- 模块根目录最少包含：`module.yaml`、`__init__.py`、`tasks/`、`workflows/`。
- `module.yaml.name`、目录名、Python 包名默认保持一致，避免 DevLink 和策略配置漂移。
- `config_schema.json` 是当前稳定的声明式配置 UI 路径。
- 模块项目里的 `pyproject.toml` 只负责本地开发环境，不代表宿主应用会自动安装这些依赖。
- 正式安装验收当前走 `zip` 包，不把 `.whl` 当应用内模块安装格式。

## 开发与验证

- 初始化后先做最小自检：
  - `uv sync`
  - `uv run crawler4j list`
- 先通过 CLI 生成 task / workflow / UI，再补充业务代码。
- 调试主路径是 `DevLink -> ATM 调试 -> IDE 附加 debugpy`，不要回退到旧版 `debug_runner.py` 工作流。
- 正式安装前至少做一次 `zip` 安装 smoke，验证 `module.yaml`、工作流注册和 UI 扩展可被 Core 识别。

## 评审清单

- 是否手写了本可由 CLI 生成的脚手架
- 是否破坏了 `module.yaml`、任务名、工作流名或模块根入口的一致性
- 是否把 `.whl` 错当成正式模块安装包
- 是否只把运行时依赖放进模块 `pyproject.toml`，却没有确认宿主环境可用
- 是否遗漏了 SDK CLI / 模板 / Core 契约的回归测试

## 按需加载资料

- `references/cli-workflow.md`
- `references/module-structure.md`
- `references/core-integration.md`

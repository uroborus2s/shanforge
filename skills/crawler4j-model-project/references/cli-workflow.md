# Crawler4j CLI 工作流

## 首选命令

- 常规场景默认使用 PyPI 上最新发布的 `crawler4j-sdk`，不要写死版本号。
- 已发布 SDK：
  - `uvx --from crawler4j-sdk crawler4j init-model <module_name>`
- 脚本或 CI：
  - `uvx --from crawler4j-sdk crawler4j init-model <module_name> --defaults --no-git --no-install`
- 已进入模块项目：
  - `uv run crawler4j new <task_name>`
  - `uv run crawler4j add-workflow <workflow_name>`
  - `uv run crawler4j add-ui`
  - `uv run crawler4j list`
- 在 `crawler4j` Core 源码仓验证本地 CLI：
  - `uv run python -m crawler4j_sdk.cli.commands --help`
  - `uv run python -m crawler4j_sdk.cli.commands init-model demo_model --defaults --no-git --no-install`

## 默认初始化语义

`init-model` 默认会：

- 进入交互式初始化向导
- 生成 `.gitignore`
- 生成 `.python-version`
- 执行 `git init`
- 执行 `uv sync`

如果当前任务只需要脚手架或测试夹具，优先关闭自动副作用：

- `--defaults`
- `--no-git`
- `--no-install`

## 何时禁止手写脚手架

以下场景默认不先手写：

- 新建模块项目
- 新增 task 文件骨架
- 新增 workflow 文件并注册到 `module.yaml`
- 新增声明式配置 UI

只有当 CLI 或模板本身就是待修改对象时，才直接改源码或模板文件。

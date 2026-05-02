# Crawler4j `0.4.0` CLI 工作流

## 首选命令

- 常规场景默认使用与当前 Core 兼容的 `crawler4j-sdk 0.4.0`，不要再写旧 `init-model` / `new` / `add-workflow` / `add-ui`。
- 创建模块项目：
  - `uvx --from crawler4j-sdk crawler4j module init`
  - 脚本或 CI：
    - `uvx --from crawler4j-sdk crawler4j module init <module_name> --repo owner/repo --no-git --no-install`
- 已进入模块项目：
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
  - `uv run crawler4j package verify <zip>`
- 在 `crawler4j` Core / SDK 源码仓验证本地 CLI：
  - `uv run python -m crawler4j_sdk.cli.commands --help`
  - `uv run python -m crawler4j_sdk.cli.commands module init demo_module --repo demo/demo_module --no-git --no-install`

## 默认初始化语义

`crawler4j module init` 默认会：

- 生成 `core-native-v2` 标准骨架
- 生成 `module.yaml`
- 生成 `.crawler4j/manifest.lock.json`
- 生成 `.gitignore`
- 生成 `.python-version`
- 生成基础 `README.md`、`pyproject.toml`、初始 workflow/page-action/page
- 执行 `git init`
- 执行 `uv sync`

如果当前任务只需要脚手架、测试夹具或 dry-run，优先关闭自动副作用：

- `--no-git`
- `--no-install`

## 何时禁止手写脚手架

以下场景默认不先手写：

- 新建模块项目
- 新增 `@interface` / `@component` / `@workflow` / `@page_action`
- 新增 `@data_table` / `@data_query`
- 新增 `@env_candidates` / `@env_cleanup_candidates`
- 新增 Hosted UI `@page`
- 生成或刷新 `.crawler4j/manifest.lock.json`
- 构建正式安装 ZIP

只有当 CLI 本身、模板本身或扫描/校验规则本身是待修改对象时，才直接改源码或模板文件。

## 已删除的旧命令

`0.4.0` 下，下列命令视为迁移信号，不要继续建议用户执行：

- `crawler4j init-model`
- `crawler4j add`
- `crawler4j task create`
- `crawler4j new`
- `crawler4j list`
- `crawler4j add-workflow`
- `crawler4j add-ui`
- `crawler4j add-data-table`
- `crawler4j add-data`

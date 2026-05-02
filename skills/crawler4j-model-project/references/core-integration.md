# Crawler4j `0.4.0` Core 集成

## 真实运行链路

当前最稳的模块开发链路：

```text
crawler4j module init
-> 用 CLI 补 interface / component / workflow / page_action / data / page / candidate / cleanup
-> crawler4j manifest lock
-> crawler4j check structure -> release -> full
-> crawler4j host devlink add <module_root>
-> crawler4j host debug config
-> 在宿主 ATM 中按真实任务调试
-> crawler4j package build
-> crawler4j package verify <zip>
-> crawler4j host install preview/apply <zip> [--skip-remote-check]
```

## 调试与宿主边界

- DevLink 绑定的是包含 `module.yaml` 的模块根目录。
- 目录源码只能走 `crawler4j host devlink add <module_root>`，不要走 `host install`。
- `host install` 只支持：
  - 本地 ZIP
  - GitHub `owner/repo`
- 本地调试配置由 `crawler4j host debug config` 生成 `.vscode/launch.json`；CLI 只负责 attach 配置，不负责托管调试会话生命周期。
- workflow / page_action / page / data / object 参数等运行描述来自 v2 scanner 和 `manifest.lock`，不再从 `module.yaml.workflows` 或 `ui_extension` 读取。

## 发布与安装约束

- 当前正式安装只支持单根目录 ZIP。
- 不要把 `.whl` 当成应用内模块安装格式。
- ZIP 安装前建议完整跑一遍：
  - `crawler4j check structure`
  - `crawler4j check release`
  - `crawler4j check full`
  - `crawler4j package verify <zip>`
- 模块 `pyproject.toml` 里的第三方依赖不会被宿主自动安装；运行时代码只能假设 `crawler4j-contracts` 和宿主注入能力存在。
- 如果本地 ZIP 只做离线验收，可在宿主安装预览/应用时加 `--skip-remote-check` 跳过 `upgrade_source.repo` 的远端校验。

## 在 Core / SDK 仓里优先阅读的位置

- `packages/crawler4j-sdk/README.md`
- `packages/crawler4j-sdk/src/cli/commands.py`
- `packages/crawler4j-sdk/src/v2_scanner.py`
- `packages/crawler4j/tests/integration/test_sdk_cli_module_mode.py`
- `packages/crawler4j/tests/acceptance/README.md`

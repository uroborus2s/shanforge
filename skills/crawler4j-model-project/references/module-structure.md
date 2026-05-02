# Crawler4j `0.4.0` 模块结构

## 标准目录

```text
<module_name>/
├── .crawler4j/
│   └── manifest.lock.json
├── __init__.py
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
├── module.yaml
├── interfaces/
├── objects/
├── workflows/
├── tasks/
├── data/
├── pages/
├── candidates/
└── cleanups/
```

`cleanups/` 在扫描规则中是正式入口；尽管最小结构校验主要强制 `interfaces/objects/workflows/tasks/data/pages/candidates`，实际模块项目通常也应保留 `cleanups/`。

## 关键契约

- `module.yaml`
  - 只保留模块元数据、`runtime_api`、`upgrade_source`、`config_defaults`
  - `runtime_api` 必须是 `core-native-v2`
  - `upgrade_source.type` 当前必须是 `github_release`
- `.crawler4j/manifest.lock.json`
  - 由 `crawler4j manifest lock` 生成
  - 是 `0.4.0` 发布、安装、宿主读取的重要扫描产物
- `__init__.py`
  - 只作为模块根包入口，不再承载运行时装配逻辑
- `interfaces/`
  - 放 `@interface`
- `objects/`
  - 放 `@component`
- `workflows/`
  - 放 `@workflow`
- `tasks/`
  - 放 `@page_action`
- `data/`
  - 放 `@data_table` / `@data_query`
- `pages/`
  - 放 Hosted UI `@page`
  - 既可平铺在 `pages/*.py`，也可按单层业务分组放在 `pages/<group>/*.py`
- `candidates/`
  - 放 `@env_candidates` 同步纯函数
- `cleanups/`
  - 放 `@env_cleanup_candidates` 同步纯函数

## 明确移除的旧结构

以下内容在 `0.4.0` 不再属于正式模块契约：

- `module_runtime.py`
- `hooks/`
- `env_selectors/`
- `config_schema.json`
- `ui/`
- `strategy.yaml`
- `module.yaml.default_workflow`
- `module.yaml.workflows`
- `module.yaml.data`
- `module.yaml.interfaces`
- `module.yaml.objects`
- `module.yaml.tasks`
- `module.yaml.ui_extension`
- `module.yaml.resource_pools`
- `config_defaults.workflows`

## 命名纪律

- 模块目录名、Python 包名、`module.yaml.name` 默认保持一致。
- `module.yaml.name` 必须是可导入的 `snake_case` 包名。
- workflow / page_action / page / data / interface / component 名称统一使用小写标识符。
- 任何需要被 Core 调度或扫描的名字，都必须同时校验文件名、装饰器声明名和 `manifest.lock` 结果。

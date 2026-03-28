# Crawler4j 模块结构

## 标准目录

```text
<module_name>/
├── __init__.py
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
├── module.yaml
├── config_schema.json
├── tasks/
│   ├── __init__.py
│   └── example_task.py
└── workflows/
    ├── __init__.py
    └── main_workflow.py
```

`config_schema.json` 是可选项；启用 UI 扩展时才生成。

## 关键契约

- `module.yaml`
  - 模块清单
  - 运行时模块名、工作流声明、UI 扩展从这里读取
- `__init__.py`
  - 模块根入口
  - Core 最终导入这个文件，而不是读取 wheel 元数据
- `tasks/`
  - 放 `TaskScript`
- `workflows/`
  - 放 `TaskFlow`
- `pyproject.toml`
  - 面向模块开发环境，不等于宿主应用安装清单

## 命名纪律

- 模块目录名、Python 包名、`module.yaml.name` 默认保持一致
- task / workflow 名称使用小写 Python 标识符
- 任何需要 Core 调度的名字，都必须同时校验文件名、注册表名和 `module.yaml` 声明

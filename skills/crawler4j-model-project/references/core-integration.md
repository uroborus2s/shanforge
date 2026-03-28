# Crawler4j Core 集成

## 真实运行链路

当前最稳的模块开发链路：

```text
init-model
-> 在模块项目里补 tasks / workflows / module.yaml / config_schema.json
-> 用 DevLink 接进 Core
-> 在 ATM 中按真实 Job + Strategy 调试
-> 用 zip 做正式安装验收
```

## 调试约束

- DevLink 选择的是包含 `module.yaml` 的目录
- 策略里的 `execution.module` 对应 `module.yaml.name`
- 策略里的 `execution.workflow` 对应 `module.yaml.workflows[*].name`
- 只有解析到 DevLink 模块的作业，ATM 才会显示调试入口

## 发布与安装约束

- 当前正式安装只支持 `zip` 包
- 不要把 `.whl` 当成应用内模块安装格式
- 模块代码最终运行在 `crawler4j` 宿主 Python 环境里
- 模块 `pyproject.toml` 中的第三方依赖不会被宿主自动安装

## 在 Core 仓库里优先阅读的位置

- `crawler4j_sdk/README.md`
- `crawler4j_sdk/cli/commands.py`
- `docs/02-user-guide/module-developer-guide.md`
- `docs/04-project-development/04-design/module-boundaries.md`
- `docs/04-project-development/04-design/api-design.md`

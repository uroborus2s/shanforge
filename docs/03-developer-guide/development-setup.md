# 开发环境

## 1. 开发前准备

- 阅读 [应用开发](./application-development.md)
- 阅读 [技术选型与工程规则](../04-project-development/04-design/technical-selection.md)
- 安装 `uv`
- 确认本地可以提供 `Python 3.14+`
- 确认本地可读取 `skills/`、`docs/` 和 `.factory/memory/`

## 2. 推荐环境初始化

在仓库根目录执行：

```bash
uv python install 3.14
uv sync
```

最小可用性校验：

```bash
uv run pytest -q
python3 skills/skill-creator/scripts/quick_validate.py skills/using-shanforge
python3 skills/skill-creator/scripts/quick_validate.py skills/project-memory
```

## 3. 开发环境原则

- 使用项目当前约定的工具链和规则
- 优先通过 `using-shanforge`、`project-memory` 和正式文档进入上下文
- 在开始编码前，先确认需求与设计基线
- 代码和规则改动后，优先使用 `uv run pytest` 做最小回归；需要时再补 `uv run ruff check .` 与 `uv run mypy`

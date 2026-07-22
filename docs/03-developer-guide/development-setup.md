# 开发环境

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `DOC-DEVELOPMENT-SETUP-001` |
| 正式版本 | `v1.0.0` |
| 来源候选 | `TASK-DESIGN-001-R019` |
| 发布事务 | `DESIGN-RELEASE-TX-R019-G001` |
| 负责人 | `HUMAN_DEVELOPMENT_EXECUTOR` |
| 修改 / 审核 / 批准 | `uroborus` / `uroborus` / `uroborus` |
| 状态 | 已批准并生效 |
| 上游 | `technical-selection`、`quick-start` |
| 下游 | `application-development` |

## 文档职责

- 允许保存：环境准备；依赖；调试；验证命令。
- 禁止保存：密钥原值；机器私有路径；一次性日志。
- 主要读者：开发者、维护者。

## 正式内容

## 1. 开发前准备

- 阅读 [应用开发](./application-development.md)
- 阅读 [技术选型与工程规则](../05-design/technical-selection.md)
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
```

创建或修改 Skill 时，使用 Codex 系统 `skill-creator` 完成结构校验和前向测试；直接运行其 `quick_validate.py` 前，执行环境必须提供 `PyYAML`。仓库不维护重复的 Skill 创建与评估工具链。

## 3. 开发环境原则

- 使用项目当前约定的工具链和规则
- 优先通过 `using-shanforge`、`project-memory` 和正式文档进入上下文
- 在开始编码前，先确认需求与设计基线
- 代码和规则改动后，优先使用 `uv run pytest` 做最小回归；需要时再补 `uv run ruff check .` 与 `uv run mypy`

## 正式版本历史（仅已发布）

| 版本 | 日期 | 变更 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v1.0.0` | 2026-07-18 | 基于 `TASK-DESIGN-001-R019` 正式落档 | `uroborus` | `uroborus` | `uroborus` |

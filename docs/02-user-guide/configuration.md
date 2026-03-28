# 配置说明

## 1. 配置入口

项目级核心配置主要在：

- `AGENTS.md`
- `GEMINI.md`
- `.factory/project.json`
- `.factory/memory/current-state.md`

## 2. 配置原则

- 稳定协作规则写在 `AGENTS.md` / `GEMINI.md`
- 当前阶段、角色、状态写在 `.factory/project.json`
- 易变运行事实写在 `.factory/memory/current-state.md`
- 正式需求、设计和使用说明写在 `docs/`

## 3. 常见配置误区

- 不要把“当天构建失败”“当前依赖缺失”这类临时事实写进顶层协作规则。
- 不要让 `.factory/memory/` 代替正式人类文档。
- 不要只改代码而不更新 `docs/`。

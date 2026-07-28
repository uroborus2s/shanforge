# 山海工枢（shanforge）

山海工枢是一个面向 `Codex` 与 `Gemini CLI` 的 skill-first 软件工厂仓库，用共享 skills、阶段化文档和项目规则来约束 AI 协作式软件交付。

它不是单一模型的“自由发挥式代码生成器”，而是一套把需求、设计、实现、测试、发布、交接和持续维护串起来的工程操作系统。

## 项目特点

- 以 `docs/` 作为人类正式文档入口
- 以 `skills/` 复用方法论、规则和专项能力
- 支持新项目初始化、历史项目纳管、需求设计推进、任务闭环、发布交接和复盘演进
- 同时兼容 `Codex` 与 `Gemini CLI` 的协作场景

## 仓库结构

- `docs/`：项目正式文档、需求、设计、用户指南与追踪矩阵
- `skills/`：可被 AI 直接调用的技能与参考资料
- `scripts/`：仓库级同步入口，不承载软件工厂流程主控
- `config/`：默认配置与项目约束
- `agents/`：协作角色说明
- `workflows/`：专项流程或辅助资料

## 快速开始

### 1. 阅读入口

建议先看以下文档：

1. `docs/01-getting-started/project-overview.md`
2. `docs/04-project-development/01-governance/project-charter.md`
3. `docs/04-project-development/04-design/solution-overview.md`
4. `docs/02-user-guide/user-guide.md`

### 2. 同步共享 skills

如果你希望把仓库内 skills 同步到本地 `Codex`、`Gemini CLI` 和 `Agents`：

```bash
uv run python scripts/sync-codex-skills
```

### 3. 常用入口

在 `Codex` 或 `Gemini CLI` 中工作时，直接用自然语言描述目标。流程路由由 `using-shanforge` 判断，会话恢复由 `project-memory` 处理，具体工作再交给对应 skill。

## 适用场景

- 从创意启动一个新的软件工厂项目
- 将已经存在的历史项目纳入统一工程治理
- 用阶段化文档和工作项管理需求、设计、实现、测试与发布
- 在多人或多 Agent 协作中维持一致的事实来源与执行边界

## 说明

当前版本以 `skill-first` 为主，重点支持本地协作与流程约束；独立 API 平台化能力保留为后续演进方向。

可重复的确定性辅助能力随所属 skill 放在 `skills/<name>/scripts/`。目标项目不需要
安装或调用 Shanforge 源码、Python 包或独立 CLI。

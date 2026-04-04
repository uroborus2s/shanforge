# 技术选型与工程规则

**项目名称：** 山海工枢 / shanforge  
**负责人：** 仓库维护者  
**主要读者：** 架构 | 开发 | 测试 | 维护者  
**上游输入：** PRD | 需求分析 | 风险登记册  
**下游输出：** 架构设计 | 开发实施 | 测试计划  
**最后更新：** 2026-04-03

## 1. 技术画像摘要

- 技术栈：Python 3.14+ 脚本、`uv`、Markdown 文档、JSON 配置、共享 skills、`Codex` / `Gemini CLI`
- 选型目标：在不引入额外平台复杂度的前提下，提供可执行、可追踪、可持续演进的软件工厂工作流。
- 适用范围：当前仓库本身，以及未来由该仓库脚本和规则初始化/维护的软件工厂项目。

## 2. 必装/必选模块

- `scripts/`：承载 `factory-*` 低自由度、可重复、可校验的执行动作。
- `skills/`：承载模型工作方法、约束和专业能力说明。
- `config/software-factory.defaults.json`：承载默认阶段顺序、脚手架目录和全局文档入口。
- `docs/`：承载正式的人类文档。
- `pyproject.toml`：承载 Python 版本、`uv` 依赖管理和开发工具配置的唯一事实源。
- `.python-version`：承载本仓库默认 Python 版本基线。
- `workflows/`：仅保留非项目型的专项流程资料，不再承载软件工厂项目本身的人类正式说明文档。

## 3. 工程规则

- 当前版本坚持 CLI-first，不把 API 平台作为当前阻塞项。
- 仓库级 Python 基线固定为 `Python 3.14+`，统一通过 `uv` 管理 Python 版本、虚拟环境、依赖、锁文件和工具执行。
- 本仓库脚本和测试默认通过 `uv run python ...`、`uv run pytest`、`uv run ruff ...`、`uv run mypy ...` 执行，不再把系统 `python3` 当作主工作流。
- `docs/` 是正式人类文档，`.factory/` 是 AI 记忆和过程控制资产，二者不能互相替代。
- 涉及需求、设计、使用方式或规则入口的改动，应同步更新相关文档与配置。
- 正式文档采用单文件演进，不在目录中制造多个平行版本。
- 文档内的稳定引用统一使用 `REQ-*`、`NFR-*`、`MOD-*`、`API-*`、`TASK-*` 等 ID。
- 项目内 `docs/` 的内容维护由 `document-templates` skill 完成；`docs-stratego` CLI 是唯一正式的文档校验、聚合站点接入、同步、构建和预览入口；`factory-docs-*` 旧处理链不再保留。

## 4. 管理后台/运营侧要求

- 当前项目没有独立 Web 管理后台，管理动作主要通过本地 CLI 和仓库文件完成。
- 维护者应具备修改脚本、skill、配置和文档的能力。
- 维护者应具备使用 `uv` 切换 Python 版本、同步环境和运行本仓库脚本/测试的能力。
- 若未来新增 Web/API 平台，需要补充新的接口契约、部署说明和运维文档。

## 5. 同步要求

- 进入实现或规则变更前必须阅读本文件。
- 技术栈或核心入口变更后，必须同步更新：
  - [系统架构设计](./system-architecture.md)
  - [模块边界文档](./module-boundaries.md)
  - [API 设计文档](./api-design.md)
  - [用户指南](../../02-user-guide/user-guide.md)
  - `config/software-factory.defaults.json`

## 6. 变更记录

| 日期 | 变更内容 | 变更人 |
|---|---|---|
| 2026-03-25 | 初始版本，固化山海工枢的 CLI-first 技术路线与文档治理规则 | Codex |
| 2026-03-25 | 更新 docs-only 文档治理规则，明确 workflows 不再承载项目正式说明 | Codex |
| 2026-03-27 | 将项目名称统一更新为“山海工枢 / shanforge” | Codex |
| 2026-04-03 | 基线切到 Python 3.14+ / uv，并将文档维护流程统一重构为 `document-templates` skill + `docs-stratego` CLI | Codex |

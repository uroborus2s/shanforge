# API 设计文档

**项目名称：** 山海工枢 / shanforge  
**负责人：** 仓库维护者  
**主要读者：** 前后端 | 测试 | 集成方 | 运维  
**上游输入：** PRD | 技术选型 | 系统架构 | 模块边界  
**下游输出：** 接口实现 | 测试用例 | 契约文件  
**最后更新：** 2026-03-27  

## 1. 接口目录

| API ID | 路径/入口 | 方法/类型 | 关联需求 | 说明 |
|---|---|---|---|---|
| `API-001` | `factory-dispatch <action>` | CLI Command | `REQ-003`, `REQ-006` | 统一动作分派入口 |
| `API-002` | `factory-agent-session --project <path>` | CLI Command | `REQ-003`, `REQ-006` | 生成会话卡、推荐阅读和下一步命令 |
| `API-003` | `config/software-factory.defaults.json` | File Contract | `REQ-001`, `REQ-002`, `REQ-004` | 全局默认配置和文档入口合同 |
| `API-004` | `.factory/project.json` | File Contract | `REQ-004`, `REQ-005` | 被管理项目的运行状态合同 |
| `API-005` | `docs/*` | Document Contract | `REQ-001`, `REQ-002`, `REQ-006` | 正式人类文档合同 |
| `API-006` | `factory-dispatch historical-project-onboarding` | CLI Command | `REQ-007` | 历史项目纳管自动化入口，支持 `legacy-onboard` 别名 |
| `API-007` | `scripts/sync-codex-skills` | CLI Command | `REQ-003` | 把仓库内 `skills/` 增量同步到 `~/.codex/skills` 与 `~/.gemini/skills` |

## 2. 设计原则

- 错误契约：CLI 命令应返回可读的失败原因，文档应指向推荐补救动作。
- 认证授权：当前主要依赖本地仓库权限和 CLI 宿主环境，不定义独立鉴权协议。
- 版本策略：当前版本采用单文件演进和兼容更新，避免同时维护多个平行入口。
- 接口边界：当前版本的“API”主要是命令入口和文件契约，不假设存在对外 HTTP API。

## 3. 接口详情

### `API-001` 统一动作分派入口

- 请求：用户提供动作名和必要参数，例如 `init`、`prd-bootstrap`、`design`、`memory`。
- 响应：分派到具体 `factory-*` 脚本，并输出执行结果。
- 校验规则：
  - 动作名称必须在支持列表或别名列表中。
  - 透传参数由目标脚本负责进一步校验。
- 错误处理：
  - 未知动作返回“分派失败：未知动作”。
  - 具体脚本失败时返回对应 stderr 和退出码。

### `API-002` 会话入口生成

- 请求：项目路径、负责人、焦点等参数。
- 响应：生成给模型直接读取的 Agent 会话卡，包含推荐阅读、活跃项、阶段文档就绪度和下一步命令。
- 校验规则：
  - 项目路径必须可解析。
  - 当前阶段和推荐文档来源于项目状态。
- 错误处理：
  - 缺失状态文件或项目锁异常时，应输出明确失败原因。

### `API-003` 全局默认配置合同

- 请求：当前仓库内的配置读取或刷新。
- 响应：返回阶段顺序、共享 skills、脚手架目录和人类文档入口等默认值。
- 校验规则：
  - 所有文档路径必须存在且可读。
  - `human_workflow_docs` 与 `workflow_docs` 应统一指向 `docs/` 下的正式说明文档。
- 错误处理：
  - 配置不合法时，应阻止初始化或规则刷新继续推进。

### `API-004` 项目状态合同

- 请求：被管理项目读取或更新 `.factory/project.json` 与相关摘要。
- 响应：提供当前阶段、角色、技术画像、工作流和最近动作。
- 校验规则：
  - 必须使用标准 JSON 结构。
  - 关键字段缺失时，脚本应报错或回退到安全默认行为。
- 错误处理：
  - 读取失败或结构损坏时，应提示先修复状态文件。

### `API-005` 正式文档合同

- 请求：人类读者或维护者访问 `docs/` 中的正式文档。
- 响应：提供项目定位、需求、设计、用户指南和追踪关系。
- 校验规则：
  - 文档应包含更新时间、目标读者和变更记录。
  - 核心文档应在 `docs/index.md` 中可被发现。
- 错误处理：
  - 文档缺失时，应在索引和追踪矩阵中体现缺口。

### `API-006` 历史项目纳管自动化入口

- 请求：用户提供一个尚未纳入软件工厂的历史项目路径、负责人和纳管目标，可通过 `factory-historical-project-onboarding` 或 `factory-dispatch historical-project-onboarding` 调用。
- 响应：扫描当前真实状态、补齐软件工厂最小骨架，生成基线文档、AI 记忆、`agent-session`、`state-doctor` 和纳管报告。
- 校验规则：
  - 若项目已经存在完整软件工厂骨架，应拒绝再次当作“未纳管历史项目”初始化。
  - 必须先识别代码、配置、现有文档和最新发布结果，再生成纳管基线。
- 错误处理：
  - 项目目录为空时，应提示改用 `factory-init`。
  - 项目已纳管时，应提示改用 `agent-session`、`state-doctor` 等标准维护入口。

### `API-007` 全局 skills 同步入口

- 请求：用户从当前仓库执行 `python3 scripts/sync-codex-skills`，可选指定源目录、Codex 目录、Gemini 目录、冲突前缀与 dry-run。
- 响应：把仓库内 `skills/` 下的每个可见 skill 目录增量软链接到 `~/.codex/skills` 和 `~/.gemini/skills`，并输出逐项同步结果。
- 校验规则：
  - 默认跳过 `.system` 一类隐藏目录，避免覆盖宿主工具保留目录。
  - 若目标目录已有同名项且不是指向当前 skill 的软链接，则回退到 `shanforge-<skill>` 形式的别名。
  - 若目标根目录是损坏的软链接，默认报错；显式传入 `--repair-broken-target-links` 时才允许修复。
- 错误处理：
  - 源目录不存在或不可读时，应直接失败并提示源路径。
  - 若目标目录存在无法自动解决的命名冲突，应保留原有项并返回冲突摘要。

## 4. 契约文件

- 当前已使用的契约：
  - `config/software-factory.defaults.json`
  - `docs/index.md`
  - `docs/04-project-development/03-requirements/prd.md`
  - `docs/04-project-development/04-design/system-architecture.md`
  - `docs/02-user-guide/user-guide.md`
- 入口设计与实现说明：
  - `docs/04-project-development/04-design/historical-project-onboarding-automation.md`
- 未来若引入对外 HTTP API，再补充：
  - `docs/04-project-development/04-design/contracts/api/openapi.yaml`

## 5. 变更记录

| 日期 | 变更内容 | 变更人 |
|---|---|---|
| 2026-03-25 | 初始版本，定义 CLI 命令入口和文件契约接口 | Codex |
| 2026-03-25 | 更新默认文档入口契约，要求相关人类说明文档统一落在 docs/ | Codex |
| 2026-03-26 | 增加历史项目纳管自动化入口 `API-006` 的提案型定义 | Codex |
| 2026-03-26 | 将 `API-006` 更新为已实现 MVP，并登记脚本与别名入口 | Codex |
| 2026-03-27 | 将项目名称统一更新为“山海工枢 / shanforge”，并同步仓库路径 | Codex |
| 2026-03-27 | 增加 `API-007`，支持把仓库内共享 skills 同步到 Codex / Gemini 全局目录 | Codex |

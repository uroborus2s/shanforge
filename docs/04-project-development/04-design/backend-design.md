# 后端设计文档

## 1. 文档目标

说明 `shanforge` 在仓库内如何组织脚本执行、共享核心逻辑、状态持久化和错误处理。

## 2. 当前后端实现结构

### 2.1 命令入口层

`scripts/` 下的 `factory-*` 命令是对外稳定入口，负责：

- 解析参数
- 读取项目根目录
- 调用 `factory_core.py` 中的共享逻辑
- 输出面向人类的检查结果或执行结果

### 2.2 共享核心层

`scripts/factory_core.py` 是当前仓库的核心实现层，负责：

- 文档目录规范与索引生成
- 历史项目 `docs/` 迁移与链接重写
- `.factory` 状态文件读写
- 路径归一化、发布策略更新和校验逻辑
- 不同高层脚本的共享数据结构与公共函数

### 2.3 状态与数据层

当前项目没有传统数据库，状态主要落在仓库文件中：

- 正式人类文档：`docs/`
- 项目运行状态：`.factory/project.json`
- AI 记忆与过程记录：`.factory/memory/`、`.factory/process/`
- 默认配置：`config/software-factory.defaults.json`

### 2.4 错误处理与降级

当前实现优先采用“明确失败，不静默兜底”的策略：

- 目录结构非法时直接在检查输出中报异常
- 迁移目标冲突时拒绝覆盖，除非显式 `--force`
- 旧结构残留时阻断 `docs-index-refresh --check` 并提示先迁移
- 对于已存在的自定义 `index.md`，刷新逻辑保留人工正文，避免误覆盖

### 2.5 可观测性

当前项目的主要观测点不是服务指标，而是：

- `unittest` 回归结果
- `docs-index-refresh --check` 结果
- Markdown 链接与路径重写结果
- 迁移脚本是否正确识别旧结构和新结构

## 3. 推荐表格

| 模块 | 职责 | 输入 | 输出 | 依赖 | 风险点 |
|---|---|---|---|---|---|
| `scripts/factory-*` | 对外 CLI 入口 | 参数、项目路径 | 执行结果、检查结果 | `factory_core.py` | 参数歧义、入口漂移 |
| `scripts/factory_core.py` | 共享核心逻辑 | 仓库文件、配置、文档 | 迁移、刷新、校验结果 | `docs/`、`.factory/` | 路径兼容和覆盖风险 |
| `.factory/*` | 运行状态与记忆 | 命令执行结果 | 状态文件、过程记录 | 项目执行流程 | 状态失真 |
| `docs/*` | 正式事实源 | 需求、设计、发布信息 | 人类可读文档 | 文档维护流程 | 文档与实现脱节 |

## 4. 关联文档

- [系统架构设计](./system-architecture.md)
- [模块边界文档](./module-boundaries.md)
- [API 设计文档](./api-design.md)
- [部署与 CI/CD 设计](./deployment-architecture.md)

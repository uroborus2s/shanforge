---
name: python-uv-project
description: 约束 Python 项目的工程规范与工具链。当项目使用 Python 开发，或用户提到 uv、pyproject.toml、pytest、ruff、mypy、FastAPI、Typer、Django、CLI、服务端、自动化脚本等 Python 工程搭建、重构、评审时使用。统一要求用 uv 管理 Python 版本、虚拟环境、依赖、锁文件和工具运行；Python Bug 的复现、根因和修复流程由 systematic-debugging 或 tdd-workflow 接管，本 skill 只提供 uv 与工具链约束。
---

# Python UV Project

用于统一 Python 项目的工程规则。核心目标不是“能跑就行”，而是把 Python 项目的依赖管理、代码质量、测试和交付动作压到一套稳定的默认工作流里。

## 硬规则

- 统一使用 `uv` 管理 Python 版本、虚拟环境、依赖、锁文件和工具执行。
- 项目以 `pyproject.toml` 为单一配置入口，以 `uv.lock` 为锁文件。
- 不把 `pip install`、`requirements.txt`、`Pipfile`、`poetry.lock`、`conda` 当作主工作流。
- 所有开发工具统一通过 `uv run` 执行。
- 默认质量工具链：
  - `ruff`：格式化与 lint
  - `pytest`：测试
  - `mypy`：类型检查
- 新增或修改的 Python 代码默认补类型标注。
- 不提交 `.venv/`、缓存目录或本地解释器产物。

## 何时激活

- 新建或重构 Python 项目。
- 维护 `pyproject.toml`、`uv.lock`、`src/`、`tests/`、`scripts/`。
- 设计 Python 服务、CLI、自动化任务或库项目结构。
- 评审 Python 项目的依赖管理、测试、格式化、类型检查是否合规。

## 与 Bug 修复流程的边界

遇到 Python Bug、pytest 失败或线上异常时，不由本 skill 单独接管修复流程。根因不明时先用 `systematic-debugging` 复现并定位直接原因、根源原因和证据；根因已清楚且需要写回归测试时由 `tdd-workflow` 推进 Red/Green。修 Bug 时必须先复现并定位根因。本 skill 只约束这些流程中的 Python 工具链：使用 `uv run` 执行测试、lint、类型检查和脚本，维护 `pyproject.toml` / `uv.lock`，并禁止用未验证兜底替代修复。

## 默认项目结构

除非仓库已有稳定约定，否则优先使用：

```text
project/
├── pyproject.toml
├── uv.lock
├── src/
│   └── <package_name>/
├── tests/
├── scripts/
└── .python-version
```

补充约定：

- 业务代码放在 `src/` 下，不把核心模块直接散落在仓库根目录。
- `tests/` 与实现目录分离。
- `scripts/` 只放运维、迁移、数据处理、辅助脚本，仍通过 `uv run` 执行。
- CLI 项目优先用 `[project.scripts]` 暴露入口，不靠 README 手写命令约定。

## 默认工作流

### 新项目

1. 先确认 Python 版本目标，默认 `>=3.11`。
2. 初始化或补齐 `pyproject.toml`。
3. 使用 `uv` 安装和锁定依赖。
4. 建立 `src/`、`tests/`、`scripts/` 结构。
5. 补齐 `ruff`、`pytest`、`mypy` 配置。

常用动作：

```bash
uv python install 3.11
uv venv
uv add <runtime-dependency>
uv add --dev pytest pytest-cov ruff mypy
uv sync
```

### 日常开发

- 加运行时依赖：`uv add <package>`
- 加开发依赖：`uv add --dev <package>`
- 同步环境：`uv sync`
- 跑测试：`uv run pytest`
- 格式化：`uv run ruff format .`
- 检查 lint：`uv run ruff check .`
- 类型检查：`uv run mypy src tests`

### 评审和交付前

至少通过以下检查：

```bash
uv run ruff format --check .
uv run ruff check .
uv run mypy src tests
uv run pytest
```

如果项目不是 `src/` 布局，按实际路径调整，但不要跳过这四类检查。

## 配置规则

- 依赖、工具、项目元数据统一收敛到 `pyproject.toml`。
- `uv.lock` 应提交到仓库。
- `dependency-groups.dev` 用于开发依赖，不把测试工具混入运行时依赖。
- 已有项目如果使用 `hatchling`、`setuptools` 等构建后端，可以保留；`uv` 负责项目管理，不强制替换构建后端。
- 如需对外导出 `requirements.txt`，它只能是派生产物，不能反过来成为事实源。

## 编码规则

- 公共函数、模块边界、数据结构默认补充类型标注。
- 优先使用 `pathlib`、`dataclasses`、`typing`、`contextlib` 等标准库能力。
- 不为一次性方便引入重依赖。
- 异常处理要带上下文，不吞异常。
- 配置统一走环境变量或设置层，不把密钥、令牌、数据库连接串硬编码进仓库。
- I/O、网络、数据库边界应可测试，不把副作用直接塞进核心业务逻辑。
- 修 Bug 时禁止用宽泛 `except Exception`、返回空集合、默认成功、静默跳过、宽松解析或额外 fallback 掩盖根因；只有当降级是既有契约且有测试和观测信号时才允许保留。

## 测试规则

- 默认使用 `pytest`。
- 单元测试与集成测试分层组织。
- 修 Bug 时先补复现测试，再写清楚直接原因、根源原因和证据，然后修造成问题的真实代码路径。
- 防回归测试必须断言根因路径，不只验证兜底输出。
- 对 CLI、HTTP、文件处理这类边界行为，优先测试可观察输出，不测试实现细节。

## 迁移规则

如果接手的 Python 项目当前不是 `uv` 工作流：

1. 先读取现有 `pyproject.toml`、锁文件、CI 和启动脚本。
2. 不直接粗暴删除旧文件；先完成 `uv` 接管，再清理旧入口。
3. 明确哪份文件是当前事实源，再把依赖和工具运行迁到 `uv`。
4. 完成迁移后，删除重复入口，避免 `pip` / `poetry` / `uv` 并存。

## Review Checklist

- 是否仍在用 `pip install` 作为日常项目管理入口。
- 是否缺少 `uv.lock` 或没有提交锁文件。
- 是否把测试、lint、类型检查工具放在运行时依赖里。
- 是否新增了未标注类型的公共接口。
- 是否缺少 `uv run pytest`、`uv run ruff check .`、`uv run mypy ...` 这类标准质量门。
- 是否引入了与现有栈重复的工具，例如同时保留 `black` 和 `ruff format`。
- 是否把 `.venv/`、`.pytest_cache/`、`.mypy_cache/`、`.ruff_cache/` 提交进仓库。

## 按需加载资料

- 需要创建或修正 `pyproject.toml` 时，读取 `references/pyproject.template.toml`。

## 状态回写与失败语义

在 Shanforge work item 中使用时，输出标准状态包：

```text
工作结果：
- work_item: <WORKITEM-ID>
- skill: python-uv-project
- status: ready_for_review | blocked | needs_user_input
- outputs:
  - <changed file path>
- evidence:
  - <uv run pytest / ruff / mypy output summary>
- ledger_event: <event id or none>
- needs:
  - review | verification | user_input | debugging | none
```

`blocked` 用于 `uv` 不可用、项目配置冲突、锁文件无法同步、质量命令失败且根因未解决，或允许文件范围不足以修复工具链事实的情况。

`needs_user_input` 用于 Python 版本、依赖取舍、迁移范围、旧工具链是否保留或外部服务配置必须由用户决定的情况。

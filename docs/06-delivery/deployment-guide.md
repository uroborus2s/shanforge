# 部署手册

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `OPS-DEPLOYMENT-GUIDE-001` |
| 正式版本 | `v3.1.0` |
| 来源候选 | `TASK-DELIVERY-001-R001` |
| 发布事务 | `DELIVERY-RELEASE-TX-R001-G001` |
| 负责人 | `HUMAN_RELEASE_OPERATIONS_LEAD` |
| 修改 / 审核 / 批准 | `AI_EXECUTOR` / 独立 Reviewer / `uroborus` |
| 状态 | 已批准并生效 |
| 上游 | R002 发布说明、技术选型、系统架构 |
| 下游 | 运维手册、环境验证、部署 evidence |

## 1. 当前交付形态

Shanforge 当前是 Python 平台工作区和可装配能力集合，不是已封装的独立线上服务。R002 提供 framework-agnostic 项目状态 API/route、应用服务、领域规则、runtime evaluator/store adapter 和 settings composition；生产 HTTP server、认证入口、生产持久化、镜像、编排和线上监控尚未交付。

因此当前可执行的是“本地环境装配与验证”，不是 staging 或 production 上线。

## 2. 环境前置

| 项目 | 要求 |
|---|---|
| Python | 3.14 或更高 |
| 依赖管理 | `uv` |
| 本地依赖 | sibling `../shanforge-di`，按 `pyproject.toml` editable source 解析 |
| 工作目录 | 仓库根目录 |
| 凭证 | 本地测试不需要生产凭证；禁止把密钥写入仓库 |
| Git | 验证可读取 diff；提交、push 和 PR 需另行授权 |

## 3. 本地安装与验证

```bash
uv sync --locked
UV_CACHE_DIR=/tmp/shanforge-uv-cache uv run pytest -q
UV_CACHE_DIR=/tmp/shanforge-uv-cache uv run ruff check src tests
UV_CACHE_DIR=/tmp/shanforge-uv-cache uv run ruff format --check src tests
UV_CACHE_DIR=/tmp/shanforge-uv-cache uv run mypy src
uv lock --check
git diff --check
```

预期：所有命令 exit 0；pytest failed/skipped/not_run 为 0；静态检查无错误；lock 和 diff 无漂移。若依赖获取因网络或缓存权限失败，先区分环境失败与代码失败，不得把未完成安装写成验证通过。

## 4. 项目状态能力装配

- composition root：`src/settings/composition/`。
- 主服务：唯一 `ProjectStatusService`。
- access 入口：`ProjectStatusAPI` 与 `GET /projects/{project_id}/status` route 声明。
- 会话恢复：`MemoryAPI -> SessionInspectionService`。
- 节点完成：`RuntimeAPI -> ExecutionService`。
- 结构化/文本输出：`ProjectStatusResponse/v4` 与严格十五行 renderer。

route 是框架无关元数据。要部署真实 HTTP 服务，实施方仍需另建受审计的 server adapter、认证/授权接入、配置和健康检查；这些动作不属于本手册当前已完成范围。

## 5. 环境资格

| 环境 | 当前资格 | 说明 |
|---|---|---|
| 开发者本地 | 支持 | 可使用 `uv run` 执行测试和 composition 验证 |
| 隔离测试 | 支持 | 可使用 pytest、SQLite/in-memory fixture 和攻击夹具 |
| staging | 未资格化 | 缺 server adapter、部署配置、外部依赖与监控接入 |
| production | 未资格化 | 缺生产持久化、认证、容量/SLO、备份恢复和发布回滚演练 |

## 6. 失败处理与回滚

1. 安装失败：保留完整 stderr，核对 Python、`uv.lock` 和 sibling dependency，不修改锁文件规避环境问题。
2. 测试或静态门失败：停止交付，按失败测试定位根因；不得用跳过、忽略或宽松兜底冒充通过。
3. 状态接口失败：核对 fixed H、lifecycle binding、permission context、reducer/renderer 唯一性和 composition wiring。
4. 发布后回滚：使用新的受控修复/发布事务绑定现状、目标 hash、验证和 Review；不要执行未授权的破坏性 Git reset。
5. staging/production 失败：当前没有已批准部署事务，必须先建立环境专用计划、回滚对象、凭证边界和人工授权。

## 7. 部署 evidence 最小字段

真实部署发生时，evidence 至少包含环境、制品/commit hash、配置摘要、迁移状态、开始/结束时间、执行者、命令/平台回执、健康检查、监控、回滚点和结果。缺任一关键回执时，状态保持“未证明部署”。

## 正式版本历史（仅已发布）

| 版本 | 日期 | 变更 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v3.0.0` | 2026-07-18 | 基于 R019 正式落档旧本地脚本交付说明 | `uroborus` | `uroborus` | `uroborus` |
| `v3.1.0` | 2026-07-20 | 校准为 R002 Python 平台工作区、本地验证和生产资格边界 | `AI_EXECUTOR` | 独立 Reviewer | `uroborus` |

# 运维手册

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `OPS-RUNBOOK-001` |
| 正式版本 | `v4.0.0` |
| 来源候选 | `SKILL-FIRST-PM-001` |
| 负责人 | `HUMAN_RELEASE_OPERATIONS_LEAD` |
| 修改 / 审核 / 批准 | `uroborus` / `uroborus` / `uroborus` |
| 状态 | 已批准并生效 |
| 上游 | 部署手册、系统架构 |
| 下游 | skill 验证、故障处理和发布证据 |

## 1. 运行边界

Shanforge 没有常驻服务、生产数据库、平台 runtime 或独立 CLI。运维对象是 Git 管理的
skills、文档、同步脚本和测试。目标项目独立拥有自己的源码与 `.factory` 事实。

## 2. 例行验证

重要变更按影响范围运行：

```bash
UV_CACHE_DIR=/tmp/shanforge-uv-cache uv run pytest -q
UV_CACHE_DIR=/tmp/shanforge-uv-cache uv run ruff check skills tests
UV_CACHE_DIR=/tmp/shanforge-uv-cache uv run ruff format --check skills tests
uv lock --check
git diff --check
test ! -d src
```

修改单个 skill 时，额外运行 skill 校验和该 skill 的定向测试。只按真实 exit code 报告；
其他脏工作项造成的失败必须列明，不得为了全绿越界修改。

## 3. PM 快照故障

标准入口：

```bash
python3 <skill-directory>/scripts/project_snapshot.py --project-root <project-root>
```

- receipt `status=failed`：按 `error` 检查项目根、`.factory`、JSON/JSONL、编码和缓存权限。
- `cache_hit=false`：输入或脚本发生变化，已生成新快照。
- 页面异常：删除目标项目 `.factory/cache/site/current/` 后重新运行。
- 路径越界：检查 `.factory` 或 `cache` 是否是指向项目外的符号链接，不得绕过保护。
- 不得回退到 Shanforge 仓库 `src/`、旧 CLI、SQLite 或手工拼装 HTML。

## 4. 恢复与发布

- skills、文档和规则从 Git 历史恢复。
- `.factory/cache/` 是派生物，不备份；从目标项目正式事实重建。
- 本仓变更默认只做本地提交；push、PR、merge 和部署仍需相应授权。
- 仓库不存在服务部署、数据库迁移、密钥轮换或生产回滚操作。

## 正式版本历史

| 版本 | 日期 | 变更内容 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v4.0.0` | 2026-07-29 | 运维边界切换为 skill-first，删除平台 runtime 巡检 | `uroborus` | `uroborus` | `uroborus` |

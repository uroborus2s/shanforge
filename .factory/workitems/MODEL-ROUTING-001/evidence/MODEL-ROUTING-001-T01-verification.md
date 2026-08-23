# MODEL-ROUTING-001-T01 验证证据

- 时间：2026-08-23T10:34:10+08:00
- 候选：T01 本地基线提交前工作区
- 备份：`/tmp/shanforge-model-routing-001-untracked-backup-20260823.tar.gz`

## 结果

| 命令 | Exit code | 结果 |
|---|---:|---|
| `UV_CACHE_DIR=/tmp/shanforge-model-routing-uv-cache uv run pytest -q` | 0 | `228 passed, 4 subtests passed` |
| `UV_CACHE_DIR=/tmp/shanforge-model-routing-uv-cache uv run ruff check .` | 0 | `All checks passed!` |
| `python3 -c 'import json,pathlib; [json.loads(p.read_text()) for p in pathlib.Path(".factory").rglob("*.json")]; [json.loads(line) for p in pathlib.Path(".factory").rglob("*.jsonl") for line in p.read_text().splitlines() if line.strip()]; print("factory JSON/JSONL valid")'` | 0 | `factory JSON/JSONL valid` |
| `git diff --check` | 0 | 无输出 |

## 范围事实

- 旧平台草稿、大型候选、原始执行证据、截图和多轮 review 过程材料已按 PRD 留存规则清理。
- 当前 Git 候选保留正式文档、当前 ledger、必要测试夹具、最小历史契约证据和当前人工 UI Gate 审计集。
- Ruff 根配置排除 `.factory` 和随文档/可视化 skills 分发、使用独立工具链的脚本目录；当前项目 Python 与测试仍由根 Ruff 门覆盖。
- 干净克隆复验必须在 T01 基线提交后执行，未在本证据中提前声明。
- 清理清单、归档哈希和最小恢复校验见
  `.factory/workitems/MODEL-ROUTING-001/evidence/MODEL-ROUTING-001-T01-cleanup-manifest.md`。

## Review 整改后复验

- 时间：2026-08-23T10:45:02+08:00
- 完整 pytest：exit 0，`228 passed, 4 subtests passed`。
- 根 Ruff：exit 0，`All checks passed!`。
- `.factory` JSON/JSONL：exit 0，`factory JSON/JSONL valid`。
- `git diff --check`：exit 0，无输出。

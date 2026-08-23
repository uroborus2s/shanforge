# MODEL-ROUTING-001-T03 集中验证证据

- 时间：2026-08-23T11:02:00+08:00
- 候选基线：`9245946`
- 完成声明范围：T02 模型路由合同与 T03 当前工作区质量候选

## 首轮完整验证

| 命令 | Exit code | 结果 |
|---|---:|---|
| `UV_CACHE_DIR=/tmp/shanforge-model-routing-uv-cache uv run pytest -q` | 1 | `4 failed, 228 passed, 4 subtests passed` |
| `UV_CACHE_DIR=/tmp/shanforge-model-routing-uv-cache uv run ruff check .` | 0 | `All checks passed!` |
| `.factory` JSON/JSONL 解析 | 0 | `factory JSON/JSONL valid` |
| `git diff --check` | 0 | 无输出 |

四项失败均完成根因修正：正式版本快照同步到 v1.5.0；当前事实合并回最多五条；会话快照跟随
ledger 最新 T02；计划路由约束移入共享项目合同区，保持专业前缀冻结。

## 修正后验证

| 命令 | Exit code | 结果 |
|---|---:|---|
| 四项失败回归 + 模型路由合同 | 0 | `8 passed` |
| `UV_CACHE_DIR=/tmp/shanforge-model-routing-uv-cache uv run pytest -q` | 0 | `232 passed, 4 subtests passed` |
| `UV_CACHE_DIR=/tmp/shanforge-model-routing-uv-cache uv run ruff check .` | 0 | `All checks passed!` |
| `.factory` JSON/JSONL 解析 | 0 | `factory JSON/JSONL valid` |
| `git diff --check` | 0 | 无输出 |

## 未运行项与边界

- UI、API、部署和生产测试未运行：本候选只修改 Markdown/YAML 声明合同与静态 Python 合同测试，未包含服务或 UI 运行时。
- 独立 review、精确本地提交和提交后干净克隆复验仍属于后续 Gate，本文未提前声明它们完成。

## 独立评审整改后验证

- 首轮 review：`changes_requested / 86 / C0-I1-M0`；唯一 Important 是关键词存在性测试无法拒绝矛盾路由、
  未授权派发和升级后继续执行。
- 语义决策表测试：Red exit 1，`1 failed`；Green 定向与相邻回归 exit 0，`22 passed`。
- 完整 pytest：exit 0，`233 passed, 4 subtests passed`。
- 根 Ruff：exit 0，`All checks passed!`；JSON/JSONL 与 `git diff --check` 均 exit 0。
- 当前等待同一独立 reviewer 复审；本地提交和干净克隆仍未提前声明完成。

## 独立复审

- 同一 reviewer 新鲜复跑定向 `22 passed`、全量 `233 passed / 4 subtests passed`、Ruff、
  JSON/JSONL、diff check 与三类 mutation probe。
- 结论：`approved / 98 / C0-I0-M0`；原唯一 Important 已关闭。
- 下一 Gate：精确本地提交及提交后干净克隆复验。
